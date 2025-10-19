/*
 * Simple Loop Workload for ILP Analysis
 * This program performs basic arithmetic operations in a loop
 * to demonstrate instruction-level parallelism opportunities
 */

#include <stdio.h>
#include <stdlib.h>

#define ITERATIONS 1000000

int main() {
    int a = 1, b = 2, c = 3, d = 4;
    int result1 = 0, result2 = 0, result3 = 0;
    
    printf("Starting simple loop workload with %d iterations\n", ITERATIONS);
    
    // Simple loop with potential ILP
    for (int i = 0; i < ITERATIONS; i++) {
        // Independent operations that can be executed in parallel
        result1 = a + b;           // Independent operation 1
        result2 = c * d;           // Independent operation 2  
        result3 = result1 + result2; // Dependent on previous results
        
        // Update variables to prevent compiler optimization
        a = result1 & 0xFF;
        b = result2 & 0xFF;
        c = result3 & 0xFF;
        d = (a + b + c) & 0xFF;
    }
    
    printf("Computation completed: result1=%d, result2=%d, result3=%d\n", 
           result1, result2, result3);
    
    return 0;
}