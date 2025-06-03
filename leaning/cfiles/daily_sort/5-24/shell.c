#include <stddef.h>

void shell_sort(int *a, size_t n){
    if(n < 2) return;
    for(size_t gap = n/2; gap > 0; gap /= 2){
        for(size_t i = gap; i < n; i++){
            size_t j = i;
            int key = a[i];
            while(j >= gap && a[j - gap] > key){
                a[j] = a[j - gap];
                j -= gap;
            }
            a[j] = key;
        }
    }
}