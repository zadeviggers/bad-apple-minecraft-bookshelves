import cv2
import json

target_fps = 10
rgb_white_value = 255 * 3
rgb_black_value = 0

videoCap = cv2.VideoCapture("bad-apple-original.mp4")
videoCap.set(cv2.CAP_PROP_FPS, target_fps)


output = []

count = 0

success, image = videoCap.read()
while success:
    frame_output = []
    for i, row in enumerate(image):
        frame_output.append([])
        for j, rgb in enumerate(row):
            frame_output[i].append([])

            # convert to ints from unit8s or whatever they are to avoid issues
            r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])

            sum = r + g + b

            if sum == rgb_black_value:
                frame_output[i][j] = 0
            elif rgb_white_value - sum < 300:
                frame_output[i][j] = 1
            else:
                # It'll be grey or something
                frame_output[i][j] = 2
    
    output.append(frame_output)
    if count % 100 == 0:
        print(f"Frame {count} done")
    count += 1

            
    success, image = videoCap.read()

json_output = json.dumps(output)
with open("output.json", "w") as outfile:
    outfile.write(json_output)