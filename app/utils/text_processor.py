"""Text processing utilities for Arabic text."""

import arabic_reshaper
from bidi.algorithm import get_display


class ArabicTextProcessor:
    """Handles Arabic text reshaping and bidirectional text processing."""

    @staticmethod
    def reshape_text(text: str) -> str:
        """
        Reshape Arabic text for proper display.

        Args:
            text: Input Arabic text

        Returns:
            Reshaped text ready for display
        """
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    @staticmethod
    def reshape_text_with_spaces(text: str) -> str:
        """
        Reshape Arabic text while preserving word boundaries.
        Better for text containing mixed content or special characters.

        Args:
            text: Input Arabic text

        Returns:
            Reshaped text with proper word spacing
        """
        words = text.split()
        reshaped_words = []

        for word in words:
            reshaped = arabic_reshaper.reshape(word)
            displayed = get_display(reshaped)
            reshaped_words.append(displayed)

        return " ".join(reshaped_words[::-1])
