package main

import (
    "C"
    "unsafe"
    // "fmt"
    "runtime"
    "sync"
)


//export test1
func test1(a int, b int) int {
    return a + b
}


func set_value(slice []C.int, wg *sync.WaitGroup) {
    for i, value := range slice {
        slice[i] = value * value
    }
    wg.Done()
}

func min(a int, b int) int {
    if a < b {
        return a
    } else {
        return b
    }
}

//export test2
func test2(array *C.int, length int) {
    routines := 10
    chunk_size := length / routines
    runtime.GOMAXPROCS(routines)
    // fmt.Printf("array address (from go) : %p\n", array)
    slice := (*[1 << 30]C.int)(unsafe.Pointer(array))[:length:length]
    var wg sync.WaitGroup
    for start := 0; start < length; start += chunk_size {
        var end = min(start + chunk_size, length)
        // fmt.Printf("start=%d, end=%d, length=%d\n", start, end, length)
        wg.Add(1)
        go set_value(slice[start:end], &wg)
    }
    wg.Wait()
}

func main(){}