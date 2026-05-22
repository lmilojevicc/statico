from html_node import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parennt node must have tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}>{result}</{self.tag}>"
