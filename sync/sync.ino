#include <Arduino.h>
#include <Streaming.h>
#include <Vector.h>

/*

*/
const int maxTimestampCount = 10;
const int numInputs = 1;
const int controlPin = 2;

int inputPins[numInputs];
int inputVals[numInputs];
int indices[numInputs];
int timestamps[numInputs][maxTimestampCount];

bool running = false;
int controlVal = 0;

void setup() {
  // initialise Serial connection
  Serial.begin(9600);
  
  // initialise control pin
  pinMode(controlPin, INPUT);
  
  // initialise input pins, values and indices
  for (int i = 0; i < numInputs; i++) {
    inputPins[i] = 3 + i;
    inputVals[i] = 0;
    indices[i] = 0;
    pinMode(inputPins[i], INPUT);
  }
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
    Serial << "start/stop received" << endl;
    running = not running;
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
// input pins. We get the current timestamp in microseconds
// (should have 1ms resolution on the Due) and record it in
// the array for the specified input pin. If the array is
// full, we instead just print it out.
void handleInput(int i) {
  if (indices[i] < maxTimestampCount) {
    int ts = micros();
    Serial << i << ": " << ts << endl;
    timestamps[i][indices[i]] = ts;
    indices[i] = indices[i] + 1;
  } else {
    printArray(timestamps[i], maxTimestampCount);
  }
}

// helper function to print an array to Serial
void printArray(int* arr, int len) {
  Serial << "[";
  for (int i = 0; i < len; i++) {
    Serial << arr[i] << ", ";
  }
  Serial << "]" << endl;
}