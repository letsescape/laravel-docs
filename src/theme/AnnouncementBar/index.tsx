import React, {useState, type ReactNode} from 'react';
import Translate, {translate} from '@docusaurus/Translate';
import styles from './styles.module.css';

export default function AnnouncementBar(): ReactNode {
  const [isDismissed, setIsDismissed] = useState(false);

  if (isDismissed) return null;

  return (
    <aside
      className={styles.notice}
      aria-label={translate({
        id: 'theme.securityNotice.label',
        message: '중요 보안 공지',
      })}>
      <div className={styles.content}>
        <span className={styles.message}>
          <span aria-hidden="true">⚠</span>
          <Translate id="theme.securityNotice.message">
            PHP 치명적 보안 취약점 대응 안내
          </Translate>
        </span>
        <a
          className={styles.link}
          href="https://laravel.com/blog/php-critical-vulnerability-response-updates">
          <Translate id="theme.securityNotice.link">대응 안내 보기</Translate>
          <span aria-hidden="true">→</span>
        </a>
      </div>
      <button
        type="button"
        className={styles.close}
        onClick={() => setIsDismissed(true)}
        aria-label={translate({
          id: 'theme.securityNotice.dismiss',
          message: '보안 공지 닫기',
        })}>
        <span aria-hidden="true">×</span>
      </button>
    </aside>
  );
}
