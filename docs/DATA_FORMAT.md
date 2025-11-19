# RFID Data Format Specification
# ข้อมูลจำเพาะรูปแบบข้อมูล RFID

## Overview | ภาพรวม

This document specifies the data format and structure used for storing thread verification information on MIFARE Classic 1K RFID cards (Kanban cards).

## Card Specifications | ข้อมูลจำเพาะการ์ด

### Physical Specifications | ข้อมูลจำเพาะทางกายภาพ

- **Card Type:** MIFARE Classic 1K (MF1S50)
- **Frequency:** 13.56 MHz
- **Protocol:** ISO/IEC 14443 Type A
- **Total Memory:** 1024 bytes (1KB)
- **User Memory:** 752 bytes
- **UID Length:** 4 bytes (configurable 7 bytes)
- **Operating Distance:** 0-100 mm

### Memory Organization | โครงสร้างหน่วยความจำ

```
Total: 1024 bytes
├─ 16 Sectors (0-15)
│  └─ Each sector: 4 blocks (64 bytes)
│     └─ Each block: 16 bytes
│
Block Structure:
├─ Block 0: Manufacturer data (read-only)
├─ Blocks 1-2: User data
└─ Block 3: Sector trailer (keys + access bits)
```

## Data Block Assignment | การกำหนดบล็อกข้อมูล

### Sector 1 Usage (Blocks 4-7) | การใช้งาน Sector 1

```
┌────────────────────────────────────────────┐
│ Sector 1: Thread Verification Data        │
├────────────────────────────────────────────┤
│ Block 4: Thread 1 Code (16 bytes)         │ ◄─── Primary Data
│ Block 5: Thread 2 Code (16 bytes)         │ ◄─── Primary Data
│ Block 6: Reserved (16 bytes)              │ ◄─── Future Use
│ Block 7: Sector Trailer (16 bytes)        │ ◄─── Keys & Access
└────────────────────────────────────────────┘
```

### Block Definitions | ความหมายของบล็อก

| Block | Address | Purpose | Size | Read | Write |
|-------|---------|---------|------|------|-------|
| 4 | 0x04 | Thread 1 Code | 16 bytes | Public | Authenticated |
| 5 | 0x05 | Thread 2 Code | 16 bytes | Public | Authenticated |
| 6 | 0x06 | Reserved | 16 bytes | - | - |
| 7 | 0x07 | Sector Trailer | 16 bytes | Special | Special |

## Thread Code Format | รูปแบบรหัสด้าย

### Standard Thread Code | รหัสด้ายปกติ

```
Field: Thread Code
Type: ASCII String
Length: 0-16 characters
Encoding: ASCII (7-bit)
Padding: NULL bytes (0x00)
Termination: Implicit (NULL padding)

Format:
┌─────────────────────────────────────┐
│ [Thread Code] [NULL Padding]       │
│ ← 1-16 chars →← Remaining bytes→   │
└─────────────────────────────────────┘

Examples:
"TH-001"      → "TH-001\0\0\0\0\0\0\0\0\0\0"
"RED-100"     → "RED-100\0\0\0\0\0\0\0\0\0"
"COTTON-01"   → "COTTON-01\0\0\0\0\0\0\0"
```

### Bypass Mode Format | รูปแบบโหมดบายพาส

```
Field: Bypass Keyword
Type: ASCII String
Value: "bypass" (case-insensitive)
Length: 6 characters
Padding: NULL bytes

Format:
┌─────────────────────────────────────┐
│ "bypass\0\0\0\0\0\0\0\0\0\0"        │
│ ← 6 chars → ← 10 NULLs →           │
└─────────────────────────────────────┘

Detection:
- Thread 1 contains "bypass" → Bypass mode
- Thread 2 ignored in bypass mode
- Case-insensitive comparison
```

### Empty/Cleared Format | รูปแบบที่ว่างเปล่า

```
Field: Empty Block
Type: NULL bytes
Value: All 0x00
Length: 16 bytes

Format:
┌─────────────────────────────────────┐
│ 0x00 0x00 0x00 ... 0x00 (16 bytes) │
└─────────────────────────────────────┘

Interpretation:
- Card is blank/cleared
- Ready for new data
- Invalid for operation
```

## Detailed Block Structure | โครงสร้างบล็อกโดยละเอียด

### Block 4: Thread 1 Code | บล็อก 4: รหัสด้าย 1

```
Byte Offset | 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
────────────┼────────────────────────────────────────────────
Content     │ [Thread Code String (ASCII)]  [NULL Padding]
────────────┼────────────────────────────────────────────────
Example     │ T  H  -  0  0  1  \0 \0 \0 \0 \0 \0 \0 \0 \0 \0
Hex         │ 54 48 2D 30 30 31 00 00 00 00 00 00 00 00 00 00
```

**Properties:**
- Address: 0x04
- Size: 16 bytes (128 bits)
- Access: Read after authentication
- Encoding: ASCII
- Max printable chars: 16
- Unused bytes: 0x00 (NULL)

### Block 5: Thread 2 Code | บล็อก 5: รหัสด้าย 2

```
Byte Offset | 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
────────────┼────────────────────────────────────────────────
Content     │ [Thread Code String (ASCII)]  [NULL Padding]
────────────┼────────────────────────────────────────────────
Example     │ R  E  D  -  1  0  0  \0 \0 \0 \0 \0 \0 \0 \0 \0
Hex         │ 52 45 44 2D 31 30 30 00 00 00 00 00 00 00 00 00
```

**Properties:**
- Address: 0x05
- Size: 16 bytes (128 bits)
- Access: Read after authentication
- Encoding: ASCII
- Same format as Block 4

### Block 6: Reserved | บล็อก 6: สำรอง

```
Byte Offset | 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
────────────┼────────────────────────────────────────────────
Content     │ [Reserved for Future Use]
────────────┼────────────────────────────────────────────────
Current     │ 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

**Potential Future Uses:**
- Batch number
- Timestamp
- Checksum/CRC
- Extended metadata
- Version information

### Block 7: Sector Trailer | บล็อก 7: Sector Trailer

```
Byte Offset | 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
────────────┼────────────────────────────────────────────────
Content     │ [Key A (6)] [Access Bits (4)] [Key B (6)]
────────────┼────────────────────────────────────────────────
Default     │ FF FF FF FF FF FF  FF 07 80 69  FF FF FF FF FF FF
```

**Structure:**
- Bytes 0-5: Key A (used for authentication)
- Bytes 6-9: Access bits (control read/write permissions)
- Bytes 10-15: Key B (optional, not used)

## Access Control | การควบคุมการเข้าถึง

### Authentication Keys | กุญแจการตรวจสอบสิทธิ์

```
Key Type: Key A
Default Value: 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF
Length: 6 bytes (48 bits)
Usage: Required for reading/writing data blocks

Key B: Not used (default value retained)
```

**Security Recommendations:**
```
Production Use:
├─ Change Key A from default
├─ Use unique keys per card (optional)
├─ Store keys securely
└─ Implement key management system

Current Implementation:
└─ Uses default Key A for simplicity
```

### Access Bits | บิตควบคุมการเข้าถึง

```
Default Access Bits: 0xFF 0x07 0x80 0x69

Interpretation:
Block 4: Read with Key A, Write with Key A
Block 5: Read with Key A, Write with Key A
Block 6: Read with Key A, Write with Key A
Block 7: Read Key A never, Write Key A

This allows:
✓ Public reading of thread codes
✓ Authenticated writing
✓ Key protection
```

## Data Validation Rules | กฎการตรวจสอบข้อมูล

### Thread Code Validation | การตรวจสอบรหัสด้าย

```python
def validate_thread_code(code: str) -> bool:
    """
    Validate thread code format
    
    Rules:
    1. Length: 0-16 characters
    2. Characters: ASCII printable (0x20-0x7E)
    3. Non-empty for normal operation
    4. Special: "bypass" keyword allowed
    """
    if len(code) == 0:
        return False  # Empty not allowed
    
    if len(code) > 16:
        return False  # Too long
    
    if code.lower() == "bypass":
        return True  # Bypass keyword
    
    if not code.isprintable():
        return False  # Non-printable characters
    
    return True
```

### Valid Character Set | ชุดตัวอักษรที่ใช้ได้

```
Allowed Characters:
├─ Letters: A-Z, a-z (0x41-0x5A, 0x61-0x7A)
├─ Numbers: 0-9 (0x30-0x39)
├─ Hyphen: - (0x2D)
├─ Underscore: _ (0x5F)
├─ Space: (0x20) - allowed but not recommended
└─ Other ASCII printable (0x20-0x7E)

Recommended Pattern:
[A-Z][A-Z0-9-_]* (uppercase, alphanumeric, hyphen, underscore)

Examples:
✓ TH-001
✓ RED-100
✓ COTTON_BLUE_01
✓ X123
✗ สีแดง (non-ASCII)
✗ TH#001 (special character #)
✗ (empty string)
✗ VERY-LONG-THREAD-NAME-EXCEEDS-16 (too long)
```

## Reading Data | การอ่านข้อมูล

### Read Procedure | ขั้นตอนการอ่าน

```
1. Wait for card
   └─ PICC_IsNewCardPresent()

2. Select card
   └─ PICC_ReadCardSerial()

3. Authenticate Block 4
   ├─ PCD_Authenticate(PICC_CMD_MF_AUTH_KEY_A, 4, key, uid)
   └─ Check status

4. Read Block 4
   ├─ MIFARE_Read(4, buffer, size)
   └─ Parse Thread 1 code

5. Authenticate Block 5
   ├─ PCD_Authenticate(PICC_CMD_MF_AUTH_KEY_A, 5, key, uid)
   └─ Check status

6. Read Block 5
   ├─ MIFARE_Read(5, buffer, size)
   └─ Parse Thread 2 code

7. Process data
   ├─ Convert bytes to string
   ├─ Trim NULL padding
   ├─ Validate format
   └─ Check for bypass keyword

8. Halt card
   └─ PICC_HaltA()
```

### Data Parsing | การแปลงข้อมูล

```cpp
String parseThreadCode(byte* buffer, byte size) {
    String code = "";
    
    // Read until NULL or end of buffer
    for (byte i = 0; i < size && i < 16; i++) {
        if (buffer[i] == 0x00) {
            break;  // End of string
        }
        
        // Only printable ASCII
        if (buffer[i] >= 0x20 && buffer[i] <= 0x7E) {
            code += (char)buffer[i];
        }
    }
    
    code.trim();  // Remove whitespace
    return code;
}
```

## Writing Data | การเขียนข้อมูล

### Write Procedure | ขั้นตอนการเขียน

```
1. Prepare data
   ├─ Validate thread codes
   ├─ Convert to ASCII bytes
   └─ Pad to 16 bytes with NULL

2. Wait for card
   └─ Wait for PICC presence

3. Select card
   └─ Read card serial

4. Write Thread 1
   ├─ Authenticate Block 4
   ├─ Write 16 bytes to Block 4
   └─ Verify status

5. Write Thread 2
   ├─ Authenticate Block 5
   ├─ Write 16 bytes to Block 5
   └─ Verify status

6. Verify write
   ├─ Read back Block 4
   ├─ Read back Block 5
   └─ Compare with expected

7. Halt card
   └─ PICC_HaltA()
```

### Data Preparation | การเตรียมข้อมูล

```python
def prepare_block_data(thread_code: str) -> bytes:
    """
    Prepare thread code for writing to MIFARE block
    
    Input: "TH-001"
    Output: b'TH-001\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    """
    # Convert to bytes
    data = thread_code.encode('ascii')
    
    # Pad to 16 bytes with NULL
    padded = data.ljust(16, b'\x00')
    
    return padded[:16]  # Ensure exactly 16 bytes
```

## Data Examples | ตัวอย่างข้อมูล

### Example 1: Standard Kanban Card

```
Block 4 (Thread 1): "TH-001"
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 54 48 2D 30 30 31 00 00 00 00 00 00 00 00 00 00 │
│ ASCII  │ T  H  -  0  0  1  .  .  .  .  .  .  .  .  .  . │
└────────────────────────────────────────────────────────────┘

Block 5 (Thread 2): "TH-002"
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 54 48 2D 30 30 32 00 00 00 00 00 00 00 00 00 00 │
│ ASCII  │ T  H  -  0  0  2  .  .  .  .  .  .  .  .  .  . │
└────────────────────────────────────────────────────────────┘
```

### Example 2: Bypass Card

```
Block 4 (Thread 1): "bypass"
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 62 79 70 61 73 73 00 00 00 00 00 00 00 00 00 00 │
│ ASCII  │ b  y  p  a  s  s  .  .  .  .  .  .  .  .  .  . │
└────────────────────────────────────────────────────────────┘

Block 5 (Thread 2): Empty (ignored)
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 │
│ ASCII  │ .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . │
└────────────────────────────────────────────────────────────┘
```

### Example 3: Color-Based Codes

```
Block 4 (Thread 1): "RED-COTTON-01"
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 52 45 44 2D 43 4F 54 54 4F 4E 2D 30 31 00 00 00 │
│ ASCII  │ R  E  D  -  C  O  T  T  O  N  -  0  1  .  .  . │
└────────────────────────────────────────────────────────────┘

Block 5 (Thread 2): "BLUE-POLY-02"
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 42 4C 55 45 2D 50 4F 4C 59 2D 30 32 00 00 00 00 │
│ ASCII  │ B  L  U  E  -  P  O  L  Y  -  0  2  .  .  .  . │
└────────────────────────────────────────────────────────────┘
```

### Example 4: Cleared Card

```
Block 4: All NULL
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 │
│ ASCII  │ .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . │
└────────────────────────────────────────────────────────────┘

Block 5: All NULL
┌────────────────────────────────────────────────┐
│ Offset │ 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F │
├────────┼────────────────────────────────────────────────┤
│ Hex    │ 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 │
│ ASCII  │ .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . │
└────────────────────────────────────────────────────────────┘
```

## Error Handling | การจัดการข้อผิดพลาด

### Read Errors | ข้อผิดพลาดการอ่าน

```
Error: Authentication Failed
├─ Cause: Wrong key, damaged card
├─ Action: Try default key, replace card
└─ Code: STATUS_AUTH_ERROR

Error: Read Timeout
├─ Cause: Card removed, RF interference
├─ Action: Retry, check card placement
└─ Code: STATUS_TIMEOUT

Error: Invalid Data
├─ Cause: Corrupted block, wrong format
├─ Action: Clear card, rewrite data
└─ Code: STATUS_INVALID_DATA
```

### Write Errors | ข้อผิดพลาดการเขียน

```
Error: Write Failed
├─ Cause: Read-only block, authentication failure
├─ Action: Check block number, verify key
└─ Code: STATUS_WRITE_ERROR

Error: Verification Failed
├─ Cause: Data mismatch after write
├─ Action: Retry write, replace card
└─ Code: STATUS_VERIFY_ERROR
```

## Best Practices | แนวทางปฏิบัติที่ดี

### Thread Code Naming | การตั้งชื่อรหัสด้าย

```
Recommended Format:
[Category]-[Subcategory]-[Number]

Examples:
TH-001          Simple numbered
RED-100         Color-based
POLY-BLU-01     Material-Color-Number
ACME-X200       Brand-Model

Guidelines:
✓ Keep concise (≤16 chars)
✓ Use uppercase for consistency
✓ Use hyphens for readability
✓ Include numbers for versioning
✓ Avoid special characters
```

### Card Management | การจัดการการ์ด

```
1. Preparation:
   ├─ Pre-write batch of cards
   ├─ Label cards clearly
   ├─ Store in holders
   └─ Keep inventory

2. Usage:
   ├─ Handle carefully
   ├─ Keep clean and dry
   ├─ Avoid bending
   └─ Single card per operation

3. Maintenance:
   ├─ Clean regularly
   ├─ Check for damage
   ├─ Test periodically
   └─ Replace worn cards

4. Security:
   ├─ Control access to blank cards
   ├─ Secure bypass cards
   ├─ Track card usage
   └─ Audit regularly
```

## Future Extensions | การขยายในอนาคต

### Block 6 Potential Uses | การใช้งาน Block 6 ในอนาคต

```
Option 1: Metadata
├─ Batch number (4 bytes)
├─ Creation date (4 bytes)
├─ Expiry date (4 bytes)
└─ Checksum (4 bytes)

Option 2: Extended Data
├─ Thread 3 code (16 bytes)

Option 3: Quality Data
├─ Tension specification (2 bytes)
├─ Speed limit (2 bytes)
├─ Reserved (12 bytes)
```

### Multiple Thread Support | รองรับหลายด้าย

```
Current: 2 threads (Blocks 4-5)
Future: 4-6 threads (Blocks 4-9 in multiple sectors)

Extended Format:
Sector 1: Thread 1-2
Sector 2: Thread 3-4
Sector 3: Thread 5-6
```

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-19  
**Author:** CWT Team  
**Standard:** MIFARE Classic 1K, ISO/IEC 14443-3
