import math

def sum_of_divisors(num):
    sum = 0
    for i in range(1,num):
        if num%i==0:
            sum+=i
    return sum

def amicable_pairs(length):
    pairs = []
    num = 2
    while len(pairs) < length:
        sum1 = sum_of_divisors(num)
        if sum1 > num:
            sum2 = sum_of_divisors(sum1)
            if sum2 == num:
                pairs.append((num, sum1))
        num+=1

pairs = amicable_pairs(1)
for pair in pairs:
    print(pair)

