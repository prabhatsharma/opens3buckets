import boto3

s3 = boto3.resource('s3')
s3Client = boto3.client('s3')

openGranteeURI = 'http://acs.amazonaws.com/groups/global/AllUsers'

print('This script lists world readable S3 buckets that you own:')
for bucket in s3.buckets.all():

    bucketAcl = s3Client.get_bucket_acl(Bucket=bucket.name)
    items = bucketAcl['Grants']

    for item in items:

        openPermissions = item['Permission'] == 'READ' or item['Permission'] == 'FULL_CONTROL'

        if item['Grantee']['Type'] == "Group" and item['Grantee']['URI'] == openGranteeURI and openPermissions:
            print('Bucket: ', bucket.name)
            print('World Permissions: ',  item['Permission'])
