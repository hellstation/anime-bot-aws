![Bot Interface](image.png)

Interactive Telegram bot for anime search and automatic notifications about new episodes.

## ✨ Features

- 🔍 **Anime Search** - just type anime name in English
- 📺 **Auto Notifications** - alerts for new episodes every hour
- 🎯 **Detailed Info** - status, episodes, genres, rating, description
- ☁️ **Cloud-native** - runs on AWS ECS Fargate
- 🔐 **Secure Storage** - secrets in AWS Secrets Manager
- 🚀 **CI/CD** - automated deployment via GitHub Actions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │◄──►│   AniList API   │    │   AWS Services  │
│                 │    │                 │    │                 │
│ • Interactive   │    │ • Anime search  │    │ • ECS Fargate   │
│   messages      │    │ • Info & data   │    │ • Secrets Mgr   │
│ • Notifications │    │ • New episodes  │    │ • CloudWatch    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- AWS account with admin permissions
- Telegram bot token ([create with @BotFather](https://t.me/botfather))
- GitHub account for CI/CD

## 🚀 Quick Start

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

#### Find VPC and Subnets
1. Go to **AWS Console → VPC → Subnets**
2. Select **2 subnets from same VPC** in `eu-north-1` region
3. Copy **Subnet ID** (e.g.: `subnet-12345678`)

#### Create Security Group
1. Go to **AWS Console → EC2 → Security Groups**
2. **Create security group**:
   - Name: `anime-notifier-sg`
   - VPC: select VPC from previous step
   - Inbound rules: add `All traffic` (for testing)

### 3. Configure GitHub Secrets

Go to **GitHub → Repository → Settings → Secrets and variables → Actions**

Add these secrets:

| Secret | Description | Where to get |
|--------|-------------|--------------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key ID | AWS Console → IAM → Users → Security credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Access Key | AWS Console → IAM → Users → Security credentials |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | @BotFather → /newbot |
| `TELEGRAM_CHAT_ID` | Chat ID for notifications | Send message to bot, then `https://api.telegram.org/bot<TOKEN>/getUpdates` |
| `SUBNET_1` | First subnet ID | AWS Console → VPC → Subnets |
| `SUBNET_2` | Second subnet ID | AWS Console → VPC → Subnets (same VPC) |
| `SECURITY_GROUP_ID` | Security Group ID | AWS Console → EC2 → Security Groups |

### 4. Deploy

```bash
# Push to main branch
git add .
git commit -m "Initial deployment"
git push origin main
```

GitHub Actions automatically:
1. ✅ Validates code
2. ✅ Creates S3 bucket (if needed)
3. ✅ Runs Terraform (plan + apply)
4. ✅ Builds Docker image
5. ✅ Pushes to ECR
6. ✅ Updates ECS service

### 5. Test

#### In Telegram:
- Send `/start` to bot - get welcome message
- Send anime name: `Naruto`, `Death Note`, `One Piece`
- Bot sends detailed information

#### In AWS Console:
- **ECS → Clusters** - check `anime-cluster`
- **CloudWatch → Log groups** - logs in `/ecs/anime-notifier`
- **Secrets Manager** - secrets in `anime-notifier-secrets`

## 📱 Usage

### Commands:
- `/start` - welcome message
- `/help` - help commands
- `/anime [name]` - search anime

### Examples:
```
Naruto
/anime Attack on Titan
Death Note
/anime My Hero Academia
```

### Response Format:
```
🎬 Attack on Titan

📊 Status: Finished
📅 Season: Fall 2013
🎞️ Episodes: 87
🏷️ Genres: Action, Drama, Suspense
⭐ Score: 95/100
📺 Next Episode: - (finished)

📝 Description:
Several hundred years ago, humans were nearly...
```

## 🛠️ Project Structure

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

## 🔧 Development

### Local Testing:

```bash
# Fill environment variables
cp .env.example .env

# Run with Docker Compose
docker-compose up --build
```

## 🔒 Security

- 🔐 **Secrets Manager** - tokens stored in AWS Secrets Manager
- 🚫 **No hardcode** - all secrets in variables
- 🔑 **IAM roles** - minimal required permissions
- 📊 **Logging** - all actions logged in CloudWatch

## 📊 Monitoring

- **CloudWatch Logs** - app logs
- **CloudWatch Metrics** - ECS metrics
- **ECS Service** - container status
- **GitHub Actions** - deployment status
