# VideoSegTool

A semi-automatic video segmentation tool that accelerates the preparation of image segmentation data for video sequences. This tool allows users to manually label objects in key frames and automatically propagate labels to subsequent frames using computer vision algorithms.

## Features

- **Manual Annotation Tools**
  - Pencil tool for freehand drawing/erasing
  - Polygon tool for precise region selection
  - Move tool for navigation
  - Adjustable tool size and transparency

- **Semi-Automatic Segmentation**
  - Optical Flow algorithm for motion-based label propagation
  - OSVOS (One-Shot Video Object Segmentation) deep learning model
  - Key frame-based workflow for efficient annotation

- **User Interface**
  - PyQt6-based desktop application
  - Frame-by-frame navigation
  - Zoom controls
  - Interactive frame selection for batch processing
  - Multi-label support with different colors

## Installation

### Prerequisites
- Python 3.8 or higher
- CUDA-capable GPU (recommended for OSVOS)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/VideoSegTool.git
cd VideoSegTool
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download OSVOS pre-trained models:
```bash
cd osvos/models
bash download_parent_model.sh
bash download_vgg_weights.sh
cd ../..
```

## Usage

### Basic Workflow

1. **Launch the application:**
```bash
python app.py
```

2. **Load a video:**
   - Click "Load Video" and select an MP4 file
   - The video will be loaded and the first frame displayed

3. **Create annotations:**
   - Select the Pencil or Polygon tool
   - Draw on the video frame to create labels
   - Use different label IDs for different objects
   - Mark important frames as "key frames"

4. **Propagate labels:**
   - Click "Run" to open the algorithm selection window
   - Choose frames to process
   - Select either Optical Flow or OSVOS algorithm
   - Click "Run" to propagate labels automatically

### Tools

- **Move Tool**: Pan around the video frame (useful when zoomed)
- **Pencil Tool**: Draw or erase labels freehand
  - Left click: Draw
  - Right click: Erase
- **Polygon Tool**: Create precise polygon selections
  - Click to add points
  - Close the polygon to fill the region

### Keyboard Shortcuts

- `Space`: Play/pause video
- `Left/Right Arrow`: Navigate frames
- `+/-`: Zoom in/out
- `K`: Mark current frame as key frame

## Architecture

The application follows an MVC (Model-View-Controller) pattern:

```
VideoSegTool/
├── app.py              # Main application entry point
├── models/             # Data models
│   └── model.py        # Application state management
├── views/              # UI components
│   ├── main_view.py    # Main window interface
│   └── run_view.py     # Algorithm execution interface
├── controllers/        # Business logic
│   ├── main_ctrl.py    # Core application logic
│   ├── tools.py        # Drawing tools implementation
│   ├── render.py       # Frame rendering
│   └── pipeline.py     # Processing pipeline framework
└── osvos/              # OSVOS algorithm implementation
    ├── main.py         # OSVOS runner
    └── vgg_osvos.py    # Neural network architecture
```

## Algorithms

### Optical Flow
Uses OpenCV's Farneback optical flow algorithm to track pixel movements between frames and propagate labels accordingly. Best for objects with consistent motion patterns.

### OSVOS (One-Shot Video Object Segmentation)
A deep learning approach that learns object appearance from annotated key frames and segments the same objects in other frames. Based on a VGG-16 architecture fine-tuned for video segmentation.

## Dependencies

- PyQt6 - GUI framework
- PyTorch - Deep learning framework
- OpenCV - Computer vision library
- NumPy - Numerical computing
- torchvision - Computer vision models for PyTorch
- tqdm - Progress bars

## Troubleshooting

### OSVOS Model Not Found
If you encounter model loading errors, ensure you've downloaded the pre-trained weights using the provided scripts in `osvos/models/`.

### GPU Memory Issues
For large videos or when using OSVOS, you may need to:
- Process fewer frames at once
- Reduce video resolution
- Use CPU mode (slower but more memory efficient)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

[Add your license information here]

## Acknowledgments

- OSVOS implementation based on the paper: "One-Shot Video Object Segmentation" by S. Caelles et al.
- Uses the DAVIS 2016 dataset format for training and evaluation