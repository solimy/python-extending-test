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
    values = 100_000_000
    runs = 100
    nb_threads = 10

    print('C-Style :')
    array_c = (C.c_int32 * values)(*range(values))
    print(f'array_c address (from python) : {hex(C.addressof(array_c))}')
    print(f'gcc output : "{subprocess.check_output("gcc -lpthread -shared -o hello.c.so hello.c".split(" ")).decode("utf-8")}"')
    clib = C.cdll.LoadLibrary("hello.c.so")
    ctimes = []
    for run in range(runs):
        cret, ctime = time(clib.test2)(array_c, len(array_c), nb_threads)
        ctimes.append(ctime)
    ctime = sum(ctimes, td(0)) / len(ctimes)
    print(f'array_c[:5] : {array_c[:5]}')
    print(f'array_c[-5:] : {array_c[-5:]}')

    print('GO-Style :')
    array_go = (C.c_int32 * values)(*range(values))
    print(f'array_go address (from python) : {hex(C.addressof(array_go))}')
    print(f'go build output : "{subprocess.check_output("go build -o hello.go.so -buildmode=c-shared hello.go".split(" ")).decode("utf-8")}"')
    golib = C.cdll.LoadLibrary("hello.go.so")
    gotimes = []
    for run in range(runs):
        goret, gotime = time(golib.test2)(array_go, len(array_go), nb_threads)
        gotimes.append(gotime)
    gotime = sum(gotimes, td(0)) / len(gotimes)
    print(f'array_go[:5] : {array_go[:5]}')
    print(f'array_go[-5:] : {array_go[-5:]}')

    print()
    print(f'C-Style took (average over {runs} runs, {nb_threads} threads) : {ctime}')
    print(f'GO-Style took (average over {runs} runs, {nb_threads} goroutines) : {gotime}')

