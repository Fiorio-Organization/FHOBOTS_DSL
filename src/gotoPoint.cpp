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
	robot->setObjective(	robot->x	robot->y);
	robot->setOrientationObjective();
	worldModelVss->isStuck();
	robot->stop();
	robot->stop();
	robot->isStopped	worldModelVss->isPlayingLeft	worldModelVss->isStuck();
	robot->isStopped	robot->stop();
	robot->move();
	robot->robotTimer	robot->setObjective(	robot->x	robot->y);
}

void GotoPoint::onState(Robot * robot, IWorldModel * worldModel){
	robot->stop();
	robot->isStopped	worldModelVss->isPlayingLeft	worldModelVss->isStuck();
	robot->isStopped	robot->stop();
	robot->move();
}

void GotoPoint::onExit(Robot * robot, IWorldModel * worldModel){
	robot->isStopped = false;
	varY = x;
	x = 0;
}

	robot->isStopped	worldModelVss->isStuck();
	robot->isStopped	float varX;
	x = varX;
	worldModelVss->isPlayingLeft = 1;
	robot->isStopped	x = varY;
GotoPoint * GotoPoint::getInstance(std::string stateLabel){
	if(GotoPoint::instance == NULL)
		GotoPoint::instance = new GotoPoint(stateLabel);

	return GotoPoint::instance;
}