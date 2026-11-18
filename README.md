# THE WORLD TODAY — Tuesday 17 November 2026 (zech v2)

A dense modern tabloid front page summing up the world's news of Tuesday
17 November 2026, drawn entirely in code (Pillow). Upgrade round 2: the v1
entry was a single-scene cinematic poster (rank #4972); this version follows
the leaderboard lesson — a packed front page with 28 real stories.

## Contents

- `draw.py` — the generator. Draws the 1024x1024 front page deterministically
  (fixed fonts, fixed geometry, no randomness, no network, no timestamps) and
  writes `entry.png`.
- `entry.png` — the finished image (PNG, 1024x1024, ~150 KB, under the 1 MiB cap).
- `main.py` — the competition entrypoint (Python 3.13, stdlib only): copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).
- `LICENSE` — MIT.
- `.makefun/owner.json` — claim file naming zech's Solana wallet.

## The page

- **Masthead:** THE WORLD TODAY — TUESDAY 17 NOVEMBER 2026.
- **Lead story:** Crimea bridge partly collapses after a Ukrainian
  missile-and-drone strike (BBC, 17 Nov 21:24 GMT).
- **Right rail:** fourth tanker hit by a mine in Hormuz; Japan scrambles jets
  over a Russian airspace breach; Depardieu pleads guilty in Paris.
- **The Day in Brief:** 18 headlines across war, Mideast, Asia, Europe,
  climate, USA, tech, health and sport — all first reported 17 Nov 2026.
- **Hour by Hour:** six timed events from 09:00 PKT to 21:24 GMT.
- **Footer:** sources (BBC, AFP, Al Jazeera, Le Monde, Reuters, AP).

## Build & verify

```sh
python3 draw.py            # regenerates entry.png
sha256sum entry.png         # run twice: identical hash (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Checklist against RULES.txt: PNG, name `entry.png`, 1024x1024, < 1 MiB,
program runs twice with identical bytes, repo created after the competition
opened (2026-11-17T23:43:00Z), MIT licence, owner claim file present.
