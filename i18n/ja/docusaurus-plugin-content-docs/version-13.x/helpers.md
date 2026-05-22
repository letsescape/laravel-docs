# ヘルパ (Helpers)

- [Introduction](#introduction)
- [利用可能な方法](#available-methods)
- [その他のユーティリティ](#other-utilities)
    - [Benchmarking](#benchmarking)
    - [日付と時刻](#dates)
    - [遅延関数](#deferred-functions)
    - [Lottery](#lottery)
    - [Pipeline](#pipeline)
    - [Sleep](#sleep)
    - [Timebox](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel には、さまざまなグローバル「ヘルパ」PHP 関数が含まれています。これらの関数の多くはフレームワーク自体によって使用されます。ただし、便利だと思われる場合は、独自のアプリケーションで自由に使用できます。

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

<a name="arrays-and-objects-method-list"></a>
### 配列とオブジェクト

<div class="collection-method-list" markdown="1">

[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::array](#method-array-array)
[Arr::boolean](#method-array-boolean)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::every](#method-array-every)
[Arr::except](#method-array-except)
[Arr::exceptValues](#method-array-except-values)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::float](#method-array-float)
[Arr::forget](#method-array-forget)
[Arr::from](#method-array-from)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAll](#method-array-hasall)
[Arr::hasAny](#method-array-hasany)
[Arr::integer](#method-array-integer)
[Arr::isAssoc](#method-array-isassoc)
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::mapSpread](#method-array-map-spread)
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::onlyValues](#method-array-only-values)
[Arr::partition](#method-array-partition)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::push](#method-array-push)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
[Arr::select](#method-array-select)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sole](#method-array-sole)
[Arr::some](#method-array-some)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::string](#method-array-string)
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
### 数字

<div class="collection-method-list" markdown="1">

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
[Number::parseInt](#method-number-parse-int)
[Number::parseFloat](#method-number-parse-float)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
[Number::spellOrdinal](#method-number-spell-ordinal)
[Number::trim](#method-number-trim)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)
[Number::useCurrency](#method-number-use-currency)
[Number::withCurrency](#method-number-with-currency)

</div>

<a name="paths-method-list"></a>
### パス

<div class="collection-method-list" markdown="1">

[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

</div>

<a name="urls-method-list"></a>
### URL

<div class="collection-method-list" markdown="1">

[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_action](#method-to-action)
[to_route](#method-to-route)
[uri](#method-uri)
[url](#method-url)

</div>

<a name="miscellaneous-method-list"></a>
### その他

<div class="collection-method-list" markdown="1">

[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[app](#method-app)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[blank](#method-blank)
[broadcast](#method-broadcast)
[broadcast_if](#method-broadcast-if)
[broadcast_unless](#method-broadcast-unless)
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

</div>

<a name="arrays"></a>
## 配列とオブジェクト (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()` {.collection-method .first-collection-method}

`Arr::accessible` メソッドは、指定された値が配列にアクセスできるかどうかを判断します。

```php
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
#### `Arr::add()` {.collection-method}

`Arr::add` メソッドは、指定されたキーが配列内に存在しない場合、または `null` に設定されている場合に、指定されたキーと値のペアを配列に追加します。

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()` {.collection-method}

`Arr::array` メソッドは、([Arr::get()](#method-array-get) と同様に) 「ドット」表記を使用して深くネストされた配列から値を取得しますが、要求された値が `array` でない場合は `InvalidArgumentException` をスローします。

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::array($array, 'languages');

// ['PHP', 'Ruby']

$value = Arr::array($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-boolean"></a>
#### `Arr::boolean()` {.collection-method}

`Arr::boolean` メソッドは、([Arr::get()](#method-array-get) と同様に) 「ドット」表記を使用して、深くネストされた配列から値を取得しますが、要求された値が `boolean` でない場合は、`InvalidArgumentException` をスローします。

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'available' => true];

$value = Arr::boolean($array, 'available');

// true

$value = Arr::boolean($array, 'name');

// throws InvalidArgumentException
```


<a name="method-array-collapse"></a>
#### `Arr::collapse()` {.collection-method}

`Arr::collapse` メソッドは、配列またはコレクションの配列を単一の配列に折りたたみます。

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()` {.collection-method}

`Arr::crossJoin` メソッドは、指定された配列を相互結合し、すべての可能な順列を含むデカルト積を返します。

```php
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
#### `Arr::divide()` {.collection-method}

`Arr::divide` メソッドは 2 つの配列を返します。1 つはキーを含み、もう 1 つは指定された配列の値を含みます。

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()` {.collection-method}

`Arr::dot` メソッドは、多次元配列を、深さを示すために「ドット」表記を使用する単一レベルの配列に平坦化します。

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-every"></a>
#### `Arr::every()` {.collection-method}

`Arr::every` メソッドは、配列内のすべての値が指定された真理テストに合格することを保証します。

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3];

Arr::every($array, fn ($i) => $i > 0);

// true

Arr::every($array, fn ($i) => $i > 2);

// false
```

<a name="method-array-except"></a>
#### `Arr::except()` {.collection-method}

`Arr::except` メソッドは、指定されたキーと値のペアを配列から削除します。

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-except-values"></a>
#### `Arr::exceptValues()` {.collection-method}

`Arr::exceptValues` メソッドは、指定された値を配列から削除します。

```php
use Illuminate\Support\Arr;

$array = ['foo', 'bar', 'baz', 'qux'];

$filtered = Arr::exceptValues($array, ['foo', 'baz']);

// ['bar', 'qux']
```

`true` を `strict` 引数に渡して、フィルタリング時に厳密な型比較を使用することもできます。

```php
use Illuminate\Support\Arr;

$array = [1, '1', 2, '2'];

$filtered = Arr::exceptValues($array, [1, 2], strict: true);

// ['1', '2']
```

<a name="method-array-exists"></a>
#### `Arr::exists()` {.collection-method}

`Arr::exists` メソッドは、指定されたキーが指定された配列に存在することを確認します。

```php
use Illuminate\Support\Arr;

$array = ['name' => 'John Doe', 'age' => 17];

$exists = Arr::exists($array, 'name');

// true

$exists = Arr::exists($array, 'salary');

// false
```

<a name="method-array-first"></a>
#### `Arr::first()` {.collection-method}

`Arr::first` メソッドは、指定された真理値テストに合格した配列の最初の要素を返します。

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

デフォルト値を 3 番目のパラメータとしてメソッドに渡すこともできます。真実テストに合格する値がない場合、この値が返されます。

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()` {.collection-method}

`Arr::flatten` メソッドは、多次元配列を単一レベルの配列にフラット化します。

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-float"></a>
#### `Arr::float()` {.collection-method}

`Arr::float` メソッドは、([Arr::get()](#method-array-get) と同様に) 「ドット」表記を使用して、深くネストされた配列から値を取得しますが、要求された値が `float` でない場合は、`InvalidArgumentException` をスローします。

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'balance' => 123.45];

$value = Arr::float($array, 'balance');

// 123.45

$value = Arr::float($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-forget"></a>
#### `Arr::forget()` {.collection-method}

`Arr::forget` メソッドは、「ドット」表記を使用して、深くネストされた配列から指定されたキーと値のペアを削除します。

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-from"></a>
#### `Arr::from()` {.collection-method}

`Arr::from` メソッドは、さまざまな入力タイプをプレーンな PHP 配列に変換します。配列、オブジェクト、および `Arrayable`、`Enumerable`、`Jsonable`、`JsonSerializable` などのいくつかの一般的な Laravel インターフェイスを含む、さまざまな入力タイプをサポートします。さらに、`Traversable` インスタンスと `WeakMap` インスタンスも処理します。

```php
use Illuminate\Support\Arr;

Arr::from((object) ['foo' => 'bar']); // ['foo' => 'bar']

class TestJsonableObject implements Jsonable
{
    public function toJson($options = 0)
    {
        return json_encode(['foo' => 'bar']);
    }
}

Arr::from(new TestJsonableObject); // ['foo' => 'bar']
```

<a name="method-array-get"></a>
#### `Arr::get()` {.collection-method}

`Arr::get` メソッドは、「ドット」表記を使用して、深くネストされた配列から値を取得します。

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

`Arr::get` メソッドは、指定されたキーが配列に存在しない場合に返されるデフォルト値も受け入れます。

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()` {.collection-method}

`Arr::has` メソッドは、「ドット」表記を使用して、指定された項目が配列内に存在するかどうかをチェックします。

```php
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::has($array, 'product.name');

// true

$contains = Arr::has($array, ['product.price', 'product.discount']);

// false
```

<a name="method-array-hasall"></a>
#### `Arr::hasAll()` {.collection-method}

`Arr::hasAll` メソッドは、「ドット」表記を使用して、指定されたすべてのキーが指定された配列に存在するかどうかを判断します。

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Taylor', 'language' => 'PHP'];

Arr::hasAll($array, ['name']); // true
Arr::hasAll($array, ['name', 'language']); // true
Arr::hasAll($array, ['name', 'IDE']); // false
```

<a name="method-array-hasany"></a>
#### `Arr::hasAny()` {.collection-method}

`Arr::hasAny` メソッドは、「ドット」表記を使用して、指定されたセット内の項目が配列内に存在するかどうかをチェックします。

```php
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::hasAny($array, 'product.name');

// true

$contains = Arr::hasAny($array, ['product.name', 'product.discount']);

// true

$contains = Arr::hasAny($array, ['category', 'product.discount']);

// false
```

<a name="method-array-integer"></a>
#### `Arr::integer()` {.collection-method}

`Arr::integer` メソッドは、([Arr::get()](#method-array-get) と同様に) 「ドット」表記を使用して深くネストされた配列から値を取得しますが、要求された値が `int` でない場合は `InvalidArgumentException` をスローします。

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'age' => 42];

$value = Arr::integer($array, 'age');

// 42

$value = Arr::integer($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-isassoc"></a>
#### `Arr::isAssoc()` {.collection-method}

指定された配列が連想配列の場合、`Arr::isAssoc` メソッドは `true` を返します。配列にゼロで始まる連続した数値キーがない場合、その配列は「結合」とみなされます。

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()` {.collection-method}

指定された配列のキーがゼロから始まる連続した整数の場合、`Arr::isList` メソッドは `true` を返します。

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()` {.collection-method}

`Arr::join` メソッドは、配列要素を文字列と結合します。このメソッドの 3 番目の引数を使用して、配列の最後の要素の結合文字列を指定することもできます。

```php
use Illuminate\Support\Arr;

$array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

$joined = Arr::join($array, ', ');

// Tailwind, Alpine, Laravel, Livewire

$joined = Arr::join($array, ', ', ', and ');

// Tailwind, Alpine, Laravel, and Livewire
```

<a name="method-array-keyby"></a>
#### `Arr::keyBy()` {.collection-method}

`Arr::keyBy` メソッドは、指定されたキーによって配列にキーを設定します。複数の項目が同じキーを持つ場合、最後の項目だけが新しい配列に表示されます。

```php
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
#### `Arr::last()` {.collection-method}

`Arr::last` メソッドは、指定された真理値テストに合格した配列の最後の要素を返します。

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

デフォルト値は、メソッドの 3 番目の引数として渡すことができます。真実テストに合格する値がない場合、この値が返されます。

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()` {.collection-method}

`Arr::map` メソッドは配列を反復処理し、各値とキーを指定されたコールバックに渡します。配列の値は、コールバックによって返される値に置き換えられます。

```php
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function (string $value, string $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
```

<a name="method-array-map-spread"></a>
#### `Arr::mapSpread()` {.collection-method}

`Arr::mapSpread` メソッドは配列を反復処理し、ネストされた各項目の値を指定されたクロージャに渡します。クロージャは自由に項目を変更して返すことができるため、変更された項目の新しい配列が形成されます。

```php
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
#### `Arr::mapWithKeys()` {.collection-method}

`Arr::mapWithKeys` メソッドは配列を反復処理し、各値を指定されたコールバックに渡します。コールバックは、単一のキーと値のペアを含む連想配列を返す必要があります。

```php
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
#### `Arr::only()` {.collection-method}

`Arr::only` メソッドは、指定された配列から指定されたキーと値のペアのみを返します。

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-only-values"></a>
#### `Arr::onlyValues()` {.collection-method}

`Arr::onlyValues` メソッドは、配列から指定された値のみを返します。

```php
use Illuminate\Support\Arr;

$array = ['foo', 'bar', 'baz', 'qux'];

$filtered = Arr::onlyValues($array, ['foo', 'baz']);

// ['foo', 'baz']
```

`true` を `strict` 引数に渡して、フィルタリング時に厳密な型比較を使用することもできます。

```php
use Illuminate\Support\Arr;

$array = [1, '1', 2, '2'];

$filtered = Arr::onlyValues($array, [1, 2], strict: true);

// [1, 2]
```

<a name="method-array-partition"></a>
#### `Arr::partition()` {.collection-method}

`Arr::partition` メソッドを PHP 配列の構造化と組み合わせて、特定の真実テストに合格する要素とそうでない要素を分離することができます。

```php
<?php

use Illuminate\Support\Arr;

$numbers = [1, 2, 3, 4, 5, 6];

[$underThree, $equalOrAboveThree] = Arr::partition($numbers, function (int $i) {
    return $i < 3;
});

dump($underThree);

// [1, 2]

dump($equalOrAboveThree);

// [3, 4, 5, 6]
```

<a name="method-array-pluck"></a>
#### `Arr::pluck()` {.collection-method}

`Arr::pluck` メソッドは、配列から指定されたキーのすべての値を取得します。

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

結果のリストにどのようにキーを設定するかを指定することもできます。

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()` {.collection-method}

`Arr::prepend` メソッドは、項目を配列の先頭にプッシュします。

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

必要に応じて、値に使用するキーを指定できます。

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()` {.collection-method}

`Arr::prependKeysWith` は、連想配列のすべてのキー名の前に指定されたプレフィックスを付加します。

```php
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
#### `Arr::pull()` {.collection-method}

`Arr::pull` メソッドは、キーと値のペアを返し、配列から削除します。

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

デフォルト値は、メソッドの 3 番目の引数として渡すことができます。キーが存在しない場合は、この値が返されます。

```php
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-push"></a>
#### `Arr::push()` {.collection-method}

`Arr::push` メソッドは、「ドット」表記を使用して項目を配列にプッシュします。指定されたキーに配列が存在しない場合は、配列が作成されます。

```php
use Illuminate\Support\Arr;

$array = [];

Arr::push($array, 'office.furniture', 'Desk');

// $array: ['office' => ['furniture' => ['Desk']]]
```

<a name="method-array-query"></a>
#### `Arr::query()` {.collection-method}

`Arr::query` メソッドは、配列をクエリ文字列に変換します。

```php
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
#### `Arr::random()` {.collection-method}

`Arr::random` メソッドは、配列からランダムな値を返します。

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (retrieved randomly)
```

オプションの 2 番目の引数として、返す項目の数を指定することもできます。この引数を指定すると、必要な項目が 1 つだけの場合でも配列が返されることに注意してください。

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (retrieved randomly)
```

<a name="method-array-reject"></a>
#### `Arr::reject()` {.collection-method}

`Arr::reject` メソッドは、指定されたクロージャを使用して配列から項目を削除します。

```php
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::reject($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [0 => 100, 2 => 300, 4 => 500]
```

<a name="method-array-select"></a>
#### `Arr::select()` {.collection-method}

`Arr::select` メソッドは、配列から値の配列を選択します。

```php
use Illuminate\Support\Arr;

$array = [
    ['id' => 1, 'name' => 'Desk', 'price' => 200],
    ['id' => 2, 'name' => 'Table', 'price' => 150],
    ['id' => 3, 'name' => 'Chair', 'price' => 300],
];

Arr::select($array, ['name', 'price']);

// [['name' => 'Desk', 'price' => 200], ['name' => 'Table', 'price' => 150], ['name' => 'Chair', 'price' => 300]]
```

<a name="method-array-set"></a>
#### `Arr::set()` {.collection-method}

`Arr::set` メソッドは、「ドット」表記を使用して、深くネストされた配列内の値を設定します。

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()` {.collection-method}

`Arr::shuffle` メソッドは、配列内の項目をランダムにシャッフルします。

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-array-sole"></a>
#### `Arr::sole()` {.collection-method}

`Arr::sole` メソッドは、指定されたクロージャを使用して配列から単一の値を取得します。配列内の複数の値が指定された真理値テストに一致する場合、`Illuminate\Support\MultipleItemsFoundException` 例外がスローされます。真実のテストに一致する値がない場合は、`Illuminate\Support\ItemNotFoundException` 例外がスローされます。

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

// 'Desk'
```

<a name="method-array-some"></a>
#### `Arr::some()` {.collection-method}

`Arr::some` メソッドは、配列内の値の少なくとも 1 つが指定された真理値テストに合格することを保証します。

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3];

Arr::some($array, fn ($i) => $i > 2);

// true
```

<a name="method-array-sort"></a>
#### `Arr::sort()` {.collection-method}

`Arr::sort` メソッドは、配列を値で並べ替えます。

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

特定のクロージャの結果によって配列を並べ替えることもできます。

```php
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
#### `Arr::sortDesc()` {.collection-method}

`Arr::sortDesc` メソッドは、配列を値の降順に並べ替えます。

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

特定のクロージャの結果によって配列を並べ替えることもできます。

```php
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
#### `Arr::sortRecursive()` {.collection-method}

`Arr::sortRecursive` メソッドは、数値インデックス付きサブ配列の場合は `sort` 関数を使用し、連想サブ配列の場合は `ksort` 関数を使用して、配列を再帰的に並べ替えます。

```php
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

結果を降順に並べ替えたい場合は、`Arr::sortRecursiveDesc` メソッドを使用できます。

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-string"></a>
#### `Arr::string()` {.collection-method}

`Arr::string` メソッドは、([Arr::get()](#method-array-get) と同様に) 「ドット」表記を使用して、深くネストされた配列から値を取得しますが、要求された値が `string` でない場合は、`InvalidArgumentException` をスローします。

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::string($array, 'name');

// Joe

$value = Arr::string($array, 'languages');

// throws InvalidArgumentException
```

<a name="method-array-take"></a>
#### `Arr::take()` {.collection-method}

`Arr::take` メソッドは、指定された項目数を含む新しい配列を返します。

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

負の整数を渡して、配列の末尾から指定した数の項目を取得することもできます。

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()` {.collection-method}

`Arr::toCssClasses` メソッドは、CSS クラス文字列を条件付きでコンパイルします。このメソッドはクラスの配列を受け入れます。配列キーには追加するクラスが含まれ、値はブール式です。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

```php
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
#### `Arr::toCssStyles()` {.collection-method}

`Arr::toCssStyles` メソッドは、条件付きで CSS スタイル文字列をコンパイルします。このメソッドは CSS 宣言の配列を受け入れます。配列キーには追加する CSS 宣言が含まれ、値はブール式です。配列要素に数値キーがある場合、コンパイルされた CSS スタイル文字列に常に含まれます。

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

このメソッドは、Laravel の機能を強化し、[クラスを Blade コンポーネントの属性バッグと結合する](/docs/{{version}}/blade#conditionally-merge-classes) および `@class` [Blade ディレクティブ](/docs/{{version}}/blade#conditional-classes) を許可します。

<a name="method-array-undot"></a>
#### `Arr::undot()` {.collection-method}

`Arr::undot` メソッドは、「ドット」表記を使用する 1 次元配列を多次元配列に拡張します。

```php
use Illuminate\Support\Arr;

$array = [
    'user.name' => 'Kevin Malone',
    'user.occupation' => 'Accountant',
];

$array = Arr::undot($array);

// ['user' => ['name' => 'Kevin Malone', 'occupation' => 'Accountant']]
```

<a name="method-array-where"></a>
#### `Arr::where()` {.collection-method}

`Arr::where` メソッドは、指定されたクロージャを使用して配列をフィルタリングします。

```php
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::where($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [1 => '200', 3 => '400']
```

<a name="method-array-where-not-null"></a>
#### `Arr::whereNotNull()` {.collection-method}

`Arr::whereNotNull` メソッドは、指定された配列からすべての `null` 値を削除します。

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()` {.collection-method}

`Arr::wrap` メソッドは、指定された値を配列にラップします。指定された値がすでに配列である場合は、変更せずに返されます。

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

指定された値が `null` の場合、空の配列が返されます。

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()` {.collection-method}

`data_fill` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の欠損値を設定します。

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

この関数はワイルドカードとしてアスタリスクも受け入れ、それに応じてターゲットを入力します。

```php
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
#### `data_get()` {.collection-method}

`data_get` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクトから値を取得します。

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

`data_get` 関数は、指定されたキーが見つからない場合に返されるデフォルト値も受け入れます。

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

この関数は、配列またはオブジェクトの任意のキーを対象とするアスタリスクを使用したワイルドカードも受け入れます。

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}` および `{last}` プレースホルダーは、配列内の最初または最後の項目を取得するために使用できます。

```php
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
#### `data_set()` {.collection-method}

`data_set` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の値を設定します。

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

この関数はアスタリスクを使用したワイルドカードも受け入れ、それに応じてターゲットに値を設定します。

```php
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

デフォルトでは、既存の値はすべて上書きされます。値が存在しない場合にのみ値を設定したい場合は、関数の 4 番目の引数として `false` を渡すことができます。

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()` {.collection-method}

`data_forget` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の値を削除します。

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

この関数はアスタリスクを使用したワイルドカードも受け入れ、それに応じてターゲットの値を削除します。

```php
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
#### `head()` {.collection-method}

`head` 関数は、指定された配列の最初の要素を返します。配列が空の場合、`false` が返されます。

```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()` {.collection-method}

`last` 関数は、指定された配列の最後の要素を返します。配列が空の場合、`false` が返されます。

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 数字 (Numbers)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()` {.collection-method}

`Number::abbreviate` メソッドは、単位の略語を付けて、指定された数値を人間が判読できる形式で返します。

```php
use Illuminate\Support\Number;

$number = Number::abbreviate(1000);

// 1K

$number = Number::abbreviate(489939);

// 490K

$number = Number::abbreviate(1230000, precision: 2);

// 1.23M
```

<a name="method-number-clamp"></a>
#### `Number::clamp()` {.collection-method}

`Number::clamp` メソッドは、指定された数値が指定された範囲内に収まることを保証します。数値が最小値より小さい場合は、最小値が返されます。数値が最大値より大きい場合は、最大値が返されます。

```php
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
#### `Number::currency()` {.collection-method}

`Number::currency` メソッドは、指定された値の通貨表現を文字列として返します。

```php
use Illuminate\Support\Number;

$currency = Number::currency(1000);

// $1,000.00

$currency = Number::currency(1000, in: 'EUR');

// €1,000.00

$currency = Number::currency(1000, in: 'EUR', locale: 'de');

// 1.000,00 €

$currency = Number::currency(1000, in: 'EUR', locale: 'de', precision: 0);

// 1.000 €
```

<a name="method-default-currency"></a>
#### `Number::defaultCurrency()` {.collection-method}

`Number::defaultCurrency` メソッドは、`Number` クラスで使用されるデフォルトの通貨を返します。

```php
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()` {.collection-method}

`Number::defaultLocale` メソッドは、`Number` クラスで使用されるデフォルトのロケールを返します。

```php
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()` {.collection-method}

`Number::fileSize` メソッドは、指定されたバイト値のファイル サイズ表現を文字列として返します。

```php
use Illuminate\Support\Number;

$size = Number::fileSize(1024);

// 1 KB

$size = Number::fileSize(1024 * 1024);

// 1 MB

$size = Number::fileSize(1024, precision: 2);

// 1.00 KB
```

<a name="method-number-for-humans"></a>
#### `Number::forHumans()` {.collection-method}

`Number::forHumans` メソッドは、指定された数値を人間が判読できる形式で返します。

```php
use Illuminate\Support\Number;

$number = Number::forHumans(1000);

// 1 thousand

$number = Number::forHumans(489939);

// 490 thousand

$number = Number::forHumans(1230000, precision: 2);

// 1.23 million
```

<a name="method-number-format"></a>
#### `Number::format()` {.collection-method}

`Number::format` メソッドは、指定された数値をロケール固有の文字列にフォーマットします。

```php
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
#### `Number::ordinal()` {.collection-method}

`Number::ordinal` メソッドは、数値の序数表現を返します。

```php
use Illuminate\Support\Number;

$number = Number::ordinal(1);

// 1st

$number = Number::ordinal(2);

// 2nd

$number = Number::ordinal(21);

// 21st
```

<a name="method-number-pairs"></a>
#### `Number::pairs()` {.collection-method}

`Number::pairs` メソッドは、指定された範囲とステップ値に基づいて数値ペア (サブ範囲) の配列を生成します。この方法は、ページネーションやタスクのバッチ処理などで、大きな範囲の数値を管理しやすい小さなサブ範囲に分割する場合に役立ちます。 `pairs` メソッドは配列の配列を返します。各内部配列は数値のペア (サブ範囲) を表します。

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[0, 9], [10, 19], [20, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-parse-int"></a>
#### `Number::parseInt()` {.collection-method}

`Number::parseInt` メソッドは、指定されたロケールに従って文字列を整数に解析します。

```php
use Illuminate\Support\Number;

$result = Number::parseInt('10.123');

// (int) 10

$result = Number::parseInt('10,123', locale: 'fr');

// (int) 10
```

<a name="method-number-parse-float"></a>
#### `Number::parseFloat()` {.collection-method}

`Number::parseFloat` メソッドは、指定されたロケールに従って文字列を float に解析します。

```php
use Illuminate\Support\Number;

$result = Number::parseFloat('10');

// (float) 10.0

$result = Number::parseFloat('10', locale: 'fr');

// (float) 10.0
```

<a name="method-number-percentage"></a>
#### `Number::percentage()` {.collection-method}

`Number::percentage` メソッドは、指定された値のパーセント表現を文字列として返します。

```php
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
#### `Number::spell()` {.collection-method}

`Number::spell` メソッドは、指定された数値を単語の文字列に変換します。

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 引数を使用すると、すべての数値の後に続く値を指定できます。

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 引数を使用すると、すべての数値の前にスペルアウトする必要がある値を指定できます。

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-spell-ordinal"></a>
#### `Number::spellOrdinal()` {.collection-method}

`Number::spellOrdinal` メソッドは、数値の序数表現を単語の文字列として返します。

```php
use Illuminate\Support\Number;

$number = Number::spellOrdinal(1);

// first

$number = Number::spellOrdinal(2);

// second

$number = Number::spellOrdinal(21);

// twenty-first
```

<a name="method-number-trim"></a>
#### `Number::trim()` {.collection-method}

`Number::trim` メソッドは、指定された数値の小数点以下の末尾のゼロの数字を削除します。

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()` {.collection-method}

`Number::useLocale` メソッドは、デフォルトの数値ロケールをグローバルに設定します。これは、`Number` クラスのメソッドの後続の呼び出しによって数値と通貨がどのようにフォーマットされるかに影響します。

```php
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
#### `Number::withLocale()` {.collection-method}

`Number::withLocale` メソッドは、指定されたロケールを使用して指定されたクロージャを実行し、コールバックの実行後に元のロケールを復元します。

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()` {.collection-method}

`Number::useCurrency` メソッドは、デフォルトの数値通貨をグローバルに設定します。これは、その後の `Number` クラスのメソッドの呼び出しによって通貨がどのようにフォーマットされるかに影響します。

```php
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
#### `Number::withCurrency()` {.collection-method}

`Number::withCurrency` メソッドは、指定された通貨を使用して指定されたクロージャを実行し、コールバックの実行後に元の通貨を復元します。

```php
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
```

<a name="paths"></a>
## パス (Paths)

<a name="method-app-path"></a>
#### `app_path()` {.collection-method}

`app_path` 関数は、アプリケーションの `app` ディレクトリへの完全修飾パスを返します。 `app_path` 関数を使用して、アプリケーション ディレクトリを基準としたファイルへの完全修飾パスを生成することもできます。

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()` {.collection-method}

`base_path` 関数は、アプリケーションのルート ディレクトリへの完全修飾パスを返します。 `base_path` 関数を使用して、プロジェクトのルート ディレクトリを基準とした特定のファイルへの完全修飾パスを生成することもできます。

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()` {.collection-method}

`config_path` 関数は、アプリケーションの `config` ディレクトリへの完全修飾パスを返します。 `config_path` 関数を使用して、アプリケーションの構成ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()` {.collection-method}

`database_path` 関数は、アプリケーションの `database` ディレクトリへの完全修飾パスを返します。 `database_path` 関数を使用して、データベース ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()` {.collection-method}

`lang_path` 関数は、アプリケーションの `lang` ディレクトリへの完全修飾パスを返します。 `lang_path` 関数を使用して、ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

<a name="method-public-path"></a>
#### `public_path()` {.collection-method}

`public_path` 関数は、アプリケーションの `public` ディレクトリへの完全修飾パスを返します。 `public_path` 関数を使用して、パブリック ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()` {.collection-method}

`resource_path` 関数は、アプリケーションの `resources` ディレクトリへの完全修飾パスを返します。 `resource_path` 関数を使用して、リソース ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()` {.collection-method}

`storage_path` 関数は、アプリケーションの `storage` ディレクトリへの完全修飾パスを返します。 `storage_path` 関数を使用して、ストレージ ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL (URLs)

<a name="method-action"></a>
#### `action()` {.collection-method}

`action` 関数は、指定されたコントローラ アクションの URL を生成します。

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

メソッドがルート パラメーターを受け入れる場合は、それらを 2 番目の引数としてメソッドに渡すことができます。

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()` {.collection-method}

`asset` 関数は、現在のリクエスト スキーム (HTTP または HTTPS) を使用してアセットの URL を生成します。

```php
$url = asset('img/photo.jpg');
```

`.env` ファイルで `ASSET_URL` 変数を設定することで、アセット URL ホストを構成できます。これは、Amazon S3 や別の CDN などの外部サービスでアセットをホストする場合に便利です。

```php
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()` {.collection-method}

`route` 関数は、指定された [名前付きルート](/docs/{{version}}/routing#named-routes) の URL を生成します。

```php
$url = route('route.name');
```

ルートがパラメーターを受け入れる場合は、それらを関数の 2 番目の引数として渡すことができます。

```php
$url = route('route.name', ['id' => 1]);
```

デフォルトでは、`route` 関数は絶対 URL を生成します。相対 URL を生成したい場合は、関数の 3 番目の引数として `false` を渡すことができます。

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()` {.collection-method}

`secure_asset` 関数は、HTTPS を使用してアセットの URL を生成します。

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()` {.collection-method}

`secure_url` 関数は、指定されたパスへの完全修飾 HTTPS URL を生成します。追加の URL セグメントを関数の 2 番目の引数に渡すことができます。

```php
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-action"></a>
#### `to_action()` {.collection-method}

`to_action` 関数は、指定されたコントローラ アクションの [HTTP 応答をリダイレクトする](/docs/{{version}}/responses#redirects) を生成します。

```php
use App\Http\Controllers\UserController;

return to_action([UserController::class, 'show'], ['user' => 1]);
```

必要に応じて、リダイレクトに割り当てる必要がある HTTP ステータス コードと追加の応答ヘッダーを `to_action` メソッドの 3 番目と 4 番目の引数として渡すことができます。

```php
return to_action(
    [UserController::class, 'show'],
    ['user' => 1],
    302,
    ['X-Framework' => 'Laravel']
);
```

<a name="method-to-route"></a>
#### `to_route()` {.collection-method}

`to_route` 関数は、指定された [名前付きルート](/docs/{{version}}/responses#redirects) の [HTTP 応答をリダイレクトする](/docs/{{version}}/routing#named-routes) を生成します。

```php
return to_route('users.show', ['user' => 1]);
```

必要に応じて、リダイレクトに割り当てる必要がある HTTP ステータス コードと追加の応答ヘッダーを `to_route` メソッドの 3 番目と 4 番目の引数として渡すことができます。

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-uri"></a>
#### `uri()` {.collection-method}

`uri` 関数は、指定された URI の [流暢な URI インスタンス](#uri) を生成します。

```php
$uri = uri('https://example.com')
    ->withPath('/users')
    ->withQuery(['page' => 1]);
```

`uri` 関数に呼び出し可能なコントローラとメソッドのペアを含む配列が指定された場合、関数はコントローラ メソッドのルート パスの `Uri` インスタンスを作成します。

```php
use App\Http\Controllers\UserController;

$uri = uri([UserController::class, 'show'], ['user' => $user]);
```

コントローラが呼び出し可能な場合は、コントローラのクラス名を指定するだけで済みます。

```php
use App\Http\Controllers\UserIndexController;

$uri = uri(UserIndexController::class);
```

`uri` 関数に指定された値が [名前付きルート](/docs/{{version}}/routing#named-routes) の名前と一致する場合、そのルートのパスに対して `Uri` インスタンスが生成されます。

```php
$uri = uri('users.show', ['user' => $user]);
```

<a name="method-url"></a>
#### `url()` {.collection-method}

`url` 関数は、指定されたパスへの完全修飾 URL を生成します。

```php
$url = url('user/profile');

$url = url('user/profile', [1]);
```

パスが指定されていない場合は、`Illuminate\Routing\UrlGenerator` インスタンスが返されます。

```php
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

`url` 関数の使用方法の詳細については、[URL生成ドキュメント](/docs/{{version}}/urls#generating-urls) を参照してください。

<a name="miscellaneous"></a>
## その他 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()` {.collection-method}

`abort` 関数は、[例外ハンドラ](/docs/{{version}}/errors#http-exceptions) によってレンダリングされる [HTTP例外](/docs/{{version}}/errors#handling-exceptions) をスローします。

```php
abort(403);
```

ブラウザに送信する例外のメッセージとカスタム HTTP 応答ヘッダーを指定することもできます。

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()` {.collection-method}

指定されたブール式が `true` と評価される場合、`abort_if` 関数は HTTP 例外をスローします。

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` メソッドと同様に、関数の 3 番目の引数として例外の応答テキストを指定し、4 番目の引数としてカスタム応答ヘッダーの配列を指定することもできます。

<a name="method-abort-unless"></a>
#### `abort_unless()` {.collection-method}

指定されたブール式が `false` と評価される場合、`abort_unless` 関数は HTTP 例外をスローします。

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

`abort` メソッドと同様に、関数の 3 番目の引数として例外の応答テキストを指定し、4 番目の引数としてカスタム応答ヘッダーの配列を指定することもできます。

<a name="method-app"></a>
#### `app()` {.collection-method}

`app` 関数は、[サービスコンテナ](/docs/{{version}}/container) インスタンスを返します。

```php
$container = app();
```

クラス名またはインターフェース名を渡して、コンテナーから解決できます。

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()` {.collection-method}

`auth` 関数は、[authenticator](/docs/{{version}}/authentication) インスタンスを返します。 `Auth` ファサードの代替として使用できます。

```php
$user = auth()->user();
```

必要に応じて、アクセスするガード インスタンスを指定できます。

```php
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()` {.collection-method}

`back` 関数は、ユーザーの以前の場所に [HTTP 応答をリダイレクトする](/docs/{{version}}/responses#redirects) を生成します。

```php
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()` {.collection-method}

`bcrypt` 関数 [hashes](/docs/{{version}}/hashing) は、Bcrypt を使用して指定された値を取得します。この関数は、`Hash` ファサードの代わりに使用できます。

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()` {.collection-method}

`blank` 関数は、指定された値が「空白」かどうかを判断します。

```php
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

`blank` の逆関数については、[filled](#method-filled) 関数を参照してください。

<a name="method-broadcast"></a>
#### `broadcast()` {.collection-method}

`broadcast` 関数 [broadcasts](/docs/{{version}}/broadcasting) は、指定された [event](/docs/{{version}}/events) をリスナに渡します。

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-if"></a>
#### `broadcast_if()` {.collection-method}

指定されたブール式が `true` と評価される場合、`broadcast_if` 関数 [broadcasts](/docs/{{version}}/broadcasting) は指定された [event](/docs/{{version}}/events) をリスナに送信します。

```php
broadcast_if($user->isActive(), new UserRegistered($user));

broadcast_if($user->isActive(), new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-unless"></a>
#### `broadcast_unless()` {.collection-method}

指定されたブール式が `false` と評価される場合、`broadcast_unless` 関数 [broadcasts](/docs/{{version}}/broadcasting) は指定された [event](/docs/{{version}}/events) をリスナに送信します。

```php
broadcast_unless($user->isBanned(), new UserRegistered($user));

broadcast_unless($user->isBanned(), new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()` {.collection-method}

`cache` 関数を使用して、[cache](/docs/{{version}}/cache) から値を取得できます。指定されたキーがキャッシュに存在しない場合は、オプションのデフォルト値が返されます。

```php
$value = cache('key');

$value = cache('key', 'default');
```

キーと値のペアの配列を関数に渡すことで、キャッシュに項目を追加できます。キャッシュされた値が有効であるとみなされる秒数または期間も渡す必要があります。

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->plus(seconds: 10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()` {.collection-method}

`class_uses_recursive` 関数は、そのすべての親クラスで使用される特性を含む、クラスで使用されるすべての特性を返します。

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()` {.collection-method}

`collect` 関数は、指定された値から [collection](/docs/{{version}}/collections) インスタンスを作成します。

```php
$collection = collect(['Taylor', 'Abigail']);
```

<a name="method-config"></a>
#### `config()` {.collection-method}

`config` 関数は、[configuration](/docs/{{version}}/configuration) 変数の値を取得します。設定値には、ファイル名とアクセスするオプションを含む「ドット」構文を使用してアクセスできます。構成オプションが存在しない場合に返されるデフォルト値を指定することもできます。

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

キーと値のペアの配列を渡すことで、実行時に構成変数を設定できます。ただし、この関数は現在のリクエストの構成値にのみ影響し、実際の構成値は更新されないことに注意してください。

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()` {.collection-method}

`context` 関数は、現在の [context](/docs/{{version}}/context) から値を取得します。コンテキスト キーが存在しない場合に返されるデフォルト値を指定することもできます。

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

キーと値のペアの配列を渡すことでコンテキスト値を設定できます。

```php
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
#### `cookie()` {.collection-method}

`cookie` 関数は、新しい [cookie](/docs/{{version}}/requests#cookies) インスタンスを作成します。

```php
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()` {.collection-method}

`csrf_field` 関数は、CSRF トークンの値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade 構文](/docs/{{version}}/blade) を使用すると、次のようになります。

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()` {.collection-method}

`csrf_token` 関数は、現在の CSRF トークンの値を取得します。

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()` {.collection-method}

`decrypt` 関数 [decrypts](/docs/{{version}}/encryption) に指定された値。この関数は、`Crypt` ファサードの代わりに使用できます。

```php
$password = decrypt($value);
```

`decrypt` の逆関数については、[encrypt](#method-encrypt) 関数を参照してください。

<a name="method-dd"></a>
#### `dd()` {.collection-method}

`dd` 関数は、指定された変数をダンプし、スクリプトの実行を終了します。

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

スクリプトの実行を停止したくない場合は、代わりに [dump](#method-dump) 関数を使用してください。

<a name="method-dispatch"></a>
#### `dispatch()` {.collection-method}

`dispatch` 関数は、指定された [job](/docs/{{version}}/queues#creating-jobs) を Laravel [ジョブキュー](/docs/{{version}}/queues) にプッシュします。

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()` {.collection-method}

`dispatch_sync` 関数は、指定されたジョブを [sync](/docs/{{version}}/queues#synchronous-dispatching) キューにプッシュして、すぐに処理されるようにします。

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()` {.collection-method}

`dump` 関数は、指定された変数をダンプします。

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

変数をダンプした後にスクリプトの実行を停止する場合は、代わりに [dd](#method-dd) 関数を使用します。

<a name="method-encrypt"></a>
#### `encrypt()` {.collection-method}

`encrypt` 関数 [encrypts](/docs/{{version}}/encryption) に指定された値。この関数は、`Crypt` ファサードの代わりに使用できます。

```php
$secret = encrypt('my-secret-value');
```

`encrypt` の逆関数については、[decrypt](#method-decrypt) 関数を参照してください。

<a name="method-env"></a>
#### `env()` {.collection-method}

`env` 関数は、[環境変数](/docs/{{version}}/configuration#environment-configuration) の値を取得するか、デフォルト値を返します。

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされず、`env` 関数へのすべての呼び出しは、サーバー レベルまたはシステム レベルの環境変数、または `null` などの外部環境変数を返します。

<a name="method-event"></a>
#### `event()` {.collection-method}

`event` 関数は、指定された [event](/docs/{{version}}/events) をリスナにディスパッチします。

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()` {.collection-method}

`fake` 関数は、コンテナーから [Faker](https://github.com/FakerPHP/Faker) シングルトンを解決します。これは、モデル ファクトリ、データベース シーディング、テスト、およびプロトタイピング ビューで偽のデータを作成するときに役立ちます。

```blade
@for ($i = 0; $i < 10; $i++)
    <dl>
        <dt>Name</dt>
        <dd>{{ fake()->name() }}</dd>

        <dt>Email</dt>
        <dd>{{ fake()->unique()->safeEmail() }}</dd>
    </dl>
@endfor
```

デフォルトでは、`fake` 関数は、`config/app.php` 構成の `app.faker_locale` 構成オプションを利用します。通常、この構成オプションは `APP_FAKER_LOCALE` 環境変数を介して設定されます。ロケールを `fake` 関数に渡して指定することもできます。各ロケールは個別のシングルトンを解決します。

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()` {.collection-method}

`filled` 関数は、指定された値が「空白」でないかどうかを判断します。

```php
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

`filled` の逆関数については、[blank](#method-blank) 関数を参照してください。

<a name="method-info"></a>
#### `info()` {.collection-method}

`info` 関数は、アプリケーションの [log](/docs/{{version}}/logging) に情報を書き込みます。

```php
info('Some helpful information!');
```

コンテキスト データの配列を関数に渡すこともできます。

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()` {.collection-method}

`literal` 関数は、指定された名前付き引数をプロパティとして使用して、新しい [stdClass](https://www.php.net/manual/en/class.stdclass.php) インスタンスを作成します。

```php
$obj = literal(
    name: 'Joe',
    languages: ['PHP', 'Ruby'],
);

$obj->name; // 'Joe'
$obj->languages; // ['PHP', 'Ruby']
```

<a name="method-logger"></a>
#### `logger()` {.collection-method}

`logger` 関数を使用して、`debug` レベルのメッセージを [log](/docs/{{version}}/logging) に書き込むことができます。

```php
logger('Debug message');
```

コンテキスト データの配列を関数に渡すこともできます。

```php
logger('User has logged in.', ['id' => $user->id]);
```

関数に値が渡されない場合、[logger](/docs/{{version}}/logging) インスタンスが返されます。

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()` {.collection-method}

`method_field` 関数は、フォームの HTTP 動詞の偽値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade 構文](/docs/{{version}}/blade) を使用すると、次のようになります。

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()` {.collection-method}

`now` 関数は、現時点での新しい `Illuminate\Support\Carbon` インスタンスを作成します。

```php
$now = now();
```

<a name="method-old"></a>
#### `old()` {.collection-method}

`old` 関数 [retrieves](/docs/{{version}}/requests#retrieving-input) および [古い入力](/docs/{{version}}/requests#old-input) 値がセッションにフラッシュされました。

```php
$value = old('value');

$value = old('value', 'default');
```

`old` 関数の 2 番目の引数として指定される「デフォルト値」は多くの場合 Eloquent モデルの属性であるため、Laravel では Eloquent モデル全体を 2 番目の引数として `old` 関数に渡すだけで済みます。これを行うと、Laravel は、`old` 関数に指定された最初の引数が、「デフォルト値」とみなされるべき Eloquent 属性の名前であると想定します。

```blade
{{ old('name', $user->name) }}

// Is equivalent to...

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()` {.collection-method}

`once` 関数は、指定されたコールバックを実行し、リクエストの間、結果をメモリにキャッシュします。同じコールバックを使用した後続の `once` 関数の呼び出しでは、以前にキャッシュされた結果が返されます。

```php
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
#### `optional()` {.collection-method}

`optional` 関数は任意の引数を受け入れ、そのオブジェクトのプロパティにアクセスしたり、メソッドを呼び出したりすることができます。指定されたオブジェクトが `null` の場合、プロパティとメソッドはエラーを引き起こす代わりに `null` を返します。

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

`optional` 関数は、2 番目の引数としてクロージャも受け入れます。最初の引数として指定された値が null でない場合、クロージャが呼び出されます。

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()` {.collection-method}

`policy` メソッドは、指定されたクラスの [policy](/docs/{{version}}/authorization#creating-policies) インスタンスを取得します。

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()` {.collection-method}

`redirect` 関数は [HTTP 応答をリダイレクトする](/docs/{{version}}/responses#redirects) を返すか、引数なしで呼び出された場合はリダイレクター インスタンスを返します。

```php
return redirect($to = null, $status = 302, $headers = [], $secure = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()` {.collection-method}

`report` 関数は、[例外ハンドラ](/docs/{{version}}/errors#handling-exceptions) を使用して例外を報告します。

```php
report($e);
```

`report` 関数は、引数として文字列も受け入れます。文字列が関数に与えられると、関数は指定された文字列をメッセージとして持つ例外を作成します。

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()` {.collection-method}

指定されたブール式が `true` と評価される場合、`report_if` 関数は、[例外ハンドラ](/docs/{{version}}/errors#handling-exceptions) を使用して例外を報告します。

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()` {.collection-method}

指定されたブール式が `false` と評価される場合、`report_unless` 関数は、[例外ハンドラ](/docs/{{version}}/errors#handling-exceptions) を使用して例外を報告します。

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()` {.collection-method}

`request` 関数は、現在の [request](/docs/{{version}}/requests) インスタンスを返すか、現在のリクエストから入力フィールドの値を取得します。

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()` {.collection-method}

`rescue` 関数は、指定されたクロージャを実行し、その実行中に発生する例外をキャッチします。キャッチされた例外はすべて [例外ハンドラ](/docs/{{version}}/errors#handling-exceptions) に送信されます。ただし、リクエストは処理を続行します。

```php
return rescue(function () {
    return $this->method();
});
```

`rescue` 関数に 2 番目の引数を渡すこともできます。この引数は、クロージャの実行中に例外が発生した場合に返される「デフォルト」値になります。

```php
return rescue(function () {
    return $this->method();
}, false);

return rescue(function () {
    return $this->method();
}, function () {
    return $this->failure();
});
```

`report` 引数を `rescue` 関数に指定して、例外を `report` 関数経由で報告するかどうかを決定できます。

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()` {.collection-method}

`resolve` 関数は、[サービスコンテナ](/docs/{{version}}/container) を使用して、指定されたクラスまたはインターフェイス名をインスタンスに解決します。

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()` {.collection-method}

`response` 関数は、[response](/docs/{{version}}/responses) インスタンスを作成するか、応答ファクトリーのインスタンスを取得します。

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()` {.collection-method}

`retry` 関数は、指定された最大試行しきい値に達するまで、指定されたコールバックの実行を試行します。コールバックが例外をスローしない場合は、その戻り値が返されます。コールバックが例外をスローした場合、自動的に再試行されます。最大試行回数を超えると、例外がスローされます。

```php
return retry(5, function () {
    // Attempt 5 times while resting 100ms between attempts...
}, 100);
```

スリープ期間は `CarbonInterval` インスタンスも受け入れます。

```php
use function Illuminate\Support\seconds;

return retry(5, function () {
    // Attempt 5 times while resting 5 seconds between attempts...
}, seconds(5));
```

試行間のスリープ時間を手動で計算したい場合は、`retry` 関数の 3 番目の引数としてクロージャを渡すことができます。

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

便宜上、配列を `retry` 関数の最初の引数として指定できます。この配列は、次の試行の間にスリープする時間をミリ秒単位で決定するために使用されます。

```php
return retry([100, 200], function () {
    // Sleep for 100ms on first retry, 200ms on second retry...
});
```

特定の条件下でのみ再試行するには、`retry` 関数の 4 番目の引数としてクロージャを渡すことができます。

```php
use App\Exceptions\TemporaryException;
use Exception;

return retry(5, function () {
    // ...
}, 100, function (Exception $exception) {
    return $exception instanceof TemporaryException;
});
```

<a name="method-session"></a>
#### `session()` {.collection-method}

`session` 関数は、[session](/docs/{{version}}/session) 値を取得または設定するために使用できます。

```php
$value = session('key');
```

キーと値のペアの配列を関数に渡すことで、値を設定できます。

```php
session(['chairs' => 7, 'instruments' => 3]);
```

関数に値が渡されない場合、セッション ストアが返されます。

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()` {.collection-method}

`tap` 関数は、任意の `$value` とクロージャの 2 つの引数を受け入れます。 `$value` はクロージャに渡され、`tap` 関数によって返されます。クロージャの戻り値は無関係です。

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'Taylor';

    $user->save();
});
```

クロージャーが `tap` 関数に渡されない場合は、指定された `$value` で任意のメソッドを呼び出すことができます。呼び出したメソッドの戻り値は、メソッドがその定義で実際に何を返すかに関係なく、常に `$value` になります。たとえば、Eloquent `update` メソッドは通常、整数を返します。ただし、`tap` 関数を介して `update` メソッド呼び出しを連鎖させることで、メソッドがモデル自体を返すように強制できます。

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

`tap` メソッドをクラスに追加するには、`Illuminate\Support\Traits\Tappable` 特性をクラスに追加します。このトレイトの `tap` メソッドは、唯一の引数として Closure を受け入れます。オブジェクト インスタンス自体はクロージャに渡され、`tap` メソッドによって返されます。

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()` {.collection-method}

指定されたブール式が `true` と評価される場合、`throw_if` 関数は指定された例外をスローします。

```php
throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

throw_if(
    ! Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-throw-unless"></a>
#### `throw_unless()` {.collection-method}

指定されたブール式が `false` と評価される場合、`throw_unless` 関数は指定された例外をスローします。

```php
throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

throw_unless(
    Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-today"></a>
#### `today()` {.collection-method}

`today` 関数は、現在の日付の新しい `Illuminate\Support\Carbon` インスタンスを作成します。

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()` {.collection-method}

`trait_uses_recursive` 関数は、特性によって使用されるすべての特性を返します。

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()` {.collection-method}

`transform` 関数は、値が [blank](#method-blank) でない場合、指定された値に対してクロージャを実行し、クロージャの戻り値を返します。

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

デフォルト値またはクロージャは、関数の 3 番目の引数として渡すことができます。指定された値が空白の場合、この値が返されます。

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()` {.collection-method}

`validator` 関数は、指定された引数を使用して新しい [validator](/docs/{{version}}/validation) インスタンスを作成します。 `Validator` ファサードの代替として使用できます。

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()` {.collection-method}

`value` 関数は、指定された値を返します。ただし、関数にクロージャを渡すと、クロージャが実行され、その戻り値が返されます。

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

追加の引数を `value` 関数に渡すことができます。最初の引数がクロージャの場合、追加のパラメータは引数としてクロージャに渡されます。それ以外の場合は無視されます。

```php
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()` {.collection-method}

`view` 関数は、[view](/docs/{{version}}/views) インスタンスを取得します。

```php
return view('auth.login');
```

<a name="method-with"></a>
#### `with()` {.collection-method}

`with` 関数は、指定された値を返します。クロージャが関数の 2 番目の引数として渡されると、クロージャが実行され、その戻り値が返されます。

```php
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
#### `when()` {.collection-method}

`when` 関数は、指定された条件が `true` と評価された場合に指定された値を返します。それ以外の場合は、`null` が返されます。クロージャが関数の 2 番目の引数として渡されると、クロージャが実行され、その戻り値が返されます。

```php
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

`when` 関数は、主に HTML 属性を条件付きでレンダリングする場合に役立ちます。

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## その他のユーティリティ (Other Utilities)

<a name="benchmarking"></a>
### ベンチマーク

場合によっては、アプリケーションの特定の部分のパフォーマンスを簡単にテストしたい場合があります。このような場合、`Benchmark` サポート クラスを利用して、指定されたコールバックが完了するまでにかかるミリ秒数を測定できます。

```php
<?php

use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    'Scenario 1' => fn () => User::count(), // 0.5 ms
    'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

デフォルトでは、指定されたコールバックは 1 回 (1 回の反復) 実行され、その期間はブラウザ/コンソールに表示されます。

コールバックを複数回呼び出すには、コールバックを呼び出す反復回数をメソッドの 2 番目の引数として指定できます。コールバックを複数回実行すると、`Benchmark` クラスは、すべての反復にわたってコールバックの実行にかかった平均ミリ秒数を返します。

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

場合によっては、コールバックから返される値を取得しながら、コールバックの実行のベンチマークを行いたい場合があります。 `value` メソッドは、コールバックによって返された値とコールバックの実行にかかったミリ秒数を含むタプルを返します。

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 日付と時刻

Laravel には、強力な日付と時刻の操作ライブラリである [Carbon](https://carbon.nesbot.com/guide/getting-started/introduction.html) が含まれています。新しい `Carbon` インスタンスを作成するには、`now` 関数を呼び出します。この関数は、Laravel アプリケーション内でグローバルに使用できます。

```php
$now = now();
```

または、`Illuminate\Support\Carbon` クラスを使用して、新しい `Carbon` インスタンスを作成することもできます。

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Laravel は、`plus` メソッドと `minus` メソッドを使用して `Carbon` インスタンスを拡張し、インスタンスの日付と時刻を簡単に操作できるようにします。

```php
return now()->plus(minutes: 5);
return now()->plus(hours: 8);
return now()->plus(weeks: 4);

return now()->minus(minutes: 5);
return now()->minus(hours: 8);
return now()->minus(weeks: 4);
```

Carbon とその機能の詳細については、[Carbon の公式ドキュメント](https://carbon.nesbot.com/guide/getting-started/introduction.html) を参照してください。

<a name="interval-functions"></a>
#### インターバル関数

Laravel は、`CarbonInterval` インスタンスを返す `milliseconds`、`seconds`、`minutes`、`hours`、`days`、`weeks`、`months`、および `years` 関数も提供しており、これは PHP の機能を拡張します。 [DateInterval](https://www.php.net/manual/en/class.dateinterval.php) クラス。これらの関数は、Laravel が `DateInterval` インスタンスを受け入れる場所であればどこでも使用できます。

```php
use Illuminate\Support\Facades\Cache;

use function Illuminate\Support\{minutes};

Cache::put('metrics', $metrics, minutes(10));
```

<a name="deferred-functions"></a>
### 遅延関数

Laravel の [キューに入れられたジョブ](/docs/{{version}}/queues) を使用すると、バックグラウンド処理のためにタスクをキューに入れることができますが、長時間実行されるキューワーカーを構成または維持せずに、単純なタスクを延期したい場合があります。

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

デフォルトでは、遅延関数は、`Illuminate\Support\defer` の呼び出し元の HTTP 応答、Artisan コマンド、またはキューに入れられたジョブが正常に完了した場合にのみ実行されます。これは、リクエストの結果が `4xx` または `5xx` HTTP レスポンスになった場合、遅延関数は実行されないことを意味します。遅延関数を常に実行したい場合は、`always` メソッドを遅延関数にチェーンできます。

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

> [!WARNING]
> [Swoole PHP 拡張機能](https://www.php.net/manual/en/book.swoole.php) がインストールされている場合、Laravel の `defer` 関数が Swoole 独自のグローバル `defer` 関数と競合し、Web サーバー エラーが発生する可能性があります。 Laravel の `defer` ヘルパを明示的に名前空間を指定して呼び出すようにしてください: `use function Illuminate\Support\defer;`

<a name="cancelling-deferred-functions"></a>
#### 遅延関数のキャンセル

遅延関数を実行前にキャンセルする必要がある場合は、`forget` メソッドを使用して、その名前で関数をキャンセルできます。遅延関数に名前を付けるには、`Illuminate\Support\defer` 関数に 2 番目の引数を指定します。

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### テストでの遅延関数の無効化

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
### 宝くじ

Laravel の宝くじクラスは、指定されたオッズのセットに基づいてコールバックを実行するために使用できます。これは、受信リクエストの一部のコードのみを実行したい場合に特に便利です。

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

Laravel のロッタリークラスを他の Laravel 機能と組み合わせることができます。たとえば、低速クエリのほんの一部だけを例外ハンドラーに報告したい場合があります。また、lottery クラスは呼び出し可能であるため、呼び出し可能オブジェクトを受け入れる任意のメソッドにクラスのインスタンスを渡すことができます。

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;

DB::whenQueryingForLongerThan(
    CarbonInterval::seconds(2),
    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
);
```

<a name="testing-lotteries"></a>
#### 宝くじのテスト

Laravel には、アプリケーションの宝くじ呼び出しを簡単にテストできるようにするための簡単なメソッドがいくつか用意されています。

```php
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
### パイプライン

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

ご覧のとおり、パイプライン内の各呼び出し可能なクラスまたはクロージャには、入力と `$next` クロージャが提供されます。 `$next` クロージャーを呼び出すと、パイプライン内の次の呼び出し可能オブジェクトが呼び出されます。お気づきかと思いますが、これは [middleware](/docs/{{version}}/middleware) に非常に似ています。

パイプライン内の最後の呼び出し可能オブジェクトが `$next` クロージャーを呼び出すと、`then` メソッドに提供された呼び出し可能オブジェクトが呼び出されます。通常、この呼び出し可能関数は単に指定された入力を返します。便宜上、処理後に入力を単に返したい場合は、`thenReturn` メソッドを使用できます。

もちろん、前に説明したように、パイプラインにクロージャを提供することに限定されません。呼び出し可能なクラスを提供することもできます。クラス名が指定されている場合、クラスは Laravel の [サービスコンテナ](/docs/{{version}}/container) を介してインスタンス化され、呼び出し可能なクラスに依存関係を注入できるようになります。

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

`withinTransaction` メソッドをパイプライン上で呼び出すと、パイプラインのすべてのステップが単一のデータベース トランザクション内で自動的にラップされます。

```php
$user = Pipeline::send($user)
    ->withinTransaction()
    ->through([
        ProcessOrder::class,
        TransferFunds::class,
        UpdateInventory::class,
    ])
    ->thenReturn();
```

<a name="sleep"></a>
### 寝る

Laravel の `Sleep` クラスは、PHP のネイティブ `sleep` および `usleep` 関数の軽量ラッパーであり、より優れたテスト容易性を提供すると同時に、時間を扱うための開発者に優しい API を公開します。

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` クラスは、さまざまな時間単位を操作できるさまざまなメソッドを提供します。

```php
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
Sleep::until(now()->plus(minutes: 1));

// Alias of PHP's native "sleep" function...
Sleep::sleep(2);

// Alias of PHP's native "usleep" function...
Sleep::usleep(5000);
```

時間の単位を簡単に組み合わせるには、`and` メソッドを使用できます。

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### 睡眠のテスト

`Sleep` クラスまたは PHP のネイティブ スリープ関数を利用するコードをテストする場合、テストは実行を一時停止します。ご想像のとおり、これによりテスト スイートが大幅に遅くなります。たとえば、次のコードをテストしていると想像してください。

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

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

`Sleep` クラスを偽装すると、実際の実行一時停止がバイパスされ、テストが大幅に高速化されます。

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

もちろん、`Sleep` クラスは、テスト時に使用できる他のさまざまなアサーションを提供します。

```php
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

場合によっては、偽の睡眠が発生するたびにアクションを実行すると便利な場合があります。これを実現するには、`whenFakingSleep` メソッドへのコールバックを提供できます。次の例では、Laravel の [時間操作ヘルパ](/docs/{{version}}/mocking#interacting-with-time) を使用して、各スリープの継続時間ごとに時間を瞬時に進めます。

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // Progress time when faking sleep...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

進行時間は一般的な要件であるため、`fake` メソッドは `syncWithCarbon` 引数を受け入れて、テスト内でスリープしているときに Carbon の同期を維持します。

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

Laravel は、実行を一時停止するたびに、内部で `Sleep` クラスを使用します。たとえば、[retry](#method-retry) ヘルパはスリープ時に `Sleep` クラスを使用するため、そのヘルパを使用する際のテスト容易性が向上します。

<a name="timebox"></a>
### タイムボックス

Laravel の `Timebox` クラスは、実際の実行がもっと早く完了する場合でも、指定されたコールバックの実行には常に一定の時間がかかることを保証します。これは、攻撃者が実行時間の変動を利用して機密情報を推測する可能性がある暗号操作やユーザー認証チェックに特に役立ちます。

実行が固定期間を超えた場合、`Timebox` は効果がありません。最悪のシナリオを考慮して十分に長い時間を固定期間として選択するかどうかは開発者次第です。

call メソッドはクロージャとマイクロ秒単位の時間制限を受け入れ、クロージャを実行して時間制限に達するまで待機します。

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

クロージャ内で例外がスローされた場合、このクラスは定義された遅延を尊重し、遅延後に例外を再スローします。

<a name="uri"></a>
### URI

Laravel の `Uri` クラスは、URI を作成および操作するための便利で流暢なインターフェイスを提供します。このクラスは、基礎となる League URI パッケージによって提供される機能をラップし、Laravel のルーティング システムとシームレスに統合します。

静的メソッドを使用して、`Uri` インスタンスを簡単に作成できます。

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// Generate a URI instance from the given string...
$uri = Uri::of('https://example.com/path');

// Generate URI instances to paths, named routes, or controller actions...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// Generate a URI instance from the current request URL...
$uri = $request->uri();
```

URI インスタンスを取得したら、それをスムーズに変更できます。

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

<a name="inspecting-uris"></a>
#### URIの検査

`Uri` クラスを使用すると、基になる URI のさまざまなコンポーネントを簡単に検査することもできます。

```php
$scheme = $uri->scheme();
$authority = $uri->authority();
$host = $uri->host();
$port = $uri->port();
$path = $uri->path();
$segments = $uri->pathSegments();
$query = $uri->query();
$fragment = $uri->fragment();
```

<a name="manipulating-query-strings"></a>
#### クエリ文字列の操作

`Uri` クラスは、URI のクエリ文字列を操作するために使用できるいくつかのメソッドを提供します。 `withQuery` メソッドを使用して、追加のクエリ文字列パラメータを既存のクエリ文字列にマージできます。

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

指定されたキーがクエリ文字列にまだ存在しない場合、`withQueryIfMissing` メソッドを使用して、追加のクエリ文字列パラメータを既存のクエリ文字列にマージできます。

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery` メソッドを使用して、既存のクエリ文字列を新しいクエリ文字列に完全に置き換えることができます。

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery` メソッドは、配列値を持つクエリ文字列パラメータに追加のパラメータをプッシュするために使用できます。

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery` メソッドは、クエリ文字列からパラメータを削除するために使用できます。

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI からの応答の生成

`redirect` メソッドを使用して、指定された URI に `RedirectResponse` インスタンスを生成できます。

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

または、単にルートまたはコントローラ アクションから `Uri` インスタンスを返すこともできます。これにより、返された URI へのリダイレクト応答が自動的に生成されます。

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```

