import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip

VIDEO_PATH = "10sec.mp4"
AUDIO_PATH = "ADSS.mp3"

st.title("Media Studio")

if st.button("Replace Audio"):

    video = VideoFileClip(VIDEO_PATH)

    audio = AudioFileClip(AUDIO_PATH)

    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)

    final = video.set_audio(audio)

    final.write_videofile(
        "output.mp4",
        codec="libx264",
        audio_codec="aac"
    )

    st.success("Done!")

    st.video("output.mp4")
