# Stage 7 Testing and Verification Record

> **TEAM TO COMPLETE — status note (remove when the record is done)**
> `project/tests/test_domain.py` was added and `project/tests/test_services.py` extended. TEST IDs, the traceability matrix (B–G), the human-first Copilot design (H, I), regression counts at your own SHA (J), review/contribution evidence (L, M) and quiz answers (N) are left blank for your group. Assign your own TEST IDs and record results you actually observe.


Group/tutorial: Group 4, tutorial [complete]  Members/cohorts: Emmanuel Cadman (Emmanuel07-code, UG); Tanveer Uppal (TanveerUppal, UG); Tanzir Ahon (Tanzir1718, UG)
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register patient P1, "Alex Example", with an unused ID. | Register P1 again with a different name (duplicate ID), or register with a blank name. | Positive: find_patient("P1") is the returned patient and the name matches. Negative: ValueError is raised and the original P1 is still stored, unchanged. |
| FR-05 Prevent practitioner conflict | Book A2 with practitioner D1 at 2026-10-11 11:00 when D1 already has A1 at 10:00 (a different time), or book a different practitioner at 10:00. | Book A2 with D1 at 2026-10-11 10:00 while A1 with D1 at 10:00 is still SCHEDULED. | Positive: both appointments are stored. Negative: ValueError is raised and only A1 is stored. |
| FR-06 Cancel appointment | Cancel A1 while it is SCHEDULED. | Cancel A1 again after it is already cancelled; separately, cancel an unknown ID such as A99. | Positive: the same A1 object is returned with status CANCELLED. Negative: a repeated cancel raises ValueError and A1 stays CANCELLED; an unknown ID raises LookupError. |
| FR-07 Retain cancelled history | Cancel A1, then look it up and list all appointments. | Try to cancel A1 a second time; the failed operation must not remove or replace it. | find_appointment("A1") is the same object, it still appears in list_appointments(), and its status is CANCELLED after the failed attempt. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: It is always true, whether the code works or is completely broken. It never fails, so it cannot detect any bug and proves no behaviour at all.

`assert appointment is not None`
Judgement: Weak/unclear  Why: It only shows that something was returned. If the function returns the wrong appointment, wrong data or a replacement object, this still passes, so it does not prove identity, status or retained history.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: It checks the exact required state after cancellation (FR-06, AC-05.1), so it fails if cancel() does not change the status. Limit: on its own it does not prove the appointment is still stored (FR-07) or that the same object was returned.

`assert len(results) > 0`
Judgement: Weak/unclear  Why: It only checks that the list has at least one item. If the results are wrong, incomplete or contain the wrong appointments, it still passes, as long as the list is not empty.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: It checks object identity: the store returns the exact same appointment object, not a copy or replacement. That supports retained history (FR-07, AC-05.2) and lookup (AC-06.1). Limit: it does not check the appointment's status.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract:

| Input / state | Expected result | Supporting contract |
|---|---|---|
| Blank or whitespace-only identifier, e.g. Patient("   ", "Alex Example") or find_patient("   ") | ValueError; nothing is stored | IDs are trimmed and must be non-blank. Without characters there is no way to identify the record. A blank ID is invalid input, not an absent record, so it is ValueError, not LookupError. |
| Whitespace-only name, e.g. Patient("P1", "   ") | ValueError; nothing is stored | Required text fields are trimmed and must be non-blank. A name with no characters is treated as missing. |
| Same practitioner, exact same datetime, where the existing appointment is CANCELLED | Allowed: the new booking is stored as SCHEDULED | A conflict needs the same practitioner, the exact same time and an existing SCHEDULED appointment. A cancelled appointment frees the slot. |
| Same practitioner, exact same datetime, where the existing appointment is SCHEDULED | ValueError; only the original is stored | This is the exact conflict boundary (FR-05, AC-04.1). |
| Cancelling an appointment that is already CANCELLED | ValueError; status stays CANCELLED | Only SCHEDULED appointments may be cancelled (FR-06, AC-05.3). |
| Cancelling a COMPLETED appointment | ValueError; status stays COMPLETED | Only SCHEDULED appointments may be cancelled. It is like trying to return food you have already eaten: the appointment has already happened. |

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Only asserts the patient is not None, which is too weak. It would still pass if the wrong patient, or a newly created replacement, was returned. | Register P1, then assert find_patient("P1") is the same registered patient object and its name is correct (FR-02, AC-02.1). |
| 2 | Only asserts the appointment is not None, which is also too weak. It would pass for the wrong appointment or the wrong status. | Book A1, then assert find_appointment("A1") is the booked object, linked to the registered patient and practitioner, with status SCHEDULED (FR-04, AC-03.1; FR-08, AC-06.1). |
| 3 | Asserts True, which can never fail, so it proves nothing about the code. | Check one specific observable outcome instead, for example that a duplicate patient ID raises ValueError and the original patient is unchanged (FR-01, AC-01.2). |
| 4 | Tests SMS on booking, but SmartCare has no notification feature. The test invents a requirement, and the handout says not to invent notification rules. | Test real booking behaviour instead: the booked appointment is stored with status SCHEDULED and can be found by its ID (FR-04, AC-03.1). |
| 5 | Tests SMS on cancellation instead of the actual cancellation logic. It invents a requirement that does not exist. | Test real cancellation instead: the same appointment object is returned, its status is CANCELLED, and it can still be found (FR-06, AC-05.1; FR-07, AC-05.2). |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
Coverage only shows which lines ran during the tests, not whether anything was checked. Tests can run every line of code with weak checks such as assert True, without verifying that the code works correctly. Coverage also cannot show a missing requirement or a missing case, such as a forgotten boundary, so 100% coverage can still leave wrong behaviour undetected.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

Note: TEST IDs T-01 to T-37 identify our student-authored tests and T-38 to T-45 the eight supplied tests in tests/test_starter.py. They are evidence labels, not new requirements. Results are from python -m pytest run from project/ (45 passed); see J for the run on merged main.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | AC-01.1 (partial domain evidence only; storage through the service is checked by supplied T-39) | T-01 | Unit | test_patient_stores_trimmed_values (tests/test_domain.py) | patient_id == "P1", name == "Alex Example" | Passed | Student-authored |
| FR-01 | Contract: "IDs are trimmed, non-blank" (not AC-01.2) | T-02 | Unit | test_blank_patient_id_is_rejected (tests/test_domain.py) | ValueError | Passed | Student-authored |
| FR-01 | Contract: required text is trimmed and non-blank | T-03 | Unit | test_whitespace_only_patient_name_is_rejected (tests/test_domain.py) | ValueError | Passed | Student-authored |
| FR-01 | Contract: "Properties provide read-only identity" | T-04 | Unit | test_patient_id_cannot_be_changed (tests/test_domain.py) | AttributeError on assignment | Passed | Student-authored |
| FR-03 | Partial domain evidence for practitioner registration | T-05 | Unit | test_practitioner_stores_all_fields (tests/test_domain.py) | ID, name and specialty match | Passed | Student-authored |
| FR-03 | Contract: specialty is required text | T-06 | Unit | test_blank_specialty_is_rejected (tests/test_domain.py) | ValueError | Passed | Student-authored |
| FR-04 | AC-03.1 (partial domain evidence only) | T-07 | Unit | test_new_appointment_starts_scheduled (tests/test_domain.py) | status is SCHEDULED, ID is "A1" | Passed | Student-authored |
| FR-04 | Contract: appointments link actual Patient objects | T-08 | Unit | test_appointment_needs_a_patient_object (tests/test_domain.py) | ValueError | Passed | Student-authored |
| FR-04 | Contract: local datetime at minute precision | T-09 | Unit | test_appointment_time_with_seconds_is_rejected (tests/test_domain.py) | ValueError | Passed | Student-authored |
| FR-04 | Contract: date/time must be a datetime value | T-10 | Unit | test_appointment_time_as_text_is_rejected (tests/test_domain.py) | ValueError | Passed | Student-authored |
| FR-06 | AC-05.1 | T-11 | Unit | test_cancel_changes_status (tests/test_domain.py) | status is CANCELLED | Passed | Student-authored |
| FR-06 | AC-05.3 | T-12 | Unit | test_repeated_cancellation_is_rejected (tests/test_domain.py) | ValueError; status stays CANCELLED | Passed | Student-authored |
| FR-06 | Contract: only SCHEDULED may be cancelled | T-13 | Unit | test_completed_appointment_cannot_be_cancelled (tests/test_domain.py) | ValueError; status stays COMPLETED | Passed | Student-authored |
| FR-06 | Contract: state changes only through domain methods | T-14 | Unit | test_status_cannot_be_set_directly (tests/test_domain.py) | AttributeError; status stays SCHEDULED | Passed | Student-authored |
| FR-02 | AC-02.1 | T-15 | Service | test_find_patient_returns_the_stored_patient (tests/test_services.py) | found is the stored patient; name matches | Passed | Student-authored |
| FR-02 | AC-02.1 + contract: IDs are trimmed | T-16 | Service | test_find_patient_trims_the_id (tests/test_services.py) | patient_id == "P1" | Passed | Student-authored |
| FR-02 | AC-02.2 | T-17 | Service | test_find_unknown_patient_raises_lookup_error (tests/test_services.py) | LookupError | Passed | Student-authored |
| FR-02 | AC-02.2 + contract: IDs are case-sensitive | T-18 | Service | test_find_patient_is_case_sensitive (tests/test_services.py) | LookupError | Passed | Student-authored |
| FR-02 | Contract: blank ID is invalid input (ValueError) | T-19 | Service | test_blank_patient_id_lookup_raises_value_error (tests/test_services.py) | ValueError | Passed | Student-authored |
| FR-02 | Contract: lookup must not create a replacement | T-20 | Service | test_failed_patient_lookup_does_not_add_a_patient (tests/test_services.py) | LookupError; still 1 patient stored | Passed | Student-authored |
| FR-03 (supporting lookup) | Contract: returns the actual stored practitioner | T-21 | Service | test_find_practitioner_returns_the_stored_practitioner (tests/test_services.py) | found is the stored practitioner; specialty matches | Passed | Student-authored |
| FR-03 (supporting lookup) | Contract: IDs are trimmed | T-22 | Service | test_find_practitioner_trims_the_id (tests/test_services.py) | name matches | Passed | Student-authored |
| FR-03 (supporting lookup) | Contract: absent ID raises LookupError | T-23 | Service | test_find_unknown_practitioner_raises_lookup_error (tests/test_services.py) | LookupError | Passed | Student-authored |
| FR-03 (supporting lookup) | Contract: IDs are case-sensitive | T-24 | Service | test_find_practitioner_is_case_sensitive (tests/test_services.py) | LookupError | Passed | Student-authored |
| FR-03 (supporting lookup) | Contract: blank ID is invalid input | T-25 | Service | test_blank_practitioner_id_lookup_raises_value_error (tests/test_services.py) | ValueError | Passed | Student-authored |
| FR-01 | AC-01.2 | T-26 | Service | test_duplicate_patient_id_with_spaces_keeps_original (tests/test_services.py) | ValueError; original name kept | Passed | Student-authored |
| FR-04 | AC-03.2 | T-27 | Service | test_booking_unknown_practitioner_stores_nothing (tests/test_services.py) | LookupError; no appointments stored | Passed | Student-authored |
| FR-05 | AC-04.1 | T-28 | Service | test_conflict_is_rejected_and_original_is_kept (tests/test_services.py) | ValueError; only the first appointment stored | Passed | Student-authored |
| FR-05 | Contract: conflict needs the exact same datetime | T-29 | Service | test_same_practitioner_at_a_different_time_is_allowed (tests/test_services.py) | 2 appointments stored | Passed | Student-authored |
| FR-05 | Contract: conflict needs an existing SCHEDULED appointment | T-30 | Service | test_cancelled_appointment_frees_the_time_slot (tests/test_services.py) | New booking is SCHEDULED | Passed | Student-authored |
| FR-06 | AC-05.1 | T-31 | Service | test_cancel_returns_same_appointment_as_cancelled (tests/test_services.py) | result is the booked appointment; status CANCELLED | Passed | Student-authored |
| FR-07, FR-08 | AC-05.2, AC-06.1 | T-32 | Service | test_cancelled_appointment_is_still_stored (tests/test_services.py) | find_appointment("A1") is the object; list == [appointment] | Passed | Student-authored |
| FR-06 | AC-05.3 | T-33 | Service | test_cancelling_twice_raises_value_error (tests/test_services.py) | ValueError; status stays CANCELLED | Passed | Student-authored |
| FR-06 | Contract: only SCHEDULED may be cancelled | T-34 | Service | test_completed_appointment_cannot_be_cancelled (tests/test_services.py) | ValueError; status stays COMPLETED | Passed | Student-authored |
| FR-06 | Contract: unknown ID raises LookupError at the service | T-35 | Service | test_cancel_unknown_appointment_raises_lookup_error (tests/test_services.py) | LookupError; A1 still SCHEDULED | Passed | Student-authored |
| FR-06 | Contract: blank ID is invalid input | T-36 | Service | test_cancel_with_blank_id_raises_value_error (tests/test_services.py) | ValueError | Passed | Student-authored |
| FR-06 | AC-05.1 | T-37 | Service | test_cancel_only_changes_the_chosen_appointment (tests/test_services.py) | other appointment stays SCHEDULED | Passed | Student-authored |
| FR-01, FR-03 | Contract: required fields | T-38 | Unit | test_required_fields (tests/test_starter.py) | ValueError | Passed | Supplied |
| FR-01, FR-04, FR-08 | AC-01.1, AC-03.1, AC-06.1 | T-39 | Service | test_registration_and_booking (tests/test_starter.py) | find_appointment is the booked object; status SCHEDULED | Passed | Supplied |
| FR-01 | AC-01.2 | T-40 | Service | test_duplicate_patient_preserves_original (tests/test_starter.py) | ValueError; original kept | Passed | Supplied |
| FR-03 | Contract: duplicate practitioner ID rejected | T-41 | Service | test_duplicate_practitioner_preserves_original (tests/test_starter.py) | ValueError; original kept | Passed | Supplied |
| FR-04 | Contract: duplicate appointment ID rejected | T-42 | Service | test_duplicate_appointment_preserves_original (tests/test_starter.py) | ValueError; original kept | Passed | Supplied |
| FR-04 | AC-03.2 | T-43 | Service | test_unregistered_participants_rejected (tests/test_starter.py) | LookupError / ValueError; nothing stored | Passed | Supplied |
| FR-05 | AC-04.1, AC-04.2 | T-44 | Service | test_conflict_rule_and_different_practitioner (tests/test_starter.py) | ValueError; D2 booking succeeds | Passed | Supplied |
| FR-06, FR-07 | AC-05.1, AC-05.3 | T-45 | Unit | test_domain_cancellation_and_guard (tests/test_starter.py) | CANCELLED; ValueError on repeat | Passed | Supplied |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| T-01 | FR-01 | AC-01.1 (partial domain evidence only; storage through the service is checked by supplied T-39) | Positive | Valid patient data is kept with spaces trimmed | patient_id == "P1", name == "Alex Example" | Shows trimming of both fields, which the supplied tests do not check |
| T-02 | FR-01 | Contract: "IDs are trimmed, non-blank" (not AC-01.2) | Negative | A blank patient ID is invalid | ValueError | Keeps the reference intention "blank patient ID rejected"; supplied test only uses a space |
| T-03 | FR-01 | Contract: required text is trimmed and non-blank | Boundary | A name made only of spaces counts as blank | ValueError | Boundary between blank and valid text for names |
| T-04 | FR-01 | Contract: "Properties provide read-only identity" | Negative | Identity cannot be reassigned | AttributeError on assignment | Not covered by supplied tests |
| T-05 | FR-03 | Partial domain evidence for practitioner registration | Positive | Valid practitioner fields are stored | ID, name and specialty match | Checks specialty value, not only rejection |
| T-06 | FR-03 | Contract: specialty is required text | Negative | Specialty is required | ValueError | Overlaps the supplied check, kept as a focused unit test |
| T-07 | FR-04 | AC-03.1 (partial domain evidence only) | Positive | A new appointment starts SCHEDULED | status is SCHEDULED, ID is "A1" | Keeps the reference intention "new appointment starts SCHEDULED" |
| T-08 | FR-04 | Contract: appointments link actual Patient objects | Negative | A patient ID string is not accepted as a Patient | ValueError | Invalid participant type is not in supplied tests |
| T-09 | FR-04 | Contract: local datetime at minute precision | Boundary | Seconds are not allowed | ValueError | Precision boundary not in supplied tests |
| T-10 | FR-04 | Contract: date/time must be a datetime value | Negative | Text dates are rejected by the domain | ValueError | Invalid type for date/time |
| T-11 | FR-06 | AC-05.1 | Positive | Cancelling SCHEDULED makes it CANCELLED | status is CANCELLED | Keeps the reference intention "cancellation changes status" |
| T-12 | FR-06 | AC-05.3 | Negative | A second cancel is rejected without change | ValueError; status stays CANCELLED | Keeps the reference intention "repeated cancellation rejected" |
| T-13 | FR-06 | Contract: only SCHEDULED may be cancelled | Negative | COMPLETED cannot be cancelled | ValueError; status stays COMPLETED | Illegal transition from COMPLETED is not in supplied tests |
| T-14 | FR-06 | Contract: state changes only through domain methods | Negative | Status cannot be assigned directly | AttributeError; status stays SCHEDULED | Protects the guarded transition |
| T-15 | FR-02 | AC-02.1 | Positive | Known lookup returns the stored object | found is the stored patient; name matches | Stage 6 target: identity, not only "not None" |
| T-16 | FR-02 | AC-02.1 + contract: IDs are trimmed | Boundary | Padded ID finds the patient | patient_id == "P1" | Trimming at the service boundary |
| T-17 | FR-02 | AC-02.2 | Negative | Unknown valid ID reports absence | LookupError | Stage 6 target: absence is LookupError, not None |
| T-18 | FR-02 | AC-02.2 + contract: IDs are case-sensitive | Boundary | "p1" is not "P1" | LookupError | Case-sensitivity boundary |
| T-19 | FR-02 | Contract: blank ID is invalid input (ValueError) | Negative | Blank ID is invalid, not absent | ValueError | Separates invalid from absent |
| T-20 | FR-02 | Contract: lookup must not create a replacement | Negative | Failed lookup creates nothing | LookupError; still 1 patient stored | State unchanged after rejection |
| T-21 | FR-03 (supporting lookup) | Contract: returns the actual stored practitioner | Positive | Known lookup returns the stored object | found is the stored practitioner; specialty matches | Stage 6 supporting target |
| T-22 | FR-03 (supporting lookup) | Contract: IDs are trimmed | Boundary | Padded ID finds the practitioner | name matches | Trimming for practitioners |
| T-23 | FR-03 (supporting lookup) | Contract: absent ID raises LookupError | Negative | Unknown ID reports absence | LookupError | Stage 6 supporting target |
| T-24 | FR-03 (supporting lookup) | Contract: IDs are case-sensitive | Boundary | "d1" is not "D1" | LookupError | Case-sensitivity boundary |
| T-25 | FR-03 (supporting lookup) | Contract: blank ID is invalid input | Negative | Blank ID is invalid | ValueError | Separates invalid from absent |
| T-26 | FR-01 | AC-01.2 | Boundary | " P1 " is a duplicate of "P1" | ValueError; original name kept | Trimmed duplicate boundary, beyond the supplied exact duplicate |
| T-27 | FR-04 | AC-03.2 | Negative | Booking an unknown practitioner is rejected | LookupError; no appointments stored | Supplied test covers unknown patient; this covers practitioner |
| T-28 | FR-05 | AC-04.1 | Negative | Same practitioner, exact time, SCHEDULED conflicts | ValueError; only the first appointment stored | Checks unchanged state after rejection |
| T-29 | FR-05 | Contract: conflict needs the exact same datetime | Boundary | A different time is not a conflict | 2 appointments stored | Exact-time boundary |
| T-30 | FR-05 | Contract: conflict needs an existing SCHEDULED appointment | Boundary | A cancelled booking does not block the slot | New booking is SCHEDULED | Status boundary of the conflict rule |
| T-31 | FR-06 | AC-05.1 | Positive | Service cancel returns the stored object, CANCELLED | result is the booked appointment; status CANCELLED | Stage 6 target: same-object return |
| T-32 | FR-07, FR-08 | AC-05.2, AC-06.1 | Positive | Cancelled history stays retrievable | find_appointment("A1") is the object; list == [appointment] | Stage 6 target: retained history through the service |
| T-33 | FR-06 | AC-05.3 | Negative | Repeated service cancel is rejected without change | ValueError; status stays CANCELLED | Service-level guard |
| T-34 | FR-06 | Contract: only SCHEDULED may be cancelled | Negative | COMPLETED cannot be cancelled through the service | ValueError; status stays COMPLETED | Illegal transition at the service boundary |
| T-35 | FR-06 | Contract: unknown ID raises LookupError at the service | Negative | Unknown ID reports absence; others unchanged | LookupError; A1 still SCHEDULED | State unchanged after rejection |
| T-36 | FR-06 | Contract: blank ID is invalid input | Negative | Blank ID is invalid | ValueError | Separates invalid from absent |
| T-37 | FR-06 | AC-05.1 | Positive | Cancelling one appointment leaves others alone | other appointment stays SCHEDULED | No side effects on other records |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| T-15 | Fresh store and services; register P1 "Alex Example" and D1 (make_session) | patient_service.find_patient("P1") | found is data_store.find_patient("P1"); found.name == "Alex Example" | Identity proves the actual stored object is returned, not a copy or replacement (AC-02.1). "Not None" alone would not. |
| T-17 | Fresh session with only P1 registered | find_patient("P2") | pytest.raises(LookupError) | Proves absence is reported with the specific service exception (AC-02.2), not None or ValueError. |
| T-28 | Fresh session; book A1 with D1 at 2026-10-01 09:00 | book A2 with D1 at the same time | pytest.raises(ValueError); list_appointments() == [first] | Checks both the rejection (AC-04.1) and that the stored state did not change. |
| T-31 | Fresh session; book A1 | cancel_appointment("A1") | result is appointment; result.status is CANCELLED | Same-object identity and the exact status prove the domain transition was used on the stored object (AC-05.1). |
| T-32 | Fresh session; book A1 | cancel_appointment("A1") | find_appointment("A1") is appointment; list_appointments() == [appointment] | Proves cancelled history is retained for lookup and listing (AC-05.2, AC-06.1). |
| T-33 | Fresh session; book and cancel A1 | cancel_appointment("A1") again | pytest.raises(ValueError); status is still CANCELLED | Proves the repeat is rejected and the failed operation left state unchanged (AC-05.3). |
| T-13 | Appointment constructed with status COMPLETED | appointment.cancel() | pytest.raises(ValueError); status is still COMPLETED | Proves only SCHEDULED can be cancelled and the guard does not mutate state. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| T-01 | Valid patient data is kept with spaces trimmed | tests/test_domain.py::test_patient_stores_trimmed_values | Passed |
| T-02 | A blank patient ID is invalid | tests/test_domain.py::test_blank_patient_id_is_rejected | Passed |
| T-03 | A name made only of spaces counts as blank | tests/test_domain.py::test_whitespace_only_patient_name_is_rejected | Passed |
| T-04 | Identity cannot be reassigned | tests/test_domain.py::test_patient_id_cannot_be_changed | Passed |
| T-05 | Valid practitioner fields are stored | tests/test_domain.py::test_practitioner_stores_all_fields | Passed |
| T-06 | Specialty is required | tests/test_domain.py::test_blank_specialty_is_rejected | Passed |
| T-07 | A new appointment starts SCHEDULED | tests/test_domain.py::test_new_appointment_starts_scheduled | Passed |
| T-08 | A patient ID string is not accepted as a Patient | tests/test_domain.py::test_appointment_needs_a_patient_object | Passed |
| T-09 | Seconds are not allowed | tests/test_domain.py::test_appointment_time_with_seconds_is_rejected | Passed |
| T-10 | Text dates are rejected by the domain | tests/test_domain.py::test_appointment_time_as_text_is_rejected | Passed |
| T-11 | Cancelling SCHEDULED makes it CANCELLED | tests/test_domain.py::test_cancel_changes_status | Passed |
| T-12 | A second cancel is rejected without change | tests/test_domain.py::test_repeated_cancellation_is_rejected | Passed |
| T-13 | COMPLETED cannot be cancelled | tests/test_domain.py::test_completed_appointment_cannot_be_cancelled | Passed |
| T-14 | Status cannot be assigned directly | tests/test_domain.py::test_status_cannot_be_set_directly | Passed |
| T-38 | Blank patient ID and blank specialty rejected (supplied) | tests/test_starter.py::test_required_fields | Passed |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| T-15 | Known lookup returns the stored object | FR-02 / AC-02.1 | tests/test_services.py::test_find_patient_returns_the_stored_patient | Passed |
| T-16 | Padded ID finds the patient | FR-02 / AC-02.1 + contract: IDs are trimmed | tests/test_services.py::test_find_patient_trims_the_id | Passed |
| T-17 | Unknown valid ID reports absence | FR-02 / AC-02.2 | tests/test_services.py::test_find_unknown_patient_raises_lookup_error | Passed |
| T-18 | "p1" is not "P1" | FR-02 / AC-02.2 + contract: IDs are case-sensitive | tests/test_services.py::test_find_patient_is_case_sensitive | Passed |
| T-19 | Blank ID is invalid, not absent | FR-02 / Contract: blank ID is invalid input (ValueError) | tests/test_services.py::test_blank_patient_id_lookup_raises_value_error | Passed |
| T-20 | Failed lookup creates nothing | FR-02 / Contract: lookup must not create a replacement | tests/test_services.py::test_failed_patient_lookup_does_not_add_a_patient | Passed |
| T-21 | Known lookup returns the stored object | FR-03 (supporting lookup) / Contract: returns the actual stored practitioner | tests/test_services.py::test_find_practitioner_returns_the_stored_practitioner | Passed |
| T-22 | Padded ID finds the practitioner | FR-03 (supporting lookup) / Contract: IDs are trimmed | tests/test_services.py::test_find_practitioner_trims_the_id | Passed |
| T-23 | Unknown ID reports absence | FR-03 (supporting lookup) / Contract: absent ID raises LookupError | tests/test_services.py::test_find_unknown_practitioner_raises_lookup_error | Passed |
| T-24 | "d1" is not "D1" | FR-03 (supporting lookup) / Contract: IDs are case-sensitive | tests/test_services.py::test_find_practitioner_is_case_sensitive | Passed |
| T-25 | Blank ID is invalid | FR-03 (supporting lookup) / Contract: blank ID is invalid input | tests/test_services.py::test_blank_practitioner_id_lookup_raises_value_error | Passed |
| T-26 | " P1 " is a duplicate of "P1" | FR-01 / AC-01.2 | tests/test_services.py::test_duplicate_patient_id_with_spaces_keeps_original | Passed |
| T-27 | Booking an unknown practitioner is rejected | FR-04 / AC-03.2 | tests/test_services.py::test_booking_unknown_practitioner_stores_nothing | Passed |
| T-28 | Same practitioner, exact time, SCHEDULED conflicts | FR-05 / AC-04.1 | tests/test_services.py::test_conflict_is_rejected_and_original_is_kept | Passed |
| T-29 | A different time is not a conflict | FR-05 / Contract: conflict needs the exact same datetime | tests/test_services.py::test_same_practitioner_at_a_different_time_is_allowed | Passed |
| T-30 | A cancelled booking does not block the slot | FR-05 / Contract: conflict needs an existing SCHEDULED appointment | tests/test_services.py::test_cancelled_appointment_frees_the_time_slot | Passed |
| T-31 | Service cancel returns the stored object, CANCELLED | FR-06 / AC-05.1 | tests/test_services.py::test_cancel_returns_same_appointment_as_cancelled | Passed |
| T-32 | Cancelled history stays retrievable | FR-07, FR-08 / AC-05.2, AC-06.1 | tests/test_services.py::test_cancelled_appointment_is_still_stored | Passed |
| T-33 | Repeated service cancel is rejected without change | FR-06 / AC-05.3 | tests/test_services.py::test_cancelling_twice_raises_value_error | Passed |
| T-34 | COMPLETED cannot be cancelled through the service | FR-06 / Contract: only SCHEDULED may be cancelled | tests/test_services.py::test_completed_appointment_cannot_be_cancelled | Passed |
| T-35 | Unknown ID reports absence; others unchanged | FR-06 / Contract: unknown ID raises LookupError at the service | tests/test_services.py::test_cancel_unknown_appointment_raises_lookup_error | Passed |
| T-36 | Blank ID is invalid | FR-06 / Contract: blank ID is invalid input | tests/test_services.py::test_cancel_with_blank_id_raises_value_error | Passed |
| T-37 | Cancelling one appointment leaves others alone | FR-06 / AC-05.1 | tests/test_services.py::test_cancel_only_changes_the_chosen_appointment | Passed |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Patient ID validation | Blank "" or whitespace-only "   " ID | ValueError; nothing stored | T-02, T-19 |
| Patient name validation | Whitespace-only name | ValueError | T-03 |
| Practitioner validation | Blank specialty | ValueError | T-06 |
| ID trimming | " P1 " / " D1 " on lookup | Finds the stored record | T-16, T-22 |
| ID case sensitivity | "p1" / "d1" | LookupError (different ID) | T-18, T-24 |
| Duplicate after trimming | Register " P1 " when P1 exists | ValueError; original name kept | T-26 |
| Unknown vs blank ID | "P2" vs "   " | LookupError vs ValueError | T-17, T-19 |
| Lookup side effects | Unknown ID lookup | LookupError; patient count unchanged | T-20 |
| Date/time precision | datetime with seconds | ValueError | T-09 |
| Date/time type | Text "2026-10-01 09:00" | ValueError | T-10 |
| Practitioner conflict | Same practitioner, exact same time, SCHEDULED | ValueError; only original stored | T-28 |
| Conflict boundary: time | Same practitioner, 1 hour later | Allowed; both stored | T-29 |
| Conflict boundary: status | Same practitioner and time, original CANCELLED | Allowed; new booking SCHEDULED | T-30 |
| Repeated cancellation | Cancel A1 twice | ValueError; stays CANCELLED | T-12, T-33 |
| Illegal transition | Cancel a COMPLETED appointment | ValueError; stays COMPLETED | T-13, T-34 |
| Unknown cancellation | Cancel "A2" when only A1 exists | LookupError; A1 stays SCHEDULED | T-35 |
| Direct state change | appointment.status = CANCELLED | AttributeError; stays SCHEDULED | T-14 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? Our tests use small, fixed synthetic data and call the domain and service classes directly. They do not prove that the interactive console menu works, because it is not built until Stage 9. They do not check text input typed by a user, such as a date written as "tomorrow": parse_date_time in console.py has no tests yet, although test_domain.py does check that an Appointment rejects a date given as text. They do not check behaviour with large numbers of records. Data is kept only for the current session by design (FR-10 persistence is retired), so keeping data after the program closes is correctly not tested.
Coverage if used: Not used.
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? The areas that matter most are the console date parsing and the Stage 9 menu, because that is where real user input enters the system. Even 100% coverage would only show that lines ran, not that the assertions check the right behaviour or that every requirement and boundary has a test.
Optional fixtures/parametrisation used and why, if any: Not used. Each test calls a plain helper function, make_session(), that creates a fresh data store and services, so every test starts from its own state. We chose simple, separate tests because they are easier for everyone in the team to read and explain.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| Emmanuel Cadman (Emmanuel07-code) | Brought tests/test_domain.py and tests/test_services.py into the project, ran the full suite, single tests and a reordered run, answered tutorial Activities 1 to 4, the exit question, K and the formative questions (N), assigned the TEST IDs and checked the traceability tables (B to G), and managed the GitHub branch, commits and PR. | PR #1, commit ede66ac; Stage 7 PR [link to add] |
| Tanveer Uppal (TanveerUppal) | [complete] | [complete] |
| Tanzir Ahon (Tanzir1718) | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
Verification asks: did we build it right? It checks that the implementation meets the specified requirements, for example that cancel_appointment really changes a SCHEDULED appointment to CANCELLED as FR-06 says.

2. What question does validation answer?
Validation asks: did we build the right thing? It checks that the specified product actually meets the users' real need, for example that keeping cancelled appointments is what the clinic actually needs.

3. What is a unit test?
A unit test checks a small, isolated piece of code on its own, such as one method of one class. Our tests in test_domain.py are unit tests, for example checking that Appointment.cancel() rejects a second cancellation.

4. What is a pytest fixture?
A pytest fixture is reusable setup, marked with @pytest.fixture, that gives each test a fresh starting state, so tests do not depend on each other. We used a plain helper function, make_session(), which does the same job: every test gets a new data store and services.

5. What is parametrisation in pytest?
Parametrisation, with @pytest.mark.parametrize, runs the same test several times with different inputs, for example one blank-ID test run with "", "   " and None. We chose separate simple tests instead, to keep them easy to read.

6. What is regression testing?
Regression testing means rerunning all the existing tests after a change, to make sure nothing that previously worked got broken. That is why we run all 45 tests, including the 8 supplied ones, after every change, not just the new tests.

7. What does code coverage tell us, and what does it not prove?
Coverage tells us which lines of code ran during the tests. It does not prove that those lines were checked properly, that the assertions are meaningful, or that every requirement and boundary case has a test.

8. What makes an assertion weak?
An assertion is weak when it is too vague or always passes, so it would not notice broken code. Examples are assert True, or assert appointment is not None, which passes even if the wrong appointment is returned.

9. What is the appropriate role of GitHub Copilot as a test assistant?
Copilot can suggest test ideas and candidate tests, but the human always decides and verifies. We check each suggestion against the real requirement and code, reject weak assertions or invented features such as SMS, and only count a test as passing after we have actually run it.

10. What is the Stage 7 engineering rule?
Every test must prove a specific required behaviour, traced to a requirement or acceptance criterion, with an assertion that would fail if that behaviour broke. The question to ask is: what required behaviour does this test actually prove?

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
