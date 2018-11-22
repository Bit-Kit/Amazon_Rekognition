#Źródło:"https://docs.aws.amazon.com/rekognition/latest/dg/faces-comparefaces.html"
import boto3
import picamera
import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont, ImageDraw, Image

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)
file_data = open("files/data.txt", "r")

for line in file_data:
    a = line.split('\"')
    if a[1]=="bucket":
        bucket = a[3]
    elif a[1]=="sourceFile_1":
        sourceFile_1 = a[3]
    elif a[1]=="sourceFile_2":
        sourceFile_2 = a[3]
    elif a[1]=="sourceFile_3":
        sourceFile_3 = a[3]
        
#bucket =''
#sourceFile_1 =''
#sourceFile_2 =''
#sourceFile_3 =''

print(' -----------------------------------------------------------')
print('|Ten program porównuje 3 pliki z s3                     >   |')
print('|z lokalnym plikiem "camera.jpg", robionym przez camere >   |')
print('|oraz wyswietla kludke przez oled >                         |')
print('|"Comparing Faces in Images"                                |')
print(' -----------------------------------------------------------')
with canvas(device) as draw:
    draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=1)
    draw.bitmap((0, 0), Image.open('files/closed.png'), fill=0)

def response_person_1():
    try:
        targetFile='camera.jpg'
        client=boto3.client('rekognition')
        imageTarget=open(targetFile,'rb')
        response=client.compare_faces(SimilarityThreshold=70,
                                        SourceImage={'S3Object':{'Bucket':bucket,'Name':sourceFile_1}},
                                        TargetImage={'Bytes': imageTarget.read()})
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            confidence = str(faceMatch['Face']['Confidence'])
            print('The face at ' +
                    str(position['Left']) + ' ' +
                    str(position['Top']) +
                    ' matches with ' + confidence + '% confidence')
            if confidence and float(confidence)>=80:
                return True
            else:
                return False
    except:
        print("Zdjecie nie jest rozpoznawalne")
        return False

def response_person_2():
    try:
        targetFile='camera.jpg'
        client=boto3.client('rekognition')
        imageTarget=open(targetFile,'rb')
        response=client.compare_faces(SimilarityThreshold=70,
                                        SourceImage={'S3Object':{'Bucket':bucket,'Name':sourceFile_2}},
                                        TargetImage={'Bytes': imageTarget.read()})        
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            confidence = str(faceMatch['Face']['Confidence'])
            print('The face at ' +
                    str(position['Left']) + ' ' +
                    str(position['Top']) +
                    ' matches with ' + confidence + '% confidence')
            if confidence and float(confidence)>=80:
                return True
            else:
                return False
    except:
        print("Zdjecie nie jest rozpoznawalne")
        return False

def response_person_3():
    try:
        targetFile='camera.jpg'
        client=boto3.client('rekognition')
        imageTarget=open(targetFile,'rb')
        response=client.compare_faces(SimilarityThreshold=70,
                                        SourceImage={'S3Object':{'Bucket':bucket,'Name':sourceFile_3}},
                                        TargetImage={'Bytes': imageTarget.read()})        
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            confidence = str(faceMatch['Face']['Confidence'])
            print('The face at ' +
                    str(position['Left']) + ' ' +
                    str(position['Top']) +
                    ' matches with ' + confidence + '% confidence')
            if confidence and float(confidence)>=80:
                return True
            else:
                return False
    except:
        print("Zdjecie nie jest rozpoznawalne")
        return False
            
def oled(name):
    with canvas(device) as draw:
        draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=1)
        draw.text((0, 0), name, fill="white")
        draw.bitmap((0, 0), Image.open('files/open.png'), fill=0)

if __name__ == "__main__":

    try:
        camera = picamera.PiCamera(resolution=(320, 240))
        camera.start_preview(fullscreen=False, window = (400, 5, 320, 240))
        camera.annotate_text_size = 24
        camera.rotation=180
        time.sleep(2)
        camera.capture('camera.jpg',resize=(1280, 800))#1280, 1024 ,800
        camera.annotate_text = "Photo is making"
  
        if response_person_1()== True:
            print("Hello Person_1!")
            oled("Person1")
            
        elif response_person_2()== True: 
            print("Hello Person_2!")
            oled("Person2")
        elif response_person_3()== True:
            print("Hello Person_3!")
            oled("Person3")
                
        else:
            print("Photo is not recognise.")

    except KeyboardInterrupt:
        print("Exit pressed Ctrl+C")
        camera.close()
        #GPIO.cleanup()
        
    except:
        print('Error')
        camera.close()
        #GPIO.cleanup()
        
    finally:
        time.sleep(5)
        #GPIO.cleanup()
        camera.close()
        print("End of program")
