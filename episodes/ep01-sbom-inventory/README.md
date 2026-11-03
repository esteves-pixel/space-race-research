# EP01 · What is inside open-source space software?

A software bill of materials (SBOM) is the ingredients list for a program. We checked nine open-source space software repositories: which publish one, which have a security policy, which accept private bug reports.

**Result, 2 Nov 2026: of 9 repositories, 1 publishes an SBOM.** Same result on 15 Oct.

- `data/sbom-inventory-<date>.json` / `.md` — each dated snapshot.
- Rerun it: `python3 tools/space_sbom_inventory.py` (needs the GitHub CLI, `gh`, signed in; reads public data only). The definitions of what counts are in the script header.
- Replay a saved run without the network: `python3 tools/space_sbom_inventory.py --from-json episodes/ep01-sbom-inventory/data/sbom-inventory-2026-11-02.json --no-write`
