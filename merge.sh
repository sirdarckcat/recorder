cd recorder_output/records
ffmpeg -i video.avi -i audio.wav -c:v copy -c:a aac output.mp4