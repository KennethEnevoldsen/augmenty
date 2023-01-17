from ...util import registry


@registry.keyboards("it_qwerty_v1")
def create_qwerty_it():
    qwerty = {
        "default": [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "'", "ì"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "è", "+"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ò", "à", "ù"],
            ["<", "z", "x", "c", "v", "b", "n", "m", ",", ".", "-"],
        ],
        "shift": [
            ["!", '"', "£", "$", "%", "&", "/", "(", ")", "=", "?", "^"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "é", "*"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "ç", "°", "§"],
            [">", "Z", "X", "C", "V", "B", "N", "M", ";", ":", "_"],
        ],
    }
    return qwerty
