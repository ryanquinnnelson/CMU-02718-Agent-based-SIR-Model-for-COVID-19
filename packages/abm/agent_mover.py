import random


class Agent:
    """
    Defines an Agent's properties and behaviors when interacting with other Agents.

    Fields:

        asymptomatic:  True if agent is asymptomatic when infected.

        days_infected: How long agent has been infected, if currently infected.

    """
    statuses = ['R', 'S', 'I', 'Q']  # allowable statuses
    days_infected = 0

    def __init__(self, position, status, mask, distancing):
        """
        Initializes an agent.
        :param position: Location of the Agent in the world, as defined by (x,y).
        :param status: The state of the Agent's health. Allowable statuses are:
            (R) Recovered;
            (S) Susceptible to Infection;
            (I) Infected;
            (Q) Quarantined
        :param mask: True if agent is wearing a mask.
        :param distancing: True if agent is physically distancing.
        """
        # position (x,y)
        self.position = position

        # status
        if status in self.statuses:
            self.status = status
        else:
            raise ValueError('status: ' + status + ' is not valid.')

        # possibly asymptomatic if infected
        if status == 'I':
            if self.is_asymptomatic():
                self.asymptomatic = True
            else:
                self.asymptomatic = False
        else:
            self.asymptomatic = False

        self.mask = mask
        self.distancing = distancing

    def is_event(self, num_event, num_outcomes):
        """
        Calculates whether an event has occurred given the assumed likelihood of that event.
        If an event has a 25% chance, num_event = 1 and num_outcomes = 4.
        :param num_event: The number of occurrences of an event out of all possible outcomes.
        :param num_outcomes: The number of possible outcomes.
        :return: True if event occurs, False otherwise.
        """
        return random.randint(1, num_outcomes) <= num_event

    def is_infected(self, adjacent_agents):
        """
        Calculates whether Agent is infected, given a list of adjacent agents. Infection depends on whether
        an adjacent agent is infected or masked and whether the agent is masked.

        A check is performed separately for each agent adjacent to this agent.
        :param adjacent_agents:
        :return: True if the agent is now infected, False otherwise.
        """
        infected = False

        # perform check for all adjacent agents
        for adjacent in adjacent_agents:

            # chance of infection if an adjacent agent is infected
            if adjacent.status == 'I':

                # infection probability depends on mask status of both
                if self.mask and adjacent.mask:

                    if self.is_event(1, 10000):  # 0.01% chance
                        infected = True

                elif self.mask or adjacent.mask:

                    if self.is_event(1, 100):  # 1% chance
                        infected = True

                else:

                    if self.is_event(1, 4):  # 25% chance
                        infected = True

        return infected

    def is_asymptomatic(self):
        """
        Calculates whether Agent is asymptomatic. Model assumes that Agents have a
        20% chance of being asymptomatic upon infection.

        :return: True if agent is asymptomatic, False otherwise.
        """
        return self.is_event(1, 5)  # 20% chance of being asymptomatic

    def will_quarantine(self):
        """
        Calculates whether Agent will go into Quarantine status.
        :return: True if the agent has been infected for at least 3 days and is symptomatic, False otherwise.
        """
        return self.days_infected > 2 and not self.asymptomatic

    def infection_over(self):
        """
        Calculates whether Agent has recovered from infection.
        :return: True if the agent has been infected for at least 15 days, False otherwise.
        """
        return self.days_infected > 14

    def update_status(self, adjacent_agents):
        """
        Checks whether modification to the agent's status is needed, and updates the status as necessary.
        :param adjacent_agents: List of Agents adjacent to this Agent
        :return: None
        """

        if self.status == 'S':  # not yet infected

            if self.is_infected(adjacent_agents):
                self.status = 'I'

        elif self.status == 'I':  # already infected

            if self.will_quarantine():
                self.status = 'Q'

            if self.infection_over():
                self.status = 'R'

        elif self.status == 'Q':  # already in quarantine

            if self.infection_over():
                self.status = 'R'

    def update_agent(self, adjacent_agents):
        """
        Updates agent metrics based on adjacent agents. Does not update position.
        :param adjacent_agents: List of Agents adjacent to this Agent.
        :return: None
        """

        # update days infected if already infected
        if self.status == 'I' or self.status == 'Q':
            self.days_infected += 1  # day passed since infection started

        # update status
        status_before = self.status
        self.update_status(adjacent_agents)

        # if now infected, determine if asymptomatic
        if status_before != 'I' and self.status == 'I':
            self.asymptomatic = self.is_asymptomatic()

        elif status_before != 'R' and self.status == 'R':

            # reset metrics related to infection
            self.days_infected = 0
            self.asymptomatic = False

    def __str__(self):
        """
        :return: String representation of Agent.
        """
        return 'Agent{' + 'position:' + str(self.position) + ', status:' + str(self.status) + ', mask:' + str(
            self.mask) + ', distancing:' + str(self.distancing) + ', days_infected:' + str(
            self.days_infected) + ', asymptomatic:' + str(self.asymptomatic) + '}'

    def has_died(self):
        """
        Calculates whether Agent has died. This model assumes Agent has a 0.2% chance of dying during infection.
        :return: True if agent dies due to infection, False otherwise.
        """
        infected = self.status == 'I' or self.status == 'Q'
        return infected and self.is_event(2, 1000)  # 0.2% chance
