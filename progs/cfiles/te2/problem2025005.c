#include <stdio.h>

#define NUM 6 // 生徒数
#define SUBJECT 2 // 科目数

int main(void){
    // 生徒ごとの点数
    int tensu[NUM][SUBJECT];
    // 生徒ごとの合計点
    int sum[NUM];
    // 科目ごとの合計点
    int sub_sum[SUBJECT];
    int i, j;

    // 入力
    printf("%d人分の%d科目の点数を入力してください。\n", NUM, SUBJECT);
    for(i = 0; i < NUM; i++){
        printf("%d人目\n", i + 1);
        for(j = 0; j < SUBJECT; j++){
            printf("科目%d: ", j + 1);
            scanf("%d", &tensu[i][j]);
        }
    }

    // 科目ごとの合計点を計算
    for(i = 0; i < SUBJECT; i++){
        sub_sum[i] = 0;
        for(j = 0; j < NUM; j++){
            sub_sum[i] += tensu[j][i];
        }
    }

    // 生徒ごとの合計点を計算
    for(i = 0; i < NUM; i++){
        sum[i] = 0;
        for(j = 0; j < SUBJECT; j++){
            sum[i] += tensu[i][j];
        }
    }

    // 科目ごとの合計点と平均点を表示
    printf("国語の合計点：%d点 国語の平均点：%d点\n", sub_sum[0], sub_sum[0] / NUM);
    printf("数学の合計点：%d点 数学の平均点：%d点\n", sub_sum[1], sub_sum[1] / NUM);


    // 生徒ごとの成績を表示
    printf("生徒の成績\n");
    for(i = 0; i < NUM; i++){
        printf("%2d人目：国語%6d点 数学%6d点 合計%6d点 平均%6.1f点\n", i + 1, tensu[i][0], tensu[i][1], sum[i], (double)sum[i] / SUBJECT);
    }

    return 0;
}