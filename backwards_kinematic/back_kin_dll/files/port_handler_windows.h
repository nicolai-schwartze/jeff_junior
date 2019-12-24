/*******************************************************************************
* Copyright 2017 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

/* Author: Ryu Woon Jung (Leon) */

#ifndef DYNAMIXEL_SDK_INCLUDE_DYNAMIXEL_SDK_WINDOWS_PORTHANDLERWINDOWS_C_H_
#define DYNAMIXEL_SDK_INCLUDE_DYNAMIXEL_SDK_WINDOWS_PORTHANDLERWINDOWS_C_H_

#include <Windows.h>
#include "port_handler.h"

uint8_t setupPortWindows            (int port_num, const int baudrate);

double  getCurrentTimeWindows       (int port_num);
double  getTimeSinceStartWindows    (int port_num);

int     portHandlerWindows          (const char *port_name);

uint8_t openPortWindows             (int port_num);
void    closePortWindows            (int port_num);
void    clearPortWindows            (int port_num);

void    setPortNameWindows          (int port_num, const char* port_name);
char   *getPortNameWindows          (int port_num);

uint8_t setBaudRateWindows          (int port_num, const int baudrate);
int     getBaudRateWindows          (int port_num);

int     readPortWindows             (int port_num, uint8_t *packet, int length);
int     writePortWindows            (int port_num, uint8_t *packet, int length);

void    setPacketTimeoutWindows     (int port_num, uint16_t packet_length);
void    setPacketTimeoutMSecWindows (int port_num, double msec);
uint8_t isPacketTimeoutWindows      (int port_num);

#endif /* DYNAMIXEL_SDK_INCLUDE_DYNAMIXEL_SDK_LINUX_PORTHANDLERWINDOWS_C_H_ */
