#! /usr/bin/python

# -----------------------------------------------------------------------------
# aws_virtualenv.py
#
# install tools for managing virtualenv projects for AWS & Lambda. Needs to
# be run by user with sudo permissions (or root).
#
# installs awscli, emulambda, virtualenv and boto3 then creates a command
# /usr/local/bin/virtualaws which will create a virtualenv project and then
# modify the activate script to point at a local AWS credentials file
# 

import os
import sys
import pip

def pip_install(package_name, package_source='dummyvalue'):
    if (package_source == 'dummyvalue'):
        package_source = package_name

    installed = [package.project_name for package in pip.get_installed_distributions()]

    if package_name not in installed:
        pip.main(['install', package_source])




# Make sure we're running as root - means we need to run as a user capable of sudoing
if os.geteuid() != 0:
    # os.execvp() replaces the running process, rather than launching a child
    # process, so there's no need to exit afterwards. The extra "sudo" in the
    # second parameter is required because Python doesn't automatically set $0
    # in the new process.
    os.execvp("sudo", ["sudo"] + sys.argv)


# Install required packages
pip_install('awscli')
pip_install('virtualenv')
pip_install('boto3')
pip_install('emulambda', 'git+https://github.com/fugue/emulambda.git')

# create /usr/local/bin/virtualaws
script_text="""#!/bin/bash
virtualenv $1
mkdir $1/.aws
echo 'export AWS_SHARED_CREDENTIALS_FILE=${VIRTUAL_ENV}/.aws/credentials' >> $1/bin/activate
"""

with open('/usr/local/bin/virtualaws', 'wb', 0755) as script:
    os.chmod('/usr/local/bin/virtualaws', 0755)
    script.write(script_text)
