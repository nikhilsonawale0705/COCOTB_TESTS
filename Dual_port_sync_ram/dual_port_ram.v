`timescale 1ns/1ps

module dual_port_ram (
    clk, reset,
    rd_enb, rd_addr,
    wr_enb, wr_addr, 
    data_in, data_out 
);

parameter ram_width = 8 ;
parameter ram_depth = 256;
parameter addr_size = 8;

input clk, reset, rd_enb, wr_enb;
input [ram_width-1:0] data_in;
input [addr_size-1:0] rd_addr, wr_addr;
output reg [ram_width-1:0] data_out;

reg [ram_width-1:0] mem[ram_depth-1:0];
integer i;

always @(posedge clk) begin
    if (reset) begin
        for(i=0; i<ram_depth; i=i+1)
            mem[i] <= 0;
    end
    else begin
        if (wr_enb) begin
            mem[wr_addr] <= data_in;
        end
            
        if (rd_enb) begin
            data_out <= mem[rd_addr];
        end
            
    end
end


`ifdef COCOTB_SIM
    initial begin
        $dumpfile ("dual_port_ram.vcd");
        $dumpvars (0, dual_port_ram);
        #1;
    end
`endif


endmodule