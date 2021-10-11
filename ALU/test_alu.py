import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
import adder_model


def add(a, b):
    return a+b


@cocotb.test()
async def testing_alu(dut):
    print("Initialise Code")
    dut.reset <= 1
    await Timer(2, units='ns')
    dut.reset <= 0
    for i in range(4):
        dut.s.value = i
        a = random.randint(0, 6)
        b = random.randint(0, 8)
        dut.a.value = a
        dut.b.value = b
        await Timer(2, units='ns')
        if dut.s.value == 0:
            assert dut.y.value == adder_model.adder_model(a, b), "Randomised test failed with: {a} + {b} = {y}".format(
                a=dut.a.value, b=dut.b.value, y=dut.y.value)
        elif dut.s.value == 1:
            assert dut.y.value == adder_model.sub_model(a, b), "Randomised test failed with: {a} + {b} = {y}".format(
                a=dut.a.value, b=dut.b.value, y=dut.y.value)
        elif dut.s.value == 2:
            assert dut.y.value == adder_model.and_model(a, b), "Randomised test failed with: {a} + {b} = {y}".format(
                a=dut.a.value, b=dut.b.value, y=dut.y.value)
        else:
            assert dut.y.value == adder_model.or_model(a, b), "Randomised test failed with: {a} + {b} = {y}".format(
                a=dut.a.value, b=dut.b.value, y=dut.y.value)
