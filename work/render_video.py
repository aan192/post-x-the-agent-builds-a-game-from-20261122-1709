import subprocess, os

# 1. Create hook video (3s)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x11081c:s=1080x1920:r=30:d=3",
    "-vf", "drawtext=textfile=work/hook.txt:fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=20",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "work/seg1_hook.mp4"
], check=True)

# 2. Create prompt video (4s)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x190a2a:s=1080x1920:r=30:d=4",
    "-vf", "drawtext=textfile=work/prompt_text.txt:fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=20",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "work/seg2_prompt.mp4"
], check=True)

# 3. Create agent working video (5s)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x11081c:s=1080x1920:r=30:d=5",
    "-vf", "drawtext=textfile=work/agent_text.txt:fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=20",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "work/seg3_agent.mp4"
], check=True)

# 4. Create gameplay video from captured frames (10s)
subprocess.run([
    "ffmpeg", "-y", "-framerate", "3", "-start_number", "0", "-i", "work/frames/frame_%03d.png",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
    "-t", "10", "-c:v", "libx264", "-pix_fmt", "yuv420p", "work/seg4_gameplay.mp4"
], check=True)

# 5. Prepare end card with referral code xmjv0bg8
subprocess.run([
    "ffmpeg", "-y", "-i", "work/endcard.mp4",
    "-vf", "drawtext=text='xmjv0bg8':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=62:fontcolor=#191419:x=210:y=1220",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "work/seg5_endcard.mp4"
], check=True)

# 6. Generate audio track (sine wave beep/ambient tone, 25s total)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "sine=f=523.25:r=44100:d=25",
    "-c:a", "aac", "work/audio.m4a"
], check=True)

# 7. Concat video segments
with open("work/concat.txt", "w") as f:
    f.write("file 'seg1_hook.mp4'\n")
    f.write("file 'seg2_prompt.mp4'\n")
    f.write("file 'seg3_agent.mp4'\n")
    f.write("file 'seg4_gameplay.mp4'\n")
    f.write("file 'seg5_endcard.mp4'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "work/concat.txt",
    "-c:v", "copy", "work/combined_video.mp4"
], check=True)

# 8. Add audio to combined video
subprocess.run([
    "ffmpeg", "-y", "-i", "work/combined_video.mp4", "-i", "work/audio.m4a",
    "-c:v", "copy", "-c:a", "aac", "-shortest", "work/ad.mp4"
], check=True)

print("Video rendered successfully to work/ad.mp4")
