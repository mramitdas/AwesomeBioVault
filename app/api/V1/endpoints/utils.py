import json

import requests


def fetch_user_info(username: str):
    """
    Fetches user information from the GitHub API based on the provided username.

    Args:
        username (str): The GitHub username.

    Returns:
        tuple: A tuple containing the HTTP status code and the user information (dict).

    Example:
        To retrieve information for a GitHub user with the username 'example_user', use the function as follows:

        ```python
        status_code, user_info = fetch_user_info('example_user')
        ```

        The `status_code` represents the HTTP status code of the response, and `user_info` is a dictionary containing
        information about the GitHub user.

    Note:
        The function uses the GitHub API to fetch user information. If the request to the GitHub API fails for any reason,
        the function returns a tuple with `None` as the status code and an empty dictionary.

    TODO:
        - Consider adding more error handling or logging based on your application's requirements.
    """
    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user information: {e}")
        return None, {}
