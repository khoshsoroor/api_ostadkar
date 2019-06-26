from infrastructure.errors import BackendError


class SkillError(BackendError):
    pass


class SkillFoundError(SkillError):
    pass


class ErrorMessages:
    NoSkillsFound = 'No Skills found'


class ErrorCodes:
    NoSkillsFound = 20404
