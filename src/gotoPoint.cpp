#include "../../header/common/gotoPoint.hpp"
#include <iostream>

GotoPoint * GotoPoint::instance = NULL;

GotoPoint::GotoPoint(std::string stateLabel){
	this->stateLabel = stateLabel;
}

void GotoPoint::onEntry(Robot * robot, IWorldModel * worldModel){
	robot->isStopped = false;
	robot->resetRobotTimers();
	robot->move();
}

void GotoPoint::onState(Robot * robot, IWorldModel * worldModel){
	robot->setObjective(robot->xObj, robot->yObj);
	if(worldModelVss->isSlidingOnTheWall() == true or worldModelVss->isStuckAtByline() == true){
	robot->robotTimerSlidingOnTheWallrobot->robotTimerSlidingOnTheWall = r.;

	}
}

void GotoPoint::onExit(Robot * robot, IWorldModel * worldModel){
}

void GotoPoint::transition(Robot * robot, IWorldModel * worldModel){
	if(worldModelVss->robotTimerSlidingOnTheWall > 200){
	return StateFactory::getInstance("IsSlidingOnTheWall");
}
	if(worldModelVss->robotTimerSlidingOnTheWall > 80){
	return StateFactory::getInstance("IsStuckAtByline");
}
GotoPoint * GotoPoint::getInstance(std::string stateLabel){
	if(GotoPoint::instance == NULL)
		GotoPoint::instance = new GotoPoint(stateLabel);

	return GotoPoint::instance;
}