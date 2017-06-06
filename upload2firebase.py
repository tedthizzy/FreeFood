from google.cloud import storage
# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://cufreefood-1cdb5.firebaseio.com/', None)
# result = firebase.get('/users', None)
# new_user = 'Ted Testing'
# print(result)

# Enable Storage
client = storage.Client()

# Reference an existing bucket.
bucket = client.get_bucket('my-existing-bucket')

# Upload a local file to a new file to be created in your bucket.
zebraBlob = bucket.get_blob('zebra.jpg')
zebraBlob.upload_from_filename(filename='/photos/zoo/zebra.jpg')

# Download a file from your bucket.
giraffeBlob = bucket.get_blob('giraffe.jpg')
giraffeBlob.download_as_string()
In line client = storage.Client()


