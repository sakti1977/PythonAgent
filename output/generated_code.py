```python
class TreeNode:
    """Represents a node in a binary tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def find_lca(root, p, q):
    """
    Find the Lowest Common Ancestor (LCA) of two nodes in a binary search tree.
    
    The LCA is the lowest node in the tree that has both p and q as descendants
    (where a node can be a descendant of itself).
    
    Args:
        root (TreeNode): The root node of the binary search tree
        p (TreeNode): First node to find
        q (TreeNode): Second node to find
    
    Returns:
        TreeNode: The lowest common ancestor node, or None if not found
    
    Time Complexity: O(h) where h is the height of the tree
    Space Complexity: O(1) for iterative approach
    """
    if not root or not p or not q:
        return None
    
    # Iterative approach for BST
    current = root
    
    while current:
        # If both p and q are smaller than current, go left
        if p.value < current.value and q.value < current.value:
            current = current.left
        # If both p and q are greater than current, go right
        elif p.value > current.value and q.value > current.value:
            current = current.right
        # Otherwise, current is the LCA (p and q are on different sides or one is current)
        else:
            return current
    
    return None


def find_lca_recursive(root, p, q):
    """
    Recursive approach to find LCA in a binary search tree.
    
    Args:
        root (TreeNode): The root node of the binary search tree
        p (TreeNode): First node to find
        q (TreeNode): Second node to find
    
    Returns:
        TreeNode: The lowest common ancestor node, or None if not found
    """
    if not root or not p or not q:
        return None
    
    # If both values are smaller than root, LCA is in left subtree
    if p.value < root.value and q.value < root.value:
        return find_lca_recursive(root.left, p, q)
    
    # If both values are greater than root, LCA is in right subtree
    if p.value > root.value and q.value > root.value:
        return find_lca_recursive(root.right, p, q)
    
    # Otherwise, root is the LCA
    return root


def find_lca_binary_tree(root, p, q):
    """
    Find LCA in a general binary tree (not necessarily BST).
    
    Args:
        root (TreeNode): The root node of the binary tree
        p (TreeNode): First node to find
        q (TreeNode): Second node to find
    
    Returns:
        TreeNode: The lowest common ancestor node, or None if not found
    """
    if not root:
        return None
    
    # If root matches either p or q, root is an ancestor
    if root == p or root == q:
        return root
    
    # Look for keys in left and right subtrees
    left_result = find_lca_binary_tree(root.left, p, q)
    right_result = find_lca_binary_tree(root.right, p, q)
    
    # If both left and right return non-null, root is LCA
    if left_result and right_result:
        return root
    
    # If only one subtree has a result, return that result
    return left_result if left_result else right_result


# Example usage and testing
if __name__ == "__main__":
    # Create a sample BST
    #       5
    #      / \
    #     3   7
    #    / \ / \
    #   2  4 6  8
    
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(7)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)