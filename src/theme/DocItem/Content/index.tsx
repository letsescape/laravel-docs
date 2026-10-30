import React, {type ReactNode} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import DocItemContent from '@theme-original/DocItem/Content';
import type {Props} from '@theme/DocItem/Content';
import {QRCodeSVG} from 'qrcode.react';

export default function DocItemContentWrapper(props: Props): ReactNode {
  const {metadata} = useDoc();
  const {i18n: {currentLocale}} = useDocusaurusContext();
  const sourceUrl = `https://laravel.com/docs/${metadata.version}/${metadata.id}`;
  const language = currentLocale === 'ja' ? '日本語ドキュメント' : '한국어 문서';

  return (
    <>
      <div className="docs-print-header">
        <div>
          <strong>Laravel {metadata.version} · {language}</strong>
          <a href={sourceUrl}>{sourceUrl}</a>
        </div>
        <BrowserOnly>
          {() => (
            <QRCodeSVG
              className="docs-print-qr"
              value={sourceUrl}
              title={sourceUrl}
              size={128}
              level="M"
              marginSize={4}
            />
          )}
        </BrowserOnly>
      </div>
      <DocItemContent {...props} />
    </>
  );
}
