# llm-gateway

## Cohere

### Setup

*This setup requires a Cohere account. If you do not have a Cohere account, you can create one [here](https://cohere.ai/).*

1. Login to your Cohere account and select `API keys` to view your API keys.
2. If you do not have an existing API key, select `Create Trial key` to create one.
3. Within llm-gateway, set the `COHERE_API_KEY` environment variable to your API key.

### Available Models

- Command Light

## OpenAI

### Setup

*This setup requires an OpenAI account. If you do not have an OpenAI account, you can create one [here](https://beta.openai.com/).*

1. Login to your OpenAI account and navigate to the API page.
2. Select `API keys` to view your API keys.
2. If you do not have an existing API key, select `Create new secret key` to create one.
3. Within llm-gateway, set the `OPENAI_API_KEY` environment variable to your API key.

### Available Models

- GPT 3.5 Turbo
- GPT 3.5 Turbo 16k
- GPT 4

## AWS Bedrock

### Setup

*This setup requires an Amazon Web Services (AWS) account. If you do not have an AWS account, you can create one [here](https://aws.amazon.com/).*

1. Enable Amazon Bedrock on your AWS account using the AWS Console.
2. Within Amazon Bedrock in the AWS Console, select `Model access` > `Manage Model Access`, and enable the LLM models you want to use. </br> **Pricing information for models offered on Amazon Bedrock can be found** [here](https://aws.amazon.com/bedrock/pricing/).
3. Within llm-gateway, set the `AWS_REGION` environment variable to the region in which Amazon Bedrock is enabled on your AWS account.
4. Within llm-gateway, set the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables to the access key ID and secret access key of the AWS account you enabled Amazon Bedrock on.

### Available Models

**AI21 Labs**
- Jurrasic-2 Ultra
- Jurassic-2 Mid

**Amazon**
- Titan Text Lite
- Titan Text Express
- Titan Text Embeddings

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
