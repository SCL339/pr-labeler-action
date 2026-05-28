# PR Labeler Action 🏷️

[![GitHub Release](https://img.shields.io/github/v/release/SCL339/pr-labeler-action?style=flat-square&logo=github)](https://github.com/SCL339/pr-labeler-action/releases)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-PR%20Labeler-blue?style=flat-square&logo=githubactions)](https://github.com/marketplace/actions/pr-labeler-action)
[![MIT License](https://img.shields.io/github/license/SCL339/pr-labeler-action?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

A GitHub Action that **automatically adds labels to pull requests based on the file paths changed**. Define path-to-label mappings in a simple YAML file and let the action do the rest — no more manually labeling PRs!

> ✨ Part of the [SCL339](https://github.com/SCL339) open-source ecosystem.

---

## Features ✨

- **Zero config** — Create a simple YAML file and you're done
- **Glob pattern matching** — Use `**`, `*`, and `?` patterns familiar from `.gitignore`
- **Smart deduplication** — Won't add labels that already exist on the PR
- **CI/CD ready** — Works on `pull_request` and `pull_request_target` events
- **Lightweight** — Pure Python, no Docker image to pull
- **JSON support** — Can also use `.json` config format

## Usage 📦

### Step 1: Create a config file

Create `.github/pr-labeler.yml` in your repository:

```yaml
# .github/pr-labeler.yml
frontend:
  - 'src/components/**'
  - 'src/styles/**'
  - 'src/pages/**'

backend:
  - 'src/api/**'
  - 'src/models/**'
  - 'src/services/**'

documentation:
  - 'docs/**'
  - '*.md'
  - '**/*.md'

dependencies:
  - 'package.json'
  - 'package-lock.json'
  - 'requirements.txt'
  - '**/go.mod'

infrastructure:
  - 'Dockerfile'
  - 'docker-compose.yml'
  - '.github/**'
  - 'k8s/**'
```

### Step 2: Add the workflow

Create `.github/workflows/pr-labeler.yml`:

```yaml
name: PR Labeler

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: SCL339/pr-labeler-action@v1.0.0
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

That's it! Now every PR will be automatically labeled based on the files it changes.

## Inputs ⚙️

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github-token` | GitHub token with label write access | No | `${{ github.token }}` |
| `config-path` | Path to label config file in the repo | No | `.github/pr-labeler.yml` |
| `fail-on-missing-config` | Fail if config file is missing | No | `false` |

## Config Format 📝

### YAML format (`.github/pr-labeler.yml`)

```yaml
label-name:
  - 'glob/pattern/**'
  - 'another/pattern/**'
```

### JSON format (`.github/pr-labeler.json`)

```json
{
  "frontend": ["src/components/**", "src/styles/**"],
  "backend": ["src/api/**", "src/models/**"]
}
```

## Pattern Matching 🔍

The action uses Python's `fnmatch` for glob matching. Supported wildcards:

| Pattern | Matches |
|---------|---------|
| `*` | Any sequence of characters (except `/`) |
| `**` | Any sequence of characters (including `/`) |
| `?` | Any single character (except `/`) |
| `[abc]` | Any character in the set |

### Examples

```yaml
tests:
  - 'tests/**'                    # Any file under tests/
  - '**/test_*.py'               # Any test Python file anywhere
  - 'src/**/__tests__/**'        # Nested test directories

python:
  - '**/*.py'                     # Any Python file anywhere

config:
  - '*.yml'                       # YAML files in root
  - 'config/**'                   # Everything under config/
  - '.env*'                       # .env, .env.example, etc.
```

## Example Workflows 🚀

### Basic (recommended)

```yaml
name: PR Labeler
on: [pull_request]
permissions:
  contents: read
  pull-requests: write
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: SCL339/pr-labeler-action@v1.0.0
```

### With custom config path and fail-on-missing

```yaml
- uses: SCL339/pr-labeler-action@v1.0.0
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    config-path: .github/label-config.yml
    fail-on-missing-config: 'true'
```

### Using pull_request_target (for fork PRs)

```yaml
on:
  pull_request_target:
    types: [opened, synchronize, reopened]
jobs:
  label:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: SCL339/pr-labeler-action@v1.0.0
```

## Related Projects 🔗

Check out other [SCL339](https://github.com/SCL339) tools:

- [auto-changelog-action](https://github.com/SCL339/auto-changelog-action) — Auto-generate CHANGELOG from PR titles/labels
- [md-slides](https://github.com/SCL339/md-slides) — Markdown-to-HTML presentation tool

## Development 🛠️

```bash
git clone https://github.com/SCL339/pr-labeler-action.git
cd pr-labeler-action
# Test locally with a mock event:
python3 entrypoint.py
```



---

## 🤝 Support

If you find this project useful, consider supporting my work:

- 💖 **Sponsor via WeChat/Alipay**: Email `530765059@qq.com` for details
- ☁️ **Get $200 free credit** on [DigitalOcean](https://www.digitalocean.com/?refcode=scl339-01&utm_campaign=Referral_Invite&utm_medium=opensource&utm_source=SCL339)
- 🚀 **Deploy your frontend** on [Vercel](https://vercel.com/?utm_source=scl339&utm_campaign=oss)
- ⭐ **Star this repo** to help others discover it


## 📄 License

MIT — see [LICENSE](LICENSE) for details.
