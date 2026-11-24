# smartci

A Python shopping-cart application with a GitHub Actions pipeline. Each assignment report includes the procedure, observed results, and lessons learned.

| Assignment | Submission |
| --- | --- |
| 4.1 | [Baseline CI, tests, and failure analysis](LAB2.md) |
| 4.2 | [Smart Build-Cache Invalidation (PDF)](docs/assignments/4-2.pdf) |
| 4.3 | [Dynamic Test-Subset Routing (PDF)](docs/assignments/4-3.pdf) |
| 4.4 | [LLM-Based Build/Error-Log Summarization (PDF)](docs/assignments/4-4.pdf) |
| 4.5 | [Build-Failure Prediction (PDF)](docs/assignments/4-5.pdf) |

Run the full suite from the repository root using Python 3.12.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements.lock
python -m pytest
```
