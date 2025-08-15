from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import MESITwoLevelCacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600, SingleChannelDDR3_2133, SingleChannelLPDDR3_1600, SingleChannelDDR4_2400, DIMM_DDR5_4400, DIMM_DDR5_6400, DIMM_DDR5_8400

from gem5.components.memory.multi_channel import DualChannelDDR3_1600, DualChannelDDR3_2133, DualChannelDDR4_2400, DualChannelLPDDR3_1600

from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import Resource
from gem5.resources.resource import CustomResource
from gem5.simulate.simulator import Simulator

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--isa",help='ISA to run', required=True)
parser.add_argument("--binary",help='Binary Path to run', required=True)

parser.add_argument("--memorymodel",help='Memory model to run', required=True)
parser.add_argument("--cputype",help='CPU Type to run', required=True)
parser.add_argument("--cpufrequency",help='CPU Frequency to run', required=True)

args = vars(parser.parse_args())

print(args)

isa_mapping = {
    'X86' : ISA.X86,
    'ARM' : ISA.ARM,
    'MIPS' : ISA.MIPS,
    'POWER' : ISA.POWER,
    'RISCV' : ISA.RISCV,
    'SPARC' : ISA.SPARC
}

#cache_hierarchy = NoCache()
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(l1d_size="16KiB", l1i_size="16KiB",l2_size="256KiB")
#cache_hierarchy = MESITwoLevelCacheHierarchy(   l1d_size="16KiB",l1d_assoc=8,l1i_size="16KiB"l1i_assoc=8, l2_size="256KiB", l2_assoc=16, num_l2_banks=1)

memory_mapping ={
    "SINGLE_CHANNEL_DDR3_1600" : SingleChannelDDR3_1600,
    "SINGLE_CHANNEL_DDR3_2133" : SingleChannelDDR3_2133,
    "SINGLE_CHANNEL_LPDDR3_1600" : SingleChannelLPDDR3_1600,
    "SINGLE_CHANNEL_DDR4_2400" : SingleChannelDDR4_2400,
    "SINGLE_CHANNEL_DIMM_DDR5_4400" : DIMM_DDR5_4400,
    "SINGLE_CHANNEL_DIMM_DDR5_6400" : DIMM_DDR5_6400,
    "SINGLE_CHANNEL_DIMM_DDR5_8400" : DIMM_DDR5_8400,

    "DUAL_CHANNEL_DDR3_1600" : DualChannelDDR3_1600,
    "DUAL_CHANNEL_DDR3_2133" : DualChannelDDR3_2133,
    "DUAL_CHANNEL_LPDDR3_1600" : DualChannelLPDDR3_1600,
    "DUAL_CHANNEL_DDR4_2400" : DualChannelDDR4_2400
}

#memory = SingleChannelDDR3_1600("1GiB")

memory = memory_mapping[args['memorymodel']]("1GiB")

processor_mapping = {
    "ATOMIC" : CPUTypes.ATOMIC,
    "TIMING" : CPUTypes.TIMING,
    "MINOR" : CPUTypes.MINOR,
    "O3" : CPUTypes.O3,
    "KVM" : CPUTypes.KVM
}

processor = SimpleProcessor(cpu_type=processor_mapping[args['cputype']], num_cores=1, isa=isa_mapping[args['isa']])



board = SimpleBoard(
    clk_freq=args['cpufrequency'],
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

binary = CustomResource(args['binary'])
#"x86-hello64-static"
board.set_se_binary_workload(binary)

simulator = Simulator(board=board)
simulator.run()


