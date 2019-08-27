import boto3
import datetime
import logging
import os
import sys

FORMAT = "%(asctime)s %(message)s"
logfile = "iam-server-certs-delete-" + datetime.datetime.now().isoformat() + ".log"
logging.basicConfig(level=logging.INFO, format=FORMAT, filename=logfile)

profile = os.getenv('AWS_PROFILE')
if profile == None:
    logging.error("Please set the AWS_PROFILE. use the below command!")
    logging.error("AWS_PROFILE=<the target profile set in ~/.aws/config> python3 certs.py")
    sys.exit(1)

session = boto3.Session(profile_name=profile)
iam = session.client('iam')
elb = session.client('elbv2')

def delete_unassoc_certs(list_assoc_cert): #Deletes certs that are not associated with any LB and also not expired
    current_time = datetime.datetime.now(datetime.timezone.utc)
    paginator = iam.get_paginator('list_server_certificates')
    is_cert_assoc = lambda x,y: True if (y in x) else False
    is_cert_expired = lambda x: True if (current_time > x) else False
    for response in paginator.paginate():
        for certificate in response['ServerCertificateMetadataList']:
            if not is_cert_assoc(list_assoc_cert, certificate['Arn']) and is_cert_expired(certificate['Expiration']):
                logging.info(f"{certificate} will be deleted")
                iam.delete_server_certificate(ServerCertificateName=certificate['ServerCertificateName'])
            else:
                logging.info(f"{certificate} will be retained")

def get_certs_assoc_with_lb(): # Returns list of certificates which are associated with atleast 1 Load Balancer
    paginator = elb.get_paginator('describe_load_balancers')
    count = 0
    list_assoc_cert = [""]
    for response in paginator.paginate():
        for lb in response['LoadBalancers']:
            count += 1
            logging.info("####################")
            logging.info(lb)
            lb_arn = lb['LoadBalancerArn']
            logging.info(lb_arn)
            listener_response = elb.describe_listeners(LoadBalancerArn=lb_arn)
            for listener in listener_response['Listeners']:
                logging.info("------")
                logging.info(listener)
                try:
                    for cert in listener['Certificates']:
                        logging.info(f"CERT ARN IS - {cert['CertificateArn']}")
                        list_assoc_cert.append(cert['CertificateArn'])
                except KeyError:
                    logging.info("No certificate present for the LB!")

    logging.info(f"number of LB's {count}")
    return list_assoc_cert



list_assoc_cert = get_certs_assoc_with_lb()
logging.info(f"The list of associated certificates is \n {list_assoc_cert}")
logging.info(f"Number of associated certificates is - {len(list_assoc_cert)}")
delete_unassoc_certs(list_assoc_cert)
