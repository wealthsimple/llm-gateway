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
import Markdown from 'markdown-to-jsx';
import { MarkdownPreBlock } from '../markdown-pre-block';
import { isMessageMarkdown } from './message-content.utils';

export const MessageContent = ({ content }: { content: string }) => {
  if (isMessageMarkdown(content)) {
    // Format markdown messages with markdown:
    return (
      <Markdown
        options={{
          // Out of caution, disable parsing raw HTML to JSX. We don't want to
          // allow OpenAI or other LLM providers to be able to inject arbitrary
          // HTML into our app:
          disableParsingRawHTML: true,
          // Override the default `pre` block component with our own which
          // supports syntax highlighting:
          overrides: {
            pre: { component: MarkdownPreBlock },
          },
        }}
      >
        {content}
      </Markdown>
    );
  }

  return (
    // Otherwise, return non-markdown messages in plain text:
    <div>{content}</div>
  );
};
