from packages.abm.agent_generator import AgentGenerator

def test__init__percent_vaccinated():
    ag = AgentGenerator(100, 10, 0.25, 0.35, 0.45)
    assert ag.m == 100
    assert ag.num_infected == 10
    assert ag.num_distancing == 25
    assert ag.num_mask == 35
    assert ag.num_vaccinated == 45

def test__init__no_percent_vaccinated():
    ag = AgentGenerator(100, 10, 0.25, 0.35)
    assert ag.m == 100
    assert ag.num_infected == 10
    assert ag.num_distancing == 25
    assert ag.num_mask == 35
    assert ag.num_vaccinated == 0

def test_is_infected():
    ag = AgentGenerator(100, 1, 0.25, 0.35, 0.45)
    current_infected = 0
    infected = ag.is_infected(current_infected)
    assert infected

    current_infected = 1
    infected = ag.is_infected(current_infected)
    assert infected is False

def test_is_vaccinated():
    ag = AgentGenerator(100, 1, 0.25, 0.35, 0.45)

    # infected should not become vaccinated
    current_vaccinated = 0
    infected = True
    vaccinated = ag.is_vaccinated(infected, current_vaccinated)
    assert vaccinated is False

    # remaining should become vaccinated
    current_vaccinated = 0
    infected = False
    vaccinated = ag.is_vaccinated(infected, current_vaccinated)
    assert vaccinated

    # full should not become vaccinated
    current_vaccinated = 45
    infected = False
    vaccinated = ag.is_vaccinated(infected, current_vaccinated)
    assert vaccinated is False

def test_get_status():
    ag = AgentGenerator(100, 1, 0.25, 0.35, 0.45)

    # infected
    infected = True
    vaccinated = False
    status = ag.get_status(infected, vaccinated)
    assert status == 'I'

    # vaccinated
    infected = False
    vaccinated = True
    status = ag.get_status(infected, vaccinated)
    assert status == 'R'

    # susceptible
    infected = False
    vaccinated = False
    status = ag.get_status(infected, vaccinated)
    assert status == 'S'

    # error handling
    try:
        infected = True
        vaccinated = True
        status = ag.get_status(infected, vaccinated)
        assert False
    except ValueError:
        assert True


def test_select_indexes():
    m = 100
    ag = AgentGenerator(m, 1, 0.25, 0.35, 0.45)

    num_positions = 25
    positions = ag.select_indexes(num_positions)

    assert len(positions) == num_positions
    assert len(set(positions)) == num_positions

    counter = 0
    for p in positions:
        if p >= m or p < 0:  # should be within [0...m-1] index positions
            counter += 1
    assert counter == 0

def test_create_agents():
    m = 100
    ag = AgentGenerator(m, 10, 0.25, 0.35, 0.45)
    agents = ag.generate_agents()

    assert len(agents) == m

    infected_counter = 0
    vaccinated_counter = 0
    susceptible_counter = 0
    mask_counter = 0
    distancing_counter = 0

    for agent in agents:
        if agent.status == 'I':
            infected_counter += 1
        elif agent.status == 'R':
            vaccinated_counter += 1
        elif agent.status == 'S':
            susceptible_counter += 1

        if agent.mask:
            mask_counter += 1

        if agent.distancing:
            distancing_counter += 1

    assert infected_counter == 10, infected_counter
    assert distancing_counter == 25, distancing_counter
    assert mask_counter == 35, mask_counter
    assert vaccinated_counter == 45, vaccinated_counter
    assert susceptible_counter == m - infected_counter - vaccinated_counter, susceptible_counter

