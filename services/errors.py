from infrastructure.errors import BackendError


class ServiceError(BackendError):
    pass


class ServiceListError(ServiceError):
    pass


class ServiceDeletionError(ServiceError):
    pass


class ErrorMessages:
    NoServicesFound = 'No Customers found'
    NoSuchService = 'Customer code {} does not exist'
    ServiceListAccessForbidden = 'Empty X-User-Id in header'
    ServiceDeletionForbidden = 'You are not allowed to delete customers'


class ErrorCodes:
    NoService = 10404
    AccessForbidden = 10403

