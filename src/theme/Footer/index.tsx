import React, {type ReactNode} from 'react';

import {useThemeConfig} from '@docusaurus/theme-common';
import {useLocation} from '@docusaurus/router';
import FooterSection from '@site/src/components/Homepage/FooterSection';

function Footer(): ReactNode {
  const {footer} = useThemeConfig();
  const {pathname} = useLocation();
  if (!footer) {
    return null;
  }

  const isDocs = /^\/(?:[a-z]{2}\/)?docs(?:\/|$)/.test(pathname);

  return <FooterSection variant={isDocs ? 'docs' : 'home'} />;
}

export default React.memo(Footer);
