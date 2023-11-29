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

export enum Role {
  assistant = 'assistant',
  user = 'user',
  system = 'system',
}

export interface Message {
  role: Role;
  content: string;
}

export interface IRequestBody {
  messages: Message[];
  model: string;
  temperature: number;
  uploadedFile?: File;
  filename?: string;
}

export interface ModelInfo {
  name: string;
  distributor: string;
  apiEndpoint: string;
  description: string;
  maxTokensLimit: number;
  isSecureModel: boolean;
  advanceMetadata: ModelMetadata;
  supportFileUpload: boolean;
  initialPrompt: Message[];
  requestBody: (req: IRequestBody) => OpenAIRequestBody | CohereRequestBody;
  responseHandler: (res: any) => string;
}

export interface OpenAIRequestBody {
  messages: Message[];
  model: string;
  temperature: number;
}

export interface CohereRequestBody {
  temperature: number;
  prompt: string;
  max_tokens: number;
  model: string;
}

interface ModelMetadata {
  [key: string]: string;
}

export interface Models {
  [key: string]: ModelInfo;
}

export interface Settings {
  model: string;
}

export interface Conversation {
  title: string;
  messages: Message[];
  model: string;
  id: number;
}

export interface ConversationsState {
  conversations: Conversation[];
  selectedConversationId: number | null;
}
