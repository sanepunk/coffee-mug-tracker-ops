# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose  
This document provides a detailed Software Requirements Specification (SRS) for the **Coffee Mug Detection and Tracking** application. The application is a Streamlit-based web app that allows users to upload a video and see coffee mugs automatically detected and tracked with unique identifiers.

### 1.2 Scope  
The system will:

- Accept video file uploads (MP4, MOV, AVI).
- Process the video using a YOLOv5 object detector (trained on “cup” class) and DeepSORT tracker.
- Generate an output video with bounding boxes and IDs over tracked mugs.
- Display the processed video in the browser using Streamlit.
- Allow single- or multi-mug tracking.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term        | Definition                                                                 |
|-------------|----------------------------------------------------------------------------|
| YOLOv5      | “You Only Look Once” version 5, a real-time object detection model.        |
| DeepSORT    | Deep Simple Online and Realtime Tracking, a multi-object tracker.          |
| Streamlit   | A Python framework for building data-driven web apps.                      |
| SRS         | Software Requirements Specification.                                       |
| UI          | User Interface.                                                            |
| API         | Application Programming Interface.                                         |

### 1.4 References

- Ultralytics YOLOv5 GitHub: https://github.com/ultralytics/yolov5  
- DeepSORT-Realtime PyPI: https://pypi.org/project/deep-sort-realtime/  
- Streamlit documentation: https://docs.streamlit.io/

## 2. Overall Description

### 2.1 Product Perspective  
This is a standalone web application. Internally, it integrates:

- **Frontend**: Streamlit UI for file upload and video display.  
- **Backend**: Video processing pipeline (YOLOv5 + DeepSORT).  

### 2.2 Product Functions  
1. **Upload Video**: User can select and upload a video file.  
2. **Process Video**: Server runs the object detection and tracking pipeline.  
3. **Display Output**: Streamlit displays the processed video with overlays.  

### 2.3 User Characteristics  
- **End Users**: Non-technical users who want real-time video tracking demos.  
- **Developers**: Engineers extending or customizing the detection/tracking logic.

### 2.4 Constraints  
- Must run on machines with GPU for real-time processing (optional CPU).  
- Supported video formats: MP4, MOV, AVI.  
- Python 3.8+ environment.  

### 2.5 Assumptions and Dependencies  
- Internet access to download YOLOv5 weights on first run.  
- Pre-trained YOLOv5s model available.  
- `deep_sort_realtime` and other Python packages installed.

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Video Upload  
- **ID**: FR-1  
- **Description**: The system shall allow users to upload a video file through the web UI.  
- **Inputs**: Video file.  
- **Outputs**: Temporary file path for processing.  
- **Error Handling**: Display an error if format unsupported or file corrupted.

#### 3.1.2 Mug Detection  
- **ID**: FR-2  
- **Description**: The system shall run YOLOv5 inference on each video frame to detect mugs (class “cup”).  
- **Performance**: Minimum 5 FPS on GPU.

#### 3.1.3 Mug Tracking  
- **ID**: FR-3  
- **Description**: The system shall use DeepSORT to assign and maintain unique IDs for each detected mug across frames.

#### 3.1.4 Video Output Generation  
- **ID**: FR-4  
- **Description**: The system shall draw bounding boxes and ID labels on frames and write to an output video file.  
- **Output Formats**: MP4 (H.264).

#### 3.1.5 Display Processed Video  
- **ID**: FR-5  
- **Description**: The system shall embed and play the processed video in the Streamlit interface.

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance  
- Must process 720p video at minimum 5 FPS on a modern GPU.  
- End-to-end pipeline latency &le; 2× video length.

#### 3.2.2 Reliability  
- 99% uptime when hosted.  
- Graceful handling of processing failures.

#### 3.2.3 Usability  
- Intuitive UI with clear “Upload” and “Play” buttons.  
- Progress indicator during processing.

#### 3.2.4 Maintainability  
- Modular code structure (`app.py`, `utils/tracking.py`).  
- Clear README and comments.

#### 3.2.5 Portability  
- Python 3.12.4+ compatible.  
- Runs on Windows, macOS, Linux.

## 4. System Architecture

### 4.1 Component Diagram  
[ Streamlit UI ] ←→ [ Processor Module (YOLOv5 + DeepSORT) ] ←→ [ Video I/O ]


### 4.2 Data Flow  
1. User uploads → 2. Video saved → 3. Processor reads frames → 4. Detection & tracking → 5. Write output → 6. UI displays

## 5. External Interface Requirements

### 5.1 User Interfaces  
- **File Uploader** widget.  
- **Video** player component.

### 5.2 Hardware Interfaces  
- GPU (optional) via CUDA.  
- Webcam (future extension).

### 5.3 Software Interfaces  
- Torch Hub for YOLOv5.  
- OpenCV for video I/O.  
- DeepSORT-Realtime API.

## 6. Other Requirements

### 6.1 Logging & Monitoring  
- Logs at INFO level for start/end of processing.  
- Warnings for missing frames/errors.

### 6.2 Security  
- Sanitize uploaded filenames.  
- Limit upload size (e.g., 200 MB).

### 6.3 Backup & Recovery  
- Temporary files purged after session ends.

## 7. Appendices

### 7.1 Glossary  
- **Frame**: Single image from video.  
- **Tracker**: Algorithm to maintain object identity.

### 7.2 Revision History

| Date       | Version | Description                    | Author |
|------------|---------|--------------------------------|--------|
| 2025-05-29 | 1.0     | Initial creation of SRS        | Ojas   |

