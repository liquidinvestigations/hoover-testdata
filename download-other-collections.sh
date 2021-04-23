#!/bin/bash
set -ex

# check we have tools
curl --version
wget --version
tar --version

# cd to parent of this file
cd "$(dirname ${BASH_SOURCE[0]})/.."

# make all dirs
mkdir -p testdata-textfiles/data
mkdir -p testdata-enron/data

# download testdata-textfiles
(
  cd testdata-textfiles/data
  
  set +e

  if ! [ -d extra ]; then
    (
      mkdir -p extra/ww2
      cd extra/ww2
      wget https://github.com/liquidinvestigations/testdata-extra-demo-data/archive/refs/heads/master.zip
    )
  fi
  
  if ! [ -f virus.zip ]; then
    wget http://archives.textfiles.com/adventure.zip
    wget http://archives.textfiles.com/anarchy.zip
    wget http://archives.textfiles.com/apple.tar.gz
    wget http://archives.textfiles.com/art.zip
    wget http://archives.textfiles.com/bbs.zip
    wget http://archives.textfiles.com/computers.zip
    wget http://archives.textfiles.com/conspiracy.tar.gz
    wget http://archives.textfiles.com/drugs.zip
    wget http://archives.textfiles.com/food.zip
    wget http://archives.textfiles.com/fun.tar.gz
    wget http://archives.textfiles.com/games.zip
    wget http://archives.textfiles.com/groups.zip
    wget http://archives.textfiles.com/hacking.zip
    wget http://archives.textfiles.com/hamradio.zip
    wget http://archives.textfiles.com/holiday.zip
    wget http://archives.textfiles.com/humor.zip
    wget http://archives.textfiles.com/internet.zip
    wget http://archives.textfiles.com/law.zip
    wget http://archives.textfiles.com/magazines.zip
    wget http://archives.textfiles.com/media.zip
    wget http://archives.textfiles.com/messages.zip
    wget http://archives.textfiles.com/music.zip
    wget http://archives.textfiles.com/news.zip
    wget http://archives.textfiles.com/phreak.zip
    wget http://archives.textfiles.com/piracy.zip
    wget http://archives.textfiles.com/politics.zip
    wget http://archives.textfiles.com/programming.zip
    wget http://archives.textfiles.com/reports.zip
    wget http://archives.textfiles.com/rpg.zip
    wget http://archives.textfiles.com/science.zip
    wget http://archives.textfiles.com/sex.zip
    wget http://archives.textfiles.com/sf.zip
    wget http://archives.textfiles.com/stories.zip
    wget http://archives.textfiles.com/survival.zip
    wget http://archives.textfiles.com/ufo.zip
    wget http://archives.textfiles.com/uploads.zip
    wget http://archives.textfiles.com/virus.zip

    mkdir -p etext
    (
      cd etext
      set +e
      wget -r -np -k  http://www.textfiles.com/etext/
    )
  fi

)


# download testdata-enron/data
(
  cd testdata-enron/data

  set +e
  if ! [ -f enron_mail_20150507.tar.gz ]; then
    wget https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz
    tar zxf enron_mail_20150507.tar.gz
  fi
)
