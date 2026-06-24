<!-- # Helpers -->
# Helpers

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Other Utilities](#other-utilities)
    - [Benchmarking](#benchmarking)
    - [Dates](#dates)
    - [Deferred Functions](#deferred-functions)
    - [Lottery](#lottery)
    - [Pipeline](#pipeline)
    - [Sleep](#sleep)
    - [Timebox](#timebox)

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
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::mapSpread](#method-array-map-spread)
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::take](#method-array-take)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::toCssStyles](#method-array-to-css-styles)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[data_forget](#method-data-forget)
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
[Arr::mapSpread](#method-array-map-spread)
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::take](#method-array-take)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::toCssStyles](#method-array-to-css-styles)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[data_forget](#method-data-forget)
[head](#method-head)
[last](#method-last)
</div>

<a name="numbers-method-list"></a>
<!-- ### Numbers -->
### Numbers

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Number::abbreviate](#method-number-abbreviate)
[Number::clamp](#method-number-clamp)
[Number::currency](#method-number-currency)
[Number::defaultCurrency](#method-default-currency)
[Number::defaultLocale](#method-default-locale)
[Number::fileSize](#method-number-file-size)
[Number::forHumans](#method-number-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::pairs](#method-number-pairs)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
[Number::trim](#method-number-trim)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)
[Number::useCurrency](#method-number-use-currency)
[Number::withCurrency](#method-number-with-currency)
-->
[Number::abbreviate](#method-number-abbreviate)
[Number::clamp](#method-number-clamp)
[Number::currency](#method-number-currency)
[Number::defaultCurrency](#method-default-currency)
[Number::defaultLocale](#method-default-locale)
[Number::fileSize](#method-number-file-size)
[Number::forHumans](#method-number-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::pairs](#method-number-pairs)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
[Number::trim](#method-number-trim)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)
[Number::useCurrency](#method-number-use-currency)
[Number::withCurrency](#method-number-with-currency)

<!-- </div> -->
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
[context](#method-context)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dispatch_sync](#method-dispatch-sync)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[literal](#method-literal)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[once](#method-once)
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
[when](#method-when)
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
[context](#method-context)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dispatch_sync](#method-dispatch-sync)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[literal](#method-literal)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[once](#method-once)
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
[when](#method-when)

<!-- </div> -->
</div>

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

$first = Arr::first($array, function (int $value, int $key) {
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
<!-- The `Arr::isAssoc` method returns `true` if the given array is an associative array. An array is considered "associative" if it doesn't have sequential numerical keys beginning with zero: -->
指定された配列が連想配列の場合、`Arr::isAssoc` メソッドは `true` を返します。配列にゼロで始まる連続した数値キーがない場合、その配列は「結合」とみなされます。

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
指定された配列のキーがゼロから始まる連続した整数の場合、`Arr::isList` メソッドは `true` を返します。

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
`Arr::join` メソッドは、配列要素を文字列と結合します。このメソッドの 2 番目の引数を使用して、配列の最後の要素の結合文字列を指定することもできます。

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
`Arr::keyBy` メソッドは、指定されたキーによって配列にキーを設定します。複数の項目が同じキーを持つ場合、最後の項目だけが新しい配列に表示されます。

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
`Arr::last` メソッドは、指定された真理値テストに合格した配列の最後の要素を返します。

```
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
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

<a name="method-array-map"></a>
<!-- #### `Arr::map()` -->
#### `Arr::map()`
<!-- The `Arr::map` method iterates through the array and passes each value and key to the given callback. The array value is replaced by the value returned by the callback: -->
`Arr::map` メソッドは配列を反復処理し、各値とキーを指定されたコールバックに渡します。配列の値は、コールバックによって返される値に置き換えられます。

```
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function (string $value, string $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
```

<a name="method-array-map-spread"></a>
<!-- #### `Arr::mapSpread()` -->
#### `Arr::mapSpread()`
<!-- The `Arr::mapSpread` method iterates over the array, passing each nested item value into the given closure. The closure is free to modify the item and return it, thus forming a new array of modified items: -->
`Arr::mapSpread` メソッドは配列を反復処理し、ネストされた各項目の値を指定されたクロージャに渡します。クロージャは自由に項目を変更して返すことができるため、変更された項目の新しい配列が形成されます。

```
use Illuminate\Support\Arr;

$array = [
    [0, 1],
    [2, 3],
    [4, 5],
    [6, 7],
    [8, 9],
];

$mapped = Arr::mapSpread($array, function (int $even, int $odd) {
    return $even + $odd;
});

/*
    [1, 5, 9, 13, 17]
*/
```

<a name="method-array-map-with-keys"></a>
<!-- #### `Arr::mapWithKeys()` -->
#### `Arr::mapWithKeys()`
<!-- The `Arr::mapWithKeys` method iterates through the array and passes each value to the given callback. The callback should return an associative array containing a single key / value pair: -->
`Arr::mapWithKeys` メソッドは配列を反復処理し、各値を指定されたコールバックに渡します。コールバックは、単一のキーと値のペアを含む連想配列を返す必要があります。

```
use Illuminate\Support\Arr;

$array = [
    [
        'name' => 'John',
        'department' => 'Sales',
        'email' => 'john@example.com',
    ],
    [
        'name' => 'Jane',
        'department' => 'Marketing',
        'email' => 'jane@example.com',
    ]
];

$mapped = Arr::mapWithKeys($array, function (array $item, int $key) {
    return [$item['email'] => $item['name']];
});

/*
    [
        'john@example.com' => 'John',
        'jane@example.com' => 'Jane',
    ]
*/
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

<a name="method-array-prependkeyswith"></a>
<!-- #### `Arr::prependKeysWith()` -->
#### `Arr::prependKeysWith()`
<!-- The `Arr::prependKeysWith` prepends all key names of an associative array with the given prefix: -->
`Arr::prependKeysWith` は、連想配列のすべてのキー名の前に指定されたプレフィックスを付加します。

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

<a name="method-array-reject"></a>
<!-- #### `Arr::reject()` -->
#### `Arr::reject()`
<!-- The `Arr::reject` method removes items from an array using the given closure: -->
`Arr::reject` メソッドは、指定されたクロージャを使用して配列から項目を削除します。

```
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::reject($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [0 => 100, 2 => 300, 4 => 500]
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

$sorted = array_values(Arr::sort($array, function (array $value) {
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
`Arr::sortDesc` メソッドは、配列を値の降順に並べ替えます。

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
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

$sorted = array_values(Arr::sortDesc($array, function (array $value) {
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

<!-- If you would like the results sorted in descending order, you may use the `Arr::sortRecursiveDesc` method. -->
結果を降順に並べ替えたい場合は、`Arr::sortRecursiveDesc` メソッドを使用できます。

```
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-take"></a>
<!-- #### `Arr::take()` -->
#### `Arr::take()`
<!-- The `Arr::take` method returns a new array with the specified number of items: -->
`Arr::take` メソッドは、指定された項目数を含む新しい配列を返します。

```
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

<!-- You may also pass a negative integer to take the specified number of items from the end of the array: -->
負の整数を渡して、配列の末尾から指定した数の項目を取得することもできます。

```
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
<!-- #### `Arr::toCssClasses()` -->
#### `Arr::toCssClasses()`
<!-- The `Arr::toCssClasses` method conditionally compiles a CSS class string. The method accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`Arr::toCssClasses` メソッドは、CSS クラス文字列を条件付きでコンパイルします。このメソッドはクラスの配列を受け入れます。配列キーには追加するクラスが含まれ、値はブール式です。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

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

<a name="method-array-to-css-styles"></a>
<!-- #### `Arr::toCssStyles()` -->
#### `Arr::toCssStyles()`
<!-- The `Arr::toCssStyles` conditionally compiles a CSS style string. The method accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`Arr::toCssStyles` は、条件付きで CSS スタイル文字列をコンパイルします。このメソッドはクラスの配列を受け入れます。配列キーには追加するクラスが含まれ、値はブール式です。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

<!-- This method powers Laravel's functionality allowing [merging classes with a Blade component's attribute bag](/docs/11.x/blade#conditionally-merge-classes) as well as the `@class` [Blade directive](/docs/11.x/blade#conditional-classes). -->
このメソッドは、Laravel の機能を強化し、[merging classes with a Blade component's attribute bag](/docs/11.x/blade#conditionally-merge-classes) および `@class` [Blade directive](/docs/11.x/blade#conditional-classes) を許可します。

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

$filtered = Arr::where($array, function (string|int $value, int $key) {
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

<!-- The `{first}` and `{last}` placeholders may be used to retrieve the first or last items in an array: -->
`{first}` および `{last}` プレースホルダーは、配列内の最初または最後の項目を取得するために使用できます。

```
$flight = [
    'segments' => [
        ['from' => 'LHR', 'departure' => '9:00', 'to' => 'IST', 'arrival' => '15:00'],
        ['from' => 'IST', 'departure' => '16:00', 'to' => 'PKX', 'arrival' => '20:00'],
    ],
];

data_get($flight, 'segments.{first}.arrival');

// 15:00
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

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
<!-- #### `data_forget()` -->
#### `data_forget()`
<!-- The `data_forget` function removes a value within a nested array or object using "dot" notation: -->
`data_forget` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の値を削除します。

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

<!-- This function also accepts wildcards using asterisks and will remove values on the target accordingly: -->
この関数はアスタリスクを使用したワイルドカードも受け入れ、それに応じてターゲットの値を削除します。

```
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2', 'price' => 150],
    ],
];

data_forget($data, 'products.*.price');

/*
    [
        'products' => [
            ['name' => 'Desk 1'],
            ['name' => 'Desk 2'],
        ],
    ]
*/
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

<a name="numbers"></a>
<!-- ## Numbers -->
## Numbers

<a name="method-number-abbreviate"></a>
<!-- #### `Number::abbreviate()` -->
#### `Number::abbreviate()`
<!-- The `Number::abbreviate` method returns the human-readable format of the provided numerical value, with an abbreviation for the units: -->
`Number::abbreviate` メソッドは、単位の略語を付けて、指定された数値を人間が判読できる形式で返します。

```
use Illuminate\Support\Number;

$number = Number::abbreviate(1000);

// 1K

$number = Number::abbreviate(489939);

// 490K

$number = Number::abbreviate(1230000, precision: 2);

// 1.23M
```

<a name="method-number-clamp"></a>
<!-- #### `Number::clamp()` -->
#### `Number::clamp()`
<!-- The `Number::clamp` method ensures a given number stays within a specified range. If the number is lower than the minimum, the minimum value is returned. If the number is higher than the maximum, the maximum value is returned: -->
`Number::clamp` メソッドは、指定された数値が指定された範囲内に収まることを保証します。数値が最小値より小さい場合は、最小値が返されます。数値が最大値より大きい場合は、最大値が返されます。

```
use Illuminate\Support\Number;

$number = Number::clamp(105, min: 10, max: 100);

// 100

$number = Number::clamp(5, min: 10, max: 100);

// 10

$number = Number::clamp(10, min: 10, max: 100);

// 10

$number = Number::clamp(20, min: 10, max: 100);

// 20
```

<a name="method-number-currency"></a>
<!-- #### `Number::currency()` -->
#### `Number::currency()`
<!-- The `Number::currency` method returns the currency representation of the given value as a string: -->
`Number::currency` メソッドは、指定された値の通貨表現を文字列として返します。

```
use Illuminate\Support\Number;

$currency = Number::currency(1000);

// $1,000.00

$currency = Number::currency(1000, in: 'EUR');

// €1,000.00

$currency = Number::currency(1000, in: 'EUR', locale: 'de');

// 1.000,00 €
```

<a name="method-default-currency"></a>
<!-- #### `Number::defaultCurrency()` -->
#### `Number::defaultCurrency()`
<!-- The `Number::defaultCurrency` method returns the default currency being used by the `Number` class: -->
`Number::defaultCurrency` メソッドは、`Number` クラスで使用されるデフォルトの通貨を返します。

```
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
<!-- #### `Number::defaultLocale()` -->
#### `Number::defaultLocale()`
<!-- The `Number::defaultLocale` method returns the default locale being used by the `Number` class: -->
`Number::defaultLocale` メソッドは、`Number` クラスで使用されるデフォルトのロケールを返します。

```
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
<!-- #### `Number::fileSize()` -->
#### `Number::fileSize()`
<!-- The `Number::fileSize` method returns the file size representation of the given byte value as a string: -->
`Number::fileSize` メソッドは、指定されたバイト値のファイル サイズ表現を文字列として返します。

```
use Illuminate\Support\Number;

$size = Number::fileSize(1024);

// 1 KB

$size = Number::fileSize(1024 * 1024);

// 1 MB

$size = Number::fileSize(1024, precision: 2);

// 1.00 KB
```

<a name="method-number-for-humans"></a>
<!-- #### `Number::forHumans()` -->
#### `Number::forHumans()`
<!-- The `Number::forHumans` method returns the human-readable format of the provided numerical value: -->
`Number::forHumans` メソッドは、指定された数値を人間が判読できる形式で返します。

```
use Illuminate\Support\Number;

$number = Number::forHumans(1000);

// 1 thousand

$number = Number::forHumans(489939);

// 490 thousand

$number = Number::forHumans(1230000, precision: 2);

// 1.23 million
```

<a name="method-number-format"></a>
<!-- #### `Number::format()` -->
#### `Number::format()`
<!-- The `Number::format` method formats the given number into a locale specific string: -->
`Number::format` メソッドは、指定された数値をロケール固有の文字列にフォーマットします。

```
use Illuminate\Support\Number;

$number = Number::format(100000);

// 100,000

$number = Number::format(100000, precision: 2);

// 100,000.00

$number = Number::format(100000.123, maxPrecision: 2);

// 100,000.12

$number = Number::format(100000, locale: 'de');

// 100.000
```

<a name="method-number-ordinal"></a>
<!-- #### `Number::ordinal()` -->
#### `Number::ordinal()`
<!-- The `Number::ordinal` method returns a number's ordinal representation: -->
`Number::ordinal` メソッドは、数値の序数表現を返します。

```
use Illuminate\Support\Number;

$number = Number::ordinal(1);

// 1st

$number = Number::ordinal(2);

// 2nd

$number = Number::ordinal(21);

// 21st
```

<a name="method-number-pairs"></a>
<!-- #### `Number::pairs()` -->
#### `Number::pairs()`
<!-- The `Number::pairs` method generates an array of number pairs (sub-ranges) based on a specified range and step value. This method can be useful for dividing a larger range of numbers into smaller, manageable sub-ranges for things like pagination or batching tasks. The `pairs` method returns an array of arrays, where each inner array represents a pair (sub-range) of numbers: -->
`Number::pairs` メソッドは、指定された範囲とステップ値に基づいて数値ペア (サブ範囲) の配列を生成します。この方法は、ページネーションやタスクのバッチ処理などで、大きな範囲の数値を管理しやすい小さなサブ範囲に分割する場合に役立ちます。 `pairs` メソッドは配列の配列を返します。各内部配列は数値のペア (サブ範囲) を表します。

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[1, 10], [11, 20], [21, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-percentage"></a>
<!-- #### `Number::percentage()` -->
#### `Number::percentage()`
<!-- The `Number::percentage` method returns the percentage representation of the given value as a string: -->
`Number::percentage` メソッドは、指定された値のパーセント表現を文字列として返します。

```
use Illuminate\Support\Number;

$percentage = Number::percentage(10);

// 10%

$percentage = Number::percentage(10, precision: 2);

// 10.00%

$percentage = Number::percentage(10.123, maxPrecision: 2);

// 10.12%

$percentage = Number::percentage(10, precision: 2, locale: 'de');

// 10,00%
```

<a name="method-number-spell"></a>
<!-- #### `Number::spell()` -->
#### `Number::spell()`
<!-- The `Number::spell` method transforms the given number into a string of words: -->
`Number::spell` メソッドは、指定された数値を単語の文字列に変換します。

```
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

<!-- The `after` argument allows you to specify a value after which all numbers should be spelled out: -->
`after` 引数を使用すると、すべての数値の後に続く値を指定できます。

```
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

<!-- The `until` argument allows you to specify a value before which all numbers should be spelled out: -->
`until` 引数を使用すると、すべての数値の前にスペルアウトする必要がある値を指定できます。

```
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-trim"></a>
<!-- #### `Number::trim()` -->
#### `Number::trim()`
<!-- The `Number::trim` method removes any trailing zero digits after the decimal point of the given number: -->
`Number::trim` メソッドは、指定された数値の小数点以下の末尾のゼロの数字を削除します。

```
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
<!-- #### `Number::useLocale()` -->
#### `Number::useLocale()`
<!-- The `Number::useLocale` method sets the default number locale globally, which affects how numbers and currency are formatted by subsequent invocations to the `Number` class's methods: -->
`Number::useLocale` メソッドは、デフォルトの数値ロケールをグローバルに設定します。これは、`Number` クラスのメソッドの後続の呼び出しによって数値と通貨がどのようにフォーマットされるかに影響します。

```
use Illuminate\Support\Number;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Number::useLocale('de');
}
```

<a name="method-number-with-locale"></a>
<!-- #### `Number::withLocale()` -->
#### `Number::withLocale()`
<!-- The `Number::withLocale` method executes the given closure using the specified locale and then restores the original locale after the callback has executed: -->
`Number::withLocale` メソッドは、指定されたロケールを使用して指定されたクロージャを実行し、コールバックの実行後に元のロケールを復元します。

```
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
<!-- #### `Number::useCurrency()` -->
#### `Number::useCurrency()`
<!-- The `Number::useCurrency` method sets the default number currency globally, which affects how the currency is formatted by subsequent invocations to the `Number` class's methods: -->
`Number::useCurrency` メソッドは、デフォルトの数値通貨をグローバルに設定します。これは、その後の `Number` クラスのメソッドの呼び出しによって通貨がどのようにフォーマットされるかに影響します。

```
use Illuminate\Support\Number;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Number::useCurrency('GBP');
}
```

<a name="method-number-with-currency"></a>
<!-- #### `Number::withCurrency()` -->
#### `Number::withCurrency()`
<!-- The `Number::withCurrency` method executes the given closure using the specified currency and then restores the original currency after the callback has executed: -->
`Number::withCurrency` メソッドは、指定された通貨を使用して指定されたクロージャを実行し、コールバックの実行後に元の通貨を復元します。

```
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
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

<a name="method-lang-path"></a>
<!-- #### `lang_path()` -->
#### `lang_path()`
<!-- The `lang_path` function returns the fully qualified path to your application's `lang` directory. You may also use the `lang_path` function to generate a fully qualified path to a given file within the directory: -->
`lang_path` 関数は、アプリケーションの `lang` ディレクトリへの完全修飾パスを返します。 `lang_path` 関数を使用して、ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

<a name="method-mix"></a>
<!-- #### `mix()` -->
#### `mix()`
<!-- The `mix` function returns the path to a [versioned Mix file](/docs/11.x/mix): -->
`mix` 関数は、[versioned Mix file](/docs/11.x/mix) へのパスを返します。

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
<!-- The `route` function generates a URL for a given [named route](/docs/11.x/routing#named-routes): -->
`route` 関数は、指定された [named route](/docs/11.x/routing#named-routes) の URL を生成します。

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

<a name="method-to-route"></a>
<!-- #### `to_route()` -->
#### `to_route()`
<!-- The `to_route` function generates a [redirect HTTP response](/docs/11.x/responses#redirects) for a given [named route](/docs/11.x/routing#named-routes): -->
`to_route` 関数は、指定された [redirect HTTP response](/docs/11.x/routing#named-routes) への [named route](/docs/11.x/responses#redirects) を生成します。

```
return to_route('users.show', ['user' => 1]);
```

<!-- If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the `to_route` method: -->
必要に応じて、リダイレクトに割り当てる必要がある HTTP ステータス コードと追加の応答ヘッダーを `to_route` メソッドの 3 番目と 4 番目の引数として渡すことができます。

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
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
<!-- The `abort` function throws [an HTTP exception](/docs/11.x/errors#http-exceptions) which will be rendered by the [exception handler](/docs/11.x/errors#handling-exceptions): -->
`abort` 関数は、[an HTTP exception](/docs/11.x/errors#http-exceptions) をスローし、これは [exception handler](/docs/11.x/errors#handling-exceptions) によってレンダリングされます。

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
<!-- The `app` function returns the [service container](/docs/11.x/container) instance: -->
`app` 関数は、[service container](/docs/11.x/container) インスタンスを返します。

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
<!-- The `auth` function returns an [authenticator](/docs/11.x/authentication) instance. You may use it as an alternative to the `Auth` facade: -->
`auth` 関数は、[authenticator](/docs/11.x/authentication) インスタンスを返します。 `Auth` ファサードの代替として使用できます。

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
<!-- The `back` function generates a [redirect HTTP response](/docs/11.x/responses#redirects) to the user's previous location: -->
`back` 関数は、ユーザーの以前の場所に [redirect HTTP response](/docs/11.x/responses#redirects) を生成します。

```
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
<!-- #### `bcrypt()` -->
#### `bcrypt()`
<!-- The `bcrypt` function [hashes](/docs/11.x/hashing) the given value using Bcrypt. You may use this function as an alternative to the `Hash` facade: -->
`bcrypt` 関数は、Bcrypt を使用して指定された値を[hashes](/docs/11.x/hashing)します。この関数は、`Hash` ファサードの代わりに使用できます。

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
<!-- The `broadcast` function [broadcasts](/docs/11.x/broadcasting) the given [event](/docs/11.x/events) to its listeners: -->
`broadcast` 関数 [broadcasts](/docs/11.x/broadcasting) は、指定された [event](/docs/11.x/events) をリスナに渡します。

```
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
<!-- #### `cache()` -->
#### `cache()`
<!-- The `cache` function may be used to get values from the [cache](/docs/11.x/cache). If the given key does not exist in the cache, an optional default value will be returned: -->
`cache` 関数を使用して、[cache](/docs/11.x/cache) から値を取得できます。指定されたキーがキャッシュに存在しない場合は、オプションのデフォルト値が返されます。

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
<!-- The `collect` function creates a [collection](/docs/11.x/collections) instance from the given value: -->
`collect` 関数は、指定された値から [collection](/docs/11.x/collections) インスタンスを作成します。

```
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
<!-- #### `config()` -->
#### `config()`
<!-- The `config` function gets the value of a [configuration](/docs/11.x/configuration) variable. The configuration values may be accessed using "dot" syntax, which includes the name of the file and the option you wish to access. A default value may be specified and is returned if the configuration option does not exist: -->
`config` 関数は、[configuration](/docs/11.x/configuration) 変数の値を取得します。設定値には、ファイル名とアクセスするオプションを含む「ドット」構文を使用してアクセスできます。デフォルト値を指定することができ、構成オプションが存在しない場合はデフォルト値が返されます。

```
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

<!-- You may set configuration variables at runtime by passing an array of key / value pairs. However, note that this function only affects the configuration value for the current request and does not update your actual configuration values: -->
キーと値のペアの配列を渡すことで、実行時に構成変数を設定できます。ただし、この関数は現在のリクエストの構成値にのみ影響し、実際の構成値は更新されないことに注意してください。

```
config(['app.debug' => true]);
```

<a name="method-context"></a>
<!-- #### `context()` -->
#### `context()`
<!-- The `context` function gets the value from the [current context](/docs/11.x/context). A default value may be specified and is returned if the context key does not exist: -->
`context` 関数は、[current context](/docs/11.x/context) から値を取得します。デフォルト値を指定することができ、コンテキスト キーが存在しない場合はデフォルト値が返されます。

```
$value = context('trace_id');

$value = context('trace_id', $default);
```

<!-- You may set context values by passing an array of key / value pairs: -->
キーと値のペアの配列を渡すことでコンテキスト値を設定できます。

```
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
<!-- #### `cookie()` -->
#### `cookie()`
<!-- The `cookie` function creates a new [cookie](/docs/11.x/requests#cookies) instance: -->
`cookie` 関数は、新しい [cookie](/docs/11.x/requests#cookies) インスタンスを作成します。

```
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
<!-- #### `csrf_field()` -->
#### `csrf_field()`
<!-- The `csrf_field` function generates an HTML `hidden` input field containing the value of the CSRF token. For example, using [Blade syntax](/docs/11.x/blade): -->
`csrf_field` 関数は、CSRF トークンの値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade syntax](/docs/11.x/blade) を使用すると、次のようになります。

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

<a name="method-decrypt"></a>
<!-- #### `decrypt()` -->
#### `decrypt()`
<!-- The `decrypt` function [decrypts](/docs/11.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade: -->
`decrypt` 関数は、指定された値を[decrypts](/docs/11.x/encryption)します。この関数は、`Crypt` ファサードの代わりに使用できます。

```
$password = decrypt($value);
```

<a name="method-dd"></a>
<!-- #### `dd()` -->
#### `dd()`
<!-- The `dd` function dumps the given variables and ends the execution of the script: -->
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
<!-- The `dispatch` function pushes the given [job](/docs/11.x/queues#creating-jobs) onto the Laravel [job queue](/docs/11.x/queues): -->
`dispatch` 関数は、指定された [job](/docs/11.x/queues#creating-jobs) を Laravel [job queue](/docs/11.x/queues) にプッシュします。

```
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
<!-- #### `dispatch_sync()` -->
#### `dispatch_sync()`
<!-- The `dispatch_sync` function pushes the given job to the [sync](/docs/11.x/queues#synchronous-dispatching) queue so that it is processed immediately: -->
`dispatch_sync` 関数は、指定されたジョブを [sync](/docs/11.x/queues#synchronous-dispatching) キューにプッシュして、すぐに処理されるようにします。

```
dispatch_sync(new App\Jobs\SendEmails);
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

<a name="method-encrypt"></a>
<!-- #### `encrypt()` -->
#### `encrypt()`
<!-- The `encrypt` function [encrypts](/docs/11.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade: -->
`encrypt` 関数は、指定された値を[encrypts](/docs/11.x/encryption)します。この関数は、`Crypt` ファサードの代わりに使用できます。

```
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
<!-- #### `env()` -->
#### `env()`
<!-- The `env` function retrieves the value of an [environment variable](/docs/11.x/configuration#environment-configuration) or returns a default value: -->
`env` 関数は、[environment variable](/docs/11.x/configuration#environment-configuration) の値を取得するか、デフォルト値を返します。

```
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされず、`env` 関数へのすべての呼び出しは `null` を返します。

<a name="method-event"></a>
<!-- #### `event()` -->
#### `event()`
<!-- The `event` function dispatches the given [event](/docs/11.x/events) to its listeners: -->
`event` 関数は、指定された [event](/docs/11.x/events) をリスナにディスパッチします。

```
event(new UserRegistered($user));
```

<a name="method-fake"></a>
<!-- #### `fake()` -->
#### `fake()`
<!-- The `fake` function resolves a [Faker](https://github.com/FakerPHP/Faker) singleton from the container, which can be useful when creating fake data in model factories, database seeding, tests, and prototyping views: -->
`fake` 関数は、コンテナーから [Faker](https://github.com/FakerPHP/Faker) シングルトンを解決します。これは、モデル ファクトリ、データベース シーディング、テスト、およびプロトタイピング ビューで偽のデータを作成するときに役立ちます。

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

<!-- By default, the `fake` function will utilize the `app.faker_locale` configuration option in your `config/app.php` configuration. Typically, this configuration option is set via the `APP_FAKER_LOCALE` environment variable. You may also specify the locale by passing it to the `fake` function. Each locale will resolve an individual singleton: -->
デフォルトでは、`fake` 関数は、`config/app.php` 構成の `app.faker_locale` 構成オプションを利用します。通常、この構成オプションは `APP_FAKER_LOCALE` 環境変数を介して設定されます。ロケールを `fake` 関数に渡して指定することもできます。各ロケールは個別のシングルトンを解決します。

```
fake('nl_NL')->name()
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
<!-- The `info` function will write information to your application's [log](/docs/11.x/logging): -->
`info` 関数は、アプリケーションの [log](/docs/11.x/logging) に情報を書き込みます。

```
info('Some helpful information!');
```

<!-- An array of contextual data may also be passed to the function: -->
コンテキスト データの配列を関数に渡すこともできます。

```
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
<!-- #### `literal()` -->
#### `literal()`
<!-- The `literal` function creates a new [stdClass](https://www.php.net/manual/en/class.stdclass.php) instance with the given named arguments as properties: -->
`literal` 関数は、指定された名前付き引数をプロパティとして使用して、新しい [stdClass](https://www.php.net/manual/en/class.stdclass.php) インスタンスを作成します。

```
$obj = literal(
    name: 'Joe',
    languages: ['PHP', 'Ruby'],
);

$obj->name; // 'Joe'
$obj->languages; // ['PHP', 'Ruby']
```

<a name="method-logger"></a>
<!-- #### `logger()` -->
#### `logger()`
<!-- The `logger` function can be used to write a `debug` level message to the [log](/docs/11.x/logging): -->
`logger` 関数を使用して、`debug` レベルのメッセージを [log](/docs/11.x/logging) に書き込むことができます。

```
logger('Debug message');
```

<!-- An array of contextual data may also be passed to the function: -->
コンテキスト データの配列を関数に渡すこともできます。

```
logger('User has logged in.', ['id' => $user->id]);
```

<!-- A [logger](/docs/11.x/logging) instance will be returned if no value is passed to the function: -->
関数に値が渡されない場合、[logger](/docs/11.x/logging) インスタンスが返されます。

```
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
<!-- #### `method_field()` -->
#### `method_field()`
<!-- The `method_field` function generates an HTML `hidden` input field containing the spoofed value of the form's HTTP verb. For example, using [Blade syntax](/docs/11.x/blade): -->
`method_field` 関数は、フォームの HTTP 動詞の偽値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade syntax](/docs/11.x/blade) を使用すると、次のようになります。

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
<!-- The `old` function [retrieves](/docs/11.x/requests#retrieving-input) an [old input](/docs/11.x/requests#old-input) value flashed into the session: -->
`old` 関数は、セッションにフラッシュされた[retrieves](/docs/11.x/requests#old-input)値を[old input](/docs/11.x/requests#retrieving-input)します。

```
$value = old('value');

$value = old('value', 'default');
```

<!-- Since the "default value" provided as the second argument to the `old` function is often an attribute of an Eloquent model, Laravel allows you to simply pass the entire Eloquent model as the second argument to the `old` function. When doing so, Laravel will assume the first argument provided to the `old` function is the name of the Eloquent attribute that should be considered the "default value": -->
`old` 関数の 2 番目の引数として指定される「デフォルト値」は多くの場合 Eloquent モデルの属性であるため、Laravel では Eloquent モデル全体を 2 番目の引数として `old` 関数に渡すだけで済みます。これを行うと、Laravel は、`old` 関数に指定された最初の引数が、「デフォルト値」とみなされるべき Eloquent 属性の名前であると想定します。

```
{{ old('name', $user->name) }}

// Is equivalent to...

{{ old('name', $user) }}
```

<a name="method-once"></a>
<!-- #### `once()` -->
#### `once()`
<!-- The `once` function executes the given callback and caches the result in memory for the duration of the request. Any subsequent calls to the `once` function with the same callback will return the previously cached result: -->
`once` 関数は、指定されたコールバックを実行し、リクエストの間、結果をメモリにキャッシュします。同じコールバックを使用した後続の `once` 関数の呼び出しでは、以前にキャッシュされた結果が返されます。

```
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (cached result)
random(); // 123 (cached result)
```

<!-- When the `once` function is executed from within an object instance, the cached result will be unique to that object instance: -->
`once` 関数がオブジェクト インスタンス内から実行されると、キャッシュされた結果はそのオブジェクト インスタンスに固有になります。

```php
<?php

class NumberService
{
    public function all(): array
    {
        return once(fn () => [1, 2, 3]);
    }
}

$service = new NumberService;

$service->all();
$service->all(); // (cached result)

$secondService = new NumberService;

$secondService->all();
$secondService->all(); // (cached result)
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
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
<!-- #### `policy()` -->
#### `policy()`
<!-- The `policy` method retrieves a [policy](/docs/11.x/authorization#creating-policies) instance for a given class: -->
`policy` メソッドは、指定されたクラスの [policy](/docs/11.x/authorization#creating-policies) インスタンスを取得します。

```
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
<!-- #### `redirect()` -->
#### `redirect()`
<!-- The `redirect` function returns a [redirect HTTP response](/docs/11.x/responses#redirects), or returns the redirector instance if called with no arguments: -->
`redirect` 関数は [redirect HTTP response](/docs/11.x/responses#redirects) を返すか、引数なしで呼び出された場合はリダイレクター インスタンスを返します。

```
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
<!-- #### `report()` -->
#### `report()`
<!-- The `report` function will report an exception using your [exception handler](/docs/11.x/errors#handling-exceptions): -->
`report` 関数は、[exception handler](/docs/11.x/errors#handling-exceptions) を使用して例外を報告します。

```
report($e);
```

<!-- The `report` function also accepts a string as an argument. When a string is given to the function, the function will create an exception with the given string as its message: -->
`report` 関数は、引数として文字列も受け入れます。文字列が関数に与えられると、関数は指定された文字列をメッセージとして持つ例外を作成します。

```
report('Something went wrong.');
```

<a name="method-report-if"></a>
<!-- #### `report_if()` -->
#### `report_if()`
<!-- The `report_if` function will report an exception using your [exception handler](/docs/11.x/errors#handling-exceptions) if the given condition is `true`: -->
指定された条件が `true` の場合、`report_if` 関数は、[exception handler](/docs/11.x/errors#handling-exceptions) を使用して例外を報告します。

```
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
<!-- #### `report_unless()` -->
#### `report_unless()`
<!-- The `report_unless` function will report an exception using your [exception handler](/docs/11.x/errors#handling-exceptions) if the given condition is `false`: -->
指定された条件が `false` の場合、`report_unless` 関数は、[exception handler](/docs/11.x/errors#handling-exceptions) を使用して例外を報告します。

```
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
<!-- #### `request()` -->
#### `request()`
<!-- The `request` function returns the current [request](/docs/11.x/requests) instance or obtains an input field's value from the current request: -->
`request` 関数は、現在の [request](/docs/11.x/requests) インスタンスを返すか、現在のリクエストから入力フィールドの値を取得します。

```
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
<!-- #### `rescue()` -->
#### `rescue()`
<!-- The `rescue` function executes the given closure and catches any exceptions that occur during its execution. All exceptions that are caught will be sent to your [exception handler](/docs/11.x/errors#handling-exceptions); however, the request will continue processing: -->
`rescue` 関数は、指定されたクロージャを実行し、その実行中に発生する例外をキャッチします。キャッチされた例外はすべて [exception handler](/docs/11.x/errors#handling-exceptions) に送信されます。ただし、リクエストは処理を続行します。

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

<!-- A `report` argument may be provided to the `rescue` function to determine if the exception should be reported via the `report` function: -->
`report` 引数を `rescue` 関数に指定して、例外を `report` 関数経由で報告するかどうかを決定できます。

```
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
<!-- #### `resolve()` -->
#### `resolve()`
<!-- The `resolve` function resolves a given class or interface name to an instance using the [service container](/docs/11.x/container): -->
`resolve` 関数は、[service container](/docs/11.x/container) を使用して、指定されたクラスまたはインターフェイス名をインスタンスに解決します。

```
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
<!-- #### `response()` -->
#### `response()`
<!-- The `response` function creates a [response](/docs/11.x/responses) instance or obtains an instance of the response factory: -->
`response` 関数は、[response](/docs/11.x/responses) インスタンスを作成するか、応答ファクトリーのインスタンスを取得します。

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
    // Attempt 5 times while resting 100ms between attempts...
}, 100);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the third argument to the `retry` function: -->
試行間のスリープ時間を手動で計算したい場合は、`retry` 関数の 3 番目の引数としてクロージャを渡すことができます。

```
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

<!-- For convenience, you may provide an array as the first argument to the `retry` function. This array will be used to determine how many milliseconds to sleep between subsequent attempts: -->
便宜上、配列を `retry` 関数の最初の引数として指定できます。この配列は、次の試行の間にスリープする時間をミリ秒単位で決定するために使用されます。

```
return retry([100, 200], function () {
    // Sleep for 100ms on first retry, 200ms on second retry...
});
```

<!-- To only retry under specific conditions, you may pass a closure as the fourth argument to the `retry` function: -->
特定の条件下でのみ再試行するには、`retry` 関数の 4 番目の引数としてクロージャを渡すことができます。

```
use Exception;

return retry(5, function () {
    // ...
}, 100, function (Exception $exception) {
    return $exception instanceof RetryException;
});
```

<a name="method-session"></a>
<!-- #### `session()` -->
#### `session()`
<!-- The `session` function may be used to get or set [session](/docs/11.x/session) values: -->
`session` 関数は、[session](/docs/11.x/session) 値を取得または設定するために使用できます。

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
$user = tap(User::first(), function (User $user) {
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
return $user->tap(function (User $user) {
    // ...
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
$callback = function (int $value) {
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
<!-- The `validator` function creates a new [validator](/docs/11.x/validation) instance with the given arguments. You may use it as an alternative to the `Validator` facade: -->
`validator` 関数は、指定された引数を使用して新しい [validator](/docs/11.x/validation) インスタンスを作成します。 `Validator` ファサードの代替として使用できます。

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

<!-- Additional arguments may be passed to the `value` function. If the first argument is a closure then the additional parameters will be passed to the closure as arguments, otherwise they will be ignored: -->
追加の引数を `value` 関数に渡すことができます。最初の引数がクロージャの場合、追加のパラメータは引数としてクロージャに渡されます。それ以外の場合は無視されます。

```
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
<!-- #### `view()` -->
#### `view()`
<!-- The `view` function retrieves a [view](/docs/11.x/views) instance: -->
`view` 関数は、[view](/docs/11.x/views) インスタンスを取得します。

```
return view('auth.login');
```

<a name="method-with"></a>
<!-- #### `with()` -->
#### `with()`
<!-- The `with` function returns the value it is given. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned: -->
`with` 関数は、指定された値を返します。クロージャが関数の 2 番目の引数として渡されると、クロージャが実行され、その戻り値が返されます。

```
$callback = function (mixed $value) {
    return is_numeric($value) ? $value * 2 : 0;
};

$result = with(5, $callback);

// 10

$result = with(null, $callback);

// 0

$result = with(5, null);

// 5
```

<a name="method-when"></a>
<!-- #### `when()` -->
#### `when()`
<!-- The `when` function returns the value it is given if a given condition evaluates to `true`. Otherwise, `null` is returned. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned: -->
`when` 関数は、指定された条件が `true` と評価された場合に指定された値を返します。それ以外の場合は、`null` が返されます。クロージャが関数の 2 番目の引数として渡されると、クロージャが実行され、その戻り値が返されます。

```
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

<!-- The `when` function is primarily useful for conditionally rendering HTML attributes: -->
`when` 関数は、主に HTML 属性を条件付きでレンダリングする場合に役立ちます。

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
<!-- ## Other Utilities -->
## Other Utilities

<a name="benchmarking"></a>
<!-- ### Benchmarking -->
### Benchmarking

<!-- Sometimes you may wish to quickly test the performance of certain parts of your application. On those occasions, you may utilize the `Benchmark` support class to measure the number of milliseconds it takes for the given callbacks to complete: -->
場合によっては、アプリケーションの特定の部分のパフォーマンスを簡単にテストしたい場合があります。このような場合、`Benchmark` サポート クラスを利用して、指定されたコールバックが完了するまでにかかるミリ秒数を測定できます。

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
デフォルトでは、指定されたコールバックは 1 回 (1 回の反復) 実行され、その期間はブラウザ/コンソールに表示されます。

<!-- To invoke a callback more than once, you may specify the number of iterations that the callback should be invoked as the second argument to the method. When executing a callback more than once, the `Benchmark` class will return the average amount of milliseconds it took to execute the callback across all iterations: -->
コールバックを複数回呼び出すには、コールバックを呼び出す反復回数をメソッドの 2 番目の引数として指定できます。コールバックを複数回実行すると、`Benchmark` クラスは、すべての反復にわたってコールバックの実行にかかった平均ミリ秒数を返します。

```
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

<!-- Sometimes, you may want to benchmark the execution of a callback while still obtaining the value returned by the callback. The `value` method will return a tuple containing the value returned by the callback and the amount of milliseconds it took to execute the callback: -->
場合によっては、コールバックから返される値を取得しながら、コールバックの実行のベンチマークを行いたい場合があります。 `value` メソッドは、コールバックによって返された値とコールバックの実行にかかったミリ秒数を含むタプルを返します。

```
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
<!-- ### Dates -->
### Dates

<!-- Laravel includes [Carbon](https://carbon.nesbot.com/docs/), a powerful date and time manipulation library. To create a new `Carbon` instance, you may invoke the `now` function. This function is globally available within your Laravel application: -->
Laravel には、強力な日付と時刻の操作ライブラリである [Carbon](https://carbon.nesbot.com/docs/) が含まれています。新しい `Carbon` インスタンスを作成するには、`now` 関数を呼び出します。この関数は、Laravel アプリケーション内でグローバルに使用できます。

```php
$now = now();
```

<!-- Or, you may create a new `Carbon` instance using the `Illuminate\Support\Carbon` class: -->
または、`Illuminate\Support\Carbon` クラスを使用して、新しい `Carbon` インスタンスを作成することもできます。

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

<!-- For a thorough discussion of Carbon and its features, please consult the [official Carbon documentation](https://carbon.nesbot.com/docs/). -->
Carbon とその機能の詳細については、[official Carbon documentation](https://carbon.nesbot.com/docs/) を参照してください。

<a name="deferred-functions"></a>
<!-- ### Deferred Functions -->
### Deferred Functions

> [!WARNING]
> 遅延機能は現在ベータ版であり、コミュニティからのフィードバックを収集しています。

<!-- While Laravel's [queued jobs](/docs/11.x/queues) allow you to queue tasks for background processing, sometimes you may have simple tasks you would like to defer without configuring or maintaining a long-running queue worker. -->
Laravel の [queued jobs](/docs/11.x/queues) を使用すると、バックグラウンド処理のためにタスクをキューに入れることができますが、長時間実行されるキューワーカーを構成または維持せずに、単純なタスクを延期したい場合があります。

<!-- Deferred functions allow you to defer the execution of a closure until after the HTTP response has been sent to the user, keeping your application feeling fast and responsive. To defer the execution of a closure, simply pass the closure to the `Illuminate\Support\defer` function: -->
遅延関数を使用すると、HTTP 応答がユーザーに送信されるまでクロージャの実行を延期でき、アプリケーションの高速性と応答性を維持できます。クロージャの実行を延期するには、単にクロージャを `Illuminate\Support\defer` 関数に渡します。

```php
use App\Services\Metrics;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use function Illuminate\Support\defer;

Route::post('/orders', function (Request $request) {
    // Create order...

    defer(fn () => Metrics::reportOrder($order));

    return $order;
});
```

<!-- By default, deferred functions will only be executed if the HTTP response, Artisan command, or queued job from which `Illuminate\Support\defer` is invoked completes successfully. This means that deferred functions will not be executed if a request results in a `4xx` or `5xx` HTTP response. If you would like a deferred function to always execute, you may chain the `always` method onto your deferred function: -->
デフォルトでは、遅延関数は、`Illuminate\Support\defer` の呼び出し元の HTTP 応答、Artisan コマンド、またはキューに入れられたジョブが正常に完了した場合にのみ実行されます。これは、リクエストの結果が `4xx` または `5xx` HTTP レスポンスになった場合、遅延関数は実行されないことを意味します。遅延関数を常に実行したい場合は、`always` メソッドを遅延関数にチェーンできます。

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
<!-- #### Cancelling Deferred Functions -->
#### Cancelling Deferred Functions

<!-- If you need to cancel a deferred function before it is executed, you can use the `forget` method to cancel the function by its name. To name a deferred function, provide a second argument to the `Illuminate\Support\defer` function: -->
遅延関数を実行前にキャンセルする必要がある場合は、`forget` メソッドを使用して、その名前で関数をキャンセルできます。遅延関数に名前を付けるには、`Illuminate\Support\defer` 関数に 2 番目の引数を指定します。

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="deferred-function-compatibility"></a>
<!-- #### Deferred Function Compatibility -->
#### Deferred Function Compatibility

<!-- If you upgraded to Laravel 11.x from a Laravel 10.x application and your application's skeleton still contains an `app/Http/Kernel.php` file, you should add the `InvokeDeferredCallbacks` middleware to the beginning of the kernel's `$middleware` property: -->
Laravel 10.x アプリケーションから Laravel 11.x にアップグレードし、アプリケーションのスケルトンに `app/Http/Kernel.php` ファイルがまだ含まれている場合は、カーネルの `$middleware` プロパティの先頭に `InvokeDeferredCallbacks` ミドルウェアを追加する必要があります。

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class, // [tl! add]
    \App\Http\Middleware\TrustProxies::class,
    // ...
];
```

<a name="disabling-deferred-functions-in-tests"></a>
<!-- #### Disabling Deferred Functions in Tests -->
#### Disabling Deferred Functions in Tests

<!-- When writing tests, it may be useful to disable deferred functions. You may call `withoutDefer` in your test to instruct Laravel to invoke all deferred functions immediately: -->
テストを作成するときは、遅延関数を無効にすると便利な場合があります。テスト内で `withoutDefer` を呼び出して、すべての遅延関数をすぐに呼び出すように Laravel に指示できます。

```php tab=Pest
test('without defer', function () {
    $this->withoutDefer();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_defer(): void
    {
        $this->withoutDefer();

        // ...
    }
}
```

<!-- If you would like to disable deferred functions for all tests within a test case, you may call the `withoutDefer` method from the `setUp` method on your base `TestCase` class: -->
テスト ケース内のすべてのテストで遅延関数を無効にしたい場合は、基本 `TestCase` クラスの `setUp` メソッドから `withoutDefer` メソッドを呼び出すことができます。

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutDefer();
    }// [tl! add:end]
}
```

<a name="lottery"></a>
<!-- ### Lottery -->
### Lottery

<!-- Laravel's lottery class may be used to execute callbacks based on a set of given odds. This can be particularly useful when you only want to execute code for a percentage of your incoming requests: -->
Laravel の宝くじクラスは、指定されたオッズのセットに基づいてコールバックを実行するために使用できます。これは、受信リクエストの一部のコードのみを実行したい場合に特に便利です。

```
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

<!-- You may combine Laravel's lottery class with other Laravel features. For example, you may wish to only report a small percentage of slow queries to your exception handler. And, since the lottery class is callable, we may pass an instance of the class into any method that accepts callables: -->
Laravel のロッタリークラスを他の Laravel 機能と組み合わせることができます。たとえば、低速クエリのほんの一部だけを例外ハンドラーに報告したい場合があります。また、lottery クラスは呼び出し可能であるため、呼び出し可能オブジェクトを受け入れる任意のメソッドにクラスのインスタンスを渡すことができます。

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
Laravel には、アプリケーションの宝くじ呼び出しを簡単にテストできるようにするための簡単なメソッドがいくつか用意されています。

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

<a name="pipeline"></a>
<!-- ### Pipeline -->
### Pipeline

<!-- Laravel's `Pipeline` facade provides a convenient way to "pipe" a given input through a series of invokable classes, closures, or callables, giving each class the opportunity to inspect or modify the input and invoke the next callable in the pipeline: -->
Laravel の `Pipeline` ファサードは、一連の呼び出し可能なクラス、クロージャ、または呼び出し可能オブジェクトを介して特定の入力を「パイプ」する便利な方法を提供し、各クラスに入力を検査または変更して、パイプライン内の次の呼び出し可能オブジェクトを呼び出す機会を与えます。

```php
use Closure;
use App\Models\User;
use Illuminate\Support\Facades\Pipeline;

$user = Pipeline::send($user)
    ->through([
        function (User $user, Closure $next) {
            // ...

            return $next($user);
        },
        function (User $user, Closure $next) {
            // ...

            return $next($user);
        },
    ])
    ->then(fn (User $user) => $user);
```

<!-- As you can see, each invokable class or closure in the pipeline is provided the input and a `$next` closure. Invoking the `$next` closure will invoke the next callable in the pipeline. As you may have noticed, this is very similar to [middleware](/docs/11.x/middleware). -->
ご覧のとおり、パイプライン内の各呼び出し可能なクラスまたはクロージャには、入力と `$next` クロージャが提供されます。 `$next` クロージャーを呼び出すと、パイプライン内の次の呼び出し可能オブジェクトが呼び出されます。お気づきかと思いますが、これは [middleware](/docs/11.x/middleware) に非常に似ています。

<!-- When the last callable in the pipeline invokes the `$next` closure, the callable provided to the `then` method will be invoked. Typically, this callable will simply return the given input. -->
パイプライン内の最後の呼び出し可能オブジェクトが `$next` クロージャーを呼び出すと、`then` メソッドに提供された呼び出し可能オブジェクトが呼び出されます。通常、この呼び出し可能関数は単に指定された入力を返します。

<!-- Of course, as discussed previously, you are not limited to providing closures to your pipeline. You may also provide invokable classes. If a class name is provided, the class will be instantiated via Laravel's [service container](/docs/11.x/container), allowing dependencies to be injected into the invokable class: -->
もちろん、前に説明したように、パイプラインにクロージャを提供することに限定されません。呼び出し可能なクラスを提供することもできます。クラス名が指定されている場合、クラスは Laravel の [service container](/docs/11.x/container) を介してインスタンス化され、呼び出し可能なクラスに依存関係を注入できるようになります。

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->then(fn (User $user) => $user);
```

<a name="sleep"></a>
<!-- ### Sleep -->
### Sleep

<!-- Laravel's `Sleep` class is a light-weight wrapper around PHP's native `sleep` and `usleep` functions, offering greater testability while also exposing a developer friendly API for working with time: -->
Laravel の `Sleep` クラスは、PHP のネイティブ `sleep` および `usleep` 関数の軽量ラッパーであり、より優れたテスト容易性を提供すると同時に、時間を扱うための開発者に優しい API を公開します。

```
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

<!-- The `Sleep` class offers a variety of methods that allow you to work with different units of time: -->
`Sleep` クラスは、さまざまな時間単位を操作できるさまざまなメソッドを提供します。

```
// Return a value after sleeping...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// Sleep while a given value is true...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// Pause execution for 90 seconds...
Sleep::for(1.5)->minutes();

// Pause execution for 2 seconds...
Sleep::for(2)->seconds();

// Pause execution for 500 milliseconds...
Sleep::for(500)->milliseconds();

// Pause execution for 5,000 microseconds...
Sleep::for(5000)->microseconds();

// Pause execution until a given time...
Sleep::until(now()->addMinute());

// Alias of PHP's native "sleep" function...
Sleep::sleep(2);

// Alias of PHP's native "usleep" function...
Sleep::usleep(5000);
```

<!-- To easily combine units of time, you may use the `and` method: -->
時間の単位を簡単に組み合わせるには、`and` メソッドを使用できます。

```
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
<!-- #### Testing Sleep -->
#### Testing Sleep

<!-- When testing code that utilizes the `Sleep` class or PHP's native sleep functions, your test will pause execution. As you might expect, this makes your test suite significantly slower. For example, imagine you are testing the following code: -->
`Sleep` クラスまたは PHP のネイティブ スリープ関数を利用するコードをテストする場合、テストは実行を一時停止します。ご想像のとおり、これによりテスト スイートが大幅に遅くなります。たとえば、次のコードをテストしていると想像してください。

```
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

<!-- Typically, testing this code would take _at least_ one second. Luckily, the `Sleep` class allows us to "fake" sleeping so that our test suite stays fast: -->
通常、このコードのテストには少なくとも 1 秒かかります。幸いなことに、`Sleep` クラスを使用すると、テスト スイートの速度を維持するために、睡眠を「偽装」することができます。

```php tab=Pest
it('waits until ready', function () {
    Sleep::fake();

    // ...
});
```

```php tab=PHPUnit
public function test_it_waits_until_ready()
{
    Sleep::fake();

    // ...
}
```

<!-- When faking the `Sleep` class, the actual execution pause is by-passed, leading to a substantially faster test. -->
`Sleep` クラスを偽装すると、実際の実行一時停止がバイパスされ、テストが大幅に高速化されます。

<!-- Once the `Sleep` class has been faked, it is possible to make assertions against the expected "sleeps" that should have occurred. To illustrate this, let's imagine we are testing code that pauses execution three times, with each pause increasing by a single second. Using the `assertSequence` method, we can assert that our code "slept" for the proper amount of time while keeping our test fast: -->
`Sleep` クラスが偽装されると、発生するはずの「スリープ」に対してアサーションを行うことができます。これを説明するために、実行を 3 回一時停止し、各一時停止が 1 秒ずつ増加するコードをテストしていると想像してみましょう。 `assertSequence` メソッドを使用すると、テストの高速性を維持しながら、コードが適切な時間「スリープ」したことを確認できます。

```php tab=Pest
it('checks if ready three times', function () {
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

```php tab=PHPUnit
public function test_it_checks_if_ready_three_times()
{
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

<!-- Of course, the `Sleep` class offers a variety of other assertions you may use when testing: -->
もちろん、`Sleep` クラスは、テスト時に使用できる他のさまざまなアサーションを提供します。

```
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// Assert that sleep was called 3 times...
Sleep::assertSleptTimes(3);

// Assert against the duration of sleep...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Assert that the Sleep class was never invoked...
Sleep::assertNeverSlept();

// Assert that, even if Sleep was called, no execution paused occurred...
Sleep::assertInsomniac();
```

<!-- Sometimes it may be useful to perform an action whenever a fake sleep occurs in your application code. To achieve this, you may provide a callback to the `whenFakingSleep` method. In the following example, we use Laravel's [time manipulation helpers](/docs/11.x/mocking#interacting-with-time) to instantly progress time by the duration of each sleep: -->
場合によっては、アプリケーション コードで偽のスリープが発生するたびにアクションを実行すると便利な場合があります。これを実現するには、`whenFakingSleep` メソッドへのコールバックを提供できます。次の例では、Laravel の [time manipulation helpers](/docs/11.x/mocking#interacting-with-time) を使用して、各スリープの継続時間ごとに時間を瞬時に進めます。

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // Progress time when faking sleep...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

<!-- As progressing time is a common requirement, the `fake` method accepts a `syncWithCarbon` argument to keep Carbon in sync when sleeping within a test: -->
進行時間は一般的な要件であるため、`fake` メソッドは `syncWithCarbon` 引数を受け入れて、テスト内でスリープしているときに Carbon の同期を維持します。

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

<!-- Laravel uses the `Sleep` class internally whenever it is pausing execution. For example, the [`retry`](#method-retry) helper uses the `Sleep` class when sleeping, allowing for improved testability when using that helper. -->
Laravel は、実行を一時停止するたびに、内部で `Sleep` クラスを使用します。たとえば、[`retry`](#method-retry) ヘルパはスリープ時に `Sleep` クラスを使用するため、そのヘルパを使用する際のテスト容易性が向上します。

<a name="timebox"></a>
<!-- ### Timebox -->
### Timebox

<!-- Laravel's `Timebox` class ensures that the given callback always takes a fixed amount of time to execute, even if its actual execution completes sooner. This is particularly useful for cryptographic operations and user authentication checks, where attackers might exploit variations in execution time to infer sensitive information. -->
Laravel の `Timebox` クラスは、実際の実行がもっと早く完了する場合でも、指定されたコールバックの実行には常に一定の時間がかかることを保証します。これは、攻撃者が実行時間の変動を利用して機密情報を推測する可能性がある暗号操作やユーザー認証チェックに特に役立ちます。

<!-- If the execution exceeds the fixed duration, `Timebox` has no effect. It is up to the developer to choose a sufficiently long time as the fixed duration to account for worst-case scenarios. -->
実行が固定期間を超えた場合、`Timebox` は効果がありません。最悪のシナリオを考慮して十分に長い時間を固定期間として選択するかどうかは開発者次第です。

<!-- The call method accepts a closure and a time limit in microseconds, and then executes the closure and waits until the time limit is reached: -->
call メソッドはクロージャとマイクロ秒単位の時間制限を受け入れ、クロージャを実行して時間制限に達するまで待機します。

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

<!-- If an exception is thrown within the closure, this class will respect the defined delay and re-throw the exception after the delay. -->
クロージャ内で例外がスローされた場合、このクラスは定義された遅延を尊重し、遅延後に例外を再スローします。

