max = 100

def checkprime(ret, i, arg):
    i = 2
    while i < arg:
        if arg % i == 0:
            ret = 0
            i = arg
        i = i + 1


def primes(max):
    i = 0
    arg = 2
    while arg < max:
        ret = 1
        checkprime(ret, i, arg)
        if ret == 1:
            print(arg)
        arg = arg + 1

primes(max)

