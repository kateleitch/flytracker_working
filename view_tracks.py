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

#filter tracks by removing uncharacteristcally large jumps
track_list, change_flag_list, debug_track_list = skytracker.filter_outlying_segments(track_list,
                                                                                    multiplier=3,
                                                                                    use_mad=False,
                                                                                    use_std = False,
                                                                                    angle_diff = 70, #in degrees
                                                                                    filter_floor_pix=50)


track_list = skytracker.join_tracks(track_list, gap_multiplier =0.25, max_tracks_to_join = 4)

output_basename = blob_data_file.split('/')[-1].split('_')[3]
output_file = output_basename+'_tracks.txt'

videoCreator = skytracker.TrackVideoCreator(video_file, track_list)
videoCreator.run()
