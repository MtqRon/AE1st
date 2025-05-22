#include <stddef.h>

void shell_sort(int *a, size_t n){
    if(n < 2) return;

    for(size_t gap = n/2, gap > 0, gap /= 2){
        for(size_t i = gap; i < n; i++){
            int tmp = a[i];
            size_t j = i;
            while(j >= gap && a[j - gap] > gap){
                a[j] = a[j - gap];
                j -= gap;
            }
            a[j] = tmp;
        }
    }
}