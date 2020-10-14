#! zsh
mypath=$0:A
thumbnails_root=$(dirname "$mypath")/../public/thumbnails
mkdir -p "$thumbnails_root"
tmpd=$(mktemp -d)
trap 'rm -rf "$tmpd"; rm -rf "$thumbnails_root"/Makefile' EXIT

cat > "$thumbnails_root"/Makefile <<EOF
all: deepweeds cwfid digifarm-mungbeans artificial natural ginger

deepweeds:
	wget -O $tmpd/deepweeds.zip https://nextcloud.qriscloud.org.au/index.php/s/a3KxPawpqkiorST/download
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
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/data/raw/SOLES/narrabri/2020-summer/20200402/img/*.jpg $tmpd/digifarm-mungbeans
	find $tmpd/digifarm-mungbeans/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/digifarm-mungbeans .


artificial:
	mkdir $tmpd/artificial
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/data/raw/SOLES/narrabri/2019-winter/20190728/img/*.jpg $tmpd/artificial
	find $tmpd/artificial/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/artificial .

natural:
	mkdir $tmpd/natural
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/data/raw/SOLES/narrabri/2019-winter/20190729/img/*.jpg $tmpd/natural
	find $tmpd/natural/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/natural .

ginger:
	mkdir $tmpd/ginger
	scp research-data-int.sydney.edu.au:/rds/PRJ-iweeds/data/raw/SOLES/chromakey/2020-spring/20200804/20200804-ginger-shed/img/*.png $tmpd/ginger
	find $tmpd/ginger/ -name "*.png" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/ginger .
EOF


cd "$thumbnails_root"
make
