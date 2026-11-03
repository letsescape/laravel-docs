"""빌드 HTML 앵커 검사와 독립 CLI의 회귀 검사."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from sync.verification import anchors


class HtmlAnchorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "build"
        self.write("index.html", '<link rel="canonical" href="https://example.test/">')

    def write(self, relative, html):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        return path

    def test_uses_rendered_links_and_ignores_comments_and_code_text(self):
        self.write("docs/13.x/index.html", """
<h2 id="real-anchor">Example</h2>
<a href="#real-anchor"><strong>Nested <code>label</code></strong></a>
<!-- <a href="#comment-only">Hidden</a> -->
<pre><code>&lt;a href="#code-only"&gt;Example&lt;/a&gt;</code></pre>
<script>const example = '<a href="#script-only">Example</a>';</script>
""")
        self.assertEqual(anchors.validate_anchors(self.root), (1, []))

    def test_resolves_relative_paths_query_encoding_and_named_anchors(self):
        self.write("index.html", '<link rel="canonical" href="https://example.test/project/">')
        self.write("docs/13.x/index.html", '<h1 id="installation">Install</h1>')
        self.write("docs/13.x/한글/index.html", '<h2 id="한글 앵커">Korean</h2>')
        self.write("docs/13.x/nested/other/index.html", '<h2 id="target">Target</h2>')
        self.write("docs/13.x/nested/custom/index.html", """
<h2 id="signed urls">Signed URLs</h2>
<h2 id="a&amp;b&quot;c">Escaped attribute</h2>
<a name="legacy"></a>
<a href="?source=cache#signed%20urls">Same page</a>
<a href="#a%26b%22c">Entity</a>
<a href="#legacy">Named anchor</a>
<a href="../other/#target">Sibling</a>
<a href="../other?source=cache#target">Slashless sibling</a>
<a href="../../#installation">Version root</a>
<a href="/project/docs/13.x/#installation">Absolute root</a>
<a href="../../%ED%95%9C%EA%B8%80/#%ED%95%9C%EA%B8%80%20%EC%95%B5%EC%BB%A4">Encoded path</a>
""")
        self.assertEqual(anchors.validate_anchors(self.root), (8, []))

    def test_uses_actual_locale_paths_without_rewriting_root_relative_links(self):
        self.write("docs/13.x/index.html", '<h1 id="ko">Korean</h1>')
        self.write("ja/docs/13.x/index.html", """
<h1 id="ja">Japanese</h1>
<a href="#ja">This page</a>
<a href="/docs/13.x/#ko">Korean</a>
<a href="/ja/docs/13.x/#ja">Japanese</a>
""")
        self.assertEqual(anchors.validate_anchors(self.root), (3, []))

    def test_accepts_empty_fragments_only_when_the_target_page_exists(self):
        self.write("docs/13.x/index.html", '<a href="#">Top</a><a href="missing/#">Missing</a>')
        total, broken = anchors.validate_anchors(self.root)
        self.assertEqual(total, 2)
        self.assertEqual(len(broken), 1)
        self.assertIn("target HTML missing", broken[0])

    def test_accepts_same_origin_absolute_links_and_excludes_external_links(self):
        self.write("docs/13.x/index.html", """
<h2 id="target">Target</h2>
<a href="https://example.test/docs/13.x/#target">Same origin</a>
<a href="https://example.test:443/docs/13.x/#target">Default port</a>
<a href="//example.test/docs/13.x/#target">Protocol relative</a>
<a href="https://elsewhere.test/docs/missing/#bad">External host</a>
<a href="http://example.test/docs/missing/#bad">Other scheme</a>
<a href="https://example.test:8443/docs/missing/#bad">Other port</a>
<a href="//elsewhere.test/docs/missing/#bad">External protocol relative</a>
<a href="mailto:user@example.test#bad">Mail</a>
<a href="custom:resource#bad">Custom scheme</a>
<a href="/docs/missing/">No fragment</a>
<a href="/unrelated-page/#bad">Outside docs</a>
""")
        self.assertEqual(anchors.validate_anchors(self.root), (3, []))

    def test_supports_html_files_and_does_not_guess_markdown_filenames(self):
        self.write("docs/13.x/renamed.html", '<h2 id="target">Target</h2>')
        self.write("docs/13.x/index.html", '<a href="renamed.html#target">Custom route</a>')
        self.assertEqual(anchors.validate_anchors(self.root), (1, []))

    def test_does_not_reapply_stale_link_rules_to_rendered_hrefs(self):
        self.write("docs/10.x/migrations/index.html", """
<h2 id="generating-migrations">Current</h2>
<a href="#writing-migrations">Still broken in HTML</a>
""")
        total, broken = anchors.validate_anchors(self.root)
        self.assertEqual(total, 1)
        self.assertEqual(len(broken), 1)
        self.assertIn("anchor id/name not found", broken[0])
        self.assertIn("docs/10.x/migrations/index.html:3 -> #writing-migrations", broken[0])

    def test_reports_missing_pages_and_missing_anchors_separately(self):
        self.write("docs/13.x/index.html", '<a href="#missing">Anchor</a><a href="missing/#id">Page</a>')
        total, broken = anchors.validate_anchors(self.root)
        self.assertEqual(total, 2)
        self.assertEqual(len(broken), 2)
        self.assertIn("anchor id/name not found", broken[0])
        self.assertIn("target HTML missing", broken[1])

    def test_reports_malformed_urls_and_continues_checking_later_links(self):
        self.write("docs/13.x/index.html", """
<a href="https://example.test:abc/docs/13.x/#bad">Invalid port</a>
<a href="https://[::1/docs/13.x/#bad">Invalid IPv6</a>
<h2 id="ok">Valid anchor</h2>
<a href="#ok">Valid link</a>
<a href="#missing">Missing anchor</a>
""")
        total, broken = anchors.validate_anchors(self.root)
        self.assertEqual(total, 4)
        self.assertEqual(len(broken), 3)
        self.assertIn("docs/13.x/index.html:2 -> https://example.test:abc/docs/13.x/#bad", broken[0])
        self.assertIn("docs/13.x/index.html:3 -> https://[::1/docs/13.x/#bad", broken[1])
        self.assertIn("docs/13.x/index.html:6 -> #missing: anchor id/name not found", broken[2])

    def test_rejects_invalid_fragment_and_path_encoding(self):
        self.write("docs/13.x/index.html", """
<a href="#%E0%A4">Invalid UTF-8</a>
<a href="#%ZZ">Invalid escape</a>
<a href="/docs/13.x/%E0%A4/#id">Invalid path</a>
""")
        total, broken = anchors.validate_anchors(self.root)
        self.assertEqual(total, 3)
        self.assertEqual(len(broken), 3)
        self.assertTrue(all("invalid URL encoding" in item for item in broken))

    def test_rejects_paths_and_symlinks_outside_the_build(self):
        outside = self.root.parent / "outside.html"
        outside.write_text('<h2 id="private">Private</h2>', encoding="utf-8")
        self.write("docs/13.x/index.html", """
<a href="/docs/%2e%2e/%2e%2e/outside.html#private">Traversal</a>
<a href="outside.html#private">Symlink</a>
""")
        (self.root / "docs/13.x/outside.html").symlink_to(outside)
        total, broken = anchors.validate_anchors(self.root)
        self.assertEqual(total, 2)
        self.assertEqual(len(broken), 2)
        self.assertTrue(all("target path outside build" in item for item in broken))

    def test_rejects_doc_paths_outside_the_configured_base_url(self):
        self.write("index.html", '<link rel="canonical" href="https://example.test/project/">')
        self.write("docs/13.x/index.html", '<a href="/docs/13.x/#id">Outside base URL</a>')
        total, broken = anchors.validate_anchors(self.root)
        self.assertEqual(total, 1)
        self.assertIn("target path outside build", broken[0])

    def test_cli_runs_without_site_packages_and_preserves_exit_codes(self):
        script = str(Path(anchors.__file__).resolve())

        def run(path):
            return subprocess.run(
                [sys.executable, "-S", script, str(path)],
                cwd=self.temporary.name, capture_output=True, text=True, check=False,
            )

        self.write("docs/13.x/index.html", '<h1 id="ok">OK</h1><a href="#ok">Valid</a>')
        valid = run(self.root)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertIn("Total HTML anchor links: 1", valid.stdout)

        self.write("docs/13.x/index.html", '<a href="#missing">Invalid</a>')
        invalid = run(self.root)
        self.assertEqual(invalid.returncode, 1, invalid.stderr)
        self.assertIn("docs/13.x/index.html:1 -> #missing", invalid.stdout)

        missing = run(self.root / "absent")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("build directory not found", missing.stderr)

        (self.root / "index.html").unlink()
        incomplete = run(self.root)
        self.assertEqual(incomplete.returncode, 2)
        self.assertIn("canonical URL", incomplete.stderr)


if __name__ == "__main__":
    unittest.main()
