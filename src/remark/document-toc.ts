import type {List, Root} from 'mdast';
import type {Transformer} from 'unified';

function isDocumentToc(list: List): boolean {
  return list.children.length > 0 && list.children.every(item =>
    item.children.length > 0 && item.children.every(child => {
      if (child.type === 'list') return isDocumentToc(child);
      return child.type === 'paragraph' && child.children.length === 1 &&
        child.children[0].type === 'link' && /^#.+/.test(child.children[0].url);
    }));
}

export default function documentTocPlugin(): Transformer<Root> {
  return (tree, file) => {
    const nodes = tree.children.filter(node =>
      !(node.type === 'html' && /^\s*<!--[\s\S]*-->\s*$/.test(node.value)));
    const [heading, list] = nodes;
    if (heading?.type !== 'heading' || heading.depth !== 1 ||
        list?.type !== 'list' || !isDocumentToc(list)) return;

    tree.children[tree.children.indexOf(list)] = {
      type: 'blockquote',
      data: {
        hName: 'nav',
        hProperties: {
          role: 'navigation',
          'aria-label': /(?:^|\/)i18n\/ja\//.test(String(file.path).replaceAll('\\', '/')) ? '目次' : '목차',
        },
      },
      children: [list],
    };
  };
}
