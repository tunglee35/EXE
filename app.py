"""Streamlit app to generate Tweets."""
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from PIL import Image
# Import from standard library
import logging
import random
from enum import Enum
import time

# Import from 3rd party libraries
import streamlit.components.v1 as components

IMAGE_PATH="elon.jpg"
IMAGE_URL_1="https://raw.githubusercontent.com/tunglee35/cdn/image/Fotor_AI.png"
IMAGE_URL_1="https://raw.githubusercontent.com/tunglee35/cdn/image/Fotor_AI-2.png"

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

class Topic(Enum):
    CURRENT_HOUSING_MARKET_IN_VIETNAM = "Current housing market in Vietnam"
    PHU_QUOC_RESORT_REAL_ESTATE_MARKET = "Phu Quoc resort real estate market"
    PRESS_RELEASE_FOR_REAL_ESTATE_PRODUCT_IN_PHU_QUOC = "Press release for real estate product in Phu Quoc"
    SALE_LETTER_FOR_PHU_QUOC_RESORT_REAL_ESTATE = "Sale letter for Phu Quoc resort real estate"
    CLOSING_DEAL_FOR_A_500000_USD_RESORT_IN_PHU_QUOC = "Closing deal for a 500,000 USD resort in Phu Quoc"

# mock generate text
def generate_text(topic: str, mood: str = "", style: str = ""):
    """Generate Tweet text."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    st.session_state.textarea = "text here"
    st.session_state.tweet = ""
    st.session_state.image = ""
    st.session_state.text_error = ""

    if not topic:
        st.session_state.text_error = "Please enter a topic"
        return
    with text_spinner_placeholder:
        with st.spinner("Please wait while your Tweet is being generated..."):
            ans = ""
            if topic == "Current housing market in Vietnam":
                ans = open('./text_data/ans_1.txt').read()
            elif topic == "Phu Quoc resort real estate market":
                ans = open('./text_data/ans_2.txt').read()
            elif topic == "Press release for real estate product in Phu Quoc":
                ans = open('./text_data/ans_3.txt').read()
            elif topic == "Sale letter for Phu Quoc resort real estate":
                ans = open('./text_data/ans_4.txt').read()
            elif topic == "Closing deal for a 500,000 USD resort in Phu Quoc":
                ans = open('./text_data/ans_5.txt').read()

            time.sleep(1)
            st.session_state.text_error = ""
            st.session_state.n_requests += 1
            st.session_state.tweet = ans
            logging.info(
                f"Tweet: {st.session_state.tweet}"
            )

# mock generate image
def generate_image(file_path=IMAGE_PATH):
    with image_spinner_placeholder:
        with st.spinner("Please wait while your image is being generated..."):
            st.session_state.n_requests += 1
            st.session_state.image = IMAGE_URL_1

# Configure Streamlit page and state
st.set_page_config(page_title="Tweet", page_icon="🤖")

text_spinner_placeholder = st.empty()
image_spinner_placeholder = st.empty()

if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "image" not in st.session_state:
    st.session_state.image = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "image_error" not in st.session_state:
    st.session_state.image_error = ""
if "feeling_lucky" not in st.session_state:
    st.session_state.feeling_lucky = False
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

# Force responsive layout for columns also on mobile
def config_reponsive():
    st.write(
        """<style>
        [data-testid="column"] {
            width: calc(50% - 1rem);
            flex: 1 1 calc(50% - 1rem);
            min-width: calc(50% - 1rem);
        }
        </style>""",
        unsafe_allow_html=True,
    )

# Render Streamlit page
def render_demo():
    st.title("Generate content for your real estate business")

    topic = st.text_input(label="Topic (or hashtag)", placeholder="AI")
    mood = st.text_input(
        label="Mood (e.g. inspirational, funny, serious) (optional)",
        placeholder="inspirational",
    )
    style = st.text_input(
        label="Twitter account handle to style-copy recent Tweets (optional)",
        placeholder="elonmusk",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.feeling_lucky = not st.button(
            label="Generate text",
            type="primary",
            on_click=generate_text,
            args=(topic, mood, style),
        )
    with col2:
        with open("moods.txt") as f:
            sample_moods = f.read().splitlines()
        st.session_state.feeling_lucky = st.button(
            label="Feeling lucky",
            type="secondary",
            on_click=generate_text,
            args=("an interesting topic", random.choice(sample_moods), ""),
        )

    if st.session_state.text_error:
        st.error(st.session_state.text_error)

    if st.session_state.tweet:
        st.markdown("# Generated content")
        st.markdown(f"""
        {st.session_state.tweet}
        """)
        # st.text_area(label="Tweet", value=st.session_state.tweet, height=100)
        col1, col2 = st.columns(2)
        with col1:
            components.html(
                f"""
                    <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{st.session_state.tweet}\n - Tweet generated via" data-url="https://tweets.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                """,
                height=45,
            )

        if not st.session_state.image:
            st.button(
                label="Generate image",
                type="primary",
                on_click=generate_image,
                args=[st.session_state.tweet],
            )
        else:
            st.image(st.session_state.image)
            st.button(
                label="Regenerate image",
                type="secondary",
                on_click=generate_image,
                args=[st.session_state.tweet],
            )

        if st.session_state.image_error:
            st.error(st.session_state.image_error)

        st.markdown("""---""")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**"
            )
            st.markdown("[Twitter Wrapped](https://twitter-likes.streamlit.app)")
            st.markdown("[Content Summarizer](https://web-summarizer.streamlit.app)")
            st.markdown("[Code Translator](https://english-to-code.streamlit.app)")
            st.markdown("[PDF Analyzer](https://pdf-keywords.streamlit.app)")
        with col2:
            st.write("If you like this app, please consider to")
            components.html(
                """
                    <form action="https://www.paypal.com/donate" method="post" target="_top">
                    <input type="hidden" name="hosted_button_id" value="8JJTGY95URQCQ" />
                    <input type="image" src="https://pics.paypal.com/00/s/MDY0MzZhODAtNGI0MC00ZmU5LWI3ODYtZTY5YTcxOTNlMjRm/file.PNG" height="35" border="0" name="submit" title="Donate with PayPal" alt="Donate with PayPal button" />
                    <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
                    </form>
                """,
                height=45,
            )
            st.write("so I can keep it alive. Thank you!")

def render_doc():
    doc = open('./README.md').read()
    st.write(doc)

def config_nav_style():
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

# config
config_reponsive()
config_nav_style()

# sidebar
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Demo', 'Doc'],
                        iconName=['dashboard', 'economy'],
                        default_choice=0)

if tabs =='Demo':
    render_demo()
elif tabs =='Doc':
    render_doc()
# -----


