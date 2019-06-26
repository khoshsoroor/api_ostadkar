from infrastructure.errors import BackendError


class ProvideError(BackendError):
    pass


class ProvideFoundError(ProvideError):
    pass


class ErrorMessages:
    NoProvidesFound = 'No Provides found'


class ErrorCodes:
    NoProvidesFound = 20404
