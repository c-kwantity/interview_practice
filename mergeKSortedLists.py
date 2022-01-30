from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if (len(lists) == 0):
            return None
        elif (len(lists) == 1):
            return lists[0]
        elif (len(lists) == 2):
            return self.merge(lists[0], lists[1])
        else:
            halfLen = len(lists) // 2
            return self.merge(self.mergeKLists(lists[:halfLen]), self.mergeKLists(lists[halfLen:]))

    #given two sorted ListNodes merges the two together
    def merge(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if (list1 == None):
            return list2
        elif (list2 == None):
            return list1
        else:
            curL1 = list1
            curL2 = list2
            mergedList = None
            curNode = None
            curLowNode = None
            # go through both arrays while still have values
            while (curL1 != None and curL2 != None):
                if (curL1.val <= curL2.val):
                    curLowNode = curL1
                    curL1 = curL1.next
                else:
                    curLowNode = curL2
                    curL2 = curL2.next
                if (mergedList == None):
                    # capture start of list to return later
                    curNode = curLowNode
                    mergedList = curNode
                else:
                    # assign value in node
                    # NOTE: this will destroy linked list inputs
                    curNode.next = curLowNode
                    curNode = curLowNode
            # check if still have values
            if (curL1 != None):
                curNode.next = curL1
            if (curL2 != None):
                curNode.next = curL2
            return mergedList

    # def printer(self, list: Optional[ListNode], prefix = "") -> None:
    #     if (list == None):
    #         print(list)
    #     else:
    #         ptr = list
    #         print(prefix, end = "")
    #         while (ptr != None):
    #             print(ptr.val, end = " ")
    #             ptr = ptr.next
    #         print("\n")


solver = Solution()
node10 = ListNode(5)
node11 = ListNode(4, node10)
node12 = ListNode(1, node11)
node20 = ListNode(4)
node21 = ListNode(3, node20)
node22 = ListNode(1, node21)
node30 = ListNode(6)
node31 = ListNode(2, node30)
res = solver.mergeKLists([node12, node22, node31])
solver.printer(res)
