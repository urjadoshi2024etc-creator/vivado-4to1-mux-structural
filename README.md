# 🔀 4:1 Multiplexer Using 2:1 MUXes — Verilog | Vivado

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,100:2c5364&height=220&section=header&text=4:1%20MUX%20Using%202:1%20MUXes&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=38" width="100%"/>
</p>

<p align="center">
  <b>A hierarchical structural Verilog implementation of a 4:1 Multiplexer using three 2:1 Multiplexer modules.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/HDL-Verilog-blue?style=for-the-badge&logo=verilog"/>
  <img src="https://img.shields.io/badge/FPGA-Xilinx%20Vivado-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Simulation-XSim-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Digital%20Logic-MUX-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

---

## 📌 Overview

This project demonstrates the design and implementation of a **4:1 Multiplexer using three 2:1 Multiplexers** in Verilog HDL.

The design follows a **hierarchical structural approach**, where a larger digital circuit is constructed by connecting smaller reusable MUX modules.

### Design Summary

```text
Data Inputs     : d0, d1, d2, d3
Select Inputs   : s0, s1
Output          : y
Building Blocks : 3 × 2:1 MUX
Logic Type      : Combinational
HDL             : Verilog
Tool            : Xilinx Vivado
Simulator       : XSim
```

The project includes:

* Hierarchical Verilog modules
* Verilog simulation testbench
* FPGA pin constraints
* RTL schematic
* Simulation waveform
* Custom architecture diagram
* Animated signal-flow visualization
* FPGA implementation visualization

---

# 🎯 Objectives

The main objectives of this project are to:

* Understand the operation of a **2:1 Multiplexer**
* Build a **4:1 Multiplexer using 2:1 MUXes**
* Implement hierarchical digital logic using Verilog
* Understand module instantiation
* Understand the Verilog ternary operator
* Develop a functional simulation testbench
* Verify all possible select combinations
* Generate and analyze an RTL schematic
* Apply FPGA pin constraints using XDC
* Understand the relationship between RTL design and FPGA hardware

---

# 🧠 What is a Multiplexer?

A **Multiplexer (MUX)** is a combinational digital circuit that selects one input from multiple inputs and connects the selected input to a single output.

For a basic **2:1 MUX**:

```text
             ┌─────────┐
       a ───►│         │
       b ───►│   2:1   ├───► y
     sel ───►│   MUX   │
             └─────────┘
```

Its selection logic can be represented in Verilog using the **ternary operator**:

```verilog
assign y = sel ? b : a;
```

The expression:

```text
condition ? true_value : false_value
```

means:

```text
condition = 0 → true_value is NOT selected
condition = 1 → true_value is selected
```

Therefore:

```text
sel = 0 → y = a
sel = 1 → y = b
```

---

# 🔢 4:1 Multiplexer

A 4:1 MUX has:

```text
4 Data Inputs
      │
      ▼
 ┌───────────┐
 │   4:1 MUX │
 └───────────┘
      ▲
      │
  2 Select Lines
      │
      ▼
      y
```

### Inputs

```text
d0
d1
d2
d3
```

### Select Lines

```text
s1
s0
```

### Output

```text
y
```

Since there are two select lines, there are:

```text
2² = 4
```

possible input selections.

---

# 📋 Truth Table

| `s1` | `s0` | Selected Input |  Output  |
| :--: | :--: | :------------: | :------: |
|   0  |   0  |      `d0`      | `y = d0` |
|   0  |   1  |      `d1`      | `y = d1` |
|   1  |   0  |      `d2`      | `y = d2` |
|   1  |   1  |      `d3`      | `y = d3` |

The select lines therefore determine which input is connected to the output.

---

# 🏗️ Architecture

The 4:1 MUX is constructed from **three 2:1 MUXes**.

The design is divided into two stages.

### Stage 1 — Pair Selection

Two 2:1 MUXes operate in parallel:

```text
MUX 0:
d0 ──┐
     ├──► w0
d1 ──┘
      ▲
      │
      s0
```

```text
MUX 1:
d2 ──┐
     ├──► w1
d3 ──┘
      ▲
      │
      s0
```

Both MUXes use `s0`.

### Stage 2 — Final Selection

The outputs `w0` and `w1` are passed to the third 2:1 MUX:

```text
w0 ──┐
     ├──► MUX 2 ───► y
w1 ──┘
        ▲
        │
        s1
```

Therefore:

```text
s0 → selects an input within each pair
s1 → selects which pair reaches the output
```

---

# 🔀 Complete Architecture

<p align="center">
  <img src="docs/mux4_1-architecture.svg"
       alt="4:1 Multiplexer Architecture"
       width="950"/>
</p>

### Signal Flow

```text
d0 ──┐
     ├── MUX 0 ──► w0 ──┐
d1 ──┘                  │
                        ├── MUX 2 ──► y
d2 ──┐                  │
     ├── MUX 1 ──► w1 ──┘
d3 ──┘
```

Select signals:

```text
s0 → MUX 0
s0 → MUX 1

s1 → MUX 2
```

---

# ⚡ Animated Signal Flow

The animation below demonstrates how the selected input propagates through the three 2:1 MUX stages.

<p align="center">
  <img src="docs/mux4_1-logic-animation.gif"
       alt="Animated 4:1 Multiplexer Logic Flow"
       width="950"/>
</p>

The animation cycles through:

```text
s1 s0 = 00 → d0 → y
s1 s0 = 01 → d1 → y
s1 s0 = 10 → d2 → y
s1 s0 = 11 → d3 → y
```

This makes the hierarchical selection process easier to visualize.

---

# 🧮 Logic Decomposition

The complete 4:1 MUX can be broken down into three simple 2:1 MUX operations.

### MUX 0

```verilog
assign w0 = s0 ? d1 : d0;
```

### MUX 1

```verilog
assign w1 = s0 ? d3 : d2;
```

### MUX 2

```verilog
assign y = s1 ? w1 : w0;
```

The complete design therefore follows:

```text
w0 = s0 ? d1 : d0

w1 = s0 ? d3 : d2

y  = s1 ? w1 : w0
```

This decomposition is the key concept behind the design.

---

# 🧩 Hierarchical Structural Design

The project uses a reusable `mux2to1` module as the basic building block.

The overall hierarchy is:

```text
mux4_1
│
├── mux2to1 m0
│
├── mux2to1 m1
│
└── mux2to1 m2
```

Conceptually:

```text
                     mux4_1
                        │
          ┌─────────────┼─────────────┐
          │             │             │
        MUX 0         MUX 1         MUX 2
         2:1           2:1           2:1
          │             │             │
        d0,d1         d2,d3         w0,w1
          │             │             │
          └──── s0 ─────┘             s1
```

A module connection can be written as:

```verilog
mux2to1 m0 (
    .a(d0),
    .b(d1),
    .sel(s0),
    .y(w0)
);
```

The complete module implementation is available in:

```text
src/mux2to1.v
src/mux4_1.v
```

---

# 📂 Source Files

## `src/mux2to1.v`

Contains the reusable **2:1 Multiplexer module**.

It acts as the basic building block for the complete design.

---

## `src/mux4_1.v`

Contains the top-level **4:1 Multiplexer**.

It connects three instances of the `mux2to1` module to create the two-stage MUX architecture.

---

# 🧪 Simulation

The project includes a Verilog testbench:

```text
sim/mux4_1tb.v
```

The testbench is used to verify the behavior of the 4:1 MUX by applying different select combinations and observing the output.

### Verification Cases

```text
s1 s0 = 00 → y = d0
s1 s0 = 01 → y = d1
s1 s0 = 10 → y = d2
s1 s0 = 11 → y = d3
```

All four combinations of the select inputs must be verified.

---

# 📈 Simulation Waveform

<p align="center">
  <img src="docs/simulation-waveform.png"
       alt="XSim Simulation Waveform"
       width="950"/>
</p>

The waveform demonstrates the relationship between:

```text
d0
d1
d2
d3
s0
s1
y
```

and confirms that the output follows the input selected by `s1` and `s0`.

---

# 🖥️ RTL Schematic

The RTL schematic generated by Vivado provides a graphical representation of the synthesized RTL structure.

<p align="center">
  <img src="docs/rtl-schematic.png"
       alt="Vivado RTL Schematic"
       width="950"/>
</p>

The expected structure contains:

```text
        ┌─────────┐
d0 ────►│         │
d1 ────►│  MUX 0  │──► w0 ──┐
        └─────────┘         │
                            ▼
                         ┌───────┐
                         │ MUX 2 │──► y
                            ▲
        ┌─────────┐         │
d2 ────►│  MUX 1  │──► w1 ──┘
d3 ────►│         │
        └─────────┘
```

This allows the logical Verilog hierarchy to be visually verified at RTL level.

---

# 🔌 FPGA Constraints

The physical FPGA pin assignments are defined using an XDC constraints file:

```text
constraints/mux4_1c.xdc
```

The constraints map the logical signals:

```text
d0
d1
d2
d3

s0
s1

y
```

to physical FPGA pins.

This allows the design to interact with physical FPGA inputs and outputs such as switches and LEDs.

---

# 🔌 FPGA Hardware Implementation

<p align="center">
  <img src="docs/fpga-hardware.svg"
       alt="FPGA Hardware Implementation"
       width="900"/>
</p>

The hardware representation illustrates how the logical MUX design maps onto an FPGA system.

Conceptually:

```text
       FPGA INPUTS
           │
     ┌─────┴─────┐
     │           │
   Data       Select
 Inputs        Inputs
 d0-d3         s0,s1
     │           │
     └─────┬─────┘
           ▼
       ┌────────┐
       │ 4:1    │
       │  MUX   │
       └───┬────┘
           │
           ▼
          y
           │
           ▼
        FPGA LED
```

---

# 🛠️ Tools & Technologies

| Technology          | Purpose                              |
| ------------------- | ------------------------------------ |
| **Verilog HDL**     | Hardware description                 |
| **Xilinx Vivado**   | Design, synthesis and implementation |
| **XSim**            | Verilog simulation                   |
| **XDC**             | FPGA pin constraints                 |
| **FPGA**            | Hardware implementation              |
| **Python + Pillow** | GIF generation                       |
| **Git**             | Version control                      |
| **GitHub**          | Project hosting                      |

---

# 🎞️ Animation Generator

The animated logic-flow visualization is generated using:

```text
create_mux_animation.py
```

The script uses **Python and Pillow** to generate:

```text
mux4_1-logic-animation.gif
```

The generated GIF is stored in:

```text
docs/mux4_1-logic-animation.gif
```

The source script is kept in the repository so the animation can be regenerated or modified later.

---

# 📁 Repository Structure

```text
vivado-4to1-mux-structural/
│
├── 📄 README.md
├── 📄 LICENSE
├── 📄 .gitignore
├── 🐍 create_mux_animation.py
│
├── 📁 src/
│   ├── mux2to1.v
│   └── mux4_1.v
│
├── 📁 sim/
│   └── mux4_1tb.v
│
├── 📁 constraints/
│   └── mux4_1c.xdc
│
└── 📁 docs/
    ├── mux4_1-architecture.svg
    ├── mux4_1-logic-animation.gif
    ├── rtl-schematic.png
    ├── simulation-waveform.png
    └── fpga-hardware.svg
```

---

# 📊 Design Specifications

| Parameter           |         Value |
| ------------------- | ------------: |
| Data Inputs         |             4 |
| Select Inputs       |             2 |
| Output              |             1 |
| MUX Building Blocks |             3 |
| MUX Type            |           2:1 |
| Logic Type          | Combinational |
| HDL                 |       Verilog |
| Simulation          |          XSim |
| FPGA Tool           | Xilinx Vivado |

---

# 🔍 Design Logic

The design operates in two selection levels.

### Level 1

`s0` selects one input from each pair:

```text
d0 / d1 → w0
d2 / d3 → w1
```

### Level 2

`s1` selects between the two intermediate signals:

```text
w0 / w1 → y
```

Therefore:

```text
                 s0
                  │
          ┌───────┴───────┐
          ▼               ▼
       d0 / d1         d2 / d3
          │               │
          ▼               ▼
         w0              w1
          │               │
          └───────┬───────┘
                  │
                 s1
                  │
                  ▼
                  y
```

---

# 🧮 Why Three 2:1 MUXes?

A 4:1 MUX requires three 2:1 MUXes when constructed hierarchically.

```text
4:1 MUX

       ┌───────┐
d0 ───►│       │
d1 ───►│ MUX 0 │───► w0
       └───────┘

       ┌───────┐
d2 ───►│       │
d3 ───►│ MUX 1 │───► w1
       └───────┘

       ┌───────┐
w0 ───►│       │
w1 ───►│ MUX 2 │───► y
       └───────┘
```

The general relationship for an `N:1` MUX constructed from 2:1 MUXes is:

```text
Number of 2:1 MUXes = N - 1
```

Therefore:

```text
4:1  → 3 × 2:1 MUXes
8:1  → 7 × 2:1 MUXes
16:1 → 15 × 2:1 MUXes
```

This demonstrates how larger digital circuits can be constructed from smaller reusable components.

---

# 🧠 Key Concepts Demonstrated

This project demonstrates several important digital-design concepts:

* Combinational logic
* Multiplexer architecture
* 2:1 MUX
* 4:1 MUX
* Truth tables
* Select-line logic
* Verilog HDL
* Ternary operator
* Structural Verilog
* Hierarchical design
* Module instantiation
* Testbench development
* Functional simulation
* XSim waveform analysis
* RTL schematic analysis
* FPGA pin constraints
* FPGA implementation
* GitHub project organization

---

# 🚀 Future Improvements

Possible extensions of this project include:

* [ ] Parameterized `N:1` MUX
* [ ] 8:1 MUX using 2:1 MUXes
* [ ] 16:1 MUX using 2:1 MUXes
* [ ] Gate-level implementation
* [ ] Timing analysis
* [ ] Resource utilization analysis
* [ ] Power analysis
* [ ] Comparison of behavioral vs structural Verilog
* [ ] Automated Vivado build flow
* [ ] Automated simulation scripts
* [ ] FPGA hardware demonstration video
* [ ] Interactive MUX visualization

---

# ✅ Project Checklist

* [x] Design 2:1 MUX
* [x] Build 4:1 MUX from 2:1 MUXes
* [x] Create hierarchical Verilog design
* [x] Create simulation testbench
* [x] Verify select combinations
* [x] Generate RTL schematic
* [x] Create XDC constraints
* [x] Synthesize the design
* [x] Implement the design
* [x] Create architecture diagram
* [x] Create animated signal-flow visualization
* [x] Organize project for GitHub
* [x] Document the complete design

---

# 📚 Learning Outcome

This project provides a practical introduction to **RTL design and FPGA-based digital logic development**.

The main takeaway is that complex combinational circuits can be designed by combining smaller, reusable modules.

In this case:

```text
       3 × 2:1 MUX
            │
            ▼
       ┌─────────┐
       │  4:1    │
       │  MUX    │
       └─────────┘
```

The design demonstrates the transition from:

```text
Digital Logic
      ↓
Verilog HDL
      ↓
Simulation
      ↓
RTL Schematic
      ↓
FPGA Constraints
      ↓
FPGA Implementation
```

---

# ⭐ Final Concept

The entire project can be summarized by three equations:

```verilog
w0 = s0 ? d1 : d0;

w1 = s0 ? d3 : d2;

y  = s1 ? w1 : w0;
```

And the selection behavior is:

```text
┌───────┬───────┬───────────────┐
│  s1   │  s0   │   Output      │
├───────┼───────┼───────────────┤
│   0   │   0   │     d0        │
│   0   │   1   │     d1        │
│   1   │   0   │     d2        │
│   1   │   1   │     d3        │
└───────┴───────┴───────────────┘
```

**Select → Route → Output.**

---

# 👨‍💻 Author

<p align="center">

<b>Urja Doshi</b>

<br>

Electronics & Communication Engineering

<br><br>

Digital Logic • Verilog • FPGA • VLSI

</p>

---

# ⭐ Support

If this project helped you understand **Multiplexers, Verilog HDL, structural design, or FPGA development**, consider giving the repository a ⭐.

---

<p align="center">

### 🔀 Select. Route. Output.

<b>Built with Verilog HDL and Xilinx Vivado.</b>

</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,100:0f2027&height=120&section=footer"/>
</p>
```

### Your final repository should therefore be

```text
vivado-4to1-mux-structural/
│
├── README.md
├── LICENSE
├── .gitignore
├── create_mux_animation.py
│
├── src/
│   ├── mux2to1.v
│   └── mux4_1.v
│
├── sim/
│   └── mux4_1tb.v
│
├── constraints/
│   └── mux4_1c.xdc
│
└── docs/
    ├── mux4_1-architecture.svg
    ├── mux4_1-logic-animation.gif
    ├── rtl-schematic.png
    ├── simulation-waveform.png
    └── fpga-hardware.svg
```

**One thing to verify before pushing:** make sure `src/mux4_1.v` really instantiates `mux2to1` three times. If it still contains only the three `assign ... ? ... : ...` statements from your original design, the README's “hierarchical structural” wording should be changed to match the actual implementation.
