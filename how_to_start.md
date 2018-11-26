Jak zacząć...
===
### Podstawą tego projektu są:
1. [AWS Command Line Interface](#cli)
2. [Python3](#pliki)
3. [Sterowniki kamery Raspberry Pi dla Python](#camera)
4. [Sterowniki wyświetlacza](#s3)
5. [Biblioteki](#biblioteki)
6. [Źródła](#zrodla)
---

<a name="cli"></a>
# AWS Command Line Interface
Jest to ujednolicone narzędzie do zarządzania usługami AWS. Za pomocą tego można kontrolować wiele usług AWS z poziomu wiersza poleceń i zautomatyzować je za pomocą skryptów.
By kożystać z serwisów Amazon przedewszystkim musimy dokonać [rejestrację.](https://portal.aws.amazon.com/billing/signup#/start) 

Po rejestracji można pobrać **awscli**:

    instalacja pip awscli
  
<a name="camera"></a>
# Sterowniki kamery Raspberry Pi

By używać kamerę Raspberry Pi trzeba ją po pierwsze podłączyć do samego urządzenia po przez interfejs CSI, a następnie w 
menu konfiguracji *raspi-config* właczyć camerę:

    sudo raspi-config    
    
Po włączeniu należy zresetować urządzenie. Po tym można sprawdzić łącznąść z kamerą poleceniem:

    vcgencmd get_camera
    
Wynik ma być taki:

    supported=1 detected=1
    
Teraz możemy zrobić pierwsze zdjęcie poleceniem:

    raspistill -o myphoto.jpg -t 2000
Zdjęcie domyślnie się zapisuje w katalogu domowym użytkownika.
By Python mógł używać zasoby kamery, należy zainstalować pakiet *picamera* poleceniem niżej:

    sudo apt-get install python-picamera python3-picamera
    
lub możemy dokonać pobranie za pomocą Python’s pip tool:

    sudo pip install picamera
    
Po installacji sprawdzimy działanie Python'a z kamerą. Twożymy plik z rozszerzeniem .py (Umaga! Nie tworzymy plików o nazwie **picamera.py**, ta nazwa jest zarezerwowana), i kopiujemy skrypt:

    from time import sleep
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(5)
    camera.capture('photo.jpg')
    
Ten skrypt wyświetla okienko *"Preview"* które przedstawia nagrywanie kamery w czasie rzeczywistym i na końcu robi zdjęcie o nazwie "photo.jpg". Okienko "Preview"* będzie widoczne tylko i wyłącznie na wideo wyjściu urządzenia. Z poziomu aplikacja **PuTTy** nic nie zaobserwujemy.
Uruchomiamy poleceniem:

    python3 plik.py





 ---
<a name="zrodla"></a>
### Źródła

* [AWS Command Line Interface Getting Started](https://aws.amazon.com/cli/)
* [Getting started with picamera](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
* [Installation picamera](https://picamera.readthedocs.io/en/release-1.13/install.html#raspbian-installation)


