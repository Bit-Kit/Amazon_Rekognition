import boto3
import picamera
import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont, ImageDraw, Image

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

bucket='my_bucketrpi'
collectionId='my_collection'

print(' -----------------------------------------------------------')
print('|Ten program porównuje 2 pliki z s3                     >   |')
print('|z lokalnym plikiem "camera.jpg", robionym przez camere >   |')
print('|oraz wyswietla kludke przez oled >                         |')
print('|"Comparing Faces in Images"                                |')
print(' -----------------------------------------------------------')
faceid=''
with canvas(device) as draw:
    draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=1)
    draw.bitmap((0, 0), Image.open('files/closed.png'), fill=0)

def response():
    try:
        threshold = 70
        maxFaces=2
        targetFile='camera.jpg'
        imageTarget=open(targetFile,'rb')
        client=boto3.client('rekognition')
        response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'Bytes': imageTarget.read()},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)
        faceMatches=response['FaceMatches']
        print ('Matching faces')
        
        for match in faceMatches:
                print ('FaceId:' + match['Face']['FaceId'])
                global faceid
                faceid = str(match['Face']['FaceId'])
                #print(faceid)
                print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                similar = str(match['Similarity'])
                #print(similar)      
        if float(similar) > 80:
            
            return True
        else:
            print("Nie znaleziono podobienstwa")
            return False

    except:
        print("Zdjecie nie jest rozpoznawalne")
        return False

def oled():
    with canvas(device) as draw:
        draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=1)
        #draw.text((0, 0), name, fill="white")
        draw.bitmap((0, 0), Image.open('files/open.png'), fill=0)

if __name__ == "__main__":

    try:
        camera = picamera.PiCamera(resolution=(320, 240))
        camera.start_preview(fullscreen=False, window = (400, 5, 320, 240))
        camera.annotate_text_size = 24
        camera.rotation=180
        time.sleep(3)
        camera.capture('camera.jpg',resize=(1280, 800))#1280, 1024 ,800
        camera.annotate_text = "Photo is making"
  
        if response()!= False:
            if(faceid=="9d8f6d87-639b-42aa-a984-e9f0653b120e"):
                print("Hello Olek")
            elif(faceid=="ea5e45ce-4fd3-458c-87db-f44ece523cec"):
                print("Hello Kinga")
            elif(faceid=="5fb97e77-bfd2-4b25-bf14-f8197d3616e3"):
                print("Hello Professor")
            else:
                print("None")
            oled()
                
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
        time.sleep(8)
        #GPIO.cleanup()
        camera.close()
        print("End of program")
