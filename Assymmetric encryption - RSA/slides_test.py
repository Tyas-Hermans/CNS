import math
def modular_Expantion(b,a,n):
    f = 1
    for i in range(len(b)):
        f = (f*f)%n
        print(b[i])
        if b[i] == '1':
            f = (f*a)%n
    print(f)
def key_generation(p,q):
    n = p*q
    xn = (p-1)*(q-1)
    e = 1
    for i in range(xn,0,-1):
        if math.gcd(i,xn)==1:
            e = i
            break
    r = [xn,e]
    w = [0,1]
    while r[-1] != 1:
        q = r[-2] // r[-1]
        r.append(r[-2] % r[-1])
        w.append(w[-2] - (q * w[-1]))
    d = w[-1] % xn

    print(n,xn,e,d)



if "__main__" == __name__:
    modular_Expantion(bin(21),7,127)
    key_generation(7,11)

