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
| changes | Weak | Every commit is a change, even editing one letter. It does not say what changed or what kind of change it was. |
| final version | Weak | It does not say what is final, what changed or what the commit contains. |
| Add patient search by ID | Strong | It says specifically what the commit does: it adds one feature, patient search by ID. |
| fix stuff | Weak | It is unprofessional and does not say what was fixed. "Stuff" could mean anything. |
| Prevent cancellation of completed appointments | Strong | It clearly states the behaviour that changed, so a reviewer knows exactly what to check. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR says it adds cancellation, so it should stick to that. Renaming patient fields, restructuring code and adding a dependency are not what the PR or its issue asked for.
- Responsibility and architecture concerns: Renaming or moving code that other parts already use, such as registration and lookup, can break work that is already done and tested. Changes like that need to be made very carefully and on their own, not hidden inside an unrelated feature.
- Testing and review concerns: Passing tests do not prove everything is fine. The tests may not cover the renamed fields at all. The reviewer has to compare the diff with the existing code, and when one diff mixes four unrelated jobs it is too big to check properly.
- Changes to remove or separate, with reasons: Keep only the cancellation code, because that is what the PR and its issue are for. Remove the field renames and the restructuring; if the team really wants them, they need their own issue and their own small PR. Remove the new dependency completely, because the project must use only the Python standard library.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: "Looks good" gives no reasons. It does not show what was checked, which lines were looked at, or whether other code, such as other functions or branches, could be affected by the change. "Tests pass" is only a claim: Copilot cannot run the tests, so a real test run is still needed.
- Follow-up review question 1: Which lines of the diff did you actually check?
- Follow-up review question 2: What changes were made, and what does each change do?
- Follow-up review question 3: Does this code affect the rest of the project? Which other functions or files use the code that was changed?
- Follow-up review question 4: Does this change have any unwanted influence on existing behaviour, such as registration, booking or the supplied tests?
- Follow-up review question 5: Which acceptance criteria in the linked issue did you check the change against, and which test proves each one?
- Additional questions if useful: You said the tests pass. Which tests, and where is the actual output of the run?

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

A commit count only shows how often someone saved, not how much or how good the work was. You could commit every tiny change, even every single line, and get a high count for very little work. Someone else could work through a file carefully and commit it once, when it is actually ready. A higher number of commits does not mean more time, effort or quality. In our team, only one member makes commits, as agreed with our tutor, so the other members' contributions show up in their reviews, issue work and testing, not in the commit count.

## L Stage 6 formative questions

1. What is version control?

Version control is a system, such as Git, that records every change made to the project over time. It keeps the whole history, so if a change breaks the code, we can go back to an earlier version that we know works.

2. Why is a feature branch useful?

A feature branch keeps the work in progress separate from main, which is the stable version. We can make and test one change on the branch without breaking main, and it only joins main after it has been reviewed.

3. What makes a commit a good engineering commit?

A good commit contains one coherent change that is actually worth saving, and its message clearly describes what changed. That makes it easy for teammates, or anyone else, to understand what happened in that commit without opening the code.

4. What is a pull request?

A pull request asks for the changes on a branch to be merged into main. It shows the diff and explains what the change does and why, so teammates can review and discuss it before it is merged.

5. What is the purpose of code review?

Code review means another person checks the change before it is merged. It is not only about whether the code runs: the reviewer checks it against the requirement and acceptance criteria, looks for mistakes, weak tests and unrelated changes, and makes sure the code is readable.

6. What does a Git diff show?

A diff shows exactly how the code has been modified: which lines were added and which were removed, line by line. On GitHub, added lines are shown in green and removed lines in red, with a total such as +424 −10.

7. What is a Definition of Done?

A Definition of Done is the checklist the team agrees on for when a piece of work really counts as finished, not just when the code is written. For example, our issues say: the code is implemented, the tests pass with all supplied tests still passing, another member has reviewed and approved it, and it has been merged into main through a pull request.

8. What is the appropriate role of GitHub Copilot in pull-request review?

Copilot is a helper, not the reviewer. It can be fast at going over a diff and pointing out small changes or possible problems that a human might take a long time to find. But the human reviewer checks the change first and records their own observations, then checks everything Copilot says against the real code, the requirement and an actual test run. Copilot cannot run the tests, and it cannot approve or merge a PR. That decision belongs to another team member.

9. Why should individual contribution not be judged only by commit count?

Because a commit count only shows how often someone saved work, not what they did. It also misses work that does not create commits, such as reviewing, writing issues, testing and helping teammates. In our team, only one member commits, as agreed with our tutor, so the commit count would show almost all the work as coming from one person, even though the others review and test.

10. What is the Stage 6 engineering rule?

Every change follows the same path: requirement, issue, feature branch, code and tests, commit, pull request, review by another member, and then merge. Nothing goes straight into main, so main always stays a stable, reviewed version that the whole team can trust.

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
