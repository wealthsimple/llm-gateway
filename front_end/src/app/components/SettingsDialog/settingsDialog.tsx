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
import { DEFAULT_SETTINGS, modelChoices } from '../../../constants';

interface Props {
  showSettings: boolean;
  setShowSettings: (arg: boolean) => void;
  createNewConversation: (title: string, model: string) => void;
}

export const ModelSettingsDialog: React.FC<Props> = ({
  showSettings,
  setShowSettings,
  createNewConversation,
}) => {
  const [selectedOption, setSelectedOption] = useState(DEFAULT_SETTINGS.model);
  const [newTitle, setNewTitle] = useState('');

  const createConversation = () => {
    let title = newTitle.trim();
    if (!title) {
      title = "Untitled Chat";
    }
    createNewConversation(title, selectedOption);
    closeModal();
  };

  const triggerChangeModel = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newSelection = event.target.value;
    setSelectedOption(newSelection);
  };

  const closeModal = () => {
    setShowSettings(false);
    setNewTitle('');
    setSelectedOption(DEFAULT_SETTINGS.model);
  };

  return (
    <dialog open={showSettings}>
      <article>
        <div className="settings-dialog-title">
          <h3>Create New Chat</h3>
        </div>
        <div>
          <input
            type="text"
            value={newTitle}
            placeholder="Chat Title"
            onChange={(e) => setNewTitle(e.target.value)}
          />
        </div>
        <div id="model-selector">
          <select
            name="selectList"
            id="selectList"
            onChange={triggerChangeModel}
            value={selectedOption}
            className="dropdown"
          >
            <optgroup label="Self Hosted Models (Secured)">
              {Object.entries(modelChoices).map(
                ([key, value]) =>
                  value.isSecureModel && (
                    <option key={key} value={key}>
                      {value.name}
                    </option>
                  ),
              )}
            </optgroup>
            <optgroup label="Public Models">
              {Object.entries(modelChoices).map(
                ([key, value]) =>
                  !value.isSecureModel && (
                    <option key={key} value={key}>
                      {value.name}
                    </option>
                  ),
              )}
            </optgroup>
          </select>
        </div>
        <p>{modelChoices[selectedOption].description}</p>
        <p>
          <details open>
            <summary>Basic Information</summary>
            <ul id="hello">
              <li>
                <b>
                  <span role="img" aria-label="plug">
                    🔌
                  </span>{' '}
                  Provider:{' '}
                </b>{' '}
                {modelChoices[selectedOption].distributor} <br />
              </li>
              <li>
                <b>
                  <span role="img" aria-label="blink">
                    ❇️
                  </span>{' '}
                  Max Tokens:{' '}
                </b>
                {modelChoices[selectedOption].maxTokensLimit} tokens <br />
              </li>
              <li>
                <b>
                  <span role="img" aria-label="blink">
                    ⚙️
                  </span>{' '}
                  Requirements:{' '}
                </b>
                {modelChoices[selectedOption].requirements} <br />
              </li>
            </ul>
          </details>
          <details>
            <summary>Advanced Information</summary>
            <ul>
              {Object.entries(modelChoices[selectedOption].advanceMetadata).map(
                ([key, value]) => (
                  <li key={key}>
                    {' '}
                    <b>{key}:</b> {value}{' '}
                  </li>
                ),
              )}
            </ul>
          </details>
          <br />
        </p>
        <footer>
          <a
            href="#cancel"
            role="button"
            className="secondary-btn"
            onClick={() => closeModal()}
          >
            Cancel
          </a>
          <a
            href="#confirm"
            role="button"
            className="primary-btn"
            onClick={() => {
              createConversation();
            }}
          >
            Create Chat
          </a>
        </footer>
      </article>
    </dialog>
  );
};
