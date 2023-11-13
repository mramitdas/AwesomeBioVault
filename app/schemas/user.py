from pydantic import BaseModel, EmailStr, constr

from .utils import TimestampMixin, generate_password


class BaseUser(BaseModel):
    """
    Represents the base user model with common attributes.

    Attributes:
        full_name (str): The full name of the user, constrained to 50 characters with leading/trailing whitespaces stripped.
        email (EmailStr, optional): The email address of the user, if provided.
        github_username (Optional[str]): The GitHub username of the user.
        tags (Optional[list]): A list of tags associated with the user.
        profile_views (Optional[int]): The number of profile views for the user.

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.

    Examples:
        >>> user_data = {
        ...     "full_name": "John Doe",
        ...     "email": "john@example.com",
        ...     "github_profile": "johndoe",
        ...     "github_username": "john_doe",
        ...     "tags": ["developer", "python"],
        ...     "profile_views": 100
        ... }
        >>> user = BaseUser(**user_data)
        >>> user.full_name
        'John Doe'
        >>> user.email
        'john@example.com'
        >>> user.github_username
        'john_doe'
        >>> user.tags
        ['developer', 'python']
        >>> user.profile_views
        100
    """

    github_username: str | None = None
    tags: list | None = None
    profile_views: int | None = None

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class UserIn(TimestampMixin, BaseUser):
    """
    Represents a user input model with additional fields and validation.

    Attributes:
        user_uuid (int, optional): The unique identifier for the user, if provided.
        email (EmailStr, optional): The email address of the user, if provided.
        password (str): The password associated with the user. Defaults to a randomly generated password.
        full_name (str): The full name of the user, constrained to 50 characters with leading/trailing whitespaces stripped.
        github_username (Optional[str]): The GitHub username of the user.
        tags (Optional[list]): A list of tags associated with the user.
        profile_views (Optional[int]): The number of profile views for the user.
        created_at (str): The timestamp indicating when the user was created (in the Asia/Kolkata timezone).
        updated_at (str): The timestamp indicating when the user was last updated (in the Asia/Kolkata timezone).

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.

    Inherits from:
        - TimestampMixin: A mixin class providing timestamp fields (e.g., created_at, updated_at).
        - BaseUser: The base user model with common attributes.

    Examples:
        >>> user_data = {
        ...     "full_name": "John Doe",
        ...     "email": "john@example.com",
        ...     "password": "secretpass",
        ...     "user_uuid": 123,
        ...     "github_username": "john_doe",
        ...     "tags": ["developer", "python"],
        ...     "profile_views": 100,
        ...     "created_at": "2023-11-13 || 10:30:45:678",
        ...     "updated_at": "2023-11-13 || 10:30:45:678"
        ... }
        >>> user = UserIn(**user_data)
        >>> user.full_name
        'John Doe'
        >>> user.email
        'john@example.com'
        >>> user.github_username
        'johndoe'
        >>> user.password
        'secretpass'
        >>> user.created_at
        '2023-11-13 || 10:30:45:678'
        >>> user.updated_at
        '2023-11-13 || 10:30:45:678'
        >>> user.profile_views
        100
    """

    user_uuid: int | None = None
    email: EmailStr | None = None
    password: str = generate_password()

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class UserOut(BaseUser):
    """
    Represents a user output model.

    This class inherits attributes and behavior from the `BaseUser` class and is intended to be used for representing user data in output or response objects.

    Attributes:
        user_uuid (int): The unique identifier for the user.
        full_name (Optional[str]): The full name of the user, constrained to a maximum length of 50 characters.
        github_avatar (Optional[str]): The URL of the user's GitHub avatar.
        github_username (Optional[str]): The GitHub username of the user.
        profile_views (Optional[int]): The number of profile views for the user.
        tags (Optional[List[str]]): A list of tags associated with the user.

    Inherits from:
        BaseUser: The base user model with common attributes.

    Note:
        This class serves as a specialized version of `BaseUser` specifically designed for representing user data in response objects. It introduces additional attributes: `full_name`, `github_avatar`, `github_username`, `profile_views`, and `tags`.

    Examples:
        >>> user_data = {
        ...     "full_name": "amit",
        ...     "github_avatar": "https://avatars.githubusercontent.com/u/51442266?v=4",
        ...     "github_username": "mramitdas",
        ...     "profile_views": 1002,
        ...     "tags": ["python", "programming"],
        ...     "user_uuid": 123
        ... }
        >>> user = UserOut(**user_data)
        >>> user.full_name
        'amit'
        >>> user.github_avatar
        'https://avatars.githubusercontent.com/u/51442266?v=4'
        >>> user.github_username
        'mramitdas'
        >>> user.profile_views
        1002
        >>> user.tags
        ['python', 'programming']
        >>> user.user_uuid
        123
    """

    full_name: constr(strip_whitespace=True, max_length=50) | None = None
    github_avatar: str | None = None

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True
