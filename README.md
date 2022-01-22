# Telegram Bot for movies search
## Developing by Python
## Deploying by AWS, Terraform, Docker

:wave:Hello and Welcome,

### Our branches:

:round_pushpin:**Telelgram_Bot_v.1.0** — the simplest Telegram Bot for choosing movies in random order. 
Check it [here](https://t.me/crisp_cinema_bot).

---

Hello, this project create and deploy
infrastructure on AWS

### Before running deployment commands:

> You need to open file `terraform.tfvars` and change
variables values:
> - `aws_account`
> - `ecr_repository_url`
>
> Replace current **ID** to **your AWS account ID**

> Also you need change `root` directory
> on './modules./init-build/' using command:
> ```md
> cd .\modules\init-build\ # for Windows
> ```
> ```md
> cd ./modules/init-build/ # for Linux
> ```

> Finally, being in the right directory
> execute command:
> ```md
> terraform init
> ```

### Main Terraform commands:

```md
terraform plan
``` 

```md
terraform apply
```

```md
terraform destroy
```
