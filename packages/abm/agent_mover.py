import random


class AgentMover:
    """
    Defines a virtual n x n torus grid world and
    manages the positioning and movement of all
    Agents in this world.

    Fields:

        n: the dimension of the square torus grid
           used to define the world in which Agents
           move
    """

    # allowable moves
    directions = [[-1, 0],  # left
                  [1, 0],  # right
                  [0, -1],  # up
                  [0, 1],  # down
                  [-1, -1],  # left & up
                  [-1, 1],  # left & down
                  [1, -1],  # right & up
                  [1, 1]]  # right & down

    # all moves which extend 3 positions from current position (0,0)
    directions_dia_3 = [[i, j] for i in range(-3, 4) for j in range(-3, 4) if (i, j) != (0, 0)]

    # all moves which extend 2 positions from current position (0,0)
    directions_dia_2 = [[i, j] for i in range(-2, 3) for j in range(-2, 3) if (i, j) != (0, 0)]

    def __init__(self, n):
        """
        Initializes AgentMover.
        :param n: The dimension of the n x n torus grid world.
        """
        self.n = n

    def get_random_position(self, selected):
        """
        Selects a random position in the n x n grid which has not a position in the list of selected positions.

        :param selected:
        :return: (int, int) Tuple representing (i,j) position in an n x n grid
        """

        # try random position
        i = random.randint(0, self.n - 1)
        j = random.randint(0, self.n - 1)

        while (i, j) in selected:
            # keep trying if position has already been chosen
            i = random.randint(0, self.n - 1)
            j = random.randint(0, self.n - 1)

        return (i, j)

    def split_agents(self, agents):
        """
        Splits agents into those which are distancing and other.

        :param agents:
        :return: (List, List) Tuple containing collections of Agents. Tuple contains (distancing agents, other agents).
        """

        # position distancing agents first
        distancing_agents = list()
        other_agents = list()

        for agent in agents:
            if agent.distancing:
                distancing_agents.append(agent)
            else:
                other_agents.append(agent)

        return distancing_agents, other_agents

    def get_x(self, x_curr, change):
        """
        Calculates next x coordinate, wrapping around torus grid if position would move off the top or bottom.
        :param x_curr: Current x position
        :param change: Integer (positive or negative) indicating the increment of movement.
        Positive means move up; negative means move down.
        :return: The x position to which the Agent would be moved.
        """

        x_result = x_curr + change
        if x_result < 0:
            x_next = self.n + x_result
        elif x_result > self.n - 1:
            x_next = x_result % self.n
        else:
            x_next = x_result

        return x_next

    def get_y(self, y_curr, change):
        """
        Calculates next y coordinate, wrapping around torus grid if position would move off the left or right.
        :param y_curr: Current y position
        :param change: Integer (positive or negative) indicating the increment of movement.
        Positive means move right; negative means move left.
        :return: The y position to which the Agent would be moved
        """
        return self.get_x(y_curr, change)  # works the same as x changes

    def get_adj_positions(self, position):
        """
        Calculates the 8 grid positions adjacent to the given position, wrapping around the torus grid when necessary.
        :param position: Current (i,j) position
        :return: Set of all 8 (i,j) positions which surround the given position.
        """

        adjacent = set()

        x_curr = position[0]
        y_curr = position[1]

        for x_change, y_change in self.directions:
            # get resulting coordinates after change
            x_next = self.get_x(x_curr, x_change)
            y_next = self.get_y(y_curr, y_change)

            adjacent.add((x_next, y_next))

        return adjacent

    def get_search_space(self, position, directions_set):
        """
        Returns a set of all positions which surround the given position according to the diameter specified in the
        given directions_set, wrapping around the torus grid when necessary.

        - For a directions set of diameter 3, there are 48 positions.
        - For a directions set of diameter 2, there are 24 positions.
        - For a directions set of diameter 1, there are 8 positions.

        :param position: Current (i,j) position
        :param directions_set: 2D list containing allowable moves within the grid.
        :return: Set of all (i,j) positions which surround the given position.
        """

        adjacent = set()

        x_curr = position[0]
        y_curr = position[1]

        for x_change, y_change in directions_set:
            # get resulting coordinates after change
            x_next = self.get_x(x_curr, x_change)
            y_next = self.get_y(y_curr, y_change)

            adjacent.add((x_next, y_next))

        return adjacent

    def positions_available(self, unavailable, agents, positioned):
        """
        Calculates whether there are any available positions in which the remaining Agents could be positioned.

        :param unavailable: List of unavailable positions
        :param agents: List of Agents to be positioned
        :param positioned: Number of Agents which have already been positioned
        :return: True if there is at least one position available for each agent not yet positioned, False otherwise.
        """

        num_agents_left = len(agents) - positioned
        num_positions_left = self.n * self.n - len(unavailable)
        return num_positions_left >= num_agents_left

    def position_distancing_agents(self, distancing_agents):
        """
        Attempts to find unique positions for given list of distancing agents such that every agent maintains at least
        one position between itself and every other agent.

        :param distancing_agents: List of Agents which have distancing requirements.
        :return: (True, unavailable) if such a positioning is found, (False, unavailable) otherwise. unavailable is a
        set containing all positions which cannot be selected for agents.
        """

        # reset for new attempt
        unavailable = set()
        num_positioned = 0

        for agent in distancing_agents:

            # if there aren't enough available positions left, start over
            if not self.positions_available(unavailable, distancing_agents, num_positioned):
                return (False, unavailable)

                # choose available position
            position = self.get_random_position(unavailable)
            agent.position = position

            # update available positions
            curr_unavailable = self.get_adj_positions(position)  # positions surrounding are not available
            curr_unavailable.add(position)  # position taken is not available
            unavailable = unavailable.union(curr_unavailable)  # update full list

            # update counter
            num_positioned += 1

        # all agents were positioned successfully
        return (True, unavailable)

    def position_remaining_agents(self, agents, unavailable):
        """
        Positions all agents without distancing requirements.

        :param agents: List of Agents to be positioned
        :param unavailable: List of unavailable positions
        :return:  True if agents were positioned successfully, False otherwise.
        """

        num_positioned = 0
        for agent in agents:

            # only continue if there are enough positions left
            if not self.positions_available(unavailable, agents, num_positioned):
                return False

            # choose available position
            position = self.get_random_position(unavailable)
            agent.position = position

            # update available positions
            unavailable.add(position)

            # update counter
            num_positioned += 1

        # all agents were positioned successfully
        return True

    def find_nearby_agents(self, agents, position):
        """
        Finds all agents within 3 spaces of this agent in every direction.
        This reduces the search space for available positions to only
        those agents which may be affected by this agent after a move.

        See diagram "02718-HW4-Moves.png" which illustrates why a diameter of 3 is used.
        :param agents: List of Agents
        :param position: Current (i,j) position
        :return: List of available positions
        """
        # determine positions within 3 spaces of this agent
        search_space = self.get_search_space(position, self.directions_dia_3)

        # find all agents within that search space
        nearby = list()
        for agent in agents:
            if agent.position in search_space:
                nearby.append(agent)

        return nearby

    def remove_position_if_occupied(self, other, avail):
        """
        If position of other Agent is in available positions, removes position from list of available.
        :param other: Agent which would be within movement interaction distance
        :param avail: List of available positions
        :return: None
        """

        if other.position in avail:
            avail.remove(other.position)

    def remove_positions_distancing_others(self, other, avail):
        """
        If other agent is distancing, removes all positions adjacent to other agent from available positions.

        :param other: Agent which would be within movement interaction distance
        :param avail: List of available positions
        :return: None
        """

        # restrictions depend on distancing of agent and other
        if other.distancing:

            # all positions within 1 space of other are unavailble
            other_adj = self.get_adj_positions(other.position)

            # remove restricted positions
            for pos in other_adj:
                if pos in avail:
                    avail.remove(pos)

    def remove_positions_distancing_self(self, agent, other, avail):
        """
        If this agent is distancing, removes all positions which would breach distancing due to
        proximity of other agent.
        :param agent: Agent being considered
        :param other: Agent which would be within movement interaction distance
        :param avail: List of available positions
        :return: None
        """

        if agent.distancing:

            # all positions within 1 space of other are unavailable
            other_adj = self.get_adj_positions(other.position)

            # remove restricted positions
            for pos in other_adj:
                if pos in avail:
                    avail.remove(pos)

    def get_available_positions(self, agent, agents):
        """
        Calculates a list of possible positions to which a given agent can move, considering all other agents.
        Availability is constrained by the current position of other agents and whether another agent is distancing.

        This method determines which of those positions are:
         1 - not occupied;
         2 - allow this agent to maintain its own distancing boundaries if necessary;
         3 - outside distancing boundaries of another agent;

        :param agent: Agent being considered
        :param agents: List of all Agents
        :return: List of available positions
        """
        # if no nearby agents, all positions available
        avail = self.get_adj_positions(agent.position)

        # find all nearby agents
        nearby = self.find_nearby_agents(agents, agent.position)

        # if there are nearby agents, determine availability
        if nearby:

            # check moves against each nearby agent
            for other in nearby:
                # remove occupied positions
                self.remove_position_if_occupied(other, avail)

                # remove positions which breach distancing of others
                self.remove_positions_distancing_others(other, avail)

                # remove positions which breach distancing of this agent
                self.remove_positions_distancing_self(agent, other, avail)

        return avail

    def move_agent(self, agent, positions):
        """
        Selects a random position from positions and updates the agent to be at that location.
        If positions list is empty, does not move the agent.
        :param agent: Agent under consideration
        :param positions: List of available positions
        :return: None
        """
        if positions:
            i = random.randint(0, len(positions) - 1)  # random index
            agent.position = list(positions)[i]

    def move_all_agents(self, agents):
        """
        Selects and moves each agent in agents.
        :param agents: List of all Agents
        :return: None
        """
        for agent in agents:
            moves = self.get_available_positions(agent, agents)
            self.move_agent(agent, moves)

    def check_position_conflicts(self, agents):
        """
        Returns a set of positions which contain more than one agent. Used for testing purposes.
        :param agents: List of all Agents
        :return: List of positions on which more than one Agent is positioned
        """

        conflicts = set()
        chosen = dict()
        for agent in agents:
            pos = agent.position
            if pos in chosen:
                chosen[pos] += 1  # increment value of key by 1
            else:
                chosen[pos] = 1  # add key to dictionary

        for key in chosen.keys():
            if chosen[key] > 1:
                conflicts.add(key)  # more than 1 Agent here

        return conflicts

    def check_distancing_conflicts(self, agents):
        """
        Returns a set of positions which contain agents that breach distancing constraints.
        Used for testing purposes.
        :param agents: List of all Agents
        :return: List of Agents which violate distancing requirements
        """

        conflicts = set()

        for agent in agents:

            if agent.distancing:

                pos = agent.position
                adj = self.get_adj_positions(pos)

                # no other agent should be in an adjacent position

                # Note agent won't conflict with itself because its
                # position is not in adj
                for each in agents:

                    # check whether any agent is within the distancing range
                    if each.position in adj:
                        conflicts.add(each.position)

        return conflicts

    def position_agents(self, agents):
        """
        Positions given agents on n x n grid, following distancing constraints for distancing agents. Performs multiple
        positioning attempts until either a solution is found or the number of allowed attempts is exhausted.

        Raises ValueError if no viable positioning is found after all attempts.

        :param agents: List of all Agents
        :return: True if positioning is found.
        """

        # split agents into distancing and other
        distancing_agents, other_agents = self.split_agents(agents)
        attempt_counter_outer = 0
        all_success = False

        # both distancing and other agents must be positioned
        while all_success is False:

            # reset for next attempt
            unavailable = set()
            d_success = False
            attempt_counter_inner = 0

            # attempt to position distancing agents first
            while d_success is False:

                d_success, unavailable = self.position_distancing_agents(distancing_agents)

                attempt_counter_inner += 1
                if attempt_counter_inner >= 10:
                    raise ValueError('Unable to find positions for all distancing agents')

            # position remaining agents after successful positioning of distancing agents
            all_success = self.position_remaining_agents(other_agents, unavailable)

            attempt_counter_outer += 1
            if attempt_counter_outer >= 100:
                remaining = self.n * self.n - len(unavailable)
                raise ValueError('Unable to find positions for other agents:', remaining)

        # all agents positioned
        return True
