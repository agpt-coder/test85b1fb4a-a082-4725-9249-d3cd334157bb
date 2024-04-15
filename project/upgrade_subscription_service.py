from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpgradeSubscriptionResponse(BaseModel):
    """
    This response model provides the updated subscription details after a successful upgrade operation.
    """

    user_id: str
    subscription_type: prisma.enums.SubscriptionType
    subscription_start_date: datetime
    subscription_end_date: Optional[datetime] = None


async def upgrade_subscription(
    user_id: str, new_subscription_type: prisma.enums.SubscriptionType
) -> UpgradeSubscriptionResponse:
    """
    Endpoint for users to upgrade their subscription level

    Args:
    user_id (str): The unique identifier of the user wishing to upgrade their subscription.
    new_subscription_type (prisma.enums.SubscriptionType): The desired new subscription level the user wishes to upgrade to.

    Returns:
    UpgradeSubscriptionResponse: This response model provides the updated subscription details after a successful upgrade operation.
    """
    current_datetime = datetime.now()
    if new_subscription_type == prisma.enums.SubscriptionType.MONTHLY:
        duration = timedelta(days=30)
    elif new_subscription_type == prisma.enums.SubscriptionType.YEARLY:
        duration = timedelta(days=365)
    else:
        raise ValueError("Unsupported subscription type")
    existing_subscription = await prisma.models.Subscription.prisma().find_first(
        where={"userId": user_id, "type": {"not": prisma.enums.SubscriptionType.FREE}}
    )
    if existing_subscription:
        updated_subscription = await prisma.models.Subscription.prisma().update(
            where={"id": existing_subscription.id},
            data={
                "type": new_subscription_type,
                "startDate": current_datetime,
                "endDate": current_datetime + duration,
            },
        )
    else:
        updated_subscription = await prisma.models.Subscription.prisma().create(
            data={
                "userId": user_id,
                "type": new_subscription_type,
                "startDate": current_datetime,
                "endDate": current_datetime + duration,
            }
        )
    response = UpgradeSubscriptionResponse(
        user_id=user_id,
        subscription_type=new_subscription_type,
        subscription_start_date=updated_subscription.startDate,
        subscription_end_date=updated_subscription.endDate,
    )
    return response
