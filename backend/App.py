from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import whisperx
import torch
import os
from torch import load
import mimetypes
import base64
from moviepy.editor import *

app = Flask(__name__)

cors = CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


device = "cuda" if torch.cuda.is_available() else "cpu"
batch_size = 16  # Reduce if low on GPU memory
compute_type = "float16" if device == 'cuda' else 'float32'  # Change to "int8" if low on GPU memory (may reduce accuracy)

def check_file(session_key):
    # Path to the directory where the file should be
    file_dir = os.path.join('tmp', session_key)

    # The file name you're looking for, without the extension
    base_filename = 'source'

    for ext in ['.mp4', '.webm', '.mov', '.wav', '.mp3']:  # Add any file types you expect
        file_path = os.path.join(file_dir, base_filename + ext)
        if os.path.exists(file_path):
            print(f"Found file: {file_path}")
            return file_path  # Return the path of the found file
    
    print(f"No file named 'source' found in directory {file_dir}.")
    return None

# Takes json word objects and appends sublcips into video
def generateVideo(sessionKey, wordsJson, sourceVideoPath):
    words = json.loads(wordsJson)
    subclips = []
    
    if os.path.exists(sourceVideoPath):
        print('source path exists')
    else:
        print('source not downloaded!')
    
    fullVideoClip = VideoFileClip(sourceVideoPath)

    for i in range(len(words)):
        if words[i]["start"] != "xyz":
            subclips.append(
                fullVideoClip.subclip(float(words[i]["start"]), float(words[i]["end"]))
            )
    concatClip = concatenate_videoclips(subclips)
    
    concatClip.write_videofile('tmp/' + sessionKey + "/final.mp4", temp_audiofile='tmp/tempaudio.mp3')
    
# Takes json word objects and appends sublcips into audio
def generateAudio(sessionKey, wordsJson, sourceAudioPath):
    words = json.loads(wordsJson)
    subclips = []
    
    fullAudioClip = AudioFileClip(sourceAudioPath)

    
    for i in range(len(words)):
        if words[i]["start"] != "xyz":
            subclips.append(
                fullAudioClip.subclip(float(words[i]["start"]), float(words[i]["end"]))
            )

    concatClip = concatenate_audioclips(subclips)
    concatClip.write_audiofile(
        'tmp/' + sessionKey + "/final.wav", codec="pcm_s16le"
    )

def read_file_content(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

@app.route('/upload', methods=['POST'])
def upload():
    # Get the session key and uploaded file from the form data
    sessionKey = request.form.get('sessionKey')
    uploaded_file = request.files.get('file')

    try:
        # Extract the file extension
        file_extension = os.path.splitext(uploaded_file.filename)[1]
        new_filename = 'source' + file_extension

        # Define the directory path to store the file
        file_dir = os.path.join('tmp', sessionKey)

        # Create the directory if it doesn't exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            print(f"Made dir {file_dir}")

        # Save the uploaded file to the directory
        file_path = os.path.join(file_dir, new_filename)
        
        uploaded_file.save(file_path)
        print(f"Wrote file {file_path}")

    except Exception as e:
        print(e)
        return jsonify({'statusCode': 500, 'error': str(e)}), 500

    return jsonify({'statusCode': 200})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    sessionKey = data.get('sessionKey')
    isVideo = data.get('isVideo')
    lang = None if data.get('lang') == "auto" else data.get('lang')
    print(lang)

    try:
        # Open file
        sourcePath = check_file(sessionKey)
        if sourcePath is None:
            raise Exception("Source not found!")
        print("Loaded source")

        model = whisperx.load_model(whisper_arch="tiny", device=device, compute_type=compute_type, language=lang)
        audio = whisperx.load_audio(sourcePath)
        result = model.transcribe(audio, batch_size=batch_size)

        # Load alignment model and metadata
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        results = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

        wordsJson = []
        counter = 0
        for segment in results['segments']:
            for word in segment['words']:
                try:
                    wordsJson.append({"id": str(counter), "start": word["start"], "end": word["end"], "word": word["word"].strip()})
                except Exception as ex:
                    print(f"Problem accessing word: {ex}")
                    continue
                counter += 1

        print("done")
        return {
            'statusCode': 200,
            'body': wordsJson
        }

    except Exception as e:
        print("Error processing or saving:", e)
        return {
            'statusCode': 500,
            'error': str(e)
        }
    
@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Parse incoming JSON request
        data = request.get_json()
        chosenWords = data.get('chosenWords')
        sessionKey = str(data.get('sessionKey'))
        isVideo = data.get('isVideo')
        audioOnly = data.get('audioOnly')

        # Determine source and final file paths
        sourcePath = check_file(sessionKey)
        if sourcePath is None:
            return jsonify({"error": "Source file not found!"}), 404

        finalPath = ''
        if isVideo and not audioOnly:
            finalPath = f'tmp/{sessionKey}/final.mp4'
            generateVideo(sessionKey, chosenWords, sourcePath)
        else:
            finalPath = f'tmp/{sessionKey}/final.wav'
            generateAudio(sessionKey, chosenWords, sourcePath)
        
        # Ensure the generated file exists
        if not os.path.exists(finalPath):
            return jsonify({"error": f"File not found: {finalPath}"}), 404
        
        # Read the file content
        file_content = read_file_content(finalPath)

        # Encode the file content as base64
        encoded_file_content = base64.b64encode(file_content).decode('utf-8')

        # Determine content type based on file extension
        mime_type, _ = mimetypes.guess_type(finalPath)
        if not mime_type:
            mime_type = 'application/octet-stream'  # Fallback MIME type

        # Prepare the response
        return jsonify({
            'statusCode': 200,
            'headers': {'Content-Type': mime_type},
            'body': encoded_file_content
        })

    except Exception as e:
        # Catch any exceptions and return an error response
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
