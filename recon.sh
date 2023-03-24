subfinder -d $1 -o $1subfinder.txt
cat $1subfinder.txt | sort -u | uniq > $1subfinder-uniq.txt
httpx -l $1subfinder-uniq.txt -ports 0-65535 -threads 50 -o $1subdomains-live.txt
nuclei -l $1subdomains-live.txt -o $1nucleiresults.txt
