# Student Guide

[Overview](README.md) · [Instructor guide](README-INSTRUCTOR.md)

**Your task:** Add a profile, review a classmate's PR, respond to feedback, and merge.
You need Git, Python 3.9+, repository access, and an assigned issue.
Replace `david` below with your unique lowercase name or handle (no spaces).

## 1. Create your branch

Clone once, using your instructor's URL if different:

```sh
git clone https://github.com/dvdthr5/PullRequestPractice.git
cd PullRequestPractice
```

From the repository folder with a clean working tree:

```sh
git switch main
git pull --ff-only
git switch -c add-david-profile
```

## 2. Add and test your profile

Copy `students/example.html` to `students/david.html`. Add your name, About Me,
interests, and project/research interests. Keep the `<h1>`, stylesheet, and home link.

Add this inside the roster in `index.html`, keeping everyone's entries:

```html
<li><a href="students/david.html">David</a></li>
```

```sh
python3 scripts/validate.py
python3 -m http.server 8000
```

Open [localhost:8000](http://localhost:8000). Check your profile and both navigation
links. Stop the server with **Ctrl+C**.

## 3. Push and open a pull request

```sh
git status
git diff
git add index.html students/david.html
git commit -m "Add David's profile"
git push -u origin add-david-profile
```

On GitHub, choose **Compare & pull request** into **main**. Fill in what changed,
how you tested it, and `Closes #4` (use your issue number). Request your partner's review.

Your **branch** holds your **commits**. A **PR** proposes merging that branch;
the **merge** adds accepted changes to `main`.

## 4. Review and respond

Open your partner's **Files changed** tab. Check their profile, links, and that
everyone else's roster entries remain. **Leave one meaningful comment before approving**,
such as asking for a specific project idea.

- **Comment:** Feedback without approval or blocking.
- **Request changes:** Something needs fixing before merging.
- **Approve:** The reviewed changes are ready to merge.

Make a useful revision to your own files on the **same feature branch**, then:

```sh
python3 scripts/validate.py
git add index.html students/david.html
git commit -m "Address PR review feedback"
git push
```

**The existing PR updates automatically.** Reply to the feedback and request another
review. Your partner should inspect the new commit before approving.

## 5. Wait for CI and resolve conflicts

**CI** runs on PR updates and pushes to `main`. It checks required files, basic HTML,
profile headings, home links, and roster links. Read failures under **Checks → Validate
website**, fix them, and push again. Human review checks content that CI cannot judge.

<details>
<summary>If your branch is behind or has a conflict</summary>

Other students' merges change `main`. On your feature branch, commit your work, then:

```sh
git fetch origin
git merge origin/main
```

If there is a conflict, edit the affected files. Keep everyone's roster entries and
remove the `<<<<<<<`, `=======`, and `>>>>>>>` markers. Then:

```sh
python3 scripts/validate.py
git add index.html
git commit -m "Resolve roster conflict"
git push
```

Stage any other resolved files too. If the merge had no conflicts, just validate
and push. Stay on your feature branch; no force push is needed. Request renewed approval.

</details>

<details>
<summary>CI failure exercise — only when instructed</summary>

On your open feature branch, change `<h1>…</h1>` to `<h2>…</h2>`, commit, and push.
Find the missing-heading error in the PR's check. Restore the `<h1>` tags, validate,
commit, and push again. Watch CI turn green. Keep the broken version off `main`.

</details>

## 6. Merge and update

Merge when the task is complete, feedback is addressed, another student has approved,
**Validate website** passes, and conflicts are resolved. New commits may require fresh approval.

Choose **Squash and merge**: one completed PR becomes one commit on `main`.
The other options keep individual commits: **merge commit** joins the histories;
**rebase and merge** replays the commits with new IDs.

```sh
git switch main
git pull --ff-only
```

**CD** automatically deploys validated changes from `main` to GitHub Pages.
Wait for deployment in **Actions**, then check your profile at the class website URL.
Start future tasks on a new branch from updated `main`.
