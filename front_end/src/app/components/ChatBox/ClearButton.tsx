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
import { CONVERSATION_KEY } from '../../../constants';

interface ClearButtonProps {
  onClear: () => void;
}

// eslint-disable-next-line @typescript-eslint/ban-types
export const ClearButton: React.FC<ClearButtonProps> = ({ onClear }) => {
  const [showConfirmationDialog, setShowConfirmationDialog] = useState(false);

  const clearConversation = () => {
    localStorage.removeItem(CONVERSATION_KEY);
    onClear();
    setShowConfirmationDialog(false);
  };

  const openConfirmation = () => {
    setShowConfirmationDialog(true);
  };

  const closeConfirmation = () => {
    setShowConfirmationDialog(false);
  };

  return (
    <>
      <button onClick={openConfirmation}>Clear Conversation</button>

      {showConfirmationDialog && (
        <div className="confirmation-modal">
          <div className="confirmation-content">
            <h2>Confirmation</h2>
            <p>Are you sure you want to clear the conversation?</p>
            <div className="confirmation-buttons">
              <button className="green-button" onClick={clearConversation}>
                Yes
              </button>
              <button className="red-button" onClick={closeConfirmation}>
                No
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
