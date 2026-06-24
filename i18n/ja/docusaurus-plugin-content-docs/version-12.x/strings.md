<!-- # Strings -->
# Strings

- [Introduction](#introduction)
- [Available Methods](#available-methods)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel includes a variety of functions for manipulating string values. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient. -->
Laravel には、文字列値を操作するためのさまざまな関数が含まれています。これらの関数の多くはフレームワーク自体によって使用されます。ただし、便利だと思われる場合は、独自のアプリケーションで自由に使用できます。

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods

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
[Str::apa](#method-str-apa)
[Str::ascii](#method-str-ascii)
[Str::before](#method-str-before)
[Str::beforeLast](#method-str-before-last)
[Str::between](#method-str-between)
[Str::betweenFirst](#method-str-between-first)
[Str::camel](#method-camel-case)
[Str::charAt](#method-char-at)
[Str::chopStart](#method-str-chop-start)
[Str::chopEnd](#method-str-chop-end)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::doesntContain](#method-str-doesnt-contain)
[Str::doesntEndWith](#method-str-doesnt-end-with)
[Str::doesntStartWith](#method-str-doesnt-start-with)
[Str::deduplicate](#method-deduplicate)
[Str::endsWith](#method-ends-with)
[Str::excerpt](#method-excerpt)
[Str::finish](#method-str-finish)
[Str::fromBase64](#method-str-from-base64)
[Str::headline](#method-str-headline)
[Str::initials](#method-str-initials)
[Str::inlineMarkdown](#method-str-inline-markdown)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isJson](#method-str-is-json)
[Str::isUlid](#method-str-is-ulid)
[Str::isUrl](#method-str-is-url)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
[Str::lcfirst](#method-str-lcfirst)
[Str::length](#method-str-length)
[Str::limit](#method-str-limit)
[Str::lower](#method-str-lower)
[Str::markdown](#method-str-markdown)
[Str::mask](#method-str-mask)
[Str::match](#method-str-match)
[Str::matchAll](#method-str-match-all)
[Str::isMatch](#method-str-is-match)
[Str::orderedUuid](#method-str-ordered-uuid)
[Str::padBoth](#method-str-padboth)
[Str::padLeft](#method-str-padleft)
[Str::padRight](#method-str-padright)
[Str::password](#method-str-password)
[Str::plural](#method-str-plural)
[Str::pluralStudly](#method-str-plural-studly)
[Str::position](#method-str-position)
[Str::random](#method-str-random)
[Str::remove](#method-str-remove)
[Str::repeat](#method-str-repeat)
[Str::replace](#method-str-replace)
[Str::replaceArray](#method-str-replace-array)
[Str::replaceFirst](#method-str-replace-first)
[Str::replaceLast](#method-str-replace-last)
[Str::replaceMatches](#method-str-replace-matches)
[Str::replaceStart](#method-str-replace-start)
[Str::replaceEnd](#method-str-replace-end)
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
[Str::take](#method-take)
[Str::title](#method-title-case)
[Str::toBase64](#method-str-to-base64)
[Str::transliterate](#method-str-transliterate)
[Str::trim](#method-str-trim)
[Str::ltrim](#method-str-ltrim)
[Str::rtrim](#method-str-rtrim)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::ucwords](#method-str-ucwords)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::unwrap](#method-str-unwrap)
[Str::uuid](#method-str-uuid)
[Str::uuid7](#method-str-uuid7)
[Str::wordCount](#method-str-word-count)
[Str::wordWrap](#method-str-word-wrap)
[Str::words](#method-str-words)
[Str::wrap](#method-str-wrap)
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
[Str::apa](#method-str-apa)
[Str::ascii](#method-str-ascii)
[Str::before](#method-str-before)
[Str::beforeLast](#method-str-before-last)
[Str::between](#method-str-between)
[Str::betweenFirst](#method-str-between-first)
[Str::camel](#method-camel-case)
[Str::charAt](#method-char-at)
[Str::chopStart](#method-str-chop-start)
[Str::chopEnd](#method-str-chop-end)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::doesntContain](#method-str-doesnt-contain)
[Str::doesntEndWith](#method-str-doesnt-end-with)
[Str::doesntStartWith](#method-str-doesnt-start-with)
[Str::deduplicate](#method-deduplicate)
[Str::endsWith](#method-ends-with)
[Str::excerpt](#method-excerpt)
[Str::finish](#method-str-finish)
[Str::fromBase64](#method-str-from-base64)
[Str::headline](#method-str-headline)
[Str::initials](#method-str-initials)
[Str::inlineMarkdown](#method-str-inline-markdown)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isJson](#method-str-is-json)
[Str::isUlid](#method-str-is-ulid)
[Str::isUrl](#method-str-is-url)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
[Str::lcfirst](#method-str-lcfirst)
[Str::length](#method-str-length)
[Str::limit](#method-str-limit)
[Str::lower](#method-str-lower)
[Str::markdown](#method-str-markdown)
[Str::mask](#method-str-mask)
[Str::match](#method-str-match)
[Str::matchAll](#method-str-match-all)
[Str::isMatch](#method-str-is-match)
[Str::orderedUuid](#method-str-ordered-uuid)
[Str::padBoth](#method-str-padboth)
[Str::padLeft](#method-str-padleft)
[Str::padRight](#method-str-padright)
[Str::password](#method-str-password)
[Str::plural](#method-str-plural)
[Str::pluralStudly](#method-str-plural-studly)
[Str::position](#method-str-position)
[Str::random](#method-str-random)
[Str::remove](#method-str-remove)
[Str::repeat](#method-str-repeat)
[Str::replace](#method-str-replace)
[Str::replaceArray](#method-str-replace-array)
[Str::replaceFirst](#method-str-replace-first)
[Str::replaceLast](#method-str-replace-last)
[Str::replaceMatches](#method-str-replace-matches)
[Str::replaceStart](#method-str-replace-start)
[Str::replaceEnd](#method-str-replace-end)
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
[Str::take](#method-take)
[Str::title](#method-title-case)
[Str::toBase64](#method-str-to-base64)
[Str::transliterate](#method-str-transliterate)
[Str::trim](#method-str-trim)
[Str::ltrim](#method-str-ltrim)
[Str::rtrim](#method-str-rtrim)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::ucwords](#method-str-ucwords)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::unwrap](#method-str-unwrap)
[Str::uuid](#method-str-uuid)
[Str::uuid7](#method-str-uuid7)
[Str::wordCount](#method-str-word-count)
[Str::wordWrap](#method-str-word-wrap)
[Str::words](#method-str-words)
[Str::wrap](#method-str-wrap)
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
[apa](#method-fluent-str-apa)
[append](#method-fluent-str-append)
[ascii](#method-fluent-str-ascii)
[basename](#method-fluent-str-basename)
[before](#method-fluent-str-before)
[beforeLast](#method-fluent-str-before-last)
[between](#method-fluent-str-between)
[betweenFirst](#method-fluent-str-between-first)
[camel](#method-fluent-str-camel)
[charAt](#method-fluent-str-char-at)
[classBasename](#method-fluent-str-class-basename)
[chopStart](#method-fluent-str-chop-start)
[chopEnd](#method-fluent-str-chop-end)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[decrypt](#method-fluent-str-decrypt)
[deduplicate](#method-fluent-str-deduplicate)
[dirname](#method-fluent-str-dirname)
[doesntContain](#method-fluent-str-doesnt-contain)
[doesntEndWith](#method-fluent-str-doesnt-end-with)
[doesntStartWith](#method-fluent-str-doesnt-start-with)
[encrypt](#method-fluent-str-encrypt)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[excerpt](#method-fluent-str-excerpt)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[fromBase64](#method-fluent-str-from-base64)
[hash](#method-fluent-str-hash)
[headline](#method-fluent-str-headline)
[initials](#method-fluent-str-initials)
[inlineMarkdown](#method-fluent-str-inline-markdown)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isJson](#method-fluent-str-is-json)
[isUlid](#method-fluent-str-is-ulid)
[isUrl](#method-fluent-str-is-url)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[lcfirst](#method-fluent-str-lcfirst)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
[isMatch](#method-fluent-str-is-match)
[newLine](#method-fluent-str-new-line)
[padBoth](#method-fluent-str-padboth)
[padLeft](#method-fluent-str-padleft)
[padRight](#method-fluent-str-padright)
[pipe](#method-fluent-str-pipe)
[plural](#method-fluent-str-plural)
[position](#method-fluent-str-position)
[prepend](#method-fluent-str-prepend)
[remove](#method-fluent-str-remove)
[repeat](#method-fluent-str-repeat)
[replace](#method-fluent-str-replace)
[replaceArray](#method-fluent-str-replace-array)
[replaceFirst](#method-fluent-str-replace-first)
[replaceLast](#method-fluent-str-replace-last)
[replaceMatches](#method-fluent-str-replace-matches)
[replaceStart](#method-fluent-str-replace-start)
[replaceEnd](#method-fluent-str-replace-end)
[scan](#method-fluent-str-scan)
[singular](#method-fluent-str-singular)
[slug](#method-fluent-str-slug)
[snake](#method-fluent-str-snake)
[split](#method-fluent-str-split)
[squish](#method-fluent-str-squish)
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[stripTags](#method-fluent-str-strip-tags)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[swap](#method-fluent-str-swap)
[take](#method-fluent-str-take)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[toBase64](#method-fluent-str-to-base64)
[toHtmlString](#method-fluent-str-to-html-string)
[toUri](#method-fluent-str-to-uri)
[transliterate](#method-fluent-str-transliterate)
[trim](#method-fluent-str-trim)
[ltrim](#method-fluent-str-ltrim)
[rtrim](#method-fluent-str-rtrim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[ucwords](#method-fluent-str-ucwords)
[unwrap](#method-fluent-str-unwrap)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenDoesntEndWith](#method-fluent-str-when-doesnt-end-with)
[whenDoesntStartWith](#method-fluent-str-when-doesnt-start-with)
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
[wrap](#method-fluent-str-wrap)
-->
[after](#method-fluent-str-after)
[afterLast](#method-fluent-str-after-last)
[apa](#method-fluent-str-apa)
[append](#method-fluent-str-append)
[ascii](#method-fluent-str-ascii)
[basename](#method-fluent-str-basename)
[before](#method-fluent-str-before)
[beforeLast](#method-fluent-str-before-last)
[between](#method-fluent-str-between)
[betweenFirst](#method-fluent-str-between-first)
[camel](#method-fluent-str-camel)
[charAt](#method-fluent-str-char-at)
[classBasename](#method-fluent-str-class-basename)
[chopStart](#method-fluent-str-chop-start)
[chopEnd](#method-fluent-str-chop-end)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[decrypt](#method-fluent-str-decrypt)
[deduplicate](#method-fluent-str-deduplicate)
[dirname](#method-fluent-str-dirname)
[doesntContain](#method-fluent-str-doesnt-contain)
[doesntEndWith](#method-fluent-str-doesnt-end-with)
[doesntStartWith](#method-fluent-str-doesnt-start-with)
[encrypt](#method-fluent-str-encrypt)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[excerpt](#method-fluent-str-excerpt)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[fromBase64](#method-fluent-str-from-base64)
[hash](#method-fluent-str-hash)
[headline](#method-fluent-str-headline)
[initials](#method-fluent-str-initials)
[inlineMarkdown](#method-fluent-str-inline-markdown)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isJson](#method-fluent-str-is-json)
[isUlid](#method-fluent-str-is-ulid)
[isUrl](#method-fluent-str-is-url)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[lcfirst](#method-fluent-str-lcfirst)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
[isMatch](#method-fluent-str-is-match)
[newLine](#method-fluent-str-new-line)
[padBoth](#method-fluent-str-padboth)
[padLeft](#method-fluent-str-padleft)
[padRight](#method-fluent-str-padright)
[pipe](#method-fluent-str-pipe)
[plural](#method-fluent-str-plural)
[position](#method-fluent-str-position)
[prepend](#method-fluent-str-prepend)
[remove](#method-fluent-str-remove)
[repeat](#method-fluent-str-repeat)
[replace](#method-fluent-str-replace)
[replaceArray](#method-fluent-str-replace-array)
[replaceFirst](#method-fluent-str-replace-first)
[replaceLast](#method-fluent-str-replace-last)
[replaceMatches](#method-fluent-str-replace-matches)
[replaceStart](#method-fluent-str-replace-start)
[replaceEnd](#method-fluent-str-replace-end)
[scan](#method-fluent-str-scan)
[singular](#method-fluent-str-singular)
[slug](#method-fluent-str-slug)
[snake](#method-fluent-str-snake)
[split](#method-fluent-str-split)
[squish](#method-fluent-str-squish)
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[stripTags](#method-fluent-str-strip-tags)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[swap](#method-fluent-str-swap)
[take](#method-fluent-str-take)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[toBase64](#method-fluent-str-to-base64)
[toHtmlString](#method-fluent-str-to-html-string)
[toUri](#method-fluent-str-to-uri)
[transliterate](#method-fluent-str-transliterate)
[trim](#method-fluent-str-trim)
[ltrim](#method-fluent-str-ltrim)
[rtrim](#method-fluent-str-rtrim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[ucwords](#method-fluent-str-ucwords)
[unwrap](#method-fluent-str-unwrap)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenDoesntEndWith](#method-fluent-str-when-doesnt-end-with)
[whenDoesntStartWith](#method-fluent-str-when-doesnt-start-with)
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
[wrap](#method-fluent-str-wrap)

<!-- </div> -->
</div>

<a name="strings"></a>
<!-- ## Strings -->
## Strings

<a name="method-__"></a>
<!-- #### `__()` -->
#### `__()`
<!-- The `__` function translates the given translation string or translation key using your [language files](/docs/12.x/localization): -->
`__` 関数は、[language files](/docs/12.x/localization) を使用して、指定された翻訳文字列または翻訳キーを翻訳します。

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

<!-- If the specified translation string or key does not exist, the `__` function will return the given value. So, using the example above, the `__` function would return `messages.welcome` if that translation key does not exist. -->
指定された変換文字列またはキーが存在しない場合、`__` 関数は指定された値を返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`__` 関数は `messages.welcome` を返します。

<a name="method-class-basename"></a>
<!-- #### `class_basename()` -->
#### `class_basename()`
<!-- The `class_basename` function returns the class name of the given class with the class's namespace removed: -->
`class_basename` 関数は、クラスの名前空間が削除された、指定されたクラスのクラス名を返します。

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
<!-- #### `e()` -->
#### `e()`
<!-- The `e` function runs PHP's `htmlspecialchars` function with the `double_encode` option set to `true` by default: -->
`e` 関数は、デフォルトで `double_encode` オプションを `true` に設定して、PHP の `htmlspecialchars` 関数を実行します。

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
<!-- #### `preg_replace_array()` -->
#### `preg_replace_array()`
<!-- The `preg_replace_array` function replaces a given pattern in the string sequentially using an array: -->
`preg_replace_array` 関数は、配列を使用して文字列内の指定されたパターンを順番に置き換えます。

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
<!-- #### `Str::after()` -->
#### `Str::after()`
<!-- The `Str::after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::after` メソッドは、文字列内の指定された値以降のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
<!-- #### `Str::afterLast()` -->
#### `Str::afterLast()`
<!-- The `Str::afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
<!-- #### `Str::apa()` -->
#### `Str::apa()`
<!-- The `Str::apa` method converts the given string to title case following the [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case): -->
`Str::apa` メソッドは、指定された文字列を [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case) に従ってタイトルケースに変換します。

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
<!-- #### `Str::ascii()` -->
#### `Str::ascii()`
<!-- The `Str::ascii` method will attempt to transliterate the string into an ASCII value: -->
`Str::ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
<!-- #### `Str::before()` -->
#### `Str::before()`
<!-- The `Str::before` method returns everything before the given value in a string: -->
`Str::before` メソッドは、文字列内の指定された値より前のすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
<!-- #### `Str::beforeLast()` -->
#### `Str::beforeLast()`
<!-- The `Str::beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`Str::beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
<!-- #### `Str::between()` -->
#### `Str::between()`
<!-- The `Str::between` method returns the portion of a string between two values: -->
`Str::between` メソッドは、2 つの値の間の文字列の部分を返します。

```php
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
<!-- #### `Str::betweenFirst()` -->
#### `Str::betweenFirst()`
<!-- The `Str::betweenFirst` method returns the smallest possible portion of a string between two values: -->
`Str::betweenFirst` メソッドは、2 つの値の間の文字列の可能な最小部分を返します。

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
<!-- #### `Str::camel()` -->
#### `Str::camel()`
<!-- The `Str::camel` method converts the given string to `camelCase`: -->
`Str::camel` メソッドは、指定された文字列を `camelCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
<!-- #### `Str::charAt()` -->
#### `Str::charAt()`
<!-- The `Str::charAt` method returns the character at the specified index. If the index is out of bounds, `false` is returned: -->
`Str::charAt` メソッドは、指定されたインデックスの文字を返します。インデックスが範囲外の場合、`false` が返されます。

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
<!-- #### `Str::chopStart()` -->
#### `Str::chopStart()`
<!-- The `Str::chopStart` method removes the first occurrence of the given value only if the value appears at the start of the string: -->
`Str::chopStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

<!-- You may also pass an array as the second argument. If the string starts with any of the values in the array then that value will be removed from string: -->
2 番目の引数として配列を渡すこともできます。文字列が配列内のいずれかの値で始まる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
<!-- #### `Str::chopEnd()` -->
#### `Str::chopEnd()`
<!-- The `Str::chopEnd` method removes the last occurrence of the given value only if the value appears at the end of the string: -->
`Str::chopEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

<!-- You may also pass an array as the second argument. If the string ends with any of the values in the array then that value will be removed from string: -->
2 番目の引数として配列を渡すこともできます。文字列が配列内のいずれかの値で終わる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
<!-- #### `Str::contains()` -->
#### `Str::contains()`
<!-- The `Str::contains` method determines if the given string contains the given value. By default, this method is case sensitive: -->
`Str::contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

<!-- You may disable case sensitivity by setting the `ignoreCase` argument to `true`: -->
`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
<!-- #### `Str::containsAll()` -->
#### `Str::containsAll()`
<!-- The `Str::containsAll` method determines if the given string contains all of the values in a given array: -->
`Str::containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

<!-- You may disable case sensitivity by setting the `ignoreCase` argument to `true`: -->
`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
<!-- #### `Str::doesntContain()` -->
#### `Str::doesntContain()`
<!-- The `Str::doesntContain` method determines if the given string doesn't contain the given value. By default, this method is case sensitive: -->
`Str::doesntContain` メソッドは、指定された文字列に指定された値が含まれていないかどうかを判断します。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

<!-- You may also pass an array of values to determine if the given string doesn't contain any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれていないかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'framework']);

// true
```

<!-- You may disable case sensitivity by setting the `ignoreCase` argument to `true`: -->
`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
<!-- #### `Str::deduplicate()` -->
#### `Str::deduplicate()`
<!-- The `Str::deduplicate` method replaces consecutive instances of a character with a single instance of that character in the given string. By default, the method deduplicates spaces: -->
`Str::deduplicate` メソッドは、指定された文字列内の文字の連続したインスタンスをその文字の単一のインスタンスに置き換えます。デフォルトでは、このメソッドはスペースを重複排除します。

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

<!-- You may specify a different character to deduplicate by passing it in as the second argument to the method: -->
重複排除する別の文字を指定するには、それをメソッドの 2 番目の引数として渡します。

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-str-doesnt-end-with"></a>
<!-- #### `Str::doesntEndWith()` -->
#### `Str::doesntEndWith()`
<!-- The `Str::doesntEndWith` method determines if the given string doesn't end with the given value: -->
`Str::doesntEndWith` メソッドは、指定された文字列が指定された値で終わっていないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', 'dog');

// true
```

<!-- You may also pass an array of values to determine if the given string doesn't end with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のどの値でも終わっていないかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', ['this', 'foo']);

// true

$result = Str::doesntEndWith('This is my name', ['name', 'foo']);

// false
```

<a name="method-str-doesnt-start-with"></a>
<!-- #### `Str::doesntStartWith()` -->
#### `Str::doesntStartWith()`
<!-- The `Str::doesntStartWith` method determines if the given string doesn't begin with the given value: -->
`Str::doesntStartWith` メソッドは、指定された文字列が指定された値で始まらないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::doesntStartWith('This is my name', 'That');

// true
```

<!-- If an array of possible values is passed, the `doesntStartWith` method will return `true` if the string doesn't begin with any of the given values: -->
可能な値の配列が渡された場合、文字列が指定された値のいずれでも始まらない場合、`doesntStartWith` メソッドは `true` を返します。

```php
$result = Str::doesntStartWith('This is my name', ['What', 'That', 'There']);

// true
```

<a name="method-ends-with"></a>
<!-- #### `Str::endsWith()` -->
#### `Str::endsWith()`
<!-- The `Str::endsWith` method determines if the given string ends with the given value: -->
`Str::endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

```php
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
`Str::excerpt` メソッドは、指定された文字列から、その文字列内のフレーズの最初のインスタンスに一致する抜粋を抽出します。

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

<!-- The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string. -->
`radius` オプション (デフォルトは `100`) を使用すると、切り詰められた文字列の両側に表示される文字数を定義できます。

<!-- In addition, you may use the `omission` option to define the string that will be prepended and appended to the truncated string: -->
さらに、`omission` オプションを使用して、切り詰められた文字列の前後に追加される文字列を定義できます。

```php
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
`Str::finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-from-base64"></a>
<!-- #### `Str::fromBase64()` -->
#### `Str::fromBase64()`
<!-- The `Str::fromBase64` method decodes the given Base64 string: -->
`Str::fromBase64` メソッドは、指定された Base64 文字列をデコードします。

```php
use Illuminate\Support\Str;

$decoded = Str::fromBase64('TGFyYXZlbA==');

// Laravel
```

<a name="method-str-headline"></a>
<!-- #### `Str::headline()` -->
#### `Str::headline()`
<!-- The `Str::headline` method will convert strings delimited by casing, hyphens, or underscores into a space delimited string with each word's first letter capitalized: -->
`Str::headline` メソッドは、大文字と小文字、ハイフン、またはアンダースコアで区切られた文字列を、各単語の最初の文字が大文字になったスペースで区切られた文字列に変換します。

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-initials"></a>
<!-- #### `Str::initials()` -->
#### `Str::initials()`
<!-- The `Str::initials` method will return the initials of a given string, optionally capitalizing them: -->
`Str::initials` メソッドは、指定された文字列のイニシャルを返します。オプションで大文字にすることもできます。

```php
use Illuminate\Support\Str;

$initials = Str::initials('taylor otwell');

// to

$initials = Str::initials('taylor otwell', capitalize: true);

// TO
```

<a name="method-str-inline-markdown"></a>
<!-- #### `Str::inlineMarkdown()` -->
#### `Str::inlineMarkdown()`
<!-- The `Str::inlineMarkdown` method converts GitHub flavored Markdown into inline HTML using [CommonMark](https://commonmark.thephpleague.com/). However, unlike the `markdown` method, it does not wrap all generated HTML in a block-level element: -->
`Str::inlineMarkdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown をインライン HTML に変換します。ただし、`markdown` メソッドとは異なり、生成されたすべての HTML をブロックレベル要素でラップするわけではありません。

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

<!-- #### Markdown Security -->
#### Markdown Security

<!-- By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier: -->
デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark Security documentation](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

```php
use Illuminate\Support\Str;

Str::inlineMarkdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-str-is"></a>
<!-- #### `Str::is()` -->
#### `Str::is()`
<!-- The `Str::is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values: -->
`Str::is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます。

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

<!-- You may disable case sensitivity by setting the `ignoreCase` argument to `true`: -->
`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
<!-- #### `Str::isAscii()` -->
#### `Str::isAscii()`
<!-- The `Str::isAscii` method determines if a given string is 7 bit ASCII: -->
`Str::isAscii` メソッドは、指定された文字列が 7 ビット ASCII であるかどうかを判断します。

```php
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
`Str::isJson` メソッドは、指定された文字列が有効な JSON かどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::isJson('[1,2,3]');

// true

$result = Str::isJson('{"first": "John", "last": "Doe"}');

// true

$result = Str::isJson('{first: "John", last: "Doe"}');

// false
```

<a name="method-str-is-url"></a>
<!-- #### `Str::isUrl()` -->
#### `Str::isUrl()`
<!-- The `Str::isUrl` method determines if the given string is a valid URL: -->
`Str::isUrl` メソッドは、指定された文字列が有効な URL かどうかを判断します。

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

<!-- The `isUrl` method considers a wide range of protocols as valid. However, you may specify the protocols that should be considered valid by providing them to the `isUrl` method: -->
`isUrl` メソッドは、幅広いプロトコルを有効であるとみなします。ただし、`isUrl` メソッドにプロトコルを指定することで、有効であるとみなされるプロトコルを指定できます。

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
<!-- #### `Str::isUlid()` -->
#### `Str::isUlid()`
<!-- The `Str::isUlid` method determines if the given string is a valid ULID: -->
`Str::isUlid` メソッドは、指定された文字列が有効な ULID かどうかを判断します。

```php
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
`Str::isUuid` メソッドは、指定された文字列が有効な UUID かどうかを判断します。

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

<!-- You may also validate that the given UUID matches a UUID specification by version (1, 3, 4, 5, 6, 7, or 8): -->
指定された UUID がバージョン (1、3、4、5、6、7、または 8) ごとの UUID 仕様と一致することを検証することもできます。

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 4);

// true

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 1);

// false
```

<a name="method-kebab-case"></a>
<!-- #### `Str::kebab()` -->
#### `Str::kebab()`
<!-- The `Str::kebab` method converts the given string to `kebab-case`: -->
`Str::kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
<!-- #### `Str::lcfirst()` -->
#### `Str::lcfirst()`
<!-- The `Str::lcfirst` method returns the given string with the first character lowercased: -->
`Str::lcfirst` メソッドは、最初の文字を小文字にして指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
<!-- #### `Str::length()` -->
#### `Str::length()`
<!-- The `Str::length` method returns the length of the given string: -->
`Str::length` メソッドは、指定された文字列の長さを返します。

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
<!-- #### `Str::limit()` -->
#### `Str::limit()`
<!-- The `Str::limit` method truncates the given string to the specified length: -->
`Str::limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

<!-- You may pass a third argument to the method to change the string that will be appended to the end of the truncated string: -->
メソッドに 3 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更できます。

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

<!-- If you would like to preserve complete words when truncating the string, you may utilize the `preserveWords` argument. When this argument is `true`, the string will be truncated to the nearest complete word boundary: -->
文字列を切り詰めるときに完全な単語を保持したい場合は、`preserveWords` 引数を利用できます。この引数が `true` の場合、文字列は最も近い完全な単語境界まで切り詰められます。

```php
$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

// The quick...
```

<a name="method-str-lower"></a>
<!-- #### `Str::lower()` -->
#### `Str::lower()`
<!-- The `Str::lower` method converts the given string to lowercase: -->
`Str::lower` メソッドは、指定された文字列を小文字に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
<!-- #### `Str::markdown()` -->
#### `Str::markdown()`
<!-- The `Str::markdown` method converts GitHub flavored Markdown into HTML using [CommonMark](https://commonmark.thephpleague.com/): -->
`Str::markdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown を HTML に変換します。

```php
use Illuminate\Support\Str;

$html = Str::markdown('# Laravel');

// <h1>Laravel</h1>

$html = Str::markdown('# Taylor <b>Otwell</b>', [
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

<!-- #### Markdown Security -->
#### Markdown Security

<!-- By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier: -->
デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark Security documentation](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

```php
use Illuminate\Support\Str;

Str::markdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-str-mask"></a>
<!-- #### `Str::mask()` -->
#### `Str::mask()`
<!-- The `Str::mask` method masks a portion of a string with a repeated character, and may be used to obfuscate segments of strings such as email addresses and phone numbers: -->
`Str::mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

<!-- If needed, you provide a negative number as the third argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
必要に応じて、`mask` メソッドの 3 番目の引数として負の数値を指定します。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-match"></a>
<!-- #### `Str::match()` -->
#### `Str::match()`
<!-- The `Str::match` method will return the portion of a string that matches a given regular expression pattern: -->
`Str::match` メソッドは、指定された正規表現パターンに一致する文字列の部分を返します。

```php
use Illuminate\Support\Str;

$result = Str::match('/bar/', 'foo bar');

// 'bar'

$result = Str::match('/foo (.*)/', 'foo bar');

// 'bar'
```

<a name="method-str-match-all"></a>
<!-- #### `Str::matchAll()` -->
#### `Str::matchAll()`
<!-- The `Str::matchAll` method will return a collection containing the portions of a string that match a given regular expression pattern: -->
`Str::matchAll` メソッドは、指定された正規表現パターンに一致する文字列の部分を含むコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/bar/', 'bar foo bar');

// collect(['bar', 'bar'])
```

<!-- If you specify a matching group within the expression, Laravel will return a collection of the first matching group's matches: -->
式内で一致するグループを指定すると、Laravel は最初に一致したグループの一致のコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

// collect(['un', 'ly']);
```

<!-- If no matches are found, an empty collection will be returned. -->
一致するものが見つからない場合は、空のコレクションが返されます。

<a name="method-str-is-match"></a>
<!-- #### `Str::isMatch()` -->
#### `Str::isMatch()`
<!-- The `Str::isMatch` method will return `true` if the string matches a given regular expression: -->
文字列が指定された正規表現に一致する場合、`Str::isMatch` メソッドは `true` を返します。

```php
use Illuminate\Support\Str;

$result = Str::isMatch('/foo (.*)/', 'foo bar');

// true

$result = Str::isMatch('/foo (.*)/', 'laravel');

// false
```

<a name="method-str-ordered-uuid"></a>
<!-- #### `Str::orderedUuid()` -->
#### `Str::orderedUuid()`
<!-- The `Str::orderedUuid` method generates a "timestamp first" UUID that may be efficiently stored in an indexed database column. Each UUID that is generated using this method will be sorted after UUIDs previously generated using the method: -->
`Str::orderedUuid` メソッドは、インデックス付きデータベース列に効率的に格納できる「タイムスタンプ優先」の UUID を生成します。このメソッドを使用して生成された各 UUID は、以前に次のメソッドを使用して生成された UUID の後にソートされます。

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
<!-- #### `Str::padBoth()` -->
#### `Str::padBoth()`
<!-- The `Str::padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches a desired length: -->
`Str::padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

```php
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
`Str::padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

```php
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
`Str::padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
<!-- #### `Str::password()` -->
#### `Str::password()`
<!-- The `Str::password` method may be used to generate a secure, random password of a given length. The password will consist of a combination of letters, numbers, symbols, and spaces. By default, passwords are 32 characters long: -->
`Str::password` メソッドを使用すると、指定された長さの安全なランダムなパスワードを生成できます。パスワードは文字、数字、記号、スペースの組み合わせで構成されます。デフォルトでは、パスワードの長さは 32 文字です。

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
<!-- #### `Str::plural()` -->
#### `Str::plural()`
<!-- The `Str::plural` method converts a singular word string to its plural form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language): -->
`Str::plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

<!-- The `prependCount` argument may be provided to prefix the pluralized string with the formatted `$count`: -->
`prependCount` 引数を指定すると、書式設定された `$count` を複数化された文字列の前に付けることができます。

```php
use Illuminate\Support\Str;

$label = Str::plural('car', 1000, prependCount: true);

// 1,000 cars
```

<a name="method-str-plural-studly"></a>
<!-- #### `Str::pluralStudly()` -->
#### `Str::pluralStudly()`
<!-- The `Str::pluralStudly` method converts a singular word string formatted in studly caps case to its plural form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language): -->
`Str::pluralStudly` メソッドは、大文字小文字でフォーマットされた単数形の単語文字列を複数形に変換します。この関数は [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>
<!-- #### `Str::position()` -->
#### `Str::position()`
<!-- The `Str::position` method returns the position of the first occurrence of a substring in a string. If the substring does not exist in the given string, `false` is returned: -->
`Str::position` メソッドは、文字列内で最初に出現する部分文字列の位置を返します。指定された文字列に部分文字列が存在しない場合は、`false` が返されます。

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
<!-- #### `Str::random()` -->
#### `Str::random()`
<!-- The `Str::random` method generates a random string of the specified length. This function uses PHP's `random_bytes` function: -->
`Str::random` メソッドは、指定された長さのランダムな文字列を生成します。この関数は、PHP の `random_bytes` 関数を使用します。

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

<!-- During testing, it may be useful to "fake" the value that is returned by the `Str::random` method. To accomplish this, you may use the `createRandomStringsUsing` method: -->
テスト中に、`Str::random` メソッドによって返される値を「偽装」すると便利な場合があります。これを実現するには、`createRandomStringsUsing` メソッドを使用できます。

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

<!-- To instruct the `random` method to return to generating random strings normally, you may invoke the `createRandomStringsNormally` method: -->
`random` メソッドに通常のランダム文字列の生成に戻るように指示するには、`createRandomStringsNormally` メソッドを呼び出します。

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
<!-- #### `Str::remove()` -->
#### `Str::remove()`
<!-- The `Str::remove` method removes the given value or array of values from the string: -->
`Str::remove` メソッドは、指定された値または値の配列を文字列から削除します。

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

<!-- You may also pass `false` as a third argument to the `remove` method to ignore case when removing strings. -->
文字列を削除するときに大文字と小文字を区別しないように、`false` を `remove` メソッドの 3 番目の引数として渡すこともできます。

<a name="method-str-repeat"></a>
<!-- #### `Str::repeat()` -->
#### `Str::repeat()`
<!-- The `Str::repeat` method repeats the given string: -->
`Str::repeat` メソッドは、指定された文字列を繰り返します。

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
<!-- #### `Str::replace()` -->
#### `Str::replace()`
<!-- The `Str::replace` method replaces a given string within the string: -->
`Str::replace` メソッドは、文字列内の指定された文字列を置き換えます。

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

<!-- The `replace` method also accepts a `caseSensitive` argument. By default, the `replace` method is case sensitive: -->
`replace` メソッドは、`caseSensitive` 引数も受け入れます。デフォルトでは、`replace` メソッドでは大文字と小文字が区別されます。

```php
$replaced = Str::replace(
    'php',
    'Laravel',
    'PHP Framework for Web Artisans',
    caseSensitive: false
);

// Laravel Framework for Web Artisans
```

<a name="method-str-replace-array"></a>
<!-- #### `Str::replaceArray()` -->
#### `Str::replaceArray()`
<!-- The `Str::replaceArray` method replaces a given value in the string sequentially using an array: -->
`Str::replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
<!-- #### `Str::replaceFirst()` -->
#### `Str::replaceFirst()`
<!-- The `Str::replaceFirst` method replaces the first occurrence of a given value in a string: -->
`Str::replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
<!-- #### `Str::replaceLast()` -->
#### `Str::replaceLast()`
<!-- The `Str::replaceLast` method replaces the last occurrence of a given value in a string: -->
`Str::replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
<!-- #### `Str::replaceMatches()` -->
#### `Str::replaceMatches()`
<!-- The `Str::replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string: -->
`Str::replaceMatches` メソッドは、パターンに一致する文字列のすべての部分を指定された置換文字列に置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

<!-- The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value: -->
`replaceMatches` メソッドは、指定されたパターンに一致する文字列の各部分で呼び出されるクロージャも受け入れます。これにより、クロージャ内で置換ロジックを実行し、置換された値を返すことができます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
<!-- #### `Str::replaceStart()` -->
#### `Str::replaceStart()`
<!-- The `Str::replaceStart` method replaces the first occurrence of the given value only if the value appears at the start of the string: -->
`Str::replaceStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
<!-- #### `Str::replaceEnd()` -->
#### `Str::replaceEnd()`
<!-- The `Str::replaceEnd` method replaces the last occurrence of the given value only if the value appears at the end of the string: -->
`Str::replaceEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

// Hello Laravel

$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-reverse"></a>
<!-- #### `Str::reverse()` -->
#### `Str::reverse()`
<!-- The `Str::reverse` method reverses the given string: -->
`Str::reverse` メソッドは、指定された文字列を反転します。

```php
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
<!-- #### `Str::singular()` -->
#### `Str::singular()`
<!-- The `Str::singular` method converts a string to its singular form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language): -->
`Str::singular` メソッドは、文字列を単数形に変換します。この関数は [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language) をサポートします。

```php
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
`Str::slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
<!-- #### `Str::snake()` -->
#### `Str::snake()`
<!-- The `Str::snake` method converts the given string to `snake_case`: -->
`Str::snake` メソッドは、指定された文字列を `snake_case` に変換します。

```php
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
`Str::squish` メソッドは、単語間の無関係な空白を含め、文字列から無関係な空白をすべて削除します。

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
<!-- #### `Str::start()` -->
#### `Str::start()`
<!-- The `Str::start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`Str::start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

```php
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
`Str::startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

<!-- If an array of possible values is passed, the `startsWith` method will return `true` if the string begins with any of the given values: -->
可能な値の配列が渡された場合、文字列が指定された値のいずれかで始まる場合、`startsWith` メソッドは `true` を返します。

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
<!-- #### `Str::studly()` -->
#### `Str::studly()`
<!-- The `Str::studly` method converts the given string to `StudlyCase`: -->
`Str::studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
<!-- #### `Str::substr()` -->
#### `Str::substr()`
<!-- The `Str::substr` method returns the portion of string specified by the start and length parameters: -->
`Str::substr` メソッドは、start パラメーターと length パラメーターで指定された文字列の部分を返します。

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
<!-- #### `Str::substrCount()` -->
#### `Str::substrCount()`
<!-- The `Str::substrCount` method returns the number of occurrences of a given value in the given string: -->
`Str::substrCount` メソッドは、指定された文字列内の指定された値の出現数を返します。

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
<!-- #### `Str::substrReplace()` -->
#### `Str::substrReplace()`
<!-- The `Str::substrReplace` method replaces text within a portion of a string, starting at the position specified by the third argument and replacing the number of characters specified by the fourth argument. Passing `0` to the method's fourth argument will insert the string at the specified position without replacing any of the existing characters in the string: -->
`Str::substrReplace` メソッドは、文字列の一部内のテキストを、3 番目の引数で指定された位置から開始して 4 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 4 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

```php
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
`Str::swap` メソッドは、PHP の `strtr` 関数を使用して、指定された文字列内の複数の値を置き換えます。

```php
use Illuminate\Support\Str;

$string = Str::swap([
    'Tacos' => 'Burritos',
    'great' => 'fantastic',
], 'Tacos are great!');

// Burritos are fantastic!
```

<a name="method-take"></a>
<!-- #### `Str::take()` -->
#### `Str::take()`
<!-- The `Str::take` method returns a specified number of characters from the beginning of a string: -->
`Str::take` メソッドは、文字列の先頭から指定された数の文字を返します。

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
<!-- #### `Str::title()` -->
#### `Str::title()`
<!-- The `Str::title` method converts the given string to `Title Case`: -->
`Str::title` メソッドは、指定された文字列を `Title Case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
<!-- #### `Str::toBase64()` -->
#### `Str::toBase64()`
<!-- The `Str::toBase64` method converts the given string to Base64: -->
`Str::toBase64` メソッドは、指定された文字列を Base64 に変換します。

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
<!-- #### `Str::transliterate()` -->
#### `Str::transliterate()`
<!-- The `Str::transliterate` method will attempt to convert a given string into its closest ASCII representation: -->
`Str::transliterate` メソッドは、指定された文字列を最も近い ASCII 表現に変換しようとします。

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
<!-- #### `Str::trim()` -->
#### `Str::trim()`
<!-- The `Str::trim` method strips whitespace (or other characters) from the beginning and end of the given string. Unlike PHP's native `trim` function, the `Str::trim` method also removes unicode whitespace characters: -->
`Str::trim` メソッドは、指定された文字列の先頭と末尾から空白 (または他の文字) を削除します。 PHP のネイティブ `trim` 関数とは異なり、`Str::trim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
<!-- #### `Str::ltrim()` -->
#### `Str::ltrim()`
<!-- The `Str::ltrim` method strips whitespace (or other characters) from the beginning of the given string. Unlike PHP's native `ltrim` function, the `Str::ltrim` method also removes unicode whitespace characters: -->
`Str::ltrim` メソッドは、指定された文字列の先頭から空白 (または他の文字) を削除します。 PHP のネイティブ `ltrim` 関数とは異なり、`Str::ltrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
<!-- #### `Str::rtrim()` -->
#### `Str::rtrim()`
<!-- The `Str::rtrim` method strips whitespace (or other characters) from the end of the given string. Unlike PHP's native `rtrim` function, the `Str::rtrim` method also removes unicode whitespace characters: -->
`Str::rtrim` メソッドは、指定された文字列の末尾から空白 (または他の文字) を削除します。 PHP のネイティブ `rtrim` 関数とは異なり、`Str::rtrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
<!-- #### `Str::ucfirst()` -->
#### `Str::ucfirst()`
<!-- The `Str::ucfirst` method returns the given string with the first character capitalized: -->
`Str::ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
<!-- #### `Str::ucsplit()` -->
#### `Str::ucsplit()`
<!-- The `Str::ucsplit` method splits the given string into an array by uppercase characters: -->
`Str::ucsplit` メソッドは、指定された文字列を大文字ごとに配列に分割します。

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-ucwords"></a>
<!-- #### `Str::ucwords()` -->
#### `Str::ucwords()`
<!-- The `Str::ucwords` method converts the first character of each word in the given string to uppercase: -->
`Str::ucwords` メソッドは、指定された文字列内の各単語の最初の文字を大文字に変換します。

```php
use Illuminate\Support\Str;

$string = Str::ucwords('laravel framework');

// Laravel Framework
```

<a name="method-str-upper"></a>
<!-- #### `Str::upper()` -->
#### `Str::upper()`
<!-- The `Str::upper` method converts the given string to uppercase: -->
`Str::upper` メソッドは、指定された文字列を大文字に変換します。

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
<!-- #### `Str::ulid()` -->
#### `Str::ulid()`
<!-- The `Str::ulid` method generates a ULID, which is a compact, time-ordered unique identifier: -->
`Str::ulid` メソッドは、コンパクトな時間順の一意の識別子である ULID を生成します。

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

<!-- If you would like to retrieve a `Illuminate\Support\Carbon` date instance representing the date and time that a given ULID was created, you may use the `createFromId` method provided by Laravel's Carbon integration: -->
特定の ULID が作成された日時を表す `Illuminate\Support\Carbon` 日付インスタンスを取得したい場合は、Laravel の Carbon 統合によって提供される `createFromId` メソッドを使用できます。

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

<!-- During testing, it may be useful to "fake" the value that is returned by the `Str::ulid` method. To accomplish this, you may use the `createUlidsUsing` method: -->
テスト中に、`Str::ulid` メソッドによって返される値を「偽装」すると便利な場合があります。これを実現するには、`createUlidsUsing` メソッドを使用できます。

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

<!-- To instruct the `ulid` method to return to generating ULIDs normally, you may invoke the `createUlidsNormally` method: -->
`ulid` メソッドに通常の ULID の生成に戻るように指示するには、`createUlidsNormally` メソッドを呼び出します。

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
<!-- #### `Str::unwrap()` -->
#### `Str::unwrap()`
<!-- The `Str::unwrap` method removes the specified strings from the beginning and end of a given string: -->
`Str::unwrap` メソッドは、指定された文字列の先頭と末尾から指定された文字列を削除します。

```php
use Illuminate\Support\Str;

Str::unwrap('-Laravel-', '-');

// Laravel

Str::unwrap('{framework: "Laravel"}', '{', '}');

// framework: "Laravel"
```

<a name="method-str-uuid"></a>
<!-- #### `Str::uuid()` -->
#### `Str::uuid()`
<!-- The `Str::uuid` method generates a UUID (version 4): -->
`Str::uuid` メソッドは UUID (バージョン 4) を生成します。

```php
use Illuminate\Support\Str;

return (string) Str::uuid();
```

<!-- During testing, it may be useful to "fake" the value that is returned by the `Str::uuid` method. To accomplish this, you may use the `createUuidsUsing` method: -->
テスト中に、`Str::uuid` メソッドによって返される値を「偽装」すると便利な場合があります。これを実現するには、`createUuidsUsing` メソッドを使用できます。

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

<!-- To instruct the `uuid` method to return to generating UUIDs normally, you may invoke the `createUuidsNormally` method: -->
`uuid` メソッドに通常の UUID 生成に戻るように指示するには、`createUuidsNormally` メソッドを呼び出します。

```php
Str::createUuidsNormally();
```

<a name="method-str-uuid7"></a>
<!-- #### `Str::uuid7()` -->
#### `Str::uuid7()`
<!-- The `Str::uuid7` method generates a UUID (version 7): -->
`Str::uuid7` メソッドは UUID (バージョン 7) を生成します。

```php
use Illuminate\Support\Str;

return (string) Str::uuid7();
```

<!-- A `DateTimeInterface` may be passed as an optional parameter which will be used to generate the ordered UUID: -->
`DateTimeInterface` は、順序付けされた UUID の生成に使用されるオプションのパラメーターとして渡すことができます。

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
<!-- #### `Str::wordCount()` -->
#### `Str::wordCount()`
<!-- The `Str::wordCount` method returns the number of words that a string contains: -->
`Str::wordCount` メソッドは、文字列に含まれる単語の数を返します。

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
<!-- #### `Str::wordWrap()` -->
#### `Str::wordWrap()`
<!-- The `Str::wordWrap` method wraps a string to a given number of characters: -->
`Str::wordWrap` メソッドは、文字列を指定された文字数にラップします。

```php
use Illuminate\Support\Str;

$text = "The quick brown fox jumped over the lazy dog."

Str::wordWrap($text, characters: 20, break: "<br />\n");

/*
The quick brown fox<br />
jumped over the lazy<br />
dog.
*/
```

<a name="method-str-words"></a>
<!-- #### `Str::words()` -->
#### `Str::words()`
<!-- The `Str::words` method limits the number of words in a string. An additional string may be passed to this method via its third argument to specify which string should be appended to the end of the truncated string: -->
`Str::words` メソッドは、文字列内の単語数を制限します。追加の文字列を 3 番目の引数を介してこのメ​​ソッドに渡し、切り詰められた文字列の末尾に追加する文字列を指定できます。

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
<!-- #### `Str::wrap()` -->
#### `Str::wrap()`
<!-- The `Str::wrap` method wraps the given string with an additional string or pair of strings: -->
`Str::wrap` メソッドは、指定された文字列を追加の文字列または文字列のペアでラップします。

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
<!-- #### `str()` -->
#### `str()`
<!-- The `str` function returns a new `Illuminate\Support\Stringable` instance of the given string. This function is equivalent to the `Str::of` method: -->
`str` 関数は、指定された文字列の新しい `Illuminate\Support\Stringable` インスタンスを返します。この関数は、`Str::of` メソッドと同等です。

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<!-- If no argument is provided to the `str` function, the function returns an instance of `Illuminate\Support\Str`: -->
`str` 関数に引数が指定されていない場合、関数は `Illuminate\Support\Str` のインスタンスを返します。

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
<!-- #### `trans()` -->
#### `trans()`
<!-- The `trans` function translates the given translation key using your [language files](/docs/12.x/localization): -->
`trans` 関数は、[language files](/docs/12.x/localization) を使用して、指定された変換キーを変換します。

```php
echo trans('messages.welcome');
```

<!-- If the specified translation key does not exist, the `trans` function will return the given key. So, using the example above, the `trans` function would return `messages.welcome` if the translation key does not exist. -->
指定された変換キーが存在しない場合、`trans` 関数は指定されたキーを返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`trans` 関数は `messages.welcome` を返します。

<a name="method-trans-choice"></a>
<!-- #### `trans_choice()` -->
#### `trans_choice()`
<!-- The `trans_choice` function translates the given translation key with inflection: -->
`trans_choice` 関数は、指定された変換キーを語形変化を使用して変換します。

```php
echo trans_choice('messages.notifications', $unreadCount);
```

<!-- If the specified translation key does not exist, the `trans_choice` function will return the given key. So, using the example above, the `trans_choice` function would return `messages.notifications` if the translation key does not exist. -->
指定された変換キーが存在しない場合、`trans_choice` 関数は指定されたキーを返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`trans_choice` 関数は `messages.notifications` を返します。

<a name="fluent-strings"></a>
<!-- ## Fluent Strings -->
## Fluent Strings

<!-- Fluent strings provide a more fluent, object-oriented interface for working with string values, allowing you to chain multiple string operations together using a more readable syntax compared to traditional string operations. -->
Fluent String は、文字列値を操作するためのより流暢なオブジェクト指向インターフェイスを提供し、従来の文字列操作と比較して読みやすい構文を使用して複数の文字列操作を連鎖させることができます。

<a name="method-fluent-str-after"></a>
<!-- #### `after` -->
#### `after`
<!-- The `after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`after` メソッドは、文字列内の指定された値以降のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
<!-- #### `afterLast` -->
#### `afterLast`
<!-- The `afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-apa"></a>
<!-- #### `apa` -->
#### `apa`
<!-- The `apa` method converts the given string to title case following the [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case): -->
`apa` メソッドは、指定された文字列を [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case) に従ってタイトルケースに変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->apa();

// A Nice Title Uses the Correct Case
```

<a name="method-fluent-str-append"></a>
<!-- #### `append` -->
#### `append`
<!-- The `append` method appends the given values to the string: -->
`append` メソッドは、指定された値を文字列に追加します。

```php
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
<!-- #### `ascii` -->
#### `ascii`
<!-- The `ascii` method will attempt to transliterate the string into an ASCII value: -->
`ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

```php
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
<!-- #### `basename` -->
#### `basename`
<!-- The `basename` method will return the trailing name component of the given string: -->
`basename` メソッドは、指定された文字列の末尾の名前コンポーネントを返します。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

<!-- If needed, you may provide an "extension" that will be removed from the trailing component: -->
必要に応じて、後続コンポーネントから削除される「拡張機能」を指定できます。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
<!-- #### `before` -->
#### `before`
<!-- The `before` method returns everything before the given value in a string: -->
`before` メソッドは、文字列内の指定された値より前のすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
<!-- #### `beforeLast` -->
#### `beforeLast`
<!-- The `beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
<!-- #### `between` -->
#### `between`
<!-- The `between` method returns the portion of a string between two values: -->
`between` メソッドは、2 つの値の間の文字列の部分を返します。

```php
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
<!-- #### `betweenFirst` -->
#### `betweenFirst`
<!-- The `betweenFirst` method returns the smallest possible portion of a string between two values: -->
`betweenFirst` メソッドは、2 つの値の間の文字列の可能な最小部分を返します。

```php
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
<!-- #### `camel` -->
#### `camel`
<!-- The `camel` method converts the given string to `camelCase`: -->
`camel` メソッドは、指定された文字列を `camelCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// 'fooBar'
```

<a name="method-fluent-str-char-at"></a>
<!-- #### `charAt` -->
#### `charAt`
<!-- The `charAt` method returns the character at the specified index. If the index is out of bounds, `false` is returned: -->
`charAt` メソッドは、指定されたインデックスの文字を返します。インデックスが範囲外の場合、`false` が返されます。

```php
use Illuminate\Support\Str;

$character = Str::of('This is my name.')->charAt(6);

// 's'
```

<a name="method-fluent-str-class-basename"></a>
<!-- #### `classBasename` -->
#### `classBasename`
<!-- The `classBasename` method returns the class name of the given class with the class's namespace removed: -->
`classBasename` メソッドは、クラスの名前空間が削除された、指定されたクラスのクラス名を返します。

```php
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// 'Baz'
```

<a name="method-fluent-str-chop-start"></a>
<!-- #### `chopStart` -->
#### `chopStart`
<!-- The `chopStart` method removes the first occurrence of the given value only if the value appears at the start of the string: -->
`chopStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopStart('https://');

// 'laravel.com'
```

<!-- You may also pass an array. If the string starts with any of the values in the array then that value will be removed from string: -->
配列を渡すこともできます。文字列が配列内のいずれかの値で始まる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopStart(['https://', 'http://']);

// 'laravel.com'
```

<a name="method-fluent-str-chop-end"></a>
<!-- #### `chopEnd` -->
#### `chopEnd`
<!-- The `chopEnd` method removes the last occurrence of the given value only if the value appears at the end of the string: -->
`chopEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopEnd('.com');

// 'https://laravel'
```

<!-- You may also pass an array. If the string ends with any of the values in the array then that value will be removed from string: -->
配列を渡すこともできます。文字列が配列内のいずれかの値で終わる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopEnd(['.com', '.io']);

// 'http://laravel'
```

<a name="method-fluent-str-contains"></a>
<!-- #### `contains` -->
#### `contains`
<!-- The `contains` method determines if the given string contains the given value. By default, this method is case sensitive: -->
`contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

<!-- You can disable case sensitivity by setting the `ignoreCase` argument to `true`: -->
大文字と小文字の区別を無効にするには、`ignoreCase` 引数を `true` に設定します。

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('MY', ignoreCase: true);

// true
```

<a name="method-fluent-str-contains-all"></a>
<!-- #### `containsAll` -->
#### `containsAll`
<!-- The `containsAll` method determines if the given string contains all of the values in the given array: -->
`containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

<!-- You can disable case sensitivity by setting the `ignoreCase` argument to `true`: -->
大文字と小文字の区別を無効にするには、`ignoreCase` 引数を `true` に設定します。

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-fluent-str-decrypt"></a>
<!-- #### `decrypt` -->
#### `decrypt`
<!-- The `decrypt` method [decrypts](/docs/12.x/encryption) the encrypted string: -->
`decrypt` メソッドは、暗号化された文字列を[decrypts](/docs/12.x/encryption)します。

```php
use Illuminate\Support\Str;

$decrypted = $encrypted->decrypt();

// 'secret'
```

<!-- For the inverse of `decrypt`, see the [encrypt](#method-fluent-str-encrypt) method. -->
`decrypt` の逆については、[encrypt](#method-fluent-str-encrypt) メソッドを参照してください。

<a name="method-fluent-str-deduplicate"></a>
<!-- #### `deduplicate` -->
#### `deduplicate`
<!-- The `deduplicate` method replaces consecutive instances of a character with a single instance of that character in the given string. By default, the method deduplicates spaces: -->
`deduplicate` メソッドは、指定された文字列内の文字の連続したインスタンスをその文字の単一のインスタンスに置き換えます。デフォルトでは、このメソッドはスペースを重複排除します。

```php
use Illuminate\Support\Str;

$result = Str::of('The   Laravel   Framework')->deduplicate();

// The Laravel Framework
```

<!-- You may specify a different character to deduplicate by passing it in as the second argument to the method: -->
重複排除する別の文字を指定するには、それをメソッドの 2 番目の引数として渡します。

```php
use Illuminate\Support\Str;

$result = Str::of('The---Laravel---Framework')->deduplicate('-');

// The-Laravel-Framework
```

<a name="method-fluent-str-dirname"></a>
<!-- #### `dirname` -->
#### `dirname`
<!-- The `dirname` method returns the parent directory portion of the given string: -->
`dirname` メソッドは、指定された文字列の親ディレクトリ部分を返します。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

<!-- If necessary, you may specify how many directory levels you wish to trim from the string: -->
必要に応じて、文字列から削除するディレクトリ レベルの数を指定できます。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-doesnt-contain"></a>
<!-- #### `doesntContain()` -->
#### `doesntContain()`
<!-- The `doesntContain` method determines if the given string does not contain the given value. This method is the inverse of the [contains](#method-fluent-str-contains) method. By default, this method is case sensitive: -->
`doesntContain` メソッドは、指定された文字列に指定された値が含まれていないかどうかを判断します。このメソッドは、[contains](#method-fluent-str-contains) メソッドの逆です。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain('my');

// true
```

<!-- You may also pass an array of values to determine if the given string does not contain any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれていないかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain(['my', 'framework']);

// true
```

<!-- You may disable case sensitivity by setting the `ignoreCase` argument to `true`: -->
`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is my name')->doesntContain('MY', ignoreCase: true);

// false
```

<a name="method-fluent-str-doesnt-end-with"></a>
<!-- #### `doesntEndWith` -->
#### `doesntEndWith`
<!-- The `doesntEndWith` method determines if the given string doesn't end with the given value: -->
`doesntEndWith` メソッドは、指定された文字列が指定された値で終わっていないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith('dog');

// true
```

<!-- You may also pass an array of values to determine if the given string doesn't end with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のどの値でも終わっていないかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith(['this', 'foo']);

// true

$result = Str::of('This is my name')->doesntEndWith(['name', 'foo']);

// false
```

<a name="method-fluent-str-doesnt-start-with"></a>
<!-- #### `doesntStartWith` -->
#### `doesntStartWith`
<!-- The `doesntStartWith` method determines if the given string doesn't begin with the given value: -->
`doesntStartWith` メソッドは、指定された文字列が指定された値で始まらないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith('That');

// true
```

<!-- You may also pass an array of values to determine if the given string doesn't start with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のどの値でも始まらないかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith(['What', 'That', 'There']);

// true
```

<a name="method-fluent-str-encrypt"></a>
<!-- #### `encrypt` -->
#### `encrypt`
<!-- The `encrypt` method [encrypts](/docs/12.x/encryption) the string: -->
`encrypt` メソッドは、文字列を[encrypts](/docs/12.x/encryption)します。

```php
use Illuminate\Support\Str;

$encrypted = Str::of('secret')->encrypt();
```

<!-- For the inverse of `encrypt`, see the [decrypt](#method-fluent-str-decrypt) method. -->
`encrypt` の逆については、[decrypt](#method-fluent-str-decrypt) メソッドを参照してください。

<a name="method-fluent-str-ends-with"></a>
<!-- #### `endsWith` -->
#### `endsWith`
<!-- The `endsWith` method determines if the given string ends with the given value: -->
`endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

```php
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
`exactly` メソッドは、指定された文字列が別の文字列と完全に一致するかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-excerpt"></a>
<!-- #### `excerpt` -->
#### `excerpt`
<!-- The `excerpt` method extracts an excerpt from the string that matches the first instance of a phrase within that string: -->
`excerpt` メソッドは、文字列内のフレーズの最初のインスタンスに一致する文字列からの抜粋を抽出します。

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

<!-- The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string. -->
`radius` オプション (デフォルトは `100`) を使用すると、切り詰められた文字列の両側に表示される文字数を定義できます。

<!-- In addition, you may use the `omission` option to change the string that will be prepended and appended to the truncated string: -->
さらに、`omission` オプションを使用して、切り詰められた文字列の前後に追加される文字列を変更することもできます。

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-fluent-str-explode"></a>
<!-- #### `explode` -->
#### `explode`
<!-- The `explode` method splits the string by the given delimiter and returns a collection containing each section of the split string: -->
`explode` メソッドは、指定された区切り文字で文字列を分割し、分割された文字列の各セクションを含むコレクションを返します。

```php
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
<!-- #### `finish` -->
#### `finish`
<!-- The `finish` method adds a single instance of the given value to a string if it does not already end with that value: -->
`finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-from-base64"></a>
<!-- #### `fromBase64` -->
#### `fromBase64`
<!-- The `fromBase64` method decodes the given Base64 string: -->
`fromBase64` メソッドは、指定された Base64 文字列をデコードします。

```php
use Illuminate\Support\Str;

$decoded = Str::of('TGFyYXZlbA==')->fromBase64();

// Laravel
```

<a name="method-fluent-str-hash"></a>
<!-- #### `hash` -->
#### `hash`
<!-- The `hash` method hashes the string using the given [algorithm](https://www.php.net/manual/en/function.hash-algos.php): -->
`hash` メソッドは、指定された [algorithm](https://www.php.net/manual/en/function.hash-algos.php) を使用して文字列をハッシュします。

```php
use Illuminate\Support\Str;

$hashed = Str::of('secret')->hash(algorithm: 'sha256');

// '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
```

<a name="method-fluent-str-headline"></a>
<!-- #### `headline` -->
#### `headline`
<!-- The `headline` method will convert strings delimited by casing, hyphens, or underscores into a space delimited string with each word's first letter capitalized: -->
`headline` メソッドは、大文字と小文字、ハイフン、またはアンダースコアで区切られた文字列を、各単語の最初の文字が大文字になったスペースで区切られた文字列に変換します。

```php
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-initials"></a>
<!-- #### `initials` -->
#### `initials`
<!-- The `initials` method will convert the string to its initials: -->
`initials` メソッドは文字列をそのイニシャルに変換します。

```php
use Illuminate\Support\Str;

$initials = Str::of('Taylor Otwell')->initials()->upper();

// TO
```

<a name="method-fluent-str-inline-markdown"></a>
<!-- #### `inlineMarkdown` -->
#### `inlineMarkdown`
<!-- The `inlineMarkdown` method converts GitHub flavored Markdown into inline HTML using [CommonMark](https://commonmark.thephpleague.com/). However, unlike the `markdown` method, it does not wrap all generated HTML in a block-level element: -->
`inlineMarkdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown をインライン HTML に変換します。ただし、`markdown` メソッドとは異なり、生成されたすべての HTML をブロックレベル要素でラップするわけではありません。

```php
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

<!-- #### Markdown Security -->
#### Markdown Security

<!-- By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier: -->
デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark Security documentation](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->inlineMarkdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-fluent-str-is"></a>
<!-- #### `is` -->
#### `is`
<!-- The `is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values -->
`is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます

```php
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
`isAscii` メソッドは、指定された文字列が ASCII 文字列であるかどうかを判断します。

```php
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
`isEmpty` メソッドは、指定された文字列が空かどうかを判断します。

```php
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
`isNotEmpty` メソッドは、指定された文字列が空でないかどうかを判断します。

```php
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
`isJson` メソッドは、指定された文字列が有効な JSON かどうかを判断します。

```php
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
`isUlid` メソッドは、指定された文字列が ULID であるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-url"></a>
<!-- #### `isUrl` -->
#### `isUrl`
<!-- The `isUrl` method determines if a given string is a URL: -->
`isUrl` メソッドは、指定された文字列が URL かどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('http://example.com')->isUrl();

// true

$result = Str::of('Taylor')->isUrl();

// false
```

<!-- The `isUrl` method considers a wide range of protocols as valid. However, you may specify the protocols that should be considered valid by providing them to the `isUrl` method: -->
`isUrl` メソッドは、幅広いプロトコルを有効であるとみなします。ただし、`isUrl` メソッドにプロトコルを指定することで、有効であるとみなされるプロトコルを指定できます。

```php
$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

<a name="method-fluent-str-is-uuid"></a>
<!-- #### `isUuid` -->
#### `isUuid`
<!-- The `isUuid` method determines if a given string is a UUID: -->
`isUuid` メソッドは、指定された文字列が UUID かどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

<!-- You may also validate that the given UUID matches a UUID specification by version (1, 3, 4, 5, 6, 7, or 8): -->
指定された UUID がバージョン (1、3、4、5、6、7、または 8) ごとの UUID 仕様と一致することを検証することもできます。

```php
use Illuminate\Support\Str;

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 4);

// true

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 1);

// false
```

<a name="method-fluent-str-kebab"></a>
<!-- #### `kebab` -->
#### `kebab`
<!-- The `kebab` method converts the given string to `kebab-case`: -->
`kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
<!-- #### `lcfirst` -->
#### `lcfirst`
<!-- The `lcfirst` method returns the given string with the first character lowercased: -->
`lcfirst` メソッドは、最初の文字を小文字にして指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```

<a name="method-fluent-str-length"></a>
<!-- #### `length` -->
#### `length`
<!-- The `length` method returns the length of the given string: -->
`length` メソッドは、指定された文字列の長さを返します。

```php
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
<!-- #### `limit` -->
#### `limit`
<!-- The `limit` method truncates the given string to the specified length: -->
`limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

```php
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

<!-- You may also pass a second argument to change the string that will be appended to the end of the truncated string: -->
2 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更することもできます。

```php
$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

<!-- If you would like to preserve complete words when truncating the string, you may utilize the `preserveWords` argument. When this argument is `true`, the string will be truncated to the nearest complete word boundary: -->
文字列を切り詰めるときに完全な単語を保持したい場合は、`preserveWords` 引数を利用できます。この引数が `true` の場合、文字列は最も近い完全な単語境界まで切り詰められます。

```php
$truncated = Str::of('The quick brown fox')->limit(12, preserveWords: true);

// The quick...
```

<a name="method-fluent-str-lower"></a>
<!-- #### `lower` -->
#### `lower`
<!-- The `lower` method converts the given string to lowercase: -->
`lower` メソッドは、指定された文字列を小文字に変換します。

```php
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-markdown"></a>
<!-- #### `markdown` -->
#### `markdown`
<!-- The `markdown` method converts GitHub flavored Markdown into HTML: -->
`markdown` メソッドは、GitHub フレーバーの Markdown を HTML に変換します。

```php
use Illuminate\Support\Str;

$html = Str::of('# Laravel')->markdown();

// <h1>Laravel</h1>

$html = Str::of('# Taylor <b>Otwell</b>')->markdown([
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

<!-- #### Markdown Security -->
#### Markdown Security

<!-- By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier: -->
デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark Security documentation](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->markdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-fluent-str-mask"></a>
<!-- #### `mask` -->
#### `mask`
<!-- The `mask` method masks a portion of a string with a repeated character, and may be used to obfuscate segments of strings such as email addresses and phone numbers: -->
`mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

```php
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

<!-- If needed, you may provide negative numbers as the third or fourth argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
必要に応じて、`mask` メソッドの 3 番目または 4 番目の引数として負の数値を指定できます。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

```php
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
<!-- #### `match` -->
#### `match`
<!-- The `match` method will return the portion of a string that matches a given regular expression pattern: -->
`match` メソッドは、指定された正規表現パターンに一致する文字列の部分を返します。

```php
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
`matchAll` メソッドは、指定された正規表現パターンに一致する文字列の部分を含むコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

<!-- If you specify a matching group within the expression, Laravel will return a collection of the first matching group's matches: -->
式内で一致するグループを指定すると、Laravel は最初に一致したグループの一致のコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

<!-- If no matches are found, an empty collection will be returned. -->
一致するものが見つからない場合は、空のコレクションが返されます。

<a name="method-fluent-str-is-match"></a>
<!-- #### `isMatch` -->
#### `isMatch`
<!-- The `isMatch` method will return `true` if the string matches a given regular expression: -->
文字列が指定された正規表現に一致する場合、`isMatch` メソッドは `true` を返します。

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->isMatch('/foo (.*)/');

// true

$result = Str::of('laravel')->isMatch('/foo (.*)/');

// false
```

<a name="method-fluent-str-new-line"></a>
<!-- #### `newLine` -->
#### `newLine`
<!-- The `newLine` method appends an "end of line" character to a string: -->
`newLine` メソッドは、文字列に「行末」文字を追加します。

```php
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
<!-- #### `padBoth` -->
#### `padBoth`
<!-- The `padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches the desired length: -->
`padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

```php
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
`padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

```php
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
`padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

```php
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
`pipe` メソッドを使用すると、現在の値を指定された呼び出し可能オブジェクトに渡すことで文字列を変換できます。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$hash = Str::of('Laravel')->pipe('md5')->prepend('Checksum: ');

// 'Checksum: a5c95b86291ea299fcbe64458ed12702'

$closure = Str::of('foo')->pipe(function (Stringable $str) {
    return 'bar';
});

// 'bar'
```

<a name="method-fluent-str-plural"></a>
<!-- #### `plural` -->
#### `plural`
<!-- The `plural` method converts a singular word string to its plural form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language): -->
`plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

<!-- You may provide an integer argument to the function to retrieve the singular or plural form of the string: -->
関数に整数の引数を指定して、文字列の単数形または複数形を取得できます。

```php
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

<!-- You may provide the `prependCount` argument to prefix the pluralized string with the formatted `$count`: -->
`prependCount` 引数を指定して、書式設定された `$count` を複数化された文字列の前に付けることができます。

```php
use Illuminate\Support\Str;

$label = Str::of('car')->plural(1000, prependCount: true);

// 1,000 cars
```

<a name="method-fluent-str-position"></a>
<!-- #### `position` -->
#### `position`
<!-- The `position` method returns the position of the first occurrence of a substring in a string. If the substring does not exist within the string, `false` is returned: -->
`position` メソッドは、文字列内で最初に出現する部分文字列の位置を返します。文字列内に部分文字列が存在しない場合は、`false` が返されます。

```php
use Illuminate\Support\Str;

$position = Str::of('Hello, World!')->position('Hello');

// 0

$position = Str::of('Hello, World!')->position('W');

// 7
```

<a name="method-fluent-str-prepend"></a>
<!-- #### `prepend` -->
#### `prepend`
<!-- The `prepend` method prepends the given values onto the string: -->
`prepend` メソッドは、指定された値を文字列の先頭に追加します。

```php
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
<!-- #### `remove` -->
#### `remove`
<!-- The `remove` method removes the given value or array of values from the string: -->
`remove` メソッドは、指定された値または値の配列を文字列から削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite ');

// Arkansas is beautiful!
```

<!-- You may also pass `false` as a second parameter to ignore case when removing strings. -->
文字列を削除するときに大文字と小文字を区別しないように、2 番目のパラメーターとして `false` を渡すこともできます。

<a name="method-fluent-str-repeat"></a>
<!-- #### `repeat` -->
#### `repeat`
<!-- The `repeat` method repeats the given string: -->
`repeat` メソッドは、指定された文字列を繰り返します。

```php
use Illuminate\Support\Str;

$repeated = Str::of('a')->repeat(5);

// aaaaa
```

<a name="method-fluent-str-replace"></a>
<!-- #### `replace` -->
#### `replace`
<!-- The `replace` method replaces a given string within the string: -->
`replace` メソッドは、文字列内の指定された文字列を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

<!-- The `replace` method also accepts a `caseSensitive` argument. By default, the `replace` method is case sensitive: -->
`replace` メソッドは、`caseSensitive` 引数も受け入れます。デフォルトでは、`replace` メソッドでは大文字と小文字が区別されます。

```php
$replaced = Str::of('macOS 13.x')->replace(
    'macOS', 'iOS', caseSensitive: false
);
```

<a name="method-fluent-str-replace-array"></a>
<!-- #### `replaceArray` -->
#### `replaceArray`
<!-- The `replaceArray` method replaces a given value in the string sequentially using an array: -->
`replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
<!-- #### `replaceFirst` -->
#### `replaceFirst`
<!-- The `replaceFirst` method replaces the first occurrence of a given value in a string: -->
`replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
<!-- #### `replaceLast` -->
#### `replaceLast`
<!-- The `replaceLast` method replaces the last occurrence of a given value in a string: -->
`replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
<!-- #### `replaceMatches` -->
#### `replaceMatches`
<!-- The `replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string: -->
`replaceMatches` メソッドは、パターンに一致する文字列のすべての部分を指定された置換文字列に置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

<!-- The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value: -->
`replaceMatches` メソッドは、指定されたパターンに一致する文字列の各部分で呼び出されるクロージャも受け入れます。これにより、クロージャ内で置換ロジックを実行し、置換された値を返すことができます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-replace-start"></a>
<!-- #### `replaceStart` -->
#### `replaceStart`
<!-- The `replaceStart` method replaces the first occurrence of the given value only if the value appears at the start of the string: -->
`replaceStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceStart('Hello', 'Laravel');

// Laravel World

$replaced = Str::of('Hello World')->replaceStart('World', 'Laravel');

// Hello World
```

<a name="method-fluent-str-replace-end"></a>
<!-- #### `replaceEnd` -->
#### `replaceEnd`
<!-- The `replaceEnd` method replaces the last occurrence of the given value only if the value appears at the end of the string: -->
`replaceEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

// Hello Laravel

$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

// Hello World
```

<a name="method-fluent-str-scan"></a>
<!-- #### `scan` -->
#### `scan`
<!-- The `scan` method parses input from a string into a collection according to a format supported by the [`sscanf` PHP function](https://www.php.net/manual/en/function.sscanf.php): -->
`scan` メソッドは、[`sscanf` PHP function](https://www.php.net/manual/en/function.sscanf.php) でサポートされている形式に従って、文字列からの入力を解析してコレクションに入れます。

```php
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
<!-- #### `singular` -->
#### `singular`
<!-- The `singular` method converts a string to its singular form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language): -->
`singular` メソッドは、文字列を単数形に変換します。この関数は [any of the languages supported by Laravel's pluralizer](/docs/12.x/localization#pluralization-language) をサポートします。

```php
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
`slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

```php
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
<!-- #### `snake` -->
#### `snake`
<!-- The `snake` method converts the given string to `snake_case`: -->
`snake` メソッドは、指定された文字列を `snake_case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
<!-- #### `split` -->
#### `split`
<!-- The `split` method splits a string into a collection using a regular expression: -->
`split` メソッドは、正規表現を使用して文字列をコレクションに分割します。

```php
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
<!-- #### `squish` -->
#### `squish`
<!-- The `squish` method removes all extraneous white space from a string, including extraneous white space between words: -->
`squish` メソッドは、単語間の無関係な空白を含め、文字列から無関係な空白をすべて削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
<!-- #### `start` -->
#### `start`
<!-- The `start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

```php
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
`startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

<!-- You may also pass an array of values to determine if the given string starts with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のいずれかの値で始まるかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith(['This', 'That']);

// true
```

<a name="method-fluent-str-strip-tags"></a>
<!-- #### `stripTags` -->
#### `stripTags`
<!-- The `stripTags` method removes all HTML and PHP tags from a string: -->
`stripTags` メソッドは、文字列からすべての HTML タグと PHP タグを削除します。

```php
use Illuminate\Support\Str;

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags();

// Taylor Otwell

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags('<b>');

// Taylor <b>Otwell</b>
```

<a name="method-fluent-str-studly"></a>
<!-- #### `studly` -->
#### `studly`
<!-- The `studly` method converts the given string to `StudlyCase`: -->
`studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
<!-- #### `substr` -->
#### `substr`
<!-- The `substr` method returns the portion of the string specified by the given start and length parameters: -->
`substr` メソッドは、指定された start パラメーターと length パラメーターで指定された文字列の部分を返します。

```php
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
`substrReplace` メソッドは、文字列の一部内のテキストを、2 番目の引数で指定された位置から開始して、3 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 3 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

```php
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
`swap` メソッドは、PHP の `strtr` 関数を使用して文字列内の複数の値を置き換えます。

```php
use Illuminate\Support\Str;

$string = Str::of('Tacos are great!')
    ->swap([
        'Tacos' => 'Burritos',
        'great' => 'fantastic',
    ]);

// Burritos are fantastic!
```

<a name="method-fluent-str-take"></a>
<!-- #### `take` -->
#### `take`
<!-- The `take` method returns a specified number of characters from the beginning of the string: -->
`take` メソッドは、文字列の先頭から指定された数の文字を返します。

```php
use Illuminate\Support\Str;

$taken = Str::of('Build something amazing!')->take(5);

// Build
```

<a name="method-fluent-str-tap"></a>
<!-- #### `tap` -->
#### `tap`
<!-- The `tap` method passes the string to the given closure, allowing you to examine and interact with the string while not affecting the string itself. The original string is returned by the `tap` method regardless of what is returned by the closure: -->
`tap` メソッドは文字列を指定されたクロージャに渡します。これにより、文字列自体には影響を与えずに、文字列を調べて操作できるようになります。クロージャによって何が返されるかに関係なく、元の文字列が `tap` メソッドによって返されます。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Laravel')
    ->append(' Framework')
    ->tap(function (Stringable $string) {
        dump('String after append: '.$string);
    })
    ->upper();

// LARAVEL FRAMEWORK
```

<a name="method-fluent-str-test"></a>
<!-- #### `test` -->
#### `test`
<!-- The `test` method determines if a string matches the given regular expression pattern: -->
`test` メソッドは、文字列が指定された正規表現パターンに一致するかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
<!-- #### `title` -->
#### `title`
<!-- The `title` method converts the given string to `Title Case`: -->
`title` メソッドは、指定された文字列を `Title Case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-to-base64"></a>
<!-- #### `toBase64` -->
#### `toBase64`
<!-- The `toBase64` method converts the given string to Base64: -->
`toBase64` メソッドは、指定された文字列を Base64 に変換します。

```php
use Illuminate\Support\Str;

$base64 = Str::of('Laravel')->toBase64();

// TGFyYXZlbA==
```

<a name="method-fluent-str-to-html-string"></a>
<!-- #### `toHtmlString` -->
#### `toHtmlString`
<!-- The `toHtmlString` method converts the given string to an instance of `Illuminate\Support\HtmlString`, which will not be escaped when rendered in Blade templates: -->
`toHtmlString` メソッドは、指定された文字列を `Illuminate\Support\HtmlString` のインスタンスに変換します。これは、Blade テンプレートでレンダリングされるときにエスケープされません。

```php
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-fluent-str-to-uri"></a>
<!-- #### `toUri` -->
#### `toUri`
<!-- The `toUri` method converts the given string to an instance of [Illuminate\Support\Uri](/docs/12.x/helpers#uri): -->
`toUri` メソッドは、指定された文字列を [Illuminate\Support\Uri](/docs/12.x/helpers#uri) のインスタンスに変換します。

```php
use Illuminate\Support\Str;

$uri = Str::of('https://example.com')->toUri();
```

<a name="method-fluent-str-transliterate"></a>
<!-- #### `transliterate` -->
#### `transliterate`
<!-- The `transliterate` method will attempt to convert a given string into its closest ASCII representation: -->
`transliterate` メソッドは、指定された文字列を最も近い ASCII 表現に変換しようとします。

```php
use Illuminate\Support\Str;

$email = Str::of('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ')->transliterate()

// 'test@laravel.com'
```

<a name="method-fluent-str-trim"></a>
<!-- #### `trim` -->
#### `trim`
<!-- The `trim` method trims the given string. Unlike PHP's native `trim` function, Laravel's `trim` method also removes unicode whitespace characters: -->
`trim` メソッドは、指定された文字列をトリミングします。 PHP のネイティブ `trim` 関数とは異なり、Laravel の `trim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ltrim"></a>
<!-- #### `ltrim` -->
#### `ltrim`
<!-- The `ltrim` method trims the left side of the string. Unlike PHP's native `ltrim` function, Laravel's `ltrim` method also removes unicode whitespace characters: -->
`ltrim` メソッドは、文字列の左側をトリミングします。 PHP のネイティブ `ltrim` 関数とは異なり、Laravel の `ltrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```

<a name="method-fluent-str-rtrim"></a>
<!-- #### `rtrim` -->
#### `rtrim`
<!-- The `rtrim` method trims the right side of the given string. Unlike PHP's native `rtrim` function, Laravel's `rtrim` method also removes unicode whitespace characters: -->
`rtrim` メソッドは、指定された文字列の右側をトリミングします。 PHP のネイティブ `rtrim` 関数とは異なり、Laravel の `rtrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
<!-- #### `ucfirst` -->
#### `ucfirst`
<!-- The `ucfirst` method returns the given string with the first character capitalized: -->
`ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
<!-- #### `ucsplit` -->
#### `ucsplit`
<!-- The `ucsplit` method splits the given string into a collection by uppercase characters: -->
`ucsplit` メソッドは、指定された文字列を大文字でコレクションに分割します。

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo ', 'Bar'])
```

<a name="method-fluent-str-ucwords"></a>
<!-- #### `ucwords` -->
#### `ucwords`
<!-- The `ucwords` method converts the first character of each word in the given string to uppercase: -->
`ucwords` メソッドは、指定された文字列内の各単語の最初の文字を大文字に変換します。

```php
use Illuminate\Support\Str;

$string = Str::of('laravel framework')->ucwords();

// Laravel Framework
```

<a name="method-fluent-str-unwrap"></a>
<!-- #### `unwrap` -->
#### `unwrap`
<!-- The `unwrap` method removes the specified strings from the beginning and end of a given string: -->
`unwrap` メソッドは、指定された文字列の先頭と末尾から指定された文字列を削除します。

```php
use Illuminate\Support\Str;

Str::of('-Laravel-')->unwrap('-');

// Laravel

Str::of('{framework: "Laravel"}')->unwrap('{', '}');

// framework: "Laravel"
```

<a name="method-fluent-str-upper"></a>
<!-- #### `upper` -->
#### `upper`
<!-- The `upper` method converts the given string to uppercase: -->
`upper` メソッドは、指定された文字列を大文字に変換します。

```php
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
<!-- #### `when` -->
#### `when`
<!-- The `when` method invokes the given closure if a given condition is `true`. The closure will receive the fluent string instance: -->
`when` メソッドは、指定された条件が `true` の場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Taylor')
    ->when(true, function (Stringable $string) {
        return $string->append(' Otwell');
    });

// 'Taylor Otwell'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the condition parameter evaluates to `false`. -->
必要に応じて、別のクロージャを 3 番目のパラメータとして `when` メソッドに渡すことができます。このクロージャは、条件パラメータが `false` と評価された場合に実行されます。

<a name="method-fluent-str-when-contains"></a>
<!-- #### `whenContains` -->
#### `whenContains`
<!-- The `whenContains` method invokes the given closure if the string contains the given value. The closure will receive the fluent string instance: -->
`whenContains` メソッドは、文字列に指定された値が含まれている場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains('tony', function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter. The closure will be invoked if the string does not contain the given value. -->
必要に応じて、別のクロージャを 3 番目のパラメータとして渡すことができます。文字列に指定された値が含まれていない場合、クロージャが呼び出されます。

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains(['tony', 'hulk'], function (Stringable $string) {
        return $string->title();
    });

// Tony Stark
```

<a name="method-fluent-str-when-contains-all"></a>
<!-- #### `whenContainsAll` -->
#### `whenContainsAll`
<!-- The `whenContainsAll` method invokes the given closure if the string contains all of the given sub-strings. The closure will receive the fluent string instance: -->
`whenContainsAll` メソッドは、文字列に指定されたサブ文字列がすべて含まれている場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContainsAll(['tony', 'stark'], function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter. The closure will be invoked if the condition parameter evaluates to `false`. -->
必要に応じて、別のクロージャを 3 番目のパラメータとして渡すことができます。条件パラメータが `false` と評価された場合、クロージャが呼び出されます。

<a name="method-fluent-str-when-doesnt-end-with"></a>
<!-- #### `whenDoesntEndWith` -->
#### `whenDoesntEndWith`
<!-- The `whenDoesntEndWith` method invokes the given closure if the string doesn't end with the given sub-string. The closure will receive the fluent string instance: -->
`whenDoesntEndWith` メソッドは、文字列が指定された部分文字列で終わっていない場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenDoesntEndWith('land', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-doesnt-start-with"></a>
<!-- #### `whenDoesntStartWith` -->
#### `whenDoesntStartWith`
<!-- The `whenDoesntStartWith` method invokes the given closure if the string doesn't start with the given sub-string. The closure will receive the fluent string instance: -->
`whenDoesntStartWith` メソッドは、文字列が指定された部分文字列で始まらない場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenDoesntStartWith('sea', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-empty"></a>
<!-- #### `whenEmpty` -->
#### `whenEmpty`
<!-- The `whenEmpty` method invokes the given closure if the string is empty. If the closure returns a value, that value will also be returned by the `whenEmpty` method. If the closure does not return a value, the fluent string instance will be returned: -->
`whenEmpty` メソッドは、文字列が空の場合、指定されたクロージャを呼び出します。クロージャが値を返す場合、その値は `whenEmpty` メソッドによっても返されます。クロージャが値を返さない場合は、流暢な文字列インスタンスが返されます。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('  ')->trim()->whenEmpty(function (Stringable $string) {
    return $string->prepend('Laravel');
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-empty"></a>
<!-- #### `whenNotEmpty` -->
#### `whenNotEmpty`
<!-- The `whenNotEmpty` method invokes the given closure if the string is not empty. If the closure returns a value, that value will also be returned by the `whenNotEmpty` method. If the closure does not return a value, the fluent string instance will be returned: -->
文字列が空でない場合、`whenNotEmpty` メソッドは指定されたクロージャを呼び出します。クロージャが値を返す場合、その値は `whenNotEmpty` メソッドによっても返されます。クロージャが値を返さない場合は、流暢な文字列インスタンスが返されます。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Framework')->whenNotEmpty(function (Stringable $string) {
    return $string->prepend('Laravel ');
});

// 'Laravel Framework'
```

<a name="method-fluent-str-when-starts-with"></a>
<!-- #### `whenStartsWith` -->
#### `whenStartsWith`
<!-- The `whenStartsWith` method invokes the given closure if the string starts with the given sub-string. The closure will receive the fluent string instance: -->
`whenStartsWith` メソッドは、文字列が指定された部分文字列で始まる場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenStartsWith('disney', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-ends-with"></a>
<!-- #### `whenEndsWith` -->
#### `whenEndsWith`
<!-- The `whenEndsWith` method invokes the given closure if the string ends with the given sub-string. The closure will receive the fluent string instance: -->
`whenEndsWith` メソッドは、文字列が指定された部分文字列で終わる場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenEndsWith('world', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-exactly"></a>
<!-- #### `whenExactly` -->
#### `whenExactly`
<!-- The `whenExactly` method invokes the given closure if the string exactly matches the given string. The closure will receive the fluent string instance: -->
`whenExactly` メソッドは、文字列が指定された文字列と正確に一致する場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-exactly"></a>
<!-- #### `whenNotExactly` -->
#### `whenNotExactly`
<!-- The `whenNotExactly` method invokes the given closure if the string does not exactly match the given string. The closure will receive the fluent string instance: -->
`whenNotExactly` メソッドは、文字列が指定された文字列と正確に一致しない場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('framework')->whenNotExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Framework'
```

<a name="method-fluent-str-when-is"></a>
<!-- #### `whenIs` -->
#### `whenIs`
<!-- The `whenIs` method invokes the given closure if the string matches a given pattern. Asterisks may be used as wildcard values. The closure will receive the fluent string instance: -->
`whenIs` メソッドは、文字列が指定されたパターンに一致する場合に、指定されたクロージャを呼び出します。アスタリスクはワイルドカード値として使用できます。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('foo/bar')->whenIs('foo/*', function (Stringable $string) {
    return $string->append('/baz');
});

// 'foo/bar/baz'
```

<a name="method-fluent-str-when-is-ascii"></a>
<!-- #### `whenIsAscii` -->
#### `whenIsAscii`
<!-- The `whenIsAscii` method invokes the given closure if the string is 7 bit ASCII. The closure will receive the fluent string instance: -->
文字列が 7 ビット ASCII の場合、`whenIsAscii` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenIsAscii(function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is-ulid"></a>
<!-- #### `whenIsUlid` -->
#### `whenIsUlid`
<!-- The `whenIsUlid` method invokes the given closure if the string is a valid ULID. The closure will receive the fluent string instance: -->
文字列が有効な ULID の場合、`whenIsUlid` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
<!-- #### `whenIsUuid` -->
#### `whenIsUuid`
<!-- The `whenIsUuid` method invokes the given closure if the string is a valid UUID. The closure will receive the fluent string instance: -->
文字列が有効な UUID の場合、`whenIsUuid` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// 'a0a2a2d2'
```

<a name="method-fluent-str-when-test"></a>
<!-- #### `whenTest` -->
#### `whenTest`
<!-- The `whenTest` method invokes the given closure if the string matches the given regular expression. The closure will receive the fluent string instance: -->
`whenTest` メソッドは、文字列が指定された正規表現と一致する場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel framework')->whenTest('/laravel/', function (Stringable $string) {
    return $string->title();
});

// 'Laravel Framework'
```

<a name="method-fluent-str-word-count"></a>
<!-- #### `wordCount` -->
#### `wordCount`
<!-- The `wordCount` method returns the number of words that a string contains: -->
`wordCount` メソッドは、文字列に含まれる単語の数を返します。

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
<!-- #### `words` -->
#### `words`
<!-- The `words` method limits the number of words in a string. If necessary, you may specify an additional string that will be appended to the truncated string: -->
`words` メソッドは、文字列内の単語数を制限します。必要に応じて、切り詰められた文字列に追加される追加の文字列を指定できます。

```php
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-fluent-str-wrap"></a>
<!-- #### `wrap` -->
#### `wrap`
<!-- The `wrap` method wraps the given string with an additional string or pair of strings: -->
`wrap` メソッドは、指定された文字列を追加の文字列または文字列のペアでラップします。

```php
use Illuminate\Support\Str;

Str::of('Laravel')->wrap('"');

// "Laravel"

Str::is('is')->wrap(before: 'This ', after: ' Laravel!');

// This is Laravel!
```

