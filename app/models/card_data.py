"""Data models for PlayStation card information."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CardPrice(str, Enum):
    """Available PlayStation card prices."""

    TEN = "10$"
    TWENTY = "20$"
    TWENTY_FIVE = "25$"
    FIFTY = "50$"
    HUNDRED = "100$"


class Country(str, Enum):
    """Available countries for PlayStation cards."""

    USA = "USA"
    KSA = "KSA"
    UAE = "UAE"


@dataclass
class CardData:
    """Data structure for PlayStation card information."""

    price: str
    country: str
    activation_code: str
    customer_name: str
    issue_date: str
    issue_time: str

    @property
    def category(self) -> str:
        """Get the formatted category (price + country)."""
        return f"{self.price} {self.country}"

    @property
    def formatted_name(self) -> str:
        """Get the formatted customer name with Arabic prefix."""
        return f"يا {self.customer_name}"

    def to_dict(self) -> dict:
        """Convert card data to dictionary for image generation."""
        return {
            "الفئة": self.category,
            "رمز التفعيل": self.activation_code,
            "اسم العميل": self.formatted_name,
            "تاريخ الاصدار": self.issue_date,
            "وقت الاصدار": self.issue_time,
        }

    @staticmethod
    def format_activation_code(code: str) -> str:
        """
        Format activation code to XXXX-XXXX-XXXX format.

        Args:
            code: Raw activation code input

        Returns:
            Formatted activation code
        """
        # If already properly formatted, return as is
        if code.count("-") == 2 and all(len(part) == 4 for part in code.split("-")):
            return code.upper()

        # Remove spaces and dashes, then reformat
        raw_code = code.replace(" ", "").replace("-", "").upper()
        formatted_parts = [raw_code[i : i + 4] for i in range(0, min(len(raw_code), 12), 4)]
        return "-".join(formatted_parts)
