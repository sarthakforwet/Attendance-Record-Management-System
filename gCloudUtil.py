from google.cloud import storage
import os, io
import numpy as np
import cv2, ast

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "AttendanceSystemConfigCloud.json"
storage_client = storage.Client()
BUCKET_NAME = "bkt-1"
bucket = storage_client.bucket(BUCKET_NAME)

def downloadFileFromBucket(blob_name, file_path):
    try:
        blob = bucket.blob(blob_name)
        with open(file_path, "wb") as f:
            storage_client.download_blob_to_file(blob, f)
    except Exception as e:
        print(e)

def getFileDataFromBucket(blob_name):
    try:
        blob = bucket.blob(blob_name)
        data = blob.download_as_bytes()
        data = data.decode("utf-8")
        return ast.literal_eval(data)
    except Exception as e:
        print(e)

def getImageDataFromBucket(file_path):
    try:
        blob = bucket.get_blob(file_path)
        downloaded_val = blob.download_as_bytes()
        buff = io.BytesIO(downloaded_val)
        np_data = np.asarray(bytearray(buff.read()),dtype=np.uint8)
        image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        print(image)
        return image
    except Exception as e:
        print(e)

def pushFileToBucket(blob_name, file_path):
    try:
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)

    except Exception as e:
        print(e)

def pushDataToBucket(blob_name, data):
    try:
        blob = bucket.blob(blob_name)
        blob.upload_from_string(str(data))
    except Exception as e:
        print(e)

def ifFileExists(file_path):
    stats = storage.Blob(bucket=bucket, name=file_path).exists(storage_client)
    return stats

def ifDirExists(folder_path):
    files = storage_client.list_blobs(bucket)
    for e in files:
        if folder_path in e.name:
            return True
    return False

img_path = "Dataset/CSD/EN18CS301233/"
#x = ifFileExists(img_path)
#print(x)
y = ifDirExists(img_path)
print(y)
#pushFileToBucket(img_path, img_path)
