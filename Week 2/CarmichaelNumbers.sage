
def gcd(x,y):
    if y==0:
        return x
    else:
        return gcd(y, x%y)
    
def is_prime(x):
    for i in range(2,x):
        if x%i==0:
            return 1  #Returns 1 is number is composite
    return 0

def carmichael_numbers(n):
    carmichael_num = []
    for i in range (2,n+1):
        k = 0
        if not is_prime(i):
            continue
        for j in range (2,i):
            if gcd(i,j)==1:
                if not (j**(i-1))%i==1:
                    k=1
                    break
        if k==0:
            carmichael_num.append(i)
    return carmichael_num

x = int(input("Enter a positive integer: "))
result = carmichael_numbers(x)
length = len(result)
if len==0:
    print("No Carmichael Numbers were found")
else:
    print(result)




