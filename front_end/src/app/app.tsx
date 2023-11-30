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

import React, { useEffect, useState } from 'react';
import {
  modelChoices,
  DEFAULT_MODEL_TEMP,
  APP_DESCRIPTION,
  APP_FOOTER,
  DEFAULT_SETTINGS,
  CONVERSATION_KEY,
  DEFAULT_CONVERSATIONS_STATE,
} from '../constants';
import { ChatBoxComponent } from './components/ChatBox';
import { ModelSettingsDialog } from './components/SettingsDialog';
import {
  type Conversation,
  type ConversationsState,
  type Message,
} from './interfaces';
import { ChatNavBarComponent } from './components/ChatNavBar';
import { EmptyChatBoxComponent } from './components/EmptyChatBox';
import { ModelBannerComponent } from './components/ModelBanner';

// Key actions for the gateway app. We should put it in the highest level component.
const saveConversationsStateToLocalStorage = (
  conversationsState: ConversationsState,
) => {
  const conversationJson = JSON.stringify(conversationsState);
  localStorage.setItem(CONVERSATION_KEY, conversationJson);
};

const loadConversationsStateFromLocalStorage = (): ConversationsState => {
  const conversationJson = localStorage.getItem(CONVERSATION_KEY);
  if (conversationJson) {
    return JSON.parse(conversationJson);
  }
  return DEFAULT_CONVERSATIONS_STATE;
};

export function App(): JSX.Element {
  const [conversationState, setConversationState] =
    useState<ConversationsState>(loadConversationsStateFromLocalStorage());

  const getConversationById = (
    state: ConversationsState,
    id: number | null,
  ) => {
    return state.conversations.find((convo) => convo.id === id);
  };

  const [currentSelectedId, setCurrentSelectedId] = useState<number | null>(
    conversationState.selectedConversationId,
  );
  const [currentMessages, setCurrentMessages] = useState<Message[]>(
    getConversationById(conversationState, currentSelectedId)?.messages || [],
  );
  const [currentModel, setCurrentModel] = useState<string>(
    getConversationById(conversationState, currentSelectedId)?.model ||
      DEFAULT_SETTINGS.model,
  );
  const [currentChatTitle, setCurrentChatTitle] = useState<string>(
    getConversationById(conversationState, currentSelectedId)?.title || '',
  );
  const [isLoadingReply, setIsLoadingReply] = useState<boolean>(false);

  useEffect(() => {
    const newConversationState = { ...conversationState };
    const conversationIdx = newConversationState.conversations.findIndex(
      (c) => c.id === currentSelectedId,
    );
    if (conversationIdx === -1) {
      return;
    }
    newConversationState.conversations[conversationIdx].messages =
      currentMessages;
    newConversationState.conversations[conversationIdx].model = currentModel;
    newConversationState.conversations[conversationIdx].title =
      currentChatTitle;
    setConversationState(newConversationState);
  }, [currentMessages, currentModel, currentChatTitle]);

  useEffect(() => {
    saveConversationsStateToLocalStorage(conversationState);
  }, [conversationState]);

  useEffect(() => {
    const newConversationState = { ...conversationState };
    newConversationState.selectedConversationId = currentSelectedId;
    const currentConversation = getConversationById(
      newConversationState,
      currentSelectedId,
    );
    setCurrentMessages(currentConversation?.messages || []);
    setCurrentModel(currentConversation?.model || DEFAULT_SETTINGS.model);
    setCurrentChatTitle(currentConversation?.title || '');
    setConversationState(newConversationState);
  }, [currentSelectedId]);

  const updateChatTitle = (id: number, title: string) => {
    const newConversationState = { ...conversationState };
    const conversationIdx = newConversationState.conversations.findIndex(
      (c) => c.id === id,
    );
    newConversationState.conversations[conversationIdx].title = title;
    setConversationState(newConversationState);
  };

  const addConversation = (title: string, model: string) => {
    const newConversationState = { ...conversationState };
    const newConversation: Conversation = {
      id: Date.now(),
      title: title,
      model: model,
      messages: modelChoices[model].initialPrompt,
    };
    newConversationState.conversations.push(newConversation);
    setConversationState(newConversationState);
    setCurrentSelectedId(newConversation.id);
  };

  const deleteConversation = (id: number | null) => {
    const newConversationState = { ...conversationState };
    newConversationState.conversations =
      newConversationState.conversations.filter((convo) => convo.id !== id);
    if (newConversationState.conversations.length > 0) {
      setCurrentSelectedId(newConversationState.conversations[0].id);
    } else {
      setCurrentSelectedId(null);
    }
    setConversationState(newConversationState);
  };

  const clearCurrentConversation = () => {
    if (currentSelectedId !== null) {
      const newCurrentMessages = modelChoices[currentModel].initialPrompt;
      setCurrentMessages(newCurrentMessages);
    }
  };

  const temperature = DEFAULT_MODEL_TEMP;
  const description = APP_DESCRIPTION;
  const appFooter = APP_FOOTER;

  const [showSettings, setShowSettings] = useState(false);

  return (
    <>
      {/* Note: To set cursor animation and disable cursor at the same time,
      set cursor to waiting in the parent component first
      then disable the cursor in the child component */}
      <main className={`container ${isLoadingReply ? 'waiting' : ''}`}>
        <article className="appDescription">
          <body>{description}</body>
        </article>

        <div className="chat-container">
          <ChatNavBarComponent
            setOpenAddNewChatDialog={setShowSettings}
            conversationsState={conversationState}
            setSelectedId={setCurrentSelectedId}
            selectedId={currentSelectedId}
            isModelLoadingReply={isLoadingReply}
            deleteConversation={deleteConversation}
            updateChatTitle={updateChatTitle}
          />

          <div className="main-chat-container">
            {currentSelectedId !== null ? (
              <>
                <ModelBannerComponent
                  modelName={modelChoices[currentModel].name}
                  isModelLoadingReply={isLoadingReply}
                  clearCurrentChatMessagesAction={clearCurrentConversation}
                />
                <ChatBoxComponent
                  messages={currentMessages}
                  setMessages={setCurrentMessages}
                  modelName={currentModel}
                  modelTemperature={temperature}
                  isModelLoadingReply={isLoadingReply}
                  setIsModelLoadingReply={setIsLoadingReply}
                />
              </>
            ) : (
              <EmptyChatBoxComponent />
            )}
          </div>
        </div>
        <br></br>
        <div className="footer">{appFooter}</div>
      </main>
      <ModelSettingsDialog
        showSettings={showSettings}
        setShowSettings={setShowSettings}
        createNewConversation={addConversation}
      />
    </>
  );
}
