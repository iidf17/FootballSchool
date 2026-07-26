# presentation/api/routers/attendance.py
from fastapi import APIRouter, Depends, HTTPException
from application.use_cases.mark_attendance import MarkAttendanceUseCase, TrainingNotFoundError
from application.dto.attendance_dto import AttendanceMarkRequest
from presentation.api.dependencies import get_mark_attendance_use_case
from presentation.api.schemas.attendance_schemas import AttendanceMarkRequestSchema, AttendanceResponseSchema

router = APIRouter(prefix="/trainings", tags=["attendance"])


@router.post("/{training_id}/attendance", response_model=list[AttendanceResponseSchema], status_code=201)
def mark_attendance(
    training_id: int,
    data: AttendanceMarkRequestSchema,
    use_case: MarkAttendanceUseCase = Depends(get_mark_attendance_use_case),
):
    requests = [
        AttendanceMarkRequest(player_id=item.player_id, status=item.status)
        for item in data.items
    ]

    try:
        result = use_case.execute(training_id=training_id, requests=requests)
    except TrainingNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result