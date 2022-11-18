import json
  
print("opening json file...")
f = open("output.data")
print("file opened!")
  
data = json.load(f)
print("data loaded")
f.close()
print("file closed")

#setblock ~-1 ~ ~ minecraft:chiseled_bookshelf[facing=east, slot_0_occupied=true]

frame_count = len(data)

print("generating functions")

def bool_str(thing: bool) -> str:
    if thing:
        return "true"
    return "false"


for frame_number, frame in enumerate(data):
    commands = []
    height = len(frame)
    width = len(frame[0])

    for i, row in enumerate(frame):
        # Skip every other row
        if i % 2 == 0:
            continue

        for j, colour in enumerate(row):
            # Skip every other colour
            if j % 2 == 0:
                continue

            top_left = colour
            top_right = False
            if width != j + 1:
                top_right = frame[i][j + 1] 
            bottom_left = False 
            if height != i + 1:
                bottom_left = frame[i + 1][j]
            bottom_right = False
            if (height != i + 1) and (width != j + 1):
                bottom_right = frame[i + 1][j + 1]

            top_middle = top_left or top_right
            bottom_middle = bottom_left or bottom_right
            
            slots = [bool_str(top_left), bool_str(top_middle), bool_str(top_right), bool_str(bottom_left), bool_str(bottom_middle), bool_str(bottom_right)]
            # White pixels are true

            command = f"""setblock 0 {-60 + height - i} {j} minecraft:chiseled_bookshelf[facing=east, slot_0_occupied={slots[0]}, slot_1_occupied={slots[1]}, slot_2_occupied={slots[2]}, slot_3_occupied={slots[3]}, slot_4_occupied={slots[4]}, slot_5_occupied={slots[5]}]"""
            
            commands_length = len(commands)
            if commands_length <= 2 or command != commands[commands_length - 1]:
                commands.append(command)

    # for i, row in enumerate(frame):
    #     for j, colour in enumerate(row):
    #         if frame_number == 0 or (colour != data[frame_number - 1][i][j]):
    #             slots = []
    #             # White pixels are true
    #             if colour:
    #                 slots = ["false", "false", "false", "false", "false", "false"]
    #             # Black pixels are false
    #             else:
    #                 slots = ["true", "true", "true", "true", "true", "true"]

    #             command = f"""setblock 0 {-60 + height - i} {j} minecraft:chiseled_bookshelf[facing=east, slot_0_occupied={slots[0]}, slot_1_occupied={slots[1]}, slot_2_occupied={slots[2]}, slot_3_occupied={slots[3]}, slot_4_occupied={slots[4]}, slot_5_occupied={slots[5]}]"""
    #             commands.append(command)
   
    if frame_number != frame_count - 1:
        commands.append(f"schedule function bad-apple:frames/frame-{frame_number + 1} 2t")

    with open(f"datapack/data/bad-apple/functions/frames/frame-{frame_number}.mcfunction", "w") as outfile:
        outfile.write("\n".join(commands))
        if frame_number % 100 == 0:
            print(f"generated function {frame_number}")

print("Done!")
