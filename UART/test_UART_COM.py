import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge


@cocotb.coroutine
def clock_counter(dut):
    for i in range(dut.CLKS_PER_BIT.value):
        yield RisingEdge(dut.i_clock)


@cocotb.test()
def testing_UART_communication(dut):
    i_clk = dut.i_clock
    cocotb.fork(Clock(i_clk, 10, units='us').start())
    yield RisingEdge(i_clk)
    dut.r_tx_dv = 0
    yield RisingEdge(i_clk)
    dut.r_tx_dv = 1
    dut.r_TX_Byte = 200
    yield RisingEdge(i_clk)
    dut.r_tx_dv = 0
    yield RisingEdge(i_clk)

    while (dut.w_tx_active == 1):
        yield clock_counter(dut)
        if (dut.w_tx_serial.value != dut.w_UART_Line.value):
            dut._log.error("Recevier expected %d but got %d" %
                           (dut.w_tx_serial.value, dut.w_UART_Line.value))
            print(dut.w_tx_active)

    if (dut.r_TX_Byte.value == dut.w_RX_Byte.value):
        dut._log.info(
            'UART Connection established Message Received %s' % dut.w_RX_Byte.value.binstr)
    dut._log.info('Simulation End')
