---
name: aws
description: Explain AWS infrastructure, EC2 deployment, cloud security, and application hosting.
---

# AWS Skill

## Purpose
Help users understand AWS infrastructure and deployment.

## EC2 deployment workflow
1. Choose an appropriate AMI and instance type.
2. Configure the VPC and subnet.
3. Create or select an SSH key pair.
4. Configure a security group with minimum required access.
5. Launch and connect to the instance.
6. Install application dependencies.
7. Configure environment variables securely.
8. Set up HTTPS and a reverse proxy where appropriate.
9. Monitor logs, security, and costs.

## Security
- Never expose private keys or cloud credentials.
- Avoid opening SSH access to everyone.
- Apply least-privilege IAM policies.
- Stop or terminate unused resources.
