# Hunt the Wumpus
#
# Hunt the Wumpus is a text-based adventure game developed by Gregory Yob
# in 1973. This version is my Python reinterpretation of the classic Basic
# Game. In this game, the player navigates through a series of connected caves
# arranged in the shape of a dodecahedron as they hunt the dreaded Wumpus.
#
# Unlike the classic version, this game uses dictionaries, lists, and recursive
# programming to simulate the same feel as the original.

import board
import random
import builtins


def search(my_list, location):
    # my basic list search. This function is used for all boolean searches
    # regarding lists. We input a single integer, and if that integer is in
    # the list, return True, otherwise False.
    for i in range(len(my_list)):
        if my_list[i] == location:
            return True
    return False


def shooting_time(home, wumpus, arrows, wumpus_dead):
    wumpus_dead = False
    you_died = False
    arrow_path = []
    flight_path = []
    x = 0
    # get the number of rooms that the user wants to have the arrow fly through
    number_rooms = int(builtins.input("Number of rooms(1 - 5) [0 - not shooting]: "))

    # get the rooms in order to the maximum of the number of rooms that the user
    # wants the arrow to fly through
    if number_rooms in range(0, 6):
        my_arrows = arrows - 1
        x = 0
        arrow_path.insert(0, home)
        while x != number_rooms:
            x += 1
            arrow_path.insert(x, int(builtins.input("Room #%d " % x)))

        # part two - the flight of the arrow.
        # now to figure out the flight path..
        # we will start with the home position.
        print("twaaaang!")
        if my_arrows < 1:
            print("You have used you last arrow.")

        # we want to start with our own location. So we are going to
        # do a quick insert into the flight_path list to do a search
        # to see if the first room that the user selects is a valid one.

        x = -1
        # with the first room selected, is this room a valid room
        # for the flight path? If so, we will continue cycling through
        # the path.
        while x < number_rooms + 1:
            x += 1
            if x < number_rooms + 1:
                if x > 0:
                    print("The arrow is entering room # %d " % arrow_path[x])
                # This is where construct our list array that contains the adjacent rooms.
                flight_path.clear()
                flight_path.insert(0, game_board[arrow_path[x]]["room1"])
                flight_path.insert(1, game_board[arrow_path[x]]["room2"])
                flight_path.insert(2, game_board[arrow_path[x]]["room3"])

                # now, if the while loop is at the last room, this will check that room by itself.
                # I found that without it, there was a constant indexing issue.
                if x == number_rooms:

                    # did we hit the wumpus?
                    if wumpus == arrow_path[x]:
                        print("You hear a howl in the distance.\nYou killed the Wumpus.")
                        return my_arrows, True, False
                    if home == arrow_path[x]:
                        # why did you shoot yourself?
                        print("Smack! Right in the backside.\nYou shot yourself!\nYou died.")
                        return my_arrows, False, True
                    else:
                        # nope, we just hit the wall
                        print("Smack right into the wall.")
                        return my_arrows, False, False
                else:
                    # now , we check the flight of the arrow to see if it hit the wumpus or just a wall.
                    if not search(flight_path, arrow_path[x + 1]):
                        print("Smack right into the wall.")
                        return my_arrows, False, False
                    else:
                        if wumpus == arrow_path[x]:
                            print("You hear a howl in the distance.\nYou killed the Wumpus.")
                            return my_arrows, True, False

    elif number_rooms != 0:
        shooting_time(home, wumpus, arrows, wumpus_dead)

    return my_arrows, wumpus_dead, you_died


def set_bats(bats):
    # we have two bats, so let's place them in the game.
    bat_one = random.randint(1, 20)
    bat_two = random.randint(1, 20)

    # Both bats should be in their own rooms. Let's make sure of that.
    if bat_one != bat_two:
        bats.clear()
        bats.insert(0, bat_one)
        bats.insert(1, bat_two)
    else:
        set_bats(bats)
    return bats


def set_home(wumpus, bats, pits, home):
    # where do we start? Let's see
    my_start = random.randint(1, 20)

    # first check, we don't want to be set right on top of bats or pits.
    if search(bats, my_start) or search(pits, my_start):
        set_home(wumpus, bats, pits, home)

    # sometimes I have found that due to the recursive feature, my_start will
    # be set to None. We don't want that.
    if my_start is not None:
        return my_start
    else:
        set_home(wumpus, bats, pits, home)

    # lastly, we don't want to be just set down upon the wumpus.
    # let's give the user a chance.
    if my_start == wumpus:
        set_home(wumpus, bats, pits, home)

    # also, the new room can't be the same as the previous.
    if my_start == home:
        set_home(wumpus, bats, pits, home)

    return my_start


def set_wumpus(home, pits, bats):
    # set a random location for the wumpus.
    wumpus = random.randint(1, 20)

    # let's not set the wumpus in the same room as the bats.
    if search(bats, wumpus):
        set_wumpus(home, pits, bats)

    # now to check to see that the new location for the wumpus
    # is not on top of you.
    if wumpus != home:
        return wumpus
    else:
        set_wumpus(home, pits, bats)


def set_pits(pits, bats):
    # why do we have pits in the cave? I don't know, but its a hazard.
    # For the game, we have only two.
    pit_one = random.randint(1, 20)
    pit_two = random.randint(1, 20)

    # first check, the bats can't be where the pits are. That would be
    # too easy.
    if search(bats, pit_one) or search(bats, pit_two):
        set_pits(pits, bats)

    # also, the pits can't be in the same room.
    elif pit_one != pit_two:
        pits.clear()
        pits.insert(0, pit_one)
        pits.insert(1, pit_two)
    else:
        set_pits(pits, bats)
    return pits


def action(home, room1, room2, room3, arrows, wumpus):
    wumpus_dead = False
    you_died = False

    # what do you want to do? Let's find out.
    my_action = builtins.input("Shoot, Move, Help, or Quit (S-M-H-Q): ")
    my_action = my_action.strip()  # get rid of any blanks
    my_action = my_action.lower()  # make everything lowercase. It's just easier to work with.
    if my_action == 'm':  # move
        new_location = int(input("Where To: "))
        if new_location == home:  # why do you want to move to the same room as you are already?
            print("Okay?")
        elif new_location == room1 or new_location == room2 or new_location == room3:
            home = new_location
        else:  # The user wants to move to a room that isn't connected or even exists.
            print("Where?")
            action(home, room1, room2, room3, arrows, wumpus)
    elif my_action == 'h':
        # get help
        board.instructions()
    elif my_action == 's':
        # shooting time, but first do we have any arrows?
        if arrows < 1:
            print("You have already used your last arrow.")
            # I like recursive programming. If things fall out, just call the function again.
            action(home, room1, room2, room3, arrows, wumpus)
        else:
            # yes, we have arrows, and are ready to use them.
            arrows, wumpus_dead, you_died = shooting_time(home, wumpus, arrows, wumpus_dead)

    elif my_action == 'q':
        # Let's quit.
        print("Good Bye.")
        exit()
    else:
        action(home, room1, room2, room3, arrows, wumpus)

    return home, arrows, wumpus_dead, you_died


def check_for_baddies(wumpus, bats, pits, room1, room2, room3, home):
    dead = False  # are we dead yet?

    # wumpus
    # first check, is the wumpus nearby?
    if wumpus == room1 or wumpus == room2 or wumpus == room3:
        print("I smell a Wumpus!")
    # is the wumpus in the same room?
    elif wumpus == home:
        wake_wumpus = random.randint(1, 100)
        if wake_wumpus > 25:  # too bad, the odds were not in your favor.
            print("TSK TSK TSK - Wumpus Got You.\nGame Over.")
            return True, wumpus
        else:
            # you scared the wumpus. How is that possible.
            print("You bump an something and feel it run away from you.")
            wumpus = set_wumpus(home, pits, bats)

    # bats
    # Check for bats nearby...
    if search(bats, room1) or search(bats, room2) or search(bats, room3):
        print("Bats nearby....")
    # if true, then you are in the same room as bats.
    elif search(bats, home):
        print("ZAP -- Super Bat Snatch! Elsewhereville for you!!")
        home = set_home(wumpus, bats, pits, home)

    # pits
    # are there pits nearby? if so, where is the draft?
    if search(pits, room1) or search(pits, room2) or search(pits, room3):
        print("I feel a draft....")
    elif search(pits, home):
        # you walked in a pit. Too bad. Game over.
        print("YYYIIIEEEE  FELL IN A PIT!!\nGame Over.")
        dead = True

    return dead, wumpus


def start_game(my_board):
    bats = []
    pits = []

    arrows = 5
    wumpus_dead = False
    bats = set_bats(bats)
    pits = set_pits(pits, bats)
    wumpus = set_wumpus(0, pits, bats)
    home = set_home(wumpus, bats, pits, 0)
    dead = False

    while not dead:
        if wumpus_dead:
            print("Hee Hee - The Wumpus will getcha next time!!")
            break

        dead, wumpus = check_for_baddies(wumpus, bats, pits, game_board[home]["room1"], game_board[home]["room2"],
                                         game_board[home]["room3"], home)
        if not dead:
            # print("bats: ", bats, "pits: ", pits, "home: ", home, "wumpus: ", wumpus)
            print("You are in room: %d" % home)
            print("Tunnels lead to rooms: ", game_board[home]["room1"], ",", game_board[home]["room2"], ",",
                  game_board[home]["room3"])
            print("You have %d arrows" % arrows)
            print("")
            home, arrows, wumpus_dead, dead = action(home, game_board[home]["room1"], game_board[home]["room2"],
                                                     game_board[home]["room3"], arrows, wumpus)


if __name__ == '__main__':
    print("Wumpus\n")
    game_board = board.dodecahedron
    start_game(game_board)
