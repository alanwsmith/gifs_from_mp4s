#!/usr/bin/env python3

import subprocess
import glob
import os
from pathlib import Path

source_dir = "/Users/alan/GIFs/mp4s"
dest_dir = "/Users/alan/GIFs/mp4_output"

file_list = [
    file for file in glob.glob(f"{source_dir}/*.mp4")
    if os.path.isfile(file)
]

for start_path in file_list:
    output_path = start_path.replace(source_dir, dest_dir).replace(".mp4", ".gif")

    if Path(output_path).is_file():
        continue 


    print(start_path)
    get_crop_command = [
        "ffmpeg", "-i", start_path, 
        "-vf", "cropdetect", "-f", "null", "-"
    ]

    results_crop = subprocess.run(get_crop_command,
         capture_output=True,
         check=True
    )

    lines = results_crop.stderr.decode("utf-8").split("\n")
    crop_line = lines[-5].split("crop=")[1]
    print(crop_line)

    command_2 = [
        "ffmpeg", 
        "-i", start_path, 
        "-vf", f"crop={crop_line},fps=11,scale=380:-2:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=52[p];[s1][p]paletteuse",
        "-y", output_path
    ]

    results_2 = subprocess.run(command_2,
         capture_output=True,
         check=True
    )

print("done")


                      # - 2>&1 | \
# awk '/crop/ { print $NF }' | \
# tail -1 | xargs -I{} ffmpeg \
# -ss 25 -t 9.2 -i "input.mp4" \
# -vf "{},fps=11,scale=380:-2:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=52[p];[s1][p]paletteuse" \
# -y "output.gif"

# command_1 = subprocess.run(
#     ['echo', 'quick brown fox'],
#     capture_output=True,
#     check=True
# )

