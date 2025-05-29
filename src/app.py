import streamlit as st
import cv2
import tempfile
from pathlib import Path
from utils.tracking import VideoProcessor

st.set_page_config(
    page_title="Coffee Mug Detection & Tracking",
    page_icon="☕",
    layout="wide"
)

def main():
    st.title("Coffee Mug Detection & Tracking")
    st.write("Upload a video to detect and track coffee mugs!")

    uploaded_file = st.file_uploader(
        "Choose a video file", 
        type=["mp4", "mov", "avi"],
        help="Supported formats: MP4, MOV, AVI"
    )

    if uploaded_file is not None:
        # Create a temporary file to store the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name

        with st.spinner('Processing video...'):
            try:
                processor = VideoProcessor()
                output_path = processor.process_video(video_path)
                
                # Display the processed video
                st.video(output_path)
                
            except Exception as e:
                st.error(f"Error processing video: {str(e)}")
            finally:
                # Cleanup temporary files
                try:
                    Path(video_path).unlink()
                    Path(output_path).unlink()
                except:
                    pass

if __name__ == "__main__":
    main()
