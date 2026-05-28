1|     1|     1|# PR Labeler Action 🏷️
     2|     2|     2|
     3|     3|     3|[![GitHub Release](https://img.shields.io/github/v/release/SCL339/pr-labeler-action?style=flat-square&logo=github)](https://github.com/SCL339/pr-labeler-action/releases)
     4|     4|     4|[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-PR%20Labeler-blue?style=flat-square&logo=githubactions)](https://github.com/marketplace/actions/pr-labeler-action)
     5|     5|     5|[![MIT License](https://img.shields.io/github/license/SCL339/pr-labeler-action?style=flat-square)](LICENSE)
     6|     6|     6|[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
     7|     7|     7|
     8|     8|     8|---
     9|     9|     9|
    10|    10|    10|
    11|    11|    11|- **Smart deduplication** — Won't add labels that already exist on the PR
    12|    12|    12|- **CI/CD ready** — Works on `pull_request` and `pull_request_target` events
    13|    13|    13|- **Lightweight** — Pure Python, no Docker image to pull
    14|    14|    14|- **JSON support** — Can also use `.json` config format
    15|    15|    15|
    16|    16|    16|---
    17|    17|    17|
    18|    18|    18|
    19|    19|    19|  - 'src/styles/**'
    20|    20|    20|  - 'src/pages/**'
    21|    21|    21|
    22|    22|    22|backend:
    23|    23|    23|  - 'src/api/**'
    24|    24|    24|  - 'src/models/**'
    25|    25|    25|  - 'src/services/**'
    26|    26|    26|
    27|    27|    27|documentation:
    28|    28|    28|  - 'docs/**'
    29|    29|    29|  - '*.md'
    30|    30|    30|  - '**/*.md'
    31|    31|    31|
    32|    32|    32|dependencies:
    33|    33|    33|  - 'package.json'
    34|    34|    34|  - 'package-lock.json'
    35|    35|    35|  - 'requirements.txt'
    36|    36|    36|  - '**/go.mod'
    37|    37|    37|
    38|    38|    38|infrastructure:
    39|    39|    39|  - 'Dockerfile'
    40|    40|    40|  - 'docker-compose.yml'
    41|    41|    41|  - '.github/**'
    42|    42|    42|  - 'k8s/**'
    43|    43|    43|```
    44|    44|    44|
    45|    45|    45|---
    46|    46|    46|
    47|    47|    47|
    48|    48|    48|    types: [opened, synchronize, reopened]
    49|    49|    49|
    50|    50|    50|permissions:
    51|    51|    51|  contents: read
    52|    52|    52|  pull-requests: write
    53|    53|    53|
    54|    54|    54|jobs:
    55|    55|    55|  label:
    56|    56|    56|    runs-on: ubuntu-latest
    57|    57|    57|    steps:
    58|    58|    58|      - uses: SCL339/pr-labeler-action@v1.0.0
    59|    59|    59|        with:
    60|    60|    60|          github-token: ${{ secrets.GITHUB_TOKEN }}
    61|    61|    61|```
    62|    62|    62|
    63|    63|    63|---
    64|    64|    64|
    65|    65|    65|
    66|    66|    66||-------|-------------|----------|---------|
    67|    67|    67|| `github-token` | GitHub token with label write access | No | `${{ github.token }}` |
    68|    68|    68|| `config-path` | Path to label config file in the repo | No | `.github/pr-labeler.yml` |
    69|    69|    69|| `fail-on-missing-config` | Fail if config file is missing | No | `false` |
    70|    70|    70|
    71|    71|    71|---
    72|    72|    72|
    73|    73|    73|
    74|    74|    74|  - 'another/pattern/**'
    75|    75|    75|```
    76|    76|    76|
    77|    77|    77|---
    78|    78|    78|
    79|    79|    79|
    80|    80|    80|{
    81|    81|    81|  "frontend": ["src/components/**", "src/styles/**"],
    82|    82|    82|  "backend": ["src/api/**", "src/models/**"]
    83|    83|    83|}
    84|    84|    84|```
    85|    85|    85|
    86|    86|    86|---
    87|    87|    87|
    88|    88|    88|
    89|    89|    89|| `**` | Any sequence of characters (including `/`) |
    90|    90|    90|| `?` | Any single character (except `/`) |
    91|    91|    91|| `[abc]` | Any character in the set |
    92|    92|    92|
    93|    93|    93|---
    94|    94|    94|
    95|    95|    95|
    96|    96|    96|tests:
    97|    97|    97|  - 'tests/**'                    # Any file under tests/
    98|    98|    98|  - '**/test_*.py'               # Any test Python file anywhere
    99|    99|    99|  - 'src/**/__tests__/**'        # Nested test directories
   100|   100|   100|
   101|   101|   101|python:
   102|   102|   102|  - '**/*.py'                     # Any Python file anywhere
   103|   103|   103|
   104|   104|   104|config:
   105|   105|   105|  - '*.yml'                       # YAML files in root
   106|   106|   106|  - 'config/**'                   # Everything under config/
   107|   107|   107|  - '.env*'                       # .env, .env.example, etc.
   108|   108|   108|```
   109|   109|   109|
   110|   110|   110|---
   111|   111|   111|
   112|   112|   112|
   113|   113|   113|on: [pull_request]
   114|   114|   114|permissions:
   115|   115|   115|  contents: read
   116|   116|   116|  pull-requests: write
   117|   117|   117|jobs:
   118|   118|   118|  label:
   119|   119|   119|    runs-on: ubuntu-latest
   120|   120|   120|    steps:
   121|   121|   121|      - uses: SCL339/pr-labeler-action@v1.0.0
   122|   122|   122|```
   123|   123|   123|
   124|   124|   124|---
   125|   125|   125|
   126|   126|   126|
   127|   127|   127|- uses: SCL339/pr-labeler-action@v1.0.0
   128|   128|   128|  with:
   129|   129|   129|    github-token: ${{ secrets.GITHUB_TOKEN }}
   130|   130|   130|    config-path: .github/label-config.yml
   131|   131|   131|    fail-on-missing-config: 'true'
   132|   132|   132|```
   133|   133|   133|
   134|   134|   134|---
   135|   135|   135|
   136|   136|   136|
   137|   137|   137|on:
   138|   138|   138|  pull_request_target:
   139|   139|   139|    types: [opened, synchronize, reopened]
   140|   140|   140|jobs:
   141|   141|   141|  label:
   142|   142|   142|    runs-on: ubuntu-latest
   143|   143|   143|    permissions:
   144|   144|   144|      contents: read
   145|   145|   145|      pull-requests: write
   146|   146|   146|    steps:
   147|   147|   147|      - uses: SCL339/pr-labeler-action@v1.0.0
   148|   148|   148|```
   149|   149|   149|
   150|   150|   150|---
   151|   151|   151|
   152|   152|   152|m/SCL339/pr-labeler-action.git
   153|   153|   153|cd pr-labeler-action
   154|   154|   154|# Test locally with a mock event:
   155|   155|   155|python3 entrypoint.py
   156|   156|   156|```
   157|   157|   157|
   158|   158|   158|---
   159|   159|   159|
   160|   160|   160|ARKER
   161|   161|   161|- 🚀 **Deploy your frontend** on [Vercel](https://vercel.com/?utm_source=scl339&utm_campaign=oss)
   162|   162|   162|- ⭐ **Star this repo** to help others discover it
   163|   163|   163|
   164|   164|   164|
   165|   165|   165|---
   166|   166|   166|
   167|   167|   167|
   168|   168|   168|

---

## 🤝 赞助支持 (Sponsor)

如果这个项目对你有帮助，可以请我喝杯咖啡 ☕

- 💖 **支付宝 (Alipay)**: `18559219554` | 邮箱联系: `530765059@qq.com`
- ☁️ **DigitalOcean 联盟链接**: [免费 $200 额度](https://www.digitalocean.com/?refcode=scl339-01&utm_campaign=Referral_Invite&utm_medium=opensource&utm_source=SCL339)
- ⭐ **在 GitHub 上点 Star** 帮助更多人发现这个项目

## 📄 License
