from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    A simple confirmation model indicating the outcome of the user profile update request.
    """

    success: bool
    message: str


async def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


async def update_user_profile(
    user_id: str,
    email: Optional[str],
    password: Optional[str],
    subscription_type: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Endpoint for users to update their profile information

    Args:
    user_id (str): The unique identifier of the user whose profile is to be updated.
    email (Optional[str]): The user's new email address.
    password (Optional[str]): The user's new password. It should be hashed before saving to the database for security reasons.
    subscription_type (Optional[str]): The user's new subscription type if they want to update it.

    Returns:
    UpdateUserProfileResponse: A simple confirmation model indicating the outcome of the user profile update request.
    """
    try:
        update_data = {}
        if email:
            update_data["email"] = email
        if password:
            hashed_password = await hash_password(password)
            update_data["hashedPassword"] = hashed_password
        if subscription_type:
            update_data["role"] = subscription_type.upper()
        user = await prisma.models.User.prisma().update(
            where={"id": user_id}, data=update_data
        )
        return UpdateUserProfileResponse(
            success=True, message="User profile updated successfully."
        )
    except Exception as e:
        return UpdateUserProfileResponse(success=False, message=str(e))
