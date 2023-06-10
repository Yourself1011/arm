String angles[3];
void *SplitString(String str, String outputArray[3])
{
    // Split the string into substrings
    int StringCount = 0;
    while (str.length() > 0)
    {
        int index = str.indexOf(',');
        if (index == -1) // No space found
        {
            outputArray[StringCount++] = str;
            break;
        }
        else
        {
            outputArray[StringCount++] = str.substring(0, index);
            str = str.substring(index + 1);
        }
    }
}

void setup()
{
    Serial.begin(115200);
    Serial.setTimeout(5);
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

    Serial.print(F("Thumb moving to "));
    Serial.print(angles[0]);
    Serial.print(F(" degrees\t"));
    Serial.print(F("Index moving to "));
    Serial.print(angles[1]);
    Serial.print(F(" degrees\t"));
    Serial.print(F("Middle moving to "));
    Serial.print(angles[2]);
    Serial.print(F(" degrees\n"));
}
