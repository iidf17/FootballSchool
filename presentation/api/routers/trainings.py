from fastapi import APIRouter, Depends, HTTPException
from application.use_cases.create_training import CreateTrainingUseCase
from domain.exceptions import TrainingOverlapError
from presentation.api.dependencies import get_create_training_use_case
from presentation.api.schemas.training_schemas import TrainingCreateSchema, TrainingResponseSchema
from fastapi import APIRouter, Depends, HTTPException
from application.interfaces.training_repository import TrainingRepository
from presentation.api.dependencies import get_training_repository

router = APIRouter(prefix="/trainings", tags=["trainings"])


@router.post("/", response_model=TrainingResponseSchema, status_code=201)
def create_training(
    data: TrainingCreateSchema,
    use_case: CreateTrainingUseCase = Depends(get_create_training_use_case),
):
    try:
        training = use_case.execute(
            training_date=data.date,
            start_time=data.start_time,
            end_time=data.end_time,
            location=data.location,
        )
    except TrainingOverlapError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return training


@router.get("/{training_id}", response_model=TrainingResponseSchema)
def get_training(
    training_id: int,
    repository: TrainingRepository = Depends(get_training_repository),
):
    training = repository.get_by_id(training_id)
    if training is None:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return training


@router.get("/", response_model=list[TrainingResponseSchema])
def list_trainings(
    repository: TrainingRepository = Depends(get_training_repository),
):
    return repository.get_all()