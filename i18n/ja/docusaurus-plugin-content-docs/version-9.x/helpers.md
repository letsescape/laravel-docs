# ヘルパ (Helpers)

- [Introduction](#introduction)
- [利用可能な方法](#available-methods)
- [その他のユーティリティ](#other-utilities)
    - [Benchmarking](#benchmarking)
    - [Lottery](#lottery)

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
### パス

<div class="collection-method-list" markdown="1">

[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[mix](#method-mix)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

</div>

<a name="strings-method-list"></a>
### 文字列

<div class="collection-method-list" markdown="1">

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

</div>

<a name="fluent-strings-method-list"></a>
### 流暢な文字列

<div class="collection-method-list" markdown="1">

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

</div>

<a name="urls-method-list"></a>
### URL

<div class="collection-method-list" markdown="1">

[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_route](#method-to-route)
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

</div>

<a name="method-listing"></a>
## メソッドリスト (Method Listing)

<style>
    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="arrays"></a>
## 配列とオブジェクト (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()` {.collection-method .first-collection-method}

`Arr::accessible` メソッドは、指定された値が配列にアクセスできるかどうかを判断します。

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

<a name="method-array-add"></a>
#### `Arr::add()` {.collection-method}

`Arr::add` メソッドは、指定されたキーが配列内に存在しない場合、または `null` に設定されている場合に、指定されたキーと値のペアを配列に追加します。

    use Illuminate\Support\Arr;

    $array = Arr::add(['name' => 'Desk'], 'price', 100);

    // ['name' => 'Desk', 'price' => 100]

    $array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

    // ['name' => 'Desk', 'price' => 100]


<a name="method-array-collapse"></a>
#### `Arr::collapse()` {.collection-method}

`Arr::collapse` メソッドは、配列の配列を単一の配列に折りたたみます。

    use Illuminate\Support\Arr;

    $array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

    // [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()` {.collection-method}

`Arr::crossJoin` メソッドは、指定された配列を相互結合し、すべての可能な順列を含むデカルト積を返します。

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

<a name="method-array-divide"></a>
#### `Arr::divide()` {.collection-method}

`Arr::divide` メソッドは 2 つの配列を返します。1 つはキーを含み、もう 1 つは指定された配列の値を含みます。

    use Illuminate\Support\Arr;

    [$keys, $values] = Arr::divide(['name' => 'Desk']);

    // $keys: ['name']

    // $values: ['Desk']

<a name="method-array-dot"></a>
#### `Arr::dot()` {.collection-method}

`Arr::dot` メソッドは、多次元配列を、深さを示すために「ドット」表記を使用する単一レベルの配列に平坦化します。

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    $flattened = Arr::dot($array);

    // ['products.desk.price' => 100]

<a name="method-array-except"></a>
#### `Arr::except()` {.collection-method}

`Arr::except` メソッドは、指定されたキーと値のペアを配列から削除します。

    use Illuminate\Support\Arr;

    $array = ['name' => 'Desk', 'price' => 100];

    $filtered = Arr::except($array, ['price']);

    // ['name' => 'Desk']

<a name="method-array-exists"></a>
#### `Arr::exists()` {.collection-method}

`Arr::exists` メソッドは、指定されたキーが指定された配列に存在することを確認します。

    use Illuminate\Support\Arr;

    $array = ['name' => 'John Doe', 'age' => 17];

    $exists = Arr::exists($array, 'name');

    // true

    $exists = Arr::exists($array, 'salary');

    // false

<a name="method-array-first"></a>
#### `Arr::first()` {.collection-method}

`Arr::first` メソッドは、指定された真理値テストに合格した配列の最初の要素を返します。

    use Illuminate\Support\Arr;

    $array = [100, 200, 300];

    $first = Arr::first($array, function ($value, $key) {
        return $value >= 150;
    });

    // 200

デフォルト値を 3 番目のパラメータとしてメソッドに渡すこともできます。真実テストに合格する値がない場合、この値が返されます。

    use Illuminate\Support\Arr;

    $first = Arr::first($array, $callback, $default);

<a name="method-array-flatten"></a>
#### `Arr::flatten()` {.collection-method}

`Arr::flatten` メソッドは、多次元配列を単一レベルの配列にフラット化します。

    use Illuminate\Support\Arr;

    $array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

    $flattened = Arr::flatten($array);

    // ['Joe', 'PHP', 'Ruby']

<a name="method-array-forget"></a>
#### `Arr::forget()` {.collection-method}

`Arr::forget` メソッドは、「ドット」表記を使用して、深くネストされた配列から指定されたキーと値のペアを削除します。

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    Arr::forget($array, 'products.desk');

    // ['products' => []]

<a name="method-array-get"></a>
#### `Arr::get()` {.collection-method}

`Arr::get` メソッドは、「ドット」表記を使用して、深くネストされた配列から値を取得します。

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    $price = Arr::get($array, 'products.desk.price');

    // 100

`Arr::get` メソッドは、指定されたキーが配列に存在しない場合に返されるデフォルト値も受け入れます。

    use Illuminate\Support\Arr;

    $discount = Arr::get($array, 'products.desk.discount', 0);

    // 0

<a name="method-array-has"></a>
#### `Arr::has()` {.collection-method}

`Arr::has` メソッドは、「ドット」表記を使用して、指定された項目が配列内に存在するかどうかをチェックします。

    use Illuminate\Support\Arr;

    $array = ['product' => ['name' => 'Desk', 'price' => 100]];

    $contains = Arr::has($array, 'product.name');

    // true

    $contains = Arr::has($array, ['product.price', 'product.discount']);

    // false

<a name="method-array-hasany"></a>
#### `Arr::hasAny()` {.collection-method}

`Arr::hasAny` メソッドは、「ドット」表記を使用して、指定されたセット内の項目が配列内に存在するかどうかをチェックします。

    use Illuminate\Support\Arr;

    $array = ['product' => ['name' => 'Desk', 'price' => 100]];

    $contains = Arr::hasAny($array, 'product.name');

    // true

    $contains = Arr::hasAny($array, ['product.name', 'product.discount']);

    // true

    $contains = Arr::hasAny($array, ['category', 'product.discount']);

    // false

<a name="method-array-isassoc"></a>
#### `Arr::isAssoc()` {.collection-method}

指定された配列が連想配列の場合、`Arr::isAssoc` メソッドは `true` を返します。配列にゼロで始まる連続した数値キーがない場合、その配列は「結合」とみなされます。

    use Illuminate\Support\Arr;

    $isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

    // true

    $isAssoc = Arr::isAssoc([1, 2, 3]);

    // false

<a name="method-array-islist"></a>
#### `Arr::isList()` {.collection-method}

指定された配列のキーがゼロから始まる連続した整数の場合、`Arr::isList` メソッドは `true` を返します。

    use Illuminate\Support\Arr;

    $isList = Arr::isList(['foo', 'bar', 'baz']);

    // true

    $isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

    // false

<a name="method-array-join"></a>
#### `Arr::join()` {.collection-method}

`Arr::join` メソッドは、配列要素を文字列と結合します。このメソッドの 2 番目の引数を使用して、配列の最後の要素の結合文字列を指定することもできます。

    use Illuminate\Support\Arr;

    $array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

    $joined = Arr::join($array, ', ');

    // Tailwind, Alpine, Laravel, Livewire

    $joined = Arr::join($array, ', ', ' and ');

    // Tailwind, Alpine, Laravel and Livewire

<a name="method-array-keyby"></a>
#### `Arr::keyBy()` {.collection-method}

`Arr::keyBy` メソッドは、指定されたキーによって配列にキーを設定します。複数の項目が同じキーを持つ場合、最後の項目だけが新しい配列に表示されます。

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

<a name="method-array-last"></a>
#### `Arr::last()` {.collection-method}

`Arr::last` メソッドは、指定された真理値テストに合格した配列の最後の要素を返します。

    use Illuminate\Support\Arr;

    $array = [100, 200, 300, 110];

    $last = Arr::last($array, function ($value, $key) {
        return $value >= 150;
    });

    // 300

デフォルト値は、メソッドの 3 番目の引数として渡すことができます。真実テストに合格する値がない場合、この値が返されます。

    use Illuminate\Support\Arr;

    $last = Arr::last($array, $callback, $default);

<a name="method-array-map"></a>
#### `Arr::map()` {.collection-method}

`Arr::map` メソッドは配列を反復処理し、各値とキーを指定されたコールバックに渡します。配列の値は、コールバックによって返される値に置き換えられます。

    use Illuminate\Support\Arr;

    $array = ['first' => 'james', 'last' => 'kirk'];

    $mapped = Arr::map($array, function ($value, $key) {
        return ucfirst($value);
    });

    // ['first' => 'James', 'last' => 'Kirk']

<a name="method-array-only"></a>
#### `Arr::only()` {.collection-method}

`Arr::only` メソッドは、指定された配列から指定されたキーと値のペアのみを返します。

    use Illuminate\Support\Arr;

    $array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

    $slice = Arr::only($array, ['name', 'price']);

    // ['name' => 'Desk', 'price' => 100]

<a name="method-array-pluck"></a>
#### `Arr::pluck()` {.collection-method}

`Arr::pluck` メソッドは、配列から指定されたキーのすべての値を取得します。

    use Illuminate\Support\Arr;

    $array = [
        ['developer' => ['id' => 1, 'name' => 'Taylor']],
        ['developer' => ['id' => 2, 'name' => 'Abigail']],
    ];

    $names = Arr::pluck($array, 'developer.name');

    // ['Taylor', 'Abigail']

結果のリストにどのようにキーを設定するかを指定することもできます。

    use Illuminate\Support\Arr;

    $names = Arr::pluck($array, 'developer.name', 'developer.id');

    // [1 => 'Taylor', 2 => 'Abigail']

<a name="method-array-prepend"></a>
#### `Arr::prepend()` {.collection-method}

`Arr::prepend` メソッドは、項目を配列の先頭にプッシュします。

    use Illuminate\Support\Arr;

    $array = ['one', 'two', 'three', 'four'];

    $array = Arr::prepend($array, 'zero');

    // ['zero', 'one', 'two', 'three', 'four']

必要に応じて、値に使用するキーを指定できます。

    use Illuminate\Support\Arr;

    $array = ['price' => 100];

    $array = Arr::prepend($array, 'Desk', 'name');

    // ['name' => 'Desk', 'price' => 100]

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()` {.collection-method}

`Arr::prependKeysWith` は、連想配列のすべてのキー名の前に指定されたプレフィックスを付加します。

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

<a name="method-array-pull"></a>
#### `Arr::pull()` {.collection-method}

`Arr::pull` メソッドは、キーと値のペアを返し、配列から削除します。

    use Illuminate\Support\Arr;

    $array = ['name' => 'Desk', 'price' => 100];

    $name = Arr::pull($array, 'name');

    // $name: Desk

    // $array: ['price' => 100]

デフォルト値は、メソッドの 3 番目の引数として渡すことができます。キーが存在しない場合は、この値が返されます。

    use Illuminate\Support\Arr;

    $value = Arr::pull($array, $key, $default);

<a name="method-array-query"></a>
#### `Arr::query()` {.collection-method}

`Arr::query` メソッドは、配列をクエリ文字列に変換します。

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

<a name="method-array-random"></a>
#### `Arr::random()` {.collection-method}

`Arr::random` メソッドは、配列からランダムな値を返します。

    use Illuminate\Support\Arr;

    $array = [1, 2, 3, 4, 5];

    $random = Arr::random($array);

    // 4 - (retrieved randomly)

オプションの 2 番目の引数として、返す項目の数を指定することもできます。この引数を指定すると、必要な項目が 1 つだけの場合でも配列が返されることに注意してください。

    use Illuminate\Support\Arr;

    $items = Arr::random($array, 2);

    // [2, 5] - (retrieved randomly)

<a name="method-array-set"></a>
#### `Arr::set()` {.collection-method}

`Arr::set` メソッドは、「ドット」表記を使用して、深くネストされた配列内の値を設定します。

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    Arr::set($array, 'products.desk.price', 200);

    // ['products' => ['desk' => ['price' => 200]]]

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()` {.collection-method}

`Arr::shuffle` メソッドは、配列内の項目をランダムにシャッフルします。

    use Illuminate\Support\Arr;

    $array = Arr::shuffle([1, 2, 3, 4, 5]);

    // [3, 2, 5, 1, 4] - (generated randomly)

<a name="method-array-sort"></a>
#### `Arr::sort()` {.collection-method}

`Arr::sort` メソッドは、配列を値で並べ替えます。

    use Illuminate\Support\Arr;

    $array = ['Desk', 'Table', 'Chair'];

    $sorted = Arr::sort($array);

    // ['Chair', 'Desk', 'Table']

特定のクロージャの結果によって配列を並べ替えることもできます。

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

<a name="method-array-sort-desc"></a>
#### `Arr::sortDesc()` {.collection-method}

`Arr::sortDesc` メソッドは、配列を値の降順に並べ替えます。

    use Illuminate\Support\Arr;

    $array = ['Desk', 'Table', 'Chair'];

    $sorted = Arr::sortDesc($array);

    // ['Table', 'Desk', 'Chair']

特定のクロージャの結果によって配列を並べ替えることもできます。

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

<a name="method-array-sort-recursive"></a>
#### `Arr::sortRecursive()` {.collection-method}

`Arr::sortRecursive` メソッドは、数値インデックス付きサブ配列の場合は `sort` 関数を使用し、連想サブ配列の場合は `ksort` 関数を使用して、配列を再帰的に並べ替えます。

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

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()` {.collection-method}

`Arr::toCssClasses` は、CSS クラス文字列を条件付きでコンパイルします。このメソッドはクラスの配列を受け入れます。配列キーには追加するクラスが含まれ、値はブール式です。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

    use Illuminate\Support\Arr;

    $isActive = false;
    $hasError = true;

    $array = ['p-4', 'font-bold' => $isActive, 'bg-red' => $hasError];

    $classes = Arr::toCssClasses($array);

    /*
        'p-4 bg-red'
    */

このメソッドは、Laravel の機能を強化し、[クラスを Blade コンポーネントの属性バッグと結合する](/docs/{{version}}/blade#conditionally-merge-classes) および `@class` [Blade ディレクティブ](/docs/{{version}}/blade#conditional-classes) を許可します。

<a name="method-array-undot"></a>
#### `Arr::undot()` {.collection-method}

`Arr::undot` メソッドは、「ドット」表記を使用する 1 次元配列を多次元配列に拡張します。

    use Illuminate\Support\Arr;

    $array = [
        'user.name' => 'Kevin Malone',
        'user.occupation' => 'Accountant',
    ];

    $array = Arr::undot($array);

    // ['user' => ['name' => 'Kevin Malone', 'occupation' => 'Accountant']]

<a name="method-array-where"></a>
#### `Arr::where()` {.collection-method}

`Arr::where` メソッドは、指定されたクロージャを使用して配列をフィルタリングします。

    use Illuminate\Support\Arr;

    $array = [100, '200', 300, '400', 500];

    $filtered = Arr::where($array, function ($value, $key) {
        return is_string($value);
    });

    // [1 => '200', 3 => '400']

<a name="method-array-where-not-null"></a>
#### `Arr::whereNotNull()` {.collection-method}

`Arr::whereNotNull` メソッドは、指定された配列からすべての `null` 値を削除します。

    use Illuminate\Support\Arr;

    $array = [0, null];

    $filtered = Arr::whereNotNull($array);

    // [0 => 0]

<a name="method-array-wrap"></a>
#### `Arr::wrap()` {.collection-method}

`Arr::wrap` メソッドは、指定された値を配列にラップします。指定された値がすでに配列である場合は、変更せずに返されます。

    use Illuminate\Support\Arr;

    $string = 'Laravel';

    $array = Arr::wrap($string);

    // ['Laravel']

指定された値が `null` の場合、空の配列が返されます。

    use Illuminate\Support\Arr;

    $array = Arr::wrap(null);

    // []

<a name="method-data-fill"></a>
#### `data_fill()` {.collection-method}

`data_fill` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の欠損値を設定します。

    $data = ['products' => ['desk' => ['price' => 100]]];

    data_fill($data, 'products.desk.price', 200);

    // ['products' => ['desk' => ['price' => 100]]]

    data_fill($data, 'products.desk.discount', 10);

    // ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]

この関数はワイルドカードとしてアスタリスクも受け入れ、それに応じてターゲットを入力します。

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

<a name="method-data-get"></a>
#### `data_get()` {.collection-method}

`data_get` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクトから値を取得します。

    $data = ['products' => ['desk' => ['price' => 100]]];

    $price = data_get($data, 'products.desk.price');

    // 100

`data_get` 関数は、指定されたキーが見つからない場合に返されるデフォルト値も受け入れます。

    $discount = data_get($data, 'products.desk.discount', 0);

    // 0

この関数は、配列またはオブジェクトの任意のキーを対象とするアスタリスクを使用したワイルドカードも受け入れます。

    $data = [
        'product-one' => ['name' => 'Desk 1', 'price' => 100],
        'product-two' => ['name' => 'Desk 2', 'price' => 150],
    ];

    data_get($data, '*.name');

    // ['Desk 1', 'Desk 2'];

<a name="method-data-set"></a>
#### `data_set()` {.collection-method}

`data_set` 関数は、「ドット」表記を使用して、ネストされた配列またはオブジェクト内の値を設定します。

    $data = ['products' => ['desk' => ['price' => 100]]];

    data_set($data, 'products.desk.price', 200);

    // ['products' => ['desk' => ['price' => 200]]]

この関数はアスタリスクを使用したワイルドカードも受け入れ、それに応じてターゲットに値を設定します。

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

デフォルトでは、既存の値はすべて上書きされます。値が存在しない場合にのみ値を設定したい場合は、関数の 4 番目の引数として `false` を渡すことができます。

    $data = ['products' => ['desk' => ['price' => 100]]];

    data_set($data, 'products.desk.price', 200, overwrite: false);

    // ['products' => ['desk' => ['price' => 100]]]

<a name="method-head"></a>
#### `head()` {.collection-method}

`head` 関数は、指定された配列の最初の要素を返します。

    $array = [100, 200, 300];

    $first = head($array);

    // 100

<a name="method-last"></a>
#### `last()` {.collection-method}

`last` 関数は、指定された配列の最後の要素を返します。

    $array = [100, 200, 300];

    $last = last($array);

    // 300

<a name="paths"></a>
## パス (Paths)

<a name="method-app-path"></a>
#### `app_path()` {.collection-method}

`app_path` 関数は、アプリケーションの `app` ディレクトリへの完全修飾パスを返します。 `app_path` 関数を使用して、アプリケーション ディレクトリを基準としたファイルへの完全修飾パスを生成することもできます。

    $path = app_path();

    $path = app_path('Http/Controllers/Controller.php');

<a name="method-base-path"></a>
#### `base_path()` {.collection-method}

`base_path` 関数は、アプリケーションのルート ディレクトリへの完全修飾パスを返します。 `base_path` 関数を使用して、プロジェクトのルート ディレクトリを基準とした特定のファイルへの完全修飾パスを生成することもできます。

    $path = base_path();

    $path = base_path('vendor/bin');

<a name="method-config-path"></a>
#### `config_path()` {.collection-method}

`config_path` 関数は、アプリケーションの `config` ディレクトリへの完全修飾パスを返します。 `config_path` 関数を使用して、アプリケーションの構成ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

    $path = config_path();

    $path = config_path('app.php');

<a name="method-database-path"></a>
#### `database_path()` {.collection-method}

`database_path` 関数は、アプリケーションの `database` ディレクトリへの完全修飾パスを返します。 `database_path` 関数を使用して、データベース ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

    $path = database_path();

    $path = database_path('factories/UserFactory.php');

<a name="method-lang-path"></a>
#### `lang_path()` {.collection-method}

`lang_path` 関数は、アプリケーションの `lang` ディレクトリへの完全修飾パスを返します。 `lang_path` 関数を使用して、ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

    $path = lang_path();

    $path = lang_path('en/messages.php');

<a name="method-mix"></a>
#### `mix()` {.collection-method}

`mix` 関数は、[バージョン管理されたMix ファイル](/docs/{{version}}/mix) へのパスを返します。

    $path = mix('css/app.css');

<a name="method-public-path"></a>
#### `public_path()` {.collection-method}

`public_path` 関数は、アプリケーションの `public` ディレクトリへの完全修飾パスを返します。 `public_path` 関数を使用して、パブリック ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

    $path = public_path();

    $path = public_path('css/app.css');

<a name="method-resource-path"></a>
#### `resource_path()` {.collection-method}

`resource_path` 関数は、アプリケーションの `resources` ディレクトリへの完全修飾パスを返します。 `resource_path` 関数を使用して、リソース ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

    $path = resource_path();

    $path = resource_path('sass/app.scss');

<a name="method-storage-path"></a>
#### `storage_path()` {.collection-method}

`storage_path` 関数は、アプリケーションの `storage` ディレクトリへの完全修飾パスを返します。 `storage_path` 関数を使用して、ストレージ ディレクトリ内の特定のファイルへの完全修飾パスを生成することもできます。

    $path = storage_path();

    $path = storage_path('app/file.txt');

<a name="strings"></a>
## 文字列 (Strings)

<a name="method-__"></a>
#### `__()` {.collection-method}

`__` 関数は、[ローカリゼーションファイル](/docs/{{version}}/localization) を使用して、指定された翻訳文字列または翻訳キーを翻訳します。

    echo __('Welcome to our application');

    echo __('messages.welcome');

指定された変換文字列またはキーが存在しない場合、`__` 関数は指定された値を返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`__` 関数は `messages.welcome` を返します。

<a name="method-class-basename"></a>
#### `class_basename()` {.collection-method}

`class_basename` 関数は、クラスの名前空間が削除された、指定されたクラスのクラス名を返します。

    $class = class_basename('Foo\Bar\Baz');

    // Baz

<a name="method-e"></a>
#### `e()` {.collection-method}

`e` 関数は、デフォルトで `double_encode` オプションを `true` に設定して、PHP の `htmlspecialchars` 関数を実行します。

    echo e('<html>foo</html>');

    // &lt;html&gt;foo&lt;/html&gt;

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()` {.collection-method}

`preg_replace_array` 関数は、配列を使用して文字列内の指定されたパターンを順番に置き換えます。

    $string = 'The event will take place between :start and :end';

    $replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

    // The event will take place between 8:30 and 9:00

<a name="method-str-after"></a>
#### `Str::after()` {.collection-method}

`Str::after` メソッドは、文字列内の指定された値以降のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

    use Illuminate\Support\Str;

    $slice = Str::after('This is my name', 'This is');

    // ' my name'

<a name="method-str-after-last"></a>
#### `Str::afterLast()` {.collection-method}

`Str::afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

    use Illuminate\Support\Str;

    $slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

    // 'Controller'

<a name="method-str-ascii"></a>
#### `Str::ascii()` {.collection-method}

`Str::ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

    use Illuminate\Support\Str;

    $slice = Str::ascii('û');

    // 'u'

<a name="method-str-before"></a>
#### `Str::before()` {.collection-method}

`Str::before` メソッドは、文字列内の指定された値より前のすべてを返します。

    use Illuminate\Support\Str;

    $slice = Str::before('This is my name', 'my name');

    // 'This is '

<a name="method-str-before-last"></a>
#### `Str::beforeLast()` {.collection-method}

`Str::beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

    use Illuminate\Support\Str;

    $slice = Str::beforeLast('This is my name', 'is');

    // 'This '

<a name="method-str-between"></a>
#### `Str::between()` {.collection-method}

`Str::between` メソッドは、2 つの値の間の文字列の部分を返します。

    use Illuminate\Support\Str;

    $slice = Str::between('This is my name', 'This', 'name');

    // ' is my '

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()` {.collection-method}

`Str::betweenFirst` メソッドは、2 つの値の間の文字列の可能な最小部分を返します。

    use Illuminate\Support\Str;

    $slice = Str::betweenFirst('[a] bc [d]', '[', ']');

    // 'a'

<a name="method-camel-case"></a>
#### `Str::camel()` {.collection-method}

`Str::camel` メソッドは、指定された文字列を `camelCase` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::camel('foo_bar');

    // fooBar

<a name="method-str-contains"></a>
#### `Str::contains()` {.collection-method}

`Str::contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。このメソッドでは大文字と小文字が区別されます。

    use Illuminate\Support\Str;

    $contains = Str::contains('This is my name', 'my');

    // true

値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

    use Illuminate\Support\Str;

    $contains = Str::contains('This is my name', ['my', 'foo']);

    // true

<a name="method-str-contains-all"></a>
#### `Str::containsAll()` {.collection-method}

`Str::containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

    use Illuminate\Support\Str;

    $containsAll = Str::containsAll('This is my name', ['my', 'name']);

    // true

<a name="method-ends-with"></a>
#### `Str::endsWith()` {.collection-method}

`Str::endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::endsWith('This is my name', 'name');

    // true


値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

    use Illuminate\Support\Str;

    $result = Str::endsWith('This is my name', ['name', 'foo']);

    // true

    $result = Str::endsWith('This is my name', ['this', 'foo']);

    // false

<a name="method-excerpt"></a>
#### `Str::excerpt()` {.collection-method}

`Str::excerpt` メソッドは、指定された文字列から、その文字列内のフレーズの最初のインスタンスに一致する抜粋を抽出します。

    use Illuminate\Support\Str;

    $excerpt = Str::excerpt('This is my name', 'my', [
        'radius' => 3
    ]);

    // '...is my na...'

`radius` オプション (デフォルトは `100`) を使用すると、切り詰められた文字列の両側に表示される文字数を定義できます。

さらに、`omission` オプションを使用して、切り詰められた文字列の前後に追加される文字列を定義できます。

    use Illuminate\Support\Str;

    $excerpt = Str::excerpt('This is my name', 'name', [
        'radius' => 3,
        'omission' => '(...) '
    ]);

    // '(...) my name'

<a name="method-str-finish"></a>
#### `Str::finish()` {.collection-method}

`Str::finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

    use Illuminate\Support\Str;

    $adjusted = Str::finish('this/string', '/');

    // this/string/

    $adjusted = Str::finish('this/string/', '/');

    // this/string/

<a name="method-str-headline"></a>
#### `Str::headline()` {.collection-method}

`Str::headline` メソッドは、大文字と小文字、ハイフン、またはアンダースコアで区切られた文字列を、各単語の最初の文字が大文字になったスペースで区切られた文字列に変換します。

    use Illuminate\Support\Str;

    $headline = Str::headline('steve_jobs');

    // Steve Jobs

    $headline = Str::headline('EmailNotificationSent');

    // Email Notification Sent

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()` {.collection-method}

`Str::inlineMarkdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown をインライン HTML に変換します。ただし、`markdown` メソッドとは異なり、生成されたすべての HTML をブロックレベル要素でラップするわけではありません。

    use Illuminate\Support\Str;

    $html = Str::inlineMarkdown('**Laravel**');

    // <strong>Laravel</strong>

<a name="method-str-is"></a>
#### `Str::is()` {.collection-method}

`Str::is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます。

    use Illuminate\Support\Str;

    $matches = Str::is('foo*', 'foobar');

    // true

    $matches = Str::is('baz*', 'foobar');

    // false

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()` {.collection-method}

`Str::isAscii` メソッドは、指定された文字列が 7 ビット ASCII であるかどうかを判断します。

    use Illuminate\Support\Str;

    $isAscii = Str::isAscii('Taylor');

    // true

    $isAscii = Str::isAscii('ü');

    // false

<a name="method-str-is-json"></a>
#### `Str::isJson()` {.collection-method}

`Str::isJson` メソッドは、指定された文字列が有効な JSON かどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::isJson('[1,2,3]');

    // true

    $result = Str::isJson('{"first": "John", "last": "Doe"}');

    // true

    $result = Str::isJson('{first: "John", last: "Doe"}');

    // false

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()` {.collection-method}

`Str::isUlid` メソッドは、指定された文字列が有効な ULID かどうかを判断します。

    use Illuminate\Support\Str;

    $isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

    // true

    $isUlid = Str::isUlid('laravel');

    // false

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()` {.collection-method}

`Str::isUuid` メソッドは、指定された文字列が有効な UUID かどうかを判断します。

    use Illuminate\Support\Str;

    $isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

    // true

    $isUuid = Str::isUuid('laravel');

    // false

<a name="method-kebab-case"></a>
#### `Str::kebab()` {.collection-method}

`Str::kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::kebab('fooBar');

    // foo-bar

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()` {.collection-method}

`Str::lcfirst` メソッドは、最初の文字を小文字にして指定された文字列を返します。

    use Illuminate\Support\Str;

    $string = Str::lcfirst('Foo Bar');

    // foo Bar

<a name="method-str-length"></a>
#### `Str::length()` {.collection-method}

`Str::length` メソッドは、指定された文字列の長さを返します。

    use Illuminate\Support\Str;

    $length = Str::length('Laravel');

    // 7

<a name="method-str-limit"></a>
#### `Str::limit()` {.collection-method}

`Str::limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

    use Illuminate\Support\Str;

    $truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

    // The quick brown fox...

メソッドに 3 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更できます。

    use Illuminate\Support\Str;

    $truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

    // The quick brown fox (...)

<a name="method-str-lower"></a>
#### `Str::lower()` {.collection-method}

`Str::lower` メソッドは、指定された文字列を小文字に変換します。

    use Illuminate\Support\Str;

    $converted = Str::lower('LARAVEL');

    // laravel

<a name="method-str-markdown"></a>
#### `Str::markdown()` {.collection-method}

`Str::markdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown を HTML に変換します。

    use Illuminate\Support\Str;

    $html = Str::markdown('# Laravel');

    // <h1>Laravel</h1>

    $html = Str::markdown('# Taylor <b>Otwell</b>', [
        'html_input' => 'strip',
    ]);

    // <h1>Taylor Otwell</h1>

<a name="method-str-mask"></a>
#### `Str::mask()` {.collection-method}

`Str::mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

    use Illuminate\Support\Str;

    $string = Str::mask('taylor@example.com', '*', 3);

    // tay***************

必要に応じて、`mask` メソッドの 3 番目の引数として負の数値を指定します。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

    $string = Str::mask('taylor@example.com', '*', -15, 3);

    // tay***@example.com

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()` {.collection-method}

`Str::orderedUuid` メソッドは、インデックス付きデータベース列に効率的に格納できる「タイムスタンプ優先」の UUID を生成します。このメソッドを使用して生成された各 UUID は、以前に次のメソッドを使用して生成された UUID の後にソートされます。

    use Illuminate\Support\Str;

    return (string) Str::orderedUuid();

<a name="method-str-padboth"></a>
#### `Str::padBoth()` {.collection-method}

`Str::padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

    use Illuminate\Support\Str;

    $padded = Str::padBoth('James', 10, '_');

    // '__James___'

    $padded = Str::padBoth('James', 10);

    // '  James   '

<a name="method-str-padleft"></a>
#### `Str::padLeft()` {.collection-method}

`Str::padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

    use Illuminate\Support\Str;

    $padded = Str::padLeft('James', 10, '-=');

    // '-=-=-James'

    $padded = Str::padLeft('James', 10);

    // '     James'

<a name="method-str-padright"></a>
#### `Str::padRight()` {.collection-method}

`Str::padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

    use Illuminate\Support\Str;

    $padded = Str::padRight('James', 10, '-');

    // 'James-----'

    $padded = Str::padRight('James', 10);

    // 'James     '

<a name="method-str-plural"></a>
#### `Str::plural()` {.collection-method}

`Str::plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

    use Illuminate\Support\Str;

    $plural = Str::plural('car');

    // cars

    $plural = Str::plural('child');

    // children

関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

    use Illuminate\Support\Str;

    $plural = Str::plural('child', 2);

    // children

    $singular = Str::plural('child', 1);

    // child

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()` {.collection-method}

`Str::pluralStudly` メソッドは、大文字小文字でフォーマットされた単数形の単語文字列を複数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

    use Illuminate\Support\Str;

    $plural = Str::pluralStudly('VerifiedHuman');

    // VerifiedHumans

    $plural = Str::pluralStudly('UserFeedback');

    // UserFeedback

関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

    use Illuminate\Support\Str;

    $plural = Str::pluralStudly('VerifiedHuman', 2);

    // VerifiedHumans

    $singular = Str::pluralStudly('VerifiedHuman', 1);

    // VerifiedHuman

<a name="method-str-random"></a>
#### `Str::random()` {.collection-method}

`Str::random` メソッドは、指定された長さのランダムな文字列を生成します。この関数は、PHP の `random_bytes` 関数を使用します。

    use Illuminate\Support\Str;

    $random = Str::random(40);

<a name="method-str-remove"></a>
#### `Str::remove()` {.collection-method}

`Str::remove` メソッドは、指定された値または値の配列を文字列から削除します。

    use Illuminate\Support\Str;

    $string = 'Peter Piper picked a peck of pickled peppers.';

    $removed = Str::remove('e', $string);

    // Ptr Pipr pickd a pck of pickld ppprs.

文字列を削除するときに大文字と小文字を区別しないように、`false` を `remove` メソッドの 3 番目の引数として渡すこともできます。

<a name="method-str-replace"></a>
#### `Str::replace()` {.collection-method}

`Str::replace` メソッドは、文字列内の指定された文字列を置き換えます。

    use Illuminate\Support\Str;

    $string = 'Laravel 8.x';

    $replaced = Str::replace('8.x', '9.x', $string);

    // Laravel 9.x

<a name="method-str-replace-array"></a>
#### `Str::replaceArray()` {.collection-method}

`Str::replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

    use Illuminate\Support\Str;

    $string = 'The event will take place between ? and ?';

    $replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

    // The event will take place between 8:30 and 9:00

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()` {.collection-method}

`Str::replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

    use Illuminate\Support\Str;

    $replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

    // a quick brown fox jumps over the lazy dog

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()` {.collection-method}

`Str::replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

    use Illuminate\Support\Str;

    $replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

    // the quick brown fox jumps over a lazy dog


<a name="method-str-reverse"></a>
#### `Str::reverse()` {.collection-method}

`Str::reverse` メソッドは、指定された文字列を反転します。

    use Illuminate\Support\Str;

    $reversed = Str::reverse('Hello World');

    // dlroW olleH

<a name="method-str-singular"></a>
#### `Str::singular()` {.collection-method}

`Str::singular` メソッドは、文字列を単数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

    use Illuminate\Support\Str;

    $singular = Str::singular('cars');

    // car

    $singular = Str::singular('children');

    // child

<a name="method-str-slug"></a>
#### `Str::slug()` {.collection-method}

`Str::slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

    use Illuminate\Support\Str;

    $slug = Str::slug('Laravel 5 Framework', '-');

    // laravel-5-framework

<a name="method-snake-case"></a>
#### `Str::snake()` {.collection-method}

`Str::snake` メソッドは、指定された文字列を `snake_case` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::snake('fooBar');

    // foo_bar

    $converted = Str::snake('fooBar', '-');

    // foo-bar

<a name="method-str-squish"></a>
#### `Str::squish()` {.collection-method}

`Str::squish` メソッドは、単語間の無関係な空白を含め、文字列から無関係な空白をすべて削除します。

    use Illuminate\Support\Str;

    $string = Str::squish('    laravel    framework    ');

    // laravel framework

<a name="method-str-start"></a>
#### `Str::start()` {.collection-method}

`Str::start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

    use Illuminate\Support\Str;

    $adjusted = Str::start('this/string', '/');

    // /this/string

    $adjusted = Str::start('/this/string', '/');

    // /this/string

<a name="method-starts-with"></a>
#### `Str::startsWith()` {.collection-method}

`Str::startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::startsWith('This is my name', 'This');

    // true

可能な値の配列が渡された場合、文字列が指定された値のいずれかで始まる場合、`startsWith` メソッドは `true` を返します。

    $result = Str::startsWith('This is my name', ['This', 'That', 'There']);

    // true

<a name="method-studly-case"></a>
#### `Str::studly()` {.collection-method}

`Str::studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::studly('foo_bar');

    // FooBar

<a name="method-str-substr"></a>
#### `Str::substr()` {.collection-method}

`Str::substr` メソッドは、start パラメーターと length パラメーターで指定された文字列の部分を返します。

    use Illuminate\Support\Str;

    $converted = Str::substr('The Laravel Framework', 4, 7);

    // Laravel

<a name="method-str-substrcount"></a>
#### `Str::substrCount()` {.collection-method}

`Str::substrCount` メソッドは、指定された文字列内の指定された値の出現数を返します。

    use Illuminate\Support\Str;

    $count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

    // 2

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()` {.collection-method}

`Str::substrReplace` メソッドは、文字列の一部内のテキストを、3 番目の引数で指定された位置から開始して 4 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 4 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

    use Illuminate\Support\Str;

    $result = Str::substrReplace('1300', ':', 2);
    // 13:

    $result = Str::substrReplace('1300', ':', 2, 0);
    // 13:00

<a name="method-str-swap"></a>
#### `Str::swap()` {.collection-method}

`Str::swap` メソッドは、PHP の `strtr` 関数を使用して、指定された文字列内の複数の値を置き換えます。

    use Illuminate\Support\Str;

    $string = Str::swap([
        'Tacos' => 'Burritos',
        'great' => 'fantastic',
    ], 'Tacos are great!');

    // Burritos are fantastic!

<a name="method-title-case"></a>
#### `Str::title()` {.collection-method}

`Str::title` メソッドは、指定された文字列を `Title Case` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::title('a nice title uses the correct case');

    // A Nice Title Uses The Correct Case

<a name="method-str-to-html-string"></a>
#### `Str::toHtmlString()` {.collection-method}

`Str::toHtmlString` メソッドは、文字列インスタンスを `Illuminate\Support\HtmlString` のインスタンスに変換し、Blade テンプレートに表示される可能性があります。

    use Illuminate\Support\Str;

    $htmlString = Str::of('Nuno Maduro')->toHtmlString();

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()` {.collection-method}

`Str::ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

    use Illuminate\Support\Str;

    $string = Str::ucfirst('foo bar');

    // Foo bar

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()` {.collection-method}

`Str::ucsplit` メソッドは、指定された文字列を大文字ごとに配列に分割します。

    use Illuminate\Support\Str;

    $segments = Str::ucsplit('FooBar');

    // [0 => 'Foo', 1 => 'Bar']

<a name="method-str-upper"></a>
#### `Str::upper()` {.collection-method}

`Str::upper` メソッドは、指定された文字列を大文字に変換します。

    use Illuminate\Support\Str;

    $string = Str::upper('laravel');

    // LARAVEL

<a name="method-str-ulid"></a>
#### `Str::ulid()` {.collection-method}

`Str::ulid` メソッドは ULID を生成します。

    use Illuminate\Support\Str;

    return (string) Str::ulid();
    
    // 01gd6r360bp37zj17nxb55yv40

<a name="method-str-uuid"></a>
#### `Str::uuid()` {.collection-method}

`Str::uuid` メソッドは UUID (バージョン 4) を生成します。

    use Illuminate\Support\Str;

    return (string) Str::uuid();

<a name="method-str-word-count"></a>
#### `Str::wordCount()` {.collection-method}

`Str::wordCount` メソッドは、文字列に含まれる単語の数を返します。

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-words"></a>
#### `Str::words()` {.collection-method}

`Str::words` メソッドは、文字列内の単語数を制限します。追加の文字列を 3 番目の引数を介してこのメ​​ソッドに渡し、切り詰められた文字列の末尾に追加する文字列を指定できます。

    use Illuminate\Support\Str;

    return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

    // Perfectly balanced, as >>>

<a name="method-str"></a>
#### `str()` {.collection-method}

`str` 関数は、指定された文字列の新しい `Illuminate\Support\Stringable` インスタンスを返します。この関数は、`Str::of` メソッドと同等です。

    $string = str('Taylor')->append(' Otwell');

    // 'Taylor Otwell'

`str` 関数に引数が指定されていない場合、関数は `Illuminate\Support\Str` のインスタンスを返します。

    $snake = str()->snake('FooBar');

    // 'foo_bar'

<a name="method-trans"></a>
#### `trans()` {.collection-method}

`trans` 関数は、[ローカリゼーションファイル](/docs/{{version}}/localization) を使用して、指定された変換キーを変換します。

    echo trans('messages.welcome');

指定された変換キーが存在しない場合、`trans` 関数は指定されたキーを返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`trans` 関数は `messages.welcome` を返します。

<a name="method-trans-choice"></a>
#### `trans_choice()` {.collection-method}

`trans_choice` 関数は、指定された変換キーを語形変化を使用して変換します。

    echo trans_choice('messages.notifications', $unreadCount);

指定された変換キーが存在しない場合、`trans_choice` 関数は指定されたキーを返します。したがって、上記の例を使用すると、変換キーが存在しない場合、`trans_choice` 関数は `messages.notifications` を返します。

<a name="fluent-strings"></a>
## 流暢な文字列 (Fluent Strings)

Fluent String は、文字列値を操作するためのより流暢なオブジェクト指向インターフェイスを提供し、従来の文字列操作と比較して読みやすい構文を使用して複数の文字列操作を連鎖させることができます。

<a name="method-fluent-str-after"></a>
#### `after` {.collection-method}

`after` メソッドは、文字列内の指定された値以降のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

    use Illuminate\Support\Str;

    $slice = Str::of('This is my name')->after('This is');

    // ' my name'

<a name="method-fluent-str-after-last"></a>
#### `afterLast` {.collection-method}

`afterLast` メソッドは、文字列内の指定された値が最後に出現した後のすべてを返します。文字列内に値が存在しない場合は、文字列全体が返されます。

    use Illuminate\Support\Str;

    $slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

    // 'Controller'

<a name="method-fluent-str-append"></a>
#### `append` {.collection-method}

`append` メソッドは、指定された値を文字列に追加します。

    use Illuminate\Support\Str;

    $string = Str::of('Taylor')->append(' Otwell');

    // 'Taylor Otwell'

<a name="method-fluent-str-ascii"></a>
#### `ascii` {.collection-method}

`ascii` メソッドは、文字列を ASCII 値に音訳しようとします。

    use Illuminate\Support\Str;

    $string = Str::of('ü')->ascii();

    // 'u'

<a name="method-fluent-str-basename"></a>
#### `basename` {.collection-method}

`basename` メソッドは、指定された文字列の末尾の名前コンポーネントを返します。

    use Illuminate\Support\Str;

    $string = Str::of('/foo/bar/baz')->basename();

    // 'baz'

必要に応じて、後続コンポーネントから削除される「拡張機能」を指定できます。

    use Illuminate\Support\Str;

    $string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

    // 'baz'

<a name="method-fluent-str-before"></a>
#### `before` {.collection-method}

`before` メソッドは、文字列内の指定された値より前のすべてを返します。

    use Illuminate\Support\Str;

    $slice = Str::of('This is my name')->before('my name');

    // 'This is '

<a name="method-fluent-str-before-last"></a>
#### `beforeLast` {.collection-method}

`beforeLast` メソッドは、文字列内の指定された値が最後に出現するまでのすべてを返します。

    use Illuminate\Support\Str;

    $slice = Str::of('This is my name')->beforeLast('is');

    // 'This '

<a name="method-fluent-str-between"></a>
#### `between` {.collection-method}

`between` メソッドは、2 つの値の間の文字列の部分を返します。

    use Illuminate\Support\Str;

    $converted = Str::of('This is my name')->between('This', 'name');

    // ' is my '

<a name="method-fluent-str-between-first"></a>
#### `betweenFirst` {.collection-method}

`betweenFirst` メソッドは、2 つの値の間の文字列の可能な最小部分を返します。

    use Illuminate\Support\Str;

    $converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

    // 'a'

<a name="method-fluent-str-camel"></a>
#### `camel` {.collection-method}

`camel` メソッドは、指定された文字列を `camelCase` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::of('foo_bar')->camel();

    // fooBar

<a name="method-fluent-str-class-basename"></a>
#### `classBasename` {.collection-method}

`classBasename` メソッドは、クラスの名前空間が削除された、指定されたクラスのクラス名を返します。

    use Illuminate\Support\Str;

    $class = Str::of('Foo\Bar\Baz')->classBasename();

    // Baz

<a name="method-fluent-str-contains"></a>
#### `contains` {.collection-method}

`contains` メソッドは、指定された文字列に指定された値が含まれているかどうかを判断します。このメソッドでは大文字と小文字が区別されます。

    use Illuminate\Support\Str;

    $contains = Str::of('This is my name')->contains('my');

    // true

値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

    use Illuminate\Support\Str;

    $contains = Str::of('This is my name')->contains(['my', 'foo']);

    // true

<a name="method-fluent-str-contains-all"></a>
#### `containsAll` {.collection-method}

`containsAll` メソッドは、指定された文字列に指定された配列内のすべての値が含まれているかどうかを判断します。

    use Illuminate\Support\Str;

    $containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

    // true

<a name="method-fluent-str-dirname"></a>
#### `dirname` {.collection-method}

`dirname` メソッドは、指定された文字列の親ディレクトリ部分を返します。

    use Illuminate\Support\Str;

    $string = Str::of('/foo/bar/baz')->dirname();

    // '/foo/bar'

必要に応じて、文字列から削除するディレクトリ レベルの数を指定できます。

    use Illuminate\Support\Str;

    $string = Str::of('/foo/bar/baz')->dirname(2);

    // '/foo'

<a name="method-fluent-str-excerpt"></a>
#### `excerpt` {.collection-method}

`excerpt` メソッドは、文字列内のフレーズの最初のインスタンスに一致する文字列からの抜粋を抽出します。

    use Illuminate\Support\Str;

    $excerpt = Str::of('This is my name')->excerpt('my', [
        'radius' => 3
    ]);

    // '...is my na...'

`radius` オプション (デフォルトは `100`) を使用すると、切り詰められた文字列の両側に表示される文字数を定義できます。

さらに、`omission` オプションを使用して、切り詰められた文字列の前後に追加される文字列を変更することもできます。

    use Illuminate\Support\Str;

    $excerpt = Str::of('This is my name')->excerpt('name', [
        'radius' => 3,
        'omission' => '(...) '
    ]);

    // '(...) my name'

<a name="method-fluent-str-ends-with"></a>
#### `endsWith` {.collection-method}

`endsWith` メソッドは、指定された文字列が指定された値で終わるかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('This is my name')->endsWith('name');

    // true

値の配列を渡して、指定された文字列が配列内のいずれかの値で終わるかどうかを判断することもできます。

    use Illuminate\Support\Str;

    $result = Str::of('This is my name')->endsWith(['name', 'foo']);

    // true

    $result = Str::of('This is my name')->endsWith(['this', 'foo']);

    // false

<a name="method-fluent-str-exactly"></a>
#### `exactly` {.collection-method}

`exactly` メソッドは、指定された文字列が別の文字列と完全に一致するかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('Laravel')->exactly('Laravel');

    // true

<a name="method-fluent-str-explode"></a>
#### `explode` {.collection-method}

`explode` メソッドは、指定された区切り文字で文字列を分割し、分割された文字列の各セクションを含むコレクションを返します。

    use Illuminate\Support\Str;

    $collection = Str::of('foo bar baz')->explode(' ');

    // collect(['foo', 'bar', 'baz'])

<a name="method-fluent-str-finish"></a>
#### `finish` {.collection-method}

`finish` メソッドは、指定された値の単一インスタンスを文字列に追加します (指定された値で終わっていない場合)。

    use Illuminate\Support\Str;

    $adjusted = Str::of('this/string')->finish('/');

    // this/string/

    $adjusted = Str::of('this/string/')->finish('/');

    // this/string/

<a name="method-fluent-str-headline"></a>
#### `headline` {.collection-method}

`headline` メソッドは、大文字と小文字、ハイフン、またはアンダースコアで区切られた文字列を、各単語の最初の文字が大文字になったスペースで区切られた文字列に変換します。

    use Illuminate\Support\Str;

    $headline = Str::of('taylor_otwell')->headline();

    // Taylor Otwell

    $headline = Str::of('EmailNotificationSent')->headline();

    // Email Notification Sent

<a name="method-fluent-str-inline-markdown"></a>
#### `inlineMarkdown` {.collection-method}

`inlineMarkdown` メソッドは、[CommonMark](https://commonmark.thephpleague.com/) を使用して、GitHub フレーバーの Markdown をインライン HTML に変換します。ただし、`markdown` メソッドとは異なり、生成されたすべての HTML をブロックレベル要素でラップするわけではありません。

    use Illuminate\Support\Str;

    $html = Str::of('**Laravel**')->inlineMarkdown();

    // <strong>Laravel</strong>

<a name="method-fluent-str-is"></a>
#### `is` {.collection-method}

`is` メソッドは、指定された文字列が指定されたパターンに一致するかどうかを判断します。アスタリスクはワイルドカード値として使用できます

    use Illuminate\Support\Str;

    $matches = Str::of('foobar')->is('foo*');

    // true

    $matches = Str::of('foobar')->is('baz*');

    // false

<a name="method-fluent-str-is-ascii"></a>
#### `isAscii` {.collection-method}

`isAscii` メソッドは、指定された文字列が ASCII 文字列であるかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('Taylor')->isAscii();

    // true

    $result = Str::of('ü')->isAscii();

    // false

<a name="method-fluent-str-is-empty"></a>
#### `isEmpty` {.collection-method}

`isEmpty` メソッドは、指定された文字列が空かどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('  ')->trim()->isEmpty();

    // true

    $result = Str::of('Laravel')->trim()->isEmpty();

    // false

<a name="method-fluent-str-is-not-empty"></a>
#### `isNotEmpty` {.collection-method}

`isNotEmpty` メソッドは、指定された文字列が空でないかどうかを判断します。


    use Illuminate\Support\Str;

    $result = Str::of('  ')->trim()->isNotEmpty();

    // false

    $result = Str::of('Laravel')->trim()->isNotEmpty();

    // true

<a name="method-fluent-str-is-json"></a>
#### `isJson` {.collection-method}

`isJson` メソッドは、指定された文字列が有効な JSON かどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('[1,2,3]')->isJson();

    // true

    $result = Str::of('{"first": "John", "last": "Doe"}')->isJson();

    // true

    $result = Str::of('{first: "John", last: "Doe"}')->isJson();

    // false

<a name="method-fluent-str-is-ulid"></a>
#### `isUlid` {.collection-method}

`isUlid` メソッドは、指定された文字列が ULID であるかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

    // true

    $result = Str::of('Taylor')->isUlid();

    // false

<a name="method-fluent-str-is-uuid"></a>
#### `isUuid` {.collection-method}

`isUuid` メソッドは、指定された文字列が UUID かどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

    // true

    $result = Str::of('Taylor')->isUuid();

    // false

<a name="method-fluent-str-kebab"></a>
#### `kebab` {.collection-method}

`kebab` メソッドは、指定された文字列を `kebab-case` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::of('fooBar')->kebab();

    // foo-bar

<a name="method-fluent-str-lcfirst"></a>
#### `lcfirst` {.collection-method}

`lcfirst` メソッドは、最初の文字を小文字にして指定された文字列を返します。

    use Illuminate\Support\Str;

    $string = Str::of('Foo Bar')->lcfirst();

    // foo Bar


<a name="method-fluent-str-length"></a>
#### `length` {.collection-method}

`length` メソッドは、指定された文字列の長さを返します。

    use Illuminate\Support\Str;

    $length = Str::of('Laravel')->length();

    // 7

<a name="method-fluent-str-limit"></a>
#### `limit` {.collection-method}

`limit` メソッドは、指定された文字列を指定された長さに切り詰めます。

    use Illuminate\Support\Str;

    $truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

    // The quick brown fox...

2 番目の引数を渡して、切り詰められた文字列の末尾に追加される文字列を変更することもできます。

    use Illuminate\Support\Str;

    $truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

    // The quick brown fox (...)

<a name="method-fluent-str-lower"></a>
#### `lower` {.collection-method}

`lower` メソッドは、指定された文字列を小文字に変換します。

    use Illuminate\Support\Str;

    $result = Str::of('LARAVEL')->lower();

    // 'laravel'

<a name="method-fluent-str-ltrim"></a>
#### `ltrim` {.collection-method}

`ltrim` メソッドは、文字列の左側をトリミングします。

    use Illuminate\Support\Str;

    $string = Str::of('  Laravel  ')->ltrim();

    // 'Laravel  '

    $string = Str::of('/Laravel/')->ltrim('/');

    // 'Laravel/'

<a name="method-fluent-str-markdown"></a>
#### `markdown` {.collection-method}

`markdown` メソッドは、GitHub フレーバーの Markdown を HTML に変換します。

    use Illuminate\Support\Str;

    $html = Str::of('# Laravel')->markdown();

    // <h1>Laravel</h1>

    $html = Str::of('# Taylor <b>Otwell</b>')->markdown([
        'html_input' => 'strip',
    ]);

    // <h1>Taylor Otwell</h1>

<a name="method-fluent-str-mask"></a>
#### `mask` {.collection-method}

`mask` メソッドは、文字列の一部を繰り返し文字でマスクし、電子メール アドレスや電話番号などの文字列のセグメントを難読化するために使用できます。

    use Illuminate\Support\Str;

    $string = Str::of('taylor@example.com')->mask('*', 3);

    // tay***************

必要に応じて、`mask` メソッドの 3 番目または 4 番目の引数として負の数値を指定できます。これにより、文字列の末尾から指定された距離でマスクを開始するようにメソッドに指示されます。

    $string = Str::of('taylor@example.com')->mask('*', -15, 3);

    // tay***@example.com

    $string = Str::of('taylor@example.com')->mask('*', 4, -4);

    // tayl**********.com

<a name="method-fluent-str-match"></a>
#### `match` {.collection-method}

`match` メソッドは、指定された正規表現パターンに一致する文字列の部分を返します。

    use Illuminate\Support\Str;

    $result = Str::of('foo bar')->match('/bar/');

    // 'bar'

    $result = Str::of('foo bar')->match('/foo (.*)/');

    // 'bar'

<a name="method-fluent-str-match-all"></a>
#### `matchAll` {.collection-method}

`matchAll` メソッドは、指定された正規表現パターンに一致する文字列の部分を含むコレクションを返します。

    use Illuminate\Support\Str;

    $result = Str::of('bar foo bar')->matchAll('/bar/');

    // collect(['bar', 'bar'])

式内で一致するグループを指定すると、Laravel はそのグループの一致のコレクションを返します。

    use Illuminate\Support\Str;

    $result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

    // collect(['un', 'ly']);

一致するものが見つからない場合は、空のコレクションが返されます。

<a name="method-fluent-str-new-line"></a>
#### `newLine` {.collection-method}

`newLine` メソッドは、文字列に「行末」文字を追加します。

    use Illuminate\Support\Str;

    $padded = Str::of('Laravel')->newLine()->append('Framework');

    // 'Laravel
    //  Framework'

<a name="method-fluent-str-padboth"></a>
#### `padBoth` {.collection-method}

`padBoth` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の両側を別の文字列でパディングします。

    use Illuminate\Support\Str;

    $padded = Str::of('James')->padBoth(10, '_');

    // '__James___'

    $padded = Str::of('James')->padBoth(10);

    // '  James   '

<a name="method-fluent-str-padleft"></a>
#### `padLeft` {.collection-method}

`padLeft` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の左側を別の文字列で埋めます。

    use Illuminate\Support\Str;

    $padded = Str::of('James')->padLeft(10, '-=');

    // '-=-=-James'

    $padded = Str::of('James')->padLeft(10);

    // '     James'

<a name="method-fluent-str-padright"></a>
#### `padRight` {.collection-method}

`padRight` メソッドは、PHP の `str_pad` 関数をラップし、最終的な文字列が目的の長さに達するまで、文字列の右側を別の文字列で埋め込みます。

    use Illuminate\Support\Str;

    $padded = Str::of('James')->padRight(10, '-');

    // 'James-----'

    $padded = Str::of('James')->padRight(10);

    // 'James     '

<a name="method-fluent-str-pipe"></a>
#### `pipe` {.collection-method}

`pipe` メソッドを使用すると、現在の値を指定された呼び出し可能オブジェクトに渡すことで文字列を変換できます。

    use Illuminate\Support\Str;

    $hash = Str::of('Laravel')->pipe('md5')->prepend('Checksum: ');

    // 'Checksum: a5c95b86291ea299fcbe64458ed12702'

    $closure = Str::of('foo')->pipe(function ($str) {
        return 'bar';
    });

    // 'bar'

<a name="method-fluent-str-plural"></a>
#### `plural` {.collection-method}

`plural` メソッドは、単数形の単語文字列を複数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

    use Illuminate\Support\Str;

    $plural = Str::of('car')->plural();

    // cars

    $plural = Str::of('child')->plural();

    // children

関数の 2 番目の引数として整数を指定して、文字列の単数形または複数形を取得できます。

    use Illuminate\Support\Str;

    $plural = Str::of('child')->plural(2);

    // children

    $plural = Str::of('child')->plural(1);

    // child

<a name="method-fluent-str-prepend"></a>
#### `prepend` {.collection-method}

`prepend` メソッドは、指定された値を文字列の先頭に追加します。

    use Illuminate\Support\Str;

    $string = Str::of('Framework')->prepend('Laravel ');

    // Laravel Framework

<a name="method-fluent-str-remove"></a>
#### `remove` {.collection-method}

`remove` メソッドは、指定された値または値の配列を文字列から削除します。

    use Illuminate\Support\Str;

    $string = Str::of('Arkansas is quite beautiful!')->remove('quite');

    // Arkansas is beautiful!

文字列を削除するときに大文字と小文字を区別しないように、2 番目のパラメーターとして `false` を渡すこともできます。

<a name="method-fluent-str-replace"></a>
#### `replace` {.collection-method}

`replace` メソッドは、文字列内の指定された文字列を置き換えます。

    use Illuminate\Support\Str;

    $replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

    // Laravel 7.x

<a name="method-fluent-str-replace-array"></a>
#### `replaceArray` {.collection-method}

`replaceArray` メソッドは、配列を使用して文字列内の指定された値を順番に置き換えます。

    use Illuminate\Support\Str;

    $string = 'The event will take place between ? and ?';

    $replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

    // The event will take place between 8:30 and 9:00

<a name="method-fluent-str-replace-first"></a>
#### `replaceFirst` {.collection-method}

`replaceFirst` メソッドは、文字列内の指定された値の最初の出現を置き換えます。

    use Illuminate\Support\Str;

    $replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

    // a quick brown fox jumps over the lazy dog

<a name="method-fluent-str-replace-last"></a>
#### `replaceLast` {.collection-method}

`replaceLast` メソッドは、文字列内の指定された値の最後の出現を置き換えます。

    use Illuminate\Support\Str;

    $replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

    // the quick brown fox jumps over a lazy dog

<a name="method-fluent-str-replace-matches"></a>
#### `replaceMatches` {.collection-method}

`replaceMatches` メソッドは、パターンに一致する文字列のすべての部分を指定された置換文字列に置き換えます。

    use Illuminate\Support\Str;

    $replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

    // '15015551000'

`replaceMatches` メソッドは、指定されたパターンに一致する文字列の各部分で呼び出されるクロージャも受け入れます。これにより、クロージャ内で置換ロジックを実行し、置換された値を返すことができます。

    use Illuminate\Support\Str;

    $replaced = Str::of('123')->replaceMatches('/\d/', function ($match) {
        return '['.$match[0].']';
    });

    // '[1][2][3]'

<a name="method-fluent-str-rtrim"></a>
#### `rtrim` {.collection-method}

`rtrim` メソッドは、指定された文字列の右側をトリミングします。

    use Illuminate\Support\Str;

    $string = Str::of('  Laravel  ')->rtrim();

    // '  Laravel'

    $string = Str::of('/Laravel/')->rtrim('/');

    // '/Laravel'

<a name="method-fluent-str-scan"></a>
#### `scan` {.collection-method}

`scan` メソッドは、[`sscanf` PHP 関数](https://www.php.net/manual/en/function.sscanf.php) でサポートされている形式に従って、文字列からの入力を解析してコレクションに入れます。

    use Illuminate\Support\Str;

    $collection = Str::of('filename.jpg')->scan('%[^.].%s');

    // collect(['filename', 'jpg'])

<a name="method-fluent-str-singular"></a>
#### `singular` {.collection-method}

`singular` メソッドは、文字列を単数形に変換します。この関数は [Laravelのpluralizerでサポートされている言語のいずれか](/docs/{{version}}/localization#pluralization-language) をサポートします。

    use Illuminate\Support\Str;

    $singular = Str::of('cars')->singular();

    // car

    $singular = Str::of('children')->singular();

    // child

<a name="method-fluent-str-slug"></a>
#### `slug` {.collection-method}

`slug` メソッドは、指定された文字列から URL フレンドリな「スラッグ」を生成します。

    use Illuminate\Support\Str;

    $slug = Str::of('Laravel Framework')->slug('-');

    // laravel-framework

<a name="method-fluent-str-snake"></a>
#### `snake` {.collection-method}

`snake` メソッドは、指定された文字列を `snake_case` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::of('fooBar')->snake();

    // foo_bar

<a name="method-fluent-str-split"></a>
#### `split` {.collection-method}

`split` メソッドは、正規表現を使用して文字列をコレクションに分割します。

    use Illuminate\Support\Str;

    $segments = Str::of('one, two, three')->split('/[\s,]+/');

    // collect(["one", "two", "three"])

<a name="method-fluent-str-squish"></a>
#### `squish` {.collection-method}

`squish` メソッドは、単語間の無関係な空白を含め、文字列から無関係な空白をすべて削除します。

    use Illuminate\Support\Str;

    $string = Str::of('    laravel    framework    ')->squish();

    // laravel framework

<a name="method-fluent-str-start"></a>
#### `start` {.collection-method}

`start` メソッドは、指定された値の単一インスタンスを文字列に追加します (まだその値で始まっていない場合)。

    use Illuminate\Support\Str;

    $adjusted = Str::of('this/string')->start('/');

    // /this/string

    $adjusted = Str::of('/this/string')->start('/');

    // /this/string

<a name="method-fluent-str-starts-with"></a>
#### `startsWith` {.collection-method}

`startsWith` メソッドは、指定された文字列が指定された値で始まるかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('This is my name')->startsWith('This');

    // true

<a name="method-fluent-str-studly"></a>
#### `studly` {.collection-method}

`studly` メソッドは、指定された文字列を `StudlyCase` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::of('foo_bar')->studly();

    // FooBar

<a name="method-fluent-str-substr"></a>
#### `substr` {.collection-method}

`substr` メソッドは、指定された start パラメーターと length パラメーターで指定された文字列の部分を返します。

    use Illuminate\Support\Str;

    $string = Str::of('Laravel Framework')->substr(8);

    // Framework

    $string = Str::of('Laravel Framework')->substr(8, 5);

    // Frame

<a name="method-fluent-str-substrreplace"></a>
#### `substrReplace` {.collection-method}

`substrReplace` メソッドは、文字列の一部内のテキストを、2 番目の引数で指定された位置から開始して、3 番目の引数で指定された文字数まで置き換えます。 `0` をメソッドの 3 番目の引数に渡すと、文字列内の既存の文字を置換せずに、指定された位置に文字列が挿入されます。

    use Illuminate\Support\Str;

    $string = Str::of('1300')->substrReplace(':', 2);

    // 13:

    $string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

    // The Laravel Framework

<a name="method-fluent-str-swap"></a>
#### `swap` {.collection-method}

`swap` メソッドは、PHP の `strtr` 関数を使用して文字列内の複数の値を置き換えます。

    use Illuminate\Support\Str;

    $string = Str::of('Tacos are great!')
        ->swap([
            'Tacos' => 'Burritos',
            'great' => 'fantastic',
        ]);

    // Burritos are fantastic!

<a name="method-fluent-str-tap"></a>
#### `tap` {.collection-method}

`tap` メソッドは文字列を指定されたクロージャに渡します。これにより、文字列自体には影響を与えずに、文字列を調べて操作できるようになります。クロージャによって何が返されるかに関係なく、元の文字列が `tap` メソッドによって返されます。

    use Illuminate\Support\Str;

    $string = Str::of('Laravel')
        ->append(' Framework')
        ->tap(function ($string) {
            dump('String after append: '.$string);
        })
        ->upper();

    // LARAVEL FRAMEWORK

<a name="method-fluent-str-test"></a>
#### `test` {.collection-method}

`test` メソッドは、文字列が指定された正規表現パターンに一致するかどうかを判断します。

    use Illuminate\Support\Str;

    $result = Str::of('Laravel Framework')->test('/Laravel/');

    // true

<a name="method-fluent-str-title"></a>
#### `title` {.collection-method}

`title` メソッドは、指定された文字列を `Title Case` に変換します。

    use Illuminate\Support\Str;

    $converted = Str::of('a nice title uses the correct case')->title();

    // A Nice Title Uses The Correct Case

<a name="method-fluent-str-trim"></a>
#### `trim` {.collection-method}

`trim` メソッドは、指定された文字列をトリミングします。

    use Illuminate\Support\Str;

    $string = Str::of('  Laravel  ')->trim();

    // 'Laravel'

    $string = Str::of('/Laravel/')->trim('/');

    // 'Laravel'

<a name="method-fluent-str-ucfirst"></a>
#### `ucfirst` {.collection-method}

`ucfirst` メソッドは、最初の文字を大文字にした指定された文字列を返します。

    use Illuminate\Support\Str;

    $string = Str::of('foo bar')->ucfirst();

    // Foo bar

<a name="method-fluent-str-ucsplit"></a>
#### `ucsplit` {.collection-method}

`ucsplit` メソッドは、指定された文字列を大文字でコレクションに分割します。

    use Illuminate\Support\Str;

    $string = Str::of('Foo Bar')->ucsplit();

    // collect(['Foo', 'Bar'])

<a name="method-fluent-str-upper"></a>
#### `upper` {.collection-method}

`upper` メソッドは、指定された文字列を大文字に変換します。

    use Illuminate\Support\Str;

    $adjusted = Str::of('laravel')->upper();

    // LARAVEL

<a name="method-fluent-str-when"></a>
#### `when` {.collection-method}

`when` メソッドは、指定された条件が `true` の場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('Taylor')
                    ->when(true, function ($string) {
                        return $string->append(' Otwell');
                    });

    // 'Taylor Otwell'

必要に応じて、別のクロージャを 3 番目のパラメータとして `when` メソッドに渡すことができます。このクロージャは、条件パラメータが `false` と評価された場合に実行されます。

<a name="method-fluent-str-when-contains"></a>
#### `whenContains` {.collection-method}

`whenContains` メソッドは、文字列に指定された値が含まれている場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('tony stark')
                ->whenContains('tony', function ($string) {
                    return $string->title();
                });

    // 'Tony Stark'

必要に応じて、別のクロージャを 3 番目のパラメータとして `when` メソッドに渡すことができます。このクロージャは、文字列に指定された値が含まれていない場合に実行されます。

値の配列を渡して、指定された文字列に配列内の値が含まれているかどうかを確認することもできます。

    use Illuminate\Support\Str;

    $string = Str::of('tony stark')
                ->whenContains(['tony', 'hulk'], function ($string) {
                    return $string->title();
                });

    // Tony Stark

<a name="method-fluent-str-when-contains-all"></a>
#### `whenContainsAll` {.collection-method}

`whenContainsAll` メソッドは、文字列に指定されたサブ文字列がすべて含まれている場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('tony stark')
                    ->whenContainsAll(['tony', 'stark'], function ($string) {
                        return $string->title();
                    });

    // 'Tony Stark'

必要に応じて、別のクロージャを 3 番目のパラメータとして `when` メソッドに渡すことができます。このクロージャは、条件パラメータが `false` と評価された場合に実行されます。

<a name="method-fluent-str-when-empty"></a>
#### `whenEmpty` {.collection-method}

`whenEmpty` メソッドは、文字列が空の場合、指定されたクロージャを呼び出します。クロージャが値を返す場合、その値は `whenEmpty` メソッドによっても返されます。クロージャが値を返さない場合は、流暢な文字列インスタンスが返されます。

    use Illuminate\Support\Str;

    $string = Str::of('  ')->whenEmpty(function ($string) {
        return $string->trim()->prepend('Laravel');
    });

    // 'Laravel'

<a name="method-fluent-str-when-not-empty"></a>
#### `whenNotEmpty` {.collection-method}

文字列が空でない場合、`whenNotEmpty` メソッドは指定されたクロージャを呼び出します。クロージャが値を返す場合、その値は `whenNotEmpty` メソッドによっても返されます。クロージャが値を返さない場合は、流暢な文字列インスタンスが返されます。

    use Illuminate\Support\Str;

    $string = Str::of('Framework')->whenNotEmpty(function ($string) {
        return $string->prepend('Laravel ');
    });

    // 'Laravel Framework'

<a name="method-fluent-str-when-starts-with"></a>
#### `whenStartsWith` {.collection-method}

`whenStartsWith` メソッドは、文字列が指定された部分文字列で始まる場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('disney world')->whenStartsWith('disney', function ($string) {
        return $string->title();
    });

    // 'Disney World'

<a name="method-fluent-str-when-ends-with"></a>
#### `whenEndsWith` {.collection-method}

`whenEndsWith` メソッドは、文字列が指定された部分文字列で終わる場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('disney world')->whenEndsWith('world', function ($string) {
        return $string->title();
    });

    // 'Disney World'

<a name="method-fluent-str-when-exactly"></a>
#### `whenExactly` {.collection-method}

`whenExactly` メソッドは、文字列が指定された文字列と正確に一致する場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('laravel')->whenExactly('laravel', function ($string) {
        return $string->title();
    });

    // 'Laravel'

<a name="method-fluent-str-when-not-exactly"></a>
#### `whenNotExactly` {.collection-method}

`whenNotExactly` メソッドは、文字列が指定された文字列と正確に一致しない場合、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('framework')->whenNotExactly('laravel', function ($string) {
        return $string->title();
    });

    // 'Framework'

<a name="method-fluent-str-when-is"></a>
#### `whenIs` {.collection-method}

`whenIs` メソッドは、文字列が指定されたパターンに一致する場合に、指定されたクロージャを呼び出します。アスタリスクはワイルドカード値として使用できます。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('foo/bar')->whenIs('foo/*', function ($string) {
        return $string->append('/baz');
    });

    // 'foo/bar/baz'

<a name="method-fluent-str-when-is-ascii"></a>
#### `whenIsAscii` {.collection-method}

文字列が 7 ビット ASCII の場合、`whenIsAscii` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('laravel')->whenIsAscii(function ($string) {
        return $string->title();
    });

    // 'Laravel'

<a name="method-fluent-str-when-is-ulid"></a>
#### `whenIsUlid` {.collection-method}

文字列が有効な ULID の場合、`whenIsUlid` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function ($string) {
        return $string->substr(0, 8);
    });

    // '01gd6r36'

<a name="method-fluent-str-when-is-uuid"></a>
#### `whenIsUuid` {.collection-method}

文字列が有効な UUID の場合、`whenIsUuid` メソッドは指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function ($string) {
        return $string->substr(0, 8);
    });

    // 'a0a2a2d2'

<a name="method-fluent-str-when-test"></a>
#### `whenTest` {.collection-method}

`whenTest` メソッドは、文字列が指定された正規表現と一致する場合に、指定されたクロージャを呼び出します。クロージャは流暢な文字列インスタンスを受け取ります。

    use Illuminate\Support\Str;

    $string = Str::of('laravel framework')->whenTest('/laravel/', function ($string) {
        return $string->title();
    });

    // 'Laravel Framework'

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

    use Illuminate\Support\Str;

    $string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

    // Perfectly balanced, as >>>

<a name="urls"></a>
## URL (URLs)

<a name="method-action"></a>
#### `action()` {.collection-method}

`action` 関数は、指定されたコントローラ アクションの URL を生成します。

    use App\Http\Controllers\HomeController;

    $url = action([HomeController::class, 'index']);

メソッドがルート パラメーターを受け入れる場合は、それらを 2 番目の引数としてメソッドに渡すことができます。

    $url = action([UserController::class, 'profile'], ['id' => 1]);

<a name="method-asset"></a>
#### `asset()` {.collection-method}

`asset` 関数は、現在のリクエスト スキーム (HTTP または HTTPS) を使用してアセットの URL を生成します。

    $url = asset('img/photo.jpg');

`.env` ファイルで `ASSET_URL` 変数を設定することで、アセット URL ホストを構成できます。これは、Amazon S3 や別の CDN などの外部サービスでアセットをホストする場合に便利です。

    // ASSET_URL=http://example.com/assets

    $url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg

<a name="method-route"></a>
#### `route()` {.collection-method}

`route` 関数は、指定された [名前付きルート](/docs/{{version}}/routing#named-routes) の URL を生成します。

    $url = route('route.name');

ルートがパラメーターを受け入れる場合は、それらを関数の 2 番目の引数として渡すことができます。

    $url = route('route.name', ['id' => 1]);

デフォルトでは、`route` 関数は絶対 URL を生成します。相対 URL を生成したい場合は、関数の 3 番目の引数として `false` を渡すことができます。

    $url = route('route.name', ['id' => 1], false);

<a name="method-secure-asset"></a>
#### `secure_asset()` {.collection-method}

`secure_asset` 関数は、HTTPS を使用してアセットの URL を生成します。

    $url = secure_asset('img/photo.jpg');

<a name="method-secure-url"></a>
#### `secure_url()` {.collection-method}

`secure_url` 関数は、指定されたパスへの完全修飾 HTTPS URL を生成します。追加の URL セグメントを関数の 2 番目の引数に渡すことができます。

    $url = secure_url('user/profile');

    $url = secure_url('user/profile', [1]);

<a name="method-to-route"></a>
#### `to_route()` {.collection-method}

`to_route` 関数は、指定された [名前付きルート](/docs/{{version}}/responses#redirects) の [HTTP 応答をリダイレクトする](/docs/{{version}}/routing#named-routes) を生成します。

    return to_route('users.show', ['user' => 1]);

必要に応じて、リダイレクトに割り当てる必要がある HTTP ステータス コードと追加の応答ヘッダーを `to_route` メソッドの 3 番目と 4 番目の引数として渡すことができます。

    return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);

<a name="method-url"></a>
#### `url()` {.collection-method}

`url` 関数は、指定されたパスへの完全修飾 URL を生成します。

    $url = url('user/profile');

    $url = url('user/profile', [1]);

パスが指定されていない場合は、`Illuminate\Routing\UrlGenerator` インスタンスが返されます。

    $current = url()->current();

    $full = url()->full();

    $previous = url()->previous();

<a name="miscellaneous"></a>
## その他 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()` {.collection-method}

`abort` 関数は、[例外ハンドラ](/docs/{{version}}/errors#http-exceptions) によってレンダリングされる [HTTP例外](/docs/{{version}}/errors#the-exception-handler) をスローします。

    abort(403);

ブラウザに送信する例外のメッセージとカスタム HTTP 応答ヘッダーを指定することもできます。

    abort(403, 'Unauthorized.', $headers);

<a name="method-abort-if"></a>
#### `abort_if()` {.collection-method}

指定されたブール式が `true` と評価される場合、`abort_if` 関数は HTTP 例外をスローします。

    abort_if(! Auth::user()->isAdmin(), 403);

`abort` メソッドと同様に、関数の 3 番目の引数として例外の応答テキストを指定し、4 番目の引数としてカスタム応答ヘッダーの配列を指定することもできます。

<a name="method-abort-unless"></a>
#### `abort_unless()` {.collection-method}

指定されたブール式が `false` と評価される場合、`abort_unless` 関数は HTTP 例外をスローします。

    abort_unless(Auth::user()->isAdmin(), 403);

`abort` メソッドと同様に、関数の 3 番目の引数として例外の応答テキストを指定し、4 番目の引数としてカスタム応答ヘッダーの配列を指定することもできます。

<a name="method-app"></a>
#### `app()` {.collection-method}

`app` 関数は、[サービスコンテナ](/docs/{{version}}/container) インスタンスを返します。

    $container = app();

クラス名またはインターフェース名を渡して、コンテナーから解決できます。

    $api = app('HelpSpot\API');

<a name="method-auth"></a>
#### `auth()` {.collection-method}

`auth` 関数は、[authenticator](/docs/{{version}}/authentication) インスタンスを返します。 `Auth` ファサードの代替として使用できます。

    $user = auth()->user();

必要に応じて、アクセスするガード インスタンスを指定できます。

    $user = auth('admin')->user();

<a name="method-back"></a>
#### `back()` {.collection-method}

`back` 関数は、ユーザーの以前の場所に [HTTP 応答をリダイレクトする](/docs/{{version}}/responses#redirects) を生成します。

    return back($status = 302, $headers = [], $fallback = '/');

    return back();

<a name="method-bcrypt"></a>
#### `bcrypt()` {.collection-method}

`bcrypt` 関数 [hashes](/docs/{{version}}/hashing) は、Bcrypt を使用して指定された値を取得します。この関数は、`Hash` ファサードの代わりに使用できます。

    $password = bcrypt('my-secret-password');

<a name="method-blank"></a>
#### `blank()` {.collection-method}

`blank` 関数は、指定された値が「空白」かどうかを判断します。

    blank('');
    blank('   ');
    blank(null);
    blank(collect());

    // true

    blank(0);
    blank(true);
    blank(false);

    // false

`blank` の逆については、[`filled`](#method-filled) メソッドを参照してください。

<a name="method-broadcast"></a>
#### `broadcast()` {.collection-method}

`broadcast` 関数 [broadcasts](/docs/{{version}}/broadcasting) は、指定された [event](/docs/{{version}}/events) をリスナに渡します。

    broadcast(new UserRegistered($user));

    broadcast(new UserRegistered($user))->toOthers();

<a name="method-cache"></a>
#### `cache()` {.collection-method}

`cache` 関数を使用して、[cache](/docs/{{version}}/cache) から値を取得できます。指定されたキーがキャッシュに存在しない場合は、オプションのデフォルト値が返されます。

    $value = cache('key');

    $value = cache('key', 'default');

キーと値のペアの配列を関数に渡すことで、キャッシュに項目を追加できます。キャッシュされた値が有効であるとみなされる秒数または期間も渡す必要があります。

    cache(['key' => 'value'], 300);

    cache(['key' => 'value'], now()->addSeconds(10));

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()` {.collection-method}

`class_uses_recursive` 関数は、そのすべての親クラスで使用される特性を含む、クラスで使用されるすべての特性を返します。

    $traits = class_uses_recursive(App\Models\User::class);

<a name="method-collect"></a>
#### `collect()` {.collection-method}

`collect` 関数は、指定された値から [collection](/docs/{{version}}/collections) インスタンスを作成します。

    $collection = collect(['taylor', 'abigail']);

<a name="method-config"></a>
#### `config()` {.collection-method}

`config` 関数は、[configuration](/docs/{{version}}/configuration) 変数の値を取得します。設定値には、ファイル名とアクセスするオプションを含む「ドット」構文を使用してアクセスできます。デフォルト値を指定することができ、構成オプションが存在しない場合はデフォルト値が返されます。

    $value = config('app.timezone');

    $value = config('app.timezone', $default);

キーと値のペアの配列を渡すことで、実行時に構成変数を設定できます。ただし、この関数は現在のリクエストの構成値にのみ影響し、実際の構成値は更新されないことに注意してください。

    config(['app.debug' => true]);

<a name="method-cookie"></a>
#### `cookie()` {.collection-method}

`cookie` 関数は、新しい [cookie](/docs/{{version}}/requests#cookies) インスタンスを作成します。

    $cookie = cookie('name', 'value', $minutes);

<a name="method-csrf-field"></a>
#### `csrf_field()` {.collection-method}

`csrf_field` 関数は、CSRF トークンの値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade 構文](/docs/{{version}}/blade) を使用すると、次のようになります。

    {{ csrf_field() }}

<a name="method-csrf-token"></a>
#### `csrf_token()` {.collection-method}

`csrf_token` 関数は、現在の CSRF トークンの値を取得します。

    $token = csrf_token();

<a name="method-decrypt"></a>
#### `decrypt()` {.collection-method}

`decrypt` 関数 [decrypts](/docs/{{version}}/encryption) に指定された値。この関数は、`Crypt` ファサードの代わりに使用できます。

    $password = decrypt($value);

<a name="method-dd"></a>
#### `dd()` {.collection-method}

`dd` 関数は、指定された変数をダンプし、スクリプトの実行を終了します。

    dd($value);

    dd($value1, $value2, $value3, ...);

スクリプトの実行を停止したくない場合は、代わりに [`dump`](#method-dump) 関数を使用してください。

<a name="method-dispatch"></a>
#### `dispatch()` {.collection-method}

`dispatch` 関数は、指定された [job](/docs/{{version}}/queues#creating-jobs) を Laravel [ジョブキュー](/docs/{{version}}/queues) にプッシュします。

    dispatch(new App\Jobs\SendEmails);

<a name="method-dump"></a>
#### `dump()` {.collection-method}

`dump` 関数は、指定された変数をダンプします。

    dump($value);

    dump($value1, $value2, $value3, ...);

変数をダンプした後にスクリプトの実行を停止する場合は、代わりに [`dd`](#method-dd) 関数を使用します。

<a name="method-encrypt"></a>
#### `encrypt()` {.collection-method}

`encrypt` 関数 [encrypts](/docs/{{version}}/encryption) に指定された値。この関数は、`Crypt` ファサードの代わりに使用できます。

    $secret = encrypt('my-secret-value');

<a name="method-env"></a>
#### `env()` {.collection-method}

`env` 関数は、[環境変数](/docs/{{version}}/configuration#environment-configuration) の値を取得するか、デフォルト値を返します。

    $env = env('APP_ENV');

    $env = env('APP_ENV', 'production');

> **警告**
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされず、`env` 関数へのすべての呼び出しは `null` を返します。

<a name="method-event"></a>
#### `event()` {.collection-method}

`event` 関数は、指定された [event](/docs/{{version}}/events) をリスナにディスパッチします。

    event(new UserRegistered($user));

<a name="method-fake"></a>
#### `fake()` {.collection-method}

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

デフォルトでは、`fake` 関数は、`config/app.php` 構成ファイル内の `app.faker_locale` 構成オプションを利用します。ただし、ロケールを `fake` 関数に渡して指定することもできます。各ロケールは個々のシングルトンを解決します。

    fake('nl_NL')->name()

<a name="method-filled"></a>
#### `filled()` {.collection-method}

`filled` 関数は、指定された値が「空白」でないかどうかを判断します。

    filled(0);
    filled(true);
    filled(false);

    // true

    filled('');
    filled('   ');
    filled(null);
    filled(collect());

    // false

`filled` の逆については、[`blank`](#method-blank) メソッドを参照してください。

<a name="method-info"></a>
#### `info()` {.collection-method}

`info` 関数は、アプリケーションの [log](/docs/{{version}}/logging) に情報を書き込みます。

    info('Some helpful information!');

コンテキスト データの配列を関数に渡すこともできます。

    info('User login attempt failed.', ['id' => $user->id]);

<a name="method-logger"></a>
#### `logger()` {.collection-method}

`logger` 関数を使用して、`debug` レベルのメッセージを [log](/docs/{{version}}/logging) に書き込むことができます。

    logger('Debug message');

コンテキスト データの配列を関数に渡すこともできます。

    logger('User has logged in.', ['id' => $user->id]);

関数に値が渡されない場合、[logger](/docs/{{version}}/logging) インスタンスが返されます。

    logger()->error('You are not allowed here.');

<a name="method-method-field"></a>
#### `method_field()` {.collection-method}

`method_field` 関数は、フォームの HTTP 動詞の偽値を含む HTML `hidden` 入力フィールドを生成します。たとえば、[Blade 構文](/docs/{{version}}/blade) を使用すると、次のようになります。

    <form method="POST">
        {{ method_field('DELETE') }}
    </form>

<a name="method-now"></a>
#### `now()` {.collection-method}

`now` 関数は、現時点での新しい `Illuminate\Support\Carbon` インスタンスを作成します。

    $now = now();

<a name="method-old"></a>
#### `old()` {.collection-method}

`old` 関数 [retrieves](/docs/{{version}}/requests#retrieving-input) および [古い入力](/docs/{{version}}/requests#old-input) 値がセッションにフラッシュされました。

    $value = old('value');

    $value = old('value', 'default');

`old` 関数の 2 番目の引数として指定される「デフォルト値」は多くの場合 Eloquent モデルの属性であるため、Laravel では Eloquent モデル全体を 2 番目の引数として `old` 関数に渡すだけで済みます。これを行うと、Laravel は、`old` 関数に指定された最初の引数が、「デフォルト値」とみなされるべき Eloquent 属性の名前であると想定します。

    {{ old('name', $user->name) }}

    // Is equivalent to...

    {{ old('name', $user) }}

<a name="method-optional"></a>
#### `optional()` {.collection-method}

`optional` 関数は任意の引数を受け入れ、そのオブジェクトのプロパティにアクセスしたり、メソッドを呼び出したりすることができます。指定されたオブジェクトが `null` の場合、プロパティとメソッドはエラーを引き起こす代わりに `null` を返します。

    return optional($user->address)->street;

    {!! old('name', optional($user)->name) !!}

`optional` 関数は、2 番目の引数としてクロージャも受け入れます。最初の引数として指定された値が null でない場合、クロージャが呼び出されます。

    return optional(User::find($id), function ($user) {
        return $user->name;
    });

<a name="method-policy"></a>
#### `policy()` {.collection-method}

`policy` メソッドは、指定されたクラスの [policy](/docs/{{version}}/authorization#creating-policies) インスタンスを取得します。

    $policy = policy(App\Models\User::class);

<a name="method-redirect"></a>
#### `redirect()` {.collection-method}

`redirect` 関数は [HTTP 応答をリダイレクトする](/docs/{{version}}/responses#redirects) を返すか、引数なしで呼び出された場合はリダイレクター インスタンスを返します。

    return redirect($to = null, $status = 302, $headers = [], $https = null);

    return redirect('/home');

    return redirect()->route('route.name');

<a name="method-report"></a>
#### `report()` {.collection-method}

`report` 関数は、[例外ハンドラ](/docs/{{version}}/errors#the-exception-handler) を使用して例外を報告します。

    report($e);

`report` 関数は、引数として文字列も受け入れます。文字列が関数に与えられると、関数は指定された文字列をメッセージとして持つ例外を作成します。

    report('Something went wrong.');

<a name="method-report-if"></a>
#### `report_if()` {.collection-method}

指定された条件が `true` の場合、`report_if` 関数は、[例外ハンドラ](/docs/{{version}}/errors#the-exception-handler) を使用して例外を報告します。

    report_if($shouldReport, $e);

    report_if($shouldReport, 'Something went wrong.');

<a name="method-report-unless"></a>
#### `report_unless()` {.collection-method}

指定された条件が `false` の場合、`report_unless` 関数は、[例外ハンドラ](/docs/{{version}}/errors#the-exception-handler) を使用して例外を報告します。

    report_unless($reportingDisabled, $e);

    report_unless($reportingDisabled, 'Something went wrong.');

<a name="method-request"></a>
#### `request()` {.collection-method}

`request` 関数は、現在の [request](/docs/{{version}}/requests) インスタンスを返すか、現在のリクエストから入力フィールドの値を取得します。

    $request = request();

    $value = request('key', $default);

<a name="method-rescue"></a>
#### `rescue()` {.collection-method}

`rescue` 関数は、指定されたクロージャを実行し、その実行中に発生する例外をキャッチします。キャッチされた例外はすべて [例外ハンドラ](/docs/{{version}}/errors#the-exception-handler) に送信されます。ただし、リクエストは処理を続行します。

    return rescue(function () {
        return $this->method();
    });

`rescue` 関数に 2 番目の引数を渡すこともできます。この引数は、クロージャの実行中に例外が発生した場合に返される「デフォルト」値になります。

    return rescue(function () {
        return $this->method();
    }, false);

    return rescue(function () {
        return $this->method();
    }, function () {
        return $this->failure();
    });

<a name="method-resolve"></a>
#### `resolve()` {.collection-method}

`resolve` 関数は、[サービスコンテナ](/docs/{{version}}/container) を使用して、指定されたクラスまたはインターフェイス名をインスタンスに解決します。

    $api = resolve('HelpSpot\API');

<a name="method-response"></a>
#### `response()` {.collection-method}

`response` 関数は、[response](/docs/{{version}}/responses) インスタンスを作成するか、応答ファクトリーのインスタンスを取得します。

    return response('Hello World', 200, $headers);

    return response()->json(['foo' => 'bar'], 200, $headers);

<a name="method-retry"></a>
#### `retry()` {.collection-method}

`retry` 関数は、指定された最大試行しきい値に達するまで、指定されたコールバックの実行を試行します。コールバックが例外をスローしない場合は、その戻り値が返されます。コールバックが例外をスローした場合、自動的に再試行されます。最大試行回数を超えると、例外がスローされます。

    return retry(5, function () {
        // Attempt 5 times while resting 100ms between attempts...
    }, 100);

試行間のスリープ時間を手動で計算したい場合は、`retry` 関数の 3 番目の引数としてクロージャを渡すことができます。

    return retry(5, function () {
        // ...
    }, function ($attempt, $exception) {
        return $attempt * 100;
    });

便宜上、配列を `retry` 関数の最初の引数として指定できます。この配列は、次の試行の間にスリープする時間をミリ秒単位で決定するために使用されます。

    return retry([100, 200], function () {
        // Sleep for 100ms on first retry, 200ms on second retry...
    });

特定の条件下でのみ再試行するには、`retry` 関数の 4 番目の引数としてクロージャを渡すことができます。

    return retry(5, function () {
        // ...
    }, 100, function ($exception) {
        return $exception instanceof RetryException;
    });

<a name="method-session"></a>
#### `session()` {.collection-method}

`session` 関数は、[session](/docs/{{version}}/session) 値を取得または設定するために使用できます。

    $value = session('key');

キーと値のペアの配列を関数に渡すことで、値を設定できます。

    session(['chairs' => 7, 'instruments' => 3]);

関数に値が渡されない場合、セッション ストアが返されます。

    $value = session()->get('key');

    session()->put('key', $value);

<a name="method-tap"></a>
#### `tap()` {.collection-method}

`tap` 関数は、任意の `$value` とクロージャの 2 つの引数を受け入れます。 `$value` はクロージャに渡され、`tap` 関数によって返されます。クロージャの戻り値は無関係です。

    $user = tap(User::first(), function ($user) {
        $user->name = 'taylor';

        $user->save();
    });

クロージャーが `tap` 関数に渡されない場合は、指定された `$value` で任意のメソッドを呼び出すことができます。呼び出したメソッドの戻り値は、メソッドがその定義で実際に何を返すかに関係なく、常に `$value` になります。たとえば、Eloquent `update` メソッドは通常、整数を返します。ただし、`tap` 関数を介して `update` メソッド呼び出しを連鎖させることで、メソッドがモデル自体を返すように強制できます。

    $user = tap($user)->update([
        'name' => $name,
        'email' => $email,
    ]);

`tap` メソッドをクラスに追加するには、`Illuminate\Support\Traits\Tappable` 特性をクラスに追加します。このトレイトの `tap` メソッドは、唯一の引数として Closure を受け入れます。オブジェクト インスタンス自体はクロージャに渡され、`tap` メソッドによって返されます。

    return $user->tap(function ($user) {
        //
    });

<a name="method-throw-if"></a>
#### `throw_if()` {.collection-method}

指定されたブール式が `true` と評価される場合、`throw_if` 関数は指定された例外をスローします。

    throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

    throw_if(
        ! Auth::user()->isAdmin(),
        AuthorizationException::class,
        'You are not allowed to access this page.'
    );

<a name="method-throw-unless"></a>
#### `throw_unless()` {.collection-method}

指定されたブール式が `false` と評価される場合、`throw_unless` 関数は指定された例外をスローします。

    throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

    throw_unless(
        Auth::user()->isAdmin(),
        AuthorizationException::class,
        'You are not allowed to access this page.'
    );

<a name="method-today"></a>
#### `today()` {.collection-method}

`today` 関数は、現在の日付の新しい `Illuminate\Support\Carbon` インスタンスを作成します。

    $today = today();

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()` {.collection-method}

`trait_uses_recursive` 関数は、特性によって使用されるすべての特性を返します。

    $traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);

<a name="method-transform"></a>
#### `transform()` {.collection-method}

`transform` 関数は、値が [blank](#method-blank) でない場合、指定された値に対してクロージャを実行し、クロージャの戻り値を返します。

    $callback = function ($value) {
        return $value * 2;
    };

    $result = transform(5, $callback);

    // 10

デフォルト値またはクロージャは、関数の 3 番目の引数として渡すことができます。指定された値が空白の場合、この値が返されます。

    $result = transform(null, $callback, 'The value is blank');

    // The value is blank

<a name="method-validator"></a>
#### `validator()` {.collection-method}

`validator` 関数は、指定された引数を使用して新しい [validator](/docs/{{version}}/validation) インスタンスを作成します。 `Validator` ファサードの代替として使用できます。

    $validator = validator($data, $rules, $messages);

<a name="method-value"></a>
#### `value()` {.collection-method}

`value` 関数は、指定された値を返します。ただし、関数にクロージャを渡すと、クロージャが実行され、その戻り値が返されます。

    $result = value(true);

    // true

    $result = value(function () {
        return false;
    });

    // false
    
追加の引数を `value` 関数に渡すことができます。最初の引数がクロージャの場合、追加のパラメータは引数としてクロージャに渡されます。それ以外の場合は無視されます。

    $result = value(function ($name) {
        return $parameter;
    }, 'Taylor');
    
    // 'Taylor'

<a name="method-view"></a>
#### `view()` {.collection-method}

`view` 関数は、[view](/docs/{{version}}/views) インスタンスを取得します。

    return view('auth.login');

<a name="method-with"></a>
#### `with()` {.collection-method}

`with` 関数は、指定された値を返します。クロージャが関数の 2 番目の引数として渡されると、クロージャが実行され、その戻り値が返されます。

    $callback = function ($value) {
        return is_numeric($value) ? $value * 2 : 0;
    };

    $result = with(5, $callback);

    // 10

    $result = with(null, $callback);

    // 0

    $result = with(5, null);

    // 5

<a name="other-utilities"></a>
## その他のユーティリティ (Other Utilities)

<a name="benchmarking"></a>
### ベンチマーク

場合によっては、アプリケーションの特定の部分のパフォーマンスを簡単にテストしたい場合があります。このような場合、`Benchmark` サポート クラスを利用して、指定されたコールバックが完了するまでにかかるミリ秒数を測定できます。

    <?php

    use App\Models\User;
    use Illuminate\Support\Benchmark;

    Benchmark::dd(fn () => User::find(1)); // 0.1 ms

    Benchmark::dd([
        'Scenario 1' => fn () => User::count(), // 0.5 ms
        'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
    ]);

デフォルトでは、指定されたコールバックは 1 回 (1 回の反復) 実行され、その期間はブラウザ/コンソールに表示されます。

コールバックを複数回呼び出すには、コールバックを呼び出す反復回数をメソッドの 2 番目の引数として指定できます。コールバックを複数回実行すると、`Benchmark` クラスは、すべての反復にわたってコールバックの実行にかかった平均ミリ秒数を返します。

    Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms

<a name="lottery"></a>
### 宝くじ

Laravel の宝くじクラスは、指定されたオッズのセットに基づいてコールバックを実行するために使用できます。これは、受信リクエストの一部のコードのみを実行したい場合に特に便利です。

    use Illuminate\Support\Lottery;

    Lottery::odds(1, 20)
        ->winner(fn () => $user->won())
        ->loser(fn () => $user->lost())
        ->choose();

Laravel のロッタリークラスを他の Laravel 機能と組み合わせることができます。たとえば、低速クエリのほんの一部だけを例外ハンドラーに報告したい場合があります。また、lottery クラスは呼び出し可能であるため、呼び出し可能オブジェクトを受け入れる任意のメソッドにクラスのインスタンスを渡すことができます。

    use Carbon\CarbonInterval;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\Lottery;

    DB::whenQueryingForLongerThan(
        CarbonInterval::seconds(2),
        Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
    );

<a name="testing-lotteries"></a>
#### 宝くじのテスト

Laravel には、アプリケーションの宝くじ呼び出しを簡単にテストできるようにするための簡単なメソッドがいくつか用意されています。

    // Lottery will always win...
    Lottery::alwaysWin();

    // Lottery will always lose...
    Lottery::alwaysLose();

    // Lottery will win then lose, and finally return to normal behavior...
    Lottery::fix([true, false]);

    // Lottery will return to normal behavior...
    Lottery::determineResultsNormally();

