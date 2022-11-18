import json
  
print("opening json file...")
f = open("output.json")
print("file opened!")
  
data = json.load(f)
print("data loaded")
f.close()
print("file closed")

#setblock ~-1 ~ ~ minecraft:chiseled_bookshelf[facing=east, slot_0_occupied=true]

frame_count = len(data)

print("generating functions")
for frame_number, frame in enumerate(data):
    commands = []
    height = len(frame)
    for i, row in enumerate(frame):
        for j, colour in enumerate(row):
            if frame_number == 0 or (colour != data[frame_number - 1][i][j]):
                slots = []
                # White pixels are true
                if colour:
                    slots = ["false", "false", "false", "false", "false", "false"]
                # Black pixels are false
                else:
                    slots = ["true", "true", "true", "true", "true", "true"]

                command = f"""setblock 0 {-60 + height - i} {j} minecraft:chiseled_bookshelf[facing=east, slot_0_occupied={slots[0]}, slot_1_occupied={slots[1]}, slot_2_occupied={slots[2]}, slot_3_occupied={slots[3]}, slot_4_occupied={slots[4]}, slot_5_occupied={slots[5]}]"""
                commands.append(command)
   
    if frame_number != frame_count - 1:
        commands.append(f"schedule function bad-apple:frames/frame-{frame_number + 1} 2t")

    with open(f"datapack/data/bad-apple/functions/frames/frame-{frame_number}.mcfunction", "w") as outfile:
        outfile.write("\n".join(commands))
        if count % 100 == 0:
            print(f"generated function {frame_number}")

print("Done!")