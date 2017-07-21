import boto3
import time

startTime = time.time()
s3 = boto3.resource('s3')
s3Client = boto3.client('s3')

openGranteeURI = 'http://acs.amazonaws.com/groups/global/AllUsers'

print('This script lists world readable S3 buckets that you own:')
for bucket in s3.buckets.all():

    bucketAcl = s3Client.get_bucket_acl(Bucket=bucket.name)
    grants = bucketAcl['Grants']

    for grant in grants:

        openPermissions = grant['Permission'] in ['READ', 'WRITE', 'FULL_CONTROL']

        if grant['Grantee']['Type'] == "Group" and grant['Grantee']['URI'] == openGranteeURI and openPermissions:
            print('Bucket: ', bucket.name)
            print('World Permissions: ',  grant['Permission'])

print('open buckets found in: ', round(time.time() - startTime, 2), ' seconds')