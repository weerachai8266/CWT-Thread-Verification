# System Architecture
# สถาปัตยกรรมระบบ

## High-Level Architecture | สถาปัตยกรรมระดับสูง

```
┌────────────────────────────────────────────────────────────┐
│                     CWT SYSTEM                             │
│                                                            │
│  ┌──────────────────┐         ┌─────────────────────┐    │
│  │  Kanban Tool     │         │   Machine System    │    │
│  │  (Python/PC)     │         │   (ESP32/Embedded)  │    │
│  │                  │         │                     │    │
│  │  ┌────────────┐  │         │  ┌──────────────┐  │    │
│  │  │    GUI     │  │         │  │ State Machine│  │    │
│  │  │  (Tkinter) │  │         │  │   Controller │  │    │
│  │  └─────┬──────┘  │         │  └───────┬──────┘  │    │
│  │        │         │         │          │         │    │
│  │  ┌─────▼──────┐  │         │  ┌───────▼──────┐  │    │
│  │  │RFID Manager│  │         │  │RFID+QR+Sensor│  │    │
│  │  │ (pyscard)  │  │         │  │   Drivers    │  │    │
│  │  └─────┬──────┘  │         │  └───────┬──────┘  │    │
│  │        │         │         │          │         │    │
│  │  ┌─────▼──────┐  │         │  ┌───────▼──────┐  │    │
│  │  │ ACR122U    │  │         │  │   Hardware   │  │    │
│  │  │  Reader    │  │         │  │  Interfaces  │  │    │
│  │  └─────┬──────┘  │         │  └───────┬──────┘  │    │
│  └────────┼─────────┘         └──────────┼─────────┘    │
│           │                              │              │
│           ▼                              ▼              │
│    ┌──────────────┐            ┌──────────────────┐    │
│    │ MIFARE Card  │            │  Physical I/O    │    │
│    │  (Kanban)    │            │  - RFID Reader   │    │
│    └──────────────┘            │  - QR Scanners   │    │
│                                │  - Sensors       │    │
│                                │  - LEDs          │    │
│                                │  - Relay         │    │
│                                └──────────────────┘    │
└────────────────────────────────────────────────────────────┘
```

## Component Architecture | สถาปัตยกรรมส่วนประกอบ

### 1. Kanban Tool Architecture | สถาปัตยกรรมเครื่องมือ Kanban

```
┌─────────────────────────────────────────────────┐
│              Application Layer                  │
│  ┌───────────────────────────────────────────┐  │
│  │         KanbanToolApp                     │  │
│  │  - Application Controller                │  │
│  │  - Event Coordination                    │  │
│  │  - Error Handling                        │  │
│  └───────────┬─────────────┬─────────────────┘  │
│              │             │                     │
├──────────────┼─────────────┼─────────────────────┤
│              │             │                     │
│  ┌───────────▼──────┐  ┌───▼──────────────────┐ │
│  │   KanbanGUI      │  │   RFIDManager        │ │
│  │                  │  │                      │ │
│  │  - Tkinter UI    │  │  - Card Operations   │ │
│  │  - User Input    │  │  - APDU Commands     │ │
│  │  - Display       │  │  - Authentication    │ │
│  │  - Logging       │  │  - Read/Write        │ │
│  └───────────┬──────┘  └───┬──────────────────┘ │
│              │             │                     │
├──────────────┼─────────────┼─────────────────────┤
│              │             │                     │
│  ┌───────────▼─────────────▼──────────────────┐ │
│  │          Configuration (config.py)         │ │
│  │  - Block Assignments                       │ │
│  │  - Keys                                    │ │
│  │  - UI Settings                             │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
├──────────────────────────────────────────────────┤
│           Hardware Abstraction Layer             │
│  ┌────────────────────────────────────────────┐ │
│  │        pyscard Library                     │ │
│  │  - PC/SC Interface                         │ │
│  │  - Smart Card API                          │ │
│  │  - Reader Management                       │ │
│  └────────────────┬───────────────────────────┘ │
│                   │                              │
├───────────────────┼──────────────────────────────┤
│                   │                              │
│  ┌────────────────▼───────────────────────────┐ │
│  │      PC/SC Service (Windows)               │ │
│  └────────────────┬───────────────────────────┘ │
│                   │                              │
├───────────────────┼──────────────────────────────┤
│                   │                              │
│  ┌────────────────▼───────────────────────────┐ │
│  │       ACR122U USB Driver                   │ │
│  └────────────────┬───────────────────────────┘ │
│                   │                              │
└───────────────────┼──────────────────────────────┘
                    │
            ┌───────▼────────┐
            │   ACR122U      │
            │   Hardware     │
            └────────────────┘
```

### 2. Machine System Architecture | สถาปัตยกรรมระบบเครื่องจักร

```
┌─────────────────────────────────────────────────┐
│           Application Layer (ESP32)             │
│  ┌───────────────────────────────────────────┐  │
│  │         Main Loop                         │  │
│  │  - State Machine Execution                │  │
│  │  - Timing Control                         │  │
│  └───────────────┬───────────────────────────┘  │
│                  │                               │
│  ┌───────────────▼───────────────────────────┐  │
│  │      State Machine Controller             │  │
│  │                                           │  │
│  │  States:                                  │  │
│  │  - WAIT_KANBAN                            │  │
│  │  - READ_KANBAN                            │  │
│  │  - WAIT_BOBBINS                           │  │
│  │  - SCAN_QR1                               │  │
│  │  - SCAN_QR2                               │  │
│  │  - VERIFY                                 │  │
│  │  - READY                                  │  │
│  │  - ERROR                                  │  │
│  │  - BYPASS                                 │  │
│  └───┬─────┬─────┬─────┬─────┬─────┬─────┬──┘  │
│      │     │     │     │     │     │     │     │
├──────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│      │     │     │     │     │     │     │     │
│  ┌───▼──┐ ┌▼───┐ ┌▼──┐ ┌▼──┐ ┌▼──┐ ┌▼──┐ ┌▼──┐ │
│  │RFID  │ │QR1 │ │QR2│ │Sen│ │LED│ │Rel│ │Log│ │
│  │Mgr   │ │Mgr │ │Mgr│ │sor│ │Mgr│ │ay │ │ger│ │
│  └───┬──┘ └┬───┘ └┬──┘ └┬──┘ └┬──┘ └┬──┘ └─┬─┘ │
│      │     │     │     │     │     │      │   │
├──────┼─────┼─────┼─────┼─────┼─────┼──────┼───┤
│      │     │     │     │     │     │      │   │
│  ┌───▼──┐ ┌▼───┐ ┌▼──┐ ┌▼──┐ ┌▼──┐ ┌▼──┐  │   │
│  │MFRC  │ │Soft│ │Soft│ │GPIO│GPIO│GPIO│  │   │
│  │522   │ │Ser1│ │Ser2│ │Read│Wrt│Wrt│  │   │
│  │(SPI) │ │(U1)│ │(U2)│ │    │   │   │  │   │
│  └───┬──┘ └┬───┘ └┬──┘ └┬──┘ └┬──┘ └┬──┘  │   │
│      │     │     │     │     │     │      │   │
├──────┼─────┼─────┼─────┼─────┼─────┼──────┼───┤
│      │     │     │     │     │     │      │   │
│  Hardware Interfaces                      │   │
│  - SPI Bus                                │   │
│  - UART1, UART2                           │   │
│  - GPIO Pins                              │   │
│  - Serial Console ◄───────────────────────┘   │
│                                                │
└────────┬─────┬─────┬─────┬─────┬─────┬─────────┘
         │     │     │     │     │     │
    ┌────▼──┐ ┌▼──┐ ┌▼──┐ ┌▼──┐ ┌▼──┐ ┌▼──┐
    │MFRC522│ │GM65│ │GM65│ │Prox│ │LED│ │Rel│
    │Reader │ │QR#1│ │QR#2│ │Sen │ │(4)│ │ay │
    └───────┘ └───┘ └───┘ └────┘ └───┘ └───┘
```

## Data Flow Architecture | สถาปัตยกรรมการไหลของข้อมูล

### Write Kanban Flow | การไหลของข้อมูลการเขียน Kanban

```
[User Input]
    │
    ├─ Thread1: "TH-001"
    └─ Thread2: "TH-002"
    │
    ▼
[GUI Validation]
    │
    ├─ Length Check (≤16 chars)
    ├─ Character Check (ASCII only)
    └─ Non-empty Check
    │
    ▼
[RFIDManager.write_kanban()]
    │
    ├─ Convert to bytes
    ├─ Pad to 16 bytes
    │
    ▼
[Wait for Card]
    │
    └─ Timeout: 10 seconds
    │
    ▼
[Authenticate Block 4]
    │
    ├─ Load Key A
    └─ Authenticate
    │
    ▼
[Write Block 4]
    │
    └─ APDU: FF D6 00 04 10 [16 bytes]
    │
    ▼
[Authenticate Block 5]
    │
    ├─ Load Key A
    └─ Authenticate
    │
    ▼
[Write Block 5]
    │
    └─ APDU: FF D6 00 05 10 [16 bytes]
    │
    ▼
[Verify Data]
    │
    ├─ Read back Block 4
    ├─ Read back Block 5
    ├─ Compare with expected
    │
    ▼
[Result]
    │
    ├─ SUCCESS → Show dialog
    └─ FAILURE → Show error
```

### Machine Verification Flow | การไหลของข้อมูลการตรวจสอบ

```
[WAIT_KANBAN State]
    │
    ▼
[RFID Card Detected]
    │
    ▼
[READ_KANBAN State]
    │
    ├─ Authenticate Block 4
    ├─ Read Thread1
    ├─ Authenticate Block 5
    ├─ Read Thread2
    ├─ Parse strings
    │
    ├─ If "bypass" → BYPASS State
    │
    ▼
[WAIT_BOBBINS State]
    │
    ├─ Read Sensor 1
    ├─ Read Sensor 2
    ├─ Debounce (50ms)
    │
    ├─ If both detected → Continue
    ├─ If timeout (30s) → ERROR State
    │
    ▼
[SCAN_QR1 State]
    │
    ├─ Trigger QR Scanner 1
    ├─ Wait for data (5s timeout)
    ├─ Parse QR code string
    │
    ├─ If success → Continue
    ├─ If failure → ERROR State
    │
    ▼
[SCAN_QR2 State]
    │
    ├─ Trigger QR Scanner 2
    ├─ Wait for data (5s timeout)
    ├─ Parse QR code string
    │
    ├─ If success → Continue
    ├─ If failure → ERROR State
    │
    ▼
[VERIFY State]
    │
    ├─ Compare QR1 with Thread1
    ├─ Compare QR2 with Thread2
    │
    ├─ If both match → READY State
    ├─ If mismatch → ERROR State
    │
    ▼
[READY State]
    │
    ├─ Set LEDs: Green ON, Red OFF
    ├─ Set Relay: ON (Machine Enabled)
    ├─ Monitor card presence
    │
    ├─ If card removed → WAIT_KANBAN State
    │
[ERROR State]
    │
    ├─ Set LEDs: Green OFF, Red BLINK
    ├─ Set Relay: OFF (Machine Disabled)
    ├─ Monitor card presence
    │
    ├─ If card removed → WAIT_KANBAN State
```

## Communication Protocols | โปรโตคอลการสื่อสาร

### PC/SC Protocol Stack (Kanban Tool)

```
┌─────────────────────────────────────┐
│   Application (Python)              │
├─────────────────────────────────────┤
│   pyscard API                       │
├─────────────────────────────────────┤
│   PC/SC Lite / Winscard             │
├─────────────────────────────────────┤
│   USB CCID Driver                   │
├─────────────────────────────────────┤
│   USB Protocol                      │
├─────────────────────────────────────┤
│   ACR122U Firmware                  │
├─────────────────────────────────────┤
│   ISO 14443-3 (RFID Protocol)       │
├─────────────────────────────────────┤
│   MIFARE Classic Protocol           │
└─────────────────────────────────────┘
```

### ESP32 Protocol Stack (Machine System)

```
┌─────────────────────────────────────┐
│   Application (Arduino C++)         │
├─────────────────────────────────────┤
│   MFRC522 Library                   │
│   SoftwareSerial Library            │
├─────────────────────────────────────┤
│   Arduino Framework                 │
├─────────────────────────────────────┤
│   ESP-IDF (ESP32 SDK)               │
├─────────────────────────────────────┤
│   Hardware Peripherals:             │
│   - SPI Driver                      │
│   - UART Driver                     │
│   - GPIO Driver                     │
└─────────────────────────────────────┘
```

## Interface Specifications | ข้อมูลจำเพาะอินเทอร์เฟส

### RFID Interface (SPI)

```
Protocol: SPI Mode 0
Clock: 10 MHz (max)
Data: 8-bit
Chip Select: Active LOW
Data Direction: Full-duplex

Pin Mapping:
ESP32          MFRC522
GPIO 18   →    SCK
GPIO 23   →    MOSI
GPIO 19   ←    MISO
GPIO 5    →    SDA (CS)
GPIO 22   →    RST
```

### QR Scanner Interface (UART)

```
Protocol: UART (Asynchronous Serial)
Baud Rate: 9600 bps
Data Bits: 8
Parity: None
Stop Bits: 1
Flow Control: None

Data Format:
[QR Code Data]\r\n
- Variable length (up to 256 bytes)
- ASCII string
- Terminated with CR+LF

Trigger Signal:
- GPIO pulse (100ms minimum)
- Active HIGH
- 3.3V or 5V compatible
```

### Sensor Interface (GPIO)

```
Type: Digital Input
Voltage: 3.3V logic
Pull: Internal pull-up enabled
Active: LOW (for NPN sensors)
Debounce: 50ms software debounce

Reading Logic:
LOW  = Object detected
HIGH = No object
```

### LED Interface (GPIO)

```
Type: Digital Output
Voltage: 3.3V logic
Current: 20mA max (with resistor)
Resistor: 220Ω (current limiting)

Control Logic:
HIGH = LED ON
LOW  = LED OFF
```

### Relay Interface (GPIO)

```
Type: Digital Output  
Voltage: 3.3V logic
Module: 5V relay with optocoupler
Control: Active HIGH

Isolation: Optocoupler (1000V+)
Contact Rating: 10A @ 250V AC
```

## Security Architecture | สถาปัตยกรรมความปลอดภัย

### Card Security | ความปลอดภัยของการ์ด

```
┌─────────────────────────────────────┐
│   MIFARE Classic 1K Card            │
│                                     │
│   Sector 0:                         │
│   ├─ Block 0: UID (Read-Only)       │
│   ├─ Block 1: Data                  │
│   ├─ Block 2: Data                  │
│   └─ Block 3: Keys + Access Bits    │
│                                     │
│   Sector 1:                         │
│   ├─ Block 4: Thread1 ◄─── Used    │
│   ├─ Block 5: Thread2 ◄─── Used    │
│   ├─ Block 6: Data                  │
│   └─ Block 7: Keys + Access Bits    │
│                                     │
│   Security:                         │
│   ├─ Key A: FF FF FF FF FF FF       │
│   │   (Default - should change)     │
│   ├─ Key B: Not used                │
│   └─ Access Bits: Default           │
└─────────────────────────────────────┘
```

### System Security Layers | ชั้นความปลอดภัยของระบบ

```
Layer 1: Physical Security
├─ Card holder custody
├─ Reader access control
└─ Bypass card storage

Layer 2: Logical Security
├─ MIFARE authentication
├─ Block access control
└─ Data validation

Layer 3: Application Security
├─ Input validation
├─ Error handling
└─ Logging/audit trail

Layer 4: Network Security (Future)
├─ Encrypted communication
├─ User authentication
└─ Access control lists
```

## Deployment Architecture | สถาปัตยกรรมการติดตั้ง

### Single Machine Deployment | การติดตั้งเครื่องเดียว

```
┌──────────────────────────────────────┐
│   Supervisor Office                  │
│                                      │
│   ┌────────────────────────┐         │
│   │   PC with Kanban Tool  │         │
│   │   + ACR122U Reader     │         │
│   └────────────────────────┘         │
│             │                        │
│             │ Kanban Cards           │
│             ▼                        │
└─────────────┼────────────────────────┘
              │
              │
┌─────────────┼────────────────────────┐
│             │                        │
│   ┌─────────▼──────────┐             │
│   │  Sewing Machine    │             │
│   │  + ESP32 System    │             │
│   │  + Sensors         │             │
│   └────────────────────┘             │
│                                      │
│   Production Floor                   │
└──────────────────────────────────────┘
```

### Multiple Machine Deployment | การติดตั้งหลายเครื่อง

```
┌──────────────────────────────────────┐
│   Central Office                     │
│                                      │
│   ┌────────────────────────┐         │
│   │  Shared Kanban Tool PC │         │
│   │  + ACR122U Reader      │         │
│   └────────────────────────┘         │
│             │                        │
│             │ Distribute Cards       │
│             ▼                        │
└─────────────┼────────────────────────┘
              │
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
┌───▼───┐ ┌──▼────┐ ┌──▼────┐ ┌──▼────┐
│Machine│ │Machine│ │Machine│ │Machine│
│   #1  │ │   #2  │ │   #3  │ │   #4  │
│ESP32  │ │ESP32  │ │ESP32  │ │ESP32  │
└───────┘ └───────┘ └───────┘ └───────┘

Each machine operates independently
Shared thread code standards
Common Kanban management
```

### Future: Network Architecture | อนาคต: สถาปัตยกรรมเครือข่าย

```
┌──────────────────────────────────────┐
│   Cloud / Central Server             │
│   ┌────────────────────────┐         │
│   │  Database              │         │
│   │  - Thread Inventory    │         │
│   │  - Production Logs     │         │
│   │  - Analytics           │         │
│   └────────────────────────┘         │
└─────────────┬────────────────────────┘
              │ WiFi/Ethernet
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
┌───▼───┐ ┌──▼────┐ ┌──▼────┐ ┌──▼────┐
│Machine│ │Machine│ │Kanban │ │Mobile │
│ESP32  │ │ESP32  │ │Tool PC│ │ App   │
│(WiFi) │ │(WiFi) │ │       │ │       │
└───────┘ └───────┘ └───────┘ └───────┘
```

## Scalability Considerations | ข้อพิจารณาการขยายระบบ

### Vertical Scaling (Single Machine) | การขยายแนวตั้ง

- ✅ Add more thread positions (4, 6, 8 threads)
- ✅ Additional sensors and scanners
- ✅ More complex verification logic
- ✅ Enhanced reporting features

### Horizontal Scaling (Multiple Machines) | การขยายแนวนอน

- ✅ Independent operation per machine
- ✅ Shared Kanban tool and cards
- ✅ Standardized thread codes
- ✅ Centralized management (future)

### Integration Scaling | การขยายการเชื่อมต่อ

- ✅ MES integration
- ✅ ERP synchronization
- ✅ Inventory management
- ✅ Quality tracking systems

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-19  
**Author:** CWT Team
