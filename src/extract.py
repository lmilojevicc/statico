import re

from blocks import BlockType, block_to_block_type, markdown_to_blocks


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_title(markdown: str) -> str:
    for block in markdown_to_blocks(markdown):
        if block.startswith("# "):
            return block[2:].strip()
    raise ValueError("H1 Title must be present in the document")
