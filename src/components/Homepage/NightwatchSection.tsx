import React, {type ReactNode} from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Translate, {translate} from '@docusaurus/Translate';
import {CheckIcon, ArrowIcon, NoiseOverlay} from './SharedIcons';

export default function NightwatchSection(): ReactNode {
  const dashboardUrl = useBaseUrl('/images/home/nightwatch-dashboard.avif');
  return (
    <section className="nightwatch-section">
        <div className="nightwatch-section-gradient" />
        <NoiseOverlay className="nightwatch-noise-overlay" />
        <div className="nightwatch-grid">
          <div className="nightwatch-info">
            <h3>
              <Translate id="homepage.nightwatch.title" description="Nightwatch 섹션 제목">
                Nightwatch로 이슈를 모니터링하고 해결하세요
              </Translate>
            </h3>
            <p>
              <Translate id="homepage.nightwatch.desc" description="Nightwatch 섹션 설명">
                Laravel Nightwatch는 팀이 알아차리기 전에 앱의 오류와 주요 성능 이슈를 찾을 수 있도록 완전한 관찰성을 제공합니다.
              </Translate>
            </p>
            <ul className="nightwatch-feature-list">
              <li>
                <CheckIcon className="cloud-check-icon" />
                <span><Translate id="homepage.nightwatch.feature.fix" description="Nightwatch 기능 1">추천 해결책으로 오류와 성능 문제 수정</Translate></span>
              </li>
              <li>
                <CheckIcon className="cloud-check-icon" />
                <span><Translate id="homepage.nightwatch.feature.trace" description="Nightwatch 기능 2">요청, 작업, 로그, 명령어, 캐시 등 추적</Translate></span>
              </li>
              <li>
                <CheckIcon className="cloud-check-icon" />
                <span><Translate id="homepage.nightwatch.feature.mcp" description="Nightwatch 기능 3">Nightwatch MCP로 에이전트가 직접 코드 수정</Translate></span>
              </li>
            </ul>
            <div className="nightwatch-btn-wrapper">
              <a href="https://nightwatch.laravel.com" className="explore-btn">
                <Translate id="homepage.nightwatch.cta" description="Nightwatch CTA 링크">Nightwatch 살펴보기</Translate>
                <ArrowIcon />
              </a>
            </div>
          </div>

          <div className="nightwatch-img-outer">
            <div className="nightwatch-img-wrapper">
              <img
                src={dashboardUrl}
                alt={translate({id: 'homepage.nightwatch.img.alt', message: 'Nightwatch 대시보드 스크린샷', description: 'Nightwatch 대시보드 이미지 alt'})}
                className="nightwatch-img"
                loading="lazy"
              />
            </div>
          </div>
        </div>
    </section>
  );
}
