from configparser import ConfigParser
from dataclasses import dataclass

@dataclass
class Languages:
    base_language: str
    second_languange: str

class Config:
    """
    Класс для получения данных о языках и токенах для chatgpt
    """

    @staticmethod
    def __get_config_object() -> ConfigParser:
        """
        Создание объекта config для получения данных из конфигурационного файла
        Статический метод
        """

        config = ConfigParser()
        config.read("./chatgpt_info/chatgpt_config.cnf")
        return config

    def get_token(self) -> str:
        """
        Получение токена chatgpt
        """

        config = Config.__get_config_object()
        return config["TOKENS"]["token"]

    def get_languages(self) -> Languages:
        config = Config.__get_config_object()
        return Languages(
            config["LANGUAGES"]["base"],
            config["LANGUAGES"]["second"]
        )
    

if __name__ == "__main__":
    cnf = Config()
    Lang = cnf.get_languages()
    print(Lang.second_languange)