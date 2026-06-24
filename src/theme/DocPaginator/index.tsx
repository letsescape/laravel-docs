import React, {type ReactNode} from 'react';
import clsx from 'clsx';
import Translate, {translate} from '@docusaurus/Translate';
import {useDocsSidebar} from '@docusaurus/plugin-content-docs/client';
import PaginatorNavLink from '@theme/PaginatorNavLink';
import type {Props} from '@theme/DocPaginator';
import type {
  PropSidebar,
  PropSidebarItem,
} from '@docusaurus/plugin-content-docs';

type NavLink = NonNullable<Props['previous']>;

function normalizePath(path: string): string {
  let end = path.length;

  while (end > 0 && path[end - 1] === '/') {
    end -= 1;
  }

  return path.slice(0, end) || '/';
}

function getSidebarLabel(
  items: PropSidebar,
  permalink: string,
): string | undefined {
  const target = normalizePath(permalink);
  const labels = new Set<string>();

  function visit(item: PropSidebarItem): void {
    if (item.type === 'link' && normalizePath(item.href) === target) {
      labels.add(item.label);
    }

    if (item.type === 'category') {
      if (item.href && normalizePath(item.href) === target) {
        labels.add(item.label);
      }

      for (const child of item.items) {
        visit(child);
      }
    }
  }

  for (const item of items) {
    visit(item);
  }

  return labels.size === 1 ? Array.from(labels)[0] : undefined;
}

function syncNavLinkTitle(link: NavLink, sidebarItems?: PropSidebar): NavLink {
  const title = sidebarItems && getSidebarLabel(sidebarItems, link.permalink);

  return title ? {...link, title} : link;
}

export default function DocPaginator(props: Props): ReactNode {
  const {className, previous, next} = props;
  const sidebar = useDocsSidebar();
  const translatedPrevious = previous
    ? syncNavLinkTitle(previous, sidebar?.items)
    : undefined;
  const translatedNext = next ? syncNavLinkTitle(next, sidebar?.items) : undefined;

  return (
    <nav
      className={clsx(className, 'pagination-nav')}
      aria-label={translate({
        id: 'theme.docs.paginator.navAriaLabel',
        message: 'Docs pages',
        description: 'The ARIA label for the docs pagination',
      })}>
      {translatedPrevious && (
        <PaginatorNavLink
          {...translatedPrevious}
          subLabel={
            <Translate
              id="theme.docs.paginator.previous"
              description="The label used to navigate to the previous doc">
              Previous
            </Translate>
          }
        />
      )}
      {translatedNext && (
        <PaginatorNavLink
          {...translatedNext}
          subLabel={
            <Translate
              id="theme.docs.paginator.next"
              description="The label used to navigate to the next doc">
              Next
            </Translate>
          }
          isNext
        />
      )}
    </nav>
  );
}
