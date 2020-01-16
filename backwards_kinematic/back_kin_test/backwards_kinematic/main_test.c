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
	robot_stop(pn);
	return 0;
}