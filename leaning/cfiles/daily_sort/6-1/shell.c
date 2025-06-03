#include <stddef.h>

void shell_sort(int *a, size_t n){
    if(n < 2) return;

    for(size_t gap = n/2; gap > 0; gap /= 2){
        for(size_t i = gap; i < n; i++){
            int key = a[i];
            size_t j = i;
            for(; j >= gap && a[j - gap] > key; j -= gap) a[j] = a[j - gap];
            a[j] = key;
        }
    }
}