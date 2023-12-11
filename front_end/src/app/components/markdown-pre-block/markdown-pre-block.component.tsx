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
import 'highlight.js/styles/a11y-dark.css';
import hljs from 'highlight.js';
import { COMMON_PROGRAMMING_LANGUAGES } from '../../../constants';

interface MarkdownPreBlockProps {
  className: string | undefined;
  // A `pre` tag in markdown can either be:
  // 1. A standard <pre> block with no nested code block (just a string)
  // 2. A <pre> block with a nested <code> block
  children:
    | string
    | {
        type: 'code';
        props: { className: string | undefined; children: string };
      };
}

export const MarkdownPreBlock = ({
  className,
  children,
}: MarkdownPreBlockProps) => {
  const [copiedCodeSnippet, setCopiedCodeSnippet] = useState(false);
  // Don't attempt to syntax highlight non-code `pre` blocks:
  if (!children || typeof children !== 'object') {
    return <pre className={className}>{children}</pre>;
  }

  const { className: codeClassName, children: codeContent } = children.props;
  const code = String(codeContent).replace(/\n$/, '');
  // OpenAI responses will not always tag a code block with the language. In
  // this case, default to `bash` which has syntax highlighting that tends to
  // work well across many languages:
  const language = codeClassName ? codeClassName.replace('lang-', '') : null;

  const getSyntaxHighlightedCode = () => {
    if (language) {
      try {
        return hljs.highlight(code, { language, ignoreIllegals: true }).value;
      } catch (error) {
        return hljs.highlight(code, { language: 'bash' }).value;
      }
    }
    // If no language is specified or unable to process the language,
    // try to auto-detect the language based on the
    // common languages we use:
    return hljs.highlightAuto(code, COMMON_PROGRAMMING_LANGUAGES).value;
  };

  const copyCodeToClipboard = () => {
    navigator.clipboard.writeText(code);
    setCopiedCodeSnippet(true);
    setTimeout(() => setCopiedCodeSnippet(false), 3000);
  };

  // Render multi-line syntax highlighted code block:
  return (
    <pre>
      <div className="markdown-code-header">
        {language ? <span>{language}</span> : null}
        <span onClick={copyCodeToClipboard} className="clipboard">
          <span role="img" aria-label="clipboard">
            {copiedCodeSnippet ? '✔' : '️📋'}
          </span>{' '}
          {copiedCodeSnippet ? 'Copied!' : 'Copy code'}
        </span>
      </div>
      <code
        role="code"
        className="hljs"
        dangerouslySetInnerHTML={{ __html: getSyntaxHighlightedCode() }}
      />
    </pre>
  );
};
