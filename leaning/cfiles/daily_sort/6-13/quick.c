#include <stddef.h>

static void swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}
int partition(int *a, int left, int right){
    int pivot = a[(left + right) / 2];
    int i = left - 1;
    int j = right + 1;

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

    //最初に注目する区間
    int left = 0, right = n - 1;

    //左端，右端の順でスタックに入れる．
    stack[++top] = left;
    stack[++top] = right;

    //スタックが無くなるまで
    while(top >= 0){
        //左端，右端の順で入れたので，右端→左端の順でポップする
        right = stack[top--];
        left = stack[top--];

        while(left < right){
            //最終的なピボットのインデックスがmid
            int mid = partition(a, left, right);

            if(mid - left < right - mid){
                if(mid + 1 < right){
                    stack[++top] = mid + 1;
                    stack[++top] = right;
                }
                right = mid;
            }else{
                if(left < mid){
                    stack[++top] = left;
                    stack[++top] = mid;
                }
                left = mid + 1;
            }
        }
    }
}