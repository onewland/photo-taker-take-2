#!/bin/bash

for i in $1 $2 $3 $4; do
	convert $i.jpg -colorspace gray -sigmoidal-contrast 10,40% $i-gray.jpg;
	convert $i-gray.jpg -crop 330x720+445+0 $i-crop.jpg;
	convert $i-crop.jpg -resize 480x1080\! $i-crop-resized.jpg;
done

montage -geometry 480x1080 \
        -tile 4x1 \
	$1-crop-resized.jpg $2-crop-resized.jpg $3-crop-resized.jpg $4-crop-resized.jpg \
	snapshot-montage.jpg

for i in $1 $2 $3 $4; do
	rm $i-gray.jpg;
	rm $i-crop.jpg;
	rm $i-crop-resized.jpg;
done
