# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-003.
- **Status:** APP-003 implementation kept and learner record approved; preparing PR.
- **Next step:** Commit/push kept changes, open PR and verify latest CI before merge.
- **Implementation marker:** `studio.json` is at `implemented_through: 3` after passing cumulative checks.

This repository owns application code. Server/proxy changes and production
deployment are outside these three local-development lessons. Prepared helpers
are reusable foundations, not evidence that unfinished routes are implemented.

## APP-001 · Branded homepage

**Scope:** make the neutral FastAPI homepage express one chosen identity with
a simple original SVG mark, coherent copy, navigation and shared style tokens.
Keep account actions honest about their unfinished state.

| Decision | Agreement |
|---|---|
| Visitor and concrete use situation | Gen Z students exploring approachable budgeting alongside a social life |
| Reused IS117 brand, or name / promise / primary archetype | FunnyMoney; build better money habits without giving up your social life; playful supportive companion (AI archetype label: Everyperson) |
| One visible choice and visitor benefit | Consistent pixel typography and inviting landscape; learner links consistency to brand credibility and playful styling to approachability |
| Own issue / branch / PR | Issue https://github.com/dhruvi0805/my-app-studio/issues/1; codex/app-001-funnymoney; PR https://github.com/dhruvi0805/my-app-studio/pull/2 merged |

**Keep when:** the agreed identity is visible and usable at desktop/narrow widths;
full foundation + APP-001 checks pass; AI review and the learner's actual check
interpretation/browser observation/keep reason are recorded; reviewed evidence
and verified GitHub state are linked below.

## APP-002 · Signup, login and logout

**Scope:** add browser forms and REST behavior for member signup, login, a private
dashboard and logout backed by SQLite. Reuse the prepared password/JWT/CSRF/session
helpers; keep data local. New accounts cannot choose their role.

| Decision | Agreement |
|---|---|
| Expected public/private behavior and account flow | Signup creates a member; anonymous /dashboard redirects to /login; login shows username/member status; logout revokes session and redirects to /login |
| Valid and rejected cases to demonstrate | Valid signup/login; reject duplicate/invalid signup, role input, wrong credentials, missing CSRF and revoked/expired sessions |
| Own issue / branch / PR | https://github.com/dhruvi0805/my-app-studio/issues/3; codex/app-002-accounts; PR https://github.com/dhruvi0805/my-app-studio/pull/4 merged |

**Keep when:** the agreed forms/API work; duplicate/invalid signup and wrong
credentials are rejected; passwords are hashed; authentication uses validated,
expiring JWTs with protected cookies and CSRF; private requests require a live
session and logout revokes it. Full cumulative checks, AI review, actual learner
contributions and GitHub state are recorded. This is not a production-security certification.

## APP-003 · Server-enforced roles

**Scope:** enforce a small member/admin boundary in the API and browser. Assign
roles only through the trusted local terminal command; use current server-side
permissions, including for an existing session after a role change.

| Visitor | Homepage | Member area | Admin area/API |
|---|---|---|---|
| Anonymous | Allowed | Login required | Login required |
| Member | Allowed | Allowed | Forbidden |
| Admin | Allowed | Allowed | Allowed |

| Decision | Agreement |
|---|---|
| Intended admin-only result | Project status at /admin and /api/admin; anonymous login required, member forbidden, admin allowed. Role changes affect existing sessions on next request |
| Actual allowed/denied request evidence | /api/admin: anonymous 401, member 403, admin 200; same session after downgrade 403. HTML anonymous redirects to login and members receive 403. Verified in isolated Chromium and cumulative contracts |
| Own issue / branch / PR | https://github.com/dhruvi0805/my-app-studio/issues/5; codex/app-003-roles; PR Pending |

**Keep when:** a direct request cannot bypass the role boundary, role changes
take effect as specified, new signup remains member-only, and full cumulative
checks plus AI review pass. Link the learner's actual interpretation/observation,
reviewed record and verified GitHub result. Hidden navigation alone is insufficient.

## Evidence

Link actual files/checks and the student's own issues/PRs. No fabricated URLs,
customer research or claims that a timestamp proves learning.

| Feature | Files / own issue / PR | Actual checks and learner observations | Kept / GitHub state |
|---|---|---|---|
| APP-001 | app/brand.json, templates/home.html, templates/base.html, static/site.css, static/logo.svg, static/pig.svg, static/fonts; issue #1 | Full check: 98 foundation/tooling/helper tests, 2 APP-001 contracts, 2 Chromium checks passed; fonts, sticky header and overflow inspected at 390/768/1440px; learner contributions in LEARNING.md | PR #2 merged, issue #1 closed; both main CI jobs and local merged-main checks verified passing |
| APP-002 | app/features/accounts.py, app/templates/account.html, app/templates/dashboard.html, app/static/site.css, tests/test_accounts_boundary.py; issue #3 | Full check: 100 foundation/helper/boundary tests, 14 cumulative contracts, 2 Chromium journeys passed. Learner login/logout observation in LEARNING.md | PR #4 merged; issue #3 closed; both main CI jobs and local merged-main checks verified passing |
| APP-003 | app/features/roles.py, app/templates/admin.html, app/templates/forbidden.html; issue https://github.com/dhruvi0805/my-app-studio/issues/5; codex/app-003-roles | Full check: 100 foundation/helper/boundary tests, 18 cumulative contracts, 2 Chromium journeys passed; learner member/promotion/downgrade observations and interpretation in LEARNING.md | Learner kept behavior and approved record; PR/CI/merge Pending |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.

### APP-001 local agreement
FunnyMoney homepage for Gen Z students: build better money habits without giving up your social life. Friendly, playful companion character; Everyperson is the AI-proposed archetype label. Learner selected retro 8-bit pixel art and teal #006D77, aqua #7FDBFF, cream #FFF8E1, yellow #FFD166, coral #FF7F7F. Dark ink supports readable text. Original SVG pig, shared styles and concept copy only; accounts, bank connections and budgeting tools remain unfinished.
Files: app/brand.json, app/templates/home.html, app/templates/base.html, app/static/logo.svg, app/static/site.css.
Branch: codex/app-001-funnymoney. Learner supplied issue: https://github.com/dhruvi0805/my-app-studio/issues/1 (verified open through GitHub API with APP-001 marker and agreed scope). Full checks passed; learner inspected and kept current design.

Revision agreement: full-width light-blue pixel sky, clouds, grass, cute pig/coin; consistent Pixelify Sans headings and Oxanium body, dark green/navy text, yellow highlights, pixel buttons and sticky navigation. Learner requested revision because font inconsistency and monotonous color could distract visitors and weaken credibility. Fonts served locally with OFL licenses. Full revised checks passed; learner inspected and chose to proceed.

Kept final iteration: green continuation below grass, cream/yellow text, shaded blue sky with more clouds, layered multi-strand grass and learner-supplied pig.svg with background cleaned. Prior version was staged as an iteration checkpoint. Learner subsequently kept the latest iteration and approved the evidence for publication.

APP-002 agreed scope: signup/login forms and REST endpoints, private dashboard showing username/member status, logout with server revocation. Anonymous dashboard requests redirect to /login; authenticated requests show the current account. No budgeting feature or admin routes. Issue https://github.com/dhruvi0805/my-app-studio/issues/3 verified open with APP-002 marker; branch codex/app-002-accounts. Reject duplicate/invalid signup, signup role input, wrong login, missing CSRF and revoked sessions. Use prepared password hashing, signed expiring JWT cookies, SQLite and limits. Full checks passed; learner inspected login/logout and chose to keep.

APP-002 local validation: full explicit cumulative check passed (100 foundation/helper tests, 14 APP-001/002 contracts, 2 Chromium journeys). AI inspected desktop signup and narrow member layout; all account pages fit 390px. Added tests/test_accounts_boundary.py for expired database sessions and HTML role injection. Browser forms and JSON endpoints share prepared signup/login/logout services. Marker set to 2 after explicit check; normal full check also passed. Learner inspected login/logout, kept the flow and approved the record. Direct /dashboard revisit not explicitly reported; AI checked the redirect.

APP-003 agreement: small read-only admin project status page/API using the prepared trusted role helper. Signup stays member-only. Database role is checked on every request, including after promotion/downgrade in existing sessions. No public role editor or budgeting feature. Files: app/features/roles.py, app/templates/admin.html, app/templates/forbidden.html. Full checks passed; learner inspected member denial, promotion and downgrade and chose to keep.

APP-003 validation: full explicit check passed (100 foundation/helper/boundary tests, 18 cumulative contracts, 2 Chromium journeys). AI inspected desktop/narrow admin and forbidden pages and verified trusted role command promotion/downgrade in an existing session with a disposable database. No overflow at 390/1440px. Normal full check after marker change also passed. Learner interpreted the downgrade check, reported member/promotion/downgrade behavior, chose to keep it and approved the summary.
