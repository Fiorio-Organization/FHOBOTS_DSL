#include "../../header/common/gotoBall.hpp"
#include <iostream>

GotoBall * GotoBall::instance = NULL;

GotoBall::GotoBall(std::string stateLabel){
	this->stateLabel = stateLabel;
}

void GotoBall::onEntry(Robot * robot, IWorldModel * worldModel){
}

void GotoBall::onState(Robot * robot, IWorldModel * worldModel){
}

void GotoBall::onExit(Robot * robot, IWorldModel * worldModel){
}

void GotoBall::transition(Robot * robot, IWorldModel * worldModel){
}

GotoBall * GotoBall::getInstance(std::string stateLabel){
	if(GotoBall::instance == NULL)
		GotoBall::instance = new GotoBall(stateLabel);

	return GotoBall::instance;
}