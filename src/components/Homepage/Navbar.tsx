import React, {useState, useEffect, useRef, useCallback, type ReactNode} from 'react';
import './homepage.css';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
type DropdownName = 'framework' | 'products' | 'resources' | 'events';

// ---------------------------------------------------------------------------
// Chevron icon shared by dropdown triggers
// ---------------------------------------------------------------------------
function ChevronDown({open}: {open: boolean}) {
  return (
    <svg
      width="12"
      height="12"
      viewBox="0 0 12 12"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="nav-chevron"
      style={{transform: open ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 200ms'}}
    >
      <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Main Navbar Component
// ---------------------------------------------------------------------------
export default function Navbar(): ReactNode {
  const [openDropdown, setOpenDropdown] = useState<DropdownName | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileAccordion, setMobileAccordion] = useState<string | null>(null);
  const navRef = useRef<HTMLElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (navRef.current && !navRef.current.contains(e.target as Node)) {
        setOpenDropdown(null);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  // Close mobile menu on resize above breakpoint
  useEffect(() => {
    function handleResize() {
      if (window.innerWidth >= 768) {
        setMobileOpen(false);
        setMobileAccordion(null);
      }
    }
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleDropdown = useCallback((name: DropdownName) => {
    setOpenDropdown(prev => (prev === name ? null : name));
  }, []);

  const triggerSearch = useCallback(() => {
    document.dispatchEvent(new KeyboardEvent('keydown', {key: 'k', code: 'KeyK', ctrlKey: true, bubbles: true}));
  }, []);

  const isOpen = (name: DropdownName) => openDropdown === name;
  const dataState = (name: DropdownName) => (isOpen(name) ? 'open' : 'closed');

  return (
    <nav
      ref={navRef}
      aria-label="Main"
      className="nav-main"
    >
      <div className="nav-container">
        {/* ---- Left side ---- */}
        <div className="nav-left">
          {/* Logo */}
          <a href="/" className="nav-logo-link" aria-label="Laravel">
            <img src="/img/logotype.min.svg" alt="Laravel" className="nav-logo-img" />
          </a>

          {/* Desktop nav items */}
          <div className="nav-desktop-items">
            {(['framework', 'products', 'resources', 'events'] as DropdownName[]).map(name => (
              <button
                key={name}
                id={`trigger-${name}`}
                aria-controls={`content-${name}`}
                aria-expanded={isOpen(name)}
                data-state={dataState(name)}
                className="nav-dropdown-trigger"
                onClick={() => toggleDropdown(name)}
              >
                {name.charAt(0).toUpperCase() + name.slice(1)}
                <ChevronDown open={isOpen(name)} />
              </button>
            ))}
            <a href="/docs" className="nav-docs-link">Docs</a>
          </div>
        </div>

        {/* ---- Right side ---- */}
        <div className="nav-right">
          <button
            className="nav-search-btn"
            onClick={triggerSearch}
            aria-label="Search docs"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M11.25 11.25L14 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              <circle cx="7" cy="7" r="5.25" stroke="currentColor" strokeWidth="1.5"/>
            </svg>
            <span>Search docs</span>
            <kbd className="nav-kbd">⌘K</kbd>
          </button>
        </div>

        {/* ---- Mobile hamburger ---- */}
        <button
          className="nav-hamburger"
          aria-label="Open navigation menu"
          onClick={() => setMobileOpen(true)}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>

      {/* ===================== Desktop Dropdown Panels ===================== */}

      {/* Framework */}
      {isOpen('framework') && (
        <div id="content-framework" data-state={dataState('framework')} className="nav-dropdown-panel">
          <div className="nav-dropdown-inner nav-framework-grid">
            {/* Explore Laravel */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Explore Laravel</h3>
              <a href="/" className="nav-dd-link">Overview</a>
              <a href="/docs/changelog" className="nav-dd-link">Changelog</a>
              <a href="/learn" className="nav-dd-link">Laravel Learn</a>
            </div>
            {/* Latest packages */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Latest packages</h3>
              <a href="/ai" className="nav-dd-link">AI SDK</a>
              <a href="/ai/boost" className="nav-dd-link">Boost</a>
              <a href="https://github.com/laravel/wayfinder" className="nav-dd-link">Wayfinder</a>
            </div>
            {/* Documentation */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Documentation</h3>
              <a href="/docs/installation" className="nav-dd-link">Installation</a>
              <a href="/docs/agent" className="nav-dd-link">Agent Setup</a>
              <a href="/docs/eloquent" className="nav-dd-link">Eloquent ORM</a>
              <a href="/docs/artisan" className="nav-dd-link">Artisan Console</a>
              <a href="/docs/routing" className="nav-dd-link">Routing</a>
              <a href="/docs" className="nav-dd-link nav-dd-viewall">View all</a>
            </div>
            {/* Starter kits */}
            <div className="nav-dd-col">
              <a href="/starter-kits" className="nav-dd-link nav-dd-starter-link">Starter kits</a>
              <div className="nav-dd-file-tabs">
                <span className="nav-dd-file-tab">users.svelte</span>
                <span className="nav-dd-file-tab">users.tsx</span>
                <span className="nav-dd-file-tab">users.vue</span>
                <span className="nav-dd-file-tab">users.blade.php</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Products */}
      {isOpen('products') && (
        <div id="content-products" data-state={dataState('products')} className="nav-dropdown-panel">
          <div className="nav-dropdown-inner nav-products-grid">
            <a href="https://cloud.laravel.com" className="nav-product-card">
              <span className="nav-product-name">Cloud</span>
              <span className="nav-product-desc">The fastest way to deploy and scale Laravel applications</span>
              <span className="nav-product-cta">Deploy now</span>
            </a>
            <a href="https://forge.laravel.com" className="nav-product-card">
              <span className="nav-product-name">Forge</span>
              <span className="nav-product-desc">Next-level server management with unparalleled control</span>
              <span className="nav-product-cta">Manage your servers</span>
            </a>
            <a href="https://nightwatch.laravel.com" className="nav-product-card">
              <span className="nav-product-name">Nightwatch</span>
              <span className="nav-product-desc">Full observability and monitoring for Laravel apps</span>
              <span className="nav-product-cta">Free plans available</span>
            </a>
          </div>
        </div>
      )}

      {/* Resources */}
      {isOpen('resources') && (
        <div id="content-resources" data-state={dataState('resources')} className="nav-dropdown-panel">
          <div className="nav-dropdown-inner nav-resources-grid">
            {/* Company */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Company</h3>
              <a href="/blog" className="nav-dd-link">Blog</a>
              <a href="/careers" className="nav-dd-link">Careers</a>
              <a href="https://trust.laravel.com" className="nav-dd-link">Trust</a>
              <a href="/legal" className="nav-dd-link">Legal</a>
              <a href="https://status.laravel.com" className="nav-dd-link">Status</a>
            </div>
            {/* Social */}
            <div className="nav-dd-col">
              <a href="https://github.com/laravel" className="nav-dd-link">GitHub</a>
              <a href="https://www.youtube.com/@LaravelPHP" className="nav-dd-link">YouTube</a>
              <a href="https://x.com/laaboratory" className="nav-dd-link">X</a>
              <a href="https://www.linkedin.com/company/laravel" className="nav-dd-link">LinkedIn</a>
              <a href="https://discord.gg/laravel" className="nav-dd-link">Discord</a>
            </div>
            {/* Partners */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Partners</h3>
              <a href="/partners/caci-limited" className="nav-dd-link">CACI Limited</a>
              <a href="/partners/kirschbaum" className="nav-dd-link">Kirschbaum</a>
              <a href="/partners/curotec" className="nav-dd-link">Curotec</a>
              <a href="/partners/64-robots" className="nav-dd-link">64 Robots</a>
              <a href="/partners/steadfast-collective" className="nav-dd-link">Steadfast Collective</a>
              <a href="/partners/byte5" className="nav-dd-link">byte5</a>
              <a href="/partners" className="nav-dd-link nav-dd-viewall">View all</a>
            </div>
            {/* Featured article */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Featured article</h3>
              <a href="/blog" className="nav-dd-link nav-dd-featured">
                <span className="nav-dd-featured-title">Latest from the Laravel Blog</span>
              </a>
              <a href="/blog" className="nav-dd-link nav-dd-viewall">Read more</a>
            </div>
          </div>
        </div>
      )}

      {/* Events */}
      {isOpen('events') && (
        <div id="content-events" data-state={dataState('events')} className="nav-dropdown-panel">
          <div className="nav-dropdown-inner nav-events-grid">
            {/* Upcoming events list */}
            <div className="nav-dd-col nav-events-upcoming">
              <h3 className="nav-dd-heading nav-dd-heading--red">Upcoming events</h3>
              <ul className="nav-events-list">
                <li>
                  <a href="https://www.meetup.com/laravel-copenhagen/" className="nav-event-list-item">
                    <span className="nav-event-date-badge">
                      <span className="nav-event-date-day">7</span>
                      <span className="nav-event-date-month">APR</span>
                    </span>
                    <div className="nav-event-list-info">
                      <span className="nav-event-list-name">Laravel Meetup: Copenhagen, April 2026</span>
                      <span className="nav-event-list-location">Hejrevej 28, Copenhagen,...</span>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="https://www.meetup.com/phpamersfoort/" className="nav-event-list-item">
                    <span className="nav-event-date-badge">
                      <span className="nav-event-date-day">14</span>
                      <span className="nav-event-date-month">APR</span>
                    </span>
                    <div className="nav-event-list-info">
                      <span className="nav-event-list-name">PHPAmersfoort Monthly Meetup: Laravel + Inertia.js</span>
                      <span className="nav-event-list-location">Euroweg 20, 3825 HD Amersfoort,...</span>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="https://www.meetup.com/laravel-serbia/" className="nav-event-list-item">
                    <span className="nav-event-date-badge">
                      <span className="nav-event-date-day">16</span>
                      <span className="nav-event-date-month">APR</span>
                    </span>
                    <div className="nav-event-list-info">
                      <span className="nav-event-list-name">Laravel Meetup Serbia</span>
                      <span className="nav-event-list-location">Online</span>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="https://www.meetup.com/laravel-wales/" className="nav-event-list-item">
                    <span className="nav-event-date-badge">
                      <span className="nav-event-date-day">22</span>
                      <span className="nav-event-date-month">APR</span>
                    </span>
                    <div className="nav-event-list-info">
                      <span className="nav-event-list-name">Laravel Wales</span>
                      <span className="nav-event-list-location">Havannah Street, Cardiff, X5,...</span>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="https://www.meetup.com/building-laravel-ai/" className="nav-event-list-item">
                    <span className="nav-event-date-badge">
                      <span className="nav-event-date-day">23</span>
                      <span className="nav-event-date-month">APR</span>
                    </span>
                    <div className="nav-event-list-info">
                      <span className="nav-event-list-name">Building with Laravel in the Age of AI</span>
                      <span className="nav-event-list-location">Speicherstraße 1, Frankfurt am...</span>
                    </div>
                  </a>
                </li>
              </ul>
              <a href="/community" className="nav-dd-link nav-dd-viewall" style={{display: 'flex', alignItems: 'center', gap: 4, marginTop: 8}}>
                View all
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="12" height="12"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
              </a>
            </div>
            {/* Featured Laracon cards */}
            <div className="nav-events-featured">
              <a href="https://laravellive.jp" className="nav-event-card nav-event-card--japan">
                <div className="nav-event-card-bg">
                  <img src="/img/nav/events/japan-bg.webp" alt="" className="nav-event-card-bg-img" />
                </div>
                <div className="nav-event-card-content">
                  <img src="/img/nav/events/japan-logo.png" alt="Laravel Live Japan" className="nav-event-card-logo-img" />
                  <div className="nav-event-card-bottom">
                    <div className="nav-event-card-footer">
                      <div className="nav-event-card-date">
                        <span className="nav-event-card-label">MAY</span>
                        <span className="nav-event-card-value">26-27</span>
                      </div>
                      <div className="nav-event-card-date nav-event-card-date--right">
                        <span className="nav-event-card-value">2026</span>
                      </div>
                    </div>
                    <div className="nav-event-card-footer">
                      <span className="nav-event-card-place">TOKYO</span>
                      <span className="nav-event-card-place nav-event-card-place--right">JP</span>
                    </div>
                  </div>
                </div>
              </a>
              <a href="https://laravellive.uk" className="nav-event-card nav-event-card--uk">
                <div className="nav-event-card-bg">
                  <img src="/img/nav/events/uk-bg.webp" alt="" className="nav-event-card-bg-img" />
                </div>
                <div className="nav-event-card-content">
                  <img src="/img/nav/events/uk-logo.svg" alt="Laravel Live UK" className="nav-event-card-logo-img" />
                  <div className="nav-event-card-bottom">
                    <div className="nav-event-card-footer">
                      <div className="nav-event-card-date">
                        <span className="nav-event-card-label">JUN</span>
                        <span className="nav-event-card-value">18-19</span>
                      </div>
                      <div className="nav-event-card-date nav-event-card-date--right">
                        <span className="nav-event-card-value">2026</span>
                      </div>
                    </div>
                    <div className="nav-event-card-footer">
                      <span className="nav-event-card-place">LONDON</span>
                      <span className="nav-event-card-place nav-event-card-place--right">UK</span>
                    </div>
                  </div>
                </div>
              </a>
              <a href="https://laracon.us" className="nav-event-card nav-event-card--us">
                <div className="nav-event-card-bg">
                  <img src="/img/nav/events/us-bg.webp" alt="" className="nav-event-card-bg-img" />
                </div>
                <div className="nav-event-card-content">
                  <img src="/img/nav/events/us-logo.svg" alt="Laracon US" className="nav-event-card-logo-img" />
                  <div className="nav-event-card-bottom">
                    <div className="nav-event-card-footer">
                      <div className="nav-event-card-date">
                        <span className="nav-event-card-label">JUL</span>
                        <span className="nav-event-card-value">28-29</span>
                      </div>
                      <div className="nav-event-card-date nav-event-card-date--right">
                        <span className="nav-event-card-value">2026</span>
                      </div>
                    </div>
                    <div className="nav-event-card-footer">
                      <span className="nav-event-card-place">BOSTON</span>
                      <span className="nav-event-card-place nav-event-card-place--right">US</span>
                    </div>
                  </div>
                </div>
              </a>
            </div>
          </div>
        </div>
      )}

      {/* ===================== Mobile Drawer ===================== */}
      {mobileOpen && (
        <div className="nav-mobile-overlay" onClick={() => { setMobileOpen(false); setMobileAccordion(null); }}>
          <div className="nav-mobile-drawer" onClick={e => e.stopPropagation()}>
            <div className="nav-mobile-header">
              <a href="/" aria-label="Laravel">
                <img src="/img/logotype.min.svg" alt="Laravel" className="nav-logo-img" />
              </a>
              <button
                className="nav-mobile-close"
                aria-label="Close navigation menu"
                onClick={() => { setMobileOpen(false); setMobileAccordion(null); }}
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <line x1="6" y1="6" x2="18" y2="18"/>
                  <line x1="6" y1="18" x2="18" y2="6"/>
                </svg>
              </button>
            </div>

            <div className="nav-mobile-body">
              {/* Framework accordion */}
              <div className="nav-mobile-section">
                <button
                  className="nav-mobile-accordion-trigger"
                  onClick={() => setMobileAccordion(prev => (prev === 'framework' ? null : 'framework'))}
                >
                  Framework
                  <ChevronDown open={mobileAccordion === 'framework'} />
                </button>
                {mobileAccordion === 'framework' && (
                  <div className="nav-mobile-accordion-content">
                    <a href="/" className="nav-mobile-link">Overview</a>
                    <a href="/starter-kits" className="nav-mobile-link">Starter Kits</a>
                    <a href="/docs/releases" className="nav-mobile-link">Release Notes</a>
                    <a href="/docs" className="nav-mobile-link">Documentation</a>
                    <a href="/learn" className="nav-mobile-link">Laravel Learn</a>
                  </div>
                )}
              </div>

              {/* Products accordion */}
              <div className="nav-mobile-section">
                <button
                  className="nav-mobile-accordion-trigger"
                  onClick={() => setMobileAccordion(prev => (prev === 'products' ? null : 'products'))}
                >
                  Products
                  <ChevronDown open={mobileAccordion === 'products'} />
                </button>
                {mobileAccordion === 'products' && (
                  <div className="nav-mobile-accordion-content">
                    <a href="https://cloud.laravel.com" className="nav-mobile-link">Laravel Cloud</a>
                    <a href="https://forge.laravel.com" className="nav-mobile-link">Forge</a>
                    <a href="https://nightwatch.laravel.com" className="nav-mobile-link">Nightwatch</a>
                    <a href="https://nova.laravel.com" className="nav-mobile-link">Nova</a>
                  </div>
                )}
              </div>

              {/* Resources accordion */}
              <div className="nav-mobile-section">
                <button
                  className="nav-mobile-accordion-trigger"
                  onClick={() => setMobileAccordion(prev => (prev === 'resources' ? null : 'resources'))}
                >
                  Resources
                  <ChevronDown open={mobileAccordion === 'resources'} />
                </button>
                {mobileAccordion === 'resources' && (
                  <div className="nav-mobile-accordion-content">
                    <a href="/blog" className="nav-mobile-link">Blog</a>
                    <a href="/partners" className="nav-mobile-link">Partners</a>
                    <a href="/careers" className="nav-mobile-link">Careers</a>
                    <a href="https://trust.laravel.com" className="nav-mobile-link">Trust</a>
                    <a href="/legal" className="nav-mobile-link">Legal</a>
                    <a href="https://status.laravel.com" className="nav-mobile-link">Status</a>
                  </div>
                )}
              </div>

              {/* Events - direct link */}
              <div className="nav-mobile-section">
                <a href="/community" className="nav-mobile-accordion-trigger nav-mobile-direct-link">Events</a>
              </div>

              {/* Docs - direct link */}
              <div className="nav-mobile-section">
                <a href="/docs" className="nav-mobile-accordion-trigger nav-mobile-direct-link">Docs</a>
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
