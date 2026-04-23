import React, {useState, useRef, useCallback, type ReactNode} from 'react';
import Translate, {translate} from '@docusaurus/Translate';
import {ArrowIcon} from './SharedIcons';

const events = [
  {
    name: 'Laravel Live Japan',
    date: 'May 26-27',
    year: '2026',
    city: 'Tokyo',
    cityKo: '도쿄',
    country: 'JP',
    ticketUrl: 'https://laravellive.jp/en',
    image: '/images/home/event-japan.webp',
    logo: '/images/home/event-logo-japan.png',
    logoSmall: true,
  },
  {
    name: 'Laravel Live UK',
    date: 'Jun 18-19',
    year: '2026',
    city: 'London',
    cityKo: '런던',
    country: 'UK',
    ticketUrl: 'https://laravellive.uk/',
    image: '/images/home/event-uk.webp',
    logo: '/images/home/event-logo-uk.svg',
    metaAlignEnd: true,
  },
  {
    name: 'Laracon US',
    date: 'Jul 28-29',
    year: '2026',
    city: 'Boston',
    cityKo: '보스턴',
    country: 'US',
    ticketUrl: 'https://laracon.us',
    image: '/images/home/event-us.webp',
    logo: '/images/home/event-logo-us.svg',
    logoMedium: true,
    metaAlignEnd: true,
  },
  {
    name: 'Laravel Live Denmark',
    date: 'Aug 20-21',
    year: '2026',
    city: 'Copenhagen',
    cityKo: '코펜하겐',
    country: 'DK',
    ticketUrl: 'https://laravellive.dk/',
    image: '/images/home/event-dk.webp',
    logo: '/images/home/event-logo-dk.png',
    metaAlignEnd: true,
  },
];

export default function EventsSection(): ReactNode {
  // Track position uses 1-based index because slide 0 is the last clone
  const [pos, setPos] = useState(1);
  const [animate, setAnimate] = useState(true);
  const trackRef = useRef<HTMLDivElement>(null);
  const isTransitioning = useRef(false);

  const total = events.length;
  // Build slides: [clone-last, ...originals, clone-first]
  const slides = [events[total - 1], ...events, events[0]];

  // 캐러셀 비활성 동안 displayCity / cityAnimating 애니메이션 상태 제거.
  // 재활성 시 H2 의 <Translate id="homepage.events.title.city"> 자리를
  // {displayCity} 로 돌리고 관련 state / useEffect 를 복구할 것.

  const handleTransitionEnd = useCallback(() => {
    isTransitioning.current = false;
    if (pos <= 0) {
      setAnimate(false);
      setPos(total);
    } else if (pos >= total + 1) {
      setAnimate(false);
      setPos(1);
    }
  }, [pos, total]);

  // Re-enable animation after instant jump
  React.useEffect(() => {
    if (!animate) {
      requestAnimationFrame(() => {
        setAnimate(true);
      });
    }
  }, [animate]);

  const goPrev = () => {
    if (isTransitioning.current) return;
    isTransitioning.current = true;
    setAnimate(true);
    setPos(prev => prev - 1);
  };

  const goNext = () => {
    if (isTransitioning.current) return;
    isTransitioning.current = true;
    setAnimate(true);
    setPos(prev => prev + 1);
  };

  return (
    <>
      {/* Header */}
      <section className="events-section hp-section hp-section-bordered">
        <div className="container">
          <div className="events-label">
            <span className="events-bracket">[</span>
            <span><Translate id="homepage.events.label" description="Events 섹션 라벨">Events</Translate></span>
            <span className="events-bracket">]</span>
          </div>
          <h2>
            <span className="events-city-wrapper">
              <span className="events-city-highlight events-city--in">
                <Translate id="homepage.events.title.city" description="Events 섹션 제목 - 강조 단어">이벤트</Translate>
              </span>
            </span>
            <Translate id="homepage.events.title.suffix" description="Events 섹션 제목 접미사 (강조 단어 뒤에 옴)">에서 만나요</Translate>
          </h2>
          <p className="events-description">
            <Translate id="homepage.events.desc" description="Events 섹션 설명">
              라라벨은 멋진 커뮤니티로 유명합니다. 온라인에서 시작된 우정이 34개가 넘는 국가의 Laracon, Live, 밋업에서 실제 만남으로 이어집니다.
            </Translate>
          </p>
          <div className="events-link-wrapper">
            <a href="https://laravel.com/events" className="explore-btn" target="_blank" rel="noopener noreferrer">
              <Translate id="homepage.events.cta" description="Events CTA 링크">근처 밋업 찾기</Translate>
              <ArrowIcon />
            </a>
          </div>
        </div>
      </section>

      {/* Carousel - 일시 비활성화 (단일 트랙, 슬라이드가 뷰포트 거터로 넘침) */}
      {false && (
      <section className="events-carousel-section">
        <div className="events-carousel-container">
          <div
            ref={trackRef}
            className={`events-carousel-track ${animate ? '' : 'events-carousel-track--no-transition'}`}
            style={{transform: `translateX(calc(-${pos} * var(--slide-width)))`}}
            onTransitionEnd={handleTransitionEnd}
          >
            {slides.map((event, idx) => (
              <div key={`${event.name}-${idx}`} className={`events-slide ${idx === pos ? 'events-slide--active' : ''}`}>
                <div className="events-slide-card">
                  <img
                    src={event.image}
                    alt={event.name}
                    className="events-slide-image"
                    loading="lazy"
                  />
                  <div className="events-slide-overlay" />
                  <div className="events-slide-content">
                    <div className={`events-slide-info ${event.metaAlignEnd ? 'events-slide-info--align-end' : ''}`}>
                      <img src={event.logo} alt={event.name} className={`events-slide-logo ${event.logoSmall ? 'events-slide-logo--sm' : ''} ${event.logoMedium ? 'events-slide-logo--md' : ''}`} loading="lazy" />
                      <div className="events-slide-meta">
                        <div className="events-slide-date">{event.date}</div>
                        <div className="events-slide-year">{event.year}</div>
                        <div className="events-slide-city">{event.cityKo}</div>
                        <div className="events-slide-country">{event.country}</div>
                      </div>
                    </div>
                    <a
                      href={event.ticketUrl}
                      className="events-slide-ticket"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Translate id="homepage.events.ticket" description="이벤트 티켓 CTA">티켓 받기</Translate>
                      <ArrowIcon />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <button className="events-nav-btn events-nav-btn--prev" onClick={goPrev} aria-label={translate({id: 'homepage.events.nav.prev', message: '이전 이벤트', description: '이벤트 캐러셀 이전 버튼 aria-label'})} type="button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M15 18l-6-6 6-6" /></svg>
          </button>
          <button className="events-nav-btn events-nav-btn--next" onClick={goNext} aria-label={translate({id: 'homepage.events.nav.next', message: '다음 이벤트', description: '이벤트 캐러셀 다음 버튼 aria-label'})} type="button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M9 18l6-6-6-6" /></svg>
          </button>
        </div>
      </section>
      )}
    </>
  );
}
