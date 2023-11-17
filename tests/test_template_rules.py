import unittest

from source.server.utils import TemplateRules


class TestTemplateRules(unittest.TestCase):
    def test_loc_with_leadingslash(self):
        self.assertEqual(
            TemplateRules.render_html_segment("/read.html"), "components/read.html"
        )

    def test_loc_without_leadingslash(self):
        self.assertEqual(
            TemplateRules.render_html_segment("read.html"), "components/read.html"
        )

    def test_loc_with_trailing_html_extension(self):
        self.assertEqual(
            TemplateRules.render_html_segment("/read.html", component=False),
            "sections/read.html",
        )

    def test_loc_without_trailing_html_extension(self):
        self.assertEqual(
            TemplateRules.render_html_segment("read", component=False),
            "sections/read.html",
        )
        self.assertEqual(
            TemplateRules.render_html_segment(
                "/read",
            ),
            "components/read.html",
        )
