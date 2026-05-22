# 文字列 (Strings)

- [Introduction](#introduction)
- [利用可能な方法](#available-methods)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel には、文字列値を操作するためのさまざまな関数が含まれています。これらの関数の多くはフレームワーク自体によって使用されます。ただし、便利だと思われる場合は、独自のアプリケーションで自由に使用できます。

<a name="available-methods"></a>
## 利用可能な方法 (Available Methods)

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
### 文字列

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
### 流暢な文字列

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
## 文字列 (Strings)

<a name="method-__"></a>
#### `__()` {.collection-method}

`__` 関数は、[言語ファイル](/docs/{{version}}/localization) を使用して、指定された翻訳文字列または翻訳キーを翻訳します。

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

指定された変換文字列またはキーが存在しない場合、`__` 関数は指定された値を返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`__` 関数は `messages.welcome` を返します。

<a name="method-class-basename"></a>
#### `class_basename()` {.collection-method}

`class_basename` 関数は、クラスの名前空間が削除された、指定されたクラスのクラス名を返します。

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()` {.collection-method}

`e` 関数は、デフォルトで `double_encode` オプションを `true` に設定して、PHP の `htmlspecialchars` 関数を実行します。

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()` {.collection-method}

`preg_replace_array` 関数は、配列を使用して文字列内の指定されたパターンを順番に置き換えます。

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()` {.collection-method}

`Str::after` メソッドは、文字列内の指定された値以降のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()` {.collection-method}

`Str::afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
#### `Str::apa()` {.collection-method}

`Str::apa` メソッドは、指定された文字列を [APAガイドライン](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case) に従ってタイトルケースに変換します。

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()` {.collection-method}

`Str::ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()` {.collection-method}

`Str::before` メソッドは、文字列内の指定された値より前のすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()` {.collection-method}

`Str::beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
#### `Str::between()` {.collection-method}

`Str::between` メソッドは、2 つの値の間の文字列の部分を返します。

```php
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()` {.collection-method}

`Str::betweenFirst` メソッドは、2 つの値の間の文字列の可能な最小部分を返します。

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()` {.collection-method}

`Str::camel` メソッドは、指定された文字列を `camelCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
#### `Str::charAt()` {.collection-method}

`Str::charAt` メソッドは、指定されたインデックスの文字を返します。インデックスが範囲外の場合、`false` が返されます。

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
#### `Str::chopStart()` {.collection-method}

`Str::chopStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

2 番目の引数として配列を渡すこともできます。文字列が配列内のいずれかの値で始まる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()` {.collection-method}

`Str::chopEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

2 番目の引数として配列を渡すこともできます。文字列が配列内のいずれかの値で終わる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
#### `Str::contains()` {.collection-method}

`Str::contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()` {.collection-method}

`Str::containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()` {.collection-method}

`Str::doesntContain` メソッドは、指定された文字列に指定された値が含まれていないかどうかを判断します。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

値の配列を渡して、指定された文字列に配列内の値が含まれていないかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'framework']);

// true
```

`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
#### `Str::deduplicate()` {.collection-method}

`Str::deduplicate` メソッドは、指定された文字列内の文字の連続したインスタンスをその文字の単一のインスタンスに置き換えます。デフォルトでは、このメソッドはスペースを重複排除します。

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

重複排除する別の文字を指定するには、それをメソッドの 2 番目の引数として渡します。

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-str-doesnt-end-with"></a>
#### `Str::doesntEndWith()` {.collection-method}

`Str::doesntEndWith` メソッドは、指定された文字列が指定された値で終わっていないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', 'dog');

// true
```

値の配列を渡して、指定された文字列が配列内のどの値でも終わっていないかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', ['this', 'foo']);

// true

$result = Str::doesntEndWith('This is my name', ['name', 'foo']);

// false
```

<a name="method-str-doesnt-start-with"></a>
#### `Str::doesntStartWith()` {.collection-method}

`Str::doesntStartWith` メソッドは、指定された文字列が指定された値で始まらないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::doesntStartWith('This is my name', 'That');

// true
```

可能な値の配列が渡された場合、文字列が指定された値のいずれでも始まらない場合、`doesntStartWith` メソッドは `true` を返します。

```php
$result = Str::doesntStartWith('This is my name', ['What', 'That', 'There']);

// true
```

<a name="method-ends-with"></a>
#### `Str::endsWith()` {.collection-method}

`Str::endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()` {.collection-method}

`Str::excerpt` メソッドは、指定された文字列から、その文字列内のフレーズの最初のインスタンスに一致する抜粋を抽出します。

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` オプション (デフォルトは `100`) を使用すると、切り詰められた文字列の両側に表示される文字数を定義できます。

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
#### `Str::finish()` {.collection-method}

`Str::finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-from-base64"></a>
#### `Str::fromBase64()` {.collection-method}

`Str::fromBase64` メソッドは、指定された Base64 文字列をデコードします。

```php
use Illuminate\Support\Str;

$decoded = Str::fromBase64('TGFyYXZlbA==');

// Laravel
```

<a name="method-str-headline"></a>
#### `Str::headline()` {.collection-method}

`Str::headline` メソッドは、大文字と小文字、ハイフン、またはアンダースコアで区切られた文字列を、各単語の最初の文字が大文字になったスペースで区切られた文字列に変換します。

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-initials"></a>
#### `Str::initials()` {.collection-method}

`Str::initials` メソッドは、指定された文字列のイニシャルを返します。オプションで大文字にすることもできます。

```php
use Illuminate\Support\Str;

$initials = Str::initials('taylor otwell');

// to

$initials = Str::initials('taylor otwell', capitalize: true);

// TO
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()` {.collection-method}

`Str::inlineMarkdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown をインライン HTML に変換します。ただし、`markdown` メソッドとは異なり、生成されたすべての HTML をブロックレベル要素でラップするわけではありません。

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

#### マークダウンセキュリティ

デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark セキュリティのドキュメント](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

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

`Str::is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます。

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()` {.collection-method}

`Str::isAscii` メソッドは、指定された文字列が 7 ビット ASCII であるかどうかを判断します。

```php
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()` {.collection-method}

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
#### `Str::isUrl()` {.collection-method}

`Str::isUrl` メソッドは、指定された文字列が有効な URL かどうかを判断します。

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

`isUrl` メソッドは、幅広いプロトコルを有効であるとみなします。ただし、`isUrl` メソッドにプロトコルを指定することで、有効であるとみなされるプロトコルを指定できます。

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()` {.collection-method}

`Str::isUlid` メソッドは、指定された文字列が有効な ULID かどうかを判断します。

```php
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()` {.collection-method}

`Str::isUuid` メソッドは、指定された文字列が有効な UUID かどうかを判断します。

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

指定された UUID がバージョン (1、3、4、5、6、7、または 8) ごとの UUID 仕様と一致することを検証することもできます。

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 4);

// true

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 1);

// false
```

<a name="method-kebab-case"></a>
#### `Str::kebab()` {.collection-method}

`Str::kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()` {.collection-method}

`Str::lcfirst` メソッドは、最初の文字を小文字にして指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()` {.collection-method}

`Str::length` メソッドは、指定された文字列の長さを返します。

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()` {.collection-method}

`Str::limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

メソッドに 3 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更できます。

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

文字列を切り詰めるときに完全な単語を保持したい場合は、`preserveWords` 引数を利用できます。この引数が `true` の場合、文字列は最も近い完全な単語境界まで切り詰められます。

```php
$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

// The quick...
```

<a name="method-str-lower"></a>
#### `Str::lower()` {.collection-method}

`Str::lower` メソッドは、指定された文字列を小文字に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
#### `Str::markdown()` {.collection-method}

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

#### マークダウンセキュリティ

デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark セキュリティのドキュメント](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

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

`Str::mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

必要に応じて、`mask` メソッドの 3 番目の引数として負の数値を指定します。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-match"></a>
#### `Str::match()` {.collection-method}

`Str::match` メソッドは、指定された正規表現パターンに一致する文字列の部分を返します。

```php
use Illuminate\Support\Str;

$result = Str::match('/bar/', 'foo bar');

// 'bar'

$result = Str::match('/foo (.*)/', 'foo bar');

// 'bar'
```

<a name="method-str-match-all"></a>
#### `Str::matchAll()` {.collection-method}

`Str::matchAll` メソッドは、指定された正規表現パターンに一致する文字列の部分を含むコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/bar/', 'bar foo bar');

// collect(['bar', 'bar'])
```

式内で一致するグループを指定すると、Laravel は最初に一致したグループの一致のコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

// collect(['un', 'ly']);
```

一致するものが見つからない場合は、空のコレクションが返されます。

<a name="method-str-is-match"></a>
#### `Str::isMatch()` {.collection-method}

文字列が指定された正規表現に一致する場合、`Str::isMatch` メソッドは `true` を返します。

```php
use Illuminate\Support\Str;

$result = Str::isMatch('/foo (.*)/', 'foo bar');

// true

$result = Str::isMatch('/foo (.*)/', 'laravel');

// false
```

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()` {.collection-method}

`Str::orderedUuid` メソッドは、インデックス付きデータベース列に効率的に格納できる「タイムスタンプ優先」の UUID を生成します。このメソッドを使用して生成された各 UUID は、以前に次のメソッドを使用して生成された UUID の後にソートされます。

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()` {.collection-method}

`Str::padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

```php
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()` {.collection-method}

`Str::padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

```php
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()` {.collection-method}

`Str::padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
#### `Str::password()` {.collection-method}

`Str::password` メソッドを使用すると、指定された長さの安全なランダムなパスワードを生成できます。パスワードは文字、数字、記号、スペースの組み合わせで構成されます。デフォルトでは、パスワードの長さは 32 文字です。

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
#### `Str::plural()` {.collection-method}

`Str::plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

`prependCount` 引数を指定すると、書式設定された `$count` を複数化された文字列の前に付けることができます。

```php
use Illuminate\Support\Str;

$label = Str::plural('car', 1000, prependCount: true);

// 1,000 cars
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()` {.collection-method}

`Str::pluralStudly` メソッドは、大文字小文字でフォーマットされた単数形の単語文字列を複数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>
#### `Str::position()` {.collection-method}

`Str::position` メソッドは、文字列内で最初に出現する部分文字列の位置を返します。指定された文字列に部分文字列が存在しない場合は、`false` が返されます。

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
#### `Str::random()` {.collection-method}

`Str::random` メソッドは、指定された長さのランダムな文字列を生成します。この関数は、PHP の `random_bytes` 関数を使用します。

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

テスト中に、`Str::random` メソッドによって返される値を「偽装」すると便利な場合があります。これを実現するには、`createRandomStringsUsing` メソッドを使用できます。

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

`random` メソッドに通常のランダム文字列の生成に戻るように指示するには、`createRandomStringsNormally` メソッドを呼び出します。

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
#### `Str::remove()` {.collection-method}

`Str::remove` メソッドは、指定された値または値の配列を文字列から削除します。

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

文字列を削除するときに大文字と小文字を区別しないように、`false` を `remove` メソッドの 3 番目の引数として渡すこともできます。

<a name="method-str-repeat"></a>
#### `Str::repeat()` {.collection-method}

`Str::repeat` メソッドは、指定された文字列を繰り返します。

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()` {.collection-method}

`Str::replace` メソッドは、文字列内の指定された文字列を置き換えます。

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

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
#### `Str::replaceArray()` {.collection-method}

`Str::replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()` {.collection-method}

`Str::replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()` {.collection-method}

`Str::replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()` {.collection-method}

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

`replaceMatches` メソッドは、指定されたパターンに一致する文字列の各部分で呼び出されるクロージャも受け入れます。これにより、クロージャ内で置換ロジックを実行し、置換された値を返すことができます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()` {.collection-method}

`Str::replaceStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()` {.collection-method}

`Str::replaceEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

// Hello Laravel

$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-reverse"></a>
#### `Str::reverse()` {.collection-method}

`Str::reverse` メソッドは、指定された文字列を反転します。

```php
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
#### `Str::singular()` {.collection-method}

`Str::singular` メソッドは、文字列を単数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()` {.collection-method}

`Str::slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()` {.collection-method}

`Str::snake` メソッドは、指定された文字列を `snake_case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()` {.collection-method}

`Str::squish` メソッドは、単語間の無関係な空白を含め、文字列から無関係な空白をすべて削除します。

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()` {.collection-method}

`Str::start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

```php
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()` {.collection-method}

`Str::startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

可能な値の配列が渡された場合、文字列が指定された値のいずれかで始まる場合、`startsWith` メソッドは `true` を返します。

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()` {.collection-method}

`Str::studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()` {.collection-method}

`Str::substr` メソッドは、start パラメーターと length パラメーターで指定された文字列の部分を返します。

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()` {.collection-method}

`Str::substrCount` メソッドは、指定された文字列内の指定された値の出現数を返します。

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()` {.collection-method}

`Str::substrReplace` メソッドは、文字列の一部内のテキストを、3 番目の引数で指定された位置から開始して 4 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 4 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

```php
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()` {.collection-method}

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
#### `Str::take()` {.collection-method}

`Str::take` メソッドは、文字列の先頭から指定された数の文字を返します。

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
#### `Str::title()` {.collection-method}

`Str::title` メソッドは、指定された文字列を `Title Case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
#### `Str::toBase64()` {.collection-method}

`Str::toBase64` メソッドは、指定された文字列を Base64 に変換します。

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
#### `Str::transliterate()` {.collection-method}

`Str::transliterate` メソッドは、指定された文字列を最も近い ASCII 表現に変換しようとします。

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
#### `Str::trim()` {.collection-method}

`Str::trim` メソッドは、指定された文字列の先頭と末尾から空白 (または他の文字) を削除します。 PHP のネイティブ `trim` 関数とは異なり、`Str::trim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
#### `Str::ltrim()` {.collection-method}

`Str::ltrim` メソッドは、指定された文字列の先頭から空白 (または他の文字) を削除します。 PHP のネイティブ `ltrim` 関数とは異なり、`Str::ltrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
#### `Str::rtrim()` {.collection-method}

`Str::rtrim` メソッドは、指定された文字列の末尾から空白 (または他の文字) を削除します。 PHP のネイティブ `rtrim` 関数とは異なり、`Str::rtrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()` {.collection-method}

`Str::ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()` {.collection-method}

`Str::ucsplit` メソッドは、指定された文字列を大文字ごとに配列に分割します。

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-ucwords"></a>
#### `Str::ucwords()` {.collection-method}

`Str::ucwords` メソッドは、指定された文字列内の各単語の最初の文字を大文字に変換します。

```php
use Illuminate\Support\Str;

$string = Str::ucwords('laravel framework');

// Laravel Framework
```

<a name="method-str-upper"></a>
#### `Str::upper()` {.collection-method}

`Str::upper` メソッドは、指定された文字列を大文字に変換します。

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()` {.collection-method}

`Str::ulid` メソッドは、コンパクトな時間順の一意の識別子である ULID を生成します。

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

特定の ULID が作成された日時を表す `Illuminate\Support\Carbon` 日付インスタンスを取得したい場合は、Laravel の Carbon 統合によって提供される `createFromId` メソッドを使用できます。

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

テスト中に、`Str::ulid` メソッドによって返される値を「偽装」すると便利な場合があります。これを実現するには、`createUlidsUsing` メソッドを使用できます。

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

`ulid` メソッドに通常の ULID の生成に戻るように指示するには、`createUlidsNormally` メソッドを呼び出します。

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
#### `Str::unwrap()` {.collection-method}

`Str::unwrap` メソッドは、指定された文字列の先頭と末尾から指定された文字列を削除します。

```php
use Illuminate\Support\Str;

Str::unwrap('-Laravel-', '-');

// Laravel

Str::unwrap('{framework: "Laravel"}', '{', '}');

// framework: "Laravel"
```

<a name="method-str-uuid"></a>
#### `Str::uuid()` {.collection-method}

`Str::uuid` メソッドは UUID (バージョン 4) を生成します。

```php
use Illuminate\Support\Str;

return (string) Str::uuid();
```

テスト中に、`Str::uuid` メソッドによって返される値を「偽装」すると便利な場合があります。これを実現するには、`createUuidsUsing` メソッドを使用できます。

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

`uuid` メソッドに通常の UUID 生成に戻るように指示するには、`createUuidsNormally` メソッドを呼び出します。

```php
Str::createUuidsNormally();
```

<a name="method-str-uuid7"></a>
#### `Str::uuid7()` {.collection-method}

`Str::uuid7` メソッドは UUID (バージョン 7) を生成します。

```php
use Illuminate\Support\Str;

return (string) Str::uuid7();
```

`DateTimeInterface` は、順序付けされた UUID の生成に使用されるオプションのパラメーターとして渡すことができます。

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()` {.collection-method}

`Str::wordCount` メソッドは、文字列に含まれる単語の数を返します。

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()` {.collection-method}

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
#### `Str::words()` {.collection-method}

`Str::words` メソッドは、文字列内の単語数を制限します。追加の文字列を 3 番目の引数を介してこのメ​​ソッドに渡し、切り詰められた文字列の末尾に追加する文字列を指定できます。

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
#### `Str::wrap()` {.collection-method}

`Str::wrap` メソッドは、指定された文字列を追加の文字列または文字列のペアでラップします。

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
#### `str()` {.collection-method}

`str` 関数は、指定された文字列の新しい `Illuminate\Support\Stringable` インスタンスを返します。この関数は、`Str::of` メソッドと同等です。

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

`str` 関数に引数が指定されていない場合、関数は `Illuminate\Support\Str` のインスタンスを返します。

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()` {.collection-method}

`trans` 関数は、[言語ファイル](/docs/{{version}}/localization) を使用して、指定された変換キーを変換します。

```php
echo trans('messages.welcome');
```

指定された変換キーが存在しない場合、`trans` 関数は指定されたキーを返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`trans` 関数は `messages.welcome` を返します。

<a name="method-trans-choice"></a>
#### `trans_choice()` {.collection-method}

`trans_choice` 関数は、指定された変換キーを語形変化を使用して変換します。

```php
echo trans_choice('messages.notifications', $unreadCount);
```

指定された変換キーが存在しない場合、`trans_choice` 関数は指定されたキーを返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`trans_choice` 関数は `messages.notifications` を返します。

<a name="fluent-strings"></a>
## 流暢な文字列 (Fluent Strings)

Fluent String は、文字列値を操作するためのより流暢なオブジェクト指向インターフェイスを提供し、従来の文字列操作と比較して読みやすい構文を使用して複数の文字列操作を連鎖させることができます。

<a name="method-fluent-str-after"></a>
#### `after` {.collection-method}

`after` メソッドは、文字列内の指定された値以降のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
#### `afterLast` {.collection-method}

`afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```php
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-apa"></a>
#### `apa` {.collection-method}

`apa` メソッドは、指定された文字列を [APAガイドライン](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case) に従ってタイトルケースに変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->apa();

// A Nice Title Uses the Correct Case
```

<a name="method-fluent-str-append"></a>
#### `append` {.collection-method}

`append` メソッドは、指定された値を文字列に追加します。

```php
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
#### `ascii` {.collection-method}

`ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

```php
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
#### `basename` {.collection-method}

`basename` メソッドは、指定された文字列の末尾の名前コンポーネントを返します。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

必要に応じて、後続コンポーネントから削除される「拡張機能」を指定できます。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
#### `before` {.collection-method}

`before` メソッドは、文字列内の指定された値より前のすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
#### `beforeLast` {.collection-method}

`beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
#### `between` {.collection-method}

`between` メソッドは、2 つの値の間の文字列の部分を返します。

```php
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
#### `betweenFirst` {.collection-method}

`betweenFirst` メソッドは、2 つの値の間の文字列の可能な最小部分を返します。

```php
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
#### `camel` {.collection-method}

`camel` メソッドは、指定された文字列を `camelCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// 'fooBar'
```

<a name="method-fluent-str-char-at"></a>
#### `charAt` {.collection-method}

`charAt` メソッドは、指定されたインデックスの文字を返します。インデックスが範囲外の場合、`false` が返されます。

```php
use Illuminate\Support\Str;

$character = Str::of('This is my name.')->charAt(6);

// 's'
```

<a name="method-fluent-str-class-basename"></a>
#### `classBasename` {.collection-method}

`classBasename` メソッドは、クラスの名前空間が削除された、指定されたクラスのクラス名を返します。

```php
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// 'Baz'
```

<a name="method-fluent-str-chop-start"></a>
#### `chopStart` {.collection-method}

`chopStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopStart('https://');

// 'laravel.com'
```

配列を渡すこともできます。文字列が配列内のいずれかの値で始まる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopStart(['https://', 'http://']);

// 'laravel.com'
```

<a name="method-fluent-str-chop-end"></a>
#### `chopEnd` {.collection-method}

`chopEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を削除します。

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopEnd('.com');

// 'https://laravel'
```

配列を渡すこともできます。文字列が配列内のいずれかの値で終わる場合、その値は文字列から削除されます。

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopEnd(['.com', '.io']);

// 'http://laravel'
```

<a name="method-fluent-str-contains"></a>
#### `contains` {.collection-method}

`contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

大文字と小文字の区別を無効にするには、`ignoreCase` 引数を `true` に設定します。

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('MY', ignoreCase: true);

// true
```

<a name="method-fluent-str-contains-all"></a>
#### `containsAll` {.collection-method}

`containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

大文字と小文字の区別を無効にするには、`ignoreCase` 引数を `true` に設定します。

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-fluent-str-decrypt"></a>
#### `decrypt` {.collection-method}

`decrypt` メソッド [decrypts](/docs/{{version}}/encryption) 暗号化された文字列:

```php
use Illuminate\Support\Str;

$decrypted = $encrypted->decrypt();

// 'secret'
```

`decrypt` の逆については、[encrypt](#method-fluent-str-encrypt) メソッドを参照してください。

<a name="method-fluent-str-deduplicate"></a>
#### `deduplicate` {.collection-method}

`deduplicate` メソッドは、指定された文字列内の文字の連続したインスタンスをその文字の単一のインスタンスに置き換えます。デフォルトでは、このメソッドはスペースを重複排除します。

```php
use Illuminate\Support\Str;

$result = Str::of('The   Laravel   Framework')->deduplicate();

// The Laravel Framework
```

重複排除する別の文字を指定するには、それをメソッドの 2 番目の引数として渡します。

```php
use Illuminate\Support\Str;

$result = Str::of('The---Laravel---Framework')->deduplicate('-');

// The-Laravel-Framework
```

<a name="method-fluent-str-dirname"></a>
#### `dirname` {.collection-method}

`dirname` メソッドは、指定された文字列の親ディレクトリ部分を返します。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

必要に応じて、文字列から削除するディレクトリ レベルの数を指定できます。

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-doesnt-contain"></a>
#### `doesntContain()` {.collection-method}

`doesntContain` メソッドは、指定された文字列に指定された値が含まれていないかどうかを判断します。このメソッドは、[contains](#method-fluent-str-contains) メソッドの逆です。デフォルトでは、このメソッドは大文字と小文字が区別されます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain('my');

// true
```

値の配列を渡して、指定された文字列に配列内の値が含まれていないかどうかを確認することもできます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain(['my', 'framework']);

// true
```

`ignoreCase` 引数を `true` に設定することで、大文字と小文字の区別を無効にすることができます。

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is my name')->doesntContain('MY', ignoreCase: true);

// false
```

<a name="method-fluent-str-doesnt-end-with"></a>
#### `doesntEndWith` {.collection-method}

`doesntEndWith` メソッドは、指定された文字列が指定された値で終わっていないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith('dog');

// true
```

値の配列を渡して、指定された文字列が配列内のどの値でも終わっていないかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith(['this', 'foo']);

// true

$result = Str::of('This is my name')->doesntEndWith(['name', 'foo']);

// false
```

<a name="method-fluent-str-doesnt-start-with"></a>
#### `doesntStartWith` {.collection-method}

`doesntStartWith` メソッドは、指定された文字列が指定された値で始まらないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith('That');

// true
```

値の配列を渡して、指定された文字列が配列内のどの値でも始まらないかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith(['What', 'That', 'There']);

// true
```

<a name="method-fluent-str-encrypt"></a>
#### `encrypt` {.collection-method}

`encrypt` メソッド [encrypts](/docs/{{version}}/encryption) 文字列:

```php
use Illuminate\Support\Str;

$encrypted = Str::of('secret')->encrypt();
```

`encrypt` の逆については、[decrypt](#method-fluent-str-decrypt) メソッドを参照してください。

<a name="method-fluent-str-ends-with"></a>
#### `endsWith` {.collection-method}

`endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith(['name', 'foo']);

// true

$result = Str::of('This is my name')->endsWith(['this', 'foo']);

// false
```

<a name="method-fluent-str-exactly"></a>
#### `exactly` {.collection-method}

`exactly` メソッドは、指定された文字列が別の文字列と完全に一致するかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-excerpt"></a>
#### `excerpt` {.collection-method}

`excerpt` メソッドは、文字列内のフレーズの最初のインスタンスに一致する文字列からの抜粋を抽出します。

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` オプション (デフォルトは `100`) を使用すると、切り詰められた文字列の両側に表示される文字数を定義できます。

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
#### `explode` {.collection-method}

`explode` メソッドは、指定された区切り文字で文字列を分割し、分割された文字列の各セクションを含むコレクションを返します。

```php
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
#### `finish` {.collection-method}

`finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-from-base64"></a>
#### `fromBase64` {.collection-method}

`fromBase64` メソッドは、指定された Base64 文字列をデコードします。

```php
use Illuminate\Support\Str;

$decoded = Str::of('TGFyYXZlbA==')->fromBase64();

// Laravel
```

<a name="method-fluent-str-hash"></a>
#### `hash` {.collection-method}

`hash` メソッドは、指定された [algorithm](https://www.php.net/manual/en/function.hash-algos.php) を使用して文字列をハッシュします。

```php
use Illuminate\Support\Str;

$hashed = Str::of('secret')->hash(algorithm: 'sha256');

// '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
```

<a name="method-fluent-str-headline"></a>
#### `headline` {.collection-method}

`headline` メソッドは、大文字と小文字、ハイフン、またはアンダースコアで区切られた文字列を、各単語の最初の文字が大文字になったスペースで区切られた文字列に変換します。

```php
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-initials"></a>
#### `initials` {.collection-method}

`initials` メソッドは文字列をそのイニシャルに変換します。

```php
use Illuminate\Support\Str;

$initials = Str::of('Taylor Otwell')->initials()->upper();

// TO
```

<a name="method-fluent-str-inline-markdown"></a>
#### `inlineMarkdown` {.collection-method}

`inlineMarkdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown をインライン HTML に変換します。ただし、`markdown` メソッドとは異なり、生成されたすべての HTML をブロックレベル要素でラップするわけではありません。

```php
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

#### マークダウンセキュリティ

デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark セキュリティのドキュメント](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

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

`is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます

```php
use Illuminate\Support\Str;

$matches = Str::of('foobar')->is('foo*');

// true

$matches = Str::of('foobar')->is('baz*');

// false
```

<a name="method-fluent-str-is-ascii"></a>
#### `isAscii` {.collection-method}

`isAscii` メソッドは、指定された文字列が ASCII 文字列であるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('Taylor')->isAscii();

// true

$result = Str::of('ü')->isAscii();

// false
```

<a name="method-fluent-str-is-empty"></a>
#### `isEmpty` {.collection-method}

`isEmpty` メソッドは、指定された文字列が空かどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isEmpty();

// true

$result = Str::of('Laravel')->trim()->isEmpty();

// false
```

<a name="method-fluent-str-is-not-empty"></a>
#### `isNotEmpty` {.collection-method}

`isNotEmpty` メソッドは、指定された文字列が空でないかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-json"></a>
#### `isJson` {.collection-method}

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
#### `isUlid` {.collection-method}

`isUlid` メソッドは、指定された文字列が ULID であるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-url"></a>
#### `isUrl` {.collection-method}

`isUrl` メソッドは、指定された文字列が URL かどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('http://example.com')->isUrl();

// true

$result = Str::of('Taylor')->isUrl();

// false
```

`isUrl` メソッドは、幅広いプロトコルを有効であるとみなします。ただし、`isUrl` メソッドにプロトコルを指定することで、有効であるとみなされるプロトコルを指定できます。

```php
$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

<a name="method-fluent-str-is-uuid"></a>
#### `isUuid` {.collection-method}

`isUuid` メソッドは、指定された文字列が UUID かどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

指定された UUID がバージョン (1、3、4、5、6、7、または 8) ごとの UUID 仕様と一致することを検証することもできます。

```php
use Illuminate\Support\Str;

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 4);

// true

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 1);

// false
```

<a name="method-fluent-str-kebab"></a>
#### `kebab` {.collection-method}

`kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
#### `lcfirst` {.collection-method}

`lcfirst` メソッドは、最初の文字を小文字にして指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```

<a name="method-fluent-str-length"></a>
#### `length` {.collection-method}

`length` メソッドは、指定された文字列の長さを返します。

```php
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
#### `limit` {.collection-method}

`limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

```php
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

2 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更することもできます。

```php
$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

文字列を切り詰めるときに完全な単語を保持したい場合は、`preserveWords` 引数を利用できます。この引数が `true` の場合、文字列は最も近い完全な単語境界まで切り詰められます。

```php
$truncated = Str::of('The quick brown fox')->limit(12, preserveWords: true);

// The quick...
```

<a name="method-fluent-str-lower"></a>
#### `lower` {.collection-method}

`lower` メソッドは、指定された文字列を小文字に変換します。

```php
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-markdown"></a>
#### `markdown` {.collection-method}

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

#### マークダウンセキュリティ

デフォルトでは、Markdown は生の HTML をサポートしているため、生のユーザー入力で使用するとクロスサイト スクリプティング (XSS) の脆弱性が露呈します。 [CommonMark セキュリティのドキュメント](https://commonmark.thephpleague.com/security/) に従って、`html_input` オプションを使用して生の HTML をエスケープまたは削除し、`allow_unsafe_links` オプションを使用して安全でないリンクを許可するかどうかを指定できます。生の HTML を許可する必要がある場合は、コンパイルされた Markdown を HTML Purifier に渡す必要があります。

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

`mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

```php
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

必要に応じて、`mask` メソッドの 3 番目または 4 番目の引数として負の数値を指定できます。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

```php
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
#### `match` {.collection-method}

`match` メソッドは、指定された正規表現パターンに一致する文字列の部分を返します。

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->match('/bar/');

// 'bar'

$result = Str::of('foo bar')->match('/foo (.*)/');

// 'bar'
```

<a name="method-fluent-str-match-all"></a>
#### `matchAll` {.collection-method}

`matchAll` メソッドは、指定された正規表現パターンに一致する文字列の部分を含むコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

式内で一致するグループを指定すると、Laravel は最初に一致したグループの一致のコレクションを返します。

```php
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

一致するものが見つからない場合は、空のコレクションが返されます。

<a name="method-fluent-str-is-match"></a>
#### `isMatch` {.collection-method}

文字列が指定された正規表現に一致する場合、`isMatch` メソッドは `true` を返します。

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->isMatch('/foo (.*)/');

// true

$result = Str::of('laravel')->isMatch('/foo (.*)/');

// false
```

<a name="method-fluent-str-new-line"></a>
#### `newLine` {.collection-method}

`newLine` メソッドは、文字列に「行末」文字を追加します。

```php
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
#### `padBoth` {.collection-method}

`padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padBoth(10, '_');

// '__James___'

$padded = Str::of('James')->padBoth(10);

// '  James   '
```

<a name="method-fluent-str-padleft"></a>
#### `padLeft` {.collection-method}

`padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padLeft(10, '-=');

// '-=-=-James'

$padded = Str::of('James')->padLeft(10);

// '     James'
```

<a name="method-fluent-str-padright"></a>
#### `padRight` {.collection-method}

`padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padRight(10, '-');

// 'James-----'

$padded = Str::of('James')->padRight(10);

// 'James     '
```

<a name="method-fluent-str-pipe"></a>
#### `pipe` {.collection-method}

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
#### `plural` {.collection-method}

`plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

関数に整数の引数を指定して、文字列の単数形または複数形を取得できます。

```php
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

`prependCount` 引数を指定して、書式設定された `$count` を複数化された文字列の前に付けることができます。

```php
use Illuminate\Support\Str;

$label = Str::of('car')->plural(1000, prependCount: true);

// 1,000 cars
```

<a name="method-fluent-str-position"></a>
#### `position` {.collection-method}

`position` メソッドは、文字列内で最初に出現する部分文字列の位置を返します。文字列内に部分文字列が存在しない場合は、`false` が返されます。

```php
use Illuminate\Support\Str;

$position = Str::of('Hello, World!')->position('Hello');

// 0

$position = Str::of('Hello, World!')->position('W');

// 7
```

<a name="method-fluent-str-prepend"></a>
#### `prepend` {.collection-method}

`prepend` メソッドは、指定された値を文字列の先頭に追加します。

```php
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
#### `remove` {.collection-method}

`remove` メソッドは、指定された値または値の配列を文字列から削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite ');

// Arkansas is beautiful!
```

文字列を削除するときに大文字と小文字を区別しないように、2 番目のパラメーターとして `false` を渡すこともできます。

<a name="method-fluent-str-repeat"></a>
#### `repeat` {.collection-method}

`repeat` メソッドは、指定された文字列を繰り返します。

```php
use Illuminate\Support\Str;

$repeated = Str::of('a')->repeat(5);

// aaaaa
```

<a name="method-fluent-str-replace"></a>
#### `replace` {.collection-method}

`replace` メソッドは、文字列内の指定された文字列を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

`replace` メソッドは、`caseSensitive` 引数も受け入れます。デフォルトでは、`replace` メソッドでは大文字と小文字が区別されます。

```php
$replaced = Str::of('macOS 13.x')->replace(
    'macOS', 'iOS', caseSensitive: false
);
```

<a name="method-fluent-str-replace-array"></a>
#### `replaceArray` {.collection-method}

`replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
#### `replaceFirst` {.collection-method}

`replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
#### `replaceLast` {.collection-method}

`replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
#### `replaceMatches` {.collection-method}

`replaceMatches` メソッドは、パターンに一致する文字列のすべての部分を指定された置換文字列に置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

`replaceMatches` メソッドは、指定されたパターンに一致する文字列の各部分で呼び出されるクロージャも受け入れます。これにより、クロージャ内で置換ロジックを実行し、置換された値を返すことができます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-replace-start"></a>
#### `replaceStart` {.collection-method}

`replaceStart` メソッドは、値が文字列の先頭にある場合にのみ、指定された値の最初の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceStart('Hello', 'Laravel');

// Laravel World

$replaced = Str::of('Hello World')->replaceStart('World', 'Laravel');

// Hello World
```

<a name="method-fluent-str-replace-end"></a>
#### `replaceEnd` {.collection-method}

`replaceEnd` メソッドは、値が文字列の最後にある場合にのみ、指定された値の最後の出現を置き換えます。

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

// Hello Laravel

$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

// Hello World
```

<a name="method-fluent-str-scan"></a>
#### `scan` {.collection-method}

`scan` メソッドは、[`sscanf` PHP 関数](https://www.php.net/manual/en/function.sscanf.php) でサポートされている形式に従って、文字列からの入力を解析してコレクションに入れます。

```php
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
#### `singular` {.collection-method}

`singular` メソッドは、文字列を単数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

```php
use Illuminate\Support\Str;

$singular = Str::of('cars')->singular();

// car

$singular = Str::of('children')->singular();

// child
```

<a name="method-fluent-str-slug"></a>
#### `slug` {.collection-method}

`slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

```php
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
#### `snake` {.collection-method}

`snake` メソッドは、指定された文字列を `snake_case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
#### `split` {.collection-method}

`split` メソッドは、正規表現を使用して文字列をコレクションに分割します。

```php
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
#### `squish` {.collection-method}

`squish` メソッドは、単語間の無関係な空白を含め、文字列から無関係な空白をすべて削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
#### `start` {.collection-method}

`start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->start('/');

// /this/string

$adjusted = Str::of('/this/string')->start('/');

// /this/string
```

<a name="method-fluent-str-starts-with"></a>
#### `startsWith` {.collection-method}

`startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

値の配列を渡して、指定された文字列が配列内のいずれかの値で始まるかどうかを判断することもできます。

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith(['This', 'That']);

// true
```

<a name="method-fluent-str-strip-tags"></a>
#### `stripTags` {.collection-method}

`stripTags` メソッドは、文字列からすべての HTML タグと PHP タグを削除します。

```php
use Illuminate\Support\Str;

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags();

// Taylor Otwell

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags('<b>');

// Taylor <b>Otwell</b>
```

<a name="method-fluent-str-studly"></a>
#### `studly` {.collection-method}

`studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
#### `substr` {.collection-method}

`substr` メソッドは、指定された start パラメーターと length パラメーターで指定された文字列の部分を返します。

```php
use Illuminate\Support\Str;

$string = Str::of('Laravel Framework')->substr(8);

// Framework

$string = Str::of('Laravel Framework')->substr(8, 5);

// Frame
```

<a name="method-fluent-str-substrreplace"></a>
#### `substrReplace` {.collection-method}

`substrReplace` メソッドは、文字列の一部内のテキストを、2 番目の引数で指定された位置から開始して、3 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 3 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

```php
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-swap"></a>
#### `swap` {.collection-method}

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
#### `take` {.collection-method}

`take` メソッドは、文字列の先頭から指定された数の文字を返します。

```php
use Illuminate\Support\Str;

$taken = Str::of('Build something amazing!')->take(5);

// Build
```

<a name="method-fluent-str-tap"></a>
#### `tap` {.collection-method}

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
#### `test` {.collection-method}

`test` メソッドは、文字列が指定された正規表現パターンに一致するかどうかを判断します。

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
#### `title` {.collection-method}

`title` メソッドは、指定された文字列を `Title Case` に変換します。

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-to-base64"></a>
#### `toBase64` {.collection-method}

`toBase64` メソッドは、指定された文字列を Base64 に変換します。

```php
use Illuminate\Support\Str;

$base64 = Str::of('Laravel')->toBase64();

// TGFyYXZlbA==
```

<a name="method-fluent-str-to-html-string"></a>
#### `toHtmlString` {.collection-method}

`toHtmlString` メソッドは、指定された文字列を `Illuminate\Support\HtmlString` のインスタンスに変換します。これは、Blade テンプレートでレンダリングされるときにエスケープされません。

```php
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-fluent-str-to-uri"></a>
#### `toUri` {.collection-method}

`toUri` メソッドは、指定された文字列を [Illuminate\Support\Uri](/docs/{{version}}/helpers#uri) のインスタンスに変換します。

```php
use Illuminate\Support\Str;

$uri = Str::of('https://example.com')->toUri();
```

<a name="method-fluent-str-transliterate"></a>
#### `transliterate` {.collection-method}

`transliterate` メソッドは、指定された文字列を最も近い ASCII 表現に変換しようとします。

```php
use Illuminate\Support\Str;

$email = Str::of('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ')->transliterate()

// 'test@laravel.com'
```

<a name="method-fluent-str-trim"></a>
#### `trim` {.collection-method}

`trim` メソッドは、指定された文字列をトリミングします。 PHP のネイティブ `trim` 関数とは異なり、Laravel の `trim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ltrim"></a>
#### `ltrim` {.collection-method}

`ltrim` メソッドは、文字列の左側をトリミングします。 PHP のネイティブ `ltrim` 関数とは異なり、Laravel の `ltrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```

<a name="method-fluent-str-rtrim"></a>
#### `rtrim` {.collection-method}

`rtrim` メソッドは、指定された文字列の右側をトリミングします。 PHP のネイティブ `rtrim` 関数とは異なり、Laravel の `rtrim` メソッドは Unicode 空白文字も削除します。

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
#### `ucfirst` {.collection-method}

`ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

```php
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
#### `ucsplit` {.collection-method}

`ucsplit` メソッドは、指定された文字列を大文字でコレクションに分割します。

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo ', 'Bar'])
```

<a name="method-fluent-str-ucwords"></a>
#### `ucwords` {.collection-method}

`ucwords` メソッドは、指定された文字列内の各単語の最初の文字を大文字に変換します。

```php
use Illuminate\Support\Str;

$string = Str::of('laravel framework')->ucwords();

// Laravel Framework
```

<a name="method-fluent-str-unwrap"></a>
#### `unwrap` {.collection-method}

`unwrap` メソッドは、指定された文字列の先頭と末尾から指定された文字列を削除します。

```php
use Illuminate\Support\Str;

Str::of('-Laravel-')->unwrap('-');

// Laravel

Str::of('{framework: "Laravel"}')->unwrap('{', '}');

// framework: "Laravel"
```

<a name="method-fluent-str-upper"></a>
#### `upper` {.collection-method}

`upper` メソッドは、指定された文字列を大文字に変換します。

```php
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
#### `when` {.collection-method}

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

必要に応じて、別のクロージャを 3 番目のパラメータとして `when` メソッドに渡すことができます。このクロージャは、条件パラメータが `false` と評価された場合に実行されます。

<a name="method-fluent-str-when-contains"></a>
#### `whenContains` {.collection-method}

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

必要に応じて、別のクロージャを 3 番目のパラメータとして渡すことができます。文字列に指定された値が含まれていない場合、クロージャが呼び出されます。

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
#### `whenContainsAll` {.collection-method}

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

必要に応じて、別のクロージャを 3 番目のパラメータとして渡すことができます。条件パラメータが `false` と評価された場合、クロージャが呼び出されます。

<a name="method-fluent-str-when-doesnt-end-with"></a>
#### `whenDoesntEndWith` {.collection-method}

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
#### `whenDoesntStartWith` {.collection-method}

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
#### `whenEmpty` {.collection-method}

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
#### `whenNotEmpty` {.collection-method}

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
#### `whenStartsWith` {.collection-method}

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
#### `whenEndsWith` {.collection-method}

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
#### `whenExactly` {.collection-method}

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
#### `whenNotExactly` {.collection-method}

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
#### `whenIs` {.collection-method}

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
#### `whenIsAscii` {.collection-method}

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
#### `whenIsUlid` {.collection-method}

文字列が有効な ULID の場合、`whenIsUlid` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```php
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
#### `whenIsUuid` {.collection-method}

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
#### `whenTest` {.collection-method}

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
#### `wordCount` {.collection-method}

`wordCount` メソッドは、文字列に含まれる単語の数を返します。

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
#### `words` {.collection-method}

`words` メソッドは、文字列内の単語数を制限します。必要に応じて、切り詰められた文字列に追加される追加の文字列を指定できます。

```php
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-fluent-str-wrap"></a>
#### `wrap` {.collection-method}

`wrap` メソッドは、指定された文字列を追加の文字列または文字列のペアでラップします。

```php
use Illuminate\Support\Str;

Str::of('Laravel')->wrap('"');

// "Laravel"

Str::is('is')->wrap(before: 'This ', after: ' Laravel!');

// This is Laravel!
```

