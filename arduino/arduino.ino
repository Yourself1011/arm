#include <Servo.h>
Servo thumb;
Servo index;
Servo middle;
Servo arm;

float angles[4];
void *SplitString(String str, float outputArray[4])
{
    // Split the string into substrings
    int StringCount = 0;
    while (str.length() > 0)
    {
        int index = str.indexOf(',');
        if (index == -1) // No space found
        {
            outputArray[StringCount++] = str.toFloat();
            break;
        }
        else
        {
            outputArray[StringCount++] = str.substring(0, index).toFloat();
            str = str.substring(index + 1);
        }
    }
}

void setup()
{
    Serial.begin(115200);
    Serial.setTimeout(5);
    thumb.attach(4);
    index.attach(5);
    middle.attach(3);
    arm.attach(2);

    thumb.write(139);
    index.write(135);
    middle.write(142);
    arm.write(0);
}
void loop()
{
    while (!Serial.available())
    {
    }
    // String x = Serial.readString();
    // Serial.print(x);
    // Serial.print(F("\n\n"));
    // angles[0] = x.substring(0,3);
    // angles[1] = x.substring(3,6);
    // angles[2] = x.substring(6,9);
    SplitString(Serial.readString(), angles);

    thumb.write(min(max(map(angles[0], -17, 17, 140, 50), 50), 140));
    index.write(min(max(map(angles[1], -10, 45, 136, 46), 50), 140));
    middle.write(min(max(map(angles[2], -10, 45, 143, 53), 50), 140));
    arm.write(min(max(0, angles[3]), 180));

    // Serial.print(F("Thumb moving to "));
    // Serial.print(angles[0]);
    // Serial.print(F(" degrees\t"));
    // Serial.print(F("Index moving to "));
    // Serial.print(angles[1]);
    // Serial.print(F(" degrees\t"));
    // Serial.print(F("Middle moving to "));
    // Serial.print(angles[2]);
    // Serial.print(F(" degrees\t"));
    // Serial.print(F("Arm moving to "));
    // Serial.print(angles[3]);
    // Serial.print(F(" degrees\n"));
}
