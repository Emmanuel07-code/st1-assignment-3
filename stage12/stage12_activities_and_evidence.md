# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 4, Computer Lab 09 (Friday 08:30–10:30)
Members and UG/PG applicability: Emmanuel Cadman (Emmanuel07-code, UG); Tanveer Uppal (TanveerUppal, UG); Tanzir Ahon (Tanzir1718, UG). UG-only group: common scope only. Stages 10 and 11 are not applicable, to be done by postgraduates only.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare common UG release 1.0. SmartCare A3 Requirements Baseline 2026, revision 2.
Common starting SHA / branch / applicable members: fdace4b (main, Merge pull request #10). Its project/ code is the same as the Stage 9 code SHA 5b31a55 (PR #9); PR #10 only added the Stage 9 record. All three members.
PG starting SHA / branch / applicable members or not applicable: Not applicable. UG-only group.
Working-state review and approved integration: Stages 6 to 9 are merged into main through PRs #1, #6, #7, #8, #9 and #10. A fresh clone of main at fdace4b has a clean working tree and the full suite passes (see C).
Protected common candidate and PG differences: The common candidate is the code at 5b31a55. No PG work exists, so there are no PG differences.
Feature freeze / owner / verifier: Feature freeze from fdace4b: no new features, only documentation and record changes. Owner: Tanveer Uppal. Verifier: [complete: name of another member].


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: **Do not release** yet. Passing tests only show the tested behaviour works. Another person could not set up and run the system from an incomplete README, an unreviewed dependency could add risk we have not checked, and users would not know about the hidden limitation. Fix all three, then release.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Tests T-32, test_f8_02_cancelled_appointment_can_still_be_found, test_listing_default_includes_cancelled_history; console run step 6 (D) | tests/test_services.py, tests/test_regressions.py at fdace4b | [complete] | Yes | None |
| Architecture responsibilities are appropriate | Code review in E: domain rules, store, services, pure query, console | project/smartcare/ at fdace4b | [complete] | Yes | None |
| Rescheduling is safe — PG only | Not applicable | Not applicable | Not applicable | Not applicable | UG-only group |
| AI use is responsible — common recheck / PG assurance | Copilot decisions recorded in Stages 6–9; final check in E | stage06–stage09 records | [complete] | Yes | PG assurance not applicable |
| System is maintainable | Small focused methods, docstrings, type hints, 60 meaningful tests, README | project/ at fdace4b | [complete] | Yes | Small debt items in G |
| FR-01–03 register/find and validation | T-01 to T-26, T-38 to T-41 | tests/test_domain.py, tests/test_services.py, tests/test_starter.py | [complete] | Yes | None |
| FR-04–05 booking/conflict rules | T-27 to T-30, T-42 to T-44, test_f8_01_same_practitioner_same_time_is_a_conflict | tests/test_services.py, tests/test_starter.py, tests/test_regressions.py | [complete] | Yes | None |
| FR-06–08 cancellation/history/find | T-11 to T-14, T-31 to T-37, T-45, test_f8_02 | tests/test_domain.py, tests/test_services.py, tests/test_regressions.py | [complete] | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | tests/test_queries.py (8 tests) and 5 listing tests | tests/test_queries.py, tests/test_services.py | [complete] | Yes | None |
| UI full console sequence and error recovery | Manual console run (D); Stage 9 section D | `python main.py --interactive` at fdace4b | [complete] | Yes | No automated console tests (G) |
| Session-only scope / FR-10 retired | Store is in memory only; README states data is lost on exit | data_store.py, project/README.md | [complete] | Yes | None |
| PG RES and assurance integration | Not applicable | Not applicable | Not applicable | Not applicable | UG-only group |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.13, pytest | project/, `python -m pytest -q` | fdace4b | 60 passed, 0 failed | screenshot (kept by the team) |
| Complete PG if applicable | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Affected focused checks after correction | Not applicable: no code was changed in Stage 12 | Not applicable | Not applicable | Not applicable | Not applicable |
| Full integrated recheck | Fresh clone of main | project/, `python -m pytest -q` | fdace4b | 60 passed, 0 failed | screenshot (kept by the team) |
Prior assertions preserved / reviewed test diff: Yes. Since Stage 7 (45 tests), Stage 8 added 2 regression tests and Stage 9 added 13 tests. No earlier test was removed or weakened: Stage 8 and 9 diffs to tests/ only add lines.
Remaining failure / limitation: None failing. Limitations are listed in G.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Not applicable (spoken) | A clinic needs to register patients and practitioners, book and cancel appointments and see a practitioner's schedule. Stakeholders: reception staff, practitioners, patients. | Explained in the demo | [complete] |
| Register and find Patient and two Practitioners | Options 1–4: P1 Alex Example; D1 Taylor Example, General practice; D2 Jordan Example, Cardiology | FR-01, FR-02, FR-03 | Each registered and found with the correct name and specialty | screenshot (kept by the team) |
| Valid booking | Option 5: A1, P1, D1, 2026-10-01 09:00 | FR-04 | `Booked: A1: P1 with D1, 2026-10-01 09:00, scheduled` | screenshot (kept by the team) |
| Same practitioner exact-time conflict rejected | Option 5: AX, P1, D1, 2026-10-01 09:00 | FR-05, AC-04.1 | `Error: Practitioner already has a SCHEDULED appointment at this time`; menu returned | screenshot (kept by the team) |
| Different practitioner same time allowed | Option 5: A2, P1, D2, 2026-10-01 09:00 | AC-04.2 | A2 booked as scheduled | screenshot (kept by the team) |
| Cancel SCHEDULED and retain/find CANCELLED object | Option 6: A1, then option 7: A1 | FR-06, FR-07, FR-08 | A1 shown as cancelled, then found again as cancelled | screenshot (kept by the team) |
| Invalid/repeated cancellation rejected | Option 6: A1 again | AC-05.3 | `Error: Only SCHEDULED appointments may be cancelled`; A1 stayed cancelled | screenshot (kept by the team) |
| Default all-status listing | Option 8: D1, blank status | FR-09 | A1 cancelled listed, `1 appointment(s) found.` | screenshot (kept by the team) |
| Explicit filtering / empty vs unknown / deterministic order | Option 8: D1 `scheduled`; D9 blank; then book A3 (D1, 09:00) and list D1 | QRY-01–04 | `0 appointment(s) found.`; `Error: Practitioner not found`; A3 booked in the freed slot; list shows A1 then A3 | screenshot (kept by the team) |
| Invalid date/status/menu/lookup recovery and continued operation | `not a date`, `2026-02-30 09:00`, status `pending`, blank patient ID, choice `99` | UI-02 | Each gave an `Error:` or `Unknown choice` message and the next action worked | screenshot (kept by the team) |
| Session-only limitation and normal exit | Option 0, then start again | Session-only scope | `Goodbye. Session data discarded.`; a new run starts empty | screenshot (kept by the team) |
| One meaningful requirement-linked pytest test explained | tests/test_services.py::test_cancelled_appointment_is_still_stored (T-32) | FR-07, AC-05.2 | It cancels A1, then asserts find_appointment('A1') is the same object and it is still in the list. It would fail if cancelling deleted or replaced the appointment. | tests/test_services.py |
| Architecture and one actual AI decision / known limitation | Stage 7 section H | Responsible AI | We rejected Copilot's mocked cancellation test because it used methods our code does not have and did not test the real rule. Known limitation: data is lost on exit. | stage07 record |
| PG reschedule identity/participants/time and no-op | Not applicable | Not applicable | Not applicable | Not applicable |
| PG conflict/invalid status/failure non-mutation | Not applicable | Not applicable | Not applicable | Not applicable |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable | Not applicable | Not applicable | Not applicable |
Stable demo owner / fresh process / command: [complete: demo owner]. Fresh process from project/: `python main.py --interactive`.
PG demonstrations through service/tests or not applicable: Not applicable. UG-only group.


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | domain.py, data_store.py, services.py, queries.py, console.py | No finding. Only console.py reads input and prints; the query uses only its arguments. | No change |
| PascalCase and snake_case naming | All modules | No finding. Classes are PascalCase (AppointmentService); functions and variables are snake_case. | No change |
| Useful type hints and meaningful docstrings | All modules | No finding. Every public function has type hints and a docstring. | No change |
| Four-space indentation and imports/layout | All modules | No finding | No change |
| Focused methods / duplication / dead or commented code | main.py | Finding (low): a leftover `# this is a test` comment, and main.py still catches NotImplementedError, which the finished menu no longer raises. Neither changes behaviour. | No change during feature freeze; recorded as debt in G |
| Globals / leakage / unnecessary inheritance or frameworks | All modules | No finding. No global store; no inheritance beyond Enum. | No change |
| No SQLite/persistence/repository ABCs/speculative features | All modules | No finding. In-memory store only. | No change |
| Synthetic data / secrets / dependencies / provenance | Whole repository | No finding. Synthetic names only (Alex/Taylor/Jordan Example); no secrets; only dependency is pytest 8.3.5 for tests. | No change |
| Significant common Copilot contributions and human verification | Stage 6–9 records | No Copilot-written code was accepted without checks. Stage 7 test rejected; Stage 8 diagnoses checked against evidence; Stage 9 review found no problems and was checked with tests. | No change |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | Not applicable | Not applicable | Not applicable |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Stage 9: "No problems found" in queries.py, services.py and console.py | QRY-01–04, FP-01–03, FR-09, UI-01–02 | Full suite and checks that the tests fail when the tie-break or purity is broken on purpose | Accept with caution: Copilot did not run any code | No change; 60 passed |
| Stage 8: F8-01 "wrong field compared" | FR-05, data_store.has_practitioner_conflict | Inspected the code: the fields were right, the `!=` operator was wrong | Modify: right place, wrong reason | Fixed `!=` to `==` in 03714c7 |
| Stage 7: mocked repeated-cancellation test | FR-06, AC-05.3 | Ran it: AttributeError, used methods our code does not have | Reject | Not kept; real tests T-12 and T-33 used |
Access route or approved equivalent / limitations: GitHub Copilot Chat in PyCharm (Stages 7–8) and VS Code (Stage 9), asked to reply in chat only, without editing files or running commands.
Available AI evidence and missing evidence honestly disclosed: Prompts and decisions are in the Stage 7, 8 and 9 records, with the Stage 9 screenshot in stage09/evidence/. [complete: AI-use statement, written by Tanveer Uppal]


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | README.md, project/README.md | [complete] | Present. Common UG scope. |
| Out-of-scope capabilities and known limitations | project/README.md | [complete] | Present: session-only, no PG rescheduling, no age/duration/past-date rules |
| Confirmed teaching Python version and dependency installation | project/README.md | [complete] | Present: Python 3.13, pytest 8.3.5, `python -m pip install -r requirements-dev.txt` |
| Working directory / demo / interactive / test commands | README.md, project/README.md | [complete] | Present: run from project/, `python main.py`, `python main.py --interactive`, `python -m pytest` |
| Repository structure and architecture responsibilities | README.md, project/README.md | [complete] | Present |
| Responsible AI summary / synthetic-data rule | README.md | [complete] | Present: Copilot is the nominated assistant; synthetic data only |
| Release label/version and SHA links | README.md group index | [complete] | Gap found: the verified SHA line still said "[complete after merge]". Fixed in this commit to 5b31a55 / fdace4b. |
Root README index and project/README verified: Yes, both open from the root and link correctly.
Fresh clone or extracted ZIP / candidate identity: Fresh clone of https://github.com/Emmanuel07-code/st1-assignment-3, main at fdace4b.
Verifier and clean environment / actual version: [complete: name], new folder with Python 3.13 and pytest.
Setup/run/test commands and observed results: `cd project`, `python main.py` printed the A1 demo booking and the session-only message; `python -m pytest -q`: 60 passed.
Missing local file or setup gap / remedy and recheck: None. All needed files are tracked; .gitignore excludes .venv, caches and Stage 8 working files.


## G Known limitations debt and release notes

Delivered features: Register and find patients and practitioners; book appointments with the practitioner conflict rule; cancel with retained history; find appointments; list a practitioner's appointments with an optional status filter in date/time then ID order; interactive console menu.
Important fixes: F8-01 conflict check (`!=` to `==`) and F8-02 cancelled lookup (status filter removed), both with regression tests (Stage 8).
Architecture/quality improvements: Magic status string replaced with AppointmentStatus.SCHEDULED (Stage 8); pure query with a named sort key kept separate from the store and console (Stage 9).
Known limitations: Data is lost on exit; exact-time conflicts only; no automated console tests.
AI-assisted development note: GitHub Copilot was used for review and test ideas; every suggestion was checked against the requirements and tests before being accepted, changed or rejected. [complete: add other AI use, if any]

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Leftover comment and unused NotImplementedError catch in main.py | None on behaviour; slightly untidy | Low | Remove both in a small refactor | Accepted: feature freeze; harmless |
| No automated console tests | Menu changes could break without a failing test | Medium | Add tests that feed input to run_menu | Accepted: menu checked manually in D and Stage 9 |
| No persistence | All data lost on exit | Low (by design) | Only if requirements change | Accepted: FR-10 retired |
Session-only synthetic data and minute-precision local time: Data exists only in one run. Times are local, at minute precision, with no timezone.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: None of these are included; they are outside the course scope.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: One user, one process, small data only; no timezone handling; no logging or monitoring; text menu only.
Difference between accepted scope limit and unresolved required behaviour: A scope limit (like no persistence) is something the requirements leave out on purpose. Unresolved required behaviour would be a requirement that does not work; we have none.
PG assurance residual risks / owner / status or not applicable: Not applicable. UG-only group.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| README release SHA (F) | Root README "Verified code SHA" said "[complete after merge]" | Low: release identity unclear | Tanveer Uppal: update the line | README.md: verified SHA set to 5b31a55 (code) / fdace4b (main) | README reread; no code changed, so tests not affected | None |
Justified no-change conclusion if no defect found: No code defect found. All 60 tests pass on a fresh clone and the full console demo works, so no code was changed in Stage 12.
Release blockers still open / status: None.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Stage 9 PR #9 (code, merged as 5b31a55) and PR #10 (record, merged as fdace4b). Stage 12 changes: stage12 record and README only.
Independent reviewer / feedback / response: Merging directly was approved by our tutor; the team reviews changes together in person before upload. [complete: reviewer name and feedback]
Integration commit / full recheck: fdace4b; fresh clone, 60 passed.
Tracked and untracked file inspection / cleanliness: `git status` clean on a fresh clone. Local-only files (for example stage08/test.md) are untracked and not submitted.
Secrets/staff material/caches/tool-metadata exclusion check: `git ls-files` shows no .venv, __pycache__, .env, Stage 8 utility or recovery files.
Candidate recovery plan / known-good SHA: Known-good code SHA 5b31a55. If a later change breaks something, check it out or revert to it and rerun the tests.
Named substantive contributions: Emmanuel Cadman: Stage 6 lookups and cancellation, Stage 7 tests and record, Stage 8 repairs and record. Tanveer Uppal: Stage 9 query, listing, console, tests, READMEs and record; Stage 12 record. Tanzir Ahon: [complete].


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: **READY WITH DOCUMENTED LIMITATIONS**
Approver / date / rationale and evidence: [complete: approver], [complete: date]. All common requirements are tested (60 passed), the demo works, and the limitations are written down in G and the README.
What risks remain / conditions / owners: No automated console tests; session-only data. Both accepted and documented. Owner: the team.
Can the team explain the system: Yes. Each member can explain the domain, store, services, query and console, and one test (D).
Can a change be recovered: Yes. All work is in Git history with known-good SHA 5b31a55.
Common decision / PG decision where different: Common: ready with documented limitations. PG: not applicable.


## K Final tested release SHA

Exact common tested SHA: fdace4b (main). Its project/ code is identical to 5b31a55.
Exact PG tested SHA or not applicable: Not applicable.
Final submitted SHA / repository URL: The commit that adds this Stage 12 record [complete: SHA], https://github.com/Emmanuel07-code/st1-assignment-3
Evidence-only later commit and difference explanation: The final commit only changes stage12/stage12_activities_and_evidence.md and README.md. No code or tests change.
Executable changes after testing and re-verification: None.
Source ZIP name / SHA correspondence / extracted comparison: [complete: ZIP name], made with `git archive` from the final submitted commit, so it holds only tracked files. Extracted and checked: 60 passed.


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [x] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [complete]
Deadline/timezone: [complete]
Repository access arrangement: Public repository: https://github.com/Emmanuel07-code/st1-assignment-3
Mixed-candidate upload arrangement: Not applicable. UG-only group.
Oral/video recording/accessibility arrangements: [complete]
Remaining administration or release dependency: [complete]


## M Formative questions

1. What is a release candidate?

Response: A specific, tested version of the software that the team proposes to release, identified by an exact commit SHA. Ours is fdace4b.

2. What is feature freeze and why is it used?

Response: A point after which no new features are added, only fixes and documentation. It keeps the tested version stable so the release is not broken by late changes.

3. What is regression testing in a release context?

Response: Rerunning all existing tests on the release candidate to make sure nothing that worked before is now broken. We ran all 60 tests on a fresh clone.

4. What is a known limitation?

Response: Something the system does not do, written down so users know about it. For example, SmartCare loses all data when it exits.

5. What is technical debt?

Response: Shortcuts or untidy parts that work now but make future changes harder, like the leftover comment in main.py or having no automated console tests.

6. What are release notes?

Response: A short summary of what is in a release: new features, fixes, improvements and known limitations (see G).

7. What is software maintenance?

Response: Work done after release to fix bugs, adapt to new needs and keep the code clean, like the Stage 8 repairs and refactor.

8. What is the purpose of the individual demonstration/viva?

Response: To show that each member understands the system and their own contribution, and can explain the code and tests without relying on AI.

9. What should the final responsible-AI check establish before release?

Response: That all significant AI help was disclosed, every AI suggestion was checked by a person against requirements and tests, and nothing unverified or invented was kept.

10. What is the main course conclusion about AI and the role of the software engineer?

Response: AI can suggest code, tests and diagnoses quickly, but the engineer is still responsible for understanding the requirements, checking the evidence and deciding what is correct.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: 60 passing tests traced to the requirements, plus a full console demo on a fresh clone.
Weakest area: The console has no automated tests; it was only checked by hand.
How AI use changed from Stage 1 to Stage 12: At first we were tempted to trust Copilot's answers. By Stages 7 and 8 we wrote our own idea first, then treated Copilot's output as a hypothesis and checked it with tests and code.
Start doing — engineering and AI use: Write tests for the console, and ask Copilot for specific checks instead of general reviews.
Stop doing — engineering and AI use: Leaving placeholder text and leftover comments until the end.
Continue doing — engineering and AI use: Human idea first, small focused commits, and running the full suite after every change.
What worked / caused rework / future delivery improvement: Small branches per stage and regression tests worked well. The accidental revert of PR #1 in Stage 6 caused rework. Next time, protect main and complete records alongside the code.
One paragraph — If AI can write code why do we still need software engineers: AI can write code quickly, but it does not know what the users actually need or whether its code is correct. In this project Copilot suggested a test that used methods our code did not have, and a diagnosis that pointed at the right line for the wrong reason. A software engineer turns needs into clear requirements, checks AI output against tests and evidence, makes the final decisions and is responsible for the result.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | A clinic needs to manage patients, practitioners and appointments in one session. Stakeholders: reception staff, practitioners, patients. |
| Two requirements and acceptance criteria | FR-05: the same practitioner cannot have two SCHEDULED appointments at the exact same time (AC-04.1); different practitioners can (AC-04.2). FR-07: cancelled appointments are kept and can be found (AC-05.2). |
| Domain model and architecture | Patient, Practitioner and Appointment (with AppointmentStatus) in domain.py; one shared SmartCareDataStore; three services; a pure query; the console. |
| Design trade-off | The query takes a list as input instead of reading the store. It needs one extra argument, but it stays pure and easy to test. |
| Meaningful test and its limits / 100 percent coverage | T-32 proves cancelled history is kept (D). It does not test the console. Even 100% coverage would only show that lines ran, not that they were checked. |
| Diagnosed defect and verification | F8-02: find_appointment skipped cancelled appointments. Removed the status filter; test_f8_02 failed before and passed after (Stage 8 D). |
| Shared store and session-state/query responsibilities | All services share one store so they see the same objects. The query only filters and sorts the list it is given. |
| What would break if session-state lookup/query responsibilities changed? | If each service had its own store, a booked appointment could not find its registered patient. If the query read the store or sorted in place, it would no longer be pure and the purity tests would fail. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancel only needs the appointment's own status, so Appointment protects it. A conflict needs other appointments in the store, so the service coordinates it. |
| FR-07 retained history test | test_cancelled_appointment_is_still_stored and test_listing_default_includes_cancelled_history. |
| Actual AI change rejected/modified or honestly accepted with verification | Rejected Copilot's mocked test in Stage 7; modified its F8-01 diagnosis in Stage 8. |
| Unresolved limitation / future production work | No persistence and no automated console tests. Production would need saving data, logins and console tests. |
| Personal implementation contribution | [complete: each member] |
| Personal test/review/design/integration contribution | [complete: each member] |
| PG agentic change and rescheduling verification | Not applicable. UG-only group. |
| PG responsible-AI risk/remediation or supported no finding | Not applicable. UG-only group. |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.
Separate reflection / peer / common team viva evidence links and routing: [complete]
No further coding stage. Later corrections use the published assessment process.