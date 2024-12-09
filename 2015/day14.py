import aocd
import re
import enum

EXAMPLE = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
""".strip()

class RacerModes(enum.Enum):
    SPRINT = 0
    REST = 1
 
class Racer:

    def __init__(self, name, speed, sprint_time, rest_time):

        self.name = name
        self.speed = speed

        self.mode_timers = {
            RacerModes.SPRINT : sprint_time,
            RacerModes.REST   : rest_time
        }

        self.current_distance = 0
        self.current_mode = RacerModes.SPRINT
        self.timer = 0

    def __repr__(self):

        return f"({self.name} {self.speed} {self.mode_timers[RacerModes.REST]} {self.current_distance})"

    def update(self, steps):

        for _ in range(steps):

            if self.current_mode == RacerModes.SPRINT:
                self.current_distance += self.speed 
            self.timer += 1

            if self.timer >= self.mode_timers[self.current_mode]:
                self.current_mode = RacerModes((self.current_mode.value + 1) % 2)
                self.timer = 0

    def reset(self):
        self.timer = 0
        self.current_mode = RacerModes.SPRINT
        self.current_distance = 0

def simulate_racers(racers, time):

    farthest = None
    farthest_distance = None
    for racer in racers:
        racer.update(time)

        if farthest is None or racer.current_distance > farthest_distance:
            farthest = racer
            farthest_distance = racer.current_distance

        racer.reset()
    
    return farthest.name, farthest_distance

def simulate_racers_newscoring(racers, time):

    racer_scores = { racer.name : 0 for racer in racers }

    for _ in range(time):
    
        first_place_distance = None
        for racer in racers:
            racer.update(1)
            if first_place_distance is None or racer.current_distance > first_place_distance:
                first_place_distance = racer.current_distance

        for racer in racers:
            if racer.current_distance == first_place_distance:
                racer_scores[racer.name] += 1

    for racer in racers:
        racer.reset()

    return racer_scores

if __name__ == "__main__":

    _in = EXAMPLE
    _in = aocd.get_data(year = 2015, day = 14)

    # Parse Input
    racers = []
    for line in _in.split("\n"):
        match = re.match(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", line)
        racers += [Racer(match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)))]

    # Part 1
    print(simulate_racers(racers, 2503)[1])
    
    # Part 2
    print(max(*simulate_racers_newscoring(racers, 2503).values()))