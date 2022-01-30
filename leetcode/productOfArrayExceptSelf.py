from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        productArr = [1] * len(nums)
        prefix = 1
        # build prefix array of accumulative n-1 product
        # skip first number since no numbers before that
        for i in range(1, len(nums)):
            prefix = prefix * nums[i-1]
            productArr[i] = prefix

        suffix = 1
        # skip last number since no numbers after that
        for i in range(len(nums) - 2, -1, -1):
            suffix = suffix * nums[i + 1]
            productArr[i] = suffix * productArr[i]

        return productArr

testArr = [1,2,3,4]
solver = Solution()
print(solver.productExceptSelf(testArr))