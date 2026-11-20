
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

from agent import analyze_image

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Application heading
st.title("🤖 Multimodal AI Agent")

st.write(
    "Upload an image and ask a question. "
    "Our AI agent will analyze the image and respond."
)

st.divider()

# Image upload section
uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["png", "jpg", "jpeg", "webp"]
)

# Display uploaded image
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

# Text prompt section
prompt = st.text_area(
    "Enter your question",
    
    placeholder="Example: Explain this dashboard..."
)

# Analyze button
if st.button("Analyze Image", type="primary"):

    if uploaded_file is None:

        st.warning("Please upload an image.")

    elif not prompt.strip():

        st.warning("Please enter a question.")

    else:

        try:

            image = Image.open(uploaded_file)

            with st.spinner("AI is analyzing your image..."):

                # Call AI agent
                answer = analyze_image(image, prompt)

            # Display response
            st.subheader("🤖 AI Agent Response")

            st.write(answer)

            # Create logs folder
            os.makedirs("logs", exist_ok=True)

            # Prepare log information
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "image_name": uploaded_file.name,
                "prompt": prompt,
                "response": answer
            }

            # Save output logs
            log_file = "logs/output_logs.csv"

            df = pd.DataFrame([log_data])

            df.to_csv(
                log_file,
                mode="a",
                header=not os.path.exists(log_file),
                index=False
            )

            st.success("Analysis completed successfully!")

        except Exception as e:

            st.error(f"Something went wrong: {e}")
