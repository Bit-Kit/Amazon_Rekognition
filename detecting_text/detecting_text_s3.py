#Źródło:"https://docs.aws.amazon.com/rekognition/latest/dg/text-detecting-text-procedure.html"

import boto3
print(' ----------------------------------')
print('|Ten program wysyla plik z s3 do > |')
print('|Amazon Recognition "Text in image"|')
print(' ----------------------------------')


if __name__ == "__main__":

    bucket='bucket_example'
    photo='photo_example.jpg'

    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})             
    textDetections=response['TextDetections']
    print (response)
    print ('Matching faces')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
