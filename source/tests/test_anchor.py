import pytest

from utils.anchor import extract_anchor_definitions, extract_anchor_references, validate_anchors


class TestExtractAnchorDefinitions:
    def test_double_quotes(self):
        text = '<a name="basic-routing"></a>'
        assert extract_anchor_definitions(text) == {"basic-routing"}

    def test_single_quotes(self):
        text = "<a name='basic-routing'></a>"
        assert extract_anchor_definitions(text) == {"basic-routing"}

    def test_self_closing(self):
        text = '<a name="basic-routing"/>'
        assert extract_anchor_definitions(text) == {"basic-routing"}

    def test_self_closing_with_space(self):
        text = '<a name="basic-routing" />'
        assert extract_anchor_definitions(text) == {"basic-routing"}

    def test_multiple_anchors(self):
        text = (
            '<a name="introduction"></a>\n'
            '## Introduction\n\n'
            '<a name="installation"></a>\n'
            '### Installation\n'
        )
        assert extract_anchor_definitions(text) == {"introduction", "installation"}

    def test_no_anchors(self):
        text = "# Some heading\n\nSome text without anchors."
        assert extract_anchor_definitions(text) == set()

    def test_anchor_with_spaces(self):
        text = '<a  name="spaced-anchor"  >'
        assert extract_anchor_definitions(text) == {"spaced-anchor"}

    def test_ignores_other_a_tags(self):
        text = '<a href="https://example.com">link</a>'
        assert extract_anchor_definitions(text) == set()


class TestExtractAnchorReferences:
    def test_basic_reference(self):
        text = "- [Introduction](#introduction)"
        assert extract_anchor_references(text) == {"introduction"}

    def test_multiple_references(self):
        text = (
            "- [Introduction](#introduction)\n"
            "- [Installation](#installation)\n"
            "- [Configuration](#configuration)\n"
        )
        assert extract_anchor_references(text) == {"introduction", "installation", "configuration"}

    def test_no_references(self):
        text = "Some text without references."
        assert extract_anchor_references(text) == set()

    def test_ignores_external_references(self):
        text = "[Middleware](/docs/12.x/middleware#laravels-default-middleware-groups)"
        assert extract_anchor_references(text) == set()

    def test_ignores_url_references(self):
        text = "[Link](https://example.com#section)"
        assert extract_anchor_references(text) == set()

    def test_korean_link_text(self):
        text = "- [소개](#introduction)"
        assert extract_anchor_references(text) == {"introduction"}

    def test_empty_link_text(self):
        text = "[](#anchor)"
        assert extract_anchor_references(text) == {"anchor"}


class TestValidateAnchors:
    def test_valid_translation(self):
        original = (
            '<a name="introduction"></a>\n'
            '## Introduction\n\n'
            '- [Installation](#installation)\n\n'
            '<a name="installation"></a>\n'
            '### Installation\n'
        )
        translated = (
            '<a name="introduction"></a>\n'
            '## 소개 (Introduction)\n\n'
            '- [설치](#installation)\n\n'
            '<a name="installation"></a>\n'
            '### 설치\n'
        )
        is_valid, errors = validate_anchors(original, translated)
        assert is_valid is True
        assert errors == []

    def test_missing_anchor_in_translation(self):
        original = (
            '<a name="introduction"></a>\n'
            '## Introduction\n\n'
            '<a name="installation"></a>\n'
            '### Installation\n'
        )
        translated = (
            '<a name="introduction"></a>\n'
            '## 소개 (Introduction)\n\n'
            '### 설치\n'
        )
        is_valid, errors = validate_anchors(original, translated)
        assert is_valid is False
        assert len(errors) == 1
        assert "installation" in errors[0]

    def test_broken_reference_in_translation(self):
        original = (
            '<a name="introduction"></a>\n'
            '## Introduction\n'
        )
        translated = (
            '<a name="introduction"></a>\n'
            '## 소개 (Introduction)\n\n'
            '- [설치](#installation)\n'
        )
        is_valid, errors = validate_anchors(original, translated)
        assert is_valid is False
        assert len(errors) == 1
        assert "installation" in errors[0]

    def test_translated_anchor_name(self):
        """Anchor name should not be translated to Korean."""
        original = (
            '<a name="basic-routing"></a>\n'
            '## Basic Routing\n'
        )
        translated = (
            '<a name="기본-라우팅"></a>\n'
            '## 기본 라우팅 (Basic Routing)\n'
        )
        is_valid, errors = validate_anchors(original, translated)
        assert is_valid is False
        assert len(errors) >= 1

    def test_no_anchors_in_either(self):
        original = "# Title\n\nSome content."
        translated = "# 제목 (Title)\n\n내용입니다."
        is_valid, errors = validate_anchors(original, translated)
        assert is_valid is True
        assert errors == []

    def test_both_missing_and_broken(self):
        original = (
            '<a name="introduction"></a>\n'
            '## Introduction\n\n'
            '<a name="installation"></a>\n'
            '### Installation\n'
        )
        translated = (
            '## 소개 (Introduction)\n\n'
            '- [설치](#installation)\n'
            '### 설치\n'
        )
        is_valid, errors = validate_anchors(original, translated)
        assert is_valid is False
        assert len(errors) == 2

    def test_realistic_laravel_doc(self):
        """Test with a realistic Laravel documentation snippet."""
        original = (
            '# Routing\n\n'
            '- [Basic Routing](#basic-routing)\n'
            '    - [The Default Route Files](#the-default-route-files)\n'
            '    - [Redirect Routes](#redirect-routes)\n\n'
            '<a name="basic-routing"></a>\n'
            '## Basic Routing\n\n'
            'The most basic Laravel routes...\n\n'
            '<a name="the-default-route-files"></a>\n'
            '### The Default Route Files\n\n'
            '<a name="redirect-routes"></a>\n'
            '### Redirect Routes\n'
        )
        translated = (
            '# 라우팅 (Routing)\n\n'
            '- [기본 라우팅](#basic-routing)\n'
            '    - [기본 라우트 파일](#the-default-route-files)\n'
            '    - [리디렉션 라우트](#redirect-routes)\n\n'
            '<a name="basic-routing"></a>\n'
            '## 기본 라우팅\n\n'
            '가장 기본적인 라라벨 라우트는...\n\n'
            '<a name="the-default-route-files"></a>\n'
            '### 기본 라우트 파일\n\n'
            '<a name="redirect-routes"></a>\n'
            '### 리디렉션 라우트\n'
        )
        is_valid, errors = validate_anchors(original, translated)
        assert is_valid is True
        assert errors == []
