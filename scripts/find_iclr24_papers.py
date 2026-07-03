#!/usr/bin/env python3
import openreview

client = openreview.api.OpenReviewClient(baseurl='https://api2.openreview.net')
print("Fetching ICLR 2024 submissions...")

# Just fetch the first 1000 submissions to find our candidates
submissions = client.get_notes(invitation='ICLR.cc/2024/Conference/-/Submission', limit=100)
print(f"Fetched {len(submissions)} submissions.")

for note in submissions:
    # get reviews
    reviews = client.get_notes(forum=note.id, invitation='ICLR.cc/2024/Conference/-/Official_Review')
    if not reviews:
        continue
    
    ratings = []
    for r in reviews:
        try:
            val = r.content['rating']['value']
            # usually like "8: accept, good paper" -> extract 8
            score = int(str(val).split(':')[0].strip())
            ratings.append(score)
        except:
            pass
            
    if ratings:
        avg = sum(ratings) / len(ratings)
        print(f"Forum: {note.id} | Avg: {avg:.2f} | Ratings: {ratings} | Title: {note.content.get('title',{}).get('value','')}")
