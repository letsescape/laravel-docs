import React, {type ReactNode} from 'react';
import {CheckIcon, ArrowIcon, NoiseOverlay} from './SharedIcons';

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
                <CheckIcon className="cloud-check-icon" />
                <span>Fix errors and performance with{' '}<br className="tablet-br" />recommended solutions</span>
              </li>
              <li>
                <CheckIcon className="cloud-check-icon" />
                <span>Trace requests, jobs, logs,{' '}<br className="tablet-br" />commands, cache, and more</span>
              </li>
              <li>
                <CheckIcon className="cloud-check-icon" />
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
