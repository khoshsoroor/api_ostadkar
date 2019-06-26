from infrastructure.errors import BackendError


class CategoryError(BackendError):
    pass


class CategoryListError(CategoryError):
    pass


class CategoryDeletionError(CategoryError):
    pass


class ErrorMessages:
    NoCategoryFound = 'No categories found'
    NoSuchCategory = 'Categories code {} does not exist'
    CategoryListAccessForbidden = 'Empty X-User-Id in header'
    CategoryDeletionForbidden = 'You are not allowed to delete categories'


class ErrorCodes:
    NoService = 10404
    AccessForbidden = 10403
