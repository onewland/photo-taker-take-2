#!/bin/bash

for i in snap1 snap2 snap3 snap4; do
	convert $i.jpg -colorspace gray -sigmoidal-contrast 10,40% $i-gray.jpg;
	convert $i-gray.jpg -crop 330x720+445+0 $i-crop.jpg;
	convert $i-crop.jpg -resize 480x1080\! $i-crop-resized.jpg;
done

montage -geometry 480x1080 \
        -tile 4x1 \
	snap1-crop-resized.jpg snap2-crop-resized.jpg snap3-crop-resized.jpg snap4-crop-resized.jpg \
	snapshot-montage.jpg

for i in snap1 snap2 snap3 snap4; do
	rm $i.jpg;
	rm $i-crop.jpg;
done
