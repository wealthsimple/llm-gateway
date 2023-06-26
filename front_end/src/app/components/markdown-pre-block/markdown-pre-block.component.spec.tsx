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

import { render, screen } from '@testing-library/react';
import { MarkdownPreBlock } from './markdown-pre-block.component';

describe('MarkdownPreBlock', () => {
  describe('with a nested `code` child, and this child has the language in className', () => {
    it('should render successfully with syntax highlighting', async () => {
      const view = render(
        <MarkdownPreBlock
          className={undefined}
          children={{
            type: 'code',
            props: {
              className: 'lang-typescript',
              children: `
                const sayHello = (name: string) => {
                  return "hello " + name;
                }`,
            },
          }}
        />,
      );
      expect(view.baseElement).toBeTruthy();
      expect(await screen.findByText('sayHello')).toBeTruthy();
      expect(await screen.findByRole('code')).toBeTruthy();
    });
  });

  describe('with a nested `code` child, but this child an undefined className', () => {
    it('should render successfully', async () => {
      const view = render(
        <MarkdownPreBlock
          className={undefined}
          children={{
            type: 'code',
            props: {
              className: undefined,
              children: `
                const sayHello = (name: string) => {
                  return "hello " + name;
                }`,
            },
          }}
        />,
      );
      expect(view.baseElement).toBeTruthy();
      expect(await screen.findByText('sayHello')).toBeTruthy();
      expect(await screen.findByRole('code')).toBeTruthy();
    });
  });

  describe('for a pre block without nested `code` children', () => {
    it('should render successfully', async () => {
      const view = render(
        <MarkdownPreBlock className={undefined} children="Some plaintext" />,
      );
      expect(view.baseElement).toBeTruthy();
      expect(await screen.findByText('Some plaintext')).toBeTruthy();
      expect(screen.queryByRole('code')).toBeFalsy();
    });
  });
});
