import React, {useEffect, useState, type ReactNode} from 'react';
import Translate, {translate} from '@docusaurus/Translate';
import useIsBrowser from '@docusaurus/useIsBrowser';
import {useStorageSlot} from '@docusaurus/theme-common';
import {DISMISSAL_ATTRIBUTE, DISMISSAL_STORAGE_KEY} from './constants';
import styles from './styles.module.css';

export default function AnnouncementBar(): ReactNode {
  const isBrowser = useIsBrowser();
  const [storedDismissal, storage] = useStorageSlot(DISMISSAL_STORAGE_KEY, {
    persistence: 'localStorage',
  });
  const [isDismissed, setIsDismissed] = useState(false);

  useEffect(() => {
    if (isBrowser) document.documentElement.removeAttribute(DISMISSAL_ATTRIBUTE);
  }, [isBrowser]);

  function dismiss() {
    setIsDismissed(true);
    storage.set('true');
  }

  if (isDismissed || storedDismissal === 'true') return null;

  return (
    <aside
      className={`theme-announcement-bar ${styles.notice}`}
      aria-label={translate({
        id: 'theme.securityNotice.label',
        message: '중요 보안 공지',
      })}>
      <div className={styles.content}>
        <a
          className={styles.message}
          href="https://laravel.com/blog/php-critical-vulnerability-response-updates">
          <span aria-hidden="true">⚠</span>
          <Translate id="theme.securityNotice.message">
            취약점 대응 업데이트
          </Translate>
        </a>
        <a
          className={styles.link}
          href="https://laravel.com/blog/php-critical-vulnerability-response-updates">
          <Translate id="theme.securityNotice.link">Read</Translate>
        </a>
      </div>
      <div className={styles.actions}>
        <a
          className={styles.githubLink}
          href="https://github.com/openai/php2shell-checker"
          aria-label="GitHub: openai/php2shell-checker">
          <svg
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
            focusable="false">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
          </svg>
        </a>
        <button
          type="button"
          className={styles.close}
          onClick={dismiss}
          aria-label={translate({
            id: 'theme.securityNotice.dismiss',
            message: '보안 공지 닫기',
          })}>
          <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">
            <path d="m6 6 8 8M14 6l-8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
        </button>
      </div>
    </aside>
  );
}
