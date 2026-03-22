import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

function NightwatchIllustration(): ReactNode {
  return (
    <div className={styles.nwIllustration}>
      <div className={styles.nwImageWrap}>
        <div className={styles.nwImageInner}>
          <img
            className={styles.nwImage}
            src="/img/nightwatch-dashboard.avif"
            loading="lazy"
            alt="Nightwatch dashboard screenshot"
          />
        </div>
      </div>
    </div>
  );
}

function FrontendIllustration(): ReactNode {
  return (
    <div className={styles.feIllustration}>
      <div className={styles.feGradient} />
      <div className={styles.feSvgWrap}>
        <svg viewBox="0 0 636 375" fill="none" xmlns="http://www.w3.org/2000/svg" className={`${styles.feSvg} fe-svg`}>
          <g clipPath="url(#fe-a)" transform="translate(0 20)">
            {/* users.svelte */}
            <g className={styles.feHoverCard}><g clipPath="url(#fe-b)"><rect x="160" y="35" width="618" height="346" rx="12" fill="#fff"/><path fill="#fff" d="M160 35h618v56H160z"/><mask id="fe-c" fill="#fff"><path d="M160 35h166.159v56H160z"/></mask><path d="M160 35h166.159v56H160z" fill="#fff"/><path d="M326.159 35h-1v56h2V35zM160 91h1V35h-2v56z" fill="#e5e5e5" mask="url(#fe-c)"/><path d="M194.274 61.282s1.915-2.728.11-5.331c-2.278-2.876-4.821-1.722-4.821-1.722s-4.532 2.41-7.039 4.118c-1.929 1.378-3.086 3.114-1.419 6.02 1.68 2.893 6.309 1.667 6.309 1.667" stroke="#fe640b" strokeLinecap="round" strokeLinejoin="round"/><path d="M180.885 64.808s-1.915 2.728-.111 5.331c1.805 2.618 4.822 1.709 4.822 1.709s4.532-2.397 7.039-4.105c1.929-1.378 3.086-3.114 1.419-6.02-1.681-2.893-6.309-1.667-6.309-1.667m-2.507 1.556 5.703-3.526m-6.778 9.987 5.703-3.513" stroke="#fe640b" strokeLinecap="round" strokeLinejoin="round"/><text fill="#171717" style={{whiteSpace: 'pre'}} fontSize="20" letterSpacing="-.04em"><tspan x="207.159" y="70.4">users.svelte</tspan></text><line x1="326" y1="35" x2="326" y2="91" stroke="#e5e5e5" strokeWidth="1"/><path d="M777.5 91.5v289h-617v-289z" fill="#fafafa"/><path d="M777.5 91.5v289h-617v-289z" stroke="#e5e5e5"/><path stroke="#e5e5e5" strokeWidth="13.287" strokeLinecap="round" strokeDasharray="83.52 17.08" d="M206.644 124.356h242.967m-242.967 45.557h394.822M206.644 215.47h305.607m-305.607 45.556h225.883"/></g><rect x="160.5" y="35.5" width="617" height="345" rx="11.5" stroke="#e5e5e5"/></g>
            {/* users.tsx */}
            <g className={styles.feHoverCard}><g clipPath="url(#fe-d)"><rect x="112" y="103" width="578" height="281" rx="12" fill="#fff"/><path fill="#fff" d="M112 103h578v56H112z"/><mask id="fe-e" fill="#fff"><path d="M112 103h147.288v56H112z"/></mask><path d="M112 103h147.288v56H112z" fill="#fff"/><path d="M259.288 103h-1v56h2v-56zM112 159h1v-56h-2v56z" fill="#e5e5e5" mask="url(#fe-e)"/><path d="M142.144 134.864c5.6 0 10.144-1.732 10.144-3.869s-4.544-3.868-10.144-3.868c-5.599 0-10.144 1.731-10.144 3.868s4.545 3.882 10.144 3.882z" stroke="#1e66f5" strokeLinecap="round" strokeLinejoin="round"/><path d="M138.79 132.929c2.8 4.869 6.574 7.926 8.427 6.858 1.853-1.082 1.082-5.871-1.718-10.726s-6.574-7.913-8.427-6.844-1.082 5.87 1.718 10.712" stroke="#1e66f5" strokeLinecap="round" strokeLinejoin="round"/><path d="M138.79 129.061c-2.8 4.856-3.571 9.657-1.718 10.726 1.853 1.068 5.627-2.002 8.427-6.858 2.8-4.842 3.571-9.643 1.718-10.712-1.853-1.082-5.627 1.988-8.427 6.844" stroke="#1e66f5" strokeLinecap="round" strokeLinejoin="round"/><path d="M142.821 130.995a.676.676 0 1 1-1.352 0 .676.676 0 0 1 1.352 0" stroke="#1e66f5" strokeLinecap="round" strokeLinejoin="round"/><text fill="#171717" style={{whiteSpace: 'pre'}} fontSize="20" letterSpacing="-.04em"><tspan x="164.289" y="138.4">users.tsx</tspan></text><line x1="259" y1="103" x2="259" y2="159" stroke="#e5e5e5" strokeWidth="1"/><path d="M689.5 159.5v224h-577v-224z" fill="#fafafa"/><path d="M689.5 159.5v224h-577v-224z" stroke="#e5e5e5"/><path stroke="#e5e5e5" strokeWidth="13.287" strokeLinecap="round" strokeDasharray="83.52 17.08" d="M158.644 192.356h242.967m-242.967 45.557h394.822M158.644 283.47h305.607m-305.607 45.556h225.883"/></g><rect x="112.5" y="103.5" width="577" height="280" rx="11.5" stroke="#e5e5e5"/></g>
            {/* users.vue */}
            <g className={styles.feHoverCard}><g clipPath="url(#fe-f)"><rect x="80" y="171" width="603" height="216" rx="12" fill="#fff"/><path fill="#fff" d="M80 171h603v56H80z"/><mask id="fe-g" fill="#fff"><path d="M80 171h149.231v56H80z"/></mask><path d="M80 171h149.231v56H80z" fill="#fff"/><path d="M229.231 171h-1v56h2v-56zM80 227h1v-56h-2v56z" fill="#e5e5e5" mask="url(#fe-g)"/><path d="M100 191h6.695l1.92 3.766 1.92-3.766h6.696l-8.603 16z" stroke="#40a02b" strokeWidth="0.889" strokeLinecap="round" strokeLinejoin="round"/><path d="m113.6 191.283-4.985 9.293-4.984-9.293" stroke="#40a02b" strokeWidth="0.889" strokeLinecap="round" strokeLinejoin="round"/><text fill="#171717" style={{whiteSpace: 'pre'}} fontSize="20" letterSpacing="-.04em"><tspan x="129.231" y="206.4">users.vue</tspan></text><line x1="229" y1="171" x2="229" y2="227" stroke="#e5e5e5" strokeWidth="1"/><path fill="#fafafa" d="M80.5 227.5h602v159h-602z"/><path stroke="#e5e5e5" d="M80.5 227.5h602v159h-602z"/><path stroke="#e5e5e5" strokeWidth="13.287" strokeLinecap="round" strokeDasharray="83.52 17.08" d="M132.2 265.913h242.967M132.2 311.47h394.822M132.2 357.026h305.607"/></g><rect x="80.5" y="171.5" width="602" height="215" rx="11.5" stroke="#e5e5e5"/></g>
            {/* users.blade.php */}
            <g className={styles.feHoverCard}><g clipPath="url(#fe-h)"><rect x="48" y="239" width="603" height="216" rx="12" fill="#fff"/><path fill="#fff" d="M48 239h603v56H48z"/><mask id="fe-i" fill="#fff"><path d="M48 239h210v56H48z"/></mask><path d="M48 239h210v56H48z" fill="#fff"/><path d="M258 239h-1v56h2v-56zM48 295h1v-56h-2v56z" fill="#e5e5e5" mask="url(#fe-i)"/><path fillRule="evenodd" clipRule="evenodd" d="M88.88 274.623c-.408.617-.718 1.377-1.547 1.377-1.395 0-1.47-2.153-2.868-2.153-1.396 0-1.32 2.153-2.716 2.153-1.395 0-1.47-2.153-2.868-2.153-1.396 0-1.32 2.153-2.716 2.153s-1.472-2.153-2.868-2.153c-1.397 0-1.32 2.153-2.717 2.153-.439 0-.747-.213-1.007-.504A11.9 11.9 0 0 1 68 269.544C68 263.168 72.925 258 79 258s11 5.168 11 11.544c0 1.822-.403 3.546-1.12 5.079" style={{fill: '#fb70a9'}}/><path fillRule="evenodd" clipRule="evenodd" d="M86.5 275.77q4.323-6.432.223-14.27a11.5 11.5 0 0 1 3.276 8.068 11.5 11.5 0 0 1-1.16 5.06c-.423.615-.744 1.372-1.604 1.372-.294 0-.531-.089-.736-.23" style={{fill: '#e24ca6'}}/><path fillRule="evenodd" clipRule="evenodd" d="M78.41 272.423c3.826 0 5.436-2.219 5.436-5.37 0-3.153-2.433-6.053-5.436-6.053-3.001 0-5.435 2.901-5.435 6.052 0 3.152 1.61 5.371 5.435 5.371" style={{fill: '#fff'}}/><path d="M76.949 267.23c1.125 0 2.038-1.008 2.038-2.25s-.912-2.25-2.038-2.25-2.038 1.008-2.038 2.25.912 2.25 2.038 2.25" style={{fill: '#030776'}}/><path d="M76.609 265.5a1.03 1.03 0 0 0 1.019-1.038c0-.574-.456-1.038-1.02-1.038a1.03 1.03 0 0 0-1.02 1.038 1.03 1.03 0 0 0 1.02 1.038" style={{fill: '#fff'}}/><text fill="#171717" style={{whiteSpace: 'pre'}} fontSize="20" letterSpacing="-.04em"><tspan x="102" y="274.4">users.blade.php</tspan></text><line x1="258" y1="239" x2="258" y2="295" stroke="#e5e5e5" strokeWidth="1"/><path fill="#fafafa" d="M48.5 295.5h602v159h-602z"/><path stroke="#e5e5e5" d="M48.5 295.5h602v159h-602z"/><path stroke="#e5e5e5" strokeWidth="13.287" strokeLinecap="round" strokeDasharray="83.52 17.08" d="M94.644 328.356h242.967M94.644 373.913h394.822"/></g><rect x="48.5" y="239.5" width="602" height="215" rx="11.5" stroke="#e5e5e5"/></g>
          </g>
          <defs>
            <clipPath id="fe-a"><path fill="#fff" d="M0 0h636v375H0z"/></clipPath>
            <clipPath id="fe-b"><rect x="160" y="35" width="618" height="346" rx="12" fill="#fff"/></clipPath>
            <clipPath id="fe-d"><rect x="112" y="103" width="578" height="281" rx="12" fill="#fff"/></clipPath>
            <clipPath id="fe-f"><rect x="80" y="171" width="603" height="216" rx="12" fill="#fff"/></clipPath>
            <clipPath id="fe-h"><rect x="48" y="239" width="603" height="216" rx="12" fill="#fff"/></clipPath>
          </defs>
        </svg>
      </div>
    </div>
  );
}

export default function NightwatchFrontendSection(): ReactNode {
  return (
    <section className={styles.nfSection}>
      <div className={styles.nfLineLeft} />
      <div className={styles.nfLineRight} />
      <div className={styles.nfLineCenter} />
      <span className={styles.nfDotBL} />
      <span className={styles.nfDotBR} />
      <div className={styles.nfLineBottom} />
      <div className={styles.nfLineBottomLeft} />
      <div className={styles.nfLineBottomRight} />
      <div className={styles.nfGrid}>
        {/* Nightwatch */}
        <div className={styles.nfCard}>
          <div className={styles.nwGradient} />
          <div className={styles.nfCardContent}>
            <h3 className={styles.sectionTitle}>
              Monitor and fix issues with Nightwatch
            </h3>
            <p className={styles.sectionDescription}>
              Laravel Nightwatch gives full observability to find errors
              and top performance issues in your apps, before your team does.
            </p>
            <ul className={styles.featureList}>
              <li>Fix errors and performance with recommended solutions</li>
              <li>Trace requests, jobs, logs, commands, cache, and more</li>
              <li>Let agents fix your code using Nightwatch MCP</li>
            </ul>
            <Link className={styles.ctaLink} to="https://nightwatch.laravel.com">
              Explore Nightwatch
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M4 12L12 4M12 4H5M12 4v7" stroke="#f53003" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
          </div>
          <NightwatchIllustration />
        </div>

        {/* Frontend */}
        <div className={styles.nfCard}>
          <div className={styles.nfCardContent}>
            <h3 className={styles.sectionTitle}>
              The best partner to any front-end
            </h3>
            <p className={styles.sectionDescription}>
              Easily craft frontend experiences with React, Vue, or Svelte alongside Laravel<br />
              and Inertia. Or, accelerate your front-end development with Livewire.
            </p>
            <Link className={styles.ctaLink} to="/docs/12.x/frontend">
              Explore front-ends
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M4 12L12 4M12 4H5M12 4v7" stroke="#f53003" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
          </div>
          <FrontendIllustration />
        </div>
      </div>
    </section>
  );
}
