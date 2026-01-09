/*
 * CWT Thread Verification System - Machine Controller
 * ESP32 Firmware for Thread Verification using RFID Kanban and Dual QR Scanners
 * 
 * Features:
 * - MFRC522 RFID reader for Kanban cards
 * - Dual GM65 QR scanners for thread verification
 * - Proximity sensors for bobbin detection
 * - LED indicators (Ready/Alarm)
 * - Machine relay control
 * - Bypass mode support
 * 
 * Author: CWT Team
 * Version: 1.0.0
 * License: MIT
 */

#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <HardwareSerial.h>

// =============== PIN DEFINITIONS ===============
// MFRC522 RFID Reader (SPI)
#define RFID_SS_PIN     5
#define RFID_RST_PIN    22
#define RFID_SCK_PIN    18
#define RFID_MOSI_PIN   23
#define RFID_MISO_PIN   19

// GM65 QR Scanner 1 (Hardware Serial1 with custom pins)
#define QR1_RX_PIN      4
#define QR1_TX_PIN      2
#define QR1_TRIG_PIN    12  // Changed from 15 to avoid boot issues

// GM65 QR Scanner 2 (Hardware Serial2 - U2_RXD/U2_TXD)
#define QR2_RX_PIN      16
#define QR2_TX_PIN      17
#define QR2_TRIG_PIN    13

// Proximity Sensors
#define BOBBIN1_PIN     32
#define BOBBIN2_PIN     33

// LED Indicators
#define LED_READY1_PIN  25
#define LED_READY2_PIN  26
#define LED_ALARM1_PIN  27
#define LED_ALARM2_PIN  14

// Machine Outputs
#define MACHINE_OUT1_PIN 21
// #define MACHINE_OUT2_PIN 15  // Reserved for V2 (connect through ULN2003A)

// =============== CONSTANTS ===============
#define BLOCK_THREAD1   4
#define BLOCK_THREAD2   5
#define BLOCK_SIZE      16
#define QR_TIMEOUT      5000
#define SCAN_RETRY      3
#define BYPASS_KEYWORD  "bypass"

// =============== GLOBAL OBJECTS ===============
MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);
MFRC522::MIFARE_Key key;
HardwareSerial qrScanner1(1);  // Use UART1 with custom pins
HardwareSerial qrScanner2(2);  // Use UART2 (GPIO16/17)

// =============== STATE MACHINE ===============
enum SystemState {
    STATE_INIT,
    STATE_WAIT_KANBAN,
    STATE_READ_KANBAN,
    STATE_WAIT_BOBBINS,
    STATE_SCAN_QR1,
    STATE_SCAN_QR2,
    STATE_VERIFY,
    STATE_READY,
    STATE_ERROR,
    STATE_BYPASS
};

SystemState currentState = STATE_INIT;

// =============== DATA STRUCTURES ===============
struct ThreadData {
    String thread1;
    String thread2;
    bool isBypass;
};

ThreadData kanbanData;
String qrCode1 = "";
String qrCode2 = "";
byte kanbanUID[10]; // Store Kanban card UID (max 10 bytes)
byte kanbanUIDSize = 0;

// =============== FUNCTION PROTOTYPES ===============
void setupPins();
void setupRFID();
void setupQRScanners();
void updateLEDs(bool ready1, bool ready2, bool alarm1, bool alarm2);
void setMachineOutput(bool enable);
void triggerQRScanner(int scannerNum);
String readQRCode(HardwareSerial& scanner, int timeoutMs);
bool readKanbanCard(ThreadData& data);
bool detectBobbin(int bobbinPin);
bool verifyThreads();
void handleStateMachine();
void printState(SystemState state);
String byteArrayToString(byte* buffer, byte bufferSize);

// =============== SETUP ===============
void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("\n\n========================================");
    Serial.println("  Thread Verification System");
    Serial.println("  ESP32 Machine Controller v1.0.0");
    Serial.println("========================================\n");
    
    setupPins();
    setupRFID();
    setupQRScanners();
    
    // Initialize default key (all 0xFF)
    for (byte i = 0; i < 6; i++) {
        key.keyByte[i] = 0xFF;
    }
    
    currentState = STATE_WAIT_KANBAN;
    Serial.println("System initialized. Waiting for Kanban card...\n");
}

// =============== MAIN LOOP ===============
void loop() {
    handleStateMachine();
    delay(100);
}

// =============== PIN SETUP ===============
void setupPins() {
    // QR Scanner triggers
    pinMode(QR1_TRIG_PIN, OUTPUT);
    pinMode(QR2_TRIG_PIN, OUTPUT);
    digitalWrite(QR1_TRIG_PIN, LOW);
    digitalWrite(QR2_TRIG_PIN, LOW);
    
    // Proximity sensors
    pinMode(BOBBIN1_PIN, INPUT);
    pinMode(BOBBIN2_PIN, INPUT);
    
    // LED outputs
    pinMode(LED_READY1_PIN, OUTPUT);
    pinMode(LED_READY2_PIN, OUTPUT);
    pinMode(LED_ALARM1_PIN, OUTPUT);
    pinMode(LED_ALARM2_PIN, OUTPUT);
    
    // Machine outputs
    pinMode(MACHINE_OUT1_PIN, OUTPUT);
    // pinMode(MACHINE_OUT2_PIN, OUTPUT);  // Reserved for V2
    
    // Initialize all outputs to safe state
    updateLEDs(false, false, false, false);
    setMachineOutput(false);
    
    Serial.println("[SETUP] Pins configured");
}

// =============== RFID SETUP ===============
void setupRFID() {
    // Explicit SPI pins for ESP32
    SPI.begin(RFID_SCK_PIN, RFID_MISO_PIN, RFID_MOSI_PIN, RFID_SS_PIN);
    
    // Set SS and RST as outputs
    pinMode(RFID_SS_PIN, OUTPUT);
    pinMode(RFID_RST_PIN, OUTPUT);
    
    // Hardware reset
    digitalWrite(RFID_RST_PIN, LOW);
    delay(50);
    digitalWrite(RFID_RST_PIN, HIGH);
    delay(50);
    
    rfid.PCD_Init(RFID_SS_PIN, RFID_RST_PIN);
    delay(100);
    
    // Debug SPI communication
    // Verify RFID reader is connected
    byte version = rfid.PCD_ReadRegister(rfid.VersionReg);
    Serial.print("[SETUP] MFRC522 Register: 0x");
    Serial.println(version, HEX);
    
    if (version == 0x00 || version == 0xFF) {
        Serial.println("[WARNING] MFRC522 not detected! Check wiring.");
        // Continue anyway for testing without hardware
    } else {
        Serial.println("[SETUP] MFRC522 initialized successfully");
    }
}

// =============== QR SCANNER SETUP ===============
void setupQRScanners() {
    // Initialize QR Scanner 1 on Serial1 with custom pins
    qrScanner1.begin(9600, SERIAL_8N1, QR1_RX_PIN, QR1_TX_PIN);
    
    // Initialize QR Scanner 2 on Serial2 with hardware UART pins
    qrScanner2.begin(9600, SERIAL_8N1, QR2_RX_PIN, QR2_TX_PIN);
    
    delay(100); // Allow serial ports to stabilize
    
    // TODO: Test with actual GM65 scanners
    Serial.println("[SETUP] QR scanners initialized (Hardware Serial)");
    // Serial.println("[INFO] QR Scanner 1 (Serial1): RX=GPIO4, TX=GPIO2, TRIG=GPIO12");
    // Serial.println("[INFO] QR Scanner 2 (Serial2): RX=GPIO16 (U2_RXD), TX=GPIO17 (U2_TXD), TRIG=GPIO13");
}

// =============== LED CONTROL ===============
void updateLEDs(bool ready1, bool ready2, bool alarm1, bool alarm2) {
    digitalWrite(LED_READY1_PIN, ready1 ? HIGH : LOW);
    digitalWrite(LED_READY2_PIN, ready2 ? HIGH : LOW);
    digitalWrite(LED_ALARM1_PIN, alarm1 ? HIGH : LOW);
    digitalWrite(LED_ALARM2_PIN, alarm2 ? HIGH : LOW);
}

// =============== MACHINE OUTPUT CONTROL ===============
void setMachineOutput(bool enable) {
    static bool lastState = false;
    static bool initialized = false;
    
    // Only update and print if state changed
    if (!initialized || lastState != enable) {
        digitalWrite(MACHINE_OUT1_PIN, enable ? HIGH : LOW);
        // digitalWrite(MACHINE_OUT2_PIN, enable ? HIGH : LOW);  // Reserved for V2
        Serial.print("[OUTPUT] Machine: ");
        Serial.println(enable ? "ENABLED" : "DISABLED");
        lastState = enable;
        initialized = true;
    }
    // Future V2: Add Machine 2 control
}

// =============== QR SCANNER TRIGGER ===============
void triggerQRScanner(int scannerNum) {
    // GM65 Serial command trigger: 7E 00 08 01 00 02 01 AB CD
    byte triggerCmd[] = {0x7E, 0x00, 0x08, 0x01, 0x00, 0x02, 0x01, 0xAB, 0xCD};
    
    HardwareSerial& scanner = (scannerNum == 1) ? qrScanner1 : qrScanner2;
    
    // Clear buffer before trigger
    while (scanner.available()) scanner.read();
    
    // Send serial trigger command
    scanner.write(triggerCmd, sizeof(triggerCmd));
    
    Serial.print("[QR] Triggered scanner ");
    Serial.print(scannerNum);
    Serial.println(" (Serial command)");
}

// =============== READ QR CODE ===============
String readQRCode(HardwareSerial& scanner, int timeoutMs) {
    String qrData = "";
    unsigned long startTime = millis();
    bool headerSkipped = false;
    int headerBytes = 0;
    
    // Wait for data with timeout
    // GM65 response format: [02][00][00][01][00][LEN_HIGH][LEN_LOW] + QR_DATA + [0D]
    // Skip first 7 bytes (header + length bytes)
    while (millis() - startTime < timeoutMs) {
        while (scanner.available()) {
            byte b = scanner.read();
            
            // Skip header bytes (first 7 bytes)
            if (!headerSkipped) {
                headerBytes++;
                if (headerBytes >= 7) {
                    headerSkipped = true;
                }
                continue;
            }
            
            // End of data (CR or LF)
            if (b == 0x0D || b == 0x0A) {
                if (qrData.length() > 0) {
                    break;
                }
                continue;
            }
            
            // Printable ASCII only
            if (b >= 32 && b <= 126) {
                qrData += (char)b;
            }
        }
        
        // Exit if we got data and saw end marker
        if (qrData.length() > 0 && headerSkipped) {
            // Check if no more data coming
            delay(50);
            if (!scanner.available()) break;
        }
        delay(10);
    }
    
    qrData.trim();
    return qrData;
}

// =============== READ KANBAN CARD ===============
bool readKanbanCard(ThreadData& data) {
    // Reset data
    data.thread1 = "";
    data.thread2 = "";
    data.isBypass = false;
    
    // Try to read card serial (card already detected in WAIT_KANBAN state)
    if (!rfid.PICC_ReadCardSerial()) {
        // If failed, try detecting again
        if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
            Serial.println("[DEBUG] Cannot read card serial");
            return false;
        }
    }   
    
    // Read Thread 1 from Block 4
    byte buffer1[18];
    byte size1 = sizeof(buffer1);
    MFRC522::StatusCode status;
    
    // Authenticate Block 4
    status = rfid.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, BLOCK_THREAD1, &key, &(rfid.uid));
    if (status != MFRC522::STATUS_OK) {
        Serial.print("[RFID] Authentication failed for Block 4: ");
        Serial.println(rfid.GetStatusCodeName(status));
        rfid.PICC_HaltA();
        return false;
    }
    
    // Read Block 4
    status = rfid.MIFARE_Read(BLOCK_THREAD1, buffer1, &size1);
    if (status != MFRC522::STATUS_OK) {
        Serial.print("[RFID] Read failed for Block 4: ");
        Serial.println(rfid.GetStatusCodeName(status));
        rfid.PICC_HaltA();
        return false;
    }
    
    data.thread1 = byteArrayToString(buffer1, 16);
    Serial.print("[RFID] Thread 1: ");
    Serial.println(data.thread1);
    
    // Check for bypass mode
    if (data.thread1.equalsIgnoreCase(BYPASS_KEYWORD)) {
        data.isBypass = true;
        Serial.println("[RFID] BYPASS MODE DETECTED");
        rfid.PICC_HaltA();
        return true;
    }
    
    // Read Thread 2 from Block 5
    byte buffer2[18];
    byte size2 = sizeof(buffer2);
    
    // Authenticate Block 5
    status = rfid.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, BLOCK_THREAD2, &key, &(rfid.uid));
    if (status != MFRC522::STATUS_OK) {
        Serial.print("[RFID] Authentication failed for Block 5: ");
        Serial.println(rfid.GetStatusCodeName(status));
        rfid.PICC_HaltA();
        return false;
    }
    
    // Read Block 5
    status = rfid.MIFARE_Read(BLOCK_THREAD2, buffer2, &size2);
    if (status != MFRC522::STATUS_OK) {
        Serial.print("[RFID] Read failed for Block 5: ");
        Serial.println(rfid.GetStatusCodeName(status));
        rfid.PICC_HaltA();
        return false;
    }
    
    data.thread2 = byteArrayToString(buffer2, 16);
    Serial.print("[RFID] Thread 2: ");
    Serial.println(data.thread2);
    
    rfid.PICC_HaltA();
    return true;
}

// =============== BOBBIN DETECTION ===============
bool detectBobbin(int bobbinPin) {
    // PNP sensor or active HIGH logic
    return digitalRead(bobbinPin) == HIGH;
}

// =============== THREAD VERIFICATION ===============
bool verifyThreads() {
    bool match1 = (qrCode1 == kanbanData.thread1);
    bool match2 = (qrCode2 == kanbanData.thread2);
    
    Serial.println("\n[VERIFY] Thread Verification:");
    Serial.print("  Thread 1: ");
    Serial.print(match1 ? "✓ MATCH" : "✗ MISMATCH");
    Serial.print(" (Kanban: ");
    Serial.print(kanbanData.thread1);
    Serial.print(", QR: ");
    Serial.print(qrCode1);
    Serial.println(")");
    
    Serial.print("  Thread 2: ");
    Serial.print(match2 ? "✓ MATCH" : "✗ MISMATCH");
    Serial.print(" (Kanban: ");
    Serial.print(kanbanData.thread2);
    Serial.print(", QR: ");
    Serial.print(qrCode2);
    Serial.println(")");
    
    return match1 && match2;
}

// =============== STATE MACHINE ===============
void handleStateMachine() {
    static unsigned long stateEntryTime = 0;
    static SystemState previousState = STATE_INIT;
    
    // Detect state change
    if (currentState != previousState) {
        stateEntryTime = millis();
        printState(currentState);
        previousState = currentState;
    }
    
    switch (currentState) {
        // ===== WAIT FOR KANBAN =====
        case STATE_WAIT_KANBAN: {
            static unsigned long lastDebug = 0;
            static bool readerReset = false;
            
            // Reset RFID reader once when entering this state to clear HALT status
            if (!readerReset) {
                rfid.PCD_Init();
                delay(50);
                readerReset = true;
                Serial.println("[DEBUG] RFID reader reset");
            }
            
            if (millis() - lastDebug > 2000) {
                lastDebug = millis();
                Serial.println("[DEBUG] Waiting for card... Place card on reader.");
            }
            
            // Blink READY LEDs every 1 second when waiting (no bobbin state)
            bool blinkState = (millis() / 1000) % 2 == 0;
            updateLEDs(blinkState, blinkState, false, false);
            setMachineOutput(false);
            
            if (rfid.PICC_IsNewCardPresent()) {
                Serial.println("[DEBUG] Card detected! Moving to READ_KANBAN");
                readerReset = false; // Reset flag for next time
                currentState = STATE_READ_KANBAN;
            }
            break;
        }
        
        // ===== READ KANBAN CARD =====
        case STATE_READ_KANBAN:
            Serial.println("[DEBUG] Attempting to read card...");
            if (readKanbanCard(kanbanData)) {
                // Store Kanban card UID for later comparison
                kanbanUIDSize = rfid.uid.size;
                for (byte i = 0; i < kanbanUIDSize; i++) {
                    kanbanUID[i] = rfid.uid.uidByte[i];
                }
                
                Serial.println("\n========== KANBAN DATA ==========");
                Serial.print("[RFID] Card detected!\n[RFID] UID: ");
                for (byte i = 0; i < rfid.uid.size; i++) {
                    Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
                    Serial.print(rfid.uid.uidByte[i], HEX);
                }
                Serial.println();
                Serial.print("Thread 1: \"");
                Serial.print(kanbanData.thread1);
                Serial.println("\"");
                Serial.print("Thread 2: \"");
                Serial.print(kanbanData.thread2);
                Serial.println("\"");
                Serial.print("Bypass: ");
                Serial.println(kanbanData.isBypass ? "YES" : "NO");
                
                if (kanbanData.isBypass) {
                    currentState = STATE_BYPASS;
                } else if (kanbanData.thread1.length() > 0 && kanbanData.thread2.length() > 0) {
                    currentState = STATE_WAIT_BOBBINS;
                } else {
                    Serial.println("[ERROR] Invalid Kanban data");
                    currentState = STATE_ERROR;
                }
            } else {
                // Failed to read, try again
                delay(500);
                currentState = STATE_WAIT_KANBAN;
            }
            break;
        
        // ===== WAIT FOR BOBBINS =====
        case STATE_WAIT_BOBBINS: {
            static unsigned long lastBobbinDebug = 0;
            bool bobbin1Present = detectBobbin(BOBBIN1_PIN);
            bool bobbin2Present = detectBobbin(BOBBIN2_PIN);
            
            // Debug bobbin status every 2 seconds
            if (millis() - lastBobbinDebug > 2000) {
                lastBobbinDebug = millis();
                Serial.print("[DEBUG] Bobbin1 (GPIO32): ");
                Serial.print(digitalRead(BOBBIN1_PIN));
                Serial.print(" -> ");
                Serial.println(bobbin1Present ? "PRESENT" : "NOT PRESENT");
                Serial.print("[DEBUG] Bobbin2 (GPIO33): ");
                Serial.print(digitalRead(BOBBIN2_PIN));
                Serial.print(" -> ");
                Serial.println(bobbin2Present ? "PRESENT" : "NOT PRESENT");
            }
            
            // Blink READY LEDs every 1 second when waiting for bobbins
            bool blinkState = (millis() / 1000) % 2 == 0;
            updateLEDs(blinkState, blinkState, false, false);
            
            if (bobbin1Present && bobbin2Present) {
                Serial.println("[INFO] Both bobbins detected");
                delay(500); // Debounce
                currentState = STATE_SCAN_QR1;
            }
            
            // Timeout after 30 seconds
            if (millis() - stateEntryTime > 30000) {
                Serial.println("[TIMEOUT] Waiting for bobbins");
                currentState = STATE_ERROR;
            }
            break;
        }
        
        // ===== SCAN QR CODE 1 =====
        case STATE_SCAN_QR1:
            Serial.println("[INFO] Scanning QR Code 1...");
            triggerQRScanner(1);
            delay(500);
            
            qrCode1 = readQRCode(qrScanner1, QR_TIMEOUT);
            
            if (qrCode1.length() > 0) {
                Serial.print("[SUCCESS] QR Code 1: ");
                Serial.println(qrCode1);
                Serial.println();
                updateLEDs(true, false, false, false);
                currentState = STATE_SCAN_QR2;
            } else {
                Serial.println("[ERROR] Failed to read QR Code 1");
                updateLEDs(false, false, true, false);
                currentState = STATE_ERROR;
            }
            break;
        
        // ===== SCAN QR CODE 2 =====
        case STATE_SCAN_QR2:
            Serial.println("[INFO] Scanning QR Code 2...");
            triggerQRScanner(2);
            delay(500);
            
            qrCode2 = readQRCode(qrScanner2, QR_TIMEOUT);
            
            if (qrCode2.length() > 0) {
                Serial.print("[SUCCESS] QR Code 2: ");
                Serial.println(qrCode2);
                updateLEDs(true, true, false, false);
                currentState = STATE_VERIFY;
            } else {
                Serial.println("[ERROR] Failed to read QR Code 2");
                updateLEDs(true, false, false, true);
                currentState = STATE_ERROR;
            }
            break;
        
        // ===== VERIFY THREADS =====
        case STATE_VERIFY:
            if (verifyThreads()) {
                Serial.println("[SUCCESS] Thread verification passed!");
                Serial.println("==================================");
                currentState = STATE_READY;
            } else {
                Serial.println("[ERROR] Thread verification failed!");
                Serial.println("==================================");
                currentState = STATE_ERROR;
            }
            break;
        
        // ===== READY (MACHINE ENABLED) =====
        case STATE_READY: {
            bool bobbin1Present = detectBobbin(BOBBIN1_PIN);
            bool bobbin2Present = detectBobbin(BOBBIN2_PIN);
            
            // Check if any bobbin is removed → restart entire system
            if (!bobbin1Present || !bobbin2Present) {
                Serial.println("[WARNING] Bobbin removed! Restarting system...");
                setMachineOutput(false);
                updateLEDs(false, false, true, true);
                delay(1000);
                // Clear all data
                kanbanData.thread1 = "";
                kanbanData.thread2 = "";
                kanbanData.isBypass = false;
                qrCode1 = "";
                qrCode2 = "";
                kanbanUIDSize = 0;
                currentState = STATE_WAIT_KANBAN;
                break;
            }
            
            // No need to check Kanban card - if removed, user will reset manually
            
            updateLEDs(true, true, false, false);
            setMachineOutput(true);
            break;
        }
        
        // ===== BYPASS MODE =====
        case STATE_BYPASS:
            updateLEDs(true, true, false, false);
            setMachineOutput(true);
            break;
        
        // ===== ERROR STATE =====
        case STATE_ERROR: {
            // ALARM LEDs solid ON when mismatch
            updateLEDs(false, false, true, true);
            setMachineOutput(false);
            
            bool bobbin1Present = detectBobbin(BOBBIN1_PIN);
            bool bobbin2Present = detectBobbin(BOBBIN2_PIN);
            
            // Reset when any bobbin removed (changing thread)
            if (!bobbin1Present || !bobbin2Present) {
                Serial.println("[INFO] Bobbin removed! Resetting system...");
                // Clear all data
                kanbanData.thread1 = "";
                kanbanData.thread2 = "";
                kanbanData.isBypass = false;
                qrCode1 = "";
                qrCode2 = "";
                delay(1000);
                currentState = STATE_WAIT_KANBAN;
            }
            break;
        }
        
        default:
            currentState = STATE_WAIT_KANBAN;
            break;
    }
}

// =============== UTILITY FUNCTIONS ===============
void printState(SystemState state) {
    Serial.print("\n[STATE] ");
    switch (state) {
        case STATE_INIT:         Serial.println("INIT"); break;
        case STATE_WAIT_KANBAN:  Serial.println("WAIT_KANBAN"); break;
        case STATE_READ_KANBAN:  Serial.println("READ_KANBAN"); break;
        case STATE_WAIT_BOBBINS: Serial.println("WAIT_BOBBINS"); break;
        case STATE_SCAN_QR1:     Serial.println("SCAN_QR1"); break;
        case STATE_SCAN_QR2:     Serial.println("SCAN_QR2"); break;
        case STATE_VERIFY:       Serial.println("VERIFY"); break;
        case STATE_READY:        Serial.println("READY"); break;
        case STATE_ERROR:        Serial.println("ERROR"); break;
        case STATE_BYPASS:       Serial.println("BYPASS"); break;
        default:                 Serial.println("UNKNOWN"); break;
    }
}

String byteArrayToString(byte* buffer, byte bufferSize) {
    String result = "";
    for (byte i = 0; i < bufferSize; i++) {
        if (buffer[i] == 0) break; // Stop at null terminator
        if (buffer[i] >= 32 && buffer[i] <= 126) { // Printable ASCII
            result += (char)buffer[i];
        }
    }
    result.trim();
    return result;
}
