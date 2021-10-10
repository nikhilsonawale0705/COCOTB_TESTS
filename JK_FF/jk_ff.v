`timescale 1ns/1ps

module jk_ff (
    clk, clear,
    j,k,
    q
);
    input clk,clear,j,k;
    output reg q;

    always @(posedge clk) begin
        if (clear)begin
            q <= 0;
        end
        else begin
            case({j,k})
                2'b00 : q <= q;
                2'b01 : q <= 0;
                2'b10 : q <= 1;
                2'b11 : q <= ~q;
            endcase
        end
        
    end

`ifdef COCOTB_SIM   
    initial begin
       $dumpfile ("jk_ff.vcd");
       $dumpvars (0, jk_ff);
       #1;
    end
`endif 

endmodule