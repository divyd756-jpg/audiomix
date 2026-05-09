import streamlit as st
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip
)
from moviepy.audio.fx.all import audio_normalize
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
# LIGHT THEME
# ---------------------------------------------------

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-color: #f5f7ff;
}

.stButton > button {
    background-color: #8ec5fc;
    color: black;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #bfe9ff;
    color: black;
}

h1, h2, h3, p {
    color: #222222;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# FILE PATHS
# ---------------------------------------------------

VIDEO_PATH = "10sec.mp4"

AUDIO_1 = "white.mp3"
AUDIO_2 = "pink.mp3"
AUDIO_3 = "bbb.mp3"

# ---------------------------------------------------
# CHECK FILES
# ---------------------------------------------------

def check_file(file):
    return os.path.exists(file)

# ---------------------------------------------------
# CLEAN AUDIO
# ---------------------------------------------------

def clean_audio(audio):

    audio = audio.volumex(0.7)

    audio = audio.fx(audio_normalize)

    return audio

# ---------------------------------------------------
# REMOVE NOISE
# ---------------------------------------------------

def remove_noise(input_file, output_file):

    audio = AudioFileClip(input_file)

    cleaned = clean_audio(audio)

    cleaned.write_audiofile(
        output_file,
        fps=44100
    )

    audio.close()
    cleaned.close()

# ---------------------------------------------------
# REPLACE VIDEO AUDIO
# ---------------------------------------------------

def replace_audio(video_path, audio_path, output):

    video = VideoFileClip(video_path)

    audio = AudioFileClip(audio_path)

    audio = clean_audio(audio)

    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)

    final = video.set_audio(audio)

    final.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=24
    )

    video.close()
    audio.close()
    final.close()

# ---------------------------------------------------
# DJ MIX FUNCTION
# ---------------------------------------------------

def mix_audio_tracks(
    output,
    volume1,
    volume2,
    volume3,
    offset2,
    offset3
):

    song1 = AudioFileClip(AUDIO_1)
    song2 = AudioFileClip(AUDIO_2)
    song3 = AudioFileClip(AUDIO_3)

    # Clean songs
    song1 = clean_audio(song1)
    song2 = clean_audio(song2)
    song3 = clean_audio(song3)

    # Volume control
    song1 = song1.volumex(volume1)
    song2 = song2.volumex(volume2)
    song3 = song3.volumex(volume3)

    # Song timing
    song2 = song2.set_start(
        song1.duration + offset2
    )

    song3 = song3.set_start(
        song1.duration +
        song2.duration +
        offset3
    )

    # Combine
    mixed = CompositeAudioClip([
        song1,
        song2,
        song3
    ])

    # Export
    mixed.write_audiofile(
        output,
        fps=44100
    )

    song1.close()
    song2.close()
    song3.close()
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

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎵 Replace Video Audio"):
            st.session_state.page = "replace"

    with col2:
        if st.button("🎧 Mix Audio Tracks"):
            st.session_state.page = "mix"

    with col3:
        if st.button("🔇 Remove Noise"):
            st.session_state.page = "noise"

# ---------------------------------------------------
# REPLACE VIDEO PAGE
# ---------------------------------------------------

elif st.session_state.page == "replace":

    st.subheader("🎵 Replace Video Audio")

    if st.button("▶ Start Replacing"):

        if check_file(VIDEO_PATH) and check_file(AUDIO_1):

            with st.spinner("Processing Video..."):

                replace_audio(
                    VIDEO_PATH,
                    AUDIO_1,
                    "output_video.mp4"
                )

            st.success("✅ Audio Replaced Successfully!")

            video_file = open(
                "output_video.mp4",
                "rb"
            )

            video_bytes = video_file.read()

            st.video(video_bytes)

        else:
            st.error("❌ Missing video or audio file.")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------------------------------------------
# DJ MIX PAGE
# ---------------------------------------------------

elif st.session_state.page == "mix":

    st.subheader("🎧 DJ Audio Mixing Studio")

    st.markdown("### 🔊 Adjust Volume Levels")

    volume1 = st.slider(
        "white.mp3 Volume",
        0.0,
        2.0,
        1.0,
        0.1
    )

    volume2 = st.slider(
        "pink.mp3 Volume",
        0.0,
        2.0,
        1.0,
        0.1
    )

    volume3 = st.slider(
        "bbb.mp3 Volume",
        0.0,
        2.0,
        1.0,
        0.1
    )

    st.markdown("### ⏱ Delay Between Songs")

    offset2 = st.slider(
        "Second Song Delay",
        0,
        10,
        2
    )

    offset3 = st.slider(
        "Third Song Delay",
        0,
        10,
        2
    )

    if st.button("🎚 Create DJ Mix"):

        if (
            check_file(AUDIO_1)
            and check_file(AUDIO_2)
            and check_file(AUDIO_3)
        ):

            with st.spinner("Mixing Songs..."):

                mix_audio_tracks(
                    "dj_mix.mp3",
                    volume1,
                    volume2,
                    volume3,
                    offset2,
                    offset3
                )

            st.success("✅ DJ Mix Created!")

            audio_file = open(
                "dj_mix.mp3",
                "rb"
            )

            audio_bytes = audio_file.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

        else:
            st.error("❌ Audio files missing.")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------------------------------------------
# NOISE REMOVAL PAGE
# ---------------------------------------------------

elif st.session_state.page == "noise":

    st.subheader("🔇 Remove Background Noise")

    # white.mp3
    if st.button("▶ Clean white.mp3"):

        if check_file(AUDIO_1):

            with st.spinner("Cleaning Audio..."):

                remove_noise(
                    AUDIO_1,
                    "clean_white.mp3"
                )

            st.success("✅ white.mp3 cleaned!")

            audio_file = open(
                "clean_white.mp3",
                "rb"
            )

            audio_bytes = audio_file.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

    # pink.mp3
    if st.button("▶ Clean pink.mp3"):

        if check_file(AUDIO_2):

            with st.spinner("Cleaning Audio..."):

                remove_noise(
                    AUDIO_2,
                    "clean_pink.mp3"
                )

            st.success("✅ pink.mp3 cleaned!")

            audio_file = open(
                "clean_pink.mp3",
                "rb"
            )

            audio_bytes = audio_file.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

    # bbb.mp3
    if st.button("▶ Clean bbb.mp3"):

        if check_file(AUDIO_3):

            with st.spinner("Cleaning Audio..."):

                remove_noise(
                    AUDIO_3,
                    "clean_bbb.mp3"
                )

            st.success("✅ bbb.mp3 cleaned!")

            audio_file = open(
                "clean_bbb.mp3",
                "rb"
            )

            audio_bytes = audio_file.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------------------------------------------
# FILE STATUS
# ---------------------------------------------------

st.markdown("---")

st.subheader("📁 File Status")

files = [
    VIDEO_PATH,
    AUDIO_1,
    AUDIO_2,
    AUDIO_3
]

for file in files:

    if os.path.exists(file):
        st.success(f"✅ Found: {file}")
    else:
        st.error(f"❌ Missing: {file}")
