# 헬퍼 (Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜와 시간](#dates)
    - [지연 함수](#deferred-functions)
    - [Lottery](#lottery)
    - [Pipeline](#pipeline)
    - [Sleep](#sleep)
    - [Timebox](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel에는 다양한 전역 "헬퍼" PHP 함수가 포함되어 있습니다. 이 함수 중 많은 수는 프레임워크 자체에서 사용하지만, 편리하다고 느낀다면 여러분의 애플리케이션에서도 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

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
### 배열 및 객체

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
### 숫자

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
### 경로

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
### 기타

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
## 배열 및 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()` {.collection-method .first-collection-method}

`Arr::accessible` 메서드는 주어진 값이 배열처럼 접근 가능한지 확인합니다.

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

`Arr::add` 메서드는 주어진 키가 배열에 아직 존재하지 않거나 `null`로 설정되어 있을 때, 해당 키 / 값 쌍을 배열에 추가합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()` {.collection-method}

`Arr::array` 메서드는 [Arr::get()](#method-array-get)과 마찬가지로 "점" 표기법을 사용해 깊게 중첩된 배열에서 값을 가져오지만, 요청한 값이 `array`가 아니면 `InvalidArgumentException`을 던집니다.

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

`Arr::boolean` 메서드는 [Arr::get()](#method-array-get)과 마찬가지로 "점" 표기법을 사용해 깊게 중첩된 배열에서 값을 가져오지만, 요청한 값이 `boolean`이 아니면 `InvalidArgumentException`을 던집니다.

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

`Arr::collapse` 메서드는 배열 또는 컬렉션으로 이루어진 배열을 하나의 배열로 합칩니다.

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()` {.collection-method}

`Arr::crossJoin` 메서드는 주어진 배열들을 크로스 조인하여, 가능한 모든 조합을 담은 데카르트 곱을 반환합니다.

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

`Arr::divide` 메서드는 두 개의 배열을 반환합니다. 하나는 주어진 배열의 키를 담고, 다른 하나는 값을 담습니다.

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()` {.collection-method}

`Arr::dot` 메서드는 다차원 배열을 하나의 단일 레벨 배열로 평탄화하며, 깊이를 나타내기 위해 "점" 표기법을 사용합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-every"></a>
#### `Arr::every()` {.collection-method}

`Arr::every` 메서드는 배열의 모든 값이 주어진 참/거짓 테스트를 통과하는지 확인합니다.
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

`Arr::except` 메서드는 배열에서 주어진 키 / 값 쌍을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-except-values"></a>
#### `Arr::exceptValues()` {.collection-method}

`Arr::exceptValues` 메서드는 배열에서 지정된 값들을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['foo', 'bar', 'baz', 'qux'];

$filtered = Arr::exceptValues($array, ['foo', 'baz']);

// ['bar', 'qux']
```

필터링할 때 엄격한 타입 비교를 사용하려면 `strict` 인수에 `true`를 전달할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$array = [1, '1', 2, '2'];

$filtered = Arr::exceptValues($array, [1, 2], strict: true);

// ['1', '2']
```

<a name="method-array-exists"></a>
#### `Arr::exists()` {.collection-method}

`Arr::exists` 메서드는 제공된 배열에 주어진 키가 존재하는지 확인합니다.

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

`Arr::first` 메서드는 주어진 조건 검사를 통과하는 배열의 첫 번째 요소를 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

메서드의 세 번째 매개변수로 기본값을 전달할 수도 있습니다. 조건 검사를 통과하는 값이 없으면 이 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()` {.collection-method}

`Arr::flatten` 메서드는 다차원 배열을 단일 레벨 배열로 평탄화합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-float"></a>
#### `Arr::float()` {.collection-method}

`Arr::float` 메서드는 [Arr::get()](#method-array-get)과 마찬가지로 `"dot" notation(점 표기법)`을 사용해 깊게 중첩된 배열에서 값을 가져옵니다. 하지만 요청한 값이 `float`가 아니면 `InvalidArgumentException`을 발생시킵니다.

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

`Arr::forget` 메서드는 `"dot" notation(점 표기법)`을 사용해 깊게 중첩된 배열에서 주어진 키 / 값 쌍을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-from"></a>
#### `Arr::from()` {.collection-method}

`Arr::from` 메서드는 다양한 입력 타입을 일반 PHP 배열로 변환합니다. 배열, 객체뿐 아니라 `Arrayable`, `Enumerable`, `Jsonable`, `JsonSerializable` 같은 여러 일반적인 Laravel 인터페이스를 포함해 다양한 입력 타입을 지원합니다. 또한 `Traversable` 및 `WeakMap` 인스턴스도 처리합니다.

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

`Arr::get` 메서드는 `"dot" notation(점 표기법)`을 사용해 깊게 중첩된 배열에서 값을 가져옵니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

`Arr::get` 메서드는 기본값도 받을 수 있습니다. 지정한 키가 배열에 없으면 이 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()` {.collection-method}

`Arr::has` 메서드는 `"dot" notation(점 표기법)`을 사용해 주어진 항목 하나 또는 여러 항목이 배열에 존재하는지 확인합니다.

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

`Arr::hasAll` 메서드는 `"dot" notation(점 표기법)`을 사용해 지정된 모든 키가 주어진 배열에 존재하는지 확인합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Taylor', 'language' => 'PHP'];

Arr::hasAll($array, ['name']); // true
Arr::hasAll($array, ['name', 'language']); // true
Arr::hasAll($array, ['name', 'IDE']); // false
```

<a name="method-array-hasany"></a>
#### `Arr::hasAny()` {.collection-method}

`Arr::hasAny` 메서드는 `"dot" notation(점 표기법)`을 사용해 주어진 항목 집합 중 하나라도 배열에 존재하는지 확인합니다.

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

`Arr::integer` 메서드는 [Arr::get()](#method-array-get)과 마찬가지로 `"dot" notation(점 표기법)`을 사용해 깊게 중첩된 배열에서 값을 가져옵니다. 하지만 요청한 값이 `int`가 아니면 `InvalidArgumentException`을 발생시킵니다.

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

`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열이면 `true`를 반환합니다. 배열의 키가 0부터 시작하는 연속된 숫자 키가 아니라면 “연관 배열”로 간주됩니다.

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()` {.collection-method}

`Arr::isList` 메서드는 주어진 배열의 키가 0부터 시작하는 연속된 정수이면 `true`를 반환합니다.

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()` {.collection-method}

`Arr::join` 메서드는 배열 요소를 문자열로 이어 붙입니다. 이 메서드의 세 번째 인수를 사용하면 배열의 마지막 요소 앞에 사용할 연결 문자열도 지정할 수 있습니다.

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

`Arr::keyBy` 메서드는 주어진 키를 기준으로 배열의 키를 다시 지정합니다. 여러 항목이 같은 키를 가진 경우, 새 배열에는 마지막 항목만 나타납니다.

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

`Arr::last` 메서드는 주어진 조건 검사를 통과하는 배열의 마지막 요소를 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

메서드의 세 번째 인수로 기본값을 전달할 수 있습니다. 조건 검사를 통과하는 값이 없으면 이 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()` {.collection-method}

`Arr::map` 메서드는 배열을 순회하면서 각 값과 키를 주어진 콜백에 전달합니다. 배열의 값은 콜백이 반환한 값으로 대체됩니다.

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

`Arr::mapSpread` 메서드는 배열을 순회하면서 각 중첩 항목의 값을 주어진 클로저에 전달합니다. 클로저는 자유롭게 항목을 수정하고 반환할 수 있으며, 그 결과 수정된 항목들로 이루어진 새 배열이 만들어집니다.

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

`Arr::mapWithKeys` 메서드는 배열을 순회하며 각 값을 지정된 콜백에 전달합니다. 콜백은 하나의 키 / 값 쌍을 포함하는 연관 배열을 반환해야 합니다.

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

`Arr::only` 메서드는 주어진 배열에서 지정된 키 / 값 쌍만 반환합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-only-values"></a>
#### `Arr::onlyValues()` {.collection-method}

`Arr::onlyValues` 메서드는 배열에서 지정된 값만 반환합니다.

```php
use Illuminate\Support\Arr;

$array = ['foo', 'bar', 'baz', 'qux'];

$filtered = Arr::onlyValues($array, ['foo', 'baz']);

// ['foo', 'baz']
```

필터링할 때 엄격한 타입 비교를 사용하려면 `strict` 인수에 `true`를 전달할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$array = [1, '1', 2, '2'];

$filtered = Arr::onlyValues($array, [1, 2], strict: true);

// [1, 2]
```

<a name="method-array-partition"></a>
#### `Arr::partition()` {.collection-method}

`Arr::partition` 메서드는 PHP 배열 구조 분해와 함께 사용하여, 지정된 참 여부 검사를 통과하는 요소와 통과하지 않는 요소를 분리할 수 있습니다.

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

`Arr::pluck` 메서드는 배열에서 지정된 키에 해당하는 모든 값을 가져옵니다.

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

결과 목록의 키를 어떻게 지정할지도 함께 지정할 수 있습니다.

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()` {.collection-method}

`Arr::prepend` 메서드는 배열의 맨 앞에 항목을 추가합니다.

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

필요하다면 값에 사용할 키를 지정할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()` {.collection-method}

`Arr::prependKeysWith`는 연관 배열의 모든 키 이름 앞에 지정된 접두사를 붙입니다.

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

`Arr::pull` 메서드는 배열에서 키 / 값 쌍을 반환한 뒤 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

메서드의 세 번째 인수로 기본값을 전달할 수 있습니다. 키가 존재하지 않으면 이 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-push"></a>
#### `Arr::push()` {.collection-method}

`Arr::push` 메서드는 `"dot"` 표기법을 사용하여 배열에 항목을 추가합니다. 지정된 키에 배열이 존재하지 않으면 새로 생성됩니다.

```php
use Illuminate\Support\Arr;

$array = [];

Arr::push($array, 'office.furniture', 'Desk');

// $array: ['office' => ['furniture' => ['Desk']]]
```

<a name="method-array-query"></a>
#### `Arr::query()` {.collection-method}

`Arr::query` 메서드는 배열을 쿼리 문자열로 변환합니다.

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

`Arr::random` 메서드는 배열에서 무작위 값을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (retrieved randomly)
```

선택적 두 번째 인수로 반환할 항목 수를 지정할 수도 있습니다. 이 인수를 제공하면 항목을 하나만 원하더라도 배열이 반환된다는 점에 유의하십시오.

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (retrieved randomly)
```

<a name="method-array-reject"></a>
#### `Arr::reject()` {.collection-method}

`Arr::reject` 메서드는 지정된 클로저를 사용하여 배열에서 항목을 제거합니다.

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

`Arr::select` 메서드는 배열에서 값 배열을 선택합니다.

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

`Arr::set` 메서드는 `"dot"` 표기법을 사용하여 깊게 중첩된 배열 안의 값을 설정합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()` {.collection-method}

`Arr::shuffle` 메서드는 배열의 항목을 무작위로 섞습니다.

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-array-sole"></a>
#### `Arr::sole()` {.collection-method}

`Arr::sole` 메서드는 지정된 클로저를 사용하여 배열에서 단일 값을 가져옵니다. 배열 안에서 지정된 참 여부 검사를 통과하는 값이 둘 이상이면 `Illuminate\Support\MultipleItemsFoundException` 예외가 발생합니다. 참 여부 검사를 통과하는 값이 없으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

// 'Desk'
```

<a name="method-array-some"></a>
#### `Arr::some()` {.collection-method}

`Arr::some` 메서드는 배열의 값 중 적어도 하나가 지정된 참 여부 검사를 통과하는지 확인합니다.

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3];

Arr::some($array, fn ($i) => $i > 2);

// true
```

<a name="method-array-sort"></a>
#### `Arr::sort()` {.collection-method}

`Arr::sort` 메서드는 배열을 값 기준으로 정렬합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

지정된 클로저의 결과를 기준으로 배열을 정렬할 수도 있습니다.

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
`Arr::sortDesc` 메서드는 배열의 값을 기준으로 내림차순으로 정렬합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

주어진 클로저의 결과를 기준으로 배열을 정렬할 수도 있습니다.

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

`Arr::sortRecursive` 메서드는 숫자 인덱스를 가진 하위 배열에는 `sort` 함수를, 연관 배열인 하위 배열에는 `ksort` 함수를 사용하여 배열을 재귀적으로 정렬합니다.

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

결과를 내림차순으로 정렬하고 싶다면 `Arr::sortRecursiveDesc` 메서드를 사용할 수 있습니다.

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-string"></a>
#### `Arr::string()` {.collection-method}

`Arr::string` 메서드는 [Arr::get()](#method-array-get)과 마찬가지로 `"dot"` 표기법을 사용하여 깊게 중첩된 배열에서 값을 가져오지만, 요청한 값이 `string`이 아니면 `InvalidArgumentException`을 발생시킵니다.

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

`Arr::take` 메서드는 지정된 개수의 항목을 포함하는 새 배열을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음의 정수를 전달하여 배열의 끝에서 지정된 개수만큼 항목을 가져올 수도 있습니다.

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()` {.collection-method}

`Arr::toCssClasses` 메서드는 조건에 따라 CSS 클래스 문자열을 컴파일합니다. 이 메서드는 추가하려는 클래스 또는 클래스들이 배열 키에 들어 있고, 값에는 boolean 표현식이 들어 있는 배열을 받습니다. 배열 요소가 숫자 키를 가지고 있다면 렌더링되는 클래스 목록에 항상 포함됩니다.

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

`Arr::toCssStyles` 메서드는 조건에 따라 CSS 스타일 문자열을 컴파일합니다. 이 메서드는 추가하려는 CSS 선언이 배열 키에 들어 있고, 값에는 boolean 표현식이 들어 있는 CSS 선언 배열을 받습니다. 배열 요소가 숫자 키를 가지고 있다면 컴파일된 CSS 스타일 문자열에 항상 포함됩니다.

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 Laravel에서 [Blade 컴포넌트의 속성 백과 클래스를 병합](/docs/13.x/blade#conditionally-merge-classes)하는 기능뿐만 아니라 `@class` [Blade 지시어](/docs/13.x/blade#conditional-classes)의 기반이 됩니다.

<a name="method-array-undot"></a>
#### `Arr::undot()` {.collection-method}

`Arr::undot` 메서드는 `"dot"` 표기법을 사용하는 1차원 배열을 다차원 배열로 확장합니다.

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

`Arr::where` 메서드는 주어진 클로저를 사용하여 배열을 필터링합니다.

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

`Arr::whereNotNull` 메서드는 주어진 배열에서 모든 `null` 값을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()` {.collection-method}

`Arr::wrap` 메서드는 주어진 값을 배열로 감쌉니다. 주어진 값이 이미 배열이라면 수정하지 않고 그대로 반환합니다.

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

주어진 값이 `null`이면 빈 배열이 반환됩니다.

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()` {.collection-method}

`data_fill` 함수는 `"dot"` 표기법을 사용하여 중첩된 배열 또는 객체 안의 누락된 값을 설정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

이 함수는 별표를 와일드카드로 받을 수도 있으며, 대상에 맞게 값을 채웁니다.

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

`data_get` 함수는 `"dot"` 표기법을 사용하여 중첩된 배열 또는 객체에서 값을 가져옵니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

`data_get` 함수는 기본값도 받을 수 있으며, 지정한 키를 찾을 수 없으면 이 기본값이 반환됩니다.

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

이 함수는 별표를 사용한 와일드카드도 받을 수 있으며, 배열 또는 객체의 어떤 키든 대상으로 삼을 수 있습니다.

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}`와 `{last}` 플레이스홀더를 사용하여 배열의 첫 번째 또는 마지막 항목을 가져올 수 있습니다.

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

`data_set` 함수는 `"dot"` 표기법을 사용하여 중첩된 배열 또는 객체 안의 값을 설정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

이 함수는 별표를 사용한 와일드카드도 받을 수 있으며, 대상에 맞게 값을 설정합니다.

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

기본적으로 기존 값은 덮어씁니다. 값이 존재하지 않을 때만 설정하고 싶다면 함수의 네 번째 인수로 `false`를 전달할 수 있습니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()` {.collection-method}

`data_forget` 함수는 `"dot"` 표기법을 사용하여 중첩된 배열 또는 객체 안의 값을 제거합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

이 함수는 별표를 사용한 와일드카드도 받을 수 있으며, 대상에 맞게 값을 제거합니다.

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

`head` 함수는 주어진 배열의 첫 번째 요소를 반환합니다. 배열이 비어 있으면 `false`가 반환됩니다.
```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()` {.collection-method}

`last` 함수는 주어진 배열의 마지막 요소를 반환합니다. 배열이 비어 있으면 `false`가 반환됩니다:

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 숫자 (Numbers)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()` {.collection-method}

`Number::abbreviate` 메서드는 제공된 숫자 값을 사람이 읽기 쉬운 형식으로 반환하며, 단위는 축약형으로 표시합니다:

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

`Number::clamp` 메서드는 주어진 숫자가 지정된 범위 안에 머물도록 보장합니다. 숫자가 최솟값보다 작으면 최솟값을 반환합니다. 숫자가 최댓값보다 크면 최댓값을 반환합니다:

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

`Number::currency` 메서드는 주어진 값을 통화 표시 형식의 문자열로 반환합니다:

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

`Number::defaultCurrency` 메서드는 `Number` 클래스에서 사용 중인 기본 통화를 반환합니다:

```php
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()` {.collection-method}

`Number::defaultLocale` 메서드는 `Number` 클래스에서 사용 중인 기본 로케일을 반환합니다:

```php
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()` {.collection-method}

`Number::fileSize` 메서드는 주어진 바이트 값을 파일 크기 표시 형식의 문자열로 반환합니다:

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

`Number::forHumans` 메서드는 제공된 숫자 값을 사람이 읽기 쉬운 형식으로 반환합니다:

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

`Number::format` 메서드는 주어진 숫자를 로케일에 맞는 문자열로 포맷합니다:

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

`Number::ordinal` 메서드는 숫자의 서수 표현을 반환합니다:

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

`Number::pairs` 메서드는 지정한 범위와 단계 값을 기준으로 숫자 쌍(하위 범위)의 배열을 생성합니다. 이 메서드는 페이지네이션이나 작업 배치 처리처럼 큰 숫자 범위를 더 작고 다루기 쉬운 하위 범위로 나눌 때 유용합니다. `pairs` 메서드는 배열들의 배열을 반환하며, 내부 배열 각각은 숫자 쌍(하위 범위)을 나타냅니다:

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[0, 9], [10, 19], [20, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-parse-int"></a>
#### `Number::parseInt()` {.collection-method}

`Number::parseInt` 메서드는 지정한 로케일에 따라 문자열을 정수로 파싱합니다:

```php
use Illuminate\Support\Number;

$result = Number::parseInt('10.123');

// (int) 10

$result = Number::parseInt('10,123', locale: 'fr');

// (int) 10
```

<a name="method-number-parse-float"></a>
#### `Number::parseFloat()` {.collection-method}

`Number::parseFloat` 메서드는 지정한 로케일에 따라 문자열을 float로 파싱합니다:

```php
use Illuminate\Support\Number;

$result = Number::parseFloat('10');

// (float) 10.0

$result = Number::parseFloat('10', locale: 'fr');

// (float) 10.0
```

<a name="method-number-percentage"></a>
#### `Number::percentage()` {.collection-method}

`Number::percentage` 메서드는 주어진 값을 백분율 표시 형식의 문자열로 반환합니다:

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

`Number::spell` 메서드는 주어진 숫자를 단어로 된 문자열로 변환합니다:

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인수를 사용하면 어떤 값 이후의 모든 숫자를 단어로 풀어 쓸지 지정할 수 있습니다:

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인수를 사용하면 어떤 값 이전의 모든 숫자를 단어로 풀어 쓸지 지정할 수 있습니다:

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-spell-ordinal"></a>
#### `Number::spellOrdinal()` {.collection-method}

`Number::spellOrdinal` 메서드는 숫자의 서수 표현을 단어로 된 문자열로 반환합니다:

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

`Number::trim` 메서드는 주어진 숫자의 소수점 뒤에 붙은 0을 제거합니다:

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()` {.collection-method}

`Number::useLocale` 메서드는 기본 숫자 로케일을 전역으로 설정합니다. 이후 `Number` 클래스의 메서드를 호출할 때 숫자와 통화가 포맷되는 방식에 영향을 줍니다:

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

`Number::withLocale` 메서드는 지정한 로케일을 사용해 주어진 클로저를 실행한 다음, 콜백 실행이 끝나면 원래 로케일을 복원합니다:

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()` {.collection-method}

`Number::useCurrency` 메서드는 기본 숫자 통화를 전역으로 설정합니다. 이후 `Number` 클래스의 메서드를 호출할 때 통화가 포맷되는 방식에 영향을 줍니다:

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

`Number::withCurrency` 메서드는 지정한 통화를 사용하여 주어진 클로저를 실행한 다음, 콜백 실행이 끝나면 원래 통화로 복원합니다.

```php
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
```

<a name="paths"></a>
## 경로 (Paths)

<a name="method-app-path"></a>
#### `app_path()` {.collection-method}

`app_path` 함수는 애플리케이션의 `app` 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `app_path` 함수를 사용하여 애플리케이션 디렉터리를 기준으로 한 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()` {.collection-method}

`base_path` 함수는 애플리케이션의 루트 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `base_path` 함수를 사용하여 프로젝트 루트 디렉터리를 기준으로 한 특정 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()` {.collection-method}

`config_path` 함수는 애플리케이션의 `config` 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `config_path` 함수를 사용하여 애플리케이션의 설정 디렉터리 안에 있는 특정 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()` {.collection-method}

`database_path` 함수는 애플리케이션의 `database` 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `database_path` 함수를 사용하여 데이터베이스 디렉터리 안에 있는 특정 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()` {.collection-method}

`lang_path` 함수는 애플리케이션의 `lang` 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `lang_path` 함수를 사용하여 해당 디렉터리 안에 있는 특정 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<a name="method-public-path"></a>
#### `public_path()` {.collection-method}

`public_path` 함수는 애플리케이션의 `public` 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `public_path` 함수를 사용하여 public 디렉터리 안에 있는 특정 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()` {.collection-method}

`resource_path` 함수는 애플리케이션의 `resources` 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `resource_path` 함수를 사용하여 resources 디렉터리 안에 있는 특정 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()` {.collection-method}

`storage_path` 함수는 애플리케이션의 `storage` 디렉터리에 대한 정규화된 전체 경로를 반환합니다. 또한 `storage_path` 함수를 사용하여 storage 디렉터리 안에 있는 특정 파일의 정규화된 전체 경로를 생성할 수도 있습니다.

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL (URLs)

<a name="method-action"></a>
#### `action()` {.collection-method}

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다.

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

메서드가 라우트 파라미터를 받는 경우, 해당 파라미터를 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()` {.collection-method}

`asset` 함수는 현재 요청의 스킴(HTTP 또는 HTTPS)을 사용하여 asset에 대한 URL을 생성합니다.

```php
$url = asset('img/photo.jpg');
```

`.env` 파일에서 `ASSET_URL` 변수를 설정하여 asset URL 호스트를 구성할 수 있습니다. Amazon S3 또는 다른 CDN 같은 외부 서비스에 asset을 호스팅하는 경우 유용합니다.

```php
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()` {.collection-method}

`route` 함수는 주어진 [이름이 지정된 라우트](/docs/13.x/routing#named-routes)에 대한 URL을 생성합니다.

```php
$url = route('route.name');
```

라우트가 파라미터를 받는 경우, 해당 파라미터를 함수의 두 번째 인수로 전달할 수 있습니다.

```php
$url = route('route.name', ['id' => 1]);
```

기본적으로 `route` 함수는 절대 URL을 생성합니다. 상대 URL을 생성하려면 함수의 세 번째 인수로 `false`를 전달할 수 있습니다.

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()` {.collection-method}

`secure_asset` 함수는 HTTPS를 사용하여 asset에 대한 URL을 생성합니다.

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()` {.collection-method}

`secure_url` 함수는 주어진 경로에 대한 정규화된 HTTPS URL을 생성합니다. 추가 URL 세그먼트는 함수의 두 번째 인수로 전달할 수 있습니다.

```php
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-action"></a>
#### `to_action()` {.collection-method}

`to_action` 함수는 주어진 컨트롤러 액션에 대한 [리다이렉트 HTTP 응답](/docs/13.x/responses#redirects)을 생성합니다.

```php
use App\Http\Controllers\UserController;

return to_action([UserController::class, 'show'], ['user' => 1]);
```

필요하다면 `to_action` 메서드의 세 번째와 네 번째 인수로 리다이렉트에 지정할 HTTP 상태 코드와 추가 응답 헤더를 전달할 수 있습니다.

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

`to_route` 함수는 주어진 [이름이 지정된 라우트](/docs/13.x/routing#named-routes)에 대한 [리다이렉트 HTTP 응답](/docs/13.x/responses#redirects)을 생성합니다.

```php
return to_route('users.show', ['user' => 1]);
```

필요하다면 `to_route` 메서드의 세 번째와 네 번째 인수로 리다이렉트에 지정할 HTTP 상태 코드와 추가 응답 헤더를 전달할 수 있습니다.

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-uri"></a>
#### `uri()` {.collection-method}

`uri` 함수는 주어진 URI에 대한 [플루언트 URI 인스턴스](#uri)를 생성합니다.

```php
$uri = uri('https://example.com')
    ->withPath('/users')
    ->withQuery(['page' => 1]);
```

`uri` 함수에 호출 가능한 컨트롤러와 메서드 쌍을 담은 배열이 전달되면, 이 함수는 해당 컨트롤러 메서드의 라우트 경로에 대한 `Uri` 인스턴스를 생성합니다.

```php
use App\Http\Controllers\UserController;

$uri = uri([UserController::class, 'show'], ['user' => $user]);
```

컨트롤러가 invokable이라면 컨트롤러 클래스 이름만 제공하면 됩니다.

```php
use App\Http\Controllers\UserIndexController;

$uri = uri(UserIndexController::class);
```

`uri` 함수에 전달된 값이 [이름이 지정된 라우트](/docs/13.x/routing#named-routes)의 이름과 일치하면, 해당 라우트의 경로에 대한 `Uri` 인스턴스가 생성됩니다.

```php
$uri = uri('users.show', ['user' => $user]);
```

<a name="method-url"></a>
#### `url()` {.collection-method}

`url` 함수는 주어진 경로에 대한 정규화된 전체 URL을 생성합니다.

```php
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로가 제공되지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환됩니다.

```php
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

`url` 함수 사용에 대한 자세한 내용은 [URL 생성 문서](/docs/13.x/urls#generating-urls)를 참고하십시오.

<a name="miscellaneous"></a>
## 기타 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()` {.collection-method}

`abort` 함수는 [예외 핸들러](/docs/13.x/errors#handling-exceptions)에 의해 렌더링될 [HTTP 예외](/docs/13.x/errors#http-exceptions)를 발생시킵니다.

```php
abort(403);
```

브라우저로 전송할 예외 메시지와 커스텀 HTTP 응답 헤더를 함께 제공할 수도 있습니다.

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()` {.collection-method}

`abort_if` 함수는 주어진 boolean 표현식이 `true`로 평가되면 HTTP 예외를 발생시킵니다.

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` 메서드와 마찬가지로, 함수의 세 번째 인수로 예외의 응답 텍스트를 제공하고 네 번째 인수로 커스텀 응답 헤더 배열을 제공할 수도 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()` {.collection-method}

`abort_unless` 함수는 주어진 boolean 표현식이 `false`로 평가되면 HTTP 예외를 발생시킵니다.

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

`abort` 메서드와 마찬가지로, 함수의 세 번째 인수로 예외의 응답 텍스트를 제공하고 네 번째 인수로 커스텀 응답 헤더 배열을 제공할 수도 있습니다.

<a name="method-app"></a>
#### `app()` {.collection-method}

`app` 함수는 [서비스 컨테이너](/docs/13.x/container) 인스턴스를 반환합니다.

```php
$container = app();
```

컨테이너에서 해석(resolve)할 클래스 또는 인터페이스 이름을 전달할 수 있습니다.

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()` {.collection-method}

`auth` 함수는 [인증기](/docs/13.x/authentication) 인스턴스를 반환합니다. `Auth` 파사드의 대안으로 사용할 수 있습니다.

```php
$user = auth()->user();
```

필요하다면 접근하려는 guard 인스턴스를 지정할 수 있습니다.

```php
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()` {.collection-method}

`back` 함수는 사용자의 이전 위치로 이동하는 [리다이렉트 HTTP 응답](/docs/13.x/responses#redirects)을 생성합니다.

```php
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()` {.collection-method}

`bcrypt` 함수는 Bcrypt를 사용하여 주어진 값을 [해싱](/docs/13.x/hashing)합니다. 이 함수는 `Hash` 파사드의 대안으로 사용할 수 있습니다.

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()` {.collection-method}

`blank` 함수는 주어진 값이 "비어 있는(blank)" 값인지 판단합니다.

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

`blank`의 반대 기능은 [filled](#method-filled) 함수를 참고하십시오.

<a name="method-broadcast"></a>
#### `broadcast()` {.collection-method}

`broadcast` 함수는 주어진 [이벤트](/docs/13.x/events)를 리스너에게 [브로드캐스트](/docs/13.x/broadcasting)합니다.

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```
<a name="method-broadcast-if"></a>
#### `broadcast_if()` {.collection-method}

`broadcast_if` 함수는 주어진 불리언 표현식이 `true`로 평가되면 지정된 [event](/docs/13.x/events)를 해당 리스너에게 [브로드캐스트](/docs/13.x/broadcasting)합니다.

```php
broadcast_if($user->isActive(), new UserRegistered($user));

broadcast_if($user->isActive(), new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-unless"></a>
#### `broadcast_unless()` {.collection-method}

`broadcast_unless` 함수는 주어진 불리언 표현식이 `false`로 평가되면 지정된 [event](/docs/13.x/events)를 해당 리스너에게 [브로드캐스트](/docs/13.x/broadcasting)합니다.

```php
broadcast_unless($user->isBanned(), new UserRegistered($user));

broadcast_unless($user->isBanned(), new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()` {.collection-method}

`cache` 함수는 [cache](/docs/13.x/cache)에서 값을 가져오는 데 사용할 수 있습니다. 주어진 키가 캐시에 없으면 선택적으로 지정한 기본값이 반환됩니다.

```php
$value = cache('key');

$value = cache('key', 'default');
```

키 / 값 쌍으로 이루어진 배열을 함수에 전달하여 캐시에 항목을 추가할 수 있습니다. 또한 캐시된 값을 유효한 것으로 간주할 초 단위 시간 또는 기간도 함께 전달해야 합니다.

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->plus(seconds: 10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()` {.collection-method}

`class_uses_recursive` 함수는 클래스가 사용하는 모든 traits를 반환하며, 부모 클래스들이 사용하는 traits도 포함합니다.

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()` {.collection-method}

`collect` 함수는 주어진 값으로부터 [컬렉션](/docs/13.x/collections) 인스턴스를 생성합니다.

```php
$collection = collect(['Taylor', 'Abigail']);
```

<a name="method-config"></a>
#### `config()` {.collection-method}

`config` 함수는 [설정](/docs/13.x/configuration) 변수의 값을 가져옵니다. 설정 값은 파일 이름과 접근하려는 옵션 이름을 포함하는 "dot" 문법으로 접근할 수 있습니다. 설정 옵션이 존재하지 않을 때 반환할 기본값도 지정할 수 있습니다.

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

키 / 값 쌍으로 이루어진 배열을 전달하여 런타임에 설정 변수를 지정할 수 있습니다. 다만 이 함수는 현재 요청에 대한 설정 값에만 영향을 주며, 실제 설정 값을 업데이트하지는 않는다는 점에 유의하세요.

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()` {.collection-method}

`context` 함수는 현재 [context](/docs/13.x/context)에서 값을 가져옵니다. context 키가 존재하지 않을 때 반환할 기본값도 지정할 수 있습니다.

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

키 / 값 쌍으로 이루어진 배열을 전달하여 context 값을 설정할 수 있습니다.

```php
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
#### `cookie()` {.collection-method}

`cookie` 함수는 새 [cookie](/docs/13.x/requests#cookies) 인스턴스를 생성합니다.

```php
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()` {.collection-method}

`csrf_field` 함수는 CSRF 토큰 값을 포함하는 HTML `hidden` 입력 필드를 생성합니다. 예를 들어 [Blade 문법](/docs/13.x/blade)을 사용하면 다음과 같습니다.

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()` {.collection-method}

`csrf_token` 함수는 현재 CSRF 토큰 값을 가져옵니다.

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()` {.collection-method}

`decrypt` 함수는 주어진 값을 [복호화](/docs/13.x/encryption)합니다. 이 함수는 `Crypt` 파사드 대신 사용할 수 있습니다.

```php
$password = decrypt($value);
```

`decrypt`의 반대 기능은 [encrypt](#method-encrypt) 함수를 참고하세요.

<a name="method-dd"></a>
#### `dd()` {.collection-method}

`dd` 함수는 주어진 변수들을 덤프하고 스크립트 실행을 종료합니다.

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

스크립트 실행을 중단하고 싶지 않다면 대신 [dump](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
#### `dispatch()` {.collection-method}

`dispatch` 함수는 주어진 [job](/docs/13.x/queues#creating-jobs)을 Laravel [job queue](/docs/13.x/queues)에 넣습니다.

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()` {.collection-method}

`dispatch_sync` 함수는 주어진 job을 즉시 처리되도록 [sync](/docs/13.x/queues#synchronous-dispatching) 큐에 넣습니다.

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()` {.collection-method}

`dump` 함수는 주어진 변수들을 덤프합니다.

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

변수들을 덤프한 뒤 스크립트 실행을 중단하고 싶다면 대신 [dd](#method-dd) 함수를 사용하세요.

<a name="method-encrypt"></a>
#### `encrypt()` {.collection-method}

`encrypt` 함수는 주어진 값을 [암호화](/docs/13.x/encryption)합니다. 이 함수는 `Crypt` 파사드 대신 사용할 수 있습니다.

```php
$secret = encrypt('my-secret-value');
```

`encrypt`의 반대 기능은 [decrypt](#method-decrypt) 함수를 참고하세요.

<a name="method-env"></a>
#### `env()` {.collection-method}

`env` 함수는 [환경 변수](/docs/13.x/configuration#environment-configuration)의 값을 가져오거나 기본값을 반환합니다.

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행한다면, `env` 함수는 반드시 설정 파일 안에서만 호출해야 합니다. 설정이 캐시되면 `.env` 파일은 로드되지 않으며, `env` 함수를 호출하면 서버 수준 또는 시스템 수준의 환경 변수와 같은 외부 환경 변수 값이 반환되거나 `null`이 반환됩니다.

<a name="method-event"></a>
#### `event()` {.collection-method}

`event` 함수는 주어진 [event](/docs/13.x/events)를 해당 리스너에게 디스패치합니다.

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()` {.collection-method}

`fake` 함수는 컨테이너에서 [Faker](https://github.com/FakerPHP/Faker) 싱글톤을 해석합니다. 이는 모델 팩토리, 데이터베이스 시딩, 테스트, 뷰 프로토타이핑에서 가짜 데이터를 만들 때 유용합니다.

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

기본적으로 `fake` 함수는 `config/app.php` 설정의 `app.faker_locale` 설정 옵션을 사용합니다. 일반적으로 이 설정 옵션은 `APP_FAKER_LOCALE` 환경 변수를 통해 지정됩니다. `fake` 함수에 로케일을 전달하여 직접 지정할 수도 있습니다. 각 로케일은 개별 싱글톤으로 해석됩니다.

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()` {.collection-method}

`filled` 함수는 주어진 값이 "blank"가 아닌지 판단합니다.

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

`filled`의 반대 기능은 [blank](#method-blank) 함수를 참고하세요.

<a name="method-info"></a>
#### `info()` {.collection-method}

`info` 함수는 애플리케이션의 [로그](/docs/13.x/logging)에 정보를 기록합니다.

```php
info('Some helpful information!');
```

컨텍스트 데이터 배열도 함수에 전달할 수 있습니다.

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()` {.collection-method}

`literal` 함수는 주어진 이름 있는 인수를 속성으로 갖는 새 [stdClass](https://www.php.net/manual/en/class.stdclass.php) 인스턴스를 생성합니다.

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

`logger` 함수는 [로그](/docs/13.x/logging)에 `debug` 레벨 메시지를 기록하는 데 사용할 수 있습니다.

```php
logger('Debug message');
```

컨텍스트 데이터 배열도 함수에 전달할 수 있습니다.

```php
logger('User has logged in.', ['id' => $user->id]);
```

함수에 아무 값도 전달하지 않으면 [logger](/docs/13.x/logging) 인스턴스가 반환됩니다.

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()` {.collection-method}

`method_field` 함수는 폼의 HTTP verb를 위장한 값을 포함하는 HTML `hidden` 입력 필드를 생성합니다. 예를 들어 [Blade 문법](/docs/13.x/blade)을 사용하면 다음과 같습니다.

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()` {.collection-method}

`now` 함수는 현재 시각에 대한 새 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$now = now();
```

<a name="method-old"></a>
#### `old()` {.collection-method}

`old` 함수는 세션에 플래시된 [이전 입력](/docs/13.x/requests#old-input) 값을 [가져옵니다](/docs/13.x/requests#retrieving-input).

```php
$value = old('value');

$value = old('value', 'default');
```

`old` 함수의 두 번째 인수로 제공되는 "기본값"은 종종 Eloquent 모델의 속성입니다. 그래서 Laravel에서는 전체 Eloquent 모델을 `old` 함수의 두 번째 인수로 그대로 전달할 수 있습니다. 이렇게 하면 Laravel은 `old` 함수에 제공된 첫 번째 인수를 "기본값"으로 간주할 Eloquent 속성의 이름으로 판단합니다.

```blade
{{ old('name', $user->name) }}

// Is equivalent to...

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()` {.collection-method}

`once` 함수는 주어진 콜백을 실행하고, 요청이 지속되는 동안 그 결과를 메모리에 캐시합니다. 같은 콜백으로 `once` 함수를 다시 호출하면 이전에 캐시된 결과가 반환됩니다.

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

객체 인스턴스 안에서 `once` 함수가 실행되면 캐시된 결과는 해당 객체 인스턴스별로 고유합니다.

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

`optional` 함수는 어떤 인수든 받아들이며, 해당 객체의 속성에 접근하거나 메서드를 호출할 수 있게 해줍니다. 주어진 객체가 `null`이면 오류를 발생시키는 대신 속성과 메서드는 `null`을 반환합니다.

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```
`optional` 함수는 두 번째 인수로 클로저도 받을 수 있습니다. 첫 번째 인수로 제공된 값이 `null`이 아니면 이 클로저가 호출됩니다.

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()` {.collection-method}

`policy` 메서드는 주어진 클래스에 대한 [policy(정책)](/docs/13.x/authorization#creating-policies) 인스턴스를 가져옵니다.

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()` {.collection-method}

`redirect` 함수는 [redirect HTTP response](/docs/13.x/responses#redirects)를 반환하거나, 인수 없이 호출하면 redirector 인스턴스를 반환합니다.

```php
return redirect($to = null, $status = 302, $headers = [], $secure = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()` {.collection-method}

`report` 함수는 애플리케이션의 [예외 핸들러](/docs/13.x/errors#handling-exceptions)를 사용하여 예외를 보고합니다.

```php
report($e);
```

`report` 함수는 문자열도 인수로 받을 수 있습니다. 함수에 문자열이 전달되면, 이 함수는 주어진 문자열을 메시지로 사용하는 예외를 생성합니다.

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()` {.collection-method}

`report_if` 함수는 주어진 불리언 표현식이 `true`로 평가되면 애플리케이션의 [예외 핸들러](/docs/13.x/errors#handling-exceptions)를 사용하여 예외를 보고합니다.

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()` {.collection-method}

`report_unless` 함수는 주어진 불리언 표현식이 `false`로 평가되면 애플리케이션의 [예외 핸들러](/docs/13.x/errors#handling-exceptions)를 사용하여 예외를 보고합니다.

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()` {.collection-method}

`request` 함수는 현재 [request](/docs/13.x/requests) 인스턴스를 반환하거나, 현재 request에서 입력 필드의 값을 가져옵니다.

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()` {.collection-method}

`rescue` 함수는 주어진 클로저를 실행하고, 실행 중에 발생하는 모든 예외를 잡습니다. 잡힌 모든 예외는 애플리케이션의 [예외 핸들러](/docs/13.x/errors#handling-exceptions)로 전송됩니다. 하지만 request 처리는 계속 진행됩니다.

```php
return rescue(function () {
    return $this->method();
});
```

`rescue` 함수에 두 번째 인수를 전달할 수도 있습니다. 이 인수는 클로저를 실행하는 동안 예외가 발생했을 때 반환할 "기본" 값입니다.

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

예외를 `report` 함수를 통해 보고할지 결정하기 위해 `rescue` 함수에 `report` 인수를 제공할 수 있습니다.

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()` {.collection-method}

`resolve` 함수는 [service container](/docs/13.x/container)를 사용하여 주어진 클래스명 또는 인터페이스명을 인스턴스로 해석합니다.

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()` {.collection-method}

`response` 함수는 [response](/docs/13.x/responses) 인스턴스를 생성하거나 response factory의 인스턴스를 가져옵니다.

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()` {.collection-method}

`retry` 함수는 주어진 최대 시도 횟수에 도달할 때까지 주어진 콜백 실행을 시도합니다. 콜백이 예외를 던지지 않으면 반환값이 그대로 반환됩니다. 콜백이 예외를 던지면 자동으로 다시 시도됩니다. 최대 시도 횟수를 초과하면 해당 예외가 던져집니다.

```php
return retry(5, function () {
    // Attempt 5 times while resting 100ms between attempts...
}, 100);
```

대기 시간에는 `CarbonInterval` 인스턴스도 사용할 수 있습니다.

```php
use function Illuminate\Support\seconds;

return retry(5, function () {
    // Attempt 5 times while resting 5 seconds between attempts...
}, seconds(5));
```

시도 사이에 몇 밀리초 동안 대기할지 직접 계산하려면, `retry` 함수의 세 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

편의를 위해 `retry` 함수의 첫 번째 인수로 배열을 제공할 수 있습니다. 이 배열은 이후 각 재시도 사이에 몇 밀리초 동안 대기할지 결정하는 데 사용됩니다.

```php
return retry([100, 200], function () {
    // Sleep for 100ms on first retry, 200ms on second retry...
});
```

특정 조건에서만 다시 시도하려면, `retry` 함수의 네 번째 인수로 클로저를 전달할 수 있습니다.

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

`session` 함수는 [session](/docs/13.x/session) 값을 가져오거나 설정하는 데 사용할 수 있습니다.

```php
$value = session('key');
```

키 / 값 쌍의 배열을 함수에 전달하여 값을 설정할 수 있습니다.

```php
session(['chairs' => 7, 'instruments' => 3]);
```

함수에 값을 전달하지 않으면 session store가 반환됩니다.

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()` {.collection-method}

`tap` 함수는 임의의 `$value`와 클로저, 두 개의 인수를 받습니다. `$value`는 클로저에 전달된 다음 `tap` 함수에 의해 반환됩니다. 클로저의 반환값은 중요하지 않습니다.

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'Taylor';

    $user->save();
});
```

`tap` 함수에 클로저를 전달하지 않으면 주어진 `$value`에서 원하는 메서드를 호출할 수 있습니다. 호출한 메서드가 실제 정의에서 무엇을 반환하든, 그 메서드 호출의 반환값은 항상 `$value`가 됩니다. 예를 들어 Eloquent의 `update` 메서드는 일반적으로 정수를 반환합니다. 하지만 `tap` 함수를 통해 `update` 메서드 호출을 체이닝하면, 해당 메서드가 모델 자체를 반환하도록 강제할 수 있습니다.

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `tap` 메서드를 추가하려면, 해당 클래스에 `Illuminate\Support\Traits\Tappable` trait를 추가하면 됩니다. 이 trait의 `tap` 메서드는 Closure를 유일한 인수로 받습니다. 객체 인스턴스 자체가 Closure에 전달된 다음 `tap` 메서드에 의해 반환됩니다.

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()` {.collection-method}

`throw_if` 함수는 주어진 불리언 표현식이 `true`로 평가되면 주어진 예외를 던집니다.

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

`throw_unless` 함수는 주어진 불리언 표현식이 `false`로 평가되면 주어진 예외를 던집니다.

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

`today` 함수는 현재 날짜에 대한 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()` {.collection-method}

`trait_uses_recursive` 함수는 trait가 사용하는 모든 trait를 반환합니다.

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()` {.collection-method}

`transform` 함수는 주어진 값이 [blank](#method-blank)가 아닌 경우 그 값에 대해 클로저를 실행한 다음, 클로저의 반환값을 반환합니다.

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

함수의 세 번째 인수로 기본값 또는 클로저를 전달할 수 있습니다. 주어진 값이 blank이면 이 값이 반환됩니다.

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()` {.collection-method}

`validator` 함수는 주어진 인수로 새로운 [validator](/docs/13.x/validation) 인스턴스를 생성합니다. `Validator` facade의 대안으로 사용할 수 있습니다.

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()` {.collection-method}

`value` 함수는 전달받은 값을 반환합니다. 하지만 함수에 클로저를 전달하면, 해당 클로저가 실행되고 그 반환값이 반환됩니다.

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

`value` 함수에는 추가 인수를 전달할 수 있습니다. 첫 번째 인수가 클로저라면 추가 매개변수들이 클로저의 인수로 전달됩니다. 그렇지 않으면 추가 인수들은 무시됩니다.

```php
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()` {.collection-method}

`view` 함수는 [view](/docs/13.x/views) 인스턴스를 가져옵니다.

```php
return view('auth.login');
```

<a name="method-with"></a>
#### `with()` {.collection-method}

`with` 함수는 전달받은 값을 반환합니다. 함수의 두 번째 인수로 클로저가 전달되면, 해당 클로저가 실행되고 그 반환값이 반환됩니다.

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

`when` 함수는 주어진 조건이 `true`로 평가되면 전달받은 값을 반환합니다. 그렇지 않으면 `null`이 반환됩니다. 함수의 두 번째 인수로 클로저가 전달되면, 해당 클로저가 실행되고 그 반환값이 반환됩니다.

```php
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

`when` 함수는 주로 HTML 속성을 조건부로 렌더링할 때 유용합니다.

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)
<a name="benchmarking"></a>
### 벤치마킹

때로는 애플리케이션의 특정 부분이 얼마나 빠르게 실행되는지 간단히 테스트하고 싶을 수 있습니다. 이럴 때는 `Benchmark` 지원 클래스를 사용하여 주어진 콜백이 완료되는 데 걸리는 시간을 밀리초 단위로 측정할 수 있습니다.

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

기본적으로 주어진 콜백은 한 번만 실행되며(한 번의 반복), 실행 시간은 브라우저 / 콘솔에 표시됩니다.

콜백을 두 번 이상 실행하려면 메서드의 두 번째 인수로 콜백을 실행할 반복 횟수를 지정할 수 있습니다. 콜백을 여러 번 실행하면 `Benchmark` 클래스는 모든 반복 실행에 걸쳐 콜백을 실행하는 데 걸린 평균 밀리초를 반환합니다.

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

때로는 콜백 실행 시간을 벤치마킹하면서도 콜백이 반환한 값을 함께 얻고 싶을 수 있습니다. `value` 메서드는 콜백이 반환한 값과 콜백 실행에 걸린 밀리초를 담은 튜플을 반환합니다.

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜와 시간

Laravel에는 강력한 날짜 및 시간 조작 라이브러리인 [Carbon](https://carbon.nesbot.com/guide/getting-started/introduction.html)이 포함되어 있습니다. 새로운 `Carbon` 인스턴스를 생성하려면 `now` 함수를 호출할 수 있습니다. 이 함수는 Laravel 애플리케이션 전체에서 전역으로 사용할 수 있습니다.

```php
$now = now();
```

또는 `Illuminate\Support\Carbon` 클래스를 사용하여 새로운 `Carbon` 인스턴스를 생성할 수도 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Laravel은 또한 `Carbon` 인스턴스에 `plus` 및 `minus` 메서드를 추가하여, 인스턴스의 날짜와 시간을 쉽게 조작할 수 있도록 합니다.

```php
return now()->plus(minutes: 5);
return now()->plus(hours: 8);
return now()->plus(weeks: 4);

return now()->minus(minutes: 5);
return now()->minus(hours: 8);
return now()->minus(weeks: 4);
```

Carbon과 그 기능에 대한 자세한 설명은 [공식 Carbon 문서](https://carbon.nesbot.com/guide/getting-started/introduction.html)를 참고하십시오.

<a name="interval-functions"></a>
#### 간격 함수

Laravel은 `milliseconds`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, `years` 함수도 제공합니다. 이 함수들은 PHP의 [DateInterval](https://www.php.net/manual/en/class.dateinterval.php) 클래스를 확장한 `CarbonInterval` 인스턴스를 반환합니다. 이 함수들은 Laravel이 `DateInterval` 인스턴스를 허용하는 모든 곳에서 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

use function Illuminate\Support\{minutes};

Cache::put('metrics', $metrics, minutes(10));
```

<a name="deferred-functions"></a>
### 지연 함수

Laravel의 [큐 작업](/docs/13.x/queues)을 사용하면 백그라운드 처리를 위해 작업을 큐에 넣을 수 있습니다. 하지만 때로는 오래 실행되는 큐 워커를 설정하거나 유지 관리하지 않고, 간단한 작업만 나중에 실행하고 싶을 수 있습니다.

지연 함수는 HTTP 응답이 사용자에게 전송된 뒤 클로저 실행을 미룰 수 있게 해 줍니다. 이를 통해 애플리케이션이 빠르고 즉각적으로 반응하는 것처럼 느껴지게 할 수 있습니다. 클로저 실행을 지연하려면 클로저를 `Illuminate\Support\defer` 함수에 전달하기만 하면 됩니다.

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

기본적으로 지연 함수는 `Illuminate\Support\defer`가 호출된 HTTP 응답, Artisan 명령어 또는 큐 작업이 성공적으로 완료된 경우에만 실행됩니다. 즉, 요청이 `4xx` 또는 `5xx` HTTP 응답으로 끝나면 지연 함수는 실행되지 않습니다. 지연 함수를 항상 실행하고 싶다면 지연 함수에 `always` 메서드를 체이닝할 수 있습니다.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

> [!WARNING]
> [Swoole PHP 확장](https://www.php.net/manual/en/book.swoole.php)이 설치되어 있다면 Laravel의 `defer` 함수가 Swoole 자체의 전역 `defer` 함수와 충돌하여 웹 서버 오류가 발생할 수 있습니다. Laravel의 `defer` 헬퍼를 호출할 때는 반드시 명시적으로 네임스페이스를 지정하십시오: `use function Illuminate\Support\defer;`

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수가 실행되기 전에 취소해야 한다면 `forget` 메서드를 사용하여 이름으로 해당 함수를 취소할 수 있습니다. 지연 함수에 이름을 지정하려면 `Illuminate\Support\defer` 함수의 두 번째 인수를 제공하십시오.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화하기

테스트를 작성할 때는 지연 함수를 비활성화하는 것이 유용할 수 있습니다. 테스트에서 `withoutDefer`를 호출하면 Laravel이 모든 지연 함수를 즉시 실행하도록 지시할 수 있습니다.

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

하나의 테스트 케이스 안에 있는 모든 테스트에서 지연 함수를 비활성화하고 싶다면, 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer` 메서드를 호출할 수 있습니다.

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
### Lottery

Laravel의 Lottery 클래스는 주어진 확률에 따라 콜백을 실행하는 데 사용할 수 있습니다. 들어오는 요청 중 일정 비율에 대해서만 코드를 실행하고 싶을 때 특히 유용합니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

Laravel의 Lottery 클래스를 다른 Laravel 기능과 함께 사용할 수도 있습니다. 예를 들어 느린 쿼리 중 일부만 예외 처리기로 보고하고 싶을 수 있습니다. 또한 Lottery 클래스는 호출 가능하므로, 호출 가능한 값을 받는 어떤 메서드에도 이 클래스의 인스턴스를 전달할 수 있습니다.

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
#### Lottery 테스트하기

Laravel은 애플리케이션의 Lottery 호출을 쉽게 테스트할 수 있도록 몇 가지 간단한 메서드를 제공합니다.

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
### Pipeline

Laravel의 `Pipeline` 파사드는 주어진 입력을 일련의 호출 가능한 클래스, 클로저 또는 callable을 통해 “파이프”처럼 전달하는 편리한 방법을 제공합니다. 각 클래스는 입력을 검사하거나 수정한 뒤 파이프라인의 다음 callable을 호출할 기회를 가집니다.

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

보시다시피 파이프라인 안의 각 호출 가능한 클래스나 클로저에는 입력과 `$next` 클로저가 제공됩니다. `$next` 클로저를 호출하면 파이프라인의 다음 callable이 호출됩니다. 눈치채셨겠지만, 이는 [미들웨어](/docs/13.x/middleware)와 매우 비슷합니다.

파이프라인의 마지막 callable이 `$next` 클로저를 호출하면 `then` 메서드에 제공된 callable이 호출됩니다. 일반적으로 이 callable은 주어진 입력을 그대로 반환합니다. 편의를 위해, 처리된 입력을 그대로 반환하고 싶다면 `thenReturn` 메서드를 사용할 수 있습니다.

물론 앞서 설명했듯이 파이프라인에는 클로저만 제공할 수 있는 것이 아닙니다. 호출 가능한 클래스도 제공할 수 있습니다. 클래스 이름이 제공되면 해당 클래스는 Laravel의 [서비스 컨테이너](/docs/13.x/container)를 통해 인스턴스화되므로, 호출 가능한 클래스에 의존성을 주입할 수 있습니다.

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

`withinTransaction` 메서드를 파이프라인에서 호출하면 파이프라인의 모든 단계를 하나의 데이터베이스 트랜잭션 안에서 자동으로 감쌀 수 있습니다.

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
### Sleep

Laravel의 `Sleep` 클래스는 PHP의 기본 `sleep` 및 `usleep` 함수를 가볍게 감싼 래퍼입니다. 테스트하기 더 쉬우며, 시간 처리를 위한 개발자 친화적인 API도 제공합니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위를 다룰 수 있는 여러 메서드를 제공합니다.

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

시간 단위를 쉽게 조합하려면 `and` 메서드를 사용할 수 있습니다.

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트하기

`Sleep` 클래스나 PHP의 기본 sleep 함수를 사용하는 코드를 테스트하면 테스트 실행도 실제로 멈춥니다. 예상할 수 있듯이 이는 테스트 스위트를 상당히 느리게 만듭니다. 예를 들어 다음 코드를 테스트한다고 가정해 보겠습니다.

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

일반적으로 이 코드를 테스트하려면 _최소한_ 1초가 걸립니다. 다행히 `Sleep` 클래스는 sleep 동작을 “가짜 처리”할 수 있으므로 테스트 스위트를 빠르게 유지할 수 있습니다.

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

`Sleep` 클래스를 가짜 처리하면 실제 실행 일시 중지가 우회되므로 테스트가 훨씬 빨라집니다.

`Sleep` 클래스를 가짜 처리한 뒤에는 발생했어야 할 예상 “sleep”에 대해 어설션을 수행할 수 있습니다. 예를 들어 코드가 세 번 실행을 멈추며, 각 멈춤 시간이 1초씩 증가하는 상황을 테스트한다고 가정해 보겠습니다. `assertSequence` 메서드를 사용하면 테스트를 빠르게 유지하면서도 코드가 올바른 시간만큼 “sleep”했는지 어설션할 수 있습니다.

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

물론 `Sleep` 클래스는 테스트할 때 사용할 수 있는 다양한 다른 어설션도 제공합니다.

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
가짜 sleep이 발생할 때마다 어떤 작업을 수행하면 유용할 수 있습니다. 이를 위해 `whenFakingSleep` 메서드에 콜백을 제공할 수 있습니다. 다음 예제에서는 Laravel의 [시간 조작 헬퍼](/docs/13.x/mocking#interacting-with-time)를 사용하여 각 sleep의 지속 시간만큼 시간을 즉시 진행합니다.

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // Progress time when faking sleep...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

시간을 진행하는 것은 흔한 요구 사항이므로, `fake` 메서드는 테스트 안에서 sleep할 때 Carbon을 동기화 상태로 유지하기 위해 `syncWithCarbon` 인수를 받습니다.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

Laravel은 실행을 일시 중지할 때마다 내부적으로 `Sleep` 클래스를 사용합니다. 예를 들어 [retry](#method-retry) 헬퍼는 sleep할 때 `Sleep` 클래스를 사용하므로, 해당 헬퍼를 사용할 때 테스트하기가 더 쉬워집니다.

<a name="timebox"></a>
### Timebox

Laravel의 `Timebox` 클래스는 주어진 콜백의 실제 실행이 더 빨리 완료되더라도 항상 정해진 시간만큼 실행되도록 보장합니다. 이는 암호화 작업이나 사용자 인증 확인처럼, 공격자가 실행 시간의 차이를 악용해 민감한 정보를 추론할 수 있는 상황에서 특히 유용합니다.

실행 시간이 정해진 시간을 초과하면 `Timebox`는 아무 효과가 없습니다. 최악의 경우까지 고려할 수 있도록 충분히 긴 시간을 고정된 실행 시간으로 선택하는 것은 개발자의 책임입니다.

`call` 메서드는 클로저와 마이크로초 단위의 시간 제한을 받아 클로저를 실행한 뒤, 시간 제한에 도달할 때까지 기다립니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 안에서 예외가 발생하면 이 클래스는 정의된 지연 시간을 지킨 뒤, 지연 시간이 지난 후 예외를 다시 던집니다.

<a name="uri"></a>
### URI

Laravel의 `Uri` 클래스는 URI를 만들고 조작할 수 있는 편리하고 유창한 인터페이스를 제공합니다. 이 클래스는 기반이 되는 League URI 패키지가 제공하는 기능을 감싸며, Laravel의 라우팅 시스템과 자연스럽게 통합됩니다.

정적 메서드를 사용하면 `Uri` 인스턴스를 쉽게 만들 수 있습니다.

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

URI 인스턴스를 얻은 뒤에는 이를 유창하게 수정할 수 있습니다.

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
#### URI 검사

`Uri` 클래스는 기반 URI의 여러 구성 요소도 쉽게 검사할 수 있게 해줍니다.

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
#### 쿼리 문자열 조작

`Uri` 클래스는 URI의 쿼리 문자열을 조작하는 데 사용할 수 있는 여러 메서드를 제공합니다. `withQuery` 메서드는 기존 쿼리 문자열에 추가 쿼리 문자열 파라미터를 병합하는 데 사용할 수 있습니다.

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

`withQueryIfMissing` 메서드는 주어진 키가 쿼리 문자열에 아직 존재하지 않는 경우에만 기존 쿼리 문자열에 추가 쿼리 문자열 파라미터를 병합하는 데 사용할 수 있습니다.

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery` 메서드는 기존 쿼리 문자열을 새 쿼리 문자열로 완전히 대체하는 데 사용할 수 있습니다.

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery` 메서드는 배열 값을 가진 쿼리 문자열 파라미터에 추가 파라미터를 밀어 넣는 데 사용할 수 있습니다.

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery` 메서드는 쿼리 문자열에서 파라미터를 제거하는 데 사용할 수 있습니다.

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI에서 응답 생성

`redirect` 메서드는 주어진 URI로 이동하는 `RedirectResponse` 인스턴스를 생성하는 데 사용할 수 있습니다.

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는 라우트나 컨트롤러 액션에서 `Uri` 인스턴스를 그대로 반환할 수도 있습니다. 이 경우 반환된 URI로 이동하는 리다이렉트 응답이 자동으로 생성됩니다.

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```
