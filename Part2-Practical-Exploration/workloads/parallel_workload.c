/*
 * ILP-Friendly Workload 
 * This program is designed to have high instruction-level parallelism
 * with many independent operations that can be executed simultaneously
 */

#include <stdio.h>
#include <stdlib.h>

#define ARRAY_SIZE 10000
#define ITERATIONS 1000

int main() {
    // Allocate arrays for parallel operations
    int *array_a = malloc(ARRAY_SIZE * sizeof(int));
    int *array_b = malloc(ARRAY_SIZE * sizeof(int));
    int *array_c = malloc(ARRAY_SIZE * sizeof(int));
    int *array_d = malloc(ARRAY_SIZE * sizeof(int));
    
    if (!array_a || !array_b || !array_c || !array_d) {
        printf("Memory allocation failed\n");
        return 1;
    }
    
    printf("Starting ILP-friendly workload with %d elements and %d iterations\n", 
           ARRAY_SIZE, ITERATIONS);
    
    // Initialize arrays
    for (int i = 0; i < ARRAY_SIZE; i++) {
        array_a[i] = i;
        array_b[i] = i * 2;
        array_c[i] = i * 3;
        array_d[i] = i * 4;
    }
    
    // Main computation loop with high ILP potential
    for (int iter = 0; iter < ITERATIONS; iter++) {
        for (int i = 0; i < ARRAY_SIZE - 4; i += 4) {
            // Unrolled loop with independent operations
            // These operations can be executed in parallel
            
            // Batch 1: Independent arithmetic operations
            int temp1 = array_a[i] + array_b[i];
            int temp2 = array_a[i+1] + array_b[i+1];
            int temp3 = array_a[i+2] + array_b[i+2];
            int temp4 = array_a[i+3] + array_b[i+3];
            
            // Batch 2: Independent multiply operations
            int mult1 = array_c[i] * 3;
            int mult2 = array_c[i+1] * 3;
            int mult3 = array_c[i+2] * 3;
            int mult4 = array_c[i+3] * 3;
            
            // Batch 3: Independent bitwise operations
            int bit1 = array_d[i] << 1;
            int bit2 = array_d[i+1] << 1;
            int bit3 = array_d[i+2] << 1;
            int bit4 = array_d[i+3] << 1;
            
            // Combine results (some dependencies here)
            array_a[i] = temp1 + mult1 + bit1;
            array_a[i+1] = temp2 + mult2 + bit2;
            array_a[i+2] = temp3 + mult3 + bit3;
            array_a[i+3] = temp4 + mult4 + bit4;
            
            // Additional independent operations
            array_b[i] = (temp1 & 0xFF) ^ (mult1 & 0xFF);
            array_b[i+1] = (temp2 & 0xFF) ^ (mult2 & 0xFF);
            array_b[i+2] = (temp3 & 0xFF) ^ (mult3 & 0xFF);
            array_b[i+3] = (temp4 & 0xFF) ^ (mult4 & 0xFF);
        }
    }
    
    // Calculate final result to prevent dead code elimination
    long long sum = 0;
    for (int i = 0; i < ARRAY_SIZE; i++) {
        sum += array_a[i] + array_b[i];
    }
    
    printf("ILP-friendly computation completed: sum=%lld\n", sum);
    
    // Cleanup
    free(array_a);
    free(array_b);
    free(array_c);
    free(array_d);
    
    return 0;
}