#!/bin/bash
# can't run server.py and consumer.py there, if we will do two CMD command to run the both files, docker will take the
# last one, so to deal with it, I created bash script which will be executed and run the both python scripts
exec python3 consumer.py &
exec python3 server.py