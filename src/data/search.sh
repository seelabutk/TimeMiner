PREFIX="/export/data/dahome/ahota/wiki/pagecount"
LIST=$(ls $PREFIX)

for DIR in $LIST; do
	FILES=$(ls $PREFIX/$DIR/*.gz)
	for FILE IN $FILES; do
		zcat $FILE | grep "^en \|^en.mw " -i "$FILE" > "$FILE".en
	done
done

#for file in *;
#do
#	grep "^en \|^en.mw " -i "$file" > "$file".search;
#done
