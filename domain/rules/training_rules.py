from domain.entities.training import Training


def has_overlap(new_training: Training, existing_trainings: list[Training]) -> bool:
    """Пересекается ли new_training хотя бы с одной из existing_trainings."""
    return any(new_training.overlaps_with(t) for t in existing_trainings)