#ifndef GOTOBALL_HPP
#define GOTOBALL_HPP

class GotoBall: public State{
private:
    GotoBall(std::string stateLabel);

public:
    void onEntry(Robot * robot, IWorldModel * worldModel);
    void onState(Robot * robot, IWorldModel * worldModel);
    void onExit (Robot * robot, IWorldModel * worldModel);
    State * transition(Robot * robot, IWorldModel * worldModel);
    static GotoBall * getInstance(std::string stateLabel);
    static GotoBall * instance;
};

#endif