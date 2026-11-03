"""Service tests for Stage 6 lookup and cancellation, plus booking rules."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def make_session() -> tuple:
    """Create a fresh store, the three services and one patient and
    practitioner.
    """
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)
    patient_service.register_patient('P1', 'Alex Example')
    practitioner_service.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    return (
        data_store,
        patient_service,
        practitioner_service,
        appointment_service,
    )


# Patient lookup


def test_find_patient_returns_the_stored_patient() -> None:
    """A known ID returns the same object that is in the store."""
    data_store, patient_service, _, _ = make_session()
    found = patient_service.find_patient('P1')
    assert found is data_store.find_patient('P1')
    assert found.name == 'Alex Example'


def test_find_patient_trims_the_id() -> None:
    """Spaces around the ID are ignored."""
    _, patient_service, _, _ = make_session()
    assert patient_service.find_patient('  P1  ').patient_id == 'P1'


def test_find_unknown_patient_raises_lookup_error() -> None:
    """A valid ID that is not registered raises LookupError."""
    _, patient_service, _, _ = make_session()
    with pytest.raises(LookupError):
        patient_service.find_patient('P2')


def test_find_patient_is_case_sensitive() -> None:
    """'p1' is a different ID from 'P1'."""
    _, patient_service, _, _ = make_session()
    with pytest.raises(LookupError):
        patient_service.find_patient('p1')


def test_blank_patient_id_lookup_raises_value_error() -> None:
    """A blank ID is invalid input, not an absent patient."""
    _, patient_service, _, _ = make_session()
    with pytest.raises(ValueError):
        patient_service.find_patient('   ')


def test_failed_patient_lookup_does_not_add_a_patient() -> None:
    """Looking up an unknown ID must not create a new record."""
    data_store, patient_service, _, _ = make_session()
    with pytest.raises(LookupError):
        patient_service.find_patient('P2')
    assert len(data_store.list_patients()) == 1


# Practitioner lookup


def test_find_practitioner_returns_the_stored_practitioner() -> None:
    """A known ID returns the same object that is in the store."""
    data_store, _, practitioner_service, _ = make_session()
    found = practitioner_service.find_practitioner('D1')
    assert found is data_store.find_practitioner('D1')
    assert found.specialty == 'General'


def test_find_practitioner_trims_the_id() -> None:
    """Spaces around the ID are ignored."""
    _, _, practitioner_service, _ = make_session()
    assert practitioner_service.find_practitioner(' D1 ').name == (
        'Taylor Example'
    )


def test_find_unknown_practitioner_raises_lookup_error() -> None:
    """A valid ID that is not registered raises LookupError."""
    _, _, practitioner_service, _ = make_session()
    with pytest.raises(LookupError):
        practitioner_service.find_practitioner('D2')


def test_find_practitioner_is_case_sensitive() -> None:
    """'d1' is a different ID from 'D1'."""
    _, _, practitioner_service, _ = make_session()
    with pytest.raises(LookupError):
        practitioner_service.find_practitioner('d1')


def test_blank_practitioner_id_lookup_raises_value_error() -> None:
    """A blank ID is invalid input."""
    _, _, practitioner_service, _ = make_session()
    with pytest.raises(ValueError):
        practitioner_service.find_practitioner('')


# Registration and booking


def test_duplicate_patient_id_with_spaces_keeps_original() -> None:
    """' P1 ' trims to 'P1', so it is a duplicate and is rejected."""
    _, patient_service, _, _ = make_session()
    with pytest.raises(ValueError):
        patient_service.register_patient(' P1 ', 'Someone Else')
    assert patient_service.find_patient('P1').name == 'Alex Example'


def test_booking_unknown_practitioner_stores_nothing() -> None:
    """Booking with an unregistered practitioner raises LookupError."""
    data_store, _, _, appointment_service = make_session()
    with pytest.raises(LookupError):
        appointment_service.book_appointment(
            'A1', 'P1', 'D9', datetime(2026, 10, 1, 9, 0),
        )
    assert data_store.list_appointments() == []


def test_conflict_is_rejected_and_original_is_kept() -> None:
    """Same practitioner at the exact same time is a conflict."""
    data_store, _, _, appointment_service = make_session()
    when = datetime(2026, 10, 1, 9, 0)
    first = appointment_service.book_appointment('A1', 'P1', 'D1', when)
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P1', 'D1', when)
    assert data_store.list_appointments() == [first]


def test_same_practitioner_at_a_different_time_is_allowed() -> None:
    """Only the exact same time counts as a conflict."""
    data_store, _, _, appointment_service = make_session()
    appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0),
    )
    appointment_service.book_appointment(
        'A2', 'P1', 'D1', datetime(2026, 10, 1, 10, 0),
    )
    assert len(data_store.list_appointments()) == 2


def test_cancelled_appointment_frees_the_time_slot() -> None:
    """A cancelled booking does not block a new one at the same time."""
    _, _, _, appointment_service = make_session()
    when = datetime(2026, 10, 1, 9, 0)
    appointment_service.book_appointment('A1', 'P1', 'D1', when)
    appointment_service.cancel_appointment('A1')
    new = appointment_service.book_appointment('A2', 'P1', 'D1', when)
    assert new.status is AppointmentStatus.SCHEDULED


# Cancellation and retained history


def test_cancel_returns_same_appointment_as_cancelled() -> None:
    """Cancelling returns the stored object with CANCELLED status."""
    _, _, _, appointment_service = make_session()
    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0),
    )
    result = appointment_service.cancel_appointment('A1')
    assert result is appointment
    assert result.status is AppointmentStatus.CANCELLED


def test_cancelled_appointment_is_still_stored() -> None:
    """FR-07: the cancelled appointment can still be found and listed."""
    data_store, _, _, appointment_service = make_session()
    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0),
    )
    appointment_service.cancel_appointment('A1')
    assert appointment_service.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]


def test_cancelling_twice_raises_value_error() -> None:
    """A second cancel is rejected and the status stays CANCELLED."""
    _, _, _, appointment_service = make_session()
    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0),
    )
    appointment_service.cancel_appointment('A1')
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert appointment.status is AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled() -> None:
    """Only SCHEDULED can be cancelled; COMPLETED stays COMPLETED."""
    data_store, patient_service, practitioner_service, appointment_service = (
        make_session()
    )
    completed = Appointment(
        'A1',
        patient_service.find_patient('P1'),
        practitioner_service.find_practitioner('D1'),
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert completed.status is AppointmentStatus.COMPLETED


def test_cancel_unknown_appointment_raises_lookup_error() -> None:
    """An unknown ID raises LookupError and other bookings are unchanged."""
    _, _, _, appointment_service = make_session()
    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0),
    )
    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A2')
    assert appointment.status is AppointmentStatus.SCHEDULED


def test_cancel_with_blank_id_raises_value_error() -> None:
    """A blank ID is invalid input."""
    _, _, _, appointment_service = make_session()
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment(' ')


def test_cancel_only_changes_the_chosen_appointment() -> None:
    """Other appointments stay SCHEDULED."""
    _, _, _, appointment_service = make_session()
    appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0),
    )
    other = appointment_service.book_appointment(
        'A2', 'P1', 'D1', datetime(2026, 10, 1, 10, 0),
    )
    appointment_service.cancel_appointment('A1')
    assert other.status is AppointmentStatus.SCHEDULED
