from chatgpt_config import Config
import re
import requests

class Text:
    """
    Класс для переведенных сообщений
    """

    def __init__(self, primordial_text: str, translated_text: str):
        self.primordial_text = primordial_text
        self.translated_text = translated_text

    def __str__(self) -> str:
        return self.translated_text

class ChatGPTTranslator:
    """
    Переводчик для chatgpt
    """

    def __init__(self):
        config = Config()
        self.token = config.get_token()

    def translate_text(self) -> Text:
        """
        Перевод текста и возвращение объекта Text
        """

        ...    