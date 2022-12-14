# Bad Apple played using Minecraft Chiselled Bookshelves

[Video of it working](https://youtu.be/zHtmiLYGzsk)

## How to use the datapack

If you just want to use the datapack in your own world, you can download it from the _releases_ tab.

Use Minecraft snapshot `22w46a` or higher.

I had to assign 20gb of ram to the game to get it to load my save with this datapack.

To play the animation run `/function bad-apple:frames/frame-0`. It'll play at `0, -60, 0`, so it's best viewed on a superflat world.

## Instructions for running

> If you just want the datapack, go to the _releases_ tab.

> Note - I'm currently doing some work on this, so the output is currently so large it's not possible to load the world. Until then, I suggest you use the old pre-generated datapack.

Make sure that the bad apple video is in the root folder (you have to download it yourself) and is named `bad-apple-original.mp4`.

Install `opencv-python`:

```
pip install opencv-python
```

Run `process_video.py`.
You'll now have the video data in a JSON file called `output.data`. It's an array of frames. Each frame is a 2D array of pixels. The value `0` means that a pixel is black, `1` means that a pixel is white, `2` means that a pixel is grey..

Run `generate_function.py`.
This will generate the frame files in the datapack template. Once it's done, copy the datapack into the datapacks folder of a Minecraft java edition world save.

Make sure you're running on Minecraft snapshot `22w46a` or higher.
I had to assign 20gb of ram to the game to get it to load with the datapack enabled, so be careful.

To play the animation run `/function bad-apple:_play` (you can also use `/function bad-apple:_stop` to stop the animation). It'll play at `0, -60, 0`, so it's best viewed on a superflat world.
