Invoke-WebRequest -Uri "http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip" -Outfile ".\stanford-corenlp-full-2018-10-05.zip"
expand-archive -path '.\stanford-corenlp-full-2018-10-05.zip' -destinationpath '.\sentiment\tools' -force
rm ".\stanford-corenlp-full-2018-10-05.zip"