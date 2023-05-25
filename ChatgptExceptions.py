"""
Модуль для описания ошибок
"""

from logger_settings import logger

class NoAnswerFromChat(Exception):
    """
    Отсутствие ответа от чата
    """

    def __init__(self, value: str = "No message"):
        self.message = value

    def __str__(self) -> str:
        return f"NoAnswerFromChat: Нет ответа от ChatGpt -> {self.message}"
    
class CantDecodeAnswerFromChat(Exception):
    """
    Ошибка декодирования сообщения
    """

    def __init__(self, value: str = None):
        self.message = value

    def __str__(self) -> str:
        logger.info(self.message)
        return f"NoAnswerFromChat: Ошибка декодирования ответа ChatGpt"