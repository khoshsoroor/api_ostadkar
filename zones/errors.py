from infrastructure.errors import BackendError


class ZoneError(BackendError):
    pass


class ZoneFoundError(ZoneError):
    pass


class ErrorMessages:
    NoZonesFound = 'No Zones found'


class ErrorCodes:
    NoZonesFound = 20404
