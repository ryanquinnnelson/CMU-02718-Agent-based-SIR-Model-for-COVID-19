from packages.abm.agent import Agent


def test__init__():
    a1 = Agent((1, 1), 'I', mask=True, distancing=True)

    # check provided parameters
    assert a1.position == (1, 1)
    assert a1.status == 'I'
    assert a1.mask
    assert a1.distancing
    assert a1.days_infected == 0

    # check derived parameters
    num = 100000
    counter = 0
    for i in range(num):
        a1 = Agent((1, 1), 'I', mask=True, distancing=True)
        if a1.asymptomatic:
            counter += 1
    assert round(counter / num, 2) == 0.20


def test_is_event():
    a1 = Agent((1, 1), 'I', mask=True, distancing=True)

    num = 100000
    counter = 0
    for i in range(num):
        if a1.is_event(1, 10000):
            counter += 1
    assert round(counter / num, 4) == 0.0001, 'Failed with ' + str(round(counter / num, 4))

    counter = 0
    for i in range(num):
        if a1.is_event(1, 100):
            counter += 1
    assert round(counter / num, 2) == 0.01

    counter = 0
    for i in range(num):
        if a1.is_event(1, 4):
            counter += 1
    assert round(counter / num, 2) == 0.25

    counter = 0
    for i in range(num):
        if a1.is_event(2, 1000):
            counter += 1
    assert round(counter / num, 3) == 0.002, 'Failed with ' + str(round(counter / num, 3))


def test_is_asymptomatic():
    a1 = Agent((1, 1), 'I', mask=True, distancing=True)
    counter = 0
    num = 100000
    for i in range(num):
        if a1.is_asymptomatic():
            counter += 1
    assert round(counter / num, 2) == 0.20


def test_will_quarantine():
    a2 = Agent((0, 1), 'I', mask=True, distancing=True)

    # possibility of quarantine when symptomatic
    a2.asymptomatic = False

    a2.days_infected = 2
    assert a2.will_quarantine() is False

    a2.days_infected = 3
    assert a2.will_quarantine()

    a2.days_infected = 4
    assert a2.will_quarantine()

    # when asymptomatic, will not quarantine
    a2.asymptomatic = True
    a2.days_infected = 2
    assert a2.will_quarantine() is False

    a2.days_infected = 3
    assert a2.will_quarantine() is False

    a2.days_infected = 4
    assert a2.will_quarantine() is False


def test_infection_over():
    a3 = Agent((0, 1), 'I', mask=True, distancing=True)
    a3.days_infected = 13
    assert a3.infection_over() is False

    a3.days_infected = 14
    assert a3.infection_over() is False

    a3.days_infected = 15
    assert a3.infection_over() is True


def test_is_infected_single_adjacent():
    a1 = Agent((1, 1), 'S', mask=True, distancing=True)
    a2 = Agent((0, 1), 'I', mask=True, distancing=True)

    # test 1 adjacent, 1 infected, both masked
    a1.mask = True
    a2.mask = True
    num = 100000
    counter = 0
    for i in range(num):
        if a1.is_infected([a2]):
            counter += 1
    assert round(counter / num, 4) == 0.0001, round(counter / num, 4)

    # test 1 adjacent, 1 infected, only agent masked
    a1.mask = True
    a2.mask = False
    counter = 0
    for i in range(num):
        if a1.is_infected([a2]):
            counter += 1
    assert round(counter / num, 2) == 0.01

    # test 1 adjacent, 1 infected, only adjacent masked
    a1.mask = False
    a2.mask = True
    counter = 0
    for i in range(num):
        if a1.is_infected([a2]):
            counter += 1
    assert round(counter / num, 2) == 0.01

    # test 1 adjacent, 1 infected, no masks
    a1.mask = False
    a2.mask = False
    counter = 0
    for i in range(num):
        if a1.is_infected([a2]):
            counter += 1
    assert round(counter / num, 2) == 0.25


def test_is_infected_multiple_adjacent():
    a1 = Agent((1, 1), 'S', mask=True, distancing=True)
    a2 = Agent((0, 1), 'I', mask=True, distancing=True)
    a3 = Agent((1, 2), 'R', mask=True, distancing=True)
    num = 100000

    # test 2 adjacent, 1 infected, all masked
    a1.mask = True
    a2.mask = True
    a3.mask = True
    counter = 0
    for i in range(num):
        if a1.is_infected([a2, a3]):
            counter += 1
    assert round(counter / num, 4) == 0.0001

    # test 2 adjacent, 1 infected, only agent masked
    a1.mask = True
    a2.mask = False
    a3.mask = False
    counter = 0
    for i in range(num):
        if a1.is_infected([a2, a3]):
            counter += 1
    assert round(counter / num, 2) == 0.01

    # test 2 adjacent, 1 infected, no one masked
    a2.mask = False
    a3.mask = False
    a1.mask = False
    counter = 0
    for i in range(num):
        if a1.is_infected([a2, a3]):
            counter += 1
    assert round(counter / num, 2) == 0.25


def test_is_infected_multiple_adjacent_multiple_infected():
    a1 = Agent((1, 1), 'S', mask=True, distancing=True)
    a2 = Agent((0, 1), 'I', mask=True, distancing=True)
    a3 = Agent((1, 2), 'R', mask=True, distancing=True)
    num = 100000

    # test 2 adjacent, 2 infected, all masked
    a3.status = 'I'
    a1.mask = True
    a2.mask = True
    a3.mask = True
    counter = 0
    for i in range(num):
        if a1.is_infected([a2, a3]):
            counter += 1
    print(round(counter / num, 4))
    assert round(counter / num, 4) > 0.0001, 'Failed with ' + str(round(counter / num, 4))

    # test 2 adjacent, 2 infected, agent masked
    a3.status = 'I'
    a1.mask = True
    a2.mask = False
    a3.mask = False
    counter = 0
    for i in range(num):
        if a1.is_infected([a2, a3]):
            counter += 1
    print(round(counter / num, 2))
    assert round(counter / num, 2) > 0.01

    # test 2 adjacent, 2 infected, agent masked, one adjacent masked
    a3.status = 'I'
    a1.mask = True
    a2.mask = True
    a3.mask = False
    counter = 0
    for i in range(num):
        if a1.is_infected([a2, a3]):
            counter += 1
    print(round(counter / num, 2))
    assert round(counter / num, 2) >= 0.01

    # test 2 adjacent, 2 infected, no one masked
    a3.status = 'I'
    a1.mask = False
    a2.mask = False
    a3.mask = False
    counter = 0
    for i in range(num):
        if a1.is_infected([a2, a3]):
            counter += 1
    print(round(counter / num, 2))
    assert round(counter / num, 2) > 0.25


def test_update_status():
    a1 = Agent((1, 1), 'R', mask=True, distancing=True)
    a2 = Agent((0, 1), 'I', mask=False, distancing=True)

    # test R status
    print('Test R status...')
    a1.update_status([a2])
    assert a1.status == 'R'

    # test I status
    print('Test I status...')

    a1.status = 'I'
    a1.days_infected = 0  # test not yet quarantined
    a1.asymptomatic = True
    a1.update_status([a2])
    assert a1.status == 'I'

    a1.status = 'I'
    a1.days_infected = 3  # test change to quarantined
    a1.asymptomatic = False
    a1.update_status([a2])
    assert a1.status == 'Q'

    a1.status = 'I'
    a1.days_infected = 15  # test change to recovered
    a1.asymptomatic = False
    a1.update_status([a2])
    assert a1.status == 'R'

    # test Q status
    print('Test Q status...')
    a1.status = 'Q'
    a1.days_infected = 15  # test change to recovered
    a1.asymptomatic = False
    a1.update_status([a2])
    assert a1.status == 'R'

    # test S status
    print('Test S status...')
    a1.status = 'S'
    a1.days_infected = 0
    a1.asymptomatic = False
    num = 10000
    counter = 0
    for i in range(num):
        a1.status = 'S'
        a1.update_status([a2])
        if a1.status == 'I':
            counter += 1
    assert round(counter / num, 2) == 0.01


def test_update_agent():
    a1 = Agent((1, 1), 'R', mask=False, distancing=True)
    a2 = Agent((0, 1), 'I', mask=False, distancing=True)

    # check days_infected
    a1.status = 'I'
    a1.update_agent([a2])
    assert a1.days_infected == 1

    # check status if now recovered
    # check metrics if now recovered
    a1.status = 'I'
    a1.days_infected = 14
    a1.update_agent([a2])
    assert a1.status == 'R'
    assert a1.days_infected == 0
    assert a1.asymptomatic == False

    # check status if now recovered
    # check metrics if now recovered
    a1.status = 'Q'
    a1.days_infected = 14
    a1.update_agent([a2])
    assert a1.status == 'R'
    assert a1.days_infected == 0
    assert a1.asymptomatic is False

    # check asymptomatic if now infected
    a1.status = 'S'
    a1.days_infected = 0
    a1.asymptomatic = False
    a1.update_agent([a2])

    num = 100000
    counter = 0
    for i in range(num):
        a1.status = 'S'
        a1.asymptomatic = False
        a1.update_agent([a2])
        if a1.asymptomatic:
            counter += 1
    assert round(counter / num, 2) == 0.05


def test_has_died():
    num = 100000

    # check for infected status
    a2 = Agent((0, 1), 'I', mask=False, distancing=True)
    counter = 0
    for i in range(num):
        if a2.has_died():
            counter += 1
    assert round(counter / num, 3) == 0.002

    a2 = Agent((0, 1), 'Q', mask=False, distancing=True)
    counter = 0
    for i in range(num):
        if a2.has_died():
            counter += 1
    assert round(counter / num, 3) == 0.002

    # check if status not infected
    a3 = Agent((0, 1), 'S', mask=False, distancing=True)
    counter = 0
    for i in range(num):
        if a3.has_died():
            counter += 1
    assert round(counter / num, 1) == 0.0
