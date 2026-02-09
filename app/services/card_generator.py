"""Service for generating PlayStation card images."""

import logging
from pathlib import Path
from typing import Dict, Tuple

from PIL import Image, ImageDraw, ImageFont

from app.config import settings
from app.utils import POSITIONS, ArabicTextProcessor

logger = logging.getLogger(__name__)


class CardGeneratorService:
    """Handles the generation of PlayStation card images with custom data."""

    def __init__(self):
        """Initialize the card generator service."""
        self.template_path = settings.TEMPLATE_PATH
        self.font_path = settings.FONT_PATH
        self.base_font_size = settings.BASE_FONT_SIZE
        self.small_font_size = settings.SMALL_FONT_SIZE
        self.text_processor = ArabicTextProcessor()

    def generate_card(self, card_data: Dict[str, str], output_path: Path) -> None:
        """
        Generate a PlayStation card image with the provided data.

        Args:
            card_data: Dictionary containing card information
            output_path: Path where the generated card will be saved

        Raises:
            FileNotFoundError: If template or font files are not found
            Exception: If image generation fails
        """
        try:
            # Open and prepare the base image
            image = Image.open(self.template_path).convert("RGBA")
            txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            # Load fonts
            font = ImageFont.truetype(str(self.font_path), self.base_font_size)
            small_font = ImageFont.truetype(str(self.font_path), self.small_font_size)

            # Draw each field on the card
            for key, value in card_data.items():
                position = POSITIONS.get(key)
                if not position:
                    continue

                if key == "رمز التفعيل":
                    self._draw_activation_code(draw, value, position, image.width)
                elif key in ["تاريخ الاصدار", "وقت الاصدار"]:
                    self._draw_datetime_field(draw, value, position, small_font)
                else:
                    self._draw_centered_field(draw, value, position, font, image.width, key)

            # Combine layers and save
            combined = Image.alpha_composite(image, txt_layer)
            combined.save(output_path)
            logger.info(f"Card generated successfully: {output_path}")

        except FileNotFoundError as e:
            logger.error(f"Required file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating card: {e}")
            raise

    def _draw_activation_code(
        self, draw: ImageDraw.ImageDraw, code: str, position: Tuple[float, float], image_width: int
    ) -> None:
        """
        Draw the activation code with dynamic font sizing to fit the box.

        Args:
            draw: ImageDraw object
            code: Activation code text
            position: Position to draw the code
            image_width: Width of the image
        """
        box_width = 320 * settings.SCALE_FACTOR
        box_height = 70 * settings.SCALE_FACTOR
        box_x = int((image_width - box_width) / 2)
        box_y = int(position[1])

        # Find the optimal font size
        current_font_size = settings.CODE_MAX_FONT_SIZE
        while current_font_size >= settings.CODE_MIN_FONT_SIZE:
            test_font = ImageFont.truetype(str(self.font_path), current_font_size)
            bbox = draw.textbbox((0, 0), code, font=test_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if text_width <= box_width and text_height <= box_height:
                break
            current_font_size -= 1

        # Draw the code centered in the box
        final_font = ImageFont.truetype(str(self.font_path), current_font_size)
        text_width = draw.textlength(code, font=final_font)
        text_height = final_font.getbbox(code)[3]

        x_text = box_x + (box_width - text_width) / 2
        y_text = box_y + (box_height - text_height) / 2

        draw.text((x_text, y_text), code, font=final_font, fill=(255, 255, 255, 255))

    def _draw_datetime_field(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        position: Tuple[float, float],
        font: ImageFont.FreeTypeFont,
    ) -> None:
        """
        Draw date or time fields (small font, white color).

        Args:
            draw: ImageDraw object
            text: Text to draw
            position: Position to draw the text
            font: Font to use
        """
        draw.text(position, text, font=font, fill=(255, 255, 255, 255))

    def _draw_centered_field(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        position: Tuple[float, float],
        font: ImageFont.FreeTypeFont,
        image_width: int,
        field_name: str,
    ) -> None:
        """
        Draw a centered text field with proper Arabic text processing.

        Args:
            draw: ImageDraw object
            text: Text to draw
            position: Position to draw the text
            font: Font to use
            image_width: Width of the image
            field_name: Name of the field (for special processing)
        """
        # Process Arabic text
        if field_name == "اسم العميل" and "يا" in text:
            processed_text = self.text_processor.reshape_text_with_spaces(text)
        else:
            processed_text = self.text_processor.reshape_text(text)

        # Center the text
        bbox = draw.textbbox((0, 0), processed_text, font=font)
        text_width = bbox[2] - bbox[0]
        x_center = (image_width - text_width) / 2
        y = position[1] + 5

        draw.text((x_center, y), processed_text, font=font, fill=(255, 255, 255, 255))
