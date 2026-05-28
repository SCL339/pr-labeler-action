#!/usr/bin/env python3
"""
PR Labeler Action — Automatically adds labels to PRs based on changed file paths.

Reads a YAML config file (.github/pr-labeler.yml by default) that maps
file path globs to labels. When a PR is opened or updated, this action
queries the PR's changed files, matches them against the config, and
applies the appropriate labels.

Config format (.github/pr-labeler.yml):
    label-name:
      - 'glob/pattern/**'
      - 'another/pattern/**'

    # Example:
    frontend:
      - 'src/components/**'
      - 'src/styles/**'
    backend:
      - 'src/api/**'
      - 'src/models/**'
    documentation:
      - 'docs/**'
      - '*.md'
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from fnmatch import fnmatch


def info(msg):
    print(f"::info::{msg}", file=sys.stderr)


def debug(msg):
    print(f"::debug::{msg}", file=sys.stderr)


def warning(msg):
    print(f"::warning::{msg}", file=sys.stderr)


def error(msg):
    print(f"::error::{msg}", file=sys.stderr)


def github_request(url, token, method="GET", data=None):
    """Make an authenticated GitHub API request."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "pr-labeler-action/1.0",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error(f"GitHub API error {e.code} for {url}: {e.read().decode()}")
        if e.code >= 400 and e.code < 500:
            return None
        raise


def load_yaml_simple(path):
    """
    Simple YAML parser for the label config format.
    Supports the expected structure:
        label-name:
          - 'glob'
          - 'glob'
    Falls back to JSON if file ends with .json.
    """
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        content = f.read()

    # Try JSON first
    if path.endswith(".json"):
        return json.loads(content)

    # Simple YAML parser for the expected format
    config = {}
    current_label = None

    for line in content.split("\n"):
        line_stripped = line.strip()

        # Skip comments and empty lines
        if not line_stripped or line_stripped.startswith("#"):
            continue

        # Label line (no leading dash)
        if not line_stripped.startswith("- "):
            if ":" in line_stripped:
                label_part = line_stripped.split(":")[0].strip()
                if label_part:
                    current_label = label_part
                    config[current_label] = []
            continue

        # Pattern line (starts with - )
        if current_label and line_stripped.startswith("- "):
            pattern = line_stripped[2:].strip().strip("'").strip('"')
            if pattern:
                config[current_label].append(pattern)

    return config


def load_config(config_path, fail_on_missing):
    """Load the label configuration from the repository."""

    # Try the configured path
    config = load_yaml_simple(config_path)

    # Also try common alternatives
    if config is None and config_path != ".github/pr-labeler.yml":
        alt_paths = [config_path, ".github/pr-labeler.yml", ".github/pr-labeler.yaml"]
        for p in alt_paths:
            config = load_yaml_simple(p)
            if config:
                info(f"Found config at {p}")
                break

    if config is None:
        alt_paths = [".github/pr-labeler.yml", ".github/pr-labeler.yaml"]
        for p in alt_paths:
            config = load_yaml_simple(p)
            if config:
                info(f"Found config at {p}")
                break

    if config is None:
        msg = f"Configuration file not found ({config_path}). Create .github/pr-labeler.yml with path-to-label mappings."
        if fail_on_missing:
            error(msg)
            sys.exit(1)
        else:
            warning(msg + " Skipping.")
            sys.exit(0)

    return config


def get_pr_changed_files(repo, pr_number, token):
    """Get list of files changed in a PR using the GitHub API."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    all_files = []
    page = 1

    while True:
        page_url = f"{url}?per_page=100&page={page}"
        data = github_request(page_url, token)
        if data is None or not data:
            break
        all_files.extend(data)
        if len(data) < 100:
            break
        page += 1

    return [f["filename"] for f in all_files]


def get_existing_labels(repo, pr_number, token):
    """Get existing labels on a PR."""
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels"
    data = github_request(url, token)
    if data is None:
        return set()
    return {l["name"] for l in data}


def add_labels_to_pr(repo, pr_number, labels, token):
    """Add labels to a PR."""
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels"
    data = {"labels": list(labels)}
    result = github_request(url, token, method="POST", data=data)
    if result is not None:
        info(f"Added labels to PR #{pr_number}: {', '.join(labels)}")
    return result


def match_patterns(changed_files, config):
    """Match changed files against config patterns and return matching labels."""
    labels_to_add = set()

    for label, patterns in config.items():
        for file_path in changed_files:
            for pattern in patterns:
                if fnmatch(file_path, pattern):
                    debug(f"File '{file_path}' matches pattern '{pattern}' → label '{label}'")
                    labels_to_add.add(label)
                    break
            # Don't add the same label multiple times per PR

    return labels_to_add


def main():
    # Read inputs from environment
    token = os.environ.get("INPUT_TOKEN", "")
    config_path = os.environ.get("INPUT_CONFIG_PATH", ".github/pr-labeler.yml")
    fail_on_missing = os.environ.get("INPUT_FAIL_ON_MISSING", "false").lower() == "true"
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")

    if not token:
        error("github-token is required")
        sys.exit(1)

    if not repo:
        error("GITHUB_REPOSITORY is not set")
        sys.exit(1)

    # Only run on pull_request events
    if event_name not in ("pull_request", "pull_request_target"):
        warning(f"This action only runs on pull_request events, got: {event_name}")
        sys.exit(0)

    # Get PR number from event payload
    if not event_path or not os.path.exists(event_path):
        error(f"Event payload not found at {event_path}")
        sys.exit(1)

    with open(event_path, "r") as f:
        event_data = json.load(f)

    pr_number = event_data.get("number")
    if not pr_number:
        error("Could not determine PR number from event payload")
        sys.exit(1)

    debug(f"Processing PR #{pr_number} in {repo}")

    # Load configuration
    config = load_config(config_path, fail_on_missing)
    if not config:
        info("No labels configured. Skipping.")
        sys.exit(0)

    info(f"Loaded {len(config)} label rules from config")

    # Get changed files
    changed_files = get_pr_changed_files(repo, pr_number, token)
    if not changed_files:
        info(f"No changed files found for PR #{pr_number}")
        sys.exit(0)

    info(f"PR #{pr_number} changes {len(changed_files)} file(s)")

    # Match patterns
    new_labels = match_patterns(changed_files, config)
    if not new_labels:
        info(f"No matching labels for PR #{pr_number}")
        sys.exit(0)

    info(f"Labels to add: {', '.join(sorted(new_labels))}")

    # Add labels
    existing_labels = get_existing_labels(repo, pr_number, token)
    labels_to_actually_add = new_labels - existing_labels

    if not labels_to_actually_add:
        info(f"All matching labels already exist on PR #{pr_number}")
        sys.exit(0)

    add_labels_to_pr(repo, pr_number, labels_to_actually_add, token)
    info(f"Successfully labeled PR #{pr_number}")


if __name__ == "__main__":
    main()
