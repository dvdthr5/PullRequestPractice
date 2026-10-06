# Instructor Guide

[Overview](README.md) · [Student guide](README-STUDENT.md)

## 1. Set up the repository

Use Git, Python **3.9+**, and one shared repository with `main` as the default branch. GitHub Free supports this setup in public repositories; private repositories need a plan supporting Pages and branch protection.

- Give students **write** access; keep administrator access with the instructor.
- Enable Actions. In **Settings → Pages → Source**, select **GitHub Actions**. The workflow is already included. [Pages setup](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

Before enabling branch protection, validate and push the starter files:

```sh
git switch main
python3 scripts/validate.py
git add .
git commit -m "Add classroom activity"
git push -u origin main
```

Skip committing if the files are already committed. Wait for **Validate website** and deployment to succeed. If Pages was enabled afterward, rerun the failed workflow.

## 2. Protect main

In **Settings → Branches**, add a classic branch protection rule for `main`:

- Require a PR and **one approving review**.
- Require the **Validate website** status check; select it after its first successful run.
- Require branches to be current with `main`.
- Dismiss old approvals when new code is pushed.
- Apply protection to administrators too; allow no student bypass.
- Keep force pushes and branch deletion disabled.

See [branch protection setup](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule).

Enable **Squash and merge** in **Settings → General → Pull Requests**. In **Settings → Environments → github-pages**, allow deployment only from `main`. Deployment follows merging, so do not require deployment success on PRs.

Before class, open the published website from **Settings → Pages** and check that a sample PR requires approval and passing CI.

## 3. Run the lesson

Create one **Add Student Profile** issue per student and assign review partners. Have students follow the student guide. Require a meaningful **Files changed** review comment, a revision committed to the same branch, and approval after that revision.

**CI exercise:** On an open feature branch, change `<h1>…</h1>` to `<h2>…</h2>`, commit, and push. Inspect the failed PR check. Restore the heading, validate, commit, and push again; confirm green CI before approval. Keep the broken version off `main`.

**Conflict exercise:** Merge one roster PR while others remain open. Have later authors merge `origin/main` into their feature branches, resolve overlapping edits while preserving every student's link, and push. Conflicts may occur; stale branches do not always conflict.

After approved squash merges, confirm students pull updated `main` and find their profiles on the deployed website.
