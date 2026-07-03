#!/usr/bin/env python3
"""
Fetch 10 specific ICLR 2024 papers from OpenReview.net to build the Ground Truth dataset for the Eval Harness.
Requires: pip install openreview-py
"""
import os
import json
import argparse
try:
    import openreview
except ImportError:
    print("Error: openreview-py is not installed. Run 'pip install openreview-py'")
    exit(1)

# Hand-picked ICLR 2024 forum IDs representing the 10 target distribution categories.
# Note: These are illustrative IDs; in a real run, we would map exact known IDs.
TARGET_PAPERS = {
    # 2 Clear Accepts (Oral/Spotlight)
    "accept_1": "B1G5B10O1F", # Example: LLaMA-style architecture paper
    "accept_2": "V1X3B98R2M", # Example: High-scoring Vision Transformer
    
    # 4 Borderlines (2 ultimately accepted, 2 rejected)
    "border_acc_1": "H8V2L44K1P",
    "border_acc_2": "C2X5B19O1R",
    "border_rej_1": "J5G9B33O1X",
    "border_rej_2": "P1X4B77R2N",
    
    # 2 Clear Rejects
    "reject_1": "M3X2B11O1A",
    "reject_2": "K9V8B22R2B",
    
    # 2 Out of Scope / Pure Theory (To test Scope Guard)
    "out_scope_1": "T1V5B33O1C", # Example: Pure optimization math bound
    "out_scope_2": "Z2X1B44R2D"  # Example: HCI user study on LLM interfaces
}

def fetch_data(output_dir):
    print("Connecting to OpenReview API (Guest mode)...")
    client = openreview.api.OpenReviewClient(baseurl='https://api2.openreview.net')
    
    os.makedirs(output_dir, exist_ok=True)
    
    dataset = {}
    
    for category, forum_id in TARGET_PAPERS.items():
        print(f"Fetching {category} (Forum: {forum_id})...")
        try:
            # 1. Get the main submission note
            note = client.get_note(forum_id)
            title = note.content.get('title', {}).get('value', 'Unknown Title')
            pdf_url = f"https://openreview.net/pdf?id={forum_id}"
            
            # 2. Get all official reviews (blind)
            reviews = client.get_notes(forum=forum_id, invitation='ICLR.cc/2024/Conference/-/Official_Review')
            
            extracted_reviews = []
            for r in reviews:
                extracted_reviews.append({
                    'id': r.id,
                    'rating': r.content.get('rating', {}).get('value', 'N/A'),
                    'confidence': r.content.get('confidence', {}).get('value', 'N/A'),
                    'summary': r.content.get('summary', {}).get('value', ''),
                    'strengths': r.content.get('strengths', {}).get('value', ''),
                    'weaknesses': r.content.get('weaknesses', {}).get('value', ''),
                    'questions': r.content.get('questions', {}).get('value', '')
                })
                
            dataset[category] = {
                'forum_id': forum_id,
                'title': title,
                'pdf_url': pdf_url,
                'abstract': note.content.get('abstract', {}).get('value', ''),
                'reviews': extracted_reviews
            }
            print(f"  -> Found {len(extracted_reviews)} reviews for '{title[:30]}...'")
            
        except Exception as e:
            print(f"  -> Error fetching {forum_id}: {e}")
            
    # Save the dataset
    out_file = os.path.join(output_dir, "ground_truth_dataset.json")
    with open(out_file, 'w') as f:
        json.dump(dataset, f, indent=2)
        
    print(f"\nSaved Ground Truth dataset to {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch ICLR 2024 evaluation dataset")
    parser.add_argument("--out", default="data/eval_dataset", help="Output directory")
    args = parser.parse_args()
    fetch_data(args.out)
