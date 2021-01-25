import os
import tarfile
import logging
import click
import boto3
import pathlib

from botocore.exceptions import ClientError
from datetime import datetime
from os.path import expanduser

# AWS_PROFILE=home.gechen.s3
def upload_file(file_name, bucket, s3_dir=""):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3_dir: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if s3_dir != "" and s3_dir.split("/")[-1] != "/":
        s3_dir += "/"

    object_name = s3_dir + file_name.split("/")[-1]

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.exception(e)
        # logging.error(e)
        return False
    return True

class Cli():
    def __init__(self, input_dir, s3_bucket, s3_dir):
        self.input_dir = input_dir
        self.s3_bucket = s3_bucket
        # remove the heading "/"
        self.s3_dir = s3_dir if s3_dir[0] != "/" else s3_dir[1:]
        self.tmp_dir = expanduser("~") + "/.backup-to-s3"

    def run(self):
        # creating the tmp_dir
        if not pathlib.Path(self.tmp_dir).is_dir():
            os.makedirs(self.tmp_dir)

        # the backup_file_name can be something like: folder_2020948192_backup.tar.gz
        backup_file_name = "{}_{}_{}".format(
            pathlib.Path(self.input_dir).parent.absolute().as_posix().split("/")[-1],
            int(datetime.now().timestamp()),
            "backup.tar.gz")

        # creating the archive tmp file
        out = "{}/{}".format(self.tmp_dir, backup_file_name)
        with tarfile.open(out, mode='w:gz') as archive:
            archive.add(
                self.input_dir,
                arcname=os.path.basename(self.input_dir),
                recursive=True)

        # uploading the archive file to the s3 bucket
        upload_file(out, self.s3_bucket, self.s3_dir)

        # remove the archive tmp file
        os.remove(out)

@click.command()
@click.option(
    "-i",
    "--input",
    envvar="INPUT",
    help="The input dir for backup",
    required=True
)
@click.option(
    "-s",
    "--s3_path",
    default="",
    envvar="S3_PATH",
    help="The s3 path for uploading. (e.g. s3://path/to/upload )",
    required=True
)
def cli(input, s3_path):
    if s3_path.find("s3://") != 0:
        logging.error("incorrect s3 path format")
        exit(1)

    s = s3_path[5:].split("/")
    s3_bucket = s[0]
    s3_dir = s3_path[5+len(s3_bucket):]

    cli = Cli(input, s3_bucket, s3_dir)
    cli.run()

# if __name__ == "__main__":
#    cli()
def main():
    cli()

