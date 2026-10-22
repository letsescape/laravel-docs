type NoticeText = {
  label: string;
  message: string;
  linkText?: string;
  dismissLabel: string;
};

type AnnouncementConfig = {
  enabled: boolean;
  id: string;
  variant: 'warning' | 'info';
  href?: string;
  github?: {href: string; label: string};
  locales: Record<string, NoticeText> & {ko: NoticeText; ja: NoticeText};
};

export const announcement: AnnouncementConfig = {
  // 머지·배포 후 적용됩니다. 다시 표시하려면 true로 바꾸세요.
  enabled: false,
  // 새 공지는 고유한 ID를 사용해야 이전 공지의 닫기 기록과 분리됩니다.
  id: 'php-critical-vulnerability-response-updates',
  variant: 'warning',
  // 링크가 필요 없으면 href 또는 github를 제거하세요.
  href: 'https://laravel.com/blog/php-critical-vulnerability-response-updates',
  github: {
    href: 'https://github.com/openai/php2shell-checker',
    label: 'GitHub: openai/php2shell-checker',
  },
  locales: {
    ko: {
      label: '중요 보안 공지',
      message: '취약점 대응 업데이트',
      linkText: 'Read',
      dismissLabel: '보안 공지 닫기',
    },
    ja: {
      label: '重要なセキュリティのお知らせ',
      message: '脆弱性対応の最新情報',
      linkText: 'Read',
      dismissLabel: 'セキュリティのお知らせを閉じる',
    },
  },
};
