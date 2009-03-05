#!/bin/sh

pyrcc4 icons.qrc -o icons_rc.py
pyuic4 window.ui -o windowUi.py
