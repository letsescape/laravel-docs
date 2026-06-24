<!-- # Helpers -->
# Helpers

- [Introduction](#introduction)
- [Available Methods](#available-methods)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel includes a variety of global "helper" PHP functions. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient. -->
Laravel には、さまざまなグローバル「ヘルパ」PHP 関数が含まれています。これらの関数の多くはフレームワーク自体によって使用されます。ただし、便利だと思われる場合は、独自のアプリケーションで自由に使用できます。

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
[Arr::last](#method-array-last)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
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
[Arr::last](#method-array-last)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
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
[mix](#method-mix)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)
-->
[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
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
[Str::camel](#method-camel-case)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::endsWith](#method-ends-with)
[Str::finish](#method-str-finish)
[Str::headline](#method-str-headline)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
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
[Str::start](#method-str-start)
[Str::startsWith](#method-starts-with)
[Str::studly](#method-studly-case)
[Str::substr](#method-str-substr)
[Str::substrCount](#method-str-substrcount)
[Str::substrReplace](#method-str-substrreplace)
[Str::title](#method-title-case)
[Str::toHtmlString](#method-str-to-html-string)
[Str::ucfirst](#method-str-ucfirst)
[Str::upper](#method-str-upper)
[Str::uuid](#method-str-uuid)
[Str::wordCount](#method-str-word-count)
[Str::words](#method-str-words)
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
[Str::camel](#method-camel-case)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::endsWith](#method-ends-with)
[Str::finish](#method-str-finish)
[Str::headline](#method-str-headline)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
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
[Str::start](#method-str-start)
[Str::startsWith](#method-starts-with)
[Str::studly](#method-studly-case)
[Str::substr](#method-str-substr)
[Str::substrCount](#method-str-substrcount)
[Str::substrReplace](#method-str-substrreplace)
[Str::title](#method-title-case)
[Str::toHtmlString](#method-str-to-html-string)
[Str::ucfirst](#method-str-ucfirst)
[Str::upper](#method-str-upper)
[Str::uuid](#method-str-uuid)
[Str::wordCount](#method-str-word-count)
[Str::words](#method-str-words)
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
[camel](#method-fluent-str-camel)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[dirname](#method-fluent-str-dirname)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[ltrim](#method-fluent-str-ltrim)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
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
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[trim](#method-fluent-str-trim)
[ucfirst](#method-fluent-str-ucfirst)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenEmpty](#method-fluent-str-when-empty)
[whenNotEmpty](#method-fluent-str-when-not-empty)
[whenStartsWith](#method-fluent-str-when-starts-with)
[whenEndsWith](#method-fluent-str-when-ends-with)
[whenExactly](#method-fluent-str-when-exactly)
[whenIs](#method-fluent-str-when-is)
[whenIsAscii](#method-fluent-str-when-is-ascii)
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
[camel](#method-fluent-str-camel)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[dirname](#method-fluent-str-dirname)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[ltrim](#method-fluent-str-ltrim)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
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
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[trim](#method-fluent-str-trim)
[ucfirst](#method-fluent-str-ucfirst)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenEmpty](#method-fluent-str-when-empty)
[whenNotEmpty](#method-fluent-str-when-not-empty)
[whenStartsWith](#method-fluent-str-when-starts-with)
[whenEndsWith](#method-fluent-str-when-ends-with)
[whenExactly](#method-fluent-str-when-exactly)
[whenIs](#method-fluent-str-when-is)
[whenIsAscii](#method-fluent-str-when-is-ascii)
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
[url](#method-url)
-->
[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
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
[dd](#method-dd)
[dispatch](#method-dispatch)
[dump](#method-dump)
[env](#method-env)
[event](#method-event)
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
[dd](#method-dd)
[dispatch](#method-dispatch)
[dump](#method-dump)
[env](#method-env)
[event](#method-event)
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
`Arr::accessible` メソッドは、指定された値が配列にアクセスできるかどうかを判断します。

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
`Arr::add` メソッドは、指定されたキーが配列内に存在しない場合、または `null` に設定されている場合に、指定されたキーと値のペアを配列に追加します。

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
`Arr::collapse` メソッドは、配列の配列を単一の配列に折りたたみます。

```
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
<!-- #### `Arr::crossJoin()` -->
#### `Arr::crossJoin()`
<!-- The `Arr::crossJoin` method cross joins the given arrays, returning a Cartesian product with all possible permutations: -->
`Arr::crossJoin` メソッドは、指定された配列を相互結合し、すべての可能な順列を含むデカルト積を返します。

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
`Arr::divide` メソッドは 2 つの配列を返します。1 つはキーを含み、もう 1 つは指定された配列の値を含みます。

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
`Arr::dot` メソッドは、多次元配列を、深さを示すために「ドット」表記を使用する単一レベルの配列に平坦化します。

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
`Arr::except` メソッドは、指定されたキーと値のペアを配列から削除します。

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
`Arr::exists` メソッドは、指定されたキーが指定された配列に存在することを確認します。

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
`Arr::first` メソッドは、指定された真理値テストに合格した配列の最初の要素を返します。

```
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function ($value, $key) {
    return $value >= 150;
});

// 200
```

<!-- A default value may also be passed as the third parameter to the method. This value will be returned if no value passes the truth test: -->
デフォルト値を 3 番目のパラメータとしてメソッドに渡すこともできます。真実テストに合格する値がない場合、この値が返されます。

```
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
<!-- #### `Arr::flatten()` -->
#### `Arr::flatten()`
<!-- The `Arr::flatten` method flattens a multi-dimensional array into a single level array: -->
`Arr::flatten` メソッドは、多次元配列を単一レベルの配列にフラット化します。

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
`Arr::forget` メソッドは、「ドット」表記を使用して、深くネストされた配列から指定されたキーと値のペアを削除します。

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
`Arr::get` メソッドは、「ドット」表記を使用して、深くネストされた配列から値を取得します。

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

<!-- The `Arr::get` method also accepts a default value, which will be returned if the specified key is not present in the array: -->
`Arr::get` メソッドは、指定されたキーが配列に存在しない場合に返されるデフォルト値も受け入れます。

```
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
<!-- #### `Arr::has()` -->
#### `Arr::has()`
<!-- The `Arr::has` method checks whether a given item or items exists in an array using "dot" notation: -->
`Arr::has` メソッドは、「ドット」表記を使用して、指定された項目が配列内に存在するかどうかをチェックします。

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
`Arr::hasAny` メソッドは、「ドット」表記を使用して、指定されたセット内の項目が配列内に存在するかどうかをチェックします。

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
<!-- The `Arr::isAssoc` returns `true` if the given array is an associative array. An array is considered "associative" if it doesn't have sequential numerical keys beginning with zero: -->
指定された配列が連想配列の場合、`Arr::isAssoc` は `true` を返します。配列にゼロで始まる連続した数値キーがない場合、その配列は「結合」とみなされます。

```
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-last"></a>
<!-- #### `Arr::last()` -->
#### `Arr::last()`
<!-- The `Arr::last` method returns the last element of an array passing a given truth test: -->
`Arr::last` メソッドは、指定された真理値テストに合格した配列の最後の要素を返します。

```
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function ($value, $key) {
    return $value >= 150;
});

// 300
```

<!-- A default value may be passed as the third argument to the method. This value will be returned if no value passes the truth test: -->
デフォルト値は、メソッドの 3 番目の引数として渡すことができます。真実テストに合格する値がない場合、この値が返されます。

```
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-only"></a>
<!-- #### `Arr::only()` -->
#### `Arr::only()`
<!-- The `Arr::only` method returns only the specified key / value pairs from the given array: -->
`Arr::only` メソッドは、指定された配列から指定されたキーと値のペアのみを返します。

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
`Arr::pluck` メソッドは、配列から指定されたキーのすべての値を取得します。

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
結果のリストにどのようにキーを設定するかを指定することもできます。

```
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
<!-- #### `Arr::prepend()` -->
#### `Arr::prepend()`
<!-- The `Arr::prepend` method will push an item onto the beginning of an array: -->
`Arr::prepend` メソッドは、項目を配列の先頭にプッシュします。

```
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

<!-- If needed, you may specify the key that should be used for the value: -->
必要に応じて、値に使用するキーを指定できます。

```
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-pull"></a>
<!-- #### `Arr::pull()` -->
#### `Arr::pull()`
<!-- The `Arr::pull` method returns and removes a key / value pair from an array: -->
`Arr::pull` メソッドは、キーと値のペアを返し、配列から削除します。

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

<!-- A default value may be passed as the third argument to the method. This value will be returned if the key doesn't exist: -->
デフォルト値は、メソッドの 3 番目の引数として渡すことができます。キーが存在しない場合は、この値が返されます。

```
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
<!-- #### `Arr::query()` -->
#### `Arr::query()`
<!-- The `Arr::query` method converts the array into a query string: -->
`Arr::query` メソッドは、配列をクエリ文字列に変換します。

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
`Arr::random` メソッドは、配列からランダムな値を返します。

```
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (retrieved randomly)
```

<!-- You may also specify the number of items to return as an optional second argument. Note that providing this argument will return an array even if only one item is desired: -->
オプションの 2 番目の引数として、返す項目の数を指定することもできます。この引数を指定すると、必要な項目が 1 つだけの場合でも配列が返されることに注意してください。

```
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (retrieved randomly)
```

<a name="method-array-set"></a>
<!-- #### `Arr::set()` -->
#### `Arr::set()`
<!-- The `Arr::set` method sets a value within a deeply nested array using "dot" notation: -->
`Arr::set` メソッドは、「ドット」表記を使用して、深くネストされた配列内の値を設定します。

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
`Arr::shuffle` メソッドは、配列内の項目をランダムにシャッフルします。

```
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-array-sort"></a>
<!-- #### `Arr::sort()` -->
#### `Arr::sort()`
<!-- The `Arr::sort` method sorts an array by its values: -->
`Arr::sort` メソッドは、配列を値で並べ替えます。

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

<!-- You may also sort the array by the results of a given closure: -->
特定のクロージャの結果によって配列を並べ替えることもできます。

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

<a name="method-array-sort-recursive"></a>
<!-- #### `Arr::sortRecursive()` -->
#### `Arr::sortRecursive()`
<!-- The `Arr::sortRecursive` method recursively sorts an array using the `sort` function for numerically indexed sub-arrays and the `ksort` function for associative sub-arrays: -->
`Arr::sortRecursive` メソッドは、数値インデックス付きサブ配列の場合は `sort` 関数を使用し、連想サブ配列の場合は `ksort` 関数を使用して、配列を再帰的に並べ替えます。

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
`Arr::toCssClasses` は、CSS クラス文字列を条件付きでコンパイルします。このメソッドはクラスの配列を受け入れます。配列キーには追加するクラスが含まれ、値はブール式です。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

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

<!-- This method powers Laravel's functionality allowing [merging classes with a Blade component's attribute bag](/docs/8.x/blade#conditionally-merge-classes) as well as the `@class` [Blade directive](/docs/8.x/blade#conditional-classes). -->
このメソッドは、Laravel の機能を強化し、[merging classes with a Blade component's attribute bag](/docs/8.x/blade#conditionally-merge-classes) および `@class` [Blade directive](/docs/8.x/blade#conditional-classes) を許可します。

<a name="method-array-undot"></a>
<!-- #### `Arr::undot()` -->
#### `Arr::undot()`
<!-- The `Arr::undot` method expands a single-dimensional array that uses "dot" notation into a multi-dimensional array: -->
`Arr::undot` メソッドは、「ドット」表記を使用する 1 次元配列を多次元配列に拡張します。

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
`Arr::where` メソッドは、指定されたクロージャを使用して配列をフィルタリングします。

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
`Arr::whereNotNull` メソッドは、指定された配列からすべての `null` 値を削除します。

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
`Arr::wrap` メソッドは、指定された値を配列にラップします。指定された値がすでに配列である場合は、変更せずに返されます。

```
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

<!-- If the given value is `null`, an empty array will be returned: -->
指定された値が `null` の場合、空の配列が返されます。

```
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
<!-- #### `data_fill()` -->
#### `data_fill()`
<!-- The `data_fill` function sets a missing value within a nested array or object using "dot" notation: -->
`data_fill` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の欠損値を設定します。

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

<!-- This function also accepts asterisks as wildcards and will fill the target accordingly: -->
この関数はワイルドカードとしてアスタリスクも受け入れ、それに応じてターゲットを入力します。

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
`data_get` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクトから値を取得します。

```
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

<!-- The `data_get` function also accepts a default value, which will be returned if the specified key is not found: -->
`data_get` 関数は、指定されたキーが見つからない場合に返されるデフォルト値も受け入れます。

```
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

<!-- The function also accepts wildcards using asterisks, which may target any key of the array or object: -->
この関数は、配列またはオブジェクトの任意のキーを対象とするアスタリスクを使用したワイルドカードも受け入れます。

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
`data_set` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の値を設定します。

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<!-- This function also accepts wildcards using asterisks and will set values on the target accordingly: -->
この関数はアスタリスクを使用したワイルドカードも受け入れ、それに応じてターゲットに値を設定します。

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
デフォルトでは、既存の値はすべて上書きされます。値が存在しない場合にのみ値を設定したい場合は、関数の 4 番目の引数として `false` を渡すことができます。

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, $overwrite = false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-head"></a>
<!-- #### `head()` -->
#### `head()`
<!-- The `head` function returns the first element in the given array: -->
`head` 関数は、指定された配列の最初の要素を返します。

```
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
<!-- #### `last()` -->
#### `last()`
<!-- The `last` function returns the last element in the given array: -->
`last` 関数は、指定された配列の最後の要素を返します。

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
`app_path` 関数は、アプリケーションの `app` ディレクトリへの完全修飾パスを返します。 `app_path` 関数を使用して、アプリケーション ディレクトリを基準としたファイルへの完全修飾パスを生成することもできます。

```
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
<!-- #### `base_path()` -->
#### `base_path()`
<!-- The `base_path` function returns the fully qualified path to your application's root directory. You may also use the `base_path` function to generate a fully qualified path to a given file relative to the project root directory: -->
`base_path` 関数は、アプリケーションのルート ディレクトリへの完全修飾パスを返します。 `base_path` 関数を使用して、プロジェクトのルート ディレクトリを基準とした特定のファイルへの完全修飾パスを生成することもできます。

```
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
<!-- #### `config_path()` -->
#### `config_path()`
<!-- The `config_path` function returns the fully qualified path to your application's `config` directory. You may also use the `config_path` function to generate a fully qualified path to a given file within the application's configuration directory: -->
`config_path` 関数は、アプリケーションの `config` ディレクトリへの完全修飾パスを返します。 `config_path` 関数を使用して、アプリケーションの構成ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
<!-- #### `database_path()` -->
#### `database_path()`
<!-- The `database_path` function returns the fully qualified path to your application's `database` directory. You may also use the `database_path` function to generate a fully qualified path to a given file within the database directory: -->
`database_path` 関数は、アプリケーションの `database` ディレクトリへの完全修飾パスを返します。 `database_path` 関数を使用して、データベース ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-mix"></a>
<!-- #### `mix()` -->
#### `mix()`
<!-- The `mix` function returns the path to a [versioned Mix file](/docs/8.x/mix): -->
`mix` 関数は、[versioned Mix file](/docs/8.x/mix) へのパスを返します。

```
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
<!-- #### `public_path()` -->
#### `public_path()`
<!-- The `public_path` function returns the fully qualified path to your application's `public` directory. You may also use the `public_path` function to generate a fully qualified path to a given file within the public directory: -->
`public_path` 関数は、アプリケーションの `public` ディレクトリへの完全修飾パスを返します。 `public_path` 関数を使用して、パブリック ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
<!-- #### `resource_path()` -->
#### `resource_path()`
<!-- The `resource_path` function returns the fully qualified path to your application's `resources` directory. You may also use the `resource_path` function to generate a fully qualified path to a given file within the resources directory: -->
`resource_path` 関数は、アプリケーションの `resources` ディレクトリへの完全修飾パスを返します。 `resource_path` 関数を使用して、リソース ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
<!-- #### `storage_path()` -->
#### `storage_path()`
<!-- The `storage_path` function returns the fully qualified path to your application's `storage` directory. You may also use the `storage_path` function to generate a fully qualified path to a given file within the storage directory: -->
`storage_path` 関数は、アプリケーションの `storage` ディレクトリへの完全修飾パスを返します。 `storage_path` 関数を使用して、ストレージ ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

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
<!-- The `__` function translates the given translation string or translation key using your [localization files](/docs/8.x/localization): -->
`__` 関数は、[localization files](/docs/8.x/localization) を使用して、指定された翻訳文字列または翻訳キーを翻訳します。

```
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

```
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
<!-- #### `e()` -->
#### `e()`
<!-- The `e` function runs PHP's `htmlspecialchars` function with the `double_encode` option set to `true` by default: -->
`e` 関数は、デフォルトで `double_encode` オプションを `true` に設定して、PHP の `htmlspecialchars` 関数を実行します。

```
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
<!-- #### `preg_replace_array()` -->
#### `preg_replace_array()`
<!-- The `preg_replace_array` function replaces a given pattern in the string sequentially using an array: -->
`preg_replace_array` 関数は、配列を使用して文字列内の指定されたパターンを順番に置き換えます。

```
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
<!-- #### `Str::after()` -->
#### `Str::after()`
<!-- The `Str::after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::after` メソッドは、文字列内の指定された値以降のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
<!-- #### `Str::afterLast()` -->
#### `Str::afterLast()`
<!-- The `Str::afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`Str::afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-ascii"></a>
<!-- #### `Str::ascii()` -->
#### `Str::ascii()`
<!-- The `Str::ascii` method will attempt to transliterate the string into an ASCII value: -->
`Str::ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

```
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
<!-- #### `Str::before()` -->
#### `Str::before()`
<!-- The `Str::before` method returns everything before the given value in a string: -->
`Str::before` メソッドは、文字列内の指定された値より前のすべてを返します。

```
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
<!-- #### `Str::beforeLast()` -->
#### `Str::beforeLast()`
<!-- The `Str::beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`Str::beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

```
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
<!-- #### `Str::between()` -->
#### `Str::between()`
<!-- The `Str::between` method returns the portion of a string between two values: -->
`Str::between` メソッドは、2 つの値の間の文字列の部分を返します。

```
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-camel-case"></a>
<!-- #### `Str::camel()` -->
#### `Str::camel()`
<!-- The `Str::camel` method converts the given string to `camelCase`: -->
`Str::camel` メソッドは、指定された文字列を `camelCase` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// fooBar
```

<a name="method-str-contains"></a>
<!-- #### `Str::contains()` -->
#### `Str::contains()`
<!-- The `Str::contains` method determines if the given string contains the given value. This method is case sensitive: -->
`Str::contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。このメソッドでは大文字と小文字が区別されます。

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

<a name="method-str-contains-all"></a>
<!-- #### `Str::containsAll()` -->
#### `Str::containsAll()`
<!-- The `Str::containsAll` method determines if the given string contains all of the values in a given array: -->
`Str::containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

```
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

<a name="method-ends-with"></a>
<!-- #### `Str::endsWith()` -->
#### `Str::endsWith()`
<!-- The `Str::endsWith` method determines if the given string ends with the given value: -->
`Str::endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

```
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```


<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

```
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-str-finish"></a>
<!-- #### `Str::finish()` -->
#### `Str::finish()`
<!-- The `Str::finish` method adds a single instance of the given value to a string if it does not already end with that value: -->
`Str::finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

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
`Str::headline` メソッドは、大文字と小文字、ハイフン、またはアンダースコアで区切られた文字列を、各単語の最初の文字が大文字になったスペースで区切られた文字列に変換します。

```
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-is"></a>
<!-- #### `Str::is()` -->
#### `Str::is()`
<!-- The `Str::is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values: -->
`Str::is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます。

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
`Str::isAscii` メソッドは、指定された文字列が 7 ビット ASCII であるかどうかを判断します。

```
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-uuid"></a>
<!-- #### `Str::isUuid()` -->
#### `Str::isUuid()`
<!-- The `Str::isUuid` method determines if the given string is a valid UUID: -->
`Str::isUuid` メソッドは、指定された文字列が有効な UUID かどうかを判断します。

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
`Str::kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-length"></a>
<!-- #### `Str::length()` -->
#### `Str::length()`
<!-- The `Str::length` method returns the length of the given string: -->
`Str::length` メソッドは、指定された文字列の長さを返します。

```
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
<!-- #### `Str::limit()` -->
#### `Str::limit()`
<!-- The `Str::limit` method truncates the given string to the specified length: -->
`Str::limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

```
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

<!-- You may pass a third argument to the method to change the string that will be appended to the end of the truncated string: -->
メソッドに 3 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更できます。

```
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

<a name="method-str-lower"></a>
<!-- #### `Str::lower()` -->
#### `Str::lower()`
<!-- The `Str::lower` method converts the given string to lowercase: -->
`Str::lower` メソッドは、指定された文字列を小文字に変換します。

```
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
<!-- #### `Str::markdown()` -->
#### `Str::markdown()`
<!-- The `Str::markdown` method converts GitHub flavored Markdown into HTML: -->
`Str::markdown` メソッドは、GitHub フレーバーの Markdown を HTML に変換します。

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
`Str::mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

```
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

<!-- If needed, you provide a negative number as the third argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
必要に応じて、`mask` メソッドの 3 番目の引数として負の数値を指定します。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

```
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-ordered-uuid"></a>
<!-- #### `Str::orderedUuid()` -->
#### `Str::orderedUuid()`
<!-- The `Str::orderedUuid` method generates a "timestamp first" UUID that may be efficiently stored in an indexed database column. Each UUID that is generated using this method will be sorted after UUIDs previously generated using the method: -->
`Str::orderedUuid` メソッドは、インデックス付きデータベース列に効率的に格納できる「タイムスタンプ優先」の UUID を生成します。このメソッドを使用して生成された各 UUID は、以前に次のメソッドを使用して生成された UUID の後にソートされます。

```
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
<!-- #### `Str::padBoth()` -->
#### `Str::padBoth()`
<!-- The `Str::padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches a desired length: -->
`Str::padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

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
`Str::padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

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
`Str::padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

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
<!-- The `Str::plural` method converts a singular word string to its plural form. This function currently only supports the English language: -->
`Str::plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は現在英語のみをサポートしています。

```
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

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
<!-- The `Str::pluralStudly` method converts a singular word string formatted in studly caps case to its plural form. This function currently only supports the English language: -->
`Str::pluralStudly` メソッドは、大文字小文字でフォーマットされた単数形の単語文字列を複数形に変換します。この関数は現在英語のみをサポートしています。

```
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

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
`Str::random` メソッドは、指定された長さのランダムな文字列を生成します。この関数は、PHP の `random_bytes` 関数を使用します。

```
use Illuminate\Support\Str;

$random = Str::random(40);
```

<a name="method-str-remove"></a>
<!-- #### `Str::remove()` -->
#### `Str::remove()`
<!-- The `Str::remove` method removes the given value or array of values from the string: -->
`Str::remove` メソッドは、指定された値または値の配列を文字列から削除します。

```
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

<!-- You may also pass `false` as a third argument to the `remove` method to ignore case when removing strings. -->
文字列を削除するときに大文字と小文字を区別しないように、`false` を `remove` メソッドの 3 番目の引数として渡すこともできます。

<a name="method-str-replace"></a>
<!-- #### `Str::replace()` -->
#### `Str::replace()`
<!-- The `Str::replace` method replaces a given string within the string: -->
`Str::replace` メソッドは、文字列内の指定された文字列を置き換えます。

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
`Str::replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

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
`Str::replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

```
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
<!-- #### `Str::replaceLast()` -->
#### `Str::replaceLast()`
<!-- The `Str::replaceLast` method replaces the last occurrence of a given value in a string: -->
`Str::replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

```
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```


<a name="method-str-reverse"></a>
<!-- #### `Str::reverse()` -->
#### `Str::reverse()`
<!-- The `Str::reverse` method reverses the given string: -->
`Str::reverse` メソッドは、指定された文字列を反転します。

```
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
<!-- #### `Str::singular()` -->
#### `Str::singular()`
<!-- The `Str::singular` method converts a string to its singular form. This function currently only supports the English language: -->
`Str::singular` メソッドは、文字列を単数形に変換します。この関数は現在英語のみをサポートしています。

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
`Str::slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

```
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
<!-- #### `Str::snake()` -->
#### `Str::snake()`
<!-- The `Str::snake` method converts the given string to `snake_case`: -->
`Str::snake` メソッドは、指定された文字列を `snake_case` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-start"></a>
<!-- #### `Str::start()` -->
#### `Str::start()`
<!-- The `Str::start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`Str::start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

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
`Str::startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

```
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

<!-- If an array of possible values is passed, the `startsWith` method will return `true` if the string begins with any of the given values: -->
可能な値の配列が渡された場合、文字列が指定された値のいずれかで始まる場合、`startsWith` メソッドは `true` を返します。

```
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
<!-- #### `Str::studly()` -->
#### `Str::studly()`
<!-- The `Str::studly` method converts the given string to `StudlyCase`: -->
`Str::studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
<!-- #### `Str::substr()` -->
#### `Str::substr()`
<!-- The `Str::substr` method returns the portion of string specified by the start and length parameters: -->
`Str::substr` メソッドは、start パラメーターと length パラメーターで指定された文字列の部分を返します。

```
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
<!-- #### `Str::substrCount()` -->
#### `Str::substrCount()`
<!-- The `Str::substrCount` method returns the number of occurrences of a given value in the given string: -->
`Str::substrCount` メソッドは、指定された文字列内の指定された値の出現数を返します。

```
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
<!-- #### `Str::substrReplace()` -->
#### `Str::substrReplace()`
<!-- The `Str::substrReplace` method replaces text within a portion of a string, starting at the position specified by the third argument and replacing the number of characters specified by the fourth argument. Passing `0` to the method's fourth argument will insert the string at the specified position without replacing any of the existing characters in the string: -->
`Str::substrReplace` メソッドは、文字列の一部内のテキストを、3 番目の引数で指定された位置から開始して 4 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 4 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

```
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-title-case"></a>
<!-- #### `Str::title()` -->
#### `Str::title()`
<!-- The `Str::title` method converts the given string to `Title Case`: -->
`Str::title` メソッドは、指定された文字列を `Title Case` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-html-string"></a>
<!-- #### `Str::toHtmlString()` -->
#### `Str::toHtmlString()`
<!-- The `Str::toHtmlString` method converts the string instance to an instance of `Illuminate\Support\HtmlString`, which may be displayed in Blade templates: -->
`Str::toHtmlString` メソッドは、文字列インスタンスを `Illuminate\Support\HtmlString` のインスタンスに変換し、Blade テンプレートに表示される可能性があります。

```
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-str-ucfirst"></a>
<!-- #### `Str::ucfirst()` -->
#### `Str::ucfirst()`
<!-- The `Str::ucfirst` method returns the given string with the first character capitalized: -->
`Str::ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

```
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-upper"></a>
<!-- #### `Str::upper()` -->
#### `Str::upper()`
<!-- The `Str::upper` method converts the given string to uppercase: -->
`Str::upper` メソッドは、指定された文字列を大文字に変換します。

```
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-uuid"></a>
<!-- #### `Str::uuid()` -->
#### `Str::uuid()`
<!-- The `Str::uuid` method generates a UUID (version 4): -->
`Str::uuid` メソッドは UUID (バージョン 4) を生成します。

```
use Illuminate\Support\Str;

return (string) Str::uuid();
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

<a name="method-str-words"></a>
<!-- #### `Str::words()` -->
#### `Str::words()`
<!-- The `Str::words` method limits the number of words in a string. An additional string may be passed to this method via its third argument to specify which string should be appended to the end of the truncated string: -->
`Str::words` メソッドは、文字列内の単語数を制限します。追加の文字列を 3 番目の引数を介してこのメ​​ソッドに渡し、切り詰められた文字列の末尾に追加する文字列を指定できます。

```
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-trans"></a>
<!-- #### `trans()` -->
#### `trans()`
<!-- The `trans` function translates the given translation key using your [localization files](/docs/8.x/localization): -->
`trans` 関数は、[localization files](/docs/8.x/localization) を使用して、指定された変換キーを変換します。

```
echo trans('messages.welcome');
```

<!-- If the specified translation key does not exist, the `trans` function will return the given key. So, using the example above, the `trans` function would return `messages.welcome` if the translation key does not exist. -->
指定された変換キーが存在しない場合、`trans` 関数は指定されたキーを返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`trans` 関数は `messages.welcome` を返します。

<a name="method-trans-choice"></a>
<!-- #### `trans_choice()` -->
#### `trans_choice()`
<!-- The `trans_choice` function translates the given translation key with inflection: -->
`trans_choice` 関数は、指定された変換キーを語形変化を使用して変換します。

```
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

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
<!-- #### `afterLast` -->
#### `afterLast`
<!-- The `afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string: -->
`afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

```
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-append"></a>
<!-- #### `append` -->
#### `append`
<!-- The `append` method appends the given values to the string: -->
`append` メソッドは、指定された値を文字列に追加します。

```
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
<!-- #### `ascii` -->
#### `ascii`
<!-- The `ascii` method will attempt to transliterate the string into an ASCII value: -->
`ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

```
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
<!-- #### `basename` -->
#### `basename`
<!-- The `basename` method will return the trailing name component of the given string: -->
`basename` メソッドは、指定された文字列の末尾の名前コンポーネントを返します。

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

<!-- If needed, you may provide an "extension" that will be removed from the trailing component: -->
必要に応じて、後続コンポーネントから削除される「拡張機能」を指定できます。

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
<!-- #### `before` -->
#### `before`
<!-- The `before` method returns everything before the given value in a string: -->
`before` メソッドは、文字列内の指定された値より前のすべてを返します。

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
<!-- #### `beforeLast` -->
#### `beforeLast`
<!-- The `beforeLast` method returns everything before the last occurrence of the given value in a string: -->
`beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
<!-- #### `between` -->
#### `between`
<!-- The `between` method returns the portion of a string between two values: -->
`between` メソッドは、2 つの値の間の文字列の部分を返します。

```
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-camel"></a>
<!-- #### `camel` -->
#### `camel`
<!-- The `camel` method converts the given string to `camelCase`: -->
`camel` メソッドは、指定された文字列を `camelCase` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// fooBar
```

<a name="method-fluent-str-contains"></a>
<!-- #### `contains` -->
#### `contains`
<!-- The `contains` method determines if the given string contains the given value. This method is case sensitive: -->
`contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。このメソッドでは大文字と小文字が区別されます。

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

<a name="method-fluent-str-contains-all"></a>
<!-- #### `containsAll` -->
#### `containsAll`
<!-- The `containsAll` method determines if the given string contains all of the values in the given array: -->
`containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

```
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

<a name="method-fluent-str-dirname"></a>
<!-- #### `dirname` -->
#### `dirname`
<!-- The `dirname` method returns the parent directory portion of the given string: -->
`dirname` メソッドは、指定された文字列の親ディレクトリ部分を返します。

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

<!-- If necessary, you may specify how many directory levels you wish to trim from the string: -->
必要に応じて、文字列から削除するディレクトリ レベルの数を指定できます。

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-ends-with"></a>
<!-- #### `endsWith` -->
#### `endsWith`
<!-- The `endsWith` method determines if the given string ends with the given value: -->
`endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

<!-- You may also pass an array of values to determine if the given string ends with any of the values in the array: -->
値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

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
`exactly` メソッドは、指定された文字列が別の文字列と完全に一致するかどうかを判断します。

```
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-explode"></a>
<!-- #### `explode` -->
#### `explode`
<!-- The `explode` method splits the string by the given delimiter and returns a collection containing each section of the split string: -->
`explode` メソッドは、指定された区切り文字で文字列を分割し、分割された文字列の各セクションを含むコレクションを返します。

```
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
<!-- #### `finish` -->
#### `finish`
<!-- The `finish` method adds a single instance of the given value to a string if it does not already end with that value: -->
`finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

```
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-is"></a>
<!-- #### `is` -->
#### `is`
<!-- The `is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values -->
`is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます

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
`isAscii` メソッドは、指定された文字列が ASCII 文字列であるかどうかを判断します。

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
`isEmpty` メソッドは、指定された文字列が空かどうかを判断します。

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
`isNotEmpty` メソッドは、指定された文字列が空でないかどうかを判断します。


```
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-uuid"></a>
<!-- #### `isUuid` -->
#### `isUuid`
<!-- The `isUuid` method determines if a given string is a UUID: -->
`isUuid` メソッドは、指定された文字列が UUID かどうかを判断します。

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
`kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-length"></a>
<!-- #### `length` -->
#### `length`
<!-- The `length` method returns the length of the given string: -->
`length` メソッドは、指定された文字列の長さを返します。

```
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
<!-- #### `limit` -->
#### `limit`
<!-- The `limit` method truncates the given string to the specified length: -->
`limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

```
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

<!-- You may also pass a second argument to change the string that will be appended to the end of the truncated string: -->
2 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更することもできます。

```
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

<a name="method-fluent-str-lower"></a>
<!-- #### `lower` -->
#### `lower`
<!-- The `lower` method converts the given string to lowercase: -->
`lower` メソッドは、指定された文字列を小文字に変換します。

```
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-ltrim"></a>
<!-- #### `ltrim` -->
#### `ltrim`
<!-- The `ltrim` method trims the left side of the string: -->
`ltrim` メソッドは、文字列の左側をトリミングします。

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
`markdown` メソッドは、GitHub フレーバーの Markdown を HTML に変換します。

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
`mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

```
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

<!-- If needed, you provide a negative number as the third argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string: -->
必要に応じて、`mask` メソッドの 3 番目の引数として負の数値を指定します。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

```
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com
```

<a name="method-fluent-str-match"></a>
<!-- #### `match` -->
#### `match`
<!-- The `match` method will return the portion of a string that matches a given regular expression pattern: -->
`match` メソッドは、指定された正規表現パターンに一致する文字列の部分を返します。

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
`matchAll` メソッドは、指定された正規表現パターンに一致する文字列の部分を含むコレクションを返します。

```
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

<!-- If you specify a matching group within the expression, Laravel will return a collection of that group's matches: -->
式内で一致するグループを指定すると、Laravel はそのグループの一致のコレクションを返します。

```
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

<!-- If no matches are found, an empty collection will be returned. -->
一致するものが見つからない場合は、空のコレクションが返されます。

<a name="method-fluent-str-padboth"></a>
<!-- #### `padBoth` -->
#### `padBoth`
<!-- The `padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches the desired length: -->
`padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

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
`padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

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
`padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

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
`pipe` メソッドを使用すると、現在の値を指定された呼び出し可能オブジェクトに渡すことで文字列を変換できます。

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
<!-- The `plural` method converts a singular word string to its plural form. This function currently only supports the English language: -->
`plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は現在英語のみをサポートしています。

```
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

<!-- You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string: -->
関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

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
`prepend` メソッドは、指定された値を文字列の先頭に追加します。

```
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
<!-- #### `remove` -->
#### `remove`
<!-- The `remove` method removes the given value or array of values from the string: -->
`remove` メソッドは、指定された値または値の配列を文字列から削除します。

```
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite');

// Arkansas is beautiful!
```

<!-- You may also pass `false` as a second parameter to ignore case when removing strings. -->
文字列を削除するときに大文字と小文字を区別しないように、2 番目のパラメーターとして `false` を渡すこともできます。

<a name="method-fluent-str-replace"></a>
<!-- #### `replace` -->
#### `replace`
<!-- The `replace` method replaces a given string within the string: -->
`replace` メソッドは、文字列内の指定された文字列を置き換えます。

```
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

<a name="method-fluent-str-replace-array"></a>
<!-- #### `replaceArray` -->
#### `replaceArray`
<!-- The `replaceArray` method replaces a given value in the string sequentially using an array: -->
`replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

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
`replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
<!-- #### `replaceLast` -->
#### `replaceLast`
<!-- The `replaceLast` method replaces the last occurrence of a given value in a string: -->
`replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
<!-- #### `replaceMatches` -->
#### `replaceMatches`
<!-- The `replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string: -->
`replaceMatches` メソッドは、パターンに一致する文字列のすべての部分を指定された置換文字列に置き換えます。

```
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

<!-- The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value: -->
`replaceMatches` メソッドは、指定されたパターンに一致する文字列の各部分で呼び出されるクロージャも受け入れます。これにより、クロージャ内で置換ロジックを実行し、置換された値を返すことができます。

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
`rtrim` メソッドは、指定された文字列の右側をトリミングします。

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
`scan` メソッドは、[`sscanf` PHP function](https://www.php.net/manual/en/function.sscanf.php) でサポートされている形式に従って、文字列からの入力を解析してコレクションに入れます。

```
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
<!-- #### `singular` -->
#### `singular`
<!-- The `singular` method converts a string to its singular form. This function currently only supports the English language: -->
`singular` メソッドは、文字列を単数形に変換します。この関数は現在英語のみをサポートしています。

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
`slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

```
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
<!-- #### `snake` -->
#### `snake`
<!-- The `snake` method converts the given string to `snake_case`: -->
`snake` メソッドは、指定された文字列を `snake_case` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
<!-- #### `split` -->
#### `split`
<!-- The `split` method splits a string into a collection using a regular expression: -->
`split` メソッドは、正規表現を使用して文字列をコレクションに分割します。

```
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-start"></a>
<!-- #### `start` -->
#### `start`
<!-- The `start` method adds a single instance of the given value to a string if it does not already start with that value: -->
`start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

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
`startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

<a name="method-fluent-str-studly"></a>
<!-- #### `studly` -->
#### `studly`
<!-- The `studly` method converts the given string to `StudlyCase`: -->
`studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
<!-- #### `substr` -->
#### `substr`
<!-- The `substr` method returns the portion of the string specified by the given start and length parameters: -->
`substr` メソッドは、指定された start パラメーターと length パラメーターで指定された文字列の部分を返します。

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
<!-- The `substrReplace` method replaces text within a portion of a string, starting at the position specified by the third argument and replacing the number of characters specified by the fourth argument. Passing `0` to the method's fourth argument will insert the string at the specified position without replacing any of the existing characters in the string: -->
`substrReplace` メソッドは、文字列の一部内のテキストを、3 番目の引数で指定された位置から開始して 4 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 4 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

```
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-tap"></a>
<!-- #### `tap` -->
#### `tap`
<!-- The `tap` method passes the string to the given closure, allowing you to examine and interact with the string while not affecting the string itself. The original string is returned by the `tap` method regardless of what is returned by the closure: -->
`tap` メソッドは文字列を指定されたクロージャに渡します。これにより、文字列自体には影響を与えずに、文字列を調べて操作できるようになります。クロージャによって何が返されるかに関係なく、元の文字列が `tap` メソッドによって返されます。

```
use Illuminate\Support\Str;

$string = Str::of('Laravel')
    ->append(' Framework')
    ->tap(function ($string) {
        dump('String after append: ' . $string);
    })
    ->upper();

// LARAVEL FRAMEWORK
```

<a name="method-fluent-str-test"></a>
<!-- #### `test` -->
#### `test`
<!-- The `test` method determines if a string matches the given regular expression pattern: -->
`test` メソッドは、文字列が指定された正規表現パターンに一致するかどうかを判断します。

```
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
<!-- #### `title` -->
#### `title`
<!-- The `title` method converts the given string to `Title Case`: -->
`title` メソッドは、指定された文字列を `Title Case` に変換します。

```
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-trim"></a>
<!-- #### `trim` -->
#### `trim`
<!-- The `trim` method trims the given string: -->
`trim` メソッドは、指定された文字列をトリミングします。

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
`ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

```
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-upper"></a>
<!-- #### `upper` -->
#### `upper`
<!-- The `upper` method converts the given string to uppercase: -->
`upper` メソッドは、指定された文字列を大文字に変換します。

```
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
<!-- #### `when` -->
#### `when`
<!-- The `when` method invokes the given closure if a given condition is `true`. The closure will receive the fluent string instance: -->
`when` メソッドは、指定された条件が `true` の場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```
use Illuminate\Support\Str;

$string = Str::of('Taylor')
                ->when(true, function ($string) {
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

```
use Illuminate\Support\Str;

$string = Str::of('tony stark')
            ->whenContains('tony', function ($string) {
                return $string->title();
            });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the string does not contain the given value. -->
必要に応じて、別のクロージャを 3 番目のパラメータとして `when` メソッドに渡すことができます。このクロージャは、文字列に指定された値が含まれていない場合に実行されます。

<!-- You may also pass an array of values to determine if the given string contains any of the values in the array: -->
値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

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
`whenContainsAll` メソッドは、文字列に指定されたサブ文字列がすべて含まれている場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```
use Illuminate\Support\Str;

$string = Str::of('tony stark')
                ->whenContainsAll(['tony', 'stark'], function ($string) {
                    return $string->title();
                });

// 'Tony Stark'
```

<!-- If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the condition parameter evaluates to `false`. -->
必要に応じて、別のクロージャを 3 番目のパラメータとして `when` メソッドに渡すことができます。このクロージャは、条件パラメータが `false` と評価された場合に実行されます。

<a name="method-fluent-str-when-empty"></a>
<!-- #### `whenEmpty` -->
#### `whenEmpty`
<!-- The `whenEmpty` method invokes the given closure if the string is empty. If the closure returns a value, that value will also be returned by the `whenEmpty` method. If the closure does not return a value, the fluent string instance will be returned: -->
`whenEmpty` メソッドは、文字列が空の場合、指定されたクロージャを呼び出します。クロージャが値を返す場合、その値は `whenEmpty` メソッドによっても返されます。クロージャが値を返さない場合は、流暢な文字列インスタンスが返されます。

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
文字列が空でない場合、`whenNotEmpty` メソッドは指定されたクロージャを呼び出します。クロージャが値を返す場合、その値は `whenNotEmpty` メソッドによっても返されます。クロージャが値を返さない場合は、流暢な文字列インスタンスが返されます。

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
`whenStartsWith` メソッドは、文字列が指定された部分文字列で始まる場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

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
`whenEndsWith` メソッドは、文字列が指定された部分文字列で終わる場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

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
`whenExactly` メソッドは、文字列が指定された文字列と正確に一致する場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```
use Illuminate\Support\Str;

$string = Str::of('laravel')->whenExactly('laravel', function ($string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is"></a>
<!-- #### `whenIs` -->
#### `whenIs`
<!-- The `whenIs` method invokes the given closure if the string matches a given pattern. Asterisks may be used as wildcard values. The closure will receive the fluent string instance: -->
`whenIs` メソッドは、文字列が指定されたパターンに一致する場合に、指定されたクロージャを呼び出します。アスタリスクはワイルドカード値として使用できます。クロージャは流暢な文字列インスタンスを受け取ります。

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
文字列が 7 ビット ASCII の場合、`whenIsAscii` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```
use Illuminate\Support\Str;

$string = Str::of('foo/bar')->whenIsAscii('laravel', function ($string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is-uuid"></a>
<!-- #### `whenIsUuid` -->
#### `whenIsUuid`
<!-- The `whenIsUuid` method invokes the given closure if the string is a valid UUID. The closure will receive the fluent string instance: -->
文字列が有効な UUID の場合、`whenIsUuid` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

```
use Illuminate\Support\Str;

$string = Str::of('foo/bar')->whenIsUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', function ($string) {
    return $string->substr(0, 8);
});

// 'a0a2a2d2'
```

<a name="method-fluent-str-when-test"></a>
<!-- #### `whenTest` -->
#### `whenTest`
<!-- The `whenTest` method invokes the given closure if the string matches the given regular expression. The closure will receive the fluent string instance: -->
`whenTest` メソッドは、文字列が指定された正規表現と一致する場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

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
`action` 関数は、指定されたコントローラ アクションの URL を生成します。

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the method accepts route parameters, you may pass them as the second argument to the method: -->
メソッドがルート パラメーターを受け入れる場合は、それらを 2 番目の引数としてメソッドに渡すことができます。

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
<!-- #### `asset()` -->
#### `asset()`
<!-- The `asset` function generates a URL for an asset using the current scheme of the request (HTTP or HTTPS): -->
`asset` 関数は、現在のリクエスト スキーム (HTTP または HTTPS) を使用してアセットの URL を生成します。

```
$url = asset('img/photo.jpg');
```

<!-- You can configure the asset URL host by setting the `ASSET_URL` variable in your `.env` file. This can be useful if you host your assets on an external service like Amazon S3 or another CDN: -->
`.env` ファイルで `ASSET_URL` 変数を設定することで、アセット URL ホストを構成できます。これは、Amazon S3 や別の CDN などの外部サービスでアセットをホストする場合に便利です。

```
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
<!-- #### `route()` -->
#### `route()`
<!-- The `route` function generates a URL for a given [named route](/docs/8.x/routing#named-routes): -->
`route` 関数は、指定された [named route](/docs/8.x/routing#named-routes) の URL を生成します。

```
$url = route('route.name');
```

<!-- If the route accepts parameters, you may pass them as the second argument to the function: -->
ルートがパラメーターを受け入れる場合は、それらを関数の 2 番目の引数として渡すことができます。

```
$url = route('route.name', ['id' => 1]);
```

<!-- By default, the `route` function generates an absolute URL. If you wish to generate a relative URL, you may pass `false` as the third argument to the function: -->
デフォルトでは、`route` 関数は絶対 URL を生成します。相対 URL を生成したい場合は、関数の 3 番目の引数として `false` を渡すことができます。

```
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
<!-- #### `secure_asset()` -->
#### `secure_asset()`
<!-- The `secure_asset` function generates a URL for an asset using HTTPS: -->
`secure_asset` 関数は、HTTPS を使用してアセットの URL を生成します。

```
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
<!-- #### `secure_url()` -->
#### `secure_url()`
<!-- The `secure_url` function generates a fully qualified HTTPS URL to the given path. Additional URL segments may be passed in the function's second argument: -->
`secure_url` 関数は、指定されたパスへの完全修飾 HTTPS URL を生成します。追加の URL セグメントを関数の 2 番目の引数に渡すことができます。

```
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-url"></a>
<!-- #### `url()` -->
#### `url()`
<!-- The `url` function generates a fully qualified URL to the given path: -->
`url` 関数は、指定されたパスへの完全修飾 URL を生成します。

```
$url = url('user/profile');

$url = url('user/profile', [1]);
```

<!-- If no path is provided, an `Illuminate\Routing\UrlGenerator` instance is returned: -->
パスが指定されていない場合は、`Illuminate\Routing\UrlGenerator` インスタンスが返されます。

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
<!-- The `abort` function throws [an HTTP exception](/docs/8.x/errors#http-exceptions) which will be rendered by the [exception handler](/docs/8.x/errors#the-exception-handler): -->
`abort` 関数は、[an HTTP exception](/docs/8.x/errors#http-exceptions) をスローし、これは [exception handler](/docs/8.x/errors#the-exception-handler) によってレンダリングされます。

```
abort(403);
```

<!-- You may also provide the exception's message and custom HTTP response headers that should be sent to the browser: -->
ブラウザに送信する例外のメッセージとカスタム HTTP 応答ヘッダーを指定することもできます。

```
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
<!-- #### `abort_if()` -->
#### `abort_if()`
<!-- The `abort_if` function throws an HTTP exception if a given boolean expression evaluates to `true`: -->
指定されたブール式が `true` と評価される場合、`abort_if` 関数は HTTP 例外をスローします。

```
abort_if(! Auth::user()->isAdmin(), 403);
```

<!-- Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function. -->
`abort` メソッドと同様に、関数の 3 番目の引数として例外の応答テキストを指定し、4 番目の引数としてカスタム応答ヘッダーの配列を指定することもできます。

<a name="method-abort-unless"></a>
<!-- #### `abort_unless()` -->
#### `abort_unless()`
<!-- The `abort_unless` function throws an HTTP exception if a given boolean expression evaluates to `false`: -->
指定されたブール式が `false` と評価される場合、`abort_unless` 関数は HTTP 例外をスローします。

```
abort_unless(Auth::user()->isAdmin(), 403);
```

<!-- Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function. -->
`abort` メソッドと同様に、関数の 3 番目の引数として例外の応答テキストを指定し、4 番目の引数としてカスタム応答ヘッダーの配列を指定することもできます。

<a name="method-app"></a>
<!-- #### `app()` -->
#### `app()`
<!-- The `app` function returns the [service container](/docs/8.x/container) instance: -->
`app` 関数は、[service container](/docs/8.x/container) インスタンスを返します。

```
$container = app();
```

<!-- You may pass a class or interface name to resolve it from the container: -->
クラス名またはインターフェース名を渡して、コンテナーから解決できます。

```
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
<!-- #### `auth()` -->
#### `auth()`
<!-- The `auth` function returns an [authenticator](/docs/8.x/authentication) instance. You may use it as an alternative to the `Auth` facade: -->
`auth` 関数は、[authenticator](/docs/8.x/authentication) インスタンスを返します。 `Auth` ファサードの代替として使用できます。

```
$user = auth()->user();
```

<!-- If needed, you may specify which guard instance you would like to access: -->
必要に応じて、アクセスするガード インスタンスを指定できます。

```
$user = auth('admin')->user();
```

<a name="method-back"></a>
<!-- #### `back()` -->
#### `back()`
<!-- The `back` function generates a [redirect HTTP response](/docs/8.x/responses#redirects) to the user's previous location: -->
`back` 関数は、ユーザーの以前の場所に [redirect HTTP response](/docs/8.x/responses#redirects) を生成します。

```
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
<!-- #### `bcrypt()` -->
#### `bcrypt()`
<!-- The `bcrypt` function [hashes](/docs/8.x/hashing) the given value using Bcrypt. You may use this function as an alternative to the `Hash` facade: -->
`bcrypt` 関数は、Bcrypt を使用して指定された値を[hashes](/docs/8.x/hashing)します。この関数は、`Hash` ファサードの代わりに使用できます。

```
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
<!-- #### `blank()` -->
#### `blank()`
<!-- The `blank` function determines whether the given value is "blank": -->
`blank` 関数は、指定された値が「空白」かどうかを判断します。

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
`blank` の逆については、[`filled`](#method-filled) メソッドを参照してください。

<a name="method-broadcast"></a>
<!-- #### `broadcast()` -->
#### `broadcast()`
<!-- The `broadcast` function [broadcasts](/docs/8.x/broadcasting) the given [event](/docs/8.x/events) to its listeners: -->
`broadcast` 関数 [broadcasts](/docs/8.x/broadcasting) は、指定された [event](/docs/8.x/events) をリスナに渡します。

```
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
<!-- #### `cache()` -->
#### `cache()`
<!-- The `cache` function may be used to get values from the [cache](/docs/8.x/cache). If the given key does not exist in the cache, an optional default value will be returned: -->
`cache` 関数を使用して、[cache](/docs/8.x/cache) から値を取得できます。指定されたキーがキャッシュに存在しない場合は、オプションのデフォルト値が返されます。

```
$value = cache('key');

$value = cache('key', 'default');
```

<!-- You may add items to the cache by passing an array of key / value pairs to the function. You should also pass the number of seconds or duration the cached value should be considered valid: -->
キーと値のペアの配列を関数に渡すことで、キャッシュに項目を追加できます。キャッシュされた値が有効であるとみなされる秒数または期間も渡す必要があります。

```
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
<!-- #### `class_uses_recursive()` -->
#### `class_uses_recursive()`
<!-- The `class_uses_recursive` function returns all traits used by a class, including traits used by all of its parent classes: -->
`class_uses_recursive` 関数は、そのすべての親クラスで使用される特性を含む、クラスで使用されるすべての特性を返します。

```
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
<!-- #### `collect()` -->
#### `collect()`
<!-- The `collect` function creates a [collection](/docs/8.x/collections) instance from the given value: -->
`collect` 関数は、指定された値から [collection](/docs/8.x/collections) インスタンスを作成します。

```
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
<!-- #### `config()` -->
#### `config()`
<!-- The `config` function gets the value of a [configuration](/docs/8.x/configuration) variable. The configuration values may be accessed using "dot" syntax, which includes the name of the file and the option you wish to access. A default value may be specified and is returned if the configuration option does not exist: -->
`config` 関数は、[configuration](/docs/8.x/configuration) 変数の値を取得します。設定値には、ファイル名とアクセスするオプションを含む「ドット」構文を使用してアクセスできます。デフォルト値を指定することができ、構成オプションが存在しない場合はデフォルト値が返されます。

```
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

<!-- You may set configuration variables at runtime by passing an array of key / value pairs. However, note that this function only affects the configuration value for the current request and does not update your actual configuration values: -->
キーと値のペアの配列を渡すことで、実行時に構成変数を設定できます。ただし、この関数は現在のリクエストの構成値にのみ影響し、実際の構成値は更新されないことに注意してください。

```
config(['app.debug' => true]);
```

<a name="method-cookie"></a>
<!-- #### `cookie()` -->
#### `cookie()`
<!-- The `cookie` function creates a new [cookie](/docs/8.x/requests#cookies) instance: -->
`cookie` 関数は、新しい [cookie](/docs/8.x/requests#cookies) インスタンスを作成します。

```
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
<!-- #### `csrf_field()` -->
#### `csrf_field()`
<!-- The `csrf_field` function generates an HTML `hidden` input field containing the value of the CSRF token. For example, using [Blade syntax](/docs/8.x/blade): -->
`csrf_field` 関数は、CSRF トークンの値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade syntax](/docs/8.x/blade) を使用すると、次のようになります。

```
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
<!-- #### `csrf_token()` -->
#### `csrf_token()`
<!-- The `csrf_token` function retrieves the value of the current CSRF token: -->
`csrf_token` 関数は、現在の CSRF トークンの値を取得します。

```
$token = csrf_token();
```

<a name="method-dd"></a>
<!-- #### `dd()` -->
#### `dd()`
<!-- The `dd` function dumps the given variables and ends execution of the script: -->
`dd` 関数は、指定された変数をダンプし、スクリプトの実行を終了します。

```
dd($value);

dd($value1, $value2, $value3, ...);
```

<!-- If you do not want to halt the execution of your script, use the [`dump`](#method-dump) function instead. -->
スクリプトの実行を停止したくない場合は、代わりに [`dump`](#method-dump) 関数を使用してください。

<a name="method-dispatch"></a>
<!-- #### `dispatch()` -->
#### `dispatch()`
<!-- The `dispatch` function pushes the given [job](/docs/8.x/queues#creating-jobs) onto the Laravel [job queue](/docs/8.x/queues): -->
`dispatch` 関数は、指定された [job](/docs/8.x/queues#creating-jobs) を Laravel [job queue](/docs/8.x/queues) にプッシュします。

```
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
<!-- #### `dump()` -->
#### `dump()`
<!-- The `dump` function dumps the given variables: -->
`dump` 関数は、指定された変数をダンプします。

```
dump($value);

dump($value1, $value2, $value3, ...);
```

<!-- If you want to stop executing the script after dumping the variables, use the [`dd`](#method-dd) function instead. -->
変数をダンプした後にスクリプトの実行を停止する場合は、代わりに [`dd`](#method-dd) 関数を使用します。

<a name="method-env"></a>
<!-- #### `env()` -->
#### `env()`
<!-- The `env` function retrieves the value of an [environment variable](/docs/8.x/configuration#environment-configuration) or returns a default value: -->
`env` 関数は、[environment variable](/docs/8.x/configuration#environment-configuration) の値を取得するか、デフォルト値を返します。

```
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!NOTE]
> デプロイ プロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされず、`env` 関数へのすべての呼び出しは `null` を返します。

<a name="method-event"></a>
<!-- #### `event()` -->
#### `event()`
<!-- The `event` function dispatches the given [event](/docs/8.x/events) to its listeners: -->
`event` 関数は、指定された [event](/docs/8.x/events) をリスナにディスパッチします。

```
event(new UserRegistered($user));
```

<a name="method-filled"></a>
<!-- #### `filled()` -->
#### `filled()`
<!-- The `filled` function determines whether the given value is not "blank": -->
`filled` 関数は、指定された値が「空白」でないかどうかを判断します。

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
`filled` の逆については、[`blank`](#method-blank) メソッドを参照してください。

<a name="method-info"></a>
<!-- #### `info()` -->
#### `info()`
<!-- The `info` function will write information to your application's [log](/docs/8.x/logging): -->
`info` 関数は、アプリケーションの [log](/docs/8.x/logging) に情報を書き込みます。

```
info('Some helpful information!');
```

<!-- An array of contextual data may also be passed to the function: -->
コンテキスト データの配列を関数に渡すこともできます。

```
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-logger"></a>
<!-- #### `logger()` -->
#### `logger()`
<!-- The `logger` function can be used to write a `debug` level message to the [log](/docs/8.x/logging): -->
`logger` 関数を使用して、`debug` レベルのメッセージを [log](/docs/8.x/logging) に書き込むことができます。

```
logger('Debug message');
```

<!-- An array of contextual data may also be passed to the function: -->
コンテキスト データの配列を関数に渡すこともできます。

```
logger('User has logged in.', ['id' => $user->id]);
```

<!-- A [logger](/docs/8.x/errors#logging) instance will be returned if no value is passed to the function: -->
関数に値が渡されない場合、[logger](/docs/8.x/errors#logging) インスタンスが返されます。

```
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
<!-- #### `method_field()` -->
#### `method_field()`
<!-- The `method_field` function generates an HTML `hidden` input field containing the spoofed value of the form's HTTP verb. For example, using [Blade syntax](/docs/8.x/blade): -->
`method_field` 関数は、フォームの HTTP 動詞の偽値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade syntax](/docs/8.x/blade) を使用すると、次のようになります。

```
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
<!-- #### `now()` -->
#### `now()`
<!-- The `now` function creates a new `Illuminate\Support\Carbon` instance for the current time: -->
`now` 関数は、現時点での新しい `Illuminate\Support\Carbon` インスタンスを作成します。

```
$now = now();
```

<a name="method-old"></a>
<!-- #### `old()` -->
#### `old()`
<!-- The `old` function [retrieves](/docs/8.x/requests#retrieving-input) an [old input](/docs/8.x/requests#old-input) value flashed into the session: -->
`old` 関数は、セッションにフラッシュされた[retrieves](/docs/8.x/requests#old-input)値を[old input](/docs/8.x/requests#retrieving-input)します。

```
$value = old('value');

$value = old('value', 'default');
```

<a name="method-optional"></a>
<!-- #### `optional()` -->
#### `optional()`
<!-- The `optional` function accepts any argument and allows you to access properties or call methods on that object. If the given object is `null`, properties and methods will return `null` instead of causing an error: -->
`optional` 関数は任意の引数を受け入れ、そのオブジェクトのプロパティにアクセスしたり、メソッドを呼び出したりすることができます。指定されたオブジェクトが `null` の場合、プロパティとメソッドはエラーを引き起こす代わりに `null` を返します。

```
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

<!-- The `optional` function also accepts a closure as its second argument. The closure will be invoked if the value provided as the first argument is not null: -->
`optional` 関数は、2 番目の引数としてクロージャも受け入れます。最初の引数として指定された値が null でない場合、クロージャが呼び出されます。

```
return optional(User::find($id), function ($user) {
    return $user->name;
});
```

<a name="method-policy"></a>
<!-- #### `policy()` -->
#### `policy()`
<!-- The `policy` method retrieves a [policy](/docs/8.x/authorization#creating-policies) instance for a given class: -->
`policy` メソッドは、指定されたクラスの [policy](/docs/8.x/authorization#creating-policies) インスタンスを取得します。

```
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
<!-- #### `redirect()` -->
#### `redirect()`
<!-- The `redirect` function returns a [redirect HTTP response](/docs/8.x/responses#redirects), or returns the redirector instance if called with no arguments: -->
`redirect` 関数は [redirect HTTP response](/docs/8.x/responses#redirects) を返すか、引数なしで呼び出された場合はリダイレクター インスタンスを返します。

```
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
<!-- #### `report()` -->
#### `report()`
<!-- The `report` function will report an exception using your [exception handler](/docs/8.x/errors#the-exception-handler): -->
`report` 関数は、[exception handler](/docs/8.x/errors#the-exception-handler) を使用して例外を報告します。

```
report($e);
```

<!-- The `report` function also accepts a string as an argument. When a string is given to the function, the function will create an exception with the given string as its message: -->
`report` 関数は、引数として文字列も受け入れます。文字列が関数に与えられると、関数は指定された文字列をメッセージとして持つ例外を作成します。

```
report('Something went wrong.');
```

<a name="method-request"></a>
<!-- #### `request()` -->
#### `request()`
<!-- The `request` function returns the current [request](/docs/8.x/requests) instance or obtains an input field's value from the current request: -->
`request` 関数は、現在の [request](/docs/8.x/requests) インスタンスを返すか、現在のリクエストから入力フィールドの値を取得します。

```
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
<!-- #### `rescue()` -->
#### `rescue()`
<!-- The `rescue` function executes the given closure and catches any exceptions that occur during its execution. All exceptions that are caught will be sent to your [exception handler](/docs/8.x/errors#the-exception-handler); however, the request will continue processing: -->
`rescue` 関数は、指定されたクロージャを実行し、その実行中に発生する例外をキャッチします。キャッチされた例外はすべて [exception handler](/docs/8.x/errors#the-exception-handler) に送信されます。ただし、リクエストは処理を続行します。

```
return rescue(function () {
    return $this->method();
});
```

<!-- You may also pass a second argument to the `rescue` function. This argument will be the "default" value that should be returned if an exception occurs while executing the closure: -->
`rescue` 関数に 2 番目の引数を渡すこともできます。この引数は、クロージャの実行中に例外が発生した場合に返される「デフォルト」値になります。

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
<!-- The `resolve` function resolves a given class or interface name to an instance using the [service container](/docs/8.x/container): -->
`resolve` 関数は、[service container](/docs/8.x/container) を使用して、指定されたクラスまたはインターフェイス名をインスタンスに解決します。

```
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
<!-- #### `response()` -->
#### `response()`
<!-- The `response` function creates a [response](/docs/8.x/responses) instance or obtains an instance of the response factory: -->
`response` 関数は、[response](/docs/8.x/responses) インスタンスを作成するか、応答ファクトリーのインスタンスを取得します。

```
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
<!-- #### `retry()` -->
#### `retry()`
<!-- The `retry` function attempts to execute the given callback until the given maximum attempt threshold is met. If the callback does not throw an exception, its return value will be returned. If the callback throws an exception, it will automatically be retried. If the maximum attempt count is exceeded, the exception will be thrown: -->
`retry` 関数は、指定された最大試行しきい値に達するまで、指定されたコールバックの実行を試行します。コールバックが例外をスローしない場合は、その戻り値が返されます。コールバックが例外をスローした場合、自動的に再試行されます。最大試行回数を超えると、例外がスローされます。

```
return retry(5, function () {
    // Attempt 5 times while resting 100ms in between attempts...
}, 100);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep in between attempts, you may pass a closure as the third argument to the `retry` function: -->
試行間のスリープ時間を手動で計算したい場合は、`retry` 関数の 3 番目の引数としてクロージャを渡すことができます。

```
return retry(5, function () {
    // ...
}, function ($attempt) {
    return $attempt * 100;
});
```


<!-- To only retry under specific conditions, you may pass a closure as the fourth argument to the `retry` function: -->
特定の条件下でのみ再試行するには、`retry` 関数の 4 番目の引数としてクロージャを渡すことができます。

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
<!-- The `session` function may be used to get or set [session](/docs/8.x/session) values: -->
`session` 関数は、[session](/docs/8.x/session) 値を取得または設定するために使用できます。

```
$value = session('key');
```

<!-- You may set values by passing an array of key / value pairs to the function: -->
キーと値のペアの配列を関数に渡すことで、値を設定できます。

```
session(['chairs' => 7, 'instruments' => 3]);
```

<!-- The session store will be returned if no value is passed to the function: -->
関数に値が渡されない場合、セッション ストアが返されます。

```
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
<!-- #### `tap()` -->
#### `tap()`
<!-- The `tap` function accepts two arguments: an arbitrary `$value` and a closure. The `$value` will be passed to the closure and then be returned by the `tap` function. The return value of the closure is irrelevant: -->
`tap` 関数は、任意の `$value` とクロージャの 2 つの引数を受け入れます。 `$value` はクロージャに渡され、`tap` 関数によって返されます。クロージャの戻り値は無関係です。

```
$user = tap(User::first(), function ($user) {
    $user->name = 'taylor';

    $user->save();
});
```

<!-- If no closure is passed to the `tap` function, you may call any method on the given `$value`. The return value of the method you call will always be `$value`, regardless of what the method actually returns in its definition. For example, the Eloquent `update` method typically returns an integer. However, we can force the method to return the model itself by chaining the `update` method call through the `tap` function: -->
クロージャーが `tap` 関数に渡されない場合は、指定された `$value` で任意のメソッドを呼び出すことができます。呼び出したメソッドの戻り値は、メソッドがその定義で実際に何を返すかに関係なく、常に `$value` になります。たとえば、Eloquent `update` メソッドは通常、整数を返します。ただし、`tap` 関数を介して `update` メソッド呼び出しを連鎖させることで、メソッドがモデル自体を返すように強制できます。

```
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

<!-- To add a `tap` method to a class, you may add the `Illuminate\Support\Traits\Tappable` trait to the class. The `tap` method of this trait accepts a Closure as its only argument. The object instance itself will be passed to the Closure and then be returned by the `tap` method: -->
`tap` メソッドをクラスに追加するには、`Illuminate\Support\Traits\Tappable` 特性をクラスに追加します。このトレイトの `tap` メソッドは、唯一の引数として Closure を受け入れます。オブジェクト インスタンス自体はクロージャに渡され、`tap` メソッドによって返されます。

```
return $user->tap(function ($user) {
    //
});
```

<a name="method-throw-if"></a>
<!-- #### `throw_if()` -->
#### `throw_if()`
<!-- The `throw_if` function throws the given exception if a given boolean expression evaluates to `true`: -->
指定されたブール式が `true` と評価される場合、`throw_if` 関数は指定された例外をスローします。

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
指定されたブール式が `false` と評価される場合、`throw_unless` 関数は指定された例外をスローします。

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
`today` 関数は、現在の日付の新しい `Illuminate\Support\Carbon` インスタンスを作成します。

```
$today = today();
```

<a name="method-trait-uses-recursive"></a>
<!-- #### `trait_uses_recursive()` -->
#### `trait_uses_recursive()`
<!-- The `trait_uses_recursive` function returns all traits used by a trait: -->
`trait_uses_recursive` 関数は、特性によって使用されるすべての特性を返します。

```
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
<!-- #### `transform()` -->
#### `transform()`
<!-- The `transform` function executes a closure on a given value if the value is not [blank](#method-blank) and then returns the return value of the closure: -->
`transform` 関数は、値が [blank](#method-blank) でない場合、指定された値に対してクロージャを実行し、クロージャの戻り値を返します。

```
$callback = function ($value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

<!-- A default value or closure may be passed as the third argument to the function. This value will be returned if the given value is blank: -->
デフォルト値またはクロージャは、関数の 3 番目の引数として渡すことができます。指定された値が空白の場合、この値が返されます。

```
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
<!-- #### `validator()` -->
#### `validator()`
<!-- The `validator` function creates a new [validator](/docs/8.x/validation) instance with the given arguments. You may use it as an alternative to the `Validator` facade: -->
`validator` 関数は、指定された引数を使用して新しい [validator](/docs/8.x/validation) インスタンスを作成します。 `Validator` ファサードの代替として使用できます。

```
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
<!-- #### `value()` -->
#### `value()`
<!-- The `value` function returns the value it is given. However, if you pass a closure to the function, the closure will be executed and its returned value will be returned: -->
`value` 関数は、指定された値を返します。ただし、関数にクロージャを渡すと、クロージャが実行され、その戻り値が返されます。

```
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

<a name="method-view"></a>
<!-- #### `view()` -->
#### `view()`
<!-- The `view` function retrieves a [view](/docs/8.x/views) instance: -->
`view` 関数は、[view](/docs/8.x/views) インスタンスを取得します。

```
return view('auth.login');
```

<a name="method-with"></a>
<!-- #### `with()` -->
#### `with()`
<!-- The `with` function returns the value it is given. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned: -->
`with` 関数は、指定された値を返します。クロージャが関数の 2 番目の引数として渡されると、クロージャが実行され、その戻り値が返されます。

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

