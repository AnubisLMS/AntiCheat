from mayat.AST import AST


class FlattenedTree:
    def __init__(self, ast):
        self.flattened = ast.preorder()
        self.flattened.sort(key=lambda node: node.weight, reverse=True)
        self.removed = set()

    def nodes(self):
        self.removed = set()

        for node in self.flattened:
            if node in self.removed:
                continue
            yield node

    def remove(self, node):
        self.removed.update(node.preorder())

    def __len__(self):
        return len(self.flattened)


class Checker:
    def __init__(self, path1, path2, ast1, ast2, threshold=5):
        self.path1 = path1
        self.path2 = path2
        self.flattened1 = FlattenedTree(ast1)
        self.flattened2 = FlattenedTree(ast2)

        self.threshold = threshold
        self.similarity = 0
        self.overlapping_ranges = []

    def check_v2(self):
        flattened1_dict = {}
        for node in self.flattened1.nodes():
            key = (node.weight, node.fingerprint)
            if key in flattened1_dict:
                flattened1_dict[key].append(node)
            else:
                flattened1_dict[key] = [node]

        for key in flattened1_dict:
            flattened1_dict[key] = iter(flattened1_dict[key])

        overlaps = []
        for node in self.flattened2.nodes():
            if node.weight < self.threshold:
                continue

            key = (node.weight, node.fingerprint)
            if key in flattened1_dict:
                flattened1_node = next(flattened1_dict[key], None)
                if flattened1_node is not None:
                    overlaps.append((flattened1_node, node))

                    self.flattened2.remove(node)
                    for sub_node in flattened1_node.preorder():
                        sub_key = (sub_node.weight, sub_node.fingerprint)
                        next(flattened1_dict[sub_key], None) # Purge the nodes in the sub tree

        num_of_same_nodes = 0
        for (node1, node2) in overlaps:
            num_of_same_nodes += node1.weight
            self.overlapping_ranges.append({
                "A_start_pos":  node1.start_pos,
                "A_end_pos":    node1.end_pos,
                "B_start_pos":  node2.start_pos,
                "B_end_pos":    node2.end_pos,
            })

        self.similarity = num_of_same_nodes / min(len(self.flattened1), len(self.flattened2))

    # The optimized version
    def check(self):
        """
        Check the similarities of two ASTs
        """
        arrLL1_dict = {(node.weight, node.fingerprint):node for node in self.arrLL1}

        # The overlapped (node.weight, node.fingerprint) along with the ranges it occur
        overlaps_in_arrLL2 = {}
        for node in self.arrLL2:
            key = (node.weight, node.fingerprint)
            if key in arrLL1_dict:
                if key not in overlaps_in_arrLL2:
                    overlaps_in_arrLL2[key] = [[node], 1]
                else:
                    overlaps_in_arrLL2[key][0].append(node)
                    overlaps_in_arrLL2[key][1] += 1

        for key in overlaps_in_arrLL2:
            overlaps_in_arrLL2[key][0] = iter(overlaps_in_arrLL2[key][0])

        num_of_same_nodes = 0

        for node in self.arrLL1:
            key = (node.weight, node.fingerprint)
            if node.weight < self.threshold:
                continue

            if key in overlaps_in_arrLL2:
                if overlaps_in_arrLL2[key][1] == 0:
                    continue
                overlaps_in_arrLL2[key][1] -= 1

            if (
                node.parent is not None
                and (node.parent.weight, node.parent.fingerprint) in overlaps_in_arrLL2
            ):
                continue

            if key in overlaps_in_arrLL2:
                num_of_same_nodes += node.weight
                node_in_arrLL2 = next(overlaps_in_arrLL2[key][0])
                self.overlapping_ranges.append({
                    "A_start_pos": node.start_pos,
                    "A_end_pos": node.end_pos,
                    "B_start_pos": node_in_arrLL2.start_pos,
                    "B_end_pos": node_in_arrLL2.end_pos
                })

        self.similarity = num_of_same_nodes / min(len(self.arrLL1), len(self.arrLL2))
