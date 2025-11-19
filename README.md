# CWT Thread Verification System
# ระบบตรวจสอบความถูกต้องของด้ายสำหรับโรงงานอุตสาหกรรม

## 📋 Overview | ภาพรวม

A complete industrial thread verification system using RFID Kanban cards and dual QR-code scanners to ensure correct thread usage on sewing machines.

ระบบตรวจสอบความถูกต้องของด้ายสำหรับโรงงานอุตสาหกรรมโดยใช้การ์ด Kanban แบบ RFID และเครื่องอ่าน QR code แบบคู่เพื่อตรวจสอบการใช้ด้ายที่ถูกต้องบนจักรเย็บผ้า

## 🏗️ Project Structure | โครงสร้างโปรเจค

```
CWT-Thread-Verification/
├── machine/                    # ESP32 machine control system
│   ├── src/
│   │   └── main.cpp           # Main ESP32 firmware
│   ├── platformio.ini         # PlatformIO configuration
│   ├── README.md              # Machine system documentation
│   └── docs/
│       ├── SPEC.md            # Technical specification
│       ├── PINOUT.md          # Pin assignment table
│       └── HARDWARE.md        # Hardware requirements
│
├── kanban-tool/               # Python Kanban card writing tool
│   ├── main.py                # Main GUI application
│   ├── rfid_manager.py        # RFID operations
│   ├── gui.py                 # GUI components
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── README.md              # Tool documentation
│   └── docs/
│       ├── SPEC.md            # Program specification
│       ├── INSTALL.md         # Installation guide
│       └── USER_GUIDE.md      # User manual
│
└── docs/                      # Project documentation
    ├── OVERVIEW.md            # System overview
    ├── ARCHITECTURE.md        # Architecture design
    ├── DATA_FORMAT.md         # RFID data format
    └── WORKFLOW.md            # Complete workflow
```

## 🎯 Features | ฟีเจอร์หลัก

### Machine System (ESP32)
- ✅ RFID Kanban card reading (MFRC522)
- ✅ Dual QR-code scanning (GM65 scanners)
- ✅ Thread bobbin detection (proximity sensors)
- ✅ Visual feedback (Ready/Alarm LEDs)
- ✅ Machine output control (relay)
- ✅ Bypass mode support
- ✅ State machine logic

### Kanban Tool (Python)
- ✅ User-friendly GUI (Tkinter)
- ✅ RFID card writing (ACR122U)
- ✅ Thread code management
- ✅ Bypass mode support
- ✅ Card verification
- ✅ Windows compatible

## 🚀 Quick Start | เริ่มต้นใช้งาน

### Machine System

1. **Install PlatformIO:**
   ```bash
   # Install PlatformIO Core
   pip install platformio
   ```

2. **Build and Upload:**
   ```bash
   cd machine
   pio run --target upload
   ```

3. **Monitor Serial Output:**
   ```bash
   pio device monitor
   ```

### Kanban Tool

1. **Install Dependencies:**
   ```bash
   cd kanban-tool
   pip install -r requirements.txt
   ```

2. **Run Application:**
   ```bash
   python main.py
   ```

## 📖 Documentation | เอกสารประกอบ

### For Users | สำหรับผู้ใช้งาน
- [User Guide](kanban-tool/docs/USER_GUIDE.md) - Step-by-step instructions
- [Installation Guide](kanban-tool/docs/INSTALL.md) - Setup instructions

### For Developers | สำหรับนักพัฒนา
- [System Overview](docs/OVERVIEW.md) - High-level system design
- [Architecture](docs/ARCHITECTURE.md) - Technical architecture
- [Data Format](docs/DATA_FORMAT.md) - RFID data structure
- [Workflow](docs/WORKFLOW.md) - Complete system workflow
- [Machine Specification](machine/docs/SPEC.md) - ESP32 system details
- [Hardware Guide](machine/docs/HARDWARE.md) - Wiring and hardware setup

## 🔧 Hardware Requirements | อุปกรณ์ที่ต้องใช้

### Machine System
- ESP32 Feather board
- MFRC522 RFID reader
- 2x GM65 QR-code scanners
- 2x Proximity sensors (NPN/PNP)
- 4x LEDs (2 green, 2 red)
- 1x Relay module
- MIFARE Classic 1K cards

### Kanban Tool
- Windows PC
- ACR122U RFID reader/writer
- USB connection

## 🔄 Workflow | ขั้นตอนการทำงาน

1. **Write Kanban Card** - Use Kanban Tool to write thread codes to RFID card
2. **Present Card** - Operator places Kanban card on machine RFID reader
3. **Load Threads** - Operator loads thread bobbins on machine
4. **Automatic Verification** - System scans QR codes and compares with Kanban
5. **Machine Control** - System enables/disables machine based on verification

## 🛡️ Safety Features | ระบบความปลอดภัย

- Thread mismatch detection
- Dual verification (RFID + QR)
- Visual alerts (LED indicators)
- Machine lockout on error
- Bypass mode for special cases

## 📝 License | สัญญาอนุญาต

MIT License - see [LICENSE](LICENSE) file for details

## 👥 Contributing | การมีส่วนร่วม

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact | ติดต่อ

For questions or support, please open an issue on GitHub.

---

**Status:** Ready for hardware integration | พร้อมสำหรับการติดตั้งกับฮาร์ดแวร์

**Version:** 1.0.0

**Last Updated:** 2025-01-19
