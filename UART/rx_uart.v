module rx_uart
#(parameter CLKS_PER_BIT = 217)
(
    input clk,
    input rx_serial,
    output rx_dv,
    output rx_active,
    output [7:0] out_data
);
    
    parameter IDLE         = 3'b000;
    parameter RX_START_BIT = 3'b001;
    parameter RX_DATA_BITS = 3'b010;
    parameter RX_STOP_BIT  = 3'b011;
 
    reg [2:0] RX_STATE = 0;
    reg [7:0] clk_counter = 0;
    reg [2:0] rx_bit_index = 0;
    reg [7:0] RX_DATA = 0;
    reg rx_active = 0;

    always @(posedge clk) begin
        
        case (RX_STATE)
            IDLE : 
                begin
                    clk_counter <= 0;
                    rx_bit_index <= 0;

                    if (rx_serial == 1'b0) begin
                        // Start bit detected
                        rx_active <= 1'b1;
                        RX_STATE <= RX_START_BIT;
                    end
                    else begin
                        RX_STATE <= IDLE;
                    end
                end

            RX_START_BIT : 
                begin
                    if (clk_counter == (CLKS_PER_BIT-1)/2)begin
                        if (rx_serial == 1'b0) begin
                            clk_counter <= 0;
                            RX_STATE <= RX_DATA_BITS;
                        end
                        else begin
                            RX_STATE <= IDLE;
                        end
                    end
                    else begin
                        clk_counter <= clk_counter + 1;
                        RX_STATE <= RX_START_BIT;
                    end

                    // if (clk_counter < CLKS_PER_BIT-1) begin
                    //     // Check middle of start bit to make sure it's still low
                    //     if (clk_counter == (CLKS_PER_BIT)/2)begin
                    //         if (rx_serial != 1'b0) begin
                    //             clk_counter <= 0;
                    //             RX_STATE <= IDLE;
                    //         end
                    //     end
                    //     clk_counter <= clk_counter + 1;
                    //     RX_STATE <= RX_START_BIT;
                    // end
                    // else begin
                    //     clk_counter <= 0;
                    //     RX_STATE <= RX_DATA_BITS;
                    // end
                end

            RX_DATA_BITS :
                begin
                    if (clk_counter < CLKS_PER_BIT-1) begin
                        // if (clk_counter == (CLKS_PER_BIT)/2)begin
                        //     if (rx_serial != 1'b0) begin
                        //         clk_counter <= 0;
                        //         RX_STATE <= IDLE;
                        //     end
                        // end
                        clk_counter <= clk_counter + 1;
                        RX_STATE <= RX_DATA_BITS;
                    end
                    else begin
                        clk_counter <= 0;
                        RX_DATA[rx_bit_index] <= rx_serial;

                        if(rx_bit_index < 7) begin
                            rx_bit_index <= rx_bit_index + 1;
                            RX_STATE <= RX_DATA_BITS;
                        end
                        else begin
                            rx_bit_index <= 0;
                            RX_STATE <= RX_STOP_BIT;
                        end
                    end
                end

            RX_STOP_BIT :
                begin
                    if (clk_counter < CLKS_PER_BIT-1) begin
                        clk_counter <= clk_counter + 1;
                        RX_STATE <= RX_STOP_BIT;
                    end
                    else begin
                        rx_active <= 0;
                        clk_counter <= 0;
                        RX_STATE <= IDLE;
                    end
                end

            default: 
                RX_STATE <= IDLE;
                
        endcase
    end

    assign out_data = RX_DATA;
    
endmodule