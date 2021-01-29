import os
import cv2 as cv
from fastapi import FastAPI, UploadFile, File
import uvicorn
from fastapi.encoders import jsonable_encoder

def rescaleFrame(frame,scale):
    width=int(frame.shape[1] * scale)  #frame.shape[1] is width of frame
    height=int(frame.shape[0] * scale)  #frame.shape[0] is height of frame

    dimension = (width,height)
    return cv.resize(frame,dimension,interpolation=cv.INTER_AREA)


app=FastAPI()
@app.post("/resize_image/{scale_percent}")
async def image(*,scale_percent:int,image:UploadFile=File(...)):
    print(image.file)
    print(scale_percent)
    try:
        os.mkdir("images")
        print(os.getcwd())
    except Exception as e:
        print(e)
    file_name=os.getcwd()+"/images/"+image.filename.replace(" ","-")

    with open(file_name,'wb+') as f:
        f.write(image.file.read())
        f.close()
    
    img = cv.imread(file_name)
    scale_percent=scale_percent/100
    print("scale_percent::",scale_percent)
    resized=rescaleFrame(img,scale_percent)
    file_name1=os.getcwd()+"/images/"+"resized_"+image.filename.replace(" ","-")
    cv.imwrite(file_name1,resized)

    file=jsonable_encoder({"imagePath":file_name1})
    return file

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)