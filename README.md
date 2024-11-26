# sentencemixerai
This repository is the local version of sentencemixerai.vercel.app. This allows you to run the site and server on your own hardware.
The AI server can run on either CPU or GPU, but expect much faster results on GPU.

# Prerequisites
- Python >= 3.8

# Installation

### Install PyTorch
This will vary based on your operating system. Visit https://pytorch.org/get-started/locally/ to install.

### Install Backend
Install in backend/
I highly reccommend using a Python virtual environment, but this is optional.
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```
Install dependencies
```bash
pip install git+https://github.com/m-bain/whisperx.git
pip install moviepy==1.0.3 flask flask_cors schedule waitress
pip install numpy==1.26.4
```

### Install Frontend
Install in frontend/
```bash
cd frontend
npm install
```

# Usage
- Start backend `python Server.py`
- Start frontend `npm run dev`
- Navigate to http://localhost:5173/ 

### Donations
Donations are very much appreciated to support development!
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E616MPXB)

