#include <conio.h>
#include <stdlib.h>
#include <stdio.h>
#include <windows.h>
#include "dynamixel_sdk.h"                                  

#define ADDR_TORQUE_ENABLE				64                 
#define ADDR_GOAL_POSITION				116
#define ADDR_PRESENT_POSITION			132

#define PROTOCOL_VERSION                2.0                 

#define MOTOR_ID_0						0                   
#define MOTOR_ID_1						1
#define MOTOR_ID_2						2
#define DEVICENAME                      "COM3"				

#define TORQUE_ENABLE                   1                   
#define TORQUE_DISABLE                  0        

#define ANGLE_STEP						651.89864690
#define MAX_POS							4096
#define POS_ERROR						3

#define PI								3.14159265
#define A2								50
#define A3								100
#define D1								100
#define DF								68

int back_kin(float x, float y, float z, float alpha, float beta, float gamma);
