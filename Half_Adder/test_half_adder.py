import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.result import TestFailure

import random


@cocotb.coroutine
async def xor(a, b):
    await Timer(2, units='ns')
    return a ^ b


@cocotb.coroutine
async def AnD(a, b):
    return a & b


@cocotb.coroutine
async def Or(a, b):
    return a | b


@cocotb.test()
async def half_adder_test(dut):

    dut._log.info("Initailising HALF ADDER")

    for i in range(10):
        A = random.randint(0, 1)
        B = random.randint(0, 1)

        dut.i_bit1 <= A
        dut.i_bit2 <= B
        await Timer(10, units='ns')
        assert dut.sum.value == await xor(A, B), "Randomised test failed with: Sum of {A} and {B} = {X}".format(
            A=dut.i_bit1.value, B=dut.i_bit2.value, X=dut.sum.value)

        await Timer(10, units='ns')
        assert dut.carry.value == await AnD(A, B), "Randomised test failed with: Carry of {A} and {B} = {X}".format(
            A=dut.i_bit1.value, B=dut.i_bit2.value, X=dut.carry.value)
    dut._log.info('Simulation End')
