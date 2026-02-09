"""Constants used throughout the application."""

from enum import IntEnum
from typing import Dict, Tuple


class ConversationStates(IntEnum):
    """Conversation states for the bot."""

    PRICE = 0
    COUNTRY = 1
    CODE = 2
    NAME = 3


# Position coordinates for text on the card image (scaled by 3.125)
POSITIONS: Dict[str, Tuple[float, float]] = {
    "الفئة": (300 * 3.125, 492 * 3.125),
    "رمز التفعيل": (150.5 * 3.125, 630 * 3.125),
    "اسم العميل": (300 * 3.125, 780 * 3.125),
    "تاريخ الاصدار": (30 * 3.125, 35 * 3.125),
    "وقت الاصدار": (30 * 3.125, 55 * 3.125),
}


# Keyboard layouts for user interaction
PRICE_KEYBOARD = [["10$", "20$", "25$"], ["50$", "100$"]]
COUNTRY_KEYBOARD = [["USA", "KSA", "UAE"]]


# Messages
MESSAGES = {
    "unauthorized": "🚫 هذا البوت خاص بـ FGGSTORE فقط.",
    "select_price": "📦 اختر قيمة البطاقة:",
    "select_country": "🌍 اختر الدولة:",
    "enter_code": "🔐 أدخل رمز التفعيل:",
    "enter_name": "👤 ما اسم العميل؟",
    "cancelled": "❌ تم إلغاء العملية.",
}
