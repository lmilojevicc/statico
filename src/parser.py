from extract import extract_markdown_images, extract_markdown_links
from text_node import TextNode, TextType


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
