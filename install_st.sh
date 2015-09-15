#!/bin/bash

TARGET=$HOME'/.config/sublime-text-3/Packages'

# Plugin contents to a zip
#zip pyparse.sublime-plugin src/sublime_text/*.py src/sublime_text/PyParsePackage/

# Create package dir
cp -r src/sublime_text/PyParsePackage $TARGET
echo 'install OK'
