import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.result import TestFailure

import random


@cocotb.coroutine
def reset_counter(dut):
    dut.reset = 1
    yield FallingEdge(dut.clk)


@cocotb.coroutine
def set_counter(dut):
    dut.reset = 0
    yield FallingEdge(dut.clk)


@cocotb.coroutine
def range_value(dut):
    yield FallingEdge(dut.clk)
    value = 0
    for i in range(dut.range.value):
        value = value + 2**i
    return value


@cocotb.test()
def test_up_down_counter(dut):

    cocotb.fork(Clock(dut.clk, 10, units='us').start())

    dut._log.info("Initailising counter")

    overflow_value = yield range_value(dut)
    yield reset_counter(dut)
    yield set_counter(dut)

    for i in range(10):
        dut.upd = random.randint(0, 1)
        yield FallingEdge(dut.clk)
        if dut.out.value.integer > overflow_value:
            dut._log.error("Randomised test failed with: %d" %
                           (dut.out.value.value))
            raise TestFailure("Counter value overflowed")
        dut._log.info("count...%s" % (dut.out))
    dut._log.info('Simulation End')
