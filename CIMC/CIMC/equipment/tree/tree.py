
class Node(object):

    def __init__(self, name, type, url, equipment_id):
        self.id = None
        self.text = name
        self.type = type
        self.data = {'url': url}
        self.children = []

    def to_jstree(self):
        return {'id': self.id,
                'text': self.text,
                'type': self.type,
                'data': self.data,
                'children': self.children }


class Tree(object):

    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def to_jstree(self):
        js_tree = {}
        js_tree.update({'text': self.name, 'children': [], "state": {"opened": True}})

        for node in self.nodes:
            js_tree['children'].append(node.to_jstree())
        return js_tree
