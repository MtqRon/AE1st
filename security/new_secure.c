#include <stdio.h>
#include <stdlib.h>

//文字を格納するノード
typedef struct CHAR{
    char c;
    struct CHAR *next;
} CHAR;

//文字列を格納するリスト
typedef struct SLIST{
    struct CHAR *head;
    struct CHAR *tail;
} SLIST;


//文字を格納したノードを作成する関数（CHAR型）
CHAR *new_entry(char c_entry){
    //mallocで受けるのはポインタ
    CHAR *new = malloc(sizeof(CHAR));
    //mallocで確保したメモリに文字を格納
    //nextはNULLで初期化
    new->c = c_entry;
    new->next = NULL;
    return new;
}


//リストの初期化を行う関数
void list_init(SLIST *list){
    //headのメモリを確保し，初期値をNULL文字に設定
    list->head = malloc(sizeof(CHAR));
    list->head->c = '\0';
    //初期値ではheadのnextはNULL
    list->head->next = NULL;
    //tailはheadを指すようにする
    list->tail = list->head;
} 


//リストに文字を追加する関数
void add_entry(SLIST *list, char c_entry){
    //new_entryで新しいノードを作成
    CHAR *new = new_entry(c_entry);
    //tailのnextに新しいノードを追加(tailのおかげでO(1))
    list->tail->next = new;
    //tailを新しいノードに更新
    list->tail = new;
}


//リストを出力する関数
void print_list(SLIST *list){
    //headはNULL文字を格納しているので，出力しない(head->nextから)
    for(CHAR *p = list->head->next; p != NULL; p = p->next){
        putchar(p->c);
    }
}


//リストの内容を16進数で出力する関数
void print_hex(SLIST *list){
    //headはNULL文字を格納しているので，出力しない(head->nextから)
    for(CHAR *p = list->head->next; p != NULL; p = p->next){
        //%02Xは2桁の16進数で出力する書式指定子みたい
        printf("%02X ", p->c);
    }
}


//文字列と鍵から暗号文を生成する関数
void vernam(SLIST *text, SLIST *key, SLIST *dist){
    //headはNULL文字を格納しているのでhead->nextから処理を行う．
    CHAR *p_text = text->head->next;
    CHAR *p_key = key->head->next;

    //textとkeyの長さが異なる場合は，短い方に合わせる
    //p_textとp_keyがNULLになるまで処理を行う
    while(p_text != NULL && p_key != NULL){
        //p_textとp_keyの文字をXORしてdistに格納
        add_entry(dist, (char)(p_text->c ^ p_key->c));
        //次のノードに移動
        p_text = p_text->next;
        p_key = p_key->next;
    }
}


//文字列の読み込みを行う関数
void read_line(SLIST *read){
    //文字を読み込むための変数
    int c_entry;

    //文字を読み込む（EOFまたは改行まで）
    while((c_entry = getchar()) != '\n' && c_entry != EOF){
        add_entry(read, (char)c_entry);
    }
}

//メモリの解放を行う関数
void list_clear(SLIST *list){
    CHAR *p = list->head;
    while (p) {
        CHAR *next = p->next;
        free(p);
        p = next;
    }
    //使いまわす場合
    //引数がポインタなので&不要（なはず）
    list_init(list);
}


int main(void){
    printf("使用するモードを選択してください。\n");
    printf("1: 暗号化\n");
    printf("2: 復号化\n");
    printf("選択肢を入力してください：\n");
    int mode;
    scanf("%d", &mode);
    //改行を読み飛ばす
    getchar();
    //modeが1または2以外の場合はエラー
    if(mode != 1 && mode != 2){
        printf("無効な選択肢です。\n");
        return 1;
    }else if(mode == 1){
        printf("暗号化モードを選択しました。\n");

        /*
        text:平文
        key:鍵
        encrypted:暗号化後
        decrypted:復号
        */
        SLIST text, key, encrypted, decrypted;

        //リストの初期化
        list_init(&text);
        list_init(&key);
        list_init(&encrypted);
        list_init(&decrypted);

        //平文の入力
        printf("平文を入力してください：\n");
        read_line(&text);

        //鍵の入力
        printf("鍵を入力してください：\n");
        read_line(&key);

        //バーナム暗号化
        vernam(&text, &key, &encrypted);

        //復号
        vernam(&encrypted, &key, &decrypted);

        //結果の出力
        printf("平文(16進数表現)：\n");
        print_hex(&text);
        printf("\n");

        printf("鍵(16進数表現)：\n");
        print_hex(&key);
        printf("\n");

        printf("暗号文(16進数表現)：\n");
        print_hex(&encrypted);
        printf("\n");

        printf("暗号文(文字列表現)：\n");
        print_list(&encrypted);
        printf("\n");

        printf("復号された平文：\n");
        print_list(&decrypted);
        printf("\n");

        //メモリの解放
        list_clear(&text);
        list_clear(&key);
        list_clear(&encrypted);
        list_clear(&decrypted);
    
    }else if(mode == 2){
        printf("復号化モードを選択しました。\n");
        SLIST ciphertext, decryption_key, decrypted_text;
        list_init(&ciphertext);
        list_init(&decryption_key);
        list_init(&decrypted_text);

        printf("暗号文を入力してください：\n");
        read_line(&ciphertext);
        printf("復号鍵を入力してください：\n");
        read_line(&decryption_key);
        vernam(&ciphertext, &decryption_key, &decrypted_text);
        printf("復号された平文：\n");
        print_list(&decrypted_text);
        printf("\n");

        //メモリの解放
        list_clear(&ciphertext);
        list_clear(&decryption_key);
        list_clear(&decrypted_text);

    }
    return 0;
}