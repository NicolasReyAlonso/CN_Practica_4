aws cloudformation create-stack \
  --stack-name MiDBStack \
  --template-body file://db.yaml \
  --parameters ParameterKey=DBName,ParameterValue=tickets \
               ParameterKey=DBUser,ParameterValue=admin \
               ParameterKey=DBPassword,ParameterValue=Nicololo \
               ParameterKey=SubnetIds,ParameterValue="subnet-0434313f93540400e,subnet-0ead6bed5978c2748,subnet-068de7ffb26d81cb6,subnet-0a935f102748c575f,subnet-01a43dd43ab0714c0,subnet-0758e7636ce16a70e" \
               ParameterKey=VpcId,ParameterValue=vpc-0cc4b8ec2faadc305 