#include <stddef.h>
void insertion_sort(int *a,size_t n){
    for(size_t i = 0; i < n; i++){
        //i-1までは整列済みとなっている
        size_t j = i;
        //挿入する要素
        int key = a[i];
        //jまで整列済みにする
        while(j >= 1 && a[j-1] > key){
            //keyの方がa[j-1]より小さいならkeyを挿入するためにa[j]にa[j-1]をずらす．
            a[j] = a[j-1];
            j--;
        }
        //適切な位置にスペースが開くので（a[j]），挿入する．
        a[j] = key;
    }
}