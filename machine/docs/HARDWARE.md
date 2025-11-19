# Hardware Requirements and Wiring Guide
# คู่มือฮาร์ดแวร์และการต่อสาย

## Bill of Materials (BOM) | รายการอุปกรณ์

### Main Components | อุปกรณ์หลัก

| Item | Quantity | Specification | Notes |
|------|----------|---------------|-------|
| ESP32 Feather | 1 | Adafruit Feather ESP32 or compatible | Main controller |
| MFRC522 Module | 1 | 13.56MHz RFID Reader/Writer | SPI interface |
| GM65 QR Scanner | 2 | Barcode/QR Code Scanner Module | UART interface, 5V |
| Proximity Sensor | 2 | NPN/PNP, 8mm range, 12V | For bobbin detection |
| LED Green | 2 | 5mm, 20mA, 2V forward voltage | Ready indicators |
| LED Red | 2 | 5mm, 20mA, 2V forward voltage | Alarm indicators |
| Relay Module | 1 | 5V, 1-channel, optocoupler | Machine control |
| MIFARE Cards | 10+ | MIFARE Classic 1K, 13.56MHz | Kanban cards |

### Power Supply | แหล่งจ่ายไฟ

| Item | Quantity | Specification | Notes |
|------|----------|---------------|-------|
| Power Supply 5V | 1 | 5V DC, 2A minimum | Main power |
| Power Supply 12V | 1 | 12V DC, 0.5A | For proximity sensors |
| USB Cable | 1 | USB Type-C or Micro-USB | For programming |

### Passive Components | อุปกรณ์แบบพาสซีฟ

| Item | Quantity | Specification | Notes |
|------|----------|---------------|-------|
| Resistor 220Ω | 4 | 1/4W, 5% | For LEDs |
| Resistor 10kΩ | 2 | 1/4W, 5% | Voltage divider (optional) |
| Resistor 3.9kΩ | 2 | 1/4W, 5% | Voltage divider (optional) |

### Wiring & Connectors | สายไฟและขั้วต่อ

| Item | Quantity | Specification | Notes |
|------|----------|---------------|-------|
| Jumper Wires | 1 set | Male-to-Male, Male-to-Female | For breadboard |
| Terminal Blocks | 5 | 2-pin screw terminal | For permanent installation |
| Heat Shrink Tubing | 1 set | Various sizes | For wire protection |
| Wire 22AWG | 5m | Stranded, multiple colors | For connections |

### Optional Components | อุปกรณ์เสริม

| Item | Quantity | Specification | Notes |
|------|----------|---------------|-------|
| Level Shifter | 2 | Bi-directional, 3.3V-5V | For GM65 UART (recommended) |
| Optocoupler | 2 | PC817 or similar | For sensor isolation (recommended) |
| Enclosure | 1 | ABS plastic, IP54 rated | Protection |
| Breadboard | 1 | 830 points | For prototyping |
| PCB | 1 | Custom design | For production |

## Detailed Wiring Instructions | คำแนะนำการต่อสายละเอียด

### Safety First! | ความปลอดภัยก่อน!

⚠️ **IMPORTANT SAFETY WARNINGS:**

1. **Disconnect all power before wiring**
2. **Verify voltage levels before connecting**
3. **Use proper wire gauge for current ratings**
4. **Insulate all connections properly**
5. **Test with multimeter before powering on**
6. **Use fuses for protection**

### Wiring Diagram Overview | ภาพรวมแผนผังการต่อสาย

```
                    ┌─────────────────┐
                    │   Power Supply  │
                    │   5V DC 2A      │
                    └────┬───────┬────┘
                         │       │
                    ┌────┴───┐   │
                    │ ESP32  │   │
                    │ Feather│   │
                    └───┬────┘   │
                        │        │
        ┌───────────────┼────────┼────────────┐
        │               │        │            │
    ┌───┴───┐      ┌───┴───┐ ┌──┴──┐    ┌───┴───┐
    │MFRC522│      │ GM65  │ │GM65 │    │ Relay │
    │ 3.3V  │      │ #1 5V │ │#2 5V│    │  5V   │
    └───────┘      └───────┘ └─────┘    └───────┘

         ┌──────────────┐
         │ Power Supply │
         │  12V DC 0.5A │
         └───┬─────┬────┘
             │     │
        ┌────┴┐  ┌┴────┐
        │Prox │  │Prox │
        │Sen 1│  │Sen 2│
        └─────┘  └─────┘
```

### Step-by-Step Wiring | ขั้นตอนการต่อสายทีละขั้น

---

#### Step 1: MFRC522 RFID Reader (3.3V)

**⚠️ WARNING: Use 3.3V ONLY! 5V will damage the module!**

| MFRC522 Pin | ESP32 Pin | Wire Color (Suggested) |
|-------------|-----------|------------------------|
| SDA | GPIO 5 | Orange |
| SCK | GPIO 18 | Yellow |
| MOSI | GPIO 23 | Green |
| MISO | GPIO 19 | Blue |
| IRQ | Not connected | - |
| GND | GND | Black |
| RST | GPIO 22 | White |
| 3.3V | 3.3V | Red |

**Connection Steps:**
1. Connect GND first (black wire)
2. Connect 3.3V (red wire) - **NOT 5V!**
3. Connect SPI pins (SDA, SCK, MOSI, MISO)
4. Connect RST last

**Testing:**
- Power on ESP32
- Check Serial output: "MFRC522 Version: 0x92" (or similar)
- Place card near reader, should detect

---

#### Step 2: GM65 QR Scanner #1 (5V)

**Option A: Direct Connection (Simple but risky)**

| GM65 #1 Pin | ESP32 Pin | Wire Color |
|-------------|-----------|------------|
| VCC (5V) | 5V (USB or VIN) | Red |
| GND | GND | Black |
| TX | GPIO 4 (RX) | Yellow |
| RX | GPIO 2 (TX) | Orange |
| TRIG | GPIO 15 | Blue |

**Option B: With Level Shifter (Recommended)**

```
GM65 TX (5V) → Level Shifter HV → Level Shifter LV → ESP32 GPIO 4
ESP32 GPIO 2 → Level Shifter LV → Level Shifter HV → GM65 RX (5V)

Level Shifter Connections:
- HV: 5V
- LV: 3.3V
- GND: Common ground
```

**Testing:**
1. Trigger scanner: `digitalWrite(QR1_TRIG_PIN, HIGH); delay(100); digitalWrite(QR1_TRIG_PIN, LOW);`
2. Scanner should emit laser
3. Scan QR code, should output data to Serial

---

#### Step 3: GM65 QR Scanner #2 (5V)

Same as Scanner #1, but different pins:

| GM65 #2 Pin | ESP32 Pin | Wire Color |
|-------------|-----------|------------|
| VCC (5V) | 5V | Red |
| GND | GND | Black |
| TX | GPIO 16 (RX) | Yellow |
| RX | GPIO 17 (TX) | Orange |
| TRIG | GPIO 13 | Blue |

---

#### Step 4: Proximity Sensors (12V)

**⚠️ WARNING: Sensors run on 12V but output must be level-shifted to 3.3V!**

**Option A: Using Voltage Divider**

For each sensor:
```
Sensor OUT → 10kΩ resistor → ESP32 GPIO
                          → 3.9kΩ resistor → GND

This divides 12V to approximately 3.4V (safe for ESP32)
```

| Sensor #1 | Connection |
|-----------|------------|
| Brown (VCC) | 12V |
| Blue (GND) | GND (common with ESP32) |
| Black (OUT) | → Voltage Divider → GPIO 32 |

| Sensor #2 | Connection |
|-----------|------------|
| Brown (VCC) | 12V |
| Blue (GND) | GND (common with ESP32) |
| Black (OUT) | → Voltage Divider → GPIO 33 |

**Option B: Using Optocoupler (Safer)**

```
Sensor OUT → [1kΩ] → LED of Optocoupler
Optocoupler transistor → ESP32 GPIO (with pull-up)
```

**Testing:**
1. Place metal object near sensor
2. Sensor LED should light
3. GPIO should read LOW (NPN) or HIGH (PNP)

---

#### Step 5: LED Indicators

For each LED, use a 220Ω current-limiting resistor:

```
ESP32 GPIO → 220Ω resistor → LED Anode (+)
LED Cathode (-) → GND
```

| LED | GPIO Pin | Color |
|-----|----------|-------|
| Ready 1 | GPIO 25 | Green |
| Ready 2 | GPIO 26 | Green |
| Alarm 1 | GPIO 27 | Red |
| Alarm 2 | GPIO 14 | Red |

**Testing:**
```cpp
digitalWrite(LED_READY1_PIN, HIGH);  // LED should light
delay(1000);
digitalWrite(LED_READY1_PIN, LOW);   // LED should turn off
```

---

#### Step 6: Relay Module (Machine Control)

| Relay Pin | ESP32 Pin | Notes |
|-----------|-----------|-------|
| VCC | 5V | Relay coil power |
| GND | GND | Common ground |
| IN | GPIO 21 | Control signal |
| COM | Machine Power | Common contact |
| NO | Machine Control | Normally Open |

**⚠️ SAFETY: Ensure relay is rated for machine voltage/current!**

**Testing:**
```cpp
digitalWrite(MACHINE_OUT_PIN, HIGH);  // Relay should click ON
delay(1000);
digitalWrite(MACHINE_OUT_PIN, LOW);   // Relay should click OFF
```

---

### Power Distribution Wiring | การต่อสายจ่ายไฟ

#### 5V Power Rail

```
5V Power Supply (+) → Terminal Block → Branch to:
                                      ├─ ESP32 VIN/5V
                                      ├─ GM65 #1 VCC
                                      ├─ GM65 #2 VCC
                                      └─ Relay Module VCC

5V Power Supply (-) → Common GND
```

#### 12V Power Rail

```
12V Power Supply (+) → Terminal Block → Branch to:
                                       ├─ Proximity Sensor #1
                                       └─ Proximity Sensor #2

12V Power Supply (-) → Common GND
```

**⚠️ IMPORTANT: Use common ground for all components!**

---

## Prototyping vs Production | ต้นแบบและการผลิต

### Breadboard Prototype

**Advantages:**
- Easy to modify
- Quick testing
- No soldering required

**Disadvantages:**
- Not robust
- Loose connections
- Not suitable for industrial use

### Perfboard/Stripboard

**Advantages:**
- More permanent
- Still allows modifications
- Good for small production

**Disadvantages:**
- Requires soldering
- Takes more time
- Can be messy

### Custom PCB (Recommended for Production)

**Advantages:**
- Professional appearance
- Reliable connections
- Compact design
- Reproducible

**Disadvantages:**
- Requires design time
- Initial cost
- Hard to modify

---

## Testing Procedures | ขั้นตอนการทดสอบ

### Pre-Power Checks

- [ ] Verify all connections with multimeter (continuity test)
- [ ] Check for short circuits between VCC and GND
- [ ] Verify correct voltage on each power rail
- [ ] Ensure no components are reversed
- [ ] Check polarity of LEDs and sensors

### Power-On Sequence

1. **Connect USB cable only** (no external power)
2. Monitor Serial output for boot messages
3. If stable, connect 5V external power
4. Monitor current draw (should be < 1A)
5. If stable, connect 12V sensor power
6. Monitor for any unusual behavior

### Component Testing

1. **Test RFID reader:**
   - Place card, should detect
   - Read UID from Serial output
   - Remove card, should stop detecting

2. **Test QR scanners:**
   - Trigger scanner 1
   - Scan QR code
   - Verify data on Serial
   - Repeat for scanner 2

3. **Test sensors:**
   - Place object near sensor
   - Verify detection on Serial
   - Remove object
   - Repeat for second sensor

4. **Test LEDs:**
   - Each LED should light independently
   - Check brightness
   - Verify colors

5. **Test relay:**
   - Should click audibly
   - Verify contacts switch
   - Check with multimeter

### System Integration Test

Run complete workflow:
1. Place Kanban card
2. Load bobbins (trigger sensors)
3. Trigger QR scans
4. Verify thread matching
5. Check machine output

---

## Troubleshooting | การแก้ไขปัญหา

### Common Issues | ปัญหาที่พบบ่อย

#### MFRC522 Not Detected

**Symptoms:** "MFRC522 not detected" warning

**Solutions:**
- Check 3.3V power (NOT 5V!)
- Verify SPI connections
- Check RST pin
- Try different MFRC522 module

#### QR Scanner Not Working

**Symptoms:** No laser, no scan data

**Solutions:**
- Check 5V power
- Verify TX/RX connections (swap if needed)
- Check trigger signal
- Test scanner independently

#### Sensor Always Triggered

**Symptoms:** Sensor always reads LOW or HIGH

**Solutions:**
- Check voltage divider values
- Verify sensor type (NPN/PNP)
- Adjust sensing distance
- Check for interference

#### LED Not Lighting

**Symptoms:** LED stays off

**Solutions:**
- Check resistor value (should be 220Ω)
- Verify LED polarity (+ to resistor, - to GND)
- Test LED independently
- Check GPIO output

#### Relay Not Switching

**Symptoms:** No click, no contact closure

**Solutions:**
- Check 5V power to relay
- Verify IN signal
- Check for bad relay
- Verify relay type (active HIGH/LOW)

---

## Enclosure and Mounting | ตู้และการติดตั้ง

### Enclosure Requirements

- **Material:** ABS or polycarbonate
- **Rating:** IP54 minimum (dust and splash resistant)
- **Size:** Minimum 200x150x75mm
- **Features:**
  - Cable glands for wiring
  - Ventilation slots
  - Mounting holes
  - Window for RFID reader
  - Openings for QR scanners

### Mounting Considerations

1. **RFID Reader Position:**
   - Accessible to operator
   - Protected from damage
   - 0-60mm from card

2. **QR Scanners:**
   - Fixed angle toward thread bobbins
   - Adjustable mounting
   - 50-150mm from QR codes

3. **Sensors:**
   - 0-8mm from bobbin surface
   - Adjustable position
   - Protected from thread

4. **LEDs:**
   - Visible to operator
   - Front panel mounting
   - Clear labels

---

## Maintenance | การบำรุงรักษา

### Weekly Checks

- Clean RFID reader surface
- Clean QR scanner lenses
- Check all connections
- Verify LED functionality

### Monthly Checks

- Tighten screw terminals
- Inspect wires for damage
- Test backup power supply
- Clean enclosure

### Annual Checks

- Replace worn components
- Update firmware
- Full system calibration
- Documentation review

---

## Schematic Reference | เอกสารอ้างอิงวงจร

```
For detailed schematics, see:
- PINOUT.md: Pin assignments
- SPEC.md: Component specifications
- Main.cpp: Software configuration
```

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-19  
**Author:** CWT Team  
**Safety Level:** Industrial Use with Proper Installation
