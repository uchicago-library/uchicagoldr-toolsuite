from uchicagoldr.request import Request, InputType, ChooseBetween, \
    ChooseMultiple, TrueOrFalse, Confirm
from ast import literal_eval


class RequestHandler(object):
    def __init__(self, request):
        assert(isinstance(request, Request))
        self.request = request

    def handle_request(self):
        response = None
        try:
            while not self.request.validate(response):
                if isinstance(self.request, InputType):
                    response = self._handle_inpute_type()
                elif isinstance(self.request, ChooseBetween):
                    response = self._handle_choose_between()
                elif isinstance(self.request, ChooseMultiple):
                    response = self._handle_choose_multiple()
                elif isinstance(self.request, TrueOrFalse):
                    response = self._handle_true_or_false()
                elif isinstance(self.request, Confirm):
                    response = self._handle_confirm()
                else:
                    raise NotImplemented('The request type does not have ' +
                                         'an associated handler.')
        except NotImplemented as e:
            raise e
        return response

    def _handle_true_or_false(self):
        raise NotImplemented('The RequestHandler does not implement ' +
                             'handling for TrueOrFalse style requests.')

    def _handle_input_type(self):
        raise NotImplemented('The RequestHandler does not implement ' +
                             'handling for InputType style requests.')

    def _handle_choose_between(self):
        raise NotImplemented('The RequestHandler does not implement ' +
                             'handling for ChooseBetween style requests.')

    def _handle_choose_multiple(self):
        raise NotImplemented('The RequestHandler does not implement ' +
                             'handling for ChooseMultiple style requests.')

    def _handle_confirm(self):
        raise NotImplemented('The RequestHandler does not implement ' +
                             'handling for ChooseMultiple style requests.')


class CLIRequestHandler(RequestHandler):
    def __init__(self, request):
        RequestHandler.__init__(self, request)

    def _handle_true_or_false(self):
        print(self.request.prompt)
        print(self.request.statement)
        response = input("Response (t/f): ")
        if response == 't':
            response = True
        if response == 'f':
            response = False
        return response

    def _handle_input_type(self):
        print(self.request.prompt)
        response = input("Response: ")
        response = literal_eval(response)
        return response

    def _handle_choose_between(self):
        print(self.request.prompt)
        for i, entry in enumerate(self.request.choices):
            print("{}: {}".format(i, entry))
        print("Please type an index from the above")
        response = input("Selection: ")
        return int(response)

    def _handle_choose_multiple(self):
        print(self.request.prompt)
        for i, entry in enumerate(self.request.choices):
            print("{}: {}".format(i, entry))
        print("Please type indices from the above separated by a space")
        response = input("Selection: ")
        response = response.split(" ")
        int_responses = []
        for entry in response:
            int_responses.append(int(entry))
        return int_responses

    def _handle_confirm(self):
        print(self.request.prompt)
        response = input("Type y to confirm, anything else to reject: ")
        if response.lower() == 'y':
            return True
        else:
            return False