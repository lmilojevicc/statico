import unittest

from extract import extract_markdown_images, extract_markdown_links, extract_title


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with [external link](https://external.com)"
        )
        self.assertListEqual([("external link", "https://external.com")], matches)

    def test_invalid_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an !image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_invalid_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with [external link]https://external.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_plain_title(self):
        title = extract_title("""
        # Title

        this is some text
        that has title
        """)
        self.assertEqual(title, "Title")

    def test_extract_title_with_styles(self):
        title = extract_title("""
        # _Title_

        this is some text
        that has title
        """)
        self.assertEqual(title, "_Title_")

    def test_extract_title_without_title(self):
        with self.assertRaisesRegex(ValueError, "H1 Title must be present"):
            extract_title("""
    this is some text
    that has title
    """)
