#!/bin/bash

projectDir=$(dirname `realpath $0`)
ansible-playbook -i localhost, $projectDir/playbook.yml
