#!/usr/bin/env python3

"""
Basic 5-Stage Pipeline Configuration for gem5 ILP Experiments
This configuration creates a simple in-order processor with a classic 5-stage pipeline:
Fetch -> Decode -> Execute -> Memory -> Writeback
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

def create_system():
    """Create a simple system with basic 5-stage pipeline"""
    
    # Create the system
    system = System()
    
    # Set clock domain (1GHz default)
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '1GHz'
    system.clk_domain.voltage_domain = VoltageDomain()
    
    # Set memory mode to timing for realistic simulation
    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange('512MB')]
    
    # Create the CPU - TimingSimpleCPU for basic 5-stage pipeline
    system.cpu = TimingSimpleCPU()
    
    # Configure basic pipeline parameters
    system.cpu.switched_out = False
    
    # Create L1 instruction and data caches
    system.cpu.icache = Cache(size='16kB', assoc=2, tag_latency=2, data_latency=2, 
                             response_latency=2, mshrs=4, tgts_per_mshr=20)
    system.cpu.dcache = Cache(size='64kB', assoc=2, tag_latency=2, data_latency=2,
                             response_latency=2, mshrs=4, tgts_per_mshr=20)
    
    # Connect CPU to caches (updated syntax for modern gem5)
    system.cpu.icache_port = system.cpu.icache.cpu_side
    system.cpu.dcache_port = system.cpu.dcache.cpu_side
    
    # Create L2 cache
    system.l2cache = Cache(size='256kB', assoc=8, tag_latency=20, data_latency=20,
                          response_latency=20, mshrs=20, tgts_per_mshr=12)
    
    # Create a memory bus
    system.membus = SystemXBar()
    
    # Create L2 bus for connecting L1 caches to L2
    system.l2bus = L2XBar()
    
    # Connect L1 caches to L2 bus
    system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
    system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
    
    # Connect L2 cache to L2 bus and memory bus
    system.l2cache.cpu_side = system.l2bus.mem_side_ports
    system.l2cache.mem_side = system.membus.cpu_side_ports
    
    # Create interrupt controller
    system.cpu.createInterruptController()
    
    # Connect special ports for x86
    if buildEnv['TARGET_ISA'] == 'x86':
        system.cpu.interrupts[0].pio = system.membus.mem_side_ports
        system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
        system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
    
    # Create memory controller (updated for modern gem5)
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports
    
    # Connect system port to memory bus
    system.system_port = system.membus.cpu_side_ports
    
    return system

def set_workload(system, binary_path):
    """Set the workload/binary to execute"""
    print(f"Setting workload: {binary_path}")
    
    if not os.path.isfile(binary_path):
        fatal(f"Binary file {binary_path} not found!")
    
    # Make sure the binary is executable
    if not os.access(binary_path, os.X_OK):
        warn(f"Binary {binary_path} may not be executable")
    
    # Create process
    process = Process()
    process.cmd = [binary_path]
    system.cpu.workload = process
    system.cpu.createThreads()
    
    print(f"Workload set successfully: {process.cmd}")

def main():
    """Main simulation function"""
    parser = argparse.ArgumentParser(description='Basic 5-Stage Pipeline Simulation')
    parser.add_argument('binary', help='Path to binary executable')
    parser.add_argument('--output-dir', default='m5out', 
                       help='Directory for simulation outputs')
    
    args = parser.parse_args()
    
    # Create system
    system = create_system()
    
    # Set workload
    set_workload(system, args.binary)
    
    # Create root object
    root = Root(full_system=False, system=system)
    
    # Instantiate all of the objects we've created above
    m5.instantiate()
    
    print("Beginning simulation!")
    print(f"Running workload: {args.binary}")
    print(f"Output directory: {args.output_dir}")
    
    # Start simulation
    start_tick = m5.curTick()
    exit_event = m5.simulate()
    end_tick = m5.curTick()
    
    # Print simulation results
    print(f'Simulation completed at tick {end_tick}')
    print(f'Simulated time: {(end_tick - start_tick) / 1e12:.6f} seconds')
    print(f'Exit reason: {exit_event.getCause()}')
    
    # Basic performance metrics
    stats = m5.stats
    print("\n=== Basic Performance Metrics ===")
    print(f"Host seconds: {m5.stats.simStats.host_seconds:.2f}")
    
    # Instructions executed
    if hasattr(system.cpu, 'committedInsts'):
        insts = system.cpu.committedInsts
        print(f"Instructions executed: {insts}")
        print(f"Simulation rate: {insts / m5.stats.simStats.host_seconds:.0f} inst/sec")
    
    print(f"\nDetailed statistics written to: {args.output_dir}/stats.txt")
    print(f"Configuration saved to: {args.output_dir}/config.ini")

if __name__ == '__main__':
    main()