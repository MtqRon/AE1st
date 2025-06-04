#include <stddef.h>

static void heap_swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

static void heapify(int *a, size_t from, size_t to);

static void init_heap(int *a, size_t n){
    for(size_t i = n / 2; i > 0; i--){
        heapify(a, i - 1, n - 1);
    }
}

static void heapify(int *a, size_t from, size_t to){
    size_t i = from;
    int key = a[from];
    while(i * 2 + 1 <= to){
        size_t j = i * 2 + 1;
        if(j + 1 <= to && a[j] < a[j + 1]) j++;
        if(a[j] > key){
            a[i] = a[j];
        }else{
            break;
        }
        i = j;
    }
    a[i] = key;
}

void heap_sort(int *a, size_t n){
    if(n < 2) return;

    init_heap(a, n);

    for(size_t i = n; i > 1; i--){
        heap_swap(&a[0], &a[i - 1]);
        heapify(a, 0, i - 2);
    }
}