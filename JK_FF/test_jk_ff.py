import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.result import TestFailure

import random


@cocotb.test()
def testing_jk_ff(dut):
    clear = dut.clear
    cocotb.fork(Clock(dut.clk, 10, units="us").start())

    q_previous = []

    dut._log.info("Initialising JK FF Test")

    clear <= 1
    yield FallingEdge(dut.clk)

    clear <= 0
    q_previous.append(dut.q.value)

    for i in range(20):
        j = random.randint(0, 1)
        k = random.randint(0, 1)
        dut.j <= j
        dut.k <= k

        yield FallingEdge(dut.clk)

        if(j == 0 and k == 0):
            ''' No Change Condition '''
            assert dut.q.value == q_previous[i], "Randomised test failed at: [{a}, {b}] Current Output Q_current = {y} is not same as Previous Q output Q_previous = {v}".format(
                a=dut.j.value, b=dut.k.value, y=dut.q.value, v=q_previous[i])
            q_previous.append(dut.q.value)

        elif (j == 0 and k == 1):
            ''' Check for condition Reset(Resets Q t 0) '''

            assert dut.q.value == 0, "Randomised test failed at: [{a}, {b}] Q is not being Reset Q != 0".format(
                a=dut.j.value, b=dut.k.value, y=dut.q.value)

            q_previous.append(dut.q.value)

        elif (j == 1 and k == 0):
            ''' Check for condition Set (Sets Q t 0) '''

            assert dut.q.value == 1, "Randomised test failed at: [{a}, {b}] Q is not being Set Q != 1".format(
                a=dut.j.value, b=dut.k.value, y=dut.q.value)

            q_previous.append(dut.q.value)

        else:
            ''' Check for Toggle condition '''

            assert dut.q.value != q_previous[i], "Randomised test failed at: [{a}, {b}] Current Output Q_current = {y} is not being changed/Toggled or same as Previous Q output Q_previous = {v}".format(
                a=dut.j.value, b=dut.k.value, y=dut.q.value, v=q_previous[i])

            q_previous.append(dut.q.value)
    dut._log.info('Simulation End')
