#include <stddef.h>

void insertion_sort(int *a, size_t n){
    if(n < 2) return;

    for(size_t i = 0; i < n; i++){
        size_t j = i;
        int key = a[i];
        for(; j > 0 && a[j - 1] > key; j--) a[j] = a[j - 1];
        a[j] = key;
    }
}