# sentencemixerai

Extract words from video or audio. Mix the words around. Generate a new video or audio clip.
This repository is the local version of [sentencemixerai.vercel.app](https://sentencemixerai.vercel.app), which allows you to run both the site and server on your own hardware.

---

## Prerequisites

- **Python**: Version 3.8 or higher is required.
- **Windows**: This version is optimized for Windows with AMD GPU support

---

## Installation

Follow these steps to set up both the backend and frontend.

### 1. Install PyTorch and DirectML

1. Install PyTorch (CPU version):
```bash
pip install torch torchvision torchaudio
```

2. Install DirectML for AMD GPU support:
```bash
pip install torch-directml
```

### 2. Install Backend

1. Navigate to the `backend/` directory:
```bash
cd backend
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

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

1. Start the backend server:
```bash
cd backend
python Server.py
```

2. In a separate terminal, start the frontend:
```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to:
http://localhost:5173/

### AMD GPU Notes
- The application uses DirectML for AMD GPU acceleration
- First run might be slower due to shader compilation
- If you experience any issues, try updating your AMD drivers

### Donations
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E616MPXB)
