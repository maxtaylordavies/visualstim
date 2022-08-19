#include <Arduino.h>
#include <LiquidCrystal.h>
#include <SD.h>
#include <SPI.h>
//#include <Streaming.h>

const int maxTimestampCount = 10;
const int inputPinsStart = 3;
const int maxNumInputs = 6;
const int controlPin = 2;

int inputPins[maxNumInputs];
int inputVals[maxNumInputs];
int indices[maxNumInputs];
int timestamps[maxNumInputs][maxTimestampCount];

bool running = false;
int controlVal = 0;
int numInputs = 0;

byte off[8] = {B00000, B00000, B00000, B00000, B00000, B00000, B00000, B11111};
byte on[8] = {B11111, B11111, B11111, B11111, B11111, B11111, B11111, B11111};

// create LCD object - parameters: (rs, enable, d4, d5, d6, d7)
LiquidCrystal lcd(45, 43, 41, 39, 37, 35);

void setup() {
    // initialise serial connection
    Serial.begin(9600);

    // initialise LCD
    lcd.begin(16, 2);
    lcd.createChar(0, off);
    lcd.createChar(1, on);
    lcd.clear();
    delay(5000);

    // initialise SD
    writeStatus("initialising SD", 1000);
    if (!SD.begin(52)) {
        writeStatus("failed!", 0);
        while (1)
            ;
    }

    writeStatus("done!", 1000);

    // initialise control pin
    pinMode(controlPin, INPUT);

    // automatically determine which input pins are in use
    for (int i = inputPinsStart; i <= inputPinsStart + maxNumInputs; i++) {
        pinMode(i, INPUT);
        if (digitalRead(i) == 0) {
            Serial.println(i);

            inputPins[numInputs] = i;
            inputVals[numInputs] = 0;
            indices[numInputs] = 0;

            numInputs += 1;
        }
    }

    // initialise input pins, values and indices
    // for (int i = 0; i < numInputs; i++) {
    //     inputPins[i] = 3 + i;
    //     inputVals[i] = 0;
    //     indices[i] = 0;
    //     pinMode(inputPins[i], INPUT);
    // }

    writeStatus("waiting!", 0);
}

void loop() {
    // if we're running (start signal received and no
    // stop signal received), then loop through input
    // pins - if we receive a signal at any pin, then
    // call handleInput with the index of the pin
    if (running) {
        for (int i = 0; i < numInputs; i++) {
            if (checkPin(inputPins[i], &inputVals[i])) {
                handleInput(i);
            }
        }
    }

    // check for start/stop signal on control pin
    // - if signal received, change state accordingly
    if (checkPin(controlPin, &controlVal)) {
        running = !running;

        // if we've just received stop signal, then
        // run onStop function
        if (running) {
            writeStatus("running", 0);
        } else {
            onStop();
            writeStatus("waiting", 0);
        }
    }
}

// helper function to ensure no duplicate handling of inputs
// - accepts the pin number to check, and a pointer to the
// current value of that pin (0 or 1). Reads the pin, updates
// its value, and returns true only if the pin has just flipped
// from 0 to 1
bool checkPin(int pin, int *valPtr) {
    bool changed = false;
    int tmp = digitalRead(pin);
    if (tmp == 1 && *valPtr == 0) {
        changed = true;
    }
    *valPtr = tmp;
    return changed;
}

// helper function to handle a signal at one of the defined
// input pins. We get the current timestamp in micros conds
// (should have 1ms resolution on the Due) and record it in
// the array for the specified input pin. If the array is
// full, we instead just print it out.
void handleInput(int i) {
    if (indices[i] < maxTimestampCount) {
        timestamps[i][indices[i]] = micros();
        indices[i] = indices[i] + 1;
    }
    flash(i);
}

// function to run after stopping
void onStop() {
    // write timestamp arrays to file
    saveData();

    // reset arrays
    memset(timestamps, 0, sizeof(timestamps));
    memset(indices, 0, sizeof(indices));
}

// helper function to write current status
// to top row of 16x2 LCD
void writeStatus(char *status, int delayMs) {
    lcd.clear();
    lcd.setCursor(0, 0);  // first row
    lcd.print(status);

    if (status == "running") {
        int start = 15 - numInputs + 1;
        for (int i = 0; i < numInputs; i++) {
            lcd.setCursor(start + i, 0);
            lcd.print(i + 1);
            lcd.setCursor(start + i, 1);
            lcd.write(byte(0));
        }
    }

    delay(delayMs);
}

// helper function to flash the LCD indicator
// for a particular input
void flash(int idx) {
    int pos = 15 - numInputs + 1 + idx;
    lcd.setCursor(pos, 1);
    lcd.write(byte(1));
    delay(100);
    lcd.setCursor(pos, 1);
    lcd.write(byte(0));
}

// helper function to get number of next session file to write data to
int getSessNum() {
    File dir = SD.open("/sessions/");
    int sessNum = 0;

    while (true) {
        File entry = dir.openNextFile();
        if (!entry) {
            break;
        }

        String name = entry.name();
        int cutoff = name.lastIndexOf(".");
        int tmp = name.substring(7, cutoff).toInt();

        if (tmp > sessNum) {
            sessNum = tmp;
        }

        entry.close();
    }

    dir.close();
    return sessNum + 1;
}

// write the timestamps data to file (on SD card)
void saveData() {
    writeStatus("saving to SD...", 1000);

    // create the file
    char filename[30];
    sprintf(filename, "/sessions/session%d.txt", getSessNum());
    File f = SD.open(filename, FILE_WRITE);

    // if the file failed to open, log and return
    if (!f) {
        writeStatus("error creating file", 1000);
        return;
    }

    // otherwise, write the data to file
    for (int i = 0; i < numInputs; i++) {
        for (int j = 0; j < maxTimestampCount; j++) {
            f.print(timestamps[i][j]);
            f.print(",");
        }
        f.print("\n");
    }
    f.close();

    writeStatus("done!", 1000);
}
