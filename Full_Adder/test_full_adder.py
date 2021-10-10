import cocotb
from cocotb.triggers import Timer

import random


@cocotb.coroutine
async def sum_check(a, b, c):
    return a ^ b ^ c


@cocotb.coroutine
async def carry_check(a, b, c):
    return a & b | (a ^ b) & c


@cocotb.test()
async def testing_full_adder(dut):
    dut._log.info("Initailising FULL ADDER")
    for i in range(10):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        c = random.randint(0, 1)

        dut.A <= a
        dut.B <= b
        dut.C <= c
        await Timer(10, units='ns')
        assert dut.sum.value == await sum_check(a, b, c), "Randomised test failed with: Sum of {A} {B} {C} = {X}".format(
            A=dut.A.value, B=dut.B.value, C=dut.C.value, X=dut.sum.value)

        await Timer(10, units='ns')
        assert dut.carry.value == await carry_check(a, b, c), "Randomised test failed with: Carry of {A} {B} {C} = {X}".format(
            A=dut.A.value, B=dut.B.value, C=dut.C.value, X=dut.carry.value)
