# include "back_kin.h"

int main()
{
	int pn = start_robot();
	home(pn);
	back_kin(200, 60, 15, pn);
	stop_robot(pn);
	return 0;
}