#include <stddef.h>
#include <stdlib.h>

//再起関数で範囲[l,r]をソート
void merge_sort_rec(int *a, int *tmp, size_t l, size_t r){
    //ネストの最後
    if (r - l < 2) return;

    //範囲[l,r]の真ん中をmとして定める（r-lが真ん中範囲の真ん中．lだけずらすことでa[]に対応させる．
    size_t m = l + (r - l) / 2;

    //再帰関数．真ん中で分けた配列の前と後ろをそれぞれ範囲としてソートする
    merge_sort_rec(a, tmp, l, m);
    merge_sort_rec(a, tmp, m, r);

    //変数の初期化
    size_t i = l, j = m, k = l;

    //二つの範囲を小さい順にtmpに入れていく．[l→m][m→r]ここではlが頭，rが最後．
    while (i < m && j < r) {
        //a[i]が小さいならtmp[k]にa[i]を代入してi,kをインクリメントする
        tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    }
    //どちらかが先に中身がなくなったらもう片方の残りを代入する．
    while (i < m) tmp[k++] = a[i++];
    while (j < r) tmp[k++] = a[j++];

    //最後にaにソート済みとなったtmpをコピーする
    for (k = l; k < r; k++) a[k] = tmp[k];
}

void merge_sort(int *a, size_t n){
    //メモリの確保（受けるのは確保したメモリのポインター）
    int *tmp = malloc(n * sizeof *tmp);

    //tmp(確保したメモリのポインタ)がNULLだったらリターンする．
    if(!tmp) return;

    /*
    a:ソートする配列の先頭ポインタ
    tmp:小さい順に入れる仮の配列．merge_sort_recでは最終的にaにコピーされる．
    0,n:整列する範囲
    */
    merge_sort_rec(a,tmp,0,n);

    //メモリの開放は先頭ポインタを使用する
    free(tmp);
}