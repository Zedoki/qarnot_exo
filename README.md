# Sync 2 S3

This script sync from a local place to a remote S3 server bucket.


## How to use
```
usage: sync2s3.py [-h] [-l LOCATION] [-b BUCKET] [-e ENDPOINT] [-f] [-u URL] [--accessKey ACCESSKEY] [--secretKey SECRETKEY]

This script mirror new items from local only to remote S3 endpoint

options:
  -h, --help            show this help message and exit
  -l, --location LOCATION
                        local location
  -b, --bucket BUCKET
  -e, --endpoint ENDPOINT
  -f, --force           Do not interactive, no confirmation
  -u, --url URL
  --accessKey ACCESSKEY
  --secretKey SECRETKEY
```

### Examples
`sync2s3.py --location .\sync2s3\`

### Room for improvement
- [ ] upload folder
- [ ] reflect correct content-type in bucket
- [ ] make use of try catch
- [ ] pytlint + ruff 
- [ ] create funtion for better visibility
- [ ] remove limitation for flate files only
- [ ] make interactive version
- [ ] add debug / verbose options


## How to package and deploy
TODO