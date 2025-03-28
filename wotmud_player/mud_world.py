import json
from dao_room import DAORoom
from utils import setup_logging


class World:
    def __init__(self):
        self.visited_rooms = []
        self.rooms = DAORoom()

    def current_room(self):
        return self.visited_rooms[-1]

    def previous_room(self):
        return self.visited_rooms[-2]

    def go(self, direction, room):
        self.rooms.add_room(room)
        self.visited_rooms.append(room.id)
        current_room = self.rooms.get_room_by_id(self.current_room())
        previous_room = self.rooms.get_room_by_id(self.previous_room())
        previous_room.map_room_to_exit(direction, current_room.id)
        current_room.map_room_to_opposite_exit(direction, previous_room)

    def choose_direction(self, include_visited=False):
        pass


if __name__ == "__main__":
    logger = setup_logging()
    world = World()
    logger.info(json.dumps(world.rooms.to_dict(), indent=4))
