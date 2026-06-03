import React, {type ReactNode} from 'react';

import {useThemeConfig} from '@docusaurus/theme-common';
import FooterSection from '@site/src/components/Homepage/FooterSection';

// 모든 페이지(문서 포함)에서 메인페이지와 동일한 커스텀 푸터를 사용한다.
// themeConfig.footer가 비활성화된 경우에만 푸터를 렌더하지 않는다.
function Footer(): ReactNode {
  const {footer} = useThemeConfig();
  if (!footer) {
    return null;
  }

  return <FooterSection />;
}

export default React.memo(Footer);
