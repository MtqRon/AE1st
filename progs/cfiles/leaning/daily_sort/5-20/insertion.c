#include <stddef.h>

void insertion_sort(int *a; size_t n){
    for(size_t i = 0; i < n; i++){
        //i-1までは整列済みになっている．a[i]をa[0]-a[i-1]までの中の適切な位置に挿入するのが挿入ソート．
        //挿入する要素をkeyとする．
        int key = a[i];

        //iはインクリメントとかしたくないのでjを用意する．
        size_t j = i;

        //a[j - 1] > keyならまだ適切な位置ではない（keyのほうが小さいのに右側にある）
        while(j >= 1 && a[j - 1] > key){
            //a[j]はkeyに保存してあるのでこれでOK．要素を右にずらしていく．
            a[j] = a[j - 1];
            //整列済みの部分を後ろから前に向かって走査
            j--;
        }
        //a[j]が適切な位置となっているので（whileによる先判定なのでa[j]が適切な位置）そこにkeyを挿入する．
        a[j] = key;
    }

}