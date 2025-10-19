/*
 * Branch-Intensive Workload for Branch Prediction Analysis
 * This program contains various branch patterns to test
 * branch prediction accuracy and its impact on ILP
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ITERATIONS 100000

int main() {
    srand(time(NULL));
    int sum = 0;
    int pattern_counter = 0;
    
    printf("Starting branch-intensive workload with %d iterations\n", ITERATIONS);
    
    for (int i = 0; i < ITERATIONS; i++) {
        int random_val = rand() % 100;
        
        // Predictable branch pattern (every 4th iteration)
        if (pattern_counter % 4 == 0) {
            sum += random_val * 2;
        } else {
            sum += random_val;
        }
        
        // Random branch (unpredictable)
        if (random_val > 50) {
            sum += i;
            if (random_val > 75) {
                sum *= 2;
            }
        } else {
            sum -= i;
            if (random_val < 25) {
                sum /= 2;
            }
        }
        
        // Nested conditional with data dependency
        if (sum > 1000000) {
            sum = sum % 1000000;
            if (sum < 500000) {
                sum += random_val * i;
            }
        }
        
        pattern_counter++;
    }
    
    printf("Branch-intensive computation completed: sum=%d\n", sum);
    
    return 0;
}