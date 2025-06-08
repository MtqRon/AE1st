#include <stddef.h>

static inline void swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

static int partition(int *a, int left, int right){
    //枢軸を真ん中にする
    int pivot = a[(right + left) / 2];

    //インデックスの関係，範囲を走査する変数
    size_t i = left - 1;
    size_t j = right + 1;

    /*左側なのにピボットよりでかい数のインデックス，
    右側なのにピボットより小さい数のインデックスが
    それぞれi,jに入る*/
    while(1){
        while(a[++i] < pivot);
        while(a[--j] > pivot);
        if(i >= j) return j;
        swap(&a[i], &a[j]);
    }
}

void quick_sort(int *a, size_t n){
    int stack[32];
    int top = -1;

    //最初の左端と右端
    int left = 0, right = n - 1;

    stack[++top] = left;
    stack[++top] = right;

    while(top >= 0){
        //処理する範囲をスタックからポップする
        right = stack[top--];
        left = stack[top--];

        while(left < right){
            //mid:枢軸の最終的なインデックス
            size_t mid = partition(a, left, right);

            //これなに？
            if(mid - left < right - mid){
                //枢軸の右側が右端じゃなければ
                if(mid + 1 < right){
                    stack[++top] = mid + 1;
                    stack[++top] = right;
                }
                right = mid;
            }else{
                //枢軸の左側が左端じゃなければ
                if(left < mid){
                    stack[++top] = left;
                    stack[++top] = mid;
                }
                left = mid + 1;
            }
        }
    }
}