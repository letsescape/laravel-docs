import React, {useState, useEffect, useRef, useCallback, useMemo, type ReactNode} from 'react';
import {useColorMode} from '@docusaurus/theme-common';
import './homepage.css';

type DropdownName = 'framework' | 'products' | 'resources' | 'events';

const ALL_PARTNERS = [
  { name: 'Steadfast Collective', slug: 'steadfast-collective' },
  { name: 'Tighten', slug: 'tighten' },
  { name: 'Jump24', slug: 'jump24' },
  { name: 'Pixel', slug: 'pixel' },
  { name: 'UCodeSoft', slug: 'ucodesoft' },
  { name: 'Curotec', slug: 'curotec' },
  { name: '64 Robots', slug: '64-robots' },
  { name: 'Vehikl', slug: 'vehikl' },
  { name: 'byte5', slug: 'byte5' },
  { name: 'Kirschbaum', slug: 'kirschbaum' },
  { name: 'CACI Limited', slug: 'caci-limited' },
  { name: 'Redberry', slug: 'redberry' },
];

function getRandomPartners(count: number) {
  const shuffled = [...ALL_PARTNERS].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

function ChevronDown({open}: {open: boolean}) {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 20 20"
      fill="currentColor"
      style={{transform: open ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 200ms'}}
      className="nav-chevron"
    >
      <path fillRule="evenodd" d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z" clipRule="evenodd" />
    </svg>
  );
}

export default function NavbarDropdowns(): ReactNode {
  const [openDropdown, setOpenDropdown] = useState<DropdownName | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [mobileSubMenu, setMobileSubMenu] = useState<string | null>(null);
  const [mobileThemeMode, setMobileThemeMode] = useState<'light' | 'dark' | 'system'>('system');
  const {colorMode, setColorMode} = useColorMode();
  const wrapperRef = useRef<HTMLDivElement>(null);

  // Sync mobileThemeMode with stored preference on mount
  useEffect(() => {
    const stored = localStorage.getItem('theme');
    if (stored === 'light' || stored === 'dark') {
      setMobileThemeMode(stored);
    } else {
      setMobileThemeMode('system');
    }
  }, []);
  const closeTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const randomPartners = useMemo(() => getRandomPartners(6), []);

  const cancelClose = useCallback(() => {
    if (closeTimerRef.current) {
      clearTimeout(closeTimerRef.current);
      closeTimerRef.current = null;
    }
  }, []);

  const scheduleClose = useCallback(() => {
    cancelClose();
    closeTimerRef.current = setTimeout(() => setOpenDropdown(null), 150);
  }, [cancelClose]);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        // Also check if click is inside a dropdown panel
        const panel = (e.target as Element)?.closest?.('.nav-dropdown-panel');
        if (!panel) setOpenDropdown(null);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const canHover = typeof window !== 'undefined' && window.matchMedia('(hover: hover)').matches;

  const toggleDropdown = useCallback((name: DropdownName) => {
    setOpenDropdown(prev => (prev === name ? null : name));
  }, []);

  const isOpen = (name: DropdownName) => openDropdown === name;
  const dataState = (name: DropdownName) => (isOpen(name) ? 'open' : 'closed');

  return (
    <div ref={wrapperRef} className="nav-dropdowns-wrapper">
      {/* Dropdown triggers */}
      <div className="nav-dropdown-triggers">
        {(['framework', 'products', 'resources', 'events'] as DropdownName[]).map(name => (
          <button
            key={name}
            id={`trigger-${name}`}
            aria-controls={`content-${name}`}
            aria-expanded={isOpen(name)}
            data-state={dataState(name)}
            className="nav-dropdown-trigger"
            onClick={() => toggleDropdown(name)}
            onMouseEnter={canHover ? () => { cancelClose(); setOpenDropdown(name); } : undefined}
            onMouseLeave={canHover ? scheduleClose : undefined}
          >
            {name.charAt(0).toUpperCase() + name.slice(1)}
            <ChevronDown open={isOpen(name)} />
          </button>
        ))}
        <a href="/docs" className="nav-docs-link">Docs</a>
      </div>

      {/* Framework */}
      {isOpen('framework') && (
        <div id="content-framework" data-state={dataState('framework')} className="nav-dropdown-panel" onMouseEnter={canHover ? cancelClose : undefined} onMouseLeave={canHover ? scheduleClose : undefined}>
          <div className="nav-dropdown-inner nav-framework-grid">
            {/* Explore Laravel */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Explore Laravel</h3>
              <ul className="nav-dd-list">
                <li><a href="/" className="nav-dd-item-link">
                  <img src="/img/nav/fw-overview.png" alt="" className="nav-dd-icon" />
                  <div>
                    <span className="nav-dd-item-name">Overview</span>
                    <span className="nav-dd-item-desc">Discover the magic of Laravel</span>
                  </div>
                </a></li>
                <li><a href="/docs/changelog" className="nav-dd-item-link">
                  <img src="/img/nav/fw-changelog.png" alt="" className="nav-dd-icon" />
                  <div>
                    <span className="nav-dd-item-name">Changelog</span>
                    <span className="nav-dd-item-desc">Read the latest changes</span>
                  </div>
                </a></li>
                <li><a href="/learn" className="nav-dd-item-link">
                  <img src="/img/nav/fw-learn.png" alt="" className="nav-dd-icon" />
                  <div>
                    <span className="nav-dd-item-name">Laravel Learn</span>
                    <span className="nav-dd-item-desc">The fastest way to start building</span>
                  </div>
                </a></li>
              </ul>
            </div>
            {/* Latest packages */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Latest packages</h3>
              <ul className="nav-dd-list">
                <li><a href="/ai" className="nav-dd-item-link">
                  <img src="/img/nav/fw-ai-sdk.png" alt="" className="nav-dd-icon" />
                  <div>
                    <span className="nav-dd-item-name">AI SDK</span>
                    <span className="nav-dd-item-desc">Build AI-powered applications</span>
                  </div>
                </a></li>
                <li><a href="/ai/boost" className="nav-dd-item-link">
                  <img src="/img/nav/fw-boost.png" alt="" className="nav-dd-icon" />
                  <div>
                    <span className="nav-dd-item-name">Boost</span>
                    <span className="nav-dd-item-desc">AI-assisted development</span>
                  </div>
                </a></li>
                <li><a href="https://github.com/laravel/wayfinder" className="nav-dd-item-link">
                  <img src="/img/nav/fw-wayfinder.png" alt="" className="nav-dd-icon" />
                  <div>
                    <span className="nav-dd-item-name">Wayfinder</span>
                    <span className="nav-dd-item-desc">TypeScript front-ends</span>
                  </div>
                </a></li>
              </ul>
            </div>
            {/* Documentation */}
            <div className="nav-dd-col nav-dd-col-docs">
              <h3 className="nav-dd-heading">Documentation</h3>
              <ul className="nav-dd-list nav-dd-list-simple">
                <li><a href="/docs/installation" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M4.3335 5.00016L5.66683 6.3335L4.3335 7.66683M6.3335 7.66683H7.66683M2.3335 2.3335H13.6668V13.6668H2.3335V2.3335Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Installation
                </a></li>
                <li><a href="/docs/ai" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" fillRule="evenodd" clipRule="evenodd" d="M14.3332 7.99984C9.93502 7.99984 7.99984 9.93502 7.99984 14.3332C7.99984 9.93502 6.06465 7.99984 1.6665 7.99984C6.06465 7.99984 7.99984 6.06465 7.99984 1.6665C7.99984 6.06465 9.93502 7.99984 14.3332 7.99984Z" stroke="currentColor" strokeLinejoin="round"/>
                  </svg>
                  Agent Setup
                </a></li>
                <li><a href="/docs/eloquent" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M13 3.42576C13 4.39738 10.7614 5.18502 8 5.18502C5.23858 5.18502 3 4.39738 3 3.42576M13 3.42576C13 2.45415 10.7614 1.6665 8 1.6665C5.23858 1.6665 3 2.45415 3 3.42576M13 3.42576V12.5739C13 13.5455 10.7614 14.3332 8 14.3332C5.23858 14.3332 3 13.5455 3 12.5739V3.42576M13 7.92562C13 8.89723 10.7614 9.68488 8 9.68488C5.23858 9.68488 3 8.89723 3 7.92562" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Eloquent ORM
                </a></li>
                <li><a href="/docs/artisan" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M3 4.3335L6.66667 8.00016L3 11.6668M8.33333 11.6668H13" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Artisan Console
                </a></li>
                <li><a href="/docs/routing" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M7.99984 5.66683V2.3335H12.9998L14.3332 4.00016L12.9998 5.66683H7.99984ZM7.99984 5.66683V9.00016M7.99984 5.66683H2.99984L1.6665 7.3335L2.99984 9.00016H7.99984M7.99984 9.00016V13.6668M7.99984 13.6668H5.6665M7.99984 13.6668H10.3332" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Routing
                </a></li>
              </ul>
              <a href="/docs" className="nav-dd-link nav-dd-viewall" style={{display: 'flex', alignItems: 'center', gap: 4}}>
                View all
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="14" height="14">
                  <path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
            {/* Starter kits */}
            <a href="/starter-kits" className="nav-dd-col nav-dd-col-starter">
              <span className="nav-dd-starter-label">
                <span>Starter kits</span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="12" height="12" className="nav-dd-starter-arrow">
                  <path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" />
                </svg>
              </span>
              <div className="nav-dd-starter-stack">
                <img src="/img/nav/fw-starter-cards.svg" alt="Starter kits preview" className="nav-dd-starter-img nav-dd-starter-img--light" />
                <img src="/img/nav/fw-starter-cards-dark.svg" alt="Starter kits preview" className="nav-dd-starter-img nav-dd-starter-img--dark" />
              </div>
            </a>
          </div>
        </div>
      )}

      {/* Products */}
      {isOpen('products') && (
        <div id="content-products" data-state={dataState('products')} className="nav-dropdown-panel" onMouseEnter={canHover ? cancelClose : undefined} onMouseLeave={canHover ? scheduleClose : undefined}>
          <div className="nav-dropdown-inner nav-products-grid">
            <a href="https://cloud.laravel.com" className="nav-product-card nav-product-card--dark">
              <div className="nav-product-header">
                <svg viewBox="0 0 180 40" fill="none" className="nav-product-logo">
                  <text x="0" y="28" fill="white" fontSize="16" fontWeight="300" letterSpacing="-0.02em" fontFamily="system-ui, sans-serif">
                    <tspan fontWeight="600">Laravel</tspan> Cloud
                  </text>
                </svg>
              </div>
              <p className="nav-product-desc">The fastest way to deploy and scale Laravel applications</p>
              <span className="nav-product-cta nav-product-cta--blue">
                Deploy now
                <svg width="12" height="12" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
              </span>
              <img src="/img/nav/product-cloud.png" alt="" className="nav-product-img" />
            </a>
            <a href="https://forge.laravel.com" className="nav-product-card nav-product-card--light">
              <div className="nav-product-header">
                <svg viewBox="0 0 180 40" fill="none" className="nav-product-logo">
                  <text x="0" y="28" fill="currentColor" fontSize="18" fontWeight="800" letterSpacing="-0.03em" fontFamily="system-ui, sans-serif">FORGE</text>
                </svg>
              </div>
              <p className="nav-product-desc nav-product-desc--dark">Next-level server management with unparalleled control</p>
              <span className="nav-product-cta nav-product-cta--blue">
                Manage your servers
                <svg width="12" height="12" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
              </span>
              <img src="/img/nav/product-forge.png" alt="" className="nav-product-img" />
            </a>
            <a href="https://nightwatch.laravel.com" className="nav-product-card nav-product-card--dark nav-product-card--nightwatch">
              <div className="nav-product-header">
                <svg viewBox="0 0 180 40" fill="none" className="nav-product-logo">
                  <text x="0" y="28" fill="white" fontSize="14" fontWeight="600" letterSpacing="0.08em" fontFamily="system-ui, sans-serif">NIGHTWATCH</text>
                </svg>
              </div>
              <p className="nav-product-desc">Full observability and monitoring for Laravel apps</p>
              <span className="nav-product-cta nav-product-cta--green">
                Free plans available
                <svg width="12" height="12" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
              </span>
              <img src="/img/nav/product-nightwatch.png" alt="" className="nav-product-img" />
            </a>
          </div>
        </div>
      )}

      {/* Resources */}
      {isOpen('resources') && (
        <div id="content-resources" data-state={dataState('resources')} className="nav-dropdown-panel" onMouseEnter={canHover ? cancelClose : undefined} onMouseLeave={canHover ? scheduleClose : undefined}>
          <div className="nav-dropdown-inner nav-resources-grid">
            {/* Company */}
            <div className="nav-dd-col nav-resources-company">
              <h3 className="nav-dd-heading">Company</h3>
              <ul className="nav-dd-list nav-dd-list-simple">
                <li><a href="/blog" className="nav-dd-link nav-dd-doc-link">
                  <svg width="17" height="16" viewBox="0 0 17 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M13.1667 7.58333V1.5H1.5V12.5833C1.5 13.7339 2.43274 14.6667 3.58333 14.6667H15.25M13.1667 7.58333V12.5833C13.1667 13.7339 14.0994 14.6667 15.25 14.6667M13.1667 7.58333H16.3333V12.5833C16.3333 13.7339 15.4006 14.6667 14.25 14.6667M4.41667 10.5H10.25M4.83333 3.83333H9.83333V8H4.83333V3.83333Z" stroke="currentColor" strokeLinecap="square"/>
                  </svg>
                  Blog
                </a></li>
                <li><a href="/careers" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M7.99984 8.3335V10.0002M7.99984 8.3335H13.9998M7.99984 8.3335H1.99984M5.33317 5.00016V2.3335H10.6665V5.00016M14.3332 13.6668H1.66797V5.00016H14.3332V13.6668Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Careers
                </a></li>
                <li><a href="https://trust.laravel.com" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M6.00016 7.49984L7.3335 8.83317L10.0002 6.1665M8.00016 1.6665L13.6668 3.49984V7.9414C13.6668 11.2564 10.6668 12.9998 8.00016 14.4384C5.3335 12.9998 2.3335 11.2564 2.3335 7.9414V3.49984L8.00016 1.6665Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Trust
                </a></li>
                <li><a href="/legal" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M7.99984 1.6665V13.6665M7.99984 13.6665H4.33317M7.99984 13.6665H11.6665M1.6665 3.6665H5.6665L6.6665 2.99984H9.33317L10.6665 3.6665H14.3332M3.6665 3.6665L1.6665 9.99984C3.05112 10.7843 4.28189 10.7843 5.6665 9.99984L3.6665 3.6665ZM12.3332 3.6665L10.3332 9.99984C11.7178 10.7843 12.9486 10.7843 14.3332 9.99984L12.3332 3.6665Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Legal
                </a></li>
                <li><a href="https://status.laravel.com" className="nav-dd-link nav-dd-doc-link">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="nav-dd-doc-icon">
                    <path fill="none" d="M12.4782 3.52148C14.9515 5.9948 14.9515 10.0049 12.4782 12.4782M3.52149 12.4782C1.04817 10.0049 1.04817 5.9948 3.52149 3.52148M10.5926 5.4071C12.0245 6.839 12.0245 9.16063 10.5926 10.5926M5.40711 10.5926C3.97519 9.16063 3.97519 6.83902 5.40711 5.4071M8.99984 7.99983C8.99984 8.55211 8.55212 8.99983 7.99984 8.99983C7.44755 8.99983 6.99984 8.55211 6.99984 7.99983C6.99984 7.44754 7.44755 6.99983 7.99984 6.99983C8.55212 6.99983 8.99984 7.44754 8.99984 7.99983Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Status
                </a></li>
              </ul>
              <div className="nav-resources-social">
                <a href="https://github.com/laravel" aria-label="GitHub" className="nav-social-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
                </a>
                <a href="https://www.youtube.com/@LaravelPHP" aria-label="YouTube" className="nav-social-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                </a>
                <a href="https://x.com/laravelphp" aria-label="X" className="nav-social-icon">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M13.969 10.157L22.707 0h-2.07l-7.59 8.82L6.989 0H0l9.164 13.336L0 23.988h2.07l8.012-9.313 6.4 9.313h6.989L13.969 10.157zm-2.836 3.297l-.929-1.328L2.72 1.56h3.18l5.963 8.532.929 1.328 7.749 11.084h-3.18l-6.328-9.05z"/></svg>
                </a>
                <a href="https://www.linkedin.com/company/laravelphp" aria-label="LinkedIn" className="nav-social-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                </a>
                <a href="https://discord.com/invite/laravel" aria-label="Discord" className="nav-social-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>
                </a>
              </div>
            </div>
            {/* Partners */}
            <div className="nav-dd-col">
              <h3 className="nav-dd-heading">Partners</h3>
              <ul className="nav-dd-list nav-dd-list-simple">
                {randomPartners.map(p => (
                  <li key={p.slug}><a href={`/partners/${p.slug}`} className="nav-dd-link">{p.name}</a></li>
                ))}
              </ul>
              <a href="/partners" className="nav-dd-link nav-dd-viewall" style={{display: 'flex', alignItems: 'center', gap: 4, marginTop: 'auto'}}>
                View all
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="12" height="12"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
              </a>
            </div>
            {/* Featured article */}
            <div className="nav-dd-col nav-resources-featured">
              <h3 className="nav-dd-heading">Featured article</h3>
              <div className="nav-featured-wrap">
                <a href="/blog/scheduled-autoscaling-for-laravel-cloud" className="nav-featured-article">
                  <div className="nav-featured-thumb">
                    <img
                      alt=""
                      src="https://fls-9f826fcc-b2ad-40d8-813f-9cf7dac049fa.laravel.cloud/posts/images/01KMN7167KYNMSXT52AGJ1G7CW.avif"
                      className="nav-featured-thumb-img"
                    />
                  </div>
                  <div className="nav-featured-content">
                    <span className="nav-featured-date">March 26, 2026</span>
                    <p className="nav-featured-title">Scheduled Autoscaling for Laravel Cloud</p>
                    <div className="nav-featured-readmore">
                      <span className="nav-dd-viewall">
                        Read more
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="12" height="12" style={{verticalAlign: 'middle', marginLeft: 4}}><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
                      </span>
                    </div>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Events */}
      {isOpen('events') && (
        <div id="content-events" data-state={dataState('events')} className="nav-dropdown-panel" onMouseEnter={canHover ? cancelClose : undefined} onMouseLeave={canHover ? scheduleClose : undefined}>
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
      {/* Mobile color mode toggle: cycles light → dark → system */}
      <button
        className="nav-mobile-mode-toggle"
        aria-label="Toggle color mode"
        onClick={() => {
          const modes: Array<'light' | 'dark' | 'system'> = ['light', 'dark', 'system'];
          const idx = modes.indexOf(mobileThemeMode);
          const next = modes[(idx + 1) % modes.length];
          setMobileThemeMode(next);
          if (next === 'system') {
            localStorage.removeItem('theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            setColorMode(prefersDark ? 'dark' : 'light');
          } else {
            localStorage.setItem('theme', next);
            setColorMode(next);
          }
        }}
      >
        {mobileThemeMode === 'light' && (
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M12,9c1.65,0,3,1.35,3,3s-1.35,3-3,3s-3-1.35-3-3S10.35,9,12,9 M12,7c-2.76,0-5,2.24-5,5s2.24,5,5,5s5-2.24,5-5 S14.76,7,12,7L12,7z M2,13l2,0c0.55,0,1-0.45,1-1s-0.45-1-1-1l-2,0c-0.55,0-1,0.45-1,1S1.45,13,2,13z M20,13l2,0c0.55,0,1-0.45,1-1 s-0.45-1-1-1l-2,0c-0.55,0-1,0.45-1,1S19.45,13,20,13z M11,2v2c0,0.55,0.45,1,1,1s1-0.45,1-1V2c0-0.55-0.45-1-1-1S11,1.45,11,2z M11,20v2c0,0.55,0.45,1,1,1s1-0.45,1-1v-2c0-0.55-0.45-1-1-1C11.45,19,11,19.45,11,20z M5.99,4.58c-0.39-0.39-1.03-0.39-1.41,0 c-0.39,0.39-0.39,1.03,0,1.41l1.06,1.06c0.39,0.39,1.03,0.39,1.41,0s0.39-1.03,0-1.41L5.99,4.58z M18.36,16.95 c-0.39-0.39-1.03-0.39-1.41,0c-0.39,0.39-0.39,1.03,0,1.41l1.06,1.06c0.39,0.39,1.03,0.39,1.41,0c0.39-0.39,0.39-1.03,0-1.41 L18.36,16.95z M19.42,5.99c0.39-0.39,0.39-1.03,0-1.41c-0.39-0.39-1.03-0.39-1.41,0l-1.06,1.06c-0.39,0.39-0.39,1.03,0,1.41 s1.03,0.39,1.41,0L19.42,5.99z M7.05,18.36c0.39-0.39,0.39-1.03,0-1.41c-0.39-0.39-1.03-0.39-1.41,0l-1.06,1.06 c-0.39,0.39-0.39,1.03,0,1.41s1.03,0.39,1.41,0L7.05,18.36z"/>
          </svg>
        )}
        {mobileThemeMode === 'dark' && (
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M9.37,5.51C9.19,6.15,9.1,6.82,9.1,7.5c0,4.08,3.32,7.4,7.4,7.4c0.68,0,1.35-0.09,1.99-0.27C17.45,17.19,14.93,19,12,19 c-3.86,0-7-3.14-7-7C5,9.07,6.81,6.55,9.37,5.51z M12,3c-4.97,0-9,4.03-9,9s4.03,9,9,9s9-4.03,9-9c0-0.46-0.04-0.92-0.1-1.36 c-0.98,1.37-2.58,2.26-4.4,2.26c-2.98,0-5.4-2.42-5.4-5.4c0-1.81,0.89-3.42,2.26-4.4C12.92,3.04,12.46,3,12,3L12,3z"/>
          </svg>
        )}
        {mobileThemeMode === 'system' && (
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="m12 21c4.971 0 9-4.029 9-9s-4.029-9-9-9-9 4.029-9 9 4.029 9 9 9zm4.95-13.95c1.313 1.313 2.05 3.093 2.05 4.95s-0.738 3.637-2.05 4.95c-1.313 1.313-3.093 2.05-4.95 2.05v-14c1.857 0 3.637 0.737 4.95 2.05z"/>
          </svg>
        )}
      </button>

      {/* Mobile hamburger button */}
      <button
        className="nav-mobile-hamburger"
        aria-label="Open menu"
        onClick={() => setMobileMenuOpen(true)}
      >
        <svg width="22" height="22" viewBox="0 0 30 30" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
          <line x1="4" y1="11" x2="26" y2="11"/>
          <line x1="4" y1="21" x2="26" y2="21"/>
        </svg>
      </button>

      {/* Mobile fullscreen overlay */}
      {mobileMenuOpen && (
        <div className="nav-mobile-overlay" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>
          <div className="nav-mobile-fullscreen" onClick={e => e.stopPropagation()}>
            {/* Main menu */}
            <div className="nav-mobile-panel" style={{transform: mobileSubMenu ? 'translateX(-100%)' : 'translateX(0)'}}>
              <div className="nav-mobile-top">
                <a href="/" className="nav-mobile-logo">
                  <img src="/img/logotype.min.svg" alt="Laravel" className="nav-logo-img" />
                </a>
                <button className="nav-mobile-close" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }} aria-label="Close menu">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
              <nav className="nav-mobile-menu">
                {(['framework', 'products', 'resources'] as const).map(name => (
                  <button key={name} className="nav-mobile-menu-item" onClick={() => setMobileSubMenu(name)}>
                    <span>{name.charAt(0).toUpperCase() + name.slice(1)}</span>
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#c0c0c0" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="nav-mobile-chevron">
                      <path d="M8.25 4.5l7.5 7.5-7.5 7.5" fill="none"/>
                    </svg>
                  </button>
                ))}
                <a href="/community" className="nav-mobile-menu-item" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>
                  <span>Events</span>
                </a>
                <a href="/docs" className="nav-mobile-menu-item" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>
                  <span>Docs</span>
                </a>
              </nav>
            </div>

            {/* Sub menu */}
            <div className="nav-mobile-panel nav-mobile-subpanel" style={{transform: mobileSubMenu ? 'translateX(0)' : 'translateX(100%)'}}>
              <div className="nav-mobile-top">
                <button className="nav-mobile-back" onClick={() => setMobileSubMenu(null)}>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" className="nav-mobile-back-icon">
                    <path fillRule="evenodd" d="M17 10a.75.75 0 0 1-.75.75H5.612l3.158 3.03a.75.75 0 0 1-1.04 1.08l-4.5-4.25a.75.75 0 0 1 0-1.08l4.5-4.25a.75.75 0 0 1 1.04 1.08L5.612 9.25H16.25A.75.75 0 0 1 17 10Z" clipRule="evenodd"/>
                  </svg>
                  <span>{mobileSubMenu ? mobileSubMenu.charAt(0).toUpperCase() + mobileSubMenu.slice(1) : ''}</span>
                </button>
                <button className="nav-mobile-close" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }} aria-label="Close menu">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
              <nav className="nav-mobile-submenu">
                {mobileSubMenu === 'framework' && <>
                  <a href="/" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Overview</a>
                  <a href="https://laravel.com/starter-kits" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Starter Kits</a>
                  <a href="/docs/releases" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Release Notes</a>
                  <a href="/docs" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Documentation</a>
                  <a href="/learn" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Laravel Learn</a>
                </>}
                {mobileSubMenu === 'products' && <>
                  <a href="https://cloud.laravel.com" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Laravel Cloud</a>
                  <a href="https://forge.laravel.com" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Forge</a>
                  <a href="https://nightwatch.laravel.com" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Nightwatch</a>
                  <a href="https://nova.laravel.com" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Nova</a>
                </>}
                {mobileSubMenu === 'resources' && <>
                  <a href="/blog" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Blog</a>
                  <a href="/partners" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Partners</a>
                  <a href="/careers" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Careers</a>
                  <a href="https://trust.laravel.com" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Trust</a>
                  <a href="/legal" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Legal</a>
                  <a href="https://status.laravel.com" className="nav-mobile-subitem" onClick={() => { setMobileMenuOpen(false); setMobileSubMenu(null); }}>Status</a>
                </>}
              </nav>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
