#include <stddef.h>

void shell_sort(int *a, size_t n){

    if(n < 2) return;

    //nを2で割った数飛び（n=10だったら5個飛び→2個飛び→1個飛び）で挿入ソートを行う．
    for(size_t gap = n/2; gap > 0; gap /= 2){
        //a[j-gap]でa[j]からgap分前の要素と比較して入れ替えるので，スタートをgap分ずらす．
        for(size_t i = gap; i < n; i++){
            int tmp = a[i];
            size_t j = i;
            //挿入ソートgap飛びの数列のうち，挿入に適切な位置を要素をずらして開け，そこに挿入する．
            while(j >= gap && a[j - gap] > tmp){
                a[j] = a[j - gap];
                a[j - gap] = tmp;
                j -= gap;
            }
        }
    }
}