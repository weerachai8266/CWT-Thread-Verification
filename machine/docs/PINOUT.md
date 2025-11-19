# Pin Assignment Table
# ตารางการกำหนดขา

## Complete Pin Map | แผนผังขาทั้งหมด

### ESP32 Feather Pin Assignment

| Function | ESP32 Pin | Device Pin | Signal Type | Notes |
|----------|-----------|------------|-------------|-------|
| **MFRC522 RFID Reader (SPI)** |
| SPI SS (Chip Select) | GPIO 5 | SDA | Output | Active LOW |
| SPI SCK (Clock) | GPIO 18 | SCK | Output | 10 MHz max |
| SPI MOSI (Master Out) | GPIO 23 | MOSI | Output | Data to RFID |
| SPI MISO (Master In) | GPIO 19 | MISO | Input | Data from RFID |
| Reset | GPIO 22 | RST | Output | Active LOW |
| Power | 3.3V | 3.3V | Power | - |
| Ground | GND | GND | Ground | - |
| **GM65 QR Scanner #1 (UART1)** |
| RX (Receive) | GPIO 4 | TX | Input | 9600 baud |
| TX (Transmit) | GPIO 2 | RX | Output | 9600 baud |
| Trigger | GPIO 15 | TRIG | Output | Active HIGH |
| Power | 5V | VCC | Power | 300mA peak |
| Ground | GND | GND | Ground | - |
| **GM65 QR Scanner #2 (UART2)** |
| RX (Receive) | GPIO 16 | TX | Input | 9600 baud |
| TX (Transmit) | GPIO 17 | RX | Output | 9600 baud |
| Trigger | GPIO 13 | TRIG | Output | Active HIGH |
| Power | 5V | VCC | Power | 300mA peak |
| Ground | GND | GND | Ground | - |
| **Proximity Sensor #1 (Bobbin 1)** |
| Signal | GPIO 32 | OUT | Input | Pull-up enabled |
| Power | 12V | VCC | Power | NPN/PNP sensor |
| Ground | GND | GND | Ground | - |
| **Proximity Sensor #2 (Bobbin 2)** |
| Signal | GPIO 33 | OUT | Input | Pull-up enabled |
| Power | 12V | VCC | Power | NPN/PNP sensor |
| Ground | GND | GND | Ground | - |
| **LED Ready #1** |
| Control | GPIO 25 | Anode | Output | Via 220Ω resistor |
| Ground | GND | Cathode | Ground | - |
| **LED Ready #2** |
| Control | GPIO 26 | Anode | Output | Via 220Ω resistor |
| Ground | GND | Cathode | Ground | - |
| **LED Alarm #1** |
| Control | GPIO 27 | Anode | Output | Via 220Ω resistor |
| Ground | GND | Cathode | Ground | - |
| **LED Alarm #2** |
| Control | GPIO 14 | Anode | Output | Via 220Ω resistor |
| Ground | GND | Cathode | Ground | - |
| **Relay Module (Machine Control)** |
| Control | GPIO 21 | IN | Output | Active HIGH |
| Power | 5V | VCC | Power | Optocoupler isolated |
| Ground | GND | GND | Ground | - |

## Pin Usage Summary | สรุปการใช้งานขา

### Input Pins (5)
- GPIO 4 (QR1 RX)
- GPIO 16 (QR2 RX)
- GPIO 19 (RFID MISO)
- GPIO 32 (Bobbin Sensor 1)
- GPIO 33 (Bobbin Sensor 2)

### Output Pins (13)
- GPIO 2 (QR1 TX)
- GPIO 5 (RFID SS)
- GPIO 13 (QR2 Trigger)
- GPIO 14 (LED Alarm 2)
- GPIO 15 (QR1 Trigger)
- GPIO 17 (QR2 TX)
- GPIO 18 (RFID SCK)
- GPIO 21 (Machine Relay)
- GPIO 22 (RFID RST)
- GPIO 23 (RFID MOSI)
- GPIO 25 (LED Ready 1)
- GPIO 26 (LED Ready 2)
- GPIO 27 (LED Alarm 1)

### Available/Unused Pins
- GPIO 0, 12, 34, 35, 36, 39 (and others)
- Reserved for future expansion

## Power Distribution | การจ่ายไฟ

```
Main Power Input: 5V DC, 2A minimum

Distribution:
├─ ESP32 Board: 5V input (regulated to 3.3V internally)
├─ MFRC522: 3.3V from ESP32 regulator
├─ GM65 #1: 5V direct (300mA peak)
├─ GM65 #2: 5V direct (300mA peak)
├─ Relay Module: 5V direct (20mA)
└─ LEDs: 5V via 220Ω resistors (4x 20mA)

Separate 12V Supply:
└─ Proximity Sensors: 12V (2x 20mA)
```

## Voltage Levels | ระดับแรงดัน

| Device | Logic Level | Tolerance | Notes |
|--------|-------------|-----------|-------|
| ESP32 | 3.3V | 5V tolerant* | *Some pins only |
| MFRC522 | 3.3V | 3.3V only | Must not exceed 3.6V |
| GM65 (TX/RX) | 5V TTL | - | Level shifter recommended |
| GM65 (Trigger) | 5V TTL | 3.3V compatible | Can use 3.3V |
| Proximity Sensors | 12V PNP/NPN | - | Use voltage divider or optocoupler |
| Relay Module | 5V TTL | 3.3V compatible | Optocoupler isolated |

## Critical Notes | ข้อควรระวัง

### ⚠️ MFRC522 Voltage Warning
**The MFRC522 operates at 3.3V ONLY. Do not connect to 5V!**

```
Correct Connection:
ESP32 3.3V → MFRC522 VCC
ESP32 GND → MFRC522 GND

Incorrect (will damage MFRC522):
ESP32 5V → MFRC522 VCC ❌
```

### ⚠️ GM65 Voltage Levels

The GM65 uses 5V TTL logic while ESP32 uses 3.3V. Consider using level shifters:

**Option 1: Direct Connection (Risk)**
```
GM65 TX (5V) → ESP32 RX (5V tolerant) ⚠️
ESP32 TX (3.3V) → GM65 RX (may work) ⚠️
```

**Option 2: Level Shifter (Recommended)**
```
GM65 TX (5V) → Level Shifter → ESP32 RX (3.3V) ✓
ESP32 TX (3.3V) → Level Shifter → GM65 RX (5V) ✓
```

**Option 3: Voltage Divider (TX only)**
```
GM65 TX (5V) → [Resistor Divider] → ESP32 RX (3.3V) ✓
Divider: R1=1kΩ, R2=2kΩ
```

### ⚠️ Proximity Sensor Connection

**NPN Sensor (Active LOW):**
```
Sensor VCC → 12V
Sensor GND → Common GND
Sensor OUT → [Voltage Divider] → ESP32 GPIO
             or
Sensor OUT → [Optocoupler] → ESP32 GPIO
```

**PNP Sensor (Active HIGH):**
```
Sensor VCC → 12V
Sensor GND → Common GND
Sensor OUT → [Voltage Divider] → ESP32 GPIO
             or
Sensor OUT → [Optocoupler] → ESP32 GPIO
```

**Simple Voltage Divider (12V → 3.3V):**
```
12V Sensor OUT → R1 (10kΩ) → ESP32 GPIO
                           → R2 (3.9kΩ) → GND
Output = 12V × (3.9kΩ / 13.9kΩ) ≈ 3.4V
```

## Pin Change Procedure | วิธีเปลี่ยนขา

If you need to change pin assignments:

1. **Update Code Constants:**
   ```cpp
   // In src/main.cpp
   #define RFID_SS_PIN     5  // Change this
   ```

2. **Update Wiring:**
   - Disconnect power
   - Move wire to new pin
   - Update this documentation

3. **Test:**
   - Upload new firmware
   - Verify functionality
   - Update schematic

## Pin Conflict Checking | การตรวจสอบความขัดแย้งของขา

### Reserved Pins (Do Not Use)

| Pin | Reason | Notes |
|-----|--------|-------|
| GPIO 0 | Boot Mode | Must be HIGH during boot |
| GPIO 2 | Boot Mode | Must be floating/HIGH during boot |
| GPIO 12 | Boot Voltage | Must be LOW during boot |
| GPIO 6-11 | Flash | Connected to internal flash |

### Safe to Use
All pins used in this design are safe and tested.

### ADC2 Conflict (WiFi)
If you enable WiFi in the future, these ADC2 pins cannot be used:
- GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, 27

Current usage on ADC2 pins:
- GPIO 2 (QR1 TX) - OK if WiFi enabled
- GPIO 4 (QR1 RX) - OK if WiFi enabled  
- GPIO 13 (QR2 Trigger) - OK if WiFi enabled
- GPIO 14 (LED Alarm 2) - OK if WiFi enabled
- GPIO 15 (QR1 Trigger) - OK if WiFi enabled
- GPIO 25 (LED Ready 1) - OK if WiFi enabled
- GPIO 26 (LED Ready 2) - OK if WiFi enabled
- GPIO 27 (LED Alarm 1) - OK if WiFi enabled

All these are digital outputs/inputs, so WiFi will not interfere.

## Testing Pin Functionality | การทดสอบการทำงานของขา

### Quick Pin Test

Upload this code to test individual pins:

```cpp
// Test digital output
pinMode(25, OUTPUT);
digitalWrite(25, HIGH);  // LED should turn on
delay(1000);
digitalWrite(25, LOW);   // LED should turn off

// Test digital input
pinMode(32, INPUT_PULLUP);
int value = digitalRead(32);  // Read sensor
Serial.println(value);
```

### Pin Testing Checklist

- [ ] RFID SPI communication
- [ ] QR1 UART communication  
- [ ] QR2 UART communication
- [ ] Bobbin sensor 1 detection
- [ ] Bobbin sensor 2 detection
- [ ] LED Ready 1 control
- [ ] LED Ready 2 control
- [ ] LED Alarm 1 control
- [ ] LED Alarm 2 control
- [ ] Machine relay control
- [ ] QR1 trigger signal
- [ ] QR2 trigger signal

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-19  
**Author:** CWT Team
