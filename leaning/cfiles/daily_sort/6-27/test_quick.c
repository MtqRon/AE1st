#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

extern void quick_sort(int*, size_t);

bool is_sorted(int *a, size_t n) {
    for (size_t i = 1; i < n; ++i) {
        if (a[i - 1] > a[i]) {
            return false;
        }
    }
    return true;
}

int main() {
    int test[] = {5, 2, 8, 1, 9, 3};
    size_t n = 6;
    
    printf("Before sorting: ");
    for (size_t i = 0; i < n; i++) {
        printf("%d ", test[i]);
    }
    printf("\n");
    
    quick_sort(test, n);
    
    printf("After sorting: ");
    for (size_t i = 0; i < n; i++) {
        printf("%d ", test[i]);
    }
    printf("\n");
    
    printf("Is sorted: %s\n", is_sorted(test, n) ? "Yes" : "No");
    
    return 0;
}
