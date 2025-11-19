# Machine System Documentation
# ระบบควบคุมเครื่องจักร ESP32

## Overview | ภาพรวม

The Machine System is the core component that runs on the ESP32 microcontroller and controls the thread verification process on the sewing machine.

ระบบควบคุมเครื่องจักรเป็นส่วนหลักที่ทำงานบนไมโครคอนโทรลเลอร์ ESP32 และควบคุมกระบวนการตรวจสอบด้ายบนจักรเย็บผ้า

## Features | คุณสมบัติ

- **RFID Card Reading** - Reads Kanban cards using MFRC522 reader
- **Dual QR Scanning** - Scans thread QR codes using two GM65 scanners
- **Bobbin Detection** - Detects thread bobbin presence with proximity sensors
- **Visual Feedback** - Provides status through LED indicators
- **Machine Control** - Enables/disables machine operation via relay
- **Bypass Mode** - Special mode to bypass verification when needed

## Hardware Requirements | อุปกรณ์ที่ต้องใช้

### Core Components | อุปกรณ์หลัก

1. **ESP32 Feather Board** (or compatible)
2. **MFRC522 RFID Reader Module** (13.56 MHz)
3. **2x GM65 QR Code Scanner Modules** (UART interface)
4. **2x Proximity Sensors** (NPN or PNP, 5-24V DC)
5. **4x LEDs** (2 green for ready, 2 red for alarm)
6. **1x Relay Module** (5V, for machine control)
7. **MIFARE Classic 1K Cards** (for Kanban)
8. **Resistors** (220Ω for LEDs)
9. **Power Supply** (5V DC, minimum 2A)

### Connection Overview | ภาพรวมการต่อสาย

See [PINOUT.md](docs/PINOUT.md) for complete pin assignment table.
See [HARDWARE.md](docs/HARDWARE.md) for detailed wiring instructions.

## Building and Uploading | การคอมไพล์และอัพโหลด

### Prerequisites | สิ่งที่ต้องมี

1. Install [PlatformIO](https://platformio.org/install)
2. Install USB driver for ESP32 (CP2104 or CH340)

### Build Process | กระบวนการคอมไพล์

```bash
cd machine
pio run
```

### Upload Firmware | อัพโหลดเฟิร์มแวร์

```bash
pio run --target upload
```

### Monitor Serial Output | ดูข้อมูลผ่าน Serial

```bash
pio device monitor
```

Or use combined command:
```bash
pio run --target upload && pio device monitor
```

## Configuration | การตั้งค่า

### Pin Configuration | การกำหนดขา

All pin assignments can be modified in `src/main.cpp`:

```cpp
// MFRC522 RFID Reader (SPI)
#define RFID_SS_PIN     5
#define RFID_RST_PIN    22
// ... etc
```

### Timing Parameters | พารามิเตอร์เวลา

```cpp
#define QR_TIMEOUT      5000    // QR scan timeout (ms)
#define SCAN_RETRY      3       // Number of retry attempts
```

### RFID Data Blocks | บล็อกข้อมูล RFID

```cpp
#define BLOCK_THREAD1   4       // Block for Thread 1 data
#define BLOCK_THREAD2   5       // Block for Thread 2 data
#define BYPASS_KEYWORD  "bypass"
```

## Operation | การทำงาน

### State Machine | เครื่องสถานะ

The system operates as a state machine with the following states:

1. **WAIT_KANBAN** - Waiting for Kanban card
2. **READ_KANBAN** - Reading thread data from card
3. **WAIT_BOBBINS** - Waiting for thread bobbins to be loaded
4. **SCAN_QR1** - Scanning first thread QR code
5. **SCAN_QR2** - Scanning second thread QR code
6. **VERIFY** - Comparing QR codes with Kanban data
7. **READY** - Verification passed, machine enabled
8. **ERROR** - Verification failed, machine disabled
9. **BYPASS** - Bypass mode active, machine enabled

### Normal Operation Flow | ขั้นตอนการทำงานปกติ

1. System starts in WAIT_KANBAN state
2. Operator places Kanban card on RFID reader
3. System reads thread codes from card
4. System waits for both thread bobbins to be detected
5. System scans QR codes on both threads
6. System verifies QR codes match Kanban data
7. If match: Machine enabled (READY state)
8. If mismatch: Machine disabled (ERROR state)
9. When card is removed: Return to WAIT_KANBAN

### Bypass Mode | โหมดบายพาส

When a Kanban card contains "bypass" keyword:
- System skips QR verification
- Machine is immediately enabled
- Useful for maintenance or special operations

## LED Indicators | ไฟแสดงสถานะ

| LED | Color | State | Meaning |
|-----|-------|-------|---------|
| READY1 | Green | ON | Thread 1 OK |
| READY2 | Green | ON | Thread 2 OK |
| ALARM1 | Red | ON | Thread 1 Error |
| ALARM2 | Red | ON | Thread 2 Error |
| Both ALARM | Red | BLINK | System Error |

## Troubleshooting | การแก้ไขปัญหา

### RFID Not Detected

```
[WARNING] MFRC522 not detected! Check wiring.
```

**Solution:**
- Check SPI connections (MISO, MOSI, SCK, SS)
- Verify power supply (3.3V)
- Check RST pin connection

### QR Scanner Not Reading

```
[ERROR] Failed to read QR Code
```

**Solution:**
- Check UART connections (RX, TX)
- Verify trigger signal
- Ensure QR code is within scanner range
- Check scanner power supply

### Bobbin Not Detected

**Solution:**
- Verify sensor type (NPN/PNP)
- Adjust sensor position
- Check sensor wiring
- Modify detection logic in code if needed

## Testing Without Hardware | ทดสอบโดยไม่ใช้ฮาร์ดแวร์

The firmware includes TODO comments for hardware integration points. You can:

1. Monitor serial output to see state transitions
2. Modify code to simulate sensor inputs
3. Test state machine logic without physical hardware

## API Reference | เอกสารอ้างอิง API

### Main Functions | ฟังก์ชันหลัก

- `readKanbanCard(ThreadData& data)` - Read RFID card
- `triggerQRScanner(int scannerNum)` - Trigger QR scanner
- `readQRCode(SoftwareSerial& scanner, int timeoutMs)` - Read QR code
- `detectBobbin(int bobbinPin)` - Check bobbin presence
- `verifyThreads()` - Compare QR with Kanban data
- `updateLEDs(bool r1, bool r2, bool a1, bool a2)` - Control LEDs
- `setMachineOutput(bool enable)` - Control machine relay

## Safety Considerations | ข้อควรระวัง

⚠️ **Important Safety Notes:**

1. Always disconnect machine power when testing
2. Verify relay ratings match machine requirements
3. Use appropriate fuses and circuit protection
4. Test thoroughly before production use
5. Implement emergency stop mechanisms
6. Follow local electrical safety codes

## Support | การสนับสนุน

For technical support or questions:
- Check [SPEC.md](docs/SPEC.md) for detailed specifications
- Review [HARDWARE.md](docs/HARDWARE.md) for wiring help
- Open an issue on GitHub

## License | สัญญาอนุญาต

MIT License - See [LICENSE](../LICENSE) for details
