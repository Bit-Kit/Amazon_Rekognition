#Adding Faces to a Collection
#Sourse:https://docs.aws.amazon.com/rekognition/latest/dg/add-faces-to-collection-procedure.html

import boto3
if __name__ == "__main__":
    collectionId='my_new_collection'
    photo='test.jpg'
    imageSource=open(photo,'rb')
    client=boto3.client('rekognition')
    response=client.index_faces(CollectionId=collectionId,
                                Image={'Bytes': imageSource.read()},
                                DetectionAttributes=['ALL'])
    print ('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)

