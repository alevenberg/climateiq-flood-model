# Terraform for the flood modeling

This directory includes terraform to setup 3 GCP Storage buckets for flood modeling.

## Using Terraform 
### Pre-reqs

Install [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

### Applying the infrastructure

1. Initialize Terraform
```
cd terraform
terraform init
```

2. Create a plan
```
terraform plan -var-file "vars/dev.tfvars"  -out=tfplan_dev
```

To update the prod env:
```
terraform plan -var-file "vars/prod.tfvars"  -out=tfplan_prod
```

If you want to update a separate project, you can create a corresponding "vars/{env}.tfvars" file.

3. Apply the plan
```
terraform apply "tfplan_dev"
```

To update the prod env:
```
terraform apply "tfplan_prod"
```

### Destroy the infrastructure
To remove the resources:
```
terraform destroy  -var-file "vars/dev.tfvars"                      
```

Type "yes" if this is the correct action.

### Development notes
<details>
  <summary>Format the files</summary>
```
terraform fmt
```
</details>

<details>
  <summary>Validate the config</summary>
```
terraform validate
```         

</details>
