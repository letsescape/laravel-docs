import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import BrowserOnly from '@docusaurus/BrowserOnly';
import styles from './HeroSection.module.css';

export default function HeroSection(): ReactNode {
  return (
    <header className={styles.hero}>
      <div className={styles.container}>
        {/* Grid background for mobile */}
        <div className={styles.mobileGrid}>
          <svg className={styles.mobileGridSvg} width="100%" height="100%">
            <defs>
              <pattern id="grid-mobile" x="-1" y="-1" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="transparent" stroke="currentColor" strokeWidth="1" />
              </pattern>
            </defs>
            <rect fill="url(#grid-mobile)" width="100%" height="100%" />
          </svg>
        </div>

        {/* Text content */}
        <section className={styles.section}>
          <div className={styles.content}>
            <h1 className={styles.title}>
              The clean stack for Artisans and agents.
            </h1>
            <p className={styles.subtitle}>
              Laravel is batteries-included so everyone can build and ship web apps at ridiculous speed.
            </p>
            <div className={styles.buttons}>
              <Link
                className={styles.btnPrimary}
                to="https://cloud.laravel.com"
              >
                Deploy on Cloud{' '}
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="16" height="16" className={`${styles.btnArrow} btn-arrow-icon`}>
                  <path fill="currentColor" fillRule="evenodd" d="M2 10a.75.75 0 0 1 .75-.75h12.59l-2.1-1.95a.75.75 0 1 1 1.02-1.1l3.5 3.25a.75.75 0 0 1 0 1.1l-3.5 3.25a.75.75 0 1 1-1.02-1.1l2.1-1.95H2.75A.75.75 0 0 1 2 10Z" clipRule="evenodd" />
                </svg>
              </Link>
              <Link
                className={styles.btnSecondary}
                to="/docs/12.x"
              >
                View framework docs
              </Link>
            </div>
          </div>
        </section>

        {/* Isometric illustration */}
        <div className={styles.illustrationWrapper} aria-hidden="true">
          <BrowserOnly>
            {() => {
              const HeroIllustration = require('./HeroIllustration').default;
              return <HeroIllustration />;
            }}
          </BrowserOnly>
        </div>
      </div>
    </header>
  );
}
