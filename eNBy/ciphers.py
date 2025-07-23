class caesar:
    @staticmethod
    def encrypt(text: str, shift: int):
        enc = ""
        for char in text:
            if char.isalpha():
                start_ascii = ord("a") if char.islower() else ord("A")
                shifted_char_ascii = (
                    ord(char) - start_ascii + shift
                ) % 26 + start_ascii
                enc += chr(shifted_char_ascii)
            else:
                enc += char
        return enc

    @staticmethod
    def decrypt(text: str, shift: int):
        return caesar.encrypt(text, -shift)


def _getString():
    import random, string

    _string = list(string.ascii_letters + string.digits + string.punctuation)
    random.shuffle(_string)
    return "".join(_string)


if __name__ == "__main__":
    _string = _getString()
    print(_string)
    print(caesar.encrypt(_string, 3))
