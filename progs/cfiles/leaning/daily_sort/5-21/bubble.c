#include <stddef.h>
#include <stdbool.h>
#define SWAP(x,y,swapped) do{ int _t = (x); (x) = (y); (y) = _t; (swapped) = true;}while(0)

void bubble_sort(int *a, size_t n){
    if(n < 2) return;
    bool swapped;
    for(size_t i = 0; i < n; i++){
        swapped = false;
        for(size_t j = n - 1; j > 0; j--){
            if(a[j] < a[j - 1]) SWAP(a[j],a[j - 1],swapped);
        }
        if(!swapped) break;
    }
}