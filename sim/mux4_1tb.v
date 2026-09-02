`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/02/2026 01:54:15 PM
// Design Name: 
// Module Name: mux4_1tb
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




module mux4_1tb;
    // Inputs (Registers)
    reg d0, d1, d2, d3;
    reg s0, s1;
    
    // Output (Wire)
    // Output (Wire)
    wire y;

    // Connect to our simplified module
    mux4_1 uut (
        .d0(d0), .d1(d1), .d2(d2), .d3(d3),
        .s0(s0), .s1(s1),
        .y(y)
    );

    initial begin
        // Set up the data inputs: d3=1, d2=0, d1=1, d0=0
        //d0 = 1; 
       // d1 = 0; 
       // d2 = 1; 
       // d3 = 0;

        // Test the 4 combinations of the select switches
        s1 = 0; s0 = 0; #10; // Should output d0 (0)
        s1 = 0; s0 = 1; #10; // Should output d1 (1)
        s1 = 1; s0 = 0; #10; // Should output d2 (0)
        s1 = 1; s0 = 1; #10; // Should output d3 (1)
        
        $finish; // End the simulation
    end
endmodule
