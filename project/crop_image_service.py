import os
from datetime import datetime

import prisma
import prisma.models
from PIL import Image
from pydantic import BaseModel


class CropImageResponse(BaseModel):
    """
    Returns information about the cropped image, including a reference or path to the processed image file.
    """

    image_id: str
    cropped_image_path: str
    message: str


async def crop_image(
    image_id: str, x: int, y: int, width: int, height: int
) -> CropImageResponse:
    """
    Endpoint for cropping an uploaded image.

    Args:
        image_id (str): The ID of the image to be cropped, as stored in the database upon upload.
        x (int): The x-coordinate of the top left corner for the crop area.
        y (int): The y-coordinate of the top left corner for the crop area.
        width (int): The width of the crop area starting from the x-coordinate.
        height (int): The height of the crop area starting from the y-coordinate.

    Returns:
        CropImageResponse: Returns information about the cropped image, including a reference or path to the processed image file.
    """
    image_record = await prisma.models.ImageFile.prisma().find_unique(
        where={"id": image_id}
    )
    if not image_record:
        return CropImageResponse(
            image_id=image_id, cropped_image_path="", message="Image not found."
        )
    try:
        img = Image.open(image_record.storagePath)
        cropped_img = img.crop((x, y, x + width, y + height))
        file_root, file_ext = os.path.splitext(image_record.storagePath)
        new_image_path = f"{file_root}_cropped{file_ext}"
        cropped_img.save(new_image_path)
        await prisma.models.ImageManipulationRecord.prisma().create(
            data={
                "imageFileId": image_id,
                "userId": image_record.userId,
                "manipulation": "CROP",
                "parameters": {"x": x, "y": y, "width": width, "height": height},
                "createdAt": datetime.now(),
            }
        )
        return CropImageResponse(
            image_id=image_id,
            cropped_image_path=new_image_path,
            message="Image cropped successfully.",
        )
    except Exception as e:
        return CropImageResponse(
            image_id=image_id,
            cropped_image_path="",
            message=f"Failed to crop image: {str(e)}",
        )
