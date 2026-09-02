# 🔀 4:1 Multiplexer Using 2:1 MUXes — Verilog | Vivado

<p align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,100:2c5364&height=220&section=header&text=4:1%20MUX%20Using%202:1%20MUXes&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=38" width="100%"/>

</p>

<p align="center">
  <b>A hierarchical structural Verilog implementation of a 4:1 Multiplexer using three 2:1 Multiplexer modules.</b>
</p>

<p align="center">

![Verilog](https://img.shields.io/badge/HDL-Verilog-1f425f?style=for-the-badge\&logo=verilog)
![Xilinx Vivado](https://img.shields.io/badge/Xilinx-Vivado-red?style=for-the-badge)
![FPGA](https://img.shields.io/badge/Target-FPGA-blue?style=for-the-badge)
![Simulation](https://img.shields.io/badge/Simulation-XSim-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</p>

---

## 📌 Project Overview

This project implements a **4:1 Multiplexer (MUX)** using **three 2:1 Multiplexer modules** in **structural Verilog HDL**.

The design follows a two-stage hierarchical architecture:

```text
                 ┌─────────────┐
        d0 ─────►│             │
        d1 ─────►│   2:1 MUX   │──── w0 ────┐
        s0 ─────►│     M0      │             │
                 └─────────────┘             │
                                             ▼
                                         ┌─────────────┐
                 ┌─────────────┐         │             │
        d2 ─────►│             │         │   2:1 MUX   │────► y
        d3 ─────►│   2:1 MUX   │──── w1 ─►│     M2      │
        s0 ─────►│     M1      │         │             │
                 └─────────────┘         └──────┬──────┘
                                                ▲
                                                │
                                               s1
```

The first stage selects between pairs of inputs using `s0`.

The second stage selects between the two intermediate outputs using `s1`.

---

## 🎯 Objectives

* Design a **4:1 Multiplexer** using **2:1 MUX building blocks**
* Implement the design using **structural Verilog**
* Understand **hierarchical module instantiation**
* Verify functionality using a **Verilog testbench**
* Simulate the design using **Xilinx Vivado / XSim**
* Synthesize and implement the design for an FPGA
* Apply physical pin constraints using an **XDC file**
* Generate an FPGA bitstream

---

## 🧠 What is a Multiplexer?

A **Multiplexer (MUX)** is a combinational digital circuit that selects one input from multiple inputs and forwards it to a single output.

For a **4:1 MUX**:

* Data inputs → `d0`, `d1`, `d2`, `d3`
* Select inputs → `s0`, `s1`
* Output → `y`

The selected input depends on the two select lines.

### Truth Table

| `s1` | `s0` | Selected Input |  Output  |
| :--: | :--: | :------------: | :------: |
|   0  |   0  |      `d0`      | `y = d0` |
|   0  |   1  |      `d1`      | `y = d1` |
|   1  |   0  |      `d2`      | `y = d2` |
|   1  |   1  |      `d3`      | `y = d3` |

---

## 🏗️ Architecture

The 4:1 MUX is constructed using **three 2:1 MUXes**.

### Stage 1

Two 2:1 MUXes operate in parallel:

```text
M0:
d0 ──┐
     ├──► w0
d1 ──┘
       ▲
       │
       s0
```

```text
M1:
d2 ──┐
     ├──► w1
d3 ──┘
       ▲
       │
       s0
```

### Stage 2

A third 2:1 MUX selects between `w0` and `w1`:

```text
w0 ──┐
     ├──► y
w1 ──┘
       ▲
       │
       s1
```

Therefore:

```text
             s0
              │
       ┌──────┴──────┐
       │             │
   ┌───▼───┐     ┌───▼───┐
   │ 2:1   │     │ 2:1   │
   │ MUX M0│     │ MUX M1│
   └───┬───┘     └───┬───┘
       │ w0           │ w1
       └──────┬───────┘
              │
          ┌───▼───┐
 s1 ─────►│ 2:1   │
          │ MUX M2│
          └───┬───┘
              │
              ▼
              y
```

---

## 💻 Verilog Implementation

### 2:1 Multiplexer

`src/mux2to1.v`

```verilog
module mux2to1 (
    input  a,
    input  b,
    input  sel,
    output y
);

assign y = sel ? b : a;

endmodule
```

---

### 4:1 Multiplexer

`src/mux4_1.v`

```verilog
module mux4_1 (
    input  d0,
    input  d1,
    input  d2,
    input  d3,
    input  s0,
    input  s1,
    output y
);

wire w0;
wire w1;

// First stage
mux2to1 m0 (
    .a   (d0),
    .b   (d1),
    .sel (s0),
    .y   (w0)
);

mux2to1 m1 (
    .a   (d2),
    .b   (d3),
    .sel (s0),
    .y   (w1)
);

// Second stage
mux2to1 m2 (
    .a   (w0),
    .b   (w1),
    .sel (s1),
    .y   (y)
);

endmodule
```

---

## 🧪 Verification

The design is verified using a Verilog testbench.

The testbench applies different combinations of:

* `d0`
* `d1`
* `d2`
* `d3`
* `s0`
* `s1`

and checks whether the output `y` corresponds to the expected selected input.

### Example Test Sequence

```text
s1 s0
─────
0  0   → d0
0  1   → d1
1  0   → d2
1  1   → d3
```

A simple input pattern can be used:

```verilog
d0 = 0;
d1 = 1;
d2 = 0;
d3 = 1;
```

This allows the four select combinations to produce easily distinguishable outputs.

---

## 📊 Simulation

Simulation is performed using **Xilinx Vivado XSim**.

The expected behavior is:

```text
Select = 00  → y = d0
Select = 01  → y = d1
Select = 10  → y = d2
Select = 11  → y = d3
```

### Simulation Waveform

Add your exported waveform screenshot here:

```text
docs/simulation-waveform.png
```

Then it can be displayed using:

```markdown
![Simulation Waveform](docs/simulation-waveform.png)
```

<p align="center">

![Simulation Waveform](docs/simulation-waveform.png)

</p>

---

## 🔬 RTL Design

The synthesized RTL architecture consists of three 2:1 MUX blocks connected in a two-level structure.

### RTL Schematic

Place your Vivado RTL schematic screenshot at:

```text
docs/rtl-schematic.png
```

Then it will appear here:

<p align="center">

![RTL Schematic](docs/rtl-schematic.png)

</p>

---

## ⚙️ FPGA Implementation

The project can be synthesized, implemented, and generated as an FPGA bitstream using **Xilinx Vivado**.

### Vivado Flow

```text
Create Project
      │
      ▼
Add Verilog Sources
      │
      ▼
Add Simulation Sources
      │
      ▼
Add XDC Constraints
      │
      ▼
Run Simulation
      │
      ▼
RTL Elaboration
      │
      ▼
Synthesis
      │
      ▼
Implementation
      │
      ▼
Generate Bitstream
      │
      ▼
Program FPGA
```

---

## 📍 Pin Constraints

The project contains an XDC constraints file:

```text
constraints/mux4_1c.xdc
```

The XDC file assigns FPGA package pins to:

```text
d0
d1
d2
d3
s0
s1
y
```

> ⚠️ **Important:** FPGA pin assignments are board-specific. The provided XDC file should only be used with the FPGA development board for which it was created. For another board, replace the package-pin and I/O-standard constraints accordingly.

---

## 📁 Repository Structure

```text
vivado-4to1-mux-structural/
│
├── 📄 README.md
├── 📄 LICENSE
├── 📄 .gitignore
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
    ├── rtl-schematic.png
    ├── simulation-waveform.png
    └── fpga-hardware.jpg
```

---

## 🛠️ Tools & Technologies

| Tool / Technology          | Purpose                             |
| -------------------------- | ----------------------------------- |
| **Verilog HDL**            | Hardware description                |
| **Xilinx Vivado**          | FPGA design and synthesis           |
| **XSim**                   | HDL simulation                      |
| **XDC**                    | FPGA pin constraints                |
| **FPGA Development Board** | Hardware implementation             |
| **Git & GitHub**           | Version control and project hosting |

---

## 🔍 Verification Checklist

* [x] 2:1 MUX module implemented
* [x] 4:1 MUX constructed using three 2:1 MUXes
* [x] Hierarchical structural design
* [x] Verilog testbench
* [x] Functional simulation
* [x] RTL elaboration
* [x] Synthesis
* [x] Implementation
* [x] FPGA constraints
* [x] Bitstream generation

---

## 📈 Design Logic

The overall functionality can be represented as:

```text
w0 = s0 ? d1 : d0
w1 = s0 ? d3 : d2
y  = s1 ? w1 : w0
```

Therefore:

```text
s1 s0     y
──────────────
0  0      d0
0  1      d1
1  0      d2
1  1      d3
```

---

## 🚀 Future Improvements

Possible extensions of this project include:

* [ ] Parameterized N:1 multiplexer
* [ ] 8:1 MUX using 2:1 MUXes
* [ ] 16:1 MUX using hierarchical design
* [ ] SystemVerilog implementation
* [ ] Self-checking testbench
* [ ] Automated simulation scripts
* [ ] FPGA hardware demonstration video
* [ ] Timing and resource utilization analysis
* [ ] CI-based HDL simulation

---

## 📚 Learning Outcomes

Through this project, the following concepts are demonstrated:

* Combinational digital logic
* Multiplexer design
* Structural Verilog
* Module instantiation
* Hierarchical hardware design
* Testbench development
* Simulation and waveform analysis
* RTL elaboration
* FPGA synthesis
* FPGA implementation
* Pin constraints
* Bitstream generation
* Git/GitHub project organization

---

## 👨‍💻 Author

**Urja Doshi**

Electronics & Communication Engineering

---

## ⭐ Support

If this project helped you understand hierarchical Verilog design or FPGA development, consider giving the repository a ⭐ on GitHub.

---

<p align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,100:0f2027&height=120&section=footer" width="100%"/>

</p>
