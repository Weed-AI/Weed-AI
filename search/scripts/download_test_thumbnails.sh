#! zsh
mypath=$0:A

usage() {
	echo $0 "[OPTIONS]" >&2
	echo Options: >&2
	echo " -r|--rds      Set the path to the iweeds RDS" >&2
	exit 1
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        -r|--rds) rds_root="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

thumbnails_root=$(dirname "$mypath")/../public/thumbnails
mkdir -p "$thumbnails_root"
tmpd=$(mktemp -d)
trap 'rm -rf "$tmpd"; rm -rf "$thumbnails_root"/Makefile' EXIT

if [ -n "$rds_root" ]
then
	rds_cp='cp -r "'$rds_root'"'
else
	rds_cp='scp -r research-data-int.sydney.edu.au:/rds/PRJ-iweeds'
fi

cat > "$thumbnails_root"/Makefile <<EOF
all: deepweeds cwfid digifarm-mungbeans artificial natural ginger

deepweeds:
	mkdir $tmpd/deepweeds
	$rds_cp/external_datasets/raw/deepweeds/images.zip $tmpd/deepweeds.zip
	unzip -d $tmpd/deepweeds $tmpd/deepweeds.zip
	rm -r $tmpd/deepweeds.zip
	# find $tmpd/deepweeds -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/deepweeds .
	
cwfid:
	mkdir $tmpd/dataset
	$rds_cp/external_datasets/raw/cwfid/dataset $tmpd/
	mkdir cwfid
	find $tmpd/dataset/images -name "*.png" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/dataset/images/*.png cwfid/
	rm -rf $tmpd/dataset


digifarm-mungbeans:
	mkdir $tmpd/digifarm-mungbeans
	$rds_cp/data/raw/SOLES/narrabri/2020-summer/20200402/img/*.jpg $tmpd/digifarm-mungbeans
	find $tmpd/digifarm-mungbeans/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/digifarm-mungbeans .


artificial:
	mkdir $tmpd/artificial
	$rds_cp/data/raw/SOLES/narrabri/2019-winter/20190728/img/*.jpg $tmpd/artificial
	find $tmpd/artificial/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/artificial .

natural:
	mkdir $tmpd/natural
	$rds_cp/data/raw/SOLES/narrabri/2019-winter/20190729/img/*.jpg $tmpd/natural
	find $tmpd/natural/ -name "*.jpg" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/natural .

ginger:
	mkdir $tmpd/ginger
	$rds_cp/data/raw/SOLES/chromakey/2020-spring/20200804/20200804-ginger-shed/img/*.png $tmpd/ginger
	find $tmpd/ginger/ -name "*.png" -exec magick "{}" -resize 300x300 '{}' ';'
	mv $tmpd/ginger .
EOF


cd "$thumbnails_root"
make
