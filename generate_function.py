import json
import math
from typing import Optional

fill_limit = 32_768

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

height = len(data[0])
width = len(data[0][0])
total_pixels = width * height

canvas_bottom = -60
canvas_top = canvas_bottom + height
canvas_left = 0
canvas_right = canvas_left + width
z_coordinate = 0


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


def get_block_coords(i: int, j: int):
    return f"{math.ceil(j / 6)} {math.ceil((canvas_top - i) / 2)} {z_coordinate}"


def get_block_state(slots: list[list[str]]) -> str:
    return f"minecraft:chiseled_bookshelf[facing = south, slot_0_occupied = {slots[0][0]}, slot_1_occupied = {slots[0][1]}, slot_2_occupied = {slots[0][2]}, slot_3_occupied = {slots[1][0]}, slot_4_occupied = {slots[1][1]}, slot_5_occupied = {slots[1][2]}]"


def generate_setblock_command(coordinates: str, block_state: str):
    return f'setblock {coordinates} {block_state}'


def generate_fill_command(x1: int, y1: int, x2: int, y2: int, block_state: str):
    return f"fill {x1} {y1} {z_coordinate} {x2} {y2} {z_coordinate} {block_state}"


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
            start_index = 0
            # If coords_index is less than 10, it's the first command so start_index will be 0.
            if coords_index > 10:
                start_index = function.rfind("\n", 0, coords_index)
            end_index = function.index("\n", coords_index)
            substr = function[start_index:end_index]
            return substr
        except ValueError:
            pass
    return None


def chunked(lst: list, n: int):
    # Yields n-sized chunks
    # From https://stackoverflow.com/a/312464
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_fill_rectangles(x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int, int, int]]:
    width = x2 - x1
    height = y2 - y1
    area = width * height

    if area < fill_limit:
        return [(x1, y1, x2, y2)]

    # Kinda cringe thing that just generates vertical slices, but it works.

    num_of_chunks = math.ceil(area / fill_limit)

    to_chunk = [i for i in range(width)]

    output: list[tuple[int, int, int, int]] = []

    chunks = chunked(to_chunk, num_of_chunks)

    for i, chunk in enumerate(chunks):
        chunk_width = len(chunk)
        x_pos = x1 + ((i + 1) * chunk_width)
        output.append((x_pos, y1, x_pos + chunk_width, y2))

    return output


def commands_to_fill_area(x1: int, y1: int, x2: int, y2: int, block_state: str) -> list[str]:
    rectangles = get_fill_rectangles(x1, y1, x2, y2)
    commands = []

    for rectangle in rectangles:
        commands.append(generate_fill_command(
            rectangle[0], rectangle[1], rectangle[2], rectangle[3], block_state))

    return commands


for frame_number, frame in enumerate(data):

    if all_identical(flatten(frame)):

        slots = colour_to_slots(frame[0][0])

        commands = commands_to_fill_area(
            canvas_left, canvas_bottom, canvas_right, canvas_top, get_block_state(slots))

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
                if not ((j % 2 == 0) or (j % 3 == 0)):
                    continue

                slots: list[list[str]] = [[], []]

                slots[0].append(get_colour_or_black(books, i, j))
                slots[0].append(get_colour_or_black(books, i, j + 1))
                slots[0].append(get_colour_or_black(books, i, j + 2))
                slots[1].append(get_colour_or_black(books, i + 1, j))
                slots[1].append(get_colour_or_black(books, i + 2, j + 1))
                slots[1].append(get_colour_or_black(books, i + 3, j + 2))

                coordinates = get_block_coords(i, j)
                command = generate_setblock_command(
                    coordinates, get_block_state(slots))

                # Don't need to update the block if it was updated to be the same last time it was touched
                if len(functions) == 0 or de_dupe_functions(coordinates) != command:
                    commands.append(command)

        output = "\n".join(commands)

        output_frame(output, frame_number)

print("Done!")
