import React, {type ReactNode, useEffect} from 'react';
import {useActiveDocContext, useDocsPreferredVersion} from '@docusaurus/plugin-content-docs/client';
import SearchBar from '@theme-original/SearchBar';

export default function SearchBarWrapper(): ReactNode {
  const {activeVersion} = useActiveDocContext('default');
  const {savePreferredVersionName} = useDocsPreferredVersion();

  useEffect(() => {
    if (activeVersion) savePreferredVersionName(activeVersion.name);
  }, [activeVersion, savePreferredVersionName]);

  return <SearchBar />;
}
