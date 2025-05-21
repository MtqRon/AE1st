#include <stddef.h>
#include <stdbool.h>

void bubble_sort(int *a, size_t n){
    //交換しなかったら適切な位置に来ているので，それを判定するフラグ
    bool swapped;

    //n<2のときは何もしない（要素が1個のため）
    if(n < 2) return;

    //前から順に整列済みとなっていく
    for(int i = 0; i < n; i++){
        swapped = false;
        //後ろから小さいものを前に持ってくる（交換を利用）
        for(int j = n - 1; j > i; j--){
            //a[j-1]がa[j]よりも大きいなら交換
            if(a[j] < a[j - 1]){
                int tmp = a[j];
                a[j] = a[j - 1];
                a[j - 1] = tmp;
                swapped = true;
            }
        }
        if(!swapped) break;
    }
}