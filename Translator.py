from chatgpt_config import Config
import re
import requests
import googletrans
from logger_settings import logger
import openai
import ChatgptExceptions

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

    special_symbols = [
        {
            "open": "<<",
            "close": ">>"
        },
        {
            "open": "//",
            "close": "\\"
        },
        {
            "open": '"',
            "close": '"'
        },
        {
            "open": "《",
            "close": "》"
        }
    ]

    def __init__(self):
        self.config = Config()
        openai.api_key = self.config.get_token()

    def __get_chatgpt_answer(self, request: str) -> str:
        """
        Получение ответа от chatgpt
        """

        model_id = "gpt-3.5-turbo"
        gets_answer = False
        tryes = 0
        while tryes < 3:
            try:
                response = openai.ChatCompletion.create(
                model = model_id,
                messages = [
                    {"role": "system", "content": "You are the best translator"},
                    {"role": "user", "content": "<<Переведи на китайский>> переведи на китайский"},
                    {"role": "assistant", "content": '"Переведи на китайский" на китайском языке переводится как "翻译成中文" (fānyì chéng zhōngwén).'},
                    {"role": "user", "content": request}
                ],
                max_tokens = 3000)

                gets_answer = True
                break

            except Exception as ex:
                logger.error(f"Не удалось получить ответ от chatgpt, попытка {tryes + 1}")
                tryes += 1
                exception_from_tryes = ex
        
        del tryes, model_id
        if not gets_answer:
            raise ChatgptExceptions.NoAnswerFromChat(exception_from_tryes)
            
        try:
            return response["choices"][0]["message"]["content"].encode().decode()
        
        except Exception as ex:
            raise ChatgptExceptions.CantDecodeAnswerFromChat(f"{response}\n{ex}")

    def translate_text(self, text: str, lang: str = "zh") -> Text:
        """
        Перевод текста и возвращение объекта Text
        """

        GoogleTranslator = googletrans.Translator(service_urls = ["translate.googleapis.com"])
        cs = ChatGPTTranslator.special_symbols
        fcs = cs[0]

        tfchat = f"translate {fcs['open']}{text}{fcs['close']} to {lang}"
        try:
            chatgpt_answer = self.__get_chatgpt_answer(tfchat)

        except (ChatgptExceptions.CantDecodeAnswerFromChat, ChatgptExceptions.NoAnswerFromChat) as ex:
            logger.error("Не удалось получить ответ от chatgpt")
            logger.error(ex)
            return "Error!"
        
        del fcs
        print(chatgpt_answer)
        re_result = None
        for i in range(len(ChatGPTTranslator.special_symbols)):
            if ChatGPTTranslator.special_symbols[int(i)]["open"] in chatgpt_answer:
                pattern = f'({cs[int(i)]["open"]}.*?{cs[int(i)]["close"]})'
                re_result = re.findall(pattern = pattern, string = chatgpt_answer)

                needs_lang_is = False
                for check_language in re_result:
                    try:
                        ch_lang = GoogleTranslator.detect(check_language).lang
                        if lang in ch_lang:
                            needs_lang_is = True

                    except Exception as ex:
                        logger.error("Не удалось определить язык на моменте проверки")
                        print(ex)
                        return "Error!"
                
                if needs_lang_is:
                    break

                continue

        if re_result is None:
            logger.error(f"Не удалось найти переведенный текст, ответ {chatgpt_answer}")
            return f"Не удалось найти переведенный текст, ответ {chatgpt_answer}"
        
        print(re_result)
        for result in re_result:
            try:
                translated_lang = GoogleTranslator.detect(result).lang
                if lang in translated_lang:
                    for cs_for_replace in cs:
                        result = result.replace(cs_for_replace["open"], "")
                        result = result.replace(cs_for_replace["close"], "")

                    return Text(primordial_text = text, translated_text = result)

            except Exception as ex:
                logger.error(f"Не удалось определить переведенный язык\n{ex}")
                return f"Не удалось определить переведенный язык\n{ex}"

if __name__ == "__main__":
    Trans = ChatGPTTranslator()
    text = Trans.translate_text("你好！你怎么样？", "ru")
    print(text)
