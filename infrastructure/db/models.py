from datetime import date, time, datetime
from sqlalchemy import String, Date, Time, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


training_teams = Table(
    "training_teams",
    Base.metadata,
    Column("training_id", ForeignKey("trainings.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
)


class TeamModel(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    min_age: Mapped[int]
    max_age: Mapped[int]

    trainings: Mapped[list["TrainingModel"]] = relationship(
        secondary=training_teams, back_populates="teams"
    )


class PlayerModel(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[date] = mapped_column(Date)
    position: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="active")
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))


class TrainingModel(Base):
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, index=True) # type: ignore
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    location: Mapped[str] = mapped_column(String(200))

    teams: Mapped[list["TeamModel"]] = relationship(
        secondary=training_teams, back_populates="trainings"
    )

    __table_args__ = (
        CheckConstraint("start_time < end_time", name="check_time_order"),
    )


class AttendanceModel(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"), index=True)
    status: Mapped[str] = mapped_column(String(20))
    marked_at: Mapped[datetime] = mapped_column(DateTime)

    __table_args__ = (
        UniqueConstraint("player_id", "training_id", name="unique_player_training"),
    )
