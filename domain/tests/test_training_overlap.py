from datetime import date, time
from domain.entities.training import Training


def test_overlapping_trainings_return_true():
    training_a = Training(
        id=1, date=date(2026, 7, 20),
        start_time=time(18, 0), end_time=time(19, 0),
        location="Стадион А"
    )
    training_b = Training(
        id=2, date=date(2026, 7, 20),
        start_time=time(18, 30), end_time=time(19, 30),
        location="Стадион Б"
    )

    assert training_a.overlaps_with(training_b) is True

def test_non_overlapping_trainings_return_false():
    training_a = Training(
        id=1, date=date(2026, 7, 20),
        start_time=time(18, 0), end_time=time(19, 0),
        location="Стадион А"
    )
    training_b = Training(
        id=2, date=date(2026, 7, 20),
        start_time=time(19, 0), end_time=time(20, 0),
        location="Стадион Б"
    )

    assert training_a.overlaps_with(training_b) is False

def test_trainings_on_edge_return_false():
    training_a = Training(
        id=1, date=date(2026, 7, 20),
        start_time=time(18, 0), end_time=time(19, 0),
        location="Стадион А"
    )
    training_b = Training(
        id=2, date=date(2026, 7, 20),
        start_time=time(19, 0), end_time=time(20, 0),
        location="Стадион Б"
    )

    assert training_a.overlaps_with(training_b) is False