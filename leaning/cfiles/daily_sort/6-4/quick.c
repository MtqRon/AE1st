#include <stddef.h>

int partition(int *a, int low, int high) {
    int pivot = a[(low + high) / 2];
    int i = low - 1, j = high + 1;
    while (1) {
        while (a[++i] < pivot);   // pivot 未満を探す
        while (a[--j] > pivot);   // pivot 超えを探す
        if (i >= j) return j;     // ポインタが交差→境界
        int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
    }
}


void quick_sort(int *a, int n)
{
    // スタック手動管理で末尾再帰最適化
    int stack[32]; int top = -1;
    int low = 0, high = n - 1;
    stack[++top] = low; stack[++top] = high;

    while (top >= 0) {
        //スタックからポップする
        high = stack[top--];
        low  = stack[top--];

        while (low < high) {
            int mid = partition(a, low, high);

            // 小さい側を先に / 大きい側をスタックへ
            if(mid - low < high - mid){
                if(mid + 1 < high){
                    stack[++top] = mid + 1;
                    stack[++top] = high;
                }
                high = mid;
            }else{
                if(low < mid){
                    stack[++top] = low;
                    stack[++top] = mid;
                }
                low = mid + 1;
            }
        }
    }
}