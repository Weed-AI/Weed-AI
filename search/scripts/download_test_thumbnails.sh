#! zsh
mypath=$0:A
thumbnails_root=$(dirname "$mypath")/../public/thumbnails
mkdir -p "$thumbnails_root"
tmpd=$(mktemp -d)
trap 'rm -rf "$tmpd"; rm -rf "$thumbnails_root"/Makefile' EXIT

rds_cp='scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds'

cat > "$thumbnails_root"/Makefile <<EOF
all: deepweeds cwfid digifarm-mungbeans artificial natural ginger

deepweeds:
	wget -O $tmpd/deepweeds.zip https://drive.google.com/u/0/uc?export=download&confirm=C_v5&id=1xnK3B6K6KekDI55vwJ0vnc2IGoDga9cj
	mkdir $tmpd/deepweeds
	unzip -d $tmpd/deepweeds $tmpd/deepweeds.zip
	rm -r $tmpd/deepweeds.zip
	# find $tmpd/deepweeds -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/deepweeds .
	
cwfid:
	cd $tmpd && git clone https://github.com/cwfid/dataset && cd -
	mkdir cwfid
	find $tmpd/dataset/images -name "*.png" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/dataset/images/*.png cwfid/
	rm -rf $tmpd/dataset


digifarm-mungbeans:
	mkdir $tmpd/digifarm-mungbeans
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/Narrabri/digifarm/mungbeans/*/images/*.jpg $tmpd/digifarm-mungbeans
	find $tmpd/digifarm-mungbeans/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/digifarm-mungbeans .


artificial:
	mkdir $tmpd/artificial
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/Narrabri/artificial_illumination/20190728_Z16/images/*.jpg $tmpd/artificial
	find $tmpd/artificial/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/artificial .

natural:
	mkdir $tmpd/natural
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/Narrabri/natural_illumination/*/images/*.jpg $tmpd/natural
	find $tmpd/natural/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/natural .

ginger:
	mkdir $tmpd/ginger
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/Ginger/artificial/img/*.png $tmpd/ginger
	find $tmpd/ginger/ -name "*.png" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/ginger .
EOF


cd "$thumbnails_root"
make
