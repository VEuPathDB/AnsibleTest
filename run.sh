#!/bin/bash

projectDir=$(dirname `realpath $0`)

export ANSIBLE_CONFIG=$projectDir/conifer.cfg
ansible-playbook -i localhost, -e outputFile=$(pwd)/output.xml $projectDir/playbook.yml
