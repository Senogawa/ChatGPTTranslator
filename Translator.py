from chatgpt_config import Config
import re
import requests
import googletrans

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
        }
    ]

    def __init__(self):
        config = Config()
        self.token = config.get_token()

    def translate_text(self, text: str, test_chatgpt_answer: str, lang: str = "zh") -> Text:
        """
        Перевод текста и возвращение объекта Text
        """

        GoogleTranslator = googletrans.Translator(service_urls = ["translate.googleapis.com"])
        cs = ChatGPTTranslator.special_symbols
        fcs = cs[0]

        tfchat = f"translate {fcs['open']}{text}{fcs['close']} to {lang}" #TODO пока не используется
        del fcs

        re_result = None
        for i in range(len(ChatGPTTranslator.special_symbols)):
            if ChatGPTTranslator.special_symbols[int(i)]["open"] in test_chatgpt_answer: #TODO заменить на ответ chatgpt
                pattern = f'({cs[int(i)]["open"]}.*?{cs[int(i)]["close"]})'
                #print(pattern)
                re_result = re.findall(pattern = pattern, string = test_chatgpt_answer)
                for k in range(len(re_result)):
                    re_result[int(k)] = re_result[int(k)].replace(cs[i]["open"], "").replace(cs[i]["close"], "")
                break

        if re_result is None:
            return f"Не удалось найти переведенный текст, ответ {test_chatgpt_answer}"
        
        print(re_result)
        for result in re_result:
            try:
                translated_lang = GoogleTranslator.detect(result).lang
                if lang in translated_lang:
                    return Text(primordial_text = text, translated_text = result)

            except Exception as ex:
                return f"Не удалось определить переведенный язык\n{ex}"

    def retranslate_text(self) -> Text:
        """
        Обратный перевод сообщений в текст
        """

        ...


if __name__ == "__main__":
    Trans = ChatGPTTranslator()
    print(Trans.translate_text("Переведи на китайский", '"Переведи на китайский" на китайском языке можно сказать "翻译成中文" (fānyì chéng zhōngwén).'))