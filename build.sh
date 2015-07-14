#!/bin/bash
# Builds Pyparse Sublime Text 3 plugin
# Input: 
# - parsermoc.py    A moc parser
# - stplugin.py     A moc plugin
# Output:
# - pyparse.sublime-plugin

# zip stplugin.sublime-plugin parsermoc.py stplugin.py
# cp stplugin.sublime-plugin /home/dafp/.config/sublime-text-3/Installed\ Packages/
# mv stplugin.sublime-plugin /home/dafp/.config/sublime-text-4/Packages/User/

PLUGIN_DIR=~/.config/sublime-text-3/Packages/Pyparse
if [ ! -d $PLUGIN_DIR ]
then
    mkdir $PLUGIN_DIR
fi
cp stplugin.py /home/dafp/.config/sublime-text-3/Packages/Pyparse
cp parsermoc.py /home/dafp/.config/sublime-text-3/Packages/Pyparse
/home/dafp/Downloads/sublime_text_3/sublime_text
