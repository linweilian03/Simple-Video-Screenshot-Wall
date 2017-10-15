#coding=utf-8
import os,re,sys,fnmatch

def all_files(root,patterns='*',single_level=False,yield_folders=False):
    patterns = patterns.split(';')
    for path,subdirs,files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path,name)
                    break
                if single_level:
                    break

def get_time(path):
    otime=os.popen("ffmpeg -i '" +path+ "' 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//")
    ortime=otime.read()
    h,m,s=ortime.strip().split(":")
    return int(h) * 60 + int(m) 

yourpath='path'
for path in all_files(yourpath,'*.mkv;*.mp4;*.avi;*.wmv;*.flv'):
    jpgpath=path[:-3]
    if not os.path.exists(jpgpath[:-1]+"-ss.jpg"):
        maxtime=get_time(path)
    
        for t in range(5,maxtime+1,5):
            os.system("ffmpeg -ss "+str(t*60)+" -i '" +path+ "' -y '"+jpgpath+str(t).zfill(3)+".jpg'")
        
        os.system("montage '"+jpgpath+"'*'.jpg' -tile 4x  -geometry 300x '"+jpgpath[:-1]+"-ss.jpg'")
        os.system("rm '"+jpgpath+"'???'.jpg'")
