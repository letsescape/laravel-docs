import React, {type ReactNode} from 'react';
import Translate from '@docusaurus/Translate';

export default function CTASection(): ReactNode {
  return (
    <section className="cta-section hp-section hp-section-bordered">
      <div className="container">
        <h2>
          <Translate id="homepage.cta.title.part1" description="CTA 제목 앞">한계 없이 만들어 보세요.</Translate>
          <br />
          <Translate id="homepage.cta.title.part2" description="CTA 제목 뒤">무엇을 만들어 내시겠습니까?</Translate>
        </h2>
        <div className="cta-buttons">
          <a href="https://cloud.laravel.com" className="cta-primary" target="_blank" rel="noopener noreferrer">
            <Translate id="homepage.cta.deploy" description="CTA - 클라우드 배포 버튼">Cloud에 배포하기</Translate>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="18" height="18" className="cta-arrow-icon" aria-hidden="true">
              <path fill="currentColor" fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" />
            </svg>
          </a>
          <a href="/docs/12.x" className="explore-btn">
            <Translate id="homepage.cta.docs" description="CTA - 프레임워크 문서 보기">프레임워크 문서 보기</Translate>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="16" height="16" className="explore-btn-icon" aria-hidden="true">
              <path fillRule="evenodd" d="M5.22 14.78a.75.75 0 0 0 1.06 0l7.22-7.22v5.69a.75.75 0 0 0 1.5 0v-7.5a.75.75 0 0 0-.75-.75h-7.5a.75.75 0 0 0 0 1.5h5.69l-7.22 7.22a.75.75 0 0 0 0 1.06Z" clipRule="evenodd" />
            </svg>
          </a>
        </div>
      </div>
    </section>
  );
}
