from __future__ import print_function
import sys
import skytracker
import matplotlib.pyplot as plt
import cPickle
import json

blob_data_file = sys.argv[1]
path_to_output_directory = sys.argv[2]
video_file = sys.argv[3]
track_metadata_filename = sys.argv[4] # make an empty text file and then provide the path here
existing_track_metadata_json = sys.argv[5] #either specify the path to the existing metadata file, or provide the string 'False'

blob_data = skytracker.load_blob_data(blob_data_file)

# Get list of matched blob pairs based on distance
matcher = skytracker.BlobMatcher()
match_list = matcher.run(blob_data)

# Stitch together matched parts into tracks
stitcher = skytracker.BlobStitcher()
track_list = stitcher.run(match_list)

#"filter" tracks by removing uncharacteristcally large jumps
track_list, change_flag_list, debug_track_list = skytracker.filter_outlying_segments(track_list,
                                                                                    multiplier=3, # <---- was 3
                                                                                    use_mad=False,
                                                                                    use_std = False,
                                                                                    angle_diff = 70, #in degrees
                                                                                    filter_floor_pix=50)
# splice tracks separated by x frames
track_list = skytracker.join_tracks(track_list, gap_multiplier =0.25, max_tracks_to_join = 4) #larger gap multiplier -> more permissive joining

output_basename = blob_data_file.split('/')[-1].split('.')[0]#.split('_')[3]
output_file = path_to_output_directory + '/'+'stitched_tracks_'+output_basename+'.txt'

track_id = 0

with open(output_file,'w') as fid:

    for track in track_list:

        x_vals = [item['blob']['centroid_x'] for item in track]
        y_vals = [item['blob']['centroid_y'] for item in track]

        blobs = [item['blob'] for item in track]
        frames = [item['frame'] for item in track]

        track_data = {'track_id':track_id, 'frame': frames, 'blobs': blobs}
        track_data_json = json.dumps(track_data)
        fid.write('{0}\n'.format(track_data_json))

        track_id += 1

        print('x_vals: {0}'.format(x_vals))
        print('y_vals: {0}'.format(y_vals))
        print()

        plt.plot(x_vals, y_vals,'.-')

    plt.show()


# if 0: # kate commented out 2019_05_21
# videoCreator = skytracker.TrackVideoCreator(video_file, track_list)
# videoCreator.run()


videoCreator = skytracker.TrackVideoCreator(video_file, track_list, track_metadata_filename, existing_track_metadata_json)
videoCreator.run()
