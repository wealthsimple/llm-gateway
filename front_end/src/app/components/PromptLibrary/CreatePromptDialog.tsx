import React, { useState } from 'react';
import { Prompt, PromptTheme, PROMPT_THEMES } from '../../interfaces';

interface CreatePromptDialogProps {
  open: boolean;
  onClose: () => void;
  onCreate: (prompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>) => Promise<void>;
}

export const CreatePromptDialog: React.FC<CreatePromptDialogProps> = ({
  open,
  onClose,
  onCreate,
}) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [theme, setTheme] = useState<PromptTheme>('marketing');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await onCreate({ title, content, theme });
      setTitle('');
      setContent('');
      setTheme('marketing');
    } catch (err) {
      setError('Failed to create prompt. Please try again.');
    }
  };

  if (!open) return null;

  return (
    <div className="dialog-overlay" role="presentation">
      <div
        role="dialog"
        aria-labelledby="dialog-title"
        aria-modal="true"
        className="dialog-content"
      >
        <h2 id="dialog-title">Create New Prompt</h2>
        <form onSubmit={handleSubmit} aria-label="Create prompt form">
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="content">Content</label>
            <textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
              rows={4}
            />
          </div>
          <div className="form-group">
            <label htmlFor="theme">Theme</label>
            <select
              id="theme"
              value={theme}
              onChange={(e) => setTheme(e.target.value as PromptTheme)}
              required
            >
              {PROMPT_THEMES.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <div className="dialog-actions" role="group" aria-label="Dialog actions">
            <button type="button" onClick={onClose} aria-label="Cancel creating prompt">
              Cancel
            </button>
            <button type="submit" className="primary-btn" aria-label="Create new prompt">
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
