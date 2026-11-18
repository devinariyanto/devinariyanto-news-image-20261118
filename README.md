# THE WORLD ON WEDNESDAY — 18 NOVEMBER 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/devinariyanto/devinariyanto-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/devinariyanto/devinariyanto-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A single 1024×576 TV news broadcast frame that sums up Wednesday
18 November 2026's world news in one image. Drawn entirely with PIL
primitives — no photos, no network. The lead story is the US–Iran
Gulf strikes; the other five stories run in the headline rail.

## The six stories

1. **US–IRAN GULF STRIKES (lead)** — US jets hit a Revolutionary
   Guard missile launcher site on Qeshm Island in the Strait of
   Hormuz; Iran answered with drone strikes on Kuwait (Ali Al Salem
   Air Base) and Bahrain (a US radar site). Source: Reuters.
2. **KERCH BRIDGE HIT** — Ukrainian drones and missiles partly
   brought down the Kerch Bridge to Crimea; a road span collapsed
   into the strait. The second day of attacks.
3. **XI–PUTIN MEET IN SHENZHEN** — Xi Jinping and Vladimir Putin
   met in Shenzhen ahead of Thursday's trilateral summit with Trump;
   they condemned protectionism and Western sanctions. APEC summit.
4. **PELTOLA WINS ALASKA** — Democrat Mary Peltola beat Republican
   incumbent Dan Sullivan for Alaska's Senate seat; Democrats 56–44,
   their biggest majority since 2009. Confirmed by AP.
5. **EBOLA IN DR CONGO PASSES 11,000 CASES** — The DR Congo Ebola
   outbreak passed 11,000 cases, doubling in 3 months; 5,400 deaths;
   the second-largest outbreak ever; children hit hardest. UN.
6. **VOYAGER 1 REACHES ONE LIGHT-DAY** — Voyager 1 reached one
   light-day from Earth (~16 billion miles) at 05:16 ET; the
   farthest human-made object ever. NASA JPL.

Ticker: "US loses measles-free status after 26 years as cases pass
5,400." and "Israel elects Matan Kahana as Knesset speaker."

## How to make the image

```sh
python3 gen_image.py   # writes entry.png (1024x576, <= 1 MiB)
```

## How to run

```sh
python3 main.py        # validates entry.png, copies it to $MAKEFUN_OUTPUT_DIR
```

`main.py` uses only the Python standard library, makes no network
calls, and is deterministic: two runs on the same `entry.png` produce
byte-identical output. Set `MAKEFUN_OUTPUT_DIR` to choose the output
folder (default `/output`).

## Files

- `entry.png` — the entry image (1024×576 PNG, ≤ 1 MiB)
- `gen_image.py` — renders `entry.png` with PIL
- `main.py` — validates and copies `entry.png` to the output folder
- `README.md` — this file
- `LICENSE` — MIT
- `.makefun/owner.json` — owner wallet
