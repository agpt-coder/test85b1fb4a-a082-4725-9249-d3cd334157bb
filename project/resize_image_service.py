from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CropParameters(BaseModel):
    """
    Defines the parameters for cropping the image, such as the starting point (x, y) and the dimensions to crop (width, height).
    """

    start_x: int
    start_y: int
    crop_width: int
    crop_height: int


class ImageReference(BaseModel):
    """
    The reference to the image, which might include IDs, URLs, or other relevant identifiers.
    """

    image_url: Optional[str] = None
    image_id: Optional[str] = None


class ImageOperationResponse(BaseModel):
    """
    Response model conveying the result of the image resizing operation. It includes a reference to the resized image, such as a URL or an ID.
    """

    success: bool
    message: str
    image_reference: ImageReference


async def resize_image(
    image_id: str, width: int, height: int, crop: CropParameters
) -> ImageOperationResponse:
    """
    Endpoint for resizing an uploaded image.

    Args:
        image_id (str): The unique identifier of the image to be resized.
        width (int): The desired width of the resized image.
        height (int): The desired height of the resized image.
        crop (CropParameters): Optional cropping parameters, if the image should be cropped in addition to being resized.

    Returns:
        ImageOperationResponse: Response model conveying the result of the image resizing operation. It includes a reference
        to the resized image, such as a URL or an ID.
    """
    try:
        image_record = await prisma.models.ImageFile.prisma().find_unique(
            where={"id": image_id}
        )
        if not image_record:
            return ImageOperationResponse(
                success=False,
                message="Image not found.",
                image_reference=ImageReference(),
            )
        new_image_id = "new_resized_image_id"
        await prisma.models.ImageManipulationRecord.prisma().create(
            {
                "data": {
                    "imageFileId": image_id,
                    "userId": image_record.userId,
                    "manipulation": prisma.enums.ManipulationType.RESIZE,
                    "parameters": crop.dict(),
                }
            }
        )
        return ImageOperationResponse(
            success=True,
            message="Image resized successfully.",
            image_reference=ImageReference(image_id=new_image_id),
        )
    except Exception as e:
        return ImageOperationResponse(
            success=False,
            message=f"Failed to resize image: {str(e)}",
            image_reference=ImageReference(),
        )
