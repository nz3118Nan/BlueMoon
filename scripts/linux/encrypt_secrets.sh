#!/bin/bash

# Set error handling
set -e

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting secrets encryption process...${NC}"

# 1. Check AWS SSO login status
echo -e "\n${GREEN}1. Checking AWS SSO login...${NC}"
aws sts get-caller-identity --profile SoftwareEgnineer-933409076615 > /dev/null 2>&1 || {
    echo -e "${YELLOW}AWS SSO login required. Starting login process...${NC}"
    echo -e "SSO start URL: https://d-9067a439f9.awsapps.com/start/#"
    echo -e "Region: us-east-1\n"
    aws sso login --profile SoftwareEgnineer-933409076615
}

# 2. Check if required files exist
echo -e "\n${GREEN}2. Checking required files...${NC}"
if [ ! -f "secrets_raw.yaml" ]; then
    echo "Error: secrets_raw.yaml not found!"
    exit 1
fi

# 3. Create target directory if it doesn't exist
echo -e "\n${GREEN}3. Creating target directory if not exists...${NC}"
mkdir -p environment-stack/sui-dev

# 4. Encrypt secrets using SOPS with AWS KMS
echo -e "\n${GREEN}4. Encrypting secrets...${NC}"
sops -e \
  --kms arn:aws:kms:us-east-1:933409076615:alias/iac-secrets-encryption-key \
  --aws-profile SoftwareEgnineer-933409076615 \
  secrets_raw.yaml > environment-stack/sui-dev/secrets.yaml

# 5. Verify encrypted file
echo -e "\n${GREEN}5. Verifying encrypted file...${NC}"
if [ -f "environment-stack/sui-dev/secrets.yaml" ]; then
    echo -e "${GREEN}✓ Encryption completed successfully!${NC}"
    echo -e "Encrypted file saved to: environment-stack/sui-dev/secrets.yaml"
else
    echo "Error: Encryption failed!"
    exit 1
fi

# 6. Replace AWS profile name
echo -e "\n${GREEN}6. Updating AWS profile name...${NC}"
sed -i '' 's/SoftwareEgnineer-933409076615/"engineering"/g' environment-stack/sui-dev/secrets.yaml
echo -e "${GREEN}✓ AWS profile name updated successfully!${NC}" 