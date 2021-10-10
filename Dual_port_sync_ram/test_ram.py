import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.result import TestFailure, ReturnValue
import random


@cocotb.coroutine
def rstn(dut, depth):
    """Reset the RAM"""

    for j in range(depth):
        dut.i = j
        yield RisingEdge(dut.clk)


@cocotb.coroutine
def write_op(dut, depth):
    """This coroutine performs a write operayion of the RAM"""

    for i in range(depth):
        dut.wr_enb = 1
        dut.wr_addr = i
        dut.data_in = random.randint(5, 255)
        yield RisingEdge(dut.clk)
    dut.wr_enb = 0


@cocotb.test()
def test_ram(dut):

    width = dut.ram_width.value
    depth = dut.ram_depth.value
    clk = dut.clk
    reset = dut.reset
    cocotb.fork(Clock(clk, 10, units='us').start())

    dut._log.info("initialize code")
    yield RisingEdge(dut.clk)
    reset <= 1
    yield rstn(dut, depth)
    yield RisingEdge(clk)
    reset <= 0

    dut._log.info("Writing random values")
    yield write_op(dut, depth)

    dut._log.info("Reading back values and checking")
    for i in range(10):
        dut.rd_enb = 1
        read_address = i
        dut.rd_addr <= read_address
        yield RisingEdge(dut.clk)
        yield RisingEdge(dut.clk)

        if dut.data_out.value != dut.mem[i].value:
            dut._log.error("mem[%d] expected %d but got %d" %
                           (i, dut.mem[i].value, dut.data_out.value))
            raise TestFailure("RAM contents incorrect")

    dut.rd_enb = 0
    yield RisingEdge(dut.clk)
    dut._log.info("RAM contents OK")
