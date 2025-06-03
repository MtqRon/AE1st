#include <stddef.h>

void insertion_sort(int *a, size_t n){
    if(n < 2) return;
    for(size_t i = 1/*0→1へ変更．不要な初回ループ*/; i < n; i++){
        size_t j = i;
        int key = a[i];
        while(j > 0 && a[j - 1] > key/*まちがえた．a[j]→keyへ変更*/){
            a[j] = a[j - 1];
            j--;
        }
        a[j] = key;
    }
}