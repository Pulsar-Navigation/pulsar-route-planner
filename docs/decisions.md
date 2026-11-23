# Decisions
 
A short log of design choices and why they were made. Add a new entry when a choice affects how the code is structured or how results are interpreted.
Parameter values (antenna area, bandwidth, minimum elevation and so on) belong in `assumptions.md`.
 
Entry format: **Decision**, **Why**, **Alternatives considered**, **Status**.
 
---
 
## 1. Language and outputs
 
- **Decision:** Python, with Plotly for interactive HTML plots. Inputs and outputs are plain JSON (configs, schedules) and CSV (flat tables).
- **Why:** the astronomy tools (`astropy`, `psrqpy`) exist in Python, and the same language can be reused in later projects. Plain file formats let other modules read the outputs without depending on this code.
- **Alternatives considered:** C#. It has no equivalent astronomy libraries, so coordinate and time-scale handling would have to be written by hand.
- **Status:** accepted.
## 2. Development environment and CI
 
- **Decision:** Nix (`flake.nix`) for the local development environment. CI uses plain Python (`actions/setup-python` and `pip`) and only runs the tests.
- **Why:** the first CI run built scipy, matplotlib and astropy from source through Nix and was cancelled after about 29 minutes. CI only needs to check that the tests pass.
- **Trade-off:** CI installs packages from PyPI, while the local shell uses versions pinned by `flake.lock`, so the two environments can differ.
- **Status:** accepted.
## 3. Workflow
 
- **Decision:** one issue per pull request, work on a branch created from the issue, squash merge into `main`, and require the `test` check to pass.
- **Why:** keeps `main` working and gives a readable history, with each pull request recording why a choice was made.
- **Status:** accepted.
## 4. Slice 1: select four pulsars for one place and time
 
- **Decision:** the first slice of the planner chooses the best four pulsars for a single location and a single UTC time. The route, the time grid and the schedule come in later slices.
- **Why:** it is the smallest piece that exercises the core of the planner (visibility, integration time, geometry and selection) and can be tested on its own.
- **Why four pulsars:** four unknowns have to be solved, the three position coordinates and the receiver clock offset, so at least four independent pulsar measurements are needed.
- **Status:** accepted.
### Interface
 
- **Function:** `select_four_pulsars(lat_deg, lon_deg, time_utc)` in `planner/selection.py`.
- **Inputs:** latitude and longitude in degrees, and a timezone-aware `UTC datetime`. The receiver assumptions and the pulsar catalogue default to the config and the cached data.
- **Return value:** a `Selection` object with a `pulsars` list of four entries. Further fields (GDOP, total integration time, a "no solution" flag) are added in later issues.
- **Why plain values as inputs:** 
the function does not depend on any file format, so a test, a command-line tool or a later route loop can all call it. Files are read and written at the edges, in `io.py`.
- **Why a skeleton test first:** it fixes the signature before the code exists.
  The test is skipped until the selection is implemented.
- **Status:** accepted.
## Open questions
 
Items to settle with the coach. Move each one into a numbered entry above once it is decided.
 
- Target timing precision per pulsar
- How the best set of four is chosen (lowest GDOP only, or a GDOP threshold with
  the shortest total integration time)
- Minimum elevation angle for a visible pulsar
- Which receiver assumptions to use as the reference
 