#include <stddef.h>

void insertion_sort(int *a, size_t n){
    if(n < 2) return;

    for(size_t i = 0; i < n; i++){
        int key = a[i];
        size_t j = i;
        for(; j > 0 && a[j - 1] > a[j]; j--) a[j] = a[j - 1];
        a[j] = key;
    }
}