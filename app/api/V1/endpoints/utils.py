import asyncio

import requests
from celery import Celery
from github import Github
from pyppeteer import launch

from app.config.config import Config


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


# Create a Celery instance
app = Celery("tasks", broker=Config.REDIS_SERVER)


async def capture_screenshot(github_username: str):
    """
    Takes a screenshot of a GitHub user's profile page in dark mode and commits it to a GitHub repository.

    This function utilizes Pyppeteer, a headless browser automation library, to capture a screenshot
    of the specified GitHub user's profile page in dark mode. The dark mode is achieved by injecting
    JavaScript code to set the 'data-color-mode' attribute to 'dark'.

    Parameters:
        github_username (str): The GitHub username of the user whose profile page to capture.

    Returns:
        None

    Example:
        >>> asyncio.get_event_loop().run_until_complete(capture_screenshot('mramitdas'))

    Note:
        Ensure that you have Pyppeteer installed (`pip install pyppeteer`) and have the necessary
        dependencies (such as Chromium) available in your environment.

    After capturing the screenshot, the function automatically commits the screenshot image to a
    specified GitHub repository. The GitHub repository and commit details are configured using the
    settings in the `Config` class. Make sure to set the appropriate values in the `Config` class
    before running the function.

    Configuration:
        - GITHUB_TOKEN: GitHub personal access token with the necessary permissions.
        - REPO_OWNER: Owner of the GitHub repository.
        - REPO_NAME: Name of the GitHub repository.
        - BRANCH: Branch to which the screenshot will be committed.

    The committed file will be named '{github_username}.png', and the commit message will indicate
    the addition of the screenshot file.

    Example:
        >>> capture_screenshot('mramitdas')
    """
    browser = await launch(executablePath=Config.PUPPETEER_EXECUTABLE_PATH, args=['--no-sandbox'])
    page = await browser.newPage()

    # Emulate desktop environment
    await page.emulate(
        {
            "viewport": {"width": 1920, "height": 1080},
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
    )

    await page.goto(f"https://github.com/{github_username}", {'waitUntil': 'domcontentloaded'})

    # Inject JavaScript code to enable dark mode
    await page.evaluate(
        """
        document.documentElement.setAttribute('data-color-mode', 'dark');
    """
    )

    await page.screenshot({"path": f"{github_username}.png", "fullPage": "true"})
    await browser.close()

    github_token = Config.GITHUB_TOKEN
    repository_owner = Config.REPO_OWNER
    repository_name = Config.REPO_NAME
    target_branch = Config.BRANCH
    file_path = f"{github_username}.png"
    commit_message = f"CHORE: added {file_path}"

    commit_file_to_github(
        github_token,
        repository_owner,
        repository_name,
        target_branch,
        file_path,
        commit_message,
    )


def commit_file_to_github(
    token, repo_owner, repo_name, branch, file_path, commit_message
):
    """
    Commit a file to a specified GitHub repository and branch.

    Parameters:
        token (str): GitHub personal access token with the necessary permissions.
        repo_owner (str): Owner of the GitHub repository.
        repo_name (str): Name of the GitHub repository.
        branch (str): Branch to which the file will be committed.
        file_path (str): Local path to the file to be committed.
        commit_message (str): Commit message describing the changes.

    Returns:
        None
    """
    # Create a GitHub instance
    g = Github(token)

    # Get the repository
    repo = g.get_repo(f"{repo_owner}/{repo_name}")

    # Read the content of the file
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Specify the path where the file will be saved in the GitHub repository
    github_file_path = f"app/static/profiles/{file_path}"

    # Commit the file to GitHub
    repo.create_file(
        path=github_file_path,
        message=commit_message,
        content=file_content,
        branch=branch,
    )


# Define a Celery task
@app.task
def async_capture_screenshot(username):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(capture_screenshot(username))
