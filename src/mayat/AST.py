from hashlib import sha256


class ASTGenerationException(Exception):
    pass
class ASTSearchException(Exception):
    pass


# Base class for Abstract Syntax Trees
class AST:
    def __init__(self, parent=None, name=None, text=None, start_pos=None, end_pos=None, kind=None):
        self.parent = parent
        self.name = name
        self.text = text
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.kind = kind
        self.children = []
        self.fingerprint = None
        self.weight = 0

    def hash(self):
        """
        Hash this node by concatenating the kind and its children's fingerprints

        Returns:
            The fingerprint(hash value)
        """
        child_fingerprints = "".join(c.hash() for c in self.children)
        self.fingerprint = sha256(
            (self.kind + child_fingerprints).encode()
        ).hexdigest()

        return self.fingerprint

    def hash_non_recursive(self):
        """
        Equivalent to hash() but non-recursive
        """
        stack = [(self, iter(self.children))]

        while len(stack) > 0:
            (curr_node, curr_node_children_iter) = stack[-1]

            try:
                child_node = next(curr_node_children_iter)
                stack.append((child_node, iter(child_node.children)))
            except StopIteration:
                child_fingerprints = "".join(c.fingerprint for c in curr_node.children)
                curr_node.fingerprint = sha256(
                    (curr_node.kind + child_fingerprints).encode()
                ).hexdigest()
                stack.pop()

    def display(self, level=0):
        """
        Recursively print out the entire tree structure

        Arguments:
            level: The level of this node(for indentation purpose)
        """
        print("    " * level + str(self))
        for child in self.children:
            child.display(level + 1)

    def __str__(self):
        return f"<{self.name}, {self.start_pos}-{self.end_pos}, {self.kind}, {self.weight}>"

    def __repr__(self):
        return str(self)

    def preorder(self):
        """
        The preorder traversal of this tree

        Returns:
            A list of nodes in preorder
        """
        lst = [self]
        for child in self.children:
            lst += child.preorder()
        return lst

    def subtree(self, kind, name):
        def get_subtree_root(root, kind, name):
            if root.kind == kind and root.name == name:
                return root

            for child in root.children:
                child_result = get_subtree_root(child, kind, name)
                if child_result is not None:
                    return child_result

        subtree_root = get_subtree_root(self, kind, name)
        if subtree_root is None:
            raise ASTSearchException("Cannot find specified kind and identifier name")

        return subtree_root

    @classmethod
    def create(cls, path, **kwargs):
        """
        Create an AST of the program pointed by the path. This class method is
        meant to be overrided in the child class

        Parameters:
            path: The path to the program
            **kwargs: Additional resources needed to create an AST
        """
        raise NotImplementedError("create() method not implemented!")
