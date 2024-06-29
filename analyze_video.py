import cv2
from deepface import DeepFace
import exiftool
import hashlib
import os
import json

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    results = []
    for i in range(frame_count):
        ret, frame = cap.read()
        if ret:
            analysis = DeepFace.analyze(frame, actions=['age', 'emotion'])
            results.append(analysis)
    cap.release()
    return results

def extract_metadata(video_path):
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(video_path)
    return metadata

def generate_hash(video_path):
    BUF_SIZE = 65536
    md5 = hashlib.md5()
    with open(video_path, 'rb') as f:
        while chunk := f.read(BUF_SIZE):
            md5.update(chunk)
    return md5.hexdigest()

def document_video(video_path, analysis_results, metadata, output_dir):
    documentation = {
        "video_path": video_path,
        "analysis_results": analysis_results,
        "metadata": metadata
    }
    doc_path = os.path.join(output_dir, os.path.basename(video_path) + '.json')
    with open(doc_path, 'w') as doc_file:
        json.dump(documentation, doc_file)

if __name__ == "__main__":
    import sys
    video_path = sys.argv[1]
    output_dir = sys.argv[2]
    analysis_results = analyze_video(video_path)
    metadata = extract_metadata(video_path)
    document_video(video_path, analysis_results, metadata, output_dir)
