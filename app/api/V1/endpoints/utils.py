import requests
from pyppeteer import launch


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


async def main(github_username: str):
    """
    Takes a screenshot of a GitHub user's profile page in dark mode.

    This function launches a headless browser using Pyppeteer, navigates to the GitHub profile page
    of the specified user, and takes a screenshot with dark mode enabled. The dark mode is achieved
    by injecting JavaScript code to set the 'data-color-mode' attribute to 'dark'.

    Parameters:
        github_username (str): The GitHub username of the user whose profile page to capture.

    Returns:
        None

    Example:
        >>> asyncio.get_event_loop().run_until_complete(main('mramitdas'))

    Note:
        Ensure that you have Pyppeteer installed (`pip install pyppeteer`) and have the necessary
        dependencies (such as Chromium) available in your environment.
    """
    browser = await launch()
    page = await browser.newPage()

    # Emulate desktop environment
    await page.emulate(
        {
            "viewport": {"width": 1920, "height": 1080},
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
    )

    await page.goto(f"https://github.com/{github_username}")

    # Inject JavaScript code to enable dark mode
    await page.evaluate(
        """
        document.documentElement.setAttribute('data-color-mode', 'dark');
    """
    )

    await page.screenshot(
        {"path": f"{github_username}_dark_mode.png", "fullPage": "true"}
    )
    await browser.close()
