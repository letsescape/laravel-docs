import {useEffect, useRef} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {useActiveDocContext} from '@docusaurus/plugin-content-docs/client';
import {createChatLoader} from '@site/src/utils/chat-loader.mjs';

export default function ChatWidget(): null {
  const {siteConfig, i18n: {currentLocale}} = useDocusaurusContext();
  const {activeDoc, activeVersion} = useActiveDocContext('default');
  const {chat} = siteConfig.customFields as {chat: {sdkUrl: string; endpoint: string; browserManifestUrl?: string}};
  const {sdkUrl, endpoint, browserManifestUrl} = chat;
  const loader = useRef<ReturnType<typeof createChatLoader> | null>(null);
  const path = activeDoc?.path;
  const docKey = activeDoc?.id;
  const version = activeVersion?.name;
  const trailingSlash = siteConfig.trailingSlash;

  useEffect(() => {
    const current = createChatLoader({sdkUrl, endpoint, browserManifestUrl});
    loader.current = current;
    return () => {
      current.destroy();
      loader.current = null;
    };
  }, [sdkUrl, endpoint, browserManifestUrl]);

  useEffect(() => {
    const page = path && docKey && version ? {
      path: trailingSlash ? `${path.replace(/\/+$/, '')}/` : path,
      docKey,
      version,
      language: currentLocale,
    } : null;
    void loader.current?.update(page).catch(() => {
      console.warn('문서 채팅 SDK를 불러오지 못했습니다.');
    });
  }, [sdkUrl, endpoint, browserManifestUrl, path, docKey, version, currentLocale, trailingSlash]);

  return null;
}
