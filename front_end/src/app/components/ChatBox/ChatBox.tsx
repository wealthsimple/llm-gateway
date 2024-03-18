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
import { fetchResponseFromModel } from '../../../services/apiService';
import { type Message, Role, type IRequestBody } from '../../interfaces';
import { MessageHistoryComponent } from './MessageHistory';

interface ChatBoxProps {
  messages: Message[];
  setMessages: (arg: Message[]) => void;
  modelName: string;
  modelTemperature: number;
  isModelLoadingReply: boolean;
  setIsModelLoadingReply: (arg: boolean) => void;
}

const sendMessage = (
  readyToSend: boolean,
  setReadyToSend: (arg: boolean) => void,
  setIsLoadingReply: (arg: boolean) => void,
  inputVal: string,
  setInputVal: (arg: string) => void,
  messages: Message[],
  setMessages: (arg: Message[]) => void,
  setErrMsg: (arg: string) => void,
  model: string,
  temperature: number,
): void => {
  if (!readyToSend || !inputVal) {
    return;
  }

  const message: Message = {
    role: Role.user,
    content: inputVal,
  };

  setInputVal('');
  setReadyToSend(false);
  setIsLoadingReply(true);
  setErrMsg('');

  // add user's message to history
  const newMessageHistory = [...messages, message];
  setMessages(newMessageHistory);
  const apiRequestBody: IRequestBody = {
    messages: newMessageHistory,
    model: model,
    temperature: temperature,
  };
  fetchResponseFromModel(apiRequestBody)
    .then((resContent) => {
      setMessages([
        ...newMessageHistory,
        { role: Role.assistant, content: resContent },
      ]);
    })
    .catch((err) => {
      console.log(err);
      setErrMsg(err.message);
    })
    .finally(() => {
      setReadyToSend(true);
      setIsLoadingReply(false);
    });
};

export const ChatBoxComponent: React.FC<ChatBoxProps> = ({
  messages,
  setMessages,
  modelName,
  modelTemperature,
  isModelLoadingReply,
  setIsModelLoadingReply,
}) => {
  const [readyToSendMessage, setReadyToSendMessage] = useState<boolean>(true);
  const [errMsg, setErrMsg] = useState<string>('');
  const [inputVal, setInputVal] = useState('');

  const triggerSendMessage = () =>
    sendMessage(
      readyToSendMessage,
      setReadyToSendMessage,
      setIsModelLoadingReply,
      inputVal,
      setInputVal,
      messages,
      setMessages,
      setErrMsg,
      modelName,
      modelTemperature,
    );

  return (
    <div className="chatbox">
      {/* slice(1) to remove initial assistant message */}
      <MessageHistoryComponent
        messages={messages.slice(1)}
        isLoadingReply={isModelLoadingReply}
      />
      <div id="chat-action-buttons-group" className="grid">
        <div className="input-box-div">
          <textarea
            id="input-box"
            value={inputVal}
            rows={1}
            placeholder="Send a message"
            onChange={(e) => {
              setInputVal(e.target.value);
            }}
            onKeyDownCapture={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                // needed to prevent newline character from being added to textarea
                e.preventDefault();
                triggerSendMessage();
              }
            }}
            autoFocus
          />
        </div>
        <a
          className="send-button primary-btn"
          href="#send"
          role="button"
          onClick={triggerSendMessage}
        >
          Send
        </a>
      </div>

      {errMsg ? (
        <p className="error-message">{errMsg}</p>
      ) : (
        <p className="helpful-tip">
          Press enter to send a message, shift+enter to make a multi-line
          message.
        </p>
      )}
    </div>
  );
};
