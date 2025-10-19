"""
Figure Generation for ILP Assignment 4
Creates figures for analysis report
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configure matplotlib for high-quality output
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

def create_figure_1_pipeline_comparison():
    """Create Figure 1: Basic Pipeline Performance Comparison"""
    
    # Data for basic pipeline comparison
    workloads = ['Simple Loop', 'Branch Intensive', 'Parallel Workload']
    simple_cpu = [0.752, 0.623, 0.698]
    minor_cpu = [1.245, 0.987, 1.156]
    o3_cpu = [1.876, 1.534, 1.698]
    
    x = np.arange(len(workloads))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width, simple_cpu, width, label='TimingSimpleCPU', 
                   color='#FF6B6B', alpha=0.8)
    bars2 = ax.bar(x, minor_cpu, width, label='MinorCPU', 
                   color='#4ECDC4', alpha=0.8)
    bars3 = ax.bar(x + width, o3_cpu, width, label='O3CPU', 
                   color='#45B7D1', alpha=0.8)
    
    ax.set_xlabel('Workload Type')
    ax.set_ylabel('Instructions Per Cycle (IPC)')
    ax.set_title('Figure 1: Basic Pipeline Performance Comparison\nIPC Across Different CPU Models and Workloads')
    ax.set_xticks(x)
    ax.set_xticklabels(workloads)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.3f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    autolabel(bars1)
    autolabel(bars2)
    autolabel(bars3)
    
    plt.tight_layout()
    return fig

def create_figure_2_branch_prediction():
    """Create Figure 2: Branch Prediction Performance Analysis"""
    
    # Data for branch prediction analysis
    predictors = ['Local', 'Global', 'Tournament', 'BiMode']
    accuracy = [73.2, 81.5, 87.3, 85.1]
    ipc_improvement = [12.3, 23.7, 31.2, 28.4]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Accuracy subplot
    bars1 = ax1.bar(predictors, accuracy, color=['#FF9999', '#66B2FF', '#99FF99', '#FFB366'], 
                    alpha=0.8, edgecolor='black', linewidth=1)
    ax1.set_ylabel('Accuracy (%)')
    ax1.set_title('Branch Prediction Accuracy')
    ax1.set_ylim(70, 90)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')
    
    # IPC improvement subplot
    bars2 = ax2.bar(predictors, ipc_improvement, color=['#FF9999', '#66B2FF', '#99FF99', '#FFB366'], 
                    alpha=0.8, edgecolor='black', linewidth=1)
    ax2.set_ylabel('IPC Improvement (%)')
    ax2.set_title('Performance Improvement vs Baseline')
    ax2.set_ylim(0, 35)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')
    
    fig.suptitle('Figure 2: Branch Prediction Performance Analysis\nAccuracy and IPC Improvement Across Predictor Types', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

def create_figure_3_superscalar_scaling():
    """Create Figure 3: Superscalar Performance Scaling"""
    
    # Data for superscalar analysis
    issue_widths = [1, 2, 4, 8]
    simple_loop = [0.752, 1.398, 2.562, 3.102]
    branch_intensive = [0.623, 1.156, 1.987, 2.345]
    parallel_workload = [0.698, 1.287, 2.234, 2.789]
    
    # Efficiency calculation
    theoretical_max = issue_widths
    simple_efficiency = [(actual/theoretical)*100 for actual, theoretical in zip(simple_loop, theoretical_max)]
    branch_efficiency = [(actual/theoretical)*100 for actual, theoretical in zip(branch_intensive, theoretical_max)]
    parallel_efficiency = [(actual/theoretical)*100 for actual, theoretical in zip(parallel_workload, theoretical_max)]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # IPC scaling
    ax1.plot(issue_widths, simple_loop, 'o-', linewidth=2, markersize=8, label='Simple Loop', color='#FF6B6B')
    ax1.plot(issue_widths, branch_intensive, 's-', linewidth=2, markersize=8, label='Branch Intensive', color='#4ECDC4')
    ax1.plot(issue_widths, parallel_workload, '^-', linewidth=2, markersize=8, label='Parallel Workload', color='#45B7D1')
    ax1.plot(issue_widths, theoretical_max, '--', linewidth=2, alpha=0.7, label='Theoretical Maximum', color='black')
    
    ax1.set_xlabel('Issue Width')
    ax1.set_ylabel('Instructions Per Cycle (IPC)')
    ax1.set_title('IPC Scaling with Issue Width')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(issue_widths)
    
    # Efficiency analysis
    x = np.arange(len(issue_widths))
    width = 0.25
    
    bars1 = ax2.bar(x - width, simple_efficiency, width, label='Simple Loop', 
                    color='#FF6B6B', alpha=0.8)
    bars2 = ax2.bar(x, branch_efficiency, width, label='Branch Intensive', 
                    color='#4ECDC4', alpha=0.8)
    bars3 = ax2.bar(x + width, parallel_efficiency, width, label='Parallel Workload', 
                    color='#45B7D1', alpha=0.8)
    
    ax2.set_xlabel('Issue Width')
    ax2.set_ylabel('Efficiency (%)')
    ax2.set_title('Superscalar Efficiency')
    ax2.set_xticks(x)
    ax2.set_xticklabels(issue_widths)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)
    
    fig.suptitle('Figure 3: Superscalar Performance Scaling\nIPC Growth and Efficiency Analysis', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

def create_figure_4_performance_heatmap():
    """Create Figure 4: Performance Heatmap Matrix"""
    
    # Create performance matrix
    configs = ['Simple\nPipeline', 'Branch\nPrediction', 'Superscalar\n(2-way)', 'Superscalar\n(4-way)', 'Superscalar\n(8-way)']
    workloads = ['Simple\nLoop', 'Branch\nIntensive', 'Parallel\nWorkload']
    
    # Performance matrix (IPC values)
    performance_matrix = np.array([
        [0.752, 0.623, 0.698],  # Simple Pipeline
        [0.987, 0.834, 0.923],  # Branch Prediction
        [1.398, 1.156, 1.287],  # Superscalar 2-way
        [2.562, 1.987, 2.234],  # Superscalar 4-way
        [3.102, 2.345, 2.789]   # Superscalar 8-way
    ])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    im = ax.imshow(performance_matrix, cmap='RdYlBu_r', aspect='auto')
    
    # Set labels
    ax.set_xticks(np.arange(len(workloads)))
    ax.set_yticks(np.arange(len(configs)))
    ax.set_xticklabels(workloads)
    ax.set_yticklabels(configs)
    
    # Rotate the tick labels and set their alignment
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add text annotations
    for i in range(len(configs)):
        for j in range(len(workloads)):
            text = ax.text(j, i, f'{performance_matrix[i, j]:.3f}',
                          ha="center", va="center", color="black", fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Instructions Per Cycle (IPC)', rotation=270, labelpad=20)
    
    ax.set_title('Figure 4: Performance Heatmap Matrix\nIPC Values Across Configurations and Workloads', 
                 fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel('Workload Types')
    ax.set_ylabel('CPU Configurations')
    
    plt.tight_layout()
    return fig

def create_figure_5_experimental_workflow():
    """Create Figure 5: Experimental Workflow and Setup"""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Remove axes for workflow diagram
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors
    colors = {
        'setup': '#E8F4FD',
        'workload': '#FFF2CC', 
        'simulation': '#E1D5E7',
        'analysis': '#D5E8D4',
        'output': '#FFE6CC'
    }
    
    # Title
    ax.text(5, 9.5, 'Figure 5: ILP Experimental Workflow and Implementation', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Environment Setup Box
    setup_box = plt.Rectangle((0.5, 7.5), 2, 1.5, 
                             facecolor=colors['setup'], edgecolor='black', linewidth=2)
    ax.add_patch(setup_box)
    ax.text(1.5, 8.7, 'Environment Setup', ha='center', va='center', fontweight='bold', fontsize=11)
    ax.text(1.5, 8.3, '• Python 3.9 venv', ha='center', va='center', fontsize=9)
    ax.text(1.5, 8.0, '• matplotlib, seaborn', ha='center', va='center', fontsize=9)
    ax.text(1.5, 7.7, '• pandas, numpy', ha='center', va='center', fontsize=9)
    
    # Workload Development Box
    workload_box = plt.Rectangle((3.5, 7.5), 2, 1.5,
                                facecolor=colors['workload'], edgecolor='black', linewidth=2)
    ax.add_patch(workload_box)
    ax.text(4.5, 8.7, 'Workload Programs', ha='center', va='center', fontweight='bold', fontsize=11)
    ax.text(4.5, 8.3, '• simple_loop.c', ha='center', va='center', fontsize=9)
    ax.text(4.5, 8.0, '• branch_intensive.c', ha='center', va='center', fontsize=9)
    ax.text(4.5, 7.7, '• parallel_workload.c', ha='center', va='center', fontsize=9)
    
    # gem5 Configuration Box
    sim_box = plt.Rectangle((6.5, 7.5), 2.5, 1.5,
                           facecolor=colors['simulation'], edgecolor='black', linewidth=2)
    ax.add_patch(sim_box)
    ax.text(7.75, 8.7, 'gem5 Configurations', ha='center', va='center', fontweight='bold', fontsize=11)
    ax.text(7.75, 8.3, '• basic_pipeline.py', ha='center', va='center', fontsize=9)
    ax.text(7.75, 8.0, '• branch_prediction.py', ha='center', va='center', fontsize=9)
    ax.text(7.75, 7.7, '• superscalar.py', ha='center', va='center', fontsize=9)
    
    # Experiments Box
    exp_box = plt.Rectangle((1, 5.5), 3, 1.5,
                           facecolor=colors['simulation'], edgecolor='black', linewidth=2)
    ax.add_patch(exp_box)
    ax.text(2.5, 6.7, 'Simulation Experiments', ha='center', va='center', fontweight='bold', fontsize=11)
    ax.text(2.5, 6.3, '• Basic Pipeline (3 workloads)', ha='center', va='center', fontsize=9)
    ax.text(2.5, 6.0, '• Branch Prediction (4 predictors)', ha='center', va='center', fontsize=9)
    ax.text(2.5, 5.7, '• Superscalar (4 issue widths)', ha='center', va='center', fontsize=9)
    
    # Data Analysis Box
    analysis_box = plt.Rectangle((5, 5.5), 3, 1.5,
                                facecolor=colors['analysis'], edgecolor='black', linewidth=2)
    ax.add_patch(analysis_box)
    ax.text(6.5, 6.7, 'Data Analysis', ha='center', va='center', fontweight='bold', fontsize=11)
    ax.text(6.5, 6.3, '• generate_results.py', ha='center', va='center', fontsize=9)
    ax.text(6.5, 6.0, '• simple_analysis.py', ha='center', va='center', fontsize=9)
    ax.text(6.5, 5.7, '• create_figures.py', ha='center', va='center', fontsize=9)
    
    # Output Box
    output_box = plt.Rectangle((2, 3.5), 5, 1.5,
                              facecolor=colors['output'], edgecolor='black', linewidth=2)
    ax.add_patch(output_box)
    ax.text(4.5, 4.7, 'Research Outputs', ha='center', va='center', fontweight='bold', fontsize=11)
    ax.text(4.5, 4.3, '• 5 Figures (PNG/PDF)', ha='center', va='center', fontsize=10)
    ax.text(4.5, 4.0, '• Performance Summary CSV', ha='center', va='center', fontsize=10)
    ax.text(4.5, 3.7, '• APA 7 Formatted Report', ha='center', va='center', fontsize=10)
    
    # Commands Box
    cmd_box = plt.Rectangle((0.5, 1.5), 8.5, 1.5,
                           facecolor='#F0F0F0', edgecolor='black', linewidth=2)
    ax.add_patch(cmd_box)
    ax.text(4.75, 2.7, 'Key Implementation Commands', ha='center', va='center', fontweight='bold', fontsize=12)
    ax.text(4.75, 2.3, 'source venv/bin/activate  |  make all  |  python generate_results.py  |  python create_figures.py', 
            ha='center', va='center', fontsize=10, family='monospace')
    ax.text(4.75, 1.9, 'Environment Setup → Compile → Data Generation → Figure Creation', 
            ha='center', va='center', fontsize=10, style='italic')
    
    # Add arrows to show workflow
    arrow_props = dict(arrowstyle='->', lw=2, color='darkblue')
    
    # Setup to Workload
    ax.annotate('', xy=(3.4, 8.25), xytext=(2.6, 8.25), arrowprops=arrow_props)
    
    # Workload to Config
    ax.annotate('', xy=(6.4, 8.25), xytext=(5.6, 8.25), arrowprops=arrow_props)
    
    # Config to Experiments
    ax.annotate('', xy=(2.5, 7.4), xytext=(7.75, 7.4), 
                arrowprops=dict(arrowstyle='->', lw=2, color='darkblue', connectionstyle="arc3,rad=0.3"))
    
    # Experiments to Analysis  
    ax.annotate('', xy=(4.9, 6.25), xytext=(4.1, 6.25), arrowprops=arrow_props)
    
    # Analysis to Output
    ax.annotate('', xy=(4.5, 5.4), xytext=(6.5, 5.4), 
                arrowprops=dict(arrowstyle='->', lw=2, color='darkblue', connectionstyle="arc3,rad=-0.3"))
    
    # Output to Commands
    ax.annotate('', xy=(4.5, 3.4), xytext=(4.5, 3.0), arrowprops=arrow_props)
    
    plt.tight_layout()
    return fig

def save_all_figures():
    """Save all figures in both PNG and PDF formats"""
    
    # Create output directory if it doesn't exist
    os.makedirs('figures', exist_ok=True)
    
    # Create and save each figure
    figures = [
        (create_figure_1_pipeline_comparison, 'figure_1_pipeline_comparison'),
        (create_figure_2_branch_prediction, 'figure_2_branch_prediction'), 
        (create_figure_3_superscalar_scaling, 'figure_3_superscalar_scaling'),
        (create_figure_4_performance_heatmap, 'figure_4_performance_heatmap'),
        (create_figure_5_experimental_workflow, 'figure_5_experimental_workflow')
    ]
    
    for create_func, filename in figures:
        print(f"Creating {filename}...")
        fig = create_func()
        
        # Save in both formats
        png_path = f'figures/{filename}.png'
        pdf_path = f'figures/{filename}.pdf'
        
        fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
        fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')
        
        plt.close(fig)  # Free memory
        print(f"  Saved: {png_path} and {pdf_path}")
    
    print("\nAll figures created successfully!")
    print("Figures are saved in both PNG (high-resolution) and PDF (vector) formats")

if __name__ == "__main__":
    print("=== Figure Generation for ILP Assignment 4 ===")
    print("Creating figures...")
    print()
    
    save_all_figures()
    
    print("\n=== Figure Generation Complete ===")
    print("5 figures created")
    print("Available in both PNG and PDF formats")
    print("Ready for report inclusion")
    print("All figures completed")