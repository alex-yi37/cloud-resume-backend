# someone else's repo for the aws cloud resume challenge https://github.com/jlewis92/ResumeProject-backend/tree/main
# they include the terraform {} block and set the required_providers {} block there, and in main.tf they
# define variable {} blocks and also configure the provider "aws" {} block  
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      # provider version
      # as of 10/28/2024, the aws provider's latest release is v5.73.0 so I'll use that
      version = "~> 5.73"
    }
  }

  # terraform version?
  # see version constraint syntax here https://developer.hashicorp.com/terraform/language/expressions/version-constraints
  # as of writing this file, when I run "terraform --version" in my cli it outputs Terraform v1.9.8
  # so I will require at least version 1.9.8 and above, allowing version 2 and up
  # if i used "~> 1.9.8", that would mean it would only allow 1.9.9 to 1.9.10 (minor version can change) but not anything
  # past that
  required_version = ">= 1.9.8"
}

provider "aws" {
  region  = "us-east-1"
  profile = "dev-ebi-sso"
}

# see import id docs for aws provider docs for s3 buckets
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket#import
import {
  to = aws_s3_bucket.www_bucket
  id = "www.alex-cloud-resume.info"
}
resource "aws_s3_bucket" "www_bucket" {
  bucket = "www.alex-cloud-resume.info"
  tags = {
    Project = "alex-cloud-resume"
  }
}

import {
  to = aws_s3_bucket.root_bucket
  id = "alex-cloud-resume.info"
}
resource "aws_s3_bucket" "root_bucket" {
  bucket = "alex-cloud-resume.info"
  tags = {
    Project = "alex-cloud-resume"
  }
}

# should I try to host my terraform state in a remote backend or locally?
# if totally local, I believe I would not push terraform state files to github. Would I be able to
# download git repo to different computer and run "terraform init" to be able to work with my infra from a
# different computer? Or would I only be able to access the state on the computer where I initially ran terraform init?

# resources as described by cloud resume challenge section on using terraform for infra:

# s3 buckets - there are two buckets, one for www and one for apex domain that redirects to www bucket
# - would there be conflicts if I tried to create another s3 bucket with the same name as existing one since names are supposed
# - to be globally unique?
# - imported the www and root buckets and added tag 'Project = "alex-cloud-resume"' to both of them

# https infra - i don't remember which aws service this is. Certificate Manager?
# dns infra? - I did some stuff in route53 (honestly don't remember what) but I bought my domain through namecheap
# dynamodb - assume it's not possible to make multiple tables with the same name
# lambda
# api gateway
# others? - should I set up vpc, internet gateway, etc in terraform? each aws account has a vpc set up by default I think
# - should reuse default vpc created with my aws account?
# logging? cloudwatch? cloudtrail?
# iam? roles, policies, etc? need lambda to assume a role that has a certian policy to read/update dynamodb?


