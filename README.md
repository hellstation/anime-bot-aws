#  anime-bot-aws
![Bot Interface](image.png)

##  Features

-  **Intelligent Anime Search** - Search by English titles with fuzzy matching
-  **Automated Notifications** - Hourly checks for new episodes across followed anime
-  **Comprehensive Information** - Status, episodes, genres, ratings, and detailed descriptions
-  **Serverless Architecture** - Fully managed AWS ECS Fargate deployment
-  **Secure Secrets Management** - AWS Secrets Manager for sensitive data
-  **Automated CI/CD** - GitHub Actions for seamless deployment
-  **Real-time Monitoring** - CloudWatch logs and metrics
-  **Infrastructure as Code** - Terraform modules for reproducible deployments

##  Technologies

- **Backend**: Python 3.9+
- **Bot Framework**: Custom Telegram Bot API integration (requests)
- **API Integration**: AniList GraphQL API
- **Infrastructure**: Terraform, AWS (ECS, ECR, VPC, Secrets Manager)
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **State Management**: JSON file-based persistence

##  Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │◄──►│   AniList API   │    │   AWS Services  │
│                 │    │                 │    │                 │
│ • Interactive   │    │ • Anime search  │    │ • ECS Fargate   │
│   messages      │    │ • Info & data   │    │ • Secrets Mgr   │
│ • Notifications │    │ • New episodes  │    │ • CloudWatch    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

##  Prerequisites

- AWS account with admin permissions
- Telegram bot token ([create with @BotFather](https://t.me/botfather))
- GitHub account for CI/CD

##  Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-username/anime-release-notifier.git
cd anime-release-notifier
```

### 2. Setup AWS (complete in order)

#### Create S3 Bucket for Terraform
```bash
aws s3 mb s3://anime-notifier-terraform-state --region eu-north-1
aws s3api put-bucket-versioning \
  --bucket anime-notifier-terraform-state \
  --versioning-configuration Status=Enabled
```



### 3. Configure GitHub Secrets

Go to **GitHub → Repository → Settings → Secrets and variables → Actions**

Add these secrets:

| Secret | Description | Where to get |
|--------|-------------|--------------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key ID | AWS Console → IAM → Users → Security credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Access Key | AWS Console → IAM → Users → Security credentials |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | @BotFather → /newbot |
| `TELEGRAM_CHAT_ID` | Chat ID for notifications | Send message to bot, then `https://api.telegram.org/bot<TOKEN>/getUpdates` |

### 4. Deploy

```bash
# Push to main branch
git add .
git commit -m "Initial deployment"
git push origin main
```

GitHub Actions automatically:
1.  Validates code
2.  Creates S3 bucket (if needed)
3.  Runs Terraform (plan + apply)
4.  Builds Docker image
5.  Pushes to ECR
6.  Updates ECS service

### 5. Test

#### In Telegram:
- Send `/start` to bot - get welcome message
- Send anime name: `Naruto`, `Death Note`, `One Piece`
- Bot sends detailed information

#### In AWS Console:
- **ECS → Clusters** - check `anime-cluster`
- **CloudWatch → Log groups** - logs in `/ecs/anime-notifier`
- **Secrets Manager** - secrets in `anime-notifier-secrets`

##  Usage

### Commands:
- `/start` - welcome message
- `/help` - help commands
- `/anime [name]` - search anime

### Examples:
```
Naruto
/anime Attack on Titan
/anime My Hero Academia
```

### Response Format:
```
 Attack on Titan

 Status: Finished
 Season: Fall 2013
 Episodes: 87
 Genres: Action, Drama, Suspense
 Score: 95/100
 Next Episode: - (finished)

 Description:
Several hundred years ago, humans were nearly...
```

##  Project Structure

```
├── app/                    # Python app
│   ├── main.py            # Main bot logic
│   ├── telegram.py        # Telegram API integration
│   ├── anilist.py         # AniList API client
│   ├── state.py           # State management
│   └── requirements.txt   # Python dependencies
├── infra/                 # Terraform infrastructure
│   ├── main.tf           # Main config
│   ├── backend.tf        # S3 backend
│   ├── variables.tf      # Variables
│   ├── outputs.tf        # Outputs
│   └── modules/          # Terraform modules
│       ├── network/      # VPC, subnets, security groups
│       ├── secrets/      # AWS Secrets Manager
│       ├── ecr/          # Elastic Container Registry
│       ├── ecs/          # ECS Fargate
│       ├── iam/          # IAM roles
│       ├── logs/         # CloudWatch logs
│       └── eventbridge/  # EventBridge (removed)
├── docker/               # Docker config
├── .github/workflows/    # GitHub Actions CI/CD
└── README.md            # This documentation
```

##  Development

### Local Testing:

```bash
# Fill environment variables
cp .env.example .env

# Run with Docker Compose
docker-compose up --build
```

##  Security

-  **Secrets Manager** - tokens stored in AWS Secrets Manager
-  **No hardcode** - all secrets in variables
-  **IAM roles** - minimal required permissions
-  **Logging** - all actions logged in CloudWatch

##  Monitoring

- **CloudWatch Logs** - app logs
- **CloudWatch Metrics** - ECS metrics
- **ECS Service** - container status
- **GitHub Actions** - deployment status
