from fastapi import APIRouter, Depends, HTTPException
from application.interfaces.player_repository import PlayerRepository
from application.use_cases.create_player import CreatePlayerUseCase
from presentation.api.dependencies import get_create_player_use_case, get_player_repository
from presentation.api.schemas.player_schemas import PlayerCreateSchema, PlayerResponseSchema
from domain.exceptions import PlayerAgeNotEligibleError

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/", response_model=PlayerResponseSchema, status_code=201)
def create_player(
    data: PlayerCreateSchema,
    use_case: CreatePlayerUseCase = Depends(get_create_player_use_case),
):
    try:
        player = use_case.execute(
            first_name=data.first_name,
            last_name=data.last_name,
            birth_date=data.birth_date,
            position=data.position,
            season_start_date=data.season_start_date
        )
    except PlayerAgeNotEligibleError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    return player

@router.get("/{player_id}", response_model=PlayerResponseSchema)
def get_player(
    player_id: int,
    repository: PlayerRepository = Depends(get_player_repository),
):
    player = repository.get_by_id(player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден")
    return player


@router.get("/", response_model=list[PlayerResponseSchema])
def list_players(
    repository: PlayerRepository = Depends(get_player_repository),
):
    return repository.get_all()