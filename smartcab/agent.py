import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        #Actions
        self.A = ['forward', 'left', 'right', None] #all the actions available
        self.trial = 0

        #Initialize Q table(light, oncoming, next_waypoint)
        self.Q={}
        for i in ['green', 'red']:  #possible lights
            for j in [None, 'forward', 'left', 'right']: #possible oncoming_agent
                for k in ['forward', 'left', 'right']: #possible next_waypoints
                    self.Q[(i,j,k)] = [1] * len(self.A)


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs['light'], inputs['oncoming'], self.next_waypoint)
        #Find the max Q value for the current state
        max_Q = self.Q[self.state].index(max(self.Q[self.state]))

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.8, display=True)  # create simulator (uses pygame when display=True, if available)
    sim.run(n_trials=100)  # run for a specified number of trials


if __name__ == '__main__':
    run()
