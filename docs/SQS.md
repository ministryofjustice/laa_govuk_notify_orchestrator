## How to use AWS SQS as your Message Queue

This guide is for teams with applications or services deployed on, the Ministry of Justice’s Cloud Platform.

For this guide you will need access to Cloud Platform's Kubernetes cluser, to do this please follow [this guide](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/getting-started/kubectl-config.html).

### Set your AWS ENV Variables
Firstly you are going to need to show the details of your Service Pod, this can be done using:
```
kubectl -n laa-govuk-notify-orchestrator-dev describe pods | grep "AWS_"
```
Replace laa-govuk-notify-orchestrator-dev with the name of your Cloud Platform namespace.

You should see 5 Environment variables, copy these to and place then in a local `.env` file.

### Get your AWS Web Identity Token
Next we need to find the value of `AWS_WEB_IDENTITY_TOKEN_FILE` and replicate this file locally, this can be done by getting into the kubernetes pod using
```
kubectl -n laa-govuk-notify-orchestrator-dev get pods

kubectl exec -it [The name of the pod given by the above command] -n laa-govuk-notify-orchestrator-dev sh
```
You have now opened the Bourne Shell inside the pod and all future commands you execute will be run inside the pod.

Read the file referenced by the `AWS_WEB_IDENTITY_TOKEN_FILE` by running
```
cat $AWS_WEB_IDENTITY_TOKEN_FILE
```
Copy the contents of the file exluding the final `/` and place it inside a file named `aws_token.conf`, do not share or commit the contents of this file.

Finally go to the `.env` file you created previously and replace the `AWS_WEB_IDENTITY_TOKEN_FILE` entry with 
```
AWS_WEB_IDENTITY_TOKEN_FILE='/notify_orchestrator/aws_token.conf'
```
This file will be copied to your docker instance if you have a linked volume, which is set up by default.

### Set your Celery Broker Url
As we want Celery to be using the SQS Protocol we need to append the following line to our `.env` file.
```
CELERY_BROKER_URL='sqs://'
```

### Set the Queue Name and URL
To find the SQS Queue URL you will need to login to AWS, you can find how to do this [here](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/getting-started/accessing-the-cloud-console.html).

Once you have logged in make sure your region is set to the region you got from your Kubernetes pod. Ours is 'London' (eu-west-2).

Click 'Simple Queueing Serivce' in the top-left, or search for it if it isn't there.

Find the queue you are looking for by searching for your queue name, in our case `laa-get-access-development-laa_govuk_notify_orchestrator_development_queue.fifo`

Click this and create two envrionment variables in your `.env` file:
```
QUEUE_NAME=[Queue Name from the AWS Console]
QUEUE_URL=[Queue URL from the AWS Console]
```

### Make sure RabbitMQ doesn't start
To ensure RabbitMQ doesn't start when we run `docker_compose` lets append the following line to our `.env` file
```
COMPOSE_PROFILES='SQS'
```