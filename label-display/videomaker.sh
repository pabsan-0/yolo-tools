#! /usr/bin/bash

#
# This script takes a folder with many .jpg files and concatenates
# them into a mp4 video using gstreamer
#
# Because the gstreamer plugin we will use loops only over
# integer-sequenced filenames, we'll just create a folder of symlinks
# to the actual target images
#


# The concatenating pipeline, once all symlinks have been created
gst-launch-1.0 -e multifilesrc location="%09d.jpg" index=1 caps="image/jpeg,framerate=(fraction)24/1,width=1280,height=1280" \
    ! jpegdec ! videoconvert  ! videoscale ! video/x-raw,width=1280,height=1280  !  queue ! x264enc ! queue ! mp4mux         \
    ! filesink location=../out.mp4

