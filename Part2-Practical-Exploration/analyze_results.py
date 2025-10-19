#!/usr/bin/env python3

"""
gem5 Results Analysis Script
Processes gem5 simulation statistics and generates comparative analysis
"""

import os
import re
import csv
import json
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

class Gem5ResultsAnalyzer:
    def __init__(self, results_base_dir):
        self.results_base_dir = Path(results_base_dir)
        self.experiments = {}
        
    def parse_stats_file(self, stats_path):
        """Parse gem5 stats.txt file and extract key metrics"""
        metrics = {}
        
        if not os.path.exists(stats_path):
            print(f"Warning: Stats file not found: {stats_path}")
            return metrics
            
        with open(stats_path, 'r') as f:
            content = f.read()
            
        # Define patterns for key metrics
        patterns = {
            'sim_seconds': r'sim_seconds\s+([\d\.e\-\+]+)',
            'sim_insts': r'sim_insts\s+(\d+)',
            'host_inst_rate': r'host_inst_rate\s+([\d\.e\-\+]+)',
            'committedInsts': r'system\.cpu\.committedInsts\s+(\d+)',
            'numCycles': r'system\.cpu\.numCycles\s+(\d+)',
            'ipc': r'system\.cpu\.ipc\s+([\d\.e\-\+]+)',
            
            # Branch prediction metrics
            'branch_lookups': r'system\.cpu\.branchPred\.lookups\s+(\d+)',
            'branch_condPredicted': r'system\.cpu\.branchPred\.condPredicted\s+(\d+)',
            'branch_condIncorrect': r'system\.cpu\.branchPred\.condIncorrect\s+(\d+)',
            
            # Cache metrics
            'icache_overall_hits': r'system\.cpu\.icache\.overall_hits::total\s+(\d+)',
            'icache_overall_misses': r'system\.cpu\.icache\.overall_misses::total\s+(\d+)',
            'dcache_overall_hits': r'system\.cpu\.dcache\.overall_hits::total\s+(\d+)',
            'dcache_overall_misses': r'system\.cpu\.dcache\.overall_misses::total\s+(\d+)',
            'l2cache_overall_hits': r'system\.l2cache\.overall_hits::total\s+(\d+)',
            'l2cache_overall_misses': r'system\.l2cache\.overall_misses::total\s+(\d+)',
            
            # O3CPU specific metrics (for superscalar experiments)
            'fetch_rate': r'system\.cpu\.fetch\.rate\s+([\d\.e\-\+]+)',
            'decode_rate': r'system\.cpu\.decode\.rate\s+([\d\.e\-\+]+)',
            'rename_rate': r'system\.cpu\.rename\.rate\s+([\d\.e\-\+]+)',
            'iew_rate': r'system\.cpu\.iew\.rate\s+([\d\.e\-\+]+)',
            'commit_rate': r'system\.cpu\.commit\.rate\s+([\d\.e\-\+]+)',
            
            # ROB and queue occupancy
            'rob_reads': r'system\.cpu\.rob\.reads\s+(\d+)',
            'rob_writes': r'system\.cpu\.rob\.writes\s+(\d+)',
            'iq_reads': r'system\.cpu\.iq\.reads\s+(\d+)',
            'iq_writes': r'system\.cpu\.iq\.writes\s+(\d+)',
        }
        
        for metric, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                try:
                    # Try to convert to appropriate numeric type
                    value = match.group(1)
                    if '.' in value or 'e' in value.lower():
                        metrics[metric] = float(value)
                    else:
                        metrics[metric] = int(value)
                except ValueError:
                    metrics[metric] = value
        
        # Calculate derived metrics
        if 'branch_condPredicted' in metrics and 'branch_condIncorrect' in metrics:
            if metrics['branch_condPredicted'] > 0:
                metrics['branch_accuracy'] = 1.0 - (metrics['branch_condIncorrect'] / metrics['branch_condPredicted'])
            else:
                metrics['branch_accuracy'] = 0.0
                
        # Cache hit rates
        for cache in ['icache', 'dcache', 'l2cache']:
            hits_key = f'{cache}_overall_hits'
            misses_key = f'{cache}_overall_misses'
            if hits_key in metrics and misses_key in metrics:
                total_accesses = metrics[hits_key] + metrics[misses_key]
                if total_accesses > 0:
                    metrics[f'{cache}_hit_rate'] = metrics[hits_key] / total_accesses
                else:
                    metrics[f'{cache}_hit_rate'] = 0.0
        
        return metrics
    
    def load_experiment_results(self):
        """Load results from all experiment directories"""
        experiment_dirs = [
            'basic_pipeline',
            'branch_prediction', 
            'superscalar',
            'smt'  # If implemented
        ]
        
        for exp_dir in experiment_dirs:
            exp_path = self.results_base_dir / exp_dir
            if exp_path.exists():
                self.experiments[exp_dir] = self.load_experiment_data(exp_path)
    
    def load_experiment_data(self, exp_path):
        """Load data for a specific experiment"""
        experiment_data = {}
        
        for workload_dir in exp_path.iterdir():
            if workload_dir.is_dir():
                stats_file = workload_dir / 'stats.txt'
                config_file = workload_dir / 'config.ini'
                
                workload_name = workload_dir.name
                experiment_data[workload_name] = {
                    'stats': self.parse_stats_file(stats_file),
                    'config_path': str(config_file) if config_file.exists() else None
                }
        
        return experiment_data
    
    def generate_performance_comparison(self):
        """Generate performance comparison across all experiments"""
        print("\n=== Performance Comparison Analysis ===")
        
        # Create comparison table
        comparison_data = []
        
        for exp_name, exp_data in self.experiments.items():
            for workload, data in exp_data.items():
                stats = data['stats']
                row = {
                    'experiment': exp_name,
                    'workload': workload,
                    'ipc': stats.get('ipc', 0),
                    'sim_seconds': stats.get('sim_seconds', 0),
                    'committedInsts': stats.get('committedInsts', 0),
                    'branch_accuracy': stats.get('branch_accuracy', 0),
                    'dcache_hit_rate': stats.get('dcache_hit_rate', 0),
                    'l2cache_hit_rate': stats.get('l2cache_hit_rate', 0)
                }
                comparison_data.append(row)
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(comparison_data)
        
        if not df.empty:
            print("\nPerformance Summary:")
            print(df.to_string(index=False, float_format='%.4f'))
            
            # Save to CSV
            csv_path = self.results_base_dir / 'performance_comparison.csv'
            df.to_csv(csv_path, index=False, float_format='%.6f')
            print(f"\nDetailed results saved to: {csv_path}")
            
            return df
        else:
            print("No experiment data found!")
            return None
    
    def plot_ipc_comparison(self, df):
        """Create IPC comparison plots"""
        if df is None or df.empty:
            return
            
        # IPC by workload and experiment
        plt.figure(figsize=(12, 6))
        
        workloads = df['workload'].unique()
        experiments = df['experiment'].unique()
        
        x_pos = range(len(workloads))
        width = 0.8 / len(experiments)
        
        for i, exp in enumerate(experiments):
            exp_data = df[df['experiment'] == exp]
            ipc_values = [exp_data[exp_data['workload'] == w]['ipc'].iloc[0] 
                         if not exp_data[exp_data['workload'] == w].empty else 0 
                         for w in workloads]
            
            plt.bar([x + i * width for x in x_pos], ipc_values, 
                   width, label=exp, alpha=0.8)
        
        plt.xlabel('Workload')
        plt.ylabel('Instructions Per Cycle (IPC)')
        plt.title('IPC Comparison Across Experiments and Workloads')
        plt.xticks([x + width * (len(experiments) - 1) / 2 for x in x_pos], workloads)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plot_path = self.results_base_dir / 'ipc_comparison.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"IPC comparison plot saved to: {plot_path}")
    
    def analyze_branch_prediction_impact(self):
        """Analyze branch prediction effectiveness"""
        if 'branch_prediction' not in self.experiments:
            print("Branch prediction experiment data not found")
            return
            
        print("\n=== Branch Prediction Analysis ===")
        
        bp_data = self.experiments['branch_prediction']
        
        for workload, data in bp_data.items():
            stats = data['stats']
            print(f"\n{workload.upper()}:")
            print(f"  IPC: {stats.get('ipc', 0):.4f}")
            print(f"  Branch Accuracy: {stats.get('branch_accuracy', 0):.4f}")
            print(f"  Branch Lookups: {stats.get('branch_lookups', 0)}")
            print(f"  Branch Mispredictions: {stats.get('branch_condIncorrect', 0)}")
    
    def analyze_superscalar_scaling(self):
        """Analyze superscalar performance scaling"""
        if 'superscalar' not in self.experiments:
            print("Superscalar experiment data not found")
            return
            
        print("\n=== Superscalar Scaling Analysis ===")
        
        ss_data = self.experiments['superscalar']
        
        for workload, data in ss_data.items():
            stats = data['stats']
            print(f"\n{workload.upper()}:")
            print(f"  IPC: {stats.get('ipc', 0):.4f}")
            print(f"  Fetch Rate: {stats.get('fetch_rate', 0):.4f}")
            print(f"  Decode Rate: {stats.get('decode_rate', 0):.4f}")
            print(f"  Commit Rate: {stats.get('commit_rate', 0):.4f}")
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "="*60)
        print("           GEM5 ILP EXPERIMENT SUMMARY REPORT")
        print("="*60)
        
        # Load all experiment data
        self.load_experiment_results()
        
        # Generate performance comparison
        df = self.generate_performance_comparison()
        
        # Create plots
        if df is not None:
            self.plot_ipc_comparison(df)
        
        # Specific analyses
        self.analyze_branch_prediction_impact()
        self.analyze_superscalar_scaling()
        
        # Key insights
        print("\n=== Key Insights ===")
        if df is not None and not df.empty:
            # Find best performing configurations
            best_ipc = df.loc[df['ipc'].idxmax()]
            print(f"Best IPC: {best_ipc['ipc']:.4f} ({best_ipc['experiment']} - {best_ipc['workload']})")
            
            # IPC by workload type
            workload_avg = df.groupby('workload')['ipc'].mean()
            print(f"\nAverage IPC by workload:")
            for workload, avg_ipc in workload_avg.items():
                print(f"  {workload}: {avg_ipc:.4f}")
                
            # IPC by experiment type  
            exp_avg = df.groupby('experiment')['ipc'].mean()
            print(f"\nAverage IPC by experiment:")
            for experiment, avg_ipc in exp_avg.items():
                print(f"  {experiment}: {avg_ipc:.4f}")
        
        print("\n" + "="*60)
        print("Analysis complete! Check the results directory for detailed outputs.")

def main():
    parser = argparse.ArgumentParser(description='Analyze gem5 ILP experiment results')
    parser.add_argument('results_dir', 
                       help='Base directory containing experiment results')
    parser.add_argument('--output-format', choices=['console', 'html', 'pdf'], 
                       default='console', help='Output format for report')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.results_dir):
        print(f"Error: Results directory not found: {args.results_dir}")
        return 1
    
    # Create analyzer and generate report
    analyzer = Gem5ResultsAnalyzer(args.results_dir)
    analyzer.generate_summary_report()
    
    return 0

if __name__ == '__main__':
    exit(main())