#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
    //変数の宣言
    int input = 0; //入力した数字
    int f_digit = 0, s_digit = 0, t_digit = 0; //1桁ずつ分解した数字
    int blow = 0, hit = 0; //blowとhitのカウント
    int f_rand = 0, s_rand = 0, t_rand = 0; //乱数で生成した数字
    int i = 1; //ループカウンター

    //乱数の初期化
    srand(time(NULL));

    //乱数を1桁ずつかぶらないように生成
    do{
        f_rand = rand() % 10; //1の位，0~9の乱数を生成
        s_rand = rand() % 10; //10の位，0~9の乱数を生成
        t_rand = rand() % 10; //100の位，0~9の乱数を生成
    }while(f_rand == s_rand || f_rand == t_rand || s_rand == t_rand); //かぶらないようにする

    //ゲームの説明
    printf("0~9の3桁の被りのない数字をヒントをもとに予測してください！\n");
    printf("数字を入力すると，ヒット数とブロー数を表示します．\nヒットは位置と数字が一致している数，ブローは数字は一致しているが，位置が一致していない数です．\n");
    printf("10回以内に予測できなければゲームオーバー！\n");
    printf("それではゲームスタート！\n");

    do{
        //予測した数字を入力
        printf("予測する数字を入力してください(%d回目)：\n", i);
        scanf("%d", &input);

        //入力した数字を1桁ずつ分解
        f_digit = input / 100; //100の位
        s_digit = (input / 10) % 10; //10の位
        t_digit = input % 10; //1の位
        
        //blowとhitのカウントの初期化
        blow = 0;
        hit = 0;

        //1桁目の判定
        if(s_rand == f_digit || t_rand == f_digit){
            blow++; 
        }else if (f_rand == f_digit){
            hit++;
        }
        //2桁目の判定
        if(f_rand == s_digit || t_rand == s_digit){
            blow++;
        } else if(s_rand == s_digit){
            hit++;
        }
        //3桁目の判定
        if(f_rand == t_digit || s_rand == t_digit){
            blow++;
        } else if(t_rand == t_digit){
            hit++;
        }

        //結果の表示
        printf("blow:%d, hit:%d\n", blow, hit);

        //ヒット数が3の時，正解，それ以外はもう一度予測
        if(hit == 0){
            printf("残念！もう一度予測してください！\n");
            i++; //ループカウンタをインクリメント
        }else if(hit == 1){
            printf("もう少し！もう一度予測してください！\n");
            i++;
        }else if(hit == 2){
            printf("惜しい！もう一度予測してください！\n");
            i++;
        }else if(hit == 3){
            printf("すごい！！正解です！(%d回目)\n", i);
        }
    }while(hit != 3 && i <= 10); //ヒット数が3になるまで繰り返す（最大10回まで）

    if(i > 10) {
        printf("10回以内に予測できませんでした T_T GameOver!\n");
    }

    //正解の数字を表示
    printf("正解の数字は%d%d%dです．\n", f_rand, s_rand, t_rand);
    printf("ゲームを終了します。\n");

    //プログラムの終了
    return 0;
}