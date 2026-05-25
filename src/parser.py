import re

import conversion
from blocks import BlockType, block_to_block_type, markdown_to_blocks
from extract import extract_markdown_images, extract_markdown_links
from html_node import HTMLNode
from leaf_node import LeafNode
from parent_node import ParentNode
from text_node import TextNode, TextType


def text_to_children(text: str) -> list[HTMLNode]:
    if text == "":
        return [LeafNode(None, "")]
    text_nodes = text_to_textnodes(text)
    return [conversion.text_node_to_html_node(text_node) for text_node in text_nodes]


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))

    return ParentNode("div", children)


def paragraph_to_html_node(block: str) -> HTMLNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block: str) -> HTMLNode:
    heading_level = 0
    for ch in block:
        if ch != "#":
            break
        heading_level += 1

    text = block[heading_level + 1 :]
    return ParentNode(f"h{heading_level}", text_to_children(text))


def code_to_html_node(block: str) -> HTMLNode:
    text = block[4:-3]
    return ParentNode("pre", [LeafNode("code", text)])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        if line.startswith("> "):
            clean_lines.append(line[2:])
        else:
            clean_lines.append(line[1:])

    text = " ".join(clean_lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block: str) -> HTMLNode:
    children = []
    for item in block.split("\n"):
        text = item[2:]
        children.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ul", children)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    children = []
    for item in block.split("\n"):
        text = re.sub(r"^\d+\.(?: |$)", "", item, count=1)
        children.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ol", children)


def text_to_textnodes(text: str) -> list[TextNode]:
    plain_text_node = TextNode(text, TextType.TEXT)
    text_nodes = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([plain_text_node], "**", TextType.BOLD),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
    return text_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        extracted_images = extract_markdown_images(original_text)
        if not extracted_images:
            new_nodes.append(node)
            continue

        for altImgText, imgURL in extracted_images:
            parts = original_text.split(f"![{altImgText}]({imgURL})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(altImgText, TextType.IMAGE, imgURL))
            original_text = parts[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        extracted_links = extract_markdown_links(original_text)
        if not extracted_links:
            new_nodes.append(node)
            continue

        for linkText, url in extracted_links:
            parts = original_text.split(f"[{linkText}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(linkText, TextType.LINK, url))
            original_text = parts[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(
                f"invalid Markdown format: formatted section not closed for '{delimiter}'"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue

            # Even indices are outside the delimiter (plain text)
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            # Odd indices are inside the delimiter (formatted text)
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
