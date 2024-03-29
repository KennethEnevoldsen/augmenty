from ...util import registry


@registry.keyboards("ru_v1")
def create_ru():
    qwerty = {
        "default": [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
            ["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ"],
            ["ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э", "ё"],
            ["]", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "/"],
        ],
        "shift": [
            ["!", '"', "№", "%", ":", ",", ".", ";", "(", ")", "_", "+"],
            ["Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ъ"],
            ["Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э", "Ё"],
            ["[", "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", "?"],
        ],
    }
    return qwerty
