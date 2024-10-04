import os
import streamlit as st
import replicate

st.set_page_config(layout="wide")


def main():

    col_input, col_output = st.columns([60, 40])

    with col_input:
        prompt = st.text_area("Prompt")
        secret = st.text_input("Secret", type="password")
        width = st.slider("Width", 0, 1440, 1440, 32)
        height = st.slider("Height", 0, 1440, 1152, 32)
        tolerance = st.slider("Tolerance", 1, 5, 2, 1, help="1 is most strict and 5 is most permissive.")
        seed = st.number_input("Seed",
                               min_value=-1,
                               max_value=999999999,
                               value=-1,
                               step=1,
                               help="Seed number generator. Set to -1 for a random seed.")
        go = st.button("Generate", type="primary", use_container_width=True)

    with col_output:
        if (go):
            with st.spinner(text='Processing...'):
                st.image(generate_image(prompt, secret, width, height, tolerance, seed))
        else:
            st.write("Waiting for input...")


def generate_image(prompt, secret, width, height, tolerance, seed):
    payload = {
        "width": width,
        "height": height,
        "prompt": prompt + " DSC_0111.JPG",
        "output_format": "png",
        "output_quality": 100,
        "safety_tolerance": tolerance,
        "prompt_upsampling": True
    }

    if (seed != -1):
        payload["seed"] = seed

    os.environ["REPLICATE_API_TOKEN"] = secret

    output = replicate.run(
        "black-forest-labs/flux-dev",
        input=payload)

    return output[0]


if __name__ == "__main__":
    main()
