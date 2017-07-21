import boto3
import time
import json

startTime = time.time()
s3 = boto3.resource('s3')
s3Client = boto3.client('s3')

openGranteeURI = 'http://acs.amazonaws.com/groups/global/AllUsers'

print('This script lists world readable S3 buckets that you own:')
for bucket in s3.buckets.all():
    
    # Check for bucket policies
    try:
        bucketPolicy = s3Client.get_bucket_policy(Bucket = bucket.name)
        Statements = json.loads(bucketPolicy['Policy'])['Statement']
        for Statement in Statements:
            if Statement['Principal'] == "*" and Statement['Effect'] == "Allow":
                print('Policy for Bucket: ', bucket.name)
                print("Policy: Resource: ", Statement['Resource'])
                print("Policy: Action: ", Statement['Action'])
    except:
        bucketPolicy = "No bucket policy"

    # Check for Bucket ACLs
    bucketAcl = s3Client.get_bucket_acl(Bucket=bucket.name)
    grants = bucketAcl['Grants']

    for grant in grants:
        openPermissions = grant['Permission'] in ['READ', 'WRITE', 'READ_ACP', 'WRITE_ACP', 'FULL_CONTROL']

        if grant['Grantee']['Type'] == "Group" and grant['Grantee']['URI'] == openGranteeURI and openPermissions:
            print('ACL for Bucket: ', bucket.name)
            print('World Permissions: ',  grant['Permission'])

print('open buckets found in: ', round(time.time() - startTime, 2), ' seconds')