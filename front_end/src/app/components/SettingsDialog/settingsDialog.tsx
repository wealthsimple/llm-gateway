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

import React from 'react';
import { modelChoices } from '../../../constants';

interface Props {
  model: string;
  setModel: (arg: string) => void;
  showSettings: boolean;
  setShowSettings: (arg: boolean) => void;
}

export const ModelSettingsDialog: React.FC<Props> = ({
  model,
  setModel,
  showSettings,
  setShowSettings,
}) => {
  const triggerChangeModel = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newModel = event.target.value;
    setModel(newModel);
  };
  return (
    <dialog open={showSettings}>
      <article>
        <header>
          <a
            href="#close"
            aria-label="Close"
            className="close"
            onClick={() => setShowSettings(false)}
          ></a>
          Settings
        </header>

        <div id="model-selector">
          Model
          <select
            name="selectList"
            id="selectList"
            onChange={triggerChangeModel}
            value={model}
          >
            {Object.entries(modelChoices).map(([key, value]) => (
              <option key={key} value={key}>
                {value.name}
              </option>
            ))}
          </select>
        </div>
      </article>
    </dialog>
  );
};
