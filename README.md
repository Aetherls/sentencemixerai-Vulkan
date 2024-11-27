# sentencemixerai

Extract words from video or audio. Mix the words around. Generate a new video or audio clip.
This repository is the local version of [sentencemixerai.vercel.app](https://sentencemixerai.vercel.app), which allows you to run both the site and server on your own hardware. The AI server can run on either CPU or GPU, but expect significantly faster results when using a GPU.

---

## Prerequisites

- **Python**: Version 3.8 or higher is required.

---

## Installation

Follow these steps to set up both the backend and frontend.

### 1. Install PyTorch

The installation of PyTorch depends on your operating system and hardware. To install PyTorch, follow the official instructions on the [PyTorch Get Started page](https://pytorch.org/get-started/locally/).

---

### 2. Install Backend

1. Navigate to the `backend/` directory:
    ```bash
    cd backend
    ```

2. (Optional but recommended) Create and activate a Python virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
    ```

3. Install the required Python dependencies:
    ```bash
    pip install git+https://github.com/m-bain/whisperx.git
    pip install moviepy==1.0.3 flask flask_cors schedule waitress
    pip install numpy==1.26.4
    ```

---

### 3. Install Frontend

1. Navigate to the `frontend/` directory:
    ```bash
    cd frontend
    ```

2. Install the necessary Node.js dependencies:
    ```bash
    npm install
    ```

---

## Usage

Once the installation is complete, follow these steps to run the application.

1. Navigate to the `backend/` directory (if you're not already there) and run the backend server:

```bash
python Server.py
```

2. In a separate terminal window, navigate to the frontend/ directory and start the frontend development server:
```bash
npm run dev
```

3. Once both the backend and frontend are running, open your web browser and navigate to:
http://localhost:5173/

### Donations
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E616MPXB)

