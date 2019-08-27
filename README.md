# IAM Server Certificate cleanup tool

## Installation
    
    python3 -mvenv env
    source env/bin/activate
    
    git clone https://github.com/nikhil-zadoo/iam-server-cert-cleanup.git
    cd iam-server-certs-cleanup
    pip install .

## Configuration:
Have your ~/.aws/config file ready to be used with the target account.

## Command
    AWS_PROFILE=<target profile in ~/.aws/config> python3 certs.py
