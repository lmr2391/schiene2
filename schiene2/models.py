import pendulum
from pendulum import Pendulum
from schiene2.mobile_page import DetailParser, connections


class Station:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class Connection:
    def __init__(self, journeys):
        self.journeys = journeys
        self._original_journeys = None

    def __str__(self):
        return '{}: {} -> {}: {}'.format(
            self.origin.time,
            self.origin.station.name,
            self.destination.time,
            self.destination.station.name
        )

    @property
    def original_journeys(self):
        return self._original_journeys

    @original_journeys.setter
    def original_journeys(self, value):
        if self._original_journeys is None:
            self._original_journeys = value

    @classmethod
    def search(cls, origin, destination, time=pendulum.now()):
        origin = str(origin)
        destination = str(destination)
        url = connections(origin, destination, time)[0]['detail_url']
        parser = DetailParser(url)
        return cls.from_list(parser.journeys())

    @classmethod
    def from_list(cls, lst):
        journeys = [
            Journey.from_dict(_) for _ in lst
        ]
        return Connection(journeys)

    def search_after_missed_at_station(self, station: Station):
        first_missed_journey = [journey
                                for journey in self.journeys
                                if journey.departure.station == station][0]
        earliest_departure_time = first_missed_journey.departure.time.add(minutes=1)
        return self.__class__.search(
            origin=station,
            destination=self.destination.station,
            time=earliest_departure_time
        )

    def update_after_station(self, station: Station, new_part_connection):
        self.original_journeys = self.journeys[:]
        start_index_original_journeys = self.transition_stations.index(station) + 1
        del self.journeys[start_index_original_journeys:]
        self.journeys += new_part_connection.journeys

    @property
    def origin(self):
        return self.journeys[0].departure

    @property
    def destination(self):
        return self.journeys[-1].arrival

    @property
    def transition_stations(self):
        return [journey.departure.station for journey in self.journeys[1:]]

    @property
    def delay_at_destination(self):
        period = self.destination.time - self.original_journeys[-1].arrival.time
        return period.as_timedelta()


class Train:
    def __init__(self, number):
        self.number = number

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


class DepartureOrArrival:
    def __init__(self, station: Station, time: Pendulum, track):
        self.station = station
        self.time = time
        self.track = track

    @classmethod
    def from_dict(cls, dct):
        dct['station'] = Station(dct['station'])
        return DepartureOrArrival(**dct)


class Journey:
    def __init__(self, departure: DepartureOrArrival, arrival: DepartureOrArrival, train: Train):
        self.departure = departure
        self.arrival = arrival
        self.train = train

    @classmethod
    def from_dict(cls, dct):
        return cls(
            departure=DepartureOrArrival.from_dict(dct['departure']),
            arrival=DepartureOrArrival.from_dict(dct['arrival']),
            train=Train.from_dict(dct['train'])
        )
