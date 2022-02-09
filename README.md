# Telegram Bot for movies search
<br>

## Developing by Python

:wave:Hello and Welcome,

### Telegram Bot versions:

:round_pushpin:**Telelgram_Bot_v.1.0** — the simplest Telegram Bot for choosing movies in random order. 

:round_pushpin:**Telelgram_Bot_v.1.1** — have two main functions: random movies and my movies. Random movies function is an ability to list movies in random order. My movies function is the user's library of movies. Users can add movies to their library from random movies.
Check it [here](https://t.me/crisp_cinema_bot).
<br>

## Deploying by AWS, Terraform, Docker

Hello, this project create and deploy infrastructure on AWS.

### Before running deployment commands:

> You need to open file `terraform.tfvars` and change
variables values:
> - `aws_account`
> - `ecr_repository_url`
>
> Replace current **ID** to **your AWS account ID**
<br>

> Also you need change `root` directory
> on './modules./init-build/' using command:
> ```md
> cd .\modules\init-build\ # for Windows
> ```
> ```md
> cd ./modules/init-build/ # for Linux
> ```
<br>

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

