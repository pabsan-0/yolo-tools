IM_W=640
COLLAGE_H=640

gst-launch-1.0                                                   \
    videomixer name=mix  background=0                            \
            sink_0::xpos=0   sink_0::ypos=0   sink_0::alpha=0.8  \
            sink_1::xpos=0   sink_1::ypos=0   sink_1::alpha=0.8  \
        ! videoscale                                             \
        ! "video/x-raw,height=$COLLAGE_H"                        \
        ! ximagesink                                             \
    filesrc location="out_labelled.mp4"  ! qtdemux ! queue ! h264parse ! avdec_h264 ! videoscale ! "video/x-raw,width=$IM_W" ! mix. \
    filesrc location="out_originals.mp4" ! qtdemux ! queue ! h264parse ! avdec_h264 ! videoscale ! "video/x-raw,width=$IM_W" ! mix. ;