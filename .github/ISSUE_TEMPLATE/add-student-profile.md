---
name: Add Student Profile
about: Create a student profile and add it to the class homepage.
title: "Add student profile: NAME"
labels: ""
assignees: ""
---

Create your student profile and add yourself to the class homepage. The instructor should replace NAME in the title and assign this issue to one student.

## Requirements

- [ ] Create `students/<name>.html` by copying `students/example.html`.
- [ ] Add your name as the page title and `<h1>` heading.
- [ ] Add an About Me section.
- [ ] Add your interests.
- [ ] Add your project or research interests.
- [ ] Keep a link back to `../index.html`.
- [ ] Add your profile link to the roster in `index.html`, keeping all existing entries.
- [ ] Run `python3 scripts/validate.py` and test both links in a browser.
- [ ] Open a pull request into `main` and reference this issue with `Closes #NUMBER`.

Use a branch named `add-<name>-profile`. Replace `<name>` with a unique lowercase name or handle without spaces. Follow `README-STUDENT.md` to review a classmate's PR, respond to feedback, and merge after approval and passing CI.
