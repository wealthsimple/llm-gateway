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
import { MessageContent } from './message-content.component';

describe('MessageContent', () => {
  it('should render markdown messages with markdown', async () => {
    const content = `This is an example code block:

      \`\`\`ruby
      gem install faraday
      \`\`\`

    Another message.`;
    render(<MessageContent content={content} />);
    expect(await screen.findByRole('code')).toBeTruthy();
  });

  it('should render non-markdown messages in plain text', async () => {
    const content = 'This is a plain text message.';
    render(<MessageContent content={content} />);
    expect(
      await screen.findByText('This is a plain text message.'),
    ).toBeTruthy();
    expect(screen.queryByRole('code')).toBeFalsy();
  });
});
