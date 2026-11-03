# Stage 6 activities and evidence

> **TEAM TO COMPLETE — status note (remove when the record is done)**
> The three Stage 6 service methods are implemented in `project/smartcare/services.py` and checked by `project/tests/test_services.py`. Every `[response]` field below is still blank on purpose. Issues, the workflow agreement (E), human review observations, Copilot use (H, I), contributions (J), quiz answers (L) and all SHAs must be written by your own members from your own work and accounts. Do not fill them with text you did not produce.


Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 4, tutorial [response]
- Members, GitHub usernames and cohorts: Emmanuel Cadman (Emmanuel07-code, UG); Tanveer Uppal (TanveerUppal, UG); Tanzir Ahon (Tanzir1718, UG)
- Repository URL: https://github.com/Emmanuel07-code/st1-assignment-3
- Starting SHA: 5f28e1d

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02 Patient search by ID
- Context: Every patient has an ID so the system can identify them. If you have a patient's ID, you should be able to get that exact patient back.
- Requirement: FR-02 Patient Search: PatientService.find_patient(patient_id)
- Acceptance criteria: A registered ID returns the stored patient (the same object, not a copy). A valid ID that is not registered raises LookupError. A blank ID raises ValueError. IDs are trimmed and case-sensitive. A failed lookup does not create a new patient.
- Scope: Lookup by ID only. No search by name: two patients can share a name, but each ID is unique. Adding, editing or removing patients is not part of this issue.
- Definition of Done: find_patient implemented in services.py; tests in tests/test_services.py pass with all supplied tests still passing; reviewed and approved by another team member; merged into main through a pull request.
- Owner: Emmanuel Cadman (Emmanuel07-code)
- Actual issue link: https://github.com/Emmanuel07-code/st1-assignment-3/issues/2

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06/FR-07 Cancel appointment and keep its history
- Context: Sometimes an appointment will not happen anymore and needs to be cancelled. Instead of deleting it, we keep it, so there is still a record that the appointment existed and was cancelled.
- Requirement: FR-06 Appointment Cancellation and FR-07 Retained History: AppointmentService.cancel_appointment(appointment_id)
- Acceptance criteria: Cancelling a SCHEDULED appointment changes its status to CANCELLED. The method returns the same stored appointment object. The cancelled appointment can still be found by ID and still appears in the appointment list. Cancelling an appointment that is already CANCELLED, or that is COMPLETED, raises ValueError and its status does not change. A valid ID that does not exist raises LookupError; a blank ID raises ValueError. A cancelled appointment no longer blocks that practitioner's time slot.
- Scope: Only SCHEDULED appointments can be cancelled, through Appointment.cancel(). No deleting appointments, no rescheduling and no notifications.
- Definition of Done: cancel_appointment implemented in services.py; tests in tests/test_services.py and tests/test_domain.py pass with all supplied tests still passing; reviewed and approved by another team member; merged into main through a pull request.
- Owner: Emmanuel Cadman (Emmanuel07-code)
- Actual issue link: https://github.com/Emmanuel07-code/st1-assignment-3/issues/3

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | [select] | [response] |
| final version | [select] | [response] |
| Add patient search by ID | [select] | [response] |
| fix stuff | [select] | [response] |
| Prevent cancellation of completed appointments | [select] | [response] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: [response]
- Responsibility and architecture concerns: [response]
- Testing and review concerns: [response]
- Changes to remove or separate, with reasons: [response]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [response]
- Follow-up review question 1: [response]
- Follow-up review question 2: [response]
- Follow-up review question 3: [response]
- Follow-up review question 4: [response]
- Follow-up review question 5: [response]
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [#2](https://github.com/Emmanuel07-code/st1-assignment-3/issues/2) | FR-02 Patient Search | Emmanuel Cadman | [Acceptance criteria in #2](https://github.com/Emmanuel07-code/st1-assignment-3/issues/2) | Open, linked to PR #1 |
| [#3](https://github.com/Emmanuel07-code/st1-assignment-3/issues/3) | FR-06 Appointment Cancellation with FR-07 retained history | Emmanuel Cadman | [Acceptance criteria in #3](https://github.com/Emmanuel07-code/st1-assignment-3/issues/3) | Open, linked to PR #1 |
| [#4](https://github.com/Emmanuel07-code/st1-assignment-3/issues/4) | Supporting practitioner lookup over FR-03 registrations | Emmanuel Cadman | [Acceptance criteria in #4](https://github.com/Emmanuel07-code/st1-assignment-3/issues/4) | Open, linked to PR #1 |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [#1](https://github.com/Emmanuel07-code/st1-assignment-3/pull/1) Stage 6: patient/practitioner lookup and appointment cancellation
- Linked issue and requirement: #2 FR-02, #3 FR-06/FR-07, #4 practitioner lookup (supporting, FR-03)
- Feature branch: feature/stage6-services
- Changed behaviour: PatientService.find_patient and PractitionerService.find_practitioner return the stored object, raising LookupError when absent and ValueError for a blank ID. AppointmentService.cancel_appointment cancels through Appointment.cancel(), returns the same object and keeps it stored. New tests/test_services.py and tests/test_domain.py.
- Meaningful commits: [ede66ac](https://github.com/Emmanuel07-code/st1-assignment-3/commit/ede66ac)
- Test command, directory and observed result: python -m pytest, run from project/, 45 passed (Python 3.14.7, pytest 8.3.5), on branch feature/stage6-services at ede66ac. Baseline on main before the change: 8 passed.
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: Copilot not used for the implementation. The code and tests were drafted with an AI assistant (Claude), then checked and run by Emmanuel Cadman; disclosed in PR #1.
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: 5f28e1d
- Final Stage 6 code SHA: [response]
- Test command: python -m pytest
- Working directory: project/
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
