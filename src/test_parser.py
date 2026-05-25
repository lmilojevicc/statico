import unittest

from blocks import markdown_to_blocks
from parser import (
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from text_node import TextNode, TextType


class TestHTMLParsing(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        node = markdown_to_html_node("# Heading **bold**")
        self.assertEqual(node.to_html(), "<div><h1>Heading <b>bold</b></h1></div>")

    def test_quote(self):
        md = """
> This is a **quote**
> with _italic_
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a <b>quote</b> with <i>italic</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- one
- two with **bold**
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>one</li><li>two with <b>bold</b></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. one
2. two with _italic_
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two with <i>italic</i></li></ol></div>",
        )

    def test_empty_ordered_list_items(self):
        md = """
1. 
2. 
3. 
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li></li><li></li><li></li></ol></div>",
        )


class TestBlockParsing(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_of_new_lines(self):
        md = """

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_markdown_of_excessive_new_lines(self):
        md = """
This is text


More text


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is text", "More text"],
        )


class TestFullTextParsing(unittest.TestCase):
    def test_text_with_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_plain_text(self):
        nodes = text_to_textnodes("This is plain text with no markdown")
        self.assertListEqual(
            [TextNode("This is plain text with no markdown", TextType.TEXT)],
            nodes,
        )

    def test_text_with_only_inline_styles(self):
        nodes = text_to_textnodes("**bold** then _italic_ then `code`")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" then ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" then ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

    def test_text_with_images_and_links(self):
        nodes = text_to_textnodes(
            "Look ![first](https://example.com/first.png) and [second](https://example.com)"
        )
        self.assertListEqual(
            [
                TextNode("Look ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "https://example.com/first.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_text_with_markdown_at_beginning_and_end(self):
        nodes = text_to_textnodes("**Start** middle [end](https://example.com)")
        self.assertListEqual(
            [
                TextNode("Start", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_text_with_adjacent_markdown_nodes(self):
        nodes = text_to_textnodes(
            "**bold**_italic_`code`![image](https://example.com/img.png)[link](https://example.com)"
        )
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_text_with_multiple_links_and_images(self):
        nodes = text_to_textnodes(
            "![one](https://example.com/1.png) [boot](https://boot.dev) ![two](https://example.com/2.png) [docs](https://docs.python.org)"
        )
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("boot", TextType.LINK, "https://boot.dev"),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://docs.python.org"),
            ],
            nodes,
        )

    def test_code_node_does_not_split_links_or_images(self):
        nodes = text_to_textnodes(
            "Use `[not a link](https://example.com)` and `![not an image](https://example.com/img.png)`"
        )
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("[not a link](https://example.com)", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("![not an image](https://example.com/img.png)", TextType.CODE),
            ],
            nodes,
        )


class TestImageAndLinkParsing(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This is text with an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_text_after(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This is text with a link(https://i.imgur.com/zjjcJKZ.png) and another link(https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a link(https://i.imgur.com/zjjcJKZ.png) and another link(https://i.imgur.com/3elNhQu.png)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )


class TestInlineMarkdown(unittest.TestCase):
    def test_regular_text(self):
        node = TextNode("This is text with words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with words", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
