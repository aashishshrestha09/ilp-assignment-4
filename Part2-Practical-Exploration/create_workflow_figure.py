#!/usr/bin/env python3
"""
Create Figure 5: Experimental Workflow
Diagram showing methodology from setup through analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Arrow
import numpy as np
import os

# Set up styling
plt.style.use('default')
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 10,
    'axes.linewidth': 1.2,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'text.color': 'black',
    'axes.edgecolor': 'black'
})

def create_experimental_workflow_figure():
    """Create Figure 5: Experimental Workflow"""
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Define colors for different phases
    colors = {
        'setup': '#E8F4FD',      # Light blue
        'config': '#FFF2CC',     # Light yellow
        'execution': '#E1F5FE',  # Light cyan
        'analysis': '#F3E5F5',   # Light purple
        'output': '#E8F5E8',     # Light green
        'border': '#1976D2',     # Dark blue
        'accent': '#FF6B35',     # Orange accent
        'text': '#333333'        # Dark gray text
    }
    
    # Title
    ax.text(50, 95, 'Experimental Workflow and Implementation', 
            ha='center', va='center', fontsize=16, weight='bold', color=colors['text'])
    ax.text(50, 92, 'Complete ILP Study Methodology: Environment Setup → Analysis → Visualization', 
            ha='center', va='center', fontsize=12, style='italic', color=colors['text'])
    
    # Phase 1: Environment Setup
    phase1_box = FancyBboxPatch((2, 75), 18, 15, 
                               boxstyle="round,pad=0.5", 
                               facecolor=colors['setup'], 
                               edgecolor=colors['border'], 
                               linewidth=2)
    ax.add_patch(phase1_box)
    
    ax.text(11, 87, 'Phase 1: Environment Setup', 
            ha='center', va='center', fontsize=11, weight='bold', color=colors['text'])
    
    setup_steps = [
        '• Python 3.9 Virtual Environment',
        '• Install Dependencies',
        '• gem5 Simulator Setup',
        '• Workspace Configuration'
    ]
    
    for i, step in enumerate(setup_steps):
        ax.text(3, 84 - i*2, step, ha='left', va='center', fontsize=9, color=colors['text'])
    
    # Phase 2: Configuration & Workloads
    phase2_box = FancyBboxPatch((25, 75), 25, 15, 
                               boxstyle="round,pad=0.5", 
                               facecolor=colors['config'], 
                               edgecolor=colors['border'], 
                               linewidth=2)
    ax.add_patch(phase2_box)
    
    ax.text(37.5, 87, 'Phase 2: Configuration & Workloads', 
            ha='center', va='center', fontsize=11, weight='bold', color=colors['text'])
    
    # Configuration sub-boxes
    config_boxes = [
        ('Basic Pipeline\nTimingSimpleCPU', 26, 82, '#FFE0B2'),
        ('Branch Prediction\nTournament/Local', 33, 82, '#F8BBD9'),
        ('Superscalar\nO3CPU 1-8 way', 40, 82, '#D1C4E9'),
        ('Workloads\nLoop/Branch/Parallel', 47, 82, '#DCEDC8')
    ]
    
    for label, x, y, color in config_boxes:
        box = FancyBboxPatch((x-2, y-2), 6, 4, 
                            boxstyle="round,pad=0.2", 
                            facecolor=color, 
                            edgecolor=colors['border'], 
                            linewidth=1)
        ax.add_patch(box)
        ax.text(x+1, y, label, ha='center', va='center', fontsize=8, color=colors['text'])
    
    # Phase 3: Simulation Execution
    phase3_box = FancyBboxPatch((55, 75), 20, 15, 
                               boxstyle="round,pad=0.5", 
                               facecolor=colors['execution'], 
                               edgecolor=colors['border'], 
                               linewidth=2)
    ax.add_patch(phase3_box)
    
    ax.text(65, 87, 'Phase 3: Simulation Execution', 
            ha='center', va='center', fontsize=11, weight='bold', color=colors['text'])
    
    execution_steps = [
        '• gem5 Simulation Runs',
        '• Performance Data Collection',
        '• Statistics Generation',
        '• Results Validation'
    ]
    
    for i, step in enumerate(execution_steps):
        ax.text(56, 84 - i*2, step, ha='left', va='center', fontsize=9, color=colors['text'])
    
    # Phase 4: Data Analysis
    phase4_box = FancyBboxPatch((80, 75), 18, 15, 
                               boxstyle="round,pad=0.5", 
                               facecolor=colors['analysis'], 
                               edgecolor=colors['border'], 
                               linewidth=2)
    ax.add_patch(phase4_box)
    
    ax.text(89, 87, 'Phase 4: Data Analysis', 
            ha='center', va='center', fontsize=11, weight='bold', color=colors['text'])
    
    analysis_steps = [
        '• Performance Metrics',
        '• Statistical Analysis',
        '• Comparative Studies',
        '• Trend Identification'
    ]
    
    for i, step in enumerate(analysis_steps):
        ax.text(81, 84 - i*2, step, ha='left', va='center', fontsize=9, color=colors['text'])
    
    # Detailed Workflow Components
    
    # Workload Development Section
    workload_box = FancyBboxPatch((2, 50), 30, 20, 
                                 boxstyle="round,pad=0.5", 
                                 facecolor='#FFF8E1', 
                                 edgecolor=colors['border'], 
                                 linewidth=2)
    ax.add_patch(workload_box)
    
    ax.text(17, 67, 'Workload Development & Compilation', 
            ha='center', va='center', fontsize=12, weight='bold', color=colors['text'])
    
    # Individual workload boxes
    workloads = [
        ('Simple Loop\n• Arithmetic operations\n• Moderate ILP\n• Regular control flow', 4, 58, '#E3F2FD'),
        ('Branch Intensive\n• Unpredictable branches\n• Control dependencies\n• Low ILP potential', 13, 58, '#FCE4EC'),
        ('Parallel Workload\n• Independent operations\n• High ILP potential\n• Unrolled loops', 22, 58, '#E8F5E8')
    ]
    
    for label, x, y, color in workloads:
        box = FancyBboxPatch((x, y-4), 8, 8, 
                            boxstyle="round,pad=0.3", 
                            facecolor=color, 
                            edgecolor=colors['border'], 
                            linewidth=1)
        ax.add_patch(box)
        ax.text(x+4, y, label, ha='center', va='center', fontsize=8, color=colors['text'])
    
    # gem5 Configuration Matrix
    config_box = FancyBboxPatch((35, 50), 30, 20, 
                               boxstyle="round,pad=0.5", 
                               facecolor='#F3E5F5', 
                               edgecolor=colors['border'], 
                               linewidth=2)
    ax.add_patch(config_box)
    
    ax.text(50, 67, 'gem5 Configuration Matrix', 
            ha='center', va='center', fontsize=12, weight='bold', color=colors['text'])
    
    # Configuration matrix
    configs = [
        ('Basic Pipeline', 'TimingSimpleCPU\n5-stage pipeline\n1 GHz frequency', 37, 61),
        ('Branch Prediction', 'Tournament/Local\nPrediction accuracy\nMiss penalty analysis', 50, 61),
        ('Superscalar', 'O3CPU Model\n1-8 way issue\nResource utilization', 37, 54),
        ('Cache Hierarchy', 'L1: 16KB I-cache\nL1: 64KB D-cache\nL2: 256KB unified', 50, 54)
    ]
    
    for title, desc, x, y in configs:
        box = FancyBboxPatch((x, y-2), 11, 5, 
                            boxstyle="round,pad=0.2", 
                            facecolor='#FFFFFF', 
                            edgecolor=colors['border'], 
                            linewidth=1)
        ax.add_patch(box)
        ax.text(x+0.5, y+1.5, title, ha='left', va='center', fontsize=9, weight='bold', color=colors['text'])
        ax.text(x+0.5, y-0.5, desc, ha='left', va='center', fontsize=7, color=colors['text'])
    
    # Results & Visualization Section
    results_box = FancyBboxPatch((68, 50), 30, 20, 
                                boxstyle="round,pad=0.5", 
                                facecolor=colors['output'], 
                                edgecolor=colors['border'], 
                                linewidth=2)
    ax.add_patch(results_box)
    
    ax.text(83, 67, 'Results & Visualization Pipeline', 
            ha='center', va='center', fontsize=12, weight='bold', color=colors['text'])
    
    # Results components
    results = [
        ('Performance\nMetrics', 'IPC Analysis\nScaling Factors\nEfficiency Ratios', 70, 61),
        ('Statistical\nValidation', 'Multiple Runs\nConfidence Intervals\nSignificance Tests', 83, 61),
        ('Figure\nGeneration', 'Charts\nComparative Analysis\nTrend Visualization', 70, 54),
        ('Report\nIntegration', 'Academic Format\nAPA Citations\nReproducibility', 83, 54)
    ]
    
    for title, desc, x, y in results:
        box = FancyBboxPatch((x, y-2), 11, 5, 
                            boxstyle="round,pad=0.2", 
                            facecolor='#FFFFFF', 
                            edgecolor=colors['border'], 
                            linewidth=1)
        ax.add_patch(box)
        ax.text(x+0.5, y+1.5, title, ha='left', va='center', fontsize=9, weight='bold', color=colors['text'])
        ax.text(x+0.5, y-0.5, desc, ha='left', va='center', fontsize=7, color=colors['text'])
    
    # Data Flow Arrows
    arrow_props = dict(arrowstyle='->', lw=2, color=colors['accent'])
    
    # Horizontal flow arrows
    ax.annotate('', xy=(24, 82.5), xytext=(20, 82.5), arrowprops=arrow_props)
    ax.annotate('', xy=(54, 82.5), xytext=(50, 82.5), arrowprops=arrow_props)
    ax.annotate('', xy=(79, 82.5), xytext=(75, 82.5), arrowprops=arrow_props)
    
    # Vertical flow arrows
    ax.annotate('', xy=(17, 70), xytext=(17, 73), arrowprops=arrow_props)
    ax.annotate('', xy=(50, 70), xytext=(50, 73), arrowprops=arrow_props)
    ax.annotate('', xy=(83, 70), xytext=(83, 73), arrowprops=arrow_props)
    
    # Performance Metrics Section
    metrics_box = FancyBboxPatch((2, 25), 45, 20, 
                                boxstyle="round,pad=0.5", 
                                facecolor='#FFF3E0', 
                                edgecolor=colors['border'], 
                                linewidth=2)
    ax.add_patch(metrics_box)
    
    ax.text(24.5, 42, 'Key Performance Metrics & Analysis Methods', 
            ha='center', va='center', fontsize=12, weight='bold', color=colors['text'])
    
    # Metrics grid
    metrics = [
        ('Instructions Per Cycle (IPC)', 'Primary performance indicator\nRatio of committed instructions to cycles', 4, 37),
        ('Branch Prediction Accuracy', 'Percentage of correct predictions\nMiss penalty quantification', 25, 37),
        ('Resource Utilization', 'Functional unit occupancy\nPipeline stage efficiency', 4, 30),
        ('Cache Performance', 'Hit rates and access latencies\nMemory hierarchy analysis', 25, 30)
    ]
    
    for title, desc, x, y in metrics:
        box = FancyBboxPatch((x, y-2), 20, 5, 
                            boxstyle="round,pad=0.3", 
                            facecolor='#FFFFFF', 
                            edgecolor=colors['border'], 
                            linewidth=1)
        ax.add_patch(box)
        ax.text(x+1, y+1, title, ha='left', va='center', fontsize=9, weight='bold', color=colors['text'])
        ax.text(x+1, y-0.8, desc, ha='left', va='center', fontsize=8, color=colors['text'])
    
    # Tools & Technologies Section
    tools_box = FancyBboxPatch((50, 25), 48, 20, 
                              boxstyle="round,pad=0.5", 
                              facecolor='#F1F8E9', 
                              edgecolor=colors['border'], 
                              linewidth=2)
    ax.add_patch(tools_box)
    
    ax.text(74, 42, 'Tools & Technologies Used', 
            ha='center', va='center', fontsize=12, weight='bold', color=colors['text'])
    
    # Tools grid
    tools = [
        ('gem5 Simulator', 'v24.0.0.0\nArchitectural modeling\nPerformance simulation', 52, 37),
        ('Python Ecosystem', 'matplotlib, pandas, numpy\nData analysis & visualization\nStatistical computing', 73, 37),
        ('Development Environment', 'macOS with Apple Silicon\nPython 3.9 virtual environment\nGCC compiler toolchain', 52, 30),
        ('Version Control', 'Git repository management\nExperimental reproducibility\nCode documentation', 73, 30)
    ]
    
    for title, desc, x, y in tools:
        box = FancyBboxPatch((x, y-2), 20, 5, 
                            boxstyle="round,pad=0.3", 
                            facecolor='#FFFFFF', 
                            edgecolor=colors['border'], 
                            linewidth=1)
        ax.add_patch(box)
        ax.text(x+1, y+1, title, ha='left', va='center', fontsize=9, weight='bold', color=colors['text'])
        ax.text(x+1, y-0.8, desc, ha='left', va='center', fontsize=8, color=colors['text'])
    
    # Validation & Quality Assurance
    qa_box = FancyBboxPatch((2, 2), 96, 18, 
                           boxstyle="round,pad=0.5", 
                           facecolor='#FFEBEE', 
                           edgecolor=colors['border'], 
                           linewidth=2)
    ax.add_patch(qa_box)
    
    ax.text(50, 17, 'Validation & Quality Assurance Framework', 
            ha='center', va='center', fontsize=12, weight='bold', color=colors['text'])
    
    # QA components
    qa_items = [
        ('Experimental Design', '• Controlled variables\n• Systematic parameter variation\n• Baseline comparisons', 8, 12),
        ('Data Validation', '• Multiple simulation runs\n• Statistical significance testing\n• Consistency checks', 28, 12),
        ('Reproducibility', '• Complete configuration documentation\n• Version-controlled source code\n• Automated build scripts', 48, 12),
        ('Academic Standards', '• APA 7 formatting compliance\n• Peer-reviewed methodology\n• Comprehensive documentation', 68, 12),
        ('Results Verification', '• Cross-validation with literature\n• Sanity check against theory\n• Performance trend analysis', 88, 12)
    ]
    
    for title, items, x, y in qa_items:
        box = FancyBboxPatch((x-3, y-3), 18, 8, 
                            boxstyle="round,pad=0.3", 
                            facecolor='#FFFFFF', 
                            edgecolor=colors['border'], 
                            linewidth=1)
        ax.add_patch(box)
        ax.text(x, y+2, title, ha='center', va='center', fontsize=9, weight='bold', color=colors['text'])
        ax.text(x-2, y-1, items, ha='left', va='center', fontsize=7, color=colors['text'])
    
    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/figure_5_experimental_workflow.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("Figure 5: Experimental Workflow created successfully!")
    print("Saved as: figures/figure_5_experimental_workflow.png")
    print("Workflow diagram ready!")

def main():
    """Generate experimental workflow figure"""
    print("Creating Experimental Workflow Figure...")
    print("=" * 60)
    
    create_experimental_workflow_figure()
    
    print("\nFigure 5 Complete!")
    print("Features:")
    print("   • Workflow visualization")
    print("   • Academic styling") 
    print("   • Methodology documentation")
    print("   • Phase separation and data flow")
    print("   • Quality assurance framework")
    print("   • Tools and technologies overview")
    print("\nReady for report integration!")

if __name__ == '__main__':
    main()