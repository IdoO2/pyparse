#!/bin/bash
# Builds Pyparse Sublime Text 3 plugin
# Input (in directory `src`): 
# - parsermoc.py    A moc parser
# - stplugin.py     A moc plugin
# Output:
# - pyparse.sublime-plugin

# zip stplugin.sublime-plugin src/parsermoc.py src/stplugin.py
# cp stplugin.sublime-plugin ~/.config/sublime-text-3/Installed\ Packages/
# mv stplugin.sublime-plugin ~/.config/sublime-text-3/Packages/User/

PLUGIN_DIR=~/.config/sublime-text-3/Packages/Pyparse
if [ ! -d $PLUGIN_DIR ]
then
    mkdir $PLUGIN_DIR
fi

cp src/stplugin.py $PLUGIN_DIR
cp src/parsermoc.py $PLUGIN_DIR

~/Downloads/sublime_text_3/sublime_text
