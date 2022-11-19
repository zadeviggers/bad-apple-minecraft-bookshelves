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

functions: list[str] = []


prev_frame = 0


def flatten(l: list[list]) -> list:
    return [item for sublist in l for item in sublist]


def colour_to_slots(colour: int) -> list[list[str]]:
    if colour == 0:
        # Black
        return [
            ["false", "false", "false"],
            ["false", "false", "false"]
        ]
    elif colour == 1:
        # White
        return [
            ["true", "true", "true"],
            ["true", "true", "true"]
        ]
    elif colour == 2:
        # Grey
        return [
            ["false", "true", "false"],
            ["true", "false", "true"]
        ]
    # elif colour == 3:
    #     # Dark grey
    #     return [
    #         ["true", "true"],
    #         ["false", "true"]
    #     ]
    else:
        return [
            ["false", "false", "false"],
            ["false", "false", "false"]
        ]


def output_frame(output: str, frame_number: int):
    global prev_frame, functions, frame_count
    functions.append(output)

    is_last_frame = frame_number == frame_count - 1

    # Output previous frame
    if frame_number != 0:
        with open(f"datapack/data/bad-apple/functions/frames/frame-{prev_frame}.mcfunction", "w",
                  encoding="utf-8") as outfile:
            outfile.write(
                output + f"\nexecute if score playing bad_apple matches 1 run schedule function bad-apple:frames/frame-{frame_number} 2t")

    # On the last frame, we need to also output the current frame
    if is_last_frame:
        with open(f"datapack/data/bad-apple/functions/frames/frame-{frame_number}.mcfunction", "w",
                  encoding="utf-8") as outfile:
            outfile.write(output)

    if frame_number % 100 == 0:
        print(f"generated function {frame_number}")

    prev_frame = frame_number


def get_block_coords(height: int, i: int, j: int):
    return f"0 {math.ceil((-60 + height - i + height_offset) / 2)} {math.ceil(j / 3)}"


def generate_setblock_command(coordinates: str, slots: list[str]):
    return f'{command_start}{coordinates} minecraft:chiseled_bookshelf[facing=west, slot_0_occupied={slots[0][0]}, slot_1_occupied={slots[0][1]}, slot_2_occupied={slots[0][2]}, slot_3_occupied={slots[1][0]}, slot_4_occupied={slots[1][1]}, slot_5_occupied={slots[1][2]}]'


def all_identical(x: list) -> bool:
    return len(set(x)) == 1


def get_colour_or_black(things: list, i: int, j: int) -> str:
    try:
        return things[i][j]
    except IndexError:
        return "false"


def de_dupe_functions(to_check: str) -> Optional[str]:
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


for frame_number, frame in enumerate(data):
    height = len(frame)
    width = len(frame[0])

    if all_identical(flatten(frame)):
        commands = []

        slots = colour_to_slots(frame[0][0])

        for i in range(height):
            for j in range(width):
                coordinates = get_block_coords(height, i, j)
                command = generate_setblock_command(coordinates, slots)
                commands.append(command)
        output = "\n".join(commands)

        if frame_number == 0 or output != functions[-1]:
            output_frame(output, frame_number)

    else:
        commands = []
        books = []

        for i, row in enumerate(frame):
            books.append([])
            books.append([])

            for j, colour in enumerate(row):
                slots = colour_to_slots(colour)

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

                slots: list[list[str]] = [[], []]

                slots[0].append(get_colour_or_black(books, i, j))
                slots[0].append(get_colour_or_black(books, i, j + 1))
                slots[0].append(get_colour_or_black(books, i, j + 2))
                slots[1].append(get_colour_or_black(books, i + 1, j))
                slots[1].append(get_colour_or_black(books, i + 2, j + 1))
                slots[1].append(get_colour_or_black(books, i + 3, j + 2))

                coordinates = get_block_coords(height, i, j)
                command = generate_setblock_command(coordinates, slots)

                # Don't need to update the block if it was updated to be the same last time it was touched
                if len(functions) == 0 or de_dupe_functions(coordinates) != command:
                    commands.append(command)

        output = "\n".join(commands)

        output_frame(output, frame_number)

print("Done!")
