from flask import Blueprint, abort, request
from werkzeug.exceptions import (BadRequest, InternalServerError,
                                 MethodNotAllowed)

from app.models.user import User as UserModel
from app.schemas.user import UserOut

user = Blueprint("user", __name__)


@user.route("profile/", methods=["POST"])
def save_user_profile():
    if request.method == "POST":
        try:
            user_data = UserOut(**request.json)
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


@user.route("profiles/", methods=["GET"])
def get_user_profiles():
    return "profiles"
