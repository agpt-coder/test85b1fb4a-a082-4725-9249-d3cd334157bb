from datetime import datetime
from enum import Enum
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ViewSubscriptionResponse(BaseModel):
    """
    Response model containing the subscription details of the requesting user.
    """

    subscription_type: prisma.enums.SubscriptionType
    start_date: datetime
    end_date: Optional[datetime] = None


class SubscriptionType(Enum):
    FREE: str = "FREE"
    MONTHLY: str = "MONTHLY"
    YEARLY: str = "YEARLY"


async def view_subscription(user_id: str) -> ViewSubscriptionResponse:
    """
    Endpoint for users to view their current subscription details

    Args:
    user_id (str): The unique identifier of the user requesting their subscription details.

    Returns:
    ViewSubscriptionResponse: Response model containing the subscription details of the requesting user.
    """
    subscription = await prisma.models.Subscription.prisma().find_first(
        where={"userId": user_id}, order={"startDate": "desc"}
    )
    if not subscription:
        return ViewSubscriptionResponse(
            subscription_type=prisma.enums.SubscriptionType.FREE,
            start_date=datetime.utcnow(),
        )
    return ViewSubscriptionResponse(
        subscription_type=prisma.enums.SubscriptionType(subscription.type),
        start_date=subscription.startDate,
        end_date=subscription.endDate,
    )
