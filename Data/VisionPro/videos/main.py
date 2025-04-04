import pysrt
import json
import os

def srt_to_dict(srt_file):
    """Convert a single SRT file to a dictionary format."""
    subs = pysrt.open(srt_file)
    subtitles = []

    for sub in subs:
        subtitles.append({
            "start": str(sub.start),
            "end": str(sub.end),
            "text": sub.text.replace("\n", " ")  # Remove newlines for clean JSON
        })
    
    return subtitles

def batch_convert_srt_to_single_json(input_folder, output_json):
    """Convert all SRT files in a folder into a single JSON file."""
    all_subtitles = {}

    srt_files = [f for f in os.listdir(input_folder) if f.endswith(".srt")]
    
    if not srt_files:
        print("❌ No SRT files found in the folder.")
        return
    
    for srt_file in srt_files:
        srt_path = os.path.join(input_folder, srt_file)
        all_subtitles[srt_file] = srt_to_dict(srt_path)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_subtitles, f, indent=4, ensure_ascii=False)
    
    print(f"✅ All subtitles saved in: {output_json}")

# Example Usage
input_folder = "./"  # Change this to your SRT folder path
output_json = "combined_subtitles.json"  # Final output JSON file

batch_convert_srt_to_single_json(input_folder, output_json)
