"""Stage 8 regression tests for defects F8-01 and F8-02."""

from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


def make_store_with_one_appointment() -> tuple:
    """Create a store with one patient, one practitioner and one
    SCHEDULED appointment A1 with D1 at 09:00 on 1 October 2026.
    """
    data_store = SmartCareDataStore()
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    data_store.add_patient(patient)
    data_store.add_practitioner(practitioner)
    when = datetime(2026, 10, 1, 9, 0)
    appointment = Appointment('A1', patient, practitioner, when)
    data_store.add_appointment(appointment)
    return data_store, appointment, when


def test_f8_01_same_practitioner_same_time_is_a_conflict() -> None:
    """F8-01: a SCHEDULED appointment for the same practitioner at the
    same time must count as a conflict.
    """
    data_store, _, when = make_store_with_one_appointment()
    assert data_store.has_practitioner_conflict('D1', when) is True


def test_f8_02_cancelled_appointment_can_still_be_found() -> None:
    """F8-02: a cancelled appointment is kept and can still be found
    by its ID.
    """
    data_store, appointment, _ = make_store_with_one_appointment()
    appointment.cancel()
    found = data_store.find_appointment('A1')
    assert found is appointment
    assert found.status is AppointmentStatus.CANCELLED
