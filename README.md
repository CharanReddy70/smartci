# smartci

A Python shopping-cart application with a GitHub Actions pipeline. Each assignment report includes the procedure, observed results, and lessons learned.

| Assignment | Submission |
| --- | --- |
| 4.1 | [Baseline CI, tests, and failure analysis](LAB2.md) |
| 4.2 | [Smart Build-Cache Invalidation (PDF)](docs/assignments/4-2.pdf) |
| 4.3 | [Dynamic Test-Subset Routing (PDF)](docs/assignments/4-3.pdf) |
| 4.4 | [LLM-Based Build/Error-Log Summarization (PDF)](docs/assignments/4-4.pdf) |
| 4.5 | [Build-Failure Prediction (PDF)](docs/assignments/4-5.pdf) |

## How the CI pipeline works

1. **Restore dependencies (4.2).** The runner reuses cached Python wheels when the operating system, architecture, Python version, and both requirements files match. Editing the dependency constraints triggered a fresh download and offline install. [Workflow](.github/workflows/ci.yml) · [Cache invalidation run](https://github.com/CharanReddy70/smartci/actions/runs/45388307745)
2. **Estimate failure risk (4.5).** Before pytest starts, the predictor checks whether the commit edits tests and counts failures among similar historical builds. The four-build dataset makes this an advisory estimate. On a pricing-only change it reported 25%, based on two matching builds. [Predictor](ml/predict.py) · [Pricing run](https://github.com/CharanReddy70/smartci/actions/runs/45388305039)
3. **Select and run tests (4.3).** The router follows Python imports from changed modules to affected tests. The pricing-only change ran seven tests because the cart imports pricing. A dependency change triggered all 15 tests. [Test router](scripts/route_tests.py)
4. **Explain a failure (4.4).** When pytest fails, a local language model summarizes the log alongside the original assertion. To see an example, open **Actions → CI → Run workflow** and choose `main`. The replay shows a zero-discount test that expected 101 for a price of 100. [Summarizer](scripts/summarize_log.py) · [Verified replay](https://github.com/CharanReddy70/smartci/actions/runs/45389107921)

## Run tests locally

Run the full suite from the repository root using Python 3.12.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements.lock
python -m pytest
```
