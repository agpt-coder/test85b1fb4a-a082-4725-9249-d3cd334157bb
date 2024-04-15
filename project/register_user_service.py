import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    After successful registration, this model returns the newly created user's ID, email, and username. Passwords are not returned for security reasons.
    """

    id: str
    email: str
    username: str


async def register_user(
    email: str, username: str, password: str
) -> RegisterUserResponse:
    """
    Endpoint to register a new user in the database. It checks if the email or username already exists.
    If not, it will hash the password and create a new user entry in the database.

    Args:
        email (str): The email address of the new user. Must be unique and follow standard email formatting rules.
        username (str): The chosen username for the new user. Must be unique across the system.
        password (str): The password for the new user. This will be hashed and stored securely in the database.

    Returns:
        RegisterUserResponse: After successful registration, this model returns the newly created user's ID, email, and username.

    Raises:
        Exception: If the email or username already exists in the database.
    """
    existing_user = await prisma.models.User.prisma().find_first(
        where={"OR": [{"email": email}]}
    )
    if existing_user:
        raise Exception("Email or username is already in use")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "hashedPassword": hashed_password.decode("utf-8")}
    )
    return RegisterUserResponse(id=new_user.id, email=new_user.email, username=username)
