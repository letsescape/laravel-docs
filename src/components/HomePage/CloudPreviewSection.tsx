import React, {useState, useEffect, type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

const badgeStates = ['Idling', 'Scaling up', 'Scaling down'];

function CornerDots(): ReactNode {
  return (
    <>
      <span className={`${styles.cornerDot} ${styles.cornerTL}`} />
      <span className={`${styles.cornerDot} ${styles.cornerTR}`} />
      <span className={`${styles.cornerDot} ${styles.cornerBL}`} />
      <span className={`${styles.cornerDot} ${styles.cornerBR}`} />
    </>
  );
}

function CloudIllustration(): ReactNode {
  const [badgeIndex, setBadgeIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setBadgeIndex(i => (i + 1) % badgeStates.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={styles.cloudIllustration}>
      {/* Badge */}
      <div className={styles.cloudBadge} key={badgeStates[badgeIndex]}>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="7" r="5.5" stroke="#6366f1" strokeWidth="1.5"/>
          <path d="M7 4v3.5l2 1" stroke="#6366f1" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
        {badgeStates[badgeIndex]}
      </div>

      {/* Outer card shell with field lines anchored to its vertical center */}
      <div className={styles.cloudFieldAnchor}>
        <svg className={styles.fieldLines} viewBox="-250 -130 500 260" fill="none" style={{width: '850px', height: '260px'}}>
          {[50, 100, 150].map((height, i) => {
            const cy = 0;
            const edgeY = cy - height;
            const flatY = cy - 18 * (i + 1);
            const halfFlat = 250;
            const r = 100;
            const d = `M-500,${edgeY} L${-halfFlat - r * 2.5},${edgeY} C${-halfFlat - r},${flatY} ${-halfFlat},${flatY} ${-halfFlat + r},${flatY} L${halfFlat - r},${flatY} C${halfFlat},${flatY} ${halfFlat + r},${flatY} ${halfFlat + r * 2.5},${edgeY} L500,${edgeY}`;
            return <path key={`above-${i}`} d={d} stroke="#d5d5d5" strokeWidth="1" strokeDasharray="5 4" fill="none"/>;
          })}
          <line x1="-500" y1="0" x2="500" y2="0" stroke="#d5d5d5" strokeWidth="1" strokeDasharray="5 4"/>
          {[50, 100, 150].map((height, i) => {
            const cy = 0;
            const edgeY = cy + height;
            const flatY = cy + 18 * (i + 1);
            const halfFlat = 250;
            const r = 100;
            const d = `M-500,${edgeY} L${-halfFlat - r * 2.5},${edgeY} C${-halfFlat - r},${flatY} ${-halfFlat},${flatY} ${-halfFlat + r},${flatY} L${halfFlat - r},${flatY} C${halfFlat},${flatY} ${halfFlat + r},${flatY} ${halfFlat + r * 2.5},${edgeY} L500,${edgeY}`;
            return <path key={`below-${i}`} d={d} stroke="#d5d5d5" strokeWidth="1" strokeDasharray="5 4" fill="none"/>;
          })}
          {/* Blue & orange dots */}
          <circle cx="-320" cy="0" r="4" fill="#3b82f6"/>
          <circle cx="-290" cy="0" r="5" fill="#f97316"/>
        </svg>
      <div className={styles.cloudOuter}>
        <div className={styles.cloudInner}>
          {/* Main panel */}
          <div className={styles.cloudMainPanel}>
            <CornerDots />
            <div className={styles.cloudPanelHeader}>
              <span className={styles.cloudDotFilled} />
              <span className={styles.cloudBinary}>01100010 01100101 01100101</span>
              <span className={styles.cloudDotFilled} />
            </div>
            <div className={styles.cloudPanelBody}>
              {/* Laravel logo icon - stacked squares */}
              <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <rect x="16" y="20" width="28" height="28" rx="3" fill="#222" opacity="0.8"/>
                <rect x="20" y="16" width="28" height="28" rx="3" fill="#333" opacity="0.85"/>
                <rect x="24" y="12" width="28" height="28" rx="3" fill="#111"/>
                <rect x="32" y="18" width="14" height="14" rx="2" fill="#fff" opacity="0.9"/>
              </svg>
            </div>
            <div className={styles.cloudPanelFooter}>
              <span className={styles.cloudDotFilled} />
              <span className={styles.cloudBinary}>01100010 01100101 01100101</span>
              <span className={styles.cloudDotFilled} />
            </div>
          </div>

          {/* Side panels */}
          <div className={styles.cloudSidePanels}>
            <div className={styles.cloudSidePanel}>
              <CornerDots />
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#999" strokeWidth="1.2">
                <ellipse cx="12" cy="6" rx="7" ry="2.5"/>
                <path d="M5 6v5c0 1.38 3.13 2.5 7 2.5s7-1.12 7-2.5V6"/>
                <path d="M5 11v5c0 1.38 3.13 2.5 7 2.5s7-1.12 7-2.5v-5"/>
              </svg>
            </div>
            <div className={styles.cloudSidePanel}>
              <CornerDots />
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#999" strokeWidth="1.2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                <path d="M2 17l10 5 10-5"/>
                <path d="M2 12l10 5 10-5"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}

function PreviewIllustration(): ReactNode {
  const containerRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    fetch('/img/preview-illustration.svg')
      .then(res => res.text())
      .then(svgText => {
        el.innerHTML = svgText;
        const svg = el.querySelector('svg');
        if (!svg) return;
        svg.style.width = '100%';
        svg.style.height = '100%';
        // Force inline styles on fills/strokes to override global CSS
        svg.querySelectorAll('[fill]').forEach(e => {
          const fill = e.getAttribute('fill');
          if (fill && fill !== 'none') (e as HTMLElement).style.setProperty('fill', fill, 'important');
        });
        svg.querySelectorAll('[stroke]').forEach(e => {
          const stroke = e.getAttribute('stroke');
          if (stroke) (e as HTMLElement).style.setProperty('stroke', stroke, 'important');
        });
      });
  }, []);

  return (
    <div className={styles.previewIllustration}>
      <div ref={containerRef} className={styles.previewSvgContainer} />
    </div>
  );
}

export default function CloudPreviewSection(): ReactNode {
  return (
    <section className={styles.twoColSection}>
      <div className={styles.twoColLineLeft} />
      <div className={styles.twoColLineRight} />
      <span className={styles.twoColDotBL} />
      <span className={styles.twoColDotBR} />
      <div className={styles.twoColLineBottom} />
      <div className={styles.twoColLineBottomLeft} />
      <div className={styles.twoColLineBottomRight} />
      <div className={styles.twoColLineCenter} />
      <div className={styles.twoColGrid}>
        {/* Laravel Cloud */}
        <div className={styles.twoColCard}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              Laravel Cloud takes you from local to live in seconds
            </h2>
            <p className={styles.sectionDescription}>
              No more guessing how many servers you need: autoscale up under load and hibernate when<br />
              idle. Only pay for what you actually use.
            </p>
          </div>
          <ul className={styles.featureList}>
            <li>Full control via dashboard or CLI</li>
            <li>Instantly add databases, workers, cache, and storage</li>
          </ul>
          <Link className={styles.ctaLink} to="/docs/12.x">
            Explore Laravel Cloud
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M4 12L12 4M12 4H5M12 4v7" stroke="#f53003" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
          <CloudIllustration />
        </div>

        {/* Preview Environments */}
        <div className={styles.twoColCard}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              Check pull requests from your team<br />
              (or agents) in preview environments
            </h2>
            <p className={styles.sectionDescription}>
              Review every change in Cloud's zero-risk, production-like<br />
              preview environment before it ever hits your main branch.
            </p>
          </div>
          <ul className={styles.featureList}>
            <li>Integrates seamlessly with GitHub Actions</li>
            <li>Test migrations and heavy changes safely</li>
          </ul>
          <Link className={styles.ctaLink} to="/docs/12.x">
            Explore Preview Environments
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M4 12L12 4M12 4H5M12 4v7" stroke="#f53003" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
          <PreviewIllustration />
        </div>
      </div>
    </section>
  );
}
