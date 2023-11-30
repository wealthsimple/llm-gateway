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
import { type Message } from '../../interfaces';
import { MessageContent } from '../message-content';
import { RANDOM_LOADING_PHRASES } from '../../../constants';

interface Props {
  messages: Message[];
  isLoadingReply: boolean;
}

const RandomLoadingMessage = () => {
  const randomIndex = Math.floor(Math.random() * RANDOM_LOADING_PHRASES.length);
  return RANDOM_LOADING_PHRASES[randomIndex];
};

export const MessageHistoryComponent: React.FC<Props> = ({
  messages,
  isLoadingReply,
}) => {
  return (
    // wrap a second div so that scrollbar and border don't overlap
    <div className="message-history-container">
      <div className="message-history">
        <ul>
          {messages.map((message, idx) => (
            <li
              key={`${message.role}-${idx}}`}
              className={`message message-${message.role}`}
            >
              {/* Only attempt to format assistant messages which are reliably
                formatted in valid markdown. Although user input messages may
                contain markdown occasionally, it is not guaranteed to be in a
                valid format and may end up rendering badly. */}
              {message.role === 'assistant' ? (
                <MessageContent content={message.content} />
              ) : (
                message.content
              )}
            </li>
          ))}
          {isLoadingReply && (
            <li aria-busy="true" className={`message message-assistant`}>
              {RandomLoadingMessage()}
            </li>
          )}
        </ul>
      </div>
    </div>
  );
};
