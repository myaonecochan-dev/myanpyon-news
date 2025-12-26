---
description: Check git status and deploy changes
---

1. Check for uncommitted changes
    run_command: git status
2. If there are modified files that should be deployed, add and commit them.
    run_command: git add .
    run_command: git commit -m "feat: updates"
3. Push changes to remote
    run_command: git push origin main
4. Wait for 10 seconds to allow CI/CD to pick up
    run_command: sleep 10
