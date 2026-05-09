```python
import streamlit as st
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip
)
import os

# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------

st.set_page_config(
    page_title="DJ Audio & Video Studio",
    layout="centered"
)

st.title("🎧 DJ Audio & Video Mixing Studio")

# ---------------------------------------------------
# FILE PATHS
# ---------------------------------------------------

VIDEO_PATH = "10sec.mp4"

# AUDIO SONGS
AUDIO_1 = "ADSS.mp3"
AUDIO_2 = "bbb.mp3"

# ---------------------------------------------------
# CHECK FILES
# ---------------------------------------------------

def check_file(file):
    return os.path.exists(file)

# ---------------------------------------------------
# SIMPLE NOISE REDUCTION
# ---------------------------------------------------

def clean_audio(audio):

    # Reduce background noise slightly
    return audio.volumex(0.8)

# ---------------------------------------------------
# FUNCTION: REPLACE VIDEO AUDIO
# ---------------------------------------------------

def replace_audio(video_path, audio_path, output):

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Clean audio
    audio = clean_audio(audio)

    # Trim audio if longer than video
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)

    # Replace audio
    final = video.set_audio(audio)

    # Export video
    final.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=24
    )

    # Close files
    video.close()
    audio.close()
    final.close()

# ---------------------------------------------------
# FUNCTION: DJ AUDIO MIXING
# ---------------------------------------------------

def mix_audio_tracks(output):

    # Load first song
    song1 = AudioFileClip(AUDIO_1)

    # Load second song
    song2 = AudioFileClip(AUDIO_2)

    # Clean audio
    song1 = clean_audio(song1)
    song2 = clean_audio(song2)

    # Start second song after first song + 2 sec gap
    song2 = song2.set_start(song1.duration + 2)

    # Combine songs
    mixed = CompositeAudioClip([
        song1,
        song2
    ])

    # Export mixed audio
    mixed.write_audiofile(
        output,
        fps=44100
    )

    # Close files
    song1.close()
    song2.close()
    mixed.close()

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if st.session_state.page == "home":

    st.subheader("🎬 Select Operation")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎵 Replace Video Audio"):
            st.session_state.page = "replace"

    with col2:
        if st.button("🎧 Mix Audio Tracks"):
            st.session_state.page = "mix"

# ---------------------------------------------------
# REPLACE AUDIO PAGE
# ---------------------------------------------------

elif st.session_state.page == "replace":

    st.subheader("🎵 Replace Video Audio")

    st.write("Replace video sound with ADSS.mp3")

    if st.button("▶ Start Replacing"):

        if check_file(VIDEO_PATH) and check_file(AUDIO_1):

            with st.spinner("Processing Video..."):

                replace_audio(
                    VIDEO_PATH,
                    AUDIO_1,
                    "output_video.mp4"
                )

            st.success("✅ Audio Replaced Successfully!")

            st.video("output_video.mp4")

        else:
            st.error("❌ Missing video or audio file.")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------------------------------------------
# DJ MIX PAGE
# ---------------------------------------------------

elif st.session_state.page == "mix":

    st.subheader("🎧 DJ Audio Mixing Studio")

    st.write("ADSS.mp3 plays first, then 2 seconds gap, then bbb.mp3")

    if st.button("🎚 Create DJ Mix"):

        if check_file(AUDIO_1) and check_file(AUDIO_2):

            with st.spinner("Mixing Audio Tracks..."):

                mix_audio_tracks("dj_mix.mp3")

            st.success("✅ DJ Mix Created Successfully!")

            st.audio("dj_mix.mp3")

        else:
            st.error("❌ Audio files missing.")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------------------------------------------
# FILE STATUS
# ---------------------------------------------------

st.markdown("---")
st.subheader("📁 File Status")

files = [VIDEO_PATH, AUDIO_1, AUDIO_2]

for file in files:

    if os.path.exists(file):
        st.success(f"✅ Found: {file}")
    else:
        st.error(f"❌ Missing: {file}")
```
