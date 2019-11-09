# !/usr/bin/python

#a script to read in filepath and tags from a csv
# for each file, calc a hash and drop is into a new directory while updating tags and filename.
# keep a hash dictionary, if there is a dup file, do not copy it.

from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import os
import sys
import hashlib
import string
import time
import shutil

librarypath = '/mnt/PiNAS/music/library'
metadata = '/mnt/PiNAS/GIT/pythonprojects/mp3_tags-master/mp3_meta_data.csv' 
tags = ["song","artist","album","genre","track"]

def read_meta_data(metadata):
    tracks = []
    fin = open(metadata, 'r')
    
    for line in fin:
        tracks.append( line.strip().split("|"))
    #['Done', 'song', 'artist', 'album', 'genre', 'track', 'filePath', 'FileName']  
    return tracks 

def hashfile(path,blocksize = 65536):
    afile = open(path,'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()       
 
if __name__ == '__main__':
    #    main()
    print("Here we go")
    hashes = {} #a list of hashes from all the files checked so far.
    for track in read_meta_data(metadata):
        #print(track[6])
        if track[0] == 'x': #meta data file contains an 'x' where we want to keep this file
            #track[6] = full file path
            if track[6][len(track[6])-4:] == ".mp3": # and it is an .mp3 file
                file_hash = hashfile(track[6]) #hash the file
                if file_hash not in hashes: #check to see whether we have already handled a file with the same hash (i.e. a dup)
                    hashes[file_hash] = track[6]
                    new_track_name = librarypath + '/%s %s %s %s.mp3' % (track[3].strip(), track[5].strip(),track[2].strip(),track[1].strip())
                    if not os.path.exists(new_track_name): #if true then we have already go this song, perhaps a different version?
                        shutil.copy2(track[6], new_track_name)
                        mp3 = MP3File(new_track_name)
                        mp3.set_version(VERSION_2)
                        mp3.song = track[1]
                        mp3.artist = track[2]
                        mp3.album = track[3]
                        mp3.genre = track[4]
                        mp3.save()

                
        