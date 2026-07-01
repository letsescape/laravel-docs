<!-- # Helpers -->
# Helpers

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Other Utilities](#other-utilities)
    - [Benchmarking](#benchmarking)
    - [Lottery](#lottery)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel includes a variety of global "helper" PHP functions. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient. -->
Laravel에는 다양한 전역 "헬퍼" PHP 함수들이 포함되어 있습니다. 이 함수들 중 상당수는 프레임워크 내부에서 사용되지만, 필요에 따라 여러분의 애플리케이션에서도 자유롭게 활용할 수 있습니다.

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods



<a name="arrays-and-objects-method-list"></a>
<!-- ### Arrays & Objects -->
### Arrays & Objects

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::forget](#method-array-forget)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAny](#method-array-hasany)
[Arr::isAssoc](#method-array-isassoc)
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[head](#method-head)
[last](#method-last)
</div>
-->
[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::forget](#method-array-forget)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAny](#method-array-hasany)
[Arr::isAssoc](#method-array-isassoc)
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[head](#method-head)
[last](#method-last)
</div>

<a name="paths-method-list"></a>
<!-- ### Paths -->
### Paths

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[mix](#method-mix)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)
-->
[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[mix](#method-mix)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

<!-- </div> -->
</div>

<a name="strings-method-list"></a>
<!-- ### Strings -->
### Strings

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[\__](#method-__)
[class_basename](#method-class-basename)
[e](#method-e)
[preg_replace_array](#method-preg-replace-array)
[Str::after](#method-str-after)
[Str::afterLast](#method-str-after-last)
[Str::ascii](#method-str-ascii)
[Str::before](#method-str-before)
[Str::beforeLast](#method-str-before-last)
[Str::between](#method-str-between)
[Str::betweenFirst](#method-str-between-first)
[Str::camel](#method-camel-case)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::endsWith](#method-ends-with)
[Str::excerpt](#method-excerpt)
[Str::finish](#method-str-finish)
[Str::headline](#method-str-headline)
[Str::inlineMarkdown](#method-str-inline-markdown)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isJson](#method-str-is-json)
[Str::isUlid](#method-str-is-ulid)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
[Str::lcfirst](#method-str-lcfirst)
[Str::length](#method-str-length)
[Str::limit](#method-str-limit)
[Str::lower](#method-str-lower)
[Str::markdown](#method-str-markdown)
[Str::mask](#method-str-mask)
[Str::orderedUuid](#method-str-ordered-uuid)
[Str::padBoth](#method-str-padboth)
[Str::padLeft](#method-str-padleft)
[Str::padRight](#method-str-padright)
[Str::plural](#method-str-plural)
[Str::pluralStudly](#method-str-plural-studly)
[Str::random](#method-str-random)
[Str::remove](#method-str-remove)
[Str::replace](#method-str-replace)
[Str::replaceArray](#method-str-replace-array)
[Str::replaceFirst](#method-str-replace-first)
[Str::replaceLast](#method-str-replace-last)
[Str::reverse](#method-str-reverse)
[Str::singular](#method-str-singular)
[Str::slug](#method-str-slug)
[Str::snake](#method-snake-case)
[Str::squish](#method-str-squish)
[Str::start](#method-str-start)
[Str::startsWith](#method-starts-with)
[Str::studly](#method-studly-case)
[Str::substr](#method-str-substr)
[Str::substrCount](#method-str-substrcount)
[Str::substrReplace](#method-str-substrreplace)
[Str::swap](#method-str-swap)
[Str::title](#method-title-case)
[Str::toHtmlString](#method-str-to-html-string)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::uuid](#method-str-uuid)
[Str::wordCount](#method-str-word-count)
[Str::words](#method-str-words)
[str](#method-str)
[trans](#method-trans)
[trans_choice](#method-trans-choice)
-->
[\__](#method-__)
[class_basename](#method-class-basename)
[e](#method-e)
[preg_replace_array](#method-preg-replace-array)
[Str::after](#method-str-after)
[Str::afterLast](#method-str-after-last)
[Str::ascii](#method-str-ascii)
[Str::before](#method-str-before)
[Str::beforeLast](#method-str-before-last)
[Str::between](#method-str-between)
[Str::betweenFirst](#method-str-between-first)
[Str::camel](#method-camel-case)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::endsWith](#method-ends-with)
[Str::excerpt](#method-excerpt)
[Str::finish](#method-str-finish)
[Str::headline](#method-str-headline)
[Str::inlineMarkdown](#method-str-inline-markdown)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isJson](#method-str-is-json)
[Str::isUlid](#method-str-is-ulid)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
[Str::lcfirst](#method-str-lcfirst)
[Str::length](#method-str-length)
[Str::limit](#method-str-limit)
[Str::lower](#method-str-lower)
[Str::markdown](#method-str-markdown)
[Str::mask](#method-str-mask)
[Str::orderedUuid](#method-str-ordered-uuid)
[Str::padBoth](#method-str-padboth)
[Str::padLeft](#method-str-padleft)
[Str::padRight](#method-str-padright)
[Str::plural](#method-str-plural)
[Str::pluralStudly](#method-str-plural-studly)
[Str::random](#method-str-random)
[Str::remove](#method-str-remove)
[Str::replace](#method-str-replace)
[Str::replaceArray](#method-str-replace-array)
[Str::replaceFirst](#method-str-replace-first)
[Str::replaceLast](#method-str-replace-last)
[Str::reverse](#method-str-reverse)
[Str::singular](#method-str-singular)
[Str::slug](#method-str-slug)
[Str::snake](#method-snake-case)
[Str::squish](#method-str-squish)
[Str::start](#method-str-start)
[Str::startsWith](#method-starts-with)
[Str::studly](#method-studly-case)
[Str::substr](#method-str-substr)
[Str::substrCount](#method-str-substrcount)
[Str::substrReplace](#method-str-substrreplace)
[Str::swap](#method-str-swap)
[Str::title](#method-title-case)
[Str::toHtmlString](#method-str-to-html-string)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::uuid](#method-str-uuid)
[Str::wordCount](#method-str-word-count)
[Str::words](#method-str-words)
[str](#method-str)
[trans](#method-trans)
[trans_choice](#method-trans-choice)

<!-- </div> -->
</div>

<a name="fluent-strings-method-list"></a>
<!-- ### Fluent Strings -->
### Fluent Strings

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[after](#method-fluent-str-after)
[afterLast](#method-fluent-str-after-last)
[append](#method-fluent-str-append)
[ascii](#method-fluent-str-ascii)
[basename](#method-fluent-str-basename)
[before](#method-fluent-str-before)
[beforeLast](#method-fluent-str-before-last)
[between](#method-fluent-str-between)
[betweenFirst](#method-fluent-str-between-first)
[camel](#method-fluent-str-camel)
[classBasename](#method-fluent-str-class-basename)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[dirname](#method-fluent-str-dirname)
[endsWith](#method-fluent-str-ends-with)
[excerpt](#method-fluent-str-excerpt)
[exactly](#method-fluent-str-exactly)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[headline](#method-fluent-str-headline)
[inlineMarkdown](#method-fluent-str-inline-markdown)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isJson](#method-fluent-str-is-json)
[isUlid](#method-fluent-str-is-ulid)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[lcfirst](#method-fluent-str-lcfirst)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[ltrim](#method-fluent-str-ltrim)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
[newLine](#method-fluent-str-new-line)
[padBoth](#method-fluent-str-padboth)
[padLeft](#method-fluent-str-padleft)
[padRight](#method-fluent-str-padright)
[pipe](#method-fluent-str-pipe)
[plural](#method-fluent-str-plural)
[prepend](#method-fluent-str-prepend)
[remove](#method-fluent-str-remove)
[replace](#method-fluent-str-replace)
[replaceArray](#method-fluent-str-replace-array)
[replaceFirst](#method-fluent-str-replace-first)
[replaceLast](#method-fluent-str-replace-last)
[replaceMatches](#method-fluent-str-replace-matches)
[rtrim](#method-fluent-str-rtrim)
[scan](#method-fluent-str-scan)
[singular](#method-fluent-str-singular)
[slug](#method-fluent-str-slug)
[snake](#method-fluent-str-snake)
[split](#method-fluent-str-split)
[squish](#method-fluent-str-squish)
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[swap](#method-fluent-str-swap)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[trim](#method-fluent-str-trim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenEmpty](#method-fluent-str-when-empty)
[whenNotEmpty](#method-fluent-str-when-not-empty)
[whenStartsWith](#method-fluent-str-when-starts-with)
[whenEndsWith](#method-fluent-str-when-ends-with)
[whenExactly](#method-fluent-str-when-exactly)
[whenNotExactly](#method-fluent-str-when-not-exactly)
[whenIs](#method-fluent-str-when-is)
[whenIsAscii](#method-fluent-str-when-is-ascii)
[whenIsUlid](#method-fluent-str-when-is-ulid)
[whenIsUuid](#method-fluent-str-when-is-uuid)
[whenTest](#method-fluent-str-when-test)
[wordCount](#method-fluent-str-word-count)
[words](#method-fluent-str-words)
-->
[after](#method-fluent-str-after)
[afterLast](#method-fluent-str-after-last)
[append](#method-fluent-str-append)
[ascii](#method-fluent-str-ascii)
[basename](#method-fluent-str-basename)
[before](#method-fluent-str-before)
[beforeLast](#method-fluent-str-before-last)
[between](#method-fluent-str-between)
[betweenFirst](#method-fluent-str-between-first)
[camel](#method-fluent-str-camel)
[classBasename](#method-fluent-str-class-basename)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[dirname](#method-fluent-str-dirname)
[endsWith](#method-fluent-str-ends-with)
[excerpt](#method-fluent-str-excerpt)
[exactly](#method-fluent-str-exactly)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[headline](#method-fluent-str-headline)
[inlineMarkdown](#method-fluent-str-inline-markdown)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isJson](#method-fluent-str-is-json)
[isUlid](#method-fluent-str-is-ulid)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[lcfirst](#method-fluent-str-lcfirst)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[ltrim](#method-fluent-str-ltrim)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
[newLine](#method-fluent-str-new-line)
[padBoth](#method-fluent-str-padboth)
[padLeft](#method-fluent-str-padleft)
[padRight](#method-fluent-str-padright)
[pipe](#method-fluent-str-pipe)
[plural](#method-fluent-str-plural)
[prepend](#method-fluent-str-prepend)
[remove](#method-fluent-str-remove)
[replace](#method-fluent-str-replace)
[replaceArray](#method-fluent-str-replace-array)
[replaceFirst](#method-fluent-str-replace-first)
[replaceLast](#method-fluent-str-replace-last)
[replaceMatches](#method-fluent-str-replace-matches)
[rtrim](#method-fluent-str-rtrim)
[scan](#method-fluent-str-scan)
[singular](#method-fluent-str-singular)
[slug](#method-fluent-str-slug)
[snake](#method-fluent-str-snake)
[split](#method-fluent-str-split)
[squish](#method-fluent-str-squish)
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[swap](#method-fluent-str-swap)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[trim](#method-fluent-str-trim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenEmpty](#method-fluent-str-when-empty)
[whenNotEmpty](#method-fluent-str-when-not-empty)
[whenStartsWith](#method-fluent-str-when-starts-with)
[whenEndsWith](#method-fluent-str-when-ends-with)
[whenExactly](#method-fluent-str-when-exactly)
[whenNotExactly](#method-fluent-str-when-not-exactly)
[whenIs](#method-fluent-str-when-is)
[whenIsAscii](#method-fluent-str-when-is-ascii)
[whenIsUlid](#method-fluent-str-when-is-ulid)
[whenIsUuid](#method-fluent-str-when-is-uuid)
[whenTest](#method-fluent-str-when-test)
[wordCount](#method-fluent-str-word-count)
[words](#method-fluent-str-words)

<!-- </div> -->
</div>

<a name="urls-method-list"></a>
<!-- ### URLs -->
### URLs

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_route](#method-to-route)
[url](#method-url)
-->
[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_route](#method-to-route)
[url](#method-url)

<!-- </div> -->
</div>

<a name="miscellaneous-method-list"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[app](#method-app)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[blank](#method-blank)
[broadcast](#method-broadcast)
[cache](#method-cache)
[class_uses_recursive](#method-class-uses-recursive)
[collect](#method-collect)
[config](#method-config)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[optional](#method-optional)
[policy](#method-policy)
[redirect](#method-redirect)
[report](#method-report)
[report_if](#method-report-if)
[report_unless](#method-report-unless)
[request](#method-request)
[rescue](#method-rescue)
[resolve](#method-resolve)
[response](#method-response)
[retry](#method-retry)
[session](#method-session)
[tap](#method-tap)
[throw_if](#method-throw-if)
[throw_unless](#method-throw-unless)
[today](#method-today)
[trait_uses_recursive](#method-trait-uses-recursive)
[transform](#method-transform)
[validator](#method-validator)
[value](#method-value)
[view](#method-view)
[with](#method-with)
-->
[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[app](#method-app)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[blank](#method-blank)
[broadcast](#method-broadcast)
[cache](#method-cache)
[class_uses_recursive](#method-class-uses-recursive)
[collect](#method-collect)
[config](#method-config)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[optional](#method-optional)
[policy](#method-policy)
[redirect](#method-redirect)
[report](#method-report)
[report_if](#method-report-if)
[report_unless](#method-report-unless)
[request](#method-request)
[rescue](#method-rescue)
[resolve](#method-resolve)
[response](#method-response)
[retry](#method-retry)
[session](#method-session)
[tap](#method-tap)
[throw_if](#method-throw-if)
[throw_unless](#method-throw-unless)
[today](#method-today)
[trait_uses_recursive](#method-trait-uses-recursive)
[transform](#method-transform)
[validator](#method-validator)
[value](#method-value)
[view](#method-view)
[with](#method-with)

<!-- </div> -->
</div>

<a name="method-listing"></a>
<!-- ## Method Listing -->
## Method Listing



<a name="arrays"></a>
<!-- ## Arrays & Objects -->
## Arrays & Objects

<a name="method-array-accessible"></a>
<!-- #### `Arr::accessible()` -->
#### `Arr::accessible()`

<!-- The `Arr::accessible` method determines if the given value is array accessible: -->
`Arr::accessible` 메서드는 전달한 값이 배열로 접근 가능한지 여부를 판단합니다.

```
use Illuminate\Support\Arr;
use Illuminate\Support\Collection;

$isAccessible = Arr::accessible(['a' => 1, 'b' => 2]);

// true

$isAccessible = Arr::accessible(new Collection);

// true

$isAccessible = Arr::accessible('abc');

// false

$isAccessible = Arr::accessible(new stdClass);

// false
```

<a name="method-array-add"></a>
<!-- #### `Arr::add()` -->
#### `Arr::add()`

<!-- The `Arr::add` method adds a given key / value pair to an array if the given key doesn't already exist in the array or is set to `null`: -->
`Arr::add` 메서드는 배열에 주어진 키가 존재하지 않거나 값이 `null`인 경우, 해당 키/값 쌍을 배열에 추가합니다.

```
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```


<a name="method-array-collapse"></a>
<!-- #### `Arr::collapse()` -->
#### `Arr::collapse()`

<!-- The `Arr::collapse` method collapses an array of arrays into a single array: -->
`Arr::collapse` 메서드는 여러 배열로 이루어진 배열을 하나로 평탄화하여 단일 배열로 만들어 반환합니다.

```
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
<!-- #### `Arr::crossJoin()` -->
#### `Arr::crossJoin()`

<!-- The `Arr::crossJoin` method cross joins the given arrays, returning a Cartesian product with all possible permutations: -->
`Arr::crossJoin` 메서드는 주어진 여러 배열을 교차 결합하여 가능한 모든 조합(카테시안 곱)을 반환합니다.

```
use Illuminate\Support\Arr;

$matrix = Arr::crossJoin([1, 2], ['a', 'b']);

/*
    [
        [1, 'a'],
        [1, 'b'],
        [2, 'a'],
        [2, 'b'],
    ]
*/

$matrix = Arr::crossJoin([1, 2], ['a', 'b'], ['I', 'II']);

/*
    [
        [1, 'a', 'I'],
        [1, 'a', 'II'],
        [1, 'b', 'I'],
        [1, 'b', 'II'],
        [2, 'a', 'I'],
        [2, 'a', 'II'],
        [2, 'b', 'I'],
        [2, 'b', 'II'],
    ]
*/
```

<a name="method-array-divide"></a>
<!-- #### `Arr::divide()` -->
#### `Arr::divide()`

<!-- The `Arr::divide` method returns two arrays: one containing the keys and the other containing the values of the given array: -->
`Arr::divide` 메서드는 전달받은 배열을 두 개의 배열로 분리합니다. 하나는 키(key)만, 다른 배열은 값(value)만 담아 반환합니다.

```
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
<!-- #### `Arr::dot()` -->
#### `Arr::dot()`

<!-- The `Arr::dot` method flattens a multi-dimensional array into a single level array that uses "dot" notation to indicate depth: -->
`Arr::dot` 메서드는 다차원 배열을 점(dot) 표기법을 사용하여 한 단계(1차원) 배열로 평탄화합니다.

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
<!-- #### `Arr::except()` -->
#### `Arr::except()`

<!-- The `Arr::except` method removes the given key / value pairs from an array: -->
`Arr::except` 메서드는 배열에서 지정한 키/값 쌍을 제거합니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-exists"></a>
<!-- #### `Arr::exists()` -->
#### `Arr::exists()`

<!-- The `Arr::exists` method checks that the given key exists in the provided array: -->
`Arr::exists` 메서드는 주어진 배열에 해당 키가 존재하는지 확인합니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'John Doe', 'age' => 17];

$exists = Arr::exists($array, 'name');

// true

$exists = Arr::exists($array, 'salary');

// false
```

<a name="method-array-first"></a>
<!-- #### `Arr::first()` -->
#### `Arr::first()`

<!-- The `Arr::first` method returns the first element of an array passing a given truth test: -->
`Arr::first` 메서드는 배열에서 전달된 조건을 만족하는 첫 번째 요소를 반환합니다.

```
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function ($value, $key) {
    return $value >= 150;
});

// 200
```

<!-- A default value may also be passed as the third parameter to the method. This value will be returned if no value passes the truth test: -->
세 번째 인자로 기본값을 함께 전달할 수도 있습니다. 조건에 맞는 값이 없을 경우 이 기본값이 반환됩니다.

```
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
<!-- #### `Arr::flatten()` -->
#### `Arr::flatten()`

<!-- The `Arr::flatten` method flattens a multi-dimensional array into a single level array: -->
`Arr::flatten` 메서드는 다차원 배열을 한 단계(1차원) 배열로 평탄화합니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-forget"></a>
<!-- #### `Arr::forget()` -->
#### `Arr::forget()`

<!-- The `Arr::forget` method removes a given key / value pair from a deeply nested array using "dot" notation: -->
`Arr::forget` 메서드는 점(dot) 표기법을 사용해 깊이 중첩된 배열에서 특정 키/값 쌍을 제거합니다.

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-get"></a>
<!-- #### `Arr::get()` -->
#### `Arr::get()`

<!-- The `Arr::get` method retrieves a value from a deeply nested array using "dot" notation: -->
`Arr::get` 메서드는 점(dot) 표기법을 활용하여 깊이 중첩된 배열에서 값을 가져옵니다.

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

<!-- The `Arr::get` method also accepts a default value, which will be returned if the specified key is not present in the array: -->
또한 `Arr::get` 메서드는 기본값을 세 번째 인자로 전달할 수 있습니다. 지정한 키가 배열에 없을 경우 이 값이 반환됩니다.

```
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>

<!-- #### `Arr::has()` -->
#### `Arr::has()`

<!-- The `Arr::has` method checks whether a given item or items exists in an array using "dot" notation: -->
`Arr::has` 메서드는 "dot" 표기법을 사용하여 배열에 지정한 항목이 존재하는지 확인합니다:

```
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::has($array, 'product.name');

// true

$contains = Arr::has($array, ['product.price', 'product.discount']);

// false
```

<a name="method-array-hasany"></a>
<!-- #### `Arr::hasAny()` -->
#### `Arr::hasAny()`

<!-- The `Arr::hasAny` method checks whether any item in a given set exists in an array using "dot" notation: -->
`Arr::hasAny` 메서드는 "dot" 표기법을 사용하여 지정된 여러 항목 중 하나라도 배열에 존재하는지 확인합니다:

```
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::hasAny($array, 'product.name');

// true

$contains = Arr::hasAny($array, ['product.name', 'product.discount']);

// true

$contains = Arr::hasAny($array, ['category', 'product.discount']);

// false
```

<a name="method-array-isassoc"></a>
<!-- #### `Arr::isAssoc()` -->
#### `Arr::isAssoc()`

<!-- The `Arr::isAssoc` method returns `true` if the given array is an associative array. An array is considered "associative" if it doesn't have sequential numerical keys beginning with zero: -->
`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열(associative array)인지 여부를 `true`로 반환합니다. 배열의 키가 0부터 시작하는 순차적인 숫자가 아니면 연관 배열로 간주합니다:

```
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
<!-- #### `Arr::isList()` -->
#### `Arr::isList()`

<!-- The `Arr::isList` method returns `true` if the given array's keys are sequential integers beginning from zero: -->
`Arr::isList` 메서드는 배열의 키가 0부터 시작하는 순차적인 정수형이면 `true`를 반환합니다:

```
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
<!-- #### `Arr::join()` -->
#### `Arr::join()`

<!-- The `Arr::join` method joins array elements with a string. Using this method's second argument, you may also specify the joining string for the final element of the array: -->
`Arr::join` 메서드는 배열 요소들을 문자열로 합칩니다. 두 번째 인수로 구분자를 지정할 수 있으며, 배열의 마지막 요소 앞에 들어갈 구분자도 세 번째 인수로 따로 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

$joined = Arr::join($array, ', ');

// Tailwind, Alpine, Laravel, Livewire

$joined = Arr::join($array, ', ', ' and ');

// Tailwind, Alpine, Laravel and Livewire
```

<a name="method-array-keyby"></a>
<!-- #### `Arr::keyBy()` -->
#### `Arr::keyBy()`

<!-- The `Arr::keyBy` method keys the array by the given key. If multiple items have the same key, only the last one will appear in the new array: -->
`Arr::keyBy` 메서드는 지정한 키의 값을 배열의 키로 사용하여 배열을 재구성합니다. 동일한 키를 가진 항목이 여러 개면 마지막 항목만 새 배열에 포함됩니다:

```
use Illuminate\Support\Arr;

$array = [
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
];

$keyed = Arr::keyBy($array, 'product_id');

/*
    [
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

<a name="method-array-last"></a>
<!-- #### `Arr::last()` -->
#### `Arr::last()`

<!-- The `Arr::last` method returns the last element of an array passing a given truth test: -->
`Arr::last` 메서드는 전달한 조건(콜백)에 만족하는 배열의 마지막 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function ($value, $key) {
    return $value >= 150;
});

// 300
```

<!-- A default value may be passed as the third argument to the method. This value will be returned if no value passes the truth test: -->
조건에 만족하는 값이 없을 경우, 세 번째 인수로 기본값을 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
<!-- #### `Arr::map()` -->
#### `Arr::map()`

<!-- The `Arr::map` method iterates through the array and passes each value and key to the given callback. The array value is replaced by the value returned by the callback: -->
`Arr::map` 메서드는 배열을 순회하면서 각 값과 키를 지정한 콜백에 전달하여, 콜백이 반환한 값으로 배열의 값을 대체합니다:

```
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function ($value, $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
```

<a name="method-array-only"></a>
<!-- #### `Arr::only()` -->
#### `Arr::only()`

<!-- The `Arr::only` method returns only the specified key / value pairs from the given array: -->
`Arr::only` 메서드는 배열에서 지정한 키에 해당하는 키/값 쌍만 추출하여 반환합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-pluck"></a>
<!-- #### `Arr::pluck()` -->
#### `Arr::pluck()`

<!-- The `Arr::pluck` method retrieves all of the values for a given key from an array: -->
`Arr::pluck` 메서드는 배열에서 지정한 키에 해당하는 값만 모두 가져와서 반환합니다:

```
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

<!-- You may also specify how you wish the resulting list to be keyed: -->
결과 배열의 키를 어떻게 할지 세 번째 인수로 추가 지정할 수도 있습니다:

```
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
<!-- #### `Arr::prepend()` -->
#### `Arr::prepend()`

<!-- The `Arr::prepend` method will push an item onto the beginning of an array: -->
`Arr::prepend` 메서드는 항목을 배열의 맨 앞에 추가합니다:

```
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

<!-- If needed, you may specify the key that should be used for the value: -->
필요에 따라, 추가할 값에 사용할 키도 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
<!-- #### `Arr::prependKeysWith()` -->
#### `Arr::prependKeysWith()`

<!-- The `Arr::prependKeysWith` prepends all key names of an associative array with the given prefix: -->
`Arr::prependKeysWith`는 연관 배열의 모든 키명 앞에 지정한 접두어(prefix)를 붙입니다:

```
use Illuminate\Support\Arr;

$array = [
    'name' => 'Desk',
    'price' => 100,
];

$keyed = Arr::prependKeysWith($array, 'product.');

/*
    [
        'product.name' => 'Desk',
        'product.price' => 100,
    ]
*/
```

<a name="method-array-pull"></a>
<!-- #### `Arr::pull()` -->
#### `Arr::pull()`

<!-- The `Arr::pull` method returns and removes a key / value pair from an array: -->
`Arr::pull` 메서드는 배열에서 키/값 쌍을 반환하면서 해당 항목을 배열에서 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

<!-- A default value may be passed as the third argument to the method. This value will be returned if the key doesn't exist: -->
키가 존재하지 않을 경우 반환할 기본값을 세 번째 인수로 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
<!-- #### `Arr::query()` -->
#### `Arr::query()`

<!-- The `Arr::query` method converts the array into a query string: -->
`Arr::query` 메서드는 배열을 쿼리 문자열로 변환합니다:

```
use Illuminate\Support\Arr;

$array = [
    'name' => 'Taylor',
    'order' => [
        'column' => 'created_at',
        'direction' => 'desc'
    ]
];

Arr::query($array);

// name=Taylor&order[column]=created_at&order[direction]=desc
```

<a name="method-array-random"></a>
<!-- #### `Arr::random()` -->
#### `Arr::random()`

<!-- The `Arr::random` method returns a random value from an array: -->
`Arr::random` 메서드는 배열에서 무작위로 값을 반환합니다:

```
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (retrieved randomly)
```

<!-- You may also specify the number of items to return as an optional second argument. Note that providing this argument will return an array even if only one item is desired: -->
두 번째 인수로 반환받을 항목의 개수를 지정할 수도 있습니다. 이 인수를 지정하면, 하나만 선택하더라도 배열 형태로 반환됩니다:

```
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (retrieved randomly)
```

<a name="method-array-set"></a>
<!-- #### `Arr::set()` -->
#### `Arr::set()`

<!-- The `Arr::set` method sets a value within a deeply nested array using "dot" notation: -->
`Arr::set` 메서드는 "dot" 표기법을 사용하여 중첩 배열 내부의 값을 설정합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
<!-- #### `Arr::shuffle()` -->
#### `Arr::shuffle()`

<!-- The `Arr::shuffle` method randomly shuffles the items in the array: -->
`Arr::shuffle` 메서드는 배열의 항목들을 무작위로 섞어서 반환합니다:

```
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-array-sort"></a>
<!-- #### `Arr::sort()` -->
#### `Arr::sort()`

<!-- The `Arr::sort` method sorts an array by its values: -->
`Arr::sort` 메서드는 배열을 값 기준으로 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

<!-- You may also sort the array by the results of a given closure: -->
콜백을 전달하여 해당 콜백의 실행 결과를 기준으로 정렬할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sort($array, function ($value) {
    return $value['name'];
}));

/*
    [
        ['name' => 'Chair'],
        ['name' => 'Desk'],
        ['name' => 'Table'],
    ]
*/
```

<a name="method-array-sort-desc"></a>
<!-- #### `Arr::sortDesc()` -->
#### `Arr::sortDesc()`

<!-- The `Arr::sortDesc` method sorts an array in descending order by its values: -->
`Arr::sortDesc` 메서드는 배열을 값 기준으로 내림차순 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

<!-- You may also sort the array by the results of a given closure: -->
콜백을 전달하여 해당 콜백의 실행 결과를 기준으로 내림차순 정렬할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sortDesc($array, function ($value) {
    return $value['name'];
}));

/*
    [
        ['name' => 'Table'],
        ['name' => 'Desk'],
        ['name' => 'Chair'],
    ]
*/
```

<a name="method-array-sort-recursive"></a>
<!-- #### `Arr::sortRecursive()` -->
#### `Arr::sortRecursive()`

<!-- The `Arr::sortRecursive` method recursively sorts an array using the `sort` function for numerically indexed sub-arrays and the `ksort` function for associative sub-arrays: -->
`Arr::sortRecursive` 메서드는 배열 내부를 재귀적으로 정렬합니다. 숫자 인덱스를 가진 하위 배열은 `sort` 함수를, 연관 배열은 `ksort` 함수를 사용해 정렬합니다:

```
use Illuminate\Support\Arr;

$array = [
    ['Roman', 'Taylor', 'Li'],
    ['PHP', 'Ruby', 'JavaScript'],
    ['one' => 1, 'two' => 2, 'three' => 3],
];

$sorted = Arr::sortRecursive($array);

/*
    [
        ['JavaScript', 'PHP', 'Ruby'],
        ['one' => 1, 'three' => 3, 'two' => 2],
        ['Li', 'Roman', 'Taylor'],
    ]
*/
```

<a name="method-array-to-css-classes"></a>
<!-- #### `Arr::toCssClasses()` -->
#### `Arr::toCssClasses()`

<!-- The `Arr::toCssClasses` conditionally compiles a CSS class string. The method accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`Arr::toCssClasses` 메서드는 조건에 따라 CSS 클래스 문자열을 동적으로 만듭니다. 이 메서드는, 배열의 키에 추가하고 싶은 클래스 이름 또는 클래스들, 값에는 조건식을 설정합니다. 배열 요소의 키가 숫자인 경우에는 해당 항목이 항상 결과 클래스 리스트에 포함됩니다:

```
use Illuminate\Support\Arr;

$isActive = false;
$hasError = true;

$array = ['p-4', 'font-bold' => $isActive, 'bg-red' => $hasError];

$classes = Arr::toCssClasses($array);

/*
    'p-4 bg-red'
*/
```

<!-- This method powers Laravel's functionality allowing [merging classes with a Blade component's attribute bag](/docs/9.x/blade#conditionally-merge-classes) as well as the `@class` [Blade directive](/docs/9.x/blade#conditional-classes). -->
이 메서드는 Laravel의 [merging classes with a Blade component's attribute bag](/docs/9.x/blade#conditionally-merge-classes)이나 `@class` [Blade directive](/docs/9.x/blade#conditional-classes)에서도 사용됩니다.

<a name="method-array-undot"></a>
<!-- #### `Arr::undot()` -->
#### `Arr::undot()`

<!-- The `Arr::undot` method expands a single-dimensional array that uses "dot" notation into a multi-dimensional array: -->
`Arr::undot` 메서드는 "dot" 표기법으로 작성된 단일 차원 배열을 다차원 배열로 확장합니다:

```
use Illuminate\Support\Arr;

$array = [
    'user.name' => 'Kevin Malone',
    'user.occupation' => 'Accountant',
];

$array = Arr::undot($array);

// ['user' => ['name' => 'Kevin Malone', 'occupation' => 'Accountant']]
```

<a name="method-array-where"></a>
<!-- #### `Arr::where()` -->
#### `Arr::where()`

<!-- The `Arr::where` method filters an array using the given closure: -->
`Arr::where` 메서드는 지정한 콜백을 사용해 배열을 필터링합니다:

```
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::where($array, function ($value, $key) {
    return is_string($value);
});

// [1 => '200', 3 => '400']
```

<a name="method-array-where-not-null"></a>
<!-- #### `Arr::whereNotNull()` -->
#### `Arr::whereNotNull()`

<!-- The `Arr::whereNotNull` method removes all `null` values from the given array: -->
`Arr::whereNotNull` 메서드는 배열에서 모든 `null` 값을 제거합니다:

```
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
<!-- #### `Arr::wrap()` -->
#### `Arr::wrap()`

<!-- The `Arr::wrap` method wraps the given value in an array. If the given value is already an array it will be returned without modification: -->
`Arr::wrap` 메서드는 지정한 값을 배열로 감싸서 반환합니다. 이미 배열인 값이면 그대로 반환됩니다:

```
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

<!-- If the given value is `null`, an empty array will be returned: -->
지정한 값이 `null`인 경우에는 빈 배열을 반환합니다:

```
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
<!-- #### `data_fill()` -->
#### `data_fill()`

<!-- The `data_fill` function sets a missing value within a nested array or object using "dot" notation: -->
`data_fill` 함수는 "dot" 표기법을 사용해 중첩 배열 또는 객체 내에 아직 없는 값을 설정합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

<!-- This function also accepts asterisks as wildcards and will fill the target accordingly: -->
이 함수는 와일드카드로 별표(*)도 사용할 수 있으며, 일치하는 모든 대상에 값을 채워줍니다:

```
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2'],
    ],
];

data_fill($data, 'products.*.price', 200);

/*
    [
        'products' => [
            ['name' => 'Desk 1', 'price' => 100],
            ['name' => 'Desk 2', 'price' => 200],
        ],
    ]
*/
```

<a name="method-data-get"></a>

<!-- #### `data_get()` -->
#### `data_get()`

<!-- The `data_get` function retrieves a value from a nested array or object using "dot" notation: -->
`data_get` 함수는 "점(dot) 표기법"을 사용하여 중첩된 배열이나 객체에서 원하는 값을 가져옵니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

<!-- The `data_get` function also accepts a default value, which will be returned if the specified key is not found: -->
`data_get` 함수는 기본값도 지정할 수 있습니다. 지정한 키가 존재하지 않을 경우 두 번째 인자로 넘긴 기본값이 반환됩니다.

```
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

<!-- The function also accepts wildcards using asterisks, which may target any key of the array or object: -->
이 함수는 애스터리스크(asterisk)를 이용한 와일드카드도 지원하여, 배열이나 객체의 모든 키를 대상으로 값을 가져올 수 있습니다.

```
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

<a name="method-data-set"></a>
<!-- #### `data_set()` -->
#### `data_set()`

<!-- The `data_set` function sets a value within a nested array or object using "dot" notation: -->
`data_set` 함수는 "점(dot) 표기법"을 사용하여 중첩된 배열이나 객체의 값을 설정합니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<!-- This function also accepts wildcards using asterisks and will set values on the target accordingly: -->
이 함수 역시 와일드카드로 애스터리스크(asterisk)를 사용할 수 있으며, 조건에 맞는 모든 대상에 대해 값을 설정합니다.

```
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2', 'price' => 150],
    ],
];

data_set($data, 'products.*.price', 200);

/*
    [
        'products' => [
            ['name' => 'Desk 1', 'price' => 200],
            ['name' => 'Desk 2', 'price' => 200],
        ],
    ]
*/
```

<!-- By default, any existing values are overwritten. If you wish to only set a value if it doesn't exist, you may pass `false` as the fourth argument to the function: -->
기본적으로, 기존 값이 있더라도 덮어쓰기가 됩니다. 만약 값이 없을 때만 설정하고 싶다면 네 번째 인자로 `false`를 전달하면 됩니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-head"></a>
<!-- #### `head()` -->
#### `head()`

<!-- The `head` function returns the first element in the given array: -->
`head` 함수는 전달된 배열의 첫 번째 요소를 반환합니다.

```
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
<!-- #### `last()` -->
#### `last()`

<!-- The `last` function returns the last element in the given array: -->
`last` 함수는 전달된 배열의 마지막 요소를 반환합니다.

```
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="paths"></a>
<!-- ## Paths -->
## Paths

<a name="method-app-path"></a>
<!-- #### `app_path()` -->
#### `app_path()`

<!-- The `app_path` function returns the fully qualified path to your application's `app` directory. You may also use the `app_path` function to generate a fully qualified path to a file relative to the application directory: -->
`app_path` 함수는 애플리케이션의 `app` 디렉터리에 대한 전체 경로를 반환합니다. 또한 `app_path` 함수를 사용해 애플리케이션 디렉터리를 기준으로 하는 파일의 전체 경로를 만들 수도 있습니다.

```
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
<!-- #### `base_path()` -->
#### `base_path()`

<!-- The `base_path` function returns the fully qualified path to your application's root directory. You may also use the `base_path` function to generate a fully qualified path to a given file relative to the project root directory: -->
`base_path` 함수는 애플리케이션 루트 디렉터리(프로젝트의 최상위 경로)의 전체 경로를 반환합니다. 또한 `base_path` 함수를 사용해 프로젝트 루트 디렉터리 기준으로 특정 파일의 전체 경로를 생성할 수도 있습니다.

```
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
<!-- #### `config_path()` -->
#### `config_path()`

<!-- The `config_path` function returns the fully qualified path to your application's `config` directory. You may also use the `config_path` function to generate a fully qualified path to a given file within the application's configuration directory: -->
`config_path` 함수는 애플리케이션의 `config` 디렉터리에 대한 전체 경로를 반환합니다. 또한 `config_path` 함수를 사용해 설정 디렉터리 내 특정 파일의 전체 경로를 만들 수도 있습니다.

```
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
<!-- #### `database_path()` -->
#### `database_path()`

<!-- The `database_path` function returns the fully qualified path to your application's `database` directory. You may also use the `database_path` function to generate a fully qualified path to a given file within the database directory: -->
`database_path` 함수는 애플리케이션의 `database` 디렉터리에 대한 전체 경로를 반환합니다. 또한 `database_path` 함수를 사용해 데이터베이스 디렉터리 내 특정 파일의 전체 경로를 만들 수도 있습니다.

```
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
<!-- #### `lang_path()` -->
#### `lang_path()`

<!-- The `lang_path` function returns the fully qualified path to your application's `lang` directory. You may also use the `lang_path` function to generate a fully qualified path to a given file within the directory: -->
`lang_path` 함수는 애플리케이션의 `lang` 디렉터리에 대한 전체 경로를 반환합니다. 또한 `lang_path` 함수를 사용해 해당 디렉터리 내 특정 파일의 전체 경로를 만들 수도 있습니다.

```
$path = lang_path();

$path = lang_path('en/messages.php');
```

<a name="method-mix"></a>
<!-- #### `mix()` -->
#### `mix()`

<!-- The `mix` function returns the path to a [versioned Mix file](/docs/9.x/mix): -->
`mix` 함수는 [versioned Mix file](/docs/9.x/mix)의 경로를 반환합니다.

```
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
<!-- #### `public_path()` -->
#### `public_path()`

<!-- The `public_path` function returns the fully qualified path to your application's `public` directory. You may also use the `public_path` function to generate a fully qualified path to a given file within the public directory: -->
`public_path` 함수는 애플리케이션의 `public` 디렉터리에 대한 전체 경로를 반환합니다. 또한 `public_path` 함수를 사용해 public 디렉터리 내 특정 파일의 전체 경로를 만들 수도 있습니다.

```
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
<!-- #### `resource_path()` -->
#### `resource_path()`

<!-- The `resource_path` function returns the fully qualified path to your application's `resources` directory. You may also use the `resource_path` function to generate a fully qualified path to a given file within the resources directory: -->
`resource_path` 함수는 애플리케이션의 `resources` 디렉터리에 대한 전체 경로를 반환합니다. 또한 `resource_path` 함수를 사용해 resources 디렉터리 내 특정 파일의 전체 경로를 생성할 수도 있습니다.

```
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
<!-- #### `storage_path()` -->
#### `storage_path()`

<!-- The `storage_path` function returns the fully qualified path to your application's `storage` directory. You may also use the `storage_path` function to generate a fully qualified path to a given file within the storage directory: -->
`storage_path` 함수는 애플리케이션의 `storage` 디렉터리에 대한 전체 경로를 반환합니다. 또한 `storage_path` 함수를 사용해 storage 디렉터리 내 특정 파일의 전체 경로를 만들 수도 있습니다.

```
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="strings"></a>
<!-- ## Strings -->
## Strings

<a name="method-__"></a>
<!-- #### `__()` -->
#### `__()`

<!-- The `__` function translates the given translation string or translation key using your [localization files](/docs/9.x/localization): -->
`__` 함수는 [localization files](/docs/9.x/localization)을 이용하여 지정한 번역 문자열 또는 키를 번역합니다.

```
echo __('Welcome to our application');

echo __('messages.welcome');
```

<!-- If the specified translation string or key does not exist, the `__` function will return the given value. So, using the example above, the `__` function would return `messages.welcome` if that translation key does not exist. -->
만약 지정한 번역 문자열이나 키가 존재하지 않을 경우, `__` 함수는 전달된 값을 그대로 반환합니다. 따라서 위 예시에서 해당 번역 키가 존재하지 않으면 `__` 함수는 `messages.welcome`을 그대로 반환합니다.

<a name="method-class-basename"></a>
<!-- #### `class_basename()` -->
#### `class_basename()`

<!-- The `class_basename` function returns the class name of the given class with the class's namespace removed: -->
`class_basename` 함수는 네임스페이스를 제외하고, 주어진 클래스의 클래스명만 반환합니다.

```
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
<!-- #### `e()` -->
#### `e()`

<!-- The `e` function runs PHP's `htmlspecialchars` function with the `double_encode` option set to `true` by default: -->
`e` 함수는 PHP의 `htmlspecialchars` 함수를 실행하며, 기본적으로 `double_encode` 옵션이 `true`로 설정되어 있습니다.

```
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
<!-- #### `preg_replace_array()` -->
#### `preg_replace_array()`

<!-- The `preg_replace_array` function replaces a given pattern in the string sequentially using an array: -->
`preg_replace_array` 함수는 문자열 내의 지정된 패턴을 배열의 값으로 순차적으로 치환합니다.

```
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
<!-- #### `Str::after()` -->
#### `Str::after()`

<!-- The `Str::after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::after` 메서드는 지정한 문자열 뒤에 나오는 모든 값을 반환합니다. 만약 지정한 값이 문자열 내에 없으면 전체 문자열이 반환됩니다.

```
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
<!-- #### `Str::afterLast()` -->
#### `Str::afterLast()`

<!-- The `Str::afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::afterLast` 메서드는 문자열 내에서 지정한 값의 마지막 등장 이후에 나오는 모든 내용을 반환합니다. 지정한 값이 문자열 내에 없으면 전체 문자열이 반환됩니다.

```
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-ascii"></a>
<!-- #### `Str::ascii()` -->
#### `Str::ascii()`

<!-- The `Str::ascii` method will attempt to transliterate the string into an ASCII value: -->
`Str::ascii` 메서드는 문자열을 ASCII 값으로 변환할 수 있도록 시도합니다.

```
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
<!-- #### `Str::before()` -->
#### `Str::before()`

<!-- The `Str::before` method returns everything before the given value in a string: -->
`Str::before` 메서드는 지정한 값 앞의 모든 내용을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
<!-- #### `Str::beforeLast()` -->
#### `Str::beforeLast()`

<!-- The `Str::beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`Str::beforeLast` 메서드는 문자열 내에서 지정한 값의 마지막 등장 이전까지의 모든 내용을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
<!-- #### `Str::between()` -->
#### `Str::between()`

<!-- The `Str::between` method returns the portion of a string between two values: -->
`Str::between` 메서드는 문자열에서 두 값 사이에 있는 부분 문자열을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
<!-- #### `Str::betweenFirst()` -->
#### `Str::betweenFirst()`

<!-- The `Str::betweenFirst` method returns the smallest possible portion of a string between two values: -->
`Str::betweenFirst` 메서드는 주어진 두 값 사이 중 가장 짧게 추출될 수 있는 부분 문자열을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
<!-- #### `Str::camel()` -->
#### `Str::camel()`

<!-- The `Str::camel` method converts the given string to `camelCase`: -->
`Str::camel` 메서드는 주어진 문자열을 `camelCase` 형식으로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// fooBar
```

<a name="method-str-contains"></a>
<!-- #### `Str::contains()` -->
#### `Str::contains()`

<!-- The `Str::contains` method determines if the given string contains the given value. This method is case sensitive: -->
`Str::contains` 메서드는 주어진 문자열에 특정 값이 포함되어 있는지 확인합니다. 이 메서드는 대소문자를 구분합니다.

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
동일한 방식으로 값의 배열을 전달하여, 주어진 문자열이 배열 내의 값들 중 하나라도 포함하고 있는지 검사할 수 있습니다.

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

<a name="method-str-contains-all"></a>
<!-- #### `Str::containsAll()` -->
#### `Str::containsAll()`

<!-- The `Str::containsAll` method determines if the given string contains all of the values in a given array: -->
`Str::containsAll` 메서드는 주어진 문자열이 배열에 있는 모든 값을 모두 포함하는지 확인합니다.

```
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

<a name="method-ends-with"></a>
<!-- #### `Str::endsWith()` -->
#### `Str::endsWith()`

<!-- The `Str::endsWith` method determines if the given string ends with the given value: -->
`Str::endsWith` 메서드는 주어진 문자열이 특정 값으로 끝나는지 확인합니다.

```
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
동일하게, 값의 배열을 전달하여 문자열이 배열 내 어떤 값으로 끝나는지 확인할 수도 있습니다.

```
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
<!-- #### `Str::excerpt()` -->
#### `Str::excerpt()`

<!-- The `Str::excerpt` method extracts an excerpt from a given string that matches the first instance of a phrase within that string: -->
`Str::excerpt` 메서드는 주어진 문자열에서 특정 구문이 처음으로 일치하는 부분을 기준으로 발췌(excerpt)를 추출합니다.

```
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

<!-- The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string. -->
`radius` 옵션은 기본값이 `100`이며, 발췌 문자열의 앞뒤에 표시할 문자 개수를 지정할 수 있습니다.

<!-- In addition, you may use the `omission` option to define the string that will be prepended and appended to the truncated string: -->
또한, `omission` 옵션을 사용해 생략 부호 등 발췌 문자열 앞뒤에 어떤 문자열을 붙일 것인지 정할 수 있습니다.

```
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-str-finish"></a>
<!-- #### `Str::finish()` -->
#### `Str::finish()`

<!-- The `Str::finish` method adds a single instance of the given value to a string if it does not already end with that value: -->
`Str::finish` 메서드는 주어진 문자열이 지정된 값으로 끝나지 않을 경우, 그 값을 한 번만 덧붙여줍니다.

```
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-headline"></a>
<!-- #### `Str::headline()` -->
#### `Str::headline()`

<!-- The `Str::headline` method will convert strings delimited by casing, hyphens, or underscores into a space delimited string with each word's first letter capitalized: -->
`Str::headline` 메서드는 대소문자 구분, 하이픈, 밑줄 등으로 구분되어 있는 문자열을 띄어쓰기로 구분된 문자열로 바꾸고, 각 단어의 첫 글자를 대문자로 변환합니다.

```
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-inline-markdown"></a>
<!-- #### `Str::inlineMarkdown()` -->
#### `Str::inlineMarkdown()`

<!-- The `Str::inlineMarkdown` method converts GitHub flavored Markdown into inline HTML using [CommonMark](https://commonmark.thephpleague.com/). However, unlike the `markdown` method, it does not wrap all generated HTML in a block-level element: -->
`Str::inlineMarkdown` 메서드는 [CommonMark](https://commonmark.thephpleague.com/)를 사용하여 GitHub 스타일의 마크다운을 인라인 HTML로 변환합니다. 단, `markdown` 메서드와 달리 모든 HTML을 블록 레벨 요소로 감싸지 않습니다.

```
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

<a name="method-str-is"></a>
<!-- #### `Str::is()` -->
#### `Str::is()`

<!-- The `Str::is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values: -->
`Str::is` 메서드는 주어진 문자열이 지정한 패턴과 일치하는지 확인합니다. 애스터리스크(asterisk)를 와일드카드 값으로 사용할 수 있습니다.

```
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

<a name="method-str-is-ascii"></a>
<!-- #### `Str::isAscii()` -->
#### `Str::isAscii()`

<!-- The `Str::isAscii` method determines if a given string is 7 bit ASCII: -->
`Str::isAscii` 메서드는 주어진 문자열이 7비트 ASCII인지 확인합니다.

```
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
<!-- #### `Str::isJson()` -->
#### `Str::isJson()`

<!-- The `Str::isJson` method determines if the given string is valid JSON: -->
`Str::isJson` 메서드는 문자열이 올바른 JSON 형식인지 검사합니다.

```
use Illuminate\Support\Str;

$result = Str::isJson('[1,2,3]');

// true

$result = Str::isJson('{"first": "John", "last": "Doe"}');

// true

$result = Str::isJson('{first: "John", last: "Doe"}');

// false
```

<a name="method-str-is-ulid"></a>
<!-- #### `Str::isUlid()` -->
#### `Str::isUlid()`

<!-- The `Str::isUlid` method determines if the given string is a valid ULID: -->
`Str::isUlid` 메서드는 문자열이 올바른 ULID 형식인지 확인합니다.

```
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>

<!-- #### `Str::isUuid()` -->
#### `Str::isUuid()`

<!-- The `Str::isUuid` method determines if the given string is a valid UUID: -->
`Str::isUuid` 메서드는 주어진 문자열이 유효한 UUID인지 확인합니다.

```
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

<a name="method-kebab-case"></a>
<!-- #### `Str::kebab()` -->
#### `Str::kebab()`

<!-- The `Str::kebab` method converts the given string to `kebab-case`: -->
`Str::kebab` 메서드는 주어진 문자열을 `kebab-case`로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
<!-- #### `Str::lcfirst()` -->
#### `Str::lcfirst()`

<!-- The `Str::lcfirst` method returns the given string with the first character lowercased: -->
`Str::lcfirst` 메서드는 주어진 문자열에서 첫 번째 문자를 소문자로 변환해서 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
<!-- #### `Str::length()` -->
#### `Str::length()`

<!-- The `Str::length` method returns the length of the given string: -->
`Str::length` 메서드는 주어진 문자열의 길이를 반환합니다.

```
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
<!-- #### `Str::limit()` -->
#### `Str::limit()`

<!-- The `Str::limit` method truncates the given string to the specified length: -->
`Str::limit` 메서드는 주어진 문자열을 지정한 길이만큼 잘라줍니다.

```
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

<!-- You may pass a third argument to the method to change the string that will be appended to the end of the truncated string: -->
이 메서드의 세 번째 인수로, 잘린 문자열 끝에 붙일 문자열을 지정할 수도 있습니다.

```
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

<a name="method-str-lower"></a>
<!-- #### `Str::lower()` -->
#### `Str::lower()`

<!-- The `Str::lower` method converts the given string to lowercase: -->
`Str::lower` 메서드는 주어진 문자열을 모두 소문자로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
<!-- #### `Str::markdown()` -->
#### `Str::markdown()`

<!-- The `Str::markdown` method converts GitHub flavored Markdown into HTML using [CommonMark](https://commonmark.thephpleague.com/): -->
`Str::markdown` 메서드는 GitHub 스타일의 Markdown을 [CommonMark](https://commonmark.thephpleague.com/)을 사용해 HTML로 변환합니다.

```
use Illuminate\Support\Str;

$html = Str::markdown('# Laravel');

// <h1>Laravel</h1>

$html = Str::markdown('# Taylor <b>Otwell</b>', [
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

<a name="method-str-mask"></a>
<!-- #### `Str::mask()` -->
#### `Str::mask()`

<!-- The `Str::mask` method masks a portion of a string with a repeated character, and may be used to obfuscate segments of strings such as email addresses and phone numbers: -->
`Str::mask` 메서드는 문자열의 일부분을 지정한 문자를 반복해서 마스킹(감춤 처리)할 수 있으며, 이메일 주소나 전화번호 일부를 숨기는데 사용할 수 있습니다.

```
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

<!-- If needed, you provide a negative number as the third argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
필요하다면, `mask` 메서드의 세 번째 인수에 음수를 전달해 문자열 끝에서부터 일정 거리를 기준으로 마스킹을 시작하도록 할 수도 있습니다.

```
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-ordered-uuid"></a>
<!-- #### `Str::orderedUuid()` -->
#### `Str::orderedUuid()`

<!-- The `Str::orderedUuid` method generates a "timestamp first" UUID that may be efficiently stored in an indexed database column. Each UUID that is generated using this method will be sorted after UUIDs previously generated using the method: -->
`Str::orderedUuid` 메서드는 "타임스탬프가 먼저 오는" UUID를 생성하여 인덱스가 설정된 데이터베이스 컬럼에 효율적으로 저장할 수 있도록 합니다. 이 메서드로 생성된 각 UUID는 이전에 생성된 UUID들 뒤에 정렬되어 저장됩니다.

```
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
<!-- #### `Str::padBoth()` -->
#### `Str::padBoth()`

<!-- The `Str::padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches a desired length: -->
`Str::padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸며, 문자열 양쪽을 지정한 문자열로 채워, 원하는 길이만큼 맞춥니다.

```
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
<!-- #### `Str::padLeft()` -->
#### `Str::padLeft()`

<!-- The `Str::padLeft` method wraps PHP's `str_pad` function, padding the left side of a string with another string until the final string reaches a desired length: -->
`Str::padLeft` 메서드는 PHP의 `str_pad` 함수를 감싸며, 문자열의 왼쪽을 지정한 문자열로 채워, 원하는 길이만큼 맞춥니다.

```
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
<!-- #### `Str::padRight()` -->
#### `Str::padRight()`

<!-- The `Str::padRight` method wraps PHP's `str_pad` function, padding the right side of a string with another string until the final string reaches a desired length: -->
`Str::padRight` 메서드는 PHP의 `str_pad` 함수를 감싸며, 문자열의 오른쪽을 지정한 문자열로 채워, 원하는 길이만큼 맞춥니다.

```
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-plural"></a>
<!-- #### `Str::plural()` -->
#### `Str::plural()`

<!-- The `Str::plural` method converts a singular word string to its plural form. This function supports [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language): -->
`Str::plural` 메서드는 단수형 문자열을 복수형으로 변환합니다. 이 함수는 [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language)를 지원합니다.

```
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
이 함수의 두 번째 인수로 정수를 전달하면, 문자열의 복수 혹은 단수형을 해당 수에 맞추어 반환합니다.

```
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

<a name="method-str-plural-studly"></a>
<!-- #### `Str::pluralStudly()` -->
#### `Str::pluralStudly()`

<!-- The `Str::pluralStudly` method converts a singular word string formatted in studly caps case to its plural form. This function supports [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language): -->
`Str::pluralStudly` 메서드는 StudlyCaps(단어마다 대문자로 구분된 형태)의 단수형 문자열을 복수형으로 변환합니다. 이 함수 역시 [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language)를 지원합니다.

```
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
이 메서드 역시 두 번째 인수로 정수를 전달해 복수 또는 단수형 반환을 제어할 수 있습니다.

```
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-random"></a>
<!-- #### `Str::random()` -->
#### `Str::random()`

<!-- The `Str::random` method generates a random string of the specified length. This function uses PHP's `random_bytes` function: -->
`Str::random` 메서드는 지정한 길이만큼의 임의의 문자열을 생성합니다. 이 함수는 PHP의 `random_bytes`를 사용합니다.

```
use Illuminate\Support\Str;

$random = Str::random(40);
```

<a name="method-str-remove"></a>
<!-- #### `Str::remove()` -->
#### `Str::remove()`

<!-- The `Str::remove` method removes the given value or array of values from the string: -->
`Str::remove` 메서드는 주어진 값(또는 값의 배열)을 문자열에서 제거합니다.

```
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

<!-- You may also pass `false` as a third argument to the `remove` method to ignore case when removing strings. -->
문자열을 제거할 때 대소문자를 구분하지 않게 하려면, `remove` 메서드의 세 번째 인수로 `false`를 전달할 수 있습니다.

<a name="method-str-replace"></a>
<!-- #### `Str::replace()` -->
#### `Str::replace()`

<!-- The `Str::replace` method replaces a given string within the string: -->
`Str::replace` 메서드는 문자열 내의 지정한 값을 새 값으로 교체합니다.

```
use Illuminate\Support\Str;

$string = 'Laravel 8.x';

$replaced = Str::replace('8.x', '9.x', $string);

// Laravel 9.x
```

<a name="method-str-replace-array"></a>
<!-- #### `Str::replaceArray()` -->
#### `Str::replaceArray()`

<!-- The `Str::replaceArray` method replaces a given value in the string sequentially using an array: -->
`Str::replaceArray` 메서드는 문자열 내의 특정 값을, 배열에 담아서 순차적으로 바꿉니다.

```
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
<!-- #### `Str::replaceFirst()` -->
#### `Str::replaceFirst()`

<!-- The `Str::replaceFirst` method replaces the first occurrence of a given value in a string: -->
`Str::replaceFirst` 메서드는 주어진 문자열에서, 첫 번째로 등장하는 값을 새 값으로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
<!-- #### `Str::replaceLast()` -->
#### `Str::replaceLast()`

<!-- The `Str::replaceLast` method replaces the last occurrence of a given value in a string: -->
`Str::replaceLast` 메서드는 주어진 문자열에서, 마지막으로 등장하는 값을 새 값으로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-reverse"></a>
<!-- #### `Str::reverse()` -->
#### `Str::reverse()`

<!-- The `Str::reverse` method reverses the given string: -->
`Str::reverse` 메서드는 주어진 문자열을 거꾸로 뒤집어 반환합니다.

```
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
<!-- #### `Str::singular()` -->
#### `Str::singular()`

<!-- The `Str::singular` method converts a string to its singular form. This function supports [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language): -->
`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. 이 함수도 [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language)를 지원합니다.

```
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
<!-- #### `Str::slug()` -->
#### `Str::slug()`

<!-- The `Str::slug` method generates a URL friendly "slug" from the given string: -->
`Str::slug` 메서드는 주어진 문자열을 URL에 적합한 "슬러그"로 변환합니다.

```
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
<!-- #### `Str::snake()` -->
#### `Str::snake()`

<!-- The `Str::snake` method converts the given string to `snake_case`: -->
`Str::snake` 메서드는 주어진 문자열을 `snake_case` 형태로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
<!-- #### `Str::squish()` -->
#### `Str::squish()`

<!-- The `Str::squish` method removes all extraneous white space from a string, including extraneous white space between words: -->
`Str::squish` 메서드는 문자열 내의 불필요한 공백을 모두 제거하고, 단어 사이의 공백도 1칸으로 줄여줍니다.

```
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
<!-- #### `Str::start()` -->
#### `Str::start()`

<!-- The `Str::start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`Str::start` 메서드는 주어진 값으로 시작하지 않을 경우, 해당 값을 문자열의 맨 앞에 한 번만 추가합니다.

```
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
<!-- #### `Str::startsWith()` -->
#### `Str::startsWith()`

<!-- The `Str::startsWith` method determines if the given string begins with the given value: -->
`Str::startsWith` 메서드는 주어진 문자열이 특정 값으로 시작하는지 여부를 확인합니다.

```
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

<!-- If an array of possible values is passed, the `startsWith` method will return `true` if the string begins with any of the given values: -->
가능한 값들의 배열을 전달하면, `startsWith` 메서드는 전달된 값 중 어느 하나라도 문자열의 시작에 있을 때 `true`를 반환합니다.

```
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
<!-- #### `Str::studly()` -->
#### `Str::studly()`

<!-- The `Str::studly` method converts the given string to `StudlyCase`: -->
`Str::studly` 메서드는 주어진 문자열을 `StudlyCase`로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
<!-- #### `Str::substr()` -->
#### `Str::substr()`

<!-- The `Str::substr` method returns the portion of string specified by the start and length parameters: -->
`Str::substr` 메서드는 지정한 시작 인덱스와 길이만큼, 주어진 문자열의 일부를 반환합니다.

```
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
<!-- #### `Str::substrCount()` -->
#### `Str::substrCount()`

<!-- The `Str::substrCount` method returns the number of occurrences of a given value in the given string: -->
`Str::substrCount` 메서드는 주어진 문자열 내에서 특정 값이 몇 번 나타나는지 반환합니다.

```
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
<!-- #### `Str::substrReplace()` -->
#### `Str::substrReplace()`

<!-- The `Str::substrReplace` method replaces text within a portion of a string, starting at the position specified by the third argument and replacing the number of characters specified by the fourth argument. Passing `0` to the method's fourth argument will insert the string at the specified position without replacing any of the existing characters in the string: -->
`Str::substrReplace` 메서드는 문자열의 일부 구간에, 선택한 텍스트로 교체해줍니다. 세 번째 인수로는 시작 위치를, 네 번째 인수로는 교체할 문자 수를 지정합니다. 네 번째 인수에 `0`을 전달하면, 기존 문자를 지우지 않고 해당 위치에 새로운 문자열을 삽입합니다.

```
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
<!-- #### `Str::swap()` -->
#### `Str::swap()`

<!-- The `Str::swap` method replaces multiple values in the given string using PHP's `strtr` function: -->
`Str::swap` 메서드는 PHP의 `strtr` 함수를 활용하여, 여러 값을 한 번에 치환합니다.

```
use Illuminate\Support\Str;

$string = Str::swap([
    'Tacos' => 'Burritos',
    'great' => 'fantastic',
], 'Tacos are great!');

// Burritos are fantastic!
```

<a name="method-title-case"></a>
<!-- #### `Str::title()` -->
#### `Str::title()`

<!-- The `Str::title` method converts the given string to `Title Case`: -->
`Str::title` 메서드는 주어진 문자열을 `Title Case`(각 단어의 첫 글자가 대문자)로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-html-string"></a>
<!-- #### `Str::toHtmlString()` -->
#### `Str::toHtmlString()`

<!-- The `Str::toHtmlString` method converts the string instance to an instance of `Illuminate\Support\HtmlString`, which may be displayed in Blade templates: -->
`Str::toHtmlString` 메서드는 문자열 인스턴스를 `Illuminate\Support\HtmlString` 타입으로 변환하여, Blade 템플릿에서 출력할 수 있도록 합니다.

```
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-str-ucfirst"></a>
<!-- #### `Str::ucfirst()` -->
#### `Str::ucfirst()`

<!-- The `Str::ucfirst` method returns the given string with the first character capitalized: -->
`Str::ucfirst` 메서드는 주어진 문자열에서 첫 번째 문자를 대문자로 변환해서 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
<!-- #### `Str::ucsplit()` -->
#### `Str::ucsplit()`

<!-- The `Str::ucsplit` method splits the given string into an array by uppercase characters: -->
`Str::ucsplit` 메서드는 문자열을 대문자 기준으로 나누어 배열로 반환합니다.

```
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-upper"></a>

<!-- #### `Str::upper()` -->
#### `Str::upper()`

<!-- The `Str::upper` method converts the given string to uppercase: -->
`Str::upper` 메서드는 전달된 문자열을 모두 대문자로 변환합니다:

```
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
<!-- #### `Str::ulid()` -->
#### `Str::ulid()`

<!-- The `Str::ulid` method generates a ULID: -->
`Str::ulid` 메서드는 ULID를 생성합니다:

```
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

<a name="method-str-uuid"></a>
<!-- #### `Str::uuid()` -->
#### `Str::uuid()`

<!-- The `Str::uuid` method generates a UUID (version 4): -->
`Str::uuid` 메서드는 UUID(버전 4)를 생성합니다:

```
use Illuminate\Support\Str;

return (string) Str::uuid();
```

<a name="method-str-word-count"></a>
<!-- #### `Str::wordCount()` -->
#### `Str::wordCount()`

<!-- The `Str::wordCount` method returns the number of words that a string contains: -->
`Str::wordCount` 메서드는 문자열에 포함된 단어의 개수를 반환합니다:

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-words"></a>
<!-- #### `Str::words()` -->
#### `Str::words()`

<!-- The `Str::words` method limits the number of words in a string. An additional string may be passed to this method via its third argument to specify which string should be appended to the end of the truncated string: -->
`Str::words` 메서드는 문자열의 단어 개수를 제한합니다. 세 번째 인수로 추가 문자열을 전달해, 잘린 문자열의 끝에 어떤 문자열을 붙일지 지정할 수 있습니다:

```
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str"></a>
<!-- #### `str()` -->
#### `str()`

<!-- The `str` function returns a new `Illuminate\Support\Stringable` instance of the given string. This function is equivalent to the `Str::of` method: -->
`str` 함수는 전달된 문자열의 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of` 메서드와 동일합니다:

```
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<!-- If no argument is provided to the `str` function, the function returns an instance of `Illuminate\Support\Str`: -->
만약 `str` 함수에 인수를 제공하지 않으면, `Illuminate\Support\Str`의 인스턴스를 반환합니다:

```
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
<!-- #### `trans()` -->
#### `trans()`

<!-- The `trans` function translates the given translation key using your [localization files](/docs/9.x/localization): -->
`trans` 함수는 [localization files](/docs/9.x/localization)을 사용하여 전달된 번역 키를 번역합니다:

```
echo trans('messages.welcome');
```

<!-- If the specified translation key does not exist, the `trans` function will return the given key. So, using the example above, the `trans` function would return `messages.welcome` if the translation key does not exist. -->
지정한 번역 키가 존재하지 않을 경우, `trans` 함수는 전달된 키 자체를 반환합니다. 따라서 위 예시에서 해당 키가 없다면 `trans` 함수는 `messages.welcome`을 반환합니다.

<a name="method-trans-choice"></a>
<!-- #### `trans_choice()` -->
#### `trans_choice()`

<!-- The `trans_choice` function translates the given translation key with inflection: -->
`trans_choice` 함수는 전달된 번역 키를 복수형 규칙에 맞게 번역합니다:

```
echo trans_choice('messages.notifications', $unreadCount);
```

<!-- If the specified translation key does not exist, the `trans_choice` function will return the given key. So, using the example above, the `trans_choice` function would return `messages.notifications` if the translation key does not exist. -->
지정한 번역 키가 존재하지 않을 경우, `trans_choice` 함수는 전달된 키 자체를 반환합니다. 위 예시에서는 번역 키가 없다면 `trans_choice` 함수가 `messages.notifications`를 반환합니다.

<a name="fluent-strings"></a>
<!-- ## Fluent Strings -->
## Fluent Strings

<!-- Fluent strings provide a more fluent, object-oriented interface for working with string values, allowing you to chain multiple string operations together using a more readable syntax compared to traditional string operations. -->
플루언트 문자열은 문자열 값을 더 유창하고 객체 지향적으로 다룰 수 있는 인터페이스를 제공합니다. 이를 사용하면 여러 문자열 작업을 전통적인 방식보다 가독성 높게 체이닝하여 연결해서 사용할 수 있습니다.

<a name="method-fluent-str-after"></a>
<!-- #### `after` -->
#### `after`

<!-- The `after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`after` 메서드는 문자열에서 지정한 값 다음의 모든 내용을 반환합니다. 만약 지정한 값이 문자열 내에 없다면, 전체 문자열이 반환됩니다:

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
<!-- #### `afterLast` -->
#### `afterLast`

<!-- The `afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`afterLast` 메서드는 문자열에서 지정한 값이 마지막으로 등장한 이후의 모든 내용을 반환합니다. 만약 지정한 값이 없다면, 전체 문자열을 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-append"></a>
<!-- #### `append` -->
#### `append`

<!-- The `append` method appends the given values to the string: -->
`append` 메서드는 전달된 값을 문자열 끝에 덧붙입니다:

```
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
<!-- #### `ascii` -->
#### `ascii`

<!-- The `ascii` method will attempt to transliterate the string into an ASCII value: -->
`ascii` 메서드는 문자열을 ASCII 값으로 변환하려고 시도합니다:

```
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
<!-- #### `basename` -->
#### `basename`

<!-- The `basename` method will return the trailing name component of the given string: -->
`basename` 메서드는 전달된 문자열의 마지막에 위치한 이름만 반환합니다:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

<!-- If needed, you may provide an "extension" that will be removed from the trailing component: -->
필요하다면, 파일 확장자를 지정하여 마지막 이름에서 확장자를 제거할 수도 있습니다:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
<!-- #### `before` -->
#### `before`

<!-- The `before` method returns everything before the given value in a string: -->
`before` 메서드는 문자열에서 지정한 값 앞까지의 모든 내용을 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
<!-- #### `beforeLast` -->
#### `beforeLast`

<!-- The `beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`beforeLast` 메서드는 지정한 값이 마지막으로 등장하기 전까지의 모든 내용을 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
<!-- #### `between` -->
#### `between`

<!-- The `between` method returns the portion of a string between two values: -->
`between` 메서드는 두 값 사이에 위치한 문자열의 일부를 반환합니다:

```
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
<!-- #### `betweenFirst` -->
#### `betweenFirst`

<!-- The `betweenFirst` method returns the smallest possible portion of a string between two values: -->
`betweenFirst` 메서드는 두 값 사이의 최소 구간에 해당하는 문자열의 일부를 반환합니다:

```
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
<!-- #### `camel` -->
#### `camel`

<!-- The `camel` method converts the given string to `camelCase`: -->
`camel` 메서드는 전달된 문자열을 `camelCase`로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// fooBar
```

<a name="method-fluent-str-class-basename"></a>
<!-- #### `classBasename` -->
#### `classBasename`

<!-- The `classBasename` method returns the class name of the given class with the class's namespace removed: -->
`classBasename` 메서드는 전달된 클래스에서 네임스페이스를 제거한 클래스명만 반환합니다:

```
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// Baz
```

<a name="method-fluent-str-contains"></a>
<!-- #### `contains` -->
#### `contains`

<!-- The `contains` method determines if the given string contains the given value. This method is case sensitive: -->
`contains` 메서드는 문자열에 특정 값이 포함되어 있는지 확인합니다. 이 메서드는 대소문자를 구분합니다:

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
여러 값을 배열로 전달하여, 그 중 하나라도 포함되어 있는지 확인할 수도 있습니다:

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

<a name="method-fluent-str-contains-all"></a>
<!-- #### `containsAll` -->
#### `containsAll`

<!-- The `containsAll` method determines if the given string contains all of the values in the given array: -->
`containsAll` 메서드는 지정한 배열에 있는 모든 값이 문자열에 포함되어 있는지 확인합니다:

```
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

<a name="method-fluent-str-dirname"></a>
<!-- #### `dirname` -->
#### `dirname`

<!-- The `dirname` method returns the parent directory portion of the given string: -->
`dirname` 메서드는 전달된 문자열에서 상위 디렉터리 부분을 반환합니다:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

<!-- If necessary, you may specify how many directory levels you wish to trim from the string: -->
필요하다면, 제거할 디렉터리의 레벨 수를 지정할 수도 있습니다:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-excerpt"></a>
<!-- #### `excerpt` -->
#### `excerpt`

<!-- The `excerpt` method extracts an excerpt from the string that matches the first instance of a phrase within that string: -->
`excerpt` 메서드는 문자열에서 처음 등장하는 특정 구문과 그 양쪽 일부분을 포함하는 발췌(Excerpt) 문자열을 추출합니다:

```
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

<!-- The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string. -->
`radius` 옵션은 좌우로 표시될 문자 수를 지정하며, 기본값은 `100`입니다.

<!-- In addition, you may use the `omission` option to change the string that will be prepended and appended to the truncated string: -->
또한, `omission` 옵션을 사용해서 잘린 문자열 앞뒤에 붙는 글자를 변경할 수 있습니다:

```
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-fluent-str-ends-with"></a>
<!-- #### `endsWith` -->
#### `endsWith`

<!-- The `endsWith` method determines if the given string ends with the given value: -->
`endsWith` 메서드는 문자열이 지정한 값으로 끝나는지를 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
여러 값을 배열로 전달하면, 그 중 하나라도 해당 값으로 끝나는지 확인할 수 있습니다:

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith(['name', 'foo']);

// true

$result = Str::of('This is my name')->endsWith(['this', 'foo']);

// false
```

<a name="method-fluent-str-exactly"></a>
<!-- #### `exactly` -->
#### `exactly`

<!-- The `exactly` method determines if the given string is an exact match with another string: -->
`exactly` 메서드는 주어진 문자열이 다른 문자열과 정확하게 일치하는지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-explode"></a>
<!-- #### `explode` -->
#### `explode`

<!-- The `explode` method splits the string by the given delimiter and returns a collection containing each section of the split string: -->
`explode` 메서드는 지정한 구분자로 문자열을 분할해서, 각 부분을 컬렉션에 담아 반환합니다:

```
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
<!-- #### `finish` -->
#### `finish`

<!-- The `finish` method adds a single instance of the given value to a string if it does not already end with that value: -->
`finish` 메서드는, 문자열이 지정한 값으로 끝나지 않는 경우, 해당 값을 한 번만 문자열 끝에 덧붙입니다:

```
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-headline"></a>
<!-- #### `headline` -->
#### `headline`

<!-- The `headline` method will convert strings delimited by casing, hyphens, or underscores into a space delimited string with each word's first letter capitalized: -->
`headline` 메서드는 대소문자, 하이픈, 언더스코어로 구분된 문자열을 단어별 첫 글자가 대문자인 공백 구분 문자열로 변환합니다:

```
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-inline-markdown"></a>
<!-- #### `inlineMarkdown` -->
#### `inlineMarkdown`

<!-- The `inlineMarkdown` method converts GitHub flavored Markdown into inline HTML using [CommonMark](https://commonmark.thephpleague.com/). However, unlike the `markdown` method, it does not wrap all generated HTML in a block-level element: -->
`inlineMarkdown` 메서드는 GitHub 스타일의 Markdown을 [CommonMark](https://commonmark.thephpleague.com/)를 사용하여 인라인 HTML로 변환합니다. 단, `markdown` 메서드와 달리 생성된 모든 HTML을 블록 레벨 요소로 감싸지 않습니다:

```
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

<a name="method-fluent-str-is"></a>
<!-- #### `is` -->
#### `is`

<!-- The `is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values -->
`is` 메서드는 문자열이 주어진 패턴과 일치하는지 확인합니다. 이때, 별표(*)를 와일드카드로 사용할 수 있습니다

```
use Illuminate\Support\Str;

$matches = Str::of('foobar')->is('foo*');

// true

$matches = Str::of('foobar')->is('baz*');

// false
```

<a name="method-fluent-str-is-ascii"></a>
<!-- #### `isAscii` -->
#### `isAscii`

<!-- The `isAscii` method determines if a given string is an ASCII string: -->
`isAscii` 메서드는 문자열이 ASCII 문자열인지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('Taylor')->isAscii();

// true

$result = Str::of('ü')->isAscii();

// false
```

<a name="method-fluent-str-is-empty"></a>
<!-- #### `isEmpty` -->
#### `isEmpty`

<!-- The `isEmpty` method determines if the given string is empty: -->
`isEmpty` 메서드는 문자열이 비어있는지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isEmpty();

// true

$result = Str::of('Laravel')->trim()->isEmpty();

// false
```

<a name="method-fluent-str-is-not-empty"></a>
<!-- #### `isNotEmpty` -->
#### `isNotEmpty`

<!-- The `isNotEmpty` method determines if the given string is not empty: -->
`isNotEmpty` 메서드는 문자열이 비어있지 않은지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-json"></a>
<!-- #### `isJson` -->
#### `isJson`

<!-- The `isJson` method determines if a given string is valid JSON: -->
`isJson` 메서드는 문자열이 유효한 JSON 형식인지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('[1,2,3]')->isJson();

// true

$result = Str::of('{"first": "John", "last": "Doe"}')->isJson();

// true

$result = Str::of('{first: "John", last: "Doe"}')->isJson();

// false
```

<a name="method-fluent-str-is-ulid"></a>
<!-- #### `isUlid` -->
#### `isUlid`

<!-- The `isUlid` method determines if a given string is a ULID: -->
`isUlid` 메서드는 문자열이 ULID 형식인지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-uuid"></a>
<!-- #### `isUuid` -->
#### `isUuid`

<!-- The `isUuid` method determines if a given string is a UUID: -->
`isUuid` 메서드는 문자열이 UUID 형식인지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

<a name="method-fluent-str-kebab"></a>

<!-- #### `kebab` -->
#### `kebab`

<!-- The `kebab` method converts the given string to `kebab-case`: -->
`kebab` 메서드는 주어진 문자열을 `kebab-case` 형식으로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
<!-- #### `lcfirst` -->
#### `lcfirst`

<!-- The `lcfirst` method returns the given string with the first character lowercased: -->
`lcfirst` 메서드는 주어진 문자열의 첫 글자를 소문자로 바꿔서 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```

<a name="method-fluent-str-length"></a>
<!-- #### `length` -->
#### `length`

<!-- The `length` method returns the length of the given string: -->
`length` 메서드는 주어진 문자열의 길이를 반환합니다.

```
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
<!-- #### `limit` -->
#### `limit`

<!-- The `limit` method truncates the given string to the specified length: -->
`limit` 메서드는 주어진 문자열을 지정한 길이만큼 잘라서 반환합니다.

```
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

<!-- You may also pass a second argument to change the string that will be appended to the end of the truncated string: -->
문자열 마지막에 붙일 문자열을 두 번째 인수로 전달하여 지정할 수도 있습니다.

```
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

<a name="method-fluent-str-lower"></a>
<!-- #### `lower` -->
#### `lower`

<!-- The `lower` method converts the given string to lowercase: -->
`lower` 메서드는 주어진 문자열을 모두 소문자로 변환합니다.

```
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-ltrim"></a>
<!-- #### `ltrim` -->
#### `ltrim`

<!-- The `ltrim` method trims the left side of the string: -->
`ltrim` 메서드는 문자열의 왼쪽 부분(앞쪽)에 있는 공백이나 지정한 문자를 제거합니다.

```
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```

<a name="method-fluent-str-markdown"></a>
<!-- #### `markdown` -->
#### `markdown`

<!-- The `markdown` method converts GitHub flavored Markdown into HTML: -->
`markdown` 메서드는 GitHub 스타일의 마크다운(Markdown)을 HTML로 변환합니다.

```
use Illuminate\Support\Str;

$html = Str::of('# Laravel')->markdown();

// <h1>Laravel</h1>

$html = Str::of('# Taylor <b>Otwell</b>')->markdown([
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

<a name="method-fluent-str-mask"></a>
<!-- #### `mask` -->
#### `mask`

<!-- The `mask` method masks a portion of a string with a repeated character, and may be used to obfuscate segments of strings such as email addresses and phone numbers: -->
`mask` 메서드는 문자열의 일부 구간을 지정한 문자로 덮어서 마스킹(masking)합니다. 이메일 주소나 전화번호 등 민감 정보의 일부를 가릴 때 사용할 수 있습니다.

```
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

<!-- If needed, you may provide negative numbers as the third or fourth argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
필요하다면, `mask` 메서드의 세 번째나 네 번째 인수에 음수를 지정하여 문자열의 끝에서부터 마스킹을 시작하도록 할 수 있습니다.

```
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
<!-- #### `match` -->
#### `match`

<!-- The `match` method will return the portion of a string that matches a given regular expression pattern: -->
`match` 메서드는 주어진 정규식 패턴과 일치하는 문자열의 일부를 반환합니다.

```
use Illuminate\Support\Str;

$result = Str::of('foo bar')->match('/bar/');

// 'bar'

$result = Str::of('foo bar')->match('/foo (.*)/');

// 'bar'
```

<a name="method-fluent-str-match-all"></a>
<!-- #### `matchAll` -->
#### `matchAll`

<!-- The `matchAll` method will return a collection containing the portions of a string that match a given regular expression pattern: -->
`matchAll` 메서드는 주어진 정규식 패턴과 일치하는 모든 부분 문자열을 컬렉션으로 반환합니다.

```
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

<!-- If you specify a matching group within the expression, Laravel will return a collection of that group's matches: -->
정규식에 그룹을 지정하면 그 그룹에 해당하는 부분만 컬렉션으로 반환합니다.

```
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

<!-- If no matches are found, an empty collection will be returned. -->
일치하는 값이 없으면 빈 컬렉션을 반환합니다.

<a name="method-fluent-str-new-line"></a>
<!-- #### `newLine` -->
#### `newLine`

<!-- The `newLine` method appends an "end of line" character to a string: -->
`newLine` 메서드는 문자열 끝에 개행(줄바꿈) 문자를 추가합니다.

```
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
<!-- #### `padBoth` -->
#### `padBoth`

<!-- The `padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches the desired length: -->
`padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸 양쪽(좌우)에서 문자열을 지정한 문자로 채워, 최종 문자열이 원하는 길이가 되도록 만듭니다.

```
use Illuminate\Support\Str;

$padded = Str::of('James')->padBoth(10, '_');

// '__James___'

$padded = Str::of('James')->padBoth(10);

// '  James   '
```

<a name="method-fluent-str-padleft"></a>
<!-- #### `padLeft` -->
#### `padLeft`

<!-- The `padLeft` method wraps PHP's `str_pad` function, padding the left side of a string with another string until the final string reaches the desired length: -->
`padLeft` 메서드는 PHP의 `str_pad` 함수를 감싸 왼쪽(앞쪽)에서 문자열을 지정한 문자로 채워, 최종 문자열이 원하는 길이가 되도록 만듭니다.

```
use Illuminate\Support\Str;

$padded = Str::of('James')->padLeft(10, '-=');

// '-=-=-James'

$padded = Str::of('James')->padLeft(10);

// '     James'
```

<a name="method-fluent-str-padright"></a>
<!-- #### `padRight` -->
#### `padRight`

<!-- The `padRight` method wraps PHP's `str_pad` function, padding the right side of a string with another string until the final string reaches the desired length: -->
`padRight` 메서드는 PHP의 `str_pad` 함수를 감싸 오른쪽(뒷쪽)에서 문자열을 지정한 문자로 채워, 최종 문자열이 원하는 길이가 되도록 만듭니다.

```
use Illuminate\Support\Str;

$padded = Str::of('James')->padRight(10, '-');

// 'James-----'

$padded = Str::of('James')->padRight(10);

// 'James     '
```

<a name="method-fluent-str-pipe"></a>
<!-- #### `pipe` -->
#### `pipe`

<!-- The `pipe` method allows you to transform the string by passing its current value to the given callable: -->
`pipe` 메서드는 현재 문자열 값을 전달하여, 주어진 콜러블(callable)로 변환할 수 있도록 해줍니다.

```
use Illuminate\Support\Str;

$hash = Str::of('Laravel')->pipe('md5')->prepend('Checksum: ');

// 'Checksum: a5c95b86291ea299fcbe64458ed12702'

$closure = Str::of('foo')->pipe(function ($str) {
    return 'bar';
});

// 'bar'
```

<a name="method-fluent-str-plural"></a>
<!-- #### `plural` -->
#### `plural`

<!-- The `plural` method converts a singular word string to its plural form. This function supports [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language): -->
`plural` 메서드는 단수 형태의 단어를 복수형으로 변환합니다. 이 함수는 [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language)를 지원합니다.

```
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
문자열의 복수형 또는 단수형을 결정하기 위해 두 번째 인수로 정수를 지정할 수 있습니다.

```
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

<a name="method-fluent-str-prepend"></a>
<!-- #### `prepend` -->
#### `prepend`

<!-- The `prepend` method prepends the given values onto the string: -->
`prepend` 메서드는 주어진 값들을 문자열 앞에 추가합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
<!-- #### `remove` -->
#### `remove`

<!-- The `remove` method removes the given value or array of values from the string: -->
`remove` 메서드는 주어진 값 또는 값들의 배열을 문자열에서 제거합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite');

// Arkansas is beautiful!
```

<!-- You may also pass `false` as a second parameter to ignore case when removing strings. -->
문자열을 제거할 때 대소문자를 무시하고 싶다면 두 번째 인수로 `false`를 전달할 수 있습니다.

<a name="method-fluent-str-replace"></a>
<!-- #### `replace` -->
#### `replace`

<!-- The `replace` method replaces a given string within the string: -->
`replace` 메서드는 문자열 내의 지정한 값을 다른 값으로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

<a name="method-fluent-str-replace-array"></a>
<!-- #### `replaceArray` -->
#### `replaceArray`

<!-- The `replaceArray` method replaces a given value in the string sequentially using an array: -->
`replaceArray` 메서드는 문자열 내에서 지정한 값을 배열 순서대로 하나씩 교체합니다.

```
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
<!-- #### `replaceFirst` -->
#### `replaceFirst`

<!-- The `replaceFirst` method replaces the first occurrence of a given value in a string: -->
`replaceFirst` 메서드는 문자열 내에서 지정한 값이 처음으로 나타나는 부분만 다른 값으로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
<!-- #### `replaceLast` -->
#### `replaceLast`

<!-- The `replaceLast` method replaces the last occurrence of a given value in a string: -->
`replaceLast` 메서드는 문자열 내에서 지정한 값이 마지막으로 나타나는 부분만 다른 값으로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
<!-- #### `replaceMatches` -->
#### `replaceMatches`

<!-- The `replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string: -->
`replaceMatches` 메서드는 지정한 패턴에 일치하는 모든 부분을 주어진 문자열로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

<!-- The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value: -->
`replaceMatches` 메서드는 클로저를 전달하여 패턴과 일치하는 각 부분에 대해 교체 로직을 직접 작성할 수도 있습니다. 이때 클로저에서 원하는 값으로 반환할 수 있습니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function ($match) {
    return '['.$match[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-rtrim"></a>
<!-- #### `rtrim` -->
#### `rtrim`

<!-- The `rtrim` method trims the right side of the given string: -->
`rtrim` 메서드는 주어진 문자열의 오른쪽(뒤쪽) 공백 또는 지정된 문자를 잘라냅니다.

```
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-scan"></a>
<!-- #### `scan` -->
#### `scan`

<!-- The `scan` method parses input from a string into a collection according to a format supported by the [`sscanf` PHP function](https://www.php.net/manual/en/function.sscanf.php): -->
`scan` 메서드는 [`sscanf` PHP function](https://www.php.net/manual/en/function.sscanf.php)에서 지원하는 형식에 따라 문자열을 파싱하여 컬렉션으로 반환합니다.

```
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
<!-- #### `singular` -->
#### `singular`

<!-- The `singular` method converts a string to its singular form. This function supports [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language): -->
`singular` 메서드는 문자열을 단수형으로 변환합니다. 이 함수는 [any of the languages support by Laravel's pluralizer](/docs/9.x/localization#pluralization-language)를 지원합니다.

```
use Illuminate\Support\Str;

$singular = Str::of('cars')->singular();

// car

$singular = Str::of('children')->singular();

// child
```

<a name="method-fluent-str-slug"></a>
<!-- #### `slug` -->
#### `slug`

<!-- The `slug` method generates a URL friendly "slug" from the given string: -->
`slug` 메서드는 주어진 문자열을 URL에 사용할 수 있는 슬러그(slug) 형태로 변환합니다.

```
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
<!-- #### `snake` -->
#### `snake`

<!-- The `snake` method converts the given string to `snake_case`: -->
`snake` 메서드는 주어진 문자열을 `snake_case` 형식으로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
<!-- #### `split` -->
#### `split`

<!-- The `split` method splits a string into a collection using a regular expression: -->
`split` 메서드는 정규 표현식을 사용해 문자열을 컬렉션으로 분할합니다.

```
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
<!-- #### `squish` -->
#### `squish`

<!-- The `squish` method removes all extraneous white space from a string, including extraneous white space between words: -->
`squish` 메서드는 문자열에서 불필요한 모든 공백을 제거하며, 단어 사이에 여분의 공백도 깔끔하게 하나로 정리합니다.

```
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
<!-- #### `start` -->
#### `start`

<!-- The `start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`start` 메서드는 문자열이 이미 지정한 값으로 시작하지 않으면, 그 값을 한 번만 앞에 붙여 반환합니다.

```
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->start('/');

// /this/string

$adjusted = Str::of('/this/string')->start('/');

// /this/string
```

<a name="method-fluent-str-starts-with"></a>
<!-- #### `startsWith` -->
#### `startsWith`

<!-- The `startsWith` method determines if the given string begins with the given value: -->
`startsWith` 메서드는 주어진 문자열이 지정한 값으로 시작하는지 여부를 반환합니다.

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

<a name="method-fluent-str-studly"></a>
<!-- #### `studly` -->
#### `studly`

<!-- The `studly` method converts the given string to `StudlyCase`: -->
`studly` 메서드는 주어진 문자열을 `StudlyCase`(단어별 첫 글자 대문자) 형식으로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
<!-- #### `substr` -->
#### `substr`

<!-- The `substr` method returns the portion of the string specified by the given start and length parameters: -->
`substr` 메서드는 주어진 시작 위치와 길이 파라미터로 지정한 부분 문자열을 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Laravel Framework')->substr(8);

// Framework

$string = Str::of('Laravel Framework')->substr(8, 5);

// Frame
```

<a name="method-fluent-str-substrreplace"></a>

<!-- #### `substrReplace` -->
#### `substrReplace`

<!-- The `substrReplace` method replaces text within a portion of a string, starting at the position specified by the second argument and replacing the number of characters specified by the third argument. Passing `0` to the method's third argument will insert the string at the specified position without replacing any of the existing characters in the string: -->
`substrReplace` 메서드는 문자열의 일부를 지정된 위치(두 번째 인자)에서 시작해서, 세 번째 인자로 지정된 문자 수만큼의 텍스트를 대체합니다. 세 번째 인자에 `0`을 전달하면, 기존 문자열의 문자를 삭제하지 않고 지정된 위치에 문자열을 삽입합니다.

```
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-swap"></a>
<!-- #### `swap` -->
#### `swap`

<!-- The `swap` method replaces multiple values in the string using PHP's `strtr` function: -->
`swap` 메서드는 PHP의 `strtr` 함수를 사용하여 문자열 내에서 여러 값을 한 번에 치환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Tacos are great!')
    ->swap([
        'Tacos' => 'Burritos',
        'great' => 'fantastic',
    ]);

// Burritos are fantastic!
```

<a name="method-fluent-str-tap"></a>
<!-- #### `tap` -->
#### `tap`

<!-- The `tap` method passes the string to the given closure, allowing you to examine and interact with the string while not affecting the string itself. The original string is returned by the `tap` method regardless of what is returned by the closure: -->
`tap` 메서드는 현재 문자열 인스턴스를 지정한 클로저로 전달하여, 문자열을 직접 변경하지 않고 문자열을 살펴보거나 처리할 수 있게 해줍니다. 클로저에서 어떤 값을 반환하더라도, 원래의 문자열 인스턴스가 `tap` 메서드의 반환값으로 사용됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('Laravel')
    ->append(' Framework')
    ->tap(function ($string) {
        dump('String after append: '.$string);
    })
    ->upper();

// LARAVEL FRAMEWORK
```

<a name="method-fluent-str-test"></a>
<!-- #### `test` -->
#### `test`

<!-- The `test` method determines if a string matches the given regular expression pattern: -->
`test` 메서드는 주어진 정규 표현식 패턴과 문자열이 일치하는지 확인합니다.

```
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
<!-- #### `title` -->
#### `title`

<!-- The `title` method converts the given string to `Title Case`: -->
`title` 메서드는 주어진 문자열을 `Title Case`(각 단어의 첫 글자만 대문자)로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-trim"></a>
<!-- #### `trim` -->
#### `trim`

<!-- The `trim` method trims the given string: -->
`trim` 메서드는 문자열 좌우의 공백(또는 지정된 문자)을 제거합니다.

```
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
<!-- #### `ucfirst` -->
#### `ucfirst`

<!-- The `ucfirst` method returns the given string with the first character capitalized: -->
`ucfirst` 메서드는 문자열의 첫 번째 문자만 대문자로 변환하여 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
<!-- #### `ucsplit` -->
#### `ucsplit`

<!-- The `ucsplit` method splits the given string into a collection by uppercase characters: -->
`ucsplit` 메서드는 문자열을 대문자 기준으로 쪼개어 컬렉션으로 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo', 'Bar'])
```

<a name="method-fluent-str-upper"></a>
<!-- #### `upper` -->
#### `upper`

<!-- The `upper` method converts the given string to uppercase: -->
`upper` 메서드는 주어진 문자열을 모두 대문자로 변환합니다.

```
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
<!-- #### `when` -->
#### `when`

<!-- The `when` method invokes the given closure if a given condition is `true`. The closure will receive the fluent string instance: -->
`when` 메서드는 주어진 조건이 `true`일 때 지정한 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('Taylor')
                ->when(true, function ($string) {
                    return $string->append(' Otwell');
                });

// 'Taylor Otwell'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the condition parameter evaluates to `false`. -->
필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 조건이 `false`일 때 실행됩니다.

<a name="method-fluent-str-when-contains"></a>
<!-- #### `whenContains` -->
#### `whenContains`

<!-- The `whenContains` method invokes the given closure if the string contains the given value. The closure will receive the fluent string instance: -->
`whenContains` 메서드는 문자열에 지정된 값이 포함되어 있을 때, 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('tony stark')
            ->whenContains('tony', function ($string) {
                return $string->title();
            });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the string does not contain the given value. -->
필요하다면 `when` 메서드처럼 세 번째 인자로 또 다른 클로저를 전달할 수 있으며, 문자열에 지정한 값이 포함되어 있지 않을 때 이 클로저가 실행됩니다.

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
또한 배열을 사용해 여러 값을 전달할 수 있으며, 배열 내 값들 중 하나라도 포함되어 있으면 클로저가 실행됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('tony stark')
            ->whenContains(['tony', 'hulk'], function ($string) {
                return $string->title();
            });

// Tony Stark
```

<a name="method-fluent-str-when-contains-all"></a>
<!-- #### `whenContainsAll` -->
#### `whenContainsAll`

<!-- The `whenContainsAll` method invokes the given closure if the string contains all of the given sub-strings. The closure will receive the fluent string instance: -->
`whenContainsAll` 메서드는 문자열이 지정한 모든 부분 문자열을 포함하고 있을 때, 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('tony stark')
                ->whenContainsAll(['tony', 'stark'], function ($string) {
                    return $string->title();
                });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the condition parameter evaluates to `false`. -->
필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있으며, 이 클로저는 조건이 `false`일 때 실행됩니다.

<a name="method-fluent-str-when-empty"></a>
<!-- #### `whenEmpty` -->
#### `whenEmpty`

<!-- The `whenEmpty` method invokes the given closure if the string is empty. If the closure returns a value, that value will also be returned by the `whenEmpty` method. If the closure does not return a value, the fluent string instance will be returned: -->
`whenEmpty` 메서드는 문자열이 비어 있을 때 지정된 클로저를 실행합니다. 클로저에서 값을 반환하면, 해당 값이 `whenEmpty` 메서드의 결과로 반환됩니다. 클로저에서 값을 반환하지 않을 경우, 원래의 Fluent String 인스턴스가 반환됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('  ')->whenEmpty(function ($string) {
    return $string->trim()->prepend('Laravel');
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-empty"></a>
<!-- #### `whenNotEmpty` -->
#### `whenNotEmpty`

<!-- The `whenNotEmpty` method invokes the given closure if the string is not empty. If the closure returns a value, that value will also be returned by the `whenNotEmpty` method. If the closure does not return a value, the fluent string instance will be returned: -->
`whenNotEmpty` 메서드는 문자열이 비어 있지 않을 때 지정된 클로저를 실행합니다. 클로저에서 값을 반환하면 그 값이 `whenNotEmpty` 메서드의 반환값이 되고, 값을 반환하지 않으면 Fluent String 인스턴스가 반환됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('Framework')->whenNotEmpty(function ($string) {
    return $string->prepend('Laravel ');
});

// 'Laravel Framework'
```

<a name="method-fluent-str-when-starts-with"></a>
<!-- #### `whenStartsWith` -->
#### `whenStartsWith`

<!-- The `whenStartsWith` method invokes the given closure if the string starts with the given sub-string. The closure will receive the fluent string instance: -->
`whenStartsWith` 메서드는 문자열이 지정한 부분 문자열로 시작할 때, 해당 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('disney world')->whenStartsWith('disney', function ($string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-ends-with"></a>
<!-- #### `whenEndsWith` -->
#### `whenEndsWith`

<!-- The `whenEndsWith` method invokes the given closure if the string ends with the given sub-string. The closure will receive the fluent string instance: -->
`whenEndsWith` 메서드는 문자열이 지정한 부분 문자열로 끝나는 경우, 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('disney world')->whenEndsWith('world', function ($string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-exactly"></a>
<!-- #### `whenExactly` -->
#### `whenExactly`

<!-- The `whenExactly` method invokes the given closure if the string exactly matches the given string. The closure will receive the fluent string instance: -->
`whenExactly` 메서드는 문자열이 지정한 문자열과 정확히 일치할 때, 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('laravel')->whenExactly('laravel', function ($string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-exactly"></a>
<!-- #### `whenNotExactly` -->
#### `whenNotExactly`

<!-- The `whenNotExactly` method invokes the given closure if the string does not exactly match the given string. The closure will receive the fluent string instance: -->
`whenNotExactly` 메서드는 문자열이 지정한 문자열과 정확히 일치하지 않을 때, 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('framework')->whenNotExactly('laravel', function ($string) {
    return $string->title();
});

// 'Framework'
```

<a name="method-fluent-str-when-is"></a>
<!-- #### `whenIs` -->
#### `whenIs`

<!-- The `whenIs` method invokes the given closure if the string matches a given pattern. Asterisks may be used as wildcard values. The closure will receive the fluent string instance: -->
`whenIs` 메서드는 문자열이 주어진 패턴과 일치할 때(별표(*)를 와일드카드로 사용 가능), 해당 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('foo/bar')->whenIs('foo/*', function ($string) {
    return $string->append('/baz');
});

// 'foo/bar/baz'
```

<a name="method-fluent-str-when-is-ascii"></a>
<!-- #### `whenIsAscii` -->
#### `whenIsAscii`

<!-- The `whenIsAscii` method invokes the given closure if the string is 7 bit ASCII. The closure will receive the fluent string instance: -->
`whenIsAscii` 메서드는 문자열이 7비트 ASCII 문자로만 이루어져 있을 때, 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('laravel')->whenIsAscii(function ($string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is-ulid"></a>
<!-- #### `whenIsUlid` -->
#### `whenIsUlid`

<!-- The `whenIsUlid` method invokes the given closure if the string is a valid ULID. The closure will receive the fluent string instance: -->
`whenIsUlid` 메서드는 문자열이 유효한 ULID인지 확인하여, 맞을 때 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function ($string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
<!-- #### `whenIsUuid` -->
#### `whenIsUuid`

<!-- The `whenIsUuid` method invokes the given closure if the string is a valid UUID. The closure will receive the fluent string instance: -->
`whenIsUuid` 메서드는 문자열이 유효한 UUID인지 확인하여, 맞을 때 주어진 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function ($string) {
    return $string->substr(0, 8);
});

// 'a0a2a2d2'
```

<a name="method-fluent-str-when-test"></a>
<!-- #### `whenTest` -->
#### `whenTest`

<!-- The `whenTest` method invokes the given closure if the string matches the given regular expression. The closure will receive the fluent string instance: -->
`whenTest` 메서드는 주어진 정규 표현식과 문자열이 일치할 때, 지정한 클로저를 실행합니다. 클로저에는 Fluent String 인스턴스가 전달됩니다.

```
use Illuminate\Support\Str;

$string = Str::of('laravel framework')->whenTest('/laravel/', function ($string) {
    return $string->title();
});

// 'Laravel Framework'
```

<a name="method-fluent-str-word-count"></a>
<!-- #### `wordCount` -->
#### `wordCount`

<!-- The `wordCount` method returns the number of words that a string contains: -->
`wordCount` 메서드는 문자열에 포함된 단어의 개수를 반환합니다.

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
<!-- #### `words` -->
#### `words`

<!-- The `words` method limits the number of words in a string. If necessary, you may specify an additional string that will be appended to the truncated string: -->
`words` 메서드는 문자열의 단어 수를 제한합니다. 필요한 경우, 잘린 부분 뒤에 추가할 문자열을 두 번째 인자로 지정할 수 있습니다.

```
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="urls"></a>
<!-- ## URLs -->
## URLs

<a name="method-action"></a>
<!-- #### `action()` -->
#### `action()`

<!-- The `action` function generates a URL for the given controller action: -->
`action` 함수는 지정한 컨트롤러 액션에 대한 URL을 생성합니다.

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the method accepts route parameters, you may pass them as the second argument to the method: -->
만약 해당 메서드가 라우트 파라미터를 받는다면, 두 번째 인자로 전달할 수 있습니다.

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
<!-- #### `asset()` -->
#### `asset()`

<!-- The `asset` function generates a URL for an asset using the current scheme of the request (HTTP or HTTPS): -->
`asset` 함수는 현재 요청의 스킴(HTTP 또는 HTTPS)에 따라 asset(정적 파일) 경로의 URL을 생성합니다.

```
$url = asset('img/photo.jpg');
```

<!-- You can configure the asset URL host by setting the `ASSET_URL` variable in your `.env` file. This can be useful if you host your assets on an external service like Amazon S3 or another CDN: -->
.asset URL의 호스트는 `.env` 파일의 `ASSET_URL` 변수를 설정하여 변경할 수 있습니다. 이는 Amazon S3나 다른 CDN 등 외부 서비스에서 asset 파일을 제공할 경우 유용하게 사용할 수 있습니다.

```
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
<!-- #### `route()` -->
#### `route()`

<!-- The `route` function generates a URL for a given [named route](/docs/9.x/routing#named-routes): -->
`route` 함수는 [named route](/docs/9.x/routing#named-routes)의 URL을 생성합니다.

```
$url = route('route.name');
```

<!-- If the route accepts parameters, you may pass them as the second argument to the function: -->
해당 라우트가 파라미터를 받는 경우, 두 번째 인자로 파라미터 배열을 전달할 수 있습니다.

```
$url = route('route.name', ['id' => 1]);
```

<!-- By default, the `route` function generates an absolute URL. If you wish to generate a relative URL, you may pass `false` as the third argument to the function: -->
기본적으로, `route` 함수는 절대 URL을 생성합니다. 만약 상대 경로 URL을 만들고 싶다면, 세 번째 인자에 `false`를 전달하면 됩니다.

```
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
<!-- #### `secure_asset()` -->
#### `secure_asset()`

<!-- The `secure_asset` function generates a URL for an asset using HTTPS: -->
`secure_asset` 함수는 HTTPS를 사용하여 asset 파일의 URL을 생성합니다.

```
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
<!-- #### `secure_url()` -->
#### `secure_url()`

<!-- The `secure_url` function generates a fully qualified HTTPS URL to the given path. Additional URL segments may be passed in the function's second argument: -->
`secure_url` 함수는 지정된 경로에 대해 전체 HTTPS URL을 생성합니다. 필요하다면, 두 번째 인자에 추가 URL 세그먼트들을 배열로 넘길 수 있습니다.

```
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
<!-- #### `to_route()` -->
#### `to_route()`

<!-- The `to_route` function generates a [redirect HTTP response](/docs/9.x/responses#redirects) for a given [named route](/docs/9.x/routing#named-routes): -->
`to_route` 함수는 [redirect HTTP response](/docs/9.x/responses#redirects)를 생성해 지정한 [named route](/docs/9.x/routing#named-routes)로 이동하게 합니다.

```
return to_route('users.show', ['user' => 1]);
```

<!-- If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the `to_route` method: -->
필요하다면, 리다이렉트에 사용할 HTTP 상태 코드와 추가 HTTP 응답 헤더를 `to_route` 메서드의 세 번째, 네 번째 인자로 전달할 수 있습니다.

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-url"></a>
<!-- #### `url()` -->
#### `url()`

<!-- The `url` function generates a fully qualified URL to the given path: -->
`url` 함수는 지정한 경로에 대해 전체 URL을 생성합니다.

```
$url = url('user/profile');

$url = url('user/profile', [1]);
```

<!-- If no path is provided, an `Illuminate\Routing\UrlGenerator` instance is returned: -->
만약 경로를 지정하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스를 반환합니다.

```
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

<a name="miscellaneous"></a>
<!-- ## Miscellaneous -->
## Miscellaneous

<a name="method-abort"></a>
<!-- #### `abort()` -->
#### `abort()`

<!-- The `abort` function throws [an HTTP exception](/docs/9.x/errors#http-exceptions) which will be rendered by the [exception handler](/docs/9.x/errors#the-exception-handler): -->
`abort` 함수는 [an HTTP exception](/docs/9.x/errors#http-exceptions)를 발생시켜 [exception handler](/docs/9.x/errors#the-exception-handler)가 해당 예외를 처리하도록 합니다.

```
abort(403);
```

<!-- You may also provide the exception's message and custom HTTP response headers that should be sent to the browser: -->
예외 메시지와 원하는 HTTP 응답 헤더를 추가로 지정할 수도 있습니다.

```
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
<!-- #### `abort_if()` -->
#### `abort_if()`

<!-- The `abort_if` function throws an HTTP exception if a given boolean expression evaluates to `true`: -->
`abort_if` 함수는 주어진 불리언 표현식이 `true`로 평가될 경우 HTTP 예외를 발생시킵니다.

```
abort_if(! Auth::user()->isAdmin(), 403);
```

<!-- Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function. -->
`abort` 함수처럼, 세 번째 인자로 예외 메시지를, 네 번째 인자로 사용자 정의 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-abort-unless"></a>
<!-- #### `abort_unless()` -->
#### `abort_unless()`

<!-- The `abort_unless` function throws an HTTP exception if a given boolean expression evaluates to `false`: -->
`abort_unless` 함수는 주어진 불리언 표현식이 `false`로 평가될 경우 HTTP 예외를 발생시킵니다.

```
abort_unless(Auth::user()->isAdmin(), 403);
```

<!-- Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function. -->
`abort` 함수처럼, 세 번째 인자로 예외 메시지를, 네 번째 인자로 사용자 정의 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-app"></a>
<!-- #### `app()` -->
#### `app()`

<!-- The `app` function returns the [service container](/docs/9.x/container) instance: -->
`app` 함수는 [service container](/docs/9.x/container) 인스턴스를 반환합니다.

```
$container = app();
```

<!-- You may pass a class or interface name to resolve it from the container: -->
클래스나 인터페이스 이름을 전달하면 컨테이너에서 해당 객체를 해결할 수 있습니다.

```
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
<!-- #### `auth()` -->
#### `auth()`

<!-- The `auth` function returns an [authenticator](/docs/9.x/authentication) instance. You may use it as an alternative to the `Auth` facade: -->
`auth` 함수는 [authenticator](/docs/9.x/authentication) 인스턴스를 반환합니다. `Auth` 파사드 대신 사용할 수 있습니다.

```
$user = auth()->user();
```

<!-- If needed, you may specify which guard instance you would like to access: -->
필요하다면, 접근하고 싶은 가드 인스턴스를 지정할 수도 있습니다.

```
$user = auth('admin')->user();
```

<a name="method-back"></a>

<!-- #### `back()` -->
#### `back()`

<!-- The `back` function generates a [redirect HTTP response](/docs/9.x/responses#redirects) to the user's previous location: -->
`back` 함수는 사용자를 [redirect HTTP response](/docs/9.x/responses#redirects)로 리디렉션하는 HTTP 응답을 생성합니다.

```
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
<!-- #### `bcrypt()` -->
#### `bcrypt()`

<!-- The `bcrypt` function [hashes](/docs/9.x/hashing) the given value using Bcrypt. You may use this function as an alternative to the `Hash` facade: -->
`bcrypt` 함수는 주어진 값을 Bcrypt를 사용하여 [hashes](/docs/9.x/hashing)합니다. 이 함수는 `Hash` 파사드의 대체로 사용할 수 있습니다.

```
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
<!-- #### `blank()` -->
#### `blank()`

<!-- The `blank` function determines whether the given value is "blank": -->
`blank` 함수는 전달된 값이 "비어있는(blank)" 값인지 판별합니다.

```
blank('');
blank('   ');
blank(null);
blank(collect());

// true

blank(0);
blank(true);
blank(false);

// false
```

<!-- For the inverse of `blank`, see the [`filled`](#method-filled) method. -->
`blank`의 반대 동작에는 [`filled`](#method-filled) 메서드를 참고하세요.

<a name="method-broadcast"></a>
<!-- #### `broadcast()` -->
#### `broadcast()`

<!-- The `broadcast` function [broadcasts](/docs/9.x/broadcasting) the given [event](/docs/9.x/events) to its listeners: -->
`broadcast` 함수는 [broadcasts](/docs/9.x/broadcasting) 기능을 사용해 주어진 [event](/docs/9.x/events)를 해당 리스너들에게 전달합니다.

```
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
<!-- #### `cache()` -->
#### `cache()`

<!-- The `cache` function may be used to get values from the [cache](/docs/9.x/cache). If the given key does not exist in the cache, an optional default value will be returned: -->
`cache` 함수는 [cache](/docs/9.x/cache)에서 값을 가져오는 데 사용할 수 있습니다. 주어진 키가 캐시에 존재하지 않으면, 선택적으로 기본값(default value)을 반환합니다.

```
$value = cache('key');

$value = cache('key', 'default');
```

<!-- You may add items to the cache by passing an array of key / value pairs to the function. You should also pass the number of seconds or duration the cached value should be considered valid: -->
함수에 키/값 쌍의 배열을 전달하여 캐시에 아이템을 저장할 수 있습니다. 이때, 캐시된 값이 유효하다고 간주할 시간(초 단위 또는 기간)을 함께 전달해야 합니다.

```
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
<!-- #### `class_uses_recursive()` -->
#### `class_uses_recursive()`

<!-- The `class_uses_recursive` function returns all traits used by a class, including traits used by all of its parent classes: -->
`class_uses_recursive` 함수는 해당 클래스 및 해당 클래스의 모든 부모 클래스에서 사용된 모든 trait를 반환합니다.

```
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
<!-- #### `collect()` -->
#### `collect()`

<!-- The `collect` function creates a [collection](/docs/9.x/collections) instance from the given value: -->
`collect` 함수는 전달된 값을 바탕으로 [collection](/docs/9.x/collections) 인스턴스를 생성합니다.

```
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
<!-- #### `config()` -->
#### `config()`

<!-- The `config` function gets the value of a [configuration](/docs/9.x/configuration) variable. The configuration values may be accessed using "dot" syntax, which includes the name of the file and the option you wish to access. A default value may be specified and is returned if the configuration option does not exist: -->
`config` 함수는 [configuration](/docs/9.x/configuration)을 가져옵니다. 설정 값은 '점(dot) 표기법'을 사용해 접근하는데, 이는 파일명과 옵션명을 점으로 이어 붙인 방식입니다. 기본값(default)을 함께 지정할 수 있으며, 설정 옵션이 존재하지 않을 때 반환됩니다.

```
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

<!-- You may set configuration variables at runtime by passing an array of key / value pairs. However, note that this function only affects the configuration value for the current request and does not update your actual configuration values: -->
실행 중에 키/값 쌍의 배열을 전달하여 설정 값을 지정할 수도 있습니다. 단, 이 함수로 변경한 값은 현재 요청에서만 유효하고 실제 설정 파일에는 반영되지 않습니다.

```
config(['app.debug' => true]);
```

<a name="method-cookie"></a>
<!-- #### `cookie()` -->
#### `cookie()`

<!-- The `cookie` function creates a new [cookie](/docs/9.x/requests#cookies) instance: -->
`cookie` 함수는 새로운 [cookie](/docs/9.x/requests#cookies) 인스턴스를 생성합니다.

```
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
<!-- #### `csrf_field()` -->
#### `csrf_field()`

<!-- The `csrf_field` function generates an HTML `hidden` input field containing the value of the CSRF token. For example, using [Blade syntax](/docs/9.x/blade): -->
`csrf_field` 함수는 CSRF 토큰 값을 담고 있는 HTML `hidden` 입력 필드를 생성합니다. 예를 들어, [Blade syntax](/docs/9.x/blade)에서 다음과 같이 사용합니다.

```
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
<!-- #### `csrf_token()` -->
#### `csrf_token()`

<!-- The `csrf_token` function retrieves the value of the current CSRF token: -->
`csrf_token` 함수는 현재 요청의 CSRF 토큰 값을 반환합니다.

```
$token = csrf_token();
```

<a name="method-decrypt"></a>
<!-- #### `decrypt()` -->
#### `decrypt()`

<!-- The `decrypt` function [decrypts](/docs/9.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade: -->
`decrypt` 함수는 주어진 값을 [decrypts](/docs/9.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대체로 사용할 수 있습니다.

```
$password = decrypt($value);
```

<a name="method-dd"></a>
<!-- #### `dd()` -->
#### `dd()`

<!-- The `dd` function dumps the given variables and ends execution of the script: -->
`dd` 함수는 전달된 변수를 출력(dump)하고 스크립트 실행을 종료합니다.

```
dd($value);

dd($value1, $value2, $value3, ...);
```

<!-- If you do not want to halt the execution of your script, use the [`dump`](#method-dump) function instead. -->
스크립트 실행을 중단하고 싶지 않다면 [`dump`](#method-dump) 함수를 대신 사용하세요.

<a name="method-dispatch"></a>
<!-- #### `dispatch()` -->
#### `dispatch()`

<!-- The `dispatch` function pushes the given [job](/docs/9.x/queues#creating-jobs) onto the Laravel [job queue](/docs/9.x/queues): -->
`dispatch` 함수는 주어진 [job](/docs/9.x/queues#creating-jobs)을 Laravel의 [job queue](/docs/9.x/queues)에 넣습니다.

```
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
<!-- #### `dump()` -->
#### `dump()`

<!-- The `dump` function dumps the given variables: -->
`dump` 함수는 전달된 변수를 출력(dump)합니다.

```
dump($value);

dump($value1, $value2, $value3, ...);
```

<!-- If you want to stop executing the script after dumping the variables, use the [`dd`](#method-dd) function instead. -->
변수 출력 후 스크립트 실행을 중단하려면 [`dd`](#method-dd) 함수를 사용하세요.

<a name="method-encrypt"></a>
<!-- #### `encrypt()` -->
#### `encrypt()`

<!-- The `encrypt` function [encrypts](/docs/9.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade: -->
`encrypt` 함수는 주어진 값을 [encrypts](/docs/9.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대체로도 사용할 수 있습니다.

```
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
<!-- #### `env()` -->
#### `env()`

<!-- The `env` function retrieves the value of an [environment variable](/docs/9.x/configuration#environment-configuration) or returns a default value: -->
`env` 함수는 주어진 [environment variable](/docs/9.x/configuration#environment-configuration)의 값을 가져오거나, 지정한 기본값을 반환합니다.

```
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행했다면, `env` 함수는 반드시 구성 파일 내에서만 사용해야 합니다. 구성 정보가 캐시된 이후에는 `.env` 파일이 로드되지 않으며, 모든 `env` 함수 호출은 `null`을 반환하게 됩니다.

<a name="method-event"></a>
<!-- #### `event()` -->
#### `event()`

<!-- The `event` function dispatches the given [event](/docs/9.x/events) to its listeners: -->
`event` 함수는 주어진 [event](/docs/9.x/events)를 해당 리스너들에게 디스패치합니다.

```
event(new UserRegistered($user));
```

<a name="method-fake"></a>
<!-- #### `fake()` -->
#### `fake()`

<!-- The `fake` function resolves a [Faker](https://github.com/FakerPHP/Faker) singleton from the container, which can be useful when creating fake data in model factories, database seeding, tests, and prototyping views: -->
`fake` 함수는 컨테이너에서 [Faker](https://github.com/FakerPHP/Faker) 싱글턴을 resolve(해결)합니다. 이 함수는 모델 팩토리, 데이터베이스 시딩, 테스트, 프로토타입 뷰를 작성할 때 더미 데이터를 생성하는 데 유용합니다.

```blade
@for($i = 0; $i < 10; $i++)
    <dl>
        <dt>Name</dt>
        <dd>{{ fake()->name() }}</dd>

        <dt>Email</dt>
        <dd>{{ fake()->unique()->safeEmail() }}</dd>
    </dl>
@endfor
```

<!-- By default, the `fake` function will utilize the `app.faker_locale` configuration option in your `config/app.php` configuration file; however, you may also specify the locale by passing it to the `fake` function. Each locale will resolve an individual singleton: -->
기본적으로 `fake` 함수는 `config/app.php` 파일의 `app.faker_locale` 설정 값을 사용합니다. 하지만, 필요에 따라 `fake` 함수에 특정 로케일을 전달하여 사용할 수도 있습니다. 서로 다른 로케일마다 별도의 싱글턴 인스턴스가 반환됩니다.

```
fake('nl_NL')->name()
```

<a name="method-filled"></a>
<!-- #### `filled()` -->
#### `filled()`

<!-- The `filled` function determines whether the given value is not "blank": -->
`filled` 함수는 전달된 값이 "비어있지 않은지" 판별합니다.

```
filled(0);
filled(true);
filled(false);

// true

filled('');
filled('   ');
filled(null);
filled(collect());

// false
```

<!-- For the inverse of `filled`, see the [`blank`](#method-blank) method. -->
`filled`의 반대 동작은 [`blank`](#method-blank) 메서드를 참고하세요.

<a name="method-info"></a>
<!-- #### `info()` -->
#### `info()`

<!-- The `info` function will write information to your application's [log](/docs/9.x/logging): -->
`info` 함수는 애플리케이션의 [log](/docs/9.x/logging)에 정보를 기록합니다.

```
info('Some helpful information!');
```

<!-- An array of contextual data may also be passed to the function: -->
이 함수에 추가적인 컨텍스트 데이터 배열을 전달할 수도 있습니다.

```
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-logger"></a>
<!-- #### `logger()` -->
#### `logger()`

<!-- The `logger` function can be used to write a `debug` level message to the [log](/docs/9.x/logging): -->
`logger` 함수는 `debug` 레벨의 메시지를 [log](/docs/9.x/logging)에 쓸 때 사용할 수 있습니다.

```
logger('Debug message');
```

<!-- An array of contextual data may also be passed to the function: -->
컨텍스트 데이터 배열 역시 함께 전달할 수 있습니다.

```
logger('User has logged in.', ['id' => $user->id]);
```

<!-- A [logger](/docs/9.x/errors#logging) instance will be returned if no value is passed to the function: -->
함수에 인수를 전달하지 않으면 [logger](/docs/9.x/errors#logging)가 반환됩니다.

```
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
<!-- #### `method_field()` -->
#### `method_field()`

<!-- The `method_field` function generates an HTML `hidden` input field containing the spoofed value of the form's HTTP verb. For example, using [Blade syntax](/docs/9.x/blade): -->
`method_field` 함수는 폼의 HTTP 메서드 값을 위조한(spoofed) 내용을 담는 HTML `hidden` 입력 필드를 생성합니다. 예를 들어 [Blade syntax](/docs/9.x/blade)에서 아래와 같이 사용할 수 있습니다.

```
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
<!-- #### `now()` -->
#### `now()`

<!-- The `now` function creates a new `Illuminate\Support\Carbon` instance for the current time: -->
`now` 함수는 현재 시점의 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```
$now = now();
```

<a name="method-old"></a>
<!-- #### `old()` -->
#### `old()`

<!-- The `old` function [retrieves](/docs/9.x/requests#retrieving-input) an [old input](/docs/9.x/requests#old-input) value flashed into the session: -->
`old` 함수는 [retrieves](/docs/9.x/requests#retrieving-input) 동작으로 세션에 플래시된 [old input](/docs/9.x/requests#old-input) 값을 가져옵니다.

```
$value = old('value');

$value = old('value', 'default');
```

<!-- Since the "default value" provided as the second argument to the `old` function is often an attribute of an Eloquent model, Laravel allows you to simply pass the entire Eloquent model as the second argument to the `old` function. When doing so, Laravel will assume the first argument provided to the `old` function is the name of the Eloquent attribute that should be considered the "default value": -->
`old` 함수에 두 번째 인수로 Eloquent 모델의 속성이 자주 사용되기 때문에, Laravel에서는 전체 Eloquent 모델을 `old` 함수의 두 번째 인수로 바로 전달할 수 있게 지원합니다. 이 경우, `old` 함수의 첫 번째 인수는 기본값으로 사용할 Eloquent 속성명을 의미합니다.

```
{{ old('name', $user->name) }}

// Is equivalent to...

{{ old('name', $user) }}
```

<a name="method-optional"></a>
<!-- #### `optional()` -->
#### `optional()`

<!-- The `optional` function accepts any argument and allows you to access properties or call methods on that object. If the given object is `null`, properties and methods will return `null` instead of causing an error: -->
`optional` 함수는 어떤 인수든 받아 그 객체의 속성이나 메서드에 접근하게 해줍니다. 만약 전달한 객체가 `null`인 경우, 속성이나 메서드를 호출해도 에러가 발생하지 않고 대신 `null`이 반환됩니다.

```
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

<!-- The `optional` function also accepts a closure as its second argument. The closure will be invoked if the value provided as the first argument is not null: -->
`optional` 함수는 두 번째 인수로 클로저를 받을 수도 있습니다. 첫 번째 인수 값이 null이 아닐 때 클로저가 실행됩니다.

```
return optional(User::find($id), function ($user) {
    return $user->name;
});
```

<a name="method-policy"></a>
<!-- #### `policy()` -->
#### `policy()`

<!-- The `policy` method retrieves a [policy](/docs/9.x/authorization#creating-policies) instance for a given class: -->
`policy` 함수는 주어진 클래스에 대한 [policy](/docs/9.x/authorization#creating-policies) 인스턴스를 반환합니다.

```
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
<!-- #### `redirect()` -->
#### `redirect()`

<!-- The `redirect` function returns a [redirect HTTP response](/docs/9.x/responses#redirects), or returns the redirector instance if called with no arguments: -->
`redirect` 함수는 [redirect HTTP response](/docs/9.x/responses#redirects)을 반환하거나, 인수를 전달하지 않으면 Redirector 인스턴스를 반환합니다.

```
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
<!-- #### `report()` -->
#### `report()`

<!-- The `report` function will report an exception using your [exception handler](/docs/9.x/errors#the-exception-handler): -->
`report` 함수는 [exception handler](/docs/9.x/errors#the-exception-handler)를 사용해 예외를 보고합니다.

```
report($e);
```

<!-- The `report` function also accepts a string as an argument. When a string is given to the function, the function will create an exception with the given string as its message: -->
또한, `report` 함수에 문자열을 전달하면 해당 문자열을 메시지로 가진 예외를 생성해 보고합니다.

```
report('Something went wrong.');
```

<a name="method-report-if"></a>
<!-- #### `report_if()` -->
#### `report_if()`

<!-- The `report_if` function will report an exception using your [exception handler](/docs/9.x/errors#the-exception-handler) if the given condition is `true`: -->
`report_if` 함수는 지정된 조건이 `true`일 때 [exception handler](/docs/9.x/errors#the-exception-handler)를 사용해 예외를 보고합니다.

```
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
<!-- #### `report_unless()` -->
#### `report_unless()`

<!-- The `report_unless` function will report an exception using your [exception handler](/docs/9.x/errors#the-exception-handler) if the given condition is `false`: -->
`report_unless` 함수는 지정된 조건이 `false`일 때 [exception handler](/docs/9.x/errors#the-exception-handler)를 사용해 예외를 보고합니다.

```
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
<!-- #### `request()` -->
#### `request()`

<!-- The `request` function returns the current [request](/docs/9.x/requests) instance or obtains an input field's value from the current request: -->
`request` 함수는 현재 [request](/docs/9.x/requests) 인스턴스를 반환하거나, 현재 요청에서 특정 입력 필드의 값을 가져옵니다.

```
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
<!-- #### `rescue()` -->
#### `rescue()`

<!-- The `rescue` function executes the given closure and catches any exceptions that occur during its execution. All exceptions that are caught will be sent to your [exception handler](/docs/9.x/errors#the-exception-handler); however, the request will continue processing: -->
`rescue` 함수는 주어진 클로저를 실행하면서 발생할 수 있는 모든 예외를 잡아냅니다. 잡힌 모든 예외는 [exception handler](/docs/9.x/errors#the-exception-handler)로 전달되지만, 요청은 계속 처리됩니다.

```
return rescue(function () {
    return $this->method();
});
```

<!-- You may also pass a second argument to the `rescue` function. This argument will be the "default" value that should be returned if an exception occurs while executing the closure: -->
`rescue` 함수에 두 번째 인수를 전달하면, 클로저 실행 중 예외가 발생할 때 반환할 "기본값"이 됩니다.

```
return rescue(function () {
    return $this->method();
}, false);

return rescue(function () {
    return $this->method();
}, function () {
    return $this->failure();
});
```

<a name="method-resolve"></a>
<!-- #### `resolve()` -->
#### `resolve()`

<!-- The `resolve` function resolves a given class or interface name to an instance using the [service container](/docs/9.x/container): -->
`resolve` 함수는 주어진 클래스나 인터페이스 이름을 [service container](/docs/9.x/container)를 통해 인스턴스로 해결합니다.

```
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
<!-- #### `response()` -->
#### `response()`

<!-- The `response` function creates a [response](/docs/9.x/responses) instance or obtains an instance of the response factory: -->
`response` 함수는 [response](/docs/9.x/responses) 인스턴스를 생성하거나, 응답 팩토리 인스턴스를 반환합니다.

```
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
<!-- #### `retry()` -->
#### `retry()`

<!-- The `retry` function attempts to execute the given callback until the given maximum attempt threshold is met. If the callback does not throw an exception, its return value will be returned. If the callback throws an exception, it will automatically be retried. If the maximum attempt count is exceeded, the exception will be thrown: -->
`retry` 함수는 지정된 최대 시도 횟수에 도달할 때까지 콜백을 실행하려 시도합니다. 콜백이 예외를 던지지 않으면 해당 반환값이 반환됩니다. 콜백 실행 중 예외가 발생하면 자동으로 재시도하게 되며, 최대 시도를 초과하면 예외가 다시 던져집니다.

```
return retry(5, function () {
    // Attempt 5 times while resting 100ms between attempts...
}, 100);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the third argument to the `retry` function: -->
시도 사이 대기 시간을 직접 계산하고 싶다면, `retry` 함수의 세 번째 인수로 클로저를 전달할 수 있습니다.

```
return retry(5, function () {
    // ...
}, function ($attempt, $exception) {
    return $attempt * 100;
});
```

<!-- For convenience, you may provide an array as the first argument to the `retry` function. This array will be used to determine how many milliseconds to sleep between subsequent attempts: -->
편의상, `retry` 함수의 첫 번째 인수로 배열을 전달할 수도 있습니다. 이 배열 값이 연속된 시도들 사이의 대기 시간(밀리초 단위)로 사용됩니다.

```
return retry([100, 200], function () {
    // Sleep for 100ms on first retry, 200ms on second retry...
});
```

<!-- To only retry under specific conditions, you may pass a closure as the fourth argument to the `retry` function: -->
특정 조건에서만 재시도하도록 하려면, `retry` 함수의 네 번째 인수로 클로저를 사용할 수 있습니다.

```
return retry(5, function () {
    // ...
}, 100, function ($exception) {
    return $exception instanceof RetryException;
});
```

<a name="method-session"></a>
<!-- #### `session()` -->
#### `session()`

<!-- The `session` function may be used to get or set [session](/docs/9.x/session) values: -->
`session` 함수는 [session](/docs/9.x/session) 값을 가져오거나 설정하는 데 사용할 수 있습니다.

```
$value = session('key');
```

<!-- You may set values by passing an array of key / value pairs to the function: -->
키/값 쌍의 배열을 전달하여 세션 값을 설정할 수도 있습니다.

```
session(['chairs' => 7, 'instruments' => 3]);
```

<!-- The session store will be returned if no value is passed to the function: -->
인수를 전달하지 않으면 세션 스토어 인스턴스가 반환됩니다.

```
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
<!-- #### `tap()` -->
#### `tap()`

<!-- The `tap` function accepts two arguments: an arbitrary `$value` and a closure. The `$value` will be passed to the closure and then be returned by the `tap` function. The return value of the closure is irrelevant: -->
`tap` 함수는 두 개의 인수를 받습니다: 임의의 `$value`와 클로저입니다. 전달한 `$value`가 클로저에 전달된 후 `tap` 함수가 다시 그 값을 반환하며, 이때 클로저의 반환값은 무시됩니다.

```
$user = tap(User::first(), function ($user) {
    $user->name = 'taylor';

    $user->save();
});
```

<!-- If no closure is passed to the `tap` function, you may call any method on the given `$value`. The return value of the method you call will always be `$value`, regardless of what the method actually returns in its definition. For example, the Eloquent `update` method typically returns an integer. However, we can force the method to return the model itself by chaining the `update` method call through the `tap` function: -->
`tap` 함수에 클로저를 전달하지 않으면, `$value`에 대해 어떤 메서드든 호출할 수 있습니다. 이때 해당 메서드의 정의상 반환값과 무관하게 항상 `$value`가 반환됩니다. 예를 들어, Eloquent의 `update` 메서드는 통상적으로 정수를 반환하지만, `update` 메서드 호출을 `tap` 함수를 통해 체이닝하면 모델 인스턴스 그 자체를 반환하도록 만들 수 있습니다.

```
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

<!-- To add a `tap` method to a class, you may add the `Illuminate\Support\Traits\Tappable` trait to the class. The `tap` method of this trait accepts a Closure as its only argument. The object instance itself will be passed to the Closure and then be returned by the `tap` method: -->
클래스에 `tap` 메서드를 추가하고 싶다면, `Illuminate\Support\Traits\Tappable` 트레이트를 클래스에 추가하세요. 이 트레이트의 `tap` 메서드는 클로저 하나만 인수로 받습니다. 오브젝트 인스턴스 자신이 클로저로 전달된 후 `tap` 메서드가 그 인스턴스를 반환합니다.

```
return $user->tap(function ($user) {
    //
});
```

<a name="method-throw-if"></a>
<!-- #### `throw_if()` -->
#### `throw_if()`

<!-- The `throw_if` function throws the given exception if a given boolean expression evaluates to `true`: -->
`throw_if` 함수는 주어진 불리언 조건이 `true`일 때 지정한 예외를 던집니다.

```
throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

throw_if(
    ! Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-throw-unless"></a>

<!-- #### `throw_unless()` -->
#### `throw_unless()`

<!-- The `throw_unless` function throws the given exception if a given boolean expression evaluates to `false`: -->
`throw_unless` 함수는 주어진 불린(boolean) 표현식의 값이 `false`일 경우, 지정한 예외를 발생시킵니다.

```
throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

throw_unless(
    Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-today"></a>
<!-- #### `today()` -->
#### `today()`

<!-- The `today` function creates a new `Illuminate\Support\Carbon` instance for the current date: -->
`today` 함수는 현재 날짜에 해당하는 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```
$today = today();
```

<a name="method-trait-uses-recursive"></a>
<!-- #### `trait_uses_recursive()` -->
#### `trait_uses_recursive()`

<!-- The `trait_uses_recursive` function returns all traits used by a trait: -->
`trait_uses_recursive` 함수는 특정 트레이트(trait)가 사용하는 모든 트레이트의 목록을 반환합니다.

```
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
<!-- #### `transform()` -->
#### `transform()`

<!-- The `transform` function executes a closure on a given value if the value is not [blank](#method-blank) and then returns the return value of the closure: -->
`transform` 함수는 주어진 값이 [blank](#method-blank)가 아니면 전달받은 클로저(익명 함수)를 실행하고, 그 결과값을 반환합니다.

```
$callback = function ($value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

<!-- A default value or closure may be passed as the third argument to the function. This value will be returned if the given value is blank: -->
값이 blank인 경우 반환할 기본값(또는 클로저)을 세 번째 인자로 전달할 수 있습니다. 이 값은 주어진 값이 blank일 경우 반환됩니다.

```
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
<!-- #### `validator()` -->
#### `validator()`

<!-- The `validator` function creates a new [validator](/docs/9.x/validation) instance with the given arguments. You may use it as an alternative to the `Validator` facade: -->
`validator` 함수는 전달받은 인수로 새로운 [validator](/docs/9.x/validation) 인스턴스를 생성합니다. 이 함수를 `Validator` 파사드의 대체로 사용할 수 있습니다.

```
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
<!-- #### `value()` -->
#### `value()`

<!-- The `value` function returns the value it is given. However, if you pass a closure to the function, the closure will be executed and its returned value will be returned: -->
`value` 함수는 전달한 값을 그대로 반환합니다. 단, 만약 클로저를 전달하면 해당 클로저를 실행한 뒤 반환값을 반환합니다.

```
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false

```
<!-- Additional arguments may be passed to the `value` function. If the first argument is a closure then the additional parameters will be passed to the closure as arguments, otherwise they will be ignored: -->
추가적인 인수를 `value` 함수에 넘길 수도 있습니다. 만약 첫 번째 인수가 클로저라면, 나머지 인수들은 클로저에 인자로 전달됩니다. 클로저가 아니면 추가 인수들은 무시됩니다.

```
$result = value(function ($name) {
    return $parameter;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
<!-- #### `view()` -->
#### `view()`

<!-- The `view` function retrieves a [view](/docs/9.x/views) instance: -->
`view` 함수는 [view](/docs/9.x/views) 인스턴스를 반환합니다.

```
return view('auth.login');
```

<a name="method-with"></a>
<!-- #### `with()` -->
#### `with()`

<!-- The `with` function returns the value it is given. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned: -->
`with` 함수는 전달받은 값을 그대로 반환합니다. 그러나 두 번째 인자로 클로저를 전달하면, 이 클로저가 실행되고 그 반환값이 반환됩니다.

```
$callback = function ($value) {
    return is_numeric($value) ? $value * 2 : 0;
};

$result = with(5, $callback);

// 10

$result = with(null, $callback);

// 0

$result = with(5, null);

// 5
```

<a name="other-utilities"></a>
<!-- ## Other Utilities -->
## Other Utilities

<a name="benchmarking"></a>
<!-- ### Benchmarking -->
### Benchmarking

<!-- Sometimes you may wish to quickly test the performance of certain parts of your application. On those occasions, you may utilize the `Benchmark` support class to measure the number of milliseconds it takes for the given callbacks to complete: -->
어떤 코드의 성능(소요 시간 등)을 빠르게 테스트하고 싶을 때가 있습니다. 이럴 때는 `Benchmark` 지원 클래스를 사용하여 지정한 콜백이 완료되는 데 걸린 시간을 밀리초 단위로 측정할 수 있습니다.

```
<?php

use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    'Scenario 1' => fn () => User::count(), // 0.5 ms
    'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

<!-- By default, the given callbacks will be executed once (one iteration), and their duration will be displayed in the browser / console. -->
기본적으로 전달한 콜백은 한 번(한 번의 반복)만 실행되며, 실행에 소요된 시간이 브라우저나 콘솔에 표시됩니다.

<!-- To invoke a callback more than once, you may specify the number of iterations that the callback should be invoked as the second argument to the method. When executing a callback more than once, the `Benchmark` class will return the average amount of milliseconds it took to execute the callback across all iterations: -->
콜백을 여러 번 반복 실행하고 싶다면, 메서드의 두 번째 인수로 반복 횟수를 지정할 수 있습니다. 콜백을 여러 번 실행할 경우, `Benchmark` 클래스는 전체 반복에서 평균 실행 소요 시간을 반환합니다.

```
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

<a name="lottery"></a>
<!-- ### Lottery -->
### Lottery

<!-- Laravel's lottery class may be used to execute callbacks based on a set of given odds. This can be particularly useful when you only want to execute code for a percentage of your incoming requests: -->
Laravel의 lottery 클래스는 주어진 확률(odds)에 따라 콜백을 실행할 수 있도록 해줍니다. 예를 들어, 들어오는 요청 중 일부에서만 특정 코드를 실행하려고 할 때 유용하게 사용할 수 있습니다.

```
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

<!-- You may combine Laravel's lottery class with other Laravel features. For example, you may wish to only report a small percentage of slow queries to your exception handler. And, since the lottery class is callable, we may pass an instance of the class into any method that accepts callables: -->
Laravel의 lottery 클래스를 다른 Laravel 기능들과 함께 사용할 수도 있습니다. 예를 들어, 느린 쿼리 중 소수만 예외 핸들러에 보고하고 싶을 수 있습니다. 그리고 lottery 클래스는 호출 가능한(callable) 객체이므로, 콜러블을 인수로 받을 수 있는 어떤 메서드에도 전달할 수 있습니다.

```
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;

DB::whenQueryingForLongerThan(
    CarbonInterval::seconds(2),
    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
);
```

<a name="testing-lotteries"></a>
<!-- #### Testing Lotteries -->
#### Testing Lotteries

<!-- Laravel provides some simple methods to allow you to easily test your application's lottery invocations: -->
Laravel은 애플리케이션의 lottery 호출을 손쉽게 테스트할 수 있도록 간단한 메서드들도 제공합니다.

```
// Lottery will always win...
Lottery::alwaysWin();

// Lottery will always lose...
Lottery::alwaysLose();

// Lottery will win then lose, and finally return to normal behavior...
Lottery::fix([true, false]);

// Lottery will return to normal behavior...
Lottery::determineResultsNormally();
```
