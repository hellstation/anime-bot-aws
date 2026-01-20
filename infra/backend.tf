terraform {
  backend "s3" {
    bucket = "anime-notifier-terraform-state"
    key    = "state"
    region = "eu-north-1"
  }
}
