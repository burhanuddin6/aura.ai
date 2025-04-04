import json
import os

def merge_json_files(json_files, output_file="merged.json"):
    merged_data = {}

    for json_file in json_files:
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                key = os.path.splitext(os.path.basename(json_file))[0]  # Remove extension
                merged_data[key] = data
        else:
            print(f"Warning: {json_file} not found.")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4)

    print(f"Merged JSON saved to {output_file}")

# Example usage
json_files = ["Docementations/visionos_docs.json", "Reddit posts/reddit_comments.json", "videos/combined_subtitles.json"]
merge_json_files(json_files)
