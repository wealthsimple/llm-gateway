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
import { EmptyState } from '../Icons/EmptyStateIllustration';
import { ThemeToggleButton } from '../ThemeProvider';

export const EmptyChatBoxComponent: React.FC = () => {
  return (
    <div className="empty-state">
      <div className="theme-toggle-container">
        <ThemeToggleButton />
      </div>
      <div className="illustration">{EmptyState}</div>
      <h1> No chat to display!</h1>
      <h3> Create a new chat to start using LLM Gateway.</h3>
    </div>
  );
};
