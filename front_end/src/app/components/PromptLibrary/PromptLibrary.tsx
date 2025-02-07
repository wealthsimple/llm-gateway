import React, { useState, useEffect } from 'react';
import { Prompt, PromptTheme, PROMPT_THEMES } from '../../interfaces';
import './PromptLibrary.css';
import { PromptCard } from './PromptCard';
import { CreatePromptDialog } from './CreatePromptDialog';

export const PromptLibrary: React.FC = () => {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<PromptTheme>('marketing');
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const fetchPrompts = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/prompts');
      const data = await response.json();
      setPrompts(data);
    } catch (error) {
      console.error('Failed to fetch prompts:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPrompts();
  }, []);

  const handleCreatePrompt = async (prompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      const response = await fetch('/api/prompts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prompt),
      });
      if (response.ok) {
        await fetchPrompts();
        setShowCreateDialog(false);
      }
    } catch (error) {
      console.error('Failed to create prompt:', error);
    }
  };

  const handleDeletePrompt = async (id: number) => {
    try {
      const response = await fetch(`/api/prompts/${id}`, { method: 'DELETE' });
      if (response.ok) {
        await fetchPrompts();
      }
    } catch (error) {
      console.error('Failed to delete prompt:', error);
    }
  };

  return (
    <div className="prompt-library">
      <div className="prompt-library-header">
        <h2>Prompt Library</h2>
        <button 
          className="primary-btn"
          onClick={() => setShowCreateDialog(true)}
        >
          Create New Prompt
        </button>
      </div>
      <div className="theme-selector">
        {PROMPT_THEMES.map(theme => (
          <button 
            key={theme}
            onClick={() => setSelectedTheme(theme)}
            className={`theme-btn ${selectedTheme === theme ? 'active' : ''}`}
          >
            {theme}
          </button>
        ))}
      </div>
      <div className="prompts-grid">
        {isLoading ? (
          <div>Loading prompts...</div>
        ) : (
          prompts
            .filter(p => p.theme === selectedTheme)
            .map(prompt => (
              <PromptCard 
                key={prompt.id} 
                prompt={prompt}
                onDelete={handleDeletePrompt}
              />
            ))
        )}
      </div>
      <CreatePromptDialog
        open={showCreateDialog}
        onClose={() => setShowCreateDialog(false)}
        onCreate={handleCreatePrompt}
      />
    </div>
  );
};
