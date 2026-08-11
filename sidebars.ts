import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Creating a sidebar enables you to:
 *
 * - Create an ordered group of docs.
 * - Render a sidebar for each doc in that group.
 * - Provide next/previous navigation.
 *
 * Sidebars can be generated from the filesystem or explicitly defined here.
 *
 * Create as many sidebars as needed.
 */

const sidebars: SidebarsConfig = {
  // Laravel 문서를 위한 사이드바 설정
  tutorialSidebar: [
    {
      type: 'category',
      label: 'index',
      collapsed: false,
      items: [
        'index',
      ],
    },
  ],
};

export default sidebars;
