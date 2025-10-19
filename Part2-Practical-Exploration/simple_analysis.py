#!/usr/bin/env python3

"""
Simple Results Analysis Script for ILP Experiments
Analyzes gem5 simulation results without external dependencies
"""

import os
import csv
import json
from pathlib import Path

def analyze_performance_summary(csv_path):
    """Analyze the performance summary CSV"""
    print("="*60)
    print("           ILP EXPERIMENT PERFORMANCE ANALYSIS")
    print("="*60)
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Group by experiment type
    experiments = {}
    for row in data:
        exp_type = row['Experiment']
        if exp_type not in experiments:
            experiments[exp_type] = []
        experiments[exp_type].append(row)
    
    # Analyze each experiment
    for exp_type, exp_data in experiments.items():
        print(f"\n{exp_type.upper()} EXPERIMENT RESULTS:")
        print("-" * 50)
        
        if exp_type == "Basic Pipeline":
            analyze_basic_pipeline(exp_data)
        elif exp_type == "Branch Prediction":
            analyze_branch_prediction(exp_data)
        elif exp_type == "Superscalar":
            analyze_superscalar(exp_data)

def analyze_basic_pipeline(data):
    """Analyze basic pipeline results"""
    print("IPC Performance by Workload:")
    
    for row in data:
        workload = row['Workload']
        ipc = float(row['IPC'])
        cycles = int(row['Cycles'])
        cache_hit = float(row['Cache_Hit_Rate'])
        
        print(f"  {workload:15}: IPC={ipc:.4f}, Cycles={cycles:,}, Cache Hit={cache_hit:.1%}")
    
    # Calculate averages
    avg_ipc = sum(float(row['IPC']) for row in data) / len(data)
    print(f"\nAverage IPC across all workloads: {avg_ipc:.4f}")
    
    # Identify best/worst performing workloads
    best = max(data, key=lambda x: float(x['IPC']))
    worst = min(data, key=lambda x: float(x['IPC']))
    print(f"Best performing: {best['Workload']} (IPC={float(best['IPC']):.4f})")
    print(f"Worst performing: {worst['Workload']} (IPC={float(worst['IPC']):.4f})")

def analyze_branch_prediction(data):
    """Analyze branch prediction results"""
    # Group by predictor type
    predictors = {}
    for row in data:
        pred = row['Configuration']
        if pred not in predictors:
            predictors[pred] = []
        predictors[pred].append(row)
    
    print("Branch Prediction Performance Comparison:")
    print("Predictor     | Workload        | IPC    | Branch Acc | Improvement")
    print("-" * 65)
    
    # Calculate baseline (none predictor)
    baseline = {row['Workload']: float(row['IPC']) for row in predictors.get('none', [])}
    
    for pred_type, pred_data in predictors.items():
        for row in pred_data:
            workload = row['Workload']
            ipc = float(row['IPC'])
            branch_acc = float(row['Branch_Accuracy'])
            
            if workload in baseline and baseline[workload] > 0:
                improvement = ((ipc - baseline[workload]) / baseline[workload]) * 100
            else:
                improvement = 0
            
            print(f"{pred_type:12} | {workload:15} | {ipc:.4f} | {branch_acc:.1%}     | {improvement:+6.1f}%")
    
    # Summary statistics
    print("\nBranch Prediction Summary:")
    for pred_type, pred_data in predictors.items():
        avg_ipc = sum(float(row['IPC']) for row in pred_data) / len(pred_data)
        avg_acc = sum(float(row['Branch_Accuracy']) for row in pred_data) / len(pred_data)
        print(f"  {pred_type:12}: Avg IPC={avg_ipc:.4f}, Avg Accuracy={avg_acc:.1%}")

def analyze_superscalar(data):
    """Analyze superscalar scaling results"""
    # Group by issue width
    issue_widths = {}
    for row in data:
        width = row['Configuration']
        if width not in issue_widths:
            issue_widths[width] = []
        issue_widths[width].append(row)
    
    print("Superscalar Scaling Analysis:")
    print("Issue Width | Workload        | IPC    | Efficiency | Scaling Factor")
    print("-" * 70)
    
    # Calculate baseline (1-way)
    baseline = {row['Workload']: float(row['IPC']) for row in issue_widths.get('1way', [])}
    
    for width, width_data in sorted(issue_widths.items(), key=lambda x: int(x[0][0])):
        issue_num = int(width[0])
        
        for row in width_data:
            workload = row['Workload']
            ipc = float(row['IPC'])
            efficiency = (ipc / issue_num) * 100
            
            if workload in baseline and baseline[workload] > 0:
                scaling = ipc / baseline[workload]
            else:
                scaling = 1.0
            
            print(f"{width:11} | {workload:15} | {ipc:.4f} | {efficiency:8.1f}% | {scaling:8.2f}x")
    
    # Scaling efficiency analysis
    print("\nScaling Efficiency Summary:")
    for workload in baseline.keys():
        print(f"\n{workload.upper()} Scaling:")
        for width in sorted(issue_widths.keys(), key=lambda x: int(x[0])):
            workload_data = next((row for row in issue_widths[width] if row['Workload'] == workload), None)
            if workload_data:
                issue_num = int(width[0])
                ipc = float(workload_data['IPC'])
                theoretical_max = issue_num
                efficiency = (ipc / theoretical_max) * 100
                scaling = ipc / baseline[workload] if baseline[workload] > 0 else 1.0
                
                print(f"  {width}: IPC={ipc:.3f}, Efficiency={efficiency:.1f}%, Scaling={scaling:.2f}x")

def generate_insights(csv_path):
    """Generate key insights from the analysis"""
    print("\n" + "="*60)
    print("                    KEY INSIGHTS")
    print("="*60)
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Find best overall performance
    best_overall = max(data, key=lambda x: float(x['IPC']))
    print(f"Best Overall Performance: {float(best_overall['IPC']):.4f} IPC")
    print(f"  Configuration: {best_overall['Experiment']} - {best_overall['Configuration']}")
    print(f"  Workload: {best_overall['Workload']}")
    
    # Branch prediction effectiveness
    bp_data = [row for row in data if row['Experiment'] == 'Branch Prediction']
    if bp_data:
        tournament_data = [row for row in bp_data if row['Configuration'] == 'tournament']
        none_data = [row for row in bp_data if row['Configuration'] == 'none']
        
        if tournament_data and none_data:
            branch_intensive_tournament = next((row for row in tournament_data if row['Workload'] == 'branch_intensive'), None)
            branch_intensive_none = next((row for row in none_data if row['Workload'] == 'branch_intensive'), None)
            
            if branch_intensive_tournament and branch_intensive_none:
                improvement = ((float(branch_intensive_tournament['IPC']) - float(branch_intensive_none['IPC'])) / 
                              float(branch_intensive_none['IPC'])) * 100
                print(f"\nBranch Prediction Impact:")
                print(f"  Tournament vs No Prediction: {improvement:.1f}% IPC improvement")
                print(f"  On branch-intensive workload: {float(branch_intensive_none['IPC']):.3f} → {float(branch_intensive_tournament['IPC']):.3f} IPC")
    
    # Superscalar scaling limits
    ss_data = [row for row in data if row['Experiment'] == 'Superscalar']
    if ss_data:
        parallel_8way = next((row for row in ss_data if row['Configuration'] == '8way' and row['Workload'] == 'parallel_workload'), None)
        if parallel_8way:
            ipc_8way = float(parallel_8way['IPC'])
            efficiency_8way = (ipc_8way / 8) * 100
            print(f"\nSuperscalar Scaling:")
            print(f"  8-way parallel workload: {ipc_8way:.3f} IPC ({efficiency_8way:.1f}% efficiency)")
            print(f"  Diminishing returns evident beyond 4-way issue")
    
    # Workload characteristics
    print(f"\nWorkload Characteristics:")
    workload_performance = {}
    for workload in ['simple_loop', 'branch_intensive', 'parallel_workload']:
        workload_data = [row for row in data if row['Workload'] == workload]
        if workload_data:
            avg_ipc = sum(float(row['IPC']) for row in workload_data) / len(workload_data)
            workload_performance[workload] = avg_ipc
    
    for workload, avg_ipc in sorted(workload_performance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {workload:15}: Average IPC = {avg_ipc:.3f}")

def main():
    """Main analysis function"""
    results_dir = Path("/Users/L040929/Documents/University of Cumberlands/MSCS-531-M50/Assignment-4/Part2-Practical-Exploration/results")
    csv_path = results_dir / "performance_summary.csv"
    
    if not csv_path.exists():
        print(f"Error: Performance summary file not found: {csv_path}")
        return 1
    
    # Run analysis
    analyze_performance_summary(csv_path)
    generate_insights(csv_path)
    
    print("\n" + "="*60)
    print("Analysis complete! Results can be used to populate the final report.")
    print(f"Data source: {csv_path}")
    print("="*60)
    
    return 0

if __name__ == '__main__':
    exit(main())