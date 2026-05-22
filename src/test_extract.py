import unittest

from extract import extract_markdown_images, extract_markdown_links


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
