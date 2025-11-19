# Machine System Technical Specification
# ข้อมูลจำเพาะทางเทคนิคของระบบควบคุมเครื่องจักร

## System Overview | ภาพรวมระบบ

The Machine System is an ESP32-based embedded controller that automates thread verification for industrial sewing machines using RFID Kanban cards and dual QR code scanners.

## Architecture | สถาปัตยกรรม

```
┌─────────────────────────────────────────────────────────┐
│                   ESP32 Controller                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │           State Machine Logic                    │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │ WAIT → READ → DETECT → SCAN → VERIFY → OK │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  RFID   │  │  QR #1  │  │  QR #2  │  │ Sensors │  │
│  │  (SPI)  │  │ (UART1) │  │ (UART2) │  │ (GPIO)  │  │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  LEDs   │  │  LEDs   │  │  LEDs   │  │  Relay  │  │
│  │ (GPIO)  │  │ (GPIO)  │  │ (GPIO)  │  │ (GPIO)  │  │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────────────────────┘
```

## State Machine Diagram | แผนภาพเครื่องสถานะ

```
                    ┌──────────────┐
                    │    INIT      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
              ┌────►│ WAIT_KANBAN  │◄─────┐
              │     └──────┬───────┘      │
              │            │ Card         │
              │            │ Detected     │
              │            ▼              │
              │     ┌──────────────┐      │
              │     │ READ_KANBAN  │      │
              │     └──────┬───────┘      │
              │            │              │
              │      ┌─────┴─────┐        │
              │      │           │        │
              │  "bypass"    Valid Data   │
              │      │           │        │
              │      ▼           ▼        │
              │  ┌────────┐ ┌──────────┐ │
              │  │BYPASS  │ │  WAIT_   │ │
              │  │        │ │ BOBBINS  │ │
              │  └───┬────┘ └────┬─────┘ │
              │      │           │ Both  │
              │  Machine     Detected    │
              │   Enabled        │       │
              │      │           ▼       │
              │      │      ┌──────────┐ │
              │      │      │SCAN_QR1  │ │
              │      │      └────┬─────┘ │
              │      │           │Success│
              │      │           ▼       │
              │      │      ┌──────────┐ │
              │      │      │SCAN_QR2  │ │
              │      │      └────┬─────┘ │
              │      │           │Success│
              │      │           ▼       │
              │      │      ┌──────────┐ │
              │      │      │ VERIFY   │ │
              │      │      └────┬─────┘ │
              │      │           │       │
              │      │      ┌────┴────┐  │
              │      │      │         │  │
              │      │    Match   Mismatch
              │      │      │         │  │
              │      │      ▼         ▼  │
              │      │  ┌──────┐ ┌──────┐│
              │      │  │READY │ │ERROR ││
              │      │  └──┬───┘ └───┬──┘│
              │      │     │          │   │
              │      │  Machine    Machine│
              │      │  Enabled   Disabled│
              │      │     │          │   │
              │      └─────┴──────────┴───┘
              │         Card Removed
              └──────────────────────────┘
```

## Component Specifications | ข้อมูลจำเพาะของส่วนประกอบ

### 1. ESP32 Feather

**Specifications:**
- MCU: ESP32-WROOM-32
- CPU: Dual-core Xtensa LX6, 240 MHz
- RAM: 520 KB SRAM
- Flash: 4 MB
- Operating Voltage: 3.3V
- I/O Voltage: 3.3V (5V tolerant on some pins)
- GPIO: 28 pins
- SPI: 4 interfaces
- UART: 3 interfaces
- ADC: 18 channels, 12-bit
- PWM: 16 channels

**Power Requirements:**
- Operating: 80-260 mA
- Deep Sleep: 10 µA
- Input: 5V via USB or 3.7-6V via BAT

### 2. MFRC522 RFID Reader

**Specifications:**
- Frequency: 13.56 MHz
- Interface: SPI
- Operating Voltage: 3.3V
- Current: 13-26 mA
- Reading Distance: 0-60 mm
- Supported Cards: MIFARE Classic, MIFARE Ultralight
- Data Rate: 10 Mbit/s

**Timing:**
- Card Detection: < 100 ms
- Read/Write: < 50 ms per block

### 3. GM65 QR Scanner

**Specifications:**
- Interface: UART (TTL)
- Baud Rate: 9600 bps (default)
- Operating Voltage: 5V DC
- Current: 160 mA (typical), 300 mA (peak)
- Scan Speed: 60 scans/second
- Trigger Mode: External trigger
- Reading Distance: 30-200 mm
- Decode Capability: 1D/2D barcodes, QR codes

**Timing:**
- Trigger Response: < 100 ms
- Decode Time: < 300 ms

### 4. Proximity Sensor

**Specifications (NPN Type):**
- Sensing Distance: 0-8 mm
- Operating Voltage: 6-36V DC
- Output Current: 200 mA
- Response Time: < 10 ms
- Output: NPN Open Collector

**Specifications (PNP Type):**
- Sensing Distance: 0-8 mm
- Operating Voltage: 6-36V DC
- Output Current: 200 mA
- Response Time: < 10 ms
- Output: PNP Open Collector

### 5. Relay Module

**Specifications:**
- Control Voltage: 5V DC
- Control Current: 15-20 mA
- Contact Rating: 10A @ 250V AC / 30V DC
- Switching Time: < 10 ms
- Isolation: Optocoupler

## Communication Protocols | โปรโตคอลการสื่อสาร

### SPI (RFID Reader)

```
Clock: 10 MHz max
Mode: Mode 0 (CPOL=0, CPHA=0)
Bit Order: MSB first

Pin Assignment:
- MISO: Data from RFID to ESP32
- MOSI: Data from ESP32 to RFID
- SCK: Clock signal
- SS: Chip select (active low)
- RST: Reset (active low)
```

### UART (QR Scanners)

```
Baud Rate: 9600 bps
Data Bits: 8
Stop Bits: 1
Parity: None
Flow Control: None

Data Format:
- QR data as ASCII string
- Terminated with CR+LF (\r\n)
- Max length: 256 bytes

Trigger:
- External trigger via GPIO
- Pulse width: 100 ms minimum
- Active high
```

### GPIO (Sensors & Outputs)

```
Bobbin Sensors:
- Input mode with internal pull-up
- Active LOW for NPN sensors
- Active HIGH for PNP sensors
- Debounce: 50 ms in software

LEDs:
- Output mode
- Active HIGH
- Current limiting: 220Ω resistor

Relay:
- Output mode
- Active HIGH
- Optocoupler isolated
```

## RFID Data Structure | โครงสร้างข้อมูล RFID

### MIFARE Classic 1K Memory Map

```
Block 0: Manufacturer Data (Read-Only)
Block 1: User Data (16 bytes)
Block 2: User Data (16 bytes)
Block 3: Sector Trailer (Keys & Access Bits)
─────────────────────────────────
Block 4: Thread 1 Code (16 bytes) ← Used
Block 5: Thread 2 Code (16 bytes) ← Used
Block 6: User Data (16 bytes)
Block 7: Sector Trailer
─────────────────────────────────
...
```

### Thread Code Format

```
Block 4 (Thread 1):
┌─────────────────────────────────┐
│ Thread Code (ASCII, max 16)    │
│ Null-padded if < 16 bytes      │
└─────────────────────────────────┘

Example: "TH-001\0\0\0\0\0\0\0\0\0\0"

Block 5 (Thread 2):
┌─────────────────────────────────┐
│ Thread Code (ASCII, max 16)    │
│ Null-padded if < 16 bytes      │
└─────────────────────────────────┘

Example: "TH-002\0\0\0\0\0\0\0\0\0\0"

Bypass Mode:
┌─────────────────────────────────┐
│ "bypass\0\0\0\0\0\0\0\0\0"      │
└─────────────────────────────────┘
```

### Authentication

```
Key Type: Key A (default)
Key Value: 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF
Access Bits: Default (0xFF 0x07 0x80 0x69)
```

## Timing Specifications | ข้อมูลจำเพาะด้านเวลา

### System Response Times

| Operation | Typical | Maximum |
|-----------|---------|---------|
| RFID Card Detection | 100 ms | 200 ms |
| RFID Block Read | 50 ms | 100 ms |
| QR Code Scan | 300 ms | 5000 ms |
| Bobbin Detection | 10 ms | 50 ms |
| State Transition | 100 ms | 500 ms |
| Total Verification | 1-2 s | 10 s |

### Timeout Values

```cpp
QR_TIMEOUT = 5000 ms        // QR scan timeout
BOBBIN_WAIT = 30000 ms      // Wait for bobbin timeout
DEBOUNCE_DELAY = 50 ms      // Sensor debounce
TRIGGER_PULSE = 100 ms      // QR trigger pulse width
```

## Error Handling | การจัดการข้อผิดพลาด

### Error Codes

| Code | Description | Action |
|------|-------------|--------|
| E01 | RFID Read Failure | Retry, check card |
| E02 | QR1 Scan Failure | Retry, check position |
| E03 | QR2 Scan Failure | Retry, check position |
| E04 | Thread Mismatch | Alarm, disable machine |
| E05 | Bobbin Timeout | Return to wait state |
| E06 | Invalid Kanban Data | Alarm, wait for new card |

### Recovery Mechanisms

1. **Automatic Retry:**
   - QR scans retry up to 3 times
   - RFID reads retry on failure

2. **State Reset:**
   - Remove Kanban card to reset
   - System returns to WAIT_KANBAN

3. **Manual Override:**
   - Use bypass mode for emergencies
   - Bypass keyword on Kanban card

## Performance Metrics | ตัวชี้วัดประสิทธิภาพ

### Throughput

- Card Read Time: < 200 ms
- QR Scan Time: < 1 second per code
- Total Verification: 1-3 seconds
- Continuous Operation: 24/7 capable

### Reliability

- RFID Success Rate: > 99%
- QR Success Rate: > 95%
- False Positive: < 0.1%
- False Negative: < 0.1%

### Environmental Limits

- Operating Temperature: 0-50°C
- Storage Temperature: -20-60°C
- Humidity: 10-90% RH (non-condensing)
- Vibration: Industrial environment compatible

## Power Budget | งบประมาณกำลังไฟ

```
Component          Current    Voltage   Power
────────────────────────────────────────────
ESP32             150 mA     5V        0.75W
MFRC522            20 mA     3.3V      0.07W
GM65 #1           160 mA     5V        0.80W
GM65 #2           160 mA     5V        0.80W
LEDs (4x)          80 mA     5V        0.40W
Relay              20 mA     5V        0.10W
Sensors (2x)       40 mA     12V       0.48W
────────────────────────────────────────────
Total (Peak)      630 mA               3.40W
────────────────────────────────────────────
Recommended PSU: 5V/2A + 12V/0.5A
```

## Testing Procedures | ขั้นตอนการทดสอบ

### Unit Testing

1. **RFID Module:**
   - Verify card detection
   - Test read/write operations
   - Check authentication

2. **QR Scanners:**
   - Test trigger response
   - Verify decode accuracy
   - Check different QR codes

3. **Sensors:**
   - Verify detection range
   - Test debounce logic
   - Check response time

4. **Outputs:**
   - Test LED indicators
   - Verify relay operation
   - Check timing

### Integration Testing

1. **Complete Workflow:**
   - Place Kanban card
   - Load bobbins
   - Verify QR scanning
   - Check verification logic
   - Confirm machine control

2. **Error Scenarios:**
   - Wrong thread loaded
   - QR scan failure
   - Card read failure
   - Sensor malfunction

3. **Edge Cases:**
   - Bypass mode
   - Card removal during scan
   - Simultaneous sensor triggers

## Maintenance | การบำรุงรักษา

### Regular Checks

- **Daily:**
  - Verify LED functionality
  - Check sensor alignment
  - Test RFID reader

- **Weekly:**
  - Clean QR scanner lenses
  - Inspect cable connections
  - Verify power supply

- **Monthly:**
  - Firmware backup
  - System log review
  - Performance audit

### Calibration

- **Proximity Sensors:**
  - Adjust detection distance
  - Verify trigger threshold
  - Test with different materials

- **QR Scanners:**
  - Clean lens
  - Check focus
  - Adjust mounting angle

## Future Enhancements | การพัฒนาในอนาคต

### Planned Features

1. **Network Connectivity:**
   - WiFi reporting
   - Remote monitoring
   - OTA updates

2. **Data Logging:**
   - SD card storage
   - Usage statistics
   - Error logs

3. **Advanced Features:**
   - Multi-language support
   - Predictive maintenance
   - Integration with MES

## References | เอกสารอ้างอิง

- ESP32 Datasheet: https://www.espressif.com/
- MFRC522 Datasheet: NXP Semiconductors
- GM65 User Manual: Shenzhen Grow Technology
- MIFARE Classic Spec: NXP Semiconductors

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-19  
**Author:** CWT Team
