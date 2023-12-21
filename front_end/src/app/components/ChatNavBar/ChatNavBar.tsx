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
import { type ConversationsState } from '../../interfaces';
import { ClearChatDialog } from './ClearChatDialog';
import { ChatNavItem } from './ChatNavItem';

interface ChatNavBarProps {
  setOpenAddNewChatDialog: (arg: boolean) => void;
  conversationsState: ConversationsState;
  setSelectedId: (arg: number) => void;
  selectedId: number | null;
  isModelLoadingReply: boolean;
  deleteConversation: (arg: number | null) => void;
  updateChatTitle: (arg: number, arg2: string) => void;
}

export const ChatNavBarComponent = (props: ChatNavBarProps): JSX.Element => {
  const [showConfirmDeleteDialog, setShowConfirmDeleteDialog] =
    useState<boolean>(false);

  return (
    <div
      className={`multichat-nav-bar ${
        props.isModelLoadingReply ? 'cursor-disable' : ''
      }`}
    >
      <div className="multichat-nav-bar-container">
        <article
          className="new-chat-button-div"
          onClick={() =>
            !props.isModelLoadingReply && props.setOpenAddNewChatDialog(true)
          }
        >
          <body>
            <button className="primary-btn">New Chat</button>
          </body>
        </article>
        <div className="multichat-nav-bar-scroll">
          {props.conversationsState.conversations.map((conversation) => (
            // eslint-disable-next-line react/jsx-key
            <ChatNavItem
              conversation={conversation}
              selectedId={props.selectedId}
              setSelectedId={props.setSelectedId}
              isModelLoadingReply={props.isModelLoadingReply}
              setShowConfirmDeleteDialog={setShowConfirmDeleteDialog}
              updateChatTitle={props.updateChatTitle}
            />
          ))}
        </div>
      </div>
      <ClearChatDialog
        selectedId={props.selectedId}
        onClear={props.deleteConversation}
        showConfirmationDialog={showConfirmDeleteDialog}
        setShowConfirmationDialog={setShowConfirmDeleteDialog}
      />
    </div>
  );
};
