<!-- # Strings -->
# Strings

- [Introduction](#introduction)
- [Available Methods](#available-methods)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel includes a variety of functions for manipulating string values. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient. -->
Laravel은 문자열 값을 조작할 수 있는 다양한 함수를 제공합니다. 이 함수들 중 상당수는 프레임워크 내부적으로도 사용되고 있지만, 여러분이 필요하다고 생각한다면 언제든지 자신의 애플리케이션에서도 자유롭게 활용할 수 있습니다.

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
[Str::isUrl](#method-str-is-url)
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
[Str::toHtmlString](#method-str-to-html-string)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::unwrap](#method-str-unwrap)
[Str::uuid](#method-str-uuid)
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
[Str::isUrl](#method-str-is-url)
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
[Str::toHtmlString](#method-str-to-html-string)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::unwrap](#method-str-unwrap)
[Str::uuid](#method-str-uuid)
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
[isUrl](#method-fluent-str-is-url)
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
[rtrim](#method-fluent-str-rtrim)
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
[trim](#method-fluent-str-trim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[unwrap](#method-fluent-str-unwrap)
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
[isUrl](#method-fluent-str-is-url)
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
[rtrim](#method-fluent-str-rtrim)
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
[trim](#method-fluent-str-trim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[unwrap](#method-fluent-str-unwrap)
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

<a name="strings"></a>
<!-- ## Strings -->
## Strings

<a name="method-__"></a>
<!-- #### `__()` -->
#### `__()`

<!-- The `__` function translates the given translation string or translation key using your [language files](/docs/10.x/localization): -->
`__` 함수는 주어진 번역 문자열 또는 번역 키를 [language files](/docs/10.x/localization)을 사용해 번역합니다.

```
echo __('Welcome to our application');

echo __('messages.welcome');
```

<!-- If the specified translation string or key does not exist, the `__` function will return the given value. So, using the example above, the `__` function would return `messages.welcome` if that translation key does not exist. -->
만약 지정한 번역 문자열이나 키가 존재하지 않는 경우, `__` 함수는 전달된 값을 그대로 반환합니다. 즉, 위의 예시에서 messages.welcome이라는 번역 키가 존재하지 않으면 `__` 함수는 `messages.welcome`을 그대로 반환합니다.

<a name="method-class-basename"></a>
<!-- #### `class_basename()` -->
#### `class_basename()`

<!-- The `class_basename` function returns the class name of the given class with the class's namespace removed: -->
`class_basename` 함수는 넘겨준 클래스에서 네임스페이스를 제외한 클래스명만 반환합니다.

```
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
<!-- #### `e()` -->
#### `e()`

<!-- The `e` function runs PHP's `htmlspecialchars` function with the `double_encode` option set to `true` by default: -->
`e` 함수는 PHP의 `htmlspecialchars` 함수에 `double_encode` 옵션을 기본값 `true`로 하여 실행합니다.

```
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
<!-- #### `preg_replace_array()` -->
#### `preg_replace_array()`

<!-- The `preg_replace_array` function replaces a given pattern in the string sequentially using an array: -->
`preg_replace_array` 함수는 문자열 내에서 지정한 패턴에 일치하는 부분을 주어진 배열의 값들로 순차적으로 치환합니다.

```
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
<!-- #### `Str::after()` -->
#### `Str::after()`

<!-- The `Str::after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::after` 메서드는 문자열에서 지정한 값 이후의 모든 값을 반환합니다. 만약 해당 값이 문자열에 존재하지 않으면 전체 문자열이 반환됩니다.

```
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
<!-- #### `Str::afterLast()` -->
#### `Str::afterLast()`

<!-- The `Str::afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::afterLast` 메서드는 문자열에서 지정한 값이 마지막으로 나온 이후의 모든 값을 반환합니다. 만약 지정한 값이 문자열에 없다면 전체 문자열이 반환됩니다.

```
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
<!-- #### `Str::apa()` -->
#### `Str::apa()`

<!-- The `Str::apa` method converts the given string to title case following the [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case): -->
`Str::apa` 메서드는 [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 문자열을 타이틀 케이스로 변환합니다.

```
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
<!-- #### `Str::ascii()` -->
#### `Str::ascii()`

<!-- The `Str::ascii` method will attempt to transliterate the string into an ASCII value: -->
`Str::ascii` 메서드는 주어진 문자열을 ASCII 값으로 변환(전환)하려 시도합니다.

```
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
<!-- #### `Str::before()` -->
#### `Str::before()`

<!-- The `Str::before` method returns everything before the given value in a string: -->
`Str::before` 메서드는 문자열에서 지정한 값 이전의 모든 내용을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
<!-- #### `Str::beforeLast()` -->
#### `Str::beforeLast()`

<!-- The `Str::beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`Str::beforeLast` 메서드는 문자열에서 지정한 값이 마지막으로 등장하기 전까지의 모든 내용을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
<!-- #### `Str::between()` -->
#### `Str::between()`

<!-- The `Str::between` method returns the portion of a string between two values: -->
`Str::between` 메서드는 두 값 사이에 있는 문자열 일부를 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
<!-- #### `Str::betweenFirst()` -->
#### `Str::betweenFirst()`

<!-- The `Str::betweenFirst` method returns the smallest possible portion of a string between two values: -->
`Str::betweenFirst` 메서드는 두 값 사이에서 가장 짧게 포함하는 부분(최소의 범위)을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
<!-- #### `Str::camel()` -->
#### `Str::camel()`

<!-- The `Str::camel` method converts the given string to `camelCase`: -->
`Str::camel` 메서드는 주어진 문자열을 `camelCase` 형태로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
<!-- #### `Str::charAt()` -->
#### `Str::charAt()`

<!-- The `Str::charAt` method returns the character at the specified index. If the index is out of bounds, `false` is returned: -->
`Str::charAt` 메서드는 지정한 인덱스 위치에 있는 문자를 반환합니다. 만약 인덱스가 범위를 벗어난 경우 `false`를 반환합니다.

```
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-contains"></a>
<!-- #### `Str::contains()` -->
#### `Str::contains()`

<!-- The `Str::contains` method determines if the given string contains the given value. This method is case sensitive: -->
`Str::contains` 메서드는 주어진 문자열이 지정한 값을 포함하고 있는지 여부를 판별합니다. 이 메서드는 대소문자를 구분합니다.

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
배열 형태로 여러 값을 전달하면, 주어진 문자열이 그 중 하나라도 포함하는지 확인할 수 있습니다.

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

<a name="method-str-contains-all"></a>
<!-- #### `Str::containsAll()` -->
#### `Str::containsAll()`

<!-- The `Str::containsAll` method determines if the given string contains all of the values in a given array: -->
`Str::containsAll` 메서드는 주어진 문자열에 배열로 전달된 모든 값이 포함되어 있는지 판별합니다.

```
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

<a name="method-ends-with"></a>
<!-- #### `Str::endsWith()` -->
#### `Str::endsWith()`

<!-- The `Str::endsWith` method determines if the given string ends with the given value: -->
`Str::endsWith` 메서드는 주어진 문자열이 특정 값으로 끝나는지 여부를 판별합니다.

```
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
여러 값을 배열로 전달하면, 그 값들 중 하나로 끝나는지 확인할 수도 있습니다.

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
`Str::excerpt` 메서드는 주어진 문자열에서 특정 문구가 처음 나타나는 부분을 중심으로 발췌(부분 추출)한 내용을 반환합니다.

```
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

<!-- The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string. -->
`radius` 옵션(기본값: `100`)을 사용해, 발췌한 문구를 중심으로 좌우에 몇 글자를 표시할지 정할 수 있습니다.

<!-- In addition, you may use the `omission` option to define the string that will be prepended and appended to the truncated string: -->
또한, `omission` 옵션으로 앞뒤에 붙일 생략 문자열을 직접 지정할 수도 있습니다.

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
`Str::finish` 메서드는 주어진 값으로 끝나지 않는 경우에 한해, 문자열의 끝에 해당 값을 한 번만 덧붙입니다.

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
`Str::headline` 메서드는 대/소문자, 하이픈(-) 또는 언더스코어(_)로 구분된 문자열을 띄어쓰기로 나누고, 각 단어의 첫 글자를 대문자로 변환합니다.

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
`Str::inlineMarkdown` 메서드는 GitHub 스타일의 마크다운을 [CommonMark](https://commonmark.thephpleague.com/)를 이용해 인라인 HTML로 변환합니다. 단, `markdown` 메서드와 달리 생성된 HTML 전체를 블록 레벨 요소로 감싸지 않습니다.

```
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

<!-- #### Markdown Security -->
#### Markdown Security

<!-- By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier: -->
기본적으로 마크다운은 순수 HTML을 지원합니다. 그러나 사용자 입력을 그대로 사용할 경우, 이는 교차 사이트 스크립팅(XSS) 취약점에 노출될 수 있습니다. [CommonMark Security documentation](https://commonmark.thephpleague.com/security/)에 따르면, `html_input` 옵션을 사용해 순수 HTML을 이스케이프하거나 제거(stript)할 수 있고, `allow_unsafe_links` 옵션으로 위험한 링크 허용 여부를 지정할 수 있습니다. 만약 일부 순수 HTML만 허용해야 한다면, 마크다운이 변환된 결과를 HTML Purifier에 통과시키는 것이 좋습니다.

```
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
`Str::is` 메서드는 주어진 문자열이 지정한 패턴과 일치하는지 확인합니다. 와일드카드 값으로 별표(*)를 사용할 수 있습니다.

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
`Str::isAscii` 메서드는 주어진 문자열이 7비트 ASCII인지 여부를 판단합니다.

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
`Str::isJson` 메서드는 주어진 문자열이 올바른 JSON 형식인지 확인합니다.

```
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
`Str::isUrl` 메서드는 주어진 문자열이 유효한 URL인지 검사합니다.

```
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

<!-- The `isUrl` method considers a wide range of protocols as valid. However, you may specify the protocols that should be considered valid by providing them to the `isUrl` method: -->
`isUrl` 메서드는 다양한 프로토콜을 유효하다고 인식합니다. 하지만, 특정 프로토콜만 유효하도록 제한하고 싶다면 `isUrl` 메서드의 두 번째 인수로 허용할 프로토콜을 전달할 수 있습니다.

```
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
<!-- #### `Str::isUlid()` -->
#### `Str::isUlid()`

<!-- The `Str::isUlid` method determines if the given string is a valid ULID: -->
`Str::isUlid` 메서드는 주어진 문자열이 올바른 ULID인지 여부를 확인합니다.

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
`Str::isUuid` 메서드는 주어진 문자열이 올바른 UUID인지 확인합니다.

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
`Str::lcfirst` 메서드는 문자열의 첫 번째 문자를 소문자로 변환하여 반환합니다.

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
`Str::limit` 메서드는 주어진 문자열을 지정한 길이로 잘라줍니다.

```
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

<!-- You may pass a third argument to the method to change the string that will be appended to the end of the truncated string: -->
문자열이 잘렸을 때 끝에 추가할 문자열을 세 번째 인수로 지정할 수 있습니다.

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
`Str::markdown` 메서드는 GitHub 스타일의 Markdown을 [CommonMark](https://commonmark.thephpleague.com/)를 사용하여 HTML로 변환합니다.

```
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
기본적으로 Markdown은 원시 HTML을 지원하기 때문에, 사용자 입력값에 직접 사용할 경우 교차 사이트 스크립팅(XSS) 취약점이 발생할 수 있습니다. [CommonMark Security documentation](https://commonmark.thephpleague.com/security/)에 따르면, `html_input` 옵션을 사용해 원시 HTML을 이스케이프하거나 제거할 수 있고, `allow_unsafe_links` 옵션을 사용해 안전하지 않은 링크의 허용 여부를 지정할 수 있습니다. 반드시 일부의 원시 HTML만 허용해야 한다면, 컴파일된 마크다운을 HTML Purifier로 한 번 더 필터링하는 것이 좋습니다.

```
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
`Str::mask` 메서드는 문자열의 일부를 지정한 문자로 마스킹 처리합니다. 이 기능은 이메일 주소나 전화번호 등 일부 정보를 가려 표현할 때 유용하게 사용할 수 있습니다.

```
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

<!-- If needed, you provide a negative number as the third argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
`mask` 메서드의 세 번째 인수로 음수를 전달하면, 문자열 끝에서부터 마스킹이 시작됩니다.

```
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-ordered-uuid"></a>
<!-- #### `Str::orderedUuid()` -->
#### `Str::orderedUuid()`

<!-- The `Str::orderedUuid` method generates a "timestamp first" UUID that may be efficiently stored in an indexed database column. Each UUID that is generated using this method will be sorted after UUIDs previously generated using the method: -->
`Str::orderedUuid` 메서드는 "타임스탬프 우선" UUID를 생성합니다. 이 UUID는 인덱스된 데이터베이스 컬럼에 저장할 때 효율적으로 정렬될 수 있습니다. 이 메서드로 생성되는 UUID는 이전에 생성된 UUID보다 뒤에 정렬됩니다.

```
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
<!-- #### `Str::padBoth()` -->
#### `Str::padBoth()`

<!-- The `Str::padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches a desired length: -->
`Str::padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸서, 문자열의 양쪽을 지정한 문자로 채워 최종적으로 원하는 길이가 되도록 만들어줍니다.

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
`Str::padLeft` 메서드는 PHP의 `str_pad` 함수를 감싸서, 문자열의 왼쪽을 지정한 문자로 채워 최종적으로 원하는 길이가 되도록 만들어줍니다.

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
`Str::padRight` 메서드는 PHP의 `str_pad` 함수를 감싸서, 문자열의 오른쪽을 지정한 문자로 채워 최종적으로 원하는 길이가 되도록 만들어줍니다.

```
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
`Str::password` 메서드는 지정된 길이만큼의 보안성이 높은 랜덤 비밀번호를 생성할 수 있습니다. 비밀번호는 영문, 숫자, 특수문자, 공백이 조합된 형태로 만들어집니다. 기본값은 32자입니다.

```
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
<!-- #### `Str::plural()` -->
#### `Str::plural()`

<!-- The `Str::plural` method converts a singular word string to its plural form. This function supports [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language): -->
`Str::plural` 메서드는 단수형 단어를 복수형으로 변환합니다. 이 함수는 [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language) 모두에서 동작합니다.

```
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
두 번째 인수로 정수를 전달하면, 단수 또는 복수형 중 올바른 형태를 반환합니다.

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

<!-- The `Str::pluralStudly` method converts a singular word string formatted in studly caps case to its plural form. This function supports [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language): -->
`Str::pluralStudly` 메서드는 StudlyCaps(첫 글자가 대문자인 형태)의 단어를 복수형으로 변환합니다. 이 함수 역시 [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language) 모두에서 사용할 수 있습니다.

```
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
두 번째 인수로 정수를 전달하면, 단수 또는 복수형 중 올바른 형태를 반환합니다.

```
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
`Str::position` 메서드는 문자열에서 특정 부분 문자열이 처음으로 등장하는 위치(인덱스)를 반환합니다. 해당 부분 문자열이 존재하지 않으면 `false`를 반환합니다.

```
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
`Str::random` 메서드는 지정한 길이만큼의 랜덤 문자열을 생성합니다. 이 함수는 PHP의 `random_bytes` 함수를 사용합니다.

```
use Illuminate\Support\Str;

$random = Str::random(40);
```

<!-- During testing, it may be useful to "fake" the value that is returned by the `Str::random` method. To accomplish this, you may use the `createRandomStringsUsing` method: -->
테스트 시에는 `Str::random` 메서드가 반환하는 값을 "임의로 지정된 값"으로 대체할 수도 있습니다. 이를 위해 `createRandomStringsUsing` 메서드를 사용합니다.

```
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

<!-- To instruct the `random` method to return to generating random strings normally, you may invoke the `createRandomStringsNormally` method: -->
`random` 메서드가 다시 원래처럼 무작위 문자열을 생성하도록 하려면, `createRandomStringsNormally` 메서드를 사용할 수 있습니다.

```
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
<!-- #### `Str::remove()` -->
#### `Str::remove()`

<!-- The `Str::remove` method removes the given value or array of values from the string: -->
`Str::remove` 메서드는 문자열에서 지정한 값 또는 값 배열에 해당하는 부분을 삭제합니다.

```
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

<!-- You may also pass `false` as a third argument to the `remove` method to ignore case when removing strings. -->
`remove` 메서드의 세 번째 인수로 `false`를 전달하면, 대소문자를 구분하지 않고 문자열을 제거할 수 있습니다.

<a name="method-str-repeat"></a>
<!-- #### `Str::repeat()` -->
#### `Str::repeat()`

<!-- The `Str::repeat` method repeats the given string: -->
`Str::repeat` 메서드는 지정한 문자열을 원하는 횟수만큼 반복하여 반환합니다.

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
`Str::replace` 메서드는 문자열 내에서 특정 문자열을 다른 문자열로 교체합니다.

```
use Illuminate\Support\Str;

$string = 'Laravel 8.x';

$replaced = Str::replace('8.x', '9.x', $string);

// Laravel 9.x
```

<!-- The `replace` method also accepts a `caseSensitive` argument. By default, the `replace` method is case sensitive: -->
`replace` 메서드는 `caseSensitive` 인수도 지원합니다. 기본적으로 `replace` 메서드는 대소문자를 구분합니다.

```
Str::replace('Framework', 'Laravel', caseSensitive: false);
```

<a name="method-str-replace-array"></a>
<!-- #### `Str::replaceArray()` -->
#### `Str::replaceArray()`

<!-- The `Str::replaceArray` method replaces a given value in the string sequentially using an array: -->
`Str::replaceArray` 메서드는 배열을 이용해 문자열 내의 지정한 값을 순서대로 교체합니다.

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
`Str::replaceFirst` 메서드는 문자열에서 지정한 값이 처음 등장하는 부분만 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
<!-- #### `Str::replaceLast()` -->
#### `Str::replaceLast()`

<!-- The `Str::replaceLast` method replaces the last occurrence of a given value in a string: -->
`Str::replaceLast` 메서드는 문자열에서 지정한 값이 마지막으로 등장하는 부분만 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
<!-- #### `Str::replaceMatches()` -->
#### `Str::replaceMatches()`

<!-- The `Str::replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string: -->
`Str::replaceMatches` 메서드는 패턴에 일치하는 문자열의 모든 부분을 주어진 문자열로 대체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

<!-- The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value: -->
`replaceMatches` 메서드는 클로저(익명 함수)를 인수로 받을 수 있으며, 패턴에 일치하는 각 부분을 처리한 결과로 대체할 수 있습니다.

```
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
`Str::replaceStart` 메서드는 문자열의 시작 부분에만 지정한 값이 있을 때에만 이 값을 교체합니다.

```
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
`Str::replaceEnd` 메서드는 문자열의 끝 부분에만 지정한 값이 있을 때에만 이 값을 교체합니다.

```
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
`Str::reverse` 메서드는 주어진 문자열을 거꾸로 뒤집어 반환합니다.

```
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
<!-- #### `Str::singular()` -->
#### `Str::singular()`

<!-- The `Str::singular` method converts a string to its singular form. This function supports [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language): -->
`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. 이 함수는 [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language)를 지원합니다.

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
`Str::slug` 메서드는 주어진 문자열로부터 URL에 적합한 "슬러그(slug)" 문자열을 생성합니다.

```
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
<!-- #### `Str::snake()` -->
#### `Str::snake()`

<!-- The `Str::snake` method converts the given string to `snake_case`: -->
`Str::snake` 메서드는 주어진 문자열을 `snake_case` 형식으로 변환합니다.

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
`Str::squish` 메서드는 문자열에서 단어 사이를 포함한 모든 불필요한 공백을 제거합니다.

```
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
<!-- #### `Str::start()` -->
#### `Str::start()`

<!-- The `Str::start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`Str::start` 메서드는 주어진 값으로 시작하지 않는다면 해당 값을 문자열 앞에 한 번만 추가합니다.

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
`Str::startsWith` 메서드는 주어진 문자열이 특정 값으로 시작하는지 확인합니다.

```
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

<!-- If an array of possible values is passed, the `startsWith` method will return `true` if the string begins with any of the given values: -->
만약 여러 값이 담긴 배열을 전달하면, 해당 배열 중 어느 값으로 시작하더라도 `startsWith` 메서드는 `true`를 반환합니다.

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
`Str::substr` 메서드는 지정한 시작 위치와 길이에 따라 해당 부분 문자열을 반환합니다.

```
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
<!-- #### `Str::substrCount()` -->
#### `Str::substrCount()`

<!-- The `Str::substrCount` method returns the number of occurrences of a given value in the given string: -->
`Str::substrCount` 메서드는 주어진 문자열 내에서 특정 값이 등장하는 횟수를 반환합니다.

```
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
<!-- #### `Str::substrReplace()` -->
#### `Str::substrReplace()`

<!-- The `Str::substrReplace` method replaces text within a portion of a string, starting at the position specified by the third argument and replacing the number of characters specified by the fourth argument. Passing `0` to the method's fourth argument will insert the string at the specified position without replacing any of the existing characters in the string: -->
`Str::substrReplace` 메서드는 지정한 위치(세 번째 인자)에서부터 주어진 길이(네 번째 인자)만큼 문자열을 대체합니다. 네 번째 인자에 `0`을 넘기면, 기존 문자를 대체하지 않고 해당 위치에 새 문자열을 삽입하게 됩니다.

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
`Str::swap` 메서드는 PHP의 `strtr` 함수를 사용해 주어진 문자열에서 여러 값을 한 번에 치환합니다.

```
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
`Str::take` 메서드는 문자열의 앞에서부터 지정한 개수만큼의 문자를 반환합니다.

```
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
<!-- #### `Str::title()` -->
#### `Str::title()`

<!-- The `Str::title` method converts the given string to `Title Case`: -->
`Str::title` 메서드는 주어진 문자열을 `Title Case`(각 단어의 첫 글자를 대문자로)로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
<!-- #### `Str::toBase64()` -->
#### `Str::toBase64()`

<!-- The `Str::toBase64` method converts the given string to Base64: -->
`Str::toBase64` 메서드는 주어진 문자열을 Base64로 인코딩합니다.

```
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-to-html-string"></a>
<!-- #### `Str::toHtmlString()` -->
#### `Str::toHtmlString()`

<!-- The `Str::toHtmlString` method converts the string instance to an instance of `Illuminate\Support\HtmlString`, which may be displayed in Blade templates: -->
`Str::toHtmlString` 메서드는 문자열 인스턴스를 `Illuminate\Support\HtmlString` 인스턴스로 변환하여, Blade 템플릿 등에서 표시할 수 있게 합니다.

```
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-str-ucfirst"></a>
<!-- #### `Str::ucfirst()` -->
#### `Str::ucfirst()`

<!-- The `Str::ucfirst` method returns the given string with the first character capitalized: -->
`Str::ucfirst` 메서드는 주어진 문자열의 첫 글자를 대문자로 변환합니다.

```
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
<!-- #### `Str::ucsplit()` -->
#### `Str::ucsplit()`

<!-- The `Str::ucsplit` method splits the given string into an array by uppercase characters: -->
`Str::ucsplit` 메서드는 문자열을 대문자를 기준으로 잘라 배열로 반환합니다.

```
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-upper"></a>
<!-- #### `Str::upper()` -->
#### `Str::upper()`

<!-- The `Str::upper` method converts the given string to uppercase: -->
`Str::upper` 메서드는 주어진 문자열을 모두 대문자로 변환합니다.

```
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
<!-- #### `Str::ulid()` -->
#### `Str::ulid()`

<!-- The `Str::ulid` method generates a ULID, which is a compact, time-ordered unique identifier: -->
`Str::ulid` 메서드는 ULID(Compact, 시간 순서가 보장되는 고유 식별자)를 생성합니다.

```
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

<!-- If you would like to retrieve a `Illuminate\Support\Carbon` date instance representing the date and time that a given ULID was created, you may use the `createFromId` method provided by Laravel's Carbon integration: -->
생성된 ULID의 생성 일시를 나타내는 `Illuminate\Support\Carbon` 날짜 인스턴스를 얻으려면, Laravel의 Carbon 통합에서 제공하는 `createFromId` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

<!-- During testing, it may be useful to "fake" the value that is returned by the `Str::ulid` method. To accomplish this, you may use the `createUlidsUsing` method: -->
테스트 시, `Str::ulid` 메서드가 반환하는 값을 임의로 지정해야 할 경우, `createUlidsUsing` 메서드를 활용할 수 있습니다.

```
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

<!-- To instruct the `ulid` method to return to generating ULIDs normally, you may invoke the `createUlidsNormally` method: -->
`ulid` 메서드가 ULID 값 생성 방식을 원래대로 되돌리게 하려면, `createUlidsNormally` 메서드를 호출하면 됩니다.

```
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
<!-- #### `Str::unwrap()` -->
#### `Str::unwrap()`

<!-- The `Str::unwrap` method removes the specified strings from the beginning and end of a given string: -->
`Str::unwrap` 메서드는 주어진 문자열의 시작과 끝에서 지정한 문자열을 제거합니다.

```
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
`Str::uuid` 메서드는 UUID(버전 4)를 생성합니다.

```
use Illuminate\Support\Str;

return (string) Str::uuid();
```

<!-- During testing, it may be useful to "fake" the value that is returned by the `Str::uuid` method. To accomplish this, you may use the `createUuidsUsing` method: -->
테스트 시, `Str::uuid` 메서드가 반환하는 값을 임의로 지정하려면 `createUuidsUsing` 메서드를 활용할 수 있습니다.

```
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

<!-- To instruct the `uuid` method to return to generating UUIDs normally, you may invoke the `createUuidsNormally` method: -->
`uuid` 메서드가 UUID 값 생성 방식을 일반적인 방식으로 되돌리게 하려면 `createUuidsNormally` 메서드를 호출하세요.

```
Str::createUuidsNormally();
```

<a name="method-str-word-count"></a>
<!-- #### `Str::wordCount()` -->
#### `Str::wordCount()`

<!-- The `Str::wordCount` method returns the number of words that a string contains: -->
`Str::wordCount` 메서드는 문자열 안에 단어가 몇 개인지 반환합니다.

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
<!-- #### `Str::wordWrap()` -->
#### `Str::wordWrap()`

<!-- The `Str::wordWrap` method wraps a string to a given number of characters: -->
`Str::wordWrap` 메서드는 문자열을 지정한 개수의 문자 단위로 줄 바꿈 처리합니다.

```
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
`Str::words` 메서드는 문자열의 단어 개수를 제한합니다. 세 번째 인자에 추가 문자열을 지정하여, 잘려진 끝에 덧붙일 문자열을 설정할 수 있습니다.

```
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
<!-- #### `Str::wrap()` -->
#### `Str::wrap()`

<!-- The `Str::wrap` method wraps the given string with an additional string or pair of strings: -->
`Str::wrap` 메서드는 지정한 단일 문자열 또는 한 쌍의 문자열로 주어진 문자열을 감쌉니다.

```
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
`str` 함수는 주어진 문자열에 대해 새로운 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of` 메서드와 동일합니다.

```
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<!-- If no argument is provided to the `str` function, the function returns an instance of `Illuminate\Support\Str`: -->
`str` 함수에 인자를 전달하지 않으면, 이 함수는 `Illuminate\Support\Str` 인스턴스를 반환합니다.

```
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
<!-- #### `trans()` -->
#### `trans()`

<!-- The `trans` function translates the given translation key using your [language files](/docs/10.x/localization): -->
`trans` 함수는 지정한 번역 키를 사용하여 [language files](/docs/10.x/localization)에서 해당 텍스트를 번역해 반환합니다.

```
echo trans('messages.welcome');
```

<!-- If the specified translation key does not exist, the `trans` function will return the given key. So, using the example above, the `trans` function would return `messages.welcome` if the translation key does not exist. -->
지정한 번역 키가 존재하지 않으면, `trans` 함수는 전달한 키 자체를 반환합니다. 즉, 위 예시에서 해당 키가 없다면 `trans` 함수는 `messages.welcome`을 그대로 반환합니다.

<a name="method-trans-choice"></a>
<!-- #### `trans_choice()` -->
#### `trans_choice()`

<!-- The `trans_choice` function translates the given translation key with inflection: -->
`trans_choice` 함수는 변환 키에 맞게 복수/단수 등 어형을 적용하여 번역합니다.

```
echo trans_choice('messages.notifications', $unreadCount);
```

<!-- If the specified translation key does not exist, the `trans_choice` function will return the given key. So, using the example above, the `trans_choice` function would return `messages.notifications` if the translation key does not exist. -->
지정한 키가 없다면, `trans_choice` 함수도 전달된 키 자체를 반환합니다. 따라서 예시의 경우 키가 존재하지 않으면 `trans_choice` 함수는 `messages.notifications`를 반환합니다.

<a name="fluent-strings"></a>
<!-- ## Fluent Strings -->
## Fluent Strings

<!-- Fluent strings provide a more fluent, object-oriented interface for working with string values, allowing you to chain multiple string operations together using a more readable syntax compared to traditional string operations. -->
플루언트 문자열은 좀 더 객체지향적이고 유연한 방식으로 문자열 값을 다룰 수 있는 인터페이스를 제공합니다. 이를 통해 기존의 문자열 함수보다 가독성 높고 체이닝이 가능한 구문으로 여러 문자열 처리를 연속 실행할 수 있습니다.

<a name="method-fluent-str-after"></a>
<!-- #### `after` -->
#### `after`

<!-- The `after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`after` 메서드는 문자열에서 주어진 값 이후의 모든 내용을 반환합니다. 해당 값이 문자열 내에 존재하지 않으면 전체 문자열이 반환됩니다.

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
<!-- #### `afterLast` -->
#### `afterLast`

<!-- The `afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`afterLast` 메서드는 문자열 안에서 주어진 값이 마지막으로 나타난 이후의 모든 내용을 반환합니다. 해당 값이 존재하지 않을 경우 전체 문자열을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-apa"></a>
<!-- #### `apa` -->
#### `apa`

<!-- The `apa` method converts the given string to title case following the [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case): -->
`apa` 메서드는 [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 주어진 문자열을 타이틀 케이스로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->apa();

// A Nice Title Uses the Correct Case
```

<a name="method-fluent-str-append"></a>
<!-- #### `append` -->
#### `append`

<!-- The `append` method appends the given values to the string: -->
`append` 메서드는 지정한 값을 문자열 끝에 추가합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
<!-- #### `ascii` -->
#### `ascii`

<!-- The `ascii` method will attempt to transliterate the string into an ASCII value: -->
`ascii` 메서드는 주어진 문자열을 가능한 한 ASCII 문자열로 변환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
<!-- #### `basename` -->
#### `basename`

<!-- The `basename` method will return the trailing name component of the given string: -->
`basename` 메서드는 주어진 문자열에서 마지막 경로 컴포넌트(파일명 등)만 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

<!-- If needed, you may provide an "extension" that will be removed from the trailing component: -->
필요하다면 확장자(예: .jpg)를 인자로 전달하여 마지막 컴포넌트에서 확장자를 제거할 수도 있습니다.

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
<!-- #### `before` -->
#### `before`

<!-- The `before` method returns everything before the given value in a string: -->
`before` 메서드는 주어진 값이 등장하기 전까지의 부분 문자열을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
<!-- #### `beforeLast` -->
#### `beforeLast`

<!-- The `beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`beforeLast` 메서드는 문자열 안에서 지정한 값이 마지막으로 등장하기 전까지의 모든 내용을 반환합니다.

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>

<!-- #### `between` -->
#### `between`

<!-- The `between` method returns the portion of a string between two values: -->
`between` 메서드는 두 값 사이에 위치한 문자열의 일부를 반환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
<!-- #### `betweenFirst` -->
#### `betweenFirst`

<!-- The `betweenFirst` method returns the smallest possible portion of a string between two values: -->
`betweenFirst` 메서드는 두 값 사이에 위치한 가장 짧은(최소 범위의) 문자열 일부를 반환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
<!-- #### `camel` -->
#### `camel`

<!-- The `camel` method converts the given string to `camelCase`: -->
`camel` 메서드는 주어진 문자열을 `camelCase` 형태로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// 'fooBar'
```

<a name="method-fluent-str-char-at"></a>
<!-- #### `charAt` -->
#### `charAt`

<!-- The `charAt` method returns the character at the specified index. If the index is out of bounds, `false` is returned: -->
`charAt` 메서드는 지정한 인덱스 위치의 문자를 반환합니다. 만약 인덱스가 범위를 벗어난 경우 `false`를 반환합니다.

```
use Illuminate\Support\Str;

$character = Str::of('This is my name.')->charAt(6);

// 's'
```

<a name="method-fluent-str-class-basename"></a>
<!-- #### `classBasename` -->
#### `classBasename`

<!-- The `classBasename` method returns the class name of the given class with the class's namespace removed: -->
`classBasename` 메서드는 주어진 클래스에서 네임스페이스를 제거한 뒤, 클래스명만을 반환합니다.

```
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// 'Baz'
```

<a name="method-fluent-str-contains"></a>
<!-- #### `contains` -->
#### `contains`

<!-- The `contains` method determines if the given string contains the given value. This method is case sensitive: -->
`contains` 메서드는 주어진 문자열이 특정 값을 포함하는지 판별합니다. 이 메서드는 대소문자를 구분합니다.

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
값의 배열을 전달하면, 해당 배열 중 하나라도 문자열에 포함되어 있는지 확인할 수 있습니다.

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

<a name="method-fluent-str-contains-all"></a>
<!-- #### `containsAll` -->
#### `containsAll`

<!-- The `containsAll` method determines if the given string contains all of the values in the given array: -->
`containsAll` 메서드는 주어진 문자열이, 전달된 배열 내 모든 값을 포함하는지 판별합니다.

```
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

<a name="method-fluent-str-dirname"></a>
<!-- #### `dirname` -->
#### `dirname`

<!-- The `dirname` method returns the parent directory portion of the given string: -->
`dirname` 메서드는 주어진 문자열에서 상위 디렉터리 부분을 반환합니다.

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

<!-- If necessary, you may specify how many directory levels you wish to trim from the string: -->
필요하다면, 몇 단계의 디렉터리 상위 경로까지 제거(자르기)할지 지정할 수 있습니다.

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-excerpt"></a>
<!-- #### `excerpt` -->
#### `excerpt`

<!-- The `excerpt` method extracts an excerpt from the string that matches the first instance of a phrase within that string: -->
`excerpt` 메서드는 문자열에서 지정한 구를 처음으로 찾은 위치를 기준으로, 해당 부분을 중심으로 발췌된 문자열 일부를 추출합니다.

```
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

<!-- The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string. -->
`radius` 옵션은 발췌된 문자열에서 각 측면(앞뒤)에 몇 글자까지 포함할지를 지정하며, 기본값은 `100`입니다.

<!-- In addition, you may use the `omission` option to change the string that will be prepended and appended to the truncated string: -->
또한, 발췌된(잘린) 문자열 앞뒤에 붙는 문자열을 `omission` 옵션으로 지정할 수 있습니다.

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
`endsWith` 메서드는 지정한 문자열로 끝나는지 여부를 판별합니다.

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
배열로 여러 값을 전달하여, 전달된 값 중 하나라도 해당 문자열로 끝나는지 확인할 수도 있습니다.

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
`exactly` 메서드는 두 문자열이 완전히 일치하는지 판별합니다.

```
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-explode"></a>
<!-- #### `explode` -->
#### `explode`

<!-- The `explode` method splits the string by the given delimiter and returns a collection containing each section of the split string: -->
`explode` 메서드는 주어진 구분자로 문자열을 나누어, 분리된 각 부분들을 컬렉션으로 반환합니다.

```
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
<!-- #### `finish` -->
#### `finish`

<!-- The `finish` method adds a single instance of the given value to a string if it does not already end with that value: -->
`finish` 메서드는 주어진 값으로 끝나지 않는 경우, 해당 값을 문자열 끝에 한 번만 추가합니다.

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
`headline` 메서드는 대소문자 구분, 하이픈(-), 언더스코어(_) 등으로 구분되어 있는 문자열을 띄어쓰기 기반의 문자열로 변환하고, 각 단어의 첫 글자를 대문자로 만듭니다.

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
`inlineMarkdown` 메서드는 GitHub 스타일의 마크다운(Markdown)을 [CommonMark](https://commonmark.thephpleague.com/)를 이용해 인라인 HTML로 변환합니다. 하지만 `markdown` 메서드와 달리, 변환된 HTML을 블록 레벨 요소로 래핑하지는 않습니다.

```
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

<!-- #### Markdown Security -->
#### Markdown Security

<!-- By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier: -->
기본적으로 마크다운은 원시 HTML을 지원하므로, 사용자로부터 입력받은 원본에 대해 사용할 경우 Cross-Site Scripting(XSS) 취약점을 노출할 수 있습니다. [CommonMark Security documentation](https://commonmark.thephpleague.com/security/)에서는 `html_input` 옵션을 사용해 원시 HTML을 escaping 또는 제거하도록, 그리고 `allow_unsafe_links` 옵션을 통해 안전하지 않은 링크의 허용 여부를 지정할 수 있다고 명시하고 있습니다. 일부 원시 HTML만 허용해야 한다면, 변환된 마크다운을 반드시 HTML Purifier로 한 번 더 처리해야 합니다.

```
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
`is` 메서드는 주어진 문자열이 특정 패턴과 일치하는지 판별합니다. 패턴에는 와일드카드로 별표(*)를 사용할 수 있습니다.

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
`isAscii` 메서드는 주어진 문자열이 ASCII 문자열인지 판별합니다.

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
`isEmpty` 메서드는 주어진 문자열이 비어있는지(공백만 포함하는지) 판별합니다.

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
`isNotEmpty` 메서드는 주어진 문자열이 비어있지 않은지 판별합니다.

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
`isJson` 메서드는 주어진 문자열이 올바른 JSON 형식인지 판별합니다.

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
`isUlid` 메서드는 주어진 문자열이 ULID인지 여부를 판별합니다.

```
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
`isUrl` 메서드는 주어진 문자열이 URL인지 판별합니다.

```
use Illuminate\Support\Str;

$result = Str::of('http://example.com')->isUrl();

// true

$result = Str::of('Taylor')->isUrl();

// false
```

<!-- The `isUrl` method considers a wide range of protocols as valid. However, you may specify the protocols that should be considered valid by providing them to the `isUrl` method: -->
`isUrl` 메서드는 다양한 종류의 프로토콜을 허용합니다. 하지만, `isUrl` 메서드에 허용할 프로토콜 목록을 전달하여 제한할 수도 있습니다.

```
$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

<a name="method-fluent-str-is-uuid"></a>
<!-- #### `isUuid` -->
#### `isUuid`

<!-- The `isUuid` method determines if a given string is a UUID: -->
`isUuid` 메서드는 주어진 문자열이 UUID인지 판별합니다.

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
`kebab` 메서드는 주어진 문자열을 `kebab-case` 형태로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
<!-- #### `lcfirst` -->
#### `lcfirst`

<!-- The `lcfirst` method returns the given string with the first character lowercased: -->
`lcfirst` 메서드는 주어진 문자열의 첫 글자를 소문자로 변환하여 반환합니다.

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
`limit` 메서드는 문자열을 지정한 길이만큼만 잘라서 반환합니다.

```
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

<!-- You may also pass a second argument to change the string that will be appended to the end of the truncated string: -->
잘린 문자열 끝에 추가될 문자열을 두 번째 인자로 지정할 수도 있습니다.

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
`ltrim` 메서드는 문자열 왼쪽(앞) 부분의 공백이나 지정한 문자를 제거합니다.

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
`markdown` 메서드는 GitHub 스타일의 마크다운을 HTML로 변환합니다.

```
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
기본적으로 마크다운은 원시 HTML을 지원하므로, 사용자로부터 입력받은 원본에 대해 사용할 경우 Cross-Site Scripting(XSS) 취약점을 노출할 수 있습니다. [CommonMark Security documentation](https://commonmark.thephpleague.com/security/)에서는 `html_input` 옵션을 사용해 원시 HTML을 escaping 또는 제거하도록, 그리고 `allow_unsafe_links` 옵션을 통해 안전하지 않은 링크의 허용 여부를 지정할 수 있다고 명시하고 있습니다. 일부 원시 HTML만 허용해야 한다면, 변환된 마크다운을 반드시 HTML Purifier로 한 번 더 처리해야 합니다.

```
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
`mask` 메서드는 문자열 일부를 반복 문자로 마스킹(가림)하여, 이메일 주소나 전화번호 등 민감한 정보의 일부를 가릴 때 사용할 수 있습니다.

```
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

<!-- If needed, you may provide negative numbers as the third or fourth argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
필요하다면, `mask` 메서드의 세 번째 또는 네 번째 인자에 음수 값을 지정하여, 문자열 끝에서부터 거리를 기준으로 마스킹을 시작하도록 할 수 있습니다.

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
`match` 메서드는 주어진 정규 표현식 패턴과 일치하는 문자열의 일부를 반환합니다.

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
`matchAll` 메서드는 정규 표현식 패턴과 일치하는 문자열의 부분들을 포함하는 컬렉션을 반환합니다.

```
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

<!-- If you specify a matching group within the expression, Laravel will return a collection of that group's matches: -->
표현식 내에 매칭 그룹을 지정하면, Laravel은 해당 그룹에 대응되는 모든 값을 컬렉션으로 반환합니다.

```
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

<!-- If no matches are found, an empty collection will be returned. -->
일치하는 항목이 없으면 빈 컬렉션이 반환됩니다.

<a name="method-fluent-str-is-match"></a>
<!-- #### `isMatch` -->
#### `isMatch`

<!-- The `isMatch` method will return `true` if the string matches a given regular expression: -->
`isMatch` 메서드는 문자열이 주어진 정규 표현식과 일치하면 `true`를 반환합니다.

```
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
`newLine` 메서드는 문자열 끝에 "줄 바꿈" 문자를 추가합니다.

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
`padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸 양쪽에서 문자열을 지정한 길이만큼 다른 문자열로 채웁니다.

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
`padLeft` 메서드는 PHP의 `str_pad` 함수를 감싸 왼쪽에서 문자열을 지정한 길이만큼 다른 문자열로 채웁니다.

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
`padRight` 메서드는 PHP의 `str_pad` 함수를 감싸 오른쪽에서 문자열을 지정한 길이만큼 다른 문자열로 채웁니다.

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
`pipe` 메서드는 현재 문자열 값을 주어진 콜러블에 전달하여 문자열을 원하는 대로 변환할 수 있습니다.

```
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

<!-- The `plural` method converts a singular word string to its plural form. This function supports [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language): -->
`plural` 메서드는 단수 형태의 단어를 복수 형태로 변환합니다. 이 함수는 [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language)에서도 사용할 수 있습니다.

```
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
함수의 두 번째 인수로 정수를 전달하면, 해당 정수에 따라 문자열의 단수 또는 복수 형태를 얻을 수 있습니다.

```
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

<a name="method-fluent-str-position"></a>
<!-- #### `position` -->
#### `position`

<!-- The `position` method returns the position of the first occurrence of a substring in a string. If the substring does not exist within the string, `false` is returned: -->
`position` 메서드는 문자열에서 지정한 부분 문자열이 처음 나타나는 위치를 반환합니다. 만약 부분 문자열이 존재하지 않으면 `false`를 반환합니다.

```
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
`prepend` 메서드는 지정한 값을 문자열 앞에 붙입니다.

```
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
<!-- #### `remove` -->
#### `remove`

<!-- The `remove` method removes the given value or array of values from the string: -->
`remove` 메서드는 지정한 값 또는 값들의 배열을 문자열에서 제거합니다.

```
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite');

// Arkansas is beautiful!
```

<!-- You may also pass `false` as a second parameter to ignore case when removing strings. -->
문자열 제거 시 대소문자 구분을 무시하려면 두 번째 파라미터로 `false`를 전달할 수 있습니다.

<a name="method-fluent-str-repeat"></a>
<!-- #### `repeat` -->
#### `repeat`

<!-- The `repeat` method repeats the given string: -->
`repeat` 메서드는 지정된 문자열을 여러 번 반복합니다.

```php
use Illuminate\Support\Str;

$repeated = Str::of('a')->repeat(5);

// aaaaa
```

<a name="method-fluent-str-replace"></a>
<!-- #### `replace` -->
#### `replace`

<!-- The `replace` method replaces a given string within the string: -->
`replace` 메서드는 문자열 내에서 지정한 값을 대체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

<!-- The `replace` method also accepts a `caseSensitive` argument. By default, the `replace` method is case sensitive: -->
`replace` 메서드는 `caseSensitive` 옵션도 지원합니다. 기본적으로 `replace` 메서드는 대소문자를 구분하여 치환합니다.

```
$replaced = Str::of('macOS 13.x')->replace(
    'macOS', 'iOS', caseSensitive: false
);
```

<a name="method-fluent-str-replace-array"></a>
<!-- #### `replaceArray` -->
#### `replaceArray`

<!-- The `replaceArray` method replaces a given value in the string sequentially using an array: -->
`replaceArray` 메서드는 문자열에 지정한 값을 배열에 있는 값들로 순차적으로 치환합니다.

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
`replaceFirst` 메서드는 지정된 값이 처음 나타나는 위치를 다른 값으로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
<!-- #### `replaceLast` -->
#### `replaceLast`

<!-- The `replaceLast` method replaces the last occurrence of a given value in a string: -->
`replaceLast` 메서드는 지정된 값이 마지막으로 나타나는 위치를 다른 값으로 교체합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
<!-- #### `replaceMatches` -->
#### `replaceMatches`

<!-- The `replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string: -->
`replaceMatches` 메서드는 패턴과 일치하는 문자열 부분을 지정한 값으로 모두 변경합니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

<!-- The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value: -->
또한 `replaceMatches` 메서드는 각 일치 항목마다 호출되는 클로저를 전달할 수 있습니다. 이를 통해 치환 로직을 직접 구현하고 반환할 값을 지정할 수 있습니다.

```
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
`replaceStart` 메서드는 지정한 값이 문자열의 시작 부분에 있을 때만 그 첫 번째 값을 변경합니다.

```
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
`replaceEnd` 메서드는 지정한 값이 문자열의 끝 부분에 있을 때만 그 마지막 값을 바꿉니다.

```
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

// Hello Laravel

$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

// Hello World
```

<a name="method-fluent-str-rtrim"></a>
<!-- #### `rtrim` -->
#### `rtrim`

<!-- The `rtrim` method trims the right side of the given string: -->
`rtrim` 메서드는 문자열의 오른쪽 끝에 있는 공백(또는 지정된 문자를) 제거합니다.

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
`scan` 메서드는 [`sscanf` PHP function](https://www.php.net/manual/en/function.sscanf.php)에서 지원하는 형식에 따라 입력 문자열을 파싱해서 컬렉션으로 반환합니다.

```
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
<!-- #### `singular` -->
#### `singular`

<!-- The `singular` method converts a string to its singular form. This function supports [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language): -->
`singular` 메서드는 문자열을 단수 형태로 변환합니다. 이 함수는 [any of the languages support by Laravel's pluralizer](/docs/10.x/localization#pluralization-language)에서도 사용할 수 있습니다.

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
`slug` 메서드는 주어진 문자열을 URL에 친화적인 "슬러그(slug)"로 생성합니다.

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
`split` 메서드는 정규 표현식을 이용해 문자열을 컬렉션으로 분할합니다.

```
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
<!-- #### `squish` -->
#### `squish`

<!-- The `squish` method removes all extraneous white space from a string, including extraneous white space between words: -->
`squish` 메서드는 문자열 내에 불필요하게 많은 공백(단어 사이 공백 포함)을 모두 제거합니다.

```
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
<!-- #### `start` -->
#### `start`

<!-- The `start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`start` 메서드는 만약 문자열이 지정한 값으로 시작하지 않는 경우, 해당 값을 맨 앞에 한 번만 붙여줍니다.

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
`startsWith` 메서드는 문자열이 지정한 값으로 시작하는지 여부를 판단합니다.

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

<a name="method-fluent-str-strip-tags"></a>
<!-- #### `stripTags` -->
#### `stripTags`

<!-- The `stripTags` method removes all HTML and PHP tags from a string: -->
`stripTags` 메서드는 문자열에서 모든 HTML, PHP 태그를 제거합니다.

```
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
`studly` 메서드는 주어진 문자열을 `StudlyCase` 형식으로 변환합니다.

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
<!-- #### `substr` -->
#### `substr`

<!-- The `substr` method returns the portion of the string specified by the given start and length parameters: -->
`substr` 메서드는 시작 위치와 길이 파라미터에 따라 문자열의 일부를 반환합니다.

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
`substrReplace` 메서드는 두 번째 인수로 지정한 위치부터 시작해서, 세 번째 인수만큼의 문자를 치환합니다. 세 번째 인수에 `0`을 전달하면 해당 위치에 문자열을 삽입만 하고 기존 문자는 삭제하지 않습니다.

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
`swap` 메서드는 PHP의 `strtr` 함수를 이용하여 문자열 내 여러 값을 한 번에 교체합니다.

```
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
`take` 메서드는 문자열의 시작 부분에서 지정한 개수만큼의 문자를 반환합니다:

```
use Illuminate\Support\Str;

$taken = Str::of('Build something amazing!')->take(5);

// Build
```

<a name="method-fluent-str-tap"></a>
<!-- #### `tap` -->
#### `tap`

<!-- The `tap` method passes the string to the given closure, allowing you to examine and interact with the string while not affecting the string itself. The original string is returned by the `tap` method regardless of what is returned by the closure: -->
`tap` 메서드는 문자열을 주어진 클로저에 전달하여, 문자열 자체에는 아무런 영향을 주지 않으면서 문자열을 확인하거나 조작할 수 있도록 해줍니다. 클로저에서 무엇을 반환하든 관계없이, `tap` 메서드는 원본 문자열을 그대로 반환합니다:

```
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
`test` 메서드는 문자열이 주어진 정규 표현식 패턴과 일치하는지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
<!-- #### `title` -->
#### `title`

<!-- The `title` method converts the given string to `Title Case`: -->
`title` 메서드는 주어진 문자열을 `Title Case`(각 단어의 첫 글자를 대문자로 변환)로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-to-base64"></a>
<!-- #### `toBase64()` -->
#### `toBase64()`

<!-- The `toBase64` method converts the given string to Base64: -->
`toBase64` 메서드는 주어진 문자열을 Base64로 인코딩합니다:

```
use Illuminate\Support\Str;

$base64 = Str::of('Laravel')->toBase64();

// TGFyYXZlbA==
```

<a name="method-fluent-str-trim"></a>
<!-- #### `trim` -->
#### `trim`

<!-- The `trim` method trims the given string: -->
`trim` 메서드는 주어진 문자열의 양쪽 끝에 있는 공백이나 지정한 문자를 제거합니다:

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
`ucfirst` 메서드는 문자열의 첫 번째 문자를 대문자로 변환하여 반환합니다:

```
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
<!-- #### `ucsplit` -->
#### `ucsplit`

<!-- The `ucsplit` method splits the given string into a collection by uppercase characters: -->
`ucsplit` 메서드는 문자열에서 대문자 문자를 기준으로 분리하여 컬렉션으로 반환합니다:

```
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo', 'Bar'])
```

<a name="method-fluent-str-unwrap"></a>
<!-- #### `unwrap` -->
#### `unwrap`

<!-- The `unwrap` method removes the specified strings from the beginning and end of a given string: -->
`unwrap` 메서드는 문자열의 시작과 끝에서 지정한 문자를 제거합니다:

```
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
`upper` 메서드는 주어진 문자열을 모두 대문자로 변환합니다:

```
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
<!-- #### `when` -->
#### `when`

<!-- The `when` method invokes the given closure if a given condition is `true`. The closure will receive the fluent string instance: -->
`when` 메서드는 지정한 조건이 `true`일 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Taylor')
                ->when(true, function (Stringable $string) {
                    return $string->append(' Otwell');
                });

// 'Taylor Otwell'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the condition parameter evaluates to `false`. -->
필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 조건이 `false`로 평가될 때 실행됩니다.

<a name="method-fluent-str-when-contains"></a>
<!-- #### `whenContains` -->
#### `whenContains`

<!-- The `whenContains` method invokes the given closure if the string contains the given value. The closure will receive the fluent string instance: -->
`whenContains` 메서드는 문자열이 지정한 값을 포함하는 경우, 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
            ->whenContains('tony', function (Stringable $string) {
                return $string->title();
            });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the string does not contain the given value. -->
필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 문자열에 지정한 값이 포함되지 않을 때 실행됩니다.

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
또한 문자열이 배열 내의 값 중 하나라도 포함하는지 확인할 때, 값의 배열을 전달할 수도 있습니다:

```
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
`whenContainsAll` 메서드는 문자열이 지정한 모든 하위 문자열을 포함하고 있을 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
                ->whenContainsAll(['tony', 'stark'], function (Stringable $string) {
                    return $string->title();
                });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the condition parameter evaluates to `false`. -->
필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 조건이 `false`로 평가될 때 실행됩니다.

<a name="method-fluent-str-when-empty"></a>
<!-- #### `whenEmpty` -->
#### `whenEmpty`

<!-- The `whenEmpty` method invokes the given closure if the string is empty. If the closure returns a value, that value will also be returned by the `whenEmpty` method. If the closure does not return a value, the fluent string instance will be returned: -->
`whenEmpty` 메서드는 문자열이 비어 있을 때 주어진 클로저를 실행합니다. 클로저가 값을 반환하면, 그 값이 `whenEmpty`의 반환값이 됩니다. 클로저가 값을 반환하지 않을 경우, fluent string 인스턴스가 반환됩니다:

```
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('  ')->whenEmpty(function (Stringable $string) {
    return $string->trim()->prepend('Laravel');
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-empty"></a>
<!-- #### `whenNotEmpty` -->
#### `whenNotEmpty`

<!-- The `whenNotEmpty` method invokes the given closure if the string is not empty. If the closure returns a value, that value will also be returned by the `whenNotEmpty` method. If the closure does not return a value, the fluent string instance will be returned: -->
`whenNotEmpty` 메서드는 문자열이 비어 있지 않을 때 주어진 클로저를 실행합니다. 클로저가 값을 반환하면, 그 값이 `whenNotEmpty`의 반환값이 됩니다. 클로저가 값을 반환하지 않을 경우, fluent string 인스턴스가 반환됩니다:

```
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
`whenStartsWith` 메서드는 문자열이 지정한 하위 문자열로 시작할 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenEndsWith` 메서드는 문자열이 지정한 하위 문자열로 끝날 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenExactly` 메서드는 문자열이 지정한 문자열과 정확하게 일치할 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenNotExactly` 메서드는 문자열이 지정한 문자열과 정확히 일치하지 않을 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenIs` 메서드는 문자열이 지정한 패턴과 일치할 때 주어진 클로저를 실행합니다. 별표(*)는 와일드카드 값으로 사용할 수 있습니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenIsAscii` 메서드는 문자열이 7비트 ASCII 문자로만 이루어져 있을 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenIsUlid` 메서드는 문자열이 올바른 ULID 형식일 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenIsUuid` 메서드는 문자열이 올바른 UUID 형식일 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`whenTest` 메서드는 문자열이 주어진 정규 표현식과 일치할 때 주어진 클로저를 실행합니다. 이 클로저는 fluent string 인스턴스를 인수로 받습니다:

```
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
`wordCount` 메서드는 문자열에 포함된 단어의 개수를 반환합니다:

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
<!-- #### `words` -->
#### `words`

<!-- The `words` method limits the number of words in a string. If necessary, you may specify an additional string that will be appended to the truncated string: -->
`words` 메서드는 문자열의 단어 수를 제한합니다. 필요하다면, 잘린 문자열 끝에 추가할 문자열을 두 번째 인자로 지정할 수 있습니다:

```
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```
