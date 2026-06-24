<!-- # Collections -->
# Collections

- [Introduction](#introduction)
    - [Creating Collections](#creating-collections)
    - [Extending Collections](#extending-collections)
- [Available Methods](#available-methods)
- [Higher Order Messages](#higher-order-messages)
- [Lazy Collections](#lazy-collections)
    - [Introduction](#lazy-collection-introduction)
    - [Creating Lazy Collections](#creating-lazy-collections)
    - [The Enumerable Contract](#the-enumerable-contract)
    - [Lazy Collection Methods](#lazy-collection-methods)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The `Illuminate\Support\Collection` class provides a fluent, convenient wrapper for working with arrays of data. For example, check out the following code. We'll use the `collect` helper to create a new collection instance from the array, run the `strtoupper` function on each element, and then remove all empty elements: -->
`Illuminate\Support\Collection` クラスは、データの配列を操作するための流暢で便利なラッパーを提供します。たとえば、次のコードを確認してください。 `collect` ヘルパを使用して配列から新しいコレクション インスタンスを作成し、各要素に対して `strtoupper` 関数を実行して、空の要素をすべて削除します。

```
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

<!-- As you can see, the `Collection` class allows you to chain its methods to perform fluent mapping and reducing of the underlying array. In general, collections are immutable, meaning every `Collection` method returns an entirely new `Collection` instance. -->
ご覧のとおり、`Collection` クラスを使用すると、そのメソッドを連鎖させて、基になる配列のスムーズなマッピングと削減を実行できます。一般に、コレクションは不変です。つまり、すべての `Collection` メソッドはまったく新しい `Collection` インスタンスを返します。

<a name="creating-collections"></a>
<!-- ### Creating Collections -->
### Creating Collections

<!-- As mentioned above, the `collect` helper returns a new `Illuminate\Support\Collection` instance for the given array. So, creating a collection is as simple as: -->
前述したように、`collect` ヘルパは、指定された配列の新しい `Illuminate\Support\Collection` インスタンスを返します。したがって、コレクションの作成は次のように簡単です。

```
$collection = collect([1, 2, 3]);
```

> [!NOTE]
> [Eloquent](/docs/11.x/eloquent) クエリの結果は、常に `Collection` インスタンスとして返されます。

<a name="extending-collections"></a>
<!-- ### Extending Collections -->
### Extending Collections

<!-- Collections are "macroable", which allows you to add additional methods to the `Collection` class at run time. The `Illuminate\Support\Collection` class' `macro` method accepts a closure that will be executed when your macro is called. The macro closure may access the collection's other methods via `$this`, just as if it were a real method of the collection class. For example, the following code adds a `toUpper` method to the `Collection` class: -->
コレクションは「マクロ可能」であるため、実行時に `Collection` クラスにメソッドを追加できます。 `Illuminate\Support\Collection` クラスの `macro` メソッドは、マクロが呼び出されたときに実行されるクロージャを受け入れます。マクロ クロージャは、あたかもコレクション クラスの実際のメソッドであるかのように、`$this` を介してコレクションの他のメソッドにアクセスできます。たとえば、次のコードは、`toUpper` メソッドを `Collection` クラスに追加します。

```
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

Collection::macro('toUpper', function () {
    return $this->map(function (string $value) {
        return Str::upper($value);
    });
});

$collection = collect(['first', 'second']);

$upper = $collection->toUpper();

// ['FIRST', 'SECOND']
```

<!-- Typically, you should declare collection macros in the `boot` method of a [service provider](/docs/11.x/providers). -->
通常、コレクション マクロは、[service provider](/docs/11.x/providers) の `boot` メソッドで宣言する必要があります。

<a name="macro-arguments"></a>
<!-- #### Macro Arguments -->
#### Macro Arguments

<!-- If necessary, you may define macros that accept additional arguments: -->
必要に応じて、追加の引数を受け入れるマクロを定義できます。

```
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Lang;

Collection::macro('toLocale', function (string $locale) {
    return $this->map(function (string $value) use ($locale) {
        return Lang::get($value, [], $locale);
    });
});

$collection = collect(['first', 'second']);

$translated = $collection->toLocale('es');
```

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods

<!-- For the majority of the remaining collection documentation, we'll discuss each method available on the `Collection` class. Remember, all of these methods may be chained to fluently manipulate the underlying array. Furthermore, almost every method returns a new `Collection` instance, allowing you to preserve the original copy of the collection when necessary: -->
残りのコレクションのドキュメントの大部分では、`Collection` クラスで使用できる各メソッドについて説明します。これらのメソッドはすべて、基礎となる配列をスムーズに操作するために連鎖させることができることに注意してください。さらに、ほぼすべてのメソッドは新しい `Collection` インスタンスを返すため、必要に応じてコレクションの元のコピーを保存できます。

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[after](#method-after)
[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[before](#method-before)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collapseWithKeys](#method-collapsewithkeys)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsOneItem](#method-containsoneitem)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffAssocUsing](#method-diffassocusing)
[diffKeys](#method-diffkeys)
[doesntContain](#method-doesntcontain)
[dot](#method-dot)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[ensure](#method-ensure)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectUsing](#method-intersectusing)
[intersectAssoc](#method-intersectAssoc)
[intersectAssocUsing](#method-intersectassocusing)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[lazy](#method-lazy)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[multiply](#method-multiply)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[percentage](#method-percentage)
[pipe](#method-pipe)
[pipeInto](#method-pipeinto)
[pipeThrough](#method-pipethrough)
[pluck](#method-pluck)
[pop](#method-pop)
[prepend](#method-prepend)
[pull](#method-pull)
[push](#method-push)
[put](#method-put)
[random](#method-random)
[range](#method-range)
[reduce](#method-reduce)
[reduceSpread](#method-reduce-spread)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[select](#method-select)
[shift](#method-shift)
[shuffle](#method-shuffle)
[skip](#method-skip)
[skipUntil](#method-skipuntil)
[skipWhile](#method-skipwhile)
[slice](#method-slice)
[sliding](#method-sliding)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortDesc](#method-sortdesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[sortKeysUsing](#method-sortkeysusing)
[splice](#method-splice)
[split](#method-split)
[splitIn](#method-splitin)
[sum](#method-sum)
[take](#method-take)
[takeUntil](#method-takeuntil)
[takeWhile](#method-takewhile)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[transform](#method-transform)
[undot](#method-undot)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[value](#method-value)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[whereNotNull](#method-wherenotnull)
[whereNull](#method-wherenull)
[wrap](#method-wrap)
[zip](#method-zip)
-->
[after](#method-after)
[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[before](#method-before)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collapseWithKeys](#method-collapsewithkeys)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsOneItem](#method-containsoneitem)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffAssocUsing](#method-diffassocusing)
[diffKeys](#method-diffkeys)
[doesntContain](#method-doesntcontain)
[dot](#method-dot)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[ensure](#method-ensure)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectUsing](#method-intersectusing)
[intersectAssoc](#method-intersectAssoc)
[intersectAssocUsing](#method-intersectassocusing)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[lazy](#method-lazy)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[multiply](#method-multiply)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[percentage](#method-percentage)
[pipe](#method-pipe)
[pipeInto](#method-pipeinto)
[pipeThrough](#method-pipethrough)
[pluck](#method-pluck)
[pop](#method-pop)
[prepend](#method-prepend)
[pull](#method-pull)
[push](#method-push)
[put](#method-put)
[random](#method-random)
[range](#method-range)
[reduce](#method-reduce)
[reduceSpread](#method-reduce-spread)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[select](#method-select)
[shift](#method-shift)
[shuffle](#method-shuffle)
[skip](#method-skip)
[skipUntil](#method-skipuntil)
[skipWhile](#method-skipwhile)
[slice](#method-slice)
[sliding](#method-sliding)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortDesc](#method-sortdesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[sortKeysUsing](#method-sortkeysusing)
[splice](#method-splice)
[split](#method-split)
[splitIn](#method-splitin)
[sum](#method-sum)
[take](#method-take)
[takeUntil](#method-takeuntil)
[takeWhile](#method-takewhile)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[transform](#method-transform)
[undot](#method-undot)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[value](#method-value)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[whereNotNull](#method-wherenotnull)
[whereNull](#method-wherenull)
[wrap](#method-wrap)
[zip](#method-zip)

<!-- </div> -->
</div>

<a name="method-listing"></a>
<!-- ## Method Listing -->
## Method Listing

<a name="method-after"></a>
<!-- #### `after()` -->
#### `after()`
<!-- The `after` method returns the item after the given item. `null` is returned if the given item is not found or is the last item: -->
`after` メソッドは、指定された項目の後の項目を返します。指定された項目が見つからない場合、または最後の項目である場合は、`null` が返されます。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

<!-- This method searches for the given item using "loose" comparison, meaning a string containing an integer value will be considered equal to an integer of the same value. To use "strict" comparison, you may provide the `strict` argument to the method: -->
このメソッドは、「緩やかな」比較を使用して指定された項目を検索します。つまり、整数値を含む文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用するには、メソッドに `strict` 引数を指定します。

```
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

<!-- Alternatively, you may provide your own closure to search for the first item that passes a given truth test: -->
あるいは、独自のクロージャを提供して、指定された真理テストに合格する最初の項目を検索することもできます。

```
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
<!-- #### `all()` -->
#### `all()`
<!-- The `all` method returns the underlying array represented by the collection: -->
`all` メソッドは、コレクションによって表される基になる配列を返します。

```
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
<!-- #### `average()` -->
#### `average()`
<!-- Alias for the [`avg`](#method-avg) method. -->
[`avg`](#method-avg) メソッドのエイリアス。

<a name="method-avg"></a>
<!-- #### `avg()` -->
#### `avg()`
<!-- The `avg` method returns the [average value](https://en.wikipedia.org/wiki/Average) of a given key: -->
`avg` メソッドは、指定されたキーの [average value](https://en.wikipedia.org/wiki/Average) を返します。

```
$average = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->avg('foo');

// 20

$average = collect([1, 1, 2, 4])->avg();

// 2
```

<a name="method-before"></a>
<!-- #### `before()` -->
#### `before()`
<!-- The `before` method is the opposite of the [`after`](#method-after) method. It returns the item before the given item. `null` is returned if the given item is not found or is the first item: -->
`before` メソッドは、[`after`](#method-after) メソッドの逆です。指定された項目の前の項目を返します。指定された項目が見つからない場合、または最初の項目である場合は、`null` が返されます。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->before(3);

// 2

$collection->before(1);

// null

collect([2, 4, 6, 8])->before('4', strict: true);

// null

collect([2, 4, 6, 8])->before(function (int $item, int $key) {
    return $item > 5;
});

// 4
```

<a name="method-chunk"></a>
<!-- #### `chunk()` -->
#### `chunk()`
<!-- The `chunk` method breaks the collection into multiple, smaller collections of a given size: -->
`chunk` メソッドは、コレクションを指定されたサイズの複数の小さなコレクションに分割します。

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

<!-- This method is especially useful in [views](/docs/11.x/views) when working with a grid system such as [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/). For example, imagine you have a collection of [Eloquent](/docs/11.x/eloquent) models you want to display in a grid: -->
この方法は、[views](https://getbootstrap.com/docs/5.3/layout/grid/) などのグリッド システムを操作する場合、[Bootstrap](/docs/11.x/views) で特に便利です。たとえば、グリッドに表示したい [Eloquent](/docs/11.x/eloquent) モデルのコレクションがあるとします。

```blade
@foreach ($products->chunk(3) as $chunk)
    <div class="row">
        @foreach ($chunk as $product)
            <div class="col-xs-4">{{ $product->name }}</div>
        @endforeach
    </div>
@endforeach
```

<a name="method-chunkwhile"></a>
<!-- #### `chunkWhile()` -->
#### `chunkWhile()`
<!-- The `chunkWhile` method breaks the collection into multiple, smaller collections based on the evaluation of the given callback. The `$chunk` variable passed to the closure may be used to inspect the previous element: -->
`chunkWhile` メソッドは、指定されたコールバックの評価に基づいて、コレクションを複数の小さなコレクションに分割します。クロージャに渡される `$chunk` 変数は、前の要素を検査するために使用できます。

```
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

<a name="method-collapse"></a>
<!-- #### `collapse()` -->
#### `collapse()`
<!-- The `collapse` method collapses a collection of arrays into a single, flat collection: -->
`collapse` メソッドは、配列のコレクションを単一のフラットなコレクションに折りたたみます。

```
$collection = collect([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]);

$collapsed = $collection->collapse();

$collapsed->all();

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-collapsewithkeys"></a>
<!-- #### `collapseWithKeys()` -->
#### `collapseWithKeys()`
<!-- The `collapseWithKeys` method flattens a collection of arrays or collections into a single collection, keeping the original keys intact: -->
`collapseWithKeys` メソッドは、元のキーをそのまま保持したまま、配列またはコレクションのコレクションを 1 つのコレクションにフラット化します。

```
$collection = collect([
  ['first'  => collect([1, 2, 3])],
  ['second' => [4, 5, 6]],
  ['third'  => collect([7, 8, 9])]
]);


$collapsed = $collection->collapseWithKeys();

$collapsed->all();

// [
//     'first'  => [1, 2, 3],
//     'second' => [4, 5, 6],
//     'third'  => [7, 8, 9],
// ]
```

<a name="method-collect"></a>
<!-- #### `collect()` -->
#### `collect()`
<!-- The `collect` method returns a new `Collection` instance with the items currently in the collection: -->
`collect` メソッドは、現在コレクション内の項目を含む新しい `Collection` インスタンスを返します。

```
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

<!-- The `collect` method is primarily useful for converting [lazy collections](#lazy-collections) into standard `Collection` instances: -->
`collect` メソッドは、主に [lazy collections](#lazy-collections) を標準の `Collection` インスタンスに変換する場合に役立ちます。

```
$lazyCollection = LazyCollection::make(function () {
    yield 1;
    yield 2;
    yield 3;
});

$collection = $lazyCollection->collect();

$collection::class;

// 'Illuminate\Support\Collection'

$collection->all();

// [1, 2, 3]
```

> [!NOTE]
> `collect` メソッドは、`Enumerable` のインスタンスがあり、非遅延コレクション インスタンスが必要な場合に特に便利です。 `collect()` は `Enumerable` コントラクトの一部であるため、これを安全に使用して `Collection` インスタンスを取得できます。

<a name="method-combine"></a>
<!-- #### `combine()` -->
#### `combine()`
<!-- The `combine` method combines the values of the collection, as keys, with the values of another array or collection: -->
`combine` メソッドは、コレクションの値をキーとして、別の配列またはコレクションの値と組み合わせます。

```
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
<!-- #### `concat()` -->
#### `concat()`
<!-- The `concat` method appends the given `array` or collection's values onto the end of another collection: -->
`concat` メソッドは、指定された `array` またはコレクションの値を別のコレクションの末尾に追加します。

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

<!-- The `concat` method numerically reindexes keys for items concatenated onto the original collection. To maintain keys in associative collections, see the [merge](#method-merge) method. -->
`concat` メソッドは、元のコレクションに連結された項目のキーを数値的に再インデックスします。連想コレクション内のキーを維持するには、[merge](#method-merge) メソッドを参照してください。

<a name="method-contains"></a>
<!-- #### `contains()` -->
#### `contains()`
<!-- The `contains` method determines whether the collection contains a given item. You may pass a closure to the `contains` method to determine if an element exists in the collection matching a given truth test: -->
`contains` メソッドは、コレクションに特定の項目が含まれているかどうかを判断します。クロージャを `contains` メソッドに渡して、指定された真理値テストに一致する要素がコレクション内に存在するかどうかを判断できます。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `contains` method to determine whether the collection contains a given item value: -->
あるいは、文字列を `contains` メソッドに渡して、コレクションに特定の項目値が含まれているかどうかを判断することもできます。

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

<!-- You may also pass a key / value pair to the `contains` method, which will determine if the given pair exists in the collection: -->
キーと値のペアを `contains` メソッドに渡すこともできます。これにより、指定されたペアがコレクション内に存在するかどうかが判断されます。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

<!-- The `contains` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [`containsStrict`](#method-containsstrict) method to filter using "strict" comparisons. -->
`contains` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`containsStrict`](#method-containsstrict) メソッドを使用します。

<!-- For the inverse of `contains`, see the [doesntContain](#method-doesntcontain) method. -->
`contains` の逆については、[doesntContain](#method-doesntcontain) メソッドを参照してください。

<a name="method-containsoneitem"></a>
<!-- #### `containsOneItem()` -->
#### `containsOneItem()`
<!-- The `containsOneItem` method determines whether the collection contains a single item: -->
`containsOneItem` メソッドは、コレクションに単一の項目が含まれているかどうかを判断します。

```
collect([])->containsOneItem();

// false

collect(['1'])->containsOneItem();

// true

collect(['1', '2'])->containsOneItem();

// false
```

<a name="method-containsstrict"></a>
<!-- #### `containsStrict()` -->
#### `containsStrict()`
<!-- This method has the same signature as the [`contains`](#method-contains) method; however, all values are compared using "strict" comparisons. -->
このメソッドには、[`contains`](#method-contains) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

> [!NOTE]
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-contains) を使用すると、このメソッドの動作が変更されます。

<a name="method-count"></a>
<!-- #### `count()` -->
#### `count()`
<!-- The `count` method returns the total number of items in the collection: -->
`count` メソッドは、コレクション内の項目の合計数を返します。

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
<!-- #### `countBy()` -->
#### `countBy()`
<!-- The `countBy` method counts the occurrences of values in the collection. By default, the method counts the occurrences of every element, allowing you to count certain "types" of elements in the collection: -->
`countBy` メソッドは、コレクション内の値の出現をカウントします。デフォルトでは、このメソッドはすべての要素の出現をカウントするため、コレクション内の要素の特定の「タイプ」をカウントできます。

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

<!-- You pass a closure to the `countBy` method to count all items by a custom value: -->
カスタム値ですべての項目をカウントするには、クロージャを `countBy` メソッドに渡します。

```
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function (string $email) {
    return substr(strrchr($email, "@"), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
<!-- #### `crossJoin()` -->
#### `crossJoin()`
<!-- The `crossJoin` method cross joins the collection's values among the given arrays or collections, returning a Cartesian product with all possible permutations: -->
`crossJoin` メソッドは、指定された配列またはコレクション間でコレクションの値を交差結合し、すべての可能な順列を含むデカルト積を返します。

```
$collection = collect([1, 2]);

$matrix = $collection->crossJoin(['a', 'b']);

$matrix->all();

/*
    [
        [1, 'a'],
        [1, 'b'],
        [2, 'a'],
        [2, 'b'],
    ]
*/

$collection = collect([1, 2]);

$matrix = $collection->crossJoin(['a', 'b'], ['I', 'II']);

$matrix->all();

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

<a name="method-dd"></a>
<!-- #### `dd()` -->
#### `dd()`
<!-- The `dd` method dumps the collection's items and ends execution of the script: -->
`dd` メソッドは、コレクションのアイテムをダンプし、スクリプトの実行を終了します。

```
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dd();

/*
    Collection {
        #items: array:2 [
            0 => "John Doe"
            1 => "Jane Doe"
        ]
    }
*/
```

<!-- If you do not want to stop executing the script, use the [`dump`](#method-dump) method instead. -->
スクリプトの実行を停止したくない場合は、代わりに [`dump`](#method-dump) メソッドを使用してください。

<a name="method-diff"></a>
<!-- #### `diff()` -->
#### `diff()`
<!-- The `diff` method compares the collection against another collection or a plain PHP `array` based on its values. This method will return the values in the original collection that are not present in the given collection: -->
`diff` メソッドは、その値に基づいて、コレクションを別のコレクションまたはプレーンな PHP `array` と比較します。このメソッドは、指定されたコレクションに存在しない元のコレクションの値を返します。

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-diff) を使用すると、このメソッドの動作が変更されます。

<a name="method-diffassoc"></a>
<!-- #### `diffAssoc()` -->
#### `diffAssoc()`
<!-- The `diffAssoc` method compares the collection against another collection or a plain PHP `array` based on its keys and values. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffAssoc` メソッドは、キーと値に基づいてコレクションを別のコレクションまたはプレーン PHP `array` と比較します。このメソッドは、指定されたコレクションに存在しない、元のコレクション内のキーと値のペアを返します。

```
$collection = collect([
    'color' => 'orange',
    'type' => 'fruit',
    'remain' => 6,
]);

$diff = $collection->diffAssoc([
    'color' => 'yellow',
    'type' => 'fruit',
    'remain' => 3,
    'used' => 6,
]);

$diff->all();

// ['color' => 'orange', 'remain' => 6]
```

<a name="method-diffassocusing"></a>
<!-- #### `diffAssocUsing()` -->
#### `diffAssocUsing()`
<!-- Unlike `diffAssoc`, `diffAssocUsing` accepts a user supplied callback function for the indices comparison: -->
`diffAssoc` とは異なり、`diffAssocUsing` はインデックス比較のためにユーザー指定のコールバック関数を受け入れます。

```
$collection = collect([
    'color' => 'orange',
    'type' => 'fruit',
    'remain' => 6,
]);

$diff = $collection->diffAssocUsing([
    'Color' => 'yellow',
    'Type' => 'fruit',
    'Remain' => 3,
], 'strnatcasecmp');

$diff->all();

// ['color' => 'orange', 'remain' => 6]
```

<!-- The callback must be a comparison function that returns an integer less than, equal to, or greater than zero. For more information, refer to the PHP documentation on [`array_diff_uassoc`](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters), which is the PHP function that the `diffAssocUsing` method utilizes internally. -->
コールバックは、ゼロ以下、ゼロ以上の整数を返す比較関数である必要があります。詳細については、[`array_diff_uassoc`](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) に関する PHP ドキュメントを参照してください。これは、`diffAssocUsing` メソッドが内部で使用する PHP 関数です。

<a name="method-diffkeys"></a>
<!-- #### `diffKeys()` -->
#### `diffKeys()`
<!-- The `diffKeys` method compares the collection against another collection or a plain PHP `array` based on its keys. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffKeys` メソッドは、キーに基づいてコレクションを別のコレクションまたはプレーン PHP `array` と比較します。このメソッドは、指定されたコレクションに存在しない、元のコレクション内のキーと値のペアを返します。

```
$collection = collect([
    'one' => 10,
    'two' => 20,
    'three' => 30,
    'four' => 40,
    'five' => 50,
]);

$diff = $collection->diffKeys([
    'two' => 2,
    'four' => 4,
    'six' => 6,
    'eight' => 8,
]);

$diff->all();

// ['one' => 10, 'three' => 30, 'five' => 50]
```

<a name="method-doesntcontain"></a>
<!-- #### `doesntContain()` -->
#### `doesntContain()`
<!-- The `doesntContain` method determines whether the collection does not contain a given item. You may pass a closure to the `doesntContain` method to determine if an element does not exist in the collection matching a given truth test: -->
`doesntContain` メソッドは、コレクションに特定の項目が含まれていないかどうかを判断します。クロージャを `doesntContain` メソッドに渡して、指定された真理値テストに一致する要素がコレクション内に存在するかどうかを判断できます。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `doesntContain` method to determine whether the collection does not contain a given item value: -->
あるいは、文字列を `doesntContain` メソッドに渡して、コレクションに特定の項目値が含まれていないかどうかを判断することもできます。

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

<!-- You may also pass a key / value pair to the `doesntContain` method, which will determine if the given pair does not exist in the collection: -->
キーと値のペアを `doesntContain` メソッドに渡すこともできます。これにより、指定されたペアがコレクションに存在しないかどうかが判断されます。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

<!-- The `doesntContain` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. -->
`doesntContain` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。

<a name="method-dot"></a>
<!-- #### `dot()` -->
#### `dot()`
<!-- The `dot` method flattens a multi-dimensional collection into a single level collection that uses "dot" notation to indicate depth: -->
`dot` メソッドは、多次元コレクションを、深さを示すために「ドット」表記を使用する単一レベルのコレクションに平坦化します。

```
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
<!-- #### `dump()` -->
#### `dump()`
<!-- The `dump` method dumps the collection's items: -->
`dump` メソッドは、コレクションの項目をダンプします。

```
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dump();

/*
    Collection {
        #items: array:2 [
            0 => "John Doe"
            1 => "Jane Doe"
        ]
    }
*/
```

<!-- If you want to stop executing the script after dumping the collection, use the [`dd`](#method-dd) method instead. -->
コレクションのダンプ後にスクリプトの実行を停止する場合は、代わりに [`dd`](#method-dd) メソッドを使用します。

<a name="method-duplicates"></a>
<!-- #### `duplicates()` -->
#### `duplicates()`
<!-- The `duplicates` method retrieves and returns duplicate values from the collection: -->
`duplicates` メソッドは、コレクションから重複した値を取得して返します。

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

<!-- If the collection contains arrays or objects, you can pass the key of the attributes that you wish to check for duplicate values: -->
コレクションに配列またはオブジェクトが含まれている場合は、重複値をチェックする属性のキーを渡すことができます。

```
$employees = collect([
    ['email' => 'abigail@example.com', 'position' => 'Developer'],
    ['email' => 'james@example.com', 'position' => 'Designer'],
    ['email' => 'victoria@example.com', 'position' => 'Developer'],
]);

$employees->duplicates('position');

// [2 => 'Developer']
```

<a name="method-duplicatesstrict"></a>
<!-- #### `duplicatesStrict()` -->
#### `duplicatesStrict()`
<!-- This method has the same signature as the [`duplicates`](#method-duplicates) method; however, all values are compared using "strict" comparisons. -->
このメソッドには、[`duplicates`](#method-duplicates) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-each"></a>
<!-- #### `each()` -->
#### `each()`
<!-- The `each` method iterates over the items in the collection and passes each item to a closure: -->
`each` メソッドは、コレクション内の項目を反復処理し、各項目をクロージャーに渡します。

```
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

<!-- If you would like to stop iterating through the items, you may return `false` from your closure: -->
項目の反復処理を停止したい場合は、クロージャから `false` を返すことができます。

```
$collection->each(function (int $item, int $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
<!-- #### `eachSpread()` -->
#### `eachSpread()`
<!-- The `eachSpread` method iterates over the collection's items, passing each nested item value into the given callback: -->
`eachSpread` メソッドはコレクションの項目を反復処理し、ネストされた各項目の値を指定されたコールバックに渡します。

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

<!-- You may stop iterating through the items by returning `false` from the callback: -->
コールバックから `false` を返すことで、項目の反復処理を停止できます。

```
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
<!-- #### `ensure()` -->
#### `ensure()`
<!-- The `ensure` method may be used to verify that all elements of a collection are of a given type or list of types. Otherwise, an `UnexpectedValueException` will be thrown: -->
`ensure` メソッドは、コレクションのすべての要素が特定の型または型のリストであることを検証するために使用できます。それ以外の場合は、`UnexpectedValueException` がスローされます。

```
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

<!-- Primitive types such as `string`, `int`, `float`, `bool`, and `array` may also be specified: -->
`string`、`int`、`float`、`bool`、`array` などのプリミティブ タイプも指定できます。

```
return $collection->ensure('int');
```

> [!WARNING]
> `ensure` メソッドは、異なるタイプの要素が後でコレクションに追加されないことを保証しません。

<a name="method-every"></a>
<!-- #### `every()` -->
#### `every()`
<!-- The `every` method may be used to verify that all elements of a collection pass a given truth test: -->
`every` メソッドは、コレクションのすべての要素が指定された真理テストに合格することを検証するために使用できます。

```
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

<!-- If the collection is empty, the `every` method will return true: -->
コレクションが空の場合、`every` メソッドは true を返します。

```
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
<!-- #### `except()` -->
#### `except()`
<!-- The `except` method returns all items in the collection except for those with the specified keys: -->
`except` メソッドは、指定されたキーを持つアイテムを除く、コレクション内のすべてのアイテムを返します。

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

<!-- For the inverse of `except`, see the [only](#method-only) method. -->
`except` の逆については、[only](#method-only) メソッドを参照してください。

> [!NOTE]
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-except) を使用すると、このメソッドの動作が変更されます。

<a name="method-filter"></a>
<!-- #### `filter()` -->
#### `filter()`
<!-- The `filter` method filters the collection using the given callback, keeping only those items that pass a given truth test: -->
`filter` メソッドは、指定されたコールバックを使用してコレクションをフィルタリングし、指定された真実テストに合格した項目のみを保持します。

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

<!-- If no callback is supplied, all entries of the collection that are equivalent to `false` will be removed: -->
コールバックが指定されていない場合は、`false` に相当するコレクションのすべてのエントリが削除されます。

```
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

<!-- For the inverse of `filter`, see the [reject](#method-reject) method. -->
`filter` の逆については、[reject](#method-reject) メソッドを参照してください。

<a name="method-first"></a>
<!-- #### `first()` -->
#### `first()`
<!-- The `first` method returns the first element in the collection that passes a given truth test: -->
`first` メソッドは、指定された真理テストに合格したコレクション内の最初の要素を返します。

```
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

<!-- You may also call the `first` method with no arguments to get the first element in the collection. If the collection is empty, `null` is returned: -->
引数なしで `first` メソッドを呼び出して、コレクションの最初の要素を取得することもできます。コレクションが空の場合、`null` が返されます。

```
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
<!-- #### `firstOrFail()` -->
#### `firstOrFail()`
<!-- The `firstOrFail` method is identical to the `first` method; however, if no result is found, an `Illuminate\Support\ItemNotFoundException` exception will be thrown: -->
`firstOrFail` メソッドは、`first` メソッドと同じです。ただし、結果が見つからない場合は、`Illuminate\Support\ItemNotFoundException` 例外がスローされます。

```
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// Throws ItemNotFoundException...
```

<!-- You may also call the `firstOrFail` method with no arguments to get the first element in the collection. If the collection is empty, an `Illuminate\Support\ItemNotFoundException` exception will be thrown: -->
引数なしで `firstOrFail` メソッドを呼び出して、コレクションの最初の要素を取得することもできます。コレクションが空の場合、`Illuminate\Support\ItemNotFoundException` 例外がスローされます。

```
collect([])->firstOrFail();

// Throws ItemNotFoundException...
```

<a name="method-first-where"></a>
<!-- #### `firstWhere()` -->
#### `firstWhere()`
<!-- The `firstWhere` method returns the first element in the collection with the given key / value pair: -->
`firstWhere` メソッドは、指定されたキーと値のペアを持つコレクション内の最初の要素を返します。

```
$collection = collect([
    ['name' => 'Regena', 'age' => null],
    ['name' => 'Linda', 'age' => 14],
    ['name' => 'Diego', 'age' => 23],
    ['name' => 'Linda', 'age' => 84],
]);

$collection->firstWhere('name', 'Linda');

// ['name' => 'Linda', 'age' => 14]
```

<!-- You may also call the `firstWhere` method with a comparison operator: -->
比較演算子を使用して `firstWhere` メソッドを呼び出すこともできます。

```
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

<!-- Like the [where](#method-where) method, you may pass one argument to the `firstWhere` method. In this scenario, the `firstWhere` method will return the first item where the given item key's value is "truthy": -->
[where](#method-where) メソッドと同様に、`firstWhere` メソッドに 1 つの引数を渡すことができます。このシナリオでは、`firstWhere` メソッドは、指定された項目キーの値が「真実」である最初の項目を返します。

```
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
<!-- #### `flatMap()` -->
#### `flatMap()`
<!-- The `flatMap` method iterates through the collection and passes each value to the given closure. The closure is free to modify the item and return it, thus forming a new collection of modified items. Then, the array is flattened by one level: -->
`flatMap` メソッドはコレクションを反復処理し、各値を指定されたクロージャに渡します。クロージャは自由に項目を変更して返すことができるため、変更された項目の新しいコレクションが形成されます。次に、配列は 1 レベル平坦化されます。

```
$collection = collect([
    ['name' => 'Sally'],
    ['school' => 'Arkansas'],
    ['age' => 28]
]);

$flattened = $collection->flatMap(function (array $values) {
    return array_map('strtoupper', $values);
});

$flattened->all();

// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];
```

<a name="method-flatten"></a>
<!-- #### `flatten()` -->
#### `flatten()`
<!-- The `flatten` method flattens a multi-dimensional collection into a single dimension: -->
`flatten` メソッドは、多次元コレクションを単一次元にフラット化します。

```
$collection = collect([
    'name' => 'taylor',
    'languages' => [
        'php', 'javascript'
    ]
]);

$flattened = $collection->flatten();

$flattened->all();

// ['taylor', 'php', 'javascript'];
```

<!-- If necessary, you may pass the `flatten` method a "depth" argument: -->
必要に応じて、`flatten` メソッドに「深さ」引数を渡すことができます。

```
$collection = collect([
    'Apple' => [
        [
            'name' => 'iPhone 6S',
            'brand' => 'Apple'
        ],
    ],
    'Samsung' => [
        [
            'name' => 'Galaxy S7',
            'brand' => 'Samsung'
        ],
    ],
]);

$products = $collection->flatten(1);

$products->values()->all();

/*
    [
        ['name' => 'iPhone 6S', 'brand' => 'Apple'],
        ['name' => 'Galaxy S7', 'brand' => 'Samsung'],
    ]
*/
```

<!-- In this example, calling `flatten` without providing the depth would have also flattened the nested arrays, resulting in `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`. Providing a depth allows you to specify the number of levels nested arrays will be flattened. -->
この例では、深さを指定せずに `flatten` を呼び出すと、ネストされた配列もフラット化され、`['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']` になります。深さを指定すると、ネストされた配列を平坦化するレベルの数を指定できます。

<a name="method-flip"></a>
<!-- #### `flip()` -->
#### `flip()`
<!-- The `flip` method swaps the collection's keys with their corresponding values: -->
`flip` メソッドは、コレクションのキーを対応する値と交換します。

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
<!-- #### `forget()` -->
#### `forget()`
<!-- The `forget` method removes an item from the collection by its key: -->
`forget` メソッドは、キーによってコレクションから項目を削除します。

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

// Forget a single key...
$collection->forget('name');

// ['framework' => 'laravel']

// Forget multiple keys...
$collection->forget(['name', 'framework']);

// []
```

> [!WARNING]
> 他のほとんどのコレクション メソッドとは異なり、`forget` は変更された新しいコレクションを返しません。呼び出されたコレクションを変更して返します。

<a name="method-forpage"></a>
<!-- #### `forPage()` -->
#### `forPage()`
<!-- The `forPage` method returns a new collection containing the items that would be present on a given page number. The method accepts the page number as its first argument and the number of items to show per page as its second argument: -->
`forPage` メソッドは、指定されたページ番号に存在する項目を含む新しいコレクションを返します。このメソッドは、最初の引数としてページ番号を受け入れ、2 番目の引数としてページごとに表示するアイテムの数を受け入れます。

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-get"></a>
<!-- #### `get()` -->
#### `get()`
<!-- The `get` method returns the item at a given key. If the key does not exist, `null` is returned: -->
`get` メソッドは、指定されたキーの項目を返します。キーが存在しない場合は、`null` が返されます。

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

<!-- You may optionally pass a default value as the second argument: -->
オプションで、デフォルト値を 2 番目の引数として渡すこともできます。

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('age', 34);

// 34
```

<!-- You may even pass a callback as the method's default value. The result of the callback will be returned if the specified key does not exist: -->
コールバックをメソッドのデフォルト値として渡すこともできます。指定されたキーが存在しない場合は、コールバックの結果が返されます。

```
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
<!-- #### `groupBy()` -->
#### `groupBy()`
<!-- The `groupBy` method groups the collection's items by a given key: -->
`groupBy` メソッドは、指定されたキーによってコレクションの項目をグループ化します。

```
$collection = collect([
    ['account_id' => 'account-x10', 'product' => 'Chair'],
    ['account_id' => 'account-x10', 'product' => 'Bookcase'],
    ['account_id' => 'account-x11', 'product' => 'Desk'],
]);

$grouped = $collection->groupBy('account_id');

$grouped->all();

/*
    [
        'account-x10' => [
            ['account_id' => 'account-x10', 'product' => 'Chair'],
            ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ],
        'account-x11' => [
            ['account_id' => 'account-x11', 'product' => 'Desk'],
        ],
    ]
*/
```

<!-- Instead of passing a string `key`, you may pass a callback. The callback should return the value you wish to key the group by: -->
文字列 `key` を渡す代わりに、コールバックを渡すこともできます。コールバックは、次のようにしてグループのキーとなる値を返す必要があります。

```
$grouped = $collection->groupBy(function (array $item, int $key) {
    return substr($item['account_id'], -3);
});

$grouped->all();

/*
    [
        'x10' => [
            ['account_id' => 'account-x10', 'product' => 'Chair'],
            ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ],
        'x11' => [
            ['account_id' => 'account-x11', 'product' => 'Desk'],
        ],
    ]
*/
```

<!-- Multiple grouping criteria may be passed as an array. Each array element will be applied to the corresponding level within a multi-dimensional array: -->
複数のグループ化基準を配列として渡すことができます。各配列要素は、多次元配列内の対応するレベルに適用されます。

```
$data = new Collection([
    10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
    20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
    30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
    40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
]);

$result = $data->groupBy(['skill', function (array $item) {
    return $item['roles'];
}], preserveKeys: true);

/*
[
    1 => [
        'Role_1' => [
            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
        ],
        'Role_2' => [
            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
        ],
        'Role_3' => [
            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
        ],
    ],
    2 => [
        'Role_1' => [
            30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
        ],
        'Role_2' => [
            40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
        ],
    ],
];
*/
```

<a name="method-has"></a>
<!-- #### `has()` -->
#### `has()`
<!-- The `has` method determines if a given key exists in the collection: -->
`has` メソッドは、指定されたキーがコレクションに存在するかどうかを判断します。

```
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->has('product');

// true

$collection->has(['product', 'amount']);

// true

$collection->has(['amount', 'price']);

// false
```

<a name="method-hasany"></a>
<!-- #### `hasAny()` -->
#### `hasAny()`
<!-- The `hasAny` method determines whether any of the given keys exist in the collection: -->
`hasAny` メソッドは、指定されたキーのいずれかがコレクションに存在するかどうかを判断します。

```
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-implode"></a>
<!-- #### `implode()` -->
#### `implode()`
<!-- The `implode` method joins items in a collection. Its arguments depend on the type of items in the collection. If the collection contains arrays or objects, you should pass the key of the attributes you wish to join, and the "glue" string you wish to place between the values: -->
`implode` メソッドは、コレクション内の項目を結合します。その引数は、コレクション内の項目のタイプによって異なります。コレクションに配列またはオブジェクトが含まれている場合は、結合する属性のキーと、値の間に配置する「接着剤」文字列を渡す必要があります。

```
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// Desk, Chair
```

<!-- If the collection contains simple strings or numeric values, you should pass the "glue" as the only argument to the method: -->
コレクションに単純な文字列または数値が含まれている場合は、メソッドの唯一の引数として「接着剤」を渡す必要があります。

```
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

<!-- You may pass a closure to the `implode` method if you would like to format the values being imploded: -->
内部分解される値をフォーマットしたい場合は、`implode` メソッドにクロージャーを渡すことができます。

```
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// DESK, CHAIR
```

<a name="method-intersect"></a>
<!-- #### `intersect()` -->
#### `intersect()`
<!-- The `intersect` method removes any values from the original collection that are not present in the given `array` or collection. The resulting collection will preserve the original collection's keys: -->
`intersect` メソッドは、指定された `array` またはコレクションに存在しない値を元のコレクションから削除します。結果として得られるコレクションは、元のコレクションのキーを保持します。

```
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-intersect) を使用すると、このメソッドの動作が変更されます。

<a name="method-intersectusing"></a>
<!-- #### `intersectUsing()` -->
#### `intersectUsing()`
<!-- The `intersectUsing` method removes any values from the original collection that are not present in the given `array` or collection, using a custom callback to compare the values. The resulting collection will preserve the original collection's keys: -->
`intersectUsing` メソッドは、値を比較するカスタム コールバックを使用して、指定された `array` またはコレクションに存在しない値を元のコレクションから削除します。結果として得られるコレクションは、元のコレクションのキーを保持します。

```
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersectUsing(['desk', 'chair', 'bookcase'], function ($a, $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

<a name="method-intersectAssoc"></a>
<!-- #### `intersectAssoc()` -->
#### `intersectAssoc()`
<!-- The `intersectAssoc` method compares the original collection against another collection or `array`, returning the key / value pairs that are present in all of the given collections: -->
`intersectAssoc` メソッドは、元のコレクションを別のコレクションまたは `array` と比較し、指定されたすべてのコレクションに存在するキーと値のペアを返します。

```
$collection = collect([
    'color' => 'red',
    'size' => 'M',
    'material' => 'cotton'
]);

$intersect = $collection->intersectAssoc([
    'color' => 'blue',
    'size' => 'M',
    'material' => 'polyester'
]);

$intersect->all();

// ['size' => 'M']
```

<a name="method-intersectassocusing"></a>
<!-- #### `intersectAssocUsing()` -->
#### `intersectAssocUsing()`
<!-- The `intersectAssocUsing` method compares the original collection against another collection or `array`, returning the key / value pairs that are present in both, using a custom comparison callback to determine equality for both keys and values: -->
`intersectAssocUsing` メソッドは、元のコレクションを別のコレクションまたは `array` と比較し、両方に存在するキーと値のペアを返します。カスタム比較コールバックを使用して、キーと値の両方が等しいかどうかを判断します。

```
$collection = collect([
    'color' => 'red',
    'Size' => 'M',
    'material' => 'cotton',
]);

$intersect = $collection->intersectAssocUsing([
    'color' => 'blue',
    'size' => 'M',
    'material' => 'polyester',
], function ($a, $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// ['Size' => 'M']
```

<a name="method-intersectbykeys"></a>
<!-- #### `intersectByKeys()` -->
#### `intersectByKeys()`
<!-- The `intersectByKeys` method removes any keys and their corresponding values from the original collection that are not present in the given `array` or collection: -->
`intersectByKeys` メソッドは、指定された `array` またはコレクションに存在しないキーとそれに対応する値を元のコレクションから削除します。

```
$collection = collect([
    'serial' => 'UX301', 'type' => 'screen', 'year' => 2009,
]);

$intersect = $collection->intersectByKeys([
    'reference' => 'UX404', 'type' => 'tab', 'year' => 2011,
]);

$intersect->all();

// ['type' => 'screen', 'year' => 2009]
```

<a name="method-isempty"></a>
<!-- #### `isEmpty()` -->
#### `isEmpty()`
<!-- The `isEmpty` method returns `true` if the collection is empty; otherwise, `false` is returned: -->
`isEmpty` メソッドは、コレクションが空の場合は `true` を返します。それ以外の場合は、`false` が返されます。

```
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
<!-- #### `isNotEmpty()` -->
#### `isNotEmpty()`
<!-- The `isNotEmpty` method returns `true` if the collection is not empty; otherwise, `false` is returned: -->
コレクションが空でない場合、`isNotEmpty` メソッドは `true` を返します。それ以外の場合は、`false` が返されます。

```
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
<!-- #### `join()` -->
#### `join()`
<!-- The `join` method joins the collection's values with a string. Using this method's second argument, you may also specify how the final element should be appended to the string: -->
`join` メソッドは、コレクションの値を文字列と結合します。このメソッドの 2 番目の引数を使用して、最後の要素を文字列に追加する方法を指定することもできます。

```
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
<!-- #### `keyBy()` -->
#### `keyBy()`
<!-- The `keyBy` method keys the collection by the given key. If multiple items have the same key, only the last one will appear in the new collection: -->
`keyBy` メソッドは、指定されたキーによってコレクションにキーを設定します。複数の項目が同じキーを持つ場合、最後の項目だけが新しいコレクションに表示されます。

```
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$keyed = $collection->keyBy('product_id');

$keyed->all();

/*
    [
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

<!-- You may also pass a callback to the method. The callback should return the value to key the collection by: -->
メソッドにコールバックを渡すこともできます。コールバックは、次のようにしてコレクションのキーとなる値を返す必要があります。

```
$keyed = $collection->keyBy(function (array $item, int $key) {
    return strtoupper($item['product_id']);
});

$keyed->all();

/*
    [
        'PROD-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'PROD-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

<a name="method-keys"></a>
<!-- #### `keys()` -->
#### `keys()`
<!-- The `keys` method returns all of the collection's keys: -->
`keys` メソッドは、コレクションのすべてのキーを返します。

```
$collection = collect([
    'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
    'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$keys = $collection->keys();

$keys->all();

// ['prod-100', 'prod-200']
```

<a name="method-last"></a>
<!-- #### `last()` -->
#### `last()`
<!-- The `last` method returns the last element in the collection that passes a given truth test: -->
`last` メソッドは、指定された真理テストに合格したコレクション内の最後の要素を返します。

```
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

<!-- You may also call the `last` method with no arguments to get the last element in the collection. If the collection is empty, `null` is returned: -->
引数なしで `last` メソッドを呼び出して、コレクション内の最後の要素を取得することもできます。コレクションが空の場合、`null` が返されます。

```
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
<!-- #### `lazy()` -->
#### `lazy()`
<!-- The `lazy` method returns a new [`LazyCollection`](#lazy-collections) instance from the underlying array of items: -->
`lazy` メソッドは、基になる項目の配列から新しい [`LazyCollection`](#lazy-collections) インスタンスを返します。

```
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

<!-- This is especially useful when you need to perform transformations on a huge `Collection` that contains many items: -->
これは、多くの項目を含む巨大な `Collection` に対して変換を実行する必要がある場合に特に便利です。

```
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

<!-- By converting the collection to a `LazyCollection`, we avoid having to allocate a ton of additional memory. Though the original collection still keeps _its_ values in memory, the subsequent filters will not. Therefore, virtually no additional memory will be allocated when filtering the collection's results. -->
コレクションを `LazyCollection` に変換することで、大量の追加メモリを割り当てる必要がなくなります。元のコレクションはメモリ内に _its_ 値を保持しますが、後続のフィルターは保持しません。したがって、コレクションの結果をフィルタリングするときに追加のメモリが割り当てられることは事実上ありません。

<a name="method-macro"></a>
<!-- #### `macro()` -->
#### `macro()`
<!-- The static `macro` method allows you to add methods to the `Collection` class at run time. Refer to the documentation on [extending collections](#extending-collections) for more information. -->
静的 `macro` メソッドを使用すると、実行時に `Collection` クラスにメソッドを追加できます。詳細については、[extending collections](#extending-collections) のドキュメントを参照してください。

<a name="method-make"></a>
<!-- #### `make()` -->
#### `make()`
<!-- The static `make` method creates a new collection instance. See the [Creating Collections](#creating-collections) section. -->
静的 `make` メソッドは、新しいコレクション インスタンスを作成します。 「[Creating Collections](#creating-collections)」セクションを参照してください。

<a name="method-map"></a>
<!-- #### `map()` -->
#### `map()`
<!-- The `map` method iterates through the collection and passes each value to the given callback. The callback is free to modify the item and return it, thus forming a new collection of modified items: -->
`map` メソッドはコレクションを反復処理し、各値を指定されたコールバックに渡します。コールバックは自由に項目を変更して返し、変更された項目の新しいコレクションを形成します。

```
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 他のほとんどのコレクション メソッドと同様に、`map` は新しいコレクション インスタンスを返します。呼び出されるコレクションは変更されません。元のコレクションを変換する場合は、[`transform`](#method-transform) メソッドを使用します。

<a name="method-mapinto"></a>
<!-- #### `mapInto()` -->
#### `mapInto()`
<!-- The `mapInto()` method iterates over the collection, creating a new instance of the given class by passing the value into the constructor: -->
`mapInto()` メソッドはコレクションを反復処理し、値をコンストラクターに渡すことによって、指定されたクラスの新しいインスタンスを作成します。

```
class Currency
{
    /**
     * Create a new currency instance.
     */
    function __construct(
        public string $code,
    ) {}
}

$collection = collect(['USD', 'EUR', 'GBP']);

$currencies = $collection->mapInto(Currency::class);

$currencies->all();

// [Currency('USD'), Currency('EUR'), Currency('GBP')]
```

<a name="method-mapspread"></a>
<!-- #### `mapSpread()` -->
#### `mapSpread()`
<!-- The `mapSpread` method iterates over the collection's items, passing each nested item value into the given closure. The closure is free to modify the item and return it, thus forming a new collection of modified items: -->
`mapSpread` メソッドはコレクションの項目を反復処理し、ネストされた各項目の値を指定されたクロージャに渡します。クロージャは自由に項目を変更して返すことができるため、変更された項目の新しいコレクションが形成されます。

```
$collection = collect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunks = $collection->chunk(2);

$sequence = $chunks->mapSpread(function (int $even, int $odd) {
    return $even + $odd;
});

$sequence->all();

// [1, 5, 9, 13, 17]
```

<a name="method-maptogroups"></a>
<!-- #### `mapToGroups()` -->
#### `mapToGroups()`
<!-- The `mapToGroups` method groups the collection's items by the given closure. The closure should return an associative array containing a single key / value pair, thus forming a new collection of grouped values: -->
`mapToGroups` メソッドは、指定されたクロージャによってコレクションの項目をグループ化します。クロージャは、単一のキーと値のペアを含む連想配列を返し、グループ化された値の新しいコレクションを形成する必要があります。

```
$collection = collect([
    [
        'name' => 'John Doe',
        'department' => 'Sales',
    ],
    [
        'name' => 'Jane Doe',
        'department' => 'Sales',
    ],
    [
        'name' => 'Johnny Doe',
        'department' => 'Marketing',
    ]
]);

$grouped = $collection->mapToGroups(function (array $item, int $key) {
    return [$item['department'] => $item['name']];
});

$grouped->all();

/*
    [
        'Sales' => ['John Doe', 'Jane Doe'],
        'Marketing' => ['Johnny Doe'],
    ]
*/

$grouped->get('Sales')->all();

// ['John Doe', 'Jane Doe']
```

<a name="method-mapwithkeys"></a>
<!-- #### `mapWithKeys()` -->
#### `mapWithKeys()`
<!-- The `mapWithKeys` method iterates through the collection and passes each value to the given callback. The callback should return an associative array containing a single key / value pair: -->
`mapWithKeys` メソッドはコレクションを反復処理し、各値を指定されたコールバックに渡します。コールバックは、単一のキーと値のペアを含む連想配列を返す必要があります。

```
$collection = collect([
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
]);

$keyed = $collection->mapWithKeys(function (array $item, int $key) {
    return [$item['email'] => $item['name']];
});

$keyed->all();

/*
    [
        'john@example.com' => 'John',
        'jane@example.com' => 'Jane',
    ]
*/
```

<a name="method-max"></a>
<!-- #### `max()` -->
#### `max()`
<!-- The `max` method returns the maximum value of a given key: -->
`max` メソッドは、指定されたキーの最大値を返します。

```
$max = collect([
    ['foo' => 10],
    ['foo' => 20]
])->max('foo');

// 20

$max = collect([1, 2, 3, 4, 5])->max();

// 5
```

<a name="method-median"></a>
<!-- #### `median()` -->
#### `median()`
<!-- The `median` method returns the [median value](https://en.wikipedia.org/wiki/Median) of a given key: -->
`median` メソッドは、指定されたキーの [median value](https://en.wikipedia.org/wiki/Median) を返します。

```
$median = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->median('foo');

// 15

$median = collect([1, 1, 2, 4])->median();

// 1.5
```

<a name="method-merge"></a>
<!-- #### `merge()` -->
#### `merge()`
<!-- The `merge` method merges the given array or collection with the original collection. If a string key in the given items matches a string key in the original collection, the given item's value will overwrite the value in the original collection: -->
`merge` メソッドは、指定された配列またはコレクションを元のコレクションとマージします。指定された項目の文字列キーが元のコレクションの文字列キーと一致する場合、指定された項目の値は元のコレクションの値を上書きします。

```
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

<!-- If the given item's keys are numeric, the values will be appended to the end of the collection: -->
指定された項目のキーが数値の場合、値はコレクションの末尾に追加されます。

```
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
<!-- #### `mergeRecursive()` -->
#### `mergeRecursive()`
<!-- The `mergeRecursive` method merges the given array or collection recursively with the original collection. If a string key in the given items matches a string key in the original collection, then the values for these keys are merged together into an array, and this is done recursively: -->
`mergeRecursive` メソッドは、指定された配列またはコレクションを元のコレクションと再帰的にマージします。指定された項目の文字列キーが元のコレクションの文字列キーと一致する場合、これらのキーの値が配列にマージされ、これが再帰的に行われます。

```
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->mergeRecursive([
    'product_id' => 2,
    'price' => 200,
    'discount' => false
]);

$merged->all();

// ['product_id' => [1, 2], 'price' => [100, 200], 'discount' => false]
```

<a name="method-min"></a>
<!-- #### `min()` -->
#### `min()`
<!-- The `min` method returns the minimum value of a given key: -->
`min` メソッドは、指定されたキーの最小値を返します。

```
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
<!-- #### `mode()` -->
#### `mode()`
<!-- The `mode` method returns the [mode value](https://en.wikipedia.org/wiki/Mode_(statistics)) of a given key: -->
`mode` メソッドは、指定されたキーの [mode value](https://en.wikipedia.org/wiki/Mode_(statistics)) を返します。

```
$mode = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->mode('foo');

// [10]

$mode = collect([1, 1, 2, 4])->mode();

// [1]

$mode = collect([1, 1, 2, 2])->mode();

// [1, 2]
```

<a name="method-multiply"></a>
<!-- #### `multiply()` -->
#### `multiply()`
<!-- The `multiply` method creates the specified number of copies of all items in the collection: -->
`multiply` メソッドは、コレクション内のすべての項目の指定された数のコピーを作成します。

```php
$users = collect([
    ['name' => 'User #1', 'email' => 'user1@example.com'],
    ['name' => 'User #2', 'email' => 'user2@example.com'],
])->multiply(3);

/*
    [
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
    ]
*/
```

<a name="method-nth"></a>
<!-- #### `nth()` -->
#### `nth()`
<!-- The `nth` method creates a new collection consisting of every n-th element: -->
`nth` メソッドは、n 番目ごとの要素で構成される新しいコレクションを作成します。

```
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

<!-- You may optionally pass a starting offset as the second argument: -->
オプションで、開始オフセットを 2 番目の引数として渡すこともできます。

```
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
<!-- #### `only()` -->
#### `only()`
<!-- The `only` method returns the items in the collection with the specified keys: -->
`only` メソッドは、指定されたキーを持つコレクション内の項目を返します。

```
$collection = collect([
    'product_id' => 1,
    'name' => 'Desk',
    'price' => 100,
    'discount' => false
]);

$filtered = $collection->only(['product_id', 'name']);

$filtered->all();

// ['product_id' => 1, 'name' => 'Desk']
```

<!-- For the inverse of `only`, see the [except](#method-except) method. -->
`only` の逆については、[except](#method-except) メソッドを参照してください。

> [!NOTE]
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-only) を使用すると、このメソッドの動作が変更されます。

<a name="method-pad"></a>
<!-- #### `pad()` -->
#### `pad()`
<!-- The `pad` method will fill the array with the given value until the array reaches the specified size. This method behaves like the [array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP function. -->
`pad` メソッドは、配列が指定されたサイズに達するまで、指定された値で配列を埋めます。このメソッドは、[array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP 関数と同様に動作します。

<!-- To pad to the left, you should specify a negative size. No padding will take place if the absolute value of the given size is less than or equal to the length of the array: -->
左側をパディングするには、負のサイズを指定する必要があります。指定されたサイズの絶対値が配列の長さ以下の場合、パディングは行われません。

```
$collection = collect(['A', 'B', 'C']);

$filtered = $collection->pad(5, 0);

$filtered->all();

// ['A', 'B', 'C', 0, 0]

$filtered = $collection->pad(-5, 0);

$filtered->all();

// [0, 0, 'A', 'B', 'C']
```

<a name="method-partition"></a>
<!-- #### `partition()` -->
#### `partition()`
<!-- The `partition` method may be combined with PHP array destructuring to separate elements that pass a given truth test from those that do not: -->
`partition` メソッドを PHP 配列の構造化と組み合わせて、特定の真実テストに合格する要素とそうでない要素を分離することができます。

```
$collection = collect([1, 2, 3, 4, 5, 6]);

[$underThree, $equalOrAboveThree] = $collection->partition(function (int $i) {
    return $i < 3;
});

$underThree->all();

// [1, 2]

$equalOrAboveThree->all();

// [3, 4, 5, 6]
```

<a name="method-percentage"></a>
<!-- #### `percentage()` -->
#### `percentage()`
<!-- The `percentage` method may be used to quickly determine the percentage of items in the collection that pass a given truth test: -->
`percentage` メソッドを使用すると、コレクション内の特定の真実テストに合格したアイテムの割合を迅速に判断できます。

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn ($value) => $value === 1);

// 33.33
```

<!-- By default, the percentage will be rounded to two decimal places. However, you may customize this behavior by providing a second argument to the method: -->
デフォルトでは、パーセンテージは小数点第 2 位に四捨五入されます。ただし、メソッドに 2 番目の引数を指定することで、この動作をカスタマイズできます。

```php
$percentage = $collection->percentage(fn ($value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
<!-- #### `pipe()` -->
#### `pipe()`
<!-- The `pipe` method passes the collection to the given closure and returns the result of the executed closure: -->
`pipe` メソッドは、コレクションを指定されたクロージャに渡し、実行されたクロージャの結果を返します。

```
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
<!-- #### `pipeInto()` -->
#### `pipeInto()`
<!-- The `pipeInto` method creates a new instance of the given class and passes the collection into the constructor: -->
`pipeInto` メソッドは、指定されたクラスの新しいインスタンスを作成し、コレクションをコンストラクターに渡します。

```
class ResourceCollection
{
    /**
     * Create a new ResourceCollection instance.
     */
    public function __construct(
        public Collection $collection,
    ) {}
}

$collection = collect([1, 2, 3]);

$resource = $collection->pipeInto(ResourceCollection::class);

$resource->collection->all();

// [1, 2, 3]
```

<a name="method-pipethrough"></a>
<!-- #### `pipeThrough()` -->
#### `pipeThrough()`
<!-- The `pipeThrough` method passes the collection to the given array of closures and returns the result of the executed closures: -->
`pipeThrough` メソッドは、コレクションを指定されたクロージャの配列に渡し、実行されたクロージャの結果を返します。

```
use Illuminate\Support\Collection;

$collection = collect([1, 2, 3]);

$result = $collection->pipeThrough([
    function (Collection $collection) {
        return $collection->merge([4, 5]);
    },
    function (Collection $collection) {
        return $collection->sum();
    },
]);

// 15
```

<a name="method-pluck"></a>
<!-- #### `pluck()` -->
#### `pluck()`
<!-- The `pluck` method retrieves all of the values for a given key: -->
`pluck` メソッドは、指定されたキーのすべての値を取得します。

```
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

<!-- You may also specify how you wish the resulting collection to be keyed: -->
結果のコレクションにどのようにキーを設定するかを指定することもできます。

```
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

<!-- The `pluck` method also supports retrieving nested values using "dot" notation: -->
`pluck` メソッドは、「ドット」表記を使用したネストされた値の取得もサポートしています。

```
$collection = collect([
    [
        'name' => 'Laracon',
        'speakers' => [
            'first_day' => ['Rosa', 'Judith'],
        ],
    ],
    [
        'name' => 'VueConf',
        'speakers' => [
            'first_day' => ['Abigail', 'Joey'],
        ],
    ],
]);

$plucked = $collection->pluck('speakers.first_day');

$plucked->all();

// [['Rosa', 'Judith'], ['Abigail', 'Joey']]
```

<!-- If duplicate keys exist, the last matching element will be inserted into the plucked collection: -->
重複したキーが存在する場合、最後に一致した要素が取り出されたコレクションに挿入されます。

```
$collection = collect([
    ['brand' => 'Tesla',  'color' => 'red'],
    ['brand' => 'Pagani', 'color' => 'white'],
    ['brand' => 'Tesla',  'color' => 'black'],
    ['brand' => 'Pagani', 'color' => 'orange'],
]);

$plucked = $collection->pluck('color', 'brand');

$plucked->all();

// ['Tesla' => 'black', 'Pagani' => 'orange']
```

<a name="method-pop"></a>
<!-- #### `pop()` -->
#### `pop()`
<!-- The `pop` method removes and returns the last item from the collection: -->
`pop` メソッドは、コレクションから最後の項目を削除して返します。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

<!-- You may pass an integer to the `pop` method to remove and return multiple items from the end of a collection: -->
整数を `pop` メソッドに渡して、コレクションの末尾から複数の項目を削除して返すことができます。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
<!-- #### `prepend()` -->
#### `prepend()`
<!-- The `prepend` method adds an item to the beginning of the collection: -->
`prepend` メソッドは、コレクションの先頭に項目を追加します。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

<!-- You may also pass a second argument to specify the key of the prepended item: -->
2 番目の引数を渡して、先頭に追加される項目のキーを指定することもできます。

```
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
<!-- #### `pull()` -->
#### `pull()`
<!-- The `pull` method removes and returns an item from the collection by its key: -->
`pull` メソッドは、キーによってコレクションから項目を削除して返します。

```
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
<!-- #### `push()` -->
#### `push()`
<!-- The `push` method appends an item to the end of the collection: -->
`push` メソッドは、コレクションの末尾に項目を追加します。

```
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<a name="method-put"></a>
<!-- #### `put()` -->
#### `put()`
<!-- The `put` method sets the given key and value in the collection: -->
`put` メソッドは、コレクション内の指定されたキーと値を設定します。

```
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
<!-- #### `random()` -->
#### `random()`
<!-- The `random` method returns a random item from the collection: -->
`random` メソッドは、コレクションからランダムな項目を返します。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (retrieved randomly)
```

<!-- You may pass an integer to `random` to specify how many items you would like to randomly retrieve. A collection of items is always returned when explicitly passing the number of items you wish to receive: -->
整数を `random` に渡して、ランダムに取得する項目の数を指定できます。受け取りたい項目の数を明示的に渡すと、常に項目のコレクションが返されます。

```
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (retrieved randomly)
```

<!-- If the collection instance has fewer items than requested, the `random` method will throw an `InvalidArgumentException`. -->
コレクション インスタンスのアイテムが要求されたアイテムよりも少ない場合、`random` メソッドは `InvalidArgumentException` をスローします。

<!-- The `random` method also accepts a closure, which will receive the current collection instance: -->
`random` メソッドは、現在のコレクション インスタンスを受け取るクロージャも受け入れます。

```
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] - (retrieved randomly)
```

<a name="method-range"></a>
<!-- #### `range()` -->
#### `range()`
<!-- The `range` method returns a collection containing integers between the specified range: -->
`range` メソッドは、指定された範囲内の整数を含むコレクションを返します。

```
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
<!-- #### `reduce()` -->
#### `reduce()`
<!-- The `reduce` method reduces the collection to a single value, passing the result of each iteration into the subsequent iteration: -->
`reduce` メソッドは、コレクションを単一の値に減らし、各反復の結果を後続の反復に渡します。

```
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

<!-- The value for `$carry` on the first iteration is `null`; however, you may specify its initial value by passing a second argument to `reduce`: -->
最初の反復の `$carry` の値は `null` です。ただし、2 番目の引数を `reduce` に渡すことで、その初期値を指定できます。

```
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

<!-- The `reduce` method also passes array keys in associative collections to the given callback: -->
`reduce` メソッドは、連想コレクション内の配列キーも指定されたコールバックに渡します。

```
$collection = collect([
    'usd' => 1400,
    'gbp' => 1200,
    'eur' => 1000,
]);

$ratio = [
    'usd' => 1,
    'gbp' => 1.37,
    'eur' => 1.22,
];

$collection->reduce(function (int $carry, int $value, int $key) use ($ratio) {
    return $carry + ($value * $ratio[$key]);
});

// 4264
```

<a name="method-reduce-spread"></a>
<!-- #### `reduceSpread()` -->
#### `reduceSpread()`
<!-- The `reduceSpread` method reduces the collection to an array of values, passing the results of each iteration into the subsequent iteration. This method is similar to the `reduce` method; however, it can accept multiple initial values: -->
`reduceSpread` メソッドは、コレクションを値の配列に縮小し、各反復の結果を後続の反復に渡します。このメソッドは、`reduce` メソッドに似ています。ただし、複数の初期値を受け入れることができます。

```
[$creditsRemaining, $batch] = Image::where('status', 'unprocessed')
    ->get()
    ->reduceSpread(function (int $creditsRemaining, Collection $batch, Image $image) {
        if ($creditsRemaining >= $image->creditsRequired()) {
            $batch->push($image);

            $creditsRemaining -= $image->creditsRequired();
        }

        return [$creditsRemaining, $batch];
    }, $creditsAvailable, collect());
```

<a name="method-reject"></a>
<!-- #### `reject()` -->
#### `reject()`
<!-- The `reject` method filters the collection using the given closure. The closure should return `true` if the item should be removed from the resulting collection: -->
`reject` メソッドは、指定されたクロージャーを使用してコレクションをフィルターします。結果のコレクションから項目を削除する必要がある場合、クロージャは `true` を返す必要があります。

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

<!-- For the inverse of the `reject` method, see the [`filter`](#method-filter) method. -->
`reject` メソッドの逆については、[`filter`](#method-filter) メソッドを参照してください。

<a name="method-replace"></a>
<!-- #### `replace()` -->
#### `replace()`
<!-- The `replace` method behaves similarly to `merge`; however, in addition to overwriting matching items that have string keys, the `replace` method will also overwrite items in the collection that have matching numeric keys: -->
`replace` メソッドは、`merge` と同様に動作します。ただし、`replace` メソッドは、文字列キーを持つ一致する項目を上書きするだけでなく、一致する数値キーを持つコレクション内の項目も上書きします。

```
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
<!-- #### `replaceRecursive()` -->
#### `replaceRecursive()`
<!-- This method works like `replace`, but it will recur into arrays and apply the same replacement process to the inner values: -->
このメソッドは `replace` と同様に機能しますが、配列内で再帰的に実行され、同じ置換プロセスが内部値に適用されます。

```
$collection = collect([
    'Taylor',
    'Abigail',
    [
        'James',
        'Victoria',
        'Finn'
    ]
]);

$replaced = $collection->replaceRecursive([
    'Charlie',
    2 => [1 => 'King']
]);

$replaced->all();

// ['Charlie', 'Abigail', ['James', 'King', 'Finn']]
```

<a name="method-reverse"></a>
<!-- #### `reverse()` -->
#### `reverse()`
<!-- The `reverse` method reverses the order of the collection's items, preserving the original keys: -->
`reverse` メソッドは、元のキーを保持したまま、コレクションの項目の順序を逆にします。

```
$collection = collect(['a', 'b', 'c', 'd', 'e']);

$reversed = $collection->reverse();

$reversed->all();

/*
    [
        4 => 'e',
        3 => 'd',
        2 => 'c',
        1 => 'b',
        0 => 'a',
    ]
*/
```

<a name="method-search"></a>
<!-- #### `search()` -->
#### `search()`
<!-- The `search` method searches the collection for the given value and returns its key if found. If the item is not found, `false` is returned: -->
`search` メソッドは、コレクション内で指定された値を検索し、見つかった場合はそのキーを返します。項目が見つからない場合は、`false` が返されます。

```
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

<!-- The search is done using a "loose" comparison, meaning a string with an integer value will be considered equal to an integer of the same value. To use "strict" comparison, pass `true` as the second argument to the method: -->
検索は「緩やかな」比較を使用して行われます。つまり、整数値を持つ文字列は同じ値の整数と等しいと見なされます。 「厳密な」比較を使用するには、メソッドの 2 番目の引数として `true` を渡します。

```
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

<!-- Alternatively, you may provide your own closure to search for the first item that passes a given truth test: -->
あるいは、独自のクロージャを提供して、指定された真理テストに合格する最初の項目を検索することもできます。

```
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
<!-- #### `select()` -->
#### `select()`
<!-- The `select` method selects the given keys from the collection, similar to an SQL `SELECT` statement: -->
`select` メソッドは、SQL `SELECT` ステートメントと同様に、コレクションから指定されたキーを選択します。

```php
$users = collect([
    ['name' => 'Taylor Otwell', 'role' => 'Developer', 'status' => 'active'],
    ['name' => 'Victoria Faith', 'role' => 'Researcher', 'status' => 'active'],
]);

$users->select(['name', 'role']);

/*
    [
        ['name' => 'Taylor Otwell', 'role' => 'Developer'],
        ['name' => 'Victoria Faith', 'role' => 'Researcher'],
    ],
*/
```

<a name="method-shift"></a>
<!-- #### `shift()` -->
#### `shift()`
<!-- The `shift` method removes and returns the first item from the collection: -->
`shift` メソッドは、コレクションから最初の項目を削除して返します。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

<!-- You may pass an integer to the `shift` method to remove and return multiple items from the beginning of a collection: -->
整数を `shift` メソッドに渡して、コレクションの先頭から複数の項目を削除して返すことができます。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
<!-- #### `shuffle()` -->
#### `shuffle()`
<!-- The `shuffle` method randomly shuffles the items in the collection: -->
`shuffle` メソッドは、コレクション内の項目をランダムにシャッフルします。

```
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-skip"></a>
<!-- #### `skip()` -->
#### `skip()`
<!-- The `skip` method returns a new collection, with the given number of elements removed from the beginning of the collection: -->
`skip` メソッドは、コレクションの先頭から指定された数の要素が削除された新しいコレクションを返します。

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
<!-- #### `skipUntil()` -->
#### `skipUntil()`
<!-- The `skipUntil` method skips over items from the collection while the given callback returns `false`. Once the callback returns `true` all of the remaining items in the collection will be returned as a new collection: -->
`skipUntil` メソッドはコレクションの項目をスキップし、指定されたコールバックは `false` を返します。コールバックが `true` を返すと、コレクション内の残りのすべての項目が新しいコレクションとして返されます。

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

<!-- You may also pass a simple value to the `skipUntil` method to skip all items until the given value is found: -->
単純な値を `skipUntil` メソッドに渡して、指定された値が見つかるまですべての項目をスキップすることもできます。

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> 指定された値が見つからない場合、またはコールバックが `true` を返さない場合、`skipUntil` メソッドは空のコレクションを返します。

<a name="method-skipwhile"></a>
<!-- #### `skipWhile()` -->
#### `skipWhile()`
<!-- The `skipWhile` method skips over items from the collection while the given callback returns `true`. Once the callback returns `false` all of the remaining items in the collection will be returned as a new collection: -->
`skipWhile` メソッドはコレクションの項目をスキップし、指定されたコールバックは `true` を返します。コールバックが `false` を返すと、コレクション内の残りのすべての項目が新しいコレクションとして返されます。

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> コールバックが `false` を返さない場合、`skipWhile` メソッドは空のコレクションを返します。

<a name="method-slice"></a>
<!-- #### `slice()` -->
#### `slice()`
<!-- The `slice` method returns a slice of the collection starting at the given index: -->
`slice` メソッドは、指定されたインデックスから始まるコレクションのスライスを返します。

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

<!-- If you would like to limit the size of the returned slice, pass the desired size as the second argument to the method: -->
返されるスライスのサイズを制限したい場合は、目的のサイズを 2 番目の引数としてメソッドに渡します。

```
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

<!-- The returned slice will preserve keys by default. If you do not wish to preserve the original keys, you can use the [`values`](#method-values) method to reindex them. -->
返されたスライスはデフォルトでキーを保持します。元のキーを保持したくない場合は、[`values`](#method-values) メソッドを使用してインデックスを再作成できます。

<a name="method-sliding"></a>
<!-- #### `sliding()` -->
#### `sliding()`
<!-- The `sliding` method returns a new collection of chunks representing a "sliding window" view of the items in the collection: -->
`sliding` メソッドは、コレクション内の項目の「スライディング ウィンドウ」ビューを表すチャンクの新しいコレクションを返します。

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

<!-- This is especially useful in conjunction with the [`eachSpread`](#method-eachspread) method: -->
これは、[`eachSpread`](#method-eachspread) メソッドと組み合わせると特に便利です。

```
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

<!-- You may optionally pass a second "step" value, which determines the distance between the first item of every chunk: -->
オプションで、各チャンクの最初の項目間の距離を決定する 2 番目の「ステップ」値を渡すこともできます。

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
<!-- #### `sole()` -->
#### `sole()`
<!-- The `sole` method returns the first element in the collection that passes a given truth test, but only if the truth test matches exactly one element: -->
`sole` メソッドは、指定された真実テストに合格したコレクション内の最初の要素を返します。ただし、真実テストが 1 つの要素と正確に一致する場合に限ります。

```
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

<!-- You may also pass a key / value pair to the `sole` method, which will return the first element in the collection that matches the given pair, but only if it exactly one element matches: -->
キーと値のペアを `sole` メソッドに渡すこともできます。これは、指定されたペアに一致するコレクション内の最初の要素を返しますが、それは 1 つの要素が正確に一致する場合に限られます。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

<!-- Alternatively, you may also call the `sole` method with no argument to get the first element in the collection if there is only one element: -->
あるいは、要素が 1 つしかない場合は、引数なしで `sole` メソッドを呼び出して、コレクション内の最初の要素を取得することもできます。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

<!-- If there are no elements in the collection that should be returned by the `sole` method, an `\Illuminate\Collections\ItemNotFoundException` exception will be thrown. If there is more than one element that should be returned, an `\Illuminate\Collections\MultipleItemsFoundException` will be thrown. -->
`sole` メソッドによって返される必要がある要素がコレクション内にない場合、`\Illuminate\Collections\ItemNotFoundException` 例外がスローされます。返すべき要素が複数ある場合は、`\Illuminate\Collections\MultipleItemsFoundException` がスローされます。

<a name="method-some"></a>
<!-- #### `some()` -->
#### `some()`
<!-- Alias for the [`contains`](#method-contains) method. -->
[`contains`](#method-contains) メソッドのエイリアス。

<a name="method-sort"></a>
<!-- #### `sort()` -->
#### `sort()`
<!-- The `sort` method sorts the collection. The sorted collection keeps the original array keys, so in the following example we will use the [`values`](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sort` メソッドはコレクションを並べ替えます。並べ替えられたコレクションには元の配列キーが保持されるため、次の例では、[`values`](#method-values) メソッドを使用してキーを連続番号のインデックスにリセットします。

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

<!-- If your sorting needs are more advanced, you may pass a callback to `sort` with your own algorithm. Refer to the PHP documentation on [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters), which is what the collection's `sort` method calls utilizes internally. -->
並べ替えのニーズがさらに高度な場合は、独自のアルゴリズムを使用して `sort` にコールバックを渡すことができます。 [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) に関する PHP ドキュメントを参照してください。これは、コレクションの `sort` メソッド呼び出しが内部的に利用するものです。

> [!NOTE]
> ネストされた配列またはオブジェクトのコレクションを並べ替える必要がある場合は、[`sortBy`](#method-sortby) メソッドと [`sortByDesc`](#method-sortbydesc) メソッドを参照してください。

<a name="method-sortby"></a>
<!-- #### `sortBy()` -->
#### `sortBy()`
<!-- The `sortBy` method sorts the collection by the given key. The sorted collection keeps the original array keys, so in the following example we will use the [`values`](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sortBy` メソッドは、指定されたキーでコレクションを並べ替えます。並べ替えられたコレクションには元の配列キーが保持されるため、次の例では、[`values`](#method-values) メソッドを使用してキーを連続番号のインデックスにリセットします。

```
$collection = collect([
    ['name' => 'Desk', 'price' => 200],
    ['name' => 'Chair', 'price' => 100],
    ['name' => 'Bookcase', 'price' => 150],
]);

$sorted = $collection->sortBy('price');

$sorted->values()->all();

/*
    [
        ['name' => 'Chair', 'price' => 100],
        ['name' => 'Bookcase', 'price' => 150],
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

<!-- The `sortBy` method accepts [sort flags](https://www.php.net/manual/en/function.sort.php) as its second argument: -->
`sortBy` メソッドは、2 番目の引数として [sort flags](https://www.php.net/manual/en/function.sort.php) を受け入れます。

```
$collection = collect([
    ['title' => 'Item 1'],
    ['title' => 'Item 12'],
    ['title' => 'Item 3'],
]);

$sorted = $collection->sortBy('title', SORT_NATURAL);

$sorted->values()->all();

/*
    [
        ['title' => 'Item 1'],
        ['title' => 'Item 3'],
        ['title' => 'Item 12'],
    ]
*/
```

<!-- Alternatively, you may pass your own closure to determine how to sort the collection's values: -->
あるいは、独自のクロージャを渡して、コレクションの値を並べ替える方法を決定することもできます。

```
$collection = collect([
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$sorted = $collection->sortBy(function (array $product, int $key) {
    return count($product['colors']);
});

$sorted->values()->all();

/*
    [
        ['name' => 'Chair', 'colors' => ['Black']],
        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
    ]
*/
```

<!-- If you would like to sort your collection by multiple attributes, you may pass an array of sort operations to the `sortBy` method. Each sort operation should be an array consisting of the attribute that you wish to sort by and the direction of the desired sort: -->
複数の属性でコレクションを並べ替える場合は、並べ替え操作の配列を `sortBy` メソッドに渡すことができます。各ソート操作は、ソートの基準となる属性と目的のソートの方向で構成される配列である必要があります。

```
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    ['name', 'asc'],
    ['age', 'desc'],
]);

$sorted->values()->all();

/*
    [
        ['name' => 'Abigail Otwell', 'age' => 32],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Taylor Otwell', 'age' => 34],
    ]
*/
```

<!-- When sorting a collection by multiple attributes, you may also provide closures that define each sort operation: -->
複数の属性でコレクションを並べ替える場合、各並べ替え操作を定義するクロージャを提供することもできます。

```
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    fn (array $a, array $b) => $a['name'] <=> $b['name'],
    fn (array $a, array $b) => $b['age'] <=> $a['age'],
]);

$sorted->values()->all();

/*
    [
        ['name' => 'Abigail Otwell', 'age' => 32],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Taylor Otwell', 'age' => 34],
    ]
*/
```

<a name="method-sortbydesc"></a>
<!-- #### `sortByDesc()` -->
#### `sortByDesc()`
<!-- This method has the same signature as the [`sortBy`](#method-sortby) method, but will sort the collection in the opposite order. -->
このメソッドは、[`sortBy`](#method-sortby) メソッドと同じシグネチャを持ちますが、コレクションを逆の順序で並べ替えます。

<a name="method-sortdesc"></a>
<!-- #### `sortDesc()` -->
#### `sortDesc()`
<!-- This method will sort the collection in the opposite order as the [`sort`](#method-sort) method: -->
このメソッドは、[`sort`](#method-sort) メソッドとは逆の順序でコレクションを並べ替えます。

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

<!-- Unlike `sort`, you may not pass a closure to `sortDesc`. Instead, you should use the [`sort`](#method-sort) method and invert your comparison. -->
`sort` とは異なり、クロージャを `sortDesc` に渡すことはできません。代わりに、[`sort`](#method-sort) メソッドを使用して、比較を反転する必要があります。

<a name="method-sortkeys"></a>
<!-- #### `sortKeys()` -->
#### `sortKeys()`
<!-- The `sortKeys` method sorts the collection by the keys of the underlying associative array: -->
`sortKeys` メソッドは、基になる連想配列のキーによってコレクションを並べ替えます。

```
$collection = collect([
    'id' => 22345,
    'first' => 'John',
    'last' => 'Doe',
]);

$sorted = $collection->sortKeys();

$sorted->all();

/*
    [
        'first' => 'John',
        'id' => 22345,
        'last' => 'Doe',
    ]
*/
```

<a name="method-sortkeysdesc"></a>
<!-- #### `sortKeysDesc()` -->
#### `sortKeysDesc()`
<!-- This method has the same signature as the [`sortKeys`](#method-sortkeys) method, but will sort the collection in the opposite order. -->
このメソッドは、[`sortKeys`](#method-sortkeys) メソッドと同じシグネチャを持ちますが、コレクションを逆の順序で並べ替えます。

<a name="method-sortkeysusing"></a>
<!-- #### `sortKeysUsing()` -->
#### `sortKeysUsing()`
<!-- The `sortKeysUsing` method sorts the collection by the keys of the underlying associative array using a callback: -->
`sortKeysUsing` メソッドは、コールバックを使用して、基になる連想配列のキーによってコレクションを並べ替えます。

```
$collection = collect([
    'ID' => 22345,
    'first' => 'John',
    'last' => 'Doe',
]);

$sorted = $collection->sortKeysUsing('strnatcasecmp');

$sorted->all();

/*
    [
        'first' => 'John',
        'ID' => 22345,
        'last' => 'Doe',
    ]
*/
```

<!-- The callback must be a comparison function that returns an integer less than, equal to, or greater than zero. For more information, refer to the PHP documentation on [`uksort`](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters), which is the PHP function that `sortKeysUsing` method utilizes internally. -->
コールバックは、ゼロ以下、ゼロ以上の整数を返す比較関数である必要があります。詳細については、`sortKeysUsing` メソッドが内部で使用する PHP 関数である [`uksort`](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters) に関する PHP ドキュメントを参照してください。

<a name="method-splice"></a>
<!-- #### `splice()` -->
#### `splice()`
<!-- The `splice` method removes and returns a slice of items starting at the specified index: -->
`splice` メソッドは、指定されたインデックスから始まる項目のスライスを削除して返します。

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

<!-- You may pass a second argument to limit the size of the resulting collection: -->
2 番目の引数を渡して、結果として得られるコレクションのサイズを制限できます。

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

<!-- In addition, you may pass a third argument containing the new items to replace the items removed from the collection: -->
さらに、コレクションから削除された項目を置き換える新しい項目を含む 3 番目の引数を渡すこともできます。

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1, [10, 11]);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 10, 11, 4, 5]
```

<a name="method-split"></a>
<!-- #### `split()` -->
#### `split()`
<!-- The `split` method breaks a collection into the given number of groups: -->
`split` メソッドは、コレクションを指定された数のグループに分割します。

```
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
<!-- #### `splitIn()` -->
#### `splitIn()`
<!-- The `splitIn` method breaks a collection into the given number of groups, filling non-terminal groups completely before allocating the remainder to the final group: -->
`splitIn` メソッドは、コレクションを指定された数のグループに分割し、非終端グループを完全に埋めてから、残りを最後のグループに割り当てます。

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
<!-- #### `sum()` -->
#### `sum()`
<!-- The `sum` method returns the sum of all items in the collection: -->
`sum` メソッドは、コレクション内のすべての項目の合計を返します。

```
collect([1, 2, 3, 4, 5])->sum();

// 15
```

<!-- If the collection contains nested arrays or objects, you should pass a key that will be used to determine which values to sum: -->
コレクションにネストされた配列またはオブジェクトが含まれている場合は、合計する値を決定するために使用されるキーを渡す必要があります。

```
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

<!-- In addition, you may pass your own closure to determine which values of the collection to sum: -->
さらに、独自のクロージャを渡して、コレクションのどの値を合計するかを決定することもできます。

```
$collection = collect([
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$collection->sum(function (array $product) {
    return count($product['colors']);
});

// 6
```

<a name="method-take"></a>
<!-- #### `take()` -->
#### `take()`
<!-- The `take` method returns a new collection with the specified number of items: -->
`take` メソッドは、指定された数の項目を含む新しいコレクションを返します。

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

<!-- You may also pass a negative integer to take the specified number of items from the end of the collection: -->
負の整数を渡して、コレクションの最後から指定した数の項目を取得することもできます。

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
<!-- #### `takeUntil()` -->
#### `takeUntil()`
<!-- The `takeUntil` method returns items in the collection until the given callback returns `true`: -->
`takeUntil` メソッドは、指定されたコールバックが `true` を返すまで、コレクション内の項目を返します。

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

<!-- You may also pass a simple value to the `takeUntil` method to get the items until the given value is found: -->
単純な値を `takeUntil` メソッドに渡して、指定された値が見つかるまで項目を取得することもできます。

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> 指定された値が見つからない場合、またはコールバックが `true` を返さない場合、`takeUntil` メソッドはコレクション内のすべての項目を返します。

<a name="method-takewhile"></a>
<!-- #### `takeWhile()` -->
#### `takeWhile()`
<!-- The `takeWhile` method returns items in the collection until the given callback returns `false`: -->
`takeWhile` メソッドは、指定されたコールバックが `false` を返すまで、コレクション内の項目を返します。

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]
> コールバックが `false` を返さない場合、`takeWhile` メソッドはコレクション内のすべての項目を返します。

<a name="method-tap"></a>
<!-- #### `tap()` -->
#### `tap()`
<!-- The `tap` method passes the collection to the given callback, allowing you to "tap" into the collection at a specific point and do something with the items while not affecting the collection itself. The collection is then returned by the `tap` method: -->
`tap` メソッドは、コレクションを指定されたコールバックに渡します。これにより、コレクション自体には影響を与えずに、特定の時点でコレクションに「タップ」し、項目に対して何らかの処理を行うことができます。その後、コレクションは `tap` メソッドによって返されます。

```
collect([2, 4, 3, 1, 5])
    ->sort()
    ->tap(function (Collection $collection) {
        Log::debug('Values after sorting', $collection->values()->all());
    })
    ->shift();

// 1
```

<a name="method-times"></a>
<!-- #### `times()` -->
#### `times()`
<!-- The static `times` method creates a new collection by invoking the given closure a specified number of times: -->
静的 `times` メソッドは、指定されたクロージャを指定された回数呼び出すことによって新しいコレクションを作成します。

```
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
<!-- #### `toArray()` -->
#### `toArray()`
<!-- The `toArray` method converts the collection into a plain PHP `array`. If the collection's values are [Eloquent](/docs/11.x/eloquent) models, the models will also be converted to arrays: -->
`toArray` メソッドは、コレクションをプレーンな PHP `array` に変換します。コレクションの値が [Eloquent](/docs/11.x/eloquent) モデルの場合、モデルも配列に変換されます。

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toArray();

/*
    [
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

> [!WARNING]
> `toArray` は、`Arrayable` のインスタンスであるコレクションのネストされたオブジェクトもすべて配列に変換します。コレクションの基礎となる生の配列を取得したい場合は、代わりに [`all`](#method-all) メソッドを使用してください。

<a name="method-tojson"></a>
<!-- #### `toJson()` -->
#### `toJson()`
<!-- The `toJson` method converts the collection into a JSON serialized string: -->
`toJson` メソッドは、コレクションを JSON シリアル化文字列に変換します。

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
<!-- #### `transform()` -->
#### `transform()`
<!-- The `transform` method iterates over the collection and calls the given callback with each item in the collection. The items in the collection will be replaced by the values returned by the callback: -->
`transform` メソッドはコレクションを反復処理し、コレクション内の各項目で指定されたコールバックを呼び出します。コレクション内の項目は、コールバックによって返された値に置き換えられます。

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 他のほとんどのコレクション メソッドとは異なり、`transform` はコレクション自体を変更します。代わりに新しいコレクションを作成する場合は、[`map`](#method-map) メソッドを使用します。

<a name="method-undot"></a>
<!-- #### `undot()` -->
#### `undot()`
<!-- The `undot` method expands a single-dimensional collection that uses "dot" notation into a multi-dimensional collection: -->
`undot` メソッドは、「ドット」表記を使用する単一次元のコレクションを多次元のコレクションに拡張します。

```
$person = collect([
    'name.first_name' => 'Marie',
    'name.last_name' => 'Valentine',
    'address.line_1' => '2992 Eagle Drive',
    'address.line_2' => '',
    'address.suburb' => 'Detroit',
    'address.state' => 'MI',
    'address.postcode' => '48219'
]);

$person = $person->undot();

$person->toArray();

/*
    [
        "name" => [
            "first_name" => "Marie",
            "last_name" => "Valentine",
        ],
        "address" => [
            "line_1" => "2992 Eagle Drive",
            "line_2" => "",
            "suburb" => "Detroit",
            "state" => "MI",
            "postcode" => "48219",
        ],
    ]
*/
```

<a name="method-union"></a>
<!-- #### `union()` -->
#### `union()`
<!-- The `union` method adds the given array to the collection. If the given array contains keys that are already in the original collection, the original collection's values will be preferred: -->
`union` メソッドは、指定された配列をコレクションに追加します。指定された配列に元のコレクションに既に存在するキーが含まれている場合は、元のコレクションの値が優先されます。

```
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
<!-- #### `unique()` -->
#### `unique()`
<!-- The `unique` method returns all of the unique items in the collection. The returned collection keeps the original array keys, so in the following example we will use the [`values`](#method-values) method to reset the keys to consecutively numbered indexes: -->
`unique` メソッドは、コレクション内のすべての一意の項目を返します。返されたコレクションには元の配列キーが保持されているため、次の例では、[`values`](#method-values) メソッドを使用してキーを連続番号のインデックスにリセットします。

```
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

<!-- When dealing with nested arrays or objects, you may specify the key used to determine uniqueness: -->
ネストされた配列またはオブジェクトを扱う場合、一意性を決定するために使用されるキーを指定できます。

```
$collection = collect([
    ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
    ['name' => 'iPhone 5', 'brand' => 'Apple', 'type' => 'phone'],
    ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
    ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
    ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
]);

$unique = $collection->unique('brand');

$unique->values()->all();

/*
    [
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
    ]
*/
```

<!-- Finally, you may also pass your own closure to the `unique` method to specify which value should determine an item's uniqueness: -->
最後に、独自のクロージャを `unique` メソッドに渡して、項目の一意性を決定する値を指定することもできます。

```
$unique = $collection->unique(function (array $item) {
    return $item['brand'].$item['type'];
});

$unique->values()->all();

/*
    [
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
        ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
    ]
*/
```

<!-- The `unique` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [`uniqueStrict`](#method-uniquestrict) method to filter using "strict" comparisons. -->
`unique` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`uniqueStrict`](#method-uniquestrict) メソッドを使用します。

> [!NOTE]
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-unique) を使用すると、このメソッドの動作が変更されます。

<a name="method-uniquestrict"></a>
<!-- #### `uniqueStrict()` -->
#### `uniqueStrict()`
<!-- This method has the same signature as the [`unique`](#method-unique) method; however, all values are compared using "strict" comparisons. -->
このメソッドには、[`unique`](#method-unique) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-unless"></a>
<!-- #### `unless()` -->
#### `unless()`
<!-- The `unless` method will execute the given callback unless the first argument given to the method evaluates to `true`: -->
`unless` メソッドは、メソッドに指定された最初の引数が `true` と評価されない限り、指定されたコールバックを実行します。

```
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection) {
    return $collection->push(4);
});

$collection->unless(false, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- A second callback may be passed to the `unless` method. The second callback will be executed when the first argument given to the `unless` method evaluates to `true`: -->
2 番目のコールバックを `unless` メソッドに渡すことができます。 2 番目のコールバックは、`unless` メソッドに指定された最初の引数が `true` と評価されたときに実行されます。

```
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- For the inverse of `unless`, see the [`when`](#method-when) method. -->
`unless` の逆については、[`when`](#method-when) メソッドを参照してください。

<a name="method-unlessempty"></a>
<!-- #### `unlessEmpty()` -->
#### `unlessEmpty()`
<!-- Alias for the [`whenNotEmpty`](#method-whennotempty) method. -->
[`whenNotEmpty`](#method-whennotempty) メソッドのエイリアス。

<a name="method-unlessnotempty"></a>
<!-- #### `unlessNotEmpty()` -->
#### `unlessNotEmpty()`
<!-- Alias for the [`whenEmpty`](#method-whenempty) method. -->
[`whenEmpty`](#method-whenempty) メソッドのエイリアス。

<a name="method-unwrap"></a>
<!-- #### `unwrap()` -->
#### `unwrap()`
<!-- The static `unwrap` method returns the collection's underlying items from the given value when applicable: -->
静的 `unwrap` メソッドは、該当する場合、指定された値からコレクションの基礎となる項目を返します。

```
Collection::unwrap(collect('John Doe'));

// ['John Doe']

Collection::unwrap(['John Doe']);

// ['John Doe']

Collection::unwrap('John Doe');

// 'John Doe'
```

<a name="method-value"></a>
<!-- #### `value()` -->
#### `value()`
<!-- The `value` method retrieves a given value from the first element of the collection: -->
`value` メソッドは、コレクションの最初の要素から指定された値を取得します。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Speaker', 'price' => 400],
]);

$value = $collection->value('price');

// 200
```

<a name="method-values"></a>
<!-- #### `values()` -->
#### `values()`
<!-- The `values` method returns a new collection with the keys reset to consecutive integers: -->
`values` メソッドは、キーが連続した整数にリセットされた新しいコレクションを返します。

```
$collection = collect([
    10 => ['product' => 'Desk', 'price' => 200],
    11 => ['product' => 'Desk', 'price' => 200],
]);

$values = $collection->values();

$values->all();

/*
    [
        0 => ['product' => 'Desk', 'price' => 200],
        1 => ['product' => 'Desk', 'price' => 200],
    ]
*/
```

<a name="method-when"></a>
<!-- #### `when()` -->
#### `when()`
<!-- The `when` method will execute the given callback when the first argument given to the method evaluates to `true`. The collection instance and the first argument given to the `when` method will be provided to the closure: -->
`when` メソッドは、メソッドに指定された最初の引数が `true` と評価されると、指定されたコールバックを実行します。コレクション インスタンスと `when` メソッドに指定された最初の引数がクロージャに提供されます。

```
$collection = collect([1, 2, 3]);

$collection->when(true, function (Collection $collection, int $value) {
    return $collection->push(4);
});

$collection->when(false, function (Collection $collection, int $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 4]
```

<!-- A second callback may be passed to the `when` method. The second callback will be executed when the first argument given to the `when` method evaluates to `false`: -->
2 番目のコールバックを `when` メソッドに渡すことができます。 2 番目のコールバックは、`when` メソッドに指定された最初の引数が `false` と評価されたときに実行されます。

```
$collection = collect([1, 2, 3]);

$collection->when(false, function (Collection $collection, int $value) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- For the inverse of `when`, see the [`unless`](#method-unless) method. -->
`when` の逆については、[`unless`](#method-unless) メソッドを参照してください。

<a name="method-whenempty"></a>
<!-- #### `whenEmpty()` -->
#### `whenEmpty()`
<!-- The `whenEmpty` method will execute the given callback when the collection is empty: -->
`whenEmpty` メソッドは、コレクションが空のときに指定されたコールバックを実行します。

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom']


$collection = collect();

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Adam']
```

<!-- A second closure may be passed to the `whenEmpty` method that will be executed when the collection is not empty: -->
2 番目のクロージャは、コレクションが空でない場合に実行される `whenEmpty` メソッドに渡すことができます。

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Michael', 'Tom', 'Taylor']
```

<!-- For the inverse of `whenEmpty`, see the [`whenNotEmpty`](#method-whennotempty) method. -->
`whenEmpty` の逆については、[`whenNotEmpty`](#method-whennotempty) メソッドを参照してください。

<a name="method-whennotempty"></a>
<!-- #### `whenNotEmpty()` -->
#### `whenNotEmpty()`
<!-- The `whenNotEmpty` method will execute the given callback when the collection is not empty: -->
`whenNotEmpty` メソッドは、コレクションが空でない場合に指定されたコールバックを実行します。

```
$collection = collect(['michael', 'tom']);

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
});

$collection->all();

// ['michael', 'tom', 'adam']


$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
});

$collection->all();

// []
```

<!-- A second closure may be passed to the `whenNotEmpty` method that will be executed when the collection is empty: -->
2 番目のクロージャは、コレクションが空のときに実行される `whenNotEmpty` メソッドに渡すことができます。

```
$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
}, function (Collection $collection) {
    return $collection->push('taylor');
});

$collection->all();

// ['taylor']
```

<!-- For the inverse of `whenNotEmpty`, see the [`whenEmpty`](#method-whenempty) method. -->
`whenNotEmpty` の逆については、[`whenEmpty`](#method-whenempty) メソッドを参照してください。

<a name="method-where"></a>
<!-- #### `where()` -->
#### `where()`
<!-- The `where` method filters the collection by a given key / value pair: -->
`where` メソッドは、指定されたキーと値のペアによってコレクションをフィルターします。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->where('price', 100);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

<!-- The `where` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [`whereStrict`](#method-wherestrict) method to filter using "strict" comparisons. -->
`where` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`whereStrict`](#method-wherestrict) メソッドを使用します。

<!-- Optionally, you may pass a comparison operator as the second parameter. Supported operators are: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', and '<=': -->
オプションで、比較演算子を 2 番目のパラメータとして渡すこともできます。サポートされている演算子は、「===」、「!==」、「!=」、「==」、「=」、「<>」、「>」、「<」、「>=」、および「<=」です。

```
$collection = collect([
    ['name' => 'Jim', 'deleted_at' => '2019-01-01 00:00:00'],
    ['name' => 'Sally', 'deleted_at' => '2019-01-02 00:00:00'],
    ['name' => 'Sue', 'deleted_at' => null],
]);

$filtered = $collection->where('deleted_at', '!=', null);

$filtered->all();

/*
    [
        ['name' => 'Jim', 'deleted_at' => '2019-01-01 00:00:00'],
        ['name' => 'Sally', 'deleted_at' => '2019-01-02 00:00:00'],
    ]
*/
```

<a name="method-wherestrict"></a>
<!-- #### `whereStrict()` -->
#### `whereStrict()`
<!-- This method has the same signature as the [`where`](#method-where) method; however, all values are compared using "strict" comparisons. -->
このメソッドには、[`where`](#method-where) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-wherebetween"></a>
<!-- #### `whereBetween()` -->
#### `whereBetween()`
<!-- The `whereBetween` method filters the collection by determining if a specified item value is within a given range: -->
`whereBetween` メソッドは、指定された項目値が指定された範囲内にあるかどうかを判断して、コレクションをフィルターします。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 80],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Pencil', 'price' => 30],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereBetween('price', [100, 200]);

$filtered->all();

/*
    [
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

<a name="method-wherein"></a>
<!-- #### `whereIn()` -->
#### `whereIn()`
<!-- The `whereIn` method removes elements from the collection that do not have a specified item value that is contained within the given array: -->
`whereIn` メソッドは、指定された配列内に含まれる指定された項目値を持たない要素をコレクションから削除します。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereIn('price', [150, 200]);

$filtered->all();

/*
    [
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Bookcase', 'price' => 150],
    ]
*/
```

<!-- The `whereIn` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [`whereInStrict`](#method-whereinstrict) method to filter using "strict" comparisons. -->
`whereIn` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`whereInStrict`](#method-whereinstrict) メソッドを使用します。

<a name="method-whereinstrict"></a>
<!-- #### `whereInStrict()` -->
#### `whereInStrict()`
<!-- This method has the same signature as the [`whereIn`](#method-wherein) method; however, all values are compared using "strict" comparisons. -->
このメソッドには、[`whereIn`](#method-wherein) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-whereinstanceof"></a>
<!-- #### `whereInstanceOf()` -->
#### `whereInstanceOf()`
<!-- The `whereInstanceOf` method filters the collection by a given class type: -->
`whereInstanceOf` メソッドは、指定されたクラス タイプでコレクションをフィルターします。

```
use App\Models\User;
use App\Models\Post;

$collection = collect([
    new User,
    new User,
    new Post,
]);

$filtered = $collection->whereInstanceOf(User::class);

$filtered->all();

// [App\Models\User, App\Models\User]
```

<a name="method-wherenotbetween"></a>
<!-- #### `whereNotBetween()` -->
#### `whereNotBetween()`
<!-- The `whereNotBetween` method filters the collection by determining if a specified item value is outside of a given range: -->
`whereNotBetween` メソッドは、指定された項目の値が指定された範囲外であるかどうかを判断して、コレクションをフィルターします。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 80],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Pencil', 'price' => 30],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereNotBetween('price', [100, 200]);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 80],
        ['product' => 'Pencil', 'price' => 30],
    ]
*/
```

<a name="method-wherenotin"></a>
<!-- #### `whereNotIn()` -->
#### `whereNotIn()`
<!-- The `whereNotIn` method removes elements from the collection that have a specified item value that is contained within the given array: -->
`whereNotIn` メソッドは、指定された配列内に含まれる指定された項目値を持つ要素をコレクションから削除します。

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereNotIn('price', [150, 200]);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

<!-- The `whereNotIn` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [`whereNotInStrict`](#method-wherenotinstrict) method to filter using "strict" comparisons. -->
`whereNotIn` メソッドは、項目値をチェックするときに「緩やかな」比較を使用します。つまり、整数値を持つ文字列は、同じ値の整数と等しいと見なされます。 「厳密な」比較を使用してフィルタリングするには、[`whereNotInStrict`](#method-wherenotinstrict) メソッドを使用します。

<a name="method-wherenotinstrict"></a>
<!-- #### `whereNotInStrict()` -->
#### `whereNotInStrict()`
<!-- This method has the same signature as the [`whereNotIn`](#method-wherenotin) method; however, all values are compared using "strict" comparisons. -->
このメソッドには、[`whereNotIn`](#method-wherenotin) メソッドと同じシグネチャがあります。ただし、すべての値は「厳密な」比較を使用して比較されます。

<a name="method-wherenotnull"></a>
<!-- #### `whereNotNull()` -->
#### `whereNotNull()`
<!-- The `whereNotNull` method returns items from the collection where the given key is not `null`: -->
`whereNotNull` メソッドは、指定されたキーが `null` ではないコレクションから項目を返します。

```
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
]);

$filtered = $collection->whereNotNull('name');

$filtered->all();

/*
    [
        ['name' => 'Desk'],
        ['name' => 'Bookcase'],
    ]
*/
```

<a name="method-wherenull"></a>
<!-- #### `whereNull()` -->
#### `whereNull()`
<!-- The `whereNull` method returns items from the collection where the given key is `null`: -->
`whereNull` メソッドは、指定されたキーが `null` であるコレクションから項目を返します。

```
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
]);

$filtered = $collection->whereNull('name');

$filtered->all();

/*
    [
        ['name' => null],
    ]
*/
```

<a name="method-wrap"></a>
<!-- #### `wrap()` -->
#### `wrap()`
<!-- The static `wrap` method wraps the given value in a collection when applicable: -->
静的 `wrap` メソッドは、該当する場合、指定された値をコレクションにラップします。

```
use Illuminate\Support\Collection;

$collection = Collection::wrap('John Doe');

$collection->all();

// ['John Doe']

$collection = Collection::wrap(['John Doe']);

$collection->all();

// ['John Doe']

$collection = Collection::wrap(collect('John Doe'));

$collection->all();

// ['John Doe']
```

<a name="method-zip"></a>
<!-- #### `zip()` -->
#### `zip()`
<!-- The `zip` method merges together the values of the given array with the values of the original collection at their corresponding index: -->
`zip` メソッドは、指定された配列の値と、対応するインデックスの元のコレクションの値をマージします。

```
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
<!-- ## Higher Order Messages -->
## Higher Order Messages

<!-- Collections also provide support for "higher order messages", which are short-cuts for performing common actions on collections. The collection methods that provide higher order messages are: [`average`](#method-average), [`avg`](#method-avg), [`contains`](#method-contains), [`each`](#method-each), [`every`](#method-every), [`filter`](#method-filter), [`first`](#method-first), [`flatMap`](#method-flatmap), [`groupBy`](#method-groupby), [`keyBy`](#method-keyby), [`map`](#method-map), [`max`](#method-max), [`min`](#method-min), [`partition`](#method-partition), [`reject`](#method-reject), [`skipUntil`](#method-skipuntil), [`skipWhile`](#method-skipwhile), [`some`](#method-some), [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc), [`sum`](#method-sum), [`takeUntil`](#method-takeuntil), [`takeWhile`](#method-takewhile), and [`unique`](#method-unique). -->
コレクションは、コレクションに対して一般的なアクションを実行するためのショートカットである「高次メッセージ」のサポートも提供します。高次メッセージを提供する収集メソッドは、[`average`](#method-average)、[`avg`](#method-avg)、[`contains`](#method-contains)、[`each`](#method-each)、[`every`](#method-every)、[`filter`](#method-filter)、[`first`](#method-first)、[`flatMap`](#method-flatmap)、[`groupBy`](#method-groupby)、[`keyBy`](#method-keyby)、[`map`](#method-map)、 [`max`](#method-max)、[`min`](#method-min)、[`partition`](#method-partition)、[`reject`](#method-reject)、[`skipUntil`](#method-skipuntil)、[`skipWhile`](#method-skipwhile)、[`some`](#method-some)、[`sortBy`](#method-sortby)、[`sortByDesc`](#method-sortbydesc)、[`sum`](#method-sum)、[`takeUntil`](#method-takeuntil)、 [`takeWhile`](#method-takewhile)、および[`unique`](#method-unique)。

<!-- Each higher order message can be accessed as a dynamic property on a collection instance. For instance, let's use the `each` higher order message to call a method on each object within a collection: -->
各高次メッセージには、コレクション インスタンスの動的プロパティとしてアクセスできます。たとえば、`each` 上位メッセージを使用して、コレクション内の各オブジェクトのメソッドを呼び出してみましょう。

```
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

<!-- Likewise, we can use the `sum` higher order message to gather the total number of "votes" for a collection of users: -->
同様に、`sum` 上位メッセージを使用して、ユーザーのコレクションの「投票」の合計数を収集できます。

```
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
<!-- ## Lazy Collections -->
## Lazy Collections

<a name="lazy-collection-introduction"></a>
<!-- ### Introduction -->
### Introduction

> [!WARNING]
> Laravel の遅延コレクションについて詳しく学ぶ前に、時間をかけて [PHP generators](https://www.php.net/manual/en/language.generators.overview.php) についてよく理解してください。

<!-- To supplement the already powerful `Collection` class, the `LazyCollection` class leverages PHP's [generators](https://www.php.net/manual/en/language.generators.overview.php) to allow you to work with very large datasets while keeping memory usage low. -->
すでに強力な `Collection` クラスを補足するために、`LazyCollection` クラスは PHP の [generators](https://www.php.net/manual/en/language.generators.overview.php) を利用して、メモリ使用量を低く抑えながら非常に大規模なデータセットを操作できるようにします。

<!-- For example, imagine your application needs to process a multi-gigabyte log file while taking advantage of Laravel's collection methods to parse the logs. Instead of reading the entire file into memory at once, lazy collections may be used to keep only a small part of the file in memory at a given time: -->
たとえば、アプリケーションがログを解析するために Laravel の収集メソッドを利用しながら、数ギガバイトのログ ファイルを処理する必要があると想像してください。ファイル全体を一度にメモリに読み取る代わりに、遅延コレクションを使用して、特定の時点でファイルのごく一部のみをメモリに保持することができます。

```
use App\Models\LogEntry;
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }
})->chunk(4)->map(function (array $lines) {
    return LogEntry::fromLines($lines);
})->each(function (LogEntry $logEntry) {
    // Process the log entry...
});
```

<!-- Or, imagine you need to iterate through 10,000 Eloquent models. When using traditional Laravel collections, all 10,000 Eloquent models must be loaded into memory at the same time: -->
あるいは、10,000 の Eloquent モデルを反復処理する必要があると想像してください。従来の Laravel コレクションを使用する場合、10,000 個の Eloquent モデルすべてを同時にメモリにロードする必要があります。

```
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

<!-- However, the query builder's `cursor` method returns a `LazyCollection` instance. This allows you to still only run a single query against the database but also only keep one Eloquent model loaded in memory at a time. In this example, the `filter` callback is not executed until we actually iterate over each user individually, allowing for a drastic reduction in memory usage: -->
ただし、クエリビルダの `cursor` メソッドは、`LazyCollection` インスタンスを返します。これにより、データベースに対して 1 つのクエリのみを実行できますが、同時にメモリにロードされた Eloquent モデルは 1 つだけになります。この例では、`filter` コールバックは、実際に各ユーザーを個別に反復処理するまで実行されず、メモリ使用量を大幅に削減できます。

```
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

<a name="creating-lazy-collections"></a>
<!-- ### Creating Lazy Collections -->
### Creating Lazy Collections

<!-- To create a lazy collection instance, you should pass a PHP generator function to the collection's `make` method: -->
遅延コレクション インスタンスを作成するには、PHP ジェネレーター関数をコレクションの `make` メソッドに渡す必要があります。

```
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }
});
```

<a name="the-enumerable-contract"></a>
<!-- ### The Enumerable Contract -->
### The Enumerable Contract

<!-- Almost all methods available on the `Collection` class are also available on the `LazyCollection` class. Both of these classes implement the `Illuminate\Support\Enumerable` contract, which defines the following methods: -->
`Collection` クラスで使用できるほぼすべてのメソッドは、`LazyCollection` クラスでも使用できます。これらのクラスは両方とも、次のメソッドを定義する `Illuminate\Support\Enumerable` コントラクトを実装します。

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffKeys](#method-diffkeys)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectAssoc](#method-intersectAssoc)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[pipe](#method-pipe)
[pluck](#method-pluck)
[random](#method-random)
[reduce](#method-reduce)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[shuffle](#method-shuffle)
[skip](#method-skip)
[slice](#method-slice)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[split](#method-split)
[sum](#method-sum)
[take](#method-take)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[wrap](#method-wrap)
[zip](#method-zip)
-->
[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffKeys](#method-diffkeys)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectAssoc](#method-intersectAssoc)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[pipe](#method-pipe)
[pluck](#method-pluck)
[random](#method-random)
[reduce](#method-reduce)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[shuffle](#method-shuffle)
[skip](#method-skip)
[slice](#method-slice)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[split](#method-split)
[sum](#method-sum)
[take](#method-take)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[wrap](#method-wrap)
[zip](#method-zip)

<!-- </div> -->
</div>

> [!WARNING]
> コレクションを変更するメソッド (`shift`、`pop`、`prepend` など) は、`LazyCollection` クラスでは**使用できません**。

<a name="lazy-collection-methods"></a>
<!-- ### Lazy Collection Methods -->
### Lazy Collection Methods

<!-- In addition to the methods defined in the `Enumerable` contract, the `LazyCollection` class contains the following methods: -->
`Enumerable` コントラクトで定義されたメソッドに加えて、`LazyCollection` クラスには次のメソッドが含まれています。

<a name="method-takeUntilTimeout"></a>
<!-- #### `takeUntilTimeout()` -->
#### `takeUntilTimeout()`
<!-- The `takeUntilTimeout` method returns a new lazy collection that will enumerate values until the specified time. After that time, the collection will then stop enumerating: -->
`takeUntilTimeout` メソッドは、指定された時間まで値を列挙する新しい遅延コレクションを返します。その後、コレクションは列挙を停止します。

```
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->addMinute());

$lazyCollection->each(function (int $number) {
    dump($number);

    sleep(1);
});

// 1
// 2
// ...
// 58
// 59
```

<!-- To illustrate the usage of this method, imagine an application that submits invoices from the database using a cursor. You could define a [scheduled task](/docs/11.x/scheduling) that runs every 15 minutes and only processes invoices for a maximum of 14 minutes: -->
このメソッドの使用法を説明するために、カーソルを使用してデータベースから請求書を送信するアプリケーションを想像してください。 15 分ごとに実行し、最大 14 分間請求書のみを処理する [scheduled task](/docs/11.x/scheduling) を定義できます。

```
use App\Models\Invoice;
use Illuminate\Support\Carbon;

Invoice::pending()->cursor()
    ->takeUntilTimeout(
        Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')
    )
    ->each(fn (Invoice $invoice) => $invoice->submit());
```

<a name="method-tapEach"></a>
<!-- #### `tapEach()` -->
#### `tapEach()`
<!-- While the `each` method calls the given callback for each item in the collection right away, the `tapEach` method only calls the given callback as the items are being pulled out of the list one by one: -->
`each` メソッドは、コレクション内の各項目に対して指定されたコールバックをすぐに呼び出しますが、`tapEach` メソッドは、項目がリストから 1 つずつ取り出されるときにのみ、指定されたコールバックを呼び出します。

```
// Nothing has been dumped so far...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// Three items are dumped...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
<!-- #### `throttle()` -->
#### `throttle()`
<!-- The `throttle` method will throttle the lazy collection such that each value is returned after the specified number of seconds. This method is especially useful for situations where you may be interacting with external APIs that rate limit incoming requests: -->
`throttle` メソッドは、指定された秒数の後に各値が返されるように遅延コレクションを調整します。このメソッドは、受信リクエストをレート制限する外部 API と対話する可能性がある状況で特に役立ちます。

```php
use App\Models\User;

User::where('vip', true)
    ->cursor()
    ->throttle(seconds: 1)
    ->each(function (User $user) {
        // Call external API...
    });
```

<a name="method-remember"></a>
<!-- #### `remember()` -->
#### `remember()`
<!-- The `remember` method returns a new lazy collection that will remember any values that have already been enumerated and will not retrieve them again on subsequent collection enumerations: -->
`remember` メソッドは、すでに列挙された値を記憶し、後続のコレクション列挙ではそれらの値を再度取得しない、新しい遅延コレクションを返します。

```
// No query has been executed yet...
$users = User::cursor()->remember();

// The query is executed...
// The first 5 users are hydrated from the database...
$users->take(5)->all();

// First 5 users come from the collection's cache...
// The rest are hydrated from the database...
$users->take(20)->all();
```

