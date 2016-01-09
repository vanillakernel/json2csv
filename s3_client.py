import boto3
import re
import sys
from os import listdir
from os.path import isfile, join, abspath

s3 = boto3.client('s3')

def download_files(bucket, prefix, file_path):
  response = s3.list_objects(Bucket=bucket, Prefix=prefix)
  for file in response['Contents']:
    key = file['Key']
    match = re.search('[\w0-9_-]+\.\w+$',key)
    file_name = match.group() if match else None
    if file_name is not None:
      file_name = join(abspath(file_path), file_name)
      sys.stderr.write("downloading %s/%s to %s\n" % (bucket, key, file_name))
      s3.download_file(bucket, key, file_name)
          

def upload_files(file_path, bucket, prefix):
  files = [abspath(join(file_path,f)) for f in listdir(file_path) if isfile(join(file_path, f))]
  for file in files:
    file_name = re.search('[\w0-9_-]+\.\w+$',file).group()
    key = prefix + '/' + file_name
    sys.stderr.write("uploading %s to %s/%s\n" % (file, bucket, key))
    s3.upload_file(file, bucket, key)

if __name__ == "__main__":
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-b", "--bucket", dest="bucket")
  parser.add_option("-p", "--prefix", dest="prefix")
  parser.add_option("-f", "--file-path", dest="file_path")
  parser.add_option("--type", dest="type")
  (options, args) = parser.parse_args()
  if options.type == 'download':
    download_files(options.bucket, options.prefix, abspath(options.file_path))
  elif options.type == 'upload':
    upload_files(abspath(options.file_path), options.bucket, options.prefix)

    


