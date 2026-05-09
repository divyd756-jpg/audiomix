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
# LIGHT COLOR THEME
# ---------------------------------------------------

st.markdown("""
<style>

/* Full page background */
[data-testid="stAppViewContainer"] {
    background-color: #f5f7ff;
}

/* Buttons */
.stButton > button {
    background-color: #8ec5fc;
    color: black;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

/* Button hover */
.stButton > button:hover {
    background-color: #bfe9ff;
    color: black;
}

/* Text */
h1, h2, h3, p {
    color: #222222;
}

/* Audio player */
audio {
    width: 100%;
    margin-top: 10px;
}

/* Video player */
video {
    border-radius: 10px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# FILE PATHS
# ---------------------------------------------------

VIDEO_PATH = "10sec.mp4"

# SONGS
AUDIO_1 = "white.mp3"
AUDIO_2 = "pink.mp3"
AUDIO_3 = "bbb.mp3"

# ---------------------------------------------------
# CHECK FILES
# ---------------------------------------------------

def check_file(file):
    return os.path.exists(file)

# ---------------------------------------------------
# NOISE REDUCTION
# ---------------------------------------------------

def clean_audio(audio):

    # Reduce noise
    audio = audio.volumex(0.7)

    # Normalize sound
    audio = audio.fx(audio_normalize)

    return audio

# ---------------------------------------------------
# REMOVE NOISE FUNCTION
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

    # Clean audio
    audio = clean_audio(audio)

    # Trim if longer
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)

    # Replace sound
    final = video.set_audio(audio)

    # Export
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
# DJ AUDIO MIXING
# ---------------------------------------------------

def mix_audio_tracks(
    output,
    volume1,
    volume2,
    volume3,
    offset2,
    offset3
):

    # Load songs
    song1 = AudioFileClip(AUDIO_1)
    song2 = AudioFileClip(AUDIO_2)
    song3 = AudioFileClip(AUDIO_3)

    # Clean audio
    song1 = clean_audio(song1)
    song2 = clean_audio(song2)
    song3 = clean_audio(song3)

    # Volume control
    song1 = song1.volumex(volume1)
    song2 = song2.volumex(volume2)
    song3 = song3.volumex(volume3)

    # Play second song after first
    song2 = song2.set_start(
        song1.duration + offset2
    )

    # Play third song after second
    song3 = song3.set_start(
        song1.duration +
        song2.duration +
        offset3
    )

    # Combine songs
    mixed = CompositeAudioClip([
        song1,
        song2,
        song3
    ])

    # Export final mix
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
# REPLACE AUDIO PAGE
# ---------------------------------------------------

# ---------------------------------------------------
# NOISE REMOVAL PAGE
# ---------------------------------------------------

elif st.session_state.page == "noise":

    st.subheader("🔇 Remove Background Noise")

    # -----------------------------------------------
    # CLEAN white.mp3
    # -----------------------------------------------

    if st.button("▶ Clean white.mp3"):

        if check_file(AUDIO_1):

            with st.spinner("Cleaning white.mp3..."):

                remove_noise(
                    AUDIO_1,
                    "clean_white.mp3"
                )

            st.success("✅ white.mp3 Noise Removed!")

            st.audio("clean_white.mp3")

        else:
            st.error("❌ white.mp3 missing.")

    # -----------------------------------------------
    # CLEAN pink.mp3
    # -----------------------------------------------

    if st.button("▶ Clean pink.mp3"):

        if check_file(AUDIO_2):

            with st.spinner("Cleaning pink.mp3..."):

                remove_noise(
                    AUDIO_2,
                    "clean_pink.mp3"
                )

            st.success("✅ pink.mp3 Noise Removed!")

            st.audio("clean_pink.mp3")

        else:
            st.error("❌ pink.mp3 missing.")

    # -----------------------------------------------
    # CLEAN bbb.mp3
    # -----------------------------------------------

    if st.button("▶ Clean bbb.mp3"):

        if check_file(AUDIO_3):

            with st.spinner("Cleaning bbb.mp3..."):

                remove_noise(
                    AUDIO_3,
                    "clean_bbb.mp3"
                )

            st.success("✅ bbb.mp3 Noise Removed!")

            st.audio("clean_bbb.mp3")

        else:
            st.error("❌ bbb.mp3 missing.")

    # -----------------------------------------------
    # BACK BUTTON
    # -----------------------------------------------

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------------------------------------------
# DJ MIX PAGE
# ---------------------------------------------------

elif st.session_state.page == "mix":

    st.subheader("🎧 DJ Audio Mixing Studio")

    # Volume controls
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

    # Timing offset
    st.markdown("### ⏱ Apply Timing Offset")

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

    # Mix button
    if st.button("🎚 Create DJ Mix"):

        if (
            check_file(AUDIO_1)
            and check_file(AUDIO_2)
            and check_file(AUDIO_3)
        ):

            with st.spinner("Mixing Audio Tracks..."):

                mix_audio_tracks(
                    "dj_mix.mp3",
                    volume1,
                    volume2,
                    volume3,
                    offset2,
                    offset3
                )

            st.success("✅ DJ Mix Created Successfully!")

            st.audio("dj_mix.mp3")

        else:
            st.error("❌ Audio files missing.")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------------------------------------------
# NOISE REMOVAL PAGE
# ---------------------------------------------------

elif st.session_state.page == "noise":

    st.subheader("🔇 Remove Background Noise")

    if st.button("▶ Clean white.mp3"):

        if check_file(AUDIO_1):

            with st.spinner("Cleaning Audio..."):

                remove_noise(
                    AUDIO_1,
                    "clean_white.mp3"
                )

            st.success("✅ Noise Removed Successfully!")

            st.audio("clean_white.mp3")

        else:
            st.error("❌ Audio file missing.")

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
