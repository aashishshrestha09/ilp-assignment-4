#!/bin/bash

# gem5 Installation and Experiment Runner Script
# This script installs gem5 and runs ILP experiments

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PART2_DIR="$SCRIPT_DIR"
GEM5_DIR="$PART2_DIR/gem5"
WORKLOADS_DIR="$PART2_DIR/workloads"
CONFIGS_DIR="$PART2_DIR/gem5-configs"
RESULTS_DIR="$PART2_DIR/results"

echo "=== gem5 ILP Experiment Setup and Runner ==="
echo "Script directory: $SCRIPT_DIR"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies on macOS
install_macos_deps() {
    echo "Installing dependencies for macOS..."
    
    # Install Homebrew if not present
    if ! command_exists brew; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install required packages
    brew install scons protobuf m4 zlib pkg-config python@3.9
    
    # Install Python packages
    pip3 install pydot
}

# Function to install dependencies on Ubuntu/Debian
install_ubuntu_deps() {
    echo "Installing dependencies for Ubuntu/Debian..."
    sudo apt update
    sudo apt install -y build-essential git m4 scons zlib1g zlib1g-dev \
        libprotobuf-dev protobuf-compiler libprotoc-dev \
        python3-dev python3-pip libboost-all-dev pkg-config
    
    pip3 install pydot
}

# Function to install gem5
install_gem5() {
    echo "Installing gem5..."
    
    if [ -d "$GEM5_DIR" ]; then
        echo "gem5 directory already exists. Updating..."
        cd "$GEM5_DIR"
        git pull
    else
        echo "Cloning gem5 repository..."
        cd "$PART2_DIR"
        git clone https://github.com/gem5/gem5.git
        cd "$GEM5_DIR"
    fi
    
    echo "Building gem5 (this may take 15-30 minutes)..."
    # Use fewer parallel jobs to avoid memory issues
    scons build/X86/gem5.opt -j$(( $(nproc) < 4 ? $(nproc) : 4 ))
    
    echo "gem5 build completed successfully!"
}

# Function to compile workloads
compile_workloads() {
    echo "Compiling workloads..."
    cd "$WORKLOADS_DIR"
    make clean
    make all
    
    echo "Testing workloads..."
    make test
    
    echo "Workloads compiled and tested successfully!"
}

# Function to run basic pipeline experiment
run_basic_pipeline() {
    echo "Running basic pipeline experiments..."
    
    mkdir -p "$RESULTS_DIR/basic_pipeline"
    cd "$GEM5_DIR"
    
    local workloads=("simple_loop" "branch_intensive" "parallel_workload")
    
    for workload in "${workloads[@]}"; do
        echo "Running $workload with basic pipeline..."
        local output_dir="$RESULTS_DIR/basic_pipeline/${workload}"
        mkdir -p "$output_dir"
        
        ./build/X86/gem5.opt \
            --outdir="$output_dir" \
            "$CONFIGS_DIR/basic_pipeline.py" \
            "$WORKLOADS_DIR/$workload"
        
        echo "Results saved to: $output_dir"
    done
}

# Function to analyze results
analyze_results() {
    echo "Analyzing experiment results..."
    
    python3 - << 'EOF'
import os
import re
import csv

def parse_stats_file(stats_path):
    """Parse gem5 stats.txt file and extract key metrics"""
    metrics = {}
    
    if not os.path.exists(stats_path):
        return metrics
        
    with open(stats_path, 'r') as f:
        content = f.read()
        
    # Extract key metrics using regex
    patterns = {
        'sim_seconds': r'sim_seconds\s+([\d\.]+)',
        'sim_insts': r'sim_insts\s+(\d+)',
        'host_inst_rate': r'host_inst_rate\s+([\d\.]+)',
        'system.cpu.committedInsts': r'system\.cpu\.committedInsts\s+(\d+)',
        'system.cpu.ipc': r'system\.cpu\.ipc\s+([\d\.]+)',
        'system.cpu.cycles': r'system\.cpu\.numCycles\s+(\d+)',
    }
    
    for metric, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            try:
                metrics[metric] = float(match.group(1))
            except ValueError:
                metrics[metric] = match.group(1)
    
    return metrics

def analyze_basic_pipeline_results():
    """Analyze basic pipeline experiment results"""
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'basic_pipeline')
    
    if not os.path.exists(results_dir):
        print(f"Results directory not found: {results_dir}")
        return
    
    print("\n=== Basic Pipeline Analysis ===")
    
    workloads = ['simple_loop', 'branch_intensive', 'parallel_workload']
    all_results = []
    
    for workload in workloads:
        workload_dir = os.path.join(results_dir, workload)
        stats_file = os.path.join(workload_dir, 'stats.txt')
        
        if os.path.exists(stats_file):
            metrics = parse_stats_file(stats_file)
            metrics['workload'] = workload
            all_results.append(metrics)
            
            print(f"\n{workload.upper()} Results:")
            print(f"  Simulation time: {metrics.get('sim_seconds', 'N/A')} seconds")
            print(f"  Instructions: {metrics.get('sim_insts', 'N/A')}")
            print(f"  IPC: {metrics.get('system.cpu.ipc', 'N/A')}")
            print(f"  Host inst rate: {metrics.get('host_inst_rate', 'N/A')} inst/sec")
        else:
            print(f"Stats file not found for {workload}: {stats_file}")
    
    # Save results to CSV
    if all_results:
        csv_path = os.path.join(results_dir, 'analysis_summary.csv')
        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ['workload', 'sim_seconds', 'sim_insts', 'system.cpu.ipc', 'host_inst_rate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in all_results:
                writer.writerow({k: result.get(k, '') for k in fieldnames})
        print(f"\nResults saved to: {csv_path}")

if __name__ == "__main__":
    analyze_basic_pipeline_results()
EOF
}

# Main execution flow
main() {
    echo "Starting gem5 setup and ILP experiments..."
    
    # Detect OS and install dependencies
    if [[ "$OSTYPE" == "darwin"* ]]; then
        install_macos_deps
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt; then
            install_ubuntu_deps
        else
            echo "Unsupported Linux distribution. Please install dependencies manually."
            echo "Required: scons, protobuf, m4, zlib, gcc, python3"
            exit 1
        fi
    else
        echo "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    
    # Install gem5
    install_gem5
    
    # Compile workloads
    compile_workloads
    
    # Run experiments
    echo "Starting ILP experiments..."
    run_basic_pipeline
    
    # Analyze results
    analyze_results
    
    echo ""
    echo "=== Experiment Complete ==="
    echo "Results available in: $RESULTS_DIR"
    echo "To view detailed statistics: cat $RESULTS_DIR/basic_pipeline/*/stats.txt"
    echo "To view configurations: cat $RESULTS_DIR/basic_pipeline/*/config.ini"
}

# Command line argument handling
case "${1:-all}" in
    "deps")
        if [[ "$OSTYPE" == "darwin"* ]]; then
            install_macos_deps
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            install_ubuntu_deps
        fi
        ;;
    "install")
        install_gem5
        ;;
    "compile")
        compile_workloads
        ;;
    "run")
        run_basic_pipeline
        ;;
    "analyze")
        analyze_results
        ;;
    "all"|*)
        main
        ;;
esac