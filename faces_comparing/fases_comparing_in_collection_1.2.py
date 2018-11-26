#Źródło:https://docs.aws.amazon.com/rekognition/latest/dg/search-face-with-image-procedure.html
import boto3
import picamera
import time
import RPi.GPIO as GPIO

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont, ImageDraw, Image

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

bucket='my_bucketrpi'
collectionId='my_collection'

led=4
button=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN)
GPIO.output(led, GPIO.LOW)

print(' -----------------------------------------------------------')
print('|Ten program porównuje kolekcje zdjęć z >                   |')
print('|z lokalnym plikiem "camera.jpg", robionym przez camere >   |')
print('|oraz wyswietla kludke przez oled >                         |')
print('|jest używany Button i timer >                              |')
print('|"Searching for a Face Using an Image"                      |')
print(' -----------------------------------------------------------')
faceid=''
with canvas(device) as draw:
    draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=1)
    draw.bitmap((0, 0), Image.open('files/closed.png'), fill=0)

def button_put():
    camera.annotate_text = "Wait for click button"
    while True:

        if GPIO.input(button) == False:
            GPIO.output(led, GPIO.HIGH)
            camera.annotate_text = "Photo is making"
            return
        else:
            GPIO.output(led, GPIO.LOW)
    
    
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
        button_put() 
        print("Zdjęcie zrobione, wysyłam komunikat...")
        start_time = time.time()
        if response()!= False:
            if(faceid=="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxx1"):
                print("Hello User1")
            elif(faceid=="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxx2"):
                print("Hello User2")
            elif(faceid=="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxx3"):
                print("Hello User3")
            else:
                print("None")
            print("To trwalo: ", round(time.time() - start_time,2), "seconds.")
            oled()
                
        else:
            print("Photo is not recognise.")

    except KeyboardInterrupt:
        print("Exit pressed Ctrl+C")
        camera.close()
        GPIO.cleanup()
        
    except:
        print('Error')
        camera.close()
        GPIO.cleanup()
        
    finally:
        time.sleep(8)
        GPIO.cleanup()
        camera.close()
        print("End of program")
