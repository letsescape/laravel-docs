import React, {useId, type ReactNode} from 'react';

function NoiseOverlay(): ReactNode {
  const id = useId();
  const filterId = `noise-filter-${id}`;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      className="frontend-noise-overlay"
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

function ArrowIcon(): ReactNode {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="cloud-arrow-icon">
      <path fillRule="evenodd" d="M5.22 14.78a.75.75 0 0 0 1.06 0l7.22-7.22v5.69a.75.75 0 0 0 1.5 0v-7.5a.75.75 0 0 0-.75-.75h-7.5a.75.75 0 0 0 0 1.5h5.69l-7.22 7.22a.75.75 0 0 0 0 1.06Z" clipRule="evenodd" />
    </svg>
  );
}

/* Stroke-based outline icons matching laravel.com style */
function SvelteIcon(): ReactNode {
  return (
    <svg viewBox="0 0 24 24" fill="none" className="frontend-card-icon" stroke="#fe640b" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.274 9.282s1.915-2.728.11-5.331c-2.278-2.876-4.821-1.722-4.821-1.722S8.03 4.64 5.524 6.347C3.594 7.725 2.437 9.46 4.104 12.367c1.68 2.893 6.309 1.667 6.309 1.667" />
      <path d="M3.885 12.808s-1.915 2.728-.111 5.331c1.805 2.618 4.822 1.709 4.822 1.709s4.532-2.397 7.039-4.105c1.929-1.378 3.086-3.114 1.419-6.02-1.681-2.893-6.309-1.667-6.309-1.667M7.238 9.612l5.703-3.526M5.887 15.599l5.703-3.513" />
    </svg>
  );
}

function ReactIcon(): ReactNode {
  return (
    <svg viewBox="0 0 24 24" fill="none" className="frontend-card-icon" stroke="#1e66f5" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="12" rx="10" ry="4" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)" />
      <path d="M12.68 12a.68.68 0 1 1-1.36 0 .68.68 0 0 1 1.36 0" />
    </svg>
  );
}

function VueIcon(): ReactNode {
  return (
    <svg viewBox="0 0 24 24" fill="none" className="frontend-card-icon" stroke="#40a02b" strokeWidth="0.889" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 3h6.695l1.92 3.766L14.535 3H21.23l-8.603 16z" />
      <path d="M17.6 3.283l-4.985 9.293-4.984-9.293" />
    </svg>
  );
}

function BladeIcon(): ReactNode {
  return (
    <svg viewBox="0 0 24 24" fill="none" className="frontend-card-icon">
      <path fillRule="evenodd" clipRule="evenodd" d="M20.88 16.623c-.408.617-.718 1.377-1.547 1.377-1.395 0-1.47-2.153-2.868-2.153-1.396 0-1.32 2.153-2.716 2.153-1.395 0-1.47-2.153-2.868-2.153-1.396 0-1.32 2.153-2.716 2.153s-1.472-2.153-2.868-2.153c-1.397 0-1.32 2.153-2.717 2.153-.439 0-.747-.213-1.007-.504A11.9 11.9 0 0 1 0 11.544C0 5.168 4.925 0 11 0s11 5.168 11 11.544c0 1.822-.403 3.546-1.12 5.079" fill="#fb70a9" style={{fill: '#fb70a9'}} />
      <path fillRule="evenodd" clipRule="evenodd" d="M18.5 17.77q4.323-6.432.223-14.27a11.5 11.5 0 0 1 3.276 8.068 11.5 11.5 0 0 1-1.16 5.06c-.423.615-.744 1.372-1.604 1.372-.294 0-.531-.089-.736-.23" fill="#e24ca6" style={{fill: '#e24ca6'}} />
      <path fillRule="evenodd" clipRule="evenodd" d="M10.41 14.423c3.826 0 5.436-2.219 5.436-5.37 0-3.153-2.433-6.053-5.436-6.053-3.001 0-5.435 2.901-5.435 6.052 0 3.152 1.61 5.371 5.435 5.371" fill="#fff" style={{fill: '#fff'}} />
      <path d="M8.949 9.23c1.125 0 2.038-1.008 2.038-2.25s-.912-2.25-2.038-2.25-2.038 1.008-2.038 2.25.912 2.25 2.038 2.25" fill="#030776" style={{fill: '#030776'}} />
      <path d="M8.609 7.5a1.03 1.03 0 0 0 1.019-1.038c0-.574-.456-1.038-1.02-1.038a1.03 1.03 0 0 0-1.02 1.038 1.03 1.03 0 0 0 1.02 1.038" fill="#fff" style={{fill: '#fff'}} />
    </svg>
  );
}

const frontendCards = [
  { name: 'users.svelte', icon: <SvelteIcon />, label: 'Svelte' },
  { name: 'users.tsx', icon: <ReactIcon />, label: 'React' },
  { name: 'users.vue', icon: <VueIcon />, label: 'Vue' },
  { name: 'users.blade.php', icon: <BladeIcon />, label: 'Blade' },
];

export default function FrontendSection(): ReactNode {
  return (
    <section className="frontend-section">
        <div className="frontend-section-gradient" />
        <NoiseOverlay />
        <div className="frontend-grid">
          <div className="frontend-info">
            <h3>The best partner to any{' '}<br className="tablet-br" />front-end</h3>
            <p>
              Easily craft frontend experiences with{' '}<br className="tablet-br" />React, Vue, or Svelte
              alongside Laravel{' '}<br className="desktop-only-br" /><br className="tablet-br" />and Inertia. Or, accelerate your front-end{' '}<br className="tablet-br" />
              development with Livewire.
            </p>
            <div className="frontend-btn-wrapper">
              <a href="https://laravel.com/docs/frontend" className="explore-btn">
                Explore front-ends
                <ArrowIcon />
              </a>
            </div>
          </div>

          <div className="frontend-cards-area">
            <div className="frontend-stacked-cards">
              {frontendCards.map((card, idx) => (
                <div
                  key={card.name}
                  className="frontend-stack-card"
                  style={{
                    '--card-top': `${idx * 64}px`,
                    '--card-left': `${(frontendCards.length - 1 - idx) * 28}px`,
                    '--card-z': idx + 1,
                  } as React.CSSProperties}
                >
                  <div className="frontend-stack-card-inner">
                    <div className="frontend-card-header">
                      <div className="frontend-card-tab-label">
                        {card.icon}
                        <span className="frontend-card-filename">{card.name}</span>
                      </div>
                      <div className="frontend-card-tab-fill" aria-hidden="true" />
                    </div>
                    <div className="frontend-card-body">
                      <div className="frontend-code-row">
                        <div className="frontend-code-pill frontend-code-pill--lg" />
                        <div className="frontend-code-pill frontend-code-pill--md" />
                        <div className="frontend-code-pill frontend-code-pill--sm" />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
    </section>
  );
}
