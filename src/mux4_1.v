`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/02/2026 01:51:51 PM
// Design Name: 
// Module Name: mux4_1
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module mux4_1 (
    input d0, d1, d2, d3,  // 4 Data Switches
    input s0, s1,          // 2 Select Switches
    output y               // 1 LED Output
);

    // Internal wires to connect the first stage to the final stage
    wire mux_bottom;
    wire mux_top;

    // First 2:1 MUX: Selects between d0 and d1 using s0
    assign mux_bottom = s0 ? d1 : d0;

    // Second 2:1 MUX: Selects between d2 and d3 using s0
    assign mux_top = s0 ? d3 : d2;

    // Third 2:1 MUX: Selects between the two wires above using s1
    assign y = s1 ? mux_top : mux_bottom;

endmodule
