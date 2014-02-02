def euclid(a,b):
    if a>b:
        swap(a,b)
    r = a%b
    while r != 0:
        a = b
        b = r
        r = a%b
    return b

def commonEuclid(a,b):
    if b == 0:
        return (a,1,0)
    (d1,x1,y1)=commonEuclid(b, a%b)
    (d,x,y)=(d1,y1,x1-(a//b)*y1)
    return (d,x,y)

def inverseModM(a,m):
    (d,x,y) = commonEuclid(a,m)
    if d != 1:
        return -1
    else:
        return x

def solveLinearComparing(a,b,n):
    (d,x1,y1) = commonEuclid(a,n)
    if d%b != 0:
        return []
    x0 = (x1*(b/d))%n
    sols=[]
    k = n/d
    for i in range(0,d):
        sols += [x0 + (i*k)%n]
    return sols
        
def swap(a,b):
    a,b = b,a
    return

def solveLinearComparingSystem(values,modules):
    m = 1
    for i in modules:
        m*=i
    e = []
    n = len(values)
    for i in range(0,n):
        M = m/modules[i]
        s = inverseModM(M,modules[i])
        e += [s*M]
    x = 0
    for i in range(0,n):
        x += values[i]*e[i]
    return x       

