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
Laravel에는 다양한 전역 "헬퍼" PHP 함수들이 포함되어 있습니다. 이 함수들 중 상당수는 Laravel 프레임워크 내부에서 활용되지만, 여러분이 편리하다고 판단한다면 자신의 애플리케이션에서도 자유롭게 사용할 수 있습니다.

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
`Arr::accessible` 메서드는 주어진 값이 배열로 접근 가능한지 판단합니다:

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
`Arr::add` 메서드는 주어진 배열에 해당 키가 존재하지 않거나 값이 `null`로 설정된 경우, 지정한 키/값 쌍을 추가합니다:

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
`Arr::collapse` 메서드는 다차원 배열(배열의 배열들)을 하나의 배열로 합쳐줍니다:

```
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
<!-- #### `Arr::crossJoin()` -->
#### `Arr::crossJoin()`

<!-- The `Arr::crossJoin` method cross joins the given arrays, returning a Cartesian product with all possible permutations: -->
`Arr::crossJoin` 메서드는 주어진 배열들의 교차 곱(카테시안 곱)을 만들어, 가능한 모든 조합을 반환합니다:

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
`Arr::divide` 메서드는 주어진 배열에서 키와 값으로 각각 이루어진 두 개의 배열을 반환합니다:

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
`Arr::dot` 메서드는 다차원 배열을 "점(dot) 표기법"을 이용해 단일 수준의 배열로 평탄화합니다:

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
`Arr::except` 메서드는 입력된 배열에서 지정된 키/값 쌍을 제거합니다:

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
`Arr::exists` 메서드는 주어진 키가 해당 배열에 존재하는지 확인합니다:

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
`Arr::first` 메서드는 지정한 조건(콜백 함수)을 만족하는 배열의 첫 번째 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

<!-- A default value may also be passed as the third parameter to the method. This value will be returned if no value passes the truth test: -->
조건을 통과하는 값이 없을 경우에 반환할 기본값을 세 번째 인자로 전달할 수 있습니다:

```
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
<!-- #### `Arr::flatten()` -->
#### `Arr::flatten()`

<!-- The `Arr::flatten` method flattens a multi-dimensional array into a single level array: -->
`Arr::flatten` 메서드는 다차원 배열을 한 단계의 배열로 만들어줍니다:

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
`Arr::forget` 메서드는 "점(dot) 표기법"을 활용하여, 깊게 중첩된 배열에서 특정 키/값 쌍을 제거합니다:

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
`Arr::get` 메서드는 "점(dot) 표기법"을 사용해 깊게 중첩된 배열에서 값을 가져옵니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

<!-- The `Arr::get` method also accepts a default value, which will be returned if the specified key is not present in the array: -->
또한, `Arr::get` 메서드는 하나의 기본값도 인자로 받을 수 있습니다. 지정한 키가 배열에 없을 경우 이 값을 반환합니다:

```
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
<!-- #### `Arr::has()` -->
#### `Arr::has()`

<!-- The `Arr::has` method checks whether a given item or items exists in an array using "dot" notation: -->
`Arr::has` 메서드는 "점(dot) 표기법"을 사용하여, 지정한 항목(들)이 배열에 존재하는지 확인합니다:

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
`Arr::hasAny` 메서드는 "점(dot) 표기법"을 이용하여, 지정한 항목들 중 하나라도 배열에 존재하는지 확인합니다:

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
`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열(associative array)인지 여부를 반환합니다. 배열의 키가 0부터 시작해서 순차적이지 않은 경우, 연관 배열로 간주됩니다:

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
`Arr::isList` 메서드는 배열의 키들이 0부터 시작하는 연속된 정수일 때 `true`를 반환합니다:

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
`Arr::join` 메서드는 배열의 요소들을 문자열로 합쳐줍니다. 두 번째 인자로 구분자를, 세 번째 인자로 마지막 요소 앞에 사용할 구분자를 지정할 수 있습니다:

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
`Arr::keyBy` 메서드는 배열의 지정된 키를 이용해 새로운 배열의 키로 할당합니다. 동일한 키가 여러 번 등장할 경우, 마지막 값만의 값이 최종적으로 할당됩니다:

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
`Arr::last` 메서드는 주어진 조건(콜백 함수)을 만족하는 배열의 마지막 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

<!-- A default value may be passed as the third argument to the method. This value will be returned if no value passes the truth test: -->
조건을 만족하는 값이 없는 경우 반환할 기본값을 세 번째 인자로 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>

<!-- #### `Arr::map()` -->
#### `Arr::map()`

<!-- The `Arr::map` method iterates through the array and passes each value and key to the given callback. The array value is replaced by the value returned by the callback: -->
`Arr::map` 메서드는 배열을 반복하면서 각 값과 키를 전달된 콜백 함수에 넘깁니다. 콜백 함수가 반환하는 값으로 배열의 값을 교체합니다.

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
`Arr::mapSpread` 메서드는 배열을 반복하면서, 각 중첩된 요소의 값을 전달된 클로저에 전달합니다. 클로저 내에서 각 요소를 자유롭게 수정하여 반환할 수 있으며, 그 반환값들로 새로운 배열이 만들어집니다.

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
`Arr::mapWithKeys` 메서드는 배열을 반복하면서 각 값을 전달된 콜백 함수에 넘깁니다. 콜백 함수는 반드시 하나의 키/값 쌍이 들어 있는 연관 배열을 반환해야 합니다.

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
`Arr::only` 메서드는 지정한 키/값 쌍만을 배열에서 반환합니다.

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
`Arr::pluck` 메서드는 배열에서 지정한 키의 모든 값을 추출해 반환합니다.

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
결과 배열의 키를 어떻게 지정할지도 선택할 수 있습니다.

```
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
<!-- #### `Arr::prepend()` -->
#### `Arr::prepend()`

<!-- The `Arr::prepend` method will push an item onto the beginning of an array: -->
`Arr::prepend` 메서드는 배열의 맨 앞에 값을 추가합니다.

```
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

<!-- If needed, you may specify the key that should be used for the value: -->
필요하다면, 값에 사용할 키를 지정할 수도 있습니다.

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
`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키 이름 앞에 지정한 접두사를 붙입니다.

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
`Arr::pull` 메서드는 배열에서 키/값 쌍을 반환하고 해당 항목을 배열에서 제거합니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

<!-- A default value may be passed as the third argument to the method. This value will be returned if the key doesn't exist: -->
세 번째 인수로 기본값을 지정할 수 있습니다. 해당 키가 배열에 없다면 이 값이 반환됩니다.

```
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
<!-- #### `Arr::query()` -->
#### `Arr::query()`

<!-- The `Arr::query` method converts the array into a query string: -->
`Arr::query` 메서드는 배열을 쿼리 문자열로 변환합니다.

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
`Arr::random` 메서드는 배열에서 임의의 값을 반환합니다.

```
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (retrieved randomly)
```

<!-- You may also specify the number of items to return as an optional second argument. Note that providing this argument will return an array even if only one item is desired: -->
두 번째 인수로 반환할 항목의 개수를 지정할 수도 있습니다. 이 인수를 지정하면 단일 항목만을 원해도 항상 배열 형태로 반환됩니다.

```
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (retrieved randomly)
```

<a name="method-array-reject"></a>
<!-- #### `Arr::reject()` -->
#### `Arr::reject()`

<!-- The `Arr::reject` method removes items from an array using the given closure: -->
`Arr::reject` 메서드는 전달된 클로저를 이용해 배열에서 항목들을 제거합니다.

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
`Arr::set` 메서드는 "dot" 표기법을 사용해 다차원 배열의 값을 설정합니다.

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
`Arr::shuffle` 메서드는 배열의 항목을 임의로 뒤섞습니다.

```
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-array-sort"></a>
<!-- #### `Arr::sort()` -->
#### `Arr::sort()`

<!-- The `Arr::sort` method sorts an array by its values: -->
`Arr::sort` 메서드는 배열의 값을 기준으로 정렬합니다.

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

<!-- You may also sort the array by the results of a given closure: -->
전달된 클로저의 결과에 따라 배열을 정렬하도록 할 수도 있습니다.

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
`Arr::sortDesc` 메서드는 배열의 값을 기준으로 내림차순 정렬합니다.

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

<!-- You may also sort the array by the results of a given closure: -->
전달된 클로저의 결과에 따라 배열을 내림차순 정렬할 수도 있습니다.

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
`Arr::sortRecursive` 메서드는 숫자 인덱스가 있는 하위 배열에는 `sort` 함수, 연관 배열에는 `ksort` 함수를 이용해 재귀적으로 배열을 정렬합니다.

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
내림차순으로 정렬된 결과가 필요하다면 `Arr::sortRecursiveDesc` 메서드를 사용할 수 있습니다.

```
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-take"></a>
<!-- #### `Arr::take()` -->
#### `Arr::take()`

<!-- The `Arr::take` method returns a new array with the specified number of items: -->
`Arr::take` 메서드는 지정한 개수만큼의 항목을 포함하는 새로운 배열을 반환합니다.

```
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

<!-- You may also pass a negative integer to take the specified number of items from the end of the array: -->
음수를 전달하면, 배열의 끝에서부터 해당 개수만큼 반환합니다.

```
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
<!-- #### `Arr::toCssClasses()` -->
#### `Arr::toCssClasses()`

<!-- The `Arr::toCssClasses` method conditionally compiles a CSS class string. The method accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`Arr::toCssClasses` 메서드는 조건적으로 CSS 클래스 문자열을 만들어냅니다. 이 메서드는 클래스 또는 클래스들의 이름을 배열의 키에, 불리언 값을 값으로 담은 배열을 받습니다. 만약 배열 항목의 키가 숫자라면, 해당 항목은 조건과 상관없이 항상 클래스 목록에 포함됩니다.

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
`Arr::toCssStyles` 메서드는 조건적으로 CSS 스타일 문자열을 만들어냅니다. 이 메서드 역시 클래스 또는 클래스들의 이름을 배열의 키에, 불리언 값을 값으로 담은 배열을 받습니다. 배열 항목의 키가 숫자일 경우, 해당 스타일 항목은 항상 포함됩니다.

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
이 메서드는 Laravel의 [merging classes with a Blade component's attribute bag](/docs/11.x/blade#conditionally-merge-classes) 및 `@class` [Blade directive](/docs/11.x/blade#conditional-classes) 기능을 지원합니다.

<a name="method-array-undot"></a>
<!-- #### `Arr::undot()` -->
#### `Arr::undot()`

<!-- The `Arr::undot` method expands a single-dimensional array that uses "dot" notation into a multi-dimensional array: -->
`Arr::undot` 메서드는 "dot" 표기법을 사용하는 1차원 배열을 다차원 배열로 확장합니다.

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
`Arr::where` 메서드는 전달된 클로저로 배열에서 항목을 필터링합니다.

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
`Arr::whereNotNull` 메서드는 전달된 배열에서 모든 `null` 값을 제거합니다.

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
`Arr::wrap` 메서드는 전달된 값을 배열로 감쌉니다. 전달값이 이미 배열이면 그대로 반환합니다.

```
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

<!-- If the given value is `null`, an empty array will be returned: -->
전달값이 `null`일 경우 빈 배열을 반환합니다.

```
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
<!-- #### `data_fill()` -->
#### `data_fill()`

<!-- The `data_fill` function sets a missing value within a nested array or object using "dot" notation: -->
`data_fill` 함수는 "dot" 표기법을 사용하여 중첩 배열 또는 객체에서 값이 없는 곳에 값을 설정합니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

<!-- This function also accepts asterisks as wildcards and will fill the target accordingly: -->
이 함수는 별표(*)를 와일드카드로 사용할 수 있으며, 해당 대상이 여러 개라면 모두 채워줍니다.

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
`data_get` 함수는 "dot" 표기법을 사용하여 중첩된 배열이나 객체에서 값을 가져옵니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

<!-- The `data_get` function also accepts a default value, which will be returned if the specified key is not found: -->
`data_get` 함수는 기본값도 받을 수 있으며, 지정한 키를 찾을 수 없을 때 이 기본값을 반환합니다.

```
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

<!-- The function also accepts wildcards using asterisks, which may target any key of the array or object: -->
또한, 이 함수는 애스터리스크(asterisk)를 와일드카드로 사용할 수 있으며, 배열이나 객체 내 모든 키를 대상으로 값을 가져올 수 있습니다.

```
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

<!-- The `{first}` and `{last}` placeholders may be used to retrieve the first or last items in an array: -->
`{first}` 및 `{last}` 플레이스홀더를 사용하면 배열의 첫 번째 또는 마지막 항목을 가져올 수 있습니다.

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
`data_set` 함수는 "dot" 표기법을 사용하여 중첩된 배열 또는 객체 내에 값을 설정합니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<!-- This function also accepts wildcards using asterisks and will set values on the target accordingly: -->
이 함수 또한 애스터리스크(asterisk)를 와일드카드로 지원하며, 대상이 되는 모든 값에 변경을 적용합니다.

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
기본적으로 기존 값이 있으면 덮어씁니다. 만약 값이 아직 없을 때만 설정하고 싶다면, 네 번째 인자로 `false`를 전달하면 됩니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
<!-- #### `data_forget()` -->
#### `data_forget()`

<!-- The `data_forget` function removes a value within a nested array or object using "dot" notation: -->
`data_forget` 함수는 "dot" 표기법을 사용하여 중첩된 배열 또는 객체에서 값을 제거합니다.

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

<!-- This function also accepts wildcards using asterisks and will remove values on the target accordingly: -->
이 함수 또한 애스터리스크(asterisk)를 와일드카드로 지원하여, 대상에 맞게 여러 값을 제거할 수 있습니다.

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
`head` 함수는 전달된 배열의 첫 번째 요소를 반환합니다.

```
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
<!-- #### `last()` -->
#### `last()`

<!-- The `last` function returns the last element in the given array: -->
`last` 함수는 전달된 배열의 마지막 요소를 반환합니다.

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
`Number::abbreviate` 메서드는 전달된 숫자 값을 사람에게 읽기 쉬운 형식(단위가 축약된 형태)으로 변환해 반환합니다.

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
`Number::clamp` 메서드는 지정한 숫자가 특정 범위 내에 있도록 제한해줍니다. 만약 숫자가 최소값보다 작으면 최소값을, 최대값보다 크면 최대값을 반환합니다.

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
`Number::currency` 메서드는 전달된 값을 화폐 단위로 변환하여 문자열로 반환합니다.

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
`Number::defaultCurrency` 메서드는 `Number` 클래스에서 사용 중인 기본 통화 단위를 반환합니다.

```
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
<!-- #### `Number::defaultLocale()` -->
#### `Number::defaultLocale()`

<!-- The `Number::defaultLocale` method returns the default locale being used by the `Number` class: -->
`Number::defaultLocale` 메서드는 `Number` 클래스에서 사용 중인 기본 로케일(언어/지역 설정)을 반환합니다.

```
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
<!-- #### `Number::fileSize()` -->
#### `Number::fileSize()`

<!-- The `Number::fileSize` method returns the file size representation of the given byte value as a string: -->
`Number::fileSize` 메서드는 바이트(byte) 단위의 값을 사람이 읽기 쉬운 파일 크기 문자열로 변환해 반환합니다.

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
`Number::forHumans` 메서드는 입력된 숫자를 사람이 읽기 쉬운 서술형 형식으로 반환합니다.

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
`Number::format` 메서드는 전달된 숫자를 지정된 로케일에 맞게 문자열로 포맷팅합니다.

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
`Number::ordinal` 메서드는 숫자의 서수(순서 표현)를 반환합니다.

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
`Number::pairs` 메서드는 지정한 범위와 단위(스텝)를 기준으로 숫자 쌍(하위 범위) 배열을 만듭니다. 이 메서드는 많은 숫자 범위를 페이지네이션, 일괄 작업 등으로 나누고자 할 때 유용하게 사용할 수 있습니다. `pairs` 메서드는 각 쌍(하위 범위)이 배열로 이루어진 다차원 배열을 반환합니다.

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
`Number::percentage` 메서드는 전달된 값을 백분율 형식의 문자열로 반환합니다.

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
`Number::spell` 메서드는 전달된 숫자를 단어로 변환하여 문자열로 반환합니다.

```
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

<!-- The `after` argument allows you to specify a value after which all numbers should be spelled out: -->
`after` 인수를 사용하면, 특정 값을 초과하는 모든 숫자를 단어로 표기하도록 지정할 수 있습니다.

```
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

<!-- The `until` argument allows you to specify a value before which all numbers should be spelled out: -->
`until` 인수를 사용하면, 특정 값 이하까지는 단어로, 그 이상은 숫자로 표기할 수 있습니다.

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
`Number::trim` 메서드는 전달된 소수점 숫자의 끝에 붙은 0을 제거한 결과를 반환합니다.

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
`Number::useLocale` 메서드는 기본 숫자 로케일을 전역적으로 지정합니다. 이 설정은 이후 `Number` 클래스의 메서드에서 숫자나 화폐를 포맷할 때 영향을 줍니다.

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
`Number::withLocale` 메서드는 지정한 로케일로 클로저(콜백) 내부 코드를 실행하고, 실행이 끝난 후에는 원래의 로케일로 되돌립니다.

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
`Number::useCurrency` 메서드는 기본 통화 단위를 전역적으로 설정합니다. 이 설정은 이후 `Number` 클래스의 메서드로 화폐를 표시할 때 모두 적용됩니다.

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
`Number::withCurrency` 메서드는 지정한 통화로 클로저(콜백) 내부 코드를 실행하고, 실행이 끝난 후에는 원래의 통화로 되돌립니다.

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
`app_path` 함수는 애플리케이션의 `app` 디렉토리에 대한 전체 경로를 반환합니다. 또한 `app_path`에 매개변수를 전달해, 애플리케이션 디렉토리 기준의 파일 전체 경로를 생성할 수도 있습니다.

```
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
<!-- #### `base_path()` -->
#### `base_path()`

<!-- The `base_path` function returns the fully qualified path to your application's root directory. You may also use the `base_path` function to generate a fully qualified path to a given file relative to the project root directory: -->
`base_path` 함수는 애플리케이션의 프로젝트 루트 디렉토리에 대한 전체 경로를 반환합니다. 또한 `base_path` 함수를 사용해 프로젝트 루트에서 특정 파일에 대한 전체 경로도 만들 수 있습니다.

```
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
<!-- #### `config_path()` -->
#### `config_path()`

<!-- The `config_path` function returns the fully qualified path to your application's `config` directory. You may also use the `config_path` function to generate a fully qualified path to a given file within the application's configuration directory: -->
`config_path` 함수는 애플리케이션의 `config` 디렉토리 전체 경로를 반환합니다. 또한 `config_path` 함수를 사용해 설정 디렉토리 내의 특정 파일에 대한 전체 경로도 생성할 수 있습니다.

```
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
<!-- #### `database_path()` -->
#### `database_path()`

<!-- The `database_path` function returns the fully qualified path to your application's `database` directory. You may also use the `database_path` function to generate a fully qualified path to a given file within the database directory: -->
`database_path` 함수는 애플리케이션의 `database` 디렉토리에 대한 전체 경로를 반환합니다. 또한 `database_path` 함수를 사용해 데이터베이스 디렉토리 내 특정 파일의 전체 경로도 얻을 수 있습니다.

```
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
<!-- #### `lang_path()` -->
#### `lang_path()`

<!-- The `lang_path` function returns the fully qualified path to your application's `lang` directory. You may also use the `lang_path` function to generate a fully qualified path to a given file within the directory: -->
`lang_path` 함수는 애플리케이션의 `lang` 디렉토리에 대한 전체 경로를 반환합니다. 또한 `lang_path` 함수를 사용해 해당 디렉토리 내 특정 파일의 전체 경로도 생성할 수 있습니다.

```
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> 기본적으로 Laravel 애플리케이션의 골격(skeleton)에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 커스터마이즈하려면, `lang:publish` Artisan 명령어를 사용해 언어 파일을 배포(publish)할 수 있습니다.

<a name="method-mix"></a>

<!-- #### `mix()` -->
#### `mix()`

<!-- The `mix` function returns the path to a [versioned Mix file](/docs/11.x/mix): -->
`mix` 함수는 [versioned Mix file](/docs/11.x/mix)의 경로를 반환합니다.

```
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
<!-- #### `public_path()` -->
#### `public_path()`

<!-- The `public_path` function returns the fully qualified path to your application's `public` directory. You may also use the `public_path` function to generate a fully qualified path to a given file within the public directory: -->
`public_path` 함수는 애플리케이션의 `public` 디렉터리에 대한 전체 경로(절대 경로)를 반환합니다. 또한, `public_path` 함수에 파일 경로를 전달하여 public 디렉터리 내부의 특정 파일에 대한 전체 경로도 생성할 수 있습니다.

```
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
<!-- #### `resource_path()` -->
#### `resource_path()`

<!-- The `resource_path` function returns the fully qualified path to your application's `resources` directory. You may also use the `resource_path` function to generate a fully qualified path to a given file within the resources directory: -->
`resource_path` 함수는 애플리케이션의 `resources` 디렉터리에 대한 전체 경로를 반환합니다. 마찬가지로, `resource_path` 함수에 파일명을 전달하여 resources 디렉터리 내 특정 파일의 전체 경로도 만들 수 있습니다.

```
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
<!-- #### `storage_path()` -->
#### `storage_path()`

<!-- The `storage_path` function returns the fully qualified path to your application's `storage` directory. You may also use the `storage_path` function to generate a fully qualified path to a given file within the storage directory: -->
`storage_path` 함수는 애플리케이션의 `storage` 디렉터리 전체 경로를 반환합니다. 또한 `storage_path` 함수를 사용해 storage 디렉터리 내 특정 파일의 전체 경로도 얻을 수 있습니다.

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
`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다.

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the method accepts route parameters, you may pass them as the second argument to the method: -->
만약 해당 메서드가 라우트 파라미터를 받는다면, 두 번째 인수로 파라미터 배열을 전달할 수 있습니다.

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
<!-- #### `asset()` -->
#### `asset()`

<!-- The `asset` function generates a URL for an asset using the current scheme of the request (HTTP or HTTPS): -->
`asset` 함수는 현재 요청의 스킴(HTTP 또는 HTTPS)을 사용하여, 에셋(asset)의 URL을 생성합니다.

```
$url = asset('img/photo.jpg');
```

<!-- You can configure the asset URL host by setting the `ASSET_URL` variable in your `.env` file. This can be useful if you host your assets on an external service like Amazon S3 or another CDN: -->
에셋의 호스트 URL은 `.env` 파일의 `ASSET_URL` 변수로 설정할 수 있습니다. 예를 들어, 에셋 파일을 Amazon S3 같은 외부 서비스나 다른 CDN에 호스팅하는 경우에 유용합니다.

```
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
<!-- #### `route()` -->
#### `route()`

<!-- The `route` function generates a URL for a given [named route](/docs/11.x/routing#named-routes): -->
`route` 함수는 지정한 [named route](/docs/11.x/routing#named-routes)에 대한 URL을 생성합니다.

```
$url = route('route.name');
```

<!-- If the route accepts parameters, you may pass them as the second argument to the function: -->
해당 라우트가 파라미터를 받는다면 두 번째 인수로 파라미터 배열을 전달할 수 있습니다.

```
$url = route('route.name', ['id' => 1]);
```

<!-- By default, the `route` function generates an absolute URL. If you wish to generate a relative URL, you may pass `false` as the third argument to the function: -->
기본적으로 `route` 함수는 절대 URL을 반환합니다. 상대 경로 URL을 생성하려면 세 번째 인수로 `false`를 전달할 수 있습니다.

```
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
<!-- #### `secure_asset()` -->
#### `secure_asset()`

<!-- The `secure_asset` function generates a URL for an asset using HTTPS: -->
`secure_asset` 함수는 HTTPS를 사용하여 에셋의 URL을 생성합니다.

```
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
<!-- #### `secure_url()` -->
#### `secure_url()`

<!-- The `secure_url` function generates a fully qualified HTTPS URL to the given path. Additional URL segments may be passed in the function's second argument: -->
`secure_url` 함수는 전달된 경로에 대해 HTTPS로 전체 URL을 생성합니다. 두 번째 인수로 추가 URL 세그먼트를 배열로 전달할 수 있습니다.

```
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
<!-- #### `to_route()` -->
#### `to_route()`

<!-- The `to_route` function generates a [redirect HTTP response](/docs/11.x/responses#redirects) for a given [named route](/docs/11.x/routing#named-routes): -->
`to_route` 함수는 주어진 [redirect HTTP response](/docs/11.x/responses#redirects)로의 [named route](/docs/11.x/routing#named-routes)을 생성합니다.

```
return to_route('users.show', ['user' => 1]);
```

<!-- If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the `to_route` method: -->
필요하다면, 리디렉션에 사용할 HTTP 상태 코드와 추가 응답 헤더를 `to_route` 메서드의 세 번째, 네 번째 인수로 전달할 수 있습니다.

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-url"></a>
<!-- #### `url()` -->
#### `url()`

<!-- The `url` function generates a fully qualified URL to the given path: -->
`url` 함수는 주어진 경로에 대해 전체(절대) URL을 생성합니다.

```
$url = url('user/profile');

$url = url('user/profile', [1]);
```

<!-- If no path is provided, an `Illuminate\Routing\UrlGenerator` instance is returned: -->
경로를 지정하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환됩니다.

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
`abort` 함수는 [an HTTP exception](/docs/11.x/errors#http-exceptions)를 발생시키며, 이는 [exception handler](/docs/11.x/errors#handling-exceptions)에 의해 렌더링됩니다.

```
abort(403);
```

<!-- You may also provide the exception's message and custom HTTP response headers that should be sent to the browser: -->
필요하다면 예외 메시지와 브라우저로 전송할 사용자 정의 HTTP 응답 헤더를 추가로 지정할 수 있습니다.

```
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
<!-- #### `abort_if()` -->
#### `abort_if()`

<!-- The `abort_if` function throws an HTTP exception if a given boolean expression evaluates to `true`: -->
`abort_if` 함수는 주어진 불리언 식의 값이 `true`일 때 HTTP 예외를 발생시킵니다.

```
abort_if(! Auth::user()->isAdmin(), 403);
```

<!-- Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function. -->
`abort` 메서드와 마찬가지로, 세 번째 인수로 예외의 메시지, 네 번째 인수로 커스텀 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-abort-unless"></a>
<!-- #### `abort_unless()` -->
#### `abort_unless()`

<!-- The `abort_unless` function throws an HTTP exception if a given boolean expression evaluates to `false`: -->
`abort_unless` 함수는 주어진 불리언 식이 `false`일 때 HTTP 예외를 발생시킵니다.

```
abort_unless(Auth::user()->isAdmin(), 403);
```

<!-- Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function. -->
`abort` 메서드와 마찬가지로, 세 번째 인수로 예외의 메시지, 네 번째 인수로 커스텀 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-app"></a>
<!-- #### `app()` -->
#### `app()`

<!-- The `app` function returns the [service container](/docs/11.x/container) instance: -->
`app` 함수는 [service container](/docs/11.x/container) 인스턴스를 반환합니다.

```
$container = app();
```

<!-- You may pass a class or interface name to resolve it from the container: -->
클래스나 인터페이스 이름을 인수로 전달하면 컨테이너에서 해당 인스턴스를 해결(resolving)할 수도 있습니다.

```
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
<!-- #### `auth()` -->
#### `auth()`

<!-- The `auth` function returns an [authenticator](/docs/11.x/authentication) instance. You may use it as an alternative to the `Auth` facade: -->
`auth` 함수는 [authenticator](/docs/11.x/authentication) 인스턴스를 반환합니다. `Auth` 파사드의 대체 방법으로도 사용할 수 있습니다.

```
$user = auth()->user();
```

<!-- If needed, you may specify which guard instance you would like to access: -->
필요하다면 접근하고자 하는 가드 인스턴스의 이름을 지정할 수도 있습니다.

```
$user = auth('admin')->user();
```

<a name="method-back"></a>
<!-- #### `back()` -->
#### `back()`

<!-- The `back` function generates a [redirect HTTP response](/docs/11.x/responses#redirects) to the user's previous location: -->
`back` 함수는 사용자의 이전 위치로 [redirect HTTP response](/docs/11.x/responses#redirects)을 생성합니다.

```
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
<!-- #### `bcrypt()` -->
#### `bcrypt()`

<!-- The `bcrypt` function [hashes](/docs/11.x/hashing) the given value using Bcrypt. You may use this function as an alternative to the `Hash` facade: -->
`bcrypt` 함수는 주어진 값을 Bcrypt로 [hashes](/docs/11.x/hashing)합니다. 이 함수는 `Hash` 파사드의 대체 방법으로 사용할 수 있습니다.

```
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
<!-- #### `blank()` -->
#### `blank()`

<!-- The `blank` function determines whether the given value is "blank": -->
`blank` 함수는 주어진 값이 "비어있는 값(blank)"인지 확인합니다.

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
`blank`와 반대 동작이 필요한 경우 [`filled`](#method-filled) 메서드를 참고하세요.

<a name="method-broadcast"></a>
<!-- #### `broadcast()` -->
#### `broadcast()`

<!-- The `broadcast` function [broadcasts](/docs/11.x/broadcasting) the given [event](/docs/11.x/events) to its listeners: -->
`broadcast` 함수는 주어진 [broadcasts](/docs/11.x/broadcasting)를 [event](/docs/11.x/events)하여 리스너들에게 전달합니다.

```
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
<!-- #### `cache()` -->
#### `cache()`

<!-- The `cache` function may be used to get values from the [cache](/docs/11.x/cache). If the given key does not exist in the cache, an optional default value will be returned: -->
`cache` 함수는 [cache](/docs/11.x/cache)에서 값을 가져올 때 사용할 수 있습니다. 전달한 키가 캐시에 없으면, 두 번째 인수로 지정한 기본값이 반환됩니다.

```
$value = cache('key');

$value = cache('key', 'default');
```

<!-- You may add items to the cache by passing an array of key / value pairs to the function. You should also pass the number of seconds or duration the cached value should be considered valid: -->
캐시에 값을 저장하려면, 키/값 쌍의 배열과 함께 캐시된 값을 유효하다고 간주할 초 단위 시간이나 기간(duration)을 전달하면 됩니다.

```
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
<!-- #### `class_uses_recursive()` -->
#### `class_uses_recursive()`

<!-- The `class_uses_recursive` function returns all traits used by a class, including traits used by all of its parent classes: -->
`class_uses_recursive` 함수는 클래스가 사용하는 모든 trait을 반환하며, 상위 클래스(부모 클래스)에서 사용하는 trait도 모두 포함됩니다.

```
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
<!-- #### `collect()` -->
#### `collect()`

<!-- The `collect` function creates a [collection](/docs/11.x/collections) instance from the given value: -->
`collect` 함수는 전달된 값에서 [collection](/docs/11.x/collections) 인스턴스를 생성합니다.

```
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
<!-- #### `config()` -->
#### `config()`

<!-- The `config` function gets the value of a [configuration](/docs/11.x/configuration) variable. The configuration values may be accessed using "dot" syntax, which includes the name of the file and the option you wish to access. A default value may be specified and is returned if the configuration option does not exist: -->
`config` 함수는 [configuration](/docs/11.x/configuration) 변수의 값을 가져옵니다. 설정 값은 "dot" 구문을 사용하여 파일 이름과 접근할 옵션을 지정할 수 있습니다. 해당 설정 키가 존재하지 않을 경우 사용할 기본값을 두 번째 인수로 지정할 수 있습니다.

```
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

<!-- You may set configuration variables at runtime by passing an array of key / value pairs. However, note that this function only affects the configuration value for the current request and does not update your actual configuration values: -->
실행 중에 설정값을 변경하려면, 키/값 쌍의 배열을 전달하면 됩니다. 단, 이 함수로 변경된 값은 현재 요청에서만 적용되며 실제 설정 파일은 변경되지 않습니다.

```
config(['app.debug' => true]);
```

<a name="method-context"></a>
<!-- #### `context()` -->
#### `context()`

<!-- The `context` function gets the value from the [current context](/docs/11.x/context). A default value may be specified and is returned if the context key does not exist: -->
`context` 함수는 [current context](/docs/11.x/context)에서 값을 가져옵니다. 컨텍스트 키가 없다면 기본값을 두 번째 인수로 지정할 수 있습니다.

```
$value = context('trace_id');

$value = context('trace_id', $default);
```

<!-- You may set context values by passing an array of key / value pairs: -->
키/값 쌍의 배열을 전달해 컨텍스트 값을 설정할 수도 있습니다.

```
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
<!-- #### `cookie()` -->
#### `cookie()`

<!-- The `cookie` function creates a new [cookie](/docs/11.x/requests#cookies) instance: -->
`cookie` 함수는 새로운 [cookie](/docs/11.x/requests#cookies) 인스턴스를 생성합니다.

```
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
<!-- #### `csrf_field()` -->
#### `csrf_field()`

<!-- The `csrf_field` function generates an HTML `hidden` input field containing the value of the CSRF token. For example, using [Blade syntax](/docs/11.x/blade): -->
`csrf_field` 함수는 CSRF 토큰 값을 담는 HTML `hidden` input 필드를 생성합니다. 예를 들어, [Blade syntax](/docs/11.x/blade)에서 사용하면 다음과 같습니다.

```
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
<!-- #### `csrf_token()` -->
#### `csrf_token()`

<!-- The `csrf_token` function retrieves the value of the current CSRF token: -->
`csrf_token` 함수는 현재의 CSRF 토큰 값을 가져옵니다.

```
$token = csrf_token();
```

<a name="method-decrypt"></a>
<!-- #### `decrypt()` -->
#### `decrypt()`

<!-- The `decrypt` function [decrypts](/docs/11.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade: -->
`decrypt` 함수는 전달된 값을 [decrypts](/docs/11.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대체 방법으로 사용할 수 있습니다.

```
$password = decrypt($value);
```

<a name="method-dd"></a>
<!-- #### `dd()` -->
#### `dd()`

<!-- The `dd` function dumps the given variables and ends the execution of the script: -->
`dd` 함수는 전달된 변수 값을 덤프(dump)하고 스크립트의 실행을 즉시 중단(종료)합니다.

```
dd($value);

dd($value1, $value2, $value3, ...);
```

<!-- If you do not want to halt the execution of your script, use the [`dump`](#method-dump) function instead. -->
스크립트 실행을 중단하지 않고 변수 값만 출력하려면 [`dump`](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
<!-- #### `dispatch()` -->
#### `dispatch()`

<!-- The `dispatch` function pushes the given [job](/docs/11.x/queues#creating-jobs) onto the Laravel [job queue](/docs/11.x/queues): -->
`dispatch` 함수는 주어진 [job](/docs/11.x/queues#creating-jobs)을 Laravel의 [job queue](/docs/11.x/queues)에 푸시합니다.

```
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
<!-- #### `dispatch_sync()` -->
#### `dispatch_sync()`

<!-- The `dispatch_sync` function pushes the given job to the [sync](/docs/11.x/queues#synchronous-dispatching) queue so that it is processed immediately: -->
`dispatch_sync` 함수는 주어진 작업을 [sync](/docs/11.x/queues#synchronous-dispatching)에 바로 푸시하여 즉시 처리하게 합니다.

```
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
<!-- #### `dump()` -->
#### `dump()`

<!-- The `dump` function dumps the given variables: -->
`dump` 함수는 전달된 변수의 값을 출력(덤프)합니다.

```
dump($value);

dump($value1, $value2, $value3, ...);
```

<!-- If you want to stop executing the script after dumping the variables, use the [`dd`](#method-dd) function instead. -->
값을 출력한 뒤 스크립트 실행도 멈추고 싶다면 [`dd`](#method-dd) 함수를 사용하세요.

<a name="method-encrypt"></a>
<!-- #### `encrypt()` -->
#### `encrypt()`

<!-- The `encrypt` function [encrypts](/docs/11.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade: -->
`encrypt` 함수는 전달된 값을 [encrypts](/docs/11.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대체 방법으로 사용할 수 있습니다.

```
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
<!-- #### `env()` -->
#### `env()`

<!-- The `env` function retrieves the value of an [environment variable](/docs/11.x/configuration#environment-configuration) or returns a default value: -->
`env` 함수는 [environment variable](/docs/11.x/configuration#environment-configuration)의 값을 가져오거나, 해당 값이 없으면 기본값을 반환합니다.

```
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행하는 경우, 반드시 `env` 함수를 설정 파일 내부에서만 호출해야 합니다. 구성이 캐시되면 `.env` 파일이 로드되지 않으며, `env` 함수 호출의 반환값은 모두 `null`이 됩니다.

<a name="method-event"></a>
<!-- #### `event()` -->
#### `event()`

<!-- The `event` function dispatches the given [event](/docs/11.x/events) to its listeners: -->
`event` 함수는 전달한 [event](/docs/11.x/events)를 리스너들에게 디스패치(전달)합니다.

```
event(new UserRegistered($user));
```

<a name="method-fake"></a>
<!-- #### `fake()` -->
#### `fake()`

<!-- The `fake` function resolves a [Faker](https://github.com/FakerPHP/Faker) singleton from the container, which can be useful when creating fake data in model factories, database seeding, tests, and prototyping views: -->
`fake` 함수는 컨테이너에서 [Faker](https://github.com/FakerPHP/Faker) 싱글턴을 가져옵니다. 이 함수는 모델 팩토리, DB 시드(seed), 테스트, 뷰 프로토타이핑 등에서 더미 데이터를 생성할 때 유용하게 사용할 수 있습니다.

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
기본적으로 `fake` 함수는 `config/app.php`의 `app.faker_locale` 설정값을 사용합니다. 일반적으로 이 설정은 `APP_FAKER_LOCALE` 환경 변수로 지정됩니다. 직접 로케일(locale)을 지정하려면, `fake` 함수에 로케일을 인수로 전달하세요. 각 로케일마다 별도의 싱글턴이 생성됩니다.

```
fake('nl_NL')->name()
```

<a name="method-filled"></a>
<!-- #### `filled()` -->
#### `filled()`

<!-- The `filled` function determines whether the given value is not "blank": -->
`filled` 함수는 주어진 값이 "비어있지 않은 값"인지 확인합니다.

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
`filled`와 반대 동작이 필요한 경우 [`blank`](#method-blank) 메서드를 참고하세요.

<a name="method-info"></a>
<!-- #### `info()` -->
#### `info()`

<!-- The `info` function will write information to your application's [log](/docs/11.x/logging): -->
`info` 함수는 애플리케이션의 [log](/docs/11.x/logging)에 정보를 기록합니다.

```
info('Some helpful information!');
```

<!-- An array of contextual data may also be passed to the function: -->
이 함수에 컨텍스트 데이터를 배열로 함께 전달할 수도 있습니다.

```
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
<!-- #### `literal()` -->
#### `literal()`

<!-- The `literal` function creates a new [stdClass](https://www.php.net/manual/en/class.stdclass.php) instance with the given named arguments as properties: -->
`literal` 함수는 제공된 이름 있는 인수들을 property로 가지는 새로운 [stdClass](https://www.php.net/manual/en/class.stdclass.php) 인스턴스를 생성합니다.

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
`logger` 함수는 [log](/docs/11.x/logging)에 `debug` 레벨 메시지를 기록할 때 사용할 수 있습니다.

```
logger('Debug message');
```

<!-- An array of contextual data may also be passed to the function: -->
이 함수에도 컨텍스트 데이터를 배열로 함께 전달할 수 있습니다.

```
logger('User has logged in.', ['id' => $user->id]);
```

<!-- A [logger](/docs/11.x/logging) instance will be returned if no value is passed to the function: -->
값을 전달하지 않으면 [logger](/docs/11.x/logging) 인스턴스가 반환됩니다.

```
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>

<!-- #### `method_field()` -->
#### `method_field()`

<!-- The `method_field` function generates an HTML `hidden` input field containing the spoofed value of the form's HTTP verb. For example, using [Blade syntax](/docs/11.x/blade): -->
`method_field` 함수는 폼의 HTTP 메서드를 위조(spoof)하는 값을 담은 HTML `hidden` 입력 필드를 생성합니다. 예를 들어, [Blade syntax](/docs/11.x/blade)을 사용할 때 다음과 같이 활용할 수 있습니다.

```
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
<!-- #### `now()` -->
#### `now()`

<!-- The `now` function creates a new `Illuminate\Support\Carbon` instance for the current time: -->
`now` 함수는 현재 시각을 나타내는 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```
$now = now();
```

<a name="method-old"></a>
<!-- #### `old()` -->
#### `old()`

<!-- The `old` function [retrieves](/docs/11.x/requests#retrieving-input) an [old input](/docs/11.x/requests#old-input) value flashed into the session: -->
`old` 함수는 [retrieves](/docs/11.x/requests#retrieving-input) [old input](/docs/11.x/requests#old-input)을 조회합니다.

```
$value = old('value');

$value = old('value', 'default');
```

<!-- Since the "default value" provided as the second argument to the `old` function is often an attribute of an Eloquent model, Laravel allows you to simply pass the entire Eloquent model as the second argument to the `old` function. When doing so, Laravel will assume the first argument provided to the `old` function is the name of the Eloquent attribute that should be considered the "default value": -->
`old` 함수에 두 번째 인자로 "기본값"을 지정하는 경우, 이 값이 종종 Eloquent 모델의 속성(property)일 때가 많기 때문에, Laravel에서는 `old` 함수의 두 번째 인자에 전체 Eloquent 모델을 바로 전달할 수 있습니다. 이렇게 전달하면, `old` 함수의 첫 번째 인자를 Eloquent의 속성명으로 간주하여, 이를 기본값으로 사용하게 됩니다.

```
{{ old('name', $user->name) }}

// Is equivalent to...

{{ old('name', $user) }}
```

<a name="method-once"></a>
<!-- #### `once()` -->
#### `once()`

<!-- The `once` function executes the given callback and caches the result in memory for the duration of the request. Any subsequent calls to the `once` function with the same callback will return the previously cached result: -->
`once` 함수는 전달받은 콜백을 실행하고, 그 결과를 해당 요청 동안 메모리에 캐시합니다. 이후 동일한 콜백으로 `once`를 다시 호출하면 이미 캐시된 결과가 반환됩니다.

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
객체 인스턴스 내에서 `once` 함수를 실행하면, 각 객체 인스턴스별로 고유한 캐시 결과를 가집니다.

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
`optional` 함수는 어떤 인자든 받아 해당 객체의 속성이나 메서드에 접근할 수 있게 해줍니다. 만약 전달된 객체가 `null`이면, 속성이나 메서드도 `null`을 반환하므로 에러가 발생하지 않습니다.

```
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

<!-- The `optional` function also accepts a closure as its second argument. The closure will be invoked if the value provided as the first argument is not null: -->
또한 `optional` 함수의 두 번째 인자로 클로저를 넘길 수도 있습니다. 첫 번째 인자로 받은 값이 null이 아니면 이 클로저가 실행됩니다.

```
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
<!-- #### `policy()` -->
#### `policy()`

<!-- The `policy` method retrieves a [policy](/docs/11.x/authorization#creating-policies) instance for a given class: -->
`policy` 함수는 주어진 클래스에 대한 [policy](/docs/11.x/authorization#creating-policies) 인스턴스를 반환합니다.

```
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
<!-- #### `redirect()` -->
#### `redirect()`

<!-- The `redirect` function returns a [redirect HTTP response](/docs/11.x/responses#redirects), or returns the redirector instance if called with no arguments: -->
`redirect` 함수는 [redirect HTTP response](/docs/11.x/responses#redirects)을 반환하거나, 인자를 지정하지 않으면 리디렉터 인스턴스를 반환합니다.

```
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
<!-- #### `report()` -->
#### `report()`

<!-- The `report` function will report an exception using your [exception handler](/docs/11.x/errors#handling-exceptions): -->
`report` 함수는 [exception handler](/docs/11.x/errors#handling-exceptions)를 사용하여 예외를 보고(report)합니다.

```
report($e);
```

<!-- The `report` function also accepts a string as an argument. When a string is given to the function, the function will create an exception with the given string as its message: -->
`report` 함수는 문자열을 인자로 받을 수도 있습니다. 문자열이 주어지면 해당 문자열을 메시지로 가지는 예외가 생성되어 보고됩니다.

```
report('Something went wrong.');
```

<a name="method-report-if"></a>
<!-- #### `report_if()` -->
#### `report_if()`

<!-- The `report_if` function will report an exception using your [exception handler](/docs/11.x/errors#handling-exceptions) if the given condition is `true`: -->
`report_if` 함수는 주어진 조건이 `true`인 경우, [exception handler](/docs/11.x/errors#handling-exceptions)를 사용하여 예외를 보고합니다.

```
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
<!-- #### `report_unless()` -->
#### `report_unless()`

<!-- The `report_unless` function will report an exception using your [exception handler](/docs/11.x/errors#handling-exceptions) if the given condition is `false`: -->
`report_unless` 함수는 주어진 조건이 `false`인 경우, [exception handler](/docs/11.x/errors#handling-exceptions)를 사용하여 예외를 보고합니다.

```
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
<!-- #### `request()` -->
#### `request()`

<!-- The `request` function returns the current [request](/docs/11.x/requests) instance or obtains an input field's value from the current request: -->
`request` 함수는 현재 [request](/docs/11.x/requests) 인스턴스를 반환하거나, 현재 요청에서 특정 입력 필드의 값을 가져옵니다.

```
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
<!-- #### `rescue()` -->
#### `rescue()`

<!-- The `rescue` function executes the given closure and catches any exceptions that occur during its execution. All exceptions that are caught will be sent to your [exception handler](/docs/11.x/errors#handling-exceptions); however, the request will continue processing: -->
`rescue` 함수는 전달된 클로저를 실행하고, 내부에서 발생하는 예외를 포착합니다. 포착한 모든 예외는 [exception handler](/docs/11.x/errors#handling-exceptions)에 전달되지만, 요청 처리는 계속됩니다.

```
return rescue(function () {
    return $this->method();
});
```

<!-- You may also pass a second argument to the `rescue` function. This argument will be the "default" value that should be returned if an exception occurs while executing the closure: -->
`rescue` 함수에 두 번째 인자를 전달하면, 이 값은 클로저 실행 중 예외가 발생했을 때 반환되는 "기본값"이 됩니다.

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
`rescue` 함수에 `report` 인자를 전달하여, 예외를 `report` 함수로 보고할지 여부를 결정할 수도 있습니다.

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
`resolve` 함수는 [service container](/docs/11.x/container)를 이용해 주어진 클래스 또는 인터페이스명을 인스턴스로 해결합니다.

```
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
<!-- #### `response()` -->
#### `response()`

<!-- The `response` function creates a [response](/docs/11.x/responses) instance or obtains an instance of the response factory: -->
`response` 함수는 [response](/docs/11.x/responses) 인스턴스를 생성하거나, 응답 팩토리 인스턴스를 획득합니다.

```
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
<!-- #### `retry()` -->
#### `retry()`

<!-- The `retry` function attempts to execute the given callback until the given maximum attempt threshold is met. If the callback does not throw an exception, its return value will be returned. If the callback throws an exception, it will automatically be retried. If the maximum attempt count is exceeded, the exception will be thrown: -->
`retry` 함수는 지정한 최대 시도 횟수만큼 콜백을 반복 실행합니다. 콜백이 예외를 발생시키지 않으면 해당 반환값이 반환됩니다. 만약 예외가 발생하면 자동으로 재시도하며, 최대 시도 횟수를 초과하면 예외가 다시 발생합니다.

```
return retry(5, function () {
    // Attempt 5 times while resting 100ms between attempts...
}, 100);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the third argument to the `retry` function: -->
시도 간 대기 시간을 직접 계산해서 지정하고 싶다면, `retry`의 세 번째 인자로 클로저를 전달할 수 있습니다.

```
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

<!-- For convenience, you may provide an array as the first argument to the `retry` function. This array will be used to determine how many milliseconds to sleep between subsequent attempts: -->
편의상, `retry` 함수의 첫 번째 인자로 배열을 전달할 수 있습니다. 이 배열의 각 값이 각 시도 간 대기할 밀리초 단위 시간으로 사용됩니다.

```
return retry([100, 200], function () {
    // Sleep for 100ms on first retry, 200ms on second retry...
});
```

<!-- To only retry under specific conditions, you may pass a closure as the fourth argument to the `retry` function: -->
특정 조건에서만 재시도를 원한다면, `retry` 함수의 네 번째 인자로 클로저를 전달할 수 있습니다.

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
`session` 함수는 [session](/docs/11.x/session) 값을 조회하거나 설정하는 데 사용할 수 있습니다.

```
$value = session('key');
```

<!-- You may set values by passing an array of key / value pairs to the function: -->
키/값 쌍의 배열을 넘겨 값을 설정할 수도 있습니다.

```
session(['chairs' => 7, 'instruments' => 3]);
```

<!-- The session store will be returned if no value is passed to the function: -->
값을 지정하지 않으면 세션 스토어 인스턴스가 반환됩니다.

```
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
<!-- #### `tap()` -->
#### `tap()`

<!-- The `tap` function accepts two arguments: an arbitrary `$value` and a closure. The `$value` will be passed to the closure and then be returned by the `tap` function. The return value of the closure is irrelevant: -->
`tap` 함수는 두 개의 인자, 임의의 `$value`와 클로저를 받습니다. `$value`는 클로저에 전달된 뒤 `tap` 함수가 그대로 반환하며, 클로저의 반환값은 무시됩니다.

```
$user = tap(User::first(), function (User $user) {
    $user->name = 'taylor';

    $user->save();
});
```

<!-- If no closure is passed to the `tap` function, you may call any method on the given `$value`. The return value of the method you call will always be `$value`, regardless of what the method actually returns in its definition. For example, the Eloquent `update` method typically returns an integer. However, we can force the method to return the model itself by chaining the `update` method call through the `tap` function: -->
`tap` 함수에 클로저를 넘기지 않으면, 전달한 `$value`에 어떤 메서드든 호출할 수 있습니다. 이때 메서드의 실제 정의상 반환값과 관계없이 항상 `$value`가 반환됩니다. 예를 들어, Eloquent의 `update` 메서드는 보통 정수를 반환하지만, `update` 메서드 호출을 `tap` 함수를 통해 체이닝하면 항상 모델 인스턴스 자신을 반환하도록 만들 수 있습니다.

```
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

<!-- To add a `tap` method to a class, you may add the `Illuminate\Support\Traits\Tappable` trait to the class. The `tap` method of this trait accepts a Closure as its only argument. The object instance itself will be passed to the Closure and then be returned by the `tap` method: -->
클래스에 `tap` 메서드를 추가하려면, `Illuminate\Support\Traits\Tappable` 트레이트를 해당 클래스에 추가하면 됩니다. 이 트레이트의 `tap` 메서드는 유일한 인자로 클로저를 받습니다. 객체 인스턴스 자체가 클로저로 전달된 후 `tap` 메서드가 그 인스턴스를 반환합니다.

```
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
<!-- #### `throw_if()` -->
#### `throw_if()`

<!-- The `throw_if` function throws the given exception if a given boolean expression evaluates to `true`: -->
`throw_if` 함수는 주어진 불리언 표현식이 `true`이면 주어진 예외를 던집니다.

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
`throw_unless` 함수는 주어진 불리언 표현식이 `false`이면 주어진 예외를 던집니다.

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
`today` 함수는 오늘 날짜를 나타내는 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```
$today = today();
```

<a name="method-trait-uses-recursive"></a>
<!-- #### `trait_uses_recursive()` -->
#### `trait_uses_recursive()`

<!-- The `trait_uses_recursive` function returns all traits used by a trait: -->
`trait_uses_recursive` 함수는 지정한 트레이트가 사용하는 모든 트레이트 목록을 반환합니다.

```
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
<!-- #### `transform()` -->
#### `transform()`

<!-- The `transform` function executes a closure on a given value if the value is not [blank](#method-blank) and then returns the return value of the closure: -->
`transform` 함수는 주어진 값이 [blank](#method-blank)가 아니면 해당 값에 클로저를 실행하고, 그 결과를 반환합니다.

```
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

<!-- A default value or closure may be passed as the third argument to the function. This value will be returned if the given value is blank: -->
값이 비어있을 때 반환할 "기본값"이나 클로저를 세 번째 인자로 지정할 수도 있습니다. 이 값은 첫 번째 인자가 비어있을 때 대신 반환됩니다.

```
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
<!-- #### `validator()` -->
#### `validator()`

<!-- The `validator` function creates a new [validator](/docs/11.x/validation) instance with the given arguments. You may use it as an alternative to the `Validator` facade: -->
`validator` 함수는 전달받은 인자들을 사용해 새로운 [validator](/docs/11.x/validation) 인스턴스를 생성합니다. 이를 `Validator` 파사드의 대안으로 사용할 수 있습니다.

```
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
<!-- #### `value()` -->
#### `value()`

<!-- The `value` function returns the value it is given. However, if you pass a closure to the function, the closure will be executed and its returned value will be returned: -->
`value` 함수는 주어진 값을 바로 반환합니다. 단, 클로저를 전달한 경우에는 해당 클로저를 실행해서 나온 결과를 반환합니다.

```
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

<!-- Additional arguments may be passed to the `value` function. If the first argument is a closure then the additional parameters will be passed to the closure as arguments, otherwise they will be ignored: -->
`value` 함수에 추가 인자를 넘길 경우, 첫 번째 인자가 클로저라면 이 추가 인자들이 클로저의 인수로 전달됩니다. 그렇지 않으면 무시됩니다.

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
`view` 함수는 [view](/docs/11.x/views) 인스턴스를 반환합니다.

```
return view('auth.login');
```

<a name="method-with"></a>
<!-- #### `with()` -->
#### `with()`

<!-- The `with` function returns the value it is given. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned: -->
`with` 함수는 전달한 값을 반환합니다. 만약 두 번째 인자로 클로저가 전달되면, 해당 클로저를 실행하여 반환된 값을 반환합니다.

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
`when` 함수는 주어진 조건이 `true`일 때 전달한 값을 반환하고, 그렇지 않으면 `null`을 반환합니다. 두 번째 인자로 클로저를 넘기면, 해당 조건이 `true`일 때 클로저를 실행하여 나온 값을 반환합니다.

```
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

<!-- The `when` function is primarily useful for conditionally rendering HTML attributes: -->
`when` 함수는 HTML 속성 등을 조건부로 렌더링해야 할 때 유용하게 사용할 수 있습니다.

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
애플리케이션의 특정 부분 성능을 빠르게 테스트하고 싶은 경우가 있습니다. 그럴 때에는 `Benchmark` 지원 클래스를 활용해 지정한 콜백이 완료되는 데 걸린 밀리초(ms) 시간을 측정할 수 있습니다.

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
기본적으로 전달받은 콜백은 한 번(1회 반복) 실행되며, 그 소요 시간이 브라우저/콘솔에 표시됩니다.

<!-- To invoke a callback more than once, you may specify the number of iterations that the callback should be invoked as the second argument to the method. When executing a callback more than once, the `Benchmark` class will return the average amount of milliseconds it took to execute the callback across all iterations: -->
콜백을 여러 번 실행하고 싶다면, 두 번째 인자로 반복 횟수를 지정하면 됩니다. 여러 번 실행하는 경우, `Benchmark` 클래스는 전체 반복 동안 콜백 실행에 걸린 평균 밀리초(ms) 시간을 반환합니다.

```
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

<!-- Sometimes, you may want to benchmark the execution of a callback while still obtaining the value returned by the callback. The `value` method will return a tuple containing the value returned by the callback and the amount of milliseconds it took to execute the callback: -->
콜백 실행 시간을 측정하되, 콜백의 반환값도 함께 받고 싶다면, `value` 메서드를 사용하면 됩니다. 이 메서드는 콜백의 반환값과 실행에 걸린 밀리초 단위 시간을 튜플로 반환합니다.

```
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
<!-- ### Dates -->
### Dates

<!-- Laravel includes [Carbon](https://carbon.nesbot.com/docs/), a powerful date and time manipulation library. To create a new `Carbon` instance, you may invoke the `now` function. This function is globally available within your Laravel application: -->
Laravel에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜 및 시간 처리 라이브러리가 기본 탑재되어 있습니다. 새로운 `Carbon` 인스턴스를 만들기 위해 `now` 함수를 사용할 수 있습니다. 이 함수는 Laravel 애플리케이션 전체에서 전역적으로 사용할 수 있습니다.

```php
$now = now();
```

<!-- Or, you may create a new `Carbon` instance using the `Illuminate\Support\Carbon` class: -->
또는 `Illuminate\Support\Carbon` 클래스를 사용해 새 `Carbon` 인스턴스를 만들 수도 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

<!-- For a thorough discussion of Carbon and its features, please consult the [official Carbon documentation](https://carbon.nesbot.com/docs/). -->
Carbon과 관련한 자세한 사용법은 [official Carbon documentation](https://carbon.nesbot.com/docs/)를 참고하시기 바랍니다.

<a name="deferred-functions"></a>
<!-- ### Deferred Functions -->
### Deferred Functions

> [!WARNING]
> 지연 함수(Deferred Functions)는 현재 베타 상태입니다. 커뮤니티 피드백을 받고 있습니다.

<!-- While Laravel's [queued jobs](/docs/11.x/queues) allow you to queue tasks for background processing, sometimes you may have simple tasks you would like to defer without configuring or maintaining a long-running queue worker. -->
Laravel의 [queued jobs](/docs/11.x/queues)을 이용하면 작업을 백그라운드에서 실행할 수 있지만, 별도의 장기 실행 큐 워커를 구성·관리하지 않고 간단히 실행을 미루고 싶은 작업도 있을 수 있습니다.

<!-- Deferred functions allow you to defer the execution of a closure until after the HTTP response has been sent to the user, keeping your application feeling fast and responsive. To defer the execution of a closure, simply pass the closure to the `Illuminate\Support\defer` function: -->
지연 함수(Deferred functions)는 클로저 실행을 HTTP 응답이 사용자에게 보내진 후로 미루어, 애플리케이션이 더 빠르고 반응성 있게 느껴지도록 만들어 줍니다. 클로저를 `Illuminate\Support\defer` 함수로 감싸면 쉽게 실행을 늦출 수 있습니다.

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
기본적으로, 지연 함수는 `Illuminate\Support\defer`가 호출된 HTTP 응답, 아티즌 명령, 또는 큐 작업이 정상적으로 완료된 경우에만 실행됩니다. 즉, 요청이 `4xx`나 `5xx` HTTP 응답으로 종료되면 지연 함수는 실행되지 않습니다. 지연 함수가 항상 실행되도록 하려면, `always` 메서드를 사용하면 됩니다.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>

<!-- #### Cancelling Deferred Functions -->
#### Cancelling Deferred Functions

<!-- If you need to cancel a deferred function before it is executed, you can use the `forget` method to cancel the function by its name. To name a deferred function, provide a second argument to the `Illuminate\Support\defer` function: -->
지연 함수가 실행되기 전에 취소해야 할 필요가 있다면, `forget` 메서드를 사용하여 해당 함수의 이름으로 취소할 수 있습니다. 지연 함수에 이름을 지정하려면 `Illuminate\Support\defer` 함수에 두 번째 인수를 전달하면 됩니다.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="deferred-function-compatibility"></a>
<!-- #### Deferred Function Compatibility -->
#### Deferred Function Compatibility

<!-- If you upgraded to Laravel 11.x from a Laravel 10.x application and your application's skeleton still contains an `app/Http/Kernel.php` file, you should add the `InvokeDeferredCallbacks` middleware to the beginning of the kernel's `$middleware` property: -->
Laravel 10.x 애플리케이션에서 Laravel 11.x로 업그레이드했으며, 프로젝트 구조에 아직 `app/Http/Kernel.php` 파일이 남아 있다면, 커널의 `$middleware` 속성 맨 앞에 `InvokeDeferredCallbacks` 미들웨어를 추가해야 합니다.

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
테스트를 작성할 때, 지연 함수를 비활성화하는 것이 필요할 수 있습니다. 테스트 내에서 `withoutDefer`를 호출하면, Laravel이 모든 지연 함수를 즉시 실행하도록 할 수 있습니다.

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
테스트 케이스 내의 모든 테스트에서 지연 함수를 비활성화하고 싶다면, 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer` 메서드를 호출할 수 있습니다.

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
Laravel의 Lottery 클래스는 지정한 확률에 따라 콜백을 실행할 수 있게 해줍니다. 이는 들어오는 요청의 일부 비율에서만 특정 코드를 실행하고 싶을 때 유용하게 사용할 수 있습니다.

```
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

<!-- You may combine Laravel's lottery class with other Laravel features. For example, you may wish to only report a small percentage of slow queries to your exception handler. And, since the lottery class is callable, we may pass an instance of the class into any method that accepts callables: -->
Laravel의 Lottery 클래스를 다른 Laravel 기능과 조합하여 사용할 수도 있습니다. 예를 들어, 느린 쿼리를 처리할 때 일부 사례만 익셉션 핸들러로 보고하도록 만들 수 있습니다. 또한 Lottery 클래스는 "호출 가능한 객체(callable)"이기 때문에, 콜러블을 받을 수 있는 모든 메서드에 인스턴스를 바로 전달할 수도 있습니다.

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
Laravel에서는 Lottery 호출을 손쉽게 테스트할 수 있도록 간단한 메서드를 제공합니다.

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
Laravel의 `Pipeline` 파사드는 주어진 입력값을 일련의 인보커블(호출 가능한) 클래스, 클로저, 콜러블을 통해 "파이프" 형태로 전달할 수 있는 편리한 방법을 제공합니다. 각 클래스는 입력값을 검사하거나 수정할 기회를 가지며, 이어서 파이프라인의 다음 콜러블을 호출하게 됩니다.

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
보시다시피, 파이프라인 안의 각 인보커블 클래스나 클로저에는 입력값과 `$next` 클로저가 전달됩니다. `$next` 클로저를 호출하면 파이프라인의 다음 콜러블이 이어서 실행됩니다. 이 구조는 [middleware](/docs/11.x/middleware)와 매우 유사합니다.

<!-- When the last callable in the pipeline invokes the `$next` closure, the callable provided to the `then` method will be invoked. Typically, this callable will simply return the given input. -->
파이프라인의 마지막 콜러블에서 `$next` 클로저가 호출되면, `then` 메서드에 전달한 콜러블이 실행됩니다. 대개 이 콜러블은 전달받은 입력값을 그대로 반환하게 됩니다.

<!-- Of course, as discussed previously, you are not limited to providing closures to your pipeline. You may also provide invokable classes. If a class name is provided, the class will be instantiated via Laravel's [service container](/docs/11.x/container), allowing dependencies to be injected into the invokable class: -->
물론, 클로저뿐 아니라 인보커블 클래스를 파이프라인에 사용할 수도 있습니다. 클래스 이름을 전달하면, 해당 클래스가 Laravel의 [service container](/docs/11.x/container)를 통해 인스턴스화되므로, 의존성 주입을 이용할 수 있습니다.

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
Laravel의 `Sleep` 클래스는 PHP의 내장 `sleep` 및 `usleep` 함수의 경량 래퍼로, 테스트의 용이성과 개발자 친화적 API를 제공합니다. 이를 통해 시간을 다루는 코드를 더 편하게 작성할 수 있습니다.

```
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

<!-- The `Sleep` class offers a variety of methods that allow you to work with different units of time: -->
`Sleep` 클래스에는 다양한 시간 단위로 사용할 수 있는 여러 메서드가 준비되어 있습니다.

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
여러 시간 단위를 쉽게 조합하려면 `and` 메서드를 사용할 수 있습니다.

```
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
<!-- #### Testing Sleep -->
#### Testing Sleep

<!-- When testing code that utilizes the `Sleep` class or PHP's native sleep functions, your test will pause execution. As you might expect, this makes your test suite significantly slower. For example, imagine you are testing the following code: -->
`Sleep` 클래스나 PHP의 내장 sleep 함수를 사용하는 코드를 테스트할 때, 테스트가 실제로 일시정지되기 때문에 테스트 실행 속도가 느려질 수 있습니다. 예를 들어 아래와 같은 코드를 테스트한다고 가정해 봅시다.

```
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

<!-- Typically, testing this code would take _at least_ one second. Luckily, the `Sleep` class allows us to "fake" sleeping so that our test suite stays fast: -->
이 코드를 일반적으로 테스트하면 최소 1초 이상이 걸릴 수 있습니다. 다행히 `Sleep` 클래스는 "sleep"을 가짜로 처리할 수 있어서 테스트 속도를 빠르게 유지할 수 있습니다.

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
`Sleep` 클래스를 가짜(faked)로 만들면, 실제 일시정지가 발생하지 않아 테스트 실행속도가 매우 빨라집니다.

<!-- Once the `Sleep` class has been faked, it is possible to make assertions against the expected "sleeps" that should have occurred. To illustrate this, let's imagine we are testing code that pauses execution three times, with each pause increasing by a single second. Using the `assertSequence` method, we can assert that our code "slept" for the proper amount of time while keeping our test fast: -->
`Sleep` 클래스를 가짜로 만든 후, 실제로 "sleep"이 호출됐는지에 대한 assertion도 할 수 있습니다. 예를 들어, 실행을 세 번 일시정지하고 각각 1초씩 시간이 늘어나는 코드를 테스트한다고 가정해 봅시다. `assertSequence` 메서드를 사용하면 우리 코드가 올바른 시간만큼 "sleep"했다는 것을 검증할 수 있습니다.

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
이 외에도 `Sleep` 클래스는 테스트 시 활용할 수 있는 다양한 assertion 메서드를 제공합니다.

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
경우에 따라, 애플리케이션 코드에서 가짜 sleep이 발생할 때마다 추가 동작을 하고 싶을 수 있습니다. 이를 위해 `whenFakingSleep` 메서드에 콜백을 전달할 수 있습니다. 아래 예시에서는 Laravel의 [time manipulation helpers](/docs/11.x/mocking#interacting-with-time)를 사용하여, sleep된 시간만큼 즉시 시간을 진행시킵니다.

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
이처럼 시간 진행이 필요한 경우가 많기 때문에, `fake` 메서드의 `syncWithCarbon` 인자를 활용하면 test 내 sleep 동작 시 Carbon 시간과 자동으로 동기화할 수 있습니다.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

<!-- Laravel uses the `Sleep` class internally whenever it is pausing execution. For example, the [`retry`](#method-retry) helper uses the `Sleep` class when sleeping, allowing for improved testability when using that helper. -->
Laravel은 내부적으로 실행 대기를 할 때 항상 `Sleep` 클래스를 사용합니다. 예를 들어 [`retry`](#method-retry) 헬퍼는 sleep 시 `Sleep` 클래스를 사용하게 되므로, 이 헬퍼를 쓸 때도 테스트의 유연성을 얻을 수 있습니다.

<a name="timebox"></a>
<!-- ### Timebox -->
### Timebox

<!-- Laravel's `Timebox` class ensures that the given callback always takes a fixed amount of time to execute, even if its actual execution completes sooner. This is particularly useful for cryptographic operations and user authentication checks, where attackers might exploit variations in execution time to infer sensitive information. -->
Laravel의 `Timebox` 클래스는 주어진 콜백이 실제 실행이 더 빨리 끝나더라도, 언제나 고정된 시간 동안 실행이 되도록 보장합니다. 암호화 작업이나 사용자 인증처럼, 실행 시간에 따른 민감 정보를 노출하지 않아야 하는 경우에 매우 유용합니다.

<!-- If the execution exceeds the fixed duration, `Timebox` has no effect. It is up to the developer to choose a sufficiently long time as the fixed duration to account for worst-case scenarios. -->
만약 실행 시간이 고정 시간(딜레이)보다 오래 걸리면, `Timebox` 는 아무런 영향을 미치지 않습니다. 최악의 실행 시간을 고려해 충분히 넉넉한 고정 시간을 직접 지정해야 합니다.

<!-- The call method accepts a closure and a time limit in microseconds, and then executes the closure and waits until the time limit is reached: -->
call 메서드는 클로저와 마이크로초 단위의 시간 제한을 받아서, 클로저를 호출한 뒤 시간 제한에 도달할 때까지 대기합니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

<!-- If an exception is thrown within the closure, this class will respect the defined delay and re-throw the exception after the delay. -->
콜백 내에서 예외가 발생해도, Timebox는 지정한 대기 시간을 지켜준 후 예외를 다시 던집니다.