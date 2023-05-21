import random

def is_prime(x):
    for i in range(2,x):
        if(x%i==0):
            return 0   #Returns 0 if composite
    return 1

def next_prime(x):
    x += 1
    while not(is_prime(x)):
        x += 1
    return x

def generate_a(x,y,a):
    while not (x*a)%y==1:
        a+=1
    return a

def four_tuple(k):
    num1 = next_prime(random.randint(10**(k-1), 10**k))
    num2 = next_prime(num1 + random.randint(10**(k-2), 10**(k-1)))
    a = generate_a(num1, num2, 1)
    b = (1-(a*num1))/num2
    while not b == int(b):
        a = generate_a(num1, num2, a)
        b = (1-(a*num1))/num2
    return (num1, num2, a, int(b))

k = int(input("Enter a positive integer: "))
result = four_tuple(k)
print(result)
        




