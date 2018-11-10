#Źródło:"https://docs.aws.amazon.com/rekognition/latest/dg/faces-comparefaces.html"
#Jest to przykład porównania 2 zdjęć z użyciem Amazon Rekognition

import boto3

if __name__ == "__main__":

    sourceFile='source.jpg'
    targetFile='target.jpg'
    client=boto3.client('rekognition')
   
    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')

    response=client.compare_faces(SimilarityThreshold=70,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + confidence + '% confidence')

    imageSource.close()
    imageTarget.close()               
