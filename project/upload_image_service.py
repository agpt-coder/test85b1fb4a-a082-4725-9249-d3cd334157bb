import io
import uuid
from datetime import datetime
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from fastapi import UploadFile
from PIL import Image
from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    """
    Response model indicating the result of the image upload operation, including references to the uploaded image.
    """

    success: bool
    message: str
    image_id: Optional[str] = None
    image_url: Optional[str] = None


async def upload_image(
    image: UploadFile, format: Optional[str], user_id: str
) -> UploadImageResponse:
    """
    Endpoint to allow users to upload images

    Args:
    image (UploadFile): The image file to be uploaded.
    format (Optional[str]): The format of the image being uploaded (e.g., PNG, JPG). This is optional and can be determined from the file if not provided.
    user_id (str): The ID of the user uploading the image, used to associate the image with a user.

    Returns:
    UploadImageResponse: Response model indicating the result of the image upload operation, including references to the uploaded image.
    """
    if format is None:
        format = image.filename.split(".")[-1].upper()
        if format not in ["PNG", "JPG", "JPEG", "SVG"]:
            return UploadImageResponse(
                success=False, message="Unsupported image format"
            )
    try:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        output_format = "PNG" if format != "SVG" else "SVG"
        image_id = str(uuid.uuid4())
        storage_path = f"uploads/{image_id}.{output_format.lower()}"
        pil_image.save(storage_path)
        uploaded_image = await prisma.models.ImageFile.prisma().create(
            data={
                "id": image_id,
                "userId": user_id,
                "format": prisma.enums.ImageFormat[output_format],
                "originalFilename": image.filename,
                "storagePath": storage_path,
                "uploadedAt": datetime.now(),
            }
        )
        return UploadImageResponse(
            success=True,
            message="Image uploaded successfully",
            image_id=image_id,
            image_url=f"/files/{image_id}.{output_format.lower()}",
        )
    except Exception as e:
        return UploadImageResponse(success=False, message=str(e))
