

import boto3

ec2 = boto3.client('ec2', region='us-east-1')

INSTANCE_ID = instanceid

def lambda_handler(event,context):
    action=event.get("action")
    if action=='start':
        response=ec2.start_instance(instanceIds(INSTANCE_ID))
        return f"started your instance: {INSTANCE_ID}"
    elif action=='stop':
        response=ec2_stop_instance(instanceIds(INSTANCE_ID))
        return f"stoped your instance : {INSTANCE_ID}"
    else:
        return "nod valid action provide"
    
    
    
    
    
aws events put-rule \
  --name EC2StartAt9AM \
  --schedule-expression "cron(30 3 * * ? *)"


aws events put-rule \
  --name EC2StopAt6PM \
  --schedule-expression "cron(30 12 * * ? *)"
  
  

# Start permission
aws lambda add-permission \
  --function-name MyEC2Lambda \
  --statement-id EC2StartPermission \
  --action "lambda:InvokeFunction" \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:ap-south-1:123456789012:rule/EC2StartAt9AM

# Stop permission
aws lambda add-permission \
  --function-name MyEC2Lambda \
  --statement-id EC2StopPermission \
  --action "lambda:InvokeFunction" \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:ap-south-1:123456789012:rule/EC2StopAt6PM


# Start target
aws events put-targets \
  --rule EC2StartAt9AM \
  --targets "Id"="1","Arn"="arn:aws:lambda:ap-south-1:123456789012:function:MyEC2Lambda","Input"="{\"action\":\"start\"}"

# Stop target
aws events put-targets \
  --rule EC2StopAt6PM \
  --targets "Id"="2","Arn"="arn:aws:lambda:ap-south-1:123456789012:function:MyEC2Lambda","Input"="{\"action\":\"stop\"}"
