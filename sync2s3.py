#!/usr/bin/env python3

import os
import argparse
import boto3
import botocore
import mimetypes


def main():
    """
        This script sync new objects to remote S3 storage
    """

    default_s3_endpoint = os.getenv("REMOTE", "http://192.168.1.63:9000")
    # pour faciliter le dev, j'ai laissé des valeurs par défaut
    default_ACCESS_KEY = os.getenv("ACCESS_KEY", "minio")
    default_SECRET_KEY = os.getenv("SECRET_KEY", "miniokey")
    default_location = "."
    default_bucket = "test"

    parser = argparse.ArgumentParser(description="This script mirror new items from local only to remote S3 endpoint")
    parser.add_argument("-l", "--location",
                        help="local location",
                        default=default_location)
    parser.add_argument("-b", "--bucket",default=default_bucket)
    parser.add_argument("-e", "--endpoint", default=default_s3_endpoint)

    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="Do not interactive, no confirmation")
    parser.add_argument("--accessKey",default=default_ACCESS_KEY)
    parser.add_argument("--secretKey",default=default_SECRET_KEY)

    args = parser.parse_args()
    print(args)

    s3 = boto3.resource("s3",
                        endpoint_url=args.endpoint,
                        aws_access_key_id=args.accessKey,
                        aws_secret_access_key=args.secretKey)

    list_for_upload = []
    list_for_deletion = []
    dict_object_lastMod = {}
    dict_file_lastMod = {}

    #args.force = True
    try:
        s3.meta.client.head_bucket(Bucket=args.bucket)
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"bucket {args.bucket} do not exist")
    finally:
        if args.force:
            s3.Bucket(args.bucket).create(ACL="private")


    for obj in s3.Bucket(args.bucket).objects.all():
        dict_object_lastMod[obj.key] = obj.last_modified.timestamp()

    for root, dirs, files in os.walk(args.location):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, args.location)
            dict_file_lastMod[relative_path] = os.path.getmtime(relative_path)

    
    for file in dict_file_lastMod:
        if file in dict_object_lastMod:
            if dict_file_lastMod[file] > dict_object_lastMod[file]:
                list_for_upload.append(file)
        else:
            list_for_upload.append(file)
        
    for obj in dict_object_lastMod:
        if obj not in dict_file_lastMod:
            list_for_deletion.append(obj)
    

    print(f"File to upload {list_for_upload}")
    print(f"Files to delete {list_for_deletion}")

    
    for root, dirs, files in os.walk(args.location):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, args.location)
            if relative_path in list_for_upload:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, args.location)
                if mimetypes.guess_type(relative_path)[0] == None:
                    s3.Bucket(args.bucket).upload_file(relative_path, relative_path)
                else:
                    s3.Bucket(args.bucket).upload_file(relative_path, relative_path, ExtraArgs={"ContentType": mimetypes.guess_type(relative_path)[0]})

    for entry in list_for_deletion:
        s3.Bucket(args.bucket).delete_objects(Delete={
            "Objects": [{"Key": entry}],
            "Quiet": True
        })
        

main()


