import React, {useId, type ReactNode} from 'react';

function NoiseOverlay({className}: {className?: string}): ReactNode {
  const id = useId();
  const filterId = `noise-filter-${id}`;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      className={className}
      width="100%"
      height="100%"
      preserveAspectRatio="none"
    >
      <defs>
        <filter id={filterId}>
          <feTurbulence
            type="turbulence"
            baseFrequency="3"
            numOctaves="1"
            stitchTiles="stitch"
            result="noise"
          />
          <feColorMatrix
            type="matrix"
            values="0 0 0 0 0
                    0 0 0 0 0
                    0 0 0 0 0
                    0 0 0 3 0"
            result="coloredNoise"
          />
        </filter>
      </defs>
      <rect width="100%" height="100%" filter={`url(#${filterId})`} />
    </svg>
  );
}

function CheckIcon(): ReactNode {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" className="cloud-check-icon">
      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
    </svg>
  );
}

function ArrowIcon(): ReactNode {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="cloud-arrow-icon">
      <path fillRule="evenodd" d="M5.22 14.78a.75.75 0 0 0 1.06 0l7.22-7.22v5.69a.75.75 0 0 0 1.5 0v-7.5a.75.75 0 0 0-.75-.75h-7.5a.75.75 0 0 0 0 1.5h5.69l-7.22 7.22a.75.75 0 0 0 0 1.06Z" clipRule="evenodd" />
    </svg>
  );
}

export default function NightwatchSection(): ReactNode {
  return (
    <section className="nightwatch-section">
        <div className="nightwatch-section-gradient" />
        <NoiseOverlay className="nightwatch-noise-overlay" />
        <div className="nightwatch-grid">
          <div className="nightwatch-info">
            <h3>Monitor and fix issues with{' '}<br className="tablet-br" /><br className="mobile-br" />Nightwatch</h3>
            <p>
              Laravel Nightwatch gives full{' '}<br className="tablet-br" />observability to find errors and top{' '}<br className="tablet-br" />
              performance{' '}<br className="desktop-only-br" />issues in your apps, before{' '}<br className="tablet-br" />your team does.
            </p>
            <ul className="nightwatch-feature-list">
              <li>
                <CheckIcon />
                <span>Fix errors and performance with{' '}<br className="tablet-br" />recommended solutions</span>
              </li>
              <li>
                <CheckIcon />
                <span>Trace requests, jobs, logs,{' '}<br className="tablet-br" />commands, cache, and more</span>
              </li>
              <li>
                <CheckIcon />
                <span>Let agents fix your code using{' '}<br className="tablet-br" />Nightwatch MCP</span>
              </li>
            </ul>
            <div className="nightwatch-btn-wrapper">
              <a href="https://nightwatch.laravel.com" className="explore-btn">
                Explore Nightwatch
                <ArrowIcon />
              </a>
            </div>
          </div>

          <div className="nightwatch-img-outer">
            <div className="nightwatch-img-wrapper">
              <img
                src="/images/home/nightwatch-dashboard.avif"
                alt="Nightwatch dashboard screenshot"
                className="nightwatch-img"
                loading="lazy"
              />
            </div>
          </div>
        </div>
    </section>
  );
}
