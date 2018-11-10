#Źródło:https://docs.aws.amazon.com/rekognition/latest/dg/images-bytes.html
#Jest to przykład użycia lokalnego zdjęcia do rozpoznawania na nim objektów
import boto3

if __name__ == "__main__":

    imageFile='input.jpg'
    client=boto3.client('rekognition')
   
    with open(imageFile, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
        
    print('Detected labels in ' + imageFile)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))

    print('Done...')
