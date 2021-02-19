from packages.abm.agent_generator import AgentGenerator
from packages.abm.agent_mover import AgentMover


class ABM:
    """
    Defines the functionality for building and managing an agent-based model which simulates a SRI model over discrete
    time steps. Also defines functionality for capturing metrics for each time step.

    Fields:

        agents:          a list of Agents currently alive in the model

        counts:          a list of dictionaries, where each dictionary represents the metrics gathered for a single time step

        num_dead:        the number of Agents which have died and have been removed from the model by the current time step

        num_quarantined: the number of Agents which have a quarantine status in the current time step

        num_recovered:   the number of Agents which have a recovered status in the current time step

        num_susceptible: the number of Agents which have a susceptible status in the current time step

       status_colors:    defines the colors used for Agent statuses while debugging
    """

    status_colors = {'R': 'r', 'S': 'b', 'I': 'g', 'Q': 'k', 'D': 'm'}

    def __init__(self, n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated=0.0):
        """

        :param n: the dimension of the square torus grid used to define the world in which Agents move
        :param m: the number of Agents in the model
        :param num_infected: the number of Agents which have an infected status upon initialization
        :param percent_distancing: the percent of Agents which have a quarantine status upon initialization
        :param percent_mask: the percent of Agents which are masked upon initialization
        :param percent_vaccinated: the percent of Agents which have a recovered status upon initialization
        """
        self.n = n
        self.m = m

        # validate
        if m > n * n:
            raise ValueError('n x n grid cannot hold all agents')

        # generate agents
        ag = AgentGenerator(self.m, num_infected, percent_distancing, percent_mask, percent_vaccinated)
        self.agents = ag.generate_agents()

        # position agents
        am = AgentMover(self.n)
        am.position_agents(self.agents)

        # set baseline metrics
        self.counts = []
        self.num_recovered = 0
        self.num_infected = 0
        self.num_susceptible = 0
        self.num_dead = 0
        self.num_quarantine = 0

    def count_baseline_metrics(self):
        """
        Counts current values for baseline metrics.
        :return: None
        """
        for agent in self.agents:
            if agent.status == 'I':
                self.num_infected += 1
            elif agent.status == 'S':
                self.num_susceptible += 1
            elif agent.status == 'R':
                self.num_recovered += 1
            elif agent.status == 'Q':
                self.num_quarantine += 1

    def update_baseline_metrics(self, status_before, status_after):
        """
        Given the status before and after an Agent update, modifies the metrics stored in the ABM model as necessary.
        :param status_before: Agent status before update
        :param status_after: Agent status after
        :return: None
        """

        if status_before != status_after:

            # remove one from status_before
            if status_before == 'I':
                self.num_infected -= 1
            elif status_before == 'S':
                self.num_susceptible -= 1
            elif status_before == 'R':
                self.num_recovered -= 1
            elif status_before == 'Q':
                self.num_quarantine -= 1

            # add one to status_after
            if status_after == 'I':
                self.num_infected += 1
            elif status_after == 'S':
                self.num_susceptible += 1
            elif status_after == 'R':
                self.num_recovered += 1
            elif status_after == 'Q':
                self.num_quarantine += 1

    def remove_agent(self, agent):
        """
        Remove agent from simulation if agent has died and increments num_dead by 1.
        :param agent: Agent that died
        :return: None
        """
        self.agents.remove(agent)
        self.num_dead += 1

    def add_counts(self):
        """
        Generates a dictionary of the current metrics and adds the dictionary to the list of counts.
        :return: None
        """
        counts = {'R': self.num_recovered, 'D': self.num_dead, 'I': self.num_infected, 'S': self.num_susceptible,
                  'Q': self.num_quarantine}
        self.counts.append(counts)

    def get_adj_agents(self, agent):
        """
        Determines which Agents are within 1 position of this Agent.
        :param agent: Agent under consideration
        :return: List of Agents within 1 position of this Agent
        """

        nearby = []

        am = AgentMover(self.n)
        positions = am.get_adj_positions(agent.position)

        for each in self.agents:
            if each.position in positions:
                nearby.append(each)  # found one

        return nearby

    def run_simulation(self, num_steps):
        """
        Runs simulation for specified number of time steps, recording a metric count after each step.

        :param num_steps: Number of time steps to run the model
        :return: List of the baseline counts taken at each time step in the model.
        """

        self.count_baseline_metrics()
        self.add_counts()
        am = AgentMover(self.n)

        # update agents and metrics for each time step
        for t in range(num_steps):

            # update agent properties
            for agent in self.agents:

                if agent.has_died():
                    self.remove_agent(agent)
                else:
                    adj = self.get_adj_agents(agent)
                    before = agent.status
                    agent.update_agent(adj)
                    after = agent.status
                    self.update_baseline_metrics(before, after)

            # move all agents
            am.move_all_agents(self.agents)

            # capture metrics after every time step
            self.add_counts()

        return self.counts

    def run_and_visualize_simulation(self, num_steps):
        """
        Helper function for debugging. Outputs visualization of the simulation.

        :param num_steps: Number of time steps to run the model
        :return: None
        """
        import matplotlib.pyplot as plt
        from IPython.display import display, clear_output

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        for t in range(num_steps):
            ax.cla()

            for agent in self.agents:
                c = self.status_colors[agent.status]
                m = 'o' if agent.distancing else 's'

                ax.scatter(agent.position[0], agent.position[1], c=c, marker=m)

            am = AgentMover(self.n)
            am.move_all_agents(self.agents)

            ax.grid(True)
            ax.set_xticks(list(range(self.n)))
            ax.set_yticks(list(range(self.n)))

            display(fig)
            clear_output(wait=True)

            plt.pause(5)
