Structural 4:1 Multiplexer Using 2:1 Multiplexers

A hierarchical Verilog HDL implementation of a 4:1 Multiplexer (MUX) constructed using three 2:1 Multiplexer submodules. The design is developed and verified using Xilinx Vivado through RTL elaboration and behavioral simulation.

📌 Project Overview

A multiplexer is a combinational digital circuit used to select one input from multiple input signals and route it to a single output.

This project demonstrates how a 4:1 MUX can be constructed structurally using three 2:1 MUXes arranged in a two-stage hierarchical tree.

The project covers:

Structural Verilog design
Hierarchical module instantiation
Reusable 2:1 MUX submodule
4:1 MUX top-level module
Behavioral testbench
RTL schematic verification
Behavioral simulation using Xilinx Vivado
🏗️ Design Architecture

The 4:1 MUX is constructed using three 2:1 MUXes.

Stage 1 — First Layer

Two 2:1 MUXes operate in parallel:

m0 selects between in[0] and in[1] using sel[0], producing w0.
m1 selects between in[2] and in[3] using sel[0], producing w1.
Stage 2 — Second Layer

The third 2:1 MUX:

m2 selects between w0 and w1 using sel[1].
The resulting signal is connected to the final output out.
Block Diagram
                         Stage 1
                   +----------------+
in[0] ------------>|                |
in[1] ------------>|    mux2to1     |---- w0 ----+
sel[0] ----------->|      (m0)      |            |
                   +----------------+            |
                                                 |      Stage 2
                                                 |   +----------------+
                                                 +-->|                |
                                                     |    mux2to1     |---- out
                                                 +-->|      (m2)      |
                                                 |   +----------------+
                   +----------------+            |        ^
in[2] ------------>|                |---- w1 ----+        |
in[3] ------------>|    mux2to1     |                     |
sel[0] ----------->|      (m1)      |                  sel[1]
                   +----------------+

📋 Truth Table
sel[1]	sel[0]	Selected Input	out
0	0	in[0]	in[0]
0	1	in[1]	in[1]
1	0	in[2]	in[2]
1	1	in[3]	in[3]

Therefore:

sel = 00 → out = in[0]
sel = 01 → out = in[1]
sel = 10 → out = in[2]
sel = 11 → out = in[3]

📁 Repository Structure
vivado-4to1-mux-structural/
│
├── src/
│   ├── mux2to1.v
│   └── mux4to1.v
│
├── sim/
│   └── tb_mux4to1.v
│
├── docs/
│   ├── rtl-schematic.png
│   └── simulation-waveform.png
│
├── .gitignore
└── README.md

💻 Verilog Source Code
1. 2:1 MUX — src/mux2to1.v
`timescale 1ns / 1ps

module mux2to1 (
    input wire a,
    input wire b,
    input wire sel,
    output wire y
);

    assign y = sel ? b : a;

endmodule


The 2:1 MUX selects:

sel = 0 → y = a
sel = 1 → y = b

2. 4:1 MUX — src/mux4to1.v
`timescale 1ns / 1ps

module mux4to1 (
    input wire [3:0] in,
    input wire [1:0] sel,
    output wire out
);

    wire w0, w1;

    // Stage 1
    mux2to1 m0 (
        .a(in[0]),
        .b(in[1]),
        .sel(sel[0]),
        .y(w0)
    );

    mux2to1 m1 (
        .a(in[2]),
        .b(in[3]),
        .sel(sel[0]),
        .y(w1)
    );

    // Stage 2
    mux2to1 m2 (
        .a(w0),
        .b(w1),
        .sel(sel[1]),
        .y(out)
    );

endmodule

3. Testbench — sim/tb_mux4to1.v
`timescale 1ns / 1ps

module tb_mux4to1;

    reg [3:0] in;
    reg [1:0] sel;
    wire out;

    // Unit Under Test
    mux4to1 uut (
        .in(in),
        .sel(sel),
        .out(out)
    );

    initial begin

        // Test pattern
        // in[3] = 1
        // in[2] = 0
        // in[1] = 1
        // in[0] = 0
        in = 4'b1010;

        sel = 2'b00;
        #10;
        // Expected: out = in[0] = 0

        sel = 2'b01;
        #10;
        // Expected: out = in[1] = 1

        sel = 2'b10;
        #10;
        // Expected: out = in[2] = 0

        sel = 2'b11;
        #10;
        // Expected: out = in[3] = 1

        $display("Simulation completed successfully.");

        $finish;
    end

endmodule

🧪 Simulation

The testbench applies the following input:

in = 1010


The expected simulation results are:

Time (ns)	sel	Selected Input	Expected out
0–10	00	in[0]	0
10–20	01	in[1]	1
20–30	10	in[2]	0
30–40	11	in[3]	1

Expected output sequence:

0 → 1 → 0 → 1

🚀 Running the Project in Xilinx Vivado
Step 1 — Create a Project

Open Xilinx Vivado and select:

Create Project


Choose:

RTL Project


You can use:

vivado-4to1-mux-structural


as the project name.

Step 2 — Add Design Sources

Add:

src/mux2to1.v
src/mux4to1.v


Set:

mux4to1


as the top module.

Step 3 — Add Simulation Source

Add:

sim/tb_mux4to1.v


under Simulation Sources.

The testbench should not be used as the synthesis top module.

Step 4 — Run Behavioral Simulation

From the Vivado Flow Navigator:

Simulation
    → Run Simulation
        → Run Behavioral Simulation


Check the waveform for:

sel = 00 → out = 0
sel = 01 → out = 1
sel = 10 → out = 0
sel = 11 → out = 1

Step 5 — View RTL Schematic

Navigate to:

RTL Analysis
    → Open Elaborated Design
        → Schematic


The schematic should show the hierarchical structure containing:

3 × mux2to1
      ↓
2-stage MUX tree
      ↓
4:1 MUX

📊 Verification

For the test input:

in = 4'b1010


the simulation should produce:

Select       Output
-------------------
00             0
01             1
10             0
11             1


This confirms that the structural 4:1 MUX correctly implements the required selection logic.

📸 Documentation

Screenshots can be stored in the docs/ directory:

docs/
├── rtl-schematic.png
└── simulation-waveform.png


Recommended screenshots:

Vivado RTL schematic showing the three mux2to1 instances.
Behavioral simulation waveform showing all four select combinations.
🎯 Learning Objectives

This project demonstrates:

Combinational logic design
Multiplexer operation
Structural Verilog modeling
Hierarchical RTL design
Module instantiation
Signal interconnection
Testbench development
Behavioral simulation
RTL schematic analysis using Vivado
🛠️ Tools Used
Tool	Purpose
Verilog HDL	RTL design and testbench
Xilinx Vivado	Design, elaboration and simulation
Git	Version control
GitHub	Project hosting
📜 License

This project is open-source and available under the MIT License.

⭐ Project Summary
4:1 MUX
   ↓
Built using 3 × 2:1 MUX
   ↓
Structural Verilog
   ↓
Xilinx Vivado
   ↓
RTL Schematic + Behavioral Simulation
