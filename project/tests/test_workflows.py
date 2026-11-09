"""Stage 9 workflow tests: one store and one set of services used
together, the same way the console menu uses them.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def make_session() -> tuple:
    """Create one store and the three services, with patient P1 and
    practitioners D1 and D2 registered.
    """
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)
    patient_service.register_patient('P1', 'Alex Example')
    practitioner_service.register_practitioner(
        'D1', 'Taylor Example', 'General',
    )
    practitioner_service.register_practitioner(
        'D2', 'Jordan Example', 'Cardiology',
    )
    return data_store, patient_service, appointment_service


def ids(appointments: list) -> list[str]:
    """Return just the appointment IDs, to make the asserts easy to read."""
    return [appointment.appointment_id for appointment in appointments]


def test_full_booking_workflow() -> None:
    """UI-01: book, reject a conflict, allow another practitioner,
    cancel, keep history, filter and book the freed slot.
    """
    data_store, _, appointment_service = make_session()
    nine = datetime(2026, 10, 1, 9, 0)

    appointment_service.book_appointment('A1', 'P1', 'D1', nine)

    # Same practitioner, same time: rejected and nothing new is stored.
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P1', 'D1', nine)
    assert ids(data_store.list_appointments()) == ['A1']

    # A different practitioner at the same time is allowed (AC-04.2).
    appointment_service.book_appointment('A2', 'P1', 'D2', nine)

    # Cancelling keeps the appointment (FR-07).
    appointment_service.cancel_appointment('A1')
    a1 = appointment_service.find_appointment('A1')
    assert a1.status is AppointmentStatus.CANCELLED

    # Listing: all statuses by default, then only SCHEDULED.
    assert ids(appointment_service.list_practitioner_appointments('D1')) == ['A1']
    scheduled = appointment_service.list_practitioner_appointments(
        'D1', AppointmentStatus.SCHEDULED,
    )
    assert scheduled == []

    # The freed slot can be booked again.
    appointment_service.book_appointment('A3', 'P1', 'D1', nine)
    assert ids(appointment_service.list_practitioner_appointments('D1')) == [
        'A1',
        'A3',
    ]


def test_rejected_requests_do_not_change_stored_records() -> None:
    """UI-02: duplicate and unknown IDs are rejected and the stored
    records stay the same.
    """
    data_store, patient_service, appointment_service = make_session()
    nine = datetime(2026, 10, 1, 9, 0)

    # Duplicate patient ID: rejected, the original patient is kept.
    original = data_store.find_patient('P1')
    with pytest.raises(ValueError):
        patient_service.register_patient('P1', 'Someone Else')
    assert data_store.find_patient('P1') is original

    # Unknown patient: rejected, and the ID A1 is not reserved.
    with pytest.raises(LookupError):
        appointment_service.book_appointment('A1', 'P9', 'D1', nine)
    assert data_store.list_appointments() == []
    appointment_service.book_appointment('A1', 'P1', 'D1', nine)
    assert ids(data_store.list_appointments()) == ['A1']

    # Unknown appointment and unknown practitioner listing.
    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A9')
    with pytest.raises(LookupError):
        appointment_service.list_practitioner_appointments('D9')


def test_repeated_cancellation_and_invalid_status_are_rejected() -> None:
    """A second cancel and a text status are rejected; A1 stays
    CANCELLED and is still listed.
    """
    _, _, appointment_service = make_session()
    appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0),
    )
    appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments('D1', 'pending')

    a1 = appointment_service.find_appointment('A1')
    assert a1.status is AppointmentStatus.CANCELLED
    assert ids(appointment_service.list_practitioner_appointments('D1')) == ['A1']
