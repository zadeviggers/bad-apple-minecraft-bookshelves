import json
import cv2

target_fps = 10

videoCap = cv2.VideoCapture("bad-apple-original.mp4")
videoCap.set(cv2.CAP_PROP_FPS, target_fps)

output = []

count = 0

threshold = 35

success, image = videoCap.read()
while success:
    frame_output = []
    for i, row in enumerate(image):
        frame_output.append([])
        for j, rgb in enumerate(row):
            frame_output[i].append([])

            # convert to ints from unit8s or whatever they are to avoid issues
            r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])

            avg = round((r + g + b) / 3)

            if avg <= (0 + threshold):
                # Black
                frame_output[i][j] = 0
            elif avg >= (255 - threshold):
                # White25
                frame_output[i][j] = 1
            else:
                # Grey
                frame_output[i][j] = 2
                # if round(avg / 255) * 255 == 255:
                #     # Light grey
                #     frame_output[i][j] = 2
                # else:
                #     # Dark grey
                #     frame_output[i][j] = 3

    output.append(frame_output)
    if count % 100 == 0:
        print(f"Frame {count} done")
    count += 1

    success, image = videoCap.read()

json_output = json.dumps(output)
with open("output.data", "w") as outfile:
    outfile.write(json_output)
