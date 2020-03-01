from datetime import datetime as dt
from datetime import timedelta as td
import ctypes as C
import subprocess


def time(f):
    def wrapper(*args, **kwargs):
        start = dt.now()
        ret = f(*args, **kwargs)
        return (ret, dt.now()-start)
    return wrapper



if __name__ == "__main__":
    values = 100000000
    runs = 100

    print('C-Style :')
    array_c = (C.c_int32 * values)(*range(values))
    print(f'array_c address (from python) : {hex(C.addressof(array_c))}')
    print(f'clib build output : "{subprocess.check_output("gcc -shared -o hello.c.so hello.c".split(" ")).decode("utf-8")}"')
    clib = C.cdll.LoadLibrary("hello.c.so")
    ctimes = []
    for run in range(runs):
        cret, ctime = time(clib.test2)(array_c, len(array_c))
        ctimes.append(ctime)
    ctime = sum(ctimes, td(0)) / len(ctimes)
    print(array_c[:5])
    print(array_c[-5:])

    print('GO-Style :')
    array_go = (C.c_int32 * values)(*range(values))
    print(f'array_go address (from python) : {hex(C.addressof(array_go))}')
    print(f'golib build output : "{subprocess.check_output("go build -o hello.go.so -buildmode=c-shared hello.go".split(" ")).decode("utf-8")}"')
    golib = C.cdll.LoadLibrary("hello.go.so")
    gotimes = []
    for run in range(runs):
        goret, gotime = time(golib.test2)(array_go, len(array_go))
        gotimes.append(gotime)
    gotime = sum(gotimes, td(0)) / len(gotimes)
    print(array_go[:5])
    print(array_go[-5:])

    print()
    print(f'C-Style took (average over {runs} runs) : {ctime}')
    print(f'GO-Style took (average over {runs} runs, using goroutines) : {gotime}')

