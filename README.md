# wmdbtrigger

Send an event to the event queue when a wafermap is added to the wafermap database.

## Building
### Debian file
#### Install stdeb

To be able to build deb files from python packages install stdeb ( you can also install with pip or easy_install ).

  git clone https://github.com/bhoflack/stdeb.git
  cd stdeb && sudo python setup.py install

#### Building the deb file
##### Introduction

To be able to build the deb file you require stdeb.  All other dependencies are included in the distribution.

##### Building #####
To create a deb file from the distribution type:

    python setup.py --command-packages=stdeb.command bdist_deb

This will generate the deb file in the deb_dist folder.

##### Building on lenny #####
Because of issue https://github.com/astraw/stdeb/issues/32 we have more issues in lenny.
I've created the following script to be able to build on lenny:

    if [ -e deb_dist ]; then
       rm -rf deb_dist
    fi
    if [ -e dist ]; then
       rm -rf dist
    fi
    if [ -e mapmerge-*.tar.gz ]; then
       rm mapmerge-*.tar.gz
    fi

    python setup.py sdist
    py2dsc --force-buildsystem=False dist/mapmerge-*.tar.gz
    cd deb_dist/mapmerge-*
    debuild -us -uc

## Installing
### The deb file
To install the deb file execute:

    sudo apt-get install wmdbtrigger

