# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 4, Computer Lab 09 (Friday 08:30–10:30)
Members and UG/PG applicability: Emmanuel Cadman (Emmanuel07-code, UG); Tanveer Uppal (TanveerUppal, UG); Tanzir Ahon (Tanzir1718, UG). UG-only group: common scope only; Stages 10 and 11 and all PG items are not part of our pathway.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare v1.0 (course release). SmartCare A3 Requirements Baseline 2026, revision 2.
Common starting SHA / branch / applicable members: 9fbd296 on main (Stages 6–9 integrated and recorded, 60 passed). All three members (UG).
PG starting SHA / branch / applicable members or not applicable: Not part of our pathway (UG-only group).
Working-state review and approved integration: main was pulled and the full suite run before release work (60 passed at 9fbd296). The only change after that was adding tests/test_workflows.py (Stage 9 handout requirement) and removing the tracked editor file .idea/.gitignore.
Protected common candidate and PG differences: The common candidate is the tested SHA in K. There is no PG candidate.
Feature freeze / owner / verifier: Feature freeze from 9fbd296: no new features, only tests, records and README. Owner: Emmanuel Cadman. Verifier: Emmanuel Cadman, with Tanveer Uppal's pull-and-test runs (Stage 8 I).


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: Do not release yet. Passing tests only show the tested behaviour works. Another person could not set up and run the system from an incomplete README, an unreviewed dependency could be unsafe, and an undocumented limitation would mislead users. Once the README is fixed, the dependency reviewed and the limitation documented, it could be released.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | test_cancelled_appointment_is_still_stored, test_f8_02_cancelled_appointment_can_still_be_found, test_full_booking_workflow (FR-06, FR-07, AC-05.2) | tests/test_services.py, tests/test_regressions.py, tests/test_workflows.py at the tested SHA (K) | Emmanuel Cadman | Yes | None |
| Architecture responsibilities are appropriate | Domain rules in domain.py, storage in data_store.py, coordination in services.py, pure query in queries.py, input/output only in console.py | project/smartcare/ at the tested SHA | Emmanuel Cadman; Tanveer Uppal reviewed the Stage 6 design (Stage 6 I) | Yes | None |
| Rescheduling is safe — PG only | Not applicable: UG-only group | — | — | — | — |
| AI use is responsible — common recheck / PG assurance | Copilot outputs were treated as hypotheses and checked against code and tests (Stage 6 H, Stage 7 H/I, Stage 8 F, Stage 9 E) | Stage records | Emmanuel Cadman | Yes | None |
| System is maintainable | Small methods, type hints, docstrings, enum instead of magic strings (Stage 8 refactor), 63 automated tests | project/ at the tested SHA | Emmanuel Cadman | Yes | None |
| FR-01–03 register/find and validation | test_domain.py and test_services.py lookup/registration tests | tests/ at the tested SHA | Emmanuel Cadman | Yes | None |
| FR-04–05 booking/conflict rules | test_conflict_is_rejected_and_original_is_kept, test_f8_01_same_practitioner_same_time_is_a_conflict, test_full_booking_workflow (AC-04.1, AC-04.2) | tests/ at the tested SHA | Emmanuel Cadman | Yes | None |
| FR-06–08 cancellation/history/find | test_cancelling_twice_raises_value_error, test_repeated_cancellation_and_invalid_status_are_rejected (AC-05.3) | tests/ at the tested SHA | Emmanuel Cadman | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | tests/test_queries.py (QRY-01–04, FP-01–03) and listing tests in test_services.py | tests/ at the tested SHA; Stage 9 C | Emmanuel Cadman | Yes | None |
| UI full console sequence and error recovery | UI-01 and UI-02 console runs (Stage 9 D) and the demo in D below | Stage 9 D; D below | Emmanuel Cadman | Yes | None |
| Session-only scope / FR-10 retired | project/README.md states data exists only for the session and FR-10 is retired; the menu exit says "Session data discarded" | project/README.md | Emmanuel Cadman | Yes | None |
| PG RES and assurance integration | Not applicable: UG-only group | — | — | — | — |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.14.7, pytest 8.3.5 | project/: `python -m pytest -q` | 29deede | 63 passed | terminal screenshot |
| Complete PG if applicable | Not applicable (UG-only) | — | — | — | — |
| Affected focused checks after correction | Python 3.14.7, pytest 8.3.5 | project/: `python -m pytest -q tests/test_workflows.py` | 29deede | 3 passed | terminal screenshot |
| Full integrated recheck | Python 3.14.7, pytest 8.3.5 | project/ on main after `git pull`: `python -m pytest -q` | 29deede | 63 passed | terminal screenshot |
Prior assertions preserved / reviewed test diff: No earlier test was changed or removed. Since Stage 9 the only test change is the new file tests/test_workflows.py.
Remaining failure / limitation: None. All 63 tests pass.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | A small clinic needs to book appointments without double-booking a practitioner. Stakeholders: reception staff, practitioners, patients. | Scope of the requirements baseline | Explained at the start of the demo | — |
| Register and find Patient and two Practitioners | Options 1, 2, 3, 4: P1 Alex Example; D1 Taylor Example (General); D2 Jordan Example (Cardiology) | FR-01–03 | Each is registered and found | Stage 9 D UI-01 |
| Valid booking | Option 5: A1, P1, D1, 2026-10-01 09:00 | FR-04 | Booked | Stage 9 D UI-01 |
| Same practitioner exact-time conflict rejected | Option 5: A2, P1, D1, 2026-10-01 09:00 | FR-05, AC-04.1 | Error shown, menu returns, A2 not stored | Stage 9 D UI-01 |
| Different practitioner same time allowed | Option 5: A2, P1, D2, 2026-10-01 09:00 | AC-04.2 | Booked | Stage 9 D UI-01 |
| Cancel SCHEDULED and retain/find CANCELLED object | Option 6: A1, then option 7: A1 | FR-06, FR-07, AC-05.2 | A1 shown as CANCELLED | Stage 9 D UI-01 |
| Invalid/repeated cancellation rejected | Option 6: A1 again; option 6: A9 | AC-05.3 | Error shown each time, A1 stays CANCELLED | Stage 9 D UI-02 |
| Default all-status listing | Option 8: D1, blank status | FR-09 | A1 (cancelled) listed | Stage 9 D UI-01 |
| Explicit filtering / empty vs unknown / deterministic order | Option 8: D1 scheduled (empty message); D9 (unknown error); book A3 in the freed slot and list D1 | QRY-01–04 | Empty list message, unknown practitioner error, then A1, A3 in date/time then ID order | Stage 9 D UI-01 |
| Invalid date/status/menu/lookup recovery and continued operation | `not a date`, `2026-02-30 09:00`, status `pending`, choice `99`, blank patient ID | UI-02 | Each error shown, the menu returns and the next valid action works | Stage 9 D UI-02 |
| Session-only limitation and normal exit | Option 0, then start the program again | Session-only scope (FR-10 retired) | "Goodbye. Session data discarded."; a new session starts empty | Stage 9 D |
| One meaningful requirement-linked pytest test explained | test_f8_02_cancelled_appointment_can_still_be_found | FR-07, AC-05.2 | It cancels A1 and checks find_appointment returns the same object with status CANCELLED; it failed on the Stage 8 fault and passes now | Stage 8 G |
| Architecture and one actual AI decision / known limitation | Copilot's F8-01 suggestion "wrong field compared" was modified: the real cause was `!=` | Stage 8 F | Explained with the evidence that changed our view | Stage 8 F, J |
| PG reschedule identity/participants/time and no-op | Not applicable (UG-only) | — | — | — |
| PG conflict/invalid status/failure non-mutation | Not applicable (UG-only) | — | — | — |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable (UG-only) | — | — | — |
Stable demo owner / fresh process / command: Emmanuel Cadman; fresh process each time; from project/: `python main.py --interactive`.
PG demonstrations through service/tests or not applicable: Not applicable (UG-only group).


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | project/smartcare/*.py | No finding: queries.py has no store access, printing or mutation (tested by FP-01–03) | No change; 63 passed |
| PascalCase and snake_case naming | project/smartcare/*.py | No finding: classes PascalCase, functions/variables snake_case | No change |
| Useful type hints and meaningful docstrings | project/smartcare/*.py | Finding: the Stage 8 preparation removed the docstrings of find_appointment and has_practitioner_conflict | Accepted as minor debt (G); behaviour is covered by tests |
| Four-space indentation and imports/layout | project/ | No finding | No change |
| Focused methods / duplication / dead or commented code | project/smartcare/*.py | No finding: short methods, Stage 8 magic string replaced with the enum | No change |
| Globals / leakage / unnecessary inheritance or frameworks | project/ | No finding: no globals; one store shared by the services in a session | No change |
| No SQLite/persistence/repository ABCs/speculative features | project/ | No finding: in-memory dictionaries only | No change |
| Synthetic data / secrets / dependencies / provenance | project/requirements-dev.txt, tests | No finding: only pytest==8.3.5 (dev), standard library at runtime, synthetic names only, no secrets. Finding: the editor file .idea/.gitignore was tracked | Removed .idea/.gitignore from Git (PR #12); .idea/ ignored in .gitignore |
| Significant common Copilot contributions and human verification | Stage 6 H, Stage 7 H/I, Stage 8 F, Stage 9 E | Copilot was used for reviews and diagnosis; each output was checked against code and tests | No change |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | Not applicable (UG-only) | — | — |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Stage 9 Copilot review: "No problems found in queries.py, services.py, or console.py." | FR-09, QRY/FP, console.py | Re-ran the full suite (63 passed) and the console demo with invalid input | Accept with caution: Copilot did not run anything, so the claim is only accepted because our own tests and demo agree | No change |
| Stage 8 Copilot F8-01 rank 1: the practitioner check compares the wrong field | FR-05, data_store.has_practitioner_conflict | Read the condition: the fields were right, the operator was `!=` | Modify: right place, wrong reason | Fixed `!=` to `==` (03714c7) |
Access route or approved equivalent / limitations: GitHub Copilot Chat in PyCharm and VS Code (course-nominated assistant), asked not to edit files or run commands.
Available AI evidence and missing evidence honestly disclosed: Copilot prompts and outputs are in the Stage 6–9 records.


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | project/README.md | Emmanuel Cadman | Present: Stage 6 and 9 tasks complete, no PG rescheduling |
| Out-of-scope capabilities and known limitations | project/README.md | Emmanuel Cadman | Present: session-only data, FR-10 retired, no age/duration/patient-conflict/past-date rules |
| Confirmed teaching Python version and dependency installation | project/README.md | Emmanuel Cadman | Present: Python 3.13, pytest 8.3.5, `python -m pip install -r requirements-dev.txt`. We ran on Python 3.14.7 with the same result |
| Working directory / demo / interactive / test commands | project/README.md and root README.md | Emmanuel Cadman | Present: `cd project`, `python main.py`, `python main.py --interactive`, `python -m pytest` |
| Repository structure and architecture responsibilities | root README.md, project/README.md | Emmanuel Cadman | Present |
| Responsible AI summary / synthetic-data rule | root README.md | Emmanuel Cadman | Present: Copilot output is verified and recorded; synthetic data only |
| Release label/version and SHA links | root README.md group index | Emmanuel Cadman | Present: verified code SHA and final submitted SHA |
Root README index and project/README verified: Yes, links to project/README.md and all stage records work.
Fresh clone or extracted ZIP / candidate identity: Release ZIP made with `git archive` from the submitted SHA (K) and extracted to a separate folder.
Verifier and clean environment / actual version: Emmanuel Cadman, Python 3.14.7, pytest 8.3.5.
Setup/run/test commands and observed results: From the extracted project/: `python -m pytest -q` → 63 passed; `python main.py --interactive` starts the menu.
Missing local file or setup gap / remedy and recheck: None found.


## G Known limitations debt and release notes

Delivered features: Register and find patients and practitioners; book appointments with practitioner conflict checking; cancel and find appointments with history kept; list a practitioner's appointments with optional status filter, ordered by date/time then ID; interactive console menu.
Important fixes: Stage 8 F8-01 (conflict check used `!=`) and F8-02 (cancelled appointments could not be found), each protected by a regression test.
Architecture/quality improvements: Stage 8 refactor replaced the magic string "scheduled" with AppointmentStatus.SCHEDULED; Stage 9 pure query with a named sort key.
Known limitations: Data is lost when the program closes; no login or roles; date/time is local with minute precision and no time zone; console only.
AI-assisted development note: GitHub Copilot was used to review code and suggest debugging causes; every suggestion was checked by the team against the code and tests before use (see Stage 6–9 records).

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Docstrings removed from find_appointment and has_practitioner_conflict by the Stage 8 preparation | Slightly harder to read | Low | Add the docstrings back | Accepted: behaviour is tested and unchanged |
| find_appointment loops over all appointments instead of using the dictionary key | Slower with many records | Low | Use the dictionary lookup | Accepted: correct and tested; course data is small |
Session-only synthetic data and minute-precision local time: Accepted scope: data exists only for the session (FR-10 retired); times are local, to the minute.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: Out of scope for this course release.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Single user, single session, console only; no time zones, monitoring or accessibility testing.
Difference between accepted scope limit and unresolved required behaviour: The limits above are outside the requirements baseline. All required behaviour in scope passes its tests; there is no unresolved required behaviour.
PG assurance residual risks / owner / status or not applicable: Not applicable (UG-only group).


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Stage 9: automated workflow tests in tests/test_workflows.py | The file was missing on main at 9fbd296 | Medium: a required Stage 9 artefact was missing | Emmanuel Cadman: added 3 workflow tests | New tests/test_workflows.py | `python -m pytest -q tests/test_workflows.py` 3 passed; full suite 63 passed | None |
| Repository cleanliness | `git ls-files` showed .idea/.gitignore (editor file) tracked | Low | Emmanuel Cadman: removed it from Git and ignored .idea/ | `git rm --cached .idea/.gitignore`; `.idea/` added to .gitignore | `git ls-files` shows no editor files; 63 passed | None |
Justified no-change conclusion if no defect found: No defects were found in the application code during release checks.
Release blockers still open / status: None.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Stage 6 PR #1, #6; Stage 7 PR #7; Stage 8 PR #8; Stage 9 PR #9, #10, #12 (workflow tests); records PR #11; Stage 12 release record in the final PR. Tested code SHA 29deede.
Independent reviewer / feedback / response: Tanveer Uppal reviewed and approved PR #1 (Stage 6 G). The later PRs were looked over by the team without written comments, and merged by Emmanuel as agreed with our tutor when GitHub showed no conflicts.
Integration commit / full recheck: See K; full suite 63 passed on main after the final merge.
Tracked and untracked file inspection / cleanliness: `git ls-files` checked; only README.md, .gitignore, project/ and the stage folders are tracked after removing .idea/.gitignore. `git status` clean.
Secrets/staff material/caches/tool-metadata exclusion check: No secrets, staff material, caches, virtual environments or Stage 8 utility files are tracked; .gitignore covers .venv/, __pycache__/, .pytest_cache/, .env and the Stage 8 recovery folders.
Candidate recovery plan / known-good SHA: Known-good SHA 9fbd296 (60 passed). Any later problem can be undone with `git revert` of the release PR merge.
Named substantive contributions: Emmanuel Cadman: Stages 6–8 code, tests and records, Stage 9 workflow tests, Stage 12 release checks and record. Tanveer Uppal: Stage 6 review and Copilot review, team test runs. Stage 9 queries, listing, console and record: see Stage 9 contributions.


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: READY WITH DOCUMENTED LIMITATIONS
Approver / date / rationale and evidence: Emmanuel Cadman, 9 Nov 2026. All in-scope requirements have passing tests (63 passed), the console demo works including error recovery, and the limitations are written down in G.
What risks remain / conditions / owners: Session-only data and the small debt items in G. Owner: the team, for any future work.
Can the team explain the system: Yes, using the architecture in B and the demo in D.
Can a change be recovered: Yes, with `git revert` back to known-good 9fbd296 (I).
Common decision / PG decision where different: Common only (UG-only group).


## K Final tested release SHA

Exact common tested SHA: 29deede (main, Merge pull request #12), 63 passed
Exact PG tested SHA or not applicable: Not applicable (UG-only group).
Final submitted SHA / repository URL: The latest commit on main; https://github.com/Emmanuel07-code/st1-assignment-3
Evidence-only later commit and difference explanation: The final commit after 29deede only adds this record, the README SHAs and a one-line .gitignore fix (.idea/). No executable code or tests changed.
Executable changes after testing and re-verification: None.
Source ZIP name / SHA correspondence / extracted comparison: SmartCare-release.zip, made with `git archive` from the final submitted SHA, extracted and checked: root README.md, .gitignore, project/ and all stage folders present; 63 passed.


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository URL accessible to marker and exact candidate SHA identified.
- [x] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: Repository URL submitted on the course site; source ZIP uploaded with it.
Deadline/timezone: 9 Nov 2026, 23:59 local time.
Repository access arrangement: Public GitHub repository.
Mixed-candidate upload arrangement: Not applicable (UG-only group).
Oral/video recording/accessibility arrangements: As arranged by the teaching team.
Remaining administration or release dependency: Individual peer forms and viva are routed separately by the course.


## M Formative questions

1. What is a release candidate? A specific, tested version (one exact commit) that the team proposes to release if no blocking problems are found.

2. What is feature freeze and why is it used? A point after which no new features are added, only fixes, tests and documents, so the version being tested stops changing.

3. What is regression testing in a release context? Running the full test suite on the release candidate to show that everything that worked before still works after the latest changes.

4. What is a known limitation? Something the system does not do or does not handle, which is written down so users are not misled.

5. What is technical debt? Shortcuts or untidy parts left in the code that work now but make future changes harder.

6. What are release notes? A short summary for users of what is in the release: features, fixes, limitations and known issues.

7. What is software maintenance? Keeping software working and useful after release: fixing bugs, updating it and improving it.

8. What is the purpose of the individual demonstration/viva? To show that each member understands the system and their own contribution, and can explain decisions and evidence.

9. What should the final responsible-AI check establish before release? That all significant AI output was checked by people against the requirements, code and tests, recorded honestly, and that no secrets or real data were shared.

10. What is the main course conclusion about AI and the role of the software engineer? AI can suggest code and causes, but the engineer is still responsible for checking it against requirements and evidence and deciding what goes into the release.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: 63 passing tests linked to the requirements, including regression tests for the two Stage 8 defects, and a working console demo with error recovery.
Weakest area: Team review: later PRs were looked over but had no written review comments.
How AI use changed from Stage 1 to Stage 12: We started by asking Copilot for answers and moved to giving it the evidence and treating its output as hypotheses to check.
Start doing — engineering and AI use: Write review comments on every PR, and record the Copilot prompt at the time it is used.
Stop doing — engineering and AI use: Merging work before the record and review are finished (this caused the Stage 6 revert).
Continue doing — engineering and AI use: Writing our own hypothesis before asking Copilot, and keeping a failing-then-passing regression test for every fix.
What worked / caused rework / future delivery improvement: Small branches and PRs worked well. Rework came from the Stage 6 revert and late communication. Next time: agree deadlines for each stage and check in daily.
One paragraph — If AI can write code why do we still need software engineers: AI can write code quickly, but it does not know if that code is right for the requirements. In Stage 8 Copilot pointed to the right line for the wrong reason, and in Stage 6 it reported a duplicate docstring that did not exist. An engineer has to decide what the system should do, check AI output against the requirements and tests, find the real cause of failures, and take responsibility for what is released.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | Clinic booking without practitioner double-booking; reception staff, practitioners, patients (D) |
| Two requirements and acceptance criteria | FR-05 / AC-04.1 conflict rejected; FR-07 / AC-05.2 cancelled appointments kept and findable (B) |
| Domain model and architecture | Patient, Practitioner, Appointment and AppointmentStatus in domain.py; store; services; pure query; console (B) |
| Design trade-off | Dictionary store is simple and fast but data is lost on exit (G) |
| Meaningful test and its limits / 100 percent coverage | test_f8_02 checks identity and status after cancel; it does not test the console. 100% coverage would not prove the requirements are right (D) |
| Diagnosed defect and verification | F8-02: find_appointment skipped cancelled appointments; regression test failed before, passed after (Stage 8 D, G) |
| Shared store and session-state/query responsibilities | One store shared by all services in a session; the query only receives a list and returns a new list (Stage 9) |
| What would break if session-state lookup/query responsibilities changed? | If the query read the store or changed the list, the purity tests (FP-01–03) would fail and listing could change stored data |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | cancel() only needs the appointment's own status; a conflict needs to look across all appointments, so the service coordinates it with the store |
| FR-07 retained history test | test_cancelled_appointment_is_still_stored and test_f8_02_cancelled_appointment_can_still_be_found |
| Actual AI change rejected/modified or honestly accepted with verification | Stage 8 F8-01 Copilot suggestion modified (B, E) |
| Unresolved limitation / future production work | Persistence, logins, time zones (G) |
| Personal implementation contribution | Emmanuel Cadman: Stage 6 services, Stage 8 repairs and refactor (PR #1, #8) |
| Personal test/review/design/integration contribution | Emmanuel Cadman: Stage 7 tests, Stage 8 regression tests, Stage 9 workflow tests, merges and records |
| PG agentic change and rescheduling verification | Not applicable (UG-only group) |
| PG responsible-AI risk/remediation or supported no finding | Not applicable (UG-only group) |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.
Separate reflection / peer / common team viva evidence links and routing: Submitted separately through the course site.
No further coding stage. Later corrections use the published assessment process.
