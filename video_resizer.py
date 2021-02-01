# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
from fastapi import FastAPI, UploadFile, File
import uvicorn
from fastapi.encoders import jsonable_encoder
'''
def rescaleFrame(frame,scale=0.5):
    width=int(frame.shape[1] * scale)  #frame.shape[1] is width of frame
    height=int(frame.shape[0] * scale)  #frame.shape[0] is height of frame

    dimension = (width,height)
    return cv2.resize(frame,dimension,interpolation=cv2.INTER_AREA)
'''

app=FastAPI()
@app.post("/resize_video/{scale_percent}")
async def image(*,scale_percent:int,video:UploadFile=File(...)):
    print(video.file)
    print(scale_percent)
    try:
        os.mkdir("videos")
        print(os.getcwd())
    except Exception as e:
        print(e)
    file_name=os.getcwd()+"/videos/"+video.filename.replace(" ","-")
    with open(file_name,'wb+') as f:
        f.write(video.file.read())
        f.close()
    
    capture=cv2.VideoCapture(file_name)

    # initialize the FourCC, video writer, dimensions of the frame, and
    # zeros array
    file_name1=os.getcwd()+"/videos/"+"resized_"+video.filename.replace(" ","-")
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    writer = None
    (h, w) = (None, None)

    # loop over frames from the video stream
    while True:
        # grab the frame from the video stream and resize it to have a
        # maximum width of 300 pixels
        isTrue,frame = capture.read()
        #frame=rescaleFrame(frame)
        frame = imutils.resize(frame, width=scale_percent)
        # check if the writer is None
        if writer is None:
            # store the image dimensions, initialize the video writer,
            # and construct the zeros array
            (h, w) = frame.shape[:2]
            writer = cv2.VideoWriter(file_name1, fourcc, 20 ,(w , h ), True)
            
        # construct the final output frame, storing the original frame
        output = np.zeros((h , w , 3), dtype="uint8")
        output[0:h,0:w] = frame
        
        #write the output frame to file
        writer.write(output)

        
    # do a bit of cleanup
    print("[INFO] cleaning up...")
    cv2.destroyAllWindows()
    capture.release()
    writer.release()

    file=jsonable_encoder({"imagePath":file_name1})
    return file

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)