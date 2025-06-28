#include <stddef.h>

static void swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

static void heapify(int *a, size_t from, size_t to)

static void init_heap(int *a, size_t n){
    for(size_t i = n/2; i > 0; i--){
        heapify(a, i - 1, n - 1);
    }
}


static void heapify(int *a, size_t from, size_t to){
    int key = a[from];
    i = from;

    while(i * 2 + 1 <= to){
        size_t j = i * 2 + 1;
        if(a[j] < a[j + 1] && j + 1 <= to) j++;

        if(a[j] < key){
            break;
        }else{
            a[i] = a[j]; 
        }
        i = j
    }
    a[i] = key;
}

void heap_sort(int *a, size_t n){
    if(n < 2) return;

    init_heap(a, n);

    for(size_t i = n - 1; i > 0; i--){
        swap(&a[0], &a[i]);
        heapify(a, 0, i - 1);
    }
}