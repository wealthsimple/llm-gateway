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

interface ClearButtonProps {
  onClear: () => void;
}

export const ClearButton: React.FC<ClearButtonProps> = ({ onClear }) => {
  const [showConfirmation, setShowConfirmation] = useState(false);

  const clearConversation = () => {
    localStorage.removeItem('conversation');
    onClear();
    setShowConfirmation(false);
  };

  const openConfirmation = () => {
    setShowConfirmation(true);
  };

  const closeConfirmation = () => {
    setShowConfirmation(false);
  };

  return (
    <>
      <button onClick={openConfirmation}>Clear Conversation</button>

      {showConfirmation && (
        <div className="confirmation-modal">
          <div className="confirmation-content">
            <h2>Confirmation</h2>
            <p>Are you sure you want to clear the conversation?</p>
            <div className="confirmation-buttons">
              <button onClick={clearConversation}>Yes</button>
              <button onClick={closeConfirmation}>No</button>
            </div>
          </div>
        </div>
      )}

      <style>
        {`
          .confirmation-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: rgba(0, 0, 0, 0.5);
          }

          .confirmation-content {
            background-color: #fff;
            padding: 20px;ß
            border-radius: 5px;
            text-align: center;
          }

          .confirmation-buttons {
            margin-top: 20px;
          }
        `}
      </style>
    </>
  );
};
