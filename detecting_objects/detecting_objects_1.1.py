#Źródło:"https://docs.aws.amazon.com/rekognition/latest/dg/images-bytes.html"

#Biblioteka Boto to pakiet programistyczny zaprojektowany w celu poprawy wykorzystania języka programowania Python w Amazon Web Services.
import boto3
#Importowanie sprzętowej biblioteki kamery RPi 
import picamera
#Importowanie sprzętowych bibliotek OLED wyswietlacza
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
#Importowanie bibliotek dla pracy z zatrzymaniami i wiliczenia czasu
import time
#Importowanie sprzętowej biblioteki I/O RPi
import RPi.GPIO as GPIO

def button_put():
    camera.annotate_text = "Wait for click button"
    while True:
        
        if GPIO.input(button) == False:
            GPIO.output(led, GPIO.HIGH)
            camera.annotate_text = "button is clicked"
            return
        else:
            GPIO.output(led, GPIO.LOW) 
    
def print_lcd(text1,text2):
    with canvas(device) as draw:
        draw.rectangle((0, 0, 127, 14), outline="white", fill="black")
        draw.text((0, 0), text1, fill="white")
        draw.text((0, 18), text2, fill="white")
        
#Metoda wyswietlania JSONa na wyswietlaczu        
def end_lcd():
    j=0
    with canvas(device) as draw:
        x=3
        draw.rectangle((0, 0, 127, 14), outline="white", fill="black")
        draw.text((0, x), " ANSWER FROM AWS:    ", fill="white")
        for i in range(len(list1[0])):
            text = str(list1[0][j])  + ' : ' + str(round(list1[1][j], 5)) #okraglenie do "5"
            x=x+14
            draw.text((0, x), text, fill="white")
            j = j+1
            
#Ustalenie parametrów pracy szyny I2C
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

led=4
button=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN)
GPIO.output(led, GPIO.LOW)
print_lcd(" Start...","")
print(' -------------------------------------------------')
print('|Ten program tworzy zdjecie o nazwie "fresh.jpg" >|')
print('|wysyla do serwera Rekognition >                  |')
print('|wyswietla wynik na wyswietlaczu >                |')
print('|tworzy preview                                   |')
print('|używa Button                                     |')
print('|liczy czas pracy                                 |')
print('|Ver 1.1                                          |')
print(' -------------------------------------------------')
#Ustalenie parametrow kamery RPi
try:
    camera = picamera.PiCamera(resolution=(320, 240)) # 800, 480
    #camera.start_preview()
    camera.start_preview(fullscreen=False, window = (400, 5, 320, 240))
    camera.annotate_text_size = 24
    camera.rotation=180
    camera.annotate_text = "Starting..."
    button_put()
    
    #Tworzenie listy do zapisywania wynikow
    list1 = [[],[]]

    #Nagrywanie zdjecia o nazwie "fresh.jpg"
    camera.capture('fresh.jpg',resize=(1280, 720))#1280, 1024
    camera.annotate_text = "Photo is making"
    print_lcd(" Photo is making!","")
    print('Photo is making ',time.strftime("%H:%M:%S", time.gmtime()))
    if __name__ == "__main__":
        print_lcd(" Recive to AWS","")
        start_time = time.time()
        imageFile='fresh.jpg'
        client=boto3.client('rekognition')

        with open(imageFile, 'rb') as image:
            response = client.detect_labels(Image={'Bytes': image.read()})
        
        print('Detected labels in ' + imageFile)
        r = 0
        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))
            list1[0].append(label['Name'])
            list1[1].append(label['Confidence'])        
            r=r+1
        camera.annotate_text = "Answer is recive"
        print("--------")
        print("To trwalo: ", round(time.time() - start_time,2), "seconds.")
        end_lcd()
        
except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
    camera.close()
    GPIO.cleanup()
 
except:
    print('Error')
    camera.close()
    GPIO.cleanup()
    
finally:    
    time.sleep(5)
    GPIO.cleanup()
    camera.close()
    print("End of program")
