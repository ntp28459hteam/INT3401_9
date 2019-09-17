nums = [1,2,3,4,5,6]
# Create new list from 'nums'
oddNums = [x for x in nums if x % 2 == 1]
print oddNums
oddNumsPlusOne = [x+1 for x in nums if x % 2 ==1]
# Iterate our new generated list
for oddNum in oddNumsPlusOne:
    print oddNum
print oddNumsPlusOne
