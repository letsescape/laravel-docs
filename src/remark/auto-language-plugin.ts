import type {Transformer} from 'unified';
import type {Code, Root} from 'mdast';
import {visit} from 'unist-util-visit';

function detectLanguage(code: string): string {
  const trimmed = code.trim();
  if (!trimmed) return '';

  const firstLine = trimmed.split('\n')[0].trim();

  // Shell/Bash
  if (
    /^(php artisan|composer |npm |npx |cd |mkdir |curl |wget |sail |laravel |cp |mv |cat |echo |sudo |apt|brew |forge |git |docker |\.\/|pip |yarn )/.test(
      firstLine,
    )
  ) {
    return 'shell';
  }

  // ENV
  if (/^[A-Z][A-Z0-9_]+=/.test(firstLine)) {
    return 'ini';
  }

  // Blade
  if (
    /^(@extends|@section|@yield|@include|@component|@props|@if|@foreach|@for|@while|@switch|@unless|@push|@slot|@can|@cannot|@auth|@guest|@env|@production|<x-)/.test(
      firstLine,
    )
  ) {
    return 'blade';
  }

  // Blade ({{ }} pattern in first few lines)
  const firstFewLines = trimmed.split('\n').slice(0, 5).join('\n');
  if (/\{\{[^}]*\}\}/.test(firstFewLines) && /</.test(firstFewLines)) {
    return 'blade';
  }

  // HTML/XML
  if (/^(<\?xml|<!DOCTYPE|<html|<head|<body|<div|<form|<table|<ul|<ol|<p |<p>|<a |<span|<img|<link|<meta|<style|<script)/.test(firstLine)) {
    return 'html';
  }

  // JSON
  if (/^\s*[\[{]/.test(firstLine) && /"/.test(trimmed.slice(0, 200))) {
    return 'json';
  }

  // SQL
  if (
    /^(CREATE |ALTER |SELECT |INSERT |UPDATE |DELETE |DROP |GRANT |REVOKE |TRUNCATE |EXPLAIN )/i.test(
      firstLine,
    )
  ) {
    return 'sql';
  }

  // Nginx
  if (/^(server\s*\{|location\s)/.test(firstLine)) {
    return 'nginx';
  }

  // INI (section header)
  if (/^\[[\w.-]+\]/.test(firstLine)) {
    return 'ini';
  }

  // YAML (key: value, but not PHP-like)
  if (
    /^\w[\w.-]*\s*:/.test(firstLine) &&
    !firstLine.includes('$') &&
    !firstLine.includes('->') &&
    !firstLine.includes('(')
  ) {
    return 'yaml';
  }

  // Default to PHP for Laravel docs
  return 'php';
}

export default function autoLanguagePlugin(): Transformer<Root> {
  return (tree) => {
    visit(tree, 'code', (node: Code) => {
      if (!node.lang && node.value) {
        const detected = detectLanguage(node.value);
        if (detected) {
          node.lang = detected;
        }
      }
    });
  };
}
