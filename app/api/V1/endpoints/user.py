from typing import List

from flask import Blueprint, abort, render_template, request, redirect, url_for
from werkzeug.exceptions import (BadRequest, InternalServerError,
                                 MethodNotAllowed)

from app.models.user import User as UserModel
from app.schemas.user import UserIn, UserOut

user = Blueprint("user", __name__)


@user.route("profile/", methods=["POST"])
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
    """
    if request.method == "POST":
        
        data = {
            "email": request.form.get('email'),
            "github_username": request.form.get('username'),
            # "tags": request.form.get('hashtags')
        }
        
        try:
            user_data = UserIn(**data)
        except ValueError as e:
            raise BadRequest(f"Validation error: {e}")

        user_instance = UserModel()

        try:
            user_dict = user_data.model_dump(exclude_unset=False)
        except ValueError as e:
            raise BadRequest(f"Invalid profile data: {e}")

        try:
            response = user_instance.save(data=user_dict)
        except Exception as e:
            raise InternalServerError(f"Failed to register user: {e}")

        if response.acknowledged:
            return redirect(url_for('user.get_user_profiles'))
        
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
