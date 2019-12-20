Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install javaruntime
cd .\sentiment
Invoke-WebRequest -Uri "http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip" -Outfile ".\stanford-corenlp-full-2018-10-05.zip"
expand-archive -path '.\stanford-corenlp-full-2018-10-05.zip' -destinationpath '.\tools' -force
rm ".\stanford-corenlp-full-2018-10-05.zip"