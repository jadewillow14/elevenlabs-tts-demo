import os
import sys
import argparse
import requests

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def synthesize(text, voice_id, output_path, model_id="eleven_multilingual_v2"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit("Please set ELEVENLABS_API_KEY in your environment.")
    url = API_URL.format(voice_id=voice_id)
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    if response.status_code != 200:
        raise SystemExit(f"API error {response.status_code}: {response.text}")
    with open(output_path, "wb") as audio_file:
        audio_file.write(response.content)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate speech from text using ElevenLabs.")
    parser.add_argument("--text", help="Text to synthesize; reads stdin when omitted.")
    parser.add_argument("--voice-id", default="21m00Tcm4TlvDq8ikWAM", help="ElevenLabs voice ID.")
    parser.add_argument("--output", default="speech.mp3", help="Output MP3 path.")
    args = parser.parse_args()
    text = args.text if args.text else sys.stdin.read()
    if not text.strip():
        raise SystemExit("No text provided.")
    path = synthesize(text.strip(), args.voice_id, args.output)
    print(f"Saved audio to {path}")


if __name__ == "__main__":
    main()
