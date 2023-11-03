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

import axios, { AxiosError, AxiosResponse } from 'axios';
import { modelChoices } from '../constants';
import { Message } from '../app/interfaces';

interface ModelRequestBody {
  messages: Message[];
  model: string;
  temperature: number;
}

export async function fetchResponseFromModel(
  modelName: string,
  messageHistory: Message[],
  modelTemperature: number,
): Promise<string> {
  const requestBody: ModelRequestBody = {
    messages: messageHistory,
    model: modelChoices[modelName].codeName,
    temperature: modelTemperature,
  };
  const url: string = modelChoices[modelName].apiEndpoint;
  try {
    const res: AxiosResponse = await axios.post(url, requestBody);
    return res.data.choices[0].message.content;
  } catch (error) {
    const err = error as AxiosError;
    const errResponse = err.response as AxiosResponse;

    if (err.message && errResponse) {
      throw new Error(`${err.message}: ${errResponse.data.error.message}`);
    }
    if (err.message) {
      throw new Error(`${err.message}`);
    }
    throw new Error('Something went wrong - check console for details.');
  }
}
