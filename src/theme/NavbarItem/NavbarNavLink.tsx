import React from 'react';
import NavbarNavLink from '@theme-original/NavbarItem/NavbarNavLink';
import type {Props} from '@theme/NavbarItem/NavbarNavLink';

export default function ResponsiveNavbarNavLink({label, 'data-locale-code': localeCode, ...props}: Props & {'data-locale-code'?: string}) {
  return (
    <NavbarNavLink
      {...props}
      label={localeCode ? (
        <>
          <span className="navbar-locale-label">{label}</span>
          <span className="navbar-locale-code">{localeCode}</span>
        </>
      ) : label}
    />
  );
}
