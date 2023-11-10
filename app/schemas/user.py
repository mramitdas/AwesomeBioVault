from pydantic import BaseModel, EmailStr, constr

from .utils import TimestampMixin, generate_password


class BaseUser(BaseModel):
    """
    Represents the base user model with common attributes.

    Attributes:
        full_name (str): The full name of the user, constrained to 50 characters with leading/trailing whitespaces stripped.
        email (EmailStr, optional): The email address of the user, if provided.
        github_profile (str, optional): The GitHub profile of the user, if provided.

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.

    Examples:
        >>> user_data = {"full_name": "John Doe", "email": "john@example.com", "github_profile": "johndoe"}
        >>> user = BaseUser(**user_data)
        >>> user.full_name
        'John Doe'
        >>> user.email
        'john@example.com'
        >>> user.github_profile
        'johndoe'
    """

    full_name: constr(strip_whitespace=True, max_length=50) | None = None
    email: EmailStr | None = None
    github_profile: str | None = None

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
        password (str): The password associated with the user. Defaults to a randomly generated password.

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.

    Inherits from:
        - TimestampMixin: A mixin class providing timestamp fields (e.g., created_at, updated_at).
        - BaseUser: The base user model with common attributes.

    Note:
        The `check_aadhar_no` validator is applied to the `aadhar_no` field if a value is provided and ensures it is exactly 12 digits long.

    Examples:
        >>> user_data = {"full_name": "John Doe", "email": "john@example.com", "github_profile": "johndoe", "password": "secretpass"}
        >>> user = UserIn(**user_data)
        >>> user.full_name
        'John Doe'
        >>> user.email
        'john@example.com'
        >>> user.github_profile
        'johndoe'
        >>> user.password
        'secretpass'
        >>> user.created_at
        datetime.datetime(...)

    """

    user_uuid: int | None = None
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

    Inherits from:
        BaseUser: The base user model with common attributes.

    Note:
        This class does not introduce additional attributes or behavior beyond what is defined in the `BaseUser` class. It serves as a specialized version of `BaseUser` specifically designed for representing user data in response objects.

    Examples:
        >>> user_data = {"full_name": "John Doe", "email": "john@example.com", "github_profile": "johndoe", "user_uuid": 123}
        >>> user = UserOut(**user_data)
        >>> user.full_name
        'John Doe'
        >>> user.email
        'john@example.com'
        >>> user.github_profile
        'johndoe'
        >>> user.user_uuid
        123

    """

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True
