#!/usr/bin/env python3

"""
Superscalar (Multiple Issue) Configuration for gem5 ILP Experiments
This configuration creates an out-of-order superscalar processor
that can issue multiple instructions per cycle
"""

import argparse
import sys
import os

# Add gem5 path if not in system path
gem5_path = os.path.dirname(os.path.abspath(__file__)) + '/../gem5'
sys.path.append(gem5_path + '/configs/')
sys.path.append(gem5_path + '/configs/common')

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal, warn

def create_superscalar_system(issue_width=4, rob_size=192):
    """Create an out-of-order superscalar processor system"""
    
    # Create the system
    system = System()
    
    # Set clock domain (higher frequency for superscalar)
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '2GHz'  # Higher frequency
    system.clk_domain.voltage_domain = VoltageDomain()
    
    # Set memory mode
    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange('1GB')]  # Larger memory for complex workloads
    
    # Create O3CPU (Out-of-Order CPU) for superscalar simulation
    system.cpu = O3CPU()
    
    # Configure superscalar parameters
    system.cpu.fetchWidth = issue_width      # Instructions fetched per cycle
    system.cpu.decodeWidth = issue_width     # Instructions decoded per cycle
    system.cpu.renameWidth = issue_width     # Instructions renamed per cycle
    system.cpu.issueWidth = issue_width      # Instructions issued per cycle
    system.cpu.wbWidth = issue_width         # Instructions written back per cycle
    system.cpu.commitWidth = issue_width     # Instructions committed per cycle
    
    # Reorder Buffer (ROB) configuration
    system.cpu.numROBEntries = rob_size
    
    # Instruction Queue sizes
    system.cpu.numIQEntries = 64    # Integer instruction queue
    system.cpu.numLQEntries = 32    # Load queue
    system.cpu.numSQEntries = 32    # Store queue
    
    # Physical register file sizes
    system.cpu.numPhysIntRegs = 256  # Integer physical registers
    system.cpu.numPhysFloatRegs = 256  # Floating-point physical registers
    
    # Functional Units configuration
    system.cpu.fuPool = DefaultO3FUPool()
    
    # Branch prediction (advanced for superscalar)
    system.cpu.branchPred = TournamentBP()
    system.cpu.branchPred.localPredictorSize = 2048
    system.cpu.branchPred.localCtrBits = 2
    system.cpu.branchPred.globalPredictorSize = 8192
    system.cpu.branchPred.globalCtrBits = 2
    system.cpu.branchPred.choicePredictorSize = 8192
    system.cpu.branchPred.choiceCtrBits = 2
    
    # BTB (Branch Target Buffer) configuration
    system.cpu.branchPred.BTBEntries = 4096
    system.cpu.branchPred.BTBTagSize = 16
    
    # RAS (Return Address Stack) configuration
    system.cpu.branchPred.RASSize = 16
    
    # Cache configuration - larger for superscalar
    system.cpu.icache = Cache(size='64kB', assoc=4, tag_latency=1, data_latency=1, 
                             response_latency=1, mshrs=8, tgts_per_mshr=20)
    system.cpu.dcache = Cache(size='64kB', assoc=4, tag_latency=2, data_latency=2,
                             response_latency=1, mshrs=8, tgts_per_mshr=20)
    
    # Connect CPU to caches
    system.cpu.icache.cpu_side = system.cpu.icache_port
    system.cpu.dcache.cpu_side = system.cpu.dcache_port
    
    # Larger L2 cache for superscalar
    system.l2cache = Cache(size='1MB', assoc=16, tag_latency=12, data_latency=12,
                          response_latency=5, mshrs=20, tgts_per_mshr=12)
    
    # L2 prefetcher for better memory performance
    system.l2cache.prefetcher = StridePrefetcher(degree=8, latency=1)
    
    # Create memory bus
    system.membus = SystemXBar()
    system.membus.width = 64  # Wider bus for superscalar
    
    # Connect L1 caches to L2 cache
    system.cpu.icache.mem_side = system.l2cache.cpu_side
    system.cpu.dcache.mem_side = system.l2cache.cpu_side
    
    # Connect L2 cache to memory bus
    system.l2cache.mem_side = system.membus.slave
    
    # Create interrupt controller
    system.cpu.createInterruptController()
    
    # Connect special ports for x86
    if buildEnv['TARGET_ISA'] == 'x86':
        system.cpu.interrupts[0].pio = system.membus.master
        system.cpu.interrupts[0].int_master = system.membus.slave
        system.cpu.interrupts[0].int_slave = system.membus.master
    
    # Memory controller with higher bandwidth
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR4_2400_8x8()  # Faster memory
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.master
    
    # Connect system port
    system.system_port = system.membus.slave
    
    return system

def set_workload(system, binary_path):
    """Set the workload/binary to execute"""
    if not os.path.isfile(binary_path):
        fatal(f"Binary file {binary_path} not found!")
    
    process = Process()
    process.cmd = [binary_path]
    system.cpu.workload = process
    system.cpu.createThreads()

def main():
    """Main simulation function"""
    parser = argparse.ArgumentParser(description='Superscalar Processor Simulation')
    parser.add_argument('binary', help='Path to binary executable')
    parser.add_argument('--output-dir', default='m5out', 
                       help='Directory for simulation outputs')
    parser.add_argument('--issue-width', type=int, default=4,
                       help='Issue width (instructions per cycle)')
    parser.add_argument('--rob-size', type=int, default=192,
                       help='Reorder buffer size')
    
    args = parser.parse_args()
    
    # Create superscalar system
    system = create_superscalar_system(args.issue_width, args.rob_size)
    
    # Set workload
    set_workload(system, args.binary)
    
    # Create root object
    root = Root(full_system=False, system=system)
    
    # Instantiate simulation
    m5.instantiate()
    
    print("Beginning superscalar simulation!")
    print(f"Running workload: {args.binary}")
    print(f"Issue width: {args.issue_width} instructions/cycle")
    print(f"ROB size: {args.rob_size} entries")
    print(f"Output directory: {args.output_dir}")
    
    # Start simulation
    start_tick = m5.curTick()
    exit_event = m5.simulate()
    end_tick = m5.curTick()
    
    # Print simulation results
    print(f'Simulation completed at tick {end_tick}')
    print(f'Simulated time: {(end_tick - start_tick) / 1e12:.6f} seconds')
    print(f'Exit reason: {exit_event.getCause()}')
    
    # Performance metrics
    print("\n=== Superscalar Performance Analysis ===")
    print(f"Host seconds: {m5.stats.simStats.host_seconds:.2f}")
    
    if hasattr(system.cpu, 'committedInsts'):
        insts = system.cpu.committedInsts
        cycles = system.cpu.numCycles
        ipc = insts / cycles if cycles > 0 else 0
        print(f"Instructions executed: {insts}")
        print(f"Cycles: {cycles}")
        print(f"IPC: {ipc:.3f}")
        print(f"Theoretical max IPC: {args.issue_width}")
        print(f"IPC efficiency: {(ipc/args.issue_width)*100:.1f}%")
    
    print(f"\nDetailed statistics written to: {args.output_dir}/stats.txt")

if __name__ == '__main__':
    main()