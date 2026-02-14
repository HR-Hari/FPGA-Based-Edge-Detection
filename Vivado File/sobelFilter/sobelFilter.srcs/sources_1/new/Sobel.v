`timescale 1ns / 1ps

module Sobel (
    input  wire clk,
    input  wire rst,
    
    // The 3x3 pixel window (8-bit grayscale)
    input  wire [7:0] p11, p12, p13, // Top row
    input  wire [7:0] p21, p22, p23, // Middle row
    input  wire [7:0] p31, p32, p33, // Bottom row
    
    // Output edge magnitude
    output reg  [7:0] pixel_out
);

    // Gradients require signed arithmetic. 
    // The maximum possible value is +/- 1020, so 11 bits are needed to prevent overflow.
    reg signed [10:0] Gx, Gy;
    reg [10:0] abs_Gx, abs_Gy;
    reg [11:0] sum;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            Gx <= 0;
            Gy <= 0;
            pixel_out <= 0;
        end else begin
            // --------------------------------------------------------
            // Stage 1: Calculate gradients
            // Note: $signed({3'b0, pXX}) zero-extends the 8-bit unsigned 
            // pixel to an 11-bit signed value before doing the math.
            // --------------------------------------------------------
            Gx <= ($signed({3'b0, p13}) - $signed({3'b0, p11})) + 
                  (($signed({3'b0, p23}) - $signed({3'b0, p21})) <<< 1) + 
                  ($signed({3'b0, p33}) - $signed({3'b0, p31}));

            Gy <= ($signed({3'b0, p31}) - $signed({3'b0, p11})) + 
                  (($signed({3'b0, p32}) - $signed({3'b0, p12})) <<< 1) + 
                  ($signed({3'b0, p33}) - $signed({3'b0, p13}));

            // --------------------------------------------------------
            // Stage 2: Get Absolute Values
            // If the 11th bit (sign bit) is 1, it's negative, so invert it.
            // --------------------------------------------------------
            abs_Gx = (Gx[10]) ? -Gx : Gx;
            abs_Gy = (Gy[10]) ? -Gy : Gy;

            // --------------------------------------------------------
            // Stage 3: Sum and Clip
            // If the sum exceeds the 8-bit maximum (255), clip it to 255.
            // --------------------------------------------------------
            sum = abs_Gx + abs_Gy;
            if (sum > 255)
                pixel_out <= 8'd255;
            else
                pixel_out <= sum[7:0];
        end
    end

endmodule