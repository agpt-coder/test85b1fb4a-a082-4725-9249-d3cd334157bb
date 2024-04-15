import logging
from contextlib import asynccontextmanager
from typing import Optional

import prisma
import prisma.enums
import project.crop_image_service
import project.login_user_service
import project.logout_user_service
import project.register_user_service
import project.resize_image_service
import project.update_user_profile_service
import project.upgrade_subscription_service
import project.upload_image_service
import project.view_subscription_service
from fastapi import FastAPI, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="test",
    lifespan=lifespan,
    description="Based on the understood requirements and prior information gathered through the interview and search process, the solution involves developing an image processing application. The core functionality of this application includes accepting an image file from the user, resizing the image to fit within specified dimensions and optionally cropping it to maintain the aspect ratio, and finally returning the resized image file to the user. The preferences for supporting PNG and SVG formats are noted, ensuring versatility and scalability in image handling. Maintaining the aspect ratio during resizing is essential for preserving the image's original visual integrity, as highlighted by the user. Additional features such as adjusting brightness and contrast, applying filters, and performing rotation and flipping have been considered to enhance the visual appeal and suitability of images for various contexts.\n\nThe tech stack recommended for this project includes Python as the programming language, known for its robust libraries and frameworks for image processing tasks. The PIL (Python Imaging Library) or its more updated fork, Pillow, will be utilized for the core image manipulation tasks, such as resizing, cropping, and applying additional visual adjustments as per the user's requirements. These libraries offer built-in functions to handle aspect ratio calculations, interpolation methods, and format-specific settings, aligning with the best practices identified during the research phase.\n\nFor the backend API, FastAPI is chosen for its performance and ease of building async APIs that can handle file uploads and processing efficiently. PostgreSQL will serve as the database to manage user sessions or stored images if needed, with Prisma as the ORM for seamless integration and database management. FastAPI's ability to work asynchronously fits well with the potentially resource-intensive nature of image processing, ensuring the application remains responsive.\n\nThe application will provide endpoints allowing users to upload images, specify desired dimensions (and optionally request cropping), and receive the processed image. This setup aims to offer a user-friendly, efficient, and scalable solution to image resizing and manipulation needs.",
)


@app.post("/auth/logout", response_model=project.logout_user_service.LogoutUserResponse)
async def api_post_logout_user(
    auth_token: str,
) -> project.logout_user_service.LogoutUserResponse | Response:
    """
    Endpoint to logout a user, invalidating their current session
    """
    try:
        res = await project.logout_user_service.logout_user(auth_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/update",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    user_id: str,
    email: Optional[str],
    password: Optional[str],
    subscription_type: Optional[str],
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Endpoint for users to update their profile information
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            user_id, email, password, subscription_type
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_user_service.UserLoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.UserLoginResponse | Response:
    """
    Endpoint for user login, providing authentication tokens
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/image/upload", response_model=project.upload_image_service.UploadImageResponse
)
async def api_post_upload_image(
    image: UploadFile, format: Optional[str], user_id: str
) -> project.upload_image_service.UploadImageResponse | Response:
    """
    Endpoint to allow users to upload images
    """
    try:
        res = await project.upload_image_service.upload_image(image, format, user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/subscription/upgrade",
    response_model=project.upgrade_subscription_service.UpgradeSubscriptionResponse,
)
async def api_post_upgrade_subscription(
    user_id: str, new_subscription_type: prisma.enums.SubscriptionType
) -> project.upgrade_subscription_service.UpgradeSubscriptionResponse | Response:
    """
    Endpoint for users to upgrade their subscription level
    """
    try:
        res = await project.upgrade_subscription_service.upgrade_subscription(
            user_id, new_subscription_type
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/subscription/details",
    response_model=project.view_subscription_service.ViewSubscriptionResponse,
)
async def api_get_view_subscription(
    user_id: str,
) -> project.view_subscription_service.ViewSubscriptionResponse | Response:
    """
    Endpoint for users to view their current subscription details
    """
    try:
        res = await project.view_subscription_service.view_subscription(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/image/resize", response_model=project.resize_image_service.ImageOperationResponse
)
async def api_post_resize_image(
    image_id: str,
    width: int,
    height: int,
    crop: project.resize_image_service.CropParameters,
) -> project.resize_image_service.ImageOperationResponse | Response:
    """
    Endpoint for resizing an uploaded image
    """
    try:
        res = await project.resize_image_service.resize_image(
            image_id, width, height, crop
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/register", response_model=project.register_user_service.RegisterUserResponse
)
async def api_post_register_user(
    email: str, username: str, password: str
) -> project.register_user_service.RegisterUserResponse | Response:
    """
    Endpoint to register a new user
    """
    try:
        res = await project.register_user_service.register_user(
            email, username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/image/crop", response_model=project.crop_image_service.CropImageResponse)
async def api_post_crop_image(
    image_id: str, x: int, y: int, width: int, height: int
) -> project.crop_image_service.CropImageResponse | Response:
    """
    Endpoint for cropping an uploaded image
    """
    try:
        res = await project.crop_image_service.crop_image(image_id, x, y, width, height)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
