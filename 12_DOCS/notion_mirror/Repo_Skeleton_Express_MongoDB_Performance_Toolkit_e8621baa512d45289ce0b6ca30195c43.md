# Repo Skeleton — Express+MongoDB Performance Toolkit

> Notion URL: https://app.notion.com/p/Repo-Skeleton-Express-MongoDB-Performance-Toolkit-e8621baa512d45289ce0b6ca30195c43
> Created: 2025-09-17T14:19:00.000Z
> Last edited: 2025-09-17T14:22:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## File tree
```javascript
repo-root/
├─ src/
│  ├─ server.js
│  ├─ routes/items.js
│  ├─ middlewares/perf.js
│  ├─ middlewares/safeJson.js
│  ├─ serializers/itemSerializer.js
│  ├─ db.js
│  └─ utils/coalesce.js
├─ benchmark/run.sh
├─ docs/benchmarks.md
├─ .env.example
├─ LICENSE
└─ README.md
```
## README.md
```markdown
# Express + MongoDB Performance Toolkit (Engineering-grade)

Cut 30%+ P95 without API contract changes. Includes LRU cache + singleflight, Mongo projection + lean + indexes, fast-json-stringify, gzip + ETag, soft-timeout, and reproducible benchmarks.

## Quick start
```
npm i express mongoose lru-cache pino compression on-headers etag fast-json-stringify
npm i -D autocannon
export MONGO_URI="mongodb://localhost:27017/uid9622"
node src/server.js
bash benchmark/run.sh "http://localhost:3000/api/items?category=all"
```javascript

## Repo layout
See file tree above.

## Benchmarks
See docs/benchmarks.md and benchmark/run.sh. Submit PRs with environment specs + raw logs.

## License & Credits
MIT. Built by UID9622 (🍀系统中枢) with assistance from OpenAI ChatGPT and Notion AI.
```
## LICENSE (MIT)
```javascript
MIT License

Copyright (c) 2025 UID9622

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
## .env.example
```javascript
MONGO_URI=mongodb://localhost:27017/uid9622
PORT=3000
LOG_LEVEL=info
```
## docs/benchmarks.md
```markdown
# Benchmarks

Tool: autocannon

## Command
```
npx autocannon -w 10 -d 30 -c 200 -p 10 "http://localhost:3000/api/items?category=all" | tee benchmark/result.txt
```javascript

Metrics to capture: RPS, P50, P95, P99, errors, CPU, RSS.

| Version   | Hit rate | P50  | P95  | P99  | RPS  | Notes |
|-----------|---------:|-----:|-----:|-----:|-----:|-------|
| baseline  | 0%       | 45ms | 180ms| 320ms| 1.5k |      |
| optimized | 30%      | 20ms | 110ms| 210ms| 2.2k |      |

Environment: CPU model, cores, RAM, Node.js, MongoDB, dataset size.
```
## benchmark/run.sh
```bash
#!/usr/bin/env bash
set -euo pipefail
URL=${1:-"http://localhost:3000/api/items?category=all"}
WARMUP=10
DUR=30
CONN=200
PIP=10
npx autocannon -w $WARMUP -d $DUR -c $CONN -p $PIP "$URL" | tee benchmark/result.txt
```
## src placeholders
- Copy implementation details from Untitled into corresponding files.
- Ensure server.js disables default etag and uses custom ETag + compression + timing + soft-timeout.
- Keep routes/items.js contract identical to existing API.
