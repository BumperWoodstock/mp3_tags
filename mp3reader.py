# !/usr/bin/python

#a quick and dirty script to walk through a directory structure and extract mps tags from files

from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import os
import sys
import hashlib
import string
import time
#from pathlib import Path

tags = ["song","artist","album","genre","filePath"]



def walk_error_handler(exception_instance):
    print("Uh-Oh, os.walk error")

def do_initial_scan_for_mp3s(dirstr):#just do a count of the mp3 files in the directory structure
    
    print("Scanning the target Directory Structure for .mp3 files")
    count = 0
    for root,dirs, files in os.walk(dirstr,onerror=walk_error_handler):
        for name in files:
            #if (Path(name).suffix == ".mp3"):
            if name[len(name)-4:] == ".mp3":
                count = count+1
    print("Total mp3 files found = "+str(count))
    return count

def write_mp3_tags(fout,targetdir):
    
    total_number_of_mp3 = do_initial_scan_for_mp3s(targetdir)
    current_time = time.time()
    count = 0
    
    print("Writing out mp3 tags now")

    f = open(fout,"w+")
    f_errors = open(fout+".err","w+")
    f.write('|'.join(tags)+"\n")

    for root,dirs, files in os.walk(targetdir,topdown=False):
        for name in files:
            try:
                mp3 = MP3File(os.path.join(root,name))
            except:
                continue
            data = []
            for tag in tags:
                if tag != "filePath":
                    try:
                        data.append(mp3.get_tags()['ID3TagV1'][tag])
                    except:
                        data.append('Not Assigned')
            data.append(os.path.join(root,name))
            try:
                f.write('|'.join(data)+"\n")
            except:
                f_errors.write(os.path.join(root,name) + "\n")
            count = count+1
            if time.time() - current_time > 120:
                print("Successfully read "+str(count) + " out of " + str(total_number_of_mp3) )
                current_time = time.time()

    f.close()

def hashfile(path,blocksize = 65536):
    afile = open(path,'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.haxidigest()

def identify_dup_mp3(dirstr):
    dupmp3 = {}
    for root,dirs, files in os.walk(dirstr,onerror=walk_error_handler):
        for name in files:
            if name[len(name)-4:] == ".mp3":
                file_hash = hashfile(os.path.join(root,name))
                if file_hash in dupmp3:
                    dupmp3[file_hash] = dupmp3[file_hash] + os.path.join(root,name)
                else:
                    dupmp3[file_hash] = os.path.join(root,name)
    return dupmp3

def print_dup_mp3(dups_dict):
    results = list(filter(lambda x: len(x) > 1,dups_dict.values()))
    if len(results) > 0:
        print("Dups Found")
        print("Following are dups")
        print("---------------------")
        for result in results:
            for subresult in result:
                print('\t\s%s' % subresult)
            print("---------------------")
    else:
        print('No Dups Found')
              
    print("Total mp3 files found = "+str(count))
    return count
    

if __name__ == '__main__':
    #    main()
    print("Here we go")
    if sys.argv[1] == "Scan":
        print("scanning now")
        file_count = do_initial_scan_for_mp3s(sys.argv[2])
    elif len(sys.argv) < 2:
        print("Insuficient arguments")
        exit
    else:
        write_mp3_tags(sys.argv[1],sys.argv[2])
