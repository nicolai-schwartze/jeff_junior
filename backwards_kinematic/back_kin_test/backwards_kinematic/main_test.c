# include "back_kin.h"

int main()
{
	int pn = robot_start();
	robot_home(pn);
	robot_drive(200, 60, 15, pn);
	int retVal;
	while (1) {
		retVal = robot_reached_target(200, 60, 15, pn);
		printf(retVal ? "true\n" : "false\n");
		if (retVal) {
			break;
		}
	}
	robot_set_theta(0.0, 0.0, 0.0, pn);
	Sleep(3000);
	float theta0 = robot_get_theta0(pn);
	float theta1 = robot_get_theta1(pn);
	float theta2 = robot_get_theta2(pn);
	printf("%f, %f, %f \n", theta0, theta1, theta2);
	Sleep(3000);
	robot_set_theta(30.0, 30.0, -30.0, pn);
	Sleep(3000);
	theta0 = robot_get_theta0(pn);
	theta1 = robot_get_theta1(pn);
	theta2 = robot_get_theta2(pn);
	printf("%f, %f, %f \n", theta0, theta1, theta2);
	Sleep(3000);
	robot_stop(pn);
	return 0;
}