from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PROJECT: AUTONOMOUS AI PILOT - MASTER MANIFEST', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Lead Integrator: Debanick Mukherjee', 0, 1, 'C')
        self.ln(5)

# Initialize PDF
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

manifest_data = [
    ("1. The Chassis", ["F450 Quadcopter Frame (Must include tall landing gear/skids)."]),
    ("2. The Brain & Data Bridge", ["Pixhawk 2.4.8 Kit (Include Power Module, Safety Switch, Buzzer).", "SiK Telemetry Radio Set - 433MHz."]),
    ("3. The Zero-Latency Vision System", ["Analog FPV Camera (1200TVL resolution).", "5.8GHz Analog VTX (Video Transmitter, 200mW+).", "5.8GHz UVC OTG Receiver (Eachine ROTG01 or Skydroid)."]),
    ("4. The Propulsion System", ["4x 2212 920KV Brushless Motors.", "4x 30A BLHeli or SimonK ESCs.", "1045 (10x4.5 inch) Propellers (Buy 3 sets)."]),
    ("5. The Power Station", ["3S (11.1V) LiPo Battery - 5000mAh to 5200mAh (XT60).", "IMAX B6 LiPo Balance Charger."]),
    ("6. The Manual Failsafe", ["FlySky FS-i6X with FS-iA6B Receiver."]),
    ("7. Assembly Consumables", ["Soldering Iron Kit & Rosin-core solder.", "Zip Ties.", "3M VHB Double-Sided Foam Tape.", "Heat Shrink Tubing."])
]

# Write data to PDF
for category, items in manifest_data:
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, category, 0, 1)
    pdf.set_font("Arial", '', 12)
    for item in items:
        pdf.cell(10) # Indent
        pdf.cell(0, 8, f"- [  ] {item}", 0, 1)
    pdf.ln(2)

# Save the file
output_filename = "Drone_Hardware_Manifest.pdf"
pdf.output(output_filename)

print(f"[SYSTEM] SUCCESS! {output_filename} has been generated in your current folder.")