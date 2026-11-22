# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/agielthree/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/agielthree/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up Sunday, 22 November 2026 — the make.fun bounty "Sum up 22 November's world news in one image" ($100 in USDC, top 50 share the table).

`entry.png` is a 1024x1024 newspaper front page headed "THE WORLD IN ONE DAY — Sunday, 22 November 2026", with six stories: Iran's IRGC missile and drone strikes on US positions in Bahrain, with a civilian industrial site hit and set on fire and no casualties; the COP31 climate summit in Antalya running into a second day of overtime, deadlocked after the final draft dropped all mention of fossil fuels, with Panama threatening to block a deal without oil output limits; Mexico capturing cartel boss 'El Chapo Isidro' (Fausto Isidro Meza-Flores) in Guasave, Sinaloa, with 11 killed in the raid; the Russian cargo ship Sparta II hit by drones and burning in the Gulf of Finland, drifting into Finnish waters with 16 crew evacuated, as Poland accused Russia of a deliberate provocation; the FBI investigating a reported breach of its NCIC criminal database — the second FBI system hit in months; and an overloaded boat capsizing in Bayelsa, Nigeria, carrying mourners to a funeral, with at least 24 dead and 24 rescued out of as many as 300 people on board.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` from the repository root into the output directory, where the gate reads it — `out/entry.png` is byte for byte the repository's `entry.png`. The poster is rendered by `draw_poster.py` (Pillow, DejaVu fonts) with a fixed palette, fixed fonts and fixed geometry, so running it twice produces a byte-identical `entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=zkm03re7&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
