class AVLT:

    class Node:
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = AVLT.Node(data)
        else:
            self._insert(data, self.root)

    def _insert(self, data, node):
        if node is None:
            return AVLT.Node(data)

        if data < node.data:
            node.left = self._insert(data, node.left)
        elif data > node.data:
            node.right = self._insert(data, node.right)
        else:
            return node

        node.height = max(self.get_height(node.left),
                          self.get_height(node.right)) + 1
        balance = self.get_balance(node)

        if balance > 1 and data < node.left.data:
            return self.right_rotate(node)
        if balance > 1 and data > node.left.data:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and data > node.right.data:
            return self.left_rotate(node)
        if balance < -1 and data < node.right.data:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, node):

        new_node = node.right
        t2 = new_node.left

        new_node.left = node
        node.right = t2

        node.height = max(self.get_height(node.left),
                          self.get_height(node.right)) + 1

        new_node.height = max(self.get_height(new_node.left),
                              self.get_height(new_node.right)) + 1

        if self.root == new_node.left:
            self.root = new_node

        return new_node

    def right_rotate(self, node):

        new_node = node.left
        t2 = new_node.right

        new_node.right = node
        node.left = t2

        node.height = max(self.get_height(node.left),
                          self.get_height(node.right)) + 1
        new_node.height = max(self.get_height(new_node.left),
                              self.get_height(new_node.right)) + 1

        if self.root == new_node.right:
            self.root = new_node

        return new_node

    def __contains__(self, data):
        return self._contains(data, self.root)

    def _contains(self, data, node):
        if node is not None:
            if data < node.data:
                return self._contains(data, node.left)
            elif data > node.data:
                return self._contains(data, node.right)
            elif data == node.data:
                return True
        else:
            return False

    def __iter__(self):
        yield from self._traverse_forward(self.root)

    def _traverse_forward(self, node):
        if node is not None:
            yield from self._traverse_forward(node.left)
            yield node.data
            yield from self._traverse_forward(node.right)

    def __reversed__(self):
        yield from self._traverse_backward(self.root)

    def _traverse_backward(self, node):
        if node is not None:
            yield from self._traverse_backward(node.right)
            yield node.data
            yield from self._traverse_backward(node.left)

    def display(self):
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is None and node.left is None:
            line = '%s' % node.data
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is None:
            lines, n, p, x = self._display_aux(node.left)
            s = '%s' % node.data
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is None:
            lines, n, p, x = self._display_aux(node.right)
            s = '%s' % node.data
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = '%s' % node.data
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * \
            '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + \
            (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + \
            [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
