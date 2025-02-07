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

  const handleUpdate = async () => {
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
    }
  };

  if (isEditing) {
    return (
      <div className="prompt-card editing">
        <input
          type="text"
          value={editedTitle}
          onChange={(e) => setEditedTitle(e.target.value)}
          className="edit-title"
        />
        <textarea
          value={editedContent}
          onChange={(e) => setEditedContent(e.target.value)}
          className="edit-content"
          rows={4}
        />
        <div className="prompt-actions">
          <button onClick={() => setIsEditing(false)}>Cancel</button>
          <button onClick={handleUpdate} className="primary-btn">Save</button>
        </div>
      </div>
    );
  }

  return (
    <div className="prompt-card">
      <h3>{prompt.title}</h3>
      <p>{prompt.content}</p>
      <div className="prompt-actions">
        <button onClick={() => setIsEditing(true)}>Edit</button>
        <button onClick={() => onDelete(prompt.id)} className="danger-btn">Delete</button>
      </div>
    </div>
  );
};
