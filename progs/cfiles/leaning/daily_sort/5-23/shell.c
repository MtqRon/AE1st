#include <stddef.h>

void shell_sort(int *a, size_t n){
    if(n < 2) return;
    for(size_t gap = n/2; gap > 0; gap /= 2){
        //a[j-gap]でa[j]からgap分前の要素と比較するので，スタートをgap分ずらす
        for(size_t i = gap; i < n; i++){
            size_t j = i;//gapまでは整列済み
            int key = a[j];
            for(;j >= gap/*a[gap - 1]までは整列済みとするため*/ && a[j - gap] > key; j -= gap) a[j] = a[j - gap]; 
            a[j] = key;
        }

    }
}