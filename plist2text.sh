#!/bin/bash

rm -f $2

sed -n 'N;/<key>Title<\/key>/{N;/<string>.*<\/string>/{s/.*<string>\(.*\)<\/string>.*/\/* \1 *\/\
"\1" = "\1";\
/p;};}' $1 >> $2

sed -n 'N;/<key>FooterText<\/key>/{N;/<string>.*<\/string>/{s/.*<string>\(.*\)<\/string>.*/\/* \1 *\/\
\"\1" = "\1";\
/p;}
;}' $1 >> $2

sed -n 'N;/<key>Titles<\/key>/{N;/<array>/{:a
/<\/array>/!{
/<string>.*<\/string>/{s/.*<string>\(.*\)<\/string>.*/\/* \1 *\/\
\"\1" = "\1";\
/p;}
N;
ba
;};};}' $1 >> $2