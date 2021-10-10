`timescale 1ns/1ps

module up_down_counter (
    upd, clk, reset, 
    out
);
    input upd, reset, clk;
    parameter range = 4;
    output reg [range-1:0] out;

    always @(posedge clk) begin
        if (reset == 1) 
            out<= 0;
        else    
            if(upd == 1)   //Up mode selected
                if(out== 15)
                    out<= 0;
                else
                    out<= out+ 1; //Incremend Counter
            else  //Down mode selected
                if(out== 0)
                    out<= 15;
                else
                    out<= out- 1; //Decrement counter
    end

`ifdef COCOTB_SIM
    initial begin
        $dumpfile("up_down_counter.vcd");
        $dumpvars(0, up_down_counter);
        #1;
    end
`endif

endmodule