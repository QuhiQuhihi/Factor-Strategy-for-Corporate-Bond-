# Preparing a public release

The maintained project consists of `docs/`, the `research/` pipeline and tests,
summary results, original figures, `study.ipynb`, and the locked Python environment.
The previous chapter directories, obsolete Python/SQL, private-data notebooks,
copied vendor assets, personal review notes and historical dependency list have
been removed. They are not needed to reproduce the study.

## Validate the current files

Run from the repository root in WSL/Linux:

~~~bash
uv sync --locked
uv run python research/download_sources.py
uv run python research/build_notebook.py
uv run python -m unittest discover -s research -p 'test_*.py' -v
uv run python research/check_artifacts.py
uv run python research/check_publication.py
~~~

The notebook build reruns the numerical study. Source archives and regenerated
monthly returns stay local and ignored; summary statistics and figures remain
versioned. The source URLs and hashes identify the exact research inputs.
GitHub Actions runs installation, unit tests and public-file checks. It does not
fetch research data on pull requests or certify the full historical analysis.

## Prepare a publication bundle

~~~bash
uv run python research/check_publication.py --export research/public-export/release-2026-09-16
~~~

Choose a new destination for each export. The command creates a `public-research/`
tree, `public-research.zip` and `SHA256SUMS.json`. It includes the reviewed working
contents of tracked and allowed untracked files, so review the diff before release.
It excludes `.git`, raw archives, regenerated monthly panels, environments and
other ignored files. Publish from this clean snapshot if starting a new repository;
do not upload the entire workspace or the recovery archive.

## Existing Git history

Deleting files from a branch does not remove old commits. This development
repository's history includes an old database share link, a bond-return export and
notebooks with database records. Check known paths with:

~~~bash
uv run python research/check_publication.py --check-history
~~~

This command deliberately fails on the current development history. A shallow
clone is insufficient for the check. The export route avoids carrying that history
into a new repository. Preserving the existing repository history would require a
separate coordinated rewrite and review of other branches/tags, remote copies and
link access. No rewrite or remote changes are performed by these commands.
[GitHub's guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
explains the remaining considerations. Even a passing path check is not a full
history secret scan or evidence that external sharing permissions were revoked.

## Attribution and blog adaptation

Keep source attribution, historical dates, gross-return conventions, statistical
uncertainty and exploratory status alongside results. The numerical inputs are
external researchers' work; this project's contribution is the replication and
analysis. See [NOTICE](NOTICE), [DATA_NOTICE.md](research/DATA_NOTICE.md) and the
[source register](research/SOURCES.md).

The benchmark source specifies
[CC BY-NC-SA 3.0](https://github.com/Alexander-M-Dickerson/co-pricing-factor-zoo#license-for-data).
Unrestricted redistribution and commercial permissions for other factor archives
were not established. Evaluate the intended use of licensed material and affected
outputs before a monetized, sponsored or employer-owned publication; this file
is not a blanket rights clearance.

For a professional blog, use the overview and original conditional-alpha figure
as a starting point. Develop one question: does adding issuer equity information
help more than reducing bond exposure? Explain the paired result and uncertainty,
then the opposing momentum/value diagnostics and the next security-level test.
Link to the full reports and notebook for methods. Avoid presenting gross
regression alpha as executable profit or revised historical data as a fresh holdout.
