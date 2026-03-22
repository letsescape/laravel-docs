import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function CTASection(): ReactNode {
  return (
    <section className={styles.ctaSection}>
      <div className={styles.ctaLineBottom} />
      <div className={styles.ctaLineLeft} />
      <div className={styles.ctaLineRight} />
      <span className={styles.ctaDotBL} />
      <span className={styles.ctaDotBR} />
      <div className={styles.container}>
        <h2 className={styles.ctaTitle}>
          Create without limits.
          <br />
          What will you ship?
        </h2>
        <div className={styles.ctaButtons}>
          <Link className={styles.ctaBtnPrimary} to="https://cloud.laravel.com">
            Deploy on Cloud
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="#fff" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
          <Link className={styles.ctaBtnSecondary} to="/docs/12.x">
            View framework docs
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M4 12L12 4M12 4H5M12 4v7" stroke="#f53003" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
}
