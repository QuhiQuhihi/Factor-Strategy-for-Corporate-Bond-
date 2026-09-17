# Data and code attribution

The study uses factor returns distributed through [Open Source Bond Asset Pricing](https://openbondassetpricing.com/).
Credit for original data construction and source portfolios belongs to the cited authors,
including Dickerson, Nozawa and Robotti; Dick-Nielsen, Feldhütter, Pedersen and Stolborg;
and Dickerson, Julliard and Mueller. Equity characteristics originate in the sources
identified in [SOURCES.md](SOURCES.md).

Public availability does not remove source-specific terms. On 16 September 2026 the
co-pricing repository's [data-license statement](https://github.com/Alexander-M-Dickerson/co-pricing-factor-zoo#license-for-data)
was checked: it specifies [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).
Its licensed material requires attribution, limits commercial use, and requires the
same license for adaptations covered by that license. The root Apache code license
does not replace these conditions. Applicability to a particular analytical output
or intended use must be assessed separately; this notice does not treat every
statistic as automatically licensed or exempt.

The other archived factor releases are distributed through the provider's
[machine-learning data page](https://openbondassetpricing.com/machine-learning-data/).
An unrestricted redistribution or commercial-use grant for those exact archives
has not been established in this review. Do not infer one from a download link or
from the phrase "open source."

## What the public tree includes

Original analysis code, source URLs and checksums, summary statistics, original
research figures and an executed notebook are retained for inspection. Outputs
document filtering, orientation changes, portfolio combinations and regressions;
these are modifications and calculations by this project, not source-author results
unless explicitly identified as replication. No source-author endorsement is implied.

Raw downloads, cached papers, extracted benchmark returns, selected monthly factor
returns and monthly risk-control return panels are excluded from Git. Run the documented
download and analysis commands to regenerate them locally under the provider's terms.
This avoids bundling source-like series while preserving inspectable summary evidence;
it does not itself resolve every permission question about that evidence.

## Public reuse

The maintained tree contains the current study only. Obsolete scripts, private-data
notebooks, bond-level exports, database share links, vendor documents and copied
screenshots have been removed. Upstream authors retain credit for their data and
portfolio construction through the source register; their processing code is not bundled.

Use the project's generated figures with the source attribution and sample limitations
intact. For a monetized, sponsored or employer-owned blog, establish permission
for the intended reuse of licensed source material and affected outputs before
publishing them. No commercial-use clearance is claimed by this review.

Tracked-file cleanup does not remove old Git commits. The historical database link,
bond-return export and embedded notebook data require a separate history/access
decision before exposing the existing repository. See [PUBLICATION.md](../PUBLICATION.md).

The source comparison is independently recomputed from the archived inputs, following
the authors' stated formulas. The new contribution is the economic-direction comparison,
conditional signal analysis, portfolio controls, inference and interpretation.
