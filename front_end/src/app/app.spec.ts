import { downloadChatAsCSVFn } from './app';
import { parseCSVFn } from './components/SettingsDialog/settingsDialog';

import { CONVO_1, CONVO_2, CONVO_3, CONVO_4 } from '../test_data/conversation';
import { Message } from './interfaces';

describe('Imported CSV and exported Message[] are equal', () => {
  it('with "', () => {
    const csvContent = downloadChatAsCSVFn(CONVO_1);

    parseCSVFn(csvContent, (arg: boolean) => { return }) // eslint-disable-line no-unused-vars
        .then((messages: Message[]) => {
            expect(messages).toEqual(CONVO_1);
        })
  });

  it('with `', () => {
    const csvContent = downloadChatAsCSVFn(CONVO_2);

    parseCSVFn(csvContent, (arg: boolean) => { return }) // eslint-disable-line no-unused-vars
        .then((messages: Message[]) => {
            expect(messages).toEqual(CONVO_2);
        })
  });

  it("with '", () => {
    const csvContent = downloadChatAsCSVFn(CONVO_3);

    parseCSVFn(csvContent, (arg: boolean) => { return }) // eslint-disable-line no-unused-vars
        .then((messages: Message[]) => {
            expect(messages).toEqual(CONVO_3);
        })
  });

  it("with new line", () => {
    const csvContent = downloadChatAsCSVFn(CONVO_4);

    parseCSVFn(csvContent, (arg: boolean) => { return }) // eslint-disable-line no-unused-vars
        .then((messages: Message[]) => {
            expect(messages).toEqual(CONVO_4);
        })
  });
});
