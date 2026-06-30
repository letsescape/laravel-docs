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
`Illuminate\Support\Collection` 클래스는 데이터 배열 작업을 위한 유연하고 편리한 래퍼를 제공합니다. 예를 들어, 다음 코드를 확인하세요. `collect` 도우미를 사용하여 배열에서 새 컬렉션 인스턴스를 만들고 각 요소에 대해 `strtoupper` 함수를 실행한 다음 모든 빈 요소를 제거합니다.

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

<!-- As you can see, the `Collection` class allows you to chain its methods to perform fluent mapping and reducing of the underlying array. In general, collections are immutable, meaning every `Collection` method returns an entirely new `Collection` instance. -->
보시다시피, `Collection` 클래스를 사용하면 메서드를 연결하여 기본 배열을 유창하게 매핑하고 축소할 수 있습니다. 일반적으로 컬렉션은 변경할 수 없습니다. 즉, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
<!-- ### Creating Collections -->
### Creating Collections

<!-- As mentioned above, the `collect` helper returns a new `Illuminate\Support\Collection` instance for the given array. So, creating a collection is as simple as: -->
위에서 언급한 것처럼 `collect` 도우미는 지정된 배열에 대해 새 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 만드는 것은 다음과 같이 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

<!-- You may also create a collection using the [make](#method-make) and [fromJson](#method-fromjson) methods. -->
[make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용하여 컬렉션을 만들 수도 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
<!-- ### Extending Collections -->
### Extending Collections

<!-- Collections are "macroable", which allows you to add additional methods to the `Collection` class at run time. The `Illuminate\Support\Collection` class' `macro` method accepts a closure that will be executed when your macro is called. The macro closure may access the collection's other methods via `$this`, just as if it were a real method of the collection class. For example, the following code adds a `toUpper` method to the `Collection` class: -->
컬렉션은 "매크로 가능"하므로 런타임에 `Collection` 클래스에 추가 메서드를 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행될 클로저를 허용합니다. 매크로 클로저는 마치 컬렉션 클래스의 실제 메서드인 것처럼 `$this`를 통해 컬렉션의 다른 메서드에 액세스할 수 있습니다. 예를 들어 다음 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다.

```php
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

<!-- Typically, you should declare collection macros in the `boot` method of a [service provider](/docs/12.x/providers). -->
일반적으로 [service provider](/docs/12.x/providers)의 `boot` 메서드에서 컬렉션 매크로를 선언해야 합니다.

<a name="macro-arguments"></a>
<!-- #### Macro Arguments -->
#### Macro Arguments

<!-- If necessary, you may define macros that accept additional arguments: -->
필요한 경우 추가 인수를 허용하는 매크로를 정의할 수 있습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Lang;

Collection::macro('toLocale', function (string $locale) {
    return $this->map(function (string $value) use ($locale) {
        return Lang::get($value, [], $locale);
    });
});

$collection = collect(['first', 'second']);

$translated = $collection->toLocale('es');

// ['primero', 'segundo'];
```

<a name="available-methods"></a>
<!-- ## Available Methods -->
## Available Methods

<!-- For the majority of the remaining collection documentation, we'll discuss each method available on the `Collection` class. Remember, all of these methods may be chained to fluently manipulate the underlying array. Furthermore, almost every method returns a new `Collection` instance, allowing you to preserve the original copy of the collection when necessary: -->
나머지 컬렉션 문서의 대부분에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 설명합니다. 이러한 모든 메서드는 기본 배열을 원활하게 조작하기 위해 연결될 수 있다는 점을 기억하세요. 게다가 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로 필요할 때 컬렉션의 원본을 보존할 수 있습니다.

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
[doesntContainStrict](#method-doesntcontainstrict)
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
[fromJson](#method-fromjson)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[hasMany](#method-hasmany)
[hasSole](#method-hassole)
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
[toPrettyJson](#method-to-pretty-json)
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
[doesntContainStrict](#method-doesntcontainstrict)
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
[fromJson](#method-fromjson)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[hasMany](#method-hasmany)
[hasSole](#method-hassole)
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
[toPrettyJson](#method-to-pretty-json)
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
`after` 메서드는 주어진 항목 뒤에 있는 항목을 반환합니다. 주어진 항목을 찾을 수 없거나 마지막 항목인 경우 `null`가 반환됩니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

<!-- This method searches for the given item using "loose" comparison, meaning a string containing an integer value will be considered equal to an integer of the same value. To use "strict" comparison, you may provide the `strict` argument to the method: -->
이 메서드는 "느슨한" 비교를 사용하여 지정된 항목을 검색합니다. 즉, 정수 값을 포함하는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다. "엄격한" 비교를 사용하려면 메서드에 `strict` 인수를 제공하면 됩니다.

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

<!-- Alternatively, you may provide your own closure to search for the first item that passes a given truth test: -->
또는 주어진 진실성 테스트를 통과한 첫 번째 항목을 검색하기 위해 자체 클로저를 제공할 수도 있습니다.

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
<!-- #### `all()` -->
#### `all()`

<!-- The `all` method returns the underlying array represented by the collection: -->
`all` 메서드는 컬렉션이 나타내는 기본 배열을 반환합니다.

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
<!-- #### `average()` -->
#### `average()`

<!-- Alias for the [avg](#method-avg) method. -->
[avg](#method-avg) 메서드의 별칭입니다.

<a name="method-avg"></a>
<!-- #### `avg()` -->
#### `avg()`

<!-- The `avg` method returns the [average value](https://en.wikipedia.org/wiki/Average) of a given key: -->
`avg` 메서드는 지정된 키의 [average value](https://en.wikipedia.org/wiki/Average)을 반환합니다.

```php
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

<!-- The `before` method is the opposite of the [after](#method-after) method. It returns the item before the given item. `null` is returned if the given item is not found or is the first item: -->
`before` 메서드는 [after](#method-after) 메서드와 반대입니다. 주어진 항목 앞에 있는 항목을 반환합니다. 주어진 항목을 찾을 수 없거나 첫 번째 항목인 경우 `null`가 반환됩니다.

```php
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
`chunk` 메서드는 컬렉션을 지정된 크기의 여러 개의 작은 컬렉션으로 나눕니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

<!-- This method is especially useful in [views](/docs/12.x/views) when working with a grid system such as [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/). For example, imagine you have a collection of [Eloquent](/docs/12.x/eloquent) models you want to display in a grid: -->
이 메서드는 [뷰](/docs/12.x/views)에서 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/)과 같은 그리드 시스템으로 작업할 때 특히 유용합니다. 예를 들어 그리드에 표시하려는 [Eloquent](/docs/12.x/eloquent) 모델 컬렉션이 있다고 가정해 보겠습니다.

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
`chunkWhile` 메서드는 지정된 콜백 평가에 따라 컬렉션을 여러 개의 작은 컬렉션으로 나눕니다. 클로저에 전달된 `$chunk` 변수는 이전 요소를 검사하는 데 사용될 수 있습니다:

```php
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

<!-- The `collapse` method collapses a collection of arrays or collections into a single, flat collection: -->
`collapse` 메서드는 배열 또는 컬렉션 컬렉션을 단일 플랫 컬렉션으로 축소합니다.

```php
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

<!-- The `collapseWithKeys` method flattens a collection of arrays or collections into a single collection, keeping the original keys intact. If the collection is already flat, it will return an empty collection: -->
`collapseWithKeys` 메서드는 배열 또는 컬렉션 모음을 단일 컬렉션으로 평면화하여 원래 키를 그대로 유지합니다. 컬렉션이 이미 플랫인 경우 빈 컬렉션을 반환합니다.

```php
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
`collect` 메서드는 현재 컬렉션에 있는 항목이 포함된 새 `Collection` 인스턴스를 반환합니다.

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

<!-- The `collect` method is primarily useful for converting [lazy collections](#lazy-collections) into standard `Collection` instances: -->
`collect` 메서드는 주로 [lazy collections](#lazy-collections)을 표준 `Collection` 인스턴스로 변환하는 데 유용합니다.

```php
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
> `collect` 메서드는 `Enumerable` 인스턴스가 있고 지연되지 않은 컬렉션 인스턴스가 필요할 때 특히 유용합니다. `collect()`는 `Enumerable` 컨트랙트의 일부이므로 이를 사용하여 `Collection` 인스턴스를 안전하게 얻을 수 있습니다.

<a name="method-combine"></a>
<!-- #### `combine()` -->
#### `combine()`

<!-- The `combine` method combines the values of the collection, as keys, with the values of another array or collection: -->
`combine` 메서드는 컬렉션의 값을 키로 다른 배열 또는 컬렉션의 값과 결합합니다.

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
<!-- #### `concat()` -->
#### `concat()`

<!-- The `concat` method appends the given array or collection's values onto the end of another collection: -->
`concat` 메서드는 주어진 배열이나 컬렉션의 값을 다른 컬렉션의 끝에 추가합니다:

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

<!-- The `concat` method numerically reindexes keys for items concatenated onto the original collection. To maintain keys in associative collections, see the [merge](#method-merge) method. -->
`concat` 메서드는 원래 컬렉션에 연결된 항목의 키를 수치적으로 다시 인덱싱합니다. 연관 컬렉션의 키를 유지하려면 [merge](#method-merge) 메서드를 참조하세요.

<a name="method-contains"></a>
<!-- #### `contains()` -->
#### `contains()`

<!-- The `contains` method determines whether the collection contains a given item. You may pass a closure to the `contains` method to determine if an element exists in the collection matching a given truth test: -->
`contains` 메서드는 컬렉션에 특정 항목이 포함되어 있는지 여부를 확인합니다. 주어진 진실 테스트와 일치하는 요소가 컬렉션에 존재하는지 확인하기 위해 `contains` 메서드에 클로저를 전달할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `contains` method to determine whether the collection contains a given item value: -->
또는 컬렉션에 지정된 항목 값이 포함되어 있는지 확인하기 위해 문자열을 `contains` 메서드에 전달할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

<!-- You may also pass a key / value pair to the `contains` method, which will determine if the given pair exists in the collection: -->
또한 키/값 쌍을 `contains` 메서드에 전달할 수도 있으며, 이는 주어진 쌍이 컬렉션에 존재하는지 확인합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

<!-- The `contains` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [containsStrict](#method-containsstrict) method to filter using "strict" comparisons. -->
`contains` 메서드는 항목 값을 확인할 때 "느슨한" 비교를 사용합니다. 즉, 정수 값이 있는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다. "엄격한" 비교를 사용하여 필터링하려면 [containsStrict](#method-containsstrict) 메서드를 사용하세요.

<!-- For the inverse of `contains`, see the [doesntContain](#method-doesntcontain) method. -->
`contains`의 반대에 대해서는 [doesntContain](#method-doesntcontain) 메서드를 참조하세요.

<a name="method-containsstrict"></a>
<!-- #### `containsStrict()` -->
#### `containsStrict()`

<!-- This method has the same signature as the [contains](#method-contains) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [contains](#method-contains) 메서드와 동일한 서명을 갖습니다. 그러나 모든 값은 "엄격한" 비교를 사용하여 비교됩니다.

> [!NOTE]
> 이 메서드의 동작은 [Eloquent Collections](/docs/12.x/eloquent-collections#method-contains)을 사용할 때 수정됩니다.

<a name="method-count"></a>
<!-- #### `count()` -->
#### `count()`

<!-- The `count` method returns the total number of items in the collection: -->
`count` 메서드는 컬렉션에 있는 총 항목 수를 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
<!-- #### `countBy()` -->
#### `countBy()`

<!-- The `countBy` method counts the occurrences of values in the collection. By default, the method counts the occurrences of every element, allowing you to count certain "types" of elements in the collection: -->
`countBy` 메서드는 컬렉션에서 값의 발생 횟수를 계산합니다. 기본적으로 이 메서드는 모든 요소의 발생 횟수를 계산하므로 컬렉션에 있는 요소의 특정 "유형"을 계산할 수 있습니다.

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

<!-- You may pass a closure to the `countBy` method to count all items by a custom value: -->
사용자 지정 값으로 모든 항목을 계산하기 위해 `countBy` 메서드에 클로저를 전달할 수 있습니다.

```php
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function (string $email) {
    return substr(strrchr($email, '@'), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
<!-- #### `crossJoin()` -->
#### `crossJoin()`

<!-- The `crossJoin` method cross joins the collection's values among the given arrays or collections, returning a Cartesian product with all possible permutations: -->
`crossJoin` 메서드는 주어진 배열 또는 컬렉션 사이에서 컬렉션의 값을 교차 조인하여 가능한 모든 순열을 포함하는 데카르트 곱을 반환합니다.

```php
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
`dd` 메서드는 컬렉션의 항목을 덤프하고 스크립트 실행을 종료합니다.

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dd();

/*
    array:2 [
        0 => "John Doe"
        1 => "Jane Doe"
    ]
*/
```

<!-- If you do not want to stop executing the script, use the [dump](#method-dump) method instead. -->
스크립트 실행을 중지하지 않으려면 대신 [dump](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>
<!-- #### `diff()` -->
#### `diff()`

<!-- The `diff` method compares the collection against another collection or a plain PHP `array` based on its values. This method will return the values in the original collection that are not present in the given collection: -->
`diff` 메서드는 해당 값을 기반으로 컬렉션을 다른 컬렉션 또는 일반 PHP `array`와 비교합니다. 이 메서드는 주어진 컬렉션에 존재하지 않는 원래 컬렉션의 값을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> 이 메서드의 동작은 [Eloquent Collections](/docs/12.x/eloquent-collections#method-diff)을 사용할 때 수정됩니다.

<a name="method-diffassoc"></a>
<!-- #### `diffAssoc()` -->
#### `diffAssoc()`

<!-- The `diffAssoc` method compares the collection against another collection or a plain PHP `array` based on its keys and values. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffAssoc` 메서드는 키와 값을 기반으로 컬렉션을 다른 컬렉션이나 일반 PHP `array`와 비교합니다. 이 메서드는 주어진 컬렉션에 존재하지 않는 원래 컬렉션의 키/값 쌍을 반환합니다.

```php
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
`diffAssoc`와 달리 `diffAssocUsing`는 인덱스 비교를 위해 사용자 제공 콜백 함수를 허용합니다.

```php
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

<!-- The callback must be a comparison function that returns an integer less than, equal to, or greater than zero. For more information, refer to the PHP documentation on [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters), which is the PHP function that the `diffAssocUsing` method utilizes internally. -->
콜백은 0보다 작거나 같거나 큰 정수를 반환하는 비교 함수여야 합니다. 자세한 내용은 `diffAssocUsing` 메서드가 내부적으로 활용하는 PHP 함수인 [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters)에 대한 PHP 설명서를 참조하세요.

<a name="method-diffkeys"></a>
<!-- #### `diffKeys()` -->
#### `diffKeys()`

<!-- The `diffKeys` method compares the collection against another collection or a plain PHP `array` based on its keys. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffKeys` 메서드는 해당 키를 기반으로 컬렉션을 다른 컬렉션 또는 일반 PHP `array`와 비교합니다. 이 메서드는 주어진 컬렉션에 존재하지 않는 원래 컬렉션의 키/값 쌍을 반환합니다.

```php
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
`doesntContain` 메서드는 컬렉션에 지정된 항목이 포함되어 있지 않은지 여부를 확인합니다. 주어진 진실 테스트와 일치하는 요소가 컬렉션에 존재하지 않는지 확인하기 위해 `doesntContain` 메서드에 클로저를 전달할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `doesntContain` method to determine whether the collection does not contain a given item value: -->
또는 컬렉션에 지정된 항목 값이 포함되어 있지 않은지 확인하기 위해 문자열을 `doesntContain` 메서드에 전달할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

<!-- You may also pass a key / value pair to the `doesntContain` method, which will determine if the given pair does not exist in the collection: -->
또한 키/값 쌍을 `doesntContain` 메서드에 전달할 수도 있습니다. 그러면 주어진 쌍이 컬렉션에 존재하지 않는지 확인할 수 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

<!-- The `doesntContain` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. -->
`doesntContain` 메서드는 항목 값을 확인할 때 "느슨한" 비교를 사용합니다. 즉, 정수 값이 있는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다.

<a name="method-doesntcontainstrict"></a>
<!-- #### `doesntContainStrict()` -->
#### `doesntContainStrict()`

<!-- This method has the same signature as the [doesntContain](#method-doesntcontain) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [doesntContain](#method-doesntcontain) 메서드와 동일한 시그니처를 갖습니다. 그러나 모든 값은 "엄격한" 비교를 사용하여 비교됩니다.

<a name="method-dot"></a>
<!-- #### `dot()` -->
#### `dot()`

<!-- The `dot` method flattens a multi-dimensional collection into a single level collection that uses "dot" notation to indicate depth: -->
`dot` 메서드는 다차원 컬렉션을 "점" 표기법을 사용하여 깊이를 나타내는 단일 수준 컬렉션으로 평면화합니다.

```php
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
<!-- #### `dump()` -->
#### `dump()`

<!-- The `dump` method dumps the collection's items: -->
`dump` 메서드는 컬렉션의 항목을 덤프합니다.

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dump();

/*
    array:2 [
        0 => "John Doe"
        1 => "Jane Doe"
    ]
*/
```

<!-- If you want to stop executing the script after dumping the collection, use the [dd](#method-dd) method instead. -->
컬렉션을 덤프한 후 스크립트 실행을 중지하려면 [dd](#method-dd) 메서드를 대신 사용하세요.

<a name="method-duplicates"></a>
<!-- #### `duplicates()` -->
#### `duplicates()`

<!-- The `duplicates` method retrieves and returns duplicate values from the collection: -->
`duplicates` 메서드는 컬렉션에서 중복 값을 검색하고 반환합니다.

```php
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

<!-- If the collection contains arrays or objects, you can pass the key of the attributes that you wish to check for duplicate values: -->
컬렉션에 배열이나 객체가 포함된 경우 중복 값을 확인하려는 속성의 키를 전달할 수 있습니다.

```php
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

<!-- This method has the same signature as the [duplicates](#method-duplicates) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [duplicates](#method-duplicates) 메서드와 동일한 시그니처를 갖습니다. 그러나 모든 값은 "엄격한" 비교를 사용하여 비교됩니다.

<a name="method-each"></a>
<!-- #### `each()` -->
#### `each()`

<!-- The `each` method iterates over the items in the collection and passes each item to a closure: -->
`each` 메서드는 컬렉션의 항목을 반복하고 각 항목을 클로저에 전달합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

<!-- If you would like to stop iterating through the items, you may return `false` from your closure: -->
항목 반복을 중지하려면 클로저에서 `false`를 반환하면 됩니다.

```php
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
`eachSpread` 메서드는 컬렉션의 항목을 반복하여 중첩된 각 항목 값을 지정된 콜백에 전달합니다.

```php
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

<!-- You may stop iterating through the items by returning `false` from the callback: -->
콜백에서 `false`를 반환하여 항목 반복을 중지할 수 있습니다.

```php
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
<!-- #### `ensure()` -->
#### `ensure()`

<!-- The `ensure` method may be used to verify that all elements of a collection are of a given type or list of types. Otherwise, an `UnexpectedValueException` will be thrown: -->
`ensure` 메서드는 컬렉션의 모든 요소가 지정된 유형 또는 유형 목록인지 확인하는 데 사용할 수 있습니다. 그렇지 않으면 `UnexpectedValueException`가 발생합니다.

```php
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

<!-- Primitive types such as `string`, `int`, `float`, `bool`, and `array` may also be specified: -->
`string`, `int`, `float`, `bool` 및 `array`와 같은 기본 유형도 지정할 수 있습니다.

```php
return $collection->ensure('int');
```

> [!WARNING]
> `ensure` 메서드는 나중에 다른 유형의 요소가 컬렉션에 추가되지 않는다고 보장하지 않습니다.

<a name="method-every"></a>
<!-- #### `every()` -->
#### `every()`

<!-- The `every` method may be used to verify that all elements of a collection pass a given truth test: -->
`every` 메서드는 컬렉션의 모든 요소가 주어진 진실 테스트를 통과하는지 확인하는 데 사용할 수 있습니다.

```php
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

<!-- If the collection is empty, the `every` method will return true: -->
컬렉션이 비어 있으면 `every` 메서드는 true를 반환합니다.

```php
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
`except` 메서드는 지정된 키가 있는 항목을 제외하고 컬렉션의 모든 항목을 반환합니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

<!-- For the inverse of `except`, see the [only](#method-only) method. -->
`except`의 반대에 대해서는 [only](#method-only) 메서드를 참조하세요.

> [!NOTE]
> 이 메서드의 동작은 [Eloquent Collections](/docs/12.x/eloquent-collections#method-except)을 사용할 때 수정됩니다.

<a name="method-filter"></a>
<!-- #### `filter()` -->
#### `filter()`

<!-- The `filter` method filters the collection using the given callback, keeping only those items that pass a given truth test: -->
`filter` 메서드는 주어진 콜백을 사용하여 컬렉션을 필터링하여 주어진 진실성 테스트를 통과한 항목만 유지합니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

<!-- If no callback is supplied, all entries of the collection that are equivalent to `false` will be removed: -->
콜백이 제공되지 않으면 `false`에 해당하는 컬렉션의 모든 항목이 제거됩니다.

```php
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

<!-- For the inverse of `filter`, see the [reject](#method-reject) method. -->
`filter`의 반대에 대해서는 [reject](#method-reject) 메서드를 참조하세요.

<a name="method-first"></a>
<!-- #### `first()` -->
#### `first()`

<!-- The `first` method returns the first element in the collection that passes a given truth test: -->
`first` 메서드는 주어진 진실성 테스트를 통과한 컬렉션의 첫 번째 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

<!-- You may also call the `first` method with no arguments to get the first element in the collection. If the collection is empty, `null` is returned: -->
컬렉션의 첫 번째 요소를 가져오기 위해 인수 없이 `first` 메서드를 호출할 수도 있습니다. 컬렉션이 비어 있으면 `null`가 반환됩니다.

```php
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
<!-- #### `firstOrFail()` -->
#### `firstOrFail()`

<!-- The `firstOrFail` method is identical to the `first` method; however, if no result is found, an `Illuminate\Support\ItemNotFoundException` exception will be thrown: -->
`firstOrFail` 메서드는 `first` 메서드와 동일합니다. 그러나 결과가 없으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// Throws ItemNotFoundException...
```

<!-- You may also call the `firstOrFail` method with no arguments to get the first element in the collection. If the collection is empty, an `Illuminate\Support\ItemNotFoundException` exception will be thrown: -->
컬렉션의 첫 번째 요소를 가져오기 위해 인수 없이 `firstOrFail` 메서드를 호출할 수도 있습니다. 컬렉션이 비어 있으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
collect([])->firstOrFail();

// Throws ItemNotFoundException...
```

<a name="method-first-where"></a>
<!-- #### `firstWhere()` -->
#### `firstWhere()`

<!-- The `firstWhere` method returns the first element in the collection with the given key / value pair: -->
`firstWhere` 메서드는 주어진 키/값 쌍이 있는 컬렉션의 첫 번째 요소를 반환합니다.

```php
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
비교 연산자를 사용하여 `firstWhere` 메서드를 호출할 수도 있습니다.

```php
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

<!-- Like the [where](#method-where) method, you may pass one argument to the `firstWhere` method. In this scenario, the `firstWhere` method will return the first item where the given item key's value is "truthy": -->
[where](#method-where) 메서드와 마찬가지로 `firstWhere` 메서드에 하나의 인수를 전달할 수 있습니다. 이 시나리오에서 `firstWhere` 메서드는 지정된 항목 키 값이 "truthy"인 첫 번째 항목을 반환합니다.

```php
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
<!-- #### `flatMap()` -->
#### `flatMap()`

<!-- The `flatMap` method iterates through the collection and passes each value to the given closure. The closure is free to modify the item and return it, thus forming a new collection of modified items. Then, the array is flattened by one level: -->
`flatMap` 메서드는 컬렉션을 반복하고 각 값을 지정된 클로저에 전달합니다. 클로저는 항목을 자유롭게 수정하고 반환할 수 있으므로 수정된 항목의 새로운 컬렉션을 형성합니다. 그런 다음 배열은 한 수준씩 평면화됩니다.

```php
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
`flatten` 메서드는 다차원 컬렉션을 단일 차원으로 평면화합니다.

```php
$collection = collect([
    'name' => 'Taylor',
    'languages' => [
        'PHP', 'JavaScript'
    ]
]);

$flattened = $collection->flatten();

$flattened->all();

// ['Taylor', 'PHP', 'JavaScript'];
```

<!-- If necessary, you may pass the `flatten` method a "depth" argument: -->
필요한 경우 `flatten` 메서드에 "깊이" 인수를 전달할 수 있습니다.

```php
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
이 예에서 깊이를 제공하지 않고 `flatten`를 호출하면 중첩 배열도 평면화되어 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`가 생성됩니다. 깊이를 제공하면 중첩 배열이 평면화될 수준 수를 지정할 수 있습니다.

<a name="method-flip"></a>
<!-- #### `flip()` -->
#### `flip()`

<!-- The `flip` method swaps the collection's keys with their corresponding values: -->
`flip` 메서드는 컬렉션의 키를 해당 값으로 바꿉니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['Taylor' => 'name', 'Laravel' => 'framework']
```

<a name="method-forget"></a>
<!-- #### `forget()` -->
#### `forget()`

<!-- The `forget` method removes an item from the collection by its key: -->
`forget` 메서드는 해당 키를 사용하여 컬렉션에서 항목을 제거합니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

// Forget a single key...
$collection->forget('name');

// ['framework' => 'Laravel']

// Forget multiple keys...
$collection->forget(['name', 'framework']);

// []
```

> [!WARNING]
> 대부분의 다른 컬렉션 메서드와 달리 `forget`는 수정된 새 컬렉션을 반환하지 않습니다. 호출된 컬렉션을 수정하고 반환합니다.

<a name="method-forpage"></a>
<!-- #### `forPage()` -->
#### `forPage()`

<!-- The `forPage` method returns a new collection containing the items that would be present on a given page number. The method accepts the page number as its first argument and the number of items to show per page as its second argument: -->
`forPage` 메서드는 주어진 페이지 번호에 나타날 항목이 포함된 새 컬렉션을 반환합니다. 이 메서드는 페이지 번호를 첫 번째 인수로, 페이지당 표시할 항목 수를 두 번째 인수로 받아들입니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-fromjson"></a>
<!-- #### `fromJson()` -->
#### `fromJson()`

<!-- The static `fromJson` method creates a new collection instance by decoding a given JSON string using the `json_decode` PHP function: -->
정적 `fromJson` 메서드는 `json_decode` PHP 함수를 사용하여 지정된 JSON 문자열을 디코딩하여 새 컬렉션 인스턴스를 생성합니다.

```php
use Illuminate\Support\Collection;

$json = json_encode([
    'name' => 'Taylor Otwell',
    'role' => 'Developer',
    'status' => 'Active',
]);

$collection = Collection::fromJson($json);
```

<a name="method-get"></a>
<!-- #### `get()` -->
#### `get()`

<!-- The `get` method returns the item at a given key. If the key does not exist, `null` is returned: -->
`get` 메서드는 주어진 키에 있는 항목을 반환합니다. 키가 존재하지 않으면 `null`가 반환됩니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$value = $collection->get('name');

// Taylor
```

<!-- You may optionally pass a default value as the second argument: -->
선택적으로 기본값을 두 번째 인수로 전달할 수 있습니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$value = $collection->get('age', 34);

// 34
```

<!-- You may even pass a callback as the method's default value. The result of the callback will be returned if the specified key does not exist: -->
메서드의 기본값으로 콜백을 전달할 수도 있습니다. 지정된 키가 존재하지 않으면 콜백 결과가 반환됩니다.

```php
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
<!-- #### `groupBy()` -->
#### `groupBy()`

<!-- The `groupBy` method groups the collection's items by a given key: -->
`groupBy` 메서드는 주어진 키를 기준으로 컬렉션의 항목을 그룹화합니다.

```php
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
문자열 `key`를 전달하는 대신 콜백을 전달할 수 있습니다. 콜백은 다음을 통해 그룹에 키를 지정하려는 값을 반환해야 합니다.

```php
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
여러 그룹화 기준을 배열로 전달할 수 있습니다. 각 배열 요소는 다차원 배열 내의 해당 수준에 적용됩니다.

```php
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
`has` 메서드는 주어진 키가 컬렉션에 존재하는지 확인합니다.

```php
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
`hasAny` 메서드는 주어진 키 중 컬렉션에 존재하는 키가 있는지 확인합니다.

```php
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-hasmany"></a>
<!-- #### `hasMany()` -->
#### `hasMany()`

<!-- The `hasMany` method determines whether the collection contains multiple items: -->
`hasMany` 메서드는 컬렉션에 여러 항목이 포함되어 있는지 확인합니다.

```php
collect([])->hasMany();

// false

collect(['1'])->hasMany();

// false

collect([1, 2, 3])->hasMany();

// true

collect([
    ['age' => 2],
    ['age' => 3],
])->hasMany(fn ($item) => $item['age'] === 2)

// false
```

<a name="method-hassole"></a>
<!-- #### `hasSole()` -->
#### `hasSole()`

<!-- The `hasSole` method determines if the collection contains a single item, optionally matching the given criteria: -->
`hasSole` 메서드는 컬렉션에 단일 항목이 포함되어 있는지 확인하고 선택적으로 주어진 기준과 일치합니다.

```php
collect([])->hasSole();

// false

collect(['1'])->hasSole();

// true

collect([1, 2, 3])->hasSole(fn (int $item) => $item === 2);

// true
```

<a name="method-implode"></a>
<!-- #### `implode()` -->
#### `implode()`

<!-- The `implode` method joins items in a collection. Its arguments depend on the type of items in the collection. If the collection contains arrays or objects, you should pass the key of the attributes you wish to join, and the "glue" string you wish to place between the values: -->
`implode` 메서드는 컬렉션의 항목을 결합합니다. 해당 인수는 컬렉션의 항목 유형에 따라 달라집니다. 컬렉션에 배열이나 개체가 포함된 경우 결합하려는 속성의 키와 값 사이에 배치하려는 "접착제" 문자열을 전달해야 합니다.

```php
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// 'Desk, Chair'
```

<!-- If the collection contains simple strings or numeric values, you should pass the "glue" as the only argument to the method: -->
컬렉션에 간단한 문자열이나 숫자 값이 포함된 경우 "glue"를 메서드의 유일한 인수로 전달해야 합니다.

```php
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

<!-- You may pass a closure to the `implode` method if you would like to format the values being imploded: -->
내포되는 값의 형식을 지정하려면 `implode` 메서드에 클로저를 전달할 수 있습니다.

```php
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// 'DESK, CHAIR'
```

<a name="method-intersect"></a>
<!-- #### `intersect()` -->
#### `intersect()`

<!-- The `intersect` method removes any values from the original collection that are not present in the given array or collection. The resulting collection will preserve the original collection's keys: -->
`intersect` 메서드는 지정된 배열이나 컬렉션에 없는 원래 컬렉션의 모든 값을 제거합니다. 결과 컬렉션은 원래 컬렉션의 키를 유지합니다.

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> 이 메서드의 동작은 [Eloquent Collections](/docs/12.x/eloquent-collections#method-intersect)을 사용할 때 수정됩니다.

<a name="method-intersectusing"></a>
<!-- #### `intersectUsing()` -->
#### `intersectUsing()`

<!-- The `intersectUsing` method removes any values from the original collection that are not present in the given array or collection, using a custom callback to compare the values. The resulting collection will preserve the original collection's keys: -->
`intersectUsing` 메서드는 값을 비교하는 사용자 지정 콜백을 사용하여 지정된 배열이나 컬렉션에 없는 원본 컬렉션의 모든 값을 제거합니다. 결과 컬렉션은 원래 컬렉션의 키를 유지합니다.

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersectUsing(['desk', 'chair', 'bookcase'], function (string $a, string $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

<a name="method-intersectAssoc"></a>
<!-- #### `intersectAssoc()` -->
#### `intersectAssoc()`

<!-- The `intersectAssoc` method compares the original collection against another collection or array, returning the key / value pairs that are present in all of the given collections: -->
`intersectAssoc` 메서드는 원본 컬렉션을 다른 컬렉션 또는 배열과 비교하여 지정된 모든 컬렉션에 존재하는 키/값 쌍을 반환합니다.

```php
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

<!-- The `intersectAssocUsing` method compares the original collection against another collection or array, returning the key / value pairs that are present in both, using a custom comparison callback to determine equality for both keys and values: -->
`intersectAssocUsing` 메서드는 원래 컬렉션을 다른 컬렉션이나 배열과 비교하여 두 컬렉션에 모두 존재하는 키/값 쌍을 반환하고, 사용자 지정 비교 콜백을 사용하여 키와 값이 같은지 확인합니다.

```php
$collection = collect([
    'color' => 'red',
    'Size' => 'M',
    'material' => 'cotton',
]);

$intersect = $collection->intersectAssocUsing([
    'color' => 'blue',
    'size' => 'M',
    'material' => 'polyester',
], function (string $a, string $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// ['Size' => 'M']
```

<a name="method-intersectbykeys"></a>
<!-- #### `intersectByKeys()` -->
#### `intersectByKeys()`

<!-- The `intersectByKeys` method removes any keys and their corresponding values from the original collection that are not present in the given array or collection: -->
`intersectByKeys` 메서드는 지정된 배열이나 컬렉션에 없는 원본 컬렉션에서 모든 키와 해당 값을 제거합니다.

```php
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
컬렉션이 비어 있으면 `isEmpty` 메서드는 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다.

```php
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
<!-- #### `isNotEmpty()` -->
#### `isNotEmpty()`

<!-- The `isNotEmpty` method returns `true` if the collection is not empty; otherwise, `false` is returned: -->
컬렉션이 비어 있지 않으면 `isNotEmpty` 메서드는 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다.

```php
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
<!-- #### `join()` -->
#### `join()`

<!-- The `join` method joins the collection's values with a string. Using this method's second argument, you may also specify how the final element should be appended to the string: -->
`join` 메서드는 컬렉션의 값을 문자열과 결합합니다. 이 메서드의 두 번째 인수를 사용하면 최종 요소를 문자열에 추가하는 방식을 지정할 수도 있습니다.

```php
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
`keyBy` 메서드는 주어진 키로 컬렉션의 키를 지정합니다. 여러 항목에 동일한 키가 있는 경우 마지막 항목만 새 컬렉션에 나타납니다.

```php
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
메서드에 콜백을 전달할 수도 있습니다. 콜백은 다음을 통해 컬렉션의 키 값을 반환해야 합니다.

```php
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
`keys` 메서드는 컬렉션의 모든 키를 반환합니다.

```php
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
`last` 메서드는 주어진 진실성 테스트를 통과한 컬렉션의 마지막 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

<!-- You may also call the `last` method with no arguments to get the last element in the collection. If the collection is empty, `null` is returned: -->
컬렉션의 마지막 요소를 가져오기 위해 인수 없이 `last` 메서드를 호출할 수도 있습니다. 컬렉션이 비어 있으면 `null`가 반환됩니다.

```php
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
<!-- #### `lazy()` -->
#### `lazy()`

<!-- The `lazy` method returns a new [LazyCollection](#lazy-collections) instance from the underlying array of items: -->
`lazy` 메서드는 기본 항목 배열에서 새 [LazyCollection](#lazy-collections) 인스턴스를 반환합니다.

```php
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

<!-- This is especially useful when you need to perform transformations on a huge `Collection` that contains many items: -->
이는 많은 항목이 포함된 거대한 `Collection`에서 변환을 수행해야 할 때 특히 유용합니다.

```php
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

<!-- By converting the collection to a `LazyCollection`, we avoid having to allocate a ton of additional memory. Though the original collection still keeps _its_ values in memory, the subsequent filters will not. Therefore, virtually no additional memory will be allocated when filtering the collection's results. -->
컬렉션을 `LazyCollection`로 변환하면 엄청난 양의 추가 메모리를 할당할 필요가 없습니다. 원래 컬렉션은 여전히 ​​_its_ 값을 메모리에 유지하지만 후속 필터는 그렇지 않습니다. 따라서 컬렉션 결과를 필터링할 때 사실상 추가 메모리가 할당되지 않습니다.

<a name="method-macro"></a>
<!-- #### `macro()` -->
#### `macro()`

<!-- The static `macro` method allows you to add methods to the `Collection` class at run time. Refer to the documentation on [extending collections](#extending-collections) for more information. -->
정적 `macro` 메서드를 사용하면 런타임에 `Collection` 클래스에 메서드를 추가할 수 있습니다. 자세한 내용은 [extending collections](#extending-collections) 문서를 참조하세요.

<a name="method-make"></a>
<!-- #### `make()` -->
#### `make()`

<!-- The static `make` method creates a new collection instance. See the [Creating Collections](#creating-collections) section. -->
정적 `make` 메서드는 새 컬렉션 인스턴스를 생성합니다. [Creating Collections](#creating-collections) 섹션을 참조하세요.

```php
use Illuminate\Support\Collection;

$collection = Collection::make([1, 2, 3]);
```

<a name="method-map"></a>
<!-- #### `map()` -->
#### `map()`

<!-- The `map` method iterates through the collection and passes each value to the given callback. The callback is free to modify the item and return it, thus forming a new collection of modified items: -->
`map` 메서드는 컬렉션을 반복하고 각 값을 지정된 콜백에 전달합니다. 콜백은 항목을 자유롭게 수정하고 반환하여 수정된 항목의 새로운 컬렉션을 형성합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 다른 컬렉션 메서드와 마찬가지로 `map`는 새 컬렉션 인스턴스를 반환합니다. 호출된 컬렉션을 수정하지 않습니다. 원본 컬렉션을 변환하려면 [transform](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
<!-- #### `mapInto()` -->
#### `mapInto()`

<!-- The `mapInto()` method iterates over the collection, creating a new instance of the given class by passing the value into the constructor: -->
`mapInto()` 메서드는 컬렉션을 반복하여 생성자에 값을 전달하여 지정된 클래스의 새 인스턴스를 만듭니다.

```php
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
`mapSpread` 메서드는 컬렉션의 항목을 반복하여 중첩된 각 항목 값을 지정된 클로저에 전달합니다. 클로저는 항목을 자유롭게 수정하고 반환할 수 있으므로 수정된 항목의 새로운 컬렉션을 형성합니다.

```php
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
`mapToGroups` 메서드는 주어진 클로저에 따라 컬렉션의 항목을 그룹화합니다. 클로저는 단일 키/값 쌍을 포함하는 연관 배열을 반환해야 하며, 따라서 그룹화된 값의 새로운 컬렉션을 형성해야 합니다.

```php
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
`mapWithKeys` 메서드는 컬렉션을 반복하고 각 값을 지정된 콜백에 전달합니다. 콜백은 단일 키/값 쌍을 포함하는 연관 배열을 반환해야 합니다.

```php
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
`max` 메서드는 주어진 키의 최대값을 반환합니다.

```php
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
`median` 메서드는 지정된 키의 [median value](https://en.wikipedia.org/wiki/Median)을 반환합니다.

```php
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
`merge` 메서드는 주어진 배열이나 컬렉션을 원래 컬렉션과 병합합니다. 지정된 항목의 문자열 키가 원래 컬렉션의 문자열 키와 일치하면 지정된 항목의 값이 원래 컬렉션의 값을 덮어씁니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

<!-- If the given item's keys are numeric, the values will be appended to the end of the collection: -->
주어진 항목의 키가 숫자인 경우 값은 컬렉션의 끝에 추가됩니다.

```php
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
<!-- #### `mergeRecursive()` -->
#### `mergeRecursive()`

<!-- The `mergeRecursive` method merges the given array or collection recursively with the original collection. If a string key in the given items matches a string key in the original collection, then the values for these keys are merged together into an array, and this is done recursively: -->
`mergeRecursive` 메서드는 지정된 배열 또는 컬렉션을 원래 컬렉션과 재귀적으로 병합합니다. 지정된 항목의 문자열 키가 원래 컬렉션의 문자열 키와 일치하면 이러한 키의 값이 배열로 병합되고 이는 재귀적으로 수행됩니다.

```php
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
`min` 메서드는 주어진 키의 최소값을 반환합니다.

```php
$min = collect([
    ['foo' => 10],
    ['foo' => 20]
])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
<!-- #### `mode()` -->
#### `mode()`

<!-- The `mode` method returns the [mode value](https://en.wikipedia.org/wiki/Mode_(statistics)) of a given key: -->
`mode` 메서드는 지정된 키의 [mode value](https://en.wikipedia.org/wiki/Mode_(statistics))을 반환합니다.

```php
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
`multiply` 메서드는 컬렉션의 모든 항목에 대해 지정된 수의 복사본을 생성합니다.

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
`nth` 메서드는 모든 n번째 요소로 구성된 새 컬렉션을 만듭니다.

```php
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

<!-- You may optionally pass a starting offset as the second argument: -->
선택적으로 시작 오프셋을 두 번째 인수로 전달할 수도 있습니다.

```php
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
<!-- #### `only()` -->
#### `only()`

<!-- The `only` method returns the items in the collection with the specified keys: -->
`only` 메서드는 지정된 키를 사용하여 컬렉션의 항목을 반환합니다.

```php
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
`only`의 반대에 대해서는 [except](#method-except) 메서드를 참조하세요.

> [!NOTE]
> 이 메서드의 동작은 [Eloquent Collections](/docs/12.x/eloquent-collections#method-only)을 사용할 때 수정됩니다.

<a name="method-pad"></a>
<!-- #### `pad()` -->
#### `pad()`

<!-- The `pad` method will fill the array with the given value until the array reaches the specified size. This method behaves like the [array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP function. -->
`pad` 메서드는 배열이 지정된 크기에 도달할 때까지 주어진 값으로 배열을 채웁니다. 이 메서드는 [array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP 함수처럼 작동합니다.

<!-- To pad to the left, you should specify a negative size. No padding will take place if the absolute value of the given size is less than or equal to the length of the array: -->
왼쪽을 채우려면 음수 크기를 지정해야 합니다. 주어진 크기의 절대값이 배열 길이보다 작거나 같으면 패딩이 발생하지 않습니다.

```php
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
`partition` 메서드는 PHP 배열 구조 분해와 결합되어 주어진 진실 테스트를 통과하는 요소를 그렇지 않은 요소와 분리할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6]);

[$underThree, $equalOrAboveThree] = $collection->partition(function (int $i) {
    return $i < 3;
});

$underThree->all();

// [1, 2]

$equalOrAboveThree->all();

// [3, 4, 5, 6]
```

> [!NOTE]
> 이 메서드의 동작은 [Eloquent collections](/docs/12.x/eloquent-collections#method-partition)과 상호 작용할 때 수정됩니다.

<a name="method-percentage"></a>
<!-- #### `percentage()` -->
#### `percentage()`

<!-- The `percentage` method may be used to quickly determine the percentage of items in the collection that pass a given truth test: -->
`percentage` 메서드를 사용하면 컬렉션에서 특정 진실성 테스트를 통과한 항목의 비율을 빠르게 확인할 수 있습니다.

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn (int $value) => $value === 1);

// 33.33
```

<!-- By default, the percentage will be rounded to two decimal places. However, you may customize this behavior by providing a second argument to the method: -->
기본적으로 백분율은 소수점 이하 두 자리로 반올림됩니다. 그러나 메서드에 두 번째 인수를 제공하여 이 동작을 사용자 지정할 수 있습니다.

```php
$percentage = $collection->percentage(fn (int $value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
<!-- #### `pipe()` -->
#### `pipe()`

<!-- The `pipe` method passes the collection to the given closure and returns the result of the executed closure: -->
`pipe` 메서드는 컬렉션을 주어진 클로저에 전달하고 실행된 클로저의 결과를 반환합니다:

```php
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
`pipeInto` 메서드는 지정된 클래스의 새 인스턴스를 생성하고 컬렉션을 생성자에 전달합니다.

```php
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
`pipeThrough` 메서드는 컬렉션을 주어진 클로저 배열에 전달하고 실행된 클로저의 결과를 반환합니다.

```php
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
`pluck` 메서드는 지정된 키에 대한 모든 값을 검색합니다.

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

<!-- You may also specify how you wish the resulting collection to be keyed: -->
결과 컬렉션의 키 지정 방식을 지정할 수도 있습니다.

```php
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

<!-- The `pluck` method also supports retrieving nested values using "dot" notation: -->
`pluck` 메서드는 "점" 표기법을 사용하여 중첩된 값 검색도 지원합니다.

```php
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
중복된 키가 존재하는 경우 마지막으로 일치하는 요소가 추출된 컬렉션에 삽입됩니다.

```php
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

<!-- The `pop` method removes and returns the last item from the collection. If the collection is empty, `null` will be returned: -->
`pop` 메서드는 컬렉션에서 마지막 항목을 제거하고 반환합니다. 컬렉션이 비어 있으면 `null`가 반환됩니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

<!-- You may pass an integer to the `pop` method to remove and return multiple items from the end of a collection: -->
컬렉션의 끝에서 여러 항목을 제거하고 반환하려면 `pop` 메서드에 정수를 전달할 수 있습니다.

```php
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
`prepend` 메서드는 컬렉션의 시작 부분에 항목을 추가합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

<!-- You may also pass a second argument to specify the key of the prepended item: -->
앞에 추가된 항목의 키를 지정하기 위해 두 번째 인수를 전달할 수도 있습니다:

```php
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
<!-- #### `pull()` -->
#### `pull()`

<!-- The `pull` method removes and returns an item from the collection by its key: -->
`pull` 메서드는 해당 키를 사용하여 컬렉션에서 항목을 제거하고 반환합니다.

```php
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
`push` 메서드는 컬렉션의 끝에 항목을 추가합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<!-- You may also provide multiple items to append to the end of the collection: -->
컬렉션 끝에 추가할 여러 항목을 제공할 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5, 6, 7);

$collection->all();

// [1, 2, 3, 4, 5, 6, 7]
```

<a name="method-put"></a>
<!-- #### `put()` -->
#### `put()`

<!-- The `put` method sets the given key and value in the collection: -->
`put` 메서드는 컬렉션에 지정된 키와 값을 설정합니다.

```php
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
<!-- #### `random()` -->
#### `random()`

<!-- The `random` method returns a random item from the collection: -->
`random` 메서드는 컬렉션에서 임의의 항목을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (retrieved randomly)
```

<!-- You may pass an integer to `random` to specify how many items you would like to randomly retrieve. A collection of items is always returned when explicitly passing the number of items you wish to receive: -->
`random`에 정수를 전달하여 무작위로 검색하려는 항목 수를 지정할 수 있습니다. 수신하려는 항목 수를 명시적으로 전달할 때 항목 컬렉션이 항상 반환됩니다.

```php
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (retrieved randomly)
```

<!-- If the collection instance has fewer items than requested, the `random` method will throw an `InvalidArgumentException`. -->
컬렉션 인스턴스에 요청된 것보다 적은 항목이 있는 경우 `random` 메서드는 `InvalidArgumentException`를 발생시킵니다.

<!-- The `random` method also accepts a closure, which will receive the current collection instance: -->
`random` 메서드는 현재 컬렉션 인스턴스를 수신하는 클로저도 허용합니다.

```php
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] - (retrieved randomly)
```

<a name="method-range"></a>
<!-- #### `range()` -->
#### `range()`

<!-- The `range` method returns a collection containing integers between the specified range: -->
`range` 메서드는 지정된 범위 사이의 정수를 포함하는 컬렉션을 반환합니다.

```php
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
<!-- #### `reduce()` -->
#### `reduce()`

<!-- The `reduce` method reduces the collection to a single value, passing the result of each iteration into the subsequent iteration: -->
`reduce` 메서드는 컬렉션을 단일 값으로 줄여 각 반복의 결과를 후속 반복에 전달합니다.

```php
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

<!-- The value for `$carry` on the first iteration is `null`; however, you may specify its initial value by passing a second argument to `reduce`: -->
첫 번째 반복에서 `$carry`의 값은 `null`입니다. 그러나 `reduce`에 두 번째 인수를 전달하여 초기 값을 지정할 수 있습니다.

```php
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

<!-- The `reduce` method also passes array keys to the given callback: -->
`reduce` 메서드는 또한 배열 키를 지정된 콜백에 전달합니다.

```php
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

$collection->reduce(function (int $carry, int $value, string $key) use ($ratio) {
    return $carry + ($value * $ratio[$key]);
}, 0);

// 4264
```

<a name="method-reduce-spread"></a>
<!-- #### `reduceSpread()` -->
#### `reduceSpread()`

<!-- The `reduceSpread` method reduces the collection to an array of values, passing the results of each iteration into the subsequent iteration. This method is similar to the `reduce` method; however, it can accept multiple initial values: -->
`reduceSpread` 메서드는 컬렉션을 값 배열로 줄여 각 반복의 결과를 후속 반복에 전달합니다. 이 메서드는 `reduce` 메서드와 유사합니다. 그러나 여러 초기값을 허용할 수 있습니다.

```php
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
`reject` 메서드는 주어진 클로저를 사용하여 컬렉션을 필터링합니다. 결과 컬렉션에서 항목을 제거해야 하는 경우 클로저는 `true`를 반환해야 합니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

<!-- For the inverse of the `reject` method, see the [filter](#method-filter) method. -->
`reject` 메서드의 반대에 대해서는 [filter](#method-filter) 메서드를 참조하세요.

<a name="method-replace"></a>
<!-- #### `replace()` -->
#### `replace()`

<!-- The `replace` method behaves similarly to `merge`; however, in addition to overwriting matching items that have string keys, the `replace` method will also overwrite items in the collection that have matching numeric keys: -->
`replace` 메서드는 `merge`와 유사하게 동작합니다. 그러나 문자열 키가 있는 일치 항목을 덮어쓰는 것 외에도 `replace` 메서드는 일치하는 숫자 키가 있는 컬렉션의 항목도 덮어씁니다.

```php
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
<!-- #### `replaceRecursive()` -->
#### `replaceRecursive()`

<!-- The `replaceRecursive` method behaves similarly to `replace`, but it will recur into arrays and apply the same replacement process to the inner values: -->
`replaceRecursive` 메서드는 `replace`와 유사하게 동작하지만 배열로 반복되고 내부 값에 동일한 대체 프로세스를 적용합니다.

```php
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
`reverse` 메서드는 원래 키를 유지하면서 컬렉션 항목의 순서를 반대로 바꿉니다.

```php
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
`search` 메서드는 컬렉션에서 지정된 값을 검색하고 해당 값이 있으면 해당 키를 반환합니다. 항목을 찾을 수 없으면 `false`가 반환됩니다.

```php
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

<!-- The search is done using a "loose" comparison, meaning a string with an integer value will be considered equal to an integer of the same value. To use "strict" comparison, pass `true` as the second argument to the method: -->
검색은 "느슨한" 비교를 사용하여 수행됩니다. 즉, 정수 값이 있는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다. "엄격한" 비교를 사용하려면 `true`를 메서드의 두 번째 인수로 전달합니다.

```php
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

<!-- Alternatively, you may provide your own closure to search for the first item that passes a given truth test: -->
또는 주어진 진실성 테스트를 통과한 첫 번째 항목을 검색하기 위해 자체 클로저를 제공할 수도 있습니다.

```php
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
<!-- #### `select()` -->
#### `select()`

<!-- The `select` method selects the given keys from the collection, similar to an SQL `SELECT` statement: -->
`select` 메서드는 SQL `SELECT` 문과 유사하게 컬렉션에서 지정된 키를 선택합니다.

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
`shift` 메서드는 컬렉션에서 첫 번째 항목을 제거하고 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

<!-- You may pass an integer to the `shift` method to remove and return multiple items from the beginning of a collection: -->
컬렉션 시작 부분에서 여러 항목을 제거하고 반환하려면 `shift` 메서드에 정수를 전달할 수 있습니다.

```php
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
`shuffle` 메서드는 컬렉션의 항목을 무작위로 섞습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-skip"></a>
<!-- #### `skip()` -->
#### `skip()`

<!-- The `skip` method returns a new collection, with the given number of elements removed from the beginning of the collection: -->
`skip` 메서드는 컬렉션 시작 부분에서 지정된 수의 요소가 제거된 새 컬렉션을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
<!-- #### `skipUntil()` -->
#### `skipUntil()`

<!-- The `skipUntil` method skips over items from the collection while the given callback returns `false`. Once the callback returns `true` all of the remaining items in the collection will be returned as a new collection: -->
`skipUntil` 메서드는 지정된 콜백이 `false`를 반환하는 동안 컬렉션의 항목을 건너뜁니다. 콜백이 `true`를 반환하면 컬렉션의 나머지 모든 항목이 새 컬렉션으로 반환됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

<!-- You may also pass a simple value to the `skipUntil` method to skip all items until the given value is found: -->
`skipUntil` 메서드에 간단한 값을 전달하여 주어진 값을 찾을 때까지 모든 항목을 건너뛸 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> 지정된 값을 찾을 수 없거나 콜백이 `true`를 반환하지 않는 경우 `skipUntil` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
<!-- #### `skipWhile()` -->
#### `skipWhile()`

<!-- The `skipWhile` method skips over items from the collection while the given callback returns `true`. Once the callback returns `false` all of the remaining items in the collection will be returned as a new collection: -->
`skipWhile` 메서드는 지정된 콜백이 `true`를 반환하는 동안 컬렉션의 항목을 건너뜁니다. 콜백이 `false`를 반환하면 컬렉션의 나머지 모든 항목이 새 컬렉션으로 반환됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> 콜백이 `false`를 반환하지 않으면 `skipWhile` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
<!-- #### `slice()` -->
#### `slice()`

<!-- The `slice` method returns a slice of the collection starting at the given index: -->
`slice` 메서드는 지정된 인덱스에서 시작하는 컬렉션 조각을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

<!-- If you would like to limit the size of the returned slice, pass the desired size as the second argument to the method: -->
반환된 조각의 크기를 제한하려면 원하는 크기를 메서드의 두 번째 인수로 전달합니다.

```php
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

<!-- The returned slice will preserve keys by default. If you do not wish to preserve the original keys, you can use the [values](#method-values) method to reindex them. -->
반환된 슬라이스는 기본적으로 키를 유지합니다. 원래 키를 유지하지 않으려면 [values](#method-values) 메서드를 사용하여 다시 색인을 생성할 수 있습니다.

<a name="method-sliding"></a>
<!-- #### `sliding()` -->
#### `sliding()`

<!-- The `sliding` method returns a new collection of chunks representing a "sliding window" view of the items in the collection: -->
`sliding` 메서드는 컬렉션에 있는 항목의 "슬라이딩 창" 뷰을 나타내는 새로운 청크 컬렉션을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

<!-- This is especially useful in conjunction with the [eachSpread](#method-eachspread) method: -->
이는 [eachSpread](#method-eachspread) 메서드와 함께 사용하면 특히 유용합니다.

```php
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

<!-- You may optionally pass a second "step" value, which determines the distance between the first item of every chunk: -->
선택적으로 두 번째 "step" 값을 전달할 수도 있습니다. 이 값은 모든 청크의 첫 번째 항목 사이의 거리를 결정합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
<!-- #### `sole()` -->
#### `sole()`

<!-- The `sole` method returns the first element in the collection that passes a given truth test, but only if the truth test matches exactly one element: -->
`sole` 메서드는 주어진 진실성 테스트를 통과한 컬렉션의 첫 번째 요소를 반환합니다. 단, 진실성 테스트가 정확히 하나의 요소와 일치하는 경우에만 해당됩니다.

```php
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

<!-- You may also pass a key / value pair to the `sole` method, which will return the first element in the collection that matches the given pair, but only if it exactly one element matches: -->
또한 키/값 쌍을 `sole` 메서드에 전달할 수도 있습니다. 이 메서드는 주어진 쌍과 일치하는 컬렉션의 첫 번째 요소를 반환하지만 정확히 하나의 요소가 일치하는 경우에만 가능합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

<!-- Alternatively, you may also call the `sole` method with no argument to get the first element in the collection if there is only one element: -->
또는 요소가 하나만 있는 경우 컬렉션의 첫 번째 요소를 가져오기 위해 인수 없이 `sole` 메서드를 호출할 수도 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

<!-- If there are no elements in the collection that should be returned by the `sole` method, an `\Illuminate\Collections\ItemNotFoundException` exception will be thrown. If there is more than one element that should be returned, an `\Illuminate\Collections\MultipleItemsFoundException` will be thrown. -->
컬렉션에 `sole` 메서드에서 반환해야 하는 요소가 없으면 `\Illuminate\Collections\ItemNotFoundException` 예외가 발생합니다. 반환해야 하는 요소가 두 개 이상인 경우 `\Illuminate\Collections\MultipleItemsFoundException`가 발생합니다.

<a name="method-some"></a>
<!-- #### `some()` -->
#### `some()`

<!-- Alias for the [contains](#method-contains) method. -->
[contains](#method-contains) 메서드의 별칭입니다.

<a name="method-sort"></a>
<!-- #### `sort()` -->
#### `sort()`

<!-- The `sort` method sorts the collection. The sorted collection keeps the original array keys, so in the following example we will use the [values](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sort` 메서드는 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래 배열 키를 유지하므로 다음 예에서는 [values](#method-values) 메서드를 사용하여 키를 연속 번호가 지정된 인덱스로 재설정합니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

<!-- If your sorting needs are more advanced, you may pass a callback to `sort` with your own algorithm. Refer to the PHP documentation on [uasort](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters), which is what the collection's `sort` method calls utilizes internally. -->
정렬 요구 사항이 더 고급인 경우 자체 알고리즘을 사용하여 `sort`에 콜백을 전달할 수 있습니다. 컬렉션의 `sort` 메서드 호출이 내부적으로 활용하는 [uasort](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters)에 대한 PHP 문서를 참조하세요.

> [!NOTE]
> 중첩된 배열 또는 객체 컬렉션을 정렬해야 하는 경우 [sortBy](#method-sortby) 및 [sortByDesc](#method-sortbydesc) 메서드를 참조하세요.

<a name="method-sortby"></a>
<!-- #### `sortBy()` -->
#### `sortBy()`

<!-- The `sortBy` method sorts the collection by the given key. The sorted collection keeps the original array keys, so in the following example we will use the [values](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sortBy` 메서드는 주어진 키를 기준으로 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래 배열 키를 유지하므로 다음 예에서는 [values](#method-values) 메서드를 사용하여 키를 연속 번호가 지정된 인덱스로 재설정합니다.

```php
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
`sortBy` 메서드는 [sort flags](https://www.php.net/manual/en/function.sort.php)를 두 번째 인수로 허용합니다.

```php
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
또는 컬렉션의 값을 정렬하는 방식을 결정하기 위해 자체 클로저를 전달할 수도 있습니다.

```php
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
여러 속성을 기준으로 컬렉션을 정렬하려면 정렬 작업 배열을 `sortBy` 메서드에 전달할 수 있습니다. 각 정렬 작업은 정렬하려는 속성과 원하는 정렬 방향으로 구성된 배열이어야 합니다.

```php
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
여러 속성으로 컬렉션을 정렬할 때 각 정렬 작업을 정의하는 클로저를 제공할 수도 있습니다.

```php
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

<!-- This method has the same signature as the [sortBy](#method-sortby) method, but will sort the collection in the opposite order. -->
이 메서드는 [sortBy](#method-sortby) 메서드와 동일한 시그니처를 갖지만 컬렉션을 반대 순서로 정렬합니다.

<a name="method-sortdesc"></a>
<!-- #### `sortDesc()` -->
#### `sortDesc()`

<!-- This method will sort the collection in the opposite order as the [sort](#method-sort) method: -->
이 메서드는 [sort](#method-sort) 메서드와 반대 순서로 컬렉션을 정렬합니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

<!-- Unlike `sort`, you may not pass a closure to `sortDesc`. Instead, you should use the [sort](#method-sort) method and invert your comparison. -->
`sort`와 달리 `sortDesc`에 클로저를 전달할 수 없습니다. 대신 [sort](#method-sort) 메서드를 사용하고 비교를 거꾸로 해야 합니다.

<a name="method-sortkeys"></a>
<!-- #### `sortKeys()` -->
#### `sortKeys()`

<!-- The `sortKeys` method sorts the collection by the keys of the underlying associative array: -->
`sortKeys` 메서드는 기본 연관 배열의 키를 기준으로 컬렉션을 정렬합니다.

```php
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

<!-- This method has the same signature as the [sortKeys](#method-sortkeys) method, but will sort the collection in the opposite order. -->
이 메서드는 [sortKeys](#method-sortkeys) 메서드와 동일한 서명을 갖지만 컬렉션을 반대 순서로 정렬합니다.

<a name="method-sortkeysusing"></a>
<!-- #### `sortKeysUsing()` -->
#### `sortKeysUsing()`

<!-- The `sortKeysUsing` method sorts the collection by the keys of the underlying associative array using a callback: -->
`sortKeysUsing` 메서드는 콜백을 사용하여 기본 연관 배열의 키를 기준으로 컬렉션을 정렬합니다.

```php
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

<!-- The callback must be a comparison function that returns an integer less than, equal to, or greater than zero. For more information, refer to the PHP documentation on [uksort](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters), which is the PHP function that `sortKeysUsing` method utilizes internally. -->
콜백은 0보다 작거나 같거나 큰 정수를 반환하는 비교 함수여야 합니다. 자세한 내용은 `sortKeysUsing` 메서드가 내부적으로 활용하는 PHP 함수인 [uksort](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters)의 PHP 문서를 참조하세요.

<a name="method-splice"></a>
<!-- #### `splice()` -->
#### `splice()`

<!-- The `splice` method removes and returns a slice of items starting at the specified index: -->
`splice` 메서드는 지정된 인덱스에서 시작하는 항목 조각을 제거하고 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

<!-- You may pass a second argument to limit the size of the resulting collection: -->
결과 컬렉션의 크기를 제한하기 위해 두 번째 인수를 전달할 수 있습니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

<!-- In addition, you may pass a third argument containing the new items to replace the items removed from the collection: -->
또한 컬렉션에서 제거된 항목을 대체하기 위해 새 항목이 포함된 세 번째 인수를 전달할 수도 있습니다.

```php
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
`split` 메서드는 컬렉션을 지정된 수의 그룹으로 나눕니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
<!-- #### `splitIn()` -->
#### `splitIn()`

<!-- The `splitIn` method breaks a collection into the given number of groups, filling non-terminal groups completely before allocating the remainder to the final group: -->
`splitIn` 메서드는 컬렉션을 지정된 수의 그룹으로 나누어 비종단 그룹을 완전히 채우고 나머지를 최종 그룹에 할당합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
<!-- #### `sum()` -->
#### `sum()`

<!-- The `sum` method returns the sum of all items in the collection: -->
`sum` 메서드는 컬렉션에 있는 모든 항목의 합계를 반환합니다.

```php
collect([1, 2, 3, 4, 5])->sum();

// 15
```

<!-- If the collection contains nested arrays or objects, you should pass a key that will be used to determine which values to sum: -->
컬렉션에 중첩된 배열이나 개체가 포함된 경우 합산할 값을 결정하는 데 사용되는 키를 전달해야 합니다.

```php
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

<!-- In addition, you may pass your own closure to determine which values of the collection to sum: -->
게다가, 합산할 컬렉션의 값을 결정하기 위해 자신만의 클로저를 전달할 수도 있습니다:

```php
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
`take` 메서드는 지정된 수의 항목이 포함된 새 컬렉션을 반환합니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

<!-- You may also pass a negative integer to take the specified number of items from the end of the collection: -->
컬렉션 끝에서 지정된 수의 항목을 가져오려면 음의 정수를 전달할 수도 있습니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
<!-- #### `takeUntil()` -->
#### `takeUntil()`

<!-- The `takeUntil` method returns items in the collection until the given callback returns `true`: -->
`takeUntil` 메서드는 지정된 콜백이 `true`를 반환할 때까지 컬렉션의 항목을 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

<!-- You may also pass a simple value to the `takeUntil` method to get the items until the given value is found: -->
또한 주어진 값을 찾을 때까지 항목을 가져오기 위해 `takeUntil` 메서드에 간단한 값을 전달할 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> 지정된 값을 찾을 수 없거나 콜백이 `true`를 반환하지 않는 경우 `takeUntil` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-takewhile"></a>
<!-- #### `takeWhile()` -->
#### `takeWhile()`

<!-- The `takeWhile` method returns items in the collection until the given callback returns `false`: -->
`takeWhile` 메서드는 지정된 콜백이 `false`를 반환할 때까지 컬렉션의 항목을 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]
> 콜백이 `false`를 반환하지 않으면 `takeWhile` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-tap"></a>
<!-- #### `tap()` -->
#### `tap()`

<!-- The `tap` method passes the collection to the given callback, allowing you to "tap" into the collection at a specific point and do something with the items while not affecting the collection itself. The collection is then returned by the `tap` method: -->
`tap` 메서드는 컬렉션을 지정된 콜백에 전달하여 특정 지점에서 컬렉션을 "탭"하고 컬렉션 자체에 영향을 주지 않으면서 항목에 대해 작업을 수행할 수 있도록 합니다. 그런 다음 컬렉션은 `tap` 메서드에 의해 반환됩니다.

```php
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
정적 `times` 메서드는 지정된 클로저를 지정된 횟수만큼 호출하여 새 컬렉션을 생성합니다.

```php
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
<!-- #### `toArray()` -->
#### `toArray()`

<!-- The `toArray` method converts the collection into a plain PHP `array`. If the collection's values are [Eloquent](/docs/12.x/eloquent) models, the models will also be converted to arrays: -->
`toArray` 메서드는 컬렉션을 일반 PHP `array`로 변환합니다. 컬렉션의 값이 [Eloquent](/docs/12.x/eloquent) 모델인 경우 모델도 배열로 변환됩니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toArray();

/*
    [
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

> [!WARNING]
> `toArray`는 또한 `Arrayable`의 인스턴스인 컬렉션의 모든 중첩 개체를 배열로 변환합니다. 컬렉션의 기본이 되는 원시 배열을 얻으려면 대신 [all](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
<!-- #### `toJson()` -->
#### `toJson()`

<!-- The `toJson` method converts the collection into a JSON serialized string: -->
`toJson` 메서드는 컬렉션을 JSON 직렬화된 문자열로 변환합니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-to-pretty-json"></a>
<!-- #### `toPrettyJson()` -->
#### `toPrettyJson()`

<!-- The `toPrettyJson` method converts the collection into a formatted JSON string using the `JSON_PRETTY_PRINT` option: -->
`toPrettyJson` 메서드는 `JSON_PRETTY_PRINT` 옵션을 사용하여 컬렉션을 형식이 지정된 JSON 문자열로 변환합니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toPrettyJson();
```

<a name="method-transform"></a>
<!-- #### `transform()` -->
#### `transform()`

<!-- The `transform` method iterates over the collection and calls the given callback with each item in the collection. The items in the collection will be replaced by the values returned by the callback: -->
`transform` 메서드는 컬렉션을 반복하고 컬렉션의 각 항목에 대해 지정된 콜백을 호출합니다. 컬렉션의 항목은 콜백에서 반환된 값으로 대체됩니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 다른 컬렉션 메서드와 달리 `transform`는 컬렉션 자체를 수정합니다. 대신 새 컬렉션을 생성하려면 [map](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
<!-- #### `undot()` -->
#### `undot()`

<!-- The `undot` method expands a single-dimensional collection that uses "dot" notation into a multi-dimensional collection: -->
`undot` 메서드는 "점" 표기법을 사용하는 1차원 컬렉션을 다차원 컬렉션으로 확장합니다.

```php
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
`union` 메서드는 주어진 배열을 컬렉션에 추가합니다. 주어진 배열에 원래 컬렉션에 이미 있는 키가 포함되어 있으면 원래 컬렉션의 값이 선호됩니다.

```php
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
<!-- #### `unique()` -->
#### `unique()`

<!-- The `unique` method returns all of the unique items in the collection. The returned collection keeps the original array keys, so in the following example we will use the [values](#method-values) method to reset the keys to consecutively numbered indexes: -->
`unique` 메서드는 컬렉션의 모든 고유 항목을 반환합니다. 반환된 컬렉션은 원래 배열 키를 유지하므로 다음 예에서는 [values](#method-values) 메서드를 사용하여 키를 연속 번호가 지정된 인덱스로 재설정합니다.

```php
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

<!-- When dealing with nested arrays or objects, you may specify the key used to determine uniqueness: -->
중첩된 배열이나 객체를 처리할 때 고유성을 결정하는 데 사용되는 키를 지정할 수 있습니다.

```php
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
마지막으로, 항목의 고유성을 결정해야 하는 값을 지정하기 위해 `unique` 메서드에 자체 클로저를 전달할 수도 있습니다.

```php
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

<!-- The `unique` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [uniqueStrict](#method-uniquestrict) method to filter using "strict" comparisons. -->
`unique` 메서드는 항목 값을 확인할 때 "느슨한" 비교를 사용합니다. 즉, 정수 값이 있는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다. "엄격한" 비교를 사용하여 필터링하려면 [uniqueStrict](#method-uniquestrict) 메서드를 사용하세요.

> [!NOTE]
> 이 메서드의 동작은 [Eloquent Collections](/docs/12.x/eloquent-collections#method-unique)을 사용할 때 수정됩니다.

<a name="method-uniquestrict"></a>
<!-- #### `uniqueStrict()` -->
#### `uniqueStrict()`

<!-- This method has the same signature as the [unique](#method-unique) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [unique](#method-unique) 메서드와 동일한 시그니처를 갖습니다. 그러나 모든 값은 "엄격한" 비교를 사용하여 비교됩니다.

<a name="method-unless"></a>
<!-- #### `unless()` -->
#### `unless()`

<!-- The `unless` method will execute the given callback unless the first argument given to the method evaluates to `true`. The collection instance and the first argument given to the `unless` method will be provided to the closure: -->
`unless` 메서드는 메서드에 제공된 첫 번째 인수가 `true`로 평가되지 않는 한 지정된 콜백을 실행합니다. `unless` 메서드에 제공된 컬렉션 인스턴스와 첫 번째 인수는 클로저에 제공됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
});

$collection->unless(false, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- A second callback may be passed to the `unless` method. The second callback will be executed when the first argument given to the `unless` method evaluates to `true`: -->
두 번째 콜백은 `unless` 메서드에 전달될 수 있습니다. 두 번째 콜백은 `unless` 메서드에 제공된 첫 번째 인수가 `true`로 평가될 때 실행됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
}, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- For the inverse of `unless`, see the [when](#method-when) method. -->
`unless`의 반대에 대해서는 [when](#method-when) 메서드를 참조하세요.

<a name="method-unlessempty"></a>
<!-- #### `unlessEmpty()` -->
#### `unlessEmpty()`

<!-- Alias for the [whenNotEmpty](#method-whennotempty) method. -->
[whenNotEmpty](#method-whennotempty) 메서드의 별칭입니다.

<a name="method-unlessnotempty"></a>
<!-- #### `unlessNotEmpty()` -->
#### `unlessNotEmpty()`

<!-- Alias for the [whenEmpty](#method-whenempty) method. -->
[whenEmpty](#method-whenempty) 메서드의 별칭입니다.

<a name="method-unwrap"></a>
<!-- #### `unwrap()` -->
#### `unwrap()`

<!-- The static `unwrap` method returns the collection's underlying items from the given value when applicable: -->
정적 `unwrap` 메서드는 해당되는 경우 주어진 값에서 컬렉션의 기본 항목을 반환합니다.

```php
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
`value` 메서드는 컬렉션의 첫 번째 요소에서 지정된 값을 검색합니다.

```php
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
`values` 메서드는 키가 연속된 정수로 재설정된 새 컬렉션을 반환합니다.

```php
$collection = collect([
    10 => ['product' => 'Desk', 'price' => 200],
    11 => ['product' => 'Speaker', 'price' => 400],
]);

$values = $collection->values();

$values->all();

/*
    [
        0 => ['product' => 'Desk', 'price' => 200],
        1 => ['product' => 'Speaker', 'price' => 400],
    ]
*/
```

<a name="method-when"></a>
<!-- #### `when()` -->
#### `when()`

<!-- The `when` method will execute the given callback when the first argument given to the method evaluates to `true`. The collection instance and the first argument given to the `when` method will be provided to the closure: -->
`when` 메서드는 메서드에 제공된 첫 번째 인수가 `true`로 평가될 때 지정된 콜백을 실행합니다. `when` 메서드에 제공된 컬렉션 인스턴스와 첫 번째 인수는 클로저에 제공됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->when(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
});

$collection->when(false, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 4]
```

<!-- A second callback may be passed to the `when` method. The second callback will be executed when the first argument given to the `when` method evaluates to `false`: -->
두 번째 콜백은 `when` 메서드에 전달될 수 있습니다. 두 번째 콜백은 `when` 메서드에 제공된 첫 번째 인수가 `false`로 평가될 때 실행됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->when(false, function (Collection $collection, bool $value) {
    return $collection->push(4);
}, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- For the inverse of `when`, see the [unless](#method-unless) method. -->
`when`의 반대에 대해서는 [unless](#method-unless) 메서드를 참조하세요.

<a name="method-whenempty"></a>
<!-- #### `whenEmpty()` -->
#### `whenEmpty()`

<!-- The `whenEmpty` method will execute the given callback when the collection is empty: -->
`whenEmpty` 메서드는 컬렉션이 비어 있을 때 지정된 콜백을 실행합니다.

```php
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
컬렉션이 비어 있지 않을 때 실행될 `whenEmpty` 메서드에 두 번째 클로저가 전달될 수 있습니다.

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Michael', 'Tom', 'Taylor']
```

<!-- For the inverse of `whenEmpty`, see the [whenNotEmpty](#method-whennotempty) method. -->
`whenEmpty`의 반대에 대해서는 [whenNotEmpty](#method-whennotempty) 메서드를 참조하세요.

<a name="method-whennotempty"></a>
<!-- #### `whenNotEmpty()` -->
#### `whenNotEmpty()`

<!-- The `whenNotEmpty` method will execute the given callback when the collection is not empty: -->
`whenNotEmpty` 메서드는 컬렉션이 비어 있지 않을 때 지정된 콜백을 실행합니다.

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom', 'Adam']

$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// []
```

<!-- A second closure may be passed to the `whenNotEmpty` method that will be executed when the collection is empty: -->
두 번째 클로저는 컬렉션이 비어 있을 때 실행될 `whenNotEmpty` 메서드에 전달될 수 있습니다.

```php
$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Taylor']
```

<!-- For the inverse of `whenNotEmpty`, see the [whenEmpty](#method-whenempty) method. -->
`whenNotEmpty`의 반대에 대해서는 [whenEmpty](#method-whenempty) 메서드를 참조하세요.

<a name="method-where"></a>
<!-- #### `where()` -->
#### `where()`

<!-- The `where` method filters the collection by a given key / value pair: -->
`where` 메서드는 주어진 키/값 쌍으로 컬렉션을 필터링합니다.

```php
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

<!-- The `where` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [whereStrict](#method-wherestrict) method to filter using "strict" comparisons, or the [whereNull](#method-wherenull) and [whereNotNull](#method-wherenotnull) methods to filter for `null` values. -->
`where` 메서드는 항목 값을 확인할 때 "느슨한" 비교를 사용합니다. 즉, 정수 값이 있는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다. "엄격한" 비교를 사용하여 필터링하려면 [whereStrict](#method-wherestrict) 메서드를 사용하고, `null` 값을 필터링하려면 [whereNull](#method-wherenull) 및 [whereNotNull](#method-wherenotnull) 메서드를 사용하세요.

<!-- Optionally, you may pass a comparison operator as the second parameter. Supported operators are: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', and '<=': -->
선택적으로 비교 연산자를 두 번째 매개변수로 전달할 수도 있습니다. 지원되는 연산자는 '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=' 및 '<='입니다.

```php
$collection = collect([
    ['name' => 'Jim', 'platform' => 'Mac'],
    ['name' => 'Sally', 'platform' => 'Mac'],
    ['name' => 'Sue', 'platform' => 'Linux'],
]);

$filtered = $collection->where('platform', '!=', 'Linux');

$filtered->all();

/*
    [
        ['name' => 'Jim', 'platform' => 'Mac'],
        ['name' => 'Sally', 'platform' => 'Mac'],
    ]
*/
```

<a name="method-wherestrict"></a>
<!-- #### `whereStrict()` -->
#### `whereStrict()`

<!-- This method has the same signature as the [where](#method-where) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [where](#method-where) 메서드와 동일한 서명을 갖습니다. 그러나 모든 값은 "엄격한" 비교를 사용하여 비교됩니다.

<a name="method-wherebetween"></a>
<!-- #### `whereBetween()` -->
#### `whereBetween()`

<!-- The `whereBetween` method filters the collection by determining if a specified item value is within a given range: -->
`whereBetween` 메서드는 지정된 항목 값이 지정된 범위 내에 있는지 확인하여 컬렉션을 필터링합니다.

```php
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
`whereIn` 메서드는 지정된 배열 내에 포함된 지정된 항목 값이 없는 컬렉션에서 요소를 제거합니다.

```php
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

<!-- The `whereIn` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [whereInStrict](#method-whereinstrict) method to filter using "strict" comparisons. -->
`whereIn` 메서드는 항목 값을 확인할 때 "느슨한" 비교를 사용합니다. 즉, 정수 값이 있는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다. "엄격한" 비교를 사용하여 필터링하려면 [whereInStrict](#method-whereinstrict) 메서드를 사용하세요.

<a name="method-whereinstrict"></a>
<!-- #### `whereInStrict()` -->
#### `whereInStrict()`

<!-- This method has the same signature as the [whereIn](#method-wherein) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [whereIn](#method-wherein) 메서드와 동일한 서명을 갖습니다. 그러나 모든 값은 "엄격한" 비교를 사용하여 비교됩니다.

<a name="method-whereinstanceof"></a>
<!-- #### `whereInstanceOf()` -->
#### `whereInstanceOf()`

<!-- The `whereInstanceOf` method filters the collection by a given class type: -->
`whereInstanceOf` 메서드는 주어진 클래스 유형으로 컬렉션을 필터링합니다.

```php
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
`whereNotBetween` 메서드는 지정된 항목 값이 지정된 범위를 벗어나는지 확인하여 컬렉션을 필터링합니다.

```php
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
`whereNotIn` 메서드는 지정된 배열 내에 포함된 지정된 항목 값이 있는 컬렉션에서 요소를 제거합니다.

```php
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

<!-- The `whereNotIn` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [whereNotInStrict](#method-wherenotinstrict) method to filter using "strict" comparisons. -->
`whereNotIn` 메서드는 항목 값을 확인할 때 "느슨한" 비교를 사용합니다. 즉, 정수 값이 있는 문자열은 동일한 값의 정수와 동일한 것으로 간주됩니다. "엄격한" 비교를 사용하여 필터링하려면 [whereNotInStrict](#method-wherenotinstrict) 메서드를 사용하세요.

<a name="method-wherenotinstrict"></a>
<!-- #### `whereNotInStrict()` -->
#### `whereNotInStrict()`

<!-- This method has the same signature as the [whereNotIn](#method-wherenotin) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [whereNotIn](#method-wherenotin) 메서드와 동일한 서명을 갖습니다. 그러나 모든 값은 "엄격한" 비교를 사용하여 비교됩니다.

<a name="method-wherenotnull"></a>
<!-- #### `whereNotNull()` -->
#### `whereNotNull()`

<!-- The `whereNotNull` method returns items from the collection where the given key is not `null`: -->
`whereNotNull` 메서드는 주어진 키가 `null`가 아닌 컬렉션에서 항목을 반환합니다.

```php
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
    ['name' => 0],
    ['name' => ''],
]);

$filtered = $collection->whereNotNull('name');

$filtered->all();

/*
    [
        ['name' => 'Desk'],
        ['name' => 'Bookcase'],
        ['name' => 0],
        ['name' => ''],
    ]
*/
```

<a name="method-wherenull"></a>
<!-- #### `whereNull()` -->
#### `whereNull()`

<!-- The `whereNull` method returns items from the collection where the given key is `null`: -->
`whereNull` 메서드는 지정된 키가 `null`인 컬렉션에서 항목을 반환합니다.

```php
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
    ['name' => 0],
    ['name' => ''],
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
정적 `wrap` 메서드는 해당되는 경우 컬렉션에 지정된 값을 래핑합니다.

```php
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
`zip` 메서드는 주어진 배열의 값을 해당 인덱스에 있는 원본 컬렉션의 값과 함께 병합합니다.

```php
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
<!-- ## Higher Order Messages -->
## Higher Order Messages

<!-- Collections also provide support for "higher order messages", which are short-cuts for performing common actions on collections. The collection methods that provide higher order messages are: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), and [unique](#method-unique). -->
컬렉션은 컬렉션에 대한 일반적인 작업을 수행하기 위한 바로 가기인 "고차 메시지"에 대한 지원도 제공합니다. 고차 메시지를 제공하는 컬렉션 메서드는 다음과 같습니다: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile) 및 [unique](#method-unique).

<!-- Each higher order message can be accessed as a dynamic property on a collection instance. For instance, let's use the `each` higher order message to call a method on each object within a collection: -->
각 고차 메시지는 컬렉션 인스턴스의 동적 속성으로 액세스할 수 있습니다. 예를 들어 `each` 고차 메시지를 사용하여 컬렉션 내의 각 개체에 대한 메서드를 호출해 보겠습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

<!-- Likewise, we can use the `sum` higher order message to gather the total number of "votes" for a collection of users: -->
마찬가지로 `sum` 고차 메시지를 사용하여 사용자 모음에 대한 총 "투표" 수를 수집할 수 있습니다.

```php
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
> Laravel의 Lazy 컬렉션에 대해 자세히 알아보기 전에 시간을 내어 [PHP generators](https://www.php.net/manual/en/language.generators.overview.php)에 익숙해지세요.

<!-- To supplement the already powerful `Collection` class, the `LazyCollection` class leverages PHP's [generators](https://www.php.net/manual/en/language.generators.overview.php) to allow you to work with very large datasets while keeping memory usage low. -->
이미 강력한 `Collection` 클래스를 보완하기 위해 `LazyCollection` 클래스는 PHP의 [generators](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여 메모리 사용량을 낮게 유지하면서 매우 큰 데이터 세트로 작업할 수 있도록 해줍니다.

<!-- For example, imagine your application needs to process a multi-gigabyte log file while taking advantage of Laravel's collection methods to parse the logs. Instead of reading the entire file into memory at once, lazy collections may be used to keep only a small part of the file in memory at a given time: -->
예를 들어, 애플리케이션이 로그를 구문 분석하기 위해 Laravel의 컬렉션 메서드를 활용하면서 멀티 기가바이트 로그 파일을 처리해야 한다고 가정해 보세요. 전체 파일을 한 번에 메모리로 읽는 대신, 지정된 시간에 파일의 작은 부분만 메모리에 유지하기 위해 지연 컬렉션을 사용할 수 있습니다.

```php
use App\Models\LogEntry;
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }

    fclose($handle);
})->chunk(4)->map(function (array $lines) {
    return LogEntry::fromLines($lines);
})->each(function (LogEntry $logEntry) {
    // Process the log entry...
});
```

<!-- Or, imagine you need to iterate through 10,000 Eloquent models. When using traditional Laravel collections, all 10,000 Eloquent models must be loaded into memory at the same time: -->
또는 10,000 Eloquent 모델을 반복해야 한다고 상상해 보세요. 기존 Laravel 컬렉션을 사용하는 경우 10,000개의 Eloquent 모델이 모두 동시에 메모리에 로드되어야 합니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

<!-- However, the query builder's `cursor` method returns a `LazyCollection` instance. This allows you to still only run a single query against the database but also only keep one Eloquent model loaded in memory at a time. In this example, the `filter` callback is not executed until we actually iterate over each user individually, allowing for a drastic reduction in memory usage: -->
그러나 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 통해 데이터베이스에 대해 단일 쿼리만 실행할 수 있을 뿐만 아니라 한 번에 하나의 Eloquent 모델만 메모리에 로드된 상태로 유지할 수 있습니다. 이 예에서 `filter` 콜백은 실제로 각 사용자를 개별적으로 반복할 때까지 실행되지 않으므로 메모리 사용량이 크게 줄어듭니다.

```php
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
지연 컬렉션 인스턴스를 생성하려면 PHP 생성기 함수를 컬렉션의 `make` 메서드에 전달해야 합니다.

```php
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }

    fclose($handle);
});
```

<a name="the-enumerable-contract"></a>
<!-- ### The Enumerable Contract -->
### The Enumerable Contract

<!-- Almost all methods available on the `Collection` class are also available on the `LazyCollection` class. Both of these classes implement the `Illuminate\Support\Enumerable` contract, which defines the following methods: -->
`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 이 두 클래스는 모두 다음 메서드를 정의하는 `Illuminate\Support\Enumerable` 컨트랙트를 구현합니다.

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
> 컬렉션을 변경하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서 사용할 수 **없습니다**.

<a name="lazy-collection-methods"></a>
<!-- ### Lazy Collection Methods -->
### Lazy Collection Methods

<!-- In addition to the methods defined in the `Enumerable` contract, the `LazyCollection` class contains the following methods: -->
`Enumerable` 컨트랙트에 정의된 메서드 외에도 `LazyCollection` 클래스에는 다음 메서드가 포함되어 있습니다.

<a name="method-takeUntilTimeout"></a>
<!-- #### `takeUntilTimeout()` -->
#### `takeUntilTimeout()`

<!-- The `takeUntilTimeout` method returns a new lazy collection that will enumerate values until the specified time. After that time, the collection will then stop enumerating: -->
`takeUntilTimeout` 메서드는 지정된 시간까지 값을 열거하는 새로운 지연 컬렉션을 반환합니다. 그 이후에는 컬렉션의 열거가 중지됩니다.

```php
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->plus(minutes: 1));

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

<!-- To illustrate the usage of this method, imagine an application that submits invoices from the database using a cursor. You could define a [scheduled task](/docs/12.x/scheduling) that runs every 15 minutes and only processes invoices for a maximum of 14 minutes: -->
이 메서드의 사용법을 설명하기 위해 커서를 사용하여 데이터베이스에서 송장을 제출하는 애플리케이션을 상상해 보십시오. 15분마다 실행되고 최대 14분 동안만 송장을 처리하는 [scheduled task](/docs/12.x/scheduling)을 정의할 수 있습니다.

```php
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
`each` 메서드는 컬렉션의 각 항목에 대해 지정된 콜백을 즉시 호출하는 반면, `tapEach` 메서드는 항목이 목록에서 하나씩 제거될 때 지정된 콜백만 호출합니다.

```php
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
`throttle` 메서드는 지정된 시간(초) 후에 각 값이 반환되도록 지연 컬렉션을 조절합니다. 이 메서드는 들어오는 요청의 속도를 제한하는 외부 API와 상호 작용할 수 있는 상황에 특히 유용합니다.

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
`remember` 메서드는 이미 열거된 모든 값을 기억하고 후속 컬렉션 열거에서 해당 값을 다시 검색하지 않는 새로운 지연 컬렉션을 반환합니다.

```php
// No query has been executed yet...
$users = User::cursor()->remember();

// The query is executed...
// The first 5 users are hydrated from the database...
$users->take(5)->all();

// First 5 users come from the collection's cache...
// The rest are hydrated from the database...
$users->take(20)->all();
```

<a name="method-with-heartbeat"></a>
<!-- #### `withHeartbeat()` -->
#### `withHeartbeat()`

<!-- The `withHeartbeat` method allows you to execute a callback at regular time intervals while a lazy collection is being enumerated. This is particularly useful for long-running operations that require periodic maintenance tasks, such as extending locks or sending progress updates: -->
`withHeartbeat` 메서드를 사용하면 지연 컬렉션이 열거되는 동안 정기적인 시간 간격으로 콜백을 실행할 수 있습니다. 이는 잠금 확장 또는 진행률 업데이트 전송과 같이 정기적인 유지 관리 작업이 필요한 장기 실행 작업에 특히 유용합니다.

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('generate-reports', seconds: 60 * 5);

if ($lock->get()) {
    try {
        Report::where('status', 'pending')
            ->lazy()
            ->withHeartbeat(
                CarbonInterval::minutes(4),
                fn () => $lock->extend(CarbonInterval::minutes(5))
            )
            ->each(fn ($report) => $report->process());
    } finally {
        $lock->release();
    }
}
```
