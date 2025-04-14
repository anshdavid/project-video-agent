import subprocess
import os

# List of input video filenames (make sure the paths are correct)
input_files = [
    "examples/Ancient Athens Shadows_simple.mp4",
    "examples/Dystopian Survival.mp4",
    "examples/Goku's Magical Forest.mp4",
    "examples/Miniature Parade Adventure.mp4",
    "examples/Miniature Taj Mahal.mp4",
    "examples/Miniature_Battlefield.mp4",
    "examples/Neon Awakening.mp4",
    "examples/Paris Rooftop Dance.mp4",
    "examples/Opulent_Feast.mp4",
    "examples/Lavish Palace.mp4",
]


def create_four_grid_segment(files, output_filename):
    """
    Create a 2x2 grid from 4 input videos.
    Each video is scaled to 360x640 and overlaid on a 720x1280 blank canvas.
    Layout:
      - Top-left:      at (0, 0)
      - Top-right:     at (360, 0)
      - Bottom-left:   at (0, 640)
      - Bottom-right:  at (360, 640)
    """
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output if exists
        "-i",
        files[0],
        "-i",
        files[1],
        "-i",
        files[2],
        "-i",
        files[3],
        "-filter_complex",
        (
            "nullsrc=size=720x1280 [base]; "
            "[0:v] setpts=PTS-STARTPTS, scale=360x640 [a]; "
            "[1:v] setpts=PTS-STARTPTS, scale=360x640 [b]; "
            "[2:v] setpts=PTS-STARTPTS, scale=360x640 [c]; "
            "[3:v] setpts=PTS-STARTPTS, scale=360x640 [d]; "
            "[base][a] overlay=shortest=1 [tmp1]; "
            "[tmp1][b] overlay=shortest=1:x=360 [tmp2]; "
            "[tmp2][c] overlay=shortest=1:y=640 [tmp3]; "
            "[tmp3][d] overlay=shortest=1:x=360:y=640"
        ),
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-preset",
        "veryfast",
        output_filename,
    ]
    print(f"Creating 4-grid segment: {output_filename}")
    subprocess.run(cmd, check=True)


def create_two_grid_segment(files, output_filename):
    """
    Create a vertical grid (2 videos stacked) from 2 input videos.
    Each video is scaled to 720x640 and overlaid on a 720x1280 blank canvas.
    Layout:
      - Top:    at (0, 0)
      - Bottom: at (0, 640)
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        files[0],
        "-i",
        files[1],
        "-filter_complex",
        (
            "nullsrc=size=720x1280 [base]; "
            "[0:v] setpts=PTS-STARTPTS, scale=720x640 [a]; "
            "[1:v] setpts=PTS-STARTPTS, scale=720x640 [b]; "
            "[base][a] overlay=shortest=1 [tmp1]; "
            "[tmp1][b] overlay=shortest=1:y=640"
        ),
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-preset",
        "veryfast",
        output_filename,
    ]
    print(f"Creating 2-grid segment: {output_filename}")
    subprocess.run(cmd, check=True)


def concat_segments(segment_files, final_output):
    """
    Concatenates video segments listed in 'segment_files' into a single video
    using the FFmpeg concat demuxer.
    """
    list_filename = "segments_list.txt"
    with open(list_filename, "w") as f:
        for seg in segment_files:
            f.write(f"file '{os.path.abspath(seg)}'\n")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_filename, "-c", "copy", final_output]
    print(f"Concatenating segments into: {final_output}")
    subprocess.run(cmd, check=True)
    os.remove(list_filename)


def main():
    segments = []

    # Group 1 (first four videos)
    if len(input_files) >= 4:
        segment1 = "segment1.mp4"
        create_four_grid_segment(input_files[0:4], segment1)
        segments.append(segment1)

    # Group 2 (next four videos, if available)
    if len(input_files) >= 8:
        segment2 = "segment2.mp4"
        create_four_grid_segment(input_files[4:8], segment2)
        segments.append(segment2)

    # Group 3 (the remaining videos; if fewer than 4, use a different grid layout)
    remaining = input_files[8:]
    if len(remaining) == 2:
        segment3 = "segment3.mp4"
        create_two_grid_segment(remaining, segment3)
        segments.append(segment3)
    elif len(remaining) == 4:
        segment3 = "segment3.mp4"
        create_four_grid_segment(remaining, segment3)
        segments.append(segment3)

    final_output = "final_grid_video.mp4"
    concat_segments(segments, final_output)
    print("Final output created:", final_output)


if __name__ == "__main__":
    main()
