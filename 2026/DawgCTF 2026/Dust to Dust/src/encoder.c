#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int strIsBin(char* buffer) {
    size_t len = strlen(buffer);
    int len2 = strspn(buffer,"01");
    if ((len-1) != len2) {
        return 0;
    }
    else {
        return 1;
    }
}

char** allocArray(int* l, int* w) {
    int MAX_LINE_LENGTH = 1024, line_count = 0, line_curr = 0;
    FILE *input, *output;
    char** arrstarr_yarharhar;
    char buffer[MAX_LINE_LENGTH];
    size_t char_count = 0;

    input = fopen("input.txt", "r");
    if (input == NULL) {
        printf("Error opening file input.txt\n");
        return NULL;
    }

    while (fgets(buffer, MAX_LINE_LENGTH, input) != NULL) {
        line_count++;
        size_t curr = strlen(buffer);
        if ((curr - 1) % 3 != 0) {
            int num = (curr - 1);
            fclose(input);
            printf("Line %i does not have multiple of 3 characters, holds %i", line_count, num);
            return NULL;
        }
        if ((char_count != curr) && (char_count != 0)) {
            fclose(input);
            printf("Line %i does not match first line", line_count);
            return NULL;
        }
        if (strIsBin(buffer) == 0) {
            fclose(input);
            printf("Line %i does not contain only binary characters", line_count);
            return NULL;
        }
        if (char_count == 0) {
            char_count = curr;
        }
    }

    if (line_count % 2 != 0) {
        fclose(input);
        printf("File does not have a multiple of 2 lines; contains %i", line_count);
        return NULL;
    }


    
    arrstarr_yarharhar = malloc(line_count * sizeof (char *));
    if (arrstarr_yarharhar == NULL) {
        printf("malloc failed for char* array");
        return NULL;
    }

    fclose(input);
    input = fopen("input.txt", "r");
    
    while (fgets(buffer, MAX_LINE_LENGTH, input) != NULL) {
        arrstarr_yarharhar[line_curr] = malloc(char_count * sizeof(char));
        if (arrstarr_yarharhar[line_curr] == NULL) {
            printf("malloc failed at line %i", line_curr);
            return NULL;
        }

        sprintf(arrstarr_yarharhar[line_curr], buffer);
        line_curr++;
    }

    fclose(input);

    *l = line_count;
    *w = char_count;
    return arrstarr_yarharhar;
}

void freeArray(char** arr, int len) {
    for (int i = 0; i < len; i++) {
        free(arr[i]);
        arr[i] = NULL;
    }
    free(arr);
    arr = NULL;
}

char** compressArray(char** arr, int level, int* length, int* width) {
    if (*length % 2 != 0 && *width-1% 3 != 0) {
        printf("Array of size %ix%i cannot be compressed (is it not null terminated?)", length, width);
        return NULL;
    }

    int length_new = *length / 2;
    int width_new = (*width / 3) + 1;

    char** arr_new = malloc(length_new * sizeof (char*));
    for (int i = 0; i < length_new; i++) {
        arr_new[i] = malloc(width_new * sizeof(char));
    }

    for (int l = 0; l < length_new; l++) {
        for (int w = 0; w < width_new; w++) {
            if (w == width_new - 1) {
                arr_new[l][w] = '\0';
            }
            else {
                char buffer[7], c;

                if (level == 1) {

                    buffer[0] = arr[l*2][w*3];
                    buffer[1] = arr[l*2][w*3 + 1];
                    buffer[2] = arr[l*2][w*3 + 2];
                    buffer[3] = arr[l*2 + 1][w*3];
                    buffer[4] = arr[l*2 + 1][w*3 + 1];
                    buffer[5] = arr[l*2 + 1][w*3 + 2];
                    buffer[6] = '\0';

                    long bin = strtol(buffer, NULL, 2);
                    c = (char)(0b00100000 + bin);
                    arr_new[l][w] = c;
                }

                /*else if (level == 2) {
                    Ignore this part I'll add it later
                }*/
            }
        }

    }

    
    freeArray(arr, (length_new * 2));
    *length = length_new;
    *width = width_new;
    return arr_new;

}

void writeArray(char** arr, int len) {
    FILE* output = fopen("output.txt", "w");
    int i = 0;
    
    while (i < len) {
        fprintf(output, "%s%c", arr[i], (char)0b01111101);
        i++;
    }
    fprintf(output, "%c", (char)0b01111110);
    fclose(output);
}

int main() {
    int l, w;
    char** str = allocArray(&l, &w);
    if (str == NULL) {
        return 1;
    }

    str = compressArray(str, 1, &l, &w);
    //str = compressArray(str, 2, &l, &w);

    writeArray(str, l);
    freeArray(str, l);
    return 0;
}