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

interface ClearChatConfirmDialogProps {
  showDialog: boolean;
  setShowDialog: (show: boolean) => void;
  clearCurrentChatAction: () => void;
}

export const ClearChatConfirmDialogComponent: React.FC<
  ClearChatConfirmDialogProps
> = (props: ClearChatConfirmDialogProps) => {
  return (
    <dialog open={props.showDialog}>
      <article>
        <h3>Clear current chat conversation?</h3>
        This chat conversation history will be cleared. This action is
        irreversible.
        <footer>
          <a
            href="#cancel"
            role="button"
            className="secondary-btn"
            onClick={() => props.setShowDialog(false)}
          >
            Cancel
          </a>
          <a
            href="#confirm"
            role="button"
            className="primary-btn"
            onClick={() => {
              props.clearCurrentChatAction();
              props.setShowDialog(false);
            }}
          >
            Confirm
          </a>
        </footer>
      </article>
    </dialog>
  );
};
