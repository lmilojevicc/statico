from extract import extract_markdown_images, extract_markdown_links
from text_node import TextNode, TextType


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    if not old_nodes:
        return []

    new_nodes = []

    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if not extracted_images:
            new_nodes.append(node)
            continue

        i = 0
        while node.text:
            if i == len(extracted_images):
                new_nodes.append(node)
                break
            altImgText, imgURL = extracted_images[i]
            parts = node.text.split(f"![{altImgText}]({imgURL})", 1)

            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(altImgText, TextType.IMAGE, imgURL))
            if len(parts) == 1:
                break
            node = TextNode(parts[1], TextType.TEXT)
            i += 1

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    if not old_nodes:
        return []

    new_nodes = []

    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue

        i = 0
        while node.text:
            if i == len(extracted_links):
                new_nodes.append(node)
                break
            linkText, url = extracted_links[i]
            parts = node.text.split(f"[{linkText}]({url})", 1)

            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(linkText, TextType.LINK, url))
            if len(parts) == 1:
                break
            node = TextNode(parts[1], TextType.TEXT)
            i += 1

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
