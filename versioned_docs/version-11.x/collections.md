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
`Illuminate\Support\Collection` 클래스는 데이터 배열을 처리할 때 유연하고 편리한 래퍼를 제공합니다. 아래 예제를 확인해 보세요. `collect` 헬퍼를 사용해 배열로부터 새로운 컬렉션 인스턴스를 생성한 후, 각 요소에 `strtoupper` 함수를 적용하고 모든 비어 있는 요소를 제거해 보겠습니다:

```
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

<!-- As you can see, the `Collection` class allows you to chain its methods to perform fluent mapping and reducing of the underlying array. In general, collections are immutable, meaning every `Collection` method returns an entirely new `Collection` instance. -->
이처럼 `Collection` 클래스는 메서드 체이닝을 통해 기본 배열에 대해 연속적으로 매핑과 필터링 같은 동작을 부드럽게 수행할 수 있도록 해줍니다. 일반적으로 컬렉션은 불변(immutable) 객체이므로, 각 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
<!-- ### Creating Collections -->
### Creating Collections

<!-- As mentioned above, the `collect` helper returns a new `Illuminate\Support\Collection` instance for the given array. So, creating a collection is as simple as: -->
위에서 언급한 것처럼, `collect` 헬퍼는 전달받은 배열로부터 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 즉, 컬렉션을 생성하는 방법은 매우 간단합니다:

```
$collection = collect([1, 2, 3]);
```

> [!NOTE]
> [Eloquent](/docs/11.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
<!-- ### Extending Collections -->
### Extending Collections

<!-- Collections are "macroable", which allows you to add additional methods to the `Collection` class at run time. The `Illuminate\Support\Collection` class' `macro` method accepts a closure that will be executed when your macro is called. The macro closure may access the collection's other methods via `$this`, just as if it were a real method of the collection class. For example, the following code adds a `toUpper` method to the `Collection` class: -->
컬렉션은 "매크로(macro) 가능"하므로, 실행 중에 `Collection` 클래스에 원하는 메서드를 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행될 클로저를 인수로 받습니다. 매크로 클로저에서는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있으며, 마치 컬렉션 클래스의 진짜 메서드처럼 사용할 수 있습니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper`라는 메서드를 추가합니다:

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
일반적으로, 컬렉션 매크로는 [service provider](/docs/11.x/providers)의 `boot` 메서드에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
<!-- #### Macro Arguments -->
#### Macro Arguments

<!-- If necessary, you may define macros that accept additional arguments: -->
필요하다면, 추가 인수를 받는 매크로도 정의할 수 있습니다:

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
남은 컬렉션 문서에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 하나씩 다룹니다. 이 모든 메서드들은 체이닝이 가능하므로, 기본 배열을 연속적으로 다루는 데 매우 유용합니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요하다면 원본 컬렉션을 그대로 보존할 수 있습니다.



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
`after` 메서드는 주어진 값 바로 뒤에 오는 아이템을 반환합니다. 만약 주어진 값이 컬렉션에 없거나 마지막 아이템일 경우 `null`을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

<!-- This method searches for the given item using "loose" comparison, meaning a string containing an integer value will be considered equal to an integer of the same value. To use "strict" comparison, you may provide the `strict` argument to the method: -->
이 메서드는 "느슨한(loose)" 비교를 이용하여 값을 찾기 때문에, 정수 값을 가진 문자열도 같은 숫자의 정수와 같다고 간주합니다. "엄격한(strict)" 비교를 사용하려면 `strict` 인수를 추가할 수 있습니다:

```
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

<!-- Alternatively, you may provide your own closure to search for the first item that passes a given truth test: -->
또는, 자신만의 클로저를 전달하여 특정 조건을 만족하는 첫 번째 아이템을 찾을 수도 있습니다:

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
`all` 메서드는 컬렉션이 내부적으로 표현하는 원본 배열을 반환합니다:

```
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
<!-- #### `average()` -->
#### `average()`

<!-- Alias for the [`avg`](#method-avg) method. -->
[`avg`](#method-avg) 메서드의 별칭입니다.

<a name="method-avg"></a>
<!-- #### `avg()` -->
#### `avg()`

<!-- The `avg` method returns the [average value](https://en.wikipedia.org/wiki/Average) of a given key: -->
`avg` 메서드는 특정 키의 [average value](https://en.wikipedia.org/wiki/Average)을 반환합니다:

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
`before` 메서드는 [`after`](#method-after) 메서드의 반대 동작을 합니다. 주어진 값 바로 앞에 오는 아이템을 반환하며, 주어진 값이 컬렉션에 없거나 첫 번째 아이템일 경우 `null`을 반환합니다:

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
`chunk` 메서드는 컬렉션을 지정한 크기만큼의 작은 컬렉션으로 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

<!-- This method is especially useful in [views](/docs/11.x/views) when working with a grid system such as [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/). For example, imagine you have a collection of [Eloquent](/docs/11.x/eloquent) models you want to display in a grid: -->
이 메서드는 [views](/docs/11.x/views)에서 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/)과 같은 그리드 시스템을 사용할 때 특히 유용합니다. 예를 들어, 그리드로 보여주고 싶은 [Eloquent](/docs/11.x/eloquent) 모델 컬렉션이 있다고 할 때 다음과 같이 활용할 수 있습니다:

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
`chunkWhile` 메서드는 전달한 콜백의 평가 결과에 따라 컬렉션을 여러 개의 작은 컬렉션으로 나눕니다. 클로저에 전달되는 `$chunk` 변수로 이전 요소를 확인할 수 있습니다:

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
`collapse` 메서드는 여러 배열로 구성된 컬렉션을 하나의 단일 평면(flat) 컬렉션으로 펼쳐줍니다:

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
`collapseWithKeys` 메서드는 배열 또는 컬렉션으로 이루어진 컬렉션을, 각 원래의 키를 그대로 유지하면서 하나의 컬렉션으로 평탄화합니다:

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
`collect` 메서드는 현재 컬렉션에 담겨 있는 값들로 새로운 `Collection` 인스턴스를 반환합니다:

```
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

<!-- The `collect` method is primarily useful for converting [lazy collections](#lazy-collections) into standard `Collection` instances: -->
`collect` 메서드는 주로 [lazy collections](#lazy-collections)을 일반적인 `Collection` 인스턴스로 변환할 때 유용합니다:

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
> `collect` 메서드는 `Enumerable` 인스턴스를 보통 컬렉션 인스턴스로 전환할 필요가 있을 때 매우 유용합니다. `collect()`는 `Enumerable` 계약의 일부이므로, 언제든 안심하고 `Collection` 인스턴스를 얻는데 사용할 수 있습니다.

<a name="method-combine"></a>
<!-- #### `combine()` -->
#### `combine()`

<!-- The `combine` method combines the values of the collection, as keys, with the values of another array or collection: -->
`combine` 메서드는 컬렉션의 값들을 키로, 전달한 또 다른 배열 또는 컬렉션의 값들을 값으로 결합합니다:

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
`concat` 메서드는 주어진 `array` 또는 컬렉션의 값을 기존 컬렉션의 끝에 덧붙여 추가합니다:

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

<!-- The `concat` method numerically reindexes keys for items concatenated onto the original collection. To maintain keys in associative collections, see the [merge](#method-merge) method. -->
`concat` 메서드는 추가된 요소들의 키를 숫자형으로 새로 부여합니다. 연관 배열(associative collection)의 키를 그대로 유지하고 싶다면 [merge](#method-merge) 메서드를 사용하세요.

<a name="method-contains"></a>
<!-- #### `contains()` -->
#### `contains()`

<!-- The `contains` method determines whether the collection contains a given item. You may pass a closure to the `contains` method to determine if an element exists in the collection matching a given truth test: -->
`contains` 메서드는 컬렉션이 특정 아이템을 포함하는지 여부를 확인합니다. `contains` 메서드에 클로저를 전달해, 주어진 조건을 만족하는 요소가 컬렉션에 존재하는지 확인할 수 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `contains` method to determine whether the collection contains a given item value: -->
또는, `contains` 메서드에 문자열을 전달하여 해당 값이 컬렉션에 존재하는지 확인할 수도 있습니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

<!-- You may also pass a key / value pair to the `contains` method, which will determine if the given pair exists in the collection: -->
`contains` 메서드에 키/값 쌍을 넘겨, 해당 조합이 컬렉션에 존재하는지 검사할 수도 있습니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

<!-- The `contains` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [`containsStrict`](#method-containsstrict) method to filter using "strict" comparisons. -->
`contains` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 숫자의 문자열도 같은 값을 가진 정수와 동일하게 판단합니다. "엄격한(strict)" 비교로 필터링하려면 [`containsStrict`](#method-containsstrict) 메서드를 참고하세요.

<!-- For the inverse of `contains`, see the [doesntContain](#method-doesntcontain) method. -->
`contains`의 반대 동작은 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsoneitem"></a>
<!-- #### `containsOneItem()` -->
#### `containsOneItem()`

<!-- The `containsOneItem` method determines whether the collection contains a single item: -->
`containsOneItem` 메서드는 컬렉션에 단 하나의 요소만 존재하는지 확인합니다:

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
이 메서드는 [`contains`](#method-contains) 메서드와 동일한 시그니처를 가집니다. 그러나 모든 값은 "엄격(strict)" 비교를 통해 비교됩니다.

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/11.x/eloquent-collections#method-contains)을 사용할 때 동작이 달라집니다.

<a name="method-count"></a>
<!-- #### `count()` -->
#### `count()`

<!-- The `count` method returns the total number of items in the collection: -->
`count` 메서드는 컬렉션의 전체 항목 개수를 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
<!-- #### `countBy()` -->
#### `countBy()`

<!-- The `countBy` method counts the occurrences of values in the collection. By default, the method counts the occurrences of every element, allowing you to count certain "types" of elements in the collection: -->
`countBy` 메서드는 컬렉션 내 값들의 등장 횟수를 셉니다. 기본적으로 컬렉션의 각 요소가 몇 번씩 등장하는지 세어주므로, 특정 "유형"의 항목이 몇 개인지 파악할 수 있습니다.

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

<!-- You pass a closure to the `countBy` method to count all items by a custom value: -->
`countBy` 메서드에 클로저를 전달하여, 사용자 정의 값으로 각 항목의 개수를 셀 수도 있습니다.

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
`crossJoin` 메서드는 컬렉션의 값들을 주어진 배열이나 컬렉션과 크로스 조인하여, 가능한 모든 조합(카티션 곱, Cartesian product)을 반환합니다.

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
`dd` 메서드는 컬렉션의 항목을 출력(dump)한 뒤 스크립트 실행을 중단합니다.

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
스크립트 실행을 중단하지 않고 컬렉션을 출력만 하려면 [`dump`](#method-dump) 메서드를 사용하십시오.

<a name="method-diff"></a>
<!-- #### `diff()` -->
#### `diff()`

<!-- The `diff` method compares the collection against another collection or a plain PHP `array` based on its values. This method will return the values in the original collection that are not present in the given collection: -->
`diff` 메서드는 컬렉션과 다른 컬렉션 또는 일반 PHP `array`를 값 기준으로 비교합니다. 이 메서드는 기준 컬렉션에 존재하지 않는 원래 컬렉션의 값을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/11.x/eloquent-collections#method-diff)을 사용할 때 동작이 달라집니다.

<a name="method-diffassoc"></a>
<!-- #### `diffAssoc()` -->
#### `diffAssoc()`

<!-- The `diffAssoc` method compares the collection against another collection or a plain PHP `array` based on its keys and values. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffAssoc` 메서드는 컬렉션과 다른 컬렉션 또는 일반 PHP `array`를 '키와 값' 기준으로 비교합니다. 이때, 기준 컬렉션에 존재하지 않는 원래 컬렉션의 키/값 쌍을 반환합니다.

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
`diffAssoc`와 달리, `diffAssocUsing` 메서드는 인덱스(키) 비교에 직접 지정한 콜백 함수를 사용합니다.

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
콜백 함수는, 비교 대상이 기준보다 작으면 0보다 작은 정수, 기준과 같으면 0, 크면 0보다 큰 정수를 반환하는 함수여야 합니다. 자세한 정보는 PHP의 [`array_diff_uassoc`](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) 설명서를 참고해 주세요. `diffAssocUsing` 메서드는 내부적으로 해당 PHP 함수를 사용합니다.

<a name="method-diffkeys"></a>
<!-- #### `diffKeys()` -->
#### `diffKeys()`

<!-- The `diffKeys` method compares the collection against another collection or a plain PHP `array` based on its keys. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffKeys` 메서드는 컬렉션과 다른 컬렉션 또는 일반 PHP `array`를 키 기준으로 비교합니다. 이때, 기준 컬렉션에 존재하지 않는 원래 컬렉션의 키/값 쌍을 반환합니다.

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
`doesntContain` 메서드는 컬렉션에 특정 값이 없는지 검사합니다. `doesntContain` 메서드에 클로저를 전달하면, 해당 조건을 만족하는 요소가 컬렉션에 '존재하지 않는지' 확인할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `doesntContain` method to determine whether the collection does not contain a given item value: -->
또는, `doesntContain` 메서드에 문자열을 전달하여 해당 값이 컬렉션에 없는지 확인할 수 있습니다.

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

<!-- You may also pass a key / value pair to the `doesntContain` method, which will determine if the given pair does not exist in the collection: -->
`doesntContain` 메서드에 키/값 쌍을 전달하여, 해당 키/값 쌍이 컬렉션에 없는지 검사할 수도 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

<!-- The `doesntContain` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. -->
`doesntContain` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 정수로 변환 가능한 문자열은 같은 정수로 간주하여 일치하는 것으로 처리합니다.

<a name="method-dot"></a>
<!-- #### `dot()` -->
#### `dot()`

<!-- The `dot` method flattens a multi-dimensional collection into a single level collection that uses "dot" notation to indicate depth: -->
`dot` 메서드는 다차원 컬렉션을 단일 단계의 컬렉션으로 평탄화하며, 깊이(depth)를 "닷(dot) 표기법"으로 표시합니다.

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
`dump` 메서드는 컬렉션의 항목을 출력(dump)합니다.

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
컬렉션을 출력한 후 스크립트 실행을 중단하고 싶다면 [`dd`](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
<!-- #### `duplicates()` -->
#### `duplicates()`

<!-- The `duplicates` method retrieves and returns duplicate values from the collection: -->
`duplicates` 메서드는 컬렉션 내에서 중복된 값을 찾아 반환합니다.

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

<!-- If the collection contains arrays or objects, you can pass the key of the attributes that you wish to check for duplicate values: -->
컬렉션에 배열이나 객체가 포함되어 있을 경우, 중복 여부를 확인할 속성의 키를 지정하여 사용할 수 있습니다.

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
이 메서드는 [`duplicates`](#method-duplicates) 메서드와 동일한 시그니처를 가집니다. 그러나 모든 값은 "엄격(strict)" 비교를 통해 중복 여부를 판단합니다.

<a name="method-each"></a>
<!-- #### `each()` -->
#### `each()`

<!-- The `each` method iterates over the items in the collection and passes each item to a closure: -->
`each` 메서드는 컬렉션의 항목을 순회하며, 각 항목을 클로저에 전달합니다.

```
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

<!-- If you would like to stop iterating through the items, you may return `false` from your closure: -->
순회를 중단하고 싶을 때는, 클로저에서 `false`를 반환하면 해당 지점에서 순회가 멈춥니다.

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
`eachSpread` 메서드는 컬렉션의 항목(배열 형태)을 펼쳐서(closing unpacking) 각각의 값들을 콜백에 전달하며 순회합니다.

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

<!-- You may stop iterating through the items by returning `false` from the callback: -->
이 역시 콜백에서 `false`를 반환하면 순회가 중단됩니다.

```
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
<!-- #### `ensure()` -->
#### `ensure()`

<!-- The `ensure` method may be used to verify that all elements of a collection are of a given type or list of types. Otherwise, an `UnexpectedValueException` will be thrown: -->
`ensure` 메서드는 컬렉션의 모든 요소가 지정한 타입 또는 타입 목록에 해당하는지 검사합니다. 그렇지 않을 경우 `UnexpectedValueException` 예외가 발생합니다.

```
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

<!-- Primitive types such as `string`, `int`, `float`, `bool`, and `array` may also be specified: -->
기본 타입인 `string`, `int`, `float`, `bool`, `array` 등도 지정할 수 있습니다.

```
return $collection->ensure('int');
```

> [!WARNING]
> `ensure` 메서드는 나중에 컬렉션에 다른 타입의 요소가 추가되는 것을 방지해주지는 않습니다.

<a name="method-every"></a>
<!-- #### `every()` -->
#### `every()`

<!-- The `every` method may be used to verify that all elements of a collection pass a given truth test: -->
`every` 메서드는 컬렉션의 모든 요소가 주어진 조건을 만족하는지 검사할 때 사용합니다.

```
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

<!-- If the collection is empty, the `every` method will return true: -->
컬렉션이 비어 있는 경우 `every` 메서드는 true를 반환합니다.

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
`except` 메서드는 지정한 키를 가진 항목을 제외한 컬렉션의 모든 항목을 반환합니다.

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

<!-- For the inverse of `except`, see the [only](#method-only) method. -->
`except`의 반대 동작은 [only](#method-only) 메서드를 참고하세요.

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/11.x/eloquent-collections#method-except)을 사용할 때 동작이 달라집니다.

<a name="method-filter"></a>
<!-- #### `filter()` -->
#### `filter()`

<!-- The `filter` method filters the collection using the given callback, keeping only those items that pass a given truth test: -->
`filter` 메서드는 주어진 콜백 함수를 통해 컬렉션의 항목을 필터링하여, 조건을 만족하는 항목만 남깁니다.

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

<!-- If no callback is supplied, all entries of the collection that are equivalent to `false` will be removed: -->
콜백을 지정하지 않으면, 컬렉션에서 `false`로 평가되는 모든 값이 제거됩니다.

```
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

<!-- For the inverse of `filter`, see the [reject](#method-reject) method. -->
`filter`의 반대 동작은 [reject](#method-reject) 메서드를 참고하세요.

<a name="method-first"></a>
<!-- #### `first()` -->
#### `first()`

<!-- The `first` method returns the first element in the collection that passes a given truth test: -->
`first` 메서드는 컬렉션의 각 항목 중 지정한 조건을 만족하는 첫 번째 항목을 반환합니다.

```
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

<!-- You may also call the `first` method with no arguments to get the first element in the collection. If the collection is empty, `null` is returned: -->
인수를 전달하지 않고 `first` 메서드를 호출하면, 컬렉션의 첫 번째 항목을 반환합니다. 컬렉션이 비어 있으면 `null`을 반환합니다.

```
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
<!-- #### `firstOrFail()` -->
#### `firstOrFail()`

<!-- The `firstOrFail` method is identical to the `first` method; however, if no result is found, an `Illuminate\Support\ItemNotFoundException` exception will be thrown: -->
`firstOrFail` 메서드는 `first` 메서드와 사용법이 동일하나, 조건을 만족하는 결과가 없을 경우 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// Throws ItemNotFoundException...
```

<!-- You may also call the `firstOrFail` method with no arguments to get the first element in the collection. If the collection is empty, an `Illuminate\Support\ItemNotFoundException` exception will be thrown: -->
인수를 전달하지 않고 `firstOrFail` 메서드를 호출하면, 컬렉션의 첫 번째 항목을 반환합니다. 컬렉션이 비어 있으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```
collect([])->firstOrFail();

// Throws ItemNotFoundException...
```

<a name="method-first-where"></a>
<!-- #### `firstWhere()` -->
#### `firstWhere()`

<!-- The `firstWhere` method returns the first element in the collection with the given key / value pair: -->
`firstWhere` 메서드는 지정한 키/값 쌍과 일치하는 컬렉션 내 첫 번째 항목을 반환합니다.

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
`firstWhere` 메서드는 비교 연산자와 함께 호출할 수도 있습니다.

```
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

<!-- Like the [where](#method-where) method, you may pass one argument to the `firstWhere` method. In this scenario, the `firstWhere` method will return the first item where the given item key's value is "truthy": -->
[where](#method-where) 메서드처럼 `firstWhere` 메서드에 인수 하나만 전달할 수도 있습니다. 이 경우 `firstWhere` 메서드는 해당 키가 'truthy' 값(즉, 참으로 평가되는 값)을 가진 첫 번째 항목을 반환합니다.

```
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
<!-- #### `flatMap()` -->
#### `flatMap()`

<!-- The `flatMap` method iterates through the collection and passes each value to the given closure. The closure is free to modify the item and return it, thus forming a new collection of modified items. Then, the array is flattened by one level: -->
`flatMap` 메서드는 컬렉션의 각 값을 주어진 클로저에 전달하여 변형하고, 변형된 결과로 새로운 컬렉션을 만듭니다. 그 후에, 반환된 배열이 한 단계 평탄화됩니다.

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
`flatten` 메서드는 다차원 컬렉션을 한 단계의 단일 컬렉션으로 평탄화합니다.

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
필요하다면 `flatten` 메서드에 "깊이(depth)" 인수를 전달할 수도 있습니다.

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
이 예시에서, 깊이 인수를 생략하고 `flatten`을 호출하면 중첩 배열까지 모두 평탄화되어 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`가 됩니다. 깊이를 지정하면 몇 단계까지 평탄화할지 직접 선택할 수 있습니다.

<a name="method-flip"></a>

<!-- #### `flip()` -->
#### `flip()`

<!-- The `flip` method swaps the collection's keys with their corresponding values: -->
`flip` 메서드는 컬렉션의 키와 값을 서로 뒤바꿉니다.

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
`forget` 메서드는 컬렉션에서 지정한 키에 해당하는 아이템을 제거합니다.

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
> 대부분의 다른 컬렉션 메서드와 달리, `forget`은 새로운 컬렉션을 반환하지 않고, 호출된 컬렉션 자체를 수정합니다.

<a name="method-forpage"></a>
<!-- #### `forPage()` -->
#### `forPage()`

<!-- The `forPage` method returns a new collection containing the items that would be present on a given page number. The method accepts the page number as its first argument and the number of items to show per page as its second argument: -->
`forPage` 메서드는 지정한 페이지 번호에 해당하는 아이템만 포함하는 새로운 컬렉션을 반환합니다. 첫 번째 인수로 페이지 번호를, 두 번째 인수로 한 페이지에 보여줄 아이템 개수를 전달할 수 있습니다.

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
`get` 메서드는 지정한 키에 해당하는 아이템을 반환합니다. 키가 존재하지 않으면 `null`을 반환합니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

<!-- You may optionally pass a default value as the second argument: -->
두 번째 인수로 기본값을 전달할 수도 있습니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('age', 34);

// 34
```

<!-- You may even pass a callback as the method's default value. The result of the callback will be returned if the specified key does not exist: -->
기본값으로 콜백을 전달할 수도 있습니다. 만약 지정한 키가 존재하지 않으면, 해당 콜백의 결과가 반환됩니다.

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
`groupBy` 메서드는 컬렉션의 아이템을 지정한 키로 그룹화합니다.

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
문자열 `key` 대신 콜백을 전달할 수도 있습니다. 콜백은 그룹의 키로 사용할 값을 반환해야 합니다.

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
여러 개의 그룹화 기준을 배열로 전달할 수도 있습니다. 배열의 각 요소는 다차원 배열의 각 단계에 적용됩니다.

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
`has` 메서드는 컬렉션에 지정한 키가 존재하는지 여부를 확인합니다.

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
`hasAny` 메서드는 전달한 키들 중 하나라도 컬렉션에 존재하는지 확인합니다.

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
`implode` 메서드는 컬렉션의 아이템을 연결하여 하나의 문자열로 만듭니다. 컬렉션이 배열이나 객체를 포함하는 경우, 연결할 속성의 키와 각 값을 이어붙일 구분자(Glue)를 인수로 전달해야 합니다.

```
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// Desk, Chair
```

<!-- If the collection contains simple strings or numeric values, you should pass the "glue" as the only argument to the method: -->
컬렉션이 단순 문자열이나 숫자 값만 포함한다면, 구분자만 인수로 전달하면 됩니다.

```
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

<!-- You may pass a closure to the `implode` method if you would like to format the values being imploded: -->
`implode` 메서드에 클로저를 전달해 각 값을 원하는 방식으로 가공한 뒤 연결할 수도 있습니다.

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
`intersect` 메서드는 원본 컬렉션에 존재하지 않는 값을 모두 제거합니다. 즉, 주어진 `array` 또는 컬렉션에 포함된 값만 남게 됩니다. 결과 컬렉션은 원본 컬렉션의 키를 그대로 유지합니다.

```
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/11.x/eloquent-collections#method-intersect)을 사용할 때 동작이 다를 수 있습니다.

<a name="method-intersectusing"></a>
<!-- #### `intersectUsing()` -->
#### `intersectUsing()`

<!-- The `intersectUsing` method removes any values from the original collection that are not present in the given `array` or collection, using a custom callback to compare the values. The resulting collection will preserve the original collection's keys: -->
`intersectUsing` 메서드는 주어진 `array` 또는 컬렉션에 포함되어 있지 않은 값들을 제거하지만, 값 비교 시 사용자가 정의한 콜백을 사용합니다. 결과 컬렉션은 원본 컬렉션의 키를 그대로 유지합니다.

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
`intersectAssoc` 메서드는 원본 컬렉션과 비교 대상 컬렉션 또는 `array` 모두에 존재하는 키/값 쌍만 반환합니다.

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
`intersectAssocUsing` 메서드는 원본 컬렉션과 비교 대상 컬렉션 또는 `array` 모두에 존재하는 키/값 쌍만 반환하되, 각 키와 값의 비교에 사용자 정의 콜백을 사용합니다.

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
`intersectByKeys` 메서드는 주어진 `array` 또는 컬렉션에 존재하지 않는 키와 그에 대응하는 값을 모두 제거합니다.

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
`isEmpty` 메서드는 컬렉션이 비어 있으면 `true`, 그렇지 않으면 `false`를 반환합니다.

```
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
<!-- #### `isNotEmpty()` -->
#### `isNotEmpty()`

<!-- The `isNotEmpty` method returns `true` if the collection is not empty; otherwise, `false` is returned: -->
`isNotEmpty` 메서드는 컬렉션이 비어 있지 않으면 `true`, 비어 있으면 `false`를 반환합니다.

```
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
<!-- #### `join()` -->
#### `join()`

<!-- The `join` method joins the collection's values with a string. Using this method's second argument, you may also specify how the final element should be appended to the string: -->
`join` 메서드는 컬렉션의 값을 특정 문자열로 연결합니다. 두 번째 인수를 사용하면 마지막 요소를 어떻게 붙일지 지정할 수 있습니다.

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
`keyBy` 메서드는 지정한 키를 기준으로 컬렉션의 키를 재설정합니다. 동일한 키가 여러 번 등장하면, 마지막 항목만 남게 됩니다.

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
메서드에 콜백을 전달할 수도 있습니다. 콜백은 컬렉션의 키로 사용할 값을 반환해야 합니다.

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
`keys` 메서드는 컬렉션에 있는 모든 키를 반환합니다.

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
`last` 메서드는 지정한 조건을 만족하는 컬렉션의 마지막 요소를 반환합니다.

```
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

<!-- You may also call the `last` method with no arguments to get the last element in the collection. If the collection is empty, `null` is returned: -->
아무 인수도 지정하지 않고 `last` 메서드를 호출하면, 컬렉션의 마지막 요소를 반환합니다. 컬렉션이 비어 있으면 `null`을 반환합니다.

```
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
<!-- #### `lazy()` -->
#### `lazy()`

<!-- The `lazy` method returns a new [`LazyCollection`](#lazy-collections) instance from the underlying array of items: -->
`lazy` 메서드는 현재 컬렉션의 아이템들을 기반으로 새로운 [`LazyCollection`](#lazy-collections) 인스턴스를 생성합니다.

```
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

<!-- This is especially useful when you need to perform transformations on a huge `Collection` that contains many items: -->
이 기능은 많은 수의 아이템을 가진 거대한 `Collection`에서 변환을 수행해야 할 때 특히 유용합니다.

```
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

<!-- By converting the collection to a `LazyCollection`, we avoid having to allocate a ton of additional memory. Though the original collection still keeps _its_ values in memory, the subsequent filters will not. Therefore, virtually no additional memory will be allocated when filtering the collection's results. -->
컬렉션을 `LazyCollection`으로 변환하면, 추가적인 메모리 할당 없이 결과를 필터링할 수 있습니다. 원본 컬렉션은 내부적으로 여전히 모든 값을 메모리에 보관하지만, 이후의 필터 동작에서는 추가 메모리를 필요로 하지 않습니다. 즉, 필터링 이후 결과에 대해선 사실상 추가 메모리 사용이 거의 없습니다.

<a name="method-macro"></a>
<!-- #### `macro()` -->
#### `macro()`

<!-- The static `macro` method allows you to add methods to the `Collection` class at run time. Refer to the documentation on [extending collections](#extending-collections) for more information. -->
정적 `macro` 메서드를 사용하면 실행 시간에 `Collection` 클래스에 메서드를 추가할 수 있습니다. 자세한 내용은 [extending collections](#extending-collections) 관련 문서를 참고하세요.

<a name="method-make"></a>
<!-- #### `make()` -->
#### `make()`

<!-- The static `make` method creates a new collection instance. See the [Creating Collections](#creating-collections) section. -->
정적 `make` 메서드는 새로운 컬렉션 인스턴스를 생성합니다. 자세한 내용은 [Creating Collections](#creating-collections) 항목을 참고하세요.

<a name="method-map"></a>
<!-- #### `map()` -->
#### `map()`

<!-- The `map` method iterates through the collection and passes each value to the given callback. The callback is free to modify the item and return it, thus forming a new collection of modified items: -->
`map` 메서드는 컬렉션을 순회하며 각 값을 지정한 콜백에 전달합니다. 콜백에서 아이템을 가공하고 반환하면, 변형된 값들로 새로운 컬렉션을 생성합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 컬렉션 메서드처럼, `map`은 새로운 컬렉션 인스턴스를 반환하며, 원본 컬렉션은 수정하지 않습니다. 원본 컬렉션 자체를 변형하려면 [`transform`](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
<!-- #### `mapInto()` -->
#### `mapInto()`

<!-- The `mapInto()` method iterates over the collection, creating a new instance of the given class by passing the value into the constructor: -->
`mapInto()` 메서드는 컬렉션을 순회하면서, 각 값을 생성자의 인수로 전달하여 지정한 클래스의 새 인스턴스를 생성합니다.

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
`mapSpread` 메서드는 컬렉션의 아이템(중첩된 값들)을 콜백에 분리해서 전달합니다. 콜백에서 가공된 값들을 반환하면, 변형된 값들로 새로운 컬렉션을 만듭니다.

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
`mapToGroups` 메서드는 컬렉션의 항목들을 주어진 클로저에 따라 그룹으로 묶습니다. 이 클로저는 하나의 키/값 쌍만을 포함하는 연관 배열을 반환해야 하며, 이로써 새로운 그룹별 값의 컬렉션을 형성하게 됩니다:

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
`mapWithKeys` 메서드는 컬렉션을 순회하면서 각 값에 대해 주어진 콜백을 호출합니다. 이 콜백은 하나의 키/값 쌍만을 포함하는 연관 배열을 반환해야 합니다:

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
`max` 메서드는 지정한 키의 최댓값을 반환합니다:

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
`median` 메서드는 지정한 키의 [median value](https://en.wikipedia.org/wiki/Median)을 반환합니다:

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
`merge` 메서드는 주어진 배열이나 컬렉션을 원본 컬렉션과 병합합니다. 만약 주어진 항목의 문자열 키가 원본 컬렉션의 문자열 키와 일치하는 경우, 주어진 항목의 값이 원본 컬렉션의 값을 덮어씁니다:

```
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

<!-- If the given item's keys are numeric, the values will be appended to the end of the collection: -->
주어진 항목의 키가 숫자인 경우, 값이 컬렉션 끝에 추가됩니다:

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
`mergeRecursive` 메서드는 주어진 배열이나 컬렉션을 원본 컬렉션과 재귀적으로 병합합니다. 만약 주어진 항목의 문자열 키가 원본 컬렉션의 문자열 키와 일치하는 경우, 이 키의 값들이 배열로 병합되며, 이 동작은 재귀적으로 적용됩니다:

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
`min` 메서드는 지정한 키의 최솟값을 반환합니다:

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
`mode` 메서드는 지정한 키의 [mode value](https://en.wikipedia.org/wiki/Mode_(statistics))을 반환합니다:

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
`multiply` 메서드는 컬렉션의 모든 항목을 지정한 횟수만큼 반복하여 복제한 새 컬렉션을 만듭니다:

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
`nth` 메서드는 컬렉션에서 n번째마다 한 번씩 요소를 선택하여 새로운 컬렉션을 생성합니다:

```
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

<!-- You may optionally pass a starting offset as the second argument: -->
두 번째 인수로 시작 위치(오프셋)를 지정할 수도 있습니다:

```
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
<!-- #### `only()` -->
#### `only()`

<!-- The `only` method returns the items in the collection with the specified keys: -->
`only` 메서드는 컬렉션에서 지정한 키들만 가진 항목들만 반환합니다:

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
`only`의 반대 동작이 필요한 경우 [except](#method-except) 메서드를 참고하세요.

> [!NOTE]
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-only)을 사용할 때는 이 메서드의 동작이 다르게 동작합니다.

<a name="method-pad"></a>
<!-- #### `pad()` -->
#### `pad()`

<!-- The `pad` method will fill the array with the given value until the array reaches the specified size. This method behaves like the [array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP function. -->
`pad` 메서드는 배열의 길이가 지정된 크기에 도달할 때까지 주어진 값으로 배열을 채웁니다. 이 메서드는 PHP의 [array_pad](https://secure.php.net/manual/en/function.array-pad.php) 함수와 유사하게 동작합니다.

<!-- To pad to the left, you should specify a negative size. No padding will take place if the absolute value of the given size is less than or equal to the length of the array: -->
배열을 왼쪽(시작 부분)으로 패딩하려면, 크기를 음수로 지정해야 합니다. 만약 배열의 길이가 지정된 크기보다 크거나 같으면 패딩이 적용되지 않습니다:

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
`partition` 메서드는 PHP 배열 구조 분해 할당과 결합하여, 특정 조건을 통과하는 요소와 통과하지 못하는 요소를 분리할 수 있습니다:

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
`percentage` 메서드는 컬렉션에서 특정 조건을 통과하는 항목의 비율(%)을 빠르게 계산할 때 사용할 수 있습니다:

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn ($value) => $value === 1);

// 33.33
```

<!-- By default, the percentage will be rounded to two decimal places. However, you may customize this behavior by providing a second argument to the method: -->
기본적으로 결과는 소수점 둘째 자리까지 반올림됩니다. 하지만 두 번째 인자(precision)를 이용해 자릿수를 커스터마이즈할 수도 있습니다:

```php
$percentage = $collection->percentage(fn ($value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
<!-- #### `pipe()` -->
#### `pipe()`

<!-- The `pipe` method passes the collection to the given closure and returns the result of the executed closure: -->
`pipe` 메서드는 컬렉션을 주어진 클로저로 전달하고, 그 실행 결과를 반환합니다:

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
`pipeInto` 메서드는 지정한 클래스의 새로운 인스턴스를 생성하고, 컬렉션을 해당 클래스의 생성자에 전달합니다:

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
`pipeThrough` 메서드는 컬렉션을 주어진 클로저 배열에 차례대로 전달하고, 그 최종 결과를 반환합니다:

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
`pluck` 메서드는 지정한 키에 해당하는 모든 값을 추출해 반환합니다:

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
결과 컬렉션의 키를 어떻게 지정할지 추가적으로 설정할 수도 있습니다:

```
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

<!-- The `pluck` method also supports retrieving nested values using "dot" notation: -->
`pluck` 메서드는 "점 표기법(dot notation)"을 사용하여 중첩된 값을 추출하는 것도 지원합니다:

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
키가 중복되는 경우, 마지막에 일치했던 값이 추출된 컬렉션에 저장됩니다:

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
`pop` 메서드는 컬렉션에서 마지막 항목을 꺼내 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

<!-- You may pass an integer to the `pop` method to remove and return multiple items from the end of a collection: -->
`pop` 메서드에 정수를 전달하면, 컬렉션의 끝에서 여러 항목을 꺼내 반환할 수 있습니다:

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
`prepend` 메서드는 컬렉션의 맨 앞에 새 항목을 추가합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

<!-- You may also pass a second argument to specify the key of the prepended item: -->
두 번째 인수로, 앞에 추가할 항목의 키를 지정할 수도 있습니다:

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
`pull` 메서드는 컬렉션에서 특정 키에 해당하는 항목을 꺼내고, 그 값을 반환합니다:

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
`push` 메서드는 컬렉션의 끝에 새 항목을 추가합니다:

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
`put` 메서드는 컬렉션에 주어진 키-값 쌍을 설정합니다:

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
`random` 메서드는 컬렉션에서 무작위로 항목 하나를 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (retrieved randomly)
```

<!-- You may pass an integer to `random` to specify how many items you would like to randomly retrieve. A collection of items is always returned when explicitly passing the number of items you wish to receive: -->
무작위로 여러 개의 항목을 가져오고 싶다면 `random`에 정수 값을 인수로 전달할 수 있습니다. 가져올 항목의 개수를 명시적으로 지정하면, 항상 컬렉션이 반환됩니다.

```
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (retrieved randomly)
```

<!-- If the collection instance has fewer items than requested, the `random` method will throw an `InvalidArgumentException`. -->
컬렉션 인스턴스에 요청한 개수보다 적은 항목이 있는 경우, `random` 메서드는 `InvalidArgumentException` 예외를 발생시킵니다.

<!-- The `random` method also accepts a closure, which will receive the current collection instance: -->
`random` 메서드는 현재 컬렉션 인스턴스를 전달받는 클로저도 인수로 받을 수 있습니다.

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
`range` 메서드는 지정한 범위 내의 정수로 구성된 컬렉션을 반환합니다.

```
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
<!-- #### `reduce()` -->
#### `reduce()`

<!-- The `reduce` method reduces the collection to a single value, passing the result of each iteration into the subsequent iteration: -->
`reduce` 메서드는 컬렉션의 항목 전체를 하나의 값으로 축약합니다. 각 반복의 결과가 다음 반복으로 전달됩니다.

```
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

<!-- The value for `$carry` on the first iteration is `null`; however, you may specify its initial value by passing a second argument to `reduce`: -->
첫 반복 시 `$carry`의 값은 `null`입니다. 하지만 `reduce`에 두 번째 인수를 전달하여 초기값을 지정할 수도 있습니다.

```
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

<!-- The `reduce` method also passes array keys in associative collections to the given callback: -->
`reduce` 메서드는 연관 배열 컬렉션에서 배열의 키도 콜백 함수에 전달합니다.

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
`reduceSpread` 메서드는 컬렉션을 여러 값이 담긴 배열로 축약합니다. 각 반복의 결과가 그다음 반복에 전달됩니다. 이 메서드는 `reduce`와 유사하지만, 여러 초기값을 지정할 수 있습니다.

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
`reject` 메서드는 주어진 클로저를 사용해 컬렉션을 필터링합니다. 클로저가 `true`를 반환하는 항목은 결과 컬렉션에서 제외됩니다.

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

<!-- For the inverse of the `reject` method, see the [`filter`](#method-filter) method. -->
`reject` 메서드의 반대 동작이 필요하다면 [`filter`](#method-filter) 메서드를 참고하세요.

<a name="method-replace"></a>
<!-- #### `replace()` -->
#### `replace()`

<!-- The `replace` method behaves similarly to `merge`; however, in addition to overwriting matching items that have string keys, the `replace` method will also overwrite items in the collection that have matching numeric keys: -->
`replace` 메서드는 `merge`와 비슷하게 동작합니다. 다만 문자열 키를 가진 일치하는 항목을 덮어쓰는 것뿐만 아니라, `replace` 메서드는 일치하는 숫자 키를 가진 컬렉션 항목도 덮어씁니다.

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
이 메서드는 `replace`와 비슷하지만, 배열 내부까지 재귀적으로 들어가 내부 값에도 동일한 치환을 적용합니다.

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
`reverse` 메서드는 컬렉션 항목의 순서를 거꾸로 뒤집으며, 원래의 키도 그대로 유지합니다.

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
`search` 메서드는 지정한 값을 컬렉션에서 찾아서, 존재할 경우 해당 키를 반환합니다. 항목이 없다면 `false`를 반환합니다.

```
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

<!-- The search is done using a "loose" comparison, meaning a string with an integer value will be considered equal to an integer of the same value. To use "strict" comparison, pass `true` as the second argument to the method: -->
이 검색은 "느슨한(loose)" 비교를 사용하므로, 정수와 동일한 값을 가진 문자열도 일치로 간주됩니다. "엄격한(strict)" 비교를 사용하고 싶다면 두 번째 인수에 `true`를 전달하세요.

```
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

<!-- Alternatively, you may provide your own closure to search for the first item that passes a given truth test: -->
또는 클로저를 제공하여, 주어진 조건을 통과하는 첫 번째 항목을 검색할 수도 있습니다.

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
`select` 메서드는 SQL의 `SELECT` 명령문처럼, 지정한 키만을 추출하여 새로운 컬렉션으로 반환합니다.

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

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

<!-- You may pass an integer to the `shift` method to remove and return multiple items from the beginning of a collection: -->
`shift` 메서드에 정수를 인수로 전달하면, 컬렉션의 시작 부분에서 여러 개의 항목을 한번에 제거하고 반환할 수 있습니다.

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
`shuffle` 메서드는 컬렉션의 항목 순서를 무작위로 섞어 새로운 컬렉션을 만듭니다.

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
`skip` 메서드는 컬렉션의 앞에서 지정한 개수만큼 항목을 건너뛴 후, 나머지가 담긴 새 컬렉션을 반환합니다.

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
`skipUntil` 메서드는 주어진 콜백이 `false`를 반환하는 동안은 항목을 건너뜁니다. 콜백이 처음으로 `true`를 반환하는 순간부터 나머지 모든 항목이 새로운 컬렉션으로 반환됩니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

<!-- You may also pass a simple value to the `skipUntil` method to skip all items until the given value is found: -->
`skipUntil` 메서드에 단순 값을 전달하면, 해당 값이 처음 나올 때까지 항목을 모두 건너뜁니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> 만약 주어진 값이 존재하지 않거나 콜백이 한번도 `true`를 반환하지 않는 경우, `skipUntil` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
<!-- #### `skipWhile()` -->
#### `skipWhile()`

<!-- The `skipWhile` method skips over items from the collection while the given callback returns `true`. Once the callback returns `false` all of the remaining items in the collection will be returned as a new collection: -->
`skipWhile` 메서드는 주어진 콜백이 `true`를 반환하는 동안 항목을 계속 건너뜁니다. 콜백이 처음으로 `false`를 반환하는 시점부터 남은 모든 항목이 새로운 컬렉션으로 반환됩니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> 콜백이 한번도 `false`를 반환하지 않으면, `skipWhile` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
<!-- #### `slice()` -->
#### `slice()`

<!-- The `slice` method returns a slice of the collection starting at the given index: -->
`slice` 메서드는 지정된 인덱스부터 시작하는 컬렉션의 일부(슬라이스)를 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

<!-- If you would like to limit the size of the returned slice, pass the desired size as the second argument to the method: -->
리턴되는 슬라이스의 크기를 제한하고 싶다면 두 번째 인수로 원하는 크기를 지정하면 됩니다.

```
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

<!-- The returned slice will preserve keys by default. If you do not wish to preserve the original keys, you can use the [`values`](#method-values) method to reindex them. -->
기본적으로 반환된 슬라이스는 원본 키를 그대로 유지합니다. 원본 키를 유지하지 않고 연속된 인덱스로 재정렬하려면 [`values`](#method-values) 메서드를 사용하세요.

<a name="method-sliding"></a>
<!-- #### `sliding()` -->
#### `sliding()`

<!-- The `sliding` method returns a new collection of chunks representing a "sliding window" view of the items in the collection: -->
`sliding` 메서드는 컬렉션의 항목을 "슬라이딩 윈도우" 방식의 덩어리(chunk)로 만든 새 컬렉션을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

<!-- This is especially useful in conjunction with the [`eachSpread`](#method-eachspread) method: -->
이 기능은 [`eachSpread`](#method-eachspread) 메서드와 함께 쓸 때 특히 유용합니다.

```
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

<!-- You may optionally pass a second "step" value, which determines the distance between the first item of every chunk: -->
두 번째 인수로 "스텝(step)" 값을 지정할 수 있는데, 이 값은 각 덩어리의 첫 항목 간 간격을 의미합니다.

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
`sole` 메서드는 주어진 조건에 딱 하나만 부합하는 첫 번째 요소를 반환합니다.

```
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

<!-- You may also pass a key / value pair to the `sole` method, which will return the first element in the collection that matches the given pair, but only if it exactly one element matches: -->
`sole` 메서드에 키/값 쌍을 전달하면, 해당 쌍에 딱 하나만 일치하는 첫 번째 요소를 반환합니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

<!-- Alternatively, you may also call the `sole` method with no argument to get the first element in the collection if there is only one element: -->
또는 인수 없이 `sole`을 호출해서, 컬렉션에 항목이 단 하나만 있을 때 그 값을 바로 반환할 수도 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

<!-- If there are no elements in the collection that should be returned by the `sole` method, an `\Illuminate\Collections\ItemNotFoundException` exception will be thrown. If there is more than one element that should be returned, an `\Illuminate\Collections\MultipleItemsFoundException` will be thrown. -->
`sole` 메서드로 반환해야 할 항목이 없으면 `\Illuminate\Collections\ItemNotFoundException` 예외가 발생합니다. 반환해야 할 항목이 둘 이상이면 `\Illuminate\Collections\MultipleItemsFoundException` 예외가 발생합니다.

<a name="method-some"></a>
<!-- #### `some()` -->
#### `some()`

<!-- Alias for the [`contains`](#method-contains) method. -->
[`contains`](#method-contains) 메서드의 별칭(alias)입니다.

<a name="method-sort"></a>
<!-- #### `sort()` -->
#### `sort()`

<!-- The `sort` method sorts the collection. The sorted collection keeps the original array keys, so in the following example we will use the [`values`](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sort` 메서드는 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래 배열의 키를 그대로 유지하므로, 아래 예시처럼 [`values`](#method-values) 메서드를 사용하여 연속된 숫자 인덱스로 키를 재설정하는 방법을 참고하세요.

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

<!-- If your sorting needs are more advanced, you may pass a callback to `sort` with your own algorithm. Refer to the PHP documentation on [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters), which is what the collection's `sort` method calls utilizes internally. -->
더 복잡한 정렬이 필요하다면, `sort` 메서드에 콜백을 전달하여 직접 알고리즘을 정의할 수 있습니다. 컬렉션의 `sort` 메서드가 내부적으로 사용하는 PHP의 [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) 함수 문서를 참고하세요.

> [!NOTE]
> 중첩된 배열이나 객체로 구성된 컬렉션을 정렬하려면 [`sortBy`](#method-sortby) 및 [`sortByDesc`](#method-sortbydesc) 메서드를 이용하세요.

<a name="method-sortby"></a>
<!-- #### `sortBy()` -->
#### `sortBy()`

<!-- The `sortBy` method sorts the collection by the given key. The sorted collection keeps the original array keys, so in the following example we will use the [`values`](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sortBy` 메서드는 지정한 키로 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래 배열의 키를 유지하기 때문에, 예제처럼 [`values`](#method-values) 메서드를 통해 키를 연속 번호로 재설정할 수 있습니다.

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
`sortBy` 메서드는 두 번째 인수로 [sort flags](https://www.php.net/manual/en/function.sort.php)를 지정할 수 있습니다.

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
또한, 직접 클로저를 전달하여 컬렉션 값을 정렬하는 기준을 자유롭게 지정할 수도 있습니다.

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
컬렉션을 여러 속성으로 정렬하고 싶다면, 각 정렬 조건을 배열로 지정하여 `sortBy`에 전달할 수 있습니다. 각 정렬 조건은 정렬하려는 속성과 정렬 방향을 지정하는 배열이어야 합니다.

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
여러 속성으로 정렬할 때도, 각각의 정렬 과정을 정의하는 클로저를 전달할 수 있습니다.

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
이 메서드는 [`sortBy`](#method-sortby) 메서드와 동일한 시그니처를 가지지만, 컬렉션을 반대 순서로 정렬합니다.

<a name="method-sortdesc"></a>
<!-- #### `sortDesc()` -->
#### `sortDesc()`

<!-- This method will sort the collection in the opposite order as the [`sort`](#method-sort) method: -->
이 메서드는 컬렉션을 [`sort`](#method-sort) 메서드와는 반대 순서로 정렬합니다.

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

<!-- Unlike `sort`, you may not pass a closure to `sortDesc`. Instead, you should use the [`sort`](#method-sort) method and invert your comparison. -->
`sort`와는 달리, `sortDesc`에는 클로저를 전달할 수 없습니다. 직접 비교 로직을 반대로 하고 싶다면 [`sort`](#method-sort) 메서드를 사용해야 합니다.

<a name="method-sortkeys"></a>
<!-- #### `sortKeys()` -->
#### `sortKeys()`

<!-- The `sortKeys` method sorts the collection by the keys of the underlying associative array: -->
`sortKeys` 메서드는 내부의 연관 배열에서 키를 기준으로 컬렉션을 정렬합니다.

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
이 메서드는 [`sortKeys`](#method-sortkeys) 메서드와 동일한 시그니처를 가지며, 반대 순서로 컬렉션을 정렬합니다.

<a name="method-sortkeysusing"></a>
<!-- #### `sortKeysUsing()` -->
#### `sortKeysUsing()`

<!-- The `sortKeysUsing` method sorts the collection by the keys of the underlying associative array using a callback: -->
`sortKeysUsing` 메서드는 콜백 함수를 사용하여 내부 연관 배열의 키를 기준으로 컬렉션을 정렬합니다.

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
콜백 함수는 정수값(음수, 0, 양수)을 반환하는 비교 함수여야 합니다. 더 자세한 정보는 PHP 공식 문서의 [`uksort`](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters)를 참고하세요. `sortKeysUsing` 메서드는 내부적으로 이 PHP 함수를 사용합니다.

<a name="method-splice"></a>
<!-- #### `splice()` -->
#### `splice()`

<!-- The `splice` method removes and returns a slice of items starting at the specified index: -->
`splice` 메서드는 지정된 인덱스에서 시작하여 일정 개수의 항목을 제거하고 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

<!-- You may pass a second argument to limit the size of the resulting collection: -->
결과 컬렉션의 크기를 제한하고 싶다면 두 번째 인수로 제한할 크기를 전달할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

<!-- In addition, you may pass a third argument containing the new items to replace the items removed from the collection: -->
또한, 제거된 항목 대신 새 항목을 추가하고 싶다면 세 번째 인수로 대체할 항목 배열을 전달할 수 있습니다.

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
`split` 메서드는 컬렉션을 지정한 개수의 그룹으로 나눕니다.

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
`splitIn` 메서드는 컬렉션을 지정한 개수의 그룹으로 나눕니다. 이때 마지막 그룹을 제외한 다른 그룹들은 가능한 한 완전히 채워진 후, 남은 항목들을 마지막 그룹에 할당합니다.

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
`sum` 메서드는 컬렉션 내 모든 항목을 더한 합계를 반환합니다.

```
collect([1, 2, 3, 4, 5])->sum();

// 15
```

<!-- If the collection contains nested arrays or objects, you should pass a key that will be used to determine which values to sum: -->
컬렉션에 중첩 배열이나 객체가 포함되어 있다면, 합계를 구할 값을 결정할 키를 지정할 수 있습니다.

```
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

<!-- In addition, you may pass your own closure to determine which values of the collection to sum: -->
또한, 직접 콜백을 전달하여 합계를 구할 항목을 지정할 수도 있습니다.

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
`take` 메서드는 지정한 개수만큼의 항목을 가진 새로운 컬렉션을 반환합니다.

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

<!-- You may also pass a negative integer to take the specified number of items from the end of the collection: -->
마지막에서부터 항목을 가져오고 싶다면 음수 값을 전달할 수 있습니다.

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
`takeUntil` 메서드는 지정한 콜백이 `true`를 반환할 때까지의 항목들을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

<!-- You may also pass a simple value to the `takeUntil` method to get the items until the given value is found: -->
`takeUntil` 메서드에 단순 값을 전달하면, 해당 값이 나올 때까지의 항목을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> 전달한 값이 컬렉션에서 발견되지 않거나, 콜백이 한 번도 `true`를 반환하지 않는 경우, `takeUntil` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-takewhile"></a>
<!-- #### `takeWhile()` -->
#### `takeWhile()`

<!-- The `takeWhile` method returns items in the collection until the given callback returns `false`: -->
`takeWhile` 메서드는 지정한 콜백이 `false`를 반환할 때까지의 항목들을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]
> 콜백이 한 번도 `false`를 반환하지 않으면, `takeWhile` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-tap"></a>
<!-- #### `tap()` -->
#### `tap()`

<!-- The `tap` method passes the collection to the given callback, allowing you to "tap" into the collection at a specific point and do something with the items while not affecting the collection itself. The collection is then returned by the `tap` method: -->
`tap` 메서드는 컬렉션 전체를 전달된 콜백에 넘겨주어, 컬렉션 자체는 변경하지 않은 채 특정 시점의 값들을 사용할 수 있도록 합니다. 이후 `tap` 메서드는 컬렉션을 그대로 반환합니다.

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
정적 메서드인 `times`는 지정한 횟수만큼 클로저를 호출하여, 그 결과값으로 새로운 컬렉션을 만듭니다.

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
`toArray` 메서드는 컬렉션을 일반 PHP `array`로 변환합니다. 컬렉션 항목이 [Eloquent](/docs/11.x/eloquent) 모델인 경우 모델도 배열로 변환됩니다.

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
> `toArray`는 컬렉션 내의 모든 하위 객체 중 `Arrayable`의 인스턴스도 배열로 변환합니다. 컬렉션의 실제 '원본' 배열만을 얻고 싶다면 [`all`](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
<!-- #### `toJson()` -->
#### `toJson()`

<!-- The `toJson` method converts the collection into a JSON serialized string: -->
`toJson` 메서드는 컬렉션을 JSON 직렬화된 문자열로 변환합니다.

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
<!-- #### `transform()` -->
#### `transform()`

<!-- The `transform` method iterates over the collection and calls the given callback with each item in the collection. The items in the collection will be replaced by the values returned by the callback: -->
`transform` 메서드는 컬렉션을 순회하면서 각 항목을 콜백으로 전달하고, 콜백이 반환한 값으로 컬렉션의 항목을 교체합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 컬렉션 메서드와 달리, `transform`은 컬렉션 객체 자체를 직접 변경합니다. 새로운 컬렉션을 얻고 싶다면 대신 [`map`](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
<!-- #### `undot()` -->
#### `undot()`

<!-- The `undot` method expands a single-dimensional collection that uses "dot" notation into a multi-dimensional collection: -->
`undot` 메서드는 점(dot) 표기법을 사용한 1차원 컬렉션을 다차원 컬렉션으로 확장합니다.

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
`union` 메서드는 주어진 배열을 컬렉션에 병합합니다. 만약 주어진 배열에 원본 컬렉션과 동일한 키가 있으면, 원본 컬렉션의 값을 우선으로 사용합니다.

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
`unique` 메서드는 컬렉션에서 중복되지 않는 항목만 반환합니다. 반환된 컬렉션은 기존의 배열 키를 그대로 유지하므로, 아래의 예시처럼 [`values`](#method-values) 메서드를 사용해 키를 연속적인 인덱스로 재설정할 수 있습니다.

```
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

<!-- When dealing with nested arrays or objects, you may specify the key used to determine uniqueness: -->
중첩 배열이나 객체의 경우, 항목의 고유성을 판단할 키를 지정할 수 있습니다.

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
마지막으로, `unique` 메서드에 클로저를 전달하여 항목의 고유성을 판단할 값을 직접 지정할 수도 있습니다.

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
`unique` 메서드는 항목 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 숫자형 문자열과 같은 값의 숫자가 같으면 동일하다고 간주됩니다. "엄격한(strict)" 비교를 사용해 필터링 하려면 [`uniqueStrict`](#method-uniquestrict) 메서드를 사용하세요.

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/11.x/eloquent-collections#method-unique)을 사용할 때 동작이 달라집니다.

<a name="method-uniquestrict"></a>
<!-- #### `uniqueStrict()` -->
#### `uniqueStrict()`

<!-- This method has the same signature as the [`unique`](#method-unique) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [`unique`](#method-unique) 메서드와 동일한 시그니처를 가지지만, 모든 값을 "엄격한(strict)" 비교로 판단하여 중복을 거릅니다.

<a name="method-unless"></a>
<!-- #### `unless()` -->
#### `unless()`

<!-- The `unless` method will execute the given callback unless the first argument given to the method evaluates to `true`: -->
`unless` 메서드는 첫 번째 인수가 `true`가 아닌 경우 주어진 콜백을 실행합니다.

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
`unless` 메서드에는 두 번째 콜백을 전달할 수도 있습니다. 두 번째 콜백은 `unless` 메서드의 첫 번째 인수가 `true`로 평가되는 경우에 실행됩니다.

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
`unless`의 반대 동작을 원하면 [`when`](#method-when) 메서드를 참고하세요.

<a name="method-unlessempty"></a>
<!-- #### `unlessEmpty()` -->
#### `unlessEmpty()`

<!-- Alias for the [`whenNotEmpty`](#method-whennotempty) method. -->
[`whenNotEmpty`](#method-whennotempty) 메서드의 별칭(aliase)입니다.

<a name="method-unlessnotempty"></a>
<!-- #### `unlessNotEmpty()` -->
#### `unlessNotEmpty()`

<!-- Alias for the [`whenEmpty`](#method-whenempty) method. -->
[`whenEmpty`](#method-whenempty) 메서드의 별칭(aliase)입니다.

<a name="method-unwrap"></a>
<!-- #### `unwrap()` -->
#### `unwrap()`

<!-- The static `unwrap` method returns the collection's underlying items from the given value when applicable: -->
정적 메서드인 `unwrap`은 값을 받아 컬렉션이 적용 가능한 경우 컬렉션의 원본 항목을 반환합니다.

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
`value` 메서드는 컬렉션의 첫 번째 요소에서 지정한 값을 추출합니다.

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
`values` 메서드는 키를 0부터 시작하는 연속적인 정수로 재설정한 새로운 컬렉션을 반환합니다.

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
`when` 메서드는 첫 번째 인자가 `true`로 평가될 때 지정한 콜백을 실행합니다. 이 콜백에는 컬렉션 인스턴스와 `when` 메서드에 전달한 첫 번째 인자가 전달됩니다.

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
`when` 메서드에는 두 번째 콜백도 전달할 수 있습니다. 두 번째 콜백은 `when` 메서드의 첫 번째 인자가 `false`로 평가될 때 실행됩니다.

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
`when`의 반대 동작을 원하실 경우 [`unless`](#method-unless) 메서드를 참고하세요.

<a name="method-whenempty"></a>
<!-- #### `whenEmpty()` -->
#### `whenEmpty()`

<!-- The `whenEmpty` method will execute the given callback when the collection is empty: -->
`whenEmpty` 메서드는 컬렉션이 비어 있을 때 지정한 콜백을 실행합니다.

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
`whenEmpty` 메서드에는 두 번째 클로저를 전달할 수 있으며, 컬렉션이 비어 있지 않을 때 이 두 번째 클로저가 실행됩니다.

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
`whenEmpty`의 반대 동작은 [`whenNotEmpty`](#method-whennotempty) 메서드를 참고하세요.

<a name="method-whennotempty"></a>
<!-- #### `whenNotEmpty()` -->
#### `whenNotEmpty()`

<!-- The `whenNotEmpty` method will execute the given callback when the collection is not empty: -->
`whenNotEmpty` 메서드는 컬렉션이 비어 있지 않을 때 지정한 콜백을 실행합니다.

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
`whenNotEmpty` 메서드에는 두 번째 클로저를 전달할 수 있으며, 컬렉션이 비어 있을 때 이 두 번째 클로저가 실행됩니다.

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
`whenNotEmpty`의 반대 동작은 [`whenEmpty`](#method-whenempty) 메서드를 참고하세요.

<a name="method-where"></a>
<!-- #### `where()` -->
#### `where()`

<!-- The `where` method filters the collection by a given key / value pair: -->
`where` 메서드는 지정한 키/값 쌍으로 컬렉션을 필터링합니다.

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
`where` 메서드는 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값과 같은 값을 가진 문자열은 정수 값과 같다고 간주합니다. "엄격한(strict)" 비교를 사용하려면 [`whereStrict`](#method-wherestrict) 메서드를 사용하세요.

<!-- Optionally, you may pass a comparison operator as the second parameter. Supported operators are: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', and '<=': -->
선택적으로 두 번째 인자로 비교 연산자를 전달할 수 있습니다. 지원되는 연산자는 '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', '<='입니다.

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
이 메서드는 [`where`](#method-where) 메서드와 사용법이 동일하지만 모든 값을 "엄격한(strict)" 비교로 비교합니다.

<a name="method-wherebetween"></a>
<!-- #### `whereBetween()` -->
#### `whereBetween()`

<!-- The `whereBetween` method filters the collection by determining if a specified item value is within a given range: -->
`whereBetween` 메서드는 지정한 아이템의 값이 주어진 범위에 포함되는지 여부로 컬렉션을 필터링합니다.

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
`whereIn` 메서드는 주어진 배열에 포함된 특정 아이템 값을 갖지 않는 요소들을 컬렉션에서 제거합니다.

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
`whereIn` 메서드는 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값과 같은 값을 가진 문자열은 정수 값과 같다고 간주합니다. "엄격한(strict)" 비교를 사용하려면 [`whereInStrict`](#method-whereinstrict) 메서드를 사용하세요.

<a name="method-whereinstrict"></a>
<!-- #### `whereInStrict()` -->
#### `whereInStrict()`

<!-- This method has the same signature as the [`whereIn`](#method-wherein) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [`whereIn`](#method-wherein) 메서드와 사용법이 동일하지만 모든 값을 "엄격한(strict)" 비교로 비교합니다.

<a name="method-whereinstanceof"></a>
<!-- #### `whereInstanceOf()` -->
#### `whereInstanceOf()`

<!-- The `whereInstanceOf` method filters the collection by a given class type: -->
`whereInstanceOf` 메서드는 지정한 클래스 타입의 인스턴스만 필터링하여 컬렉션에서 반환합니다.

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
`whereNotBetween` 메서드는 지정한 아이템의 값이 주어진 범위를 벗어나는 경우만 필터링하여 컬렉션에 남깁니다.

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
`whereNotIn` 메서드는 주어진 배열에 포함된 아이템 값을 갖는 요소들을 컬렉션에서 제거합니다.

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
`whereNotIn` 메서드는 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값과 같은 값을 가진 문자열은 정수 값과 같다고 간주합니다. "엄격한(strict)" 비교를 사용하려면 [`whereNotInStrict`](#method-wherenotinstrict) 메서드를 사용하세요.

<a name="method-wherenotinstrict"></a>
<!-- #### `whereNotInStrict()` -->
#### `whereNotInStrict()`

<!-- This method has the same signature as the [`whereNotIn`](#method-wherenotin) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [`whereNotIn`](#method-wherenotin) 메서드와 사용법이 동일하지만 모든 값을 "엄격한(strict)" 비교로 비교합니다.

<a name="method-wherenotnull"></a>
<!-- #### `whereNotNull()` -->
#### `whereNotNull()`

<!-- The `whereNotNull` method returns items from the collection where the given key is not `null`: -->
`whereNotNull` 메서드는 주어진 키가 `null`이 아닌 요소만 컬렉션에서 반환합니다.

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
`whereNull` 메서드는 주어진 키가 `null`인 요소만 컬렉션에서 반환합니다.

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
정적 메서드인 `wrap`은 전달된 값을 컬렉션으로 감쌀 수 있을 때 컬렉션으로 감쌉니다.

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
`zip` 메서드는 지정한 배열의 값과 원래 컬렉션의 값을 같은 인덱스끼리 병합해서 반환합니다.

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
컬렉션은 "하이어 오더 메시지(higher order messages)"도 지원합니다. 이는 컬렉션에서 자주 사용하는 동작을 더 간단하게 호출할 수 있는 단축 표현 방식입니다. 하이어 오더 메시지를 지원하는 컬렉션 메서드는 [`average`](#method-average), [`avg`](#method-avg), [`contains`](#method-contains), [`each`](#method-each), [`every`](#method-every), [`filter`](#method-filter), [`first`](#method-first), [`flatMap`](#method-flatmap), [`groupBy`](#method-groupby), [`keyBy`](#method-keyby), [`map`](#method-map), [`max`](#method-max), [`min`](#method-min), [`partition`](#method-partition), [`reject`](#method-reject), [`skipUntil`](#method-skipuntil), [`skipWhile`](#method-skipwhile), [`some`](#method-some), [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc), [`sum`](#method-sum), [`takeUntil`](#method-takeuntil), [`takeWhile`](#method-takewhile), [`unique`](#method-unique) 등이 있습니다.

<!-- Each higher order message can be accessed as a dynamic property on a collection instance. For instance, let's use the `each` higher order message to call a method on each object within a collection: -->
각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 속성처럼 접근할 수 있습니다. 예를 들어 컬렉션 내 각 객체에서 메서드를 호출하려면, `each` 하이어 오더 메시지를 다음과 같이 사용할 수 있습니다.

```
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

<!-- Likewise, we can use the `sum` higher order message to gather the total number of "votes" for a collection of users: -->
마찬가지로, `sum` 하이어 오더 메시지를 사용해 users 컬렉션의 "votes" 값을 모두 합칠 수도 있습니다.

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
> Laravel의 레이지 컬렉션을 학습하기 전에, [PHP generators](https://www.php.net/manual/en/language.generators.overview.php)를 먼저 확인해보시는 것이 좋습니다.

<!-- To supplement the already powerful `Collection` class, the `LazyCollection` class leverages PHP's [generators](https://www.php.net/manual/en/language.generators.overview.php) to allow you to work with very large datasets while keeping memory usage low. -->
기존의 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [generators](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여 매우 큰 데이터셋도 메모리를 적게 사용하면서 다룰 수 있게 해줍니다.

<!-- For example, imagine your application needs to process a multi-gigabyte log file while taking advantage of Laravel's collection methods to parse the logs. Instead of reading the entire file into memory at once, lazy collections may be used to keep only a small part of the file in memory at a given time: -->
예를 들어, 애플리케이션에서 수 기가바이트의 로그 파일을 처리해야 하는데, Laravel 컬렉션 메서드를 그대로 사용해서 로그 파일을 분석하고 싶다고 가정해 보겠습니다. 전체 파일을 한 번에 메모리로 읽어들이는 대신, 레이지 컬렉션을 사용하면 특정 순간 필요한 일부 데이터만 메모리에 읽어서 처리할 수 있습니다.

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
또 다른 예로, 만약 10,000개의 Eloquent 모델을 반복문으로 순회해야 하는 경우를 생각해 보세요. 일반적인 Laravel 컬렉션을 사용할 경우, 이 모든 Eloquent 모델이 한 번에 메모리로 로드됩니다.

```
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

<!-- However, the query builder's `cursor` method returns a `LazyCollection` instance. This allows you to still only run a single query against the database but also only keep one Eloquent model loaded in memory at a time. In this example, the `filter` callback is not executed until we actually iterate over each user individually, allowing for a drastic reduction in memory usage: -->
하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 사용하면 데이터베이스에 쿼리는 한 번만 실행하면서, 한 번에 하나의 Eloquent 모델만 메모리에 올릴 수 있습니다. 이 예제에서는 실제로 각 사용자(user)를 한 명씩 반복문으로 순회할 때까지 `filter` 콜백이 실행되지 않아, 메모리 사용량이 혁신적으로 줄어듭니다.

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
레이지 컬렉션 인스턴스를 만들려면, PHP 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하면 됩니다.

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
대부분의 `Collection` 클래스에서 사용할 수 있는 메서드는 `LazyCollection` 클래스에서도 사용 가능합니다. 이 두 클래스는 모두 `Illuminate\Support\Enumerable` 계약을 구현하며, 아래와 같은 메서드를 정의합니다:



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
> 컬렉션을 변경하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서는 **사용할 수 없습니다**.

<a name="lazy-collection-methods"></a>

<!-- ### Lazy Collection Methods -->
### Lazy Collection Methods

<!-- In addition to the methods defined in the `Enumerable` contract, the `LazyCollection` class contains the following methods: -->
`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에는 다음과 같은 추가 메서드들이 포함되어 있습니다.

<a name="method-takeUntilTimeout"></a>
<!-- #### `takeUntilTimeout()` -->
#### `takeUntilTimeout()`

<!-- The `takeUntilTimeout` method returns a new lazy collection that will enumerate values until the specified time. After that time, the collection will then stop enumerating: -->
`takeUntilTimeout` 메서드는 지정된 시간까지 컬렉션의 값을 순회(enumerate)하도록 동작하는 새로운 지연(lazy) 컬렉션을 반환합니다. 해당 시간이 지나면 컬렉션의 순회를 중단합니다.

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
이 메서드의 사용 예시로, 커서를 이용해 데이터베이스에서 송장(invoice)을 제출하는 애플리케이션을 상상해 보십시오. 예를 들어, 15분마다 실행되는 [scheduled task](/docs/11.x/scheduling)을 정의한 뒤, 최대 14분 동안만 송장을 처리할 수 있습니다.

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
`each` 메서드는 컬렉션의 각 항목에 대해 즉시 주어진 콜백을 호출하지만, `tapEach` 메서드는 항목이 하나씩 리스트에서 꺼내지는 시점에만 콜백을 호출합니다.

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
`throttle` 메서드는 지연(lazy) 컬렉션을 지정한 초(sec)만큼 간격을 두고 반환하게 만듭니다. 이 메서드는 외부 API와 연동하며 요청 속도를 제한해야 하는 상황(예: 외부에서 인입되는 요청의 처리 속도 제한)에서 특히 유용합니다.

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
`remember` 메서드는 이미 순회한(enumerated) 값을 기억하여, 동일한 컬렉션을 다시 순회할 때 데이터를 다시 조회하지 않고 캐시된 값을 반환하는 새로운 지연 컬렉션을 반환합니다.

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