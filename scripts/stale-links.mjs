import {readFileSync} from 'node:fs';

const REGISTRY_URL = new URL(
  '../translation-sync/stale-links.json',
  import.meta.url,
);
const TOP_LEVEL_FIELDS = ['schema_version', 'links'];
const RULE_FIELDS = ['version', 'from', 'to', 'retire_mode'];
const RETIRE_MODES = new Set(['standalone-list-label', 'bare-inline-code']);
const EXTERNAL_TARGET = /^(?:[a-z][a-z\d+.-]*:|\/\/)/i;
const LARAVEL_DOCS_TARGET = /^https?:\/\/laravel\.com\/docs\//i;

function invalidRegistry() {
  throw new Error('invalid stale-link registry');
}

function compareUtf8(left, right) {
  return Buffer.compare(Buffer.from(left, 'utf8'), Buffer.from(right, 'utf8'));
}

function loadRules() {
  let raw;
  let registry;
  try {
    raw = readFileSync(REGISTRY_URL, 'utf8');
    registry = JSON.parse(raw);
  } catch {
    invalidRegistry();
  }

  if (
    registry === null ||
    typeof registry !== 'object' ||
    Array.isArray(registry) ||
    JSON.stringify(Object.keys(registry)) !== JSON.stringify(TOP_LEVEL_FIELDS) ||
    registry.schema_version !== 1 ||
    !Array.isArray(registry.links) ||
    `${JSON.stringify(registry, null, 2)}\n` !== raw
  ) {
    invalidRegistry();
  }

  const identities = new Set();
  let previous = null;
  for (const rule of registry.links) {
    if (
      rule === null ||
      typeof rule !== 'object' ||
      Array.isArray(rule) ||
      JSON.stringify(Object.keys(rule)) !== JSON.stringify(RULE_FIELDS) ||
      typeof rule.version !== 'string' ||
      !/^(?:master|\d+\.x)$/.test(rule.version) ||
      typeof rule.from !== 'string' ||
      !rule.from ||
      (rule.to !== null && (typeof rule.to !== 'string' || !rule.to)) ||
      (rule.to === null
        ? !RETIRE_MODES.has(rule.retire_mode)
        : rule.retire_mode !== null)
    ) {
      invalidRegistry();
    }
    const identity = `${rule.version}\u0000${rule.from}`;
    if (identities.has(identity)) invalidRegistry();
    identities.add(identity);
    if (
      previous !== null &&
      (compareUtf8(previous.version, rule.version) > 0 ||
        (previous.version === rule.version &&
          compareUtf8(previous.from, rule.from) > 0))
    ) {
      invalidRegistry();
    }
    previous = rule;
  }
  return Object.freeze(registry.links.map((rule) => Object.freeze({...rule})));
}

const RULES = loadRules();

export function staleLinkResolution(target, version) {
  if (
    EXTERNAL_TARGET.test(target) &&
    !LARAVEL_DOCS_TARGET.test(target)
  ) {
    return null;
  }

  const effectiveVersion = version || 'master';
  let retired = null;
  const matches = [];
  for (const rule of RULES) {
    if (rule.version !== effectiveVersion) continue;
    if (rule.to === null && target === rule.from) {
      retired = rule;
      break;
    }
    const start = target.length - rule.from.length;
    const suffixBoundary =
      start === 0 ||
      rule.from.startsWith('#') ||
      (start > 0 && target[start - 1] === '/');
    if (
      rule.to !== null &&
      start >= 0 &&
      suffixBoundary &&
      target.endsWith(rule.from)
    ) {
      matches.push(rule);
    }
  }

  const rule =
    retired ??
    matches.reduce(
      (best, candidate) =>
        best === null ||
        Buffer.byteLength(candidate.from) > Buffer.byteLength(best.from)
          ? candidate
          : best,
      null,
    );
  if (rule === null) return null;
  return {
    target:
      rule.to === null
        ? null
        : `${target.slice(0, -rule.from.length)}${rule.to}`,
    retireMode: rule.retire_mode,
  };
}
