import copy
import unittest
from typing import Any


# Author : William A. Morris
# Purpose : Custom python datatypes to use
class SinglyLinkedNode:
    def __init__(self, entry=None, next=None) -> None:
        self.entry = entry
        self.next = next

    def points_blank(self) -> bool:
        return self.next is None


class LinkedStructure:
    # INIT
    def __init__(self) -> None:  # init an empty List, with empty pointers at the head
        self._head: SinglyLinkedNode or None = None

    def __len__(self) -> int:  # define a method to fetch the len() value
        return self.length()

    # PUBLIC METHODS
    def is_empty(self) -> bool:  # if the head of the list is None, the List will be EMPTY
        return self._head is None

    def length(self) -> int:  # method to find length of list
        if self.is_empty():
            return 0  # if the list is empty, the length will be zero
        i = 0  # define an index tracker
        jumper = self._head  # and deref the first pointer on the list

        while not (jumper.points_blank() or jumper is None):  # while the node is not pointing to None,
            jumper = jumper.next  # jump to that node
            i += 1  # and increase the index tracker by 1
        return i + 1  # when the loop terminates at an empty pointer, return the (index + 1) as the final length

    def clear(self):  # clear the list by reinitializing the memory
        self.__init__()

    def copy(self):
        return copy.deepcopy(self)

    # PRIVATE METHODS
    def _node_at(self, index, offset=0) -> SinglyLinkedNode:  # return the node at a specified index, +/- permitted
        if index == 0:  # return the head if index is 0
            return self._head
        elif index < 0:  # adjust the index in wraparound fashion index(-len()) == index(0)
            adjustedIndex = (index + self.length()) + offset
        else:
            adjustedIndex = index + offset

        if adjustedIndex >= self.length() or adjustedIndex < 0:  # check if the adjusted index actually points to
            # anything
            raise IndexError(f"No data at index: {index}, out of bounds.")

        jumper = self._head  # define a jumper at the head of the list
        for _ in range(adjustedIndex):  # skip ahead until arrived at correct index
            jumper = jumper.next
        return jumper  # return the specified node

    def _insert_node_at_head(self, node: SinglyLinkedNode):  # insert a node at the head of the list
        node.next = self._head  # point the node to the old head
        self._head = node  # reassign the head to the node

    def _insert_node_at_tail(self, insertNode: SinglyLinkedNode):  # insert a node at the end of the list
        if not self.is_empty():  # if the list is not empty
            tail = self._node_at(-1)  # get the node at the end of the list
            tail.next = insertNode  # point it to the new node
            tail = insertNode  # and move the tail to the new node
        else:  # if the list is currently empty
            self._head = insertNode  # assign the node at the head.

    def _insert_node_at_index(self, insertNode: SinglyLinkedNode, index):  # insert a node at a specified index
        jumper: SinglyLinkedNode = self._head  # deref the node at the head of the list
        if self.is_empty() or index == 0 or index == (
                0 - self.length()):  # if the list is currently empty, or the user specified a starting index
            self._insert_node_at_head(insertNode)  # the new node will be inserted at the front of the list
            return

        if index is None:  # if the user did not specify an index, insert the node at the end of the list.
            self._insert_node_at_tail(insertNode)
        else:
            jumper = self._node_at(index,
                                   -1)  # if the index is in-bound and defined, jump to it's current corresponding
            # node in the list
            insertNode.next = jumper.next  # point the new node to the old node at index
            jumper.next = insertNode  # insert the new node at the specified index, thus moving all other entries down 1

    def _pop_node_at_head(self) -> SinglyLinkedNode:  # delete the node at the head of the list
        if self.length() > 1:  # if the list has more than 1 entries, delete the head and reassign it to the next
            # node and return the deleted node
            copyOfNode = self._head
            self._head = self._head.next
            return copyOfNode
        elif self.length() == 1:  # if the list has 1 entry, clear the list and return the deleted node
            copyOfNode = self._node_at(0)
            self.__init__()
            return copyOfNode
        else:  # if the list has no entries throw an error
            raise RuntimeError("Cannot perform a remove operation on an empty list!")

    def _pop_node_at_tail(self) -> SinglyLinkedNode:  # delete the node at the end of the list
        if self.length() > 1:  # if the list has more than one entry, get the entry before the tail index(-2) and
            # point it to None
            copyOfNode = self._node_at(-1)
            newTail = self._node_at(-2)
            newTail.next = None
            return copyOfNode  # return the deleted node
        elif self.length() == 1:  # if the list has one entry, clear it and return a copy of the deleted node
            copyOfNode = self._node_at(0)
            self.__init__()
            return copyOfNode
        else:  # if the list has no entries throw an error
            raise RuntimeError("Cannot perform a remove operation on an empty list!")

    def _pop_node_at_index(self, index: int) -> SinglyLinkedNode:  # delete a node at a specified index
        if self.is_empty():  # if the list has no entries throw an error
            raise RuntimeError("Cannot perform a remove operation on an empty list!")
        elif self.length() == 1:  # if the list has one entry, clear it and return the deleted node
            copyOfNode = self._node_at(0)
            self.__init__()
            return copyOfNode
        if index == 0 or index == (
                0 - self.length()):  # if the user is trying to delete the head, call that function and return the copy
            copyOfNode = self._node_at(0)
            self._pop_node_at_head()
            return copyOfNode
        elif index is None:  # if the user doesn't specify an index, pop the node at the tail and return a copy
            copyOfNode = self._node_at(-1)
            self._pop_node_at_tail()
            return copyOfNode
        else:
            copyOfNode = self._node_at(index)
            delNode = self._node_at(index, -1)  # get the node before the node to be deleted
            if copyOfNode.next is not None:  # if the index being deleted doesn't point to None
                delNode.next = self._node_at(index, 1)  # reassign its pointer
                return copyOfNode  # return the copy
            else:
                delNode.next = None  # if the index being deleted was at the tail
                return copyOfNode


class LinkedList(LinkedStructure):
    # INIT
    def __init__(self) -> None:  # init an empty List, with empty pointers at the head
        super().__init__()
        # self._head: SinglyLinkedNode or None = None

    def at(self, index) -> Any:  # get data from a specified index
        node = self._node_at(index)  # get node at index
        return node.entry if node is not None else None  # deref the node, if present

    def push(self, entry):  # push data to the end of the list
        insertNode = SinglyLinkedNode(entry)  # define a node
        self._insert_node_at_tail(insertNode)  # insert it at the tail

    def insert(self, entry,
               index: int = None) -> None:  # insert on the list, optionally specifying an index to insert at
        insertNode = SinglyLinkedNode(entry)  # init a node to insert at the specified index
        self._insert_node_at_index(insertNode, index)  # insert

    def pop(self) -> Any:  # pop a node off the end of the list
        return self._pop_node_at_tail().entry  # return its data

    def replace(self, entry, index: int) -> Any:  # replace data at a given node
        if self.is_empty() or index is None:  # throw an error if the list is empty, or the user did not specify an
            # index to replace
            raise RuntimeError("Cannot replace data on an empty list")

        jumper = self._node_at(
            index)  # if the index is in-bound and defined, jump to it's current corresponding node in the list
        returnCopy = jumper.entry  # make a copy of its data
        jumper.entry = entry  # replace the data within the node with the new entry
        return returnCopy  # return the copy

    def delete(self,
               index: int = None) -> Any:  # delete a node at a specified index, or the end of the list if unspecified
        return self._pop_node_at_index(index).entry  # return the deleted data


class LinkedStack(LinkedStructure):
    # INIT
    def __init__(self) -> None:  # init an empty List, with empty pointers at the head
        super().__init__()
        # self._head: SinglyLinkedNode or None = None

    def push(self, entry):  # push data to the end of the list
        insertNode = SinglyLinkedNode(entry)  # define a node
        self._insert_node_at_tail(insertNode)  # insert it at the tail

    def pop(self) -> Any:  # pop a node off the end of the list
        return self._pop_node_at_tail().entry  # return its data

    def peek_top(self) -> Any:
        return self._node_at(-1).entry if len(self) > 0 else None

    def peek_bottom(self) -> Any:
        return self._node_at(0).entry if len(self) > 0 else None


class LinkedQueue(LinkedStructure):
    # INIT
    def __init__(self) -> None:  # init an empty List, with empty pointers at the head
        super().__init__()

    def enqueue(self, entry):  # push data to the end of the list
        insertNode = SinglyLinkedNode(entry)  # define a node
        self._insert_node_at_tail(insertNode)  # insert it at the tail

    def dequeue(self) -> Any:
        return self._pop_node_at_head().entry

    def peek_back(self) -> Any:
        return self._node_at(-1).entry

    def peek_front(self) -> Any:
        return self._node_at(0).entry


class LinkedListUnitTest(unittest.TestCase):
    """
    def testStart(testName: str):
    print(f'===== Unit Test: {testName} =====')

    def testFinished(testName: str, success: bool):
        print(
            f'===== {testName} PASSED =====\n'
            if success else
            f'!=!=!=!=!=!=!=!=!=!=! {testName} FAILED !=!=!=!=!=!=!=!=!=!=!\n')

    def __init__(self) -> None:
        self.list: LinkedList = LinkedList()

    def runListTests(self):
        try:
            self.nodeTest()
            self.listIsEmptyTest()
            self.pushAtFront("0:hello")
            self.insertToFront("0: new hello")
            self.replaceTest("1:hello", 1)
            self.popOffListTest()
            self.deleteFromFrontTest()
            print("===== LINKED LIST UNIT TESTS PASSED WITH NO EXCEPTIONS =====")
        except Exception as e:
            print(f"Exception thrown while running Unit Tests: \n{e}")
    """

    def test_init_node(self):
        # testStart("Node Init Test")
        node = SinglyLinkedNode("hello")
        node.next = SinglyLinkedNode("world")

        self.assertEqual("hello", node.entry)
        self.assertFalse(node.points_blank())

    def test_init_list_empty(self):
        # testStart("List Should Be Empty Test")
        testList = LinkedList()
        self.assertTrue(testList.is_empty())

    def test_push_at_front(self):
        # testStart('Push to Empty List Test')
        testList = LinkedList()
        testList.push("0:hello")
        self.assertEqual("0:hello", testList.at(0))
        self.assertEqual("0:hello", testList.at(-1))
        self.assertEqual(1, testList.length())

    def test_insert_at_front(self):
        testList = LinkedList()
        testList.push("0:hello")
        testList.push("1:world")
        testList.push("2:bye")

        self.assertEqual(3, len(testList))

        testList.insert("0N:new hello", 0)

        self.assertEqual(4, len(testList))
        self.assertEqual("0N:new hello", testList.at(0))

    def test_replace(self):
        testList = LinkedList()
        testList.push("0:hello")
        testList.push("1:world")
        testList.push("2:bye")
        testList.push("3:b")
        testList.push("4:idk")

        testList.replace("2N:better goodbye", 2)
        testList.replace("0N:better hello", 0)
        testList.replace("4N:i do know", -1)

        self.assertEqual("2N:better goodbye", testList.at(-3))
        self.assertEqual("0N:better hello", testList.at(0 - len(testList)))
        self.assertEqual("4N:i do know", testList.at(4))

    def test_pop(self):
        testList = LinkedList()
        testList.push("0:hello")
        testList.push("1:world")
        testList.push("2:bye")
        testList.push("3:b")
        testList.push("4:idk")

        copyOfTestList = testList.copy()
        for i in range(4, -1, -1):
            self.assertEqual(testList.pop(), copyOfTestList.at(i))
        self.assertEqual(0, len(testList))

    def test_delete_from_list(self):
        testList = LinkedList()
        testList.push("0:hello")
        testList.push("1:world")
        testList.push("2:bye")
        testList.push("3:b")
        testList.push("4:idk")

        self.assertEqual("3:b", testList.delete(3))
        self.assertEqual(4, len(testList))

        self.assertEqual("0:hello", testList.delete(0))
        self.assertEqual(3, len(testList))

        self.assertEqual("4:idk", testList.delete(-1))
        self.assertEqual(2, len(testList))


class LinkedQueueUnitTest(unittest.TestCase):
    def test_all(self):
        myLinkedQueue = LinkedQueue()
        myLinkedQueue.enqueue("hello")
        myLinkedQueue.enqueue("world")
        print(myLinkedQueue.dequeue())
        print(myLinkedQueue.dequeue())
        print(myLinkedQueue.is_empty())
        self.assertEqual(0, len(myLinkedQueue))


if __name__ == '__main__':
    listUnits = LinkedListUnitTest()
    listUnits.debug()
