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
	robot->setObjective(robot->xrobot->y);
	robot->setOrientationObjective();
	if(((15 > 10 and 'a' != x) or world.worldModelVss->isStuck() == r.robot->stop())){
	robot->stop();
	if(r.robot->isStopped == false){
	if(world.worldModelVss->isPlayingLeft == true){
	worldModelVss->isStuck();

	}

	}
	else if(r.robot->isStopped != false){
	robot->stop();

	}

	}
	else{
	robot->move();

	}
	if(2 < 12){

	}
	else if(r.robot->robotTimer >= 10){
	robot->setObjective(robot->xrobot->y);

	}
}

void GotoPoint::onState(Robot * robot, IWorldModel * worldModel){
	if(15 > 10){
	robot->stop();
	worldModelVss->isPlayingLeft = 0;
	if(r.robot->isStopped == false){
	if(world.worldModelVss->isPlayingLeft == true){
	worldModelVss->isStuck();

	}

	}
	else if(r.robot->isStopped != false){
	robot->stop();

	}

	}
	else{
	robot->move();

	}
}

void GotoPoint::onExit(Robot * robot, IWorldModel * worldModel){
	robot->isStopped = false;
	varY = x;
	x = 0;
}

void GotoPoint::transition(Robot * robot, IWorldModel * worldModel){
	if(r.robot->isStopped == true or world.worldModelVss->isStuck() != false){
	return StateFactory::getInstance("Backoff");
}

if(robot->role == GoalkeeperRole::getInstance()) {
	if(r.robot->isStopped == true){
	float varX;
	x = varX;
	worldModelVss->isPlayingLeft = 1;
	return StateFactory::getInstance("SpinGK");
}
	if(r.robot->isStopped == true){
	x = varY;
	return StateFactory::getInstance("GotoBall");
}
}
}
GotoPoint * GotoPoint::getInstance(std::string stateLabel){
	if(GotoPoint::instance == NULL)
		GotoPoint::instance = new GotoPoint(stateLabel);

	return GotoPoint::instance;
}