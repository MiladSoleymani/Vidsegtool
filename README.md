# Vidsegtool

Vidsegtool is a software tool designed to accelerate the preparation of image segmentation data. It integrates Optical Flow and Single-Shot segmentation algorithms to provide semi-automatic labeling capabilities. Users manually label the first frame, and the software automatically labels subsequent frames, enhancing efficiency. The tool also includes intuitive drawing tools like pens and polygons to aid in the labeling process.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview
Vidsegtool aims to simplify and speed up the process of image segmentation by automating the labeling of subsequent frames after the initial manual labeling. This makes it ideal for tasks requiring extensive frame-by-frame annotation.

## Installation
To set up Vidsegtool, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/MiladSoleymani/Vidsegtool.git
    cd Vidsegtool
    ```
2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage
To run the tool, execute the main application script:
```bash
python app.py
```
Detailed usage instructions can be found in the documentation or by exploring the provided scripts.

## Repository Structure
- `controllers`: Contains the control logic for the application.
- `models`: Includes models used for segmentation tasks.
- `osvos`: Implementation of the OSVOS (One-Shot Video Object Segmentation) algorithm.
- `vidsegtool-main`: Main application logic and supporting files.
- `views`: User interface components and views.
- `.gitignore`: Specifies intentionally untracked files to ignore.
- `requirements.txt`: Lists the dependencies required to run the software.
- `app.py`: Main application script.

## Contributing
We welcome contributions to improve Vidsegtool. Please fork the repository, create a new branch, and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
