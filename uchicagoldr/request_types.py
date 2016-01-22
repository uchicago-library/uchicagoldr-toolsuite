from collections import Iterable
from os.path import isabs

from uchicagoldr.request import InputType
from uchicagoldr.item import Item


class ProvideNewItemsInstance(InputType):
    def __init__(self):
        self.prompt = "The items you provided were not a list or " + \
            "generator. Please supply a new list or generator of items."
        InputType.__init__(self, Iterable, validator=self._validator,
                           prompt=self.prompt)

    def _validator(self, response):
        return isinstance(response, list) or \
            str(type(response)) == "<class 'generator'>"


class ProvideNewItemInstance(InputType):
    def __init__(self):
        self.prompt = 'The instance you provided is not an item. Please ' + \
            'supply a valid item instance'
        InputType.__init__(self, Item, prompt=self.prompt)


class ProvideNewIndex(InputType):
    def __init__(self, list_len):
        self.list_len = list_len
        self.prompt = "Please provide a new index. " + \
            "The list length is {}".format(str(self.list_len))
        InputType.__init__(self, int, validator=self._validator,
                           prompt=self.prompt)

    def _validator(self, response):
        return bool(response < self.list_len)


class ProvideAbsolutePath(InputType):
    def __init__(self):
        self.prompt = "The path you provided was not absolute. Please " + \
            "provide an absolute path."
        InputType.__init__(self, str, validator=self._validator,
                           prompt=self.prompt)

    def _validator(self, response):
        return isinstance(response, str) and isabs(response)


class ProvideNewRoot(ProvideAbsolutePath):
    def __init__(self):
        self.prompt = 'The root you specified is invalid. Please ' + \
            'provide a valid root path.'
        InputType.__init__(self, str, validator=self._validator,
                           prompt=self.prompt)

class ProvideNewDataPath(ProvideAbsolutePath):
    def __init__(self):
        self.prompt = 'The data path you specified is invalid. Please ' + \
            'provide a valid root path.'
        InputType.__init__(self, str, validator=self._validator,
                           prompt=self.prompt)

class ProvideNewAdminPath(ProvideAbsolutePath):
    def __init__(self):
        self.prompt = 'The admin path you specified is invalid. Please ' + \
            'provide a valid root path.'
        InputType.__init__(self, str, validator=self._validator,
                           prompt=self.prompt)

class ProvideNewArk(InputType):
    def __init__(self):
        self.prompt = "The ark you provided is not valid. " + \
            "Please provide a new one."
        InputType.__init__(self, str, validator=self._ark_validation,
                           prompt=self.prompt)



class MissingSourceDirectory(InputType):
    def __init__(self):
        self.prompt = "the source directory you entered does not exist."
        InputType.__init__(self, str, validator=self._ark_validation,
                           prompt=self.prompt)


class MissingDestinationDirectory(InputType):
    def __init__(self):
        self.prompt = "the destination directory you entered does not exist."
        InputType.__init__(self, str, validator=self._ark_validation,
                           prompt=self.prompt)


class CollissionProblem(InputType):
    def __init__(self, collisions):
        self.prompt = "there was a collision between the " + \
            "following files".format(', '.join(collisions))
        InputType.__init__(self, str, validator=self._ark_validation,
                           prompt=self.prompt)
