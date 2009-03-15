#!/bin/sh

pyrcc4 icons.qrc -o icons_rc.py
pyuic4 window.ui -o windowUi.py -x
pyuic4 editor.ui -o editorUi.py -x
