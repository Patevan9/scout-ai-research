# Scout AI Lab Runner

A standalone, PC-based test harness for running Scout Intelligence Test
v1's RAW cases against local models — completely separate from the Scout
Android app. It does not require Scout to run, and it never modifies
`Patevan9/Scout`.

**Status: Canonical Context Renderer / Option B pipeline proven with mocks
and synthetic/pilot data only. No real model has been loaded or run.**
The full pipeline is now enforced by construction:

    canonical context -> Canonical Context Renderer -> RenderedContext
      -> ModelAdapter -> InferenceBackend

`lab_runner/` contains: the canonical fixture schema + loader/validator;
`render_canonical_context()`, the single deterministic function that
turns a canonical fixture dict into a `RenderedContext`
(`RenderedContext`/`RenderedTurn` are the model-neutral boundary — see
[ADR-0006](../docs/decisions/0006-canonical-context-renderer.md)); the
approved `ModelAdapter`/`InferenceBackend` interfaces, where every
adapter (`MockAdapter`, `TinyLlamaChatMLAdapter`) receives only a
`RenderedContext`, never the raw fixture dict; and a mock backend
proving the pipeline end to end with no real model. `run_case()` always
renders before calling an adapter. There is still no real inference
backend and no TinyLlama installed or run. Benchmark Profile v1 —
RAW-only, scoped to the 9 currently committed fixtures — is now approved;
see `../benchmarks/benchmark-profile-v1.md`. No inference has been run
under it yet.

The full design (platform choice, model-adapter boundary, fixture and
result schemas, scoring approach, Benchmark Profile process, and the
implementation sequence) was reviewed and approved by Patrick and
ChatGPT before this structure was created. See `SCOUT_AI_STATUS.md` and
`RESEARCH_LOG.md` in the repository root for the current state of that
approval and what step comes next.

## Layout so far

- `config/` — hand-maintained configuration, starting with an empty
  model registry scaffold (`models.yaml`).
- `fixtures/` — holds the real RAW benchmark test-case fixtures (YAML),
  one per Scout Intelligence Test v1 case. Three pilot fixtures are
  committed so far — `B1.yaml`, `D2.yaml`, `F1.yaml` — validated against
  the current schema; the remaining cases have not been created yet.
  (Synthetic, plumbing-only fixtures used purely by automated tests live
  under `lab_runner/tests/fixture_data/`, kept deliberately separate from
  this directory.)
- `results/` — will hold benchmark result records (JSON). Empty for now —
  no benchmark has been run.
- `models/` — where local model binary files (e.g. `.gguf`) would be
  placed for testing. Its contents are gitignored — model binaries are
  never committed to this repository. See `models/README.md`.
- `lab_runner/` — the Python package. `adapter.py`/`backend.py` define
  the approved interfaces; `renderer.py` defines
  `render_canonical_context()` and `RendererError`;
  `rendered_context.py` defines the `RenderedContext`/`RenderedTurn`
  dataclasses; `mock_adapter.py`/`tinyllama_chatml.py` are the two
  concrete `ModelAdapter` implementations (the latter is prompt
  formatting only — not a real inference backend); `mock_backend.py` is
  a stand-in that proves the pipeline without any real model;
  `runner.py` is the orchestration function that renders canonical
  context and wires an adapter and a backend together;
  `fixture_schema.py`/`fixtures_loader.py` define and enforce the
  canonical RAW fixture schema; `tests/` has the automated tests,
  including synthetic-only fixture data. Run all of them with:
  ```
  cd lab
  python3 -m unittest discover -s lab_runner/tests -t . -v
  ```

No TinyLlama or any other real model file has been downloaded or run. No
real inference backend exists yet — only the mock. `requirements.txt`
lists exactly one dependency so far: PyYAML, for parsing fixtures.
