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
3. Obtains an `llama-gguf-split` binary **pinned to llama.cpp release
   `b10700`** -- the exact build the repo owner used to produce the
   locally-validated split (prebuilt Linux release asset, self-checked at
   runtime; falls back to a source build of that same pinned tag, never
   "latest"), and records the exact commit used. See "Reproducibility"
   below for why the pin matters and how it was verified.
4. Splits the model with `--split-max-size 700M` (the same parameters
   already validated locally: 13 shards, ~667-690MB each, final ~517MB).
5. Verifies each shard's SHA-256 against the repo owner's known-good,
   locally-validated hash for that exact shard number **before** uploading
   it, hard-failing without uploading on any mismatch. Only then uploads,
   verifies against GitHub's own reported digest, and deletes each shard
   **as soon as it is complete**, rather than waiting for the whole split
   to finish. This keeps peak local disk usage to roughly the original file
   plus two in-flight shards, not the original plus a full second copy of
   the shard set -- see "Disk strategy" below for why that's safe.
6. Uploads a `SHA256SUMS.txt` manifest and rewrites the release description
   to describe the 13-shard plan (replacing an earlier, stale "five shards"
   description left over from an earlier attempt).

## Reproducibility

The goal isn't just *a* valid 13-shard split -- it's reproducing the repo
owner's exact, already-validated shard bytes, so the known-good per-shard
SHA-256 values below are meaningful checks rather than a moving target.
That requires pinning the exact llama.cpp build, not "latest":

- `gguf-split`'s entire write path was read directly from the `b10700`
  source (`tools/gguf-split/gguf-split.cpp`, `ggml/src/gguf.cpp`): metadata
  lives in an order-preserving `std::vector` (not a hash map, so there's no
  STL-implementation-dependent ordering risk), every value is written as
  its raw in-memory byte representation (no locale-dependent text, no
  timestamps, no embedded file paths), and tensor payload bytes are copied
  verbatim from the source file. Windows x64 and Linux x64 are the same
  little-endian architecture family, so those raw byte writes are
  platform-invariant between them.
- Empirically confirmed: running the actual `b10700` Linux binary twice,
  independently, against the same source file with the same
  `--split-max-size` produced byte-for-byte identical shards both times.
- The prebuilt Linux asset for this exact tag
  (`llama-b10700-bin-ubuntu-x64.tar.gz`) was located, downloaded, and
  confirmed to contain a working `llama-gguf-split` before being relied on
  here. It ships with its own shared libraries, so the workflow keeps the
  whole extracted directory together and sets `LD_LIBRARY_PATH` accordingly
  rather than moving the binary out on its own.

No source of non-determinism was found anywhere in the split path.

## Known-good source values

- Model: `Qwen/Qwen3-8B-GGUF`, file `Qwen3-8B-Q8_0.gguf`
- Size: `8,709,518,112` bytes
- SHA-256: `408b955510e196121c1c375201744783b5c9a43c7956d73fc78df54c66e883d6`
- Target release: tag `qwen3-8b-q8_0-teacher` in this repo
- Split with llama.cpp `b10700`, `--split-max-size 700M`

Per-shard SHA-256, from the repo owner's locally-validated split (also
hardcoded in the workflow and checked against each shard before it's
uploaded):

| Shard | SHA-256 |
|---|---|
| 00001 | `0050a1c014f88a65679cfb6dd98640853eb8f3846e89a9b141f081b74308db59` |
| 00002 | `cad2eaefa3611b159bd43c0096f438ffd16b1812281bd9b2350b4801d9f70767` |
| 00003 | `b42dec2d52587d30a2ea927963fe5b6d8dc55f7dd1dbbd9a8eb64ec428607a9f` |
| 00004 | `ec86f890116a6650b5636597ec64d4a65b3a7b31421f53b80bf8c75fec050602` |
| 00005 | `60d172f51486cab1f31c8e387e9a05f6854917be90ecec49624a630a7873f245` |
| 00006 | `7eabc0ebff6e236bed09687fbe37fb3bf90152fbec2e12b26c078eb62b083a39` |
| 00007 | `b9e45cc5990fb4a0e44d168b37a9122b1358d222b4a883135095f45a0299b529` |
| 00008 | `ee7f2474be81cd3337ab314090fac2271e8e82236c02eaf9846029aa868ad5ca` |
| 00009 | `f16ac9fe8f60892b6d5b2c281a7a8403ea260f8505613ce3d111f52440f99dbe` |
| 00010 | `21fb78cd7864921065d04d0556710bc217b8a2779e79d56262ee37989a85bb3c` |
| 00011 | `b012a730a0e9721d07dd2ee7cf78ff7df4d9da12b6d57ffc134c41004258ef7c` |
| 00012 | `38b55a1be69bea55fc8df8a0375a5d8a82106fda7779b0f824c5bde530014063` |
| 00013 | `18b3174fda8a493bfd4ba99e006d80930b1aff074c14aa609fc6a52efa397930` |

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
