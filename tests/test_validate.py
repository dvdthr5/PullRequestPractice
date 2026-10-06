"""Exercise CI feedback using temporary repositories, without changing the website."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts.validate import REQUIRED_FILES, ROOT, validate


def html(body):
    return (
        '<!doctype html><html lang="en"><head><title>Class</title>'
        f'</head><body>{body}</body></html>'
    )


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for name in REQUIRED_FILES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Fixture file\n", encoding="utf-8")
        self.write("index.html", html('<a href="students/example.html">Example</a>'))
        self.profile = '<h1>Example Student</h1><a href="../index.html">Home</a>'
        self.write("students/example.html", html(self.profile))

    def write(self, name, content):
        (self.root / name).write_text(content, encoding="utf-8")

    def messages(self):
        return "\n".join(validate(self.root))

    def test_valid_repository_and_equivalent_backlink(self):
        self.write("students/example.html", html(self.profile.replace("../", "./../")))
        self.assertEqual(validate(self.root), [])

    def test_missing_required_file(self):
        (self.root / "styles.css").unlink()
        self.assertIn("styles.css: Required file is missing", self.messages())

    def test_missing_heading_fails_cli_from_another_directory(self):
        self.write("students/example.html", html('<!-- <h1>Name</h1> --><a href="../index.html">Home</a>'))
        shutil.copyfile(ROOT / "scripts/validate.py", self.root / "scripts/validate.py")
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/validate.py")],
            cwd=self.root.parent, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("students/example.html: Add a nonempty <h1>", result.stdout)

    def test_comment_is_not_a_homepage_link(self):
        self.write("students/example.html", html('<h1>Name</h1><!-- <a href="../index.html">Home</a> -->'))
        self.assertIn("students/example.html: Add a homepage link", self.messages())

    def test_broken_roster_link(self):
        self.write("index.html", html('<a href="students/missing.html">Missing</a>'))
        messages = self.messages()
        self.assertIn("Broken local link 'students/missing.html'", messages)
        self.assertIn("Link to students/example.html exactly once", messages)

    def test_malformed_nesting(self):
        self.write("students/example.html", html(self.profile + "<p><strong>Oops</p></strong>"))
        self.assertIn("Close <strong> before </p>", self.messages())

    def test_nested_same_tags_are_valid(self):
        self.write("students/example.html", html(self.profile + "<ul><li>A<ul><li>B</li></ul></li></ul>"))
        self.assertEqual(validate(self.root), [])

    def test_void_tags_with_trailing_slash_are_valid(self):
        page = html(self.profile + "<p>Hello<br />World</p>")
        page = page.replace("<head>", '<head><meta charset="utf-8" />')
        self.write("students/example.html", page)
        self.assertEqual(validate(self.root), [])

    def test_self_closed_heading_still_requires_closing_tag(self):
        self.write("students/example.html", html(self.profile.replace("<h1>", "<h1 />").replace("</h1>", "")))
        self.assertIn("Close <h1> before </body>", self.messages())

    def test_conflict_markers(self):
        self.write("students/example.html", html(self.profile + "\n<<<<<<< HEAD\n=======\n>>>>>>> main\n"))
        self.assertIn("Resolve the Git conflict markers", self.messages())


if __name__ == "__main__":
    unittest.main()
