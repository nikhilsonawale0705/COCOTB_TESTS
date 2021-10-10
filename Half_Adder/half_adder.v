`timescale 1ns/1ps

module half_adder 
  (
   i_bit1,
   i_bit2,
   sum,
   carry
   );
 
  input  i_bit1;
  input  i_bit2;
  output sum;
  output carry;
  assign sum   = i_bit1 ^ i_bit2;  // bitwise xor
  assign carry = i_bit1 & i_bit2;  // bitwise and

  // Dump waves
  `ifdef COCOTB_SIM
    initial begin
        $dumpfile ("half_adder.vcd");
        $dumpvars (0, half_adder);
        #1;
    end
`endif
endmodule