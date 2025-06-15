#ifndef SHOT_TO_GOAL_HPP
#define SHOT_TO_GOAL_HPP

class ShotToGoal: public State{
private:
    ShotToGoal(std::string stateLabel);

public:
    void onEntry(Robot * robot, IWorldModel * worldModel);
    void onState(Robot * robot, IWorldModel * worldModel);
    void onExit (Robot * robot, IWorldModel * worldModel);
    State * transition(Robot * robot, IWorldModel * worldModel);
    static ShotToGoal * getInstance(std::string stateLabel);
    static ShotToGoal * instance;
};

#endif