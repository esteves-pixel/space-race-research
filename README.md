# Space Race 3.0 — the research behind each episode

I run a show on AI and space security for people who own small companies and want to work in space.
Each episode has a **page** on my site for reading, and a folder **here** so you can check the work:
the sources, the data, and the code that produced every number of my own.

| Episode | Topic | Page | Folder |
|---|---|---|---|
| EP00 | The map: what is up there, what is on the ground, the four connections between them | https://goncaloesteves.io/space-race/ | [episodes/ep00-the-map](episodes/ep00-the-map) |
| EP01 | Which open-source space software tells you what is inside it (a software bill of materials) | https://goncaloesteves.io/space-race/ | [episodes/ep01-sbom-inventory](episodes/ep01-sbom-inventory) |
| EP03 | The View from Above: satellites and our planet (chapter 9 of *Red Moon Rising*) | https://goncaloesteves.io/space-race/ep03/ | [episodes/ep03-view-from-above](episodes/ep03-view-from-above) |

## Page or repo?
- **The page** is for reading: the story, the questions, what we found. Written for people.
- **The repo** is for checking and reusing: every source as data, the scripts, the dated snapshots, and the history of every change. Written for people who want to verify, rerun or correct.

## The rules this repo follows
1. **Every claim has a source**, and every source is labelled by type (primary, secondary, company claim, advocacy, state media).
2. **Every number is dated.** A snapshot says "of these 9 repositories on 2 Nov 2026", never "nobody".
3. **My own numbers come with the code that made them** (see `tools/`). Rerun it and you should get the same table, or a newer one.
4. **Corrections are public.** They go in [CORRECTIONS.md](CORRECTIONS.md) with a date, and the old version stays in the git history.
5. **What is not here:** anyone's contact details, who we plan to interview, and anything that explains how to attack a system. We report what has been reported, not how to do it.

## Spot an error?
Open an issue. Say which file and which line, and link a better source.

## Licence
Code (`tools/`): MIT. Text and data: CC BY 4.0, credit "Gonçalo Esteves, Space Race 3.0". Each source keeps its own copyright; we link to it and summarise it in our own words.

— Gonçalo Esteves
