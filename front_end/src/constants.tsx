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

const DEFAULT_INITIAL_PROMPT = [
  { role: Role.system, content: 'You are an intelligent assistant.' },
  { role: Role.user, content: 'Hello!' },
  { role: Role.assistant, content: 'Hello! How can I assist you today?' },
];

export const modelChoices: Models = {
  cohere: {
    name: 'Cohere - command-light',
    distributor: 'Cohere',
    apiEndpoint: `${appEnv.apiBaseURL}/api/cohere/generate`,
    description: `Select this option to interact with Cohere's command-light model. This is a completion endpoint -- it does not keep message history!`,
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4096,
    isSecureModel: false,
    supportFileUpload: false,
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
  gpt_3_5_turbo: {
    name: 'GPT 3.5 Turbo',
    distributor: 'OpenAI',
    apiEndpoint: `${appEnv.apiBaseURL}/api/openai/chat_completion`,
    description: `Most capable GPT-3.5 model and optimized for chat.`,
    initialPrompt: DEFAULT_INITIAL_PROMPT,
    maxTokensLimit: 4096,
    isSecureModel: false,
    supportFileUpload: false,
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
