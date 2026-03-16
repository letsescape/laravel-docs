import React, {useState, useRef, useEffect, useCallback, type ReactNode} from 'react';
import clsx from 'clsx';
import {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {useLocation} from '@docusaurus/router';
import styles from './styles.module.css';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  isError?: boolean;
}

const SUGGESTED_QUESTIONS = [
  {icon: '\u{1F4D6}', text: 'Eloquent ORM이란?', id: 'chatbot.suggestion.eloquent'},
  {icon: '\u26A1', text: '라우팅 설정 방법', id: 'chatbot.suggestion.routing'},
  {icon: '\u{1F527}', text: '마이그레이션 명령어', id: 'chatbot.suggestion.migration'},
  {icon: '\u{1F510}', text: '인증 시스템 구성', id: 'chatbot.suggestion.auth'},
];

export default function ChatBot(): ReactNode {
  const {siteConfig, i18n} = useDocusaurusContext();
  const location = useLocation();
  const chatbotApiUrl = siteConfig.customFields?.chatbotApiUrl as string | undefined;
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const chatWindowRef = useRef<HTMLDivElement>(null);
  const chatButtonRef = useRef<HTMLButtonElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const nextMessageIdRef = useRef(0);

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

  const handleClose = useCallback(() => {
    setIsOpen(false);
    chatButtonRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!isOpen) return;
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        handleClose();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, handleClose]);

  useEffect(() => {
    if (!isOpen || !chatWindowRef.current) return;
    const chatWindow = chatWindowRef.current;
    const focusableSelector = 'button:not(:disabled), input:not(:disabled), [tabindex]:not([tabindex="-1"])';

    const handleTabTrap = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      const focusable = chatWindow.querySelectorAll<HTMLElement>(focusableSelector);
      if (focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    chatWindow.addEventListener('keydown', handleTabTrap);
    return () => chatWindow.removeEventListener('keydown', handleTabTrap);
  }, [isOpen]);

  const sendMessage = useCallback(
    (text: string) => {
      const userMsg: Message = {id: nextMessageIdRef.current++, role: 'user', content: text};
      setMessages(prev => [...prev, userMsg]);
      setInput('');
      setIsLoading(true);

      abortControllerRef.current?.abort();
      const controller = new AbortController();
      abortControllerRef.current = controller;

      fetch(chatbotApiUrl!, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        signal: controller.signal,
        body: JSON.stringify({
          message: text,
          locale: i18n.currentLocale,
          // TODO: Lambda에서 context를 활용하여 현재 페이지 맥락 기반 응답 생성
          // - pageTitle: 현재 문서 제목으로 관련 섹션 우선 참조
          // - pagePath: 문서 버전/경로로 정확한 버전의 답변 제공
          // - 예: "이 페이지에서 설명하는 걸 쉽게 알려줘" 같은 맥락 질문 지원
          context: {
            pageTitle: document.title,
            pagePath: location.pathname,
          },
        }),
      })
        .then(response => {
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          return response.json();
        })
        .then(data => {
          if (controller.signal.aborted) return;
          const content = data.answer ?? data.message ?? data.response ?? '';
          if (!content) throw new Error('Empty response');
          setMessages(prev => [...prev, {id: nextMessageIdRef.current++, role: 'assistant', content}]);
        })
        .catch((error) => {
          if (error.name === 'AbortError') return;
          console.error('[ChatBot] API request failed:', error);
          setMessages(prev => [
            ...prev,
            {
              id: nextMessageIdRef.current++,
              role: 'assistant',
              content: translate({
                id: 'chatbot.errorMessage',
                message: '죄송합니다. 응답을 가져오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
                description: 'Error message shown when the chatbot API request fails',
              }),
              isError: true,
            },
          ]);
        })
        .finally(() => {
          if (!controller.signal.aborted) {
            setIsLoading(false);
          }
        });
    },
    [chatbotApiUrl, i18n.currentLocale, location.pathname],
  );

  const handleSubmit = useCallback(() => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    sendMessage(trimmed);
  }, [input, isLoading, sendMessage]);

  const handleSuggestionClick = useCallback(
    (text: string) => {
      if (isLoading) return;
      sendMessage(text);
    },
    [isLoading, sendMessage],
  );

  const handleClear = useCallback(() => {
    abortControllerRef.current?.abort();
    abortControllerRef.current = null;
    setMessages([]);
    setInput('');
    setIsLoading(false);
  }, []);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !e.nativeEvent.isComposing) {
        e.preventDefault();
        handleSubmit();
      }
    },
    [handleSubmit],
  );

  // chatbotApiUrl이 설정되지 않으면 챗봇을 렌더링하지 않음
  if (!chatbotApiUrl) {
    return null;
  }

  const lastMsg = messages.length > 0 ? messages[messages.length - 1] : null;
  let ariaLiveText = '';
  if (lastMsg?.role === 'assistant') {
    ariaLiveText = lastMsg.content;
  } else if (isLoading) {
    ariaLiveText = translate({id: 'chatbot.loading', message: '응답 생성 중...', description: 'Screen reader loading text'});
  }

  return (
    <div data-nosnippet data-pagefind-ignore>
      {isOpen && (
        <dialog
          ref={chatWindowRef}
          className={styles.chatWindow}
          open
          aria-label={translate({
            id: 'chatbot.dialogLabel',
            message: 'AI 채팅',
            description: 'ARIA label for the chat dialog',
          })}
          aria-modal="true"
        >
          <div className={styles.chatHeader}>
            <span className={styles.chatHeaderTitle}>
              {translate({
                id: 'chatbot.headerTitle',
                message: 'Laravel AI Assistant',
                description: 'Chat window header title',
              })}
            </span>
            <div className={styles.chatHeaderActions}>
              {messages.length > 0 && (
                <button
                  className={styles.chatClearButton}
                  onClick={handleClear}
                  aria-label={translate({
                    id: 'chatbot.clearChat',
                    message: '대화 초기화',
                    description: 'Clear chat history button label',
                  })}
                  title={translate({
                    id: 'chatbot.clearChat',
                    message: '대화 초기화',
                    description: 'Clear chat history button tooltip',
                  })}
                >
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                  </svg>
                </button>
              )}
              <button
                className={styles.chatCloseButton}
                onClick={handleClose}
                aria-label={translate({
                  id: 'chatbot.closeChat',
                  message: '채팅 닫기',
                  description: 'Close chat button label',
                })}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 && (
              <>
                <div className={clsx(styles.message, styles.botMessage)}>
                  {translate({
                    id: 'chatbot.welcomeMessage',
                    message: 'Laravel에 대해 궁금한 점을 질문해주세요!',
                    description: 'Welcome message shown when the chatbot is first opened',
                  })}
                </div>
                <div className={styles.suggestions}>
                  {SUGGESTED_QUESTIONS.map(q => (
                    <button
                      key={q.id}
                      className={styles.suggestionChip}
                      onClick={() => handleSuggestionClick(
                        translate({id: q.id, message: q.text}),
                      )}
                      disabled={isLoading}
                    >
                      <span className={styles.suggestionIcon}>{q.icon}</span>
                      {translate({id: q.id, message: q.text})}
                    </button>
                  ))}
                </div>
              </>
            )}
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={clsx(
                  styles.message,
                  msg.role === 'user' ? styles.userMessage : styles.botMessage,
                  msg.isError && styles.errorMessage,
                )}
              >
                {/* TODO: Phase 2 - Markdown 렌더링 + 관련 문서 페이지 링크 자동 연결
                    - react-markdown 또는 @mdx-js/react 도입
                    - 코드 블록 syntax highlighting (prism-react-renderer 활용)
                    - 문서 내부 링크 자동 감지 및 <Link> 컴포넌트로 변환 */}
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
            <div aria-live="polite" className={styles.srOnly}>
              {ariaLiveText}
            </div>
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
              placeholder={translate({
                id: 'chatbot.inputPlaceholder',
                message: '질문을 입력하세요...',
                description: 'Placeholder text for the chatbot input field',
              })}
              disabled={isLoading}
            />
            <button
              className={styles.sendButton}
              onClick={handleSubmit}
              disabled={isLoading || !input.trim()}
              aria-label={translate({
                id: 'chatbot.sendMessage',
                message: '메시지 보내기',
                description: 'Send message button label',
              })}
            >
              <svg className={styles.sendIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
              </svg>
            </button>
          </div>
        </dialog>
      )}

      <button
        ref={chatButtonRef}
        className={styles.chatButton}
        onClick={() => setIsOpen(prev => !prev)}
        aria-label={isOpen
          ? translate({id: 'chatbot.closeChat', message: '채팅 닫기', description: 'Close chat button label'})
          : translate({id: 'chatbot.openChat', message: '채팅 열기', description: 'Open chat button label'})
        }
      >
        <svg className={styles.chatButtonIcon} viewBox="0 0 24 24" fill="currentColor">
          {isOpen ? (
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
          ) : (
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z" />
          )}
        </svg>
      </button>
    </div>
  );
}
