import React, {type ReactNode} from 'react';

import {useThemeConfig} from '@docusaurus/theme-common';
import {useLocation} from '@docusaurus/router';
import FooterSection from '@site/src/components/Homepage/FooterSection';

// 모든 페이지(문서 포함)에서 메인페이지와 동일한 커스텀 푸터를 사용한다.
// 단, 문서 페이지(/docs/, /<locale>/docs/)에서는 'docs' 변형을 렌더해
// 제품군 컬럼 대신 Community 섹션을 노출한다.
function Footer(): ReactNode {
  const {footer} = useThemeConfig();
  const {pathname} = useLocation();
  if (!footer) {
    return null;
  }

  const isDocs = pathname.split('/').includes('docs');

  return <FooterSection variant={isDocs ? 'docs' : 'home'} />;
}

export default React.memo(Footer);
