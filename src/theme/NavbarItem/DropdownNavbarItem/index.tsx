import React from 'react';
import {translate} from '@docusaurus/Translate';
import DropdownNavbarItem from '@theme-original/NavbarItem/DropdownNavbarItem';
import type {Props} from '@theme/NavbarItem/DropdownNavbarItem';

export default function ResponsiveDropdownNavbarItem(props: Props) {
  if (!props.className?.split(' ').includes('navbar-version-dropdown')) {
    return <DropdownNavbarItem {...props} />;
  }

  const developmentLabel = translate({
    id: 'navbar.version.development',
    message: 'master (development)',
  });
  const items = props.items.map((item) => item.label === 'master'
    ? {...item, label: developmentLabel}
    : item);

  if (props.mobile || typeof props.label !== 'string') {
    return <DropdownNavbarItem {...props} items={items} />;
  }

  const label = props.label;
  const compactLabel = label === 'master' ? 'dev' : label.replace(/\.x$/, '');
  const accessibleLabel = translate({
    id: 'navbar.version.label',
    message: 'Documentation version: {version}',
  }, {version: label === 'master' ? `dev / ${developmentLabel}` : label});

  return (
    <DropdownNavbarItem
      {...props}
      items={items}
      aria-label={accessibleLabel}
      title={accessibleLabel}
      label={(
        <>
          <span className="navbar-version-label">{label}</span>
          <span className="navbar-version-code">{compactLabel}</span>
        </>
      )}
    />
  );
}
