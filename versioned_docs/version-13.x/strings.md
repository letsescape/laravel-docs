# 문자열 (Strings)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel에는 문자열 값을 조작하기 위한 다양한 함수가 포함되어 있습니다. 이러한 함수 중 많은 부분은 프레임워크 자체에서도 사용됩니다. 하지만 편리하다고 느낀다면 여러분의 애플리케이션에서도 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<a name="strings-method-list"></a>
### 문자열

<div class="collection-method-list" markdown="1">

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

</div>

<a name="fluent-strings-method-list"></a>
### 플루언트 문자열

<div class="collection-method-list" markdown="1">

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

</div>

<a name="strings"></a>
## 문자열 (Strings)

<a name="method-__"></a>
#### `__()` {.collection-method}

`__` 함수는 주어진 번역 문자열 또는 번역 키를 사용자의 [언어 파일](/docs/13.x/localization)을 통해 번역합니다.

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

지정한 번역 문자열이나 키가 존재하지 않으면 `__` 함수는 주어진 값을 그대로 반환합니다. 따라서 위 예시에서 해당 번역 키가 존재하지 않는다면 `__` 함수는 `messages.welcome`을 반환합니다.

<a name="method-class-basename"></a>
#### `class_basename()` {.collection-method}

`class_basename` 함수는 주어진 클래스에서 해당 클래스의 네임스페이스를 제거한 클래스명을 반환합니다.

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()` {.collection-method}

`e` 함수는 PHP의 `htmlspecialchars` 함수를 실행하며, 기본적으로 `double_encode` 옵션을 `true`로 설정합니다.

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()` {.collection-method}

`preg_replace_array` 함수는 문자열에서 주어진 패턴을 배열의 값으로 순서대로 치환합니다.

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()` {.collection-method}

`Str::after` 메서드는 문자열에서 주어진 값 뒤의 모든 내용을 반환합니다. 해당 값이 문자열 안에 존재하지 않으면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()` {.collection-method}

`Str::afterLast` 메서드는 문자열에서 주어진 값이 마지막으로 나타난 위치 뒤의 모든 내용을 반환합니다. 해당 값이 문자열 안에 존재하지 않으면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
#### `Str::apa()` {.collection-method}

`Str::apa` 메서드는 주어진 문자열을 [APA 지침](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따른 제목 표기법으로 변환합니다.

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()` {.collection-method}

`Str::ascii` 메서드는 문자열을 ASCII 값으로 음역하려고 시도합니다.

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()` {.collection-method}

`Str::before` 메서드는 문자열에서 주어진 값 앞의 모든 내용을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()` {.collection-method}

`Str::beforeLast` 메서드는 문자열에서 주어진 값이 마지막으로 나타난 위치 앞의 모든 내용을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
#### `Str::between()` {.collection-method}

`Str::between` 메서드는 두 값 사이에 있는 문자열 부분을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()` {.collection-method}
`Str::betweenFirst` 메서드는 두 값 사이에서 가능한 가장 짧은 문자열 부분을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()` {.collection-method}

`Str::camel` 메서드는 주어진 문자열을 `camelCase`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
#### `Str::charAt()` {.collection-method}

`Str::charAt` 메서드는 지정한 인덱스의 문자를 반환합니다. 인덱스가 범위를 벗어나면 `false`가 반환됩니다:

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
#### `Str::chopStart()` {.collection-method}

`Str::chopStart` 메서드는 주어진 값이 문자열의 시작 부분에 있을 때만 해당 값이 처음 나타나는 부분을 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

두 번째 인수로 배열을 전달할 수도 있습니다. 문자열이 배열의 값 중 하나로 시작하면, 해당 값이 문자열에서 제거됩니다:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()` {.collection-method}

`Str::chopEnd` 메서드는 주어진 값이 문자열의 끝 부분에 있을 때만 해당 값이 마지막으로 나타나는 부분을 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

두 번째 인수로 배열을 전달할 수도 있습니다. 문자열이 배열의 값 중 하나로 끝나면, 해당 값이 문자열에서 제거됩니다:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
#### `Str::contains()` {.collection-method}

`Str::contains` 메서드는 주어진 문자열에 주어진 값이 포함되어 있는지 판단합니다. 기본적으로 이 메서드는 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

주어진 문자열에 배열의 값 중 하나라도 포함되어 있는지 판단하려면 값의 배열을 전달할 수도 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()` {.collection-method}

`Str::containsAll` 메서드는 주어진 문자열에 주어진 배열의 모든 값이 포함되어 있는지 판단합니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()` {.collection-method}

`Str::doesntContain` 메서드는 주어진 문자열에 주어진 값이 포함되어 있지 않은지 판단합니다. 기본적으로 이 메서드는 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

주어진 문자열에 배열의 값이 하나도 포함되어 있지 않은지 판단하려면 값의 배열을 전달할 수도 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'framework']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
#### `Str::deduplicate()` {.collection-method}

`Str::deduplicate` 메서드는 주어진 문자열에서 연속해서 나타나는 문자를 해당 문자 하나로 바꿉니다. 기본적으로 이 메서드는 공백의 중복을 제거합니다:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

메서드의 두 번째 인수로 다른 문자를 전달하여 중복을 제거할 문자를 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-str-doesnt-end-with"></a>
#### `Str::doesntEndWith()` {.collection-method}

`Str::doesntEndWith` 메서드는 주어진 문자열이 주어진 값으로 끝나지 않는지 판단합니다:

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', 'dog');

// true
```

주어진 문자열이 배열의 값 중 어느 것으로도 끝나지 않는지 판단하려면 값의 배열을 전달할 수도 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', ['this', 'foo']);

// true

$result = Str::doesntEndWith('This is my name', ['name', 'foo']);

// false
```

<a name="method-str-doesnt-start-with"></a>
#### `Str::doesntStartWith()` {.collection-method}

`Str::doesntStartWith` 메서드는 주어진 문자열이 주어진 값으로 시작하지 않는지 판단합니다:

```php
use Illuminate\Support\Str;

$result = Str::doesntStartWith('This is my name', 'That');

// true
```

가능한 값의 배열을 전달하면, 문자열이 주어진 값 중 어느 것으로도 시작하지 않을 때 `doesntStartWith` 메서드는 `true`를 반환합니다:

```php
$result = Str::doesntStartWith('This is my name', ['What', 'That', 'There']);

// true
```

<a name="method-ends-with"></a>
#### `Str::endsWith()` {.collection-method}

`Str::endsWith` 메서드는 주어진 문자열이 주어진 값으로 끝나는지 판단합니다:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

주어진 문자열이 배열의 값 중 하나로 끝나는지 판단하려면 값의 배열을 전달할 수도 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()` {.collection-method}

`Str::excerpt` 메서드는 주어진 문자열 안에서 특정 구문이 처음 나타나는 위치와 일치하는 발췌문을 추출합니다:

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

기본값이 `100`인 `radius` 옵션을 사용하면 잘린 문자열의 양쪽에 표시할 문자 수를 정의할 수 있습니다.

또한 `omission` 옵션을 사용하여 잘린 문자열 앞뒤에 추가할 문자열을 정의할 수 있습니다:

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-str-finish"></a>
#### `Str::finish()` {.collection-method}

`Str::finish` 메서드는 문자열이 주어진 값으로 끝나지 않는 경우, 해당 값을 문자열 끝에 한 번만 추가합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-from-base64"></a>
#### `Str::fromBase64()` {.collection-method}

`Str::fromBase64` 메서드는 주어진 Base64 문자열을 디코딩합니다:

```php
use Illuminate\Support\Str;

$decoded = Str::fromBase64('TGFyYXZlbA==');

// Laravel
```

<a name="method-str-headline"></a>
#### `Str::headline()` {.collection-method}

`Str::headline` 메서드는 대소문자 형식, 하이픈, 밑줄로 구분된 문자열을 공백으로 구분된 문자열로 변환하고, 각 단어의 첫 글자를 대문자로 만듭니다:

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-initials"></a>
#### `Str::initials()` {.collection-method}

`Str::initials` 메서드는 주어진 문자열의 이니셜을 반환하며, 선택적으로 대문자로 변환할 수 있습니다:

```php
use Illuminate\Support\Str;

$initials = Str::initials('taylor otwell');

// to

$initials = Str::initials('taylor otwell', capitalize: true);

// TO
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()` {.collection-method}

`Str::inlineMarkdown` 메서드는 [CommonMark](https://commonmark.thephpleague.com/)를 사용하여 GitHub flavored Markdown을 인라인 HTML로 변환합니다. 하지만 `markdown` 메서드와 달리 생성된 모든 HTML을 블록 수준 요소로 감싸지 않습니다:

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

#### Markdown 보안

기본적으로 Markdown은 원시 HTML을 지원하며, 원시 사용자 입력과 함께 사용하면 Cross-Site Scripting (XSS) 취약점에 노출됩니다. [CommonMark Security 문서](https://commonmark.thephpleague.com/security/)에 따르면, `html_input` 옵션을 사용하여 원시 HTML을 이스케이프하거나 제거할 수 있고, `allow_unsafe_links` 옵션을 사용하여 안전하지 않은 링크를 허용할지 지정할 수 있습니다. 일부 원시 HTML을 허용해야 한다면, 컴파일된 Markdown을 HTML Purifier에 통과시켜야 합니다:

```php
use Illuminate\Support\Str;

Str::inlineMarkdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-str-is"></a>
#### `Str::is()` {.collection-method}

`Str::is` 메서드는 주어진 문자열이 주어진 패턴과 일치하는지 판단합니다. 별표는 와일드카드 값으로 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```
`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()` {.collection-method}

`Str::isAscii` 메서드는 주어진 문자열이 7비트 ASCII인지 확인합니다:

```php
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()` {.collection-method}

`Str::isJson` 메서드는 주어진 문자열이 유효한 JSON인지 확인합니다:

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
#### `Str::isUrl()` {.collection-method}

`Str::isUrl` 메서드는 주어진 문자열이 유효한 URL인지 확인합니다:

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

`isUrl` 메서드는 다양한 프로토콜을 유효한 것으로 간주합니다. 하지만 `isUrl` 메서드에 프로토콜을 전달하여 어떤 프로토콜을 유효한 것으로 간주할지 지정할 수 있습니다:

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()` {.collection-method}

`Str::isUlid` 메서드는 주어진 문자열이 유효한 ULID인지 확인합니다:

```php
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()` {.collection-method}

`Str::isUuid` 메서드는 주어진 문자열이 유효한 UUID인지 확인합니다:

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

주어진 UUID가 특정 버전(1, 3, 4, 5, 6, 7 또는 8)의 UUID 사양과 일치하는지도 검증할 수 있습니다:

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 4);

// true

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 1);

// false
```

<a name="method-kebab-case"></a>
#### `Str::kebab()` {.collection-method}

`Str::kebab` 메서드는 주어진 문자열을 `kebab-case`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()` {.collection-method}

`Str::lcfirst` 메서드는 주어진 문자열의 첫 번째 문자를 소문자로 바꿔 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()` {.collection-method}

`Str::length` 메서드는 주어진 문자열의 길이를 반환합니다:

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()` {.collection-method}

`Str::limit` 메서드는 주어진 문자열을 지정한 길이로 잘라냅니다:

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

메서드에 세 번째 인수를 전달하여 잘린 문자열 끝에 덧붙일 문자열을 변경할 수 있습니다:

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

문자열을 잘라낼 때 완전한 단어를 보존하고 싶다면 `preserveWords` 인수를 사용할 수 있습니다. 이 인수가 `true`이면 문자열은 가장 가까운 완전한 단어 경계에서 잘립니다:

```php
$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

// The quick...
```

<a name="method-str-lower"></a>
#### `Str::lower()` {.collection-method}

`Str::lower` 메서드는 주어진 문자열을 소문자로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
#### `Str::markdown()` {.collection-method}

`Str::markdown` 메서드는 [CommonMark](https://commonmark.thephpleague.com/)를 사용하여 GitHub Flavored Markdown을 HTML로 변환합니다:

```php
use Illuminate\Support\Str;

$html = Str::markdown('# Laravel');

// <h1>Laravel</h1>

$html = Str::markdown('# Taylor <b>Otwell</b>', [
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### Markdown 보안

기본적으로 Markdown은 원시 HTML을 지원하므로, 원시 사용자 입력과 함께 사용하면 Cross-Site Scripting (XSS) 취약점에 노출될 수 있습니다. [CommonMark Security 문서](https://commonmark.thephpleague.com/security/)에 따르면, `html_input` 옵션을 사용하여 원시 HTML을 이스케이프하거나 제거할 수 있고, `allow_unsafe_links` 옵션을 사용하여 안전하지 않은 링크를 허용할지 지정할 수 있습니다. 일부 원시 HTML을 허용해야 한다면, 컴파일된 Markdown을 HTML Purifier에 통과시켜야 합니다:

```php
use Illuminate\Support\Str;

Str::markdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-str-mask"></a>
#### `Str::mask()` {.collection-method}

`Str::mask` 메서드는 문자열의 일부를 반복되는 문자로 마스킹합니다. 이메일 주소나 전화번호 같은 문자열의 일부를 감추는 데 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

필요하다면 `mask` 메서드의 세 번째 인수로 음수를 전달할 수 있습니다. 이렇게 하면 메서드는 문자열 끝에서부터 주어진 거리만큼 떨어진 위치에서 마스킹을 시작합니다:

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-match"></a>
#### `Str::match()` {.collection-method}

`Str::match` 메서드는 주어진 정규 표현식 패턴과 일치하는 문자열의 일부를 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::match('/bar/', 'foo bar');

// 'bar'

$result = Str::match('/foo (.*)/', 'foo bar');

// 'bar'
```

<a name="method-str-match-all"></a>
#### `Str::matchAll()` {.collection-method}

`Str::matchAll` 메서드는 주어진 정규 표현식 패턴과 일치하는 문자열의 부분들을 담은 컬렉션을 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/bar/', 'bar foo bar');

// collect(['bar', 'bar'])
```

표현식 안에 매칭 그룹을 지정하면, Laravel은 첫 번째 매칭 그룹에 해당하는 결과들의 컬렉션을 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

// collect(['un', 'ly']);
```

일치하는 항목이 없으면 빈 컬렉션이 반환됩니다.

<a name="method-str-is-match"></a>
#### `Str::isMatch()` {.collection-method}

`Str::isMatch` 메서드는 문자열이 주어진 정규 표현식과 일치하면 `true`를 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::isMatch('/foo (.*)/', 'foo bar');

// true

$result = Str::isMatch('/foo (.*)/', 'laravel');

// false
```

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()` {.collection-method}

`Str::orderedUuid` 메서드는 인덱스가 있는 데이터베이스 컬럼에 효율적으로 저장할 수 있는 "timestamp first" UUID를 생성합니다. 이 메서드로 생성되는 각 UUID는 이전에 이 메서드로 생성된 UUID 뒤에 정렬됩니다:

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()` {.collection-method}

`Str::padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸는 메서드입니다. 최종 문자열이 원하는 길이에 도달할 때까지 문자열의 양쪽을 다른 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()` {.collection-method}

`Str::padLeft` 메서드는 PHP의 `str_pad` 함수를 감싸는 메서드입니다. 최종 문자열이 원하는 길이에 도달할 때까지 문자열의 왼쪽을 다른 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()` {.collection-method}

`Str::padRight` 메서드는 PHP의 `str_pad` 함수를 감싸는 메서드입니다. 최종 문자열이 원하는 길이에 도달할 때까지 문자열의 오른쪽을 다른 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
#### `Str::password()` {.collection-method}

`Str::password` 메서드는 주어진 길이의 안전한 무작위 비밀번호를 생성하는 데 사용할 수 있습니다. 비밀번호는 문자, 숫자, 기호, 공백의 조합으로 구성됩니다. 기본적으로 비밀번호 길이는 32자입니다:

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
#### `Str::plural()` {.collection-method}

`Str::plural` 메서드는 단수 단어 문자열을 복수형으로 변환합니다. 이 함수는 [Laravel의 pluralizer가 지원하는 모든 언어](/docs/13.x/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```
정수를 두 번째 인수로 전달하면 문자열의 단수형 또는 복수형을 가져올 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

`prependCount` 인수를 제공하면 복수형으로 변환된 문자열 앞에 형식이 적용된 `$count`를 붙일 수 있습니다:

```php
use Illuminate\Support\Str;

$label = Str::plural('car', 1000, prependCount: true);

// 1,000 cars
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()` {.collection-method}

`Str::pluralStudly` 메서드는 studly caps case 형식의 단수 단어 문자열을 복수형으로 변환합니다. 이 함수는 [Laravel의 pluralizer가 지원하는 모든 언어](/docs/13.x/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

정수를 두 번째 인수로 전달하면 문자열의 단수형 또는 복수형을 가져올 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>
#### `Str::position()` {.collection-method}

`Str::position` 메서드는 문자열에서 부분 문자열이 처음 나타나는 위치를 반환합니다. 주어진 문자열에 해당 부분 문자열이 없으면 `false`를 반환합니다:

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
#### `Str::random()` {.collection-method}

`Str::random` 메서드는 지정된 길이의 무작위 문자열을 생성합니다. 이 함수는 PHP의 `random_bytes` 함수를 사용합니다:

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

테스트 중에는 `Str::random` 메서드가 반환하는 값을 "가짜" 값으로 대체하는 것이 유용할 수 있습니다. 이렇게 하려면 `createRandomStringsUsing` 메서드를 사용할 수 있습니다:

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

`random` 메서드가 다시 정상적으로 무작위 문자열을 생성하도록 하려면 `createRandomStringsNormally` 메서드를 호출하면 됩니다:

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
#### `Str::remove()` {.collection-method}

`Str::remove` 메서드는 문자열에서 주어진 값 또는 값의 배열을 제거합니다:

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

문자열을 제거할 때 대소문자를 무시하려면 `remove` 메서드의 세 번째 인수로 `false`를 전달할 수도 있습니다.

<a name="method-str-repeat"></a>
#### `Str::repeat()` {.collection-method}

`Str::repeat` 메서드는 주어진 문자열을 반복합니다:

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()` {.collection-method}

`Str::replace` 메서드는 문자열 안의 주어진 문자열을 교체합니다:

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

`replace` 메서드는 `caseSensitive` 인수도 받을 수 있습니다. 기본적으로 `replace` 메서드는 대소문자를 구분합니다:

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
#### `Str::replaceArray()` {.collection-method}

`Str::replaceArray` 메서드는 배열을 사용하여 문자열 안의 주어진 값을 순서대로 교체합니다:

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()` {.collection-method}

`Str::replaceFirst` 메서드는 문자열에서 주어진 값이 처음 나타나는 부분을 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()` {.collection-method}

`Str::replaceLast` 메서드는 문자열에서 주어진 값이 마지막으로 나타나는 부분을 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()` {.collection-method}

`Str::replaceMatches` 메서드는 패턴과 일치하는 문자열의 모든 부분을 주어진 대체 문자열로 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

`replaceMatches` 메서드는 클로저도 받을 수 있습니다. 이 클로저는 주어진 패턴과 일치하는 문자열의 각 부분을 전달받아 호출되므로, 클로저 안에서 교체 로직을 수행하고 교체된 값을 반환할 수 있습니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()` {.collection-method}

`Str::replaceStart` 메서드는 주어진 값이 문자열의 시작 부분에 나타나는 경우에만, 그 첫 번째 항목을 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()` {.collection-method}

`Str::replaceEnd` 메서드는 주어진 값이 문자열의 끝부분에 나타나는 경우에만, 그 마지막 항목을 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

// Hello Laravel

$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-reverse"></a>
#### `Str::reverse()` {.collection-method}

`Str::reverse` 메서드는 주어진 문자열을 뒤집습니다:

```php
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
#### `Str::singular()` {.collection-method}

`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. 이 함수는 [Laravel의 pluralizer가 지원하는 모든 언어](/docs/13.x/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()` {.collection-method}

`Str::slug` 메서드는 주어진 문자열에서 URL에 적합한 "슬러그(slug)"를 생성합니다:

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()` {.collection-method}

`Str::snake` 메서드는 주어진 문자열을 `snake_case`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()` {.collection-method}

`Str::squish` 메서드는 단어 사이의 불필요한 공백을 포함하여 문자열의 모든 불필요한 공백을 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()` {.collection-method}

`Str::start` 메서드는 문자열이 주어진 값으로 시작하지 않는 경우, 해당 값을 문자열 앞에 한 번만 추가합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()` {.collection-method}

`Str::startsWith` 메서드는 주어진 문자열이 주어진 값으로 시작하는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

가능한 값의 배열을 전달하면, 문자열이 주어진 값 중 하나로 시작할 때 `startsWith` 메서드는 `true`를 반환합니다:

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()` {.collection-method}

`Str::studly` 메서드는 주어진 문자열을 `StudlyCase`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()` {.collection-method}

`Str::substr` 메서드는 시작 위치와 길이 매개변수로 지정한 문자열의 일부를 반환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()` {.collection-method}
`Str::substrCount` 메서드는 주어진 문자열 안에서 지정한 값이 나타나는 횟수를 반환합니다.

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()` {.collection-method}

`Str::substrReplace` 메서드는 문자열의 일부 구간에 있는 텍스트를 교체합니다. 세 번째 인수로 지정한 위치에서 시작하여, 네 번째 인수로 지정한 문자 수만큼 교체합니다. 메서드의 네 번째 인수에 `0`을 전달하면 문자열에 있는 기존 문자를 교체하지 않고, 지정한 위치에 문자열을 삽입합니다.

```php
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()` {.collection-method}

`Str::swap` 메서드는 PHP의 `strtr` 함수를 사용하여 주어진 문자열 안의 여러 값을 교체합니다.

```php
use Illuminate\Support\Str;

$string = Str::swap([
    'Tacos' => 'Burritos',
    'great' => 'fantastic',
], 'Tacos are great!');

// Burritos are fantastic!
```

<a name="method-take"></a>
#### `Str::take()` {.collection-method}

`Str::take` 메서드는 문자열의 시작 부분에서 지정한 수만큼의 문자를 반환합니다.

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
#### `Str::title()` {.collection-method}

`Str::title` 메서드는 주어진 문자열을 `Title Case`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
#### `Str::toBase64()` {.collection-method}

`Str::toBase64` 메서드는 주어진 문자열을 Base64로 변환합니다.

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
#### `Str::transliterate()` {.collection-method}

`Str::transliterate` 메서드는 주어진 문자열을 가장 가까운 ASCII 표현으로 변환하려고 시도합니다.

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
#### `Str::trim()` {.collection-method}

`Str::trim` 메서드는 주어진 문자열의 시작과 끝에서 공백 또는 다른 문자를 제거합니다. PHP의 기본 `trim` 함수와 달리, `Str::trim` 메서드는 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
#### `Str::ltrim()` {.collection-method}

`Str::ltrim` 메서드는 주어진 문자열의 시작 부분에서 공백 또는 다른 문자를 제거합니다. PHP의 기본 `ltrim` 함수와 달리, `Str::ltrim` 메서드는 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
#### `Str::rtrim()` {.collection-method}

`Str::rtrim` 메서드는 주어진 문자열의 끝 부분에서 공백 또는 다른 문자를 제거합니다. PHP의 기본 `rtrim` 함수와 달리, `Str::rtrim` 메서드는 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()` {.collection-method}

`Str::ucfirst` 메서드는 주어진 문자열의 첫 문자를 대문자로 바꾸어 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()` {.collection-method}

`Str::ucsplit` 메서드는 주어진 문자열을 대문자를 기준으로 나누어 배열로 반환합니다.

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-ucwords"></a>
#### `Str::ucwords()` {.collection-method}

`Str::ucwords` 메서드는 주어진 문자열에서 각 단어의 첫 문자를 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$string = Str::ucwords('laravel framework');

// Laravel Framework
```

<a name="method-str-upper"></a>
#### `Str::upper()` {.collection-method}

`Str::upper` 메서드는 주어진 문자열을 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()` {.collection-method}

`Str::ulid` 메서드는 작고 시간순으로 정렬 가능한 고유 식별자인 ULID를 생성합니다.

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

주어진 ULID가 생성된 날짜와 시간을 나타내는 `Illuminate\Support\Carbon` 날짜 인스턴스를 가져오려면, Laravel의 Carbon 통합 기능에서 제공하는 `createFromId` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

테스트 중에는 `Str::ulid` 메서드가 반환하는 값을 “가짜로” 지정하는 것이 유용할 수 있습니다. 이를 위해 `createUlidsUsing` 메서드를 사용할 수 있습니다.

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

`ulid` 메서드가 다시 일반적인 방식으로 ULID를 생성하도록 하려면 `createUlidsNormally` 메서드를 호출하면 됩니다.

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
#### `Str::unwrap()` {.collection-method}

`Str::unwrap` 메서드는 주어진 문자열의 시작과 끝에서 지정한 문자열을 제거합니다.

```php
use Illuminate\Support\Str;

Str::unwrap('-Laravel-', '-');

// Laravel

Str::unwrap('{framework: "Laravel"}', '{', '}');

// framework: "Laravel"
```

<a name="method-str-uuid"></a>
#### `Str::uuid()` {.collection-method}

`Str::uuid` 메서드는 UUID(version 4)를 생성합니다.

```php
use Illuminate\Support\Str;

return (string) Str::uuid();
```

테스트 중에는 `Str::uuid` 메서드가 반환하는 값을 “가짜로” 지정하는 것이 유용할 수 있습니다. 이를 위해 `createUuidsUsing` 메서드를 사용할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

`uuid` 메서드가 다시 일반적인 방식으로 UUID를 생성하도록 하려면 `createUuidsNormally` 메서드를 호출하면 됩니다.

```php
Str::createUuidsNormally();
```

<a name="method-str-uuid7"></a>
#### `Str::uuid7()` {.collection-method}

`Str::uuid7` 메서드는 UUID(version 7)를 생성합니다.

```php
use Illuminate\Support\Str;

return (string) Str::uuid7();
```

선택적 파라미터로 `DateTimeInterface`를 전달할 수 있으며, 이 값은 순서가 있는 UUID를 생성하는 데 사용됩니다.

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()` {.collection-method}

`Str::wordCount` 메서드는 문자열에 포함된 단어 수를 반환합니다.

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()` {.collection-method}

`Str::wordWrap` 메서드는 문자열을 지정한 문자 수에 맞게 줄바꿈합니다.

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
#### `Str::words()` {.collection-method}

`Str::words` 메서드는 문자열의 단어 수를 제한합니다. 잘린 문자열의 끝에 덧붙일 문자열을 지정하려면 이 메서드의 세 번째 인수로 추가 문자열을 전달할 수 있습니다.

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
#### `Str::wrap()` {.collection-method}

`Str::wrap` 메서드는 주어진 문자열을 추가 문자열 또는 문자열 쌍으로 감쌉니다.

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
#### `str()` {.collection-method}

`str` 함수는 주어진 문자열의 새 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of` 메서드와 동일합니다.

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

`str` 함수에 인수를 제공하지 않으면, 이 함수는 `Illuminate\Support\Str` 인스턴스를 반환합니다.

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()` {.collection-method}

`trans` 함수는 [언어 파일](/docs/13.x/localization)을 사용하여 주어진 번역 키를 번역합니다.

```php
echo trans('messages.welcome');
```

지정한 번역 키가 존재하지 않으면 `trans` 함수는 주어진 키를 반환합니다. 따라서 위 예제에서 번역 키가 존재하지 않는다면 `trans` 함수는 `messages.welcome`을 반환합니다.

<a name="method-trans-choice"></a>
#### `trans_choice()` {.collection-method}

`trans_choice` 함수는 굴절(inflection)을 적용하여 주어진 번역 키를 번역합니다.

```php
echo trans_choice('messages.notifications', $unreadCount);
```

지정한 번역 키가 존재하지 않으면 `trans_choice` 함수는 주어진 키를 반환합니다. 따라서 위 예제에서 번역 키가 존재하지 않는다면 `trans_choice` 함수는 `messages.notifications`를 반환합니다.

<a name="fluent-strings"></a>
## 플루언트 문자열 (Fluent Strings)

플루언트 문자열은 문자열 값을 다루기 위한 더 유연한 객체 지향 인터페이스를 제공합니다. 이를 사용하면 기존 문자열 연산보다 읽기 쉬운 문법으로 여러 문자열 작업을 이어서 호출할 수 있습니다.

<a name="method-fluent-str-after"></a>
#### `after` {.collection-method}

`after` 메서드는 문자열에서 주어진 값 뒤에 있는 모든 내용을 반환합니다. 해당 값이 문자열 안에 없으면 전체 문자열이 반환됩니다.

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```
<a name="method-fluent-str-after-last"></a>
#### `afterLast` {.collection-method}

`afterLast` 메서드는 문자열에서 주어진 값이 마지막으로 나타난 지점 이후의 모든 내용을 반환합니다. 문자열 안에 해당 값이 없으면 전체 문자열이 반환됩니다:

```php
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-apa"></a>
#### `apa` {.collection-method}

`apa` 메서드는 주어진 문자열을 [APA 지침](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따른 제목 대소문자 형식으로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->apa();

// A Nice Title Uses the Correct Case
```

<a name="method-fluent-str-append"></a>
#### `append` {.collection-method}

`append` 메서드는 주어진 값을 문자열 뒤에 추가합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
#### `ascii` {.collection-method}

`ascii` 메서드는 문자열을 ASCII 값으로 음역하려고 시도합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
#### `basename` {.collection-method}

`basename` 메서드는 주어진 문자열의 마지막 이름 구성 요소를 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

필요하다면 마지막 구성 요소에서 제거할 "확장자"를 제공할 수 있습니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
#### `before` {.collection-method}

`before` 메서드는 문자열에서 주어진 값 앞의 모든 내용을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
#### `beforeLast` {.collection-method}

`beforeLast` 메서드는 문자열에서 주어진 값이 마지막으로 나타난 지점 앞의 모든 내용을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
#### `between` {.collection-method}

`between` 메서드는 두 값 사이에 있는 문자열 부분을 반환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
#### `betweenFirst` {.collection-method}

`betweenFirst` 메서드는 두 값 사이에서 가능한 가장 작은 문자열 부분을 반환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
#### `camel` {.collection-method}

`camel` 메서드는 주어진 문자열을 `camelCase`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// 'fooBar'
```

<a name="method-fluent-str-char-at"></a>
#### `charAt` {.collection-method}

`charAt` 메서드는 지정된 인덱스의 문자를 반환합니다. 인덱스가 범위를 벗어나면 `false`가 반환됩니다:

```php
use Illuminate\Support\Str;

$character = Str::of('This is my name.')->charAt(6);

// 's'
```

<a name="method-fluent-str-class-basename"></a>
#### `classBasename` {.collection-method}

`classBasename` 메서드는 주어진 클래스에서 클래스의 네임스페이스를 제거한 클래스명을 반환합니다:

```php
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// 'Baz'
```

<a name="method-fluent-str-chop-start"></a>
#### `chopStart` {.collection-method}

`chopStart` 메서드는 주어진 값이 문자열의 시작 부분에 나타나는 경우에만 그 첫 번째 값을 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopStart('https://');

// 'laravel.com'
```

배열을 전달할 수도 있습니다. 문자열이 배열 안의 값 중 하나로 시작하면 해당 값이 문자열에서 제거됩니다:

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopStart(['https://', 'http://']);

// 'laravel.com'
```

<a name="method-fluent-str-chop-end"></a>
#### `chopEnd` {.collection-method}

`chopEnd` 메서드는 주어진 값이 문자열의 끝 부분에 나타나는 경우에만 그 마지막 값을 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopEnd('.com');

// 'https://laravel'
```

배열을 전달할 수도 있습니다. 문자열이 배열 안의 값 중 하나로 끝나면 해당 값이 문자열에서 제거됩니다:

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopEnd(['.com', '.io']);

// 'http://laravel'
```

<a name="method-fluent-str-contains"></a>
#### `contains` {.collection-method}

`contains` 메서드는 주어진 문자열이 주어진 값을 포함하는지 확인합니다. 기본적으로 이 메서드는 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

값 배열을 전달하여 주어진 문자열이 배열 안의 값 중 하나라도 포함하는지 확인할 수도 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정하면 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('MY', ignoreCase: true);

// true
```

<a name="method-fluent-str-contains-all"></a>
#### `containsAll` {.collection-method}

`containsAll` 메서드는 주어진 문자열이 주어진 배열의 모든 값을 포함하는지 확인합니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

`ignoreCase` 인수를 `true`로 설정하면 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-fluent-str-decrypt"></a>
#### `decrypt` {.collection-method}

`decrypt` 메서드는 암호화된 문자열을 [복호화합니다](/docs/13.x/encryption):

```php
use Illuminate\Support\Str;

$decrypted = $encrypted->decrypt();

// 'secret'
```

`decrypt`의 반대 동작은 [encrypt](#method-fluent-str-encrypt) 메서드를 참고하십시오.

<a name="method-fluent-str-deduplicate"></a>
#### `deduplicate` {.collection-method}

`deduplicate` 메서드는 주어진 문자열에서 연속해서 나타나는 같은 문자를 하나의 문자로 바꿉니다. 기본적으로 이 메서드는 공백을 중복 제거합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('The   Laravel   Framework')->deduplicate();

// The Laravel Framework
```

메서드의 두 번째 인수로 다른 문자를 전달하여 중복 제거할 문자를 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::of('The---Laravel---Framework')->deduplicate('-');

// The-Laravel-Framework
```

<a name="method-fluent-str-dirname"></a>
#### `dirname` {.collection-method}

`dirname` 메서드는 주어진 문자열의 상위 디렉터리 부분을 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

필요하다면 문자열에서 제거할 디렉터리 레벨 수를 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-doesnt-contain"></a>
#### `doesntContain()` {.collection-method}

`doesntContain` 메서드는 주어진 문자열이 주어진 값을 포함하지 않는지 확인합니다. 이 메서드는 [contains](#method-fluent-str-contains) 메서드의 반대입니다. 기본적으로 이 메서드는 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain('my');

// true
```

값 배열을 전달하여 주어진 문자열이 배열 안의 어떤 값도 포함하지 않는지 확인할 수도 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain(['my', 'framework']);

// true
```

`ignoreCase` 인수를 `true`로 설정하면 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is my name')->doesntContain('MY', ignoreCase: true);

// false
```

<a name="method-fluent-str-doesnt-end-with"></a>
#### `doesntEndWith` {.collection-method}

`doesntEndWith` 메서드는 주어진 문자열이 주어진 값으로 끝나지 않는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith('dog');

// true
```

값 배열을 전달하여 주어진 문자열이 배열 안의 어떤 값으로도 끝나지 않는지 확인할 수도 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith(['this', 'foo']);

// true

$result = Str::of('This is my name')->doesntEndWith(['name', 'foo']);

// false
```

<a name="method-fluent-str-doesnt-start-with"></a>
#### `doesntStartWith` {.collection-method}

`doesntStartWith` 메서드는 주어진 문자열이 주어진 값으로 시작하지 않는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith('That');

// true
```
주어진 문자열이 배열에 있는 어떤 값으로도 시작하지 않는지 확인하려면 값의 배열을 전달할 수도 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith(['What', 'That', 'There']);

// true
```

<a name="method-fluent-str-encrypt"></a>
#### `encrypt` {.collection-method}

`encrypt` 메서드는 문자열을 [암호화](/docs/13.x/encryption)합니다.

```php
use Illuminate\Support\Str;

$encrypted = Str::of('secret')->encrypt();
```

`encrypt`의 반대 작업은 [decrypt](#method-fluent-str-decrypt) 메서드를 참고하세요.

<a name="method-fluent-str-ends-with"></a>
#### `endsWith` {.collection-method}

`endsWith` 메서드는 주어진 문자열이 주어진 값으로 끝나는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

주어진 문자열이 배열에 있는 값 중 하나로 끝나는지 확인하려면 값의 배열을 전달할 수도 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith(['name', 'foo']);

// true

$result = Str::of('This is my name')->endsWith(['this', 'foo']);

// false
```

<a name="method-fluent-str-exactly"></a>
#### `exactly` {.collection-method}

`exactly` 메서드는 주어진 문자열이 다른 문자열과 정확히 일치하는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-excerpt"></a>
#### `excerpt` {.collection-method}

`excerpt` 메서드는 문자열 안에서 특정 구문이 처음 나타나는 부분과 일치하는 발췌문을 문자열에서 추출합니다.

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

기본값이 `100`인 `radius` 옵션을 사용하면 잘린 문자열의 양쪽에 표시할 문자 수를 정의할 수 있습니다.

또한 `omission` 옵션을 사용해 잘린 문자열 앞뒤에 붙일 문자열을 변경할 수 있습니다.

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-fluent-str-explode"></a>
#### `explode` {.collection-method}

`explode` 메서드는 주어진 구분자로 문자열을 나누고, 나누어진 문자열의 각 부분을 담은 컬렉션을 반환합니다.

```php
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
#### `finish` {.collection-method}

`finish` 메서드는 문자열이 이미 주어진 값으로 끝나지 않는 경우, 해당 값을 문자열 끝에 한 번만 추가합니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-from-base64"></a>
#### `fromBase64` {.collection-method}

`fromBase64` 메서드는 주어진 Base64 문자열을 디코딩합니다.

```php
use Illuminate\Support\Str;

$decoded = Str::of('TGFyYXZlbA==')->fromBase64();

// Laravel
```

<a name="method-fluent-str-hash"></a>
#### `hash` {.collection-method}

`hash` 메서드는 주어진 [알고리즘](https://www.php.net/manual/en/function.hash-algos.php)을 사용해 문자열을 해시합니다.

```php
use Illuminate\Support\Str;

$hashed = Str::of('secret')->hash(algorithm: 'sha256');

// '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
```

<a name="method-fluent-str-headline"></a>
#### `headline` {.collection-method}

`headline` 메서드는 대소문자 경계, 하이픈, 밑줄로 구분된 문자열을 공백으로 구분된 문자열로 변환하고, 각 단어의 첫 글자를 대문자로 만듭니다.

```php
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-initials"></a>
#### `initials` {.collection-method}

`initials` 메서드는 문자열을 이니셜로 변환합니다.

```php
use Illuminate\Support\Str;

$initials = Str::of('Taylor Otwell')->initials()->upper();

// TO
```

<a name="method-fluent-str-inline-markdown"></a>
#### `inlineMarkdown` {.collection-method}

`inlineMarkdown` 메서드는 [CommonMark](https://commonmark.thephpleague.com/)를 사용해 GitHub flavored Markdown을 인라인 HTML로 변환합니다. 하지만 `markdown` 메서드와 달리, 생성된 모든 HTML을 블록 수준 요소로 감싸지 않습니다.

```php
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

#### Markdown 보안

기본적으로 Markdown은 원시 HTML을 지원하므로, 사용자가 입력한 원시 데이터를 그대로 사용할 경우 Cross-Site Scripting (XSS) 취약점에 노출됩니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따르면 `html_input` 옵션을 사용해 원시 HTML을 이스케이프하거나 제거할 수 있으며, `allow_unsafe_links` 옵션으로 안전하지 않은 링크를 허용할지 지정할 수 있습니다. 일부 원시 HTML을 허용해야 한다면 컴파일된 Markdown을 HTML Purifier에 통과시켜야 합니다.

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->inlineMarkdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-fluent-str-is"></a>
#### `is` {.collection-method}

`is` 메서드는 주어진 문자열이 주어진 패턴과 일치하는지 확인합니다. 별표는 와일드카드 값으로 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

$matches = Str::of('foobar')->is('foo*');

// true

$matches = Str::of('foobar')->is('baz*');

// false
```

<a name="method-fluent-str-is-ascii"></a>
#### `isAscii` {.collection-method}

`isAscii` 메서드는 주어진 문자열이 ASCII 문자열인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('Taylor')->isAscii();

// true

$result = Str::of('ü')->isAscii();

// false
```

<a name="method-fluent-str-is-empty"></a>
#### `isEmpty` {.collection-method}

`isEmpty` 메서드는 주어진 문자열이 비어 있는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isEmpty();

// true

$result = Str::of('Laravel')->trim()->isEmpty();

// false
```

<a name="method-fluent-str-is-not-empty"></a>
#### `isNotEmpty` {.collection-method}

`isNotEmpty` 메서드는 주어진 문자열이 비어 있지 않은지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-json"></a>
#### `isJson` {.collection-method}

`isJson` 메서드는 주어진 문자열이 유효한 JSON인지 확인합니다.

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
#### `isUlid` {.collection-method}

`isUlid` 메서드는 주어진 문자열이 ULID인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-url"></a>
#### `isUrl` {.collection-method}

`isUrl` 메서드는 주어진 문자열이 URL인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('http://example.com')->isUrl();

// true

$result = Str::of('Taylor')->isUrl();

// false
```

`isUrl` 메서드는 다양한 프로토콜을 유효한 것으로 간주합니다. 하지만 유효한 것으로 간주할 프로토콜을 `isUrl` 메서드에 전달해 지정할 수 있습니다.

```php
$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

<a name="method-fluent-str-is-uuid"></a>
#### `isUuid` {.collection-method}

`isUuid` 메서드는 주어진 문자열이 UUID인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

주어진 UUID가 특정 버전(1, 3, 4, 5, 6, 7 또는 8)의 UUID 명세와 일치하는지도 유효성 검증할 수 있습니다.

```php
use Illuminate\Support\Str;

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 4);

// true

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 1);

// false
```

<a name="method-fluent-str-kebab"></a>
#### `kebab` {.collection-method}

`kebab` 메서드는 주어진 문자열을 `kebab-case`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
#### `lcfirst` {.collection-method}

`lcfirst` 메서드는 주어진 문자열의 첫 번째 문자를 소문자로 바꾸어 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```

<a name="method-fluent-str-length"></a>
#### `length` {.collection-method}

`length` 메서드는 주어진 문자열의 길이를 반환합니다.

```php
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```
<a name="method-fluent-str-limit"></a>
#### `limit` {.collection-method}

`limit` 메서드는 주어진 문자열을 지정한 길이로 잘라냅니다:

```php
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

잘린 문자열의 끝에 붙일 문자열을 변경하려면 두 번째 인수를 전달할 수도 있습니다:

```php
$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

문자열을 자를 때 완전한 단어를 보존하고 싶다면 `preserveWords` 인수를 사용할 수 있습니다. 이 인수가 `true`이면 문자열은 가장 가까운 완전한 단어 경계에서 잘립니다:

```php
$truncated = Str::of('The quick brown fox')->limit(12, preserveWords: true);

// The quick...
```

<a name="method-fluent-str-lower"></a>
#### `lower` {.collection-method}

`lower` 메서드는 주어진 문자열을 소문자로 변환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-markdown"></a>
#### `markdown` {.collection-method}

`markdown` 메서드는 GitHub flavored Markdown을 HTML로 변환합니다:

```php
use Illuminate\Support\Str;

$html = Str::of('# Laravel')->markdown();

// <h1>Laravel</h1>

$html = Str::of('# Taylor <b>Otwell</b>')->markdown([
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### Markdown 보안

기본적으로 Markdown은 원시 HTML을 지원하므로, 사용자 입력을 그대로 사용할 경우 Cross-Site Scripting (XSS) 취약점에 노출될 수 있습니다. [CommonMark Security 문서](https://commonmark.thephpleague.com/security/)에 따르면, `html_input` 옵션을 사용해 원시 HTML을 이스케이프하거나 제거할 수 있으며, `allow_unsafe_links` 옵션으로 안전하지 않은 링크를 허용할지 지정할 수 있습니다. 일부 원시 HTML을 허용해야 한다면, 컴파일된 Markdown을 HTML Purifier에 통과시켜야 합니다:

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->markdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-fluent-str-mask"></a>
#### `mask` {.collection-method}

`mask` 메서드는 문자열의 일부를 반복되는 문자로 가립니다. 이메일 주소나 전화번호와 같은 문자열의 일부 구간을 숨기는 데 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

필요하다면 `mask` 메서드의 세 번째 또는 네 번째 인수로 음수를 전달할 수 있습니다. 이렇게 하면 문자열 끝에서부터 지정한 거리만큼 떨어진 위치에서 마스킹을 시작하도록 지시합니다:

```php
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
#### `match` {.collection-method}

`match` 메서드는 주어진 정규 표현식 패턴과 일치하는 문자열의 일부를 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->match('/bar/');

// 'bar'

$result = Str::of('foo bar')->match('/foo (.*)/');

// 'bar'
```

<a name="method-fluent-str-match-all"></a>
#### `matchAll` {.collection-method}

`matchAll` 메서드는 주어진 정규 표현식 패턴과 일치하는 문자열의 부분들을 담은 컬렉션을 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

표현식 안에 매칭 그룹을 지정하면, Laravel은 첫 번째 매칭 그룹에 해당하는 결과들의 컬렉션을 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

일치하는 항목이 없으면 빈 컬렉션이 반환됩니다.

<a name="method-fluent-str-is-match"></a>
#### `isMatch` {.collection-method}

`isMatch` 메서드는 문자열이 주어진 정규 표현식과 일치하면 `true`를 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->isMatch('/foo (.*)/');

// true

$result = Str::of('laravel')->isMatch('/foo (.*)/');

// false
```

<a name="method-fluent-str-new-line"></a>
#### `newLine` {.collection-method}

`newLine` 메서드는 문자열에 "end of line" 문자를 추가합니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
#### `padBoth` {.collection-method}

`padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸며, 최종 문자열이 원하는 길이에 도달할 때까지 문자열의 양쪽을 다른 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padBoth(10, '_');

// '__James___'

$padded = Str::of('James')->padBoth(10);

// '  James   '
```

<a name="method-fluent-str-padleft"></a>
#### `padLeft` {.collection-method}

`padLeft` 메서드는 PHP의 `str_pad` 함수를 감싸며, 최종 문자열이 원하는 길이에 도달할 때까지 문자열의 왼쪽을 다른 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padLeft(10, '-=');

// '-=-=-James'

$padded = Str::of('James')->padLeft(10);

// '     James'
```

<a name="method-fluent-str-padright"></a>
#### `padRight` {.collection-method}

`padRight` 메서드는 PHP의 `str_pad` 함수를 감싸며, 최종 문자열이 원하는 길이에 도달할 때까지 문자열의 오른쪽을 다른 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padRight(10, '-');

// 'James-----'

$padded = Str::of('James')->padRight(10);

// 'James     '
```

<a name="method-fluent-str-pipe"></a>
#### `pipe` {.collection-method}

`pipe` 메서드는 현재 문자열 값을 주어진 호출 가능 객체(callable)에 전달하여 문자열을 변환할 수 있게 해줍니다:

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
#### `plural` {.collection-method}

`plural` 메서드는 단수 단어 문자열을 복수형으로 변환합니다. 이 함수는 [Laravel의 pluralizer가 지원하는 모든 언어](/docs/13.x/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

함수에 정수 인수를 전달하여 문자열의 단수형 또는 복수형을 가져올 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

`prependCount` 인수를 전달하면 복수형으로 변환된 문자열 앞에 형식화된 `$count`를 붙일 수 있습니다:

```php
use Illuminate\Support\Str;

$label = Str::of('car')->plural(1000, prependCount: true);

// 1,000 cars
```

<a name="method-fluent-str-position"></a>
#### `position` {.collection-method}

`position` 메서드는 문자열에서 부분 문자열이 처음 나타나는 위치를 반환합니다. 문자열 안에 해당 부분 문자열이 없으면 `false`가 반환됩니다:

```php
use Illuminate\Support\Str;

$position = Str::of('Hello, World!')->position('Hello');

// 0

$position = Str::of('Hello, World!')->position('W');

// 7
```

<a name="method-fluent-str-prepend"></a>
#### `prepend` {.collection-method}

`prepend` 메서드는 주어진 값을 문자열 앞에 붙입니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
#### `remove` {.collection-method}

`remove` 메서드는 문자열에서 주어진 값 또는 값 배열을 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite ');

// Arkansas is beautiful!
```

문자열을 제거할 때 대소문자를 구분하지 않으려면 두 번째 매개변수로 `false`를 전달할 수도 있습니다.

<a name="method-fluent-str-repeat"></a>
#### `repeat` {.collection-method}

`repeat` 메서드는 주어진 문자열을 반복합니다:

```php
use Illuminate\Support\Str;

$repeated = Str::of('a')->repeat(5);

// aaaaa
```

<a name="method-fluent-str-replace"></a>
#### `replace` {.collection-method}

`replace` 메서드는 문자열 안의 주어진 문자열을 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

`replace` 메서드는 `caseSensitive` 인수도 받습니다. 기본적으로 `replace` 메서드는 대소문자를 구분합니다:

```php
$replaced = Str::of('macOS 13.x')->replace(
    'macOS', 'iOS', caseSensitive: false
);
```

<a name="method-fluent-str-replace-array"></a>
#### `replaceArray` {.collection-method}

`replaceArray` 메서드는 배열을 사용하여 문자열 안의 주어진 값을 순서대로 교체합니다:

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
#### `replaceFirst` {.collection-method}

`replaceFirst` 메서드는 문자열에서 주어진 값이 처음 나타나는 항목을 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
#### `replaceLast` {.collection-method}

`replaceLast` 메서드는 문자열에서 주어진 값이 마지막으로 나타나는 항목을 교체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```
<a name="method-fluent-str-replace-matches"></a>
#### `replaceMatches` {.collection-method}

`replaceMatches` 메서드는 패턴과 일치하는 문자열의 모든 부분을 주어진 대체 문자열로 바꿉니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

`replaceMatches` 메서드는 클로저도 받을 수 있습니다. 이 클로저는 주어진 패턴과 일치하는 문자열의 각 부분마다 호출되므로, 클로저 안에서 대체 로직을 수행하고 바뀐 값을 반환할 수 있습니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-replace-start"></a>
#### `replaceStart` {.collection-method}

`replaceStart` 메서드는 주어진 값이 문자열의 시작 부분에 나타나는 경우에만, 해당 값의 첫 번째 항목을 바꿉니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceStart('Hello', 'Laravel');

// Laravel World

$replaced = Str::of('Hello World')->replaceStart('World', 'Laravel');

// Hello World
```

<a name="method-fluent-str-replace-end"></a>
#### `replaceEnd` {.collection-method}

`replaceEnd` 메서드는 주어진 값이 문자열의 끝 부분에 나타나는 경우에만, 해당 값의 마지막 항목을 바꿉니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

// Hello Laravel

$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

// Hello World
```

<a name="method-fluent-str-scan"></a>
#### `scan` {.collection-method}

`scan` 메서드는 [`sscanf` PHP 함수](https://www.php.net/manual/en/function.sscanf.php)가 지원하는 형식에 따라 문자열의 입력을 컬렉션으로 파싱합니다.

```php
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
#### `singular` {.collection-method}

`singular` 메서드는 문자열을 단수형으로 변환합니다. 이 함수는 [Laravel의 복수형 변환기가 지원하는 모든 언어](/docs/13.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$singular = Str::of('cars')->singular();

// car

$singular = Str::of('children')->singular();

// child
```

<a name="method-fluent-str-slug"></a>
#### `slug` {.collection-method}

`slug` 메서드는 주어진 문자열에서 URL에 적합한 "슬러그(slug)"를 생성합니다.

```php
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
#### `snake` {.collection-method}

`snake` 메서드는 주어진 문자열을 `snake_case`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
#### `split` {.collection-method}

`split` 메서드는 정규 표현식을 사용하여 문자열을 컬렉션으로 분리합니다.

```php
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
#### `squish` {.collection-method}

`squish` 메서드는 단어 사이의 불필요한 공백을 포함하여 문자열에서 모든 불필요한 공백을 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
#### `start` {.collection-method}

`start` 메서드는 문자열이 주어진 값으로 시작하지 않는 경우, 해당 값을 문자열 앞에 한 번만 추가합니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->start('/');

// /this/string

$adjusted = Str::of('/this/string')->start('/');

// /this/string
```

<a name="method-fluent-str-starts-with"></a>
#### `startsWith` {.collection-method}

`startsWith` 메서드는 주어진 문자열이 주어진 값으로 시작하는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

값의 배열을 전달하여, 주어진 문자열이 배열에 있는 값 중 하나로 시작하는지 확인할 수도 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith(['This', 'That']);

// true
```

<a name="method-fluent-str-strip-tags"></a>
#### `stripTags` {.collection-method}

`stripTags` 메서드는 문자열에서 모든 HTML 및 PHP 태그를 제거합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags();

// Taylor Otwell

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags('<b>');

// Taylor <b>Otwell</b>
```

<a name="method-fluent-str-studly"></a>
#### `studly` {.collection-method}

`studly` 메서드는 주어진 문자열을 `StudlyCase`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
#### `substr` {.collection-method}

`substr` 메서드는 주어진 시작 위치와 길이 매개변수로 지정한 문자열의 일부를 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Laravel Framework')->substr(8);

// Framework

$string = Str::of('Laravel Framework')->substr(8, 5);

// Frame
```

<a name="method-fluent-str-substrreplace"></a>
#### `substrReplace` {.collection-method}

`substrReplace` 메서드는 두 번째 인수로 지정한 위치부터 시작하여, 세 번째 인수로 지정한 문자 수만큼 문자열의 일부 텍스트를 바꿉니다. 메서드의 세 번째 인수에 `0`을 전달하면 문자열의 기존 문자를 바꾸지 않고 지정한 위치에 문자열을 삽입합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-swap"></a>
#### `swap` {.collection-method}

`swap` 메서드는 PHP의 `strtr` 함수를 사용하여 문자열 안의 여러 값을 바꿉니다.

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
#### `take` {.collection-method}

`take` 메서드는 문자열의 시작 부분에서 지정한 수만큼의 문자를 반환합니다.

```php
use Illuminate\Support\Str;

$taken = Str::of('Build something amazing!')->take(5);

// Build
```

<a name="method-fluent-str-tap"></a>
#### `tap` {.collection-method}

`tap` 메서드는 문자열을 주어진 클로저에 전달하여, 문자열 자체에는 영향을 주지 않으면서 문자열을 살펴보고 다룰 수 있게 합니다. 클로저가 무엇을 반환하든 `tap` 메서드는 원래 문자열을 반환합니다.

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
#### `test` {.collection-method}

`test` 메서드는 문자열이 주어진 정규 표현식 패턴과 일치하는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
#### `title` {.collection-method}

`title` 메서드는 주어진 문자열을 `Title Case`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-to-base64"></a>
#### `toBase64` {.collection-method}

`toBase64` 메서드는 주어진 문자열을 Base64로 변환합니다.

```php
use Illuminate\Support\Str;

$base64 = Str::of('Laravel')->toBase64();

// TGFyYXZlbA==
```

<a name="method-fluent-str-to-html-string"></a>
#### `toHtmlString` {.collection-method}

`toHtmlString` 메서드는 주어진 문자열을 `Illuminate\Support\HtmlString` 인스턴스로 변환합니다. 이 인스턴스는 Blade 템플릿에서 렌더링될 때 이스케이프되지 않습니다.

```php
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-fluent-str-to-uri"></a>
#### `toUri` {.collection-method}

`toUri` 메서드는 주어진 문자열을 [Illuminate\Support\Uri](/docs/13.x/helpers#uri) 인스턴스로 변환합니다.

```php
use Illuminate\Support\Str;

$uri = Str::of('https://example.com')->toUri();
```

<a name="method-fluent-str-transliterate"></a>
#### `transliterate` {.collection-method}

`transliterate` 메서드는 주어진 문자열을 가장 가까운 ASCII 표현으로 변환하려고 시도합니다.

```php
use Illuminate\Support\Str;

$email = Str::of('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ')->transliterate()

// 'test@laravel.com'
```

<a name="method-fluent-str-trim"></a>
#### `trim` {.collection-method}

`trim` 메서드는 주어진 문자열의 양끝을 잘라냅니다. PHP의 기본 `trim` 함수와 달리, Laravel의 `trim` 메서드는 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ltrim"></a>
#### `ltrim` {.collection-method}

`ltrim` 메서드는 문자열의 왼쪽 부분을 잘라냅니다. PHP의 기본 `ltrim` 함수와 달리, Laravel의 `ltrim` 메서드는 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```
<a name="method-fluent-str-rtrim"></a>
#### `rtrim` {.collection-method}

`rtrim` 메서드는 주어진 문자열의 오른쪽을 잘라냅니다. PHP의 기본 `rtrim` 함수와 달리, Laravel의 `rtrim` 메서드는 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
#### `ucfirst` {.collection-method}

`ucfirst` 메서드는 주어진 문자열에서 첫 번째 문자를 대문자로 바꾸어 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
#### `ucsplit` {.collection-method}

`ucsplit` 메서드는 주어진 문자열을 대문자 기준으로 나누어 컬렉션으로 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo ', 'Bar'])
```

<a name="method-fluent-str-ucwords"></a>
#### `ucwords` {.collection-method}

`ucwords` 메서드는 주어진 문자열에서 각 단어의 첫 번째 문자를 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('laravel framework')->ucwords();

// Laravel Framework
```

<a name="method-fluent-str-unwrap"></a>
#### `unwrap` {.collection-method}

`unwrap` 메서드는 주어진 문자열의 시작과 끝에서 지정된 문자열을 제거합니다.

```php
use Illuminate\Support\Str;

Str::of('-Laravel-')->unwrap('-');

// Laravel

Str::of('{framework: "Laravel"}')->unwrap('{', '}');

// framework: "Laravel"
```

<a name="method-fluent-str-upper"></a>
#### `upper` {.collection-method}

`upper` 메서드는 주어진 문자열을 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
#### `when` {.collection-method}

`when` 메서드는 주어진 조건이 `true`이면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Taylor')
    ->when(true, function (Stringable $string) {
        return $string->append(' Otwell');
    });

// 'Taylor Otwell'
```

필요하다면 `when` 메서드의 세 번째 매개변수로 다른 클로저를 전달할 수 있습니다. 이 클로저는 조건 매개변수가 `false`로 평가될 때 실행됩니다.

<a name="method-fluent-str-when-contains"></a>
#### `whenContains` {.collection-method}

`whenContains` 메서드는 문자열에 주어진 값이 포함되어 있으면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains('tony', function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

필요하다면 세 번째 매개변수로 다른 클로저를 전달할 수 있습니다. 이 클로저는 문자열에 주어진 값이 포함되어 있지 않을 때 호출됩니다.

주어진 문자열에 배열의 값 중 하나라도 포함되어 있는지 확인하려면 값의 배열을 전달할 수도 있습니다.

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
#### `whenContainsAll` {.collection-method}

`whenContainsAll` 메서드는 문자열에 주어진 모든 부분 문자열이 포함되어 있으면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContainsAll(['tony', 'stark'], function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

필요하다면 세 번째 매개변수로 다른 클로저를 전달할 수 있습니다. 이 클로저는 조건 매개변수가 `false`로 평가될 때 호출됩니다.

<a name="method-fluent-str-when-doesnt-end-with"></a>
#### `whenDoesntEndWith` {.collection-method}

`whenDoesntEndWith` 메서드는 문자열이 주어진 부분 문자열로 끝나지 않으면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenDoesntEndWith('land', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-doesnt-start-with"></a>
#### `whenDoesntStartWith` {.collection-method}

`whenDoesntStartWith` 메서드는 문자열이 주어진 부분 문자열로 시작하지 않으면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenDoesntStartWith('sea', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-empty"></a>
#### `whenEmpty` {.collection-method}

`whenEmpty` 메서드는 문자열이 비어 있으면 지정된 클로저를 호출합니다. 클로저가 값을 반환하면, 그 값이 `whenEmpty` 메서드에서도 반환됩니다. 클로저가 값을 반환하지 않으면 fluent string 인스턴스가 반환됩니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('  ')->trim()->whenEmpty(function (Stringable $string) {
    return $string->prepend('Laravel');
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-empty"></a>
#### `whenNotEmpty` {.collection-method}

`whenNotEmpty` 메서드는 문자열이 비어 있지 않으면 지정된 클로저를 호출합니다. 클로저가 값을 반환하면, 그 값이 `whenNotEmpty` 메서드에서도 반환됩니다. 클로저가 값을 반환하지 않으면 fluent string 인스턴스가 반환됩니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Framework')->whenNotEmpty(function (Stringable $string) {
    return $string->prepend('Laravel ');
});

// 'Laravel Framework'
```

<a name="method-fluent-str-when-starts-with"></a>
#### `whenStartsWith` {.collection-method}

`whenStartsWith` 메서드는 문자열이 주어진 부분 문자열로 시작하면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenStartsWith('disney', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-ends-with"></a>
#### `whenEndsWith` {.collection-method}

`whenEndsWith` 메서드는 문자열이 주어진 부분 문자열로 끝나면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenEndsWith('world', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-exactly"></a>
#### `whenExactly` {.collection-method}

`whenExactly` 메서드는 문자열이 주어진 문자열과 정확히 일치하면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-exactly"></a>
#### `whenNotExactly` {.collection-method}

`whenNotExactly` 메서드는 문자열이 주어진 문자열과 정확히 일치하지 않으면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('framework')->whenNotExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Framework'
```

<a name="method-fluent-str-when-is"></a>
#### `whenIs` {.collection-method}

`whenIs` 메서드는 문자열이 주어진 패턴과 일치하면 지정된 클로저를 호출합니다. 별표는 와일드카드 값으로 사용할 수 있습니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('foo/bar')->whenIs('foo/*', function (Stringable $string) {
    return $string->append('/baz');
});

// 'foo/bar/baz'
```

<a name="method-fluent-str-when-is-ascii"></a>
#### `whenIsAscii` {.collection-method}

`whenIsAscii` 메서드는 문자열이 7비트 ASCII이면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenIsAscii(function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is-ulid"></a>
#### `whenIsUlid` {.collection-method}

`whenIsUlid` 메서드는 문자열이 유효한 ULID이면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
#### `whenIsUuid` {.collection-method}

`whenIsUuid` 메서드는 문자열이 유효한 UUID이면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// 'a0a2a2d2'
```

<a name="method-fluent-str-when-test"></a>
#### `whenTest` {.collection-method}

`whenTest` 메서드는 문자열이 주어진 정규 표현식과 일치하면 지정된 클로저를 호출합니다. 클로저는 fluent string 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel framework')->whenTest('/laravel/', function (Stringable $string) {
    return $string->title();
});

// 'Laravel Framework'
```

<a name="method-fluent-str-word-count"></a>
#### `wordCount` {.collection-method}

`wordCount` 메서드는 문자열에 포함된 단어 수를 반환합니다.

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
#### `words` {.collection-method}

`words` 메서드는 문자열의 단어 수를 제한합니다. 필요하다면 잘린 문자열 뒤에 추가할 문자열을 지정할 수 있습니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-fluent-str-wrap"></a>
#### `wrap` {.collection-method}

`wrap` 메서드는 주어진 문자열을 추가 문자열 하나 또는 한 쌍의 문자열로 감쌉니다.

```php
use Illuminate\Support\Str;

Str::of('Laravel')->wrap('"');

// "Laravel"

Str::is('is')->wrap(before: 'This ', after: ' Laravel!');

// This is Laravel!
```
