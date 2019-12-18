Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install javaruntime
cd ~
cd Downloads
Invoke-WebRequest -Uri "http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip" -Outfile ".\stanford-corenlp-full-2018-10-05.zip"
expand-archive -path '.\stanford-corenlp-full-2018-10-05.zip' -destinationpath '.\stanford-corenlp-full-2018-10-05' -force
