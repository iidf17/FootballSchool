class DomainError(Exception):
    """Базовый класс для всех ошибок бизнес-правил."""


class PlayerAgeNotEligibleError(DomainError):
    pass


class TeamNotFoundError(DomainError):
    pass


class TrainingOverlapError(DomainError):
    pass