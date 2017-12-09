from __future__ import print_function
import sys
import skytracker

video_file = sys.argv[1]
blob_data_file = sys.argv[2]

blob_data = skytracker.load_blob_data(blob_data_file)

matcher = skytracker.BlobMatcher()
match_list = matcher.run(blob_data)

stitcher = skytracker.BlobStitcher()
track_list = stitcher.run(match_list)

output_basename = blob_data_file.split('/')[-1].split('_')[3]
output_file = output_basename+'_tracks.txt'

videoCreator = skytracker.TrackVideoCreator(video_file, track_list)
videoCreator.run()
