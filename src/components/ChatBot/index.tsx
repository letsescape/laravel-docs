import React, {useState, useRef, useEffect, useCallback, type ReactNode} from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  isError?: boolean;
}

const CHATBOT_API_URL = 'https://jbuch2jbxl.execute-api.ap-northeast-2.amazonaws.com/laravel-docs';

export default function ChatBot(): ReactNode {
  const {i18n} = useDocusaurusContext();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({behavior: 'smooth'});
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const handleSubmit = useCallback(() => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const userMessage: Message = {role: 'user', content: trimmed};
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    fetch(CHATBOT_API_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message: trimmed,
        locale: i18n.currentLocale,
      }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const botMessage: Message = {
          role: 'assistant',
          content: data.answer ?? data.message ?? data.response ?? '',
        };
        setMessages(prev => [...prev, botMessage]);
      })
      .catch(() => {
        const errorMessage: Message = {
          role: 'assistant',
          content: '죄송합니다. 응답을 가져오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
          isError: true,
        };
        setMessages(prev => [...prev, errorMessage]);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [input, isLoading, i18n.currentLocale]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !e.nativeEvent.isComposing) {
        e.preventDefault();
        handleSubmit();
      }
    },
    [handleSubmit],
  );

  return (
    <>
      {isOpen && (
        <div className={styles.chatWindow} role="dialog" aria-label="AI Chat">
          <div className={styles.chatHeader}>
            <span className={styles.chatHeaderTitle}>Laravel AI Assistant</span>
            <button
              className={styles.chatCloseButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 && (
              <div className={clsx(styles.message, styles.botMessage)}>
                Laravel에 대해 궁금한 점을 질문해주세요!
              </div>
            )}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={clsx(
                  styles.message,
                  msg.role === 'user' ? styles.userMessage : styles.botMessage,
                  msg.isError && styles.errorMessage,
                )}
              >
                {msg.content}
              </div>
            ))}
            {isLoading && (
              <div className={clsx(styles.message, styles.botMessage)}>
                <div className={styles.loadingDots}>
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputArea}>
            <input
              ref={inputRef}
              type="text"
              className={styles.chatInput}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="질문을 입력하세요..."
              disabled={isLoading}
            />
            <button
              className={styles.sendButton}
              onClick={handleSubmit}
              disabled={isLoading || !input.trim()}
              aria-label="Send message"
            >
              <svg className={styles.sendIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
              </svg>
            </button>
          </div>
        </div>
      )}

      <button
        className={styles.chatButton}
        onClick={() => setIsOpen(prev => !prev)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        <svg className={styles.chatButtonIcon} viewBox="0 0 24 24" fill="currentColor">
          {isOpen ? (
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
          ) : (
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z" />
          )}
        </svg>
      </button>
    </>
  );
}
