# Scout AI Lab Runner

A standalone, PC-based test harness for running Scout Intelligence Test
v1's RAW cases against local models — completely separate from the Scout
Android app. It does not require Scout to run, and it never modifies
`Patevan9/Scout`.

**Status: structure only. No code has been written yet.** This directory
currently exists to establish the approved project layout and the
`models/` gitignore protection — nothing here performs inference, loads a
model, or runs a benchmark.

The full design (platform choice, model-adapter boundary, fixture and
result schemas, scoring approach, Benchmark Profile process, and the
implementation sequence) was reviewed and approved by Patrick and
ChatGPT before this structure was created. See `SCOUT_AI_STATUS.md` and
`RESEARCH_LOG.md` in the repository root for the current state of that
approval and what step comes next.

## Layout so far

- `config/` — hand-maintained configuration, starting with an empty
  model registry scaffold (`models.yaml`).
- `fixtures/` — will hold the RAW benchmark test-case fixtures (YAML).
  Empty for now — no fixtures have been created yet.
- `results/` — will hold benchmark result records (JSON). Empty for now —
  no benchmark has been run.
- `models/` — where local model binary files (e.g. `.gguf`) would be
  placed for testing. Its contents are gitignored — model binaries are
  never committed to this repository. See `models/README.md`.

No TinyLlama or any other model file has been downloaded or run. No
inference code exists yet.
