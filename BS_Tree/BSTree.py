from BSTNode import BSTNode

# bugs to vladimir dot kulyukin at usu dot edu

class BSTree:
    def __init__(self, root=None):
        self.__root = root
        if root == None:
            self.__numNodes = 0
        else:
            self.__numNodes = 1

    def getRoot(self):
        return self.__root

    def getNumNodes(self):
        return self.__numNodes

    def isEmpty(self):
        return self.__root == None

    # implement this method
    def hasKey(self, key):
        curr_node = self.__root
        while curr_node != None:
            if key < curr_node.getKey():
                curr_node = curr_node.getLeftChild()
            elif key > curr_node.getKey():
                curr_node = curr_node.getRightChild()
            elif key == curr_node.getKey():
                return True
            else:
                raise Exception('insertKey: ' + str(key))
        return False

    def insertKey(self, key):
        if self.isEmpty():
            self.__root = BSTNode(key=key)
            self.__numNodes += 1
            return True
        elif self.hasKey(key):
            return False
        else:
            currNode = self.__root
            parNode = None
            while currNode != None:
                parNode = currNode
                if key < currNode.getKey():
                    currNode = currNode.getLeftChild()
                elif key > currNode.getKey():
                    currNode = currNode.getRightChild()
                else:
                    raise Exception('insertKey: ' + str(key))
            if parNode != None:
                if key < parNode.getKey():
                    parNode.setLeftChild(BSTNode(key=key))
                    self.__numNodes += 1
                    return True
                elif key > parNode.getKey():
                    parNode.setRightChild(BSTNode(key=key))
                    self.__numNodes += 1
                    return True
                else:
                    raise Exception('insertKey: ' + str(key))
            else:
                raise Exception('insertKey: parNode=None; key= ' + str(key))

    # implement this method
    def __heightOf(self, node):
        if node == None:
            return 0
        else:
            return 1 + max(self.__heightOf(node.getLeftChild()), self.__heightOf(node.getRightChild()))

    def heightOf(self):
        return self.__heightOf(self.__root)-1

    # Helper method for isBalanced
    def __is_balanced(self, node):
        if node == None:
            return True
        else:
            difference = abs((self.__heightOf(node.getLeftChild()) - self.__heightOf(node.getRightChild())))
            if difference > 1:
                return False
            else:
                return self.__is_balanced(node.getLeftChild()) and self.__is_balanced(node.getRightChild())

    # implement this method
    def isBalanced(self):
        return self.__is_balanced(self.__root)

    def __displayInOrder(self, currnode):
        if currnode == None:
            print('NULL')
        else:
            self.__displayInOrder(currnode.getLeftChild())
            print(str(currnode))
            self.__displayInOrder(currnode.getRightChild())

    def displayInOrder(self):
        self.__displayInOrder(self.__root)

    # implement this method
    def isList(self):
        if self.__numNodes == self.heightOf()+1:
            return True
        else:
            return False
