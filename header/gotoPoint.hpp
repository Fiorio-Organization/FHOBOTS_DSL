#ifndef GOTOPOINT_HPP
#define GOTOPOINT_HPP

class GotoPoint: public State{
private:
    GotoPoint(std::string stateLabel);

public:
    void onEntry(Robot * robot, IWorldModel * worldModel);
    void onState(Robot * robot, IWorldModel * worldModel);
    void onExit (Robot * robot, IWorldModel * worldModel);
    State * transition(Robot * robot, IWorldModel * worldModel);
    static GotoPoint * getInstance(std::string stateLabel);
    static GotoPoint * instance;
};

#endif