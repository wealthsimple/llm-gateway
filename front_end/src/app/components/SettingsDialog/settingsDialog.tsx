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

import React, { useState, useRef } from 'react';
import Papa from 'papaparse';
import { DEFAULT_SETTINGS, modelChoices } from '../../../constants';
import { type Message, type Role } from '../../interfaces';

interface Props {
  showSettings: boolean;
  setShowSettings: (arg: boolean) => void;
  createNewConversation: (
    title: string,
    model: string,
    existingConversations: Message[],
  ) => void;
}

interface CSVRow {
  id: number;
  role: string;
  content: string;
}

enum ErroMessage {
  notCSV = "Error loading file, please ensure the file is a .csv file and contains the columns 'role', 'content'",
  secureModelsOnly = 'Previous chats can only be uploaded to secure models, file is removed.',
  missingColumns = "'role' or 'content' columns are missing",
}

const notSecureModelNames = Object.entries(modelChoices)
  .filter(([, val]) => !val.isSecureModel)
  .map(([k]) => k);

export const ModelSettingsDialog: React.FC<Props> = ({
  showSettings,
  setShowSettings,
  createNewConversation,
}) => {
  const [selectedOption, setSelectedOption] = useState(DEFAULT_SETTINGS.model);
  const [csvError, setCSVError] = useState('');
  const [newTitle, setNewTitle] = useState('');
  const csvFileRef = useRef<HTMLInputElement>(null);
  const [csvConversations, setCSVConversations] = useState<Message[]>([]);

  const createConversation = () => {
    let title = newTitle.trim();
    if (!title) {
      title = "Untitled Chat";
    }
    createNewConversation(title, selectedOption, csvConversations);
    closeModal();
  };

  const triggerChangeModel = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newSelection = event.target.value;
    if (notSecureModelNames.includes(newSelection) && csvFileRef.current) {
      if (csvFileRef.current.value) {
        resetCSVFile(true);
        setCSVError(ErroMessage.secureModelsOnly);
      }
    } else {
      setCSVError('');
    }
    setSelectedOption(newSelection);
  };

  const resetCSVFile = (removeConversations: boolean) => {
    if (removeConversations) {
      setCSVConversations([]);
    }
    if (csvFileRef.current) {
      if (csvFileRef.current.value) {
        csvFileRef.current.value = '';
      }
    }
  };

  const closeModal = () => {
    setShowSettings(false);
    setNewTitle('');
    setSelectedOption(DEFAULT_SETTINGS.model);
    resetCSVFile(false);
    setCSVError('');
  };

  const handleLoadCSV = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = (event.target as HTMLInputElement).files?.[0];

    if (!selectedFile || (selectedFile && !selectedFile.name.endsWith('csv'))) {
      setCSVError(ErroMessage.notCSV);
      return;
    }
    if (notSecureModelNames.includes(selectedOption)) {
      setCSVError(ErroMessage.secureModelsOnly);
      resetCSVFile(true);
      return;
    }
    setCSVError('');

    Papa.parse<CSVRow>(selectedFile, {
      header: true,
      delimiter: ',',
      quoteChar: '"',
      skipEmptyLines: true,
      error: (e) => setCSVError(e.message),
      complete: function (results) {
        const data = results.data;
        const uploadedMessages: Message[] = [];
        data.forEach(({ role, content }) => {
          if (role && content) {
            const message: Message = {
              role: role as Role,
              content: content,
            };
            uploadedMessages.push(message);
          } else {
            setCSVError(ErroMessage.missingColumns);
            resetCSVFile(true);
            return;
          }
        });
        setCSVConversations(uploadedMessages);
      },
    });
  }

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
        <div>
          <label>(Optional) Upload Previous Chats</label>
          {csvError && <p className="error-message">{csvError}</p>}
          <input
            type="file"
            placeholder="Chat Title"
            onChange={handleLoadCSV}
            ref={csvFileRef}
          />
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
