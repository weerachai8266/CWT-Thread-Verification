# Complete System Workflow
# ขั้นตอนการทำงานของระบบทั้งหมด

## Overview | ภาพรวม

This document provides detailed workflows for all operations in the CWT Thread Verification System, from initial setup to daily production use.

## Table of Contents | สารบัญ

1. [System Setup Workflow](#system-setup-workflow)
2. [Kanban Card Creation Workflow](#kanban-card-creation-workflow)
3. [Machine Operation Workflow](#machine-operation-workflow)
4. [Error Handling Workflows](#error-handling-workflows)
5. [Maintenance Workflows](#maintenance-workflows)

---

## System Setup Workflow

### Initial Hardware Installation | การติดตั้งฮาร์ดแวร์ครั้งแรก

```
┌─────────────────────────────────────────────────┐
│ STEP 1: Install Kanban Tool (Office PC)        │
└─────────────────────────────────────────────────┘

1.1 Prerequisites Check
    ├─ Windows 10+ computer available
    ├─ USB port free
    ├─ Internet connection for downloads
    └─ Administrator access

1.2 Install Software
    ├─ Download Python 3.11+
    ├─ Install Python (check "Add to PATH")
    ├─ Download project from GitHub
    ├─ Install dependencies: pip install -r requirements.txt
    └─ Test application: python main.py

1.3 Connect ACR122U Reader
    ├─ Plug into USB port
    ├─ Wait for Windows driver installation
    ├─ Verify in Device Manager
    └─ Test with Kanban Tool application

1.4 Verify Installation
    ├─ Open Kanban Tool
    ├─ Check "Reader: Connected" status
    ├─ Place test card
    ├─ Read/write test data
    └─ Confirm success

┌─────────────────────────────────────────────────┐
│ STEP 2: Install Machine System (Production)    │
└─────────────────────────────────────────────────┘

2.1 Mount Hardware Components
    ├─ Install ESP32 in enclosure
    ├─ Mount MFRC522 RFID reader
    │   └─ Position for easy card access
    ├─ Mount QR scanners (2x)
    │   └─ Aim at thread bobbin positions
    ├─ Install proximity sensors (2x)
    │   └─ Position to detect bobbin presence
    ├─ Install LED indicators (4x)
    │   └─ Position visible to operator
    └─ Connect relay to machine control

2.2 Wire Connections
    ├─ Power connections
    │   ├─ 5V supply for ESP32, QR scanners, relay
    │   └─ 12V supply for proximity sensors
    ├─ RFID reader (SPI)
    │   ├─ Connect as per PINOUT.md
    │   └─ Verify 3.3V power
    ├─ QR scanners (UART)
    │   ├─ Connect RX/TX for both scanners
    │   └─ Connect trigger signals
    ├─ Sensors, LEDs, Relay (GPIO)
    │   └─ Connect as per wiring diagram
    └─ Double-check all connections

2.3 Upload Firmware
    ├─ Connect ESP32 via USB
    ├─ Open PlatformIO
    ├─ Build project: pio run
    ├─ Upload: pio run --target upload
    ├─ Monitor serial: pio device monitor
    └─ Verify boot messages

2.4 Hardware Testing
    ├─ Test RFID reader
    │   ├─ Place Kanban card
    │   └─ Verify detection in serial log
    ├─ Test QR scanners
    │   ├─ Manually trigger each scanner
    │   └─ Scan test QR codes
    ├─ Test sensors
    │   ├─ Place object near each sensor
    │   └─ Verify detection
    ├─ Test LEDs
    │   └─ Verify all 4 LEDs light up
    └─ Test relay
        └─ Verify clicking sound

2.5 System Integration Test
    ├─ Load test Kanban card
    ├─ Place thread bobbins
    ├─ Run full verification cycle
    └─ Confirm machine enable/disable

┌─────────────────────────────────────────────────┐
│ STEP 3: Configure Thread Codes                 │
└─────────────────────────────────────────────────┘

3.1 Define Thread Coding System
    ├─ Decide naming convention
    │   Example: TH-XXX, COLOR-NUM, etc.
    ├─ Create thread code master list
    ├─ Document in spreadsheet
    └─ Communicate to all operators

3.2 Label Thread Spools
    ├─ Generate QR codes for each thread
    ├─ Print QR labels
    ├─ Apply to thread spools
    └─ Verify scanability

3.3 Create Initial Kanban Cards
    ├─ Identify work orders
    ├─ Write Kanban cards for each
    ├─ Test cards on machine
    └─ Store in card holder

┌─────────────────────────────────────────────────┐
│ STEP 4: Train Personnel                        │
└─────────────────────────────────────────────────┘

4.1 Train Supervisors
    ├─ Kanban Tool operation
    ├─ Card writing procedures
    ├─ Bypass card handling
    ├─ Troubleshooting basics
    └─ Safety guidelines

4.2 Train Operators
    ├─ Card placement technique
    ├─ LED indicator meanings
    ├─ Error response procedures
    ├─ Basic troubleshooting
    └─ When to call supervisor

4.3 Train Maintenance
    ├─ Hardware inspection
    ├─ Reader cleaning
    ├─ Connection checking
    ├─ Firmware updates
    └─ Bypass mode usage
```

---

## Kanban Card Creation Workflow

### Standard Kanban Card | การสร้างการ์ด Kanban ปกติ

```
┌─────────────────────────────────────────────────┐
│ Role: Supervisor                                │
│ Location: Office PC with Kanban Tool           │
│ Duration: 1-2 minutes per card                  │
└─────────────────────────────────────────────────┘

Step 1: Prepare Work Order Information
    │
    ├─ Receive work order from planning
    ├─ Identify required thread types
    ├─ Look up thread codes from master list
    │   Example:
    │   - Work Order: WO-12345
    │   - Thread 1: TH-RED-100 (red cotton)
    │   - Thread 2: TH-BLUE-200 (blue polyester)
    └─ Get blank Kanban card

Step 2: Open Kanban Tool
    │
    ├─ Double-click desktop shortcut
    ├─ Wait for application to load
    ├─ Verify "Reader: Connected" status
    └─ If not connected:
        ├─ Check USB connection
        ├─ Restart application
        └─ Call IT if problem persists

Step 3: Enter Thread Codes
    │
    ├─ Click in "Thread 1" field
    ├─ Type first thread code
    │   Example: TH-RED-100
    ├─ Check character count (must be ≤16)
    ├─ Click in "Thread 2" field
    ├─ Type second thread code
    │   Example: TH-BLUE-200
    ├─ Check character count
    └─ Double-check for typos

Step 4: Write to Card
    │
    ├─ Click "Write Kanban" button
    ├─ See log message: "Waiting for card..."
    ├─ Place blank card on ACR122U reader
    │   ├─ Center card on reader
    │   ├─ Keep card flat
    │   └─ Hold still for 2-3 seconds
    ├─ Watch for log messages:
    │   ├─ "Card detected" (green)
    │   ├─ "Block 4 written successfully"
    │   ├─ "Block 5 written successfully"
    │   └─ "Kanban card written and verified successfully"
    └─ See success dialog box

Step 5: Verify and Label
    │
    ├─ Click "Read Kanban" button
    ├─ Place same card on reader
    ├─ Verify codes match what you entered
    ├─ Remove card from reader
    ├─ Write work order number on card with marker
    │   Example: "WO-12345" on back of card
    └─ Place in "Ready for Production" holder

Step 6: Deliver to Operator
    │
    ├─ Attach work order printout to card
    ├─ Hand to operator
    ├─ Brief operator on job requirements
    └─ Log in production tracking system

┌─────────────────────────────────────────────────┐
│ Batch Card Creation (Multiple Same Cards)      │
└─────────────────────────────────────────────────┘

For creating multiple cards with identical thread codes:

1. Enter thread codes once
2. Write to first card
3. Remove card
4. Place second card
5. Click "Write Kanban" again
6. Repeat for all cards
7. Time: ~5 seconds per card

Total for 10 cards: ~1 minute
```

### Bypass Card Creation | การสร้างการ์ดบายพาส

```
┌─────────────────────────────────────────────────┐
│ Role: Supervisor/Manager Only                  │
│ Location: Office PC with Kanban Tool           │
│ Security Level: HIGH - Restricted Access       │
└─────────────────────────────────────────────────┘

⚠️ WARNING: Bypass cards skip all verification!
Use only for:
- Machine maintenance
- Emergency production
- System testing
- Special authorized cases

Step 1: Verify Authorization
    │
    ├─ Confirm need for bypass card
    ├─ Check authorization from manager
    ├─ Document reason in log book
    └─ Get approval signature

Step 2: Open Kanban Tool
    │
    └─ (Same as normal card)

Step 3: Create Bypass Card
    │
    ├─ Click "Write Bypass" button
    ├─ Read warning dialog carefully:
    │   "This will write a bypass card that skips verification.
    │    Are you sure you want to continue?"
    ├─ Click "Yes" if authorized
    ├─ Place blank card on reader
    ├─ Wait for success message
    └─ Remove card

Step 4: Mark and Secure
    │
    ├─ Use RED marker to write "BYPASS" on both sides
    ├─ Write date created
    ├─ Write authorized by (name)
    ├─ Place in RED card holder
    ├─ Store in locked cabinet
    └─ Log in bypass card register:
        ├─ Date/Time created
        ├─ Created by
        ├─ Authorized by
        └─ Purpose

Step 5: Controlled Distribution
    │
    ├─ Issue only to authorized personnel
    ├─ Record:
    │   ├─ Who took the card
    │   ├─ Date/Time issued
    │   ├─ Expected return time
    │   └─ Purpose of use
    ├─ Require signature
    └─ Set return reminder

Step 6: Return and Audit
    │
    ├─ Receive card back
    ├─ Record return date/time
    ├─ Verify card still has bypass data
    ├─ Return to locked storage
    └─ Weekly audit of bypass card usage
```

### Card Reuse/Clear Workflow | การใช้การ์ดซ้ำ

```
┌─────────────────────────────────────────────────┐
│ Reusing Cards for New Jobs                     │
└─────────────────────────────────────────────────┘

Scenario: Work order completed, card no longer needed

Step 1: Collect Used Card
    │
    ├─ Retrieve from production floor
    ├─ Verify job is complete
    └─ Remove any labels/markings if possible

Step 2: Clear Old Data
    │
    ├─ Open Kanban Tool
    ├─ Click "Clear Card" button
    ├─ Confirm action in dialog
    ├─ Place card on reader
    ├─ Wait for success
    └─ Card now blank

Step 3: Write New Data
    │
    ├─ Enter new thread codes
    ├─ Write to cleared card
    ├─ Verify new data
    └─ Label for new work order

Alternative: Direct Overwrite
    │
    ├─ Enter new thread codes
    ├─ Write directly (overwrites old data)
    └─ No need to clear first
```

---

## Machine Operation Workflow

### Normal Production Run | การผลิตปกติ

```
┌─────────────────────────────────────────────────┐
│ Role: Machine Operator                         │
│ Location: Production Floor                     │
│ Duration: 1-2 minutes setup, then continuous   │
└─────────────────────────────────────────────────┘

PHASE 1: Job Setup
══════════════════════════════════════════════════

Step 1: Receive Work Order
    │
    ├─ Supervisor delivers Kanban card + paperwork
    ├─ Review work order details
    │   ├─ Part number
    │   ├─ Quantity
    │   ├─ Required threads (listed)
    │   └─ Due date/time
    └─ Acknowledge receipt

Step 2: Read Kanban Card
    │
    ├─ Take Kanban card
    ├─ Place on machine RFID reader
    │   └─ Center on reader, keep flat
    ├─ Wait for system response (~1 second)
    ├─ System displays required threads:
    │   ├─ "Thread 1: TH-RED-100"
    │   └─ "Thread 2: TH-BLUE-200"
    ├─ Note required threads
    └─ Remove card (or leave on reader)

PHASE 2: Thread Loading
══════════════════════════════════════════════════

Step 3: Prepare Threads
    │
    ├─ Go to thread storage area
    ├─ Find first required thread
    │   └─ Scan QR label to verify code
    ├─ Find second required thread
    │   └─ Scan QR label to verify code
    ├─ Bring both spools to machine
    └─ Visual check: colors match work order

Step 4: Load Thread Spools
    │
    ├─ Remove old thread spools (if any)
    ├─ Place first spool on Position 1
    │   ├─ Ensure QR code faces scanner
    │   ├─ Secure spool on spindle
    │   └─ Thread through guides
    ├─ Place second spool on Position 2
    │   ├─ Ensure QR code faces scanner
    │   ├─ Secure spool on spindle
    │   └─ Thread through guides
    └─ Verify both spools seated properly

Step 5: Position for Scanning
    │
    ├─ Rotate spools so QR codes face scanners
    ├─ Ensure QR codes are:
    │   ├─ Clean (no thread debris)
    │   ├─ Not damaged
    │   └─ Within 10cm of scanner
    └─ Ready for automatic scan

PHASE 3: Automatic Verification
══════════════════════════════════════════════════

Step 6: System Detects Spools
    │
    ├─ Proximity sensors activate
    ├─ System logs: "Both bobbins detected"
    ├─ Orange LEDs blink (scanning in progress)
    └─ Watch for LED indicators

Step 7: QR Code Scanning
    │
    ├─ Scanner 1 activates (laser visible)
    ├─ Scans Thread 1 QR code
    ├─ Success: First LED turns GREEN
    ├─ Scanner 2 activates
    ├─ Scans Thread 2 QR code
    ├─ Success: Second LED turns GREEN
    └─ Total time: 2-5 seconds

Step 8: Thread Verification
    │
    ├─ System compares:
    │   ├─ QR Code 1 vs Kanban Thread 1
    │   └─ QR Code 2 vs Kanban Thread 2
    │
    ├─ IF MATCH:
    │   ├─ Both GREEN LEDs stay on
    │   ├─ Machine relay activates (audible click)
    │   ├─ Machine is ENABLED
    │   └─ Continue to Step 9
    │
    └─ IF MISMATCH:
        ├─ RED LEDs flash
        ├─ Machine stays DISABLED
        ├─ Alarm sounds (if configured)
        └─ Go to ERROR WORKFLOW (see below)

PHASE 4: Production
══════════════════════════════════════════════════

Step 9: Begin Sewing
    │
    ├─ Machine is enabled (green LEDs on)
    ├─ Perform machine checks:
    │   ├─ Tension settings
    │   ├─ Stitch type
    │   └─ Speed setting
    ├─ Run test piece
    ├─ Check quality
    └─ Start production

Step 10: During Production
    │
    ├─ Green LEDs remain on (system OK)
    ├─ Machine operates normally
    ├─ Monitor quality periodically
    ├─ If card is removed:
    │   ├─ Machine disables after current stitch
    │   ├─ Must re-verify to continue
    │   └─ Replace card to resume
    └─ Continue until job complete

Step 11: Job Completion
    │
    ├─ Finish last piece
    ├─ Remove Kanban card
    ├─ Machine disables (safe state)
    ├─ Remove thread spools (if changing job)
    ├─ Clean work area
    ├─ Return Kanban card to supervisor
    └─ Update production log

TOTAL TIME
══════════════════════════════════════════════════
Setup: 2-3 minutes
Verification: 5-10 seconds
Production: Varies by job
Changeover: 3-5 minutes
```

### Bypass Mode Operation | การทำงานโหมดบายพาส

```
┌─────────────────────────────────────────────────┐
│ Role: Authorized Personnel Only                │
│ Use Case: Maintenance, Testing, Emergency      │
└─────────────────────────────────────────────────┘

⚠️ This mode SKIPS thread verification!

Step 1: Obtain Bypass Card
    │
    ├─ Request from supervisor
    ├─ Sign bypass card log
    ├─ Verify RED "BYPASS" marking
    └─ Receive authorization

Step 2: Place Bypass Card
    │
    ├─ Place bypass card on RFID reader
    ├─ System detects "bypass" keyword
    ├─ Log shows: "BYPASS MODE DETECTED"
    └─ Machine enables immediately

Step 3: Operation
    │
    ├─ Both GREEN LEDs ON (bypass active)
    ├─ Machine enabled
    ├─ No thread verification performed
    ├─ Can use ANY threads
    └─ Operate machine as needed

Step 4: Return to Normal
    │
    ├─ Remove bypass card
    ├─ System returns to WAIT_KANBAN state
    ├─ Next job requires normal Kanban card
    ├─ Return bypass card to supervisor
    └─ Sign return in log
```

---

## Error Handling Workflows

### Thread Mismatch Error | ข้อผิดพลาดด้ายไม่ตรงกัน

```
┌─────────────────────────────────────────────────┐
│ SYMPTOM: Red LEDs flashing, machine disabled   │
│ CAUSE: Wrong thread loaded                     │
└─────────────────────────────────────────────────┘

Automatic Response:
    ├─ System sets state to ERROR
    ├─ RED LEDs flash (alternating)
    ├─ Machine output: OFF (disabled)
    └─ Serial log shows mismatch details

Operator Actions:

Step 1: Identify Problem
    │
    ├─ Note which LED is red (or both)
    ├─ Check serial monitor (if available):
    │   Example output:
    │   [VERIFY] Thread Verification:
    │   Thread 1: ✗ MISMATCH (Kanban: TH-001, QR: TH-999)
    │   Thread 2: ✓ MATCH (Kanban: TH-002, QR: TH-002)
    │
    └─ Identify wrong spool (Thread 1 in example)

Step 2: Remove Wrong Thread
    │
    ├─ Remove incorrect thread spool
    ├─ Return to storage
    └─ Note down correct code needed

Step 3: Get Correct Thread
    │
    ├─ Fetch correct thread spool
    ├─ Verify QR code matches requirement
    └─ Double-check label

Step 4: Reload Thread
    │
    ├─ Place correct spool on spindle
    ├─ Position QR code facing scanner
    ├─ Ensure spool is seated
    └─ Thread through guides

Step 5: Auto Re-verification
    │
    ├─ System automatically re-scans
    ├─ Waits for QR code read
    ├─ Performs verification again
    ├─ If correct:
    │   ├─ GREEN LEDs turn on
    │   ├─ RED LEDs turn off
    │   ├─ Machine enables
    │   └─ Ready to continue
    └─ If still wrong:
        └─ Repeat from Step 1

Step 6: Prevention
    │
    ├─ Note why wrong thread was selected
    ├─ Check if QR labels are clear
    ├─ Report to supervisor if:
    │   ├─ Multiple errors on same job
    │   ├─ QR labels damaged
    │   └─ Thread storage disorganized
    └─ Update training if needed

Time to resolve: 1-3 minutes
```

### Card Read Failure | ข้อผิดพลาดการอ่านการ์ด

```
┌─────────────────────────────────────────────────┐
│ SYMPTOM: "Failed to read Kanban" error         │
│ CAUSE: Card not detected, damaged, or dirty    │
└─────────────────────────────────────────────────┘

Step 1: Basic Troubleshooting
    │
    ├─ Remove card from reader
    ├─ Wait 2 seconds
    ├─ Place card again (centered, flat)
    ├─ Try 2-3 times
    └─ If still fails, continue

Step 2: Clean Card and Reader
    │
    ├─ Remove card
    ├─ Wipe card with soft cloth
    ├─ Check for visible damage
    ├─ Clean reader surface
    ├─ Remove any debris
    └─ Retry

Step 3: Try Different Card
    │
    ├─ Get another Kanban card for same job
    ├─ Test if it reads correctly
    ├─ If yes: Original card is damaged
    │   └─ Set aside for supervisor
    └─ If no: Reader may have issue

Step 4: Check Reader Connection
    │
    ├─ (For machine system) Not user-serviceable
    ├─ Call maintenance technician
    ├─ Report:
    │   ├─ When problem started
    │   ├─ Which cards fail
    │   └─ Any recent changes
    └─ Use bypass card if authorized (emergency)

Step 5: Temporary Workaround
    │
    ├─ Request bypass card from supervisor
    ├─ Document thread requirements manually
    ├─ Verify threads visually
    ├─ Continue production
    └─ Report for repair
```

### QR Scanner Failure | ข้อผิดพลาดการสแกน QR

```
┌─────────────────────────────────────────────────┐
│ SYMPTOM: "Failed to read QR Code" error        │
│ CAUSE: Scanner issue, dirty QR, positioning    │
└─────────────────────────────────────────────────┘

Step 1: Check QR Code
    │
    ├─ Inspect QR label on thread spool
    ├─ Check for:
    │   ├─ Dirt or debris
    │   ├─ Scratches or damage
    │   ├─ Peeling or fading
    │   └─ Thread wrapped over label
    ├─ Clean QR label if dirty
    └─ Rotate spool to fresh QR label if available

Step 2: Check Positioning
    │
    ├─ Ensure QR code faces scanner directly
    ├─ Distance: 5-15 cm from scanner
    ├─ Angle: Perpendicular to scanner
    ├─ Lighting: Not in direct sunlight
    └─ No obstacles between scanner and QR

Step 3: Manual Retry
    │
    ├─ Remove thread spool
    ├─ Reposition carefully
    ├─ Replace on spindle
    ├─ System retries automatically
    └─ Watch for green LED

Step 4: Scanner Malfunction
    │
    ├─ If repeated failures on multiple QR codes
    ├─ Scanner may be dirty or faulty
    ├─ Call maintenance
    ├─ Options:
    │   ├─ Clean scanner lens
    │   ├─ Adjust scanner angle
    │   ├─ Replace scanner
    │   └─ Use bypass (temporary)
    └─ Document for repair

Prevention:
    ├─ Print high-quality QR labels
    ├─ Use protective laminate
    ├─ Regular scanner cleaning
    └─ Proper spool storage
```

---

## Maintenance Workflows

### Daily Maintenance | การบำรุงรักษารายวัน

```
┌─────────────────────────────────────────────────┐
│ Role: Machine Operator or Maintenance          │
│ Frequency: Daily (start of shift)              │
│ Duration: 5-10 minutes                          │
└─────────────────────────────────────────────────┘

Morning Checklist:

□ Visual Inspection
  ├─ Check all LEDs light up (power test)
  ├─ Verify no physical damage
  └─ Ensure all cables connected

□ Clean RFID Reader
  ├─ Wipe surface with soft, dry cloth
  ├─ Remove any dust or debris
  └─ Check for damage

□ Clean QR Scanners
  ├─ Gently wipe lens with microfiber cloth
  ├─ Check laser activation (brief test)
  └─ Ensure no thread debris

□ Test System
  ├─ Place test Kanban card
  ├─ Load test thread spools
  ├─ Verify complete verification cycle
  ├─ Check all LEDs function
  └─ Confirm machine enable/disable

□ Log Results
  ├─ Record in maintenance log
  ├─ Note any issues
  └─ Report problems to supervisor

End of Shift:

□ Final Check
  ├─ Remove any cards from reader
  ├─ Clear work area
  └─ Note any issues for next shift
```

### Weekly Maintenance | การบำรุงรักษารายสัปดาห์

```
┌─────────────────────────────────────────────────┐
│ Role: Maintenance Technician                   │
│ Frequency: Weekly                              │
│ Duration: 15-30 minutes                         │
└─────────────────────────────────────────────────┘

Week Maintenance Checklist:

□ Hardware Inspection
  ├─ Tighten all screw terminals
  ├─ Check wire connections
  ├─ Inspect for wear or damage
  ├─ Test proximity sensors
  └─ Verify relay operation

□ Reader Calibration
  ├─ Test RFID with multiple cards
  ├─ Check read distance
  ├─ Clean contacts if needed
  └─ Document performance

□ Scanner Alignment
  ├─ Verify QR scanner angles
  ├─ Adjust if needed
  ├─ Test with various QR codes
  └─ Clean lens thoroughly

□ Software Check
  ├─ Review serial logs for errors
  ├─ Check for firmware updates
  ├─ Verify configuration
  └─ Backup settings if changed

□ Consumables
  ├─ Check LED brightness (replace if dim)
  ├─ Test relay contacts
  ├─ Inspect Kanban cards for wear
  └─ Order replacements if needed

□ Documentation
  ├─ Update maintenance log
  ├─ Record component replacements
  ├─ Note any modifications
  └─ File for audit trail
```

### Monthly Maintenance | การบำรุงรักษารายเดือน

```
┌─────────────────────────────────────────────────┐
│ Role: Maintenance Supervisor + IT              │
│ Frequency: Monthly                             │
│ Duration: 1-2 hours                            │
└─────────────────────────────────────────────────┘

□ Full System Test
  ├─ Run diagnostic tests
  ├─ Test all failure modes
  ├─ Verify bypass mode
  └─ Check timing accuracy

□ Firmware Update Check
  ├─ Check GitHub for updates
  ├─ Review change logs
  ├─ Test in development if major
  └─ Deploy if stable

□ Calibration Verification
  ├─ Test with calibrated instruments
  ├─ Verify sensor thresholds
  ├─ Check timing parameters
  └─ Document results

□ Security Audit
  ├─ Review bypass card usage
  ├─ Check RFID key security
  ├─ Audit access logs
  └─ Update procedures if needed

□ Performance Review
  ├─ Analyze error rates
  ├─ Review response times
  ├─ Check uptime statistics
  ├─ Identify improvement areas
  └─ Plan upgrades if needed

□ Training Review
  ├─ Assess operator proficiency
  ├─ Review error patterns
  ├─ Update training materials
  └─ Schedule refresher training
```

---

## Summary Flowchart | แผนภาพสรุป

```
                    START
                      │
                      ▼
        ┌─────────────────────────┐
        │  Create Kanban Card     │
        │  (Supervisor - Office)  │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Deliver to Operator    │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Place Card on Reader   │
        │  (Operator - Machine)   │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  System Reads Kanban    │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Load Thread Spools     │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  System Detects Bobbins │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Scan QR Codes          │
        └────────────┬────────────┘
                     │
                     ▼
             ┌───────────────┐
             │  Verify       │
             │  Match?       │
             └───┬───────┬───┘
                 │       │
            YES  │       │  NO
                 │       │
                 ▼       ▼
        ┌────────────┐  ┌────────────┐
        │ Enable     │  │ Disable    │
        │ Machine    │  │ + Alarm    │
        │ (GREEN)    │  │ (RED)      │
        └──────┬─────┘  └──────┬─────┘
               │                │
               │                ▼
               │        ┌────────────────┐
               │        │ Correct Thread │
               │        │ & Retry        │
               │        └────────┬───────┘
               │                 │
               └────<────────────┘
               │
               ▼
        ┌─────────────────────────┐
        │  Production Run         │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Job Complete           │
        │  Remove Card            │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Return Card/Report     │
        └────────────┬────────────┘
                     │
                     ▼
                    END
```

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-19  
**Author:** CWT Team  
**For:** Production and Maintenance Personnel
