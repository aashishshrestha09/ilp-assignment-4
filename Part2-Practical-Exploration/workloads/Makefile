# Makefile for ILP Workloads
# Compiles test programs for gem5 simulation

CC = gcc
CFLAGS = -O2 -std=c99
TARGET_ARCH = x86_64

# Source files
SOURCES = simple_loop.c branch_intensive.c parallel_workload.c

# Object files (replace .c with .o)
OBJECTS = $(SOURCES:.c=.o)

# Executable files (replace .c with no extension)
EXECUTABLES = $(SOURCES:.c=)

# Default target
all: $(EXECUTABLES)

# Rule to compile individual programs
%: %.c
	$(CC) $(CFLAGS) -o $@ $<
	@echo "Compiled $@ successfully"

# Individual targets for clarity
simple_loop: simple_loop.c
	$(CC) $(CFLAGS) -o simple_loop simple_loop.c

branch_intensive: branch_intensive.c
	$(CC) $(CFLAGS) -o branch_intensive branch_intensive.c

parallel_workload: parallel_workload.c
	$(CC) $(CFLAGS) -o parallel_workload parallel_workload.c

# Clean compiled files
clean:
	rm -f $(EXECUTABLES) $(OBJECTS)
	@echo "Cleaned up compiled files"

# Test executables (run natively for verification)
test: $(EXECUTABLES)
	@echo "Testing compiled executables..."
	@echo "Running simple_loop:"
	./simple_loop | head -n 5
	@echo "Running branch_intensive:"
	./branch_intensive | head -n 5
	@echo "Running parallel_workload:"
	./parallel_workload | head -n 5

# Help target
help:
	@echo "Available targets:"
	@echo "  all                - Compile all workloads"
	@echo "  simple_loop        - Compile simple loop workload"
	@echo "  branch_intensive   - Compile branch-heavy workload"
	@echo "  parallel_workload  - Compile ILP-friendly workload"
	@echo "  test              - Run all executables natively"
	@echo "  clean             - Remove compiled files"
	@echo "  help              - Show this help message"

.PHONY: all clean test help