# 🔀 4:1 Multiplexer Using 2:1 MUX Logic — Verilog | Vivado

<p align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,100:2c5364&height=220&section=header&text=4:1%20Multiplexer&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=38" width="100%"/>

</p>

<p align="center">
  <b>A combinational 4:1 multiplexer implemented in Verilog HDL and prepared for FPGA synthesis using Xilinx Vivado.</b>
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

This project implements a **4:1 Multiplexer** using Verilog HDL.

A multiplexer is a combinational circuit that selects one input from several available inputs and forwards the selected value to a single output.

In this design:

* Four data inputs are used: `d0`, `d1`, `d2`, and `d3`
* Two select inputs are used: `s0` and `s1`
* One output is produced: `y`

The two select signals determine which data input is connected to the output.

The design is logically organized as **three 2:1 multiplexer operations**:

1. Select between `d0` and `d1`
2. Select between `d2` and `d3`
3. Select between the two intermediate results

This creates the complete functionality of a 4:1 multiplexer while clearly showing the internal selection stages.

---

## 🎯 Objectives

* Design a **4:1 Multiplexer** using **2:1 MUX logic**
* Implement the design using **Verilog HDL**
* Understand **combinational logic**
* Understand **continuous assignments**
* Use the Verilog **ternary/conditional operator**
* Understand internal signal/wire connections
* Verify functionality using a **Verilog testbench**
* Simulate the design using **Xilinx Vivado / XSim**
* Synthesize and implement the design for an FPGA
* Apply physical pin constraints using an **XDC file**
* Generate an FPGA bitstream

---

## 🧠 Multiplexer Operation

A 4:1 multiplexer has four data inputs and two select inputs.

The select inputs form a two-bit binary value. This value determines which data input is passed to the output.

### Truth Table

| `s1` | `s0` | Selected Input |  Output  |
| :--: | :--: | :------------: | :------: |
|   0  |   0  |      `d0`      | `y = d0` |
|   0  |   1  |      `d1`      | `y = d1` |
|   1  |   0  |      `d2`      | `y = d2` |
|   1  |   1  |      `d3`      | `y = d3` |

The lower select signal, `s0`, chooses between inputs within each pair.

The higher select signal, `s1`, chooses between the results of those two pairs.

---

## 🏗️ Internal Architecture

The design can be understood as a **two-level selection network**.

### First Selection Level

The first operation selects between the first pair of inputs:

```text
d0 ──┐
     ├──► mux_bottom
d1 ──┘
       ▲
       │
       s0
```

At the same time, another selection operates on the second pair:

```text
d2 ──┐
     ├──► mux_top
d3 ──┘
       ▲
       │
       s0
```

### Final Selection Level

The final operation selects between the two intermediate results:

```text
mux_bottom ──┐
              ├──► y
mux_top ──────┘
                ▲
                │
                s1
```

### Complete Logical Structure

```text
             s0
              │
       ┌──────┴──────┐
       │             │
   ┌───▼───┐     ┌───▼───┐
   │ 2:1   │     │ 2:1   │
   │ Logic │     │ Logic │
   └───┬───┘     └───┬───┘
       │               │
       │ mux_bottom    │ mux_top
       └───────┬───────┘
               │
           ┌───▼───┐
 s1 ──────►│ 2:1   │
           │ Logic │
           └───┬───┘
               │
               ▼
               y
```

---

## 💻 Verilog Design Concepts

The complete Verilog implementation is available in:

```text
src/mux4_1.v
```

Instead of reproducing the complete source code here, this section highlights the important Verilog concepts used in the design.

---

### ⏱️ Time Scale

The source begins with:

```verilog
`timescale 1ns / 1ps
```

This defines the simulation time unit and precision.

* `1ns` → simulation time unit
* `1ps` → simulation precision

Although the multiplexer itself does not use explicit delays, defining the time scale provides a consistent simulation environment.

---

### 🔌 Module and Ports

The top-level design is contained inside the `mux4_1` module.

Conceptually, its interface contains:

```text
Inputs  → d0, d1, d2, d3, s0, s1
Output  → y
```

All signals are **single-bit** because this project implements a one-bit 4:1 multiplexer.

The module interface allows Vivado to connect the logical signals to FPGA pins through the XDC constraints file.

---

## 🔗 Internal Wires

Two internal signals are used to store the results of the first-level selections:

```text
mux_bottom
mux_top
```

They allow the outputs of the first two selection operations to become inputs to the final selection operation.

Conceptually:

```text
d0,d1 ──► mux_bottom ──┐
                       ├──► y
d2,d3 ──► mux_top ─────┘
```

This demonstrates how intermediate signals can be used to construct larger combinational circuits.

---

## 🔀 Verilog Conditional / Ternary Operator

One of the most useful constructs in this design is the Verilog **conditional operator**, commonly called the **ternary operator**.

Its general syntax is:

```verilog
condition ? value_if_true : value_if_false
```

For example:

```verilog
mux_bottom = s0 ? d1 : d0;
```

This means:

```text
If s0 = 1 → mux_bottom = d1
If s0 = 0 → mux_bottom = d0
```

The same concept is used for the second input pair:

```text
mux_top = s0 ? d3 : d2
```

And finally:

```text
y = s1 ? mux_top : mux_bottom
```

### Why is this useful?

The ternary operator provides a compact way of describing a **2:1 multiplexer**:

```text
             ┌──────────────┐
a ──────────►│              │
b ──────────►│    2:1 MUX   ├──► y
sel ────────►│              │
             └──────────────┘
```

It is particularly useful for simple combinational selection logic.

---

## 🔄 Continuous Assignment

The design uses continuous assignments through the Verilog `assign` statement.

For example:

```verilog
assign y = condition ? b : a;
```

A continuous assignment continuously evaluates the right-hand expression and updates the output whenever an input changes.

This is appropriate for a combinational circuit because:

* No clock is required
* No storage is required
* The output responds to input changes
* The logic can be represented directly as a combinational relationship

---

## 🧩 Why `assign` Instead of an `always` Block?

A multiplexer can also be described using an `always` block.

For example, a conceptual equivalent could use:

```verilog
always @(*) begin
    ...
end
```

However, this project uses continuous assignments because the logic consists of direct combinational relationships.

The `assign` approach keeps the implementation compact and makes the selection behavior easy to identify.

---

## 🧮 Complete Selection Logic

The three logical selection stages can be summarized as:

```text
mux_bottom = s0 ? d1 : d0
mux_top    = s0 ? d3 : d2
y          = s1 ? mux_top : mux_bottom
```

Therefore:

```text
s1 s0
─────
0  0  → d0
0  1  → d1
1  0  → d2
1  1  → d3
```

The equivalent Boolean expression is:

```text
y = (~s1 & ~s0 & d0)
  | (~s1 &  s0 & d1)
  | ( s1 & ~s0 & d2)
  | ( s1 &  s0 & d3)
```

The conditional assignments provide the same functionality in a more compact form.

---

## 🧪 Verification

The design is verified using a dedicated Verilog testbench.

Testbench source:

```text
sim/mux4_1tb.v
```

The testbench applies combinations of the data and select inputs and observes the resulting output.

### Example Input Pattern

A useful test pattern is:

```verilog
d0 = 0;
d1 = 1;
d2 = 0;
d3 = 1;
```

With this pattern, changing the select signals makes it easy to observe whether the correct input is being routed to `y`.

### Expected Behavior

```text
s1 s0     y
──────────────
0  0      d0
0  1      d1
1  0      d2
1  1      d3
```

---

## 📊 Simulation

Simulation is performed using **Xilinx Vivado XSim**.

The waveform should demonstrate that `y` follows the selected data input whenever `s0` or `s1` changes.

### Simulation Waveform

Add the exported waveform screenshot to:

```text
docs/simulation-waveform.png
```

Then display it in the README:

<p align="center">

<img src="docs/simulation-waveform.png" alt="Simulation Waveform" width="850"/>

</p>

---

## 🔬 RTL Design

Vivado's RTL elaboration provides a visual representation of the synthesized logical structure.

The design consists of three logical 2:1 selection stages connected through intermediate signals.

### RTL Schematic

Place the exported Vivado RTL schematic at:

```text
docs/rtl-schematic.png
```

<p align="center">

<img src="docs/rtl-schematic.png" alt="RTL Schematic" width="850"/>

</p>

---

## ⚙️ FPGA Implementation

The design can be synthesized, implemented, and converted into an FPGA bitstream using Xilinx Vivado.

### Vivado Flow

```text
Create Project
      │
      ▼
Add Verilog Source
      │
      ▼
Add Simulation Source
      │
      ▼
Add XDC Constraints
      │
      ▼
Run Simulation
      │
      ▼
Elaborate RTL
      │
      ▼
Run Synthesis
      │
      ▼
Run Implementation
      │
      ▼
Generate Bitstream
      │
      ▼
Program FPGA
```

During synthesis, Vivado converts the Verilog description into FPGA-specific combinational logic.

---

## 📍 FPGA Pin Constraints

The project contains an XDC constraints file:

```text
constraints/mux4_1c.xdc
```

The constraints map the logical ports to physical FPGA package pins.

The project uses constraints for:

```text
d0
d1
d2
d3
s0
s1
y
```

A typical hardware configuration can connect:

```text
FPGA Switches ──► d0,d1,d2,d3
FPGA Switches ──► s0,s1
                     │
                     ▼
                   4:1 MUX
                     │
                     ▼
                    y
                     │
                     ▼
                   LED
```

> ⚠️ **Important:** FPGA pin assignments are board-specific. The provided XDC file should only be used with the target board for which it was created. For another FPGA board, the package pin assignments and I/O standards must be checked and updated.

---

## 🖥️ Hardware Demonstration

If a hardware photograph is available, place it at:

```text
docs/fpga-hardware.jpg
```

<p align="center">

<img src="docs/fpga-hardware.jpg" alt="FPGA Hardware Demonstration" width="700"/>

</p>

The hardware implementation allows the selection process to be observed directly using physical switches and an LED output.

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

Generated Vivado project files, simulation databases, synthesis artifacts, implementation files, and other temporary files are intentionally excluded from the repository.

---

## 🛠️ Tools & Technologies

| Tool / Technology          | Purpose                                    |
| :------------------------- | :----------------------------------------- |
| **Verilog HDL**            | Hardware description                       |
| **Xilinx Vivado**          | FPGA design, synthesis, and implementation |
| **XSim**                   | HDL simulation                             |
| **XDC**                    | FPGA pin and I/O constraints               |
| **FPGA Development Board** | Hardware testing                           |
| **Git & GitHub**           | Version control and documentation          |

---

## 🔍 Design Characteristics

| Characteristic   | Description              |
| :--------------- | :----------------------- |
| Logic Type       | Combinational            |
| Data Inputs      | 4                        |
| Select Inputs    | 2                        |
| Output           | 1                        |
| Clock            | Not required             |
| Reset            | Not required             |
| Storage          | None                     |
| Internal Signals | 2                        |
| Selection Stages | 3 logical 2:1 operations |
| HDL              | Verilog                  |
| Simulation       | XSim                     |
| FPGA Tool        | Xilinx Vivado            |

---

## ✅ Verification Checklist

* [x] 4:1 MUX logic implemented
* [x] Three logical 2:1 selection stages
* [x] Combinational implementation
* [x] Continuous assignments
* [x] Conditional / ternary operator
* [x] Verilog testbench
* [x] Functional simulation
* [x] RTL elaboration
* [x] Synthesis
* [x] Implementation
* [x] FPGA constraints
* [x] Bitstream generation

---

## 🚀 Possible Future Improvements

* [ ] Add a self-checking testbench
* [ ] Create a reusable `mux2to1` module
* [ ] Implement an 8:1 MUX using 2:1 MUXes
* [ ] Implement a 16:1 MUX using hierarchical design
* [ ] Create a parameterized N:1 multiplexer
* [ ] Implement the design using SystemVerilog
* [ ] Add timing and utilization analysis
* [ ] Add automated HDL simulation scripts
* [ ] Add FPGA hardware demonstration video
* [ ] Compare behavioral and structural implementations

---

## 📚 Learning Outcomes

This project demonstrates practical understanding of:

* Combinational digital logic
* Multiplexer architecture
* Select-line operation
* Hierarchical selection concepts
* Verilog module design
* Internal wire connections
* Continuous assignments
* Conditional / ternary operators
* Testbench development
* Simulation and waveform analysis
* RTL elaboration
* FPGA synthesis
* FPGA implementation
* XDC pin constraints
* Bitstream generation
* GitHub project organization

---

## 👨‍💻 Author

**Atharva Chaudhari, Arya Chawale, Jayesh Shahare, Urja Doshi**

Electronics & Telecommunication Engineering

---

## ⭐ Support

If this project helped you understand Verilog, multiplexers, or FPGA design, consider giving the repository a ⭐ on GitHub.

---

<p align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,100:0f2027&height=120&section=footer" width="100%"/>

</p>
