#!/bin/bash

echo "make dist file"
mkdir -p dist
echo "copying __main.py__ for standalone purposes"
cp sshm.py __main__.py
echo "remove zip file from dist"
rm dist/*
echo "zipping files excluding .git data __pycache__"
zip -r9 --exclude=release.sh --exclude=dist* --exclude=*__pycache__* ./dist/sshm.zip .
echo "remove __main.py__ from source"
rm __main__.py
echo "create standalone"
cd dist/
echo '#!/usr/bin/env python3' | cat - sshm.zip > sshm
chmod +x sshm
echo "cleaning up"
rm sshm.zip
