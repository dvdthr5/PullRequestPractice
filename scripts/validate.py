#!/usr/bin/env python3
"""Small classroom checks, not a full HTML standards or accessibility validator."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "index.html",
    "styles.css",
    "README.md",
    "scripts/validate.py",
    ".github/workflows/ci.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/add-student-profile.md",
)
VOID_TAGS = set("area base br col embed hr img input link meta param source track wbr".split())


class Page(HTMLParser):
    """Check explicit tag nesting and collect headings and local references."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.tags = set()
        self.errors = []
        self.references = []
        self.doctype = False
        self.language = False
        self.heading = ""
        self.title = ""

    def handle_decl(self, declaration):
        if declaration.lower().strip() == "doctype html":
            self.doctype = True

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        self.tags.add(tag)
        if tag == "html":
            self.language = bool((attributes.get("lang") or "").strip())
        if tag in ("head", "body") and self.stack != ["html"]:
            self.errors.append(f"Place <{tag}> directly inside <html>.")
        if tag == "title" and "head" not in self.stack:
            self.errors.append("Place <title> inside <head>.")
        for attribute in ("href", "src"):
            if attribute in attributes:
                self.references.append((tag, attribute, attributes[attribute] or ""))
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attributes):
        # HTML permits <br /> and <meta ... />. Other elements still need
        # explicit closing tags: <h1 /> is not a self-closing HTML heading.
        self.handle_starttag(tag, attributes)

    def handle_endtag(self, tag):
        if tag not in self.stack:
            self.errors.append(f"Unexpected </{tag}>; check the opening tag.")
        else:
            if self.stack[-1] != tag:
                self.errors.append(f"Close <{self.stack[-1]}> before </{tag}>.")
            # Recover so one mistake does not hide checks later in the page.
            while self.stack[-1] != tag:
                self.stack.pop()
            self.stack.pop()

    def handle_data(self, data):
        if "h1" in self.stack:
            self.heading += data
        if "title" in self.stack:
            self.title += data

    def finish(self):
        self.close()
        if self.stack:
            self.errors.append("Add closing tags for: " + ", ".join(self.stack) + ".")
        if not self.doctype:
            self.errors.append("Start the page with <!doctype html>.")
        for tag in ("html", "head", "title", "body"):
            if tag not in self.tags:
                self.errors.append(f"Add the required <{tag}> element.")
        if not self.language:
            self.errors.append('Set the page language, for example <html lang="en">.')
        if not self.title.strip():
            self.errors.append("Add a nonempty <title> inside <head>.")


def validate(root=ROOT):
    """Return readable errors; never change any repository files."""
    root = Path(root).resolve()
    errors = []
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"{name}: Required file is missing; restore or create it.")

    profiles = sorted((root / "students").glob("*.html"))
    homepage = root / "index.html"
    roster = []
    for path in [homepage] + profiles:
        if not path.is_file():
            continue
        name = path.relative_to(root).as_posix()
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"{name}: Save this file using UTF-8 encoding.")
            continue
        page = Page()
        page.feed(source)
        page.finish()
        if re.search(r"^(?:<{7}|={7}|>{7})(?:\s|$)", source, re.MULTILINE):
            page.errors.append("Resolve the Git conflict markers before committing.")
        targets = []
        for tag, attribute, reference in page.references:
            try:
                url = urlsplit(reference)
            except ValueError:
                page.errors.append(f"Invalid {attribute}: {reference!r}; fix the URL.")
                continue
            if url.scheme or url.netloc:
                continue  # External links are not requested over the network.
            if not reference.strip():
                page.errors.append(f"Give <{tag}> a nonempty {attribute} value.")
                continue
            if not url.path:
                continue  # Fragment targets are outside this small check's scope.
            local_path = unquote(url.path)
            if local_path.startswith("/"):
                page.errors.append(f"Use a relative URL for {reference!r} so GitHub Pages works.")
                continue
            target = (path.parent / local_path).resolve()
            if not target.is_relative_to(root):
                page.errors.append(f"{reference!r} points outside this repository; fix the path.")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                page.errors.append(f"Broken local link {reference!r}; create the file or fix the path.")
            if tag == "a" and attribute == "href":
                targets.append(target)
        if path in profiles:
            if not page.heading.strip():
                page.errors.append("Add a nonempty <h1>Your name</h1> to your profile.")
            if homepage not in targets:
                page.errors.append('Add a homepage link: <a href="../index.html">Back to home</a>.')
        else:
            roster = targets
        errors.extend(f"{name}: {error}" for error in page.errors)

    for profile in profiles:
        count = roster.count(profile.resolve())
        if count != 1:
            name = profile.relative_to(root).as_posix()
            errors.append(f"index.html: Link to {name} exactly once in the roster (found {count}).")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("Validation failed. Fix these problems, commit, and push again:")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    print("Validation passed: required files, HTML structure, profile headings, and local links.")
