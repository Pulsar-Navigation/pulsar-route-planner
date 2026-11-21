<img src="docs/pulsar-star-icon-mark-in-filled-style-vector.jpg" alt="Logo of the project" width="100">

# Pulsar Route Planner

> Observation planning for radio-pulsar navigation on large ocean-going vessels

Given a ship's voyage, the planner works out which pulsars a ship mounted receiver should observe, when, in which direction and for how long. It is the observation-planning module of a larger radio-pulsar navigation (RPN) concept, developed as part of the Radio Astronomy Track Honors project at TU/e.

**Status:** work in progress, targeting v0.1.0 (first end-to-end run). Sections marked *(planned)* describe intended behaviour that is not implemented yet.

## Motivation

GNSS can be jammed, spoofed or lost. Radio pulsars are stable natural timing sources that cannot be jammed or spoofed in practice, so a pulsar-derived position can serve as an independent **backup** and **integrity check** for open-ocean navigation. It is not a replacement for GNSS: pulsar fixes are expected to be accurate to kilometres and need minutes to hours of integration per pulsar.

Pulsar signals are extremely weak, so the receiver cannot track everything at once. It needs a plan: which pulsars are above the horizon along the route, which are quick enough to detect, and which combination gives good position geometry.

## What it does *(planned)*

1. Reads a voyage (departure, arrival, start time, constant ship speed) and receiver assumptions from a JSON config.
2. Loads pulsar parameters from a cached PSRCAT subset.
3. Computes ship position along a great-circle route and each pulsar's altitude and azimuth on a fixed time grid.
4. Estimates the integration time each pulsar needs and ranks them.
5. Selects sets of at least four pulsars with good geometry (dilution of precision, DOP).
6. Outputs an observation schedule (JSON), a ranked pulsar list (CSV) and an interactive Plotly plot (HTML) .


## Installing / Getting started

You need Git and Nix (see [Prerequisites](#prerequisites)).

```shell
git clone https://github.com/Pulsar-Navigation/pulsar-route-planner.git
cd pulsar-route-planner/
nix develop
```

`nix develop` opens a shell with the exact Python version and tools the project uses. Running the planner on the sample route *(planned)*:

```shell
python -m planner examples/rotterdam-new-york.json
```

## Developing

### Built with

- [Python](https://www.python.org/) 3.12
- [Nix](https://nixos.org/) flakes for the development environment
- [PSRCAT](https://www.atnf.csiro.au/research/pulsar/psrcat/) pulsar catalogue, accessed via [psrqpy](https://psrqpy.readthedocs.io/)
- [Astropy](https://www.astropy.org/), NumPy, SciPy for coordinates and numerics
- [Plotly](https://plotly.com/python/) for visualization
- [pytest](https://docs.pytest.org/) and [Ruff](https://docs.astral.sh/ruff/) for testing and linting

### Prerequisites

- **Git**: <https://git-scm.com/downloads>
- **Nix** with flakes enabled: <https://nixos.org/download/> (the [Determinate Systems installer](https://determinate.systems/nix-installer/) enables flakes by default)
- Optional: [Jujutsu (jj)](https://jj-vcs.github.io/jj/latest/install-and-setup/) as a Git-compatible client

### Setting up the dev environment

```shell
git clone https://github.com/Pulsar-Navigation/pulsar-route-planner.git
cd pulsar-route-planner/
nix develop
```

We use `nix develop` so that everyone runs the same pinned Python version, packages and tools. The versions are recorded in `flake.lock`, which makes results reproducible and citable.

### Project structure *(to be modified)*

```
pulsar-route-planner/
├── flake.nix / flake.lock
├── pyproject.toml
├── .editorconfig
├── .gitignore
├── README.md
├── LICENSE
├── src/planner/
│   ├── __init__.py
│   ├── voyage.py
│   ├── visibility.py
│   ├── scoring.py
│   ├── geometry.py
│   ├── scheduler.py
│   ├── io.py               # reading configs, writing JSON/CSV
│   └── plotting.py
├── tests/
│   ├── test_voyage.py
│   ├── test_visibility.py
│   ├── test_scoring.py
│   ├── test_geometry.py
│   └── test_scheduler.py
├── examples/               # sample voyage configs
├── scripts/                # fetch_catalogue.py and other helpers
├── data/                   # cached PSRCAT subset (data/scratch/ ignored)
├── docs/                   # assumptions.md, decisions.md, rfcs
├── outputs/                # generated, ignored
└── .github/
    ├── pull_request_template.md
    └── workflows/ci.yml
```

### Building

The planner is a Python package and needs no compile step. After changing code (re-enter the Nix shell if `flake.nix` changed) run the checks in [Tests](#tests) and [Style guide](#style-guide).

### Workflow

- `main` always works.
- One branch per piece of work (`feature/...`, `fix/...`, `docs/...`).
- Changes go through pull requests, squash-merged into `main`.
- Assumptions go in `docs/assumptions.md` and design choices in `docs/decisions.md`.

### Deploying / Publishing

The planner is not deployed to a server. A release is a tagged version of the repository:

```shell
git tag v0.1.0
git push origin v0.1.0
```

This marks the exact code that produced a set of results, so a report can cite it. Releases can also be created from GitHub's Releases page.

## Versioning

We use [SemVer](https://semver.org/) (`MAJOR.MINOR.PATCH`). While the project is at `0.x`, the interface may change between minor versions. See the [tags on this repository](https://github.com/Pulsar-Navigation/pulsar-route-planner/tags) for available versions.

## Configuration

The planner reads a JSON file *(planned; field names may change before v0.1.0)*:

```json
{
  "voyage": {
    "departure": {"name": "Rotterdam", "lat": 51.95, "lon": 4.14},
    "arrival": {"name": "New York", "lat": 40.66, "lon": -74.04},
    "departure_time": "2026-12-01T08:00:00Z",
    "speed_knots": 18
  },
  "receiver": {
    "collecting_area_m2": 100,
    "bandwidth_mhz": 200,
    "system_temperature_k": 50,
    "frequency_mhz": 1400,
    "min_elevation_deg": 20,
    "max_integration_s": 3600,
    "slew_time_s": 60
  }
}
```

| Field | Meaning |
|---|---|
| `departure`, `arrival` | Latitude and longitude in degrees |
| `departure_time` | UTC, ISO 8601 |
| `speed_knots` | Constant ship speed |
| `collecting_area_m2`, `bandwidth_mhz`, `system_temperature_k` | Reference receiver, used in the radiometer equation |
| `min_elevation_deg` | A pulsar counts as visible above this altitude |
| `max_integration_s` | Pulsars needing longer than this are marked unusable |
| `slew_time_s` | Fixed time to re-point between pulsars |

The values above are placeholders. The assumptions actually used, and their justification, are listed in `docs/assumptions.md`.

## Outputs *(planned)*

| File | Content |
|---|---|
| `schedule.json` | Observations with pulsar, start and end time, pointing (altitude and azimuth) and integration time, plus the config and software version used |
| `ranked_pulsars.csv` | Candidate pulsars ranked by estimated integration time |
| `altitude_plot.html` | Interactive plot of visible and selected pulsars over the voyage |

## Tests

Run inside `nix develop`:

```shell
pytest
```

The tests cover the core maths: great-circle distance and position (against a known distance), altitude and azimuth (against an independent sky calculator), the DOP calculation (well-spread sets give a low value, clustered sets a high value, fewer than four pulsars gives "no solution") and schedule consistency (no overlapping observations, every selected pulsar visible during its window).

## Style guide *(planned)*

Formatting and linting use Ruff, configured in `pyproject.toml` (line length 100; rules `E`, `F`, `I`, `B`, `UP`). Run the full local check before every commit:

```shell
ruff check . && ruff format --check . && pytest
```

To fix issues automatically:

```shell
ruff check --fix .
ruff format .
```

## Database and data
 
The planner has no database server. Its only data source is the **ATNF Pulsar Catalogue (PSRCAT)**, a public catalogue of known pulsars maintained by the Australia Telescope National Facility (CSIRO).
 
- **Source:** <https://www.atnf.csiro.au/research/pulsar/psrcat/>
- **Access:** through the [`psrqpy`](https://psrqpy.readthedocs.io/) Python package, which queries the catalogue and returns tables.
- **Citation:** Manchester et al., *The Astronomical Journal* 129, 1993-2006, 2005 (see [References](#references)).

### Parameters used
 
| Parameter | Used for |
|---|---|
| Name (J2000 and B names) | Identifying the pulsar in outputs |
| Right ascension, declination | Direction vector for visibility (altitude and azimuth) and DOP |
| Period (P0) | Reference only in v0.1.0; needed later for folding |
| Dispersion measure (DM) | Reference only in v0.1.0; needed later for dedispersion |
| Flux density (e.g. S400, S1400) | Estimating SNR and the integration time needed |
| Pulse width (W50) | Estimating timing precision (sharper pulses are better) |
 
### How the data is handled *(planned)*
 
- **Cached subset.** The planner runs offline from a subset stored in `data/` (CSV or JSON), so results are reproducible and need no network access.
- **Refresh script.** A separate script rebuilds the subset from PSRCAT via `psrqpy` *(planned)*. It also records the query date and catalogue version next to the data, so a result can be traced to the catalogue it used.
- **Incomplete entries.** Pulsars with missing flux density or W50 are excluded, and the number excluded is reported.
- **Flux scaling.** Catalogue flux densities are measured at specific frequencies (such as 400 MHz or 1400 MHz), not at the ship receiver's band. How they are scaled, for example with a spectral index where available, is documented in `docs/assumptions.md`.
- **Selection.** The subset keeps only pulsars that could plausibly be useful (bright enough, sharp enough). The cut-offs are documented in `docs/assumptions.md`.

- **Scratch data.** Larger downloads go in `data/scratch/`, which is ignored by Git.

## API reference
 
Not applicable. The planner is a command-line tool that reads and writes files, and it has no external API.
 
## References
 
- H. Hesselink et al., *PulsarPlane: D5.4 Final Report*, NLR-CR-2015-243-PT16, 2015.
- A. A. Kestilä et al., "An Extensive and Autonomous Deep Space Navigation System Using Radio Pulsars", IAC-10.B2.4.8, 2010.
- R. N. Manchester et al., "The Australia Telescope National Facility Pulsar Catalogue", *The Astronomical Journal* 129, 1993-2006, 2005.


## Licensing

See the [LICENSE](LICENSE) file in the repository root for the license text.
