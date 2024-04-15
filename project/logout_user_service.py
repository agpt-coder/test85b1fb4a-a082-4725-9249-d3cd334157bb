import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class LogoutUserResponse(BaseModel):
    """
    Response model for a logout request. Indicates whether the logout operation was successful without exposing sensitive information.
    """

    status: str
    message: str


async def logout_user(auth_token: str) -> LogoutUserResponse:
    """
    Endpoint to logout a user, invalidating their current session

    Args:
        auth_token (str): The authentication token provided in the request header used to identify the user's session. This field is expected to be handled by the API's authentication middleware rather than being part of the request body or path parameters.

    Returns:
        LogoutUserResponse: Response model for a logout request. Indicates whether the logout operation was successful without exposing sensitive information.
    """
    session = await prisma.models.SystemEvent.prisma().find_unique(
        where={
            "details": {"path": ["authToken"], "equals": auth_token},
            "type": prisma.enums.EventType.USER_SIGNUP,
        }
    )
    if session is None:
        return LogoutUserResponse(status="Failed", message="Session not found")
    await prisma.models.SystemEvent.prisma().delete(where={"id": session.id})
    return LogoutUserResponse(status="Success", message="Logout successful")
