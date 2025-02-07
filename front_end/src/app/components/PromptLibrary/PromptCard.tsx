import React, { useState } from 'react';
import { Prompt } from '../../interfaces';

interface PromptCardProps {
  prompt: Prompt;
  onDelete: (id: number) => Promise<void>;
}

export const PromptCard: React.FC<PromptCardProps> = ({ prompt, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(prompt.title);
  const [editedContent, setEditedContent] = useState(prompt.content);
  const [error, setError] = useState<string | null>(null);

  const handleUpdate = async () => {
    setError(null);
    try {
      const response = await fetch(`/api/prompts/${prompt.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: editedTitle,
          content: editedContent,
          theme: prompt.theme,
        }),
      });
      if (response.ok) {
        setIsEditing(false);
        window.location.reload(); // Temporary solution - should use proper state management
      }
    } catch (error) {
      console.error('Failed to update prompt:', error);
      setError('Failed to update prompt. Please try again.');
    }
  };

  if (isEditing) {
    return (
      <form className="prompt-card editing" onSubmit={(e) => { e.preventDefault(); handleUpdate(); }}>
        {error && <div className="error-message" role="alert">{error}</div>}
        <div className="form-group">
          <label htmlFor={`edit-title-${prompt.id}`}>Title</label>
          <input
            id={`edit-title-${prompt.id}`}
            type="text"
            value={editedTitle}
            onChange={(e) => setEditedTitle(e.target.value)}
            className="edit-title"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor={`edit-content-${prompt.id}`}>Content</label>
          <textarea
            id={`edit-content-${prompt.id}`}
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            className="edit-content"
            rows={4}
            required
          />
        </div>
        <div className="prompt-actions" role="group" aria-label="Edit actions">
          <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
          <button type="submit" className="primary-btn">Save</button>
        </div>
      </form>
    );
  }

  return (
    <article className="prompt-card" aria-labelledby={`prompt-title-${prompt.id}`}>
      <h3 id={`prompt-title-${prompt.id}`}>{prompt.title}</h3>
      <p>{prompt.content}</p>
      <div className="prompt-actions" role="group" aria-label="Prompt actions">
        <button onClick={() => setIsEditing(true)} aria-label={`Edit ${prompt.title}`}>Edit</button>
        <button onClick={() => onDelete(prompt.id)} className="danger-btn" aria-label={`Delete ${prompt.title}`}>Delete</button>
      </div>
    </article>
  );
};
