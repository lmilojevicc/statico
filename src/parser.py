from text_node import TextNode, TextType


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
