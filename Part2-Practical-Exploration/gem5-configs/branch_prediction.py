#!/usr/bin/env python3

"""
Branch Prediction Configuration for gem5 ILP Experiments
This configuration compares performance with and without branch prediction
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

def create_system_with_branch_prediction(enable_bp=True, bp_type="LocalBP"):
    """Create system with configurable branch prediction"""
    
    # Create the system
    system = System()
    
    # Set clock domain (1GHz default)
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '1GHz'
    system.clk_domain.voltage_domain = VoltageDomain()
    
    # Set memory mode
    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange('512MB')]
    
    # Create CPU - Use MinorCPU for better branch prediction modeling
    system.cpu = MinorCPU()
    
    # Configure branch prediction
    if enable_bp:
        if bp_type == "LocalBP":
            # Local branch predictor (2-bit counters)
            system.cpu.branchPred = LocalBP()
            system.cpu.branchPred.localPredictorSize = 2048
            system.cpu.branchPred.localCtrBits = 2
        elif bp_type == "BiModeBP":
            # Bi-mode branch predictor
            system.cpu.branchPred = BiModeBP()
            system.cpu.branchPred.globalPredictorSize = 8192
            system.cpu.branchPred.choicePredictorSize = 8192
            system.cpu.branchPred.choiceCtrBits = 2
            system.cpu.branchPred.globalCtrBits = 2
        elif bp_type == "TournamentBP":
            # Tournament branch predictor (advanced)
            system.cpu.branchPred = TournamentBP()
            system.cpu.branchPred.localPredictorSize = 2048
            system.cpu.branchPred.localCtrBits = 2
            system.cpu.branchPred.globalPredictorSize = 8192
            system.cpu.branchPred.globalCtrBits = 2
            system.cpu.branchPred.choicePredictorSize = 8192
            system.cpu.branchPred.choiceCtrBits = 2
    else:
        # Disable branch prediction (always predict not taken)
        system.cpu.branchPred = NullBP()
    
    # Configure pipeline parameters for MinorCPU
    system.cpu.fetch1FetchLimit = 1  # Instructions fetched per cycle
    system.cpu.fetch2InputBufferSize = 2
    system.cpu.decodeInputBufferSize = 3
    system.cpu.executeInputWidth = 2  # Instructions that can enter execute per cycle
    system.cpu.executeMaxAccessesInMemory = 2
    system.cpu.executeLSQMaxStoreBufferStoresPerCycle = 2
    
    # Create L1 caches
    system.cpu.icache = Cache(size='32kB', assoc=2, tag_latency=2, data_latency=2, 
                             response_latency=2, mshrs=4, tgts_per_mshr=20)
    system.cpu.dcache = Cache(size='64kB', assoc=2, tag_latency=2, data_latency=2,
                             response_latency=2, mshrs=4, tgts_per_mshr=20)
    
    # Connect CPU to caches
    system.cpu.icache.cpu_side = system.cpu.icache_port
    system.cpu.dcache.cpu_side = system.cpu.dcache_port
    
    # Create L2 cache
    system.l2cache = Cache(size='256kB', assoc=8, tag_latency=20, data_latency=20,
                          response_latency=20, mshrs=20, tgts_per_mshr=12)
    
    # Create memory bus
    system.membus = SystemXBar()
    
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
    
    # Create memory controller
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
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
    parser = argparse.ArgumentParser(description='Branch Prediction Impact Analysis')
    parser.add_argument('binary', help='Path to binary executable')
    parser.add_argument('--output-dir', default='m5out', 
                       help='Directory for simulation outputs')
    parser.add_argument('--branch-pred', choices=['none', 'local', 'bimode', 'tournament'],
                       default='local', help='Branch predictor type')
    
    args = parser.parse_args()
    
    # Map command line arguments to branch predictor types
    bp_mapping = {
        'none': (False, 'LocalBP'),
        'local': (True, 'LocalBP'),
        'bimode': (True, 'BiModeBP'),
        'tournament': (True, 'TournamentBP')
    }
    
    enable_bp, bp_type = bp_mapping[args.branch_pred]
    
    # Create system
    system = create_system_with_branch_prediction(enable_bp, bp_type)
    
    # Set workload
    set_workload(system, args.binary)
    
    # Create root object
    root = Root(full_system=False, system=system)
    
    # Instantiate simulation
    m5.instantiate()
    
    print("Beginning simulation with branch prediction analysis!")
    print(f"Running workload: {args.binary}")
    print(f"Branch predictor: {args.branch_pred} ({'enabled' if enable_bp else 'disabled'})")
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
    print("\n=== Branch Prediction Analysis ===")
    print(f"Host seconds: {m5.stats.simStats.host_seconds:.2f}")
    
    if hasattr(system.cpu, 'committedInsts'):
        insts = system.cpu.committedInsts
        cycles = system.cpu.numCycles
        ipc = insts / cycles if cycles > 0 else 0
        print(f"Instructions executed: {insts}")
        print(f"Cycles: {cycles}")
        print(f"IPC: {ipc:.3f}")
    
    print(f"\nDetailed statistics written to: {args.output_dir}/stats.txt")

if __name__ == '__main__':
    main()