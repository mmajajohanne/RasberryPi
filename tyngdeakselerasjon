/*
 / Verifying Earth's Gravitational Acceleration
*/
#include <wiringPi.h>
#include <iostream>
#include <ctime>
  
using namespace std;
 
int main(void)
{
     
    clock_t startTime;
    clock_t endTime;
    double duration = 0;
     
    int sensor_upper_pin = 0; // Set upper sensor pin.
    int sensor_lower_pin = 2;// Set lower sensor pin.
         
    int sensor_upper = 0;
    int sensor_lower = 0;
     
    int iteration_num = 0;
     
    wiringPiSetup();
 
    pinMode(sensor_upper_pin, INPUT); // Set upper sensor to input.
    pinMode(sensor_lower_pin, INPUT); // Set lower sensor to input.
 
    while(1)
        {
        sensor_upper = digitalRead(sensor_upper_pin); // Continually check upper sensor for input.
        if (sensor_upper == 0) // When ball passes upper sensor,
            {
            startTime = clock(); // start clock.
            sensor_lower = digitalRead(sensor_lower_pin); // Continually check lower sensor for input.
             
            while (sensor_lower == 1) // While no input from lower sensor.
                {
                sensor_lower = digitalRead(sensor_lower_pin); // Do nothing.
                }
             
            endTime = clock(); // Stop clock when ball passes lower sensor.
            duration = (endTime - startTime) / (double) CLOCKS_PER_SEC; // Calculate time difference between readings.
             
            iteration_num++;
            cout<<"\nIteration "<<iteration_num<<".\nTime between sensor detections: "<<duration<<" seconds."<<endl; // Output duration.
            }
        }
return 0;
}
