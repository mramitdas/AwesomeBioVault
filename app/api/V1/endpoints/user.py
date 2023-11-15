from typing import List

from flask import Blueprint, abort, redirect, render_template, request, url_for
from werkzeug.exceptions import (
    BadRequest,
    InternalServerError,
    MethodNotAllowed,
    NotFound,
)

from app.models.user import User as UserModel
from app.schemas.user import UserIn, UserOut, UserUpdate, UserSearch

from .utils import fetch_user_info

user = Blueprint("user", __name__)


@user.route("/profile", methods=["POST"])
def save_user_profile():
    """
    Save user profile information.

    Handles the HTTP POST method for saving user profile information. Validates the incoming JSON data against the UserIn schema,
    processes and stores the validated data using the UserModel, and returns a JSON response indicating the success or failure
    of the profile registration.

    Returns:
        dict: A JSON response indicating the status of the profile registration.

    Raises:
        BadRequest: If there is a validation error in the incoming JSON data or the profile data.
        InternalServerError: If there is an error while trying to register the user profile.
        MethodNotAllowed: If the HTTP method is not POST.

    Example:
        To save a user's profile, send a POST request to the /profile endpoint with the required data in the request json.
        The expected data includes 'email' and 'github_username'. Optional data such as 'full_name', 'github_avatar', and 'tags'
        may be retrieved from the GitHub API if the 'github_username' is provided.

    Note:
        The 'tags' field is currently commented out in the data dictionary. Uncomment and modify as needed based on your
        application's requirements.

    TODO:
        - Uncomment the 'tags' field in the data dictionary if needed.
        - Implement handling of GET requests if required.
    """
    if request.method == "POST":
        data = request.json

        response_code, response_data = fetch_user_info(username=data.get("username"))
        if response_code is not None:
            data["full_name"] = response_data.get("name")
            data["github_avatar"] = response_data.get("avatar_url")
        else:
            raise NotFound("Invalid Github username")

        try:
            user_data = UserIn(**data)
        except ValueError as e:
            raise BadRequest(f"Validation error: {e}")

        try:
            user_dict = user_data.model_dump(exclude_unset=False)
        except ValueError as e:
            raise BadRequest(f"Invalid profile data: {e}")

        user_instance = UserModel()
        try:
            response = user_instance.save(data=user_dict)
        except Exception as e:
            raise InternalServerError(f"Failed to register user: {e}")

        if response.acknowledged:
            return {"status": "success", "message": "Profile added successfully"}

        return {"status": "failure", "message": "Profile registration failed"}

    # Handle GET request if needed
    abort(MethodNotAllowed.code, description="Unsupported request method")


@user.route("/", methods=["GET"])
def get_user_profiles() -> List[UserOut]:
    """
    Retrieve a list of users.

    Returns a list of user data in the response.

    This endpoint fetches user data from a data source and returns it as a list
    of UserOut objects, which include user_uuid, full name, email, GitHub profile, GitHub avatar, profile views, and tags.

    Returns:
        List[UserOut]: A list of user data.

    Raises:
        HTTPException (status_code=500): If there is an error while trying to retrieve user data.
        HTTPException (status_code=404): If no users are found.

    Note:
        The response is an HTML document containing the user profiles.

    """
    try:
        user_instance = UserModel()
        user_data = user_instance.get_all()
    except Exception as e:
        raise InternalServerError(f"Failed to retrieve user data: {e}")

    if not user_data:
        raise NotFound("No users found")

    # Serialize the list of user_data using the UserOut schema
    data = [UserOut(**user).model_dump() for user in user_data]

    return render_template("index.html", data=data)


@user.route("/profile/update", methods=["PATCH"])
def update_user_profile():
    """
    Update user profile information.

    Handles the HTTP PATCH method for updating user profile information. Validates the incoming JSON data against the UserUpdate schema,
    processes and stores the validated data using the UserModel, and returns a JSON response indicating the success or failure
    of the profile update.

    Returns:
        dict: A JSON response indicating the status of the profile update.

    Raises:
        BadRequest: If there is a validation error in the incoming JSON data or the user data.
        InternalServerError: If there is an error while trying to retrieve or update the user profile.
        NotFound: If no users are found with the specified username.
        MethodNotAllowed: If the HTTP method is not PATCH.
    """
    if request.method == "PATCH":
        try:
            user_data = UserUpdate(**request.json)
        except ValueError as e:
            raise BadRequest(f"Validation error: {e}")

        user_instance = UserModel()

        try:
            user_dict = user_data.model_dump(exclude_unset=True)
        except ValueError as e:
            raise BadRequest(f"Invalid user data: {e}")

        try:
            user_instance = UserModel()
            user_data = user_instance.get(username=user_dict["github_username"])
        except Exception as e:
            raise InternalServerError(f"Failed to retrieve user data: {e}")

        if user_data is None:
            raise NotFound("No users found")

        try:
            response = user_instance.update(data=user_dict)
        except Exception as e:
            raise InternalServerError(f"Failed to update user: {e}")

        if response.acknowledged:
            return {"status": "success", "message": "User update successful"}
        else:
            return {"status": "failure", "message": "User update failed"}

    # Handle GET request if needed
    abort(MethodNotAllowed.code, description="Unsupported request method")


@user.route("/profile/filter", methods=["POST"])
def filter_user_profile():
    """
    Endpoint for filtering user profiles based on provided criteria.

    This endpoint expects a POST request with JSON data containing criteria for filtering user profiles. It validates the input data using the `UserSearch` model and then attempts to filter user profiles using the `UserModel`.

    Args:
        None (uses request.json): The request payload containing filtering criteria.

    Returns:
        Flask Response: A JSON response containing the filtered user profiles.

    Raises:
        BadRequest: If there is a validation error while creating the `UserSearch` instance or if the provided data is invalid.
        InternalServerError: If there is an error while attempting to filter user profiles.

    Note:
        This endpoint utilizes the `UserSearch` model for input validation and the `UserModel` for filtering user profiles based on the provided criteria.
    """
    if request.method == "POST":
        data = request.json

        try:
            user_data = UserSearch(**data)
        except ValueError as e:
            raise BadRequest(f"Validation error: {e}")

        try:
            user_dict = user_data.model_dump(exclude_unset=False)
        except ValueError as e:
            raise BadRequest(f"Invalid filter parameter: {e}")

        user_instance = UserModel()
        try:
            return user_instance.filter(data=user_dict)
        except Exception as e:
            raise InternalServerError(f"Failed to retriev user data: {e}")
