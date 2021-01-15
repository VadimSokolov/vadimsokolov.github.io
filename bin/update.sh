#!/bin/bash
python ./bin/jemdoc.py *.jemdoc
python ./bin/jemdoc.py wed/*.jemdoc
python ./bin/jemdoc.py courses/468/*.jemdoc
python ./bin/jemdoc.py courses/568/*.jemdoc
python ./bin/jemdoc.py courses/750/*.jemdoc
python ./bin/jemdoc.py courses/610/*.jemdoc
python ./bin/jemdoc.py courses/41000/*.jemdoc
#open index.html
git add .
git commit -m"update"
git push


# rsync --rsync-path=/usr/local/bin/rsync -avze ssh /Users/vsokolov/Dropbox/www/*.html vsokolov@mason.gmu.edu:/home/u2/vsokolov/public_html/

# upload to http://mason.gmu.edu/~vsokolov
# lf=/Users/vsokolov/Dropbox/www/
# echo $lf
# rsync --rsync-path=/usr/local/bin/rsync -avze ssh  $lf/image $lf/pdf $lf/courses $lf/*.html $lf/*.css vsokolov@mason.gmu.edu:/home/u2/vsokolov/public_html


# rsync --rsync-path=/usr/local/bin/rsync -avze ssh  -r /Users/vsokolov/Dropbox/www/pdf vsokolov@mason.gmu.edu:/home/u2/vsokolov/public_html
# rsync --rsync-path=/usr/local/bin/rsync -avze ssh  /Users/vsokolov/Dropbox/www/courses vsokolov@mason.gmu.edu:/home/u2/vsokolov/public_html

# rsync --rsync-path=/usr/local/bin/rsync -avze ssh  /Users/vsokolov/Dropbox/www/*.html vsokolov@mason.gmu.edu:/home/u2/vsokolov/public_html
# rsync --rsync-path=/usr/local/bin/rsync -avze ssh  /Users/vsokolov/Dropbox/www/*.css vsokolov@mason.gmu.edu:/home/u2/vsokolov/public_html