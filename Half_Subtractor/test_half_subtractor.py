import cocotb
from cocotb.triggers import Timer

import random


@cocotb.coroutine
async def diff_check(a, b):
    return a ^ b


@cocotb.coroutine
async def borrow_check(a, b):
    return ~a & b


@cocotb.test()
async def testing_full_adder(dut):
    dut._log.info("Initailising FULL ADDER")
    for i in range(10):
        a = random.randint(0, 1)
        b = random.randint(0, 1)

        dut.A <= a
        dut.B <= b
        await Timer(10, units='ns')
        assert dut.diff.value == await diff_check(a, b), "Randomised test failed with: Difference of {A}  {B} = {X}".format(
            A=dut.A.value, B=dut.B.value, X=dut.diff.value)

        await Timer(10, units='ns')
        assert dut.borrow.value == await borrow_check(a, b), "Randomised test failed with: Borrow of {A}  {B} = {X}".format(
            A=dut.A.value, B=dut.B.value, X=dut.borrow.value)
