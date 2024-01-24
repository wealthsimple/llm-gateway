// *****************************************************************************
// llm-gateway - A proxy service in front of llm models to encourage the
// responsible use of AI.

// Copyright 2023 Wealthsimple Technologies

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//   http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// *****************************************************************************

import {
  Role,
  type Models,
  type IRequestBody,
  type OpenAIRequestBody,
  type CohereRequestBody,
  type Settings,
  type ConversationsState,
  type AWSBedrockRequestBody,
} from './app/interfaces';

import { environment as PROD_ENV } from './environments/environment.prod';
import { environment as STAGING_ENV } from './environments/environment.staging';
import { environment as DEV_ENV } from './environments/environment.dev';

const getEnv = () => {
  const appEnv = process.env.REACT_APP_ENV;
  if (appEnv === 'production') {
    return PROD_ENV;
  }

  if (appEnv === 'staging') {
    return STAGING_ENV;
  }

  return DEV_ENV;
};

const appEnv = getEnv();

const OpenAIParseResponse = (response: any) => {
  return response.choices[0].message.content;
};

const CohereParseResponse = (response: any) => {
  return response.data[0];
};

const AWSBedrockLlamaChatParseResponse = (response: any) => {
  return response.generation
}

const AWSBedrockJurassic2TextParseResponse = (response: any) => {
  return response.completions[0].data.text;
}

const AWSBedrockTitanTextParseResponse = (response: any) => {
  return response.results[0].outputText;
}

const AWSBedrockClaudeTextParseResponse = (response: any) => {
  return response.completion;
}

const AWSBedrockCohereTextParseResponse = (response: any) => {
  return response.generations[0].text;
}


const DEFAULT_INITIAL_PROMPT = [
  { role: Role.system, content: 'You are an intelligent assistant.' },
  { role: Role.user, content: 'Hello!' },
  { role: Role.assistant, content: 'Hello! How can I assist you today?' },
];

export const modelChoices: Models = {
  // Cohere models
  cohere: {
    name: 'Cohere - command-light',
    distributor: 'Cohere',
    apiEndpoint: `${appEnv.apiBaseURL}/api/cohere/generate`,
    description: `Select this option to interact with Cohere's command-light model. This is a completion endpoint -- it does not keep message history!`,
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4096,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "Cohere Account",
    advanceMetadata: {
      'Hosted on': 'Cohere Cloud',
      'Inference Hardware': 'GPU',
    },
    requestBody: (req: IRequestBody) =>
      ({
        // Cohere's API requires a prompt field, which is the last message in the conversation.
        prompt: req.messages.at(-1)?.content,
        model: 'command-light',
        temperature: req.temperature,
        // Set the default max tokens to 500.
        max_tokens: 500,
      } as CohereRequestBody),
    responseHandler: CohereParseResponse,
  },
  // OpenAI models
  gpt_3_5_turbo: {
    name: 'GPT 3.5 Turbo',
    distributor: 'OpenAI',
    apiEndpoint: `${appEnv.apiBaseURL}/api/openai/chat_completion`,
    description: `Most capable GPT-3.5 model and optimized for chat.`,
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4096,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "OpenAI Account",
    advanceMetadata: {
      'Hosted on': 'OpenAI Cloud',
      'Inference Hardware': 'GPU',
      'Context window': '16k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        messages: req.messages,
        model: 'gpt-3.5-turbo',
        temperature: req.temperature,
      } as OpenAIRequestBody),
    responseHandler: OpenAIParseResponse,
  },
  gpt_3_5_turbo_16k: {
    name: 'GPT 3.5 Turbo 16k',
    distributor: 'OpenAI',
    apiEndpoint: `${appEnv.apiBaseURL}/api/openai/chat_completion`,
    description:
      'Same capabilities as the standard gpt-3.5-turbo model but with 4 times the token limit.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 16384,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "OpenAI Account",
    advanceMetadata: {
      'Hosted on': 'OpenAI Cloud',
      'Context window': '16k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        messages: req.messages,
        model: 'gpt-3.5-turbo-16k',
        temperature: req.temperature,
      } as OpenAIRequestBody),
    responseHandler: OpenAIParseResponse,
  },
  gpt_4: {
    name: 'GPT 4',
    distributor: 'OpenAI',
    apiEndpoint: `${appEnv.apiBaseURL}/api/openai/chat_completion`,
    description:
      'More capable than GPT-3.5 model, able to do more complex tasks, and optimized for chat',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 8192,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "OpenAI Account",
    advanceMetadata: {
      'Hosted on': 'OpenAI Cloud',
      'Inference Hardware': 'GPU',
      'Context window': '8k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        messages: req.messages,
        model: 'gpt-4',
        temperature: req.temperature,
      } as OpenAIRequestBody),
    responseHandler: OpenAIParseResponse,
  },
  // AWS Bedrock models
  meta_llama2_13b: {
    name: 'Llama 2 13B',
    distributor: 'Meta',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Fine-tuned model in the parameter size of 13B. Suitable for smaller-scale tasks such as text classification, sentiment analysis, and language translation.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4096,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '4k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'meta.llama2-13b-chat-v1',
        max_tokens: 500, // TODO : add model config dialog to remove hardcoded values (i.e max_tokens, temperature, model_kwargs)
        temperature: req.temperature,
        instructions: DEFAULT_INITIAL_PROMPT[0].content,
        model_kwargs: {
          "top_p": 0.9
        },
      } as AWSBedrockRequestBody),
    responseHandler: AWSBedrockLlamaChatParseResponse,
  },
  meta_llama2_70b: {
    name: 'Llama 2 70B',
    distributor: 'Meta',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Fine-tuned model in the parameter size of 70B. Suitable for larger-scale tasks such as language modeling, text generation, and dialogue systems.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4096,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '4k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'meta.llama2-70b-chat-v1',
        max_tokens: 500,
        temperature: req.temperature,
        instruction: DEFAULT_INITIAL_PROMPT[0].content,
        model_kwargs: {
          "top_p": 0.9
        },
      } as AWSBedrockRequestBody),
    responseHandler: AWSBedrockLlamaChatParseResponse,
  },
  ai21_jurassic2_mid: {
    name: 'Jurassic-2 Mid',
    distributor: 'AI21 Labs',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'AI21\'s mid-sized model, designed to strike the right balance between exceptional quality and affordability.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 8192,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '8k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'ai21.j2-mid-v1',
        max_tokens: 4096,
        temperature: req.temperature,
        model_kwargs: {
          "topP": 1,
          "countPenalty":{
            "scale": 0
          },
          "presencePenalty":{
            "scale": 0
          },
          "frequencyPenalty":{
            "scale": 0
          }
        }
      } as AWSBedrockRequestBody),
    responseHandler: AWSBedrockJurassic2TextParseResponse,
  },
  ai21_jurrasic2_ultra: {
    name: 'Jurassic-2 Ultra',
    distributor: 'AI21 Labs',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'AI21\'s most powerful model, offering exceptional quality.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 8192,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '8k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'ai21.j2-ultra-v1',
        max_tokens: 4096,
        temperature: req.temperature,
        model_kwargs: {
          "topP": 1,
          "countPenalty":{
            "scale": 0
          },
          "presencePenalty":{
            "scale": 0
          },
          "frequencyPenalty":{
            "scale": 0
          }
        }
      } as AWSBedrockRequestBody),
      responseHandler: AWSBedrockJurassic2TextParseResponse,
    },
  amazon_titan_light: {
    name: 'Titan Text Light',
    distributor: 'Amazon',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Right-sized for specific use cases, ideal for text generation tasks and fine-tuning.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4000,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '4k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'amazon.titan-text-lite-v1',
        max_tokens: 2000,
        temperature: req.temperature,
        model_kwargs: {
          "stopSequences": [],
          "topP": 1
        }
      } as AWSBedrockRequestBody),
    responseHandler: AWSBedrockTitanTextParseResponse,
  },
  amazon_titan_express: {
    name: 'Titan Text Express',
    distributor: 'Amazon',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'LLM offering a balance of price and performance.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 8000,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '8k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'amazon.titan-text-express-v1',
        max_tokens: 4000,
        temperature: req.temperature,
        model_kwargs: {
          "stopSequences": [],
          "topP": 1
        }
      } as AWSBedrockRequestBody),
    responseHandler: AWSBedrockTitanTextParseResponse,
  },
  anthropic_claude_v1: {
    name: 'Claude 1.3',
    distributor: 'Anthropic',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Claude 1.3 is an earlier version of Anthropic\'s general-purpose LLM.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 100000,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '100k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'anthropic.claude-v1',
        max_tokens: 500,
        temperature: req.temperature,
        model_kwargs: {
          "top_k": 250,
          "top_p": 1,
          "stop_sequences": [
            "\n\nHuman:"
          ],
        }
      } as AWSBedrockRequestBody),
    responseHandler: AWSBedrockClaudeTextParseResponse,
  },
  anthropic_claude_v2: {
    name: 'Claude 2.0',
    distributor: 'Anthropic',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Claude 2.0 is a leading LLM from Anthropic that enables a wide range of tasks from sophisticated dialogue and creative content generation to detailed instruction.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 100000,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '100k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'anthropic.claude-v2',
        max_tokens: 100000,
        temperature: req.temperature,
        model_kwargs: {
          "top_k": 250,
          "top_p": 1,
          "stop_sequences": [
            "\n\nHuman:"
          ],
        }
      } as AWSBedrockRequestBody),
      responseHandler: AWSBedrockClaudeTextParseResponse,
    },
  anthropic_claude_v2_1: {
    name: 'Claude 2.1',
    distributor: 'Anthropic',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Claude 2.1 is Anthropic\'s latest large language model (LLM) with an industry-leading 200K token context window, reduced hallucination rates, and improved accuracy over long documents.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 200000,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '200k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'anthropic.claude-v2:1',
        max_tokens: 200000,
        temperature: req.temperature,
        model_kwargs: {
          "top_k": 250,
          "top_p": 1,
          "stop_sequences": [
            "\n\nHuman:"
          ],
        }
      } as AWSBedrockRequestBody),
      responseHandler: AWSBedrockClaudeTextParseResponse,
    },
  anthropic_claude_instant_v1: {
    name: 'Claude Instant',
    distributor: 'Anthropic',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Claude Instant is Anthropic\'s faster, lower-priced yet very capable LLM.',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 100000,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '100k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'anthropic.claude-instant-v1',
        max_tokens: 100000,
        temperature: req.temperature,
        model_kwargs: {
          "top_k": 250,
          "top_p": 1,
          "stop_sequences": [
            "\n\nHuman:"
          ],
        }
      } as AWSBedrockRequestBody),
      responseHandler: AWSBedrockClaudeTextParseResponse,
    },
  cohere_command_v14: {
    name: 'Command',
    distributor: 'Cohere',
    apiEndpoint: `${appEnv.apiBaseURL}/api/awsbedrock/text`,
    description:
      'Command is Cohere\'s generative large language model (LLM) (52B parameters).',
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4000,
    isSecureModel: false,
    supportFileUpload: false,
    requirements: "AWS Account + Bedrock Enabled",
    advanceMetadata: {
      'Hosted on': 'Amazon Web Services (Bedrock)',
      'Inference Hardware': 'GPU',
      'Context window': '4k',
    },
    requestBody: (req: IRequestBody) =>
      ({
        prompt: req.messages.at(-1)?.content,
        model: 'cohere.command-text-v14',
        max_tokens: 4000,
        temperature: req.temperature,
        model_kwargs: {
          "p": 0.75,
          "k": 0,
          "stop_sequences": [],
          "return_likelihoods": "NONE"
        }
      } as AWSBedrockRequestBody),
    responseHandler: AWSBedrockCohereTextParseResponse,
  },
};

export const CONVERSATION_KEY =
  'llm-gateway-conversation' + (appEnv.production ? '' : '-dev');

export const SETTINGS_KEY = CONVERSATION_KEY + '-settings';

export const DEFAULT_SETTINGS: Settings = {
  model: 'gpt_4',
};

export const DEFAULT_CONVERSATIONS_STATE: ConversationsState = {
  conversations: [],
  selectedConversationId: null,
};

export const RANDOM_LOADING_PHRASES = [
  '*beep bop, beep bop*',
  'Just a moment, pondering...',
  'Give me a second, contemplating...',
  'Thinking cap on, please wait...',
  'Deep in thought, stay tuned...',
];

// This list is used for auto-detecting the language of a code block if OpenAI response does
// not specify the language:
export const COMMON_PROGRAMMING_LANGUAGES = [
  // NOTE: CSS auto-detection is disabled because otherwise it tends to
  // autodetect too many code blocks as CSS:
  // 'css',
  'bash',
  'diff',
  'graphql',
  'java',
  'javascript',
  'json',
  'kotlin',
  'markdown',
  'python',
  'ruby',
  'typescript',
  'hcl',
];

export const DEFAULT_MODEL_TEMP = 0;

export const APP_DESCRIPTION = (
  <>
    <p className="title">
      LLM Gateway{' '}
      <span role="img" aria-label="robot">
        🤖
      </span>
    </p>
    <p style={{ marginBottom: '16px' }}>
      Welcome to our re-creation of ChatGPT using OpenAIs APIs.
    </p>
  </>
);

export const APP_FOOTER = (
  <>
    Made by Wealthsimple with{' '}
    <span role="img" aria-label="love">
      ❤️
    </span>
  </>
);
