import json
import math
from typing import Optional

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


prev_frame_commands: Optional[set] = None
for frame_number, frame in enumerate(data):
    commands = set()
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
            #         ["true", "true"]
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

            command = f'setblock 0 {math.ceil((-60 + height - i) / 2)} {math.ceil(j / 3)} minecraft:chiseled_bookshelf[facing=west, slot_0_occupied={slots[0]}, slot_1_occupied={slots[1]}, slot_2_occupied={slots[2]}, slot_3_occupied={slots[3]}, slot_4_occupied={slots[4]}, slot_5_occupied={slots[5]}]'

            # Don't need to update the block if it was updated the same way last frame
            if (prev_frame_commands is not None) and (command not in prev_frame_commands):
                commands.add(command)

    prev_frame_commands = commands

    with open(f"datapack/data/bad-apple/functions/frames/frame-{frame_number}.mcfunction", "w",
              encoding="utf-8") as outfile:
        output = "\n".join(commands)
        if frame_number != frame_count - 1:
            output += f"\nexecute if score playing bad_apple matches 1 run schedule function bad-apple:frames/frame-{frame_number + 1} 2t"

        outfile.write(output)

    if frame_number % 100 == 0:
        print(f"generated function {frame_number}")

print("Done!")
