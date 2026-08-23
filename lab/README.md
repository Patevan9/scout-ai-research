# Scout AI Lab Runner

A standalone, PC-based test harness for running Scout Intelligence Test
v1's RAW cases against local models — completely separate from the Scout
Android app. It does not require Scout to run, and it never modifies
`Patevan9/Scout`.

**Status: architecture plumbing + fixture validation proven with mocks
and synthetic data only. No real model has been loaded or run.**
`lab_runner/` contains the approved `ModelAdapter`/`InferenceBackend`
interfaces, a mock adapter and mock backend proving the
`canonical context → adapter → backend → result` pipeline end to end,
and the canonical fixture schema + loader/validator, proven against one
valid and one intentionally invalid synthetic fixture. There is still no
real inference backend, no TinyLlama, no real benchmark fixtures, and no
Benchmark Profile.

The full design (platform choice, model-adapter boundary, fixture and
result schemas, scoring approach, Benchmark Profile process, and the
implementation sequence) was reviewed and approved by Patrick and
ChatGPT before this structure was created. See `SCOUT_AI_STATUS.md` and
`RESEARCH_LOG.md` in the repository root for the current state of that
approval and what step comes next.

## Layout so far

- `config/` — hand-maintained configuration, starting with an empty
  model registry scaffold (`models.yaml`).
- `fixtures/` — will hold the real RAW benchmark test-case fixtures
  (YAML), one per Scout Intelligence Test v1 case. Still empty — no real
  fixtures have been created yet. (Synthetic, plumbing-only fixtures used
  purely by automated tests live under `lab_runner/tests/fixture_data/`,
  kept deliberately separate from this directory.)
- `results/` — will hold benchmark result records (JSON). Empty for now —
  no benchmark has been run.
- `models/` — where local model binary files (e.g. `.gguf`) would be
  placed for testing. Its contents are gitignored — model binaries are
  never committed to this repository. See `models/README.md`.
- `lab_runner/` — the Python package. `adapter.py`/`backend.py` define
  the approved interfaces; `mock_adapter.py`/`mock_backend.py` are
  stand-ins that prove the pipeline without any real model;
  `runner.py` is the orchestration function that wires an adapter and a
  backend together; `fixture_schema.py`/`fixtures_loader.py` define and
  enforce the canonical RAW fixture schema; `tests/` has the automated
  tests, including synthetic-only fixture data. Run all of them with:
  ```
  cd lab
  python3 -m unittest discover -s lab_runner/tests -t . -v
  ```

No TinyLlama or any other real model file has been downloaded or run. No
real inference backend exists yet — only the mock. `requirements.txt`
lists exactly one dependency so far: PyYAML, for parsing fixtures.
