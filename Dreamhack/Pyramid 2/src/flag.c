#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(NULL));
    setvbuf(stdout, NULL, _IONBF, 0);

    int A = rand() % (10000 - 100 + 1) + 100;
    int B = rand() % (10000 - 100 + 1) + 100;
    int C = rand() % (10000 - 100 + 1) + 100;

    int guess;
    int ans = A * B + C;

    printf("%d * %d + %d = ?\n", A, B, C);
    fflush(stdout);

    scanf("%d", &guess);

    if (ans == guess) {
        printf("Flag is DH{THIS_IS_FAKE_FLAG}");
        fflush(stdout);
    } else {
        printf("Wrong");
        fflush(stdout);
    }
}