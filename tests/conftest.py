import pendulum
import pytest
from schiene2.models import Connection, Station, Train, DepartureOrArrival, Journey


@pytest.fixture
def train():
    return Train(number='ICE 329')


@pytest.fixture
def station():
    return Station(name='Freiburg Hbf')


@pytest.fixture
def departure(station):
    return DepartureOrArrival(station=station, time=pendulum.now(), track=2)


@pytest.fixture
def arrival():
    return DepartureOrArrival(station=station, time=pendulum.now().add(hours=1), track=6)


@pytest.fixture
def journey(departure, arrival, train):
    return Journey(departure, arrival, train)


@pytest.fixture
def connection(journey):
    return Connection(journeys=[journey])


@pytest.fixture
def complete_connection():
    return Connection([
        Journey(
            DepartureOrArrival(
                Station('Frankfurt Hbf'),
                pendulum.create(2017, 12, 9, 14, 45),
                6
            ),
            DepartureOrArrival(
                Station('Freiburg Hbf'),
                pendulum.create(2017, 12, 9, 16, 45),
                3
            ),
            Train(number='ICE 293')
        ),
        Journey(
            DepartureOrArrival(
                Station('Freiburg Hbf'),
                pendulum.create(2017, 12, 9, 17, 10),
                8
            ),
            DepartureOrArrival(
                Station('Hinterzarten'),
                pendulum.create(2017, 12, 9, 17, 55),
                1
            ),
            Train(number='RE 123')
        ),
    ])
