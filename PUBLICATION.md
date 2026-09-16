# Public repository and blog review

Reviewed 16 September 2026. The current working tree is curated for inspection and
reproduction. **Do not make the existing Git history public on the strength of this
cleanup alone.** Old commits contain a database download link, a bond-level return
export and notebooks with database outputs. This review did not rewrite history,
inspect remote visibility, revoke link access or establish commercial reuse rights.

## File policy

| Material | Public treatment |
|---|---|
| Current research code, tests, pyproject.toml, uv.lock | Retain; these define the supported workflow |
| README, chapter reports, protocol, sources, scientific agenda | Retain; describe completed and proposed work separately |
| Summary CSVs and original research figures | Retain with attribution and data-use caveats |
| Combined_README.ipynb | Retain executed, with bounded results and generated figures |
| Extracted benchmarks and monthly return panels | Regenerate locally; exclude source-like series from redistribution |
| Raw archives, databases and vendor panels | Exclude; download independently under source terms |
| Old database link, bond-return CSV, notebooks with embedded records | Exclude from the current tree; historical copies still require attention |
| Vendor PDFs/DOCX files, newspaper/provider screenshots, copied processing scripts | Exclude; link to authoritative originals; permission was not established |
| Empty notebook, OS/editor files, caches, environments and local credentials | Exclude |
| Personal hiring assessment | Keep locally; publish the extracted scientific research agenda |
| Retained legacy Python/SQL | Clearly identified in [LEGACY.md](LEGACY.md); not validated current research |

The cleanup untracks 35 existing files while preserving local copies. Ignore rules
also cover new local-only outputs. `.gitignore` does not untrack existing files or
erase old commits; see [Git's documentation](https://git-scm.com/docs/gitignore).
The code environment, inspectable summary evidence and original figures remain visible.

## Recheck and prepare a clean snapshot

Run from WSL/Linux at the repository root:

~~~bash
uv run python research/check_publication.py
uv run python research/check_publication.py --export research/public-export/review-2026-09-16
~~~

The second command requires a new destination; use a new directory name for another
export. It creates a `public-research/` tree, `public-research.zip`, and a SHA-256
inventory. It includes the current contents of tracked files and untracked files
allowed by `.gitignore`, so inspect new files before running it. The export contains
no `.git` directory or history. Use that snapshot if a fresh public repository is
appropriate. Do not upload the entire workspace: ignored local files are still there.

The check catches tracked-but-ignored files, local links to excluded artifacts,
invalid notebook JSON, saved error outputs, personal notebook paths and selected
credential patterns without displaying matched values. It is a limited packaging
check, not a full secret scan, binary-content inspection or license clearance.

If retaining the original history is necessary, plan a separate coordinated history
cleanup. If the database link is still active and access should be private, inspect
its sharing permissions at its host. An index removal cannot revoke external access.
[GitHub's guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
explains why older commits, copies and forks need separate handling.

## Suitability for a professional blog

The current overview and generated conditional-alpha figure are good starting points.
The five-chapter report and combined notebook are supporting material, not a concise
blog post. A focused article should develop one question: **does adding issuer equity
signals help more than simply reducing bond exposure?**

Use the following sequence:

1. Explain the allocation decision and why lower volatility alone is insufficient.
2. Describe the public factor data, economic signs and 60-month lagged control briefly.
3. Present the paired result and uncertainty; explain that the original combination
   has no clear advantage over the control.
4. Show the opposing conditional momentum/value findings as an exploratory follow-up.
5. End with the point-in-time security-level experiment needed to distinguish issuer
   information transmission from common risk and stale prices.

Keep sample dates (ending November 2021), gross returns, fixed-notional conventions
and exploratory status beside the relevant claims. Explain alpha as a regression
intercept conditional on specified controls. Avoid titles claiming newly discovered
tradable alpha or out-of-sample validation. Use original project figures and link
to the code and source register rather than republishing excluded vendor screenshots.

Source-data terms remain material. The benchmark-data provider specifies
[CC BY-NC-SA 3.0](https://github.com/Alexander-M-Dickerson/co-pricing-factor-zoo#license-for-data).
Other factor-archive redistribution/commercial permissions were not established.
A monetized, sponsored or employer-owned publication needs an intended-use review
of licensed material and affected outputs; public downloadability does not settle it.
See [DATA_NOTICE.md](research/DATA_NOTICE.md) and [NOTICE](NOTICE). This is a documented
permission question, not a conclusion that all analytical facts or original prose
are restricted.
