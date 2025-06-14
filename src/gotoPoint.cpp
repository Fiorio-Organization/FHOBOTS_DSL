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
	worldModelVss->isPlayingLeft = 0;
	worldModelVss->isStuck();
	robot->setObjective();
	robot->setOrientationObjective();
}

	robot->robotTimer = 0;
