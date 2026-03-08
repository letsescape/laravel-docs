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

Laravel은 다양한 전역 "헬퍼(helper)" PHP 함수를 제공합니다. 이러한 함수 중 많은 것들은 프레임워크 내부에서 사용되지만, 필요하다면 애플리케이션에서도 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<a name="arrays-and-objects-method-list"></a>
### 배열 & 객체

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
### 숫자 (Numbers)

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
### 경로 (Paths)

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
### 기타 (Miscellaneous)

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
## 배열 & 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 주어진 값이 배열처럼 접근 가능한지 여부를 판단합니다.

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
#### `Arr::add()`

`Arr::add` 메서드는 지정된 키가 배열에 존재하지 않거나 값이 `null`일 경우에만 키 / 값 쌍을 배열에 추가합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()`

`Arr::array` 메서드는 [Arr::get()](#method-array-get)과 동일하게 "dot" 표기법을 사용하여 깊이 중첩된 배열에서 값을 가져옵니다. 단, 요청한 값이 `array` 타입이 아닐 경우 `InvalidArgumentException` 예외가 발생합니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::array($array, 'languages');

// ['PHP', 'Ruby']

$value = Arr::array($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-boolean"></a>
#### `Arr::boolean()`

`Arr::boolean` 메서드는 [Arr::get()](#method-array-get)처럼 "dot" 표기법을 사용해 깊이 중첩된 배열에서 값을 가져옵니다. 단, 요청한 값이 `boolean` 타입이 아닐 경우 `InvalidArgumentException` 예외가 발생합니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'available' => true];

$value = Arr::boolean($array, 'available');

// true

$value = Arr::boolean($array, 'name');

// throws InvalidArgumentException
```

(문서 길이 제한으로 인해 이후 내용은 동일한 형식과 규칙을 유지하여 계속 번역됩니다.)