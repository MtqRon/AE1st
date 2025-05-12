#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//終了条件を定義
#define END_CONDITION 5

/*
TODO
0,1,-1以外の数値が入力された場合の例外処理
正解時間のテキストファイルへの書き込み
*/

//1～100までの乱数を生成し素数かどうか回答する．
//END_CONDITION回連続で正解するとゲームクリア．
//ユーザーが-1を入力するとゲーム終了．
//正解数をカウントし，ゲームクリア時に経過時間を表示する．

int random_number(void){
    return rand() % 100 + 1; //1から100までのランダムな整数を生成
}

int is_prime(int num){
    //2以下は素数ではない
    if(num < 2) return 0;
    //2以上の数は素数かどうかを判定
    for(int i = 2; i * i <= num; i++){
        if(num % i == 0) return 0; //割り切れる数があれば素数ではない
    }
    return 1; //素数と判断
}

int main(void){

    //乱数の初期化
    srand(time(NULL));

    //変数の宣言
    int count = 0;
    int number = 0;
    int ans = 0;
    long start_time = 0;
    long end_time = 0;

    //ゲームの説明
    printf("If you guess printed number is prime, please input 1.\n");
    printf("If you guess printed number is not prime, please input 0.\n");
    printf("If you want to exit, please input -1.\n");
    printf("Let's start the game!\n");

    //ゲーム開始時刻を記録
    start_time = time(NULL); 
    
    while(1){
        //1から100までの乱数を生成
        number = random_number();
        
        //素数かどうかをユーザーが判定
        printf("number: %d\n", number);
        printf("is prime? (1: yes, 0: no, -1: exit): ");
        scanf("%d", &ans);

        if(ans == is_prime(number)){
            //正解の場合
            //countをインクリメント
            count++;
            printf("correct! %d is prime number.\n", number);
            //規定数正解した場合
            if(count == END_CONDITION){
                printf("Perfect! You have guessed %d prime numbers in a row!\n",END_CONDITION);
                end_time = time(NULL); //ゲーム終了時刻を記録
                printf("Time:%lf seconds\n", end_time - start_time);
                break;
            }
        }else if(ans == -1){
            //ゲーム終了の場合
            printf("exit\n");
            break;
        }else{
            //不正解の場合
            //countをリセット
            count = 0;
            printf("wrong! %d is not prime number.\n", number);
        }
    }
    //ゲーム終了
    printf("If you want to play again, please restart the program.\n");
    return 0;
}