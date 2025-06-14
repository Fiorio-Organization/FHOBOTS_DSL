#include "../../header/common/gotoPoint.hpp"
#include <iostream>

GotoPoint * GotoPoint::instance = NULL;

GotoPoint::GotoPoint(std::string stateLabel){
	this->stateLabel = stateLabel;
}

void GotoPoint::onEntry(Robot * robot, IWorldModel * worldModel){
	robot->isStopped = false;
	robot->robotTimer = 0;
	robot->move();
	robot->stop();
	int x = 0;
	float varY;
	x = 0;
	worldModelVss->isPlayingLeft = 0;
	worldModelVss->isStuck();
	robot->setObjective();
	robot->setOrientationObjective();
	robot->stop();
	worldModelVss->isStuck();
	robot->stop();
	robot->move();
	robot->setObjective();
}

	robot->robotTimer = 0;
