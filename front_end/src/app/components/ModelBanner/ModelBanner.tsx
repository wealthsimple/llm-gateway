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
import { ThemeToggleButton } from '../ThemeProvider';
import { DeleteIcon } from '../Icons/TrashCanIcon';
import { ClearChatConfirmDialogComponent } from './ClearChatConfirmDialog';

interface ModelBannerProps {
  modelName: string;
  isModelLoadingReply: boolean;
  clearCurrentChatMessagesAction: () => void;
}

export const ModelBannerComponent: React.FC<ModelBannerProps> = (
  props: ModelBannerProps,
) => {
  const [showClearChatConfirmDialog, setShowClearChatConfirmDialog] =
    useState<boolean>(false);

  return (
    <>
      <article
        className={`model-banner ${
          props.isModelLoadingReply ? 'cursor-disable' : ''
        }`}
      >
        <div className="model-name">{props.modelName}</div>
        <div className="banner-actions">
          <div className="theme-toggle-button">
            <ThemeToggleButton />
          </div>
          <div
            className="clear-chat"
            onClick={() => setShowClearChatConfirmDialog(true)}
          >
            {DeleteIcon}
          </div>
        </div>
      </article>
      <ClearChatConfirmDialogComponent
        showDialog={showClearChatConfirmDialog}
        setShowDialog={setShowClearChatConfirmDialog}
        clearCurrentChatAction={props.clearCurrentChatMessagesAction}
      />
    </>
  );
};
