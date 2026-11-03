#!/usr/bin/env python3
"""Paper 1's original number: which open-source space software projects publish an SBOM
or a security policy. Public GitHub data only, read-only, via the `gh` CLI.

  python3 tools/space_sbom_inventory.py            # writes episodes/ep01-sbom-inventory/data/sbom-inventory-<date>.{json,md}
  python3 tools/space_sbom_inventory.py --no-write # on air: screen table only, writes no files
  python3 tools/space_sbom_inventory.py --from-json episodes/ep01-sbom-inventory/data/sbom-inventory-2026-10-15.json
                                                     # offline fallback: replays a saved run
  --json  also print the raw tally

What counts (definitions are the claim; change them here, never in the prose):
  security policy   GitHub reports a security policy for the repo (repo or org-level SECURITY.md)
  private reporting the repo accepts private vulnerability reports through GitHub
  advisories        security advisories the maintainers PUBLISHED on the repo
  SBOM (maintainer) a file in the default branch, or an asset on the last 10 releases, whose
                    name says sbom / spdx / cyclonedx / bom.json. GitHub's own auto-generated
                    dependency-graph export does NOT count: every public repo has one, nobody chose it.
                    Build tooling that generates an SBOM when YOU compile (e.g. a .cmake target) is
                    counted separately as "SBOM at build", not as published: no SBOM file exists to read.
A snapshot, dated. Bound every sentence built on it: "of these N repos on <date>", never "nobody".
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess

REPOS = [
    ("cFS", "nasa/cFS", "NASA Core Flight System (bundle)"),
    ("cFS", "nasa/cFE", "cFS core executive"),
    ("cFS", "nasa/osal", "cFS OS abstraction layer"),
    ("F Prime", "nasa/fprime", "NASA JPL flight software framework"),
    ("Yamcs", "yamcs/yamcs", "Mission control / ground"),
    ("OpenC3 COSMOS", "OpenC3/cosmos", "Command and control / ground"),
    ("CryptoLib", "nasa/CryptoLib", "CCSDS Space Data Link Security library"),
    ("SLE tools", "yamcs/jsle", "Java Space Link Extension library"),
    ("SLE tools", "visionspacetec/sle-provider", "SLE provider (archived)"),
]
SBOM_RE = re.compile(r"(sbom|spdx|cyclonedx|(^|/)bom\.(json|xml))", re.I)
DATA_EXT = re.compile(r"\.(json|xml|spdx|zip|tag\.value)$", re.I)
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "episodes/ep01-sbom-inventory/data"


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode != 0:
        return None, (r.stderr or r.stdout).strip()[:200]
    return json.loads(r.stdout) if r.stdout.strip() else None, None


def check(repo):
    owner, name = repo.split("/")
    row = {"repo": repo, "errors": []}
    q = ('query($o:String!,$n:String!){repository(owner:$o,name:$n){isArchived pushedAt '
         'isSecurityPolicyEnabled securityPolicyUrl defaultBranchRef{name} '
         'latestRelease{tagName publishedAt}}}')
    d, e = gh("api", "graphql", "-f", f"query={q}", "-F", f"o={owner}", "-F", f"n={name}")
    if e:
        row["errors"].append(f"graphql: {e}")
        return row
    r = d["data"]["repository"]
    row.update(archived=r["isArchived"], pushed_at=r["pushedAt"][:10],
               security_policy=bool(r["isSecurityPolicyEnabled"]),
               security_policy_url=r["securityPolicyUrl"],
               latest_release=(r["latestRelease"] or {}).get("tagName"),
               latest_release_date=((r["latestRelease"] or {}).get("publishedAt") or "")[:10])
    branch = r["defaultBranchRef"]["name"]

    d, e = gh("api", f"repos/{repo}/private-vulnerability-reporting")
    row["private_reporting"] = None if e else bool(d.get("enabled"))
    if e:
        row["errors"].append(f"private-reporting: {e}")

    d, e = gh("api", f"repos/{repo}/security-advisories?state=published&per_page=100")
    row["advisories_published"] = None if e else len(d)
    if e:
        row["errors"].append(f"advisories: {e}")

    d, e = gh("api", f"repos/{repo}/git/trees/{branch}?recursive=1")
    if e:
        row["errors"].append(f"tree: {e}")
        tree_hits, truncated = [], None
    else:
        tree_hits = [t["path"] for t in d["tree"] if t["type"] == "blob" and SBOM_RE.search(t["path"])]
        truncated = d.get("truncated")
    d, e = gh("api", f"repos/{repo}/releases?per_page=10")
    asset_hits = [] if e else [f"{rel['tag_name']}/{a['name']}" for rel in d for a in rel["assets"]
                               if SBOM_RE.search(a["name"])]
    data_files = [p for p in tree_hits if DATA_EXT.search(p)]
    tooling = [p for p in tree_hits if p not in data_files]
    row.update(sbom_files=data_files, sbom_tooling=tooling, sbom_release_assets=asset_hits,
               tree_truncated=truncated, sbom_published=bool(data_files or asset_hits),
               sbom_at_build=bool(tooling))
    return row


YN = {True: "yes", False: "no", None: "?"}


def screen_row(r):
    sbom = "YES" if r.get("sbom_published") else ("build" if r.get("sbom_at_build") else YN[r.get("sbom_published")])
    adv = "?" if r.get("advisories_published") is None else str(r["advisories_published"])
    flag = " *" if r["errors"] else ""
    return f"{sbom:<6} {r['repo']:<28} {YN[r.get('security_policy')]:<7} {YN[r.get('private_reporting')]:<8} {adv:>4}{flag}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--from-json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    print(f"{'SBOM':<6} {'repository':<28} {'policy':<7} {'private':<8} {'adv':>4}")
    if a.from_json:
        saved = json.loads(pathlib.Path(a.from_json).read_text())
        today, rows = saved["date"], saved["rows"]
        for r in rows:
            print(screen_row(r))
        a.no_write = True
    else:
        today = dt.date.today().isoformat()
        rows = []
        for project, repo, what in REPOS:
            row = check(repo)
            row.update(project=project, what=what)
            rows.append(row)
            print(screen_row(row), flush=True)

    n = len(rows)
    tally = {
        "repos": n,
        "with_security_policy": sum(1 for r in rows if r.get("security_policy")),
        "with_private_reporting": sum(1 for r in rows if r.get("private_reporting")),
        "with_published_advisories": sum(1 for r in rows if (r.get("advisories_published") or 0) > 0),
        "with_maintainer_sbom": sum(1 for r in rows if r.get("sbom_published")),
        "with_sbom_at_build_only": sum(1 for r in rows if r.get("sbom_at_build") and not r.get("sbom_published")),
        "unknown_cells": sum(1 for r in rows if r["errors"]),
    }
    print(f"\n{tally['with_maintainer_sbom']} of {n} publish an SBOM · {tally['with_security_policy']} policy · "
          f"{tally['with_private_reporting']} private · {n} repos · {today}")
    if tally["unknown_cells"]:
        print("* archived repo: could not look; unknown is not no")
    if a.json:
        print(json.dumps(tally))
    if a.no_write:
        return
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"sbom-inventory-{today}.json").write_text(json.dumps({"date": today, "tally": tally, "rows": rows}, indent=2))

    yn = lambda v: "unknown" if v is None else ("yes" if v else "no")
    md = [f"# Open-source space software: SBOM + security-policy inventory ({today})", "",
          "Paper 1's original number. Public GitHub data, read by `tools/space_sbom_inventory.py`. "
          "Definitions live in the script header. A dated snapshot: bound every sentence to these repos on this date.", "",
          f"**Of {n} repositories: {tally['with_maintainer_sbom']} publish an SBOM; "
          f"{tally['with_security_policy']} publish a security policy; {tally['with_private_reporting']} accept private "
          f"vulnerability reports through GitHub; {tally['with_published_advisories']} have published a security advisory.**"
          + (f" ({tally['unknown_cells']} rows have an unknown cell, see errors.)" if tally["unknown_cells"] else ""), "",
          "| Project | Repo | Security policy | Private reporting | Advisories published | Maintainer SBOM | Last push | Latest release |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        pol = f"[yes]({r['security_policy_url']})" if r.get("security_policy") else yn(r.get("security_policy"))
        sb = ("yes: " + ", ".join((r["sbom_files"] + r["sbom_release_assets"])[:2]) if r.get("sbom_published")
              else "at build only: " + ", ".join(r["sbom_tooling"][:2]) if r.get("sbom_at_build") else yn(r.get("sbom_published")))
        md.append(f"| {r['project']} | [{r['repo']}](https://github.com/{r['repo']}) | {pol} | {yn(r.get('private_reporting'))} | "
                  f"{r.get('advisories_published', 'unknown')} | {sb} | {r.get('pushed_at','')}{' (archived)' if r.get('archived') else ''} | "
                  f"{r.get('latest_release') or 'none'} {r.get('latest_release_date','')} |")
    errs = [f"- {r['repo']}: {'; '.join(r['errors'])}" for r in rows if r["errors"]]
    if errs:
        md += ["", "## Unknown cells (could not look, which is not the same as no)", *errs]
    (OUT / f"sbom-inventory-{today}.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
