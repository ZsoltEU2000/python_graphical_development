class UnselectedItemError(Exception):

    def __init__(self, message="No item have been selected!"):
        self.message = message

    def __str__(self):
        return self.message


class FileIsNotTxt(Exception):

    def __init__(self, message="The actual file is not a .txt file!"):
        self.message = message

    def __str__(self):
        return self.message


class ElementIsNotUsable(Exception):

    def __init__(self, message="The actual element can't be used with it's type."):
        self.message = message

    def __str__(self):
        return self.message


class EmptyListError(Exception):

    def __init__(self, message="The list is empty so we can't do anything with it :("):
        self.message = message

    def __str__(self):
        return self.message


class StringToFloat:

    def __init__(self, string):
        self.string = string

    def is_float(self):
        try:
            float(self.string)
        except ValueError:
            return False
        else:
            return True

