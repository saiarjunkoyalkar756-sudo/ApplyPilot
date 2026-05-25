provider "aws" {
  region = var.region
}

module "vpc" {
  source = "./modules/vpc"
  name   = "job-copilot-vpc"
}

module "eks" {
  source     = "./modules/eks"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
}

module "rds" {
  source     = "./modules/rds"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
}

module "s3" {
  source = "./modules/s3"
  bucket_name = "job-copilot-resumes"
}
