import cv2
import json

target_fps = 10
rgb_white_value = 255 * 3
rgb_white_threshold = 300
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

            # Convert to ints from unit8s or whatever they are to avoid issues
            r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
            # Average the colour of the pixel
            average = sum((r, g, b)) / 3
            # If it's closer to zero it'll be zero
            # if it's closer to 255 it'll be 255
            pixel_colour = round(average / 255) * 255 

            frame_output[i][j] = False if pixel_colour == 0 else True
    
    output.append(frame_output)
    if count % 100 == 0:
        print(f"Frame {count} done")
    count += 1

            
    success, image = videoCap.read()

json_output = json.dumps(output)
with open("output.data", "w") as outfile:
    outfile.write(json_output)