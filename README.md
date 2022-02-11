## Telegram Bot for finding good movies

#### Telegram Bot versions:

:wave:Hello and Welcome,

These are some versions of the bot. You could find it in this repository on the main branch. Telelgram_Bot_v.1.0 is the first commit on the main branch. Telelgram_Bot_v.1.1 is a 43-d commit on the main branch.

:round_pushpin:**Telelgram_Bot_v.1.0** — the simplest Telegram Bot for choosing movies in random order. 

:round_pushpin:**Telelgram_Bot_v.1.1** — have two main functions: random movies and my movies. Random movies function is an ability to list movies in random order. My movies function is the user's library of movies. Users can add movies to their library from random movies.

Check the Bot [here](https://t.me/crisp_cinema_bot).

<br>
<br>

### Deploying by AWS, Terraform, Docker

Also, this project creates and deploys infrastructure on AWS.


#### Before running, you need to deploy with commands:
<br>

:one: You need to open file `terraform.tfvars` and change variables values:

> - `aws_account`
> - `ecr_repository_url`

Replace current **ID** to **your AWS account ID**.

<br>

:two: You need to change `root` directory on `./modules./init-build/` using the command:

> ```md
> cd .\modules\init-build\ # for Windows
> ```
> ```md
> cd ./modules/init-build/ # for Linux
> ```

<br>

:three:  Finally, being in the right directory execute the command:

> ```md
> terraform init
> ```

<br>

#### Main Terraform commands:

```md
terraform plan
``` 

```md
terraform apply
```

```md
terraform destroy
```

