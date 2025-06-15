#include "../../header/common/shotToGoal.hpp"
#include <iostream>

ShotToGoal * ShotToGoal::instance = NULL;

ShotToGoal::ShotToGoal(std::string stateLabel){
	this->stateLabel = stateLabel;
}

void ShotToGoal::onEntry(Robot * robot, IWorldModel * worldModel){
	robot->move();
	robot->resetRobotTimers();
}

void ShotToGoal::onState(Robot * robot, IWorldModel * worldModel){
	robot->setObjective(worldModelVss->ball);
	if(worldModelVss->isStuckAtByline(robot) == true){
	robot->incrementRobotTimerStuckWithWall();

	}
}

void ShotToGoal::onExit(Robot * robot, IWorldModel * worldModel){
	robot->move();
}

void ShotToGoal::transition(Robot * robot, IWorldModel * worldModel){
	if(worldModelVss->distanceTo(robot, worldModelVss->ball) > 0.15){
	return StateFactory::getInstance("GotoBall");
}
	if(worldModelVss->isAtAtkPosition(worldModelVss->ball) == true && worldModelVss->isNearBall(robot) == true && (robot->y > 0.4 || robot->y < 0.4)){
	return StateFactory::getInstance("SpinATK");
}
	if(robot->robotTimerSlidingOnTheWall > 80){
	return StateFactory::getInstance("IsStuckAtByline");
}
	if(robot->robotTimer > 100){
	return StateFactory::getInstance("IsNotMoving");
}
	if(worldModelVss->isPlayingLeft == true && robot->x < 0.65 || worldModelVss->isPlayingLeft == false && robot->x > 0.65 || worldModelVss->isNearToDeffenseArea(robot) == true){
	return StateFactory::getInstance("BackOff");
}
}

ShotToGoal * ShotToGoal::getInstance(std::string stateLabel){
	if(ShotToGoal::instance == NULL)
		ShotToGoal::instance = new ShotToGoal(stateLabel);

	return ShotToGoal::instance;
}