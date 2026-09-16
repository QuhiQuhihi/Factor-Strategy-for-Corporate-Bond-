# Earlier experiments

The Python scripts in the chapter directories and `(Chapter1)Data/EDA/EDA.sql`
document earlier work. They are not the maintained research pipeline and are not
used to generate any current result. The supported entry point is
`uv run python research/run_study.py`; its environment is `pyproject.toml` and `uv.lock`.

The earlier scripts depend on a private TRACE database and contain unfinished or
superseded modeling choices documented in the chapter reports. They have not been
validated as executable strategies. Repository-relative paths replace old machine
paths, but that portability cleanup does not establish correctness. The historical
`requirements.txt` is retained for context, not as the recommended installation path.

Old notebooks with embedded database records, bond-level return exports, database
download links, copied reference documents and screenshots are excluded from the
public tree. Copies of upstream processing scripts are excluded as well; consult
the [original processing repository](https://github.com/Alexander-M-Dickerson/TRACE-corporate-bond-processing)
and its authors for attribution and applicable permissions. Excluded working files
can remain locally; they are unnecessary for reproducing the current study.

For a public repository or blog, use the current overview, chapter narrative,
`research/` code, summary tables, original figures and combined notebook. Do not
present legacy ETF outputs as evidence for the current strategy.
