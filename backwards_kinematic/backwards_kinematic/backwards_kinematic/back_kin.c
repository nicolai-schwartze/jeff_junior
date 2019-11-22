# include <math.h>
# include "back_kin.h"

int back_kin(float x, float y, float z, float alpha, float beta, float gamma) {

	int port_num = portHandler(DEVICENAME);
	packetHandler();
	openPort(port_num);

	float theta[3] = { 0.0, 0.0, 0.0 };
	int motorPos[3] = { 0, 0, 0 };
	int currentPos[3] = { 0, 0, 0 };
	int retval = 0;

	alpha = (PI / 180) * alpha;
	beta  = (PI / 180) * beta;
	gamma = (PI / 180) * gamma;

	//ToDo: replace angle test with actual formulas for bk
	theta[0] = alpha;
	theta[1] = beta;						//asin((z - D1 - DF * sin((PI / 2) - beta)) / A3);
	theta[2] = gamma;						//beta - theta[1];

	motorPos[0] = (int)(theta[0] * ANGLE_STEP);
	motorPos[1] = (int)(theta[1] * ANGLE_STEP);
	motorPos[2] = (int)(theta[2] * ANGLE_STEP);

	motorPos[0] = motorPos[0] % MAX_POS;
	motorPos[1] = motorPos[1] % MAX_POS;
	motorPos[2] = motorPos[2] % MAX_POS;

#pragma region Enable Torque
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
#pragma endregion

#pragma region Write Angle
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_GOAL_POSITION, motorPos[MOTOR_ID_0]);
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_GOAL_POSITION, motorPos[MOTOR_ID_1]);
	write4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_GOAL_POSITION, motorPos[MOTOR_ID_2]);
#pragma endregion
	
	int upperLimit[3] = { 0, 0, 0 };
	int lowerLimit[3] = { 0, 0, 0 };
	upperLimit[0] = motorPos[0] + POS_ERROR % MAX_POS;
	upperLimit[1] = motorPos[1] + POS_ERROR % MAX_POS;
	upperLimit[2] = motorPos[2] + POS_ERROR % MAX_POS;
	lowerLimit[0] = motorPos[0] - POS_ERROR % MAX_POS;
	lowerLimit[1] = motorPos[1] - POS_ERROR % MAX_POS;
	lowerLimit[2] = motorPos[2] - POS_ERROR % MAX_POS;

	while (1) {
		currentPos[0] = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_PRESENT_POSITION);
		currentPos[1] = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_PRESENT_POSITION);
		currentPos[2] = read4ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_PRESENT_POSITION);

		// Problem:  when turning over the 0 - 4095 border this does not catch
		// Solution: since the robot can not structurally turn over that border this is not an issue
		if ((currentPos[0] <= upperLimit[0]) && (currentPos[0] >= lowerLimit[0]) &&
			(currentPos[1] <= upperLimit[1]) && (currentPos[1] >= lowerLimit[1]) &&
			(currentPos[2] <= upperLimit[2]) && (currentPos[2] >= lowerLimit[2])) {
			break;
		}
		else {
			Sleep(100);
		}
	}

#pragma region Disable Torque
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_0, ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_1, ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
	write1ByteTxRx(port_num, PROTOCOL_VERSION, MOTOR_ID_2, ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
#pragma endregion

	closePort(port_num);
	return retval;
}