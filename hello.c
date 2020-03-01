#include <stdio.h>
#include <pthread.h> 
#include <stdlib.h>


int test1(int x, int y) {
    return x + y;
}

typedef struct args_s {
    int* array;
    int length;
} args_t;

void* set_value(void* args) {
    int length = ((args_t*)args)->length;
    int* array = ((args_t*)args)->array;
    for (int i = 0; i < length; ++i) {
        array[i] = array[i] * array[i]; 
    }
    return NULL;
}

int min(int a, int b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

void test2(int* array, int length, int nb_threads) {
    // printf("array address (from c) : %p\n", array);
    int chunk_size = length / nb_threads;
    int end = 0;
    int thread = 0;
    pthread_t* threads = calloc(nb_threads + 1, sizeof(pthread_t));
    args_t* args = calloc(nb_threads + 1, sizeof(args_t));
    for (int start = 0; start < length; start += chunk_size) {
        thread = start / chunk_size;
        args[thread].length = min(start + chunk_size, length) - start;
        args[thread].array = &(array[start]);
        pthread_create(&(threads[thread]), 0, &set_value, &(args[thread]));
    }
    for (thread = 0; thread < nb_threads + 1; ++thread) {
        pthread_join(threads[thread], 0);
    }
    free(threads);
    free(args);
}