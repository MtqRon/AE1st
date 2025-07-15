#include <stddef.h>

void insertion_sort(int *a, size_t n){
    if(n < 2) return;

    //頭から末尾まで走査する
    for(size_t i = 0; i < n; i++){
    //keyを比較して整列ずみの場所の適切な場所に挿入する
        int key = a[i];
        size_t j = i;
        //jが範囲外アクセスしないかつ，一個前の要素がkeyより大きいならずらす
        for(; j > 0 && a[j - 1] > key; j--) a[j] = a[j - 1];
        a[j] = key;
    }
}