import json
import math
from typing import Optional

command_start = "setblock "
command_start_len = len(command_start)

height_offset = 50

print("opening json file...")
f = open("output.data", encoding="utf-8")
print("file opened!")

data = json.load(f)
print("data loaded")
f.close()
print("file closed")

# setblock ~-1 ~ ~ minecraft:chiseled_bookshelf[facing=east, slot_0_occupied=true]

frame_count = len(data)

print("generating functions")


def get_colour_or_black(things: list, i: int, j: int) -> str:
    try:
        return things[i][j]
    except IndexError:
        return "false"


def de_dupe_functions(functions: list[str], to_check: str) -> Optional[str]:
    for function in reversed(functions):
        try:
            coords_index = function.index(to_check)
            start_index = coords_index - command_start_len
            end_index = function.index("\n", coords_index)
            substr = function[start_index:end_index]
            return substr
        except ValueError:
            pass
    return None


functions: list[str] = []

for frame_number, frame in enumerate(data):
    commands = []
    height = len(frame)

    books = []

    for i, row in enumerate(frame):
        width = len(row)

        books.append([])
        books.append([])

        for j, colour in enumerate(row):
            slots: list[list[str]] = []

            if colour == 0:
                # Black
                slots = [
                    ["false", "false"],
                    ["false", "false"]
                ]
            elif colour == 1:
                # White
                slots = [
                    ["true", "true"],
                    ["true", "true"]
                ]
            elif colour == 2:
                # Grey
                slots = [
                    ["false", "true"],
                    ["true", "false"]
                ]
            # elif colour == 3:
            #     # Dark grey
            #     slots = [
            #         ["true", "true"],
            #         ["false", "true"]
            #     ]

            books[-2].append(slots[0][0])
            books[-2].append(slots[0][1])
            books[-1].append(slots[1][0])
            books[-1].append(slots[1][1])

    for i, row in enumerate(books):
        # Only do this for the first row out of every two
        if i % 2 != 0:
            continue

        for j in range(len(row)):
            # Only run this for the first out of every three
            if (j % 2 != 0) or (j % 3 != 0):
                continue

            slots: list[str] = []

            slots.append(get_colour_or_black(books, i, j))
            slots.append(get_colour_or_black(books, i, j + 1))
            slots.append(get_colour_or_black(books, i, j + 2))
            slots.append(get_colour_or_black(books, i + 1, j))
            slots.append(get_colour_or_black(books, i + 2, j + 1))
            slots.append(get_colour_or_black(books, i + 3, j + 2))

            coordinates = f"0 {math.ceil((-60 + height - i + height_offset) / 2)} {math.ceil(j / 3)}"
            command = f'{command_start}{coordinates} minecraft:chiseled_bookshelf[facing=west, slot_0_occupied={slots[0]}, slot_1_occupied={slots[1]}, slot_2_occupied={slots[2]}, slot_3_occupied={slots[3]}, slot_4_occupied={slots[4]}, slot_5_occupied={slots[5]}]'

            # Don't need to update the block if it was updated to be the same last time it was touched
            if len(functions) == 0 or de_dupe_functions(functions, coordinates) != command:
                commands.append(command)

    output = "\n".join(commands)
    if frame_number != frame_count - 1:
        output += f"\nexecute if score playing bad_apple matches 1 run schedule function bad-apple:frames/frame-{frame_number + 1} 2t"

    with open(f"datapack/data/bad-apple/functions/frames/frame-{frame_number}.mcfunction", "w",
              encoding="utf-8") as outfile:

        outfile.write(output)

    functions.append(output)

    if frame_number % 100 == 0:
        print(f"generated function {frame_number}")

print("Done!")
