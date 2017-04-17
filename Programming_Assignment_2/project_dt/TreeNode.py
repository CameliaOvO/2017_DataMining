class TreeNode:
    value = ""
    childs = []

    def __init__(self,val, child):
        self.value = val
        if (isinstance(child,dict)):
            self.childs = child.keys()