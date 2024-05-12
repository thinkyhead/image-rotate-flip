"""
InvokeAI Node - Rotate / Flip Image
by Thinkyhead - May 2, 2024
Based on https://github.com/VeyDlin/remove-background-node/blob/master/remove_background.py

nodes / image-rotate-flip / rotate_flip_image.py

This should be a button in the InvokeAI canvas, right?
Now that we have a node that works, it will be easier to make that button.
"""

from typing import Literal
from PIL import Image

from invokeai.invocation_api import (
    BaseInvocation,
    Input,
    InvocationContext,
    invocation,
    InputField,
    ImageField,
    ImageOutput,
)

RotationLiteral = Literal[ "CW 270°", "CW 180°", "CW 90°", "0°", "CCW 90°", "CCW 180°", "CCW 270°" ]

@invocation(
    "Rotate_Image",
    title="Rotate / Flip Image",
    tags=["image", "rotation", "transform", "flip"],
    category="image",
    version="1.0.0",
    use_cache=False,
)

class RotateImageInvocation(BaseInvocation):
    """Rotate and/or Flip an Image"""
    input_image: ImageField = InputField(description="Input image")
    rotation: RotationLiteral = InputField(default="0°", description="Rotation (in degrees)")
    flip_horizontal: bool = InputField(default=False, description="Whether to horizontally flip")
    flip_vertical: bool = InputField(default=False, description="Whether to vertically flip")

    def rotate_image(self, image: Image.Image, rotation: str, flip_horizontal: bool, flip_vertical: bool) -> Image.Image:
        # Convert the rotation to an integer
        parts = rotation.split(' ')
        rot = int(parts[-1][:-1])
        if parts[0] == "CW": rot = 360 - rot

        # Create a new Image with a copy of the input image
        image_out = image.copy()

        # Rotate the image by the specified angle. The new image size will also be rotated.
        if rot > 0: image_out = image_out.rotate(rot, expand=True)

        # Both of these is the same as rotating by 180 degrees
        if flip_horizontal: image_out = image_out.transpose(Image.FLIP_LEFT_RIGHT)
        if flip_vertical: image_out = image_out.transpose(Image.FLIP_TOP_BOTTOM)

        # Return the modified image
        return image_out

    def invoke(self, context: InvocationContext) -> ImageOutput:
        image_in = context.images.get_pil(self.input_image.image_name)
        image_out = self.rotate_image(image_in, self.rotation, self.flip_horizontal, self.flip_vertical)
        image_dto = context.images.save(image=image_out)
        return ImageOutput.build(image_dto)
