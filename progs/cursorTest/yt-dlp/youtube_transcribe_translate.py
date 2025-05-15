#!/usr/bin/env python3
# YouTube Video Downloader and Translator with local Whisper transcription and local translation

import sys
import os
import subprocess
import json
from typing import Dict, Any, List, Tuple
import langdetect
import yt_dlp
from moviepy.editor import VideoFileClip
from pysrt import SubRipFile, SubRipItem, SubRipTime
import whisper  # Using local Whisper model
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

def download_youtube_video(url: str) -> str:
    """Download a YouTube video and return the path to the downloaded file."""
    print(f"Downloading video from {url}...")
    
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    
    print(f"Video downloaded to {filename}")
    return filename

def extract_audio(video_path: str) -> str:
    """Extract audio from video file and return the path to the audio file."""
    print("Extracting audio from video...")
    audio_path = "audio.mp3"
    
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec='mp3')
    
    print(f"Audio extracted to {audio_path}")
    return audio_path

def transcribe_audio(audio_path: str) -> Dict[str, Any]:
    """Transcribe audio using local Whisper model."""
    print("Transcribing audio using local Whisper model...")
    
    # Use local Whisper model (base, small, medium, or large)
    model = whisper.load_model("base")  # You can change to "small", "medium", or "large" for better accuracy
    result = model.transcribe(audio_path)
    
    detected_language = result.get("language", "")
    print(f"Detected language: {detected_language}")
    
    return result

def get_translation_model(source_lang: str, target_lang: str):
    """Get appropriate translation model based on language pair."""
    if source_lang.lower() in ["ja", "jp", "japanese"] and target_lang.lower() == "en":
        # Japanese to English
        model_name = "Helsinki-NLP/opus-mt-ja-en"
    elif source_lang.lower() == "en" and target_lang.lower() in ["ja", "jp", "japanese"]:
        # English to Japanese
        model_name = "Helsinki-NLP/opus-mt-en-jap"
    else:
        # Fallback to multilingual model
        model_name = "facebook/nllb-200-distilled-600M"
    
    print(f"Loading translation model: {model_name}")
    
    # For standard Helsinki models
    if "Helsinki-NLP" in model_name:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        translator = pipeline("translation", model=model, tokenizer=tokenizer)
        return translator
    else:
        # For NLLB model with different usage
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Map language codes to NLLB format
        source_code = "jpn_Jpan" if source_lang.lower() in ["ja", "jp", "japanese"] else "eng_Latn"
        target_code = "eng_Latn" if target_lang.lower() == "en" else "jpn_Jpan"
        
        translator = pipeline("translation", model=model, tokenizer=tokenizer, 
                               src_lang=source_code, tgt_lang=target_code)
        return translator

def translate_text(translator, text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using the provided model."""
    if not text.strip():
        return ""
    
    # For Helsinki models
    if hasattr(translator, "model") and "Helsinki-NLP" in translator.model.name_or_path:
        result = translator(text)
        return result[0]['translation_text']
    else:
        # For NLLB model
        result = translator(text)
        return result[0]['translation_text']

def translate_transcription(transcription: Dict[str, Any]) -> Dict[str, Any]:
    """Translate the transcription to the target language using local models."""
    source_lang = transcription.get("language", "")
    
    if not source_lang:
        # Try to detect language from the text
        try:
            source_lang = langdetect.detect(transcription["text"])
        except:
            print("Could not detect language. Defaulting to English.")
            source_lang = "en"
    
    target_lang = "en" if source_lang.lower() in ["ja", "jp", "japanese"] else "ja"
    print(f"Translating from {source_lang} to {target_lang} using local model...")
    
    # Get the appropriate translation model
    translator = get_translation_model(source_lang, target_lang)
    
    translated_segments = []
    total_segments = len(transcription["segments"])
    
    for i, segment in enumerate(transcription["segments"]):
        text = segment["text"]
        print(f"Translating segment {i+1}/{total_segments}...")
        
        translated_text = translate_text(translator, text, source_lang, target_lang)
        translated_segments.append({**segment, "translated_text": translated_text})
    
    return {**transcription, "translated_segments": translated_segments, "target_language": target_lang}

def create_subtitle_files(transcription: Dict[str, Any]) -> Tuple[str, str]:
    """Create subtitle files for both original and translated text."""
    print("Creating subtitle files...")
    
    original_srt = SubRipFile()
    translated_srt = SubRipFile()
    
    for i, segment in enumerate(transcription.get("translated_segments", [])):
        start_time = segment["start"]
        end_time = segment["end"]
        
        # Convert float seconds to hours, minutes, seconds, milliseconds
        start_hours, remainder = divmod(start_time, 3600)
        start_minutes, start_seconds = divmod(remainder, 60)
        start_ms = int((start_seconds - int(start_seconds)) * 1000)
        start_seconds = int(start_seconds)
        
        end_hours, remainder = divmod(end_time, 3600)
        end_minutes, end_seconds = divmod(remainder, 60)
        end_ms = int((end_seconds - int(end_seconds)) * 1000)
        end_seconds = int(end_seconds)
        
        # Create SubRipTime objects
        start_time_obj = SubRipTime(hours=int(start_hours), minutes=int(start_minutes), 
                                   seconds=start_seconds, milliseconds=start_ms)
        end_time_obj = SubRipTime(hours=int(end_hours), minutes=int(end_minutes), 
                                 seconds=end_seconds, milliseconds=end_ms)
        
        # Original subtitle
        original_item = SubRipItem(
            index=i+1,
            start=start_time_obj,
            end=end_time_obj,
            text=segment["text"]
        )
        original_srt.append(original_item)
        
        # Translated subtitle
        translated_item = SubRipItem(
            index=i+1,
            start=start_time_obj,
            end=end_time_obj,
            text=segment.get("translated_text", "")
        )
        translated_srt.append(translated_item)
    
    original_srt_path = "original.srt"
    translated_srt_path = "translated.srt"
    
    original_srt.save(original_srt_path, encoding='utf-8')
    translated_srt.save(translated_srt_path, encoding='utf-8')
    
    print(f"Created subtitle files: {original_srt_path} and {translated_srt_path}")
    return original_srt_path, translated_srt_path

def embed_subtitles(video_path: str, original_srt: str, translated_srt: str) -> str:
    """Embed subtitles into the video."""
    print("Embedding subtitles into video...")
    
    output_path = "output_video.mp4"
    
    # First, create hardcoded subtitles for the original language at the top
    temp_output1 = "temp_output1.mp4"
    cmd1 = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={original_srt}:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,BorderStyle=4,Outline=1,Shadow=0,Alignment=2'",
        "-c:a", "copy",
        temp_output1
    ]
    
    print("Step 1: Adding original language subtitles")
    subprocess.run(cmd1)
    
    # Then add the translated subtitles at the bottom of the video
    cmd2 = [
        "ffmpeg", "-y",
        "-i", temp_output1,
        "-vf", f"subtitles={translated_srt}:force_style='FontSize=24,PrimaryColour=&H0000FFFF,BorderStyle=4,Outline=1,Shadow=0,Alignment=6'",
        "-c:a", "copy",
        output_path
    ]
    
    print("Step 2: Adding translated language subtitles")
    subprocess.run(cmd2)
    
    # Clean up the temporary file
    if os.path.exists(temp_output1):
        os.remove(temp_output1)
    
    print(f"Video with subtitles saved to {output_path}")
    return output_path

def main():
    # Read YouTube URL from standard input
    print("Enter the YouTube URL: ", end="")
    url = input().strip()
    
    if not url:
        print("No URL provided.")
        sys.exit(1)
    
    # Process the video
    try:
        video_path = download_youtube_video(url)
        audio_path = extract_audio(video_path)
        transcription = transcribe_audio(audio_path)
        translated_transcription = translate_transcription(transcription)
        original_srt, translated_srt = create_subtitle_files(translated_transcription)
        output_video = embed_subtitles(video_path, original_srt, translated_srt)
        
        print(f"\nProcessing complete! Video with bilingual subtitles is at: {output_video}")
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary files
        temp_files = ["audio.mp3", "original.srt", "translated.srt", "temp_output1.mp4", "downloaded_video.mp4"]
        for file in temp_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"Removed temporary file: {file}")
                except Exception as e:
                    print(f"Failed to remove temporary file {file}: {e}")
                    pass

if __name__ == "__main__":
    main() 