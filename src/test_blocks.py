import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockType(unittest.TestCase):
    def assert_blocks_are_type(self, markdown: str, expected_type: BlockType):
        for block in markdown_to_blocks(markdown):
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected_type)

    def test_paragraph(self):
        block = "This is a normal paragraph with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This is a normal paragraph\n with **bold** and _italic_ text.\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_valid_ordered_list(self):
        text = """
1. one
2. two
3. three
4. four

1. 
2. 
3. 
        """
        self.assert_blocks_are_type(text, BlockType.ORDERED_LIST)

    def test_invalid_ordered_list(self):
        text = """
1.one
2.two
3.three
4.four

1.
6.
2.
5.
        """
        self.assert_blocks_are_type(text, BlockType.PARAGRAPH)

    def test_empty_block(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_code(self):
        text = """
```
print("hello world")
```

```
func main() int {
    return 0;
}
```
        """
        self.assert_blocks_are_type(text, BlockType.CODE)

    def test_code_only_open(self):
        text = """
```
print("hello world")
diofweiomj
vmwioefiow
ew
        """
        self.assert_blocks_are_type(text, BlockType.PARAGRAPH)

    def test_code_only_close(self):
        text = """
print("hello world")
diofweiomj
vmwioefiow
ew
```
        """
        self.assert_blocks_are_type(text, BlockType.PARAGRAPH)

    def test_quote(self):
        text = """
> This is quote

> This is multiline quote
> wiht some more lines

>this is quote without space

>this is quote without space
>and new line
        """
        self.assert_blocks_are_type(text, BlockType.QUOTE)

    def test_invalid_quote(self):
        block = "> This starts as a quote\nbut this line does not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        text = """
- unordered
- lists
- are the best
        """
        self.assert_blocks_are_type(text, BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list(self):
        text = """
-unordered
- lists
- are the best
 
 -
        """
        self.assert_blocks_are_type(text, BlockType.PARAGRAPH)

    def test_headings(self):
        text = """
# This is heading

## This is heading

### This is heading

#### This is heading

##### This is heading

###### This is heading

# C# notes
        """
        self.assert_blocks_are_type(text, BlockType.HEADING)

    def test_invalid_headings(self):
        text = """
######## Invalid

#This is not heading
##This is not heading
###This is not heading
####This is not heading
#####This is not heading
######This is not heading

#This is not heading

##This is not heading

###This is not heading

####This is not heading

#####This is not heading

######This is not heading

#

###

####

#####

######

        """
        self.assert_blocks_are_type(text, BlockType.PARAGRAPH)
