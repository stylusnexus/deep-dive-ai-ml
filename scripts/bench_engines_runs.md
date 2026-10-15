# Engine runs behind the numbers in the latency-and-caching lesson

Recorded 2026-10-02 with `scripts/bench_engines.py`. These are single runs on one machine
that was also running other work (load average between 5 and 57 during the session), so they
show direction, not rates. They are here so that every figure in the lesson can be traced.

- Machine: Apple M4 Max, 128 GB unified memory (sysctl reports 137,439,000,000 bytes, which is 128 GiB), macOS (Darwin 27.2)
- Engine: vllm-mlx 0.5.0 from PyPI in a Python 3.12 venv (mlx 0.32.3, mlx-lm 0.32.0); 0.4.1 for the first crash
- Models: mlx-community/Qwen2.5-1.5B-Instruct-4bit (cache, batching), mlx-community/Qwen3.5-9B-MLX-8bit (thinking, disk-tier retry)

## Prefix reuse, default mode
`vllm-mlx serve MODEL` then `bench_engines.py --model MODEL prefix --lengths 2000 6000 --trials 2 --repeats 2`

```
machine load average 5.5 on 16 cores  <- busy: close other apps or expect noisy numbers
 words prompt tok          cold  same request  new question     next turn    front edit
  2000      2,360         1.75s         0.09s         0.09s         0.09s         3.14s
  6000      7,071         5.18s         0.12s         0.12s         0.13s         5.51s

2 trials per length, 2 repeats of each warm kind per trial; medians of TTFT.
A warm column close to `cold` means that kind of reuse is NOT cached on this engine.
```

## Prefix reuse, continuous batching
`vllm-mlx serve MODEL --continuous-batching`, same command

```
machine load average 5.5 on 16 cores  <- busy: close other apps or expect noisy numbers
 words prompt tok          cold  same request  new question     next turn    front edit
  2000      2,359         3.40s         4.42s         0.75s         0.62s         4.32s
  6000      7,074        14.93s        15.66s         1.17s         1.20s        15.16s

2 trials per length, 2 repeats of each warm kind per trial; medians of TTFT.
A warm column close to `cold` means that kind of reuse is NOT cached on this engine.
```

## Batching, final run (machine quieter, load average about 7)
Default mode against `--continuous-batching`, `batching --concurrency 1 4 8 --tokens 400`.

```
default mode
streams    ok  aggregate tok/s  per-stream tok/s     wall
      1   1/1            308.6             316.2     1.3s
      4   1/4            311.7             317.3     1.3s
      8   1/8            309.8             316.0     1.3s

--continuous-batching
streams    ok  aggregate tok/s  per-stream tok/s     wall
      1   1/1            290.1             297.1     1.4s
      4   4/4            799.4             218.9     2.0s
      8   8/8            428.5              54.7     7.5s
```

In default mode the server log reports `SimpleEngine serialized route is busy` for each
rejected request, and the client receives an empty stream. An earlier batching run on the
same mode, made before the script counted failures, printed a flattering aggregate for 4
streams; that figure was wrong and is not used anywhere.

## Disk tier
`--continuous-batching --cache-memory-mb 250 --ssd-cache-dir DIR`, 1.5B 4-bit text model.
vllm-mlx 0.4.1 and 0.5.0 both aborted on the first eviction:
`libc++abi: terminating due to uncaught exception of type std::runtime_error: There is no Stream(cpu, N) in current thread.`
Related upstream changes: waybarrios/vllm-mlx pull requests 563 (merged) and 602 (not merged).
The 9B 8-bit model on the same flags did not crash, but ran through the multimodal scheduler:
no cache stores or evictions were logged, nothing was written to the disk-tier directory, and
the warm control was no faster than cold. That run exercised nothing and is inconclusive.

## Thinking, 9B 8-bit, `--reasoning-parser qwen3`
`thinking --arm on='{}' --arm off='{"chat_template_kwargs":{"enable_thinking":false}}' --max-tokens 1500`
(run before the script flagged cut-off replies; rows with 1,502 tokens reached the cap)

```
arm         q  tokens think chars first token first answer    total  right
on          1     565        1339       0.18s       17.81s    22.3s    yes
off         1     135           0       0.24s        0.24s     6.8s    yes
on          2    1258        2467       0.24s       44.67s    57.3s    yes
off         2     447           0       0.38s        0.38s    20.4s    yes
on          3    1192        3503       0.44s       45.34s    48.8s    yes
off         3     214           0       0.42s        0.42s     8.7s    yes
on          4    1502        2525       0.43s       56.46s    58.3s     NO
off         4     499           0       0.40s        0.40s    18.8s    yes
on          5     979        2280       0.43s       31.30s    36.7s    yes
off         5     338           0       0.46s        0.46s    12.6s    yes
on          6    1502        2822       0.38s          n/a    55.3s     NO
off         6     463           0       0.38s        0.38s    17.0s    yes

per arm: median tokens, median total time, answers right
  on            1225 tok    52.0s  4/6 right
  off            392 tok    14.8s  6/6 right

first answer is n/a when the engine leaves thinking inline in the content.
6 questions show direction, not a rate. Do not quote the right column as accuracy.
```

## Five engines, one model (the table in the formats-and-engines lesson)
Qwen2.5-1.5B-Instruct. GGUF: qwen2.5-1.5b-instruct-q4_k_m.gguf, 1,117,320,736 bytes. MLX: mlx-community/Qwen2.5-1.5B-Instruct-4bit, group size 64, 4 bits, 839 MB. Commands: `prefix --lengths 2000 6000 --trials 2 --repeats 2`, then `batching --concurrency 1 4 --tokens 300`, then `staggered --long-tokens 1500 --shorts 2`, each against the engine alone. These ran between 10:02 and 10:08 on 2026-10-02 while another benchmark was running on the same Mac; the load average printed by each run is in the output. The vllm-mlx default-mode run in particular overlapped heavy load, which is why its single-stream rate (40.9 tokens per second) is far below the 308.6 measured in the quieter run above. Read these as direction only. The identical-request miss with continuous batching (1.05 s against 0.95 s cold at 2,359 tokens; 3.90 against 3.95 at 7,072) appears here and, with different absolute times, in the continuous-batching prefix run earlier in this file.

### llama-server, GGUF Q4_K_M, -np 4 -c 49152 -ngl 99

```
### llamacpp  (10:02)
machine load average 6.5 on 16 cores  <- busy: close other apps or expect noisy numbers
 words prompt tok          cold  same request  new question     next turn    front edit
  2000      2,357         1.02s         0.01s         0.03s         0.04s         1.20s
  6000      7,073         3.85s         0.02s         0.04s         0.05s         3.68s
machine load average 6.0 on 16 cores  <- busy: close other apps or expect noisy numbers
streams    ok  aggregate tok/s  per-stream tok/s     wall
      1   1/1            176.5             181.2     1.7s
      4   4/4            102.1              25.9    11.7s
machine load average 6.9 on 16 cores  <- busy: close other apps or expect noisy numbers
short request alone, idle server   :   0.07s
short #0 while a long one runs     :   0.10s
short #1 while a long one runs     :   0.10s
long request total                 :  10.65s  (1270 tokens)
```

### Ollama 0.33.3 running the same GGUF (Modelfile, num_ctx 16384)

```
### ollama  (10:07)
machine load average 7.7 on 16 cores  <- busy: close other apps or expect noisy numbers
 words prompt tok          cold  same request  new question     next turn    front edit
  2000      2,357         0.66s         0.02s         0.03s         0.05s         0.60s
  6000      7,074         3.03s         0.03s         0.06s         0.09s         4.20s
machine load average 6.9 on 16 cores  <- busy: close other apps or expect noisy numbers
streams    ok  aggregate tok/s  per-stream tok/s     wall
      1   1/1             88.0              89.5     3.4s
      4   4/4             69.6              74.2    17.2s
machine load average 11.3 on 16 cores  <- busy: close other apps or expect noisy numbers
short request alone, idle server   :   0.05s
short #0 while a long one runs     :  17.19s
short #1 while a long one runs     :  16.92s
long request total                 :  17.15s  (1500 tokens)
```

### mlx_lm.server 0.31.3, MLX 4-bit

```
### mlxlm  (10:03)
machine load average 6.1 on 16 cores  <- busy: close other apps or expect noisy numbers
 words prompt tok          cold  same request  new question     next turn    front edit
  2000      2,360         0.73s         0.08s         0.10s         0.10s         0.68s
  6000      7,072         3.33s         0.09s         0.12s         0.13s         3.65s
machine load average 5.9 on 16 cores  <- busy: close other apps or expect noisy numbers
streams    ok  aggregate tok/s  per-stream tok/s     wall
      1   1/1            206.6             223.0     1.5s
      4   4/4            107.8              31.9    10.0s
machine load average 5.7 on 16 cores  <- busy: close other apps or expect noisy numbers
short request alone, idle server   :   0.30s
short #0 while a long one runs     :   1.80s
short #1 while a long one runs     :   1.50s
long request total                 :  44.49s  (1500 tokens)
```

### vllm-mlx 0.5.0 default mode, MLX 4-bit

```
### vllmmlx_default  (10:04)
machine load average 22.7 on 16 cores  <- busy: close other apps or expect noisy numbers
 words prompt tok          cold  same request  new question     next turn    front edit
  2000      2,360         2.62s         0.11s         0.11s         0.15s         2.41s
  6000      7,072         6.55s         0.18s         0.20s         0.23s         6.83s
machine load average 14.2 on 16 cores  <- busy: close other apps or expect noisy numbers
streams    ok  aggregate tok/s  per-stream tok/s     wall
      1   1/1             40.9              41.5     7.3s
      4   1/4             50.8              51.9     5.9s
machine load average 12.9 on 16 cores  <- busy: close other apps or expect noisy numbers
short request alone, idle server   :   0.06s
short #0 while a long one runs     :   0.01s   (EMPTY: no tokens came back)
short #1 while a long one runs     :   0.01s   (EMPTY: no tokens came back)
long request total                 :  12.02s  (1500 tokens)
```

### vllm-mlx 0.5.0 --continuous-batching, MLX 4-bit

```
### vllmmlx_cb  (10:06)
machine load average 14.3 on 16 cores  <- busy: close other apps or expect noisy numbers
 words prompt tok          cold  same request  new question     next turn    front edit
  2000      2,359         0.95s         1.05s         0.09s         0.07s         1.07s
  6000      7,072         3.95s         3.90s         0.09s         0.12s         3.91s
machine load average 9.7 on 16 cores  <- busy: close other apps or expect noisy numbers
streams    ok  aggregate tok/s  per-stream tok/s     wall
      1   1/1            257.3             268.7     1.2s
      4   4/4            317.8              83.8     3.8s
machine load average 9.3 on 16 cores  <- busy: close other apps or expect noisy numbers
short request alone, idle server   :   0.05s
short #0 while a long one runs     :   0.15s
short #1 while a long one runs     :   0.15s
long request total                 :  10.14s  (1500 tokens)
```

## Earlier runs, printed in the session and not saved as files
- First prefix run on vllm-mlx 0.5.0 default mode with no warmup request: 500 words cold 2.34 s, 2000 words cold 2.14 s, 6000 words cold 13.66 s. A rerun a few minutes later on the same server: 2000 words cold 6.54 s, 6000 words cold 25.52 s. That is the factor of three between two runs of one configuration quoted in the benchmarking lesson. The machine was busy both times.
- Early batching run, default mode, under load average 13.6: 1 stream 8.7 tokens per second, "4 streams" about 9.2 with three of the four requests rejected (the script did not yet count failures). Continuous batching, same run: 1 stream 10.3, 4 streams 29.5, a ratio of 2.9. This is the "9 tokens per second" figure in an earlier draft of the latency lesson; it was replaced by the 308 and 41 comparison above because the early run was also under load.
- Final batching run (quiet machine) is the one in the Batching section above: 290.1 to 799.4 with continuous batching, 2.8 times. The five-engine run measured 257.3 to 317.8 for the same configuration, 1.2 times, under load. Both are in this file.

## Observations from logs and help text
- vllm-mlx 0.5.0 default mode, concurrent request: server log line `SimpleEngine serialized route is busy` for each rejected request.
- vllm-mlx 0.4.1 shutdown log: `[lifespan] Saving prefix cache to ~/.cache/vllm-mlx/prefix_cache/mlx-community--Qwen2.5-1.5B-Instruct-4bit` and `SAVED 2/2 entries ... (194MB total)`; the next server's first request logged `entries=2`, so the entries were loaded at startup.
- `vllm-mlx serve --help` for 0.5.0: `--continuous-batching  Enable continuous batching for multiple concurrent users (slower for single user)`.
