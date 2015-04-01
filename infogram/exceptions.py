class InfogramPythonError(Exception):
    """ Base exception """

class InfogramError(InfogramPythonError):
    """ Exception for the Infogram API errors """

class AuthenticationError(InfogramError):
    """ Exception for the Infogram API authentication errors """

class InternalServerError(InfogramError):
    """ Exception for Infogram API's internal serer errors """

class HTTPError(InfogramPythonError):
    """ Exception for http errors """
