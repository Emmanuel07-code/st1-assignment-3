# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group 4, Computer Lab 09 (Friday 08:30–10:30)
Members and UG/PG cohorts: Emmanuel Cadman (Emmanuel07-code, UG); Tanveer Uppal (TanveerUppal, UG); Tanzir Ahon (Tanzir1718, UG)
Record owner / contribution links for each member: Record owner: Emmanuel Cadman. Contributions: see I.

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason:
1. "Appointment disappears after cancellation": **symptom**. It is what a user sees go wrong. It does not say why.
2. "The data-store removal path is probably being called": **hypothesis**. It is a guess about the cause ("probably"). We checked it against our project: SmartCareDataStore has no public delete method and Appointment.cancel() only changes the status, so this guess does not fit our code.
3. "The failing test shows store.find_appointment('A1') returns None": **evidence**. It is a fact we can see from a test run.
4. "The service layer is badly designed": **opinion**. It cannot be tested and does not point to a cause for this failure.
5. "Traceback points to smartcare/services.py line 42": **evidence**. It is a fact from the run. In our actual run the LookupError was raised at smartcare/services.py line 136 in AppointmentService.find_appointment. It shows where the error appeared, not where the real cause is.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: Scenario chosen: cancelled history.
- Expected: after A1 is cancelled, find_appointment("A1") still returns A1 with status CANCELLED (FR-07, AC-05.2).
- Observed: LookupError "Appointment not found".
- Reproduction: register patient P1 and practitioner D1, book A1 with D1 at 2026-10-01 09:00, cancel A1, then look up A1.
- Hypothesis: the lookup ignores cancelled appointments.
- Evidence to inspect: the code of SmartCareDataStore.find_appointment, and whether A1 is still in list_appointments() after the cancel.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: The test should be changed, not the product. FR-07 says cancelled appointments must be kept, so a test that expects them to be deleted is checking the wrong thing (a test defect). A test that expects two different practitioners at the same time to conflict also does not match AC-04.2, which allows this, so that test would be wrong as well. The expected result must come from the requirements, not from whatever a test says.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:
- Smells: the method is too long, it repeats status strings (magic strings), it changes the collections directly instead of using SmartCareDataStore, it prints inside the service, it mixes validation with other work, and it has deeply nested ifs.
- Small refactorings: use the AppointmentStatus enum instead of strings; call the existing SmartCareDataStore methods instead of touching the collections; return a value or raise an exception instead of printing; move repeated checks into a small helper; use early returns to reduce nesting.
- Classification: rename appt to appointment = **refactoring**; extract a repeated conflict helper = **refactoring**; add rescheduling = **feature**; restore retained cancellation lookup = **repair**; replace a magic status string with the existing enum = **refactoring**.
- Behaviour that must stay the same: the same results and the same exceptions (ValueError and LookupError) for the same inputs; conflicts are still rejected; cancelled appointments are still kept and can be found; all existing tests still pass.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason:
- Failure: tests/test_services.py::test_cancelling_twice_raises_value_error (test line 210).
- Expected: ValueError on the second cancel (FR-06, AC-05.3). Observed: LookupError "Appointment not found".
- Call path: test → AppointmentService.cancel_appointment (services.py line 145) → AppointmentService.find_appointment (services.py line 136) → SmartCareDataStore.find_appointment returned None → LookupError.
- Ranked causes and checks:
  1. The data store lookup skips cancelled appointments. Check: after cancelling, A1 is still in list_appointments() with status CANCELLED, but find_appointment("A1") returns None.
  2. Cancelling deletes the appointment from the store. Check: after cancelling, A1 is missing from list_appointments().
  3. The stored ID no longer matches "A1". Check: the stored appointment's appointment_id is different from "A1".
- A traceback only shows where the exception was raised (in the service). It does not show where the wrong value came from (here the data store returned None), so we still have to check the evidence.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Because you are guessing. You might change the wrong code, hide the real cause, break other behaviour, or "fix" a test that was actually correct. It is better to reproduce the failure first, check the requirement, write down a hypothesis and look at the evidence before changing anything.


Classification responses (1–5, each with reason): see A.1.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: see A.2.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: see A.5.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: 99f074a (main, Merge pull request #7). SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: `python -m pytest -q` in project/ on main 99f074a: 45 passed (Python 3.14.7, pytest 8.3.5), git status clean.
- Clean preparation SHA if a record-only commit followed Stage 7: Not applicable. Preparation started directly from 99f074a.
- Branch and preparer / how teammates obtained this branch: Branch debug/stage08, prepared by our tutor on Emmanuel's computer and pushed to origin. Teammates get it with `git fetch origin` then `git switch debug/stage08`.
- Downloaded tool version, source SHA256 and --check outcome: The preparation utility was run by our tutor. Its output was not given to the group, so the version, SHA256 and --check result are not available to us.
- --apply and --verify output summaries / artefact references: Run by our tutor (see above). The result is the commit 7eadcbc on debug/stage08.
- Bounded diff inspected and recovery location (not committed): `git diff main --stat` on debug/stage08 showed only project/smartcare/data_store.py changed (11 insertions, 18 deletions), in find_appointment and has_practitioner_conflict. No recovery files are committed; .gitignore excludes .stage8_faults/, .stage8-check-*/ and .stage8-verify-*/.
- Prepared faulty-state commit SHA: 7eadcbc "Prepare stage 08 debug" (parent 99f074a).
- Preparation or recovery issues and resolution, if any: At first we looked for a branch named debug/stage8; the tutor's branch is called debug/stage08. No other issues.
- Initial prepared full-suite command / result / key failures: `python -m pytest -q` in project/ on 7eadcbc: 4 failed, 41 passed. Failures: test_services.py::test_conflict_is_rejected_and_original_is_kept (DID NOT RAISE ValueError); test_starter.py::test_conflict_rule_and_different_practitioner (DID NOT RAISE ValueError); test_services.py::test_cancelled_appointment_is_still_stored (LookupError: Appointment not found); test_services.py::test_cancelling_twice_raises_value_error (LookupError: Appointment not found).

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: Booking a second appointment for the same practitioner at the same date and time is accepted with no error.
- Expected behaviour and requirement: It must raise ValueError and keep only the original appointment (FR-05, AC-04.1). A different practitioner at the same time must still be allowed (AC-04.2).
- Minimal synthetic reproduction steps: Register patient P1 and practitioner D1. Book A1 with D1 at 2026-10-01 09:00. Book A2 with D1 at the same time. A2 is accepted instead of raising ValueError.
- Meaningful failing test path/name and exact relevant failure: tests/test_regressions.py::test_f8_01_same_practitioner_same_time_is_a_conflict fails because has_practitioner_conflict("D1", 2026-10-01 09:00) returns False instead of True. The existing tests test_services.py::test_conflict_is_rejected_and_original_is_kept and test_starter.py::test_conflict_rule_and_different_practitioner fail with "DID NOT RAISE ValueError".
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: In SmartCareDataStore.has_practitioner_conflict, the practitioner check was `appointment.practitioner.practitioner_id != practitioner_id`. The `!=` means it only looks at appointments for other practitioners, so a clash with the same practitioner is never found. The diff against main and the new regression test calling has_practitioner_conflict directly both confirm this.
- Smallest justified fix / diff / why other behaviour is preserved: Changed `!=` to `==` on that one line. The other conditions (excluded ID, exact datetime, SCHEDULED status) are unchanged, so a different practitioner or a different time is still allowed and cancelled appointments still do not cause a conflict.
- Repair SHA / focused verification result: 03714c7. `python -m pytest -q` in project/: 47 passed (both regression tests pass).

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After an appointment is cancelled, looking it up by its ID raises LookupError "Appointment not found". Cancelling it a second time also raises LookupError instead of ValueError.
- Expected behaviour and requirement: A cancelled appointment stays stored and can still be found with status CANCELLED (FR-06, FR-07, AC-05.2). A second cancel raises ValueError (AC-05.3).
- Minimal synthetic reproduction steps: Register P1 and D1. Book A1 with D1 at 2026-10-01 09:00. Cancel A1. Look up A1. LookupError is raised.
- Meaningful failing test path/name and exact relevant failure: tests/test_regressions.py::test_f8_02_cancelled_appointment_can_still_be_found fails with `assert None is <Appointment>` because find_appointment("A1") returns None. The existing tests test_services.py::test_cancelled_appointment_is_still_stored and test_services.py::test_cancelling_twice_raises_value_error fail with "LookupError: Appointment not found".
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.find_appointment was changed to loop through the appointments with the condition `and appointment.status.value != "cancelled"`, so it skips any cancelled appointment and returns None. The appointment is still stored (cancel() only changes the status), it just cannot be found.
- Smallest justified fix / diff / why other behaviour is preserved: Removed the status condition, so the line is now `if appointment.appointment_id == appointment_id.strip():`. Blank IDs still raise ValueError, IDs are still trimmed, and unknown IDs still return None.
- Repair SHA / focused verification result: 03714c7. `python -m pytest -q` in project/: 47 passed.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: We think the part of has_practitioner_conflict that checks the practitioner is wrong, so it does not notice a clash with the same practitioner. It is plausible because only data_store.py was changed and both failing tests are about conflicts.
Evidence intended to inspect / competing explanation / discriminating check: Inspect the conditions in has_practitioner_conflict. Competing explanation: the service does not call the check at all. Check: call has_practitioner_conflict directly in a test; if it returns False for the same practitioner and time, the fault is in the data store, not the service.
Member and saved sequence/time or commit showing this preceded consultation: Emmanuel Cadman, written 8 Nov 2026 at 10:34 (local time), before the F8-01 Copilot prompt at 10:37.

### F8-02 human entry
Likely cause and why plausible: We think find_appointment was changed so it ignores cancelled appointments, so it cannot find them after cancelling. It is plausible because both failing tests cancel first and then look up the appointment.
Evidence intended to inspect / competing explanation / discriminating check: Inspect the code of find_appointment. Competing explanation: cancelling deletes the appointment. Check: after cancelling, see if A1 is still in list_appointments(); if it is there but find_appointment returns None, the lookup is the problem.
Member and saved sequence/time or commit showing this preceded consultation: Emmanuel Cadman, written 8 Nov 2026 at 10:34 (local time), before the F8-02 Copilot prompt at 10:39.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: Emmanuel Cadman, GitHub Copilot Chat in PyCharm, 8 Nov 2026 10:37. Prompt:
> Do not edit any files and do not run any commands. Only answer in chat.
> Observed behaviour: Booking a second appointment for the same practitioner at the same date and time is accepted with no error.
> Expected behaviour: It should raise ValueError because the practitioner already has a SCHEDULED appointment then (FR-05, AC-04.1). A different practitioner at the same time should still be allowed (AC-04.2).
> Steps to reproduce: On branch debug/stage08, from the project folder run: python -m pytest -q
> Failing tests: tests/test_services.py::test_conflict_is_rejected_and_original_is_kept and tests/test_starter.py::test_conflict_rule_and_different_practitioner both fail with "DID NOT RAISE ValueError".
> My hypothesis: The part of has_practitioner_conflict that checks the practitioner is wrong, so it does not notice a clash with the same practitioner.
> Relevant code: has_practitioner_conflict in project/smartcare/data_store.py
> Task: Rank the three most likely causes. For each one, say what evidence would confirm or rule it out. Do not rewrite the app and do not invent new requirements. I will treat your answers as hypotheses to check.

1. Ranked suggestion: the practitioner comparison uses the wrong value or field (e.g. a patient ID, or an object compared with an ID). Evidence check: trace the helper and see if the practitioner check is false for the same practitioner. Observed evidence: the check is false, but the fields are correct (practitioner_id compared with practitioner_id); the operator is `!=` instead of `==`. **Partly correct. Modify:** right place, wrong reason.
2. Ranked suggestion: the SCHEDULED status check does not match how the status is stored. Evidence check: see if the status condition is false for a scheduled appointment. Observed evidence: `appointment.status.value == "scheduled"` is True for a scheduled appointment, so it is not the cause. **Wrong. Reject.** (The magic string is still a code smell; see H.)
3. Ranked suggestion: the booking service does not call the helper, or passes the wrong arguments. Evidence check: trace book_appointment. Observed evidence: book_appointment in services.py calls has_practitioner_conflict with the practitioner ID and the same datetime, and services.py was not changed by the preparation. **Wrong. Reject.**

Final human conclusion and comparison with initial hypothesis: The root cause is the `!=` in the practitioner check. This matches our initial hypothesis (the practitioner check is wrong). Copilot's first suggestion pointed to the same place but guessed the wrong reason.

### F8-02 Copilot review
Actual prompt / output reference and member: Emmanuel Cadman, GitHub Copilot Chat in PyCharm (new chat), 8 Nov 2026 10:39. Prompt:
> Do not edit any files and do not run any commands. Only answer in chat.
> Observed behaviour: After an appointment is cancelled, looking it up by its ID raises "LookupError: Appointment not found". Cancelling it a second time also raises LookupError instead of ValueError.
> Expected behaviour: A cancelled appointment stays stored and can still be found with status CANCELLED (FR-06, FR-07, AC-05.2). A second cancel should raise ValueError (AC-05.3).
> Steps to reproduce: On branch debug/stage08, from the project folder run: python -m pytest -q
> Failing tests: tests/test_services.py::test_cancelled_appointment_is_still_stored and tests/test_services.py::test_cancelling_twice_raises_value_error both fail with "LookupError: Appointment not found".
> My hypothesis: find_appointment was changed so it ignores cancelled appointments, so it cannot find them after cancelling.
> Relevant code: find_appointment in project/smartcare/data_store.py
> Task: Rank the three most likely causes. For each one, say what evidence would confirm or rule it out. Do not rewrite the app and do not invent new requirements. I will treat your answers as hypotheses to check.

1. Ranked suggestion: find_appointment filters out cancelled appointments. Evidence check: the appointment is still stored as CANCELLED but find_appointment skips it. Observed evidence: the loop has `and appointment.status.value != "cancelled"`. **Correct. Accept.**
2. Ranked suggestion: cancelling removes the appointment from storage. Evidence check: is the record missing after cancel? Observed evidence: Appointment.cancel() in domain.py only sets the status to CANCELLED and the store has no delete method, so the record stays. **Wrong. Reject.**
3. Ranked suggestion: cancelling changes the ID or the lookup key. Evidence check: compare the stored ID/key before and after cancel. Observed evidence: appointment_id is read-only and the store keeps the appointment under the same ID. **Wrong. Reject.**

Final human conclusion and comparison with initial hypothesis: The root cause is the status filter in find_appointment. This is the same as our initial hypothesis and Copilot's first suggestion.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | 7eadcbc plus new tests/test_regressions.py (not yet committed) | `python -m pytest -q tests/test_regressions.py` in project/ | test_f8_01_same_practitioner_same_time_is_a_conflict FAILED (2 failed in 0.05s, screenshot) |
| F8-01 after repair | 03714c7 | `python -m pytest -q` in project/ | Passed (47 passed in 0.04s, screenshot) |
| F8-02 before repair | 7eadcbc plus new tests/test_regressions.py (not yet committed) | `python -m pytest -q tests/test_regressions.py` in project/ | test_f8_02_cancelled_appointment_can_still_be_found FAILED (same run as above) |
| F8-02 after repair | 03714c7 | `python -m pytest -q` in project/ | Passed (47 passed in 0.04s, same run as above) |
| Full suite after both repairs, before refactor | 03714c7 | `python -m pytest -q` in project/ | 47 passed in 0.04s (45 earlier tests + 2 regression tests) |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: The F8-01 test calls has_practitioner_conflict directly for the same practitioner and time as a stored SCHEDULED appointment and asserts it returns True, so it fails if the practitioner check is wrong again. The F8-02 test cancels A1 and asserts that find_appointment("A1") returns the same object with status CANCELLED, so it fails if the lookup skips cancelled appointments or returns a different object. Both tests are kept in tests/test_regressions.py so the bugs cannot come back without a test failing.
Unrelated failures investigated / resolution: Not applicable. All 4 original failures were caused by F8-01 or F8-02, and all tests passed after the two repairs.

## H. Refactoring decision and before/after verification

Smell and exact location: Magic string. project/smartcare/data_store.py, has_practitioner_conflict, the condition `appointment.status.value == "scheduled"`.
Small proposed structural change / why justified: Replace it with `appointment.status is AppointmentStatus.SCHEDULED`. The enum already exists and is already imported, so this removes a hard-coded string that could be mistyped, and matches how the rest of the code checks status.
External behaviour to preserve / relevant tests: has_practitioner_conflict must still return True only for another SCHEDULED appointment with the same practitioner and exact datetime. Relevant tests: tests/test_regressions.py::test_f8_01_same_practitioner_same_time_is_a_conflict, test_services.py::test_conflict_is_rejected_and_original_is_kept, test_starter.py::test_conflict_rule_and_different_practitioner, and the full suite.
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: One line changed: `and appointment.status.value == "scheduled"):` → `and appointment.status is AppointmentStatus.SCHEDULED):`. Refactor SHA: a1edcd8 (separate commit after the repair commit 03714c7).
Focused and full after-refactor commands / working directory / results / evidence: Before the refactor commit, on the edited file: `python -m pytest -q` in project/: 47 passed in 0.03s, including tests/test_regressions.py::test_f8_01_same_practitioner_same_time_is_a_conflict (terminal screenshot).
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted. The full suite passed before and after, including the F8-01 regression test that checks this exact function, so the behaviour is unchanged.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: F8-01 (practitioner conflict), F8-02 (cancelled lookup) and the refactor (magic string in has_practitioner_conflict) are tracked in this record and in the Stage 8 pull request. Owner: Emmanuel Cadman.
Branch / prepared, repair and refactor checkpoints: debug/stage08. Prepared: 7eadcbc (see B). Repairs: 03714c7 (see C/D). Refactor: a1edcd8 (see H).
PR link and another member's reviewer identity: [PR #8](https://github.com/Emmanuel07-code/st1-assignment-3/pull/8), debug/stage08 → main. Reviewer: Tanveer Uppal and Tanzir Ahon looked over the PR; no written GitHub review.
Key human feedback, difference from Copilot findings and response/outcome: No written comments and no changes requested. The Copilot findings and our human decisions are in F.
Actual review approval / merge evidence: GitHub showed no conflicts with main. Emmanuel merged PR #8 on 8 Nov 2026, as our tutor allowed for the repository owner when there are no conflicts. Merge commit 070801a "Merge pull request #8 from Emmanuel07-code/debug/stage08". No formal GitHub approval was given.
Integrated code SHA and team pull/retest command / working directory / result: 070801a (main). `git switch main`, `git pull`, `python -m pytest -q` in project/. Emmanuel: fast-forward 99f074a..070801a, 47 passed in 0.07s (screenshot). Tanveer: fast-forward 99f074a..070801a, 47 passed in 0.40s (screenshot). Tanzir: not recorded.
Evidence-only later SHA / explanation if different: The final record-only PR (the latest commit on main) adds the review, team results and contributions to this record. No code changed after 070801a.
Each member's substantive contribution and artefact:
- Emmanuel Cadman: baseline check, human-first hypotheses, both Copilot prompts and decisions, regression tests, both repairs (03714c7), refactor (a1edcd8), this record, PR #8 and merge (070801a).
- Tanveer Uppal: pulled main after the merge and retested (47 passed, screenshot); looked over PR #8.
- Tanzir Ahon: looked over PR #8.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? For F8-01, Copilot's first suggestion (the practitioner comparison uses the wrong field, like a patient ID) sounded convincing because it pointed at the right line. When we looked at the code, the fields were correct and the real problem was the `!=` operator. Its second suggestion (the status check) also sounded possible, but the string check still worked, so there was no evidence for it.
2. What evidence changed your group's view? Looking at the actual diff and the new regression tests. The tests call the data store directly, and they failed, which showed the bugs were in data_store.py and not in services.py, even though the traceback pointed to services.py.
3. How did regression tests protect the refactoring? We ran the full suite (47 passed) before and after the refactor. The F8-01 regression test checks has_practitioner_conflict, the exact function we refactored, so if replacing the string with the enum had changed the behaviour, that test would have failed.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Reproduce the failure, check the expected behaviour in the requirements, write down a hypothesis and check the evidence. Only then change the code.

2. Where should expected behaviour come from during debugging?

Response: From the requirements and acceptance criteria (for example FR-07 and AC-05.2), not from what the code currently does or from what a tool suggests.

3. What is a debugging hypothesis?

Response: A possible cause of the failure that can be checked with evidence, for example "find_appointment skips cancelled appointments".

4. What is a regression test and why is it retained?

Response: A test that reproduces a bug that was fixed. It fails before the fix and passes after. We keep it so that if the bug comes back later, the test will catch it.

5. What is meant by root cause?

Response: The actual reason the failure happens, not just where the error shows up. For F8-02 the error appeared in services.py, but the root cause was the status filter in data_store.py.

6. What is refactoring?

Response: Changing the structure of the code to make it cleaner or easier to read without changing what it does. The tests should pass the same before and after.

7. What is a swallowed exception?

Response: An exception that is caught and then ignored (for example `except: pass`), so the error is hidden and the program carries on as if nothing went wrong. This makes bugs harder to find.

8. What is a code smell?

Response: A sign in the code that something could be a problem, like a magic string, duplicated code or a very long method. It is not always a bug, but it is worth looking at.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As hypotheses, not answers. Each one has to be checked against the code and test evidence, then accepted, changed or rejected by us.

10. What is the Stage 8 engineering rule?

Response: Reproduce first, write the hypothesis before using Copilot, fix only what the evidence supports, prove it with a regression test that fails before and passes after, and only refactor when all tests are passing.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: Integrated code SHA 070801a. The submitted SHA is the latest commit on main, which only adds record and README updates after 070801a.
Unresolved issues or incomplete checks / owner / next action: None in the code. Remaining record items (review feedback, teammates' pull results and contributions) are added by Emmanuel when received.
Handover note: Stage 9 starts from main at 070801a, where the full suite gives 47 passed. Both Stage 8 defects are fixed and protected by tests/test_regressions.py, which must be kept.
