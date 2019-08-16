#!/bin/bash
raw=`/usr/bin/kubectl get pods ${1} ${2} | awk 'BEGIN {getline} {print $1} END{}' ${raw}`
for instanceid in ${raw}
do
	printf "${instanceid}\n"
done
read -r -p "Are you sure to delete all pods above? [Y/n]" response
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]] || [[ -z $response ]]; then
	for instanceid in ${raw}
	do
		printf "start deleting\n"
		kubectl delete pods --force --grace-period=0 ${instanceid}
	done
fi
