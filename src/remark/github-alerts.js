/**
 * Remark plugin to convert GitHub-style blockquote alerts to Docusaurus admonitions.
 *
 * Transforms:
 *   > [!NOTE]
 *   > Some text
 *
 * Into containerDirective nodes that Docusaurus renders as admonitions.
 */

const ALERT_TYPE_MAP = {
  NOTE: 'note',
  TIP: 'tip',
  IMPORTANT: 'info',
  WARNING: 'warning',
  CAUTION: 'danger',
};

const ALERT_REGEX = /^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n?/;

function visitBlockquotes(node, handler) {
  if (!node.children) return;
  for (let i = node.children.length - 1; i >= 0; i--) {
    const child = node.children[i];
    visitBlockquotes(child, handler);
    if (child.type === 'blockquote') {
      handler(child, i, node);
    }
  }
}

function remarkGithubAlerts() {
  return (tree) => {
    visitBlockquotes(tree, (node, index, parent) => {
      const firstChild = node.children && node.children[0];
      if (!firstChild || firstChild.type !== 'paragraph') return;

      const firstInline = firstChild.children && firstChild.children[0];
      if (!firstInline || firstInline.type !== 'text') return;

      const match = firstInline.value.match(ALERT_REGEX);
      if (!match) return;

      const admonitionType = ALERT_TYPE_MAP[match[1]];
      if (!admonitionType) return;

      // Remove the alert marker text
      firstInline.value = firstInline.value.slice(match[0].length);

      // If the text node is now empty, remove it
      if (!firstInline.value) {
        firstChild.children.shift();
      }

      // If the paragraph is now empty, remove it
      if (firstChild.children.length === 0) {
        node.children.shift();
      }

      // Replace blockquote with containerDirective (Docusaurus admonition)
      parent.children[index] = {
        type: 'containerDirective',
        name: admonitionType,
        attributes: {},
        children: node.children,
      };
    });
  };
}

module.exports = remarkGithubAlerts;
