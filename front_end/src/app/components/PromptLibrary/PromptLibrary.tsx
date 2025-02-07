import React, { useState, useEffect } from 'react';
import { PromptTheme, PROMPT_THEMES } from '../../interfaces';
import { API_ENDPOINTS } from '../../constants';
import { fetchWithAuth, APIError } from '../../utils/api';
import { Prompt, PromptArray, PromptArraySchema, CreatePromptSchema } from '../../schemas/prompt';
import './PromptLibrary.css';
import { PromptCard } from './PromptCard';
import { CreatePromptDialog } from './CreatePromptDialog';

export const PromptLibrary: React.FC<Record<string, never>> = () => {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<PromptTheme>('marketing');
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPrompts = async () => {
    setIsLoading(true);
    try {
      const data = await fetchWithAuth<PromptArray>(
        API_ENDPOINTS.prompts,
        {},
        PromptArraySchema
      );
      setPrompts(data);
    } catch (error) {
      console.error('Failed to fetch prompts:', error);
      setError(
        error instanceof APIError
          ? `Failed to load prompts: ${error.message}`
          : 'Failed to load prompts. Please try again later.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPrompts();
  }, []);

  const handleCreatePrompt = async (prompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      const validPrompt = CreatePromptSchema.parse(prompt);
      await fetchWithAuth<Prompt>(API_ENDPOINTS.prompts, {
        method: 'POST',
        body: JSON.stringify(validPrompt),
      });
      await fetchPrompts();
      setShowCreateDialog(false);
    } catch (error) {
      console.error('Failed to create prompt:', error);
      setError(
        error instanceof APIError
          ? `Failed to create prompt: ${error.message}`
          : error instanceof Error
            ? error.message
            : 'Failed to create prompt. Please try again.'
      );
    }
  };

  const handleDeletePrompt = async (id: number) => {
    try {
      setIsLoading(true);
      await fetchWithAuth<void>(`${API_ENDPOINTS.prompts}/${id}`, {
        method: 'DELETE'
      });
      await fetchPrompts();
    } catch (error) {
      console.error('Failed to delete prompt:', error);
      setError(
        error instanceof APIError
          ? `Failed to delete prompt: ${error.message}`
          : 'Failed to delete prompt. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="prompt-library">
      <header className="prompt-library-header">
        <h2>Prompt Library</h2>
        <button
          className="primary-btn"
          onClick={() => setShowCreateDialog(true)}
        >
          Create New Prompt
        </button>
      </header>
      <nav className="theme-selector">
        {PROMPT_THEMES.map(theme => (
          <button
            key={theme}
            onClick={() => setSelectedTheme(theme)}
            className={`theme-btn ${selectedTheme === theme ? 'active' : ''}`}
          >
            {theme}
          </button>
        ))}
      </nav>
      {error && (
        <div className="error-message" role="alert">
          {error}
          <button onClick={() => { setError(null); fetchPrompts(); }}>Try Again</button>
        </div>
      )}
      <section className="prompts-grid">
        {isLoading ? (
          <div role="status" aria-live="polite" className="loading-message">
            <span className="sr-only">Loading prompts...</span>
            <div className="loading-spinner"></div>
          </div>
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
      </section>
      <CreatePromptDialog
        open={showCreateDialog}
        onClose={() => setShowCreateDialog(false)}
        onCreate={handleCreatePrompt}
      />
    </section>
  );
};
