import m5
from m5.objects import *

# Create the system
system = System()
system.clk_domain = SrcClockDomain(clock = '2GHz', voltage_domain = VoltageDomain())
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Create a simple CPU
system.cpu = TimingSimpleCPU()

# Create L1 and L2 Caches (Assumes you have defined these classes elsewhere)
system.cpu.icache = L1ICache(size='32kB')
system.cpu.dcache = L1DCache(size='32kB')
system.l2cache = L2Cache(size='2MB')

# Connect CPU to L1, L1 to L2, L2 to memory bus
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
# ... (bus connection code omitted for brevity) ...

# Connect DRAMSim3 as the main memory
system.mem_ctrl = DRAMsim2()
system.mem_ctrl.configFile = "dramsim3_hbm2.ini" # Config for HBM memory
system.mem_ctrl.port = system.membus.mem_side_ports

# Set the binary to run (the C program compiled earlier)
process = Process()
process.cmd = ['seq_read', '2048'] # Running with 2KB size
system.cpu.workload = process
system.cpu.createThreads()

# Run the simulation
m5.instantiate()
print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
