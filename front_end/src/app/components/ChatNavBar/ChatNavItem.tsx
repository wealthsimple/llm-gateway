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

import React, { useState, useRef, useEffect } from 'react';
import { DeleteIcon } from '../Icons/TrashCanIcon';
import { EditIcon } from '../Icons/EditIcon';
import { SaveIcon } from '../Icons/SaveIcon';
import { CancelIcon } from '../Icons/CancelIcon';
import { type Conversation } from '../../interfaces';

export interface ChatNavItemProps {
  conversation: Conversation;
  selectedId: number | null;
  setSelectedId: (arg: number) => void;
  isModelLoadingReply: boolean;
  setShowConfirmDeleteDialog: (arg: boolean) => void;
  updateChatTitle: (arg: number, arg2: string) => void;
}

export const ChatNavItem = (props: ChatNavItemProps): JSX.Element => {
  const chatRef = useRef<HTMLDivElement | null>(null);

  const [inputTitle, setInputTitle] = useState<string>(
    props.conversation.title,
  );
  const [hovering, setHovering] = useState<boolean>(false);
  const [isUserEditingTitle, setIsUserEditingTitle] = useState<boolean>(false);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (chatRef.current && !chatRef.current.contains(event.target as Node)) {
        closeEditingTitle();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [chatRef]);

  const saveNewTitle = () => {
    const newTitle = inputTitle.trim();
    if (!newTitle) {
      return;
    }
    props.updateChatTitle(props.conversation.id, newTitle);
    closeEditingTitle();
  };

  const closeEditingTitle = () => {
    setInputTitle(props.conversation.title);
    setIsUserEditingTitle(false);
  };

  const onChangeChatBox = (id: number) => {
    props.setSelectedId(id);
  };
  return (
    <article
      className={`chat-wrap ${
        props.conversation.id === props.selectedId && 'chat-selected'
      }`}
      onClick={() =>
        !props.isModelLoadingReply && onChangeChatBox(props.conversation.id)
      }
      onMouseOver={() => setHovering(true)}
      onMouseOut={() => setHovering(false)}
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ref={chatRef as any}
    >
      <div className="nav-item-label">
        {isUserEditingTitle ? (
          <input
            className="editing-item-label"
            value={inputTitle}
            placeholder={props.conversation.title}
            onChange={(e) => setInputTitle(e.target.value)}
            onKeyDownCapture={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                saveNewTitle();
              }
            }}
          ></input>
        ) : (
          <div className="default-item-label">{props.conversation.title}</div>
        )}
      </div>
      <div className="nav-item-icons">
        {hovering && !isUserEditingTitle && (
          <>
            <div onClick={() => setIsUserEditingTitle(true)}>{EditIcon}</div>
            <div onClick={() => props.setShowConfirmDeleteDialog(true)}>
              {DeleteIcon}
            </div>
          </>
        )}
        {isUserEditingTitle && (
          <>
            <div onClick={() => saveNewTitle()}>{SaveIcon}</div>
            <div onClick={() => closeEditingTitle()}>{CancelIcon}</div>
          </>
        )}
      </div>
    </article>
  );
};
