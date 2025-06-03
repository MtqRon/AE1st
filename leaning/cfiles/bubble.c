#include <stddef.h>
#include <stdbool.h>

void bubble_sort(int *a, size_t n){
    //そのままだと，小さい要素が適切な位置に来ても配列の走査が続くので，交換されなかったタイミングでブレイクする．
    bool swapped;
    //n<2の時は何もしない
    if (n < 2) return;
    
    //整列する（前から後ろに向かって1つずつ整列済みとなっていく）
    for(size_t i = 0; i < n-1; i++){
        swapped = false;
        //交換する（後ろから前に向かって，小さいものを移動させていく）
        for(size_t j = n-1; j > i; j--){
            if(a[j-1] > a[j]){
                int tmp = a[j-1];
                a[j-1] = a[j];
                a[j] = tmp;
                swapped = true;
            }
        }
        if(!swapped) break;
    }
}