#include <stddef.c>

void merge_sort_rec(int *a, int *tmp, size_t l, size_t r){
    
}

void merge_sort(int *a, size_t n){
    //メモリの確保（受けるのは確保したメモリのポインター）
    int *tmp = malloc(n * sizeof *tmp);
    //tmp(確保したメモリのポインタ)がNULLだったらリターンする．
    if(!tmp) return;
    //a:ソートする配列の先頭ポインタ
    //tmp:確保したメモリの先頭ポインタ
    //0:
    //n:配列の要素数
    merge_sort_rec(a,tmp,0,n);
    //メモリの開放は先頭ポインタを使用する
    free(tmp);
}