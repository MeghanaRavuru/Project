from pydub import AudioSegment
import model
import streamlit as st
import numpy as np
from io import BytesIO
import streamlit.components.v1 as components

st.title('New Post')

option = st.selectbox(
    'Select the Media type',
    ('Choose', 'Text', 'Sound File', 'Voice'))

if option == 'Text':
    pred = st.text_area('Text Area', height=70, max_chars=1000, help='Text area to enter the text',
                        placeholder='Enter the text')
    col1, col2 = st.columns(2)
    with col1:
        a = st.button("Detect", key='ab', help='Click to check', disabled=False)
    with col2:
        b = st.button("Post", key='bb', help='Click to Post')
    col3, col4 = st.columns(2)
    de = model.detect([pred])
    if a:
        st.markdown(de[0])
    if b:
        if de[0] == "Offensive Language Detected":
            st.write("Offensive Language Detected. Change the post and retry.")
        else:
            st.write("Posted Successfully.")

if option == 'Sound File':
    fileObject = st.file_uploader(label="Please upload your file")
    if fileObject:
        with open(fileObject.name, 'wb') as f:
            f.write(fileObject.getbuffer())
            ogg_version = AudioSegment.from_mp3(fileObject.name)
            ogg_version.export(fileObject.name, format='wav')
            col5, col6, col7 = st.columns(3)
            with col5:
                d = st.button("Preview", help="Click to preview")
            with col6:
                e = st.button("Detect")
            with col7:
                f = st.button("Post")
            if d:
                audio_file = open(fileObject.name, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/ogg')
            if e:
                st.write(model.detect([model.voice_file(fileObject.name)])[0])

            if f:
                if model.detect([model.voice_file(fileObject.name)])[0] == "Offensive Language Detected":
                    st.write("Offensive Language Detected. Change the post and retry.")
                else:
                    st.write("Posted Successfully.")

if option == 'Voice':
    build_dir = "st_audiorec/frontend/build"
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)


    def audiorec_demo_app():
        # STREAMLIT AUDIO RECORDER Instance
        val = st_audiorec()

        if isinstance(val, dict):  # retrieve audio data
            with st.spinner('retrieving audio-recording...'):
                ind, val = zip(*val['arr'].items())
                ind = np.array(ind, dtype=int)  # convert to np array
                val = np.array(val)  # convert to np array
                sorted_ints = val[ind]
                stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
                final = AudioSegment.from_file(stream, frame_rate=8000, channels=1,
                                               sample_width=1).export('result.wav', format='wav')
                u = model.detect([model.voice_file('result.wav')])
                col7,col8 = st.columns(2)
                with col7:
                    fi = st.button("Detect")
                with col8:
                    gi = st.button("Post")
                if fi:
                    st.write(u[0])
                if gi:
                    if u[0] == "Offensive Language Detected":
                        st.write("Offensive Language Detected. Change the post and retry.")
                    else:
                        st.write("Posted Successfully.")
    # Design move app further up and remove top padding
    st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
                unsafe_allow_html=True)
    # Design change st.Audio to fixed height of 45 pixels
    st.markdown('''<style>.stAudio {height: 45px;}</style>''',
                unsafe_allow_html=True)
    # Design change hyperlink href link color
    st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
                unsafe_allow_html=True)  # darkmode
    st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
                unsafe_allow_html=True)  # lightmode
    audiorec_demo_app()