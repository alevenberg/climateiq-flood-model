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

## Bucket structure
There are 3 buckets this terraform creates: input, config, and output

The following buckets except the following structure:

### Input bucket
- CityCat.exe
- study_area1
  - Buildings.txt
  - Domain_DEM.asc
  - GreenAreas.txt
- manhattan
  - Buildings.txt
  - Domain_DEM.asc
  - GreenAreas.txt

### Configuration bucket
- config 1
  - CityCat_Config_1.txt
  - CityCat_Config_2.txt
  - Rainfall_Data_11.txt
  - Rainfall_Data_12.txt
  - config.txt

Where config.txt stores the configuration of runs. For example, a `config.txt` as follows
```
1, 11
1, 12
2, 11
2, 11
```
produces 4 runs of CityCat.exe -r X -c Y, where X is the first value and Y is the second.

### Output bucket
  - R11C1_StudyArea1.zip


