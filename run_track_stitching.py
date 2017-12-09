from __future__ import print_function
import sys
import skytracker
import matplotlib.pyplot as plt
import cPickle  
import json

blob_data_file = sys.argv[1]

blob_data = skytracker.load_blob_data(blob_data_file)

# Get list of matched blob pairs based on distance
matcher = skytracker.BlobMatcher()
match_list = matcher.run(blob_data)

# Stitch together matched paris into tracks
stitcher = skytracker.BlobStitcher()
track_list = stitcher.run(match_list)


output_basename = blob_data_file.split('/')[-1].split('_')[3]
output_file = output_basename+'_tracks.txt'

track_id = 0

with open(output_file,'w') as fid:

    for track in track_list:
    
        x_vals = [item['blob']['centroid_x'] for item in track]
        y_vals = [item['blob']['centroid_y'] for item in track]

        blobs = [item['blob'] for item in track]
        frames = [item['frame'] for item in track]

        track_data = {'track_id':track_id, 'frames': frames, 'blobs': blobs} 
        track_data_json = json.dumps(track_data)
        fid.write('{0}\n'.format(track_data_json))

        track_id += 1
    
        print('x_vals: {0}'.format(x_vals))
        print('y_vals: {0}'.format(y_vals))
        print()
    
        plt.plot(x_vals, y_vals,'.-')
    
    plt.show()


if 0:
    videoCreator = skytracker.TrackVideoCreator(video_file, track_list)
    videoCreator.run()
