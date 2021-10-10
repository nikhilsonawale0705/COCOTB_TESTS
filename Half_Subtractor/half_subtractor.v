`timescale 1ns/1ps

module half_subtractor (
    A, B,
    diff, borrow
);
    input A, B;
    output diff, borrow;

    assign diff = A ^ B;
    assign borrow = ~A & B;

    `ifdef COCOTB_SIM
        initial begin
            $dumpfile("half_subtractor.vcd");
            $dumpvars(0,half_subtractor);
            #1;
        end
    `endif

endmodule