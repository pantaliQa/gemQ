#    conv4gemQ.py is part of gemQ by Luca Franceschini & Luca Carrubba.
#    I's a simple script that help users to convert video files for gemQ.
#    For info: www.gemq.info
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    import os
    import sys
    import shutil
    from subprocess import Popen,PIPE
    import platform
    import getopt
except:
    print "ERROR: You need os, sys, shutil, subprocess, platform and getopt Python Libraries"

def listfiles(argv):
    in_path = 0
    out_path = 0
    ratio = 0
    try:
        opts, args = getopt.getopt(argv, "hi:o:s:", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if not opts:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i"):
            rootdir = arg
            in_path = os.path.abspath(arg)
            if not os.path.isdir(in_path):
                print "Input directory is not valid"
                print ""
                usage()
                sys.exit()
        elif opt in ("-o"):
            out_path = os.path.abspath(arg)
        elif opt in ("-s"):
            ratio = arg
    if not in_path or not out_path:
        usage()
        sys.exit()
    checksys = platform.system()
    ffmpeg = "ffmpeg"
    if checksys == "Windows":
        ffmpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../patches/gui/mediagrid/ffmpeg.exe")
    elif checksys == "Darwin":
        ffmpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../patches/gui/mediagrid/ffmpeg")
    tot_dir = 0
    tot_video = 0
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        print 'dir create: %s' % out_path
        tot_dir = tot_dir + 1
    for root, subFolders, files in os.walk(in_path):
        for cartella in subFolders:
            rel_path = os.path.join(out_path,os.path.relpath(os.path.join(root,cartella),in_path))
            if not os.path.isdir(rel_path):
                os.mkdir(rel_path)
                print 'dir create: %s' % rel_path
                tot_dir = tot_dir + 1
    for root, subFolders, files in os.walk(in_path):
        for file in files:
            filename = os.path.join(root,file)
            if file_type(filename):
                convertfile(filename, in_path, out_path, ratio, ffmpeg)
                tot_video = tot_video + 1
    print ""
    print "%d dir created and %d videos converted." % (tot_dir, tot_video)

#this function return 1 if is a video file
def file_type(filename):
    import mimetypes
    type = mimetypes.guess_type(filename)[0]
    if type is None:
        return 0
    type = type.split("/")[0]
    if type == "video":
        return 1
    return 0

#convert the file
def convertfile(filename, in_path, out_path, ratio, ffmpeg):
    newfile = "%s%s" % (os.path.splitext(os.path.relpath(filename,in_path))[0], ".mov")
    newfile2 = os.path.join(out_path, newfile)
    print '%s -> %s' % (filename, newfile2)
    if ratio:
        try:
            p = Popen([ffmpeg, "-i", filename, "-an", "-sameq", "-vcodec", "mjpeg", "-f", "mov", "-y", "-s", ratio, newfile2], stdout=PIPE, stderr=PIPE)
            p.wait()
            if (p.returncode == 1):
                print "Error on FFMPEG thumb creation"
        except:
            print "No FFMPEG library?"
    else:
        try:
            p = Popen([ffmpeg, "-i", filename, "-an", "-sameq", "-vcodec", "mjpeg", "-f", "mov", "-y", newfile2], stdout=PIPE, stderr=PIPE)
            p.wait()
            if (p.returncode == 1):
                print "Error on FFMPEG thumb creation"
        except:
            print "No FFMPEG library?"
    return

def usage():
    print "Usage: python %s [-s size] [-i input_directory] [-o output_directory]" % sys.argv[0]
    print ""
    print "Useful infos:"
    print "[-s size] is an aspect ratio like 800x600 and is OPTIONAL."
    print "[-i input_directory] must be a valid directory that contains video files (the script copy all videos recursively). This arg is NEEDED."
    print "[-o output_directory] is the location when the files .mov are generated. If this directory don't exist the script create it. This arg is NEEDED."
    print ""
    print "Example:"
    print "python %s -s 320x240 -i /video/clips -o /video/newclips" % sys.argv[0]
    print "Convert all files in /video/clips to .mov format and copy those in a new directory, set aspect ratio to 320x240."
    return

if __name__ == '__main__':
    listfiles(sys.argv[1:])
