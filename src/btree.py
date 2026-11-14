
class BTreeNode:

    def __init__(self, leaf=False):
        self.keys = []
        self.values = []
        self.children = []
        self.leaf = leaf


class BTree:

    def __init__(self, degree=3):

        if degree < 2:
            raise ValueError("B-tree degree must be at least 2.")

        self.degree = degree
        self.root = BTreeNode(leaf=True)

    def search(self, key):

        return self._search(self.root, key)

    def _search(self, node, key):

        index = 0

        while index < len(node.keys) and key > node.keys[index]:
            index += 1

        if index < len(node.keys) and key == node.keys[index]:
            return node.values[index]

        if node.leaf:
            return None

        return self._search(node.children[index], key)

    def insert(self, key, value):

        if self.search(key) is not None:
            raise ValueError(f"Duplicate key: {key}")

        root = self.root

        if len(root.keys) == 2 * self.degree - 1:

            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)

            self._split_child(new_root, 0)

            self.root = new_root

        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):

        index = len(node.keys) - 1

        if node.leaf:

            node.keys.append(None)
            node.values.append(None)

            while index >= 0 and key < node.keys[index]:

                node.keys[index + 1] = node.keys[index]
                node.values[index + 1] = node.values[index]

                index -= 1

            node.keys[index + 1] = key
            node.values[index + 1] = value

        else:

            while index >= 0 and key < node.keys[index]:
                index -= 1

            index += 1

            if len(node.children[index].keys) == 2 * self.degree - 1:

                self._split_child(node, index)

                if key > node.keys[index]:
                    index += 1

            self._insert_non_full(
                node.children[index],
                key,
                value
            )

    def _split_child(self, parent, index):

        degree = self.degree

        full_child = parent.children[index]

        new_child = BTreeNode(leaf=full_child.leaf)

        middle_key = full_child.keys[degree - 1]
        middle_value = full_child.values[degree - 1]

        new_child.keys = full_child.keys[degree:]
        new_child.values = full_child.values[degree:]

        full_child.keys = full_child.keys[:degree - 1]
        full_child.values = full_child.values[:degree - 1]

        if not full_child.leaf:

            new_child.children = full_child.children[degree:]
            full_child.children = full_child.children[:degree]

        parent.children.insert(index + 1, new_child)

        parent.keys.insert(index, middle_key)
        parent.values.insert(index, middle_value)

    def inorder(self):

        result = []

        self._inorder(self.root, result)

        return result

    def _inorder(self, node, result):

        for index, key in enumerate(node.keys):

            if not node.leaf:
                self._inorder(node.children[index], result)

            result.append((key, node.values[index]))

        if not node.leaf:
            self._inorder(node.children[-1], result)

    def __len__(self):

        return len(self.inorder())
