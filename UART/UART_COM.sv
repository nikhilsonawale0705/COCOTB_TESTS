`timescale 1ns/1ps

`include "tx_uart.v"
`include "rx_uart.v"

module UART_COM (
    input i_clock,
    input r_tx_dv,
    input [7:0] r_TX_Byte,
    output [7:0] w_RX_Byte
);

    parameter CLKS_PER_BIT = 217;
    // reg i_clock;
    // reg r_tx_dv;
    // reg [7:0] r_TX_Byte ;
    // wire [7:0] w_RX_Byte;
    wire w_tx_serial;
    reg w_tx_active, w_rx_active;
    wire w_UART_Line;

    assign w_UART_Line = w_tx_active ? w_tx_serial : 1'b1;
    
    tx_uart #(.CLKS_PER_BIT(CLKS_PER_BIT)) tx_uart_Inst
    (
        .clk(i_clock),
        .tx_dv(r_tx_dv),
        .in_data(r_TX_Byte),
        .tx_active(w_tx_active),
        .tx_serial(w_tx_serial)
    );

    rx_uart #(.CLKS_PER_BIT(CLKS_PER_BIT)) rx_uart_Inst
    (
        .clk(i_clock),
        .out_data(w_RX_Byte),
        .rx_active(w_rx_active),
        .rx_serial(w_UART_Line)
    );
    
    
    `ifdef COCOTB_SIM
        initial begin
            $dumpfile("UART_COMM.vcd");
            $dumpvars(0);
            #1;
        end
    `endif

endmodule