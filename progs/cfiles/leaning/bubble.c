#include <stddef.h>

void bubble_sort(int *a, size_t n){
    int swapped = 0;
    for(size_t i = 0; i + 1 < n; ++i){
        int swapped = 0;
        for(size_t j = 0; j + 1 < n - i; ++j){
            if(a[j] > a[j + 1]){
                int t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
                swapped = 1;
            }
        }
        if (!swapped) break;
    }
}