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
`Illuminate\Support\Collection` 클래스는 데이터 배열을 다룰 때 유용한, 유연하고 편리한 래퍼를 제공합니다. 예를 들어 아래 코드를 살펴보세요. `collect` 헬퍼를 사용하여 배열로부터 새로운 컬렉션 인스턴스를 만들고, 각 요소에 대해 `strtoupper` 함수를 실행한 뒤, 비어 있는 모든 요소를 제거해 봅니다.

```
$collection = collect(['taylor', 'abigail', null])->map(function ($name) {
    return strtoupper($name);
})->reject(function ($name) {
    return empty($name);
});
```

<!-- As you can see, the `Collection` class allows you to chain its methods to perform fluent mapping and reducing of the underlying array. In general, collections are immutable, meaning every `Collection` method returns an entirely new `Collection` instance. -->
보시는 것처럼, `Collection` 클래스는 메서드 체이닝을 통해 내부 배열을 쉽게 변환하거나 축소할 수 있도록 해줍니다. 일반적으로 컬렉션은 불변(immutable)하며, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
<!-- ### Creating Collections -->
### Creating Collections

<!-- As mentioned above, the `collect` helper returns a new `Illuminate\Support\Collection` instance for the given array. So, creating a collection is as simple as: -->
앞서 언급했듯이, `collect` 헬퍼는 주어진 배열에 대해 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 즉, 컬렉션을 생성하는 것은 매우 간단합니다.

```
$collection = collect([1, 2, 3]);
```

> [!TIP]
> [Eloquent](/docs/8.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
<!-- ### Extending Collections -->
### Extending Collections

<!-- Collections are "macroable", which allows you to add additional methods to the `Collection` class at run time. The `Illuminate\Support\Collection` class' `macro` method accepts a closure that will be executed when your macro is called. The macro closure may access the collection's other methods via `$this`, just as if it were a real method of the collection class. For example, the following code adds a `toUpper` method to the `Collection` class: -->
컬렉션은 "매크로(macro)" 기능을 지원합니다. 이를 통해 런타임에 `Collection` 클래스에 추가 메서드를 정의할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행되는 클로저를 받습니다. 이 클로저 내부에서 `$this`를 통해 컬렉션의 다른 메서드에도 접근할 수 있습니다. 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가하는 예시입니다.

```
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

Collection::macro('toUpper', function () {
    return $this->map(function ($value) {
        return Str::upper($value);
    });
});

$collection = collect(['first', 'second']);

$upper = $collection->toUpper();

// ['FIRST', 'SECOND']
```

<!-- Typically, you should declare collection macros in the `boot` method of a [service provider](/docs/8.x/providers). -->
일반적으로 컬렉션 매크로는 [service provider](/docs/8.x/providers)의 `boot` 메서드에서 선언하길 권장합니다.

<a name="macro-arguments"></a>
<!-- #### Macro Arguments -->
#### Macro Arguments

<!-- If necessary, you may define macros that accept additional arguments: -->
필요하다면, 추가 인수를 받는 매크로도 정의할 수 있습니다.

```
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Lang;

Collection::macro('toLocale', function ($locale) {
    return $this->map(function ($value) use ($locale) {
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
이후 대부분의 컬렉션 관련 문서에서는 `Collection` 클래스에서 제공하는 각각의 메서드에 대해 설명합니다. 이 메서드들은 모두 체이닝이 가능하므로, 내부 배열을 유연하게 조작할 수 있습니다. 더불어, 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요한 경우 기존 컬렉션을 그대로 보존할 수 있습니다.



<!-- <div id="collection-method-list" markdown="1"> -->
<div id="collection-method-list" markdown="1">

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
[doesntContain](#method-doesntcontain)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
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
[shift](#method-shift)
[shuffle](#method-shuffle)
[sliding](#method-sliding)
[skip](#method-skip)
[skipUntil](#method-skipuntil)
[skipWhile](#method-skipwhile)
[slice](#method-slice)
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
[doesntContain](#method-doesntcontain)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
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
[shift](#method-shift)
[shuffle](#method-shuffle)
[sliding](#method-sliding)
[skip](#method-skip)
[skipUntil](#method-skipuntil)
[skipWhile](#method-skipwhile)
[slice](#method-slice)
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



<a name="method-all"></a>
<!-- #### `all()` -->
#### `all()`

<!-- The `all` method returns the underlying array represented by the collection: -->
`all` 메서드는 컬렉션이 나타내는 내부 배열을 반환합니다.

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
`avg` 메서드는 지정한 키의 [average value](https://en.wikipedia.org/wiki/Average)을 반환합니다.

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

<a name="method-chunk"></a>
<!-- #### `chunk()` -->
#### `chunk()`

<!-- The `chunk` method breaks the collection into multiple, smaller collections of a given size: -->
`chunk` 메서드는 컬렉션을 지정한 크기만큼 여러 개의 작은 컬렉션으로 분할합니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

<!-- This method is especially useful in [views](/docs/8.x/views) when working with a grid system such as [Bootstrap](https://getbootstrap.com/docs/4.1/layout/grid/). For example, imagine you have a collection of [Eloquent](/docs/8.x/eloquent) models you want to display in a grid: -->
이 메서드는 [views](/docs/8.x/views)에서 [Bootstrap](https://getbootstrap.com/docs/4.1/layout/grid/)과 같은 그리드 시스템을 사용할 때 매우 유용합니다. 예를 들어, [Eloquent](/docs/8.x/eloquent) 모델 컬렉션을 그리드 형태로 보여주고 싶을 때 다음과 같이 활용할 수 있습니다.

```
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
`chunkWhile` 메서드는 전달된 콜백의 평가 결과에 따라 컬렉션을 여러 개의 작은 컬렉션으로 분할합니다. 클로저에 전달되는 `$chunk` 변수는 이전 요소를 확인하는 데 사용할 수 있습니다.

```
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function ($value, $key, $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

<a name="method-collapse"></a>
<!-- #### `collapse()` -->
#### `collapse()`

<!-- The `collapse` method collapses a collection of arrays into a single, flat collection: -->
`collapse` 메서드는 배열로 구성된 컬렉션을 하나의 평면(flat) 컬렉션으로 합칩니다.

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

<a name="method-collect"></a>
<!-- #### `collect()` -->
#### `collect()`

<!-- The `collect` method returns a new `Collection` instance with the items currently in the collection: -->
`collect` 메서드는 컬렉션이 현재 가지고 있는 아이템으로 새로운 `Collection` 인스턴스를 반환합니다.

```
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

<!-- The `collect` method is primarily useful for converting [lazy collections](#lazy-collections) into standard `Collection` instances: -->
`collect` 메서드는 주로 [lazy collections](#lazy-collections)을 일반 `Collection` 인스턴스로 변환할 때 유용합니다.

```
$lazyCollection = LazyCollection::make(function () {
    yield 1;
    yield 2;
    yield 3;
});

$collection = $lazyCollection->collect();

get_class($collection);

// 'Illuminate\Support\Collection'

$collection->all();

// [1, 2, 3]
```

> [!TIP]
> `collect` 메서드는 `Enumerable` 인스턴스를 일반(비-지연) 컬렉션으로 변환해야 하는 경우 특히 유용합니다. `collect()`는 `Enumerable` 계약에 포함되어 있으므로, 언제든 안심하고 `Collection` 인스턴스를 얻을 수 있습니다.

<a name="method-combine"></a>
<!-- #### `combine()` -->
#### `combine()`

<!-- The `combine` method combines the values of the collection, as keys, with the values of another array or collection: -->
`combine` 메서드는 컬렉션의 값을 "키"로 사용하여, 다른 배열 또는 컬렉션의 값과 결합합니다.

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
`concat` 메서드는 주어진 `array`나 컬렉션의 값을 다른 컬렉션의 끝에 덧붙입니다.

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

<a name="method-contains"></a>
<!-- #### `contains()` -->
#### `contains()`

<!-- The `contains` method determines whether the collection contains a given item. You may pass a closure to the `contains` method to determine if an element exists in the collection matching a given truth test: -->
`contains` 메서드는 컬렉션에 특정 아이템이 포함되어 있는지를 판단합니다. `contains` 메서드에 클로저를 전달하여, 조건에 맞는 요소가 컬렉션에 존재하는지 확인할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function ($value, $key) {
    return $value > 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `contains` method to determine whether the collection contains a given item value: -->
또는, `contains` 메서드에 문자열을 전달하여 컬렉션에 해당 값이 있는지 확인할 수도 있습니다.

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

<!-- You may also pass a key / value pair to the `contains` method, which will determine if the given pair exists in the collection: -->
또한, `contains` 메서드에 키와 값의 쌍을 전달해 일치하는 페어가 컬렉션에 존재하는지 확인할 수도 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

<!-- The `contains` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [`containsStrict`](#method-containsstrict) method to filter using "strict" comparisons. -->
`contains` 메서드는 아이템 값을 확인할 때 "느슨한(loose) 비교"를 사용합니다. 즉, 값이 같다면 문자열이든 정수든 같은 값으로 간주합니다. "엄격한(strict) 비교"를 원한다면 [`containsStrict`](#method-containsstrict) 메서드를 사용하세요.

<!-- For the inverse of `contains`, see the [doesntContain](#method-doesntcontain) method. -->
`contains`의 반대 기능이 필요하다면 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsstrict"></a>
<!-- #### `containsStrict()` -->
#### `containsStrict()`

<!-- This method has the same signature as the [`contains`](#method-contains) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [`contains`](#method-contains) 메서드와 동일한 시그니처를 가지지만, 모든 값의 비교를 "엄격하게(strict)" 수행합니다.

> [!TIP]
> 이 메서드는 [Eloquent Collections](/docs/8.x/eloquent-collections#method-contains)과 함께 사용할 때 동작이 다를 수 있습니다.

<a name="method-count"></a>
<!-- #### `count()` -->
#### `count()`

<!-- The `count` method returns the total number of items in the collection: -->
`count` 메서드는 컬렉션 내 전체 아이템 수를 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
<!-- #### `countBy()` -->
#### `countBy()`

<!-- The `countBy` method counts the occurrences of values in the collection. By default, the method counts the occurrences of every element, allowing you to count certain "types" of elements in the collection: -->
`countBy` 메서드는 컬렉션 내 값의 출현 횟수를 센 결과를 반환합니다. 기본적으로 모든 요소가 몇 번 등장하는지 개수를 세어주며, 이를 통해 특정 "유형"의 요소가 컬렉션에 몇 개 있는지 셀 수 있습니다.

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

<!-- You pass a closure to the `countBy` method to count all items by a custom value: -->
`countBy` 메서드에 클로저를 전달하여, 각 요소를 원하는 값으로 매핑 후 집계할 수도 있습니다.

```
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function ($email) {
    return substr(strrchr($email, "@"), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
<!-- #### `crossJoin()` -->
#### `crossJoin()`

<!-- The `crossJoin` method cross joins the collection's values among the given arrays or collections, returning a Cartesian product with all possible permutations: -->
`crossJoin` 메서드는 컬렉션의 요소들과 주어진 배열 또는 컬렉션을 교차 결합하여, 모든 가능한 순열(카테시안 곱)을 반환합니다.

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
`dd` 메서드는 컬렉션의 아이템을 출력하고, 스크립트 실행을 종료합니다.

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
스크립트 실행을 중단하지 않고 컬렉션을 출력하려면, [`dump`](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>

<!-- #### `diff()` -->
#### `diff()`

<!-- The `diff` method compares the collection against another collection or a plain PHP `array` based on its values. This method will return the values in the original collection that are not present in the given collection: -->
`diff` 메서드는 컬렉션의 값(value)을 기준으로, 다른 컬렉션이나 일반 PHP `array`와 비교하여 원본 컬렉션에는 존재하지만 주어진 컬렉션에는 없는 값들만 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!TIP]
> [Eloquent Collections](/docs/8.x/eloquent-collections#method-diff)을 사용할 경우, 이 메서드의 동작이 다소 달라집니다.

<a name="method-diffassoc"></a>
<!-- #### `diffAssoc()` -->
#### `diffAssoc()`

<!-- The `diffAssoc` method compares the collection against another collection or a plain PHP `array` based on its keys and values. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffAssoc` 메서드는 컬렉션의 키(key)와 값(value)를 기준으로, 다른 컬렉션이나 일반 PHP `array`와 비교합니다. 이 메서드는 원본 컬렉션에 있지만 주어진 컬렉션에는 없는 키/값 쌍을 반환합니다.

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

<a name="method-diffkeys"></a>
<!-- #### `diffKeys()` -->
#### `diffKeys()`

<!-- The `diffKeys` method compares the collection against another collection or a plain PHP `array` based on its keys. This method will return the key / value pairs in the original collection that are not present in the given collection: -->
`diffKeys` 메서드는 컬렉션의 키(key)를 기준으로, 다른 컬렉션이나 일반 PHP `array`와 비교합니다. 이 메서드는 원본 컬렉션에 있지만 주어진 컬렉션에는 없는 키/값 쌍을 반환합니다.

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
`doesntContain` 메서드는 컬렉션에 특정 값이 포함되어 있지 않은지 확인합니다. `doesntContain` 메서드에 콜백(클로저)을 전달하여 주어진 조건을 만족하지 않는 요소가 컬렉션에 존재하는지 검사할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function ($value, $key) {
    return $value < 5;
});

// false
```

<!-- Alternatively, you may pass a string to the `doesntContain` method to determine whether the collection does not contain a given item value: -->
또는, `doesntContain` 메서드에 문자열을 전달하여, 해당 값이 컬렉션에 포함되어 있지 않은지 확인할 수도 있습니다.

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

<!-- You may also pass a key / value pair to the `doesntContain` method, which will determine if the given pair does not exist in the collection: -->
`doesntContain` 메서드에 키/값 쌍을 전달하면, 해당 쌍이 컬렉션에 존재하지 않는지 확인할 수 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

<!-- The `doesntContain` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. -->
`doesntContain` 메서드는 값 비교를 할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 저장된 정수 값과 진짜 정수 값이 같다고 간주합니다.

<a name="method-dump"></a>
<!-- #### `dump()` -->
#### `dump()`

<!-- The `dump` method dumps the collection's items: -->
`dump` 메서드는 컬렉션의 항목들을 즉시 화면에 출력(dump)합니다.

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
컬렉션을 출력한 후 스크립트의 실행을 중단하고 싶다면, [`dd`](#method-dd) 메서드를 대신 사용하세요.

<a name="method-duplicates"></a>
<!-- #### `duplicates()` -->
#### `duplicates()`

<!-- The `duplicates` method retrieves and returns duplicate values from the collection: -->
`duplicates` 메서드는 컬렉션 내 중복된 값을 찾아 반환합니다.

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

<!-- If the collection contains arrays or objects, you can pass the key of the attributes that you wish to check for duplicate values: -->
컬렉션에 배열이나 객체가 포함되어 있다면, 중복 값 검사를 할 속성의 키를 지정할 수 있습니다.

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
이 메서드는 [`duplicates`](#method-duplicates) 메서드와 동일한 시그니처를 가지지만, 모든 값을 "엄격(strict)" 비교로 검증합니다.

<a name="method-each"></a>
<!-- #### `each()` -->
#### `each()`

<!-- The `each` method iterates over the items in the collection and passes each item to a closure: -->
`each` 메서드는 컬렉션의 모든 항목을 반복(iterate)하면서, 각 항목을 콜백(클로저)에 전달합니다.

```
$collection->each(function ($item, $key) {
    //
});
```

<!-- If you would like to stop iterating through the items, you may return `false` from your closure: -->
반복을 중단하고 싶다면, 콜백에서 `false`를 반환하면 됩니다.

```
$collection->each(function ($item, $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
<!-- #### `eachSpread()` -->
#### `eachSpread()`

<!-- The `eachSpread` method iterates over the collection's items, passing each nested item value into the given callback: -->
`eachSpread` 메서드는 컬렉션의 각 항목(중첩 배열의 경우)을 풀어서, 콜백에 전달합니다.

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function ($name, $age) {
    //
});
```

<!-- You may stop iterating through the items by returning `false` from the callback: -->
콜백에서 `false`를 반환하면 반복을 중단할 수 있습니다.

```
$collection->eachSpread(function ($name, $age) {
    return false;
});
```

<a name="method-every"></a>
<!-- #### `every()` -->
#### `every()`

<!-- The `every` method may be used to verify that all elements of a collection pass a given truth test: -->
`every` 메서드는 컬렉션의 모든 요소가 주어진 조건을 만족하는지 검사합니다.

```
collect([1, 2, 3, 4])->every(function ($value, $key) {
    return $value > 2;
});

// false
```

<!-- If the collection is empty, the `every` method will return true: -->
컬렉션이 비어 있는 경우에는 `every` 메서드는 true를 반환합니다.

```
$collection = collect([]);

$collection->every(function ($value, $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
<!-- #### `except()` -->
#### `except()`

<!-- The `except` method returns all items in the collection except for those with the specified keys: -->
`except` 메서드는 지정된 키를 제외한 모든 항목을 반환합니다.

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

<!-- For the inverse of `except`, see the [only](#method-only) method. -->
`except`의 반대 동작을 원한다면 [only](#method-only) 메서드를 참고하세요.

> [!TIP]
> [Eloquent Collections](/docs/8.x/eloquent-collections#method-except)을 사용할 경우, 이 메서드의 동작이 다소 달라집니다.

<a name="method-filter"></a>
<!-- #### `filter()` -->
#### `filter()`

<!-- The `filter` method filters the collection using the given callback, keeping only those items that pass a given truth test: -->
`filter` 메서드는 주어진 콜백(조건)을 사용하여, 조건을 통과한 항목만 남기고 컬렉션을 필터링합니다.

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function ($value, $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

<!-- If no callback is supplied, all entries of the collection that are equivalent to `false` will be removed: -->
콜백을 전달하지 않으면, `false`로 간주되는 컬렉션의 모든 항목이 제거됩니다.

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
`first` 메서드는 주어진 조건을 만족하는 컬렉션의 첫 번째 요소를 반환합니다.

```
collect([1, 2, 3, 4])->first(function ($value, $key) {
    return $value > 2;
});

// 3
```

<!-- You may also call the `first` method with no arguments to get the first element in the collection. If the collection is empty, `null` is returned: -->
인수 없이 `first` 메서드를 호출하면 컬렉션의 첫 번째 요소를 반환합니다. 컬렉션이 비어 있으면 `null`을 반환합니다.

```
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-where"></a>
<!-- #### `firstWhere()` -->
#### `firstWhere()`

<!-- The `firstWhere` method returns the first element in the collection with the given key / value pair: -->
`firstWhere` 메서드는 지정한 키/값 쌍과 일치하는 컬렉션의 첫 번째 요소를 반환합니다.

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
[where](#method-where) 메서드와 마찬가지로, `firstWhere` 메서드에 인수를 하나만 전달할 수도 있습니다. 이 경우 `firstWhere` 메서드는 해당 키가 "참(truthy)"인 첫 번째 항목을 반환합니다.

```
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
<!-- #### `flatMap()` -->
#### `flatMap()`

<!-- The `flatMap` method iterates through the collection and passes each value to the given closure. The closure is free to modify the item and return it, thus forming a new collection of modified items. Then, the array is flattened by one level: -->
`flatMap` 메서드는 컬렉션의 각 값을 주어진 콜백에 전달하여 값을 수정할 수 있으며, 이후 반환된 모든 배열을 1차원으로 평탄화(flatten)해서 새로운 컬렉션을 만듭니다.

```
$collection = collect([
    ['name' => 'Sally'],
    ['school' => 'Arkansas'],
    ['age' => 28]
]);

$flattened = $collection->flatMap(function ($values) {
    return array_map('strtoupper', $values);
});

$flattened->all();

// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];
```

<a name="method-flatten"></a>
<!-- #### `flatten()` -->
#### `flatten()`

<!-- The `flatten` method flattens a multi-dimensional collection into a single dimension: -->
`flatten` 메서드는 다차원(중첩) 컬렉션을 단일 차원 1차원 배열로 변환합니다.

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
필요하다면 `flatten` 메서드에 "depth"(깊이) 인수를 넘겨 몇 단계까지 평탄화할지 지정할 수도 있습니다.

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
이 예제에서 `flatten`을 depth 없이 호출하면 중첩 배열까지 모두 1차원으로 만들어 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']` 형태가 됩니다. depth 인수를 사용하면 몇 단계까지만 평탄화할지 조절할 수 있습니다.

<a name="method-flip"></a>
<!-- #### `flip()` -->
#### `flip()`

<!-- The `flip` method swaps the collection's keys with their corresponding values: -->
`flip` 메서드는 컬렉션의 키와 값을 서로 맞바꿉니다.

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
`forget` 메서드는 지정한 키를 가진 항목을 컬렉션에서 제거합니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$collection->forget('name');

$collection->all();

// ['framework' => 'laravel']
```

> [!NOTE]
> 대부분의 컬렉션 메서드와 달리, `forget` 메서드는 새로운 컬렉션을 반환하지 않고, 호출된 컬렉션 자체를 수정합니다.

<a name="method-forpage"></a>
<!-- #### `forPage()` -->
#### `forPage()`

<!-- The `forPage` method returns a new collection containing the items that would be present on a given page number. The method accepts the page number as its first argument and the number of items to show per page as its second argument: -->
`forPage` 메서드는 지정한 페이지 번호에 해당하는 항목들만으로 새로운 컬렉션을 반환합니다. 첫 번째 인수는 페이지 번호, 두 번째 인수는 한 페이지에 보여줄 항목 개수입니다.

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
`get` 메서드는 지정한 키에 해당하는 값을 반환합니다. 키가 존재하지 않으면 `null`을 반환합니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

<!-- You may optionally pass a default value as the second argument: -->
두 번째 인수로 기본값을 지정할 수 있습니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('age', 34);

// 34
```

<!-- You may even pass a callback as the method's default value. The result of the callback will be returned if the specified key does not exist: -->
기본값 대신 콜백을 지정하면, 키가 존재하지 않을 때 콜백 결과를 반환합니다.

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
`groupBy` 메서드는 컬렉션의 항목을 지정한 키로 묶어서 그룹화합니다.

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
문자열 `key` 대신 콜백을 전달해서, 원하는 형태로 그룹화할 수도 있습니다. 콜백에서 반환하는 값이 그룹핑에 사용됩니다.

```
$grouped = $collection->groupBy(function ($item, $key) {
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
여러 기준으로 그룹화하고 싶을 때는 배열로 그룹화 기준을 전달할 수 있습니다. 배열의 각 요소는 다차원 컬렉션의 각 계층에 적용됩니다.

```
$data = new Collection([
    10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
    20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
    30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
    40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
]);

$result = $data->groupBy(['skill', function ($item) {
    return $item['roles'];
}], $preserveKeys = true);

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
`has` 메서드는 컬렉션에 지정한 키가 존재하는지 확인합니다.

```
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->has('product');

// true

$collection->has(['product', 'amount']);

// true

$collection->has(['amount', 'price']);

// false
```

<a name="method-implode"></a>
<!-- #### `implode()` -->
#### `implode()`

<!-- The `implode` method joins items in a collection. Its arguments depend on the type of items in the collection. If the collection contains arrays or objects, you should pass the key of the attributes you wish to join, and the "glue" string you wish to place between the values: -->
`implode` 메서드는 컬렉션의 항목들을 하나의 문자열로 결합합니다. 컬렉션에 어떤 타입의 값들이 포함되어 있는지에 따라 인자 전달 방식이 다릅니다. 컬렉션이 배열이나 객체를 포함하고 있다면, 합칠 속성의 키와 값을 이어줄 문자열(Glue)을 차례로 지정해야 합니다.

```
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// Desk, Chair
```

<!-- If the collection contains simple strings or numeric values, you should pass the "glue" as the only argument to the method: -->
컬렉션이 단순한 문자열이나 숫자값만을 가지고 있다면 메서드의 유일한 인자로 Glue 문자열만 전달하면 됩니다.

```
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

<a name="method-intersect"></a>
<!-- #### `intersect()` -->
#### `intersect()`

<!-- The `intersect` method removes any values from the original collection that are not present in the given `array` or collection. The resulting collection will preserve the original collection's keys: -->
`intersect` 메서드는 전달받은 `array` 또는 컬렉션에 존재하지 않는 값을 원본 컬렉션에서 제거합니다. 반환되는 컬렉션은 원래의 키를 그대로 유지합니다.

```
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!TIP]
> [Eloquent Collections](/docs/8.x/eloquent-collections#method-intersect)을 사용할 경우, 이 메서드의 동작이 달라집니다.

<a name="method-intersectbykeys"></a>
<!-- #### `intersectByKeys()` -->
#### `intersectByKeys()`

<!-- The `intersectByKeys` method removes any keys and their corresponding values from the original collection that are not present in the given `array` or collection: -->
`intersectByKeys` 메서드는 원본 컬렉션의 키 중에서, 전달받은 `array` 또는 컬렉션에 존재하지 않는 키와 해당 값을 모두 제거합니다.

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
`isEmpty` 메서드는 컬렉션이 비어있으면 `true`를 반환하고, 비어있지 않으면 `false`를 반환합니다.

```
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
<!-- #### `isNotEmpty()` -->
#### `isNotEmpty()`

<!-- The `isNotEmpty` method returns `true` if the collection is not empty; otherwise, `false` is returned: -->
`isNotEmpty` 메서드는 컬렉션이 비어있지 않으면 `true`, 그렇지 않으면 `false`를 반환합니다.

```
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
<!-- #### `join()` -->
#### `join()`

<!-- The `join` method joins the collection's values with a string. Using this method's second argument, you may also specify how the final element should be appended to the string: -->
`join` 메서드는 컬렉션의 값들을 지정한 문자열로 연결합니다. 두 번째 인자를 사용하면 최종 요소를 문자열에 지정한 형식으로 붙일 수 있습니다.

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
`keyBy` 메서드는 지정한 키의 값을 기준으로 컬렉션의 키를 재설정합니다. 동일한 키가 여러 번 등장하면 마지막 항목만 포함됩니다.

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
이 메서드에는 콜백 함수를 전달할 수도 있습니다. 콜백이 반환하는 값이 새로운 컬렉션의 키로 사용됩니다.

```
$keyed = $collection->keyBy(function ($item) {
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
`keys` 메서드는 컬렉션의 모든 키 값을 반환합니다.

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
`last` 메서드는 주어진 조건을 통과하는 컬렉션의 마지막 요소를 반환합니다.

```
collect([1, 2, 3, 4])->last(function ($value, $key) {
    return $value < 3;
});

// 2
```

<!-- You may also call the `last` method with no arguments to get the last element in the collection. If the collection is empty, `null` is returned: -->
인자를 전달하지 않고 `last` 메서드를 호출하면 컬렉션의 마지막 요소를 반환합니다. 컬렉션이 비어 있으면 `null`을 반환합니다.

```
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-macro"></a>
<!-- #### `macro()` -->
#### `macro()`

<!-- The static `macro` method allows you to add methods to the `Collection` class at run time. Refer to the documentation on [extending collections](#extending-collections) for more information. -->
정적 메서드인 `macro`를 사용하면 런타임에 `Collection` 클래스에 새로운 메서드를 추가할 수 있습니다. 자세한 내용은 [extending collections](#extending-collections) 문서를 참고하세요.

<a name="method-make"></a>
<!-- #### `make()` -->
#### `make()`

<!-- The static `make` method creates a new collection instance. See the [Creating Collections](#creating-collections) section. -->
정적 `make` 메서드는 새로운 컬렉션 인스턴스를 만듭니다. 자세한 내용은 [Creating Collections](#creating-collections) 섹션을 참고하세요.

<a name="method-map"></a>
<!-- #### `map()` -->
#### `map()`

<!-- The `map` method iterates through the collection and passes each value to the given callback. The callback is free to modify the item and return it, thus forming a new collection of modified items: -->
`map` 메서드는 컬렉션을 순회하면서 각 값을 지정한 콜백에 전달합니다. 콜백에서는 항목을 수정한 후 반환할 수 있으며, 수정된 항목의 새 컬렉션이 만들어집니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function ($item, $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!NOTE]
> 대부분의 컬렉션 메서드와 마찬가지로, `map`은 새로운 컬렉션 인스턴스를 반환합니다. 원본 컬렉션은 변경되지 않습니다. 원본 컬렉션 자체를 변환하려면 [`transform`](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
<!-- #### `mapInto()` -->
#### `mapInto()`

<!-- The `mapInto()` method iterates over the collection, creating a new instance of the given class by passing the value into the constructor: -->
`mapInto()` 메서드는 컬렉션을 순회하면서 각 값을 지정한 클래스의 생성자에 전달하여 새로운 인스턴스를 만듭니다.

```
class Currency
{
    /**
     * Create a new currency instance.
     *
     * @param  string  $code
     * @return void
     */
    function __construct(string $code)
    {
        $this->code = $code;
    }
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
`mapSpread` 메서드는 컬렉션 항목 각각의 내부 값(중첩된 값들)을 지정한 클로저에 전달하여 순회합니다. 클로저에서 항목을 자유롭게 변형해 반환하고, 결과로 새 컬렉션이 만들어집니다.

```
$collection = collect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunks = $collection->chunk(2);

$sequence = $chunks->mapSpread(function ($even, $odd) {
    return $even + $odd;
});

$sequence->all();

// [1, 5, 9, 13, 17]
```

<a name="method-maptogroups"></a>
<!-- #### `mapToGroups()` -->
#### `mapToGroups()`

<!-- The `mapToGroups` method groups the collection's items by the given closure. The closure should return an associative array containing a single key / value pair, thus forming a new collection of grouped values: -->
`mapToGroups` 메서드는 지정한 클로저를 사용하여 컬렉션 항목들을 그룹으로 묶습니다. 클로저는 반드시 하나의 키/값 쌍을 가진 연관 배열을 반환해야 하며, 그 결과로 새로운 그룹화된 컬렉션이 생성됩니다.

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

$grouped = $collection->mapToGroups(function ($item, $key) {
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
`mapWithKeys` 메서드는 컬렉션을 순회하면서 각 값을 지정한 콜백에 전달합니다. 콜백은 반드시 하나의 키/값 쌍이 포함된 연관 배열을 반환해야 합니다.

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

$keyed = $collection->mapWithKeys(function ($item, $key) {
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
`max` 메서드는 지정한 키에 대해 가장 큰 값을 반환합니다.

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
`median` 메서드는 주어진 키에 대해 [median value](https://en.wikipedia.org/wiki/Median)을 반환합니다.

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

<!-- The `merge` method merges the given array or collection with the original collection. If a string key in the given items matches a string key in the original collection, the given items's value will overwrite the value in the original collection: -->
`merge` 메서드는 전달된 배열이나 컬렉션을 원래 컬렉션과 병합합니다. 만약 전달된 항목과 원래 컬렉션에 동일한 문자열 키가 있다면, 전달된 항목의 값이 원본 값을 덮어씁니다.

```
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

<!-- If the given items's keys are numeric, the values will be appended to the end of the collection: -->
만약 전달된 항목의 키가 숫자인 경우, 해당 값이 컬렉션의 마지막에 추가됩니다.

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
`mergeRecursive` 메서드는 전달된 배열이나 컬렉션을 원래 컬렉션과 **재귀적으로** 병합합니다. 만약 전달된 항목과 기존 컬렉션에 동일한 문자열 키가 있으면, 그 값들이 배열로 병합되고, 이 과정이 재귀적으로 반복됩니다.

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
`min` 메서드는 지정한 키에 대해 가장 작은 값을 반환합니다.

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
`mode` 메서드는 주어진 키에 대해 [mode value](https://en.wikipedia.org/wiki/Mode_(statistics))을 반환합니다.

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

<a name="method-nth"></a>
<!-- #### `nth()` -->
#### `nth()`

<!-- The `nth` method creates a new collection consisting of every n-th element: -->
`nth` 메서드는 컬렉션에서 n번째마다 하나씩만 포함하는 새로운 컬렉션을 만듭니다.

```
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

<!-- You may optionally pass a starting offset as the second argument: -->
옵션으로 두 번째 인자에 시작 오프셋을 줄 수 있습니다.

```
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
<!-- #### `only()` -->
#### `only()`

<!-- The `only` method returns the items in the collection with the specified keys: -->
`only` 메서드는 지정한 키에 해당하는 값만 포함하는 컬렉션을 반환합니다.

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
`only`의 반대 동작은 [except](#method-except) 메서드를 참고하세요.

> [!TIP]
> [Eloquent Collections](/docs/8.x/eloquent-collections#method-only)을 사용할 경우, 이 메서드의 동작이 달라집니다.

<a name="method-pad"></a>
<!-- #### `pad()` -->
#### `pad()`

<!-- The `pad` method will fill the array with the given value until the array reaches the specified size. This method behaves like the [array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP function. -->
`pad` 메서드는 배열의 크기가 지정한 길이에 도달할 때까지 지정한 값으로 배열을 채웁니다. 이 메서드는 PHP의 [array_pad](https://secure.php.net/manual/en/function.array-pad.php) 함수와 유사하게 동작합니다.

<!-- To pad to the left, you should specify a negative size. No padding will take place if the absolute value of the given size is less than or equal to the length of the array: -->
왼쪽으로 채우고 싶다면 음수 크기를 지정하세요. 절대값이 배열 길이보다 작거나 같으면 패딩이 적용되지 않습니다.

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
`partition` 메서드는 PHP 배열 구조 분해(destructuring)와 결합하여, 지정한 조건을 통과하는 요소와 그렇지 않은 요소를 나누어 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5, 6]);

[$underThree, $equalOrAboveThree] = $collection->partition(function ($i) {
    return $i < 3;
});

$underThree->all();

// [1, 2]

$equalOrAboveThree->all();

// [3, 4, 5, 6]
```

<a name="method-pipe"></a>
<!-- #### `pipe()` -->
#### `pipe()`

<!-- The `pipe` method passes the collection to the given closure and returns the result of the executed closure: -->
`pipe` 메서드는 컬렉션 전체를 지정한 클로저에 전달하고, 클로저의 실행 결과를 반환합니다.

```
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function ($collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>

<!-- #### `pipeInto()` -->
#### `pipeInto()`

<!-- The `pipeInto` method creates a new instance of the given class and passes the collection into the constructor: -->
`pipeInto` 메서드는 지정된 클래스의 새 인스턴스를 생성하고, 컬렉션을 해당 생성자에 전달합니다.

```
class ResourceCollection
{
    /**
     * The Collection instance.
     */
    public $collection;

    /**
     * Create a new ResourceCollection instance.
     *
     * @param  Collection  $collection
     * @return void
     */
    public function __construct(Collection $collection)
    {
        $this->collection = $collection;
    }
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
`pipeThrough` 메서드는 컬렉션을 전달된 클로저(익명 함수) 배열에 순서대로 전달하면서 실행한 결과를 반환합니다.

```
$collection = collect([1, 2, 3]);

$result = $collection->pipeThrough([
    function ($collection) {
        return $collection->merge([4, 5]);
    },
    function ($collection) {
        return $collection->sum();
    },
]);

// 15
```

<a name="method-pluck"></a>
<!-- #### `pluck()` -->
#### `pluck()`

<!-- The `pluck` method retrieves all of the values for a given key: -->
`pluck` 메서드는 지정한 키에 해당하는 모든 값을 추출합니다.

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
결과로 반환되는 컬렉션의 키를 직접 지정할 수도 있습니다.

```
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

<!-- The `pluck` method also supports retrieving nested values using "dot" notation: -->
`pluck` 메서드는 "점 표기법"을 사용하여 중첩된 값도 추출할 수 있습니다.

```
$collection = collect([
    [
        'speakers' => [
            'first_day' => ['Rosa', 'Judith'],
            'second_day' => ['Angela', 'Kathleen'],
        ],
    ],
]);

$plucked = $collection->pluck('speakers.first_day');

$plucked->all();

// ['Rosa', 'Judith']
```

<!-- If duplicate keys exist, the last matching element will be inserted into the plucked collection: -->
만약 중복된 키가 존재할 경우, 마지막에 일치하는 요소가 최종적으로 pluck된 컬렉션에 포함됩니다.

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
`pop` 메서드는 컬렉션의 마지막 항목을 제거하고 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

<!-- You may pass an integer to the `pop` method to remove and return multiple items from the end of a collection: -->
`pop` 메서드에 정수를 전달하면, 컬렉션의 끝에서 여러 개의 아이템을 제거하여 반환할 수 있습니다.

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
`prepend` 메서드는 컬렉션의 맨 앞에 아이템을 추가합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

<!-- You may also pass a second argument to specify the key of the prepended item: -->
두 번째 인자로 추가될 아이템의 키를 지정할 수도 있습니다.

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
`pull` 메서드는 지정한 키에 해당하는 아이템을 컬렉션에서 제거하고 반환합니다.

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
`push` 메서드는 컬렉션의 끝에 아이템을 추가합니다.

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
`put` 메서드는 컬렉션에 지정한 키와 값을 설정합니다.

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
`random` 메서드는 컬렉션에서 임의의 아이템을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (retrieved randomly)
```

<!-- You may pass an integer to `random` to specify how many items you would like to randomly retrieve. A collection of items is always returned when explicitly passing the number of items you wish to receive: -->
`random`에 정수를 인자로 전달하면, 해당 개수만큼 임의의 아이템을 추출하여 컬렉션 형태로 반환합니다. 요청한 개수를 명시적으로 전달하면, 항상 여러 개의 아이템을 담은 컬렉션이 반환됩니다.

```
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (retrieved randomly)
```

<!-- If the collection instance has fewer items than requested, the `random` method will throw an `InvalidArgumentException`. -->
컬렉션의 아이템 개수가 요청한 개수보다 적으면, `random` 메서드는 `InvalidArgumentException`을 발생시킵니다.

<a name="method-range"></a>
<!-- #### `range()` -->
#### `range()`

<!-- The `range` method returns a collection containing integers between the specified range: -->
`range` 메서드는 지정한 범위 내의 정수들을 담은 컬렉션을 반환합니다.

```
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
<!-- #### `reduce()` -->
#### `reduce()`

<!-- The `reduce` method reduces the collection to a single value, passing the result of each iteration into the subsequent iteration: -->
`reduce` 메서드는 컬렉션을 단일 값으로 압축하며, 각 반복에서 결과를 다음 반복에 전달합니다.

```
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function ($carry, $item) {
    return $carry + $item;
});

// 6
```

<!-- The value for `$carry` on the first iteration is `null`; however, you may specify its initial value by passing a second argument to `reduce`: -->
첫 번째 반복에서 `$carry`의 값은 `null`이지만, `reduce`에 두 번째 인자를 전달하여 초기값을 지정할 수 있습니다.

```
$collection->reduce(function ($carry, $item) {
    return $carry + $item;
}, 4);

// 10
```

<!-- The `reduce` method also passes array keys in associative collections to the given callback: -->
`reduce` 메서드는 연관 배열 컬렉션에서는 배열 키도 콜백 함수에 전달합니다.

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

$collection->reduce(function ($carry, $value, $key) use ($ratio) {
    return $carry + ($value * $ratio[$key]);
});

// 4264
```

<a name="method-reduce-spread"></a>
<!-- #### `reduceSpread()` -->
#### `reduceSpread()`

<!-- The `reduceSpread` method reduces the collection to an array of values, passing the results of each iteration into the subsequent iteration. This method is similar to the `reduce` method; however, it can accept multiple initial values: -->
`reduceSpread` 메서드는 컬렉션을 값 배열로 압축하며, 각 반복에서 나온 결과들을 다음 반복에 전달합니다. `reduce` 메서드와 유사하지만, 이 메서드는 여러 개의 초기값을 받을 수 있습니다.

```php
[$creditsRemaining, $batch] = Image::where('status', 'unprocessed')
        ->get()
        ->reduceSpread(function ($creditsRemaining, $batch, $image) {
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
`reject` 메서드는 전달된 클로저로 컬렉션을 필터링합니다. 클로저가 `true`를 반환하는 항목은 결과 컬렉션에서 제거됩니다.

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function ($value, $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

<!-- For the inverse of the `reject` method, see the [`filter`](#method-filter) method. -->
`reject` 메서드의 반대 동작이 필요한 경우 [`filter`](#method-filter) 메서드를 참고하세요.

<a name="method-replace"></a>
<!-- #### `replace()` -->
#### `replace()`

<!-- The `replace` method behaves similarly to `merge`; however, in addition to overwriting matching items that have string keys, the `replace` method will also overwrite items in the collection that have matching numeric keys: -->
`replace` 메서드는 `merge`와 비슷하게 동작하지만, 문자열 키가 일치하는 항목을 덮어쓰는 것 외에도, `replace` 메서드는 숫자 키가 일치하는 컬렉션 항목도 덮어씁니다.

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
이 메서드는 `replace`와 유사하지만, 배열 내부로 들어가 중첩된 값에도 동일한 방식의 대체 작업을 재귀적으로 적용합니다.

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
`reverse` 메서드는 컬렉션의 아이템 순서를 뒤집되, 각 요소의 원래 키는 유지합니다.

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
`search` 메서드는 전달된 값을 컬렉션에서 찾아, 발견하면 해당 키를 반환합니다. 값이 없으면 `false`를 반환합니다.

```
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

<!-- The search is done using a "loose" comparison, meaning a string with an integer value will be considered equal to an integer of the same value. To use "strict" comparison, pass `true` as the second argument to the method: -->
검색은 "느슨한 비교(loose comparison)"로 이루어집니다. 즉, 문자열로 표현된 정수 값과 실제 정수값이 같으면 일치합니다. "엄격한 비교(strict comparison)"를 원하면 두 번째 인자로 `true`를 전달하면 됩니다.

```
collect([2, 4, 6, 8])->search('4', $strict = true);

// false
```

<!-- Alternatively, you may provide your own closure to search for the first item that passes a given truth test: -->
또는 원하는 조건을 통과하는 첫 아이템을 검색하기 위해 직접 클로저를 전달할 수도 있습니다.

```
collect([2, 4, 6, 8])->search(function ($item, $key) {
    return $item > 5;
});

// 2
```

<a name="method-shift"></a>
<!-- #### `shift()` -->
#### `shift()`

<!-- The `shift` method removes and returns the first item from the collection: -->
`shift` 메서드는 컬렉션에서 첫 번째 아이템을 제거하고 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

<!-- You may pass an integer to the `shift` method to remove and return multiple items from the beginning of a collection: -->
`shift` 메서드에 정수를 전달하면, 컬렉션의 앞부분에서 여러 개의 아이템을 제거하여 반환합니다.

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
`shuffle` 메서드는 컬렉션의 아이템 순서를 무작위로 섞어서 새로운 컬렉션을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-sliding"></a>
<!-- #### `sliding()` -->
#### `sliding()`

<!-- The `sliding` method returns a new collection of chunks representing a "sliding window" view of the items in the collection: -->
`sliding` 메서드는 컬렉션의 아이템을 "슬라이딩 윈도우" 형태로 잘라낸 조각들의 새로운 컬렉션을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

<!-- This is especially useful in conjunction with the [`eachSpread`](#method-eachspread) method: -->
이 메서드는 [`eachSpread`](#method-eachspread)와 함께 사용하면 특히 유용합니다.

```
$transactions->sliding(2)->eachSpread(function ($previous, $current) {
    $current->total = $previous->total + $current->amount;
});
```

<!-- You may optionally pass a second "step" value, which determines the distance between the first item of every chunk: -->
두 번째 인자로 "step" 값을 지정하면, 각 조각의 시작점 간의 간격을 조절할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-skip"></a>
<!-- #### `skip()` -->
#### `skip()`

<!-- The `skip` method returns a new collection, with the given number of elements removed from the beginning of the collection: -->
`skip` 메서드는 컬렉션의 앞에서 지정한 개수만큼 요소를 제거하고, 나머지 아이템으로 새로운 컬렉션을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
<!-- #### `skipUntil()` -->
#### `skipUntil()`

<!-- The `skipUntil` method skips over items from the collection until the given callback returns `true` and then returns the remaining items in the collection as a new collection instance: -->
`skipUntil` 메서드는 전달된 콜백이 `true`를 반환할 때까지 컬렉션의 아이템을 건너뛰고, 이후 남은 아이템들로 새로운 컬렉션 인스턴스를 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function ($item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

<!-- You may also pass a simple value to the `skipUntil` method to skip all items until the given value is found: -->
`skipUntil` 메서드에 값 자체를 전달하여, 해당 값이 등장할 때까지 모든 아이템을 건너뛸 수도 있습니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!NOTE]
> 전달된 값이 발견되지 않거나 콜백이 한 번도 `true`를 반환하지 않으면, `skipUntil` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>

<!-- #### `skipWhile()` -->
#### `skipWhile()`

<!-- The `skipWhile` method skips over items from the collection while the given callback returns `true` and then returns the remaining items in the collection as a new collection: -->
`skipWhile` 메서드는 주어진 콜백이 `true`를 반환하는 동안 컬렉션의 항목을 건너뛰고, 이후 남은 항목들로 새로운 컬렉션을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function ($item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!NOTE]
> 콜백이 한 번도 `false`를 반환하지 않으면, `skipWhile` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
<!-- #### `slice()` -->
#### `slice()`

<!-- The `slice` method returns a slice of the collection starting at the given index: -->
`slice` 메서드는 지정한 인덱스부터 컬렉션의 일부 구간을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

<!-- If you would like to limit the size of the returned slice, pass the desired size as the second argument to the method: -->
반환되는 구간의 크기를 제한하고 싶다면, 두 번째 인수로 원하는 크기를 지정할 수 있습니다.

```
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

<!-- The returned slice will preserve keys by default. If you do not wish to preserve the original keys, you can use the [`values`](#method-values) method to reindex them. -->
기본적으로 반환되는 구간은 원본 키를 보존합니다. 원본 키가 필요하지 않다면 [`values`](#method-values) 메서드를 사용해 키 값을 재설정할 수 있습니다.

<a name="method-sole"></a>
<!-- #### `sole()` -->
#### `sole()`

<!-- The `sole` method returns the first element in the collection that passes a given truth test, but only if the truth test matches exactly one element: -->
`sole` 메서드는 주어진 조건을 만족하는 첫 번째 요소를 반환하되, 반드시 그 조건을 딱 하나의 요소만이 만족해야 합니다.

```
collect([1, 2, 3, 4])->sole(function ($value, $key) {
    return $value === 2;
});

// 2
```

<!-- You may also pass a key / value pair to the `sole` method, which will return the first element in the collection that matches the given pair, but only if it exactly one element matches: -->
`sole` 메서드에는 키/값 쌍을 인수로 전달할 수도 있습니다. 이 경우 주어진 키/값 쌍과 정확히 일치하는 요소가 하나만 존재할 때 해당 요소를 반환합니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

<!-- Alternatively, you may also call the `sole` method with no argument to get the first element in the collection if there is only one element: -->
또한, 컬렉션에 요소가 하나만 있을 때는 인수 없이 `sole` 메서드를 호출해 유일한 요소를 반환받을 수도 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

<!-- If there are no elements in the collection that should be returned by the `sole` method, an `\Illuminate\Collections\ItemNotFoundException` exception will be thrown. If there is more than one element that should be returned, an `\Illuminate\Collections\MultipleItemsFoundException` will be thrown. -->
`sole` 메서드가 반환할 요소가 컬렉션에 존재하지 않으면 `\Illuminate\Collections\ItemNotFoundException` 예외가 발생합니다. 반환해야 할 요소가 둘 이상일 경우에는 `\Illuminate\Collections\MultipleItemsFoundException` 예외가 발생합니다.

<a name="method-some"></a>
<!-- #### `some()` -->
#### `some()`

<!-- Alias for the [`contains`](#method-contains) method. -->
이 메서드는 [`contains`](#method-contains) 메서드의 별명(alias)입니다.

<a name="method-sort"></a>
<!-- #### `sort()` -->
#### `sort()`

<!-- The `sort` method sorts the collection. The sorted collection keeps the original array keys, so in the following example we will use the [`values`](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sort` 메서드는 컬렉션을 정렬합니다. 정렬된 컬렉션은 기존 배열의 키를 그대로 유지하므로, 아래 예시처럼 [`values`](#method-values) 메서드로 연속된 키 인덱스로 다시 정렬할 수 있습니다.

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

<!-- If your sorting needs are more advanced, you may pass a callback to `sort` with your own algorithm. Refer to the PHP documentation on [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters), which is what the collection's `sort` method calls utilizes internally. -->
더 복잡한 정렬이 필요하다면, `sort`에 콜백을 전달해 직접 정렬 알고리즘을 구현할 수 있습니다. 컬렉션의 `sort` 메서드는 내부적으로 PHP의 [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) 함수를 사용합니다.

> [!TIP]
> 중첩 배열이나 객체로 구성된 컬렉션을 정렬해야 하는 경우, [`sortBy`](#method-sortby) 및 [`sortByDesc`](#method-sortbydesc) 메서드를 참고하세요.

<a name="method-sortby"></a>
<!-- #### `sortBy()` -->
#### `sortBy()`

<!-- The `sortBy` method sorts the collection by the given key. The sorted collection keeps the original array keys, so in the following example we will use the [`values`](#method-values) method to reset the keys to consecutively numbered indexes: -->
`sortBy` 메서드는 주어진 키를 기준으로 컬렉션을 정렬합니다. 정렬 결과 역시 기존 배열의 키를 유지하므로, [`values`](#method-values) 메서드로 연속된 인덱스로 변환할 수 있습니다.

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
`sortBy` 메서드는 두 번째 인수로 [sort flags](https://www.php.net/manual/en/function.sort.php)를 받을 수 있습니다.

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
또한, 정렬 기준을 직접 정의하고 싶다면 클로저를 전달할 수도 있습니다.

```
$collection = collect([
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$sorted = $collection->sortBy(function ($product, $key) {
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
여러 속성(attribute)을 기준으로 복합 정렬을 하려면, 정렬 조건 배열을 `sortBy` 메서드에 전달할 수 있습니다. 각 정렬 조건은 속성과 정렬 방향('asc' 또는 'desc')을 포함하는 배열로 작성합니다.

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
이처럼 여러 속성 기준으로 정렬할 때는, 각 정렬 조건에 클로저를 사용할 수도 있습니다.

```
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    fn ($a, $b) => $a['name'] <=> $b['name'],
    fn ($a, $b) => $b['age'] <=> $a['age'],
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
이 메서드는 [`sortBy`](#method-sortby) 메서드와 동일한 방법으로 동작하지만, 정렬 결과가 반대 순서(내림차순)로 반환됩니다.

<a name="method-sortdesc"></a>
<!-- #### `sortDesc()` -->
#### `sortDesc()`

<!-- This method will sort the collection in the opposite order as the [`sort`](#method-sort) method: -->
이 메서드는 [`sort`](#method-sort) 메서드와 반대로, 컬렉션을 내림차순으로 정렬합니다.

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

<!-- Unlike `sort`, you may not pass a closure to `sortDesc`. Instead, you should use the [`sort`](#method-sort) method and invert your comparison. -->
`sort`와 달리, `sortDesc`에는 클로저를 전달할 수 없습니다. 직접 비교 연산을 수행해야 한다면 [`sort`](#method-sort) 메서드를 사용해 비교 연산을 반대로 구현하시기 바랍니다.

<a name="method-sortkeys"></a>
<!-- #### `sortKeys()` -->
#### `sortKeys()`

<!-- The `sortKeys` method sorts the collection by the keys of the underlying associative array: -->
`sortKeys` 메서드는 컬렉션의 연관 배열에서 키를 기준으로 정렬합니다.

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
이 메서드는 [`sortKeys`](#method-sortkeys) 메서드와 동일한 방식으로 동작하지만, 키를 내림차순으로 정렬합니다.

<a name="method-sortkeysusing"></a>
<!-- #### `sortKeysUsing()` -->
#### `sortKeysUsing()`

<!-- The `sortKeysUsing` method sorts the collection by the keys of the underlying associative array using a callback: -->
`sortKeysUsing` 메서드는 콜백 함수를 사용해 컬렉션의 연관 배열 키를 기준으로 정렬합니다.

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
여기서 콜백 함수는 0보다 작거나, 같거나, 크거나의 정수값을 반환해야 하는 비교 함수여야 합니다. 자세한 내용은 PHP 공식 문서의 [`uksort`](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters)를 참고하세요. 이 함수는 내부적으로 `sortKeysUsing` 메서드에서도 사용됩니다.

<a name="method-splice"></a>
<!-- #### `splice()` -->
#### `splice()`

<!-- The `splice` method removes and returns a slice of items starting at the specified index: -->
`splice` 메서드는 지정된 인덱스부터 항목들을 제거해 그 구간의 컬렉션을 반환하고, 원본 컬렉션에서는 해당 항목들이 삭제됩니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

<!-- You may pass a second argument to limit the size of the resulting collection: -->
두 번째 인수로 제거할 컬렉션 크기를 지정할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

<!-- In addition, you may pass a third argument containing the new items to replace the items removed from the collection: -->
또한, 세 번째 인수에 새로운 항목 배열을 넣으면 제거한 위치에 새로운 항목들로 대체할 수도 있습니다.

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
`split` 메서드는 컬렉션을 지정한 개수만큼 그룹으로 분할합니다.

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
`splitIn` 메서드는 컬렉션을 지정한 그룹 수만큼 분할합니다. 각 그룹(마지막 그룹 전까지)은 가능한 한 채우고, 남은 항목은 마지막 그룹에 할당됩니다.

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
`sum` 메서드는 컬렉션에 포함된 모든 항목의 합계를 반환합니다.

```
collect([1, 2, 3, 4, 5])->sum();

// 15
```

<!-- If the collection contains nested arrays or objects, you should pass a key that will be used to determine which values to sum: -->
컬렉션에 중첩 배열이나 객체가 포함되어 있다면, 합계를 구할 속성 키를 전달해야 합니다.

```
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

<!-- In addition, you may pass your own closure to determine which values of the collection to sum: -->
또한, 합계에 포함할 값을 직접 지정하고 싶다면 클로저를 전달할 수도 있습니다.

```
$collection = collect([
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$collection->sum(function ($product) {
    return count($product['colors']);
});

// 6
```

<a name="method-take"></a>
<!-- #### `take()` -->
#### `take()`

<!-- The `take` method returns a new collection with the specified number of items: -->
`take` 메서드는 지정한 개수만큼의 요소로 구성된 새로운 컬렉션을 반환합니다.

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

<!-- You may also pass a negative integer to take the specified number of items from the end of the collection: -->
음수 값을 전달하면 컬렉션 끝에서부터 지정한 개수만큼의 항목을 반환합니다.

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
`takeUntil` 메서드는 주어진 콜백이 `true`를 반환할 때까지 컬렉션의 항목을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function ($item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

<!-- You may also pass a simple value to the `takeUntil` method to get the items until the given value is found: -->
`takeUntil` 메서드에 특정 값을 인수로 전달하면, 해당 값이 등장하기 전까지의 항목을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!NOTE]
> 만약 전달한 값이 없거나, 콜백이 한 번도 `true`를 반환하지 않으면 `takeUntil` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-takewhile"></a>
<!-- #### `takeWhile()` -->
#### `takeWhile()`

<!-- The `takeWhile` method returns items in the collection until the given callback returns `false`: -->
`takeWhile` 메서드는 주어진 콜백이 `false`를 반환할 때까지 컬렉션의 항목을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function ($item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!NOTE]
> 콜백이 한 번도 `false`를 반환하지 않으면, `takeWhile`은 컬렉션의 모든 항목을 반환합니다.

<a name="method-tap"></a>
<!-- #### `tap()` -->
#### `tap()`

<!-- The `tap` method passes the collection to the given callback, allowing you to "tap" into the collection at a specific point and do something with the items while not affecting the collection itself. The collection is then returned by the `tap` method: -->
`tap` 메서드는 컬렉션 전체를 주어진 콜백에 전달하여, 특정 시점에서 컬렉션의 상태를 확인하거나 작업을 수행할 수 있게 해 줍니다. 이때 컬렉션 자체는 변경되지 않으며, `tap` 메서드는 컬렉션 자신을 그대로 반환합니다.

```
collect([2, 4, 3, 1, 5])
    ->sort()
    ->tap(function ($collection) {
        Log::debug('Values after sorting', $collection->values()->all());
    })
    ->shift();

// 1
```

<a name="method-times"></a>
<!-- #### `times()` -->
#### `times()`

<!-- The static `times` method creates a new collection by invoking the given closure a specified number of times: -->
정적(static) 메서드인 `times`는 지정한 횟수만큼 클로저를 실행하여 결과로 컬렉션을 생성합니다.

```
$collection = Collection::times(10, function ($number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
<!-- #### `toArray()` -->
#### `toArray()`

<!-- The `toArray` method converts the collection into a plain PHP `array`. If the collection's values are [Eloquent](/docs/8.x/eloquent) models, the models will also be converted to arrays: -->
`toArray` 메서드는 컬렉션을 일반 PHP `array`로 변환합니다. 만약 컬렉션의 값이 [Eloquent](/docs/8.x/eloquent) 모델이라면, 모델 역시 배열로 변환됩니다.

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toArray();

/*
    [
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

> [!NOTE]
> `toArray`는 컬렉션 내에 `Arrayable` 인터페이스를 구현한 모든 중첩 객체들까지 배열로 변환합니다. 만약 컬렉션의 실제 원본 배열을 그대로 얻고 싶다면 [`all`](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>

<!-- #### `toJson()` -->
#### `toJson()`

<!-- The `toJson` method converts the collection into a JSON serialized string: -->
`toJson` 메서드는 컬렉션을 JSON 직렬화 문자열로 변환합니다.

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
<!-- #### `transform()` -->
#### `transform()`

<!-- The `transform` method iterates over the collection and calls the given callback with each item in the collection. The items in the collection will be replaced by the values returned by the callback: -->
`transform` 메서드는 컬렉션의 각 항목을 순회하며, 전달된 콜백을 각 항목에 대해 실행합니다. 콜백이 반환한 값으로 기존 컬렉션 항목이 대체됩니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function ($item, $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!NOTE]
> 대부분의 다른 컬렉션 메서드와 달리, `transform` 메서드는 컬렉션 자체를 변경합니다. 새로운 컬렉션을 생성하고 싶다면 [`map`](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
<!-- #### `undot()` -->
#### `undot()`

<!-- The `undot` method expands a single-dimensional collection that uses "dot" notation into a multi-dimensional collection: -->
`undot` 메서드는 "점(dot) 표기법"을 사용한 1차원 컬렉션을 다차원 컬렉션으로 확장해줍니다.

```
$person = collect([
    'name.first_name' => 'Marie',
    'name.last_name' => 'Valentine',
    'address.line_1' => '2992 Eagle Drive',
    'address.line_2' => '',
    'address.suburb' => 'Detroit',
    'address.state' => 'MI',
    'address.postcode' => '48219'
])

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
`union` 메서드는 전달한 배열을 기존 컬렉션에 추가합니다. 만약 전달된 배열의 키가 원본 컬렉션에 이미 존재한다면, 기존 컬렉션의 값이 우선적으로 유지됩니다.

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
`unique` 메서드는 컬렉션 내의 고유한 항목들만 반환합니다. 반환된 컬렉션은 기존 배열 키를 그대로 유지하므로, 아래 예제처럼 [`values`](#method-values) 메서드를 사용해 키를 연속된 숫자 인덱스로 재설정할 수 있습니다.

```
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

<!-- When dealing with nested arrays or objects, you may specify the key used to determine uniqueness: -->
중첩 배열이나 객체에 대해 고유성을 판별할 때, 비교에 사용할 키를 직접 지정할 수도 있습니다.

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
마지막으로, `unique` 메서드에 클로저(익명 함수)를 전달하여 항목의 고유성을 판단할 값을 직접 지정할 수도 있습니다.

```
$unique = $collection->unique(function ($item) {
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
`unique` 메서드는 항목 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 표현된 정수 값과 진짜 정수 값을 동일하다고 간주합니다. "엄격한(strict)" 비교를 적용하고 싶으면 [`uniqueStrict`](#method-uniquestrict) 메서드를 사용하세요.

> [!TIP]
> [Eloquent Collections](/docs/8.x/eloquent-collections#method-unique)를 사용할 때는 이 메서드의 동작이 일부 달라질 수 있습니다.

<a name="method-uniquestrict"></a>
<!-- #### `uniqueStrict()` -->
#### `uniqueStrict()`

<!-- This method has the same signature as the [`unique`](#method-unique) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [`unique`](#method-unique) 메서드와 동일한 시그니처를 갖지만, 모든 값 비교를 "엄격한(strict)" 방식으로 수행합니다.

<a name="method-unless"></a>
<!-- #### `unless()` -->
#### `unless()`

<!-- The `unless` method will execute the given callback unless the first argument given to the method evaluates to `true`: -->
`unless` 메서드는 첫 번째 인자가 `true`가 아니라면, 전달한 콜백을 실행합니다.

```
$collection = collect([1, 2, 3]);

$collection->unless(true, function ($collection) {
    return $collection->push(4);
});

$collection->unless(false, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- A second callback may be passed to the `unless` method. The second callback will be executed when the first argument given to the `unless` method evaluates to `true`: -->
`unless` 메서드에 두 번째 콜백을 전달할 수도 있습니다. 이 두 번째 콜백은 `unless` 메서드의 첫 번째 인자가 `true`로 평가될 때 실행됩니다.

```
$collection = collect([1, 2, 3]);

$collection->unless(true, function ($collection) {
    return $collection->push(4);
}, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- For the inverse of `unless`, see the [`when`](#method-when) method. -->
`unless`의 반대로 동작하는 메서드는 [`when`](#method-when)입니다.

<a name="method-unlessempty"></a>
<!-- #### `unlessEmpty()` -->
#### `unlessEmpty()`

<!-- Alias for the [`whenNotEmpty`](#method-whennotempty) method. -->
[`whenNotEmpty`](#method-whennotempty) 메서드의 별칭입니다.

<a name="method-unlessnotempty"></a>
<!-- #### `unlessNotEmpty()` -->
#### `unlessNotEmpty()`

<!-- Alias for the [`whenEmpty`](#method-whenempty) method. -->
[`whenEmpty`](#method-whenempty) 메서드의 별칭입니다.

<a name="method-unwrap"></a>
<!-- #### `unwrap()` -->
#### `unwrap()`

<!-- The static `unwrap` method returns the collection's underlying items from the given value when applicable: -->
정적 메서드인 `unwrap`은 전달된 값이 컬렉션인 경우, 그 내부 항목들을 반환합니다. 그렇지 않으면 전달된 값 자체를 반환합니다.

```
Collection::unwrap(collect('John Doe'));

// ['John Doe']

Collection::unwrap(['John Doe']);

// ['John Doe']

Collection::unwrap('John Doe');

// 'John Doe'
```

<a name="method-values"></a>
<!-- #### `values()` -->
#### `values()`

<!-- The `values` method returns a new collection with the keys reset to consecutive integers: -->
`values` 메서드는 키를 0부터 시작하는 연속된 정수로 재설정하여 새로운 컬렉션을 반환합니다.

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

<!-- The `when` method will execute the given callback when the first argument given to the method evaluates to `true`: -->
`when` 메서드는 첫 번째 인자가 `true`로 평가될 때, 전달된 콜백을 실행합니다.

```
$collection = collect([1, 2, 3]);

$collection->when(true, function ($collection) {
    return $collection->push(4);
});

$collection->when(false, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 4]
```

<!-- A second callback may be passed to the `when` method. The second callback will be executed when the first argument given to the `when` method evaluates to `false`: -->
`when` 메서드에는 두 번째 콜백도 전달할 수 있습니다. 이 두 번째 콜백은 `when` 메서드의 첫 번째 인자가 `false`로 평가될 때 실행됩니다.

```
$collection = collect([1, 2, 3]);

$collection->when(false, function ($collection) {
    return $collection->push(4);
}, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

<!-- For the inverse of `when`, see the [`unless`](#method-unless) method. -->
`when`의 반대로 동작하는 메서드는 [`unless`](#method-unless)입니다.

<a name="method-whenempty"></a>
<!-- #### `whenEmpty()` -->
#### `whenEmpty()`

<!-- The `whenEmpty` method will execute the given callback when the collection is empty: -->
`whenEmpty` 메서드는 컬렉션이 비어 있을 때, 전달된 콜백을 실행합니다.

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function ($collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom']


$collection = collect();

$collection->whenEmpty(function ($collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Adam']
```

<!-- A second closure may be passed to the `whenEmpty` method that will be executed when the collection is not empty: -->
`whenEmpty` 메서드에는 두 번째 클로저를 전달할 수 있으며, 이 클로저는 컬렉션이 비어 있지 않을 때 실행됩니다.

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function ($collection) {
    return $collection->push('Adam');
}, function ($collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Michael', 'Tom', 'Taylor']
```

<!-- For the inverse of `whenEmpty`, see the [`whenNotEmpty`](#method-whennotempty) method. -->
`whenEmpty`와 반대의 동작은 [`whenNotEmpty`](#method-whennotempty) 메서드를 참고하세요.

<a name="method-whennotempty"></a>
<!-- #### `whenNotEmpty()` -->
#### `whenNotEmpty()`

<!-- The `whenNotEmpty` method will execute the given callback when the collection is not empty: -->
`whenNotEmpty` 메서드는 컬렉션이 비어 있지 않을 때, 전달된 콜백을 실행합니다.

```
$collection = collect(['michael', 'tom']);

$collection->whenNotEmpty(function ($collection) {
    return $collection->push('adam');
});

$collection->all();

// ['michael', 'tom', 'adam']


$collection = collect();

$collection->whenNotEmpty(function ($collection) {
    return $collection->push('adam');
});

$collection->all();

// []
```

<!-- A second closure may be passed to the `whenNotEmpty` method that will be executed when the collection is empty: -->
`whenNotEmpty` 메서드에는 두 번째 클로저를 전달할 수 있으며, 이 클로저는 컬렉션이 비어 있을 때 실행됩니다.

```
$collection = collect();

$collection->whenNotEmpty(function ($collection) {
    return $collection->push('adam');
}, function ($collection) {
    return $collection->push('taylor');
});

$collection->all();

// ['taylor']
```

<!-- For the inverse of `whenNotEmpty`, see the [`whenEmpty`](#method-whenempty) method. -->
`whenNotEmpty`와 반대의 동작은 [`whenEmpty`](#method-whenempty) 메서드를 참고하세요.

<a name="method-where"></a>
<!-- #### `where()` -->
#### `where()`

<!-- The `where` method filters the collection by a given key / value pair: -->
`where` 메서드는 주어진 키/값 쌍을 기준으로 컬렉션을 필터링합니다.

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
`where` 메서드는 항목 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 표현된 정수 값과 실제 정수 값을 동일하게 간주합니다. "엄격한(strict)" 비교를 원한다면 [`whereStrict`](#method-wherestrict) 메서드를 사용하세요.

<!-- Optionally, you may pass a comparison operator as the second parameter. -->
또한, 두 번째 파라미터로 비교 연산자를 전달할 수도 있습니다.

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
이 메서드는 [`where`](#method-where) 메서드와 동일한 시그니처를 갖지만, 모든 값을 "엄격한(strict)" 방식으로 비교합니다.

<a name="method-wherebetween"></a>
<!-- #### `whereBetween()` -->
#### `whereBetween()`

<!-- The `whereBetween` method filters the collection by determining if a specified item value is within a given range: -->
`whereBetween` 메서드는 지정한 항목 값이 주어진 범위 내에 있는지 확인하여 컬렉션을 필터링합니다.

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
`whereIn` 메서드는 지정한 항목 값이 전달한 배열에 포함되지 않은 컬렉션 요소들을 제거합니다.

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
`whereIn` 메서드는 항목 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 표현된 정수 값과 실제 정수 값을 동일하게 간주합니다. "엄격한(strict)" 방식의 비교를 하려면 [`whereInStrict`](#method-whereinstrict) 메서드를 사용하세요.

<a name="method-whereinstrict"></a>
<!-- #### `whereInStrict()` -->
#### `whereInStrict()`

<!-- This method has the same signature as the [`whereIn`](#method-wherein) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [`whereIn`](#method-wherein) 메서드와 동일한 시그니처를 가지며, 모든 값의 비교를 "엄격한(strict)" 방식으로 진행합니다.

<a name="method-whereinstanceof"></a>
<!-- #### `whereInstanceOf()` -->
#### `whereInstanceOf()`

<!-- The `whereInstanceOf` method filters the collection by a given class type: -->
`whereInstanceOf` 메서드는 지정한 클래스 타입으로 컬렉션을 필터링합니다.

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
`whereNotBetween` 메서드는 지정한 항목 값이 주어진 범위 밖에 있는지 확인하여 컬렉션을 필터링합니다.

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
`whereNotIn` 메서드는 전달한 배열에 포함된 특정 항목 값을 가진 요소들을 컬렉션에서 제거합니다.

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
`whereNotIn` 메서드는 항목 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 표현된 정수 값과 실제 정수 값을 동일하게 간주합니다. "엄격한(strict)" 비교가 필요하면 [`whereNotInStrict`](#method-wherenotinstrict) 메서드를 사용하세요.

<a name="method-wherenotinstrict"></a>

<!-- #### `whereNotInStrict()` -->
#### `whereNotInStrict()`

<!-- This method has the same signature as the [`whereNotIn`](#method-wherenotin) method; however, all values are compared using "strict" comparisons. -->
이 메서드는 [`whereNotIn`](#method-wherenotin) 메서드와 동일한 시그니처를 가지고 있습니다. 그러나 모든 값은 "엄격한(strict)" 비교 방식으로 비교됩니다.

<a name="method-wherenotnull"></a>
<!-- #### `whereNotNull()` -->
#### `whereNotNull()`

<!-- The `whereNotNull` method returns items from the collection where the given key is not `null`: -->
`whereNotNull` 메서드는 주어진 키의 값이 `null`이 아닌 컬렉션의 항목만 반환합니다.

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
`whereNull` 메서드는 주어진 키의 값이 `null`인 컬렉션의 항목만 반환합니다.

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
정적 메서드인 `wrap`은 전달된 값을 적절한 경우 컬렉션으로 감싸서 반환합니다.

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
`zip` 메서드는 주어진 배열의 값들과 원본 컬렉션의 값들을 각 인덱스에 맞게 쌍으로 합쳐줍니다.

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
컬렉션에서는 "하이어 오더 메시지(Higher Order Messages)"를 지원합니다. 이는 컬렉션에서 자주 사용하는 동작을 짧고 간단하게 수행할 수 있도록 마련된 단축 방식입니다. 하이어 오더 메시지를 지원하는 컬렉션 메서드는 다음과 같습니다: [`average`](#method-average), [`avg`](#method-avg), [`contains`](#method-contains), [`each`](#method-each), [`every`](#method-every), [`filter`](#method-filter), [`first`](#method-first), [`flatMap`](#method-flatmap), [`groupBy`](#method-groupby), [`keyBy`](#method-keyby), [`map`](#method-map), [`max`](#method-max), [`min`](#method-min), [`partition`](#method-partition), [`reject`](#method-reject), [`skipUntil`](#method-skipuntil), [`skipWhile`](#method-skipwhile), [`some`](#method-some), [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc), [`sum`](#method-sum), [`takeUntil`](#method-takeuntil), [`takeWhile`](#method-takewhile), [`unique`](#method-unique).

<!-- Each higher order message can be accessed as a dynamic property on a collection instance. For instance, let's use the `each` higher order message to call a method on each object within a collection: -->
각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티(dynamically-accessed property)로 사용할 수 있습니다. 예를 들어, `each` 하이어 오더 메시지를 사용해서 컬렉션 안의 각 객체에 있는 메서드를 호출해보겠습니다.

```
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

<!-- Likewise, we can use the `sum` higher order message to gather the total number of "votes" for a collection of users: -->
마찬가지로, `sum` 하이어 오더 메시지를 사용해서 사용자 컬렉션에서 "votes"의 합계를 쉽게 구할 수도 있습니다.

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

> [!NOTE]
> Laravel의 레이지 컬렉션에 대해 더 자세히 알기 전에, [PHP generators](https://www.php.net/manual/en/language.generators.overview.php)에 대해 미리 익숙해지시는 것이 좋습니다.

<!-- To supplement the already powerful `Collection` class, the `LazyCollection` class leverages PHP's [generators](https://www.php.net/manual/en/language.generators.overview.php) to allow you to work with very large datasets while keeping memory usage low. -->
기존의 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [generators](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다. 이를 통해 매우 큰 데이터셋을 다루면서도 메모리 사용량을 최소화할 수 있습니다.

<!-- For example, imagine your application needs to process a multi-gigabyte log file while taking advantage of Laravel's collection methods to parse the logs. Instead of reading the entire file into memory at once, lazy collections may be used to keep only a small part of the file in memory at a given time: -->
예를 들어, 여러 GB(기가바이트) 크기의 로그 파일을 Laravel의 컬렉션 메서드를 사용해 파싱해야 하는 상황을 떠올려보세요. 파일 전체를 한 번에 메모리로 읽어들이는 대신, 레이지 컬렉션을 사용하면 한 번에 파일의 일부분만 메모리에 유지하면서 작업할 수 있습니다.

```
use App\Models\LogEntry;
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }
})->chunk(4)->map(function ($lines) {
    return LogEntry::fromLines($lines);
})->each(function (LogEntry $logEntry) {
    // Process the log entry...
});
```

<!-- Or, imagine you need to iterate through 10,000 Eloquent models. When using traditional Laravel collections, all 10,000 Eloquent models must be loaded into memory at the same time: -->
또는 10,000개의 Eloquent 모델을 반복(iterate)해야 하는 경우를 생각해보세요. 기존 Laravel 컬렉션을 사용할 경우, 모든 10,000개 Eloquent 모델이 한 번에 메모리에 적재됩니다.

```
use App\Models\User;

$users = User::all()->filter(function ($user) {
    return $user->id > 500;
});
```

<!-- However, the query builder's `cursor` method returns a `LazyCollection` instance. This allows you to still only run a single query against the database but also only keep one Eloquent model loaded in memory at a time. In this example, the `filter` callback is not executed until we actually iterate over each user individually, allowing for a drastic reduction in memory usage: -->
하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 통해 데이터베이스 쿼리는 한 번만 실행하지만, Eloquent 모델은 한 번에 하나만 메모리에 적재하게 됩니다. 이 예시에서 `filter` 콜백은 실제로 각 사용자를 개별적으로 순회할 때 실행되어, 메모리 사용량을 크게 줄일 수 있습니다.

```
use App\Models\User;

$users = User::cursor()->filter(function ($user) {
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
레이지 컬렉션 인스턴스를 생성하려면, 컬렉션의 `make` 메서드에 PHP 제너레이터 함수를 전달하면 됩니다.

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
거의 모든 `Collection` 클래스의 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 이 두 클래스는 모두 `Illuminate\Support\Enumerable` 계약(Contract)을 구현하고 있으며, 여기에는 다음과 같은 메서드들이 정의되어 있습니다.

<!-- <div id="collection-method-list" markdown="1"> -->
<div id="collection-method-list" markdown="1">

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

> [!NOTE]
> 컬렉션 자체를 변경(mutate)하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서 **지원하지 않습니다**.

<a name="lazy-collection-methods"></a>
<!-- ### Lazy Collection Methods -->
### Lazy Collection Methods

<!-- In addition to the methods defined in the `Enumerable` contract, the `LazyCollection` class contains the following methods: -->
`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에는 다음과 같은 전용 메서드가 있습니다.

<a name="method-takeUntilTimeout"></a>
<!-- #### `takeUntilTimeout()` -->
#### `takeUntilTimeout()`

<!-- The `takeUntilTimeout` method returns a new lazy collection that will enumerate values until the specified time. After that time, the collection will then stop enumerating: -->
`takeUntilTimeout` 메서드는 지정된 시간까지 값을 반복(enumerate)하는 새로운 레이지 컬렉션을 반환합니다. 해당 시간이 지나면 컬렉션은 더 이상 값을 반환하지 않고 열거를 중단합니다.

```
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->addMinute());

$lazyCollection->each(function ($number) {
    dump($number);

    sleep(1);
});

// 1
// 2
// ...
// 58
// 59
```

<!-- To illustrate the usage of this method, imagine an application that submits invoices from the database using a cursor. You could define a [scheduled task](/docs/8.x/scheduling) that runs every 15 minutes and only processes invoices for a maximum of 14 minutes: -->
이 메서드의 사용 예시로, 데이터베이스에서 청구서(invoice)를 커서를 사용하여 순차적으로 제출(submit)하는 애플리케이션을 생각해 보겠습니다. [scheduled task](/docs/8.x/scheduling)을 15분마다 실행하고 매회 14분까지만 청구서를 처리하도록 할 수 있습니다.

```
use App\Models\Invoice;
use Illuminate\Support\Carbon;

Invoice::pending()->cursor()
    ->takeUntilTimeout(
        Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')
    )
    ->each(fn ($invoice) => $invoice->submit());
```

<a name="method-tapEach"></a>
<!-- #### `tapEach()` -->
#### `tapEach()`

<!-- While the `each` method calls the given callback for each item in the collection right away, the `tapEach` method only calls the given callback as the items are being pulled out of the list one by one: -->
`each` 메서드는 컬렉션의 각 항목을 즉시 전달된 콜백에 넘기지만, `tapEach` 메서드는 항목이 하나씩 컬렉션에서 꺼내질 때마다 콜백을 실행합니다.

```
// Nothing has been dumped so far...
$lazyCollection = LazyCollection::times(INF)->tapEach(function ($value) {
    dump($value);
});

// Three items are dumped...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-remember"></a>
<!-- #### `remember()` -->
#### `remember()`

<!-- The `remember` method returns a new lazy collection that will remember any values that have already been enumerated and will not retrieve them again on subsequent collection enumerations: -->
`remember` 메서드는 이미 반복(enumerate)한 값들은 컬렉션 내부에 저장해 두고, 이후의 반복에서는 다시 가져오지 않는 새로운 레이지 컬렉션을 반환합니다.

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