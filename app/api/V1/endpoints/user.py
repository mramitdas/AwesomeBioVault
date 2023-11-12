from typing import List

from flask import Blueprint, abort, request, render_template
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

    Examples:
        >>> POST /profile/
        >>> {
        >>>     "full_name": "John Doe",
        >>>     "email": "john@example.com",
        >>>     "github_profile": "johndoe"
        >>> }
        >>>
        >>> Response:
        >>> {
        >>>     "status": "success",
        >>>     "message": "Profile registration successful",
        >>>     "data": {
        >>>         "full_name": "John Doe",
        >>>         "github_profile": "johndoe"
        >>>     }
        >>> }

    """
    if request.method == "POST":
        try:
            user_data = UserIn(**request.json)
        except ValueError as e:
            raise BadRequest(f"Validation error: {e}")

        user_instance = UserModel()

        try:
            user_dict = user_data.dict(exclude_unset=False)
        except ValueError as e:
            raise BadRequest(f"Invalid profile data: {e}")

        try:
            response = user_instance.save(data=user_dict)
        except Exception as e:
            raise InternalServerError(f"Failed to register user: {e}")

        if response.acknowledged:
            return {
                "status": "success",
                "message": "Profile registration successful",
                "data": {
                    "full_name": user_dict.get("full_name"),
                    "github_profile": user_dict.get("github_profile"),
                },
            }
        return {"status": "failure", "message": "Profile registration failed"}

    # Handle GET request if needed
    abort(MethodNotAllowed.code, description="Unsupported request method")


@user.route("/", methods=["GET"])
def get_user_profiles() -> List[UserOut]:
    """
    Retrieve a list of users.

    Returns a list of user data in the response.

    This endpoint fetches user data from a data source and returns it as a list
    of UserOut objects, which include user user_uuid, full name, and email.

    Returns:
        List[UserOut]: A list of user data.

    Raises:
        HTTPException (status_code=500): If there is an error while trying to retrieve user data.
        HTTPException (status_code=404): If no users are found.

    Examples:
        >>> GET /profiles/
        >>>
        >>> Response:
        >>> [
        >>>     {
        >>>         "user_uuid": 123,
        >>>         "full_name": "John Doe",
        >>>         "email": "john@example.com"
        >>>     },
        >>>     {
        >>>         "user_uuid": 456,
        >>>         "full_name": "Jane Smith",
        >>>         "email": "jane@example.com"
        >>>     }
        >>> ]

    """
    try:
        user_instance = UserModel()
        user_data = user_instance.get_all()
    except Exception as e:
        raise InternalServerError(f"Failed to retrieve user data: {e}")

    if not user_data:
        raise NotFound("No users found")

    # Serialize the list of user_data using the UserOut schema
    data = [UserOut(**user).dict() for user in user_data]
    
    return render_template('index.html')
