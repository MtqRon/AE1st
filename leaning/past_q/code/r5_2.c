#include <stdio.h>
#define N 10

int next_partition(int a[]){
    int k = 0;
    int r = 0;
    while(k < N && a[k + 1] != 0){
        k++;
    }
    while(a[k] == 1 && k >= 0){
        r++; k--;
    }

    if(k < 0) return 0;

    a[k]--;
    r++;

    while(r > a[k]){
        a[k + 1] = a[k];
        r = r - a[k];
        k++;
    }

    a[k + 1] = r;
    a[k + 2] = 0;

    return 1;
}

int is_all_distinct(int a[]){
    int i = N;
    int check[N];

    do{
        i--;
        check[i] = 0;
    }while(i > 0);

    while(a[i] != 0){
        if(check[a[i]]){
            return 0;
        }else{
            check[a[i]]++;
            i++;
        }
    }
    return 1;
}

int odd_to_distinct(int *a){
    int i = 0;
    int j;
    do{
        for(j = 1; j < N + 1 && a[j] != 0; j++){
            if(a[j - 1] == a[j]){
                a[j - 1] += a[j];
                while(a[j] != 0){
                    a[j] = a[j + 1];
                    j++;
                }
                j = 0;
            }
        }
        i++;
    }while(a[i] != 0);
}

void main(){
    int a[N + 1] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0};

    if(!is_all_distinct(a)){
        printf("Initial partition: ");
        for(int i = 0; i < N + 1; i++){
            if(a[i] == 0) break;
            printf("%d ", a[i]);
        }
        printf("\nError: Not all elements are distinct.\n");
    }

    printf("Execute odd_to_distinct\n");

    odd_to_distinct(a);

    printf("Distinct partition: ");
    for(int i = 0; i < N + 1; i++){
        if(a[i] == 0) break;
        printf("%d ", a[i]);
    }

    if(!is_all_distinct(a)){
        printf("\nError: Not all elements are distinct after odd_to_distinct.\n");
    } else {
        printf("\nAll elements are distinct after odd_to_distinct.\n");
    }
}
