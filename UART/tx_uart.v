module tx_uart
#(parameter CLKS_PER_BIT = 217)
 (
    input clk,
    input [7:0] in_data,
    input tx_dv,
    output tx_active,
    output reg tx_serial
);
    
    parameter IDLE         = 3'b000;
    parameter TX_START_BIT = 3'b001;
    parameter TX_DATA_BITS = 3'b010;
    parameter TX_STOP_BIT  = 3'b011;
    
    reg [2:0] TX_STATE = 0;
    reg [7:0] clk_counter = 0;
    reg [2:0] bit_index = 0;
    reg [7:0] TX_DATA = 0;
    reg tx_active = 0;

    always @(posedge clk) begin

        case (TX_STATE)
           IDLE :
                begin
                    tx_serial <= 1'b1;
                    clk_counter <= 1'b0;
                    bit_index <= 1'b0;

                    if (tx_dv == 1'b1)begin
                        tx_active <= 1'b1;
                        TX_DATA <= in_data;
                        TX_STATE <= TX_START_BIT;
                    end
                    else begin
                        TX_STATE <= IDLE;
                    end
                end 

            TX_START_BIT :
                begin
                    tx_serial <= 1'b0;

                    if (clk_counter < CLKS_PER_BIT-1) begin
                        clk_counter <= clk_counter + 1;
                        TX_STATE <= TX_START_BIT;
                    end
                    else begin
                        clk_counter <= 0;
                        TX_STATE <= TX_DATA_BITS;
                    end
                end

            TX_DATA_BITS :
                begin
                    tx_serial <= TX_DATA[bit_index];

                    if (clk_counter < CLKS_PER_BIT-1) begin
                        clk_counter <= clk_counter + 1;
                        TX_STATE <= TX_DATA_BITS; 
                    end
                    else begin
                        clk_counter <= 0;

                        if (bit_index < 7) begin
                            bit_index <= bit_index + 1;
                            TX_STATE <= TX_DATA_BITS;
                        end
                        else begin
                            bit_index <= 0;
                            TX_STATE <= TX_STOP_BIT;
                        end
                    end
                end

            TX_STOP_BIT :
                begin
                    tx_serial <= 1'b1;

                    if(clk_counter < CLKS_PER_BIT-1) begin
                        clk_counter <= clk_counter + 1;
                        TX_STATE <= TX_STOP_BIT;
                    end
                    else begin
                        tx_active <= 1'b0;
                        clk_counter <= 0;
                        TX_STATE <= IDLE;
                    end
                end


            default: 
                TX_STATE <= IDLE;

        endcase
        
    end
    // `ifdef COCOTB_SIM
    //     initial begin
    //         $dumpfile("tx_uart.vcd");
    //         $dumpvars(0,tx_uart);
    //         #1;
    //     end
    // `endif


endmodule