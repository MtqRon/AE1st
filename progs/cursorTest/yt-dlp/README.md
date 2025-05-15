# YouTube Video Transcription and Translation Tool

This tool downloads YouTube videos, transcribes them using **local Whisper model**, translates the content **using local translation models**, and embeds bilingual subtitles into the video.

## Features

- Downloads YouTube videos from a URL
- Transcribes audio using **local Whisper model (no API required for transcription)**
- Translates content using **local Hugging Face models (no API required for translation)**
- Detects the language of the content automatically
- Translates content:
  - Japanese to English if the original is in Japanese
  - English to Japanese if the original is in English
- Embeds both original and translated subtitles into the video

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script and paste the YouTube URL when prompted:

```bash
python youtube_transcribe_translate.py
```

The program will:
1. Download the video
2. Extract audio
3. Transcribe the audio using the local Whisper model
4. Translate the content using local Hugging Face models
5. Create subtitle files
6. Embed both subtitle tracks into the video

The final video will be saved as `output_video.mp4` in the current directory.

## Model Details

### Transcription Models
You can change the Whisper model size in the `transcribe_audio` function:

- `base`: Default, fastest but less accurate
- `small`: Better accuracy, moderate resource usage
- `medium`: Better accuracy, higher resource usage
- `large`: Best accuracy, highest resource usage

### Translation Models
The program uses the following models for translation:

- Japanese to English: `Helsinki-NLP/opus-mt-ja-en`
- English to Japanese: `Helsinki-NLP/opus-mt-en-jap`
- Fallback for other languages: `facebook/nllb-200-distilled-600M`

## Dependencies

- yt-dlp: For downloading YouTube videos
- transformers: For local translation models
- openai-whisper: For local transcription
- langdetect: For language detection
- moviepy: For audio extraction
- pysrt: For subtitle file creation
- ffmpeg: For embedding subtitles

## Notes

- Both the Whisper model and translation models will download automatically when first used
- Transcription and translation happen entirely on your computer (no internet required after initial model download)
- Larger models provide better accuracy but require more memory and time to process 