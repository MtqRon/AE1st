#include <stddef.h>
#define SWAP(x,y) do{ int _t = (x); (x) = (y); (y) = _t;}while(0)

static void heapify(int *a,size_t from, size_t to);

void build_max_heap(int *a, size_t n){
    for(size_t i = n/2; i > 0; i--){
        heapify(a, i - 1, n - 1);
    }
}

void heapify(int *a, size_t from, size_t to){
    //iは現在注目している節，jは注目している一つ下の段
    int i,j;

    //valは沈める要素fromが注目する半順序木の頭
    int val = a[from];

    //根（頭）からスタートする．
    i = from;

    //iの左の子がto(最後の葉)よりも大きい
    while(2 * i + 1 <= to){
        //節iの左の子をjとする
        j = i * 2 + 1;

        //節iの子の内，大きいほうを節jとする
        if(j + 1 <= to && a[j] < a[j + 1]) j++;

        //もし親が子より大きいという関係を満たすなら，これ以上沈める必要はない
        if(val >= a[j]) break;

        //親が子より小さかったので，子を一つ上に上げる
        a[i] = a[j];

        //注目する節を一つ下の段にする
        i = j;
    }
    //あるべき場所のスペースをあけられたので，代入する
    a[i] = val;
}

void heap_sort(int *a, size_t n){
    if(n < 2) return;

    build_max_heap(a, n);

    for(size_t end = n; end > 1; end--){
        SWAP(a[0],a[end - 1]);
        //end - 1にはヒープの最大の要素が移動されているのでend - 2に狭める
        heapify(a, 0, end - 2);
    }
}