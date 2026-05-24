import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING
    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(
        line.startswith(f"{i}. ") or (i == len(lines) and line == f"{i}.")
        for i, line in enumerate(lines, start=1)
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
