# FPGA-Based Edge Detection (Sobel Filter)

**Target Hardware:** Basys3 FPGA (Artix-7)  
**FPGA Device:** xc7a35tcpg236-1  
**Tools:** Xilinx Vivado 2023.2  
**Language:** Verilog HDL  
**Verification:** Python (OpenCV, NumPy)

![Hardware Output](img/hardware_output.jpg)  
*Figure 1: Edge-detected output from Verilog behavioral simulation.*

---

## 📌 Project Overview

This project implements a hardware accelerator for real-time image edge detection using the **Sobel operator**. The design is written in synthesizable Verilog and targets the Basys3 FPGA development board.

A 3×3 sliding window convolution kernel computes horizontal ($G_x$) and vertical ($G_y$) image gradients.  

To reduce hardware complexity, the gradient magnitude is approximated as:

```
|G| ≈ |G_x| + |G_y|
```

This avoids square-root computation while maintaining high edge detection accuracy and significantly reducing resource utilization.

---

## 🧠 Architecture Summary

- 3×3 convolution engine  
- Horizontal and vertical gradient computation  
- Absolute value computation  
- Magnitude approximation logic  
- File-based memory interface for simulation  
- Bit-accurate Python golden reference model for verification  

---

## 📂 Repository Structure

```
├── src/
│   └── sobel_core.v
├── tb/
│   └── tb_sobel.v
├── scripts/
│   ├── img_to_hex.py
│   └── hex_to_img.py
├── docs/
│   └── waveform_reports/
├── img/
│   └── hardware_output.jpg
└── README.md
```

---

## 🚀 How to Run the Simulation

### Step 1: Generate Test Data

Convert a grayscale image into a hexadecimal memory file:

```bash
python scripts/img_to_hex.py
```

**Input:** Grayscale image (Recommended: 128×128 or 256×256)  
**Output:** `input_image.hex`

---

### Step 2: Run Behavioral Simulation in Vivado

1. Open **Xilinx Vivado 2023.2**
2. Create a new project targeting:
   ```
   xc7a35tcpg236-1
   ```
3. Add:
   - `src/sobel_core.v` → Design Sources
   - `tb/tb_sobel.v` → Simulation Sources
4. Copy `input_image.hex` into:

   ```
   project_name.sim/sim_1/behav/xsim/
   ```

5. Run **Behavioral Simulation**
6. Ensure the Tcl console prints:
   ```
   Simulation Complete
   ```

---

### Step 3: Verify Output

The simulation generates:

```
output_image.hex
```

Convert it back to an image:

```bash
python scripts/hex_to_img.py
```

Compare the result with the OpenCV Sobel output to confirm correctness.

---

## 📊 Results

| Stage | Description |
|-------|-------------|
| Input | Original grayscale image |
| Python Reference | OpenCV Sobel output (Golden Model) |
| Verilog Output | Cycle-accurate hardware simulation result |

The hardware output matches the software reference with 100% functional accuracy.

---

## ⚙️ Optimization Strategy

- Replaced square-root operation with magnitude approximation  
- Avoided multipliers where possible  
- Used absolute-value based arithmetic  
- Ensured synthesizable design practices  

This makes the design scalable for real-time embedded vision systems.

---

## 🛠 Future Work

- VGA Output Integration for real-time display  
- OV7670 Camera Module interface  
- Line buffer implementation for streaming architecture  
- Pipelined architecture for higher throughput  
- Resource utilization and timing optimization  

---

## 📌 Applications

- Real-time embedded vision systems  
- Edge AI preprocessing  
- Surveillance systems  
- Industrial inspection  
- Robotics perception pipelines  

---

## 👤 Author

Hari R.  
Final Year Electrical & Electronic Engineering Undergraduate  
University of Peradeniya  
[GitHub](https://github.com/HR-Hari)  |  [LinkedIn](https://www.linkedin.com/in/hariharasudan-ravichandran/)

