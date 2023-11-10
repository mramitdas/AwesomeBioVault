from flask import Blueprint, request

user = Blueprint('user', __name__)


@user.route('profile/', methods=['GET', 'POST'])
def get_user_profile():
    if request.method == 'GET':
        return "This is a GET request for the user profile."
    elif request.method == 'POST':
        return "This is a POST request for the user profile."
    else:
        return "Unsupported request method."


@user.route('profiles/', methods=['GET'])
def get_user_profiles():
    return "profiles"
