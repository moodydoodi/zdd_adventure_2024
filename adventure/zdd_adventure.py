from main_classes import CommandHandler, Item, Floor, Room
from zdd_rooms import ALL_ROOMS

EXIT_COMMAND = "exit"


class ZDDAdventure:
    def __init__(self):
        self.items = []
        self.floors = self.create_floors()
        self.current_floor = self.floors['cellar']
        self.current_room = None
        self.game_active = True
        self.command_handler = CommandHandler(self)

    def create_floors(self):
        # Define the floors
        cellar = Floor("cellar", "It's a bit chilly here. The only light is coming from the emergency lights.")
        ground_floor = Floor("ground floor", "You see a reception desk and a few doors on the other end of the huge hallway.")
        first_floor = Floor("first floor", "There are many doors. Study rooms, offices, and labs.")
        second_floor = Floor("second floor", "This floor hosts the professors' offices and some research labs.")
        third_floor = Floor("third floor", "This is the topmost floor with the lecture hall and meeting rooms. You have heard about a roof terrace, but that might just be stories...")
        # roof_floor = Floor("roof", "You really shouldn't be here!!!")

        # Connect floors
        cellar.add_connection("up", ground_floor)
        ground_floor.add_connection("down", cellar)
        ground_floor.add_connection("up", first_floor)
        first_floor.add_connection("down", ground_floor)
        first_floor.add_connection("up", second_floor)
        second_floor.add_connection("down", first_floor)
        second_floor.add_connection("up", third_floor)
        third_floor.add_connection("down", second_floor)

        # Define rooms in each floor
        analog_book = Item("old book", "a real book made of paper", movable=True)
        archive_room = Room("archive", "Old records and dusty books everywhere.",
                            analog_book)
        cellar.add_room("archive", archive_room)
        cellar.add_room("toilet", ALL_ROOMS["toilet_cellar"])

        reception = Room("reception", "You see a welcoming desk and a receptionist.")
        ground_floor.add_room("reception", reception)

        #... Add other rooms ...

        return {
            "cellar": cellar,
            "ground floor": ground_floor,
            "first floor": first_floor,
            "second floor": second_floor
        }

    def play(self):
        introduction = (
        "... slowly ... you .... wake ... up ...\n"
        "You are in a huge room with very little light...\n"
        "Wait! \nThat's the 'Data Science and AI lab' in the cellar of the ZDD!\n"
        "Adrenaline kicks in.\nYou look around.\nWhat is going on?\nWhere is everyone else?\n"
        "You quickly leave the room. But there's no one on the hallway either."
        )
        print(introduction)
        while self.game_active:
            print(40 * "-")
            print(f"{self.current_floor.name.upper()}:\n{self.current_floor.description}")
            print(self.current_floor.get_orientation())
            print("Type 'inventory' to inspect your inventory.")
            action = input("What do you want to do?: ").lower()

            # Handle global commands first
            if self.command_handler.handle_global_commands(action):
                break

            # Exit the game
            if action == EXIT_COMMAND or action == "inventory":
                continue
            # Change the floor:
            elif action.startswith("go "):
                direction = action.split(" ")[1]
                next_floor = self.current_floor.get_floor_in_direction(direction)
                if next_floor:
                    self.current_floor = next_floor
                    self.current_room = None
                else:
                    print("You can't go in that direction!")
            # Enter a room:
            elif action.startswith("enter "):
                direction = action.split(" ")[1]
                next_room = self.current_floor.get_room(direction)
                if next_room:
                    self.current_room = next_room
                    self.current_room.enter_room(self.items, self.command_handler)
                else:
                    print("There is no such room...")
            else:
                print(f"Unknown command! Type '{EXIT_COMMAND}' to stop the game.")


if __name__ == "__main__":
    adventure = ZDDAdventure()
    adventure.play()