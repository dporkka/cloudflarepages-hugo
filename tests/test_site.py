"""Validate the pinned Book starter without adding deployment dependencies."""
from html.parser import HTMLParser
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
HUGO = os.environ.get("HUGO_BIN") or shutil.which("hugo")


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag in {"a", "link", "script", "img"}:
            url = values.get("href") or values.get("src")
            if url:
                self.urls.append(url)


@unittest.skipUnless(HUGO, "Install Hugo 0.170.0 or set HUGO_BIN")
class StarterTests(unittest.TestCase):
    def test_root_and_nested_builds(self):
        for prefix in ("/", "/notes/"):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as temp:
                output = Path(temp)
                base = "https://example.org" + prefix
                subprocess.run([HUGO, "--source", str(ROOT), "--destination", str(output),
                                "--baseURL", base, "--minify", "--panicOnWarning"], check=True)
                for required in ("index.html", "docs/topic1/index.html",
                                 "docs/topic1/subtopic1/anotherpage/index.html",
                                 "docs/topic3/subtopic2/index.html"):
                    self.assertTrue((output / required).is_file(), required)
                pages = sorted(output.rglob("*.html"))
                self.assertGreaterEqual(len(pages), 12)
                for page in pages:
                    parser = References()
                    parser.feed(page.read_text(encoding="utf-8"))
                    path = page.relative_to(output).as_posix()
                    for link in parser.urls:
                        uri = urlsplit(urljoin(base + path, link))
                        if uri.netloc != "example.org":
                            continue
                        self.assertTrue(uri.path.startswith(prefix), (path, link))
                        target = output / unquote(uri.path[len(prefix):])
                        if target.is_dir():
                            target /= "index.html"
                        self.assertTrue(target.is_file(), (path, link))


if __name__ == "__main__":
    unittest.main()
