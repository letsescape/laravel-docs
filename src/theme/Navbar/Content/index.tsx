import React, {useCallback, useEffect, useRef, useState} from 'react';
import clsx from 'clsx';
import {useThemeConfig, ErrorCauseBoundary, ThemeClassNames} from '@docusaurus/theme-common';
import {splitNavbarItems, useNavbarMobileSidebar} from '@docusaurus/theme-common/internal';
import NavbarItem from '@theme/NavbarItem';
import NavbarColorModeToggle from '@theme/Navbar/ColorModeToggle';
import SearchBar from '@theme/SearchBar';
import NavbarMobileSidebarToggle from '@theme/Navbar/MobileSidebar/Toggle';
import NavbarLogo from '@theme/Navbar/Logo';
import NavbarSearch from '@theme/Navbar/Search';
import IconMenu from '@theme/Icon/Menu';
import {useLocation} from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import NavbarDropdowns from '@site/src/components/Homepage/NavbarDropdowns';
import './styles.module.css';

function useNavbarItems() {
  return useThemeConfig().navbar.items as any[];
}

function NavbarItems({items}: {items: any[]}) {
  const {i18n: {currentLocale, localeConfigs}} = useDocusaurusContext();
  return (
    <>
      {items.map((item, i) => (
        <ErrorCauseBoundary
          key={i}
          onError={(error) =>
            new Error(
              `A theme navbar item failed to render.\n${JSON.stringify(item, null, 2)}`,
              {cause: error},
            )
          }>
          <NavbarItem
            {...item}
            {...(item.type === 'localeDropdown' && {
              'aria-label': localeConfigs[currentLocale].label,
              'data-locale-code': currentLocale.toUpperCase(),
            })}
          />
        </ErrorCauseBoundary>
      ))}
    </>
  );
}

function NavbarContentLayout({left, right}: {left: React.ReactNode; right: React.ReactNode}) {
  const innerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const navbar = innerRef.current?.closest('.navbar');
    if (!navbar) return;
    const root = document.documentElement;
    const updateHeight = () => root.style.setProperty('--site-navbar-height', `${navbar.getBoundingClientRect().height}px`);
    updateHeight();
    const observer = new ResizeObserver(updateHeight);
    observer.observe(navbar);
    return () => {
      observer.disconnect();
      root.style.removeProperty('--site-navbar-height');
    };
  }, []);

  return (
    <div ref={innerRef} className="navbar__inner">
      <div className={clsx(ThemeClassNames.layout.navbar.containerLeft, 'navbar__items')}>
        {left}
      </div>
      <div className={clsx(ThemeClassNames.layout.navbar.containerRight, 'navbar__items navbar__items--right')}>
        {right}
      </div>
    </div>
  );
}

export default function NavbarContent(): React.ReactNode {
  const mobileSidebar = useNavbarMobileSidebar();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const mobileMenuButtonRef = useRef<HTMLButtonElement>(null);
  const closeMobileMenu = useCallback(() => {
    setMobileMenuOpen(false);
    mobileMenuButtonRef.current?.focus({preventScroll: true});
  }, []);
  const items = useNavbarItems();
  const [leftItems, rightItems] = splitNavbarItems(items);
  const searchBarItem = items.find((item: any) => item.type === 'search');
  const location = useLocation();
  const homeUrl = useBaseUrl('/');
  const isHomepage = location.pathname === homeUrl || location.pathname === homeUrl.replace(/\/$/, '') || location.pathname === '/index.html';
  const showDefaultMobileSidebarToggle = mobileSidebar.shouldRender && !isHomepage;

  return (
    <>
      <NavbarContentLayout
        left={
          <>
            <NavbarLogo />
            {isHomepage && (
              <NavbarDropdowns mobileMenuOpen={mobileMenuOpen} onMobileMenuClose={closeMobileMenu} />
            )}
            {!isHomepage && <NavbarItems items={leftItems} />}
          </>
        }
        right={
          <>
            <NavbarColorModeToggle className="navbar-color-mode-toggle" />
            <NavbarItems items={rightItems} />
            {!searchBarItem && (
              <NavbarSearch>
                <SearchBar />
              </NavbarSearch>
            )}
            {isHomepage && (
              <button
                ref={mobileMenuButtonRef}
                className="nav-mobile-hamburger"
                aria-label="Open menu"
                aria-expanded={mobileMenuOpen}
                aria-controls="homepage-mobile-menu"
                onClick={() => setMobileMenuOpen(true)}
              >
                <IconMenu />
              </button>
            )}
            {showDefaultMobileSidebarToggle && <NavbarMobileSidebarToggle />}
          </>
        }
      />
    </>
  );
}
