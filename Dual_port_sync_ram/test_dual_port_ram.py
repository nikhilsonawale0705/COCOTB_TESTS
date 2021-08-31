from logging import fatal
import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge


def array_ram(depth):
    r_mem = [0]*depth
    print(r_mem)
    return r_mem


def write_mem(wr_add, inp_data, memory):
    memory[wr_add] = inp_data
    return memory[wr_add]


@cocotb.test()
async def testing_ram(dut):
    width = dut.ram_width.value
    depth = dut.ram_depth.value
    clk = dut.clk
    reset = dut.reset
    cocotb.fork(Clock(clk, 10, units='us').start())

    print("initialize code")
    reset <= 1
    memory = array_ram(depth)
    await FallingEdge(clk)
    assert dut.data_out.value == array_ram(depth)[0]
    reset <= 0

    await FallingEdge(clk)
    dut.wr_enb = 1
    for i in range(6):
        dut.wr_addr.value = i
        input_data = random.randint(0, 15)
        dut.data_in.value = input_data
        await FallingEdge(clk)
        assert dut.mem[i].value == write_mem(
            wr_add=i, inp_data=input_data, memory=memory)

    await FallingEdge(clk)
    dut.rd_enb = 1
    for i in range(6):
        dut.rd_addr.value = i
        out_data = dut.mem[i].value
        dut.data_out.value = out_data
        await FallingEdge(clk)
        assert dut.data_out.value == memory[i]
