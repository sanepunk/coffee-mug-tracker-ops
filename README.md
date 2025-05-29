# Coffee Mug Detection and Tracking

A Streamlit-based web application that detects and tracks coffee mugs in videos using YOLOv5 and DeepSORT.

## Features

- Upload video files (MP4, MOV, AVI)
- Detect coffee mugs using YOLOv5
- Track multiple mugs with unique IDs using DeepSORT
- Real-time visualization in web browser

## Requirements

- Python 3.12.4+
- CUDA-capable GPU (optional, but recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Cup detection"
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the displayed URL (usually http://localhost:8501)

3. Upload a video file using the file uploader

4. Wait for processing to complete

5. View the results in the web interface

## Project Structure

```
├── src/
│   └── app.py              # Main Streamlit application
├── utils/
│   └── tracking.py         # Video processing and tracking logic
├── tests/
│   └── test_tracking.py    # Unit tests
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Development

To run tests:
```bash
python -m unittest discover tests
```

## License

[MIT License](LICENSE)
