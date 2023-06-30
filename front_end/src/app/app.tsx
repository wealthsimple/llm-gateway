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

import React, { useState } from 'react';
import { modelChoices, DEFAULT_MODEL_TEMP, APP_DESCRIPTION} from '../constants';
import { ChatBoxComponent } from './components/ChatBox';
import { ModelSettingsDialog } from './components/SettingsDialog';

export function App(): JSX.Element {
  const allModelsKeys = Object.keys(modelChoices);
  const [model, setModel] = useState(allModelsKeys[0]);
  const temperature = DEFAULT_MODEL_TEMP;
  const description = APP_DESCRIPTION;
  const [showSettings, setShowSettings] = useState(false);

  return (
    <>
      <main className="container">
        <div id="title">
          <h1>LLM Gateway</h1>
        </div>

        <p>{description}</p>

        <ChatBoxComponent
          modelName={model}
          modelTemperature={temperature}
          setShowSettings={setShowSettings}
        />

        <br></br>

        <hr></hr>

        <p>
          Made by Wealthsimple with{' '}
          <span role="img" aria-label="love">
            ❤️
          </span>
        </p>
      </main>
      <ModelSettingsDialog
        model={model}
        setModel={setModel}
        showSettings={showSettings}
        setShowSettings={setShowSettings}
      />
    </>
  );
}
