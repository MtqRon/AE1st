#include <stddef.h>
#define SWAP(x,y) do { int _t=(x); (x)=(y); (y)=_t; } while(0)
//void build_max_heapでheapifyを呼び出しているが，宣言を行っていないので，宣言しないといけない．
static void heapify(int *a, size_t from, size_t to);

void build_max_heap(int *a, size_t n){
    //n/2からが子を持つ節となるので，そこからヒープ化スタート
    //右下から順々にヒープにしていく．
    for (size_t i = n/2; i > 0; i--) {
        heapify(a, i-1, n-1);
    }
}

//配列長を扱う変数（from,to）はsize_tとすることで整合性，可読性UP
void heapify(int *a, size_t from, size_t to){
    //i:注目している節，j:注目してる節の一つ下の段（子）
    int i,j;

    //a[i]を親とするとき，a[2i],a[2i+1]が子となる．
    //沈められる要素の値をvalにセットしておく
    //val:沈める要素
    int val = a[from];

    //根から始める．
    i = from;

    //a[to/2]が最後の親となる．i<=to/2というのは子が存在する限り実行されるということ．
    //↑だとtoが奇数の時に最後の親を見逃してしまう．2*i + 1 <= toが適切．注目してるノードの子が末尾よりも小さいということ．
    while(2*i + 1 <= to){
        //節iの子をjとして考える
        j = i * 2 + 1;

        //節iの子のうち大きいほうを節jとする．
        if(j + 1 <= to && a[j] < a[j + 1]) j++;

        //もし親が子より大きいという関係を満たすならこれ以上沈める必要はない．
        if(val >= a[j]) break;

        //実際に沈める操作．a[i]（親）に子の大きいほう（a[j]）をずらして，jに注目する．
        a[i] = a[j];

        //注目する節が一つ下の段になる．
        i = j;
    }

    //適切な場所まで沈められたので代入する．
    a[i] = val;
}

void heap_sort(int *a, size_t n){
    if(n < 2) return;

    //配列をヒープにする
    build_max_heap(a,n);

    //配列の最後から大きい順に埋めていく操作
    for (size_t end = n; end > 1; end--) {
        //根（ヒープ内の最も大きい要素）を配列の最後に移動させる
        SWAP(a[0], a[end-1]);
        //SWAPした末尾[end-1]をソート済み領域に含めるので，再ヒープ化する範囲は[end-2]
        //ヒープの範囲を狭めて再度ヒープにする
        heapify(a, 0, end-2);
    }
}