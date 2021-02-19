import random
from packages.abm.agent_generator import AgentGenerator
from packages.abm.agent_mover import AgentMover
from packages.abm.agent_generator import Agent


def test_position_agents():
    # success
    n = 25
    am = AgentMover(n)
    a1 = Agent((-1, -1), 'I', mask=True, distancing=True)
    a2 = Agent((-1, -1), 'I', mask=True, distancing=False)
    agents = [a1, a2]

    assert am.position_agents(agents)
    for each in agents:
        print(each)
        assert each.position != (-1, -1)

    # failure
    n = 1
    am = AgentMover(n)
    a1 = Agent((-1, -1), 'I', mask=True, distancing=True)
    a2 = Agent((-1, -1), 'I', mask=True, distancing=False)
    agents = [a1, a2]

    try:
        am.position_agents(agents)
        assert False
    except ValueError:
        assert True

    # try with full number of Agents with no distancing
    n = 25
    am = AgentMover(n)
    agents = [Agent((-1, -1), 'I', mask=True, distancing=False) for i in range(250)]
    print(len(agents))
    result = am.position_agents(agents)
    assert result
    for each in agents:
        assert each.position != (-1, -1)

    # try with 10% distancing
    n = 25
    am = AgentMover(n)
    ag = AgentGenerator(250, 10, 0.1, 0.35, 0.45)
    agents = ag.generate_agents()
    result = am.position_agents(agents)
    assert result == True
    for each in agents:
        assert each.position != (-1, -1)

    # try with 50% distancing
    n = 25
    am = AgentMover(n)
    ag = AgentGenerator(250, 10, 0.20, 0.35, 0.45)
    agents = ag.generate_agents()
    result = am.position_agents(agents)
    assert result == True
    for each in agents:
        assert each.position != (-1, -1)


def test_get_random_position():
    n = 25
    am = AgentMover(n)

    selected = list()
    position = am.get_random_position(selected)

    # check if position is within n x n grid
    assert position[0] >= 0
    assert position[0] < n
    assert position[1] >= 0
    assert position[1] < n

    # check if position has been taken already
    # create list with all positions taken except (0,0)
    selected = [(i, j) for i in range(n) for j in range(n) if (i, j) != (0, 0)]
    position = am.get_random_position(selected)
    assert position == (0, 0)


def test_split_agents():
    n = 25
    am = AgentMover(n)

    a1 = Agent((1, 2), 'I', mask=True, distancing=True)
    a2 = Agent((1, 2), 'I', mask=True, distancing=True)
    a3 = Agent((1, 2), 'R', mask=True, distancing=False)
    a4 = Agent((1, 2), 'R', mask=True, distancing=False)
    a5 = Agent((1, 2), 'R', mask=True, distancing=False)

    distancing_agents, other_agents = am.split_agents([a1, a2, a3, a4, a5])

    for agent in distancing_agents:
        assert agent.status == 'I'

    for agent in other_agents:
        assert agent.status == 'R'

    assert len(distancing_agents) == 2
    assert len(other_agents) == 3


def test_get_x():
    n = 25
    am = AgentMover(n)

    # move 1 space
    assert am.get_x(0, -1) == n - 1
    assert am.get_x(0, 1) == 1
    assert am.get_x(n - 1, 1) == 0

    # move 2 spaces
    assert am.get_x(0, -2) == n - 2
    assert am.get_x(0, 2) == 2
    assert am.get_x(n - 1, 2) == 1


def test_get_y():
    n = 25
    am = AgentMover(n)

    # move 1 space
    assert am.get_y(0, -1) == n - 1
    assert am.get_y(0, 1) == 1
    assert am.get_y(n - 1, 1) == 0

    # move 2 spaces
    assert am.get_y(0, -2) == n - 2
    assert am.get_y(0, 2) == 2
    assert am.get_y(n - 1, 2) == 1


def test_get_adj_positions():
    n = 25
    am = AgentMover(n)

    # non-edge position
    current_position = (1, 1)
    adjacent_correct = [(0, 0), (0, 1), (0, 2),
                        (1, 0), (1, 2),
                        (2, 0), (2, 1), (2, 2)]
    adjacent = am.get_adj_positions(current_position)
    print(adjacent)
    for each in adjacent_correct:
        assert each in adjacent, str(each) + ' is missing from result.'

    # lower right corner
    current_position = (24, 24)
    adjacent_correct = [(23, 0), (23, 23), (23, 24),
                        (24, 0), (24, 23),
                        (0, 0), (0, 23), (0, 24)]
    adjacent = am.get_adj_positions(current_position)
    print(adjacent)
    for each in adjacent_correct:
        assert each in adjacent, str(each) + ' is missing from result.'

    # upper right corner
    current_position = (0, 24)
    adjacent_correct = [(24, 0), (24, 23), (24, 24),
                        (0, 0), (0, 23),
                        (1, 0), (1, 23), (1, 24)]
    adjacent = am.get_adj_positions(current_position)
    print(adjacent)
    for each in adjacent_correct:
        assert each in adjacent, str(each) + ' is missing from result.'

    # lower left corner
    current_position = (24, 0)
    adjacent_correct = [(23, 0), (23, 1), (23, 24),
                        (24, 1), (24, 24),
                        (0, 0), (0, 1), (0, 24)]
    adjacent = am.get_adj_positions(current_position)
    print(adjacent)
    for each in adjacent_correct:
        assert each in adjacent, str(each) + ' is missing from result.'

    # upper left corner
    current_position = (0, 0)
    adjacent_correct = [(24, 0), (24, 1), (24, 24),
                        (0, 1), (0, 24),
                        (1, 0), (1, 1), (1, 24)]
    adjacent = am.get_adj_positions(current_position)
    print(adjacent)
    for each in adjacent_correct:
        assert each in adjacent, str(each) + ' is missing from result.'


def test_positions_available():
    n = 1
    am = AgentMover(n)
    a1 = Agent((-1, -1), 'I', mask=True, distancing=True)
    unavailable = set()

    # (unavailable, agents, positioned)
    assert am.positions_available(unavailable, [a1], 0)

    unavailable.add(1)
    assert am.positions_available(unavailable, [a1], 0) is False


def test_position_distancing_agents():
    # only possible to place one agent
    n = 3
    am = AgentMover(n)
    agents = [Agent((-1, -1), 'I', mask=True, distancing=True) for i in range(2)]
    result, unavailable = am.position_distancing_agents(agents)
    assert result is False

    # multiple agents can be placed
    n = 25
    am = AgentMover(n)
    agents = [Agent((-1, -1), 'I', mask=True, distancing=True) for i in range(2)]
    result, unavailable = am.position_distancing_agents(agents)
    assert result


def test_position_remaining_agents():
    n = 1
    am = AgentMover(n)

    a1 = Agent((-1, -1), 'I', mask=True, distancing=False)
    a2 = Agent((-1, -1), 'I', mask=True, distancing=False)

    unavailable = set()

    assert am.position_remaining_agents([a1], unavailable)

    unavailable.add((0, 0))
    assert am.position_remaining_agents([a1], unavailable) is False


def test_get_search_space():
    n = 25
    am = AgentMover(n)

    # test 3 diameter, no wrap
    position = (5, 5)

    expected = [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
                (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
                (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
                (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8),
                (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8),
                (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8),
                (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
    actual = am.get_search_space(position, am.directions_dia_3)
    for each in expected:
        assert each in actual, 'missing ' + str(each)

    # test 3 diameter, wrap
    position = (0, 0)

    expected = [(0, 1), (0, 2), (0, 3), (0, 22), (0, 23), (0, 24),
                (1, 0), (1, 1), (1, 2), (1, 3), (1, 22), (1, 23), (1, 24),
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 22), (2, 23), (2, 24),
                (3, 0), (3, 1), (3, 2), (3, 3), (3, 22), (3, 23), (3, 24),

                (22, 0), (22, 1), (22, 2), (22, 3), (22, 22), (22, 23), (22, 24),
                (23, 0), (23, 1), (23, 2), (23, 3), (23, 22), (23, 23), (23, 24),
                (24, 0), (24, 1), (24, 2), (24, 3), (24, 22), (24, 23), (24, 24)]

    actual = am.get_search_space(position, am.directions_dia_3)
    for each in expected:
        assert each in actual, 'missing ' + str(each)


def test_find_nearby_agents():
    n = 25
    am = AgentMover(n)
    position = (5, 5)

    # no agent nearby
    a1 = Agent((1, 1), 'I', mask=True, distancing=False)
    result = am.find_nearby_agents([a1], position)
    assert len(result) == 0
    print(result)
    print()

    # one agent nearby
    a2 = Agent((6, 6), 'I', mask=True, distancing=False)
    result = am.find_nearby_agents([a1, a2], position)
    assert len(result) == 1
    for each in result:
        print(each)
    print()

    # two agents nearby
    a3 = Agent((6, 7), 'I', mask=True, distancing=False)
    result = am.find_nearby_agents([a1, a2, a3], position)
    assert len(result) == 2
    for each in result:
        print(each)
    print()

    # three agents nearby, wrapped
    position = (0, 0)
    a4 = Agent((24, 24), 'I', mask=True, distancing=False)
    a5 = Agent((23, 23), 'I', mask=True, distancing=False)
    a6 = Agent((22, 22), 'I', mask=True, distancing=False)
    result = am.find_nearby_agents([a4, a5, a6], position)
    assert len(result) == 3


def test_remove_position_if_occupied():
    n = 25
    am = AgentMover(n)
    available = [(0, 0), (1, 1)]

    # attempt where agent is in available
    a1 = Agent((0, 0), 'I', mask=True, distancing=True)
    am.remove_position_if_occupied(a1, available)

    assert (0, 0) not in available

    # attempt where position not in available
    a2 = Agent((1, 0), 'I', mask=True, distancing=True)
    am.remove_position_if_occupied(a2, available)

    assert len(available) == 1


def test_remove_positions_distancing_others():
    n = 25
    am = AgentMover(n)
    a1 = Agent((5, 5), 'I', mask=True, distancing=False)
    available = [(4, 4), (4, 5), (4, 6),
                 (5, 4), (5, 6),
                 (6, 4), (6, 5), (6, 6)]

    # other agent not distancing
    a3 = Agent((3, 4), 'I', mask=True, distancing=False)
    am.remove_positions_distancing_others(a3, available)
    assert len(available) == 8

    # other agent distancing
    a2 = Agent((3, 4), 'I', mask=True, distancing=True)
    removed = [(4, 4), (4, 5)]

    am.remove_positions_distancing_others(a2, available)
    for each in removed:
        assert each not in available


def test_remove_positions_distancing_self():
    n = 25
    am = AgentMover(n)
    a1 = Agent((5, 5), 'I', mask=True, distancing=True)
    available = [(4, 4), (4, 5), (4, 6),
                 (5, 4), (5, 6),
                 (6, 4), (6, 5), (6, 6)]

    # other agent not distancing
    a3 = Agent((4, 8), 'I', mask=True, distancing=False)
    am.remove_positions_distancing_self(a1, a3, available)
    assert len(available) == 8

    # other agent distancing
    a2 = Agent((3, 4), 'I', mask=True, distancing=False)
    removed = [(4, 4), (4, 5)]

    am.remove_positions_distancing_self(a1, a2, available)
    for each in removed:
        assert each not in available


def test_get_available_positions():
    n = 25
    am = AgentMover(n)
    a1 = Agent((5, 5), 'I', mask=True, distancing=False)
    expected = [(4, 4), (4, 5), (4, 6),
                (5, 4), (5, 6),
                (6, 4), (6, 5), (6, 6)]

    # no nearby agents
    a2 = Agent((0, 0), 'I', mask=True, distancing=False)
    available = am.get_available_positions(a1, [a2])
    assert len(available) == 8

    # 1 agent occupies possible move
    a2 = Agent((4, 4), 'I', mask=True, distancing=False)
    available = am.get_available_positions(a1, [a2])
    assert (4, 4) not in available

    # 2 agents occupy possible moves
    a3 = Agent((6, 6), 'I', mask=True, distancing=False)
    available = am.get_available_positions(a1, [a2, a3])
    assert (4, 4) not in available and (6, 6) not in available

    # 1 other agent distancing
    a4 = Agent((3, 4), 'I', mask=True, distancing=True)
    available = am.get_available_positions(a1, [a4])
    assert (4, 4) not in available and (4, 5) not in available

    # this agent distancing
    a5 = Agent((3, 4), 'I', mask=True, distancing=False)
    a1.distancing = True
    available = am.get_available_positions(a1, [a5])
    assert (4, 4) not in available and (4, 5) not in available

    # all spaces restricted
    a6 = Agent((3, 4), 'I', mask=True, distancing=True)
    a7 = Agent((4, 7), 'I', mask=True, distancing=True)
    a8 = Agent((7, 6), 'I', mask=True, distancing=True)
    a9 = Agent((6, 3), 'I', mask=True, distancing=True)
    available = am.get_available_positions(a1, [a6, a7, a8, a9])
    assert len(available) == 0


def test_move_agent():
    n = 25
    am = AgentMover(n)
    a1 = Agent((1, 2), 'I', mask=True, distancing=True)

    # no movement because list is empty
    am.move_agent(a1, [])

    assert a1.position == (1, 2)

    # movement to only available position
    am.move_agent(a1, [(1, 1)])

    assert a1.position == (1, 1)

    # movement to random available position
    pos = [(1, 1), (1, 3), (2, 2)]

    num = 10000
    counter = 0
    for i in range(num):
        am.move_agent(a1, pos)
        if a1.position == (2, 2):
            counter += 1
    assert round(counter / num, 2) == 0.33, 'rate ' + str(round(counter / num, 2)) + ' is not 0.33'


def test_check_position_conflicts():
    n = 25
    am = AgentMover(n)

    a1 = Agent((5, 5), 'I', mask=True, distancing=True)
    a2 = Agent((0, 0), 'I', mask=True, distancing=True)

    conflicts = am.check_position_conflicts([a1, a2])
    assert len(conflicts) == 0

    a1 = Agent((5, 5), 'I', mask=True, distancing=True)
    a2 = Agent((5, 5), 'I', mask=True, distancing=True)

    conflicts = am.check_position_conflicts([a1, a2])
    assert (5, 5) in conflicts


def test_check_distancing_conflicts():
    n = 25
    am = AgentMover(n)

    a1 = Agent((1, 1), 'I', mask=True, distancing=True)
    a2 = Agent((5, 5), 'I', mask=True, distancing=True)

    # not within distancing constraints
    conflicts = am.check_distancing_conflicts([a1, a2])
    assert len(conflicts) == 0

    # within distancing constraints
    a1.position = (4, 4)
    conflicts = am.check_distancing_conflicts([a1, a2])
    assert (4, 4) in conflicts and (5, 5) in conflicts


def test_move_all_agents():
    n = 25
    am = AgentMover(n)

    # example where there is no conflict for two agents
    a1 = Agent((5, 5), 'I', mask=True, distancing=True)
    a2 = Agent((0, 0), 'I', mask=True, distancing=True)

    available_a1 = [(4, 4), (4, 5), (4, 6),
                    (5, 4), (5, 6),
                    (6, 4), (6, 5), (6, 6)]

    available_a2 = [(0, 1), (0, 24),
                    (1, 0), (1, 1), (1, 24),

                    (24, 0), (24, 1), (24, 24)]

    am.move_all_agents([a1, a2])
    assert a1.position in available_a1
    assert a2.position in available_a2

    # example where this is potential conflict for two agents

    a1.position = (5, 5)
    a6 = Agent((3, 4), 'I', mask=True, distancing=True)
    a7 = Agent((4, 7), 'I', mask=True, distancing=True)
    a8 = Agent((7, 6), 'I', mask=True, distancing=True)
    a9 = Agent((7, 3), 'I', mask=True, distancing=True)

    agents = [a1, a6, a7, a8, a9]

    # check a large number of iterations
    # randomize order in list so different agents are moved first each time
    for i in range(1000):
        # reset positions
        a1.position = (5, 5)
        a6.position = (3, 4)
        a7.position = (4, 7)
        a8.position = (7, 6)
        a9.position = (7, 3)

        # randomize order
        random.shuffle(agents)
        am.move_all_agents(agents)

        # check that no agents are in the same position
        conflicts_pos = am.check_position_conflicts(agents)
        assert len(conflicts_pos) == 0

        # check that no agents breach distancing
        conflicts_dist = am.check_distancing_conflicts(agents)
        assert len(conflicts_dist) == 0
