from packages.abm.abm import ABM
from packages.abm.agent import Agent


def test__init__():
    # raises exception

    n = 3
    m = 250
    num_infected = 10
    percent_distancing = 0.25
    percent_mask = 0.35
    percent_vaccinated = 0.1

    try:
        abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)
        assert False
    except ValueError:
        assert True

    # doesn't raise exception
    n = 25
    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)

    # check counts of Agents
    assert len(abm.agents) == m

    # ensure all Agents were placed
    for agent in abm.agents:
        assert agent.position != (-1, -1)


def test_count_baseline_metrics():
    n = 25
    m = 250
    num_infected = 10
    percent_distancing = 0.25
    percent_mask = 0.35
    percent_vaccinated = 0.1
    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)

    # zero counts
    assert abm.num_recovered == 0
    assert abm.num_infected == 0
    assert abm.num_susceptible == 0
    assert abm.num_dead == 0
    assert abm.num_quarantine == 0

    # after performing counts
    abm.count_baseline_metrics()
    assert abm.num_recovered == 25, abm.num_recovered
    assert abm.num_infected == 10, abm.num_infected
    assert abm.num_susceptible == m - abm.num_recovered - abm.num_infected, abm.num_susceptible
    assert abm.num_dead == 0, abm.num_dead
    assert abm.num_quarantine == 0, abm.num_quarantine


def test_remove_agent():
    n = 25
    m = 250
    num_infected = 10
    percent_distancing = 0.25
    percent_mask = 0.35
    percent_vaccinated = 0.1
    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)

    a = abm.agents[0]  # select an agent from agents

    abm.remove_agent(a)

    assert a not in abm.agents
    assert len(abm.agents) == m - 1, len(abm.agents)
    assert abm.num_dead == 1


def test_add_counts():
    n = 25
    m = 250
    num_infected = 10
    percent_distancing = 0.25
    percent_mask = 0.35
    percent_vaccinated = 0.1
    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)
    abm.count_baseline_metrics()

    # empty counts list
    assert len(abm.counts) == 0

    # add set of metrics to list
    abm.add_counts()
    assert len(abm.counts) == 1

    for count_dict in abm.counts:
        print(count_dict)
        assert count_dict['R'] == 25
        assert count_dict['D'] == 0
        assert count_dict['I'] == 10
        assert count_dict['Q'] == 0
        assert count_dict['S'] == 250 - 25 - 10


def test_get_adj_agents():
    n = 25
    m = 250
    num_infected = 10
    percent_distancing = 0.25
    percent_mask = 0.35
    percent_vaccinated = 0.1
    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)

    a1 = Agent((1, 1), 'I', mask=True, distancing=False)
    a2 = Agent((0, 0), 'I', mask=True, distancing=False)
    a3 = Agent((5, 5), 'I', mask=True, distancing=False)

    # no agents nearby Agent
    abm.agents = [a1, a3]
    assert len(abm.get_adj_agents(a1)) == 0

    # at least one agent nearby Agent
    abm.agents = [a1, a2, a3]
    adj = abm.get_adj_agents(a1)

    assert len(adj) == 1
    assert a2 in adj


def test_update_baseline_metrics():
    n = 25
    m = 250
    num_infected = 10
    percent_distancing = 0.25
    percent_mask = 0.35
    percent_vaccinated = 0.1
    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)

    # no change
    abm.num_infected = 10
    abm.update_baseline_metrics('I', 'I')
    assert abm.num_infected == 10

    # change
    abm.num_infected = 10
    abm.num_recovered = 25
    abm.update_baseline_metrics('I', 'R')
    assert abm.num_infected == 9
    assert abm.num_recovered == 26

    # change
    abm.num_infected = 10
    abm.num_susceptible = 25
    abm.update_baseline_metrics('I', 'S')
    assert abm.num_infected == 9
    assert abm.num_susceptible == 26

    # change
    abm.num_infected = 10
    abm.num_quarantine = 25
    abm.update_baseline_metrics('I', 'Q')
    assert abm.num_infected == 9
    assert abm.num_quarantine == 26


def test_run_simulation():
    n = 5
    m = 10
    num_infected = 2
    percent_distancing = 0.1
    percent_mask = 0.35
    percent_vaccinated = 0.1

    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)
    counts = abm.run_simulation(1)
    assert len(counts) == 2  # one additional for initialization

    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)
    counts = abm.run_simulation(365)

    assert len(counts) == 366  # one additional for initialization


def test_run_and_visualize_simulation():
    n = 25
    m = 250
    num_infected = 10
    percent_distancing = 0.1
    percent_mask = 0.35
    percent_vaccinated = 0.1
    abm = ABM(n, m, num_infected, percent_distancing, percent_mask, percent_vaccinated)

    abm.run_and_visualize_simulation(2)
