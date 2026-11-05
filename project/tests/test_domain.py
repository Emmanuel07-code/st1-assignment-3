"""Domain tests for Patient, Practitioner and Appointment objects."""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


def make_appointment() -> Appointment:
    """Create a fresh SCHEDULED appointment for one test."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    when = datetime(2026, 10, 1, 9, 0)
    return Appointment('A1', patient, practitioner, when)


# Patient and Practitioner


def test_patient_stores_trimmed_values() -> None:
    """Valid patient data is stored without surrounding spaces."""
    patient = Patient(' P1 ', ' Alex Example ')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


def test_blank_patient_id_is_rejected() -> None:
    """An empty patient ID raises ValueError."""
    with pytest.raises(ValueError):
        Patient('', 'Alex Example')


def test_whitespace_only_patient_name_is_rejected() -> None:
    """A name made only of spaces counts as blank."""
    with pytest.raises(ValueError):
        Patient('P1', '   ')


def test_patient_id_cannot_be_changed() -> None:
    """patient_id is read-only."""
    patient = Patient('P1', 'Alex Example')
    with pytest.raises(AttributeError):
        patient.patient_id = 'P2'


def test_practitioner_stores_all_fields() -> None:
    """Valid practitioner data is stored."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'


def test_blank_specialty_is_rejected() -> None:
    """Specialty is a required field."""
    with pytest.raises(ValueError):
        Practitioner('D1', 'Taylor Example', '')


# Appointment construction


def test_new_appointment_starts_scheduled() -> None:
    """A new appointment has SCHEDULED status."""
    appointment = make_appointment()
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.appointment_id == 'A1'


def test_appointment_needs_a_patient_object() -> None:
    """Passing a patient ID string instead of a Patient is rejected."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', practitioner, datetime(2026, 10, 1, 9, 0))


def test_appointment_time_with_seconds_is_rejected() -> None:
    """Times must be whole minutes."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    with pytest.raises(ValueError):
        Appointment(
            'A1', patient, practitioner, datetime(2026, 10, 1, 9, 0, 30),
        )


def test_appointment_time_as_text_is_rejected() -> None:
    """The time must be a datetime, not a string."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, '2026-10-01 09:00')


# Cancellation


def test_cancel_changes_status() -> None:
    """Cancelling a SCHEDULED appointment makes it CANCELLED."""
    appointment = make_appointment()
    appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


def test_repeated_cancellation_is_rejected() -> None:
    """Cancelling twice raises ValueError and the status stays CANCELLED."""
    appointment = make_appointment()
    appointment.cancel()
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled() -> None:
    """A COMPLETED appointment cannot be cancelled."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.COMPLETED


def test_status_cannot_be_set_directly() -> None:
    """Status can only change through cancel()."""
    appointment = make_appointment()
    with pytest.raises(AttributeError):
        appointment.status = AppointmentStatus.CANCELLED
    assert appointment.status is AppointmentStatus.SCHEDULED
