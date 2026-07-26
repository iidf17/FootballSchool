from fastapi import FastAPI
from presentation.api.routers import attendance, players, trainings

app = FastAPI(title="Football School API")

app.include_router(trainings.router)
app.include_router(attendance.router)
app.include_router(players.router)