`timescale 1ns/1ps

module full_adder (
    A, B, C,
    sum, carry
);
    
    input A, B, C;
    output reg sum, carry;

    always @(A or B or C) begin
        sum = A^B^C;
        carry = A&B | (A^B) & C;         
    end 

     `ifdef COCOTB_SIM
    initial begin
        $dumpfile ("full_adder.vcd");
        $dumpvars (0, full_adder);
        #1;
    end
`endif

endmodule