class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        else:
            pairs = [f'{k}="{self.props[k]}"' for k in sorted(self.props.keys())]
            return " " + " ".join(pairs) if pairs else ""

    def __repr__(self):
        children_count = len(self.children) if self.children else 0
        props_str = str(self.props) if self.props else None
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={children_count}, props={props_str})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value

        attrs = self.props_to_html()
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"
