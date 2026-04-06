---
name: clawdhub
description: Поиск, установка, обновление и публикация навыков агента через ClawdHub CLI с clawdhub.com. Используйте для получения новых навыков, синхронизации установленных версий и публикации обновлений.
metadata: {"clawdbot":{"requires":{"bins":["clawdhub"]},"install":[{"id":"node","kind":"node","package":"clawdhub","bins":["clawdhub"],"label":"Install ClawdHub CLI (npm)"}]}}
---

# ClawdHub CLI

Install
```bash
npm i -g clawdhub
```

Auth (publish)
```bash
clawdhub login
clawdhub whoami
```

Search
```bash
clawdhub search "postgres backups"
```

Install
```bash
clawdhub install my-skill
clawdhub install my-skill --version 1.2.3
```

Update (hash-based match + upgrade)
```bash
clawdhub update my-skill
clawdhub update my-skill --version 1.2.3
clawdhub update --all
clawdhub update my-skill --force
clawdhub update --all --no-input --force
```

List
```bash
clawdhub list
```

Publish
```bash
clawdhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

Notes
- Default registry: https://clawdhub.com (override with CLAWDHUB_REGISTRY or --registry)
- Default workdir: cwd; install dir: ./skills (override with --workdir / --dir)
- Update command hashes local files, resolves matching version, and upgrades to latest unless --version is set
