# Teacher-Model Transfer Workflow

**This is an infrastructure/ops tool, not a Scout AI research finding or
architecture decision.** It does not touch `docs/decisions/`,
`RESEARCH_LOG.md`, `SCOUT_AI_STATUS.md`, `SCOUT_AI_RESEARCH_IDEAS.md`,
benchmarks, fixtures, or scoring, and it never touches `Patevan9/Scout`.

## Problem it solves

Uploading the ~700MB llama.cpp GGUF shards of the Qwen3-8B-Q8_0 teacher model
from a Windows client to a GitHub Release repeatedly failed with TLS/network
errors, across multiple tools, networks, and TLS backends. GitHub-hosted
Actions runners have their own normal outbound internet access and are not
subject to that client's network path, so the workflow
([`.github/workflows/transfer-teacher-model.yml`](../.github/workflows/transfer-teacher-model.yml))
downloads, splits, and uploads the model entirely on the runner instead.

## What it does

1. Confirms the target release (`qwen3-8b-q8_0-teacher`) exists and runs a
   real `df` disk-space preflight check before downloading anything.
2. Downloads the official GGUF (`Qwen/Qwen3-8B-GGUF`, file
   `Qwen3-8B-Q8_0.gguf`) and hard-aborts if its size or SHA-256 don't
   exactly match the known-good values below, before ever splitting it.
3. Obtains an `llama-gguf-split` binary (prebuilt llama.cpp release asset,
   self-checked at runtime; falls back to a source build of just that
   target), and records the exact llama.cpp tag/ref and commit used.
4. Splits the model with `--split-max-size 700M` (the same parameters
   already validated locally: 13 shards, ~667-690MB each, final ~517MB).
5. Uploads, verifies, and deletes each shard **as soon as it is complete**,
   rather than waiting for the whole split to finish. This keeps peak local
   disk usage to roughly the original file plus two in-flight shards, not
   the original plus a full second copy of the shard set -- see "Disk
   strategy" below for why that's safe.
6. Uploads a `SHA256SUMS.txt` manifest and rewrites the release description
   to describe the 13-shard plan (replacing an earlier, stale "five shards"
   description left over from an earlier attempt).

## Known-good source values

- Model: `Qwen/Qwen3-8B-GGUF`, file `Qwen3-8B-Q8_0.gguf`
- Size: `8,709,518,112` bytes
- SHA-256: `408b955510e196121c1c375201744783b5c9a43c7956d73fc78df54c66e883d6`
- Target release: tag `qwen3-8b-q8_0-teacher` in this repo

## Disk strategy

`gguf-split` opens the source file once and keeps it open for the entire
split; it writes shards strictly one at a time, fully closing each one
before starting the next (confirmed by reading
`tools/gguf-split/gguf-split.cpp` upstream, not assumed). That means the
appearance of shard *N+1*'s file on disk is itself proof that shard *N* is
finished and safe to upload and delete -- there's no need to wait for the
whole split to complete first. The workflow's watcher loop uses exactly
that signal (and, for the final shard, the splitter process's own exit).

## Idempotency / resumability

Before uploading any shard, the workflow checks whether a release asset
with that exact filename already exists:

- Filename, size, and GitHub's reported SHA-256 `digest` all match the
  local shard -> already complete, skip re-uploading it.
- An asset with that filename exists but size or digest differs -> hard
  failure with the mismatch reported. It is never silently overwritten or
  deleted.

After every upload, the workflow re-queries the asset and verifies its
`state` is `uploaded`, its size matches, and its digest matches the SHA-256
computed locally immediately before upload -- only then is the local shard
file deleted.

## Running it

Manually triggered only (`workflow_dispatch`, no inputs) from the Actions
tab of this repository. It performs no action on push, schedule, or pull
request.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
