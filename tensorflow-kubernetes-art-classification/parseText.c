#include <stdio.h>
 
int main() {
    FILE *fp;
    char* filename = "arts-select.list";
 
    fp = fopen(filename, "r");
    if (fp == NULL){
        printf("Could not open file %s",filename);
        return 1;
    }
    while (fgets(str, MAXCHAR, fp) != NULL)
        printf("%s", str);
    fclose(fp);
    
    return 0;
}