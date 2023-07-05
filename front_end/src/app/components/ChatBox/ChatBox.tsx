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

import React, { useState, useEffect } from 'react';
import { SendButtonComponent } from './SendButton';
import { ClearButton } from './ClearButton';
import { fetchResponseFromModel } from '../../../services/apiService';
import { Message, Role } from '../../interfaces';
import { MessageHistoryComponent } from './MessageHistory';

interface ChatBoxProps {
  modelName: string;
  modelTemperature: number;
  setShowSettings: (arg: boolean) => void;
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
  fetchResponseFromModel(model, newMessageHistory, temperature)
    .then((resContent) => {
      setMessages([
        ...newMessageHistory,
        { role: Role.assistant, content: resContent },
      ]);
    })
    .catch((err) => {
      console.log('error');
      setErrMsg(err.message);
    })
    .finally(() => {
      setReadyToSend(true);
      setIsLoadingReply(false);
    });
};
const saveConversation = (conversation: Message[]) => {
  const conversationJson = JSON.stringify(conversation);
  localStorage.setItem('conversation', conversationJson);
};

const loadConversation = (): Message[] => {
  const conversationJson = localStorage.getItem('conversation');
  if (conversationJson) {
    return JSON.parse(conversationJson);
  }
  return [
    { role: Role.assistant, content: 'You are an intelligent assistant.' },
    { role: Role.user, content: 'Hello!' },
    { role: Role.assistant, content: 'Hello! How can I assist you today?' },
  ];
};
export const ChatBoxComponent: React.FC<ChatBoxProps> = ({
  modelName,
  modelTemperature,
  setShowSettings,
}) => {
  const [messages, setMessages] = useState<Message[]>(loadConversation());

  useEffect(() => {
    saveConversation(messages);
  }, [messages]);

  const clearMessages = () => {
    setMessages(loadConversation);
  };

  const [isModelLoadingReply, setIsModelLoadingReply] =
    useState<boolean>(false);
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
    <div id="chatbox">
      {/* slice(1) to remove initial assistant message */}
      <MessageHistoryComponent
        messages={messages.slice(1)}
        isLoadingReply={isModelLoadingReply}
      />
      <textarea
        id="input-box"
        value={inputVal}
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
      <p id="error-message">{errMsg}</p>
      <SendButtonComponent
        sendMessageHandler={triggerSendMessage}
        setShowModelSettings={setShowSettings}
      />
      <p>
        Press enter to send a message. Press shift+enter to make a multi-line
        message.
      </p>
      <ClearButton
        onClear={clearMessages}
      />
      <p>
        Clears conversation history. Click to confirm.
      </p>
    </div>
  );
};
