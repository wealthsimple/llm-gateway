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
import { Role } from './app/interfaces';
import { environment } from './environments/environment';

export interface ModelInfo {
  name: string;
  codeName: string;
  distributor: string;
  apiEndpoint: string;
  description: string;
}

export interface Models {
  [key: string]: ModelInfo;
}

export const modelChoices: Models = {
  gpt_3_5_turbo: {
    name: 'GPT 3.5 Turbo',
    codeName: 'gpt-3.5-turbo',
    distributor: 'OpenAI',
    apiEndpoint: `${environment.apiBaseURL}/api/openai/chat_completion`,
    description: '',
  },
  gpt_3_5_turbo_16k: {
    name: 'GPT 3.5 Turbo 16k',
    codeName: 'gpt-3.5-turbo-16k',
    distributor: 'OpenAI',
    apiEndpoint: `${environment.apiBaseURL}/api/openai/chat_completion`,
    description: '',
  },
  gpt_4: {
    name: 'GPT 4',
    codeName: 'gpt-4',
    distributor: 'OpenAI',
    apiEndpoint: `${environment.apiBaseURL}/api/openai/chat_completion`,
    description:
      "GPT-4 is OpenAI's most advanced system, producing safer and more useful responses.",
  },
};

export const CONVERSATION_KEY = 'llm-gateway-conversation';

export const DIALOGUE_DEFAULT_MESSAGE = [
  { role: Role.assistant, content: 'You are an intelligent assistant.' },
  { role: Role.user, content: 'Hello!' },
  { role: Role.assistant, content: 'Hello! How can I assist you today?' },
];

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
];

export const DEFAULT_MODEL_TEMP = 0;
export const APP_DESCRIPTION = 'The Portal to Smarter Conversations - Reliably Connect, Track, and Interact with Large Language Models.';
