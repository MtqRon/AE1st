#include <stddef.h>
#define SWAP(x,y) do{int _t = (x); (x) = (y); (y) = _t;}while(0)

static void heapify(int *a, size_t from, size_t to);

void build_max_heap(int *a, size_t n){
    for(size_t i = n/2; i > 0; i--){
        heapify(a, i - 1, n - 1);
    }
}

void heapify(int *a, size_t from, size_t to){
    size_t i, j;
    i = from;
    int key = a[from];

    while(i * 2 + 1 <= to){
        j = i * 2 + 1;
        if(j + 1 <= to && a[j + 1] > a[j]) j++;
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

    build_max_heap(a, n);

    for(size_t i = n; i > 1; i--){
        SWAP(a[0], a[i - 1]);
        heapify(a, 0, i - 2);
    }
}