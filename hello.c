#include <stdio.h>


int test1(int x, int y) {
    return x + y;
}

void test2(int* array, int len) {
    // printf("array address (from c) : %p\n", array);
    for (int i=0; i<len; ++i) {
        array[i] = array[i] * array[i];
    }
}