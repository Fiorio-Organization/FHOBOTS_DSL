#include "../../header/common/gotoBall.hpp"
#include <iostream>

GotoBall * GotoBall::instance = NULL;

GotoBall::GotoBall(std::string stateLabel){
    this->stateLabel = stateLabel;
}

void GotoBall::onEntry(Robot * robot, IWorldModel * worldModel){
