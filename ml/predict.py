"""Estimate failure frequency from prior main-branch CI outcomes."""
import argparse
import csv
from pathlib import Path
import subprocess


def edits_tests(commit):
    paths = subprocess.check_output(
        ["git", "diff-tree", "--root", "-m", "--no-commit-id", "--name-only",
         "-r", "-z", commit], text=True
    )
    return any(path.startswith("tests/") for path in paths.split("\0"))


def probability(labels):
    # Beta(1,1) prior keeps sparse groups away from absolute certainty.
    return (sum(labels) + 1) / (len(labels) + 2)


def estimate(history, group):
    matching = [failed for prior_group, failed in history if prior_group == group]
    return probability(matching), len(matching)


def load_history():
    with Path(__file__).with_name("history.csv").open() as stream:
        return [(row["commit"], edits_tests(row["commit"]), row["conclusion"] == "failure")
                for row in csv.DictReader(stream)]


def evaluate(rows):
    history = []
    scores, baseline = [], []
    for commit, group, failed in rows:
        if history:
            prediction, _ = estimate(history, group)
            prior = probability([label for _, label in history])
            scores.append((prediction - failed) ** 2)
            baseline.append((prior - failed) ** 2)
            print(f"{commit[:7]} score={prediction:.3f} actual={int(failed)}")
        history.append((group, failed))
    print(f"Walk-forward Brier score ({len(scores)} predictions): "
          f"{sum(scores)/len(scores):.3f}; overall-rate baseline: "
          f"{sum(baseline)/len(baseline):.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--evaluate", action="store_true")
    args = parser.parse_args()
    rows = load_history()
    if args.evaluate:
        evaluate(rows)
    else:
        target = subprocess.check_output(["git", "rev-parse", args.commit], text=True).strip()
        history = [(group, failed) for commit, group, failed in rows
                   if commit != target and subprocess.run(
                       ["git", "merge-base", "--is-ancestor", commit, target]
                   ).returncode == 0]
        group = edits_tests(target)
        score, count = estimate(history, group)
        print(f"Advisory failure estimate {score:.1%} "
              f"(tests changed={group}, {count} matching historical builds)")
