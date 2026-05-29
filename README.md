# PR Labeler Action 🏷️

[![GitHub Release](https://img.shields.io/github/v/release/SCL339/pr-labeler-action?style=flat-square&logo=github)](https://github.com/SCL339/pr-labeler-action/releases)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-PR%20Labeler-blue?style=flat-square&logo=githubactions)](https://github.com/marketplace/actions/pr-labeler-action)
[![MIT License](https://img.shields.io/github/license/SCL339/pr-labeler-action?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

---

- **Smart deduplication** — Won't add labels that already exist on the PR
- **CI/CD ready** — Works on `pull_request` and `pull_request_target` events
- **Lightweight** — Pure Python, no Docker image to pull
- **JSON support** — Can also use `.json` config format

---

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

---

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

---

|-------|-------------|----------|---------|
| `github-token` | GitHub token with label write access | No | `${{ github.token }}` |
| `config-path` | Path to label config file in the repo | No | `.github/pr-labeler.yml` |
| `fail-on-missing-config` | Fail if config file is missing | No | `false` |

---

- 'another/pattern/**'
```

---

{
"frontend": ["src/components/**", "src/styles/**"],
"backend": ["src/api/**", "src/models/**"]
}
```

---

| `**` | Any sequence of characters (including `/`) |
| `?` | Any single character (except `/`) |
| `[abc]` | Any character in the set |

---

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

---

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

---

- uses: SCL339/pr-labeler-action@v1.0.0
with:
github-token: ${{ secrets.GITHUB_TOKEN }}
config-path: .github/label-config.yml
fail-on-missing-config: 'true'
```

---

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

---

m/SCL339/pr-labeler-action.git
cd pr-labeler-action
# Test locally with a mock event:
python3 entrypoint.py
```

---

- 🚀 **Deploy your frontend** on [Vercel](https://vercel.com/?utm_source=scl339&utm_campaign=oss)
- ⭐ **Star this repo** to help others discover it

---

---

## 🤝 赞助支持 (Sponsor)

如果这个项目对你有帮助，可以请我喝杯咖啡 ☕

- 💖 **支付宝 (Alipay)**: `18559219554` | 邮箱联系: `530765059@qq.com`
- ☁️ **DigitalOcean 联盟链接**: [免费 $200 额度](https://www.digitalocean.com/?refcode=scl339-01&utm_campaign=Referral_Invite&utm_medium=opensource&utm_source=SCL339)
- ⭐ **在 GitHub 上点 Star** 帮助更多人发现这个项目

## 📄 License