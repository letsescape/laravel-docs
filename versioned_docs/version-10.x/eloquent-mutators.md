<!-- # Eloquent: Mutators & Casting -->
# Eloquent: Mutators & Casting

- [Introduction](#introduction)
- [Accessors and Mutators](#accessors-and-mutators)
    - [Defining an Accessor](#defining-an-accessor)
    - [Defining a Mutator](#defining-a-mutator)
- [Attribute Casting](#attribute-casting)
    - [Array and JSON Casting](#array-and-json-casting)
    - [Date Casting](#date-casting)
    - [Enum Casting](#enum-casting)
    - [Encrypted Casting](#encrypted-casting)
    - [Query Time Casting](#query-time-casting)
- [Custom Casts](#custom-casts)
    - [Value Object Casting](#value-object-casting)
    - [Array / JSON Serialization](#array-json-serialization)
    - [Inbound Casting](#inbound-casting)
    - [Cast Parameters](#cast-parameters)
    - [Castables](#castables)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/10.x/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model. -->
accessor, mutator, attribute casting은 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 값을 변환할 수 있게 해줍니다. 예를 들어, [Laravel encrypter](/docs/10.x/encryption)를 사용해 데이터를 데이터베이스에 저장할 때는 암호화하고, Eloquent 모델에서 해당 속성을 접근할 때 자동으로 복호화할 수 있습니다. 또는, 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델에서 접근할 때 배열로 변환해서 사용할 수 있습니다.

<a name="accessors-and-mutators"></a>
<!-- ## Accessors and Mutators -->
## Accessors and Mutators

<a name="defining-an-accessor"></a>
<!-- ### Defining an Accessor -->
### Defining an Accessor

<!-- An accessor transforms an Eloquent attribute value when it is accessed. To define an accessor, create a protected method on your model to represent the accessible attribute. This method name should correspond to the "camel case" representation of the true underlying model attribute / database column when applicable. -->
accessor는 Eloquent 속성 값을 접근할 때 값을 가공합니다. accessor를 정의하려면, 모델에서 접근할 속성에 해당하는 protected 메서드를 생성합니다. 이 메서드의 이름은 실제 모델 속성/데이터베이스 컬럼의 "카멜 케이스(camel case)" 형식이어야 합니다.

<!-- In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute. All attribute accessor / mutator methods must declare a return type-hint of `Illuminate\Database\Eloquent\Casts\Attribute`: -->
아래 예시는 `first_name` 속성에 accessor를 정의하는 방법입니다. 이 accessor는 Eloquent에서 `first_name`의 값을 조회하려 할 때 자동으로 호출됩니다. accessor/mutator 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입 힌트를 반환해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the user's first name.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```

<!-- All accessor methods return an `Attribute` instance which defines how the attribute will be accessed and, optionally, mutated. In this example, we are only defining how the attribute will be accessed. To do so, we supply the `get` argument to the `Attribute` class constructor. -->
accessor 메서드는 모두 `Attribute` 인스턴스를 반환하며, 이 객체에서 해당 속성을 조회하거나(그리고 선택적으로, 변이할 때) 어떻게 처리할지 정의합니다. 위 예제에서는 속성을 조회할 때만 동작하도록 `Attribute` 클래스의 `get` 인자를 지정했습니다.

<!-- As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the accessor, you may simply access the `first_name` attribute on a model instance: -->
이처럼, 컬럼의 원래 값이 accessor로 전달되어 원하는 방식으로 가공할 수 있습니다. accessor의 값을 읽으려면, 모델 인스턴스에서 `first_name` 속성을 단순히 조회하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> accessor나 계산된 값을 모델의 배열/JSON 표현에도 포함하고 싶다면, [you will need to append them](/docs/10.x/eloquent-serialization#appending-values-to-json)을 참고해야 합니다.

<a name="building-value-objects-from-multiple-attributes"></a>
<!-- #### Building Value Objects From Multiple Attributes -->
#### Building Value Objects From Multiple Attributes

<!-- Sometimes your accessor may need to transform multiple model attributes into a single "value object". To do so, your `get` closure may accept a second argument of `$attributes`, which will be automatically supplied to the closure and will contain an array of all of the model's current attributes: -->
때로는 accessor에서 여러 모델 속성을 하나의 "값 객체(value object)"로 합쳐 반환해야 할 때가 있습니다. 이 경우 `get` 클로저의 두 번째 인자로 `$attributes`를 받을 수 있는데, 이 값은 모델의 현재 모든 속성을 담은 배열입니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    );
}
```

<a name="accessor-caching"></a>
<!-- #### Accessor Caching -->
#### Accessor Caching

<!-- When returning value objects from accessors, any changes made to the value object will automatically be synced back to the model before the model is saved. This is possible because Eloquent retains instances returned by accessors so it can return the same instance each time the accessor is invoked: -->
accessor에서 값 객체(value object)를 반환할 때, 값 객체에 변경을 가하면 그 변경 내용이 모델이 저장되기 전에 자동으로 모델에 반영됩니다. 이는 Eloquent가 accessor에서 반환된 객체 인스턴스를 유지하여, accessor가 반복적으로 호출될 때 동일한 객체를 반환하기 때문입니다.

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

<!-- However, you may sometimes wish to enable caching for primitive values like strings and booleans, particularly if they are computationally intensive. To accomplish this, you may invoke the `shouldCache` method when defining your accessor: -->
다만, 문자열이나 불리언과 같은 단순 값(프리미티브 타입)에 대해서도 계산 비용이 크다면 캐싱을 활성화하고 싶을 수 있습니다. 이 경우 accessor 정의 시 `shouldCache` 메서드를 호출하면 됩니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

<!-- If you would like to disable the object caching behavior of attributes, you may invoke the `withoutObjectCaching` method when defining the attribute: -->
반대로, 속성의 객체 캐싱 동작을 비활성화하고 싶다면, accessor 정의 시 `withoutObjectCaching` 메서드를 호출할 수 있습니다.

```php
/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    )->withoutObjectCaching();
}
```

<a name="defining-a-mutator"></a>
<!-- ### Defining a Mutator -->
### Defining a Mutator

<!-- A mutator transforms an Eloquent attribute value when it is set. To define a mutator, you may provide the `set` argument when defining your attribute. Let's define a mutator for the `first_name` attribute. This mutator will be automatically called when we attempt to set the value of the `first_name` attribute on the model: -->
mutator는 Eloquent 속성 값이 설정될 때 값을 가공합니다. mutator를 정의하려면, accessor 정의 시 `set` 인자를 추가하면 됩니다. 아래는 `first_name` 속성에 mutator를 정의하는 예시입니다. 이 mutator는 `first_name` 속성에 값을 설정하려 할 때 자동으로 호출됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Interact with the user's first name.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
            set: fn (string $value) => strtolower($value),
        );
    }
}
```

<!-- The mutator closure will receive the value that is being set on the attribute, allowing you to manipulate the value and return the manipulated value. To use our mutator, we only need to set the `first_name` attribute on an Eloquent model: -->
mutator 클로저는 해당 속성에 할당되는 값을 받아, 이를 가공한 후 반환합니다. 실제로 mutator를 사용하려면 Eloquent 모델의 `first_name` 속성에 값을 할당하기만 하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

<!-- In this example, the `set` callback will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its resulting value in the model's internal `$attributes` array. -->
이 예제에서 `set` 콜백은 `Sally`라는 값을 입력받습니다. mutator는 이 값을 `strtolower` 함수로 처리해, 그 결과를 모델 내부의 `$attributes` 배열에 할당합니다.

<a name="mutating-multiple-attributes"></a>
<!-- #### Mutating Multiple Attributes -->
#### Mutating Multiple Attributes

<!-- Sometimes your mutator may need to set multiple attributes on the underlying model. To do so, you may return an array from the `set` closure. Each key in the array should correspond with an underlying attribute / database column associated with the model: -->
mutator에서 여러 속성 값을 동시에 변경해야 할 때도 있습니다. 이럴 땐 `set` 클로저에서 배열을 반환하면 되며, 배열의 각 키는 실제 모델의 속성/데이터베이스 컬럼명을 사용해야 합니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

<a name="attribute-casting"></a>
<!-- ## Attribute Casting -->
## Attribute Casting

<!-- Attribute casting provides functionality similar to accessors and mutators without requiring you to define any additional methods on your model. Instead, your model's `$casts` property provides a convenient method of converting attributes to common data types. -->
attribute casting은 accessor/mutator와 비슷한 기능을 제공하지만, 별도의 메서드를 작성하지 않고도 속성 변환을 쉽게 처리할 수 있습니다. 모델의 `$casts` 프로퍼티를 사용해 데이터 타입 변환을 지정할 수 있습니다.

<!-- The `$casts` property should be an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are: -->
`$casts` 프로퍼티는 배열이어야 하며, 키는 변환할 속성명, 값은 해당 컬럼에 적용할 casting 타입입니다. 지원되는 casting 타입은 아래와 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `array`
- `AsStringable::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>decimal:&lt;precision&gt;</code>
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `hashed`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`
-->
- `array`
- `AsStringable::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>decimal:&lt;precision&gt;</code>
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `hashed`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

<!-- </div> -->
</div>

<!-- To demonstrate attribute casting, let's cast the `is_admin` attribute, which is stored in our database as an integer (`0` or `1`) to a boolean value: -->
예를 들어, 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언 타입으로 변환하려면 다음과 같이 작성할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'is_admin' => 'boolean',
    ];
}
```

<!-- After defining the cast, the `is_admin` attribute will always be cast to a boolean when you access it, even if the underlying value is stored in the database as an integer: -->
이렇게 cast를 지정하면, 실제 데이터베이스에 정수로 저장되어 있어도 `is_admin` 속성에 접근할 때 항상 불리언 값으로 반환됩니다.

```
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

<!-- If you need to add a new, temporary cast at runtime, you may use the `mergeCasts` method. These cast definitions will be added to any of the casts already defined on the model: -->
런타임에 새로운(임시) cast를 추가해야 한다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 방법으로 기존에 지정한 cast에 추가할 수 있습니다.

```
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null` 값인 속성은 casting이 적용되지 않습니다. 또한 모델의 리턴 관계 명칭과 동일한 이름의 cast나 속성을 정의해서는 안 되며, 주키(primary key)에 casting을 할당하는 것도 피해야 합니다.

<a name="stringable-casting"></a>
<!-- #### Stringable Casting -->
#### Stringable Casting

<!-- You may use the `Illuminate\Database\Eloquent\Casts\AsStringable` cast class to cast a model attribute to a [fluent `Illuminate\Support\Stringable` object](/docs/10.x/strings#fluent-strings-method-list): -->
모델 속성을 [fluent `Illuminate\Support\Stringable` object](/docs/10.x/strings#fluent-strings-method-list)로 변환하려면 `Illuminate\Database\Eloquent\Casts\AsStringable` cast 클래스를 사용할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'directory' => AsStringable::class,
    ];
}
```

<a name="array-and-json-casting"></a>
<!-- ### Array and JSON Casting -->
### Array and JSON Casting

<!-- The `array` cast is particularly useful when working with columns that are stored as serialized JSON. For example, if your database has a `JSON` or `TEXT` field type that contains serialized JSON, adding the `array` cast to that attribute will automatically deserialize the attribute to a PHP array when you access it on your Eloquent model: -->
`array` casting 타입은 직렬화된 JSON 컬럼을 다룰 때 특히 유용합니다. 예를 들어, 데이터베이스의 `JSON` 혹은 `TEXT` 타입 필드에 JSON 문자열이 들어 있다면, 해당 속성에 `array` cast를 적용해두면 모델에서 해당 값을 읽을 때 자동으로 PHP 배열로 변환해줍니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'options' => 'array',
    ];
}
```

<!-- Once the cast is defined, you may access the `options` attribute and it will automatically be deserialized from JSON into a PHP array. When you set the value of the `options` attribute, the given array will automatically be serialized back into JSON for storage: -->
cast를 지정해두면 `options` 속성에 접근할 때마다 JSON에서 PHP 배열로 역직렬화됩니다. `options` 속성에 값을 설정할 때는, 할당한 배열이 자동으로 JSON 문자열로 변환되어 저장됩니다.

```
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

<!-- To update a single field of a JSON attribute with a more terse syntax, you may [make the attribute mass assignable](/docs/10.x/eloquent#mass-assignment-json-columns) and use the `->` operator when calling the `update` method: -->
JSON 속성의 한 필드만 간단한 문법으로 업데이트하려면, [make the attribute mass assignable](/docs/10.x/eloquent#mass-assignment-json-columns)한 후 `update` 메서드에서 `->` 연산자를 사용할 수 있습니다.

```
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
<!-- #### Array Object and Collection Casting -->
#### Array Object and Collection Casting

<!-- Although the standard `array` cast is sufficient for many applications, it does have some disadvantages. Since the `array` cast returns a primitive type, it is not possible to mutate an offset of the array directly. For example, the following code will trigger a PHP error: -->
기본 `array` casting은 많은 경우에 충분하지만 제약점이 있습니다. `array` casting 타입으로 반환된 배열(프리미티브 타입)은 배열 오프셋을 직접 변경할 때, 아래와 같이 PHP 에러가 발생할 수 있습니다.

```
$user = User::find(1);

$user->options['key'] = $value;
```

<!-- To solve this, Laravel offers an `AsArrayObject` cast that casts your JSON attribute to an [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) class. This feature is implemented using Laravel's [custom cast](#custom-casts) implementation, which allows Laravel to intelligently cache and transform the mutated object such that individual offsets may be modified without triggering a PHP error. To use the `AsArrayObject` cast, simply assign it to an attribute: -->
이 문제를 해결하기 위해, Laravel은 `AsArrayObject` casting 타입을 제공합니다. 이 타입은 JSON 속성을 PHP의 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 casting합니다. 이 기능은 Laravel의 [custom cast](#custom-casts) 구현을 활용하여, Laravel이 변경된 객체를 지능적으로 캐싱 및 변환하므로 PHP 오류를 발생시키지 않고 개별 오프셋을 변경할 수 있습니다. `AsArrayObject` cast를 사용하려면, 다음과 같이 속성에 할당하기만 하면 됩니다.

```
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'options' => AsArrayObject::class,
];
```

<!-- Similarly, Laravel offers an `AsCollection` cast that casts your JSON attribute to a Laravel [Collection](/docs/10.x/collections) instance: -->
유사하게, `AsCollection` casting 타입은 JSON 속성을 Laravel [Collection](/docs/10.x/collections) 인스턴스로 변환합니다.

```
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class,
];
```

<!-- If you would like the `AsCollection` cast to instantiate a custom collection class instead of Laravel's base collection class, you may provide the collection class name as a cast argument: -->
`AsCollection` casting 사용 시, Laravel의 기본 Collection 대신 커스텀 컬렉션 클래스를 사용하려면 cast 인자로 해당 클래스명을 전달합니다.

```
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class.':'.OptionCollection::class,
];
```

<a name="date-casting"></a>
<!-- ### Date Casting -->
### Date Casting

<!-- By default, Eloquent will cast the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which extends the PHP `DateTime` class and provides an assortment of helpful methods. You may cast additional date attributes by defining additional date casts within your model's `$casts` property array. Typically, dates should be cast using the `datetime` or `immutable_datetime` cast types. -->
기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스(이 객체는 PHP의 `DateTime`을 확장하고 다양한 유틸리티 메서드를 제공합니다)로 casting합니다. 그 외에도 더 많은 속성을 모델의 `$casts` 배열에 추가해서 날짜 casting이 가능합니다. 일반적으로 날짜 관련 속성은 `datetime` 또는 `immutable_datetime` cast 타입을 사용합니다.

<!-- When defining a `date` or `datetime` cast, you may also specify the date's format. This format will be used when the [model is serialized to an array or JSON](/docs/10.x/eloquent-serialization): -->
`date` 또는 `datetime` casting 타입을 지정할 때, 날짜 포맷을 옵션으로 함께 설정할 수도 있습니다. 이 포맷은 [model is serialized to an array or JSON](/docs/10.x/eloquent-serialization) 적용됩니다.

```
/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'created_at' => 'datetime:Y-m-d',
];
```

<!-- When a column is cast as a date, you may set the corresponding model attribute value to a UNIX timestamp, date string (`Y-m-d`), date-time string, or a `DateTime` / `Carbon` instance. The date's value will be correctly converted and stored in your database. -->
날짜로 cast된 컬럼에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스를 직접 할당할 수 있습니다. 이때, 값은 내부적으로 적절한 형식으로 변환되어 저장됩니다.

<!-- You may customize the default serialization format for all of your model's dates by defining a `serializeDate` method on your model. This method does not affect how your dates are formatted for storage in the database: -->
모든 모델 날짜의 기본 직렬화 포맷을 지정하려면 모델에 `serializeDate` 메서드를 정의하면 됩니다. 이 메서드는 데이터베이스에 저장되는 포맷에는 영향을 주지 않습니다.

```
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<!-- To specify the format that should be used when actually storing a model's dates within your database, you should define a `$dateFormat` property on your model: -->
모델의 날짜 컬럼을 데이터베이스에 실제로 저장할 때의 포맷을 지정하려면 `$dateFormat` 프로퍼티를 설정합니다.

```
/**
 * The storage format of the model's date columns.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
<!-- #### Date Casting, Serialization, and Timezones -->
#### Date Casting, Serialization, and Timezones

<!-- By default, the `date` and `datetime` casts will serialize dates to a UTC ISO-8601 date string (`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`), regardless of the timezone specified in your application's `timezone` configuration option. You are strongly encouraged to always use this serialization format, as well as to store your application's dates in the UTC timezone by not changing your application's `timezone` configuration option from its default `UTC` value. Consistently using the UTC timezone throughout your application will provide the maximum level of interoperability with other date manipulation libraries written in PHP and JavaScript. -->
기본적으로 `date`, `datetime` casting은 UTC 기반의 ISO-8601 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화됩니다. 앱의 `timezone` 설정과 무관하게 UTC로 처리되므로, 앱의 `timezone` 설정을 기본값인 `UTC`로 놔두고, 일관적으로 UTC를 사용하는 것이 좋습니다. 이렇게 하면 PHP, 자바스크립트 등 다양한 날짜 라이브러리와의 호환성이 극대화됩니다.

<!-- If a custom format is applied to the `date` or `datetime` cast, such as `datetime:Y-m-d H:i:s`, the inner timezone of the Carbon instance will be used during date serialization. Typically, this will be the timezone specified in your application's `timezone` configuration option. -->
`date` 또는 `datetime` cast에 사용자 지정 포맷(예: `datetime:Y-m-d H:i:s`)을 적용하면, Carbon 인스턴스의 내부 타임존이 직렬화에 사용됩니다. 보통 이 값은 앱의 `timezone` 설정에 따릅니다.

<a name="enum-casting"></a>
<!-- ### Enum Casting -->
### Enum Casting

<!-- Eloquent also allows you to cast your attribute values to PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `$casts` property array: -->
Eloquent는 속성 값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)으로도 변환할 수 있습니다. 사용하려면, casting할 속성과 Enum 클래스를 모델의 `$casts` 배열에 지정합니다.

```
use App\Enums\ServerStatus;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

<!-- Once you have defined the cast on your model, the specified attribute will be automatically cast to and from an enum when you interact with the attribute: -->
cast를 지정하면, 해당 속성은 자동으로 Enum 인스턴스로 변환되어 읽고 쓸 수 있습니다.

```
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
<!-- #### Casting Arrays of Enums -->
#### Casting Arrays of Enums

<!-- Sometimes you may need your model to store an array of enum values within a single column. To accomplish this, you may utilize the `AsEnumArrayObject` or `AsEnumCollection` casts provided by Laravel: -->
하나의 컬럼에 Enum 값 배열을 저장해야 할 경우도 있습니다. 이럴 때는 Laravel이 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` cast를 사용할 수 있습니다.

```
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'statuses' => AsEnumCollection::class.':'.ServerStatus::class,
];
```

<a name="encrypted-casting"></a>
<!-- ### Encrypted Casting -->
### Encrypted Casting

<!-- The `encrypted` cast will encrypt a model's attribute value using Laravel's built-in [encryption](/docs/10.x/encryption) features. In addition, the `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, and `AsEncryptedCollection` casts work like their unencrypted counterparts; however, as you might expect, the underlying value is encrypted when stored in your database. -->
`encrypted` casting 타입을 지정하면, Laravel의 [encryption](/docs/10.x/encryption) 기능을 이용해 속성값을 암호화해 저장합니다. 또한, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` casting 타입도 있습니다. 이들은 각각의 비암호화 버전처럼 동작하지만, 데이터베이스에 저장 시 값을 암호화합니다.

<!-- As the final length of the encrypted text is not predictable and is longer than its plain text counterpart, make sure the associated database column is of `TEXT` type or larger. In addition, since the values are encrypted in the database, you will not be able to query or search encrypted attribute values. -->
암호화된 텍스트의 최종 길이는 예측이 어렵고 평문보다 훨씬 길 수 있습니다. 따라서, 데이터베이스 컬럼 타입을 반드시 `TEXT` 이상 크기로 지정해야 합니다. 또한, 값이 암호화되어 있으므로 데이터베이스 쿼리나 검색에서 해당 값을 직접 조회할 수 없습니다.

<a name="key-rotation"></a>
<!-- #### Key Rotation -->
#### Key Rotation

<!-- As you may know, Laravel encrypts strings using the `key` configuration value specified in your application's `app` configuration file. Typically, this value corresponds to the value of the `APP_KEY` environment variable. If you need to rotate your application's encryption key, you will need to manually re-encrypt your encrypted attributes using the new key. -->
Laravel은 애플리케이션의 `app` 설정 파일에 지정된 `key` 설정 값(`APP_KEY` 환경변수)을 사용해 문자열을 암호화합니다. 앱의 암호화 키를 변경해야 한다면, 기존에 암호화된 속성을 새 키로 직접 다시 암호화해야 합니다.

<a name="query-time-casting"></a>
<!-- ### Query Time Casting -->
### Query Time Casting

<!-- Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query: -->
때로는 쿼리 실행 시점에도 casting을 적용해야 할 때가 있습니다. 예를 들어, 테이블에서 RAW 값을 선택하는 경우가 있습니다.

```
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->get();
```

<!-- The `last_posted_at` attribute on the results of this query will be a simple string. It would be wonderful if we could apply a `datetime` cast to this attribute when executing the query. Thankfully, we may accomplish this using the `withCasts` method: -->
이 쿼리의 결과에 포함된 `last_posted_at` 속성은 일반 문자열로 반환됩니다. 이 속성에 쿼리 실행 시점에 `datetime` cast를 적용하려면 `withCasts` 메서드를 사용하면 됩니다.

```
$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->withCasts([
    'last_posted_at' => 'datetime'
])->get();
```

<a name="custom-casts"></a>
<!-- ## Custom Casts -->
## Custom Casts

<!-- Laravel has a variety of built-in, helpful cast types; however, you may occasionally need to define your own cast types. To create a cast, execute the `make:cast` Artisan command. The new cast class will be placed in your `app/Casts` directory: -->
Laravel에서는 많은 내장 casting 타입을 제공하지만, 필요하다면 직접 사용자 정의 casting 타입을 생성할 수 있습니다. 새로운 cast 클래스를 만들려면 `make:cast` Artisan 명령어를 실행합니다. 생성된 클래스는 `app/Casts` 디렉터리에 위치합니다.

```shell
php artisan make:cast Json
```

<!-- All custom cast classes implement the `CastsAttributes` interface. Classes that implement this interface must define a `get` and `set` method. The `get` method is responsible for transforming a raw value from the database into a cast value, while the `set` method should transform a cast value into a raw value that can be stored in the database. As an example, we will re-implement the built-in `json` cast type as a custom cast type: -->
사용자 정의 cast 클래스는 모두 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스는 `get`과 `set` 메서드 정의를 요구합니다. `get` 메서드는 데이터베이스의 원시 값을 변환하는 역할, `set` 메서드는 변환된 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환하는 역할을 합니다. 아래는 내장된 `json` cast 타입을 직접 구현한 예시입니다.

```
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class Json implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(Model $model, string $key, mixed $value, array $attributes): array
    {
        return json_decode($value, true);
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return json_encode($value);
    }
}
```

<!-- Once you have defined a custom cast type, you may attach it to a model attribute using its class name: -->
사용자 정의 cast 타입을 정의했으면, 클래스명을 속성에 지정해 사용하면 됩니다.

```
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'options' => Json::class,
    ];
}
```

<a name="value-object-casting"></a>
<!-- ### Value Object Casting -->
### Value Object Casting

<!-- You are not limited to casting values to primitive types. You may also cast values to objects. Defining custom casts that cast values to objects is very similar to casting to primitive types; however, the `set` method should return an array of key / value pairs that will be used to set raw, storable values on the model. -->
casting은 프리미티브 타입에만 제한되지 않습니다. 객체로도 값을 casting할 수 있습니다. 값 객체로 casting하는 사용자 정의 cast 클래스도 프리미티브 타입과 유사하게 작성하며, 다만 `set` 메서드에서 원시로 저장할 키-값 쌍의 배열을 반환해야 합니다.

<!-- As an example, we will define a custom cast class that casts multiple model values into a single `Address` value object. We will assume the `Address` value has two public properties: `lineOne` and `lineTwo`: -->
예시로, 여러 모델 값을 하나의 `Address` 값 객체로 취급하는 사용자 정의 cast 클래스를 만듭니다. 예시의 `Address` 객체에는 public 프로퍼티 `lineOne`, `lineTwo`가 있다고 가정합니다.

```
<?php

namespace App\Casts;

use App\ValueObjects\Address as AddressValueObject;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;
use InvalidArgumentException;

class Address implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function get(Model $model, string $key, mixed $value, array $attributes): AddressValueObject
    {
        return new AddressValueObject(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, string>
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): array
    {
        if (! $value instanceof AddressValueObject) {
            throw new InvalidArgumentException('The given value is not an Address instance.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

<!-- When casting to value objects, any changes made to the value object will automatically be synced back to the model before the model is saved: -->
값 객체로 casting되어 반환된 속성은 값 객체의 속성을 변경하더라도, 모델이 저장되기 전에 해당 변경 내용이 자동으로 동기화됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함한 Eloquent 모델을 JSON 또는 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
<!-- #### Value Object Caching -->
#### Value Object Caching

<!-- When attributes that are cast to value objects are resolved, they are cached by Eloquent. Therefore, the same object instance will be returned if the attribute is accessed again. -->
값 객체로 casting된 속성이 접근될 때 Eloquent에서 해당 객체 인스턴스를 캐싱합니다. 즉, 한 번 접근한 속성은 재접근 시 동일한 인스턴스가 반환됩니다.

<!-- If you would like to disable the object caching behavior of custom cast classes, you may declare a public `withoutObjectCaching` property on your custom cast class: -->
사용자 정의 cast 클래스에서 객체 캐싱 기능을 비활성화하려면, 커스텀 cast 클래스에 public `withoutObjectCaching` 프로퍼티를 선언하면 됩니다.

```php
class Address implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
<!-- ### Array / JSON Serialization -->
### Array / JSON Serialization

<!-- When an Eloquent model is converted to an array or JSON using the `toArray` and `toJson` methods, your custom cast value objects will typically be serialized as well as long as they implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces. However, when using value objects provided by third-party libraries, you may not have the ability to add these interfaces to the object. -->
Eloquent 모델을 배열이나 JSON으로 변환(`toArray`, `toJson` 메서드 사용)하면, 커스텀 cast 값 객체도 일반적으로 함께 직렬화됩니다(해당 객체가 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현한 경우). 하지만, 외부 라이브러리에서 제공하는 값 객체는 이 인터페이스를 추가할 수 없을 수도 있습니다.

<!-- Therefore, you may specify that your custom cast class will be responsible for serializing the value object. To do so, your custom cast class should implement the `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` interface. This interface states that your class should contain a `serialize` method which should return the serialized form of your value object: -->
이런 경우, 커스텀 cast 클래스에서 직접 값 객체의 직렬화 결과를 반환하도록 지정할 수 있습니다. 이를 위해, 커스텀 cast 클래스에서 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 하며, 직렬화 결과를 반환하는 `serialize` 메서드를 포함해야 합니다.

```
/**
 * Get the serialized representation of the value.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(Model $model, string $key, mixed $value, array $attributes): string
{
    return (string) $value;
}
```

<a name="inbound-casting"></a>
<!-- ### Inbound Casting -->
### Inbound Casting

<!-- Occasionally, you may need to write a custom cast class that only transforms values that are being set on the model and does not perform any operations when attributes are being retrieved from the model. -->
간혹 모델의 속성 값을 세팅할 때만 동작하고, 값을 읽을 때는 아무런 처리를 하지 않는 "입력 전용" 커스텀 cast 클래스를 만들어야 할 경우가 있습니다.

<!-- Inbound only custom casts should implement the `CastsInboundAttributes` interface, which only requires a `set` method to be defined. The `make:cast` Artisan command may be invoked with the `--inbound` option to generate an inbound only cast class: -->
입력 전용 커스텀 cast는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 인터페이스에서는 `set` 메서드만 정의하면 됩니다. `make:cast` Artisan 명령어에 `--inbound` 옵션을 추가하면 입력 전용 cast 클래스를 손쉽게 생성할 수 있습니다.

```shell
php artisan make:cast Hash --inbound
```

<!-- A classic example of an inbound only cast is a "hashing" cast. For example, we may define a cast that hashes inbound values via a given algorithm: -->
입력 전용 cast의 대표적인 예시가 해싱 cast입니다. 예를 들어, 특정 알고리즘으로 입력 값을 해싱하는 cast를 만들 수 있습니다.

```
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class Hash implements CastsInboundAttributes
{
    /**
     * Create a new cast class instance.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return is_null($this->algorithm)
                    ? bcrypt($value)
                    : hash($this->algorithm, $value);
    }
}
```

<a name="cast-parameters"></a>
<!-- ### Cast Parameters -->
### Cast Parameters

<!-- When attaching a custom cast to a model, cast parameters may be specified by separating them from the class name using a `:` character and comma-delimiting multiple parameters. The parameters will be passed to the constructor of the cast class: -->
커스텀 cast를 모델에 적용할 때, 클래스명 뒤에 `:` 문자를 사용해서 파라미터를 전달할 수 있습니다. 여러 파라미터는 콤마로 구분되며, 생성자에 인자로 전달됩니다.

```
/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'secret' => Hash::class.':sha256',
];
```

<a name="castables"></a>
<!-- ### Castables -->
### Castables

<!-- You may want to allow your application's value objects to define their own custom cast classes. Instead of attaching the custom cast class to your model, you may alternatively attach a value object class that implements the `Illuminate\Contracts\Database\Eloquent\Castable` interface: -->
애플리케이션의 값 객체가 자신만의 커스텀 caster 클래스를 직접 지정할 수 있도록 하고 싶을 수 있습니다. 이때는 모델에 커스텀 cast 클래스 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 직접 지정하면 됩니다.

```
use App\ValueObjects\Address;

protected $casts = [
    'address' => Address::class,
];
```

<!-- Objects that implement the `Castable` interface must define a `castUsing` method that returns the class name of the custom caster class that is responsible for casting to and from the `Castable` class: -->
`Castable` 인터페이스를 구현하는 객체는, `Castable` 클래스로의 casting 및 역casting을 담당하는 커스텀 caster 클래스명을 반환하는 `castUsing` 메서드를 정의해야 합니다.

```
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * Get the name of the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AddressCast::class;
    }
}
```

<!-- When using `Castable` classes, you may still provide arguments in the `$casts` definition. The arguments will be passed to the `castUsing` method: -->
`Castable` 클래스를 사용할 때도, `$casts` 설정에서 파라미터를 함께 전달할 수 있습니다. 이 값들은 `castUsing` 메서드에 인자로 전달됩니다.

```
use App\ValueObjects\Address;

protected $casts = [
    'address' => Address::class.':argument',
];
```

<a name="anonymous-cast-classes"></a>
<!-- #### Castables & Anonymous Cast Classes -->
#### Castables & Anonymous Cast Classes

<!-- By combining "castables" with PHP's [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php), you may define a value object and its casting logic as a single castable object. To accomplish this, return an anonymous class from your value object's `castUsing` method. The anonymous class should implement the `CastsAttributes` interface: -->
"Castable" 기능과 PHP의 [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합해, 값 객체와 casting 로직을 하나의 Castable 객체로 구현할 수도 있습니다. 이를 위해, 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다.

```
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * Get the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): CastsAttributes
    {
        return new class implements CastsAttributes
        {
            public function get(Model $model, string $key, mixed $value, array $attributes): Address
            {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set(Model $model, string $key, mixed $value, array $attributes): array
            {
                return [
                    'address_line_one' => $value->lineOne,
                    'address_line_two' => $value->lineTwo,
                ];
            }
        };
    }
}
```
