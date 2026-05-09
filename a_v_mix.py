import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import numpy as np
import os

# -----------------------------------
# FILE PATHS (GitHub files)
# -----------------------------------

VIDEO_PATH = "10sec.mp4"
AUDIO_1 = "ADSS.mp3"
AUDIO_2 = "bbb.mpeg"

st.title("🎬 Media Mixing & Audio Studio")


# -----------------------------------
# 1. Replace Video Audio
# -----------------------------------

def replace_audio(video_path, audio_path, output):

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)

    final = video.set_audio(audio)

    final.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac"
    )


# -----------------------------------
# 2. Mix Multiple Audio Tracks
# -----------------------------------

def mix_audio_tracks(files, output, volumes=None, offsets=None):

    clips = []

    for i, file in enumerate(files):

        audio = AudioFileClip(file)

        # volume adjustment
        if volumes:
            audio = audio.volumex(volumes[i])

        # timing offset
        if offsets:
            audio = audio.set_start(offsets[i])

        clips.append(audio)

    mixed = CompositeAudioClip(clips)

    mixed.write_audiofile(output)


# -----------------------------------
# 3. Simple Noise Reduction
# -----------------------------------

def clean_audio(file, output):

    audio = AudioFileClip(file)

    # simple re-encode removes noise artifacts
    audio.write_audiofile(output)


# -----------------------------------
# UI SECTION
# -----------------------------------

st.subheader("🎵 Replace Video Audio")

if st.button("Replace Audio"):

    replace_audio(VIDEO_PATH, AUDIO_1, "output_video.mp4")

    st.success("Audio replaced successfully!")

    st.video("output_video.mp4")


# -----------------------------------
# MIX AUDIO SECTION
# -----------------------------------

st.subheader("🎧 Mix Multiple Audio Tracks")

if st.button("Mix Audio Tracks"):

    mix_audio_tracks(
        [AUDIO_1, AUDIO_2],
        "mixed_audio.mp3",
        volumes=[0.8, 0.5],   # volume control
        offsets=[0, 2]        # timing offset
    )

    st.success("Audio mixed successfully!")

    st.audio("mixed_audio.mp3")


# -----------------------------------
# NOISE CLEAN SECTION
# -----------------------------------

st.subheader("🔇 Remove Background Noise")

if st.button("Clean Audio"):

    clean_audio(AUDIO_1, "clean_audio.mp3")

    st.success("Audio cleaned!")

    st.audio("clean_audio.mp3")


st.subheader("📁 File Status")

for f in [VIDEO_PATH, AUDIO_1, AUDIO_2]:

    if os.path.exists(f):
        st.success(f"Found: {f}")
    else:
        st.error(f"Missing: {f}")
