from __future__ import print_function
import sys
import skytracker
import json
import matplotlib.pyplot as plt
import time

video_file = sys.argv[1]
blob_data_file = sys.argv[2]
shall_we_perform_ground_truthing = sys.argv[3] # a boolean
existing_track_metadata_json = sys.argv[4] #

perform_stitching = True
if blob_data_file.split('_')[0] == 'stitched':
	print ('skippin stitching')
	perform_stitching = False

blob_data = skytracker.load_blob_data(blob_data_file)

if perform_stitching:
	matcher = skytracker.BlobMatcher()
	match_list = matcher.run(blob_data)

	stitcher = skytracker.BlobStitcher()
	track_list = stitcher.run(match_list)

	#filter tracks by removing uncharacteristcally large jumps
	track_list, change_flag_list, debug_track_list = skytracker.filter_outlying_segments(track_list,
	                                                                                    multiplier=3,
	                                                                                    use_mad=False,
	                                                                                    use_std = False,
	                                                                                    angle_diff = 80, #in degrees
	                                                                                    filter_floor_pix=50)


	track_list = skytracker.join_tracks(track_list, gap_multiplier =0.25, max_tracks_to_join = 4) #larger gap multiplier -> more permissive joining
	t = time.strftime("%Y%m%d_%H%M%S", time.localtime())
	output_basename = blob_data_file.split('/')[-1].split('_')[3] + '_' + blob_data_file.split('/')[-1].split('_')[4]

	output_track_list_name = 'tracks_'+output_basename+'_'+t+'.txt'

	with open(output_track_list_name,'w') as fid:

	    for track_id, track in enumerate(track_list):

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

t = time.strftime("%Y%m%d_%H%M%S", time.localtime())
metadata_filename = 'metadata_'+output_basename+'_'+t+'.txt'
videoCreator = skytracker.TrackVideoCreator(video_file, track_list, shall_we_perform_ground_truthing, metadata_filename, existing_track_metadata_json)
videoCreator.run()
