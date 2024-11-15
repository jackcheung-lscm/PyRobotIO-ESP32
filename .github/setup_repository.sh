#!/usr/bin/env bash
while getopts a:e:n:u:d: flag
do
    case "${flag}" in
        a) author=${OPTARG};;
        e) author_email_address=${OPTARG};;
        n) repository_name=${OPTARG};;
        u) repository_url_name=${OPTARG};;
        d) description=${OPTARG};;
    esac
done


echo "Author: $author";
echo "Author Email: $author_email_address";
echo "Repository Name: $repository_name";
echo "Repository URL name: $repository_url_name";
echo "Description: $description";

# Check if repository_url_name starts with "PyRobotIO-"
if [[ $repository_url_name == PyRobotIO-* ]]; then
    sensor_name=$(echo ${repository_url_name#*PyRobotIO-} | tr 'A-Z' 'a-z' | tr '-' '_')

    echo "Sensor Name: $sensor_name"

    echo "Setup Repository..."

    original_author="author_name"
    original_author_email_address="author_email_address"
    original_repository_name="repository_name"
    original_repository_url_name="repository_url_name"
    original_description="repository_description"
    original_sensor_name="sensor_name"

    for filename in $(git ls-files)
    do
        echo "Edit $filename"
        sed -i "s/$original_author/$author/g" $filename
        sed -i "s/$original_author_email_address/$author_email_address/g" $filename
        sed -i "s/$original_repository_name/$repository_name/g" $filename
        sed -i "s/$original_repository_url_name/$repository_url_name/g" $filename
        sed -i "s/$original_description/$description/g" $filename
        sed -i "s/$original_sensor_name/$sensor_name/g" $filename
    done

    # Rename files
    mv sensor_name/sensor_name.py "sensor_name/$sensor_name.py"
    mv sensor_name $sensor_name

    # Remove setup_repository action from workflow
    rm -rf .github/setup_repository.sh
    rm -rf .github/workflows/setup_repository.yaml
else
    echo "The project name does not start with 'PyRobotIO-'"
    rm -rf ./*
    rm -rf .github
    rm -rf .flake8
    rm -rf .gitignore
    echo "## Improper repository name" >> README.md
    echo "- Please name the repository as \`PyRobotIO-{sensor_name}\`" >> README.md
    echo "    - Replace \`{sensor_name}\` with yours e.g. \`PyRobotIO-USB-Camera\`" >> README.md
fi
