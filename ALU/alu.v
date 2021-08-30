`timescale 1ns/1ps

module alu(clk,reset,a,b,s,y);
    input clk,reset;
	input[3:0]  a;
	input[3:0]  b;
	input[2:0]  s;
	output[7:0] y;
	reg[7:0]    y;

	always@(s or a or b) begin
        if (reset)begin
            y<=0;
        end
        else begin
        
        case(s)
            3'b000:y=a+b;
            3'b001:y=a-b;
            3'b010:y=a&b;
            3'b011:y=a|b;
        endcase
            
        end 
	end


`ifdef COCOTB_SIM
    initial begin
        $dumpfile ("alu.vcd");
        $dumpvars (0, alu);
        #1;
    end
`endif

endmodule