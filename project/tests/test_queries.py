"""Stage 9 tests for the pure appointment query and its named sort key."""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments


def make_appointments() -> list[Appointment]:
    """Return an unsorted list: D1 has A3 (09:00), A2 (09:00, CANCELLED)
    and A1 (08:00, COMPLETED); D2 has A4 (07:00).
    """
    patient = Patient('P1', 'Alex Example')
    taylor = Practitioner('D1', 'Taylor Example', 'General practice')
    jordan = Practitioner('D2', 'Jordan Example', 'Cardiology')
    nine = datetime(2026, 10, 1, 9, 0)
    return [
        Appointment('A3', patient, taylor, nine),
        Appointment('A2', patient, taylor, nine, AppointmentStatus.CANCELLED),
        Appointment(
            'A1',
            patient,
            taylor,
            datetime(2026, 10, 1, 8, 0),
            AppointmentStatus.COMPLETED,
        ),
        Appointment('A4', patient, jordan, datetime(2026, 10, 1, 7, 0)),
    ]


def ids(appointments: list[Appointment]) -> list[str]:
    """Return the appointment IDs in list order."""
    return [appointment.appointment_id for appointment in appointments]


def test_named_key_orders_by_time_then_id() -> None:
    """QRY-03 / FP-02: the key is (date/time, ID) and works with sorted()."""
    appointments = make_appointments()
    assert appointment_sort_key(appointments[0]) == (
        datetime(2026, 10, 1, 9, 0),
        'A3',
    )
    sorted_ids = ids(sorted(appointments, key=appointment_sort_key))
    assert sorted_ids == ['A4', 'A1', 'A2', 'A3']


def test_default_returns_all_statuses_for_one_practitioner_in_order() -> None:
    """QRY-01 / QRY-03: all D1 statuses, no D2, equal times ordered by ID."""
    assert ids(select_appointments(make_appointments(), 'D1')) == [
        'A1',
        'A2',
        'A3',
    ]
    assert ids(select_appointments(make_appointments(), 'D2')) == ['A4']


@pytest.mark.parametrize(
    ('status', 'expected'),
    [
        (AppointmentStatus.SCHEDULED, ['A3']),
        (AppointmentStatus.CANCELLED, ['A2']),
        (AppointmentStatus.COMPLETED, ['A1']),
    ],
)
def test_status_filter(status: AppointmentStatus, expected: list[str]) -> None:
    """QRY-02 / FR-07: each status, including cancelled history, filters."""
    result = select_appointments(make_appointments(), 'D1', status)
    assert ids(result) == expected


def test_no_match_or_empty_source_returns_a_new_empty_list() -> None:
    """QRY-04: no match and an empty source both give a new empty list."""
    assert select_appointments(make_appointments(), 'D9') == []
    source: list[Appointment] = []
    result = select_appointments(source, 'D1')
    assert result == [] and result is not source


def test_source_list_and_appointments_are_unchanged() -> None:
    """FP-01: the source order and every appointment's state stay the same."""
    appointments = make_appointments()
    before = [(a, a.date_time, a.status) for a in appointments]
    select_appointments(appointments, 'D1', AppointmentStatus.SCHEDULED)
    assert [(a, a.date_time, a.status) for a in appointments] == before


def test_result_is_a_fresh_list_of_the_same_objects() -> None:
    """FP-03: a new list each call (even if already sorted), same objects."""
    appointments = sorted(make_appointments(), key=appointment_sort_key)
    first = select_appointments(appointments, 'D1')
    second = select_appointments(appointments, 'D1')
    assert first == second == appointments[1:]
    assert first is not second and first is not appointments
    assert first[0] is appointments[1]