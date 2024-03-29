from ...util import registry


@registry.keyboards("hu_qwerty_v1")
def create_qwerty_hu():
    qwerty = {
        "default": [
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "ö", "ü", "ó"],
            ["q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ő", "ú"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", "é", "á", "ű"],
            ["í", "y", "x", "c", "v", "b", "n", "m", ",", ".", "-"],
        ],
        "shift": [
            ["§", "'", '"', "+", "!", "%", "/", "=", "(", ")", "Ö", "Ü", "Ó"],
            ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "Ő", "Ú"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "É", "Á", "Ű"],
            ["Í", "Y", "X", "C", "V", "B", "N", "M", "?", ":", "_"],
        ],
    }
    return qwerty
