#!/bin/bash

while :
do
  puts "syncing with AWS"
  aws s3 sync --delete s3://photo-taker/photos photos/
  sleep 300
done
