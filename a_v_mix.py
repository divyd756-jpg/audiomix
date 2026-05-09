import streamlit as st
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip
)
import os

# -----------------------------------
# FILE PATHS
# -----------------------------------

VIDEO_PATH = "10sec.mp4"
AUDIO_1 = "ADSS.mp3"
AUDIO_2 = "bbb.mp3"

# -----------------------------------
# STREAMLIT TITLE
# -----------------------------------

st.set_page_config(page_title="Media Mixing Studio")

st.title("🎬 Media Mixing & Audio Studio")

# -----------------------------------
# CHECK FILE EXISTENCE
# -----------------------------------

def file_exists(path):
    return os.path.exists(path)

# -----------------------------------
# 1. REPLACE VIDEO AUDIO
# -----------------------------------

def replace_audio(video_path, audio_path, output):

    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Trim audio if longer than video
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)

        # Set new audio
        final = video.set_audio(audio)

        # Export video
        final.write_videofile(
            output,
            codec="libx264",
            audio_codec="aac",
            fps=24
        )

        video.close()
        audio.close()
        final.close()

        return True

    except Exception as e:
        st.error(f"Error replacing audio: {e}")
        return False

# -----------------------------------
# 2. MIX MULTIPLE AUDIO TRACKS
# -----------------------------------

def mix_audio_tracks(files, output, volumes=None, offsets=None):

    try:
        clips = []

        for i, file in enumerate(files):

            audio = AudioFileClip(file)

            # Volume control
            if volumes:
                audio = audio.volumex(volumes[i])

            # Timing offset
            if offsets:
                audio = audio.set_start(offsets[i])

            clips.append(audio)

        # Combine audio clips
        mixed = CompositeAudioClip(clips)

        # Export mixed audio
        mixed.write_audiofile(
            output,
            fps=44100,
            codec="mp3"
        )

        # Close clips
        for clip in clips:
            clip.close()

        mixed.close()

        return True

    except Exception as e:
        st.error(f"Error mixing audio: {e}")
        return False

# -----------------------------------
# 3. SIMPLE AUDIO CLEANER
# -----------------------------------

def clean_audio(file, output):

    try:
        audio = AudioFileClip(file)

        # Re-encode audio
        audio.write_audiofile(
            output,
            fps=44100
        )

        audio.close()

        return True

    except Exception as e:
        st.error(f"Error cleaning audio: {e}")
        return False

# -----------------------------------
# UI SECTION
# -----------------------------------

st.subheader("🎵 Replace Video Audio")

if st.button("Replace Audio"):

    if file_exists(VIDEO_PATH) and file_exists(AUDIO_1):

        success = replace_audio(
            VIDEO_PATH,
            AUDIO_1,
            "output_video.mp4"
        )

        if success:
            st.success("✅ Audio replaced successfully!")
            st.video("output_video.mp4")

    else:
        st.error("Missing video or audio file.")

# -----------------------------------
# MIX AUDIO SECTION
# -----------------------------------

st.subheader("🎧 Mix Multiple Audio Tracks")

if st.button("Mix Audio Tracks"):

    if file_exists(AUDIO_1) and file_exists(AUDIO_2):

        success = mix_audio_tracks(
            [AUDIO_1, AUDIO_2],
            "mixed_audio.mp3",
            volumes=[0.8, 0.5],
            offsets=[0, 2]
        )

        if success:
            st.success("✅ Audio mixed successfully!")
            st.audio("mixed_audio.mp3")

    else:
        st.error("Missing audio files.")

# -----------------------------------
# CLEAN AUDIO SECTION
# -----------------------------------

st.subheader("🔇 Remove Background Noise")

if st.button("Clean Audio"):

    if file_exists(AUDIO_1):

        success = clean_audio(
            AUDIO_1,
            "clean_audio.mp3"
        )

        if success:
            st.success("✅ Audio cleaned successfully!")
            st.audio("clean_audio.mp3")

    else:
        st.error("Missing audio file.")

# -----------------------------------
# FILE STATUS SECTION
# -----------------------------------

st.subheader("📁 File Status")

files = [VIDEO_PATH, AUDIO_1, AUDIO_2]

for f in files:

    if os.path.exists(f):
        st.success(f"Found: {f}")
    else:
        st.error(f"Missing: {f}")
