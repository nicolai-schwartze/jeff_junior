#include <conio.h>
#include <stdlib.h>
#include <stdio.h>
#include <windows.h>
#include "dynamixel_sdk.h"        


#if defined(__linux__)
#define WINDECLSPEC
#elif defined(__APPLE__)
#define WINDECLSPEC
#elif defined(_WIN32) || defined(_WIN64)
#ifdef WINDLLEXPORT
#define WINDECLSPEC __declspec(dllexport)
#else
#define WINDECLSPEC __declspec(dllimport)
#endif
#endif

#ifdef __GNUC__
#define DEPRECATED __attribute__((deprecated))
#elif defined(_MSC_VER)
#define DEPRECATED __declspec(deprecated)
#else
#pragma message("WARNING: You need to implement DEPRECATED for this compiler")
#define DEPRECATED
#endif

#define ADDR_TORQUE_ENABLE				64                 
#define ADDR_GOAL_POSITION				116
#define ADDR_PRESENT_POSITION			132
#define ADDR_PROFILE_VELOCITY			112

#define PROTOCOL_VERSION                2.0                 

#define MOTOR_ID_0						0                   
#define MOTOR_ID_1						1
#define MOTOR_ID_2						2
#define DEVICENAME                      "COM3"				

#define TORQUE_ENABLE                   1                   
#define TORQUE_DISABLE                  0        

#define ANGLE_STEP						651.89864690
#define MAX_POS							4096
#define POS_ERROR						10

#define MAX_V							20
#define HOME_0							2290
#define HOME_1							2060
#define HOME_2							3072

#define THETA_0_OFFSET					2288
#define THETA_1_OFFSET					2060
#define THETA_2_OFFSET					3072

#define PI								3.14159265
#define A2								50
#define A3								100
#define D1								100
#define DF								68

WINDECLSPEC int robot_start();
WINDECLSPEC void robot_stop(int port_num);
WINDECLSPEC void robot_home(int port_num);
WINDECLSPEC int robot_drive(float z, float alpha, float beta, int port_num);
WINDECLSPEC int robot_reached_target(float z, float alpha, float beta, int port_num);
WINDECLSPEC void robot_set_theta(float theta0, float theta1, float theta2, int port_num);
WINDECLSPEC float robot_get_theta0(int port_num);
WINDECLSPEC float robot_get_theta1(int port_num);
WINDECLSPEC float robot_get_theta2(int port_num);