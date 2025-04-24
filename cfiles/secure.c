#include <stdio.h> 
#include <string.h> 
#define N 256

char plaintext[N];    // 平文 
char ciphertext[N];   // 暗号文 
char key[N];          // バーナム暗号用の鍵 

int i; 

int main()
{
    //---- 入力 
    fprintf(stderr, "平文を入力して下さい： \t"); 
    scanf("%s", plaintext); 

    fprintf(stderr, "鍵を入力して下さい： \t"); 
    scanf("%s", key); 

    //---- バーナム暗号化 
    for (i = 0; i < strlen(plaintext); i++){ 
        ciphertext[i] = plaintext[i] ^ key[i];
    } 

    ciphertext[i] = '\0'; 

    //---- 結果出力 
    printf("平文(16進数表現)： \t"); 

    for (i = 0; i < strlen(plaintext); i++){
        printf("%02X ", plaintext[i]); 
    }

    printf("\n"); 

 

    printf("鍵(16進数表現)： \t"); 

    for (i = 0; i < strlen(key); i++) printf("%02X ", key[i]); 

    printf("\n"); 

 

    printf("暗号文(16進数表現)： \t"); 

    for (i = 0; i < strlen(plaintext); i++) printf("%02X ", ciphertext[i]); 

    printf("\n"); 

 

    printf("暗号文(文字列表現)： \t%s\n", ciphertext); 

 

    return 0; 

} 