#include<stdio.h>
#include<stdlib.h>

#define MATRIXSIZE 100

unsigned int matrix1[MATRIXSIZE][MATRIXSIZE], matrix2[MATRIXSIZE][MATRIXSIZE];
unsigned long int resultmatrix[MATRIXSIZE][MATRIXSIZE];

int main(){


    //printf("Matrix Size is %d ", MATRIXSIZE);
    for(int i=0; i<MATRIXSIZE;++i){

        for(int j=0; j<MATRIXSIZE;++j){

            matrix1[i][j] = rand();
            matrix2[i][j] = rand();
            resultmatrix[i][j] = 0;
            //printf("(%d,%d) : %d %d\n",i,j, matrix1[i][j], matrix2[i][j]);
        }
    }

    // Transposing Second Matrix
    for(int i=0;i<MATRIXSIZE;++i){

    	for(int j = 0; j < MATRIXSIZE; ++j){

		unsigned int temp = matrix2[i][j];
	        matrix2[i][j] = matrix2[j][i];
	        matrix2[j][i] = temp;
    	}
    }

    for (int i = 0; i < MATRIXSIZE; ++i){
        for(int j = 0; j < MATRIXSIZE; ++j){

	    unsigned long int sum = 0;
            for (int k = 0; k <MATRIXSIZE; ++k){
	            resultmatrix[i][j] += matrix1[i][k] * matrix2[j][k];
	    }
	
        }
    }


    return 0;
}