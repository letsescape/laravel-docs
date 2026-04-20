import React, {useState, useRef, useCallback, useEffect, type ReactNode} from 'react';
import {ArrowIcon} from './SharedIcons';

const events = [
  {
    name: 'Laravel Live Japan',
    date: 'May 26-27',
    year: '2026',
    city: 'Tokyo',
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

  const realIndex = ((pos - 1) % total + total) % total;
  const activeEvent = events[realIndex];

  // City slide-up animation
  const [displayCity, setDisplayCity] = useState(activeEvent.city);
  const [cityAnimating, setCityAnimating] = useState(false);

  useEffect(() => {
    if (activeEvent.city !== displayCity) {
      setCityAnimating(true);
      const timer = setTimeout(() => {
        setDisplayCity(activeEvent.city);
        setCityAnimating(false);
      }, 200);
      return () => clearTimeout(timer);
    }
  }, [activeEvent.city, displayCity]);

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
            <span>Events</span>
            <span className="events-bracket">]</span>
          </div>
          <h2>We'll see you in{' '}
            <span className="events-city-wrapper">
              <span className={`events-city-highlight ${cityAnimating ? 'events-city--out' : 'events-city--in'}`}>
                {displayCity}
              </span>
            </span>
          </h2>
          <p className="events-description">
            Laravel is best known for its amazing community,{' '}<br className="mobile-br" />where online friendships{' '}<br className="tablet-br" />transform{' '}<br className="desktop-only-br" />
            into real-{' '}<br className="mobile-br" />world connections at Laracons, Lives, and{' '}<br className="mobile-br" />meetups in over{' '}<br className="tablet-br" />34 countries.
          </p>
          <div className="events-link-wrapper">
            <a href="/events" className="explore-btn">
              Find nearby meetups
              <ArrowIcon />
            </a>
          </div>
        </div>
      </section>

      {/* Carousel - single track, slides overflow into viewport gutters */}
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
                        <div className="events-slide-city">{event.city}</div>
                        <div className="events-slide-country">{event.country}</div>
                      </div>
                    </div>
                    <a
                      href={event.ticketUrl}
                      className="events-slide-ticket"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Claim your ticket
                      <ArrowIcon />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <button className="events-nav-btn events-nav-btn--prev" onClick={goPrev} aria-label="Previous event" type="button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M15 18l-6-6 6-6" /></svg>
          </button>
          <button className="events-nav-btn events-nav-btn--next" onClick={goNext} aria-label="Next event" type="button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M9 18l6-6-6-6" /></svg>
          </button>
        </div>
      </section>
    </>
  );
}
