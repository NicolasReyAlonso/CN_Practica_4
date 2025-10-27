aws cloudformation create-stack \
  --stack-name MiDBStack \
  --template-body file://db.yaml \
  --parameters ParameterKey=DBName,ParameterValue=tickets \
               ParameterKey=DBUser,ParameterValue=admin \
               ParameterKey=DBPassword,ParameterValue=Nicololo \
               ParameterKey=SubnetIds,ParameterValue="" \
               ParameterKey=VpcId,ParameterValue=vpc-0cc4b8ec2faadc305 