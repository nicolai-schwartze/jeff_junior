# include <math.h>
# include "back_kin.h"

#if defined(__linux__)
#include "back_kin.h"
#elif defined(__APPLE__)
#include "back_kin.h"
#elif defined(_WIN32) || defined(_WIN64)
#define WINDLLEXPORT
#include "back_kin.h"
#endif

void back_kin(float z, float alpha, float beta, int port_num, int *goalPos);
int drive_to_goal_pos(int goalPos[3], int port_num);
int is_at_goal_pos(int goalPos[3], int port_num);


#pragma region user function

int robot_start() {

	int port_num = portHandler(DEVICENAME);
	packetHandler();
	openPort(port_num);

#pragma region Enable Torque
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
#pragma endregion

#pragma region Set max velocity
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_PROFILE_VELOCITY, MAX_V);
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_PROFILE_VELOCITY, MAX_V);
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_PROFILE_VELOCITY, MAX_V);
#pragma endregion

	return port_num;
}



int robot_drive(float z, float alpha, float beta, int port_num) {
	int goalPtr[3];
	back_kin(z, alpha, beta, port_num, goalPtr);
	drive_to_goal_pos(goalPtr, port_num);
}



int robot_reached_target(float z, float alpha, float beta, int port_num) {

	int goalPtr[3];
	back_kin(z, alpha, beta, port_num, goalPtr);
	// int goalPos[3] = { goalPtr[0], goalPtr[1], goalPtr[2] };
	return is_at_goal_pos(goalPtr, port_num);
}



void robot_home(int port_num) {

	int goalPos[3] = { HOME_0, HOME_1, HOME_2 };

	drive_to_goal_pos(goalPos, port_num);

	while (1) {
		if (is_at_goal_pos(goalPos, port_num)) {
			break;
		}
	}

}



void robot_set_theta(float theta0, float theta1, float theta2, int port_num) {
	int goalPtr[3];
	theta0 = (PI / 180) * theta0;
	theta1 = (PI / 180) * theta1;
	theta2 = (PI / 180) * theta2;
	goalPtr[0] = (int)(theta0 * ANGLE_STEP) + THETA_0_OFFSET;
	goalPtr[1] = (int)(theta1 * ANGLE_STEP) + THETA_1_OFFSET;
	goalPtr[2] = (int)(theta2 * ANGLE_STEP) + THETA_2_OFFSET;
	drive_to_goal_pos(goalPtr, port_num);
}



float robot_get_theta0(int port_num) {
	int currentPos = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_PRESENT_POSITION);
	float theta0 = ((float)(currentPos - THETA_0_OFFSET)) / ((float)ANGLE_STEP);
	theta0 = theta0 * (180 / PI);
	return theta0;
}



float robot_get_theta1(int port_num) {
	int currentPos = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_PRESENT_POSITION);
	float theta1 = ((float)(currentPos - THETA_1_OFFSET)) / ((float)ANGLE_STEP);
	theta1 = theta1 * (180 / PI);
	return theta1;
}



float robot_get_theta2(int port_num) {
	int currentPos = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_PRESENT_POSITION);
	float theta2 = ((float)(currentPos - THETA_2_OFFSET)) / ((float)ANGLE_STEP);
	theta2 = theta2 * (180 / PI);
	return theta2;
}




void robot_stop(int port_num) {

	robot_home(port_num);

#pragma region Disable Torque
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
#pragma endregion

	closePort(port_num);
}



#pragma endregion





#pragma region internal functions

void back_kin(float z, float alpha, float beta, int port_num, int *goalPos) {

	float theta[3] = { 0.0, 0.0, 0.0 };
	int retval = 0;

	alpha = (PI / 180) * alpha;
	beta = (PI / 180) * beta;

	//ToDo: replace angle test with actual formulas for bk
	theta[0] = alpha;
	theta[1] = asin((z - D1 - DF * sin((PI / 2) - beta)) / A3);
	theta[2] = beta - theta[1];

	goalPos[0] = (int)(theta[0] * ANGLE_STEP) + THETA_0_OFFSET;
	goalPos[1] = (int)(theta[1] * ANGLE_STEP) + THETA_1_OFFSET;
	goalPos[2] = (int)(theta[2] * ANGLE_STEP) + THETA_2_OFFSET;
}



int drive_to_goal_pos(int goalPos[3], int port_num) {

	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_GOAL_POSITION, goalPos[MOTOR_ID_0]);
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_GOAL_POSITION, goalPos[MOTOR_ID_1]);
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_GOAL_POSITION, goalPos[MOTOR_ID_2]);

	return 0;
}

int is_at_goal_pos(int goalPos[3], int port_num) {

	int upperLimit[3] = { 0, 0, 0 };
	int lowerLimit[3] = { 0, 0, 0 };
	upperLimit[0] = goalPos[0] + POS_ERROR;
	upperLimit[1] = goalPos[1] + POS_ERROR;
	upperLimit[2] = goalPos[2] + POS_ERROR;
	lowerLimit[0] = goalPos[0] - POS_ERROR;
	lowerLimit[1] = goalPos[1] - POS_ERROR;
	lowerLimit[2] = goalPos[2] - POS_ERROR;

	int currentPos[3] = { 0, 0, 0 };

	currentPos[0] = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_PRESENT_POSITION);
	currentPos[1] = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_PRESENT_POSITION);
	currentPos[2] = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_PRESENT_POSITION);

	// Problem:  when turning over the 0 - 4095 border this does not catch
	// Solution: since the robot can not structurally turn over that border this is not an issue
	if ((currentPos[0] <= upperLimit[0]) && (currentPos[0] >= lowerLimit[0]) &&
		(currentPos[1] <= upperLimit[1]) && (currentPos[1] >= lowerLimit[1]) &&
		(currentPos[2] <= upperLimit[2]) && (currentPos[2] >= lowerLimit[2]))
	{
		return 1;
	}

	else {
		return 0;
	}
}


#pragma endregion
