# llm-gateway

## Cohere

### Setup

*This setup requires a Cohere account. If you do not have a Cohere account, you can create one [here](https://cohere.ai/).*

### Available Models



## OpenAI

### Setup

*This setup requires an OpenAI account. If you do not have an OpenAI account, you can create one [here](https://beta.openai.com/).*

### Available Models





## AWS Bedrock

### Setup

*This setup requires an Amazon Web Services (AWS) account. If you do not have an AWS account, you can create one [here](https://aws.amazon.com/).*

*Steps 1 and 2 are to configure the AWS CLI for boto3. If you already have the AWS CLI configured, you can skip to step 3.*

1. Install the AWS CLI. OS-specific installation instructions can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
2. Setup the AWS CLI. Setup instructions can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config).
3. Enable Amazon Bedrock on your AWS account using the AWS Console.
4. Within Amazon Bedrock in the AWS Console, select `Model access` > `Manage Model Access`, and enable the LLM models you want to use. </br> **Pricing information for models offered on Amazon Bedrock can be found** [here](https://aws.amazon.com/bedrock/pricing/).
5. Set the `AWS_REGION` environment variable to the region in which Amazon Bedrock is enabled on your AWS account </br> **(i.e AWS_REGION=us-east-1)**.

### Available Models

**AI21 Labs**
- Jurrasic-2 Ultra
- Jurassic-2 Mid

**Amazon**
- Titan Text Lite
- Titan Text Express
- Titan Text Embeddings
- Titan Image Generator

**Anthropic**
- Claude 2.1
- Claude 2.0
- Claude 1.3
- Claude Instant

**Cohere**
- Command
- Command Light
- Embed - English
- Embed - Multilingual

**Meta**
- Llama-2-13b-chat
- Llama-2-70b-chat

**Stable Diffusion**
- Stable Diffusion XL 1.0
- Stable Diffusion XL 0.8
