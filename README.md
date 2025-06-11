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
  --accessKey ACCESSKEY
  --secretKey SECRETKEY
```

### Examples
You will have to override `--endpoint`.

`sync2s3.py --location ./sync2s3/`

### Room for improvement
- [X] upload folder
- [x] reflect correct content-type in bucket (partial)
- [ ] make use of try catch
- [x] ruff
- [ ] create funtion for better visibility
- [x] remove limitation for flate files only
- [ ] make interactive version
- [ ] add debug / verbose options
- [ ] packaging: bring dependancies along the package or install it in venv


## How to package and deploy
__Warning: this method install system wide dependancies, you may not want that__

1. Create file structure like in sync2s3-package
2. Copy and chmod +x postinstall and the script
3. `dpkg-deb --build sync2s3-package`
4. `dpkg -i sync2s3-package.deb`
