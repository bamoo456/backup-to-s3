# Backup-to-s3
It's a simple python commandline script for archiving a folder and upload it to the s3.

## Reqiurements

* Python3.8+
* Poetry
* Pip (optional)

## Usage

### Install poetry dependencies
```
poetry install
```

### Run with poetry

```shell
AWS_SHARED_CREDENTIALS_FILE=~/.aws/credentials \
AWS_PROFILE=profile.dev \
poetry run backup_to_s3 \
-i ~/backup-folder/
-s s3://your-bucket/backup/folder/name
```

## Install backup_to_s3 as sysstem script

For achieving this, we have to use `poetry build` to generate a tar file for `pip install`.
The detail steps can be found as following:

### Build backup_to_s3 tar file

```shell
cd backup-to-s3/
poetry build
```

The built `tar.gz` should be put under `backup-to-s3/dist`.

### Install the built file as system script

```shell
pip install backup-to-s3/dist/backup-to-s3.xxx.tar.gz
```

### Run the backup_to_s3 system script

```shell
AWS_SHARED_CREDENTIALS_FILE=~/.aws/credentials \
AWS_PROFILE=profile.dev \
backup_to_s3 \
-i ~/backup-folder/
-s s3://your-bucket/backup/folder/name
```
