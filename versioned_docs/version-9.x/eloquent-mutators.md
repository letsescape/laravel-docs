<!-- # Eloquent: Mutators & Casting -->
# Eloquent: Mutators & Casting

- [Introduction](#introduction)
- [Accessors & Mutators](#accessors-and-mutators)
    - [Defining An Accessor](#defining-an-accessor)
    - [Defining A Mutator](#defining-a-mutator)
- [Attribute Casting](#attribute-casting)
    - [Array & JSON Casting](#array-and-json-casting)
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

<!-- Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/9.x/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model. -->
accessor(accessors), mutator(mutators), 그리고 attribute casting을 사용하면 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 값을 변환할 수 있습니다. 예를 들어, [Laravel encrypter](/docs/9.x/encryption)을 활용해 데이터를 데이터베이스에 저장할 때는 암호화하고, Eloquent 모델에서 값을 조회할 때는 자동으로 복호화하도록 만들 수 있습니다. 또는, 데이터베이스에 JSON 문자열로 저장된 값을 Eloquent 모델을 통해 접근할 때 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
<!-- ## Accessors & Mutators -->
## Accessors & Mutators

<a name="defining-an-accessor"></a>
<!-- ### Defining An Accessor -->
### Defining An Accessor

<!-- An accessor transforms an Eloquent attribute value when it is accessed. To define an accessor, create a protected method on your model to represent the accessible attribute. This method name should correspond to the "camel case" representation of the true underlying model attribute / database column when applicable. -->
accessor는 Eloquent 속성 값을 조회할 때 값을 변환합니다. accessor를 정의하려면, 모델에서 해당 가능 속성에 대응하는 보호된(protected) 메서드를 만듭니다. 이 메서드의 이름은 실제 모델 속성이나 데이터베이스 컬럼의 "카멜 케이스(camel case)" 형태와 일치해야 합니다.

<!-- In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute. All attribute accessor / mutator methods must declare a return type-hint of `Illuminate\Database\Eloquent\Casts\Attribute`: -->
아래 예시에서는 `first_name` 속성에 대한 accessor를 정의합니다. 이 accessor는 Eloquent가 `first_name` 속성의 값을 조회할 때 자동으로 호출됩니다. 모든 속성 accessor/mutator 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입힌트를 반환형으로 선언해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the user's first name.
     *
     * @return \Illuminate\Database\Eloquent\Casts\Attribute
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => ucfirst($value),
        );
    }
}
```

<!-- All accessor methods return an `Attribute` instance which defines how the attribute will be accessed and, optionally, mutated. In this example, we are only defining how the attribute will be accessed. To do so, we supply the `get` argument to the `Attribute` class constructor. -->
모든 accessor 메서드는 `Attribute` 인스턴스를 반환하며, 이 인스턴스는 해당 속성을 어떻게 접근(조회)하고(필요하다면) 변이할지 정의합니다. 위 예시에서는 속성을 어떻게 조회할지만 지정하고 있습니다. 이를 위해 `Attribute` 클래스의 생성자에 `get` 인자를 전달합니다.

<!-- As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the accessor, you may simply access the `first_name` attribute on a model instance: -->
위에서 볼 수 있듯 컬럼의 원래 값이 accessor에게 전달되므로, 값을 자유롭게 가공(변경)해서 반환할 수 있습니다. accessor 값을 사용하려면, 그냥 모델 인스턴스에서 `first_name` 속성에 접근하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이렇게 계산된(가공된) 값들을 모델의 배열/JSON 표현에 포함하고 싶다면, [you will need to append them](/docs/9.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
<!-- #### Building Value Objects From Multiple Attributes -->
#### Building Value Objects From Multiple Attributes

<!-- Sometimes your accessor may need to transform multiple model attributes into a single "value object". To do so, your `get` closure may accept a second argument of `$attributes`, which will be automatically supplied to the closure and will contain an array of all of the model's current attributes: -->
어떤 경우에는 accessor가 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 수 있습니다. 이럴 때는, `get` 클로저에서 두 번째 인자인 `$attributes`를 받을 수 있으며, 이 인자에는 해당 모델의 현재 모든 속성이 배열로 전달됩니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
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
accessor를 통해 값 객체(value object)가 반환될 때, 해당 객체에서 값이 변경되면 모델을 저장하기 전에 그 내용이 자동으로 모델에 반영됩니다. 이는 Eloquent가 accessor에서 반환된 인스턴스를 내부적으로 보관하여, accessor를 호출할 때마다 같은 인스턴스를 반환하기 때문에 가능합니다.

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

<!-- However, you may sometimes wish to enable caching for primitive values like strings and booleans, particularly if they are computationally intensive. To accomplish this, you may invoke the `shouldCache` method when defining your accessor: -->
하지만, 문자열이나 불리언과 같은 원시 값(primitive value)도, 연산 비용이 많이 든다면 캐싱하고 싶을 수 있습니다. 이럴 때는 accessor 정의 시 `shouldCache` 메서드를 호출하면 됩니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn ($value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

<!-- If you would like to disable the object caching behavior of attributes, you may invoke the `withoutObjectCaching` method when defining the attribute: -->
반대로 객체 캐싱을 비활성화하고 싶다면, 속성 정의 시 `withoutObjectCaching` 메서드를 호출하면 됩니다.

```php
/**
 * Interact with the user's address.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    )->withoutObjectCaching();
}
```

<a name="defining-a-mutator"></a>
<!-- ### Defining A Mutator -->
### Defining A Mutator

<!-- A mutator transforms an Eloquent attribute value when it is set. To define a mutator, you may provide the `set` argument when defining your attribute. Let's define a mutator for the `first_name` attribute. This mutator will be automatically called when we attempt to set the value of the `first_name` attribute on the model: -->
mutator는 Eloquent 속성 값이 설정될 때 값을 변환(가공)합니다. mutator를 정의하려면, 속성 정의 시 `set` 인자를 전달하면 됩니다. 아래는 `first_name` 속성에 mutator를 정의하는 예시입니다. 이 mutator는 `first_name` 속성 값을 설정할 때 자동으로 호출됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Interact with the user's first name.
     *
     * @return \Illuminate\Database\Eloquent\Casts\Attribute
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => ucfirst($value),
            set: fn ($value) => strtolower($value),
        );
    }
}
```

<!-- The mutator closure will receive the value that is being set on the attribute, allowing you to manipulate the value and return the manipulated value. To use our mutator, we only need to set the `first_name` attribute on an Eloquent model: -->
mutator 클로저는 속성에 설정하려는 값을 받아서, 원하는 대로 가공하고 그 결과 값을 반환할 수 있습니다. mutator를 사용하려면, Eloquent 모델에서 `first_name` 속성에 값을 할당하기만 하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

<!-- In this example, the `set` callback will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its resulting value in the model's internal `$attributes` array. -->
이 예시에서 `set` 콜백은 값 `Sally`와 함께 호출됩니다. mutator는 이 값을 `strtolower` 함수로 변환해서, 내부 `$attributes` 배열에 결과 값을 저장합니다.

<a name="mutating-multiple-attributes"></a>
<!-- #### Mutating Multiple Attributes -->
#### Mutating Multiple Attributes

<!-- Sometimes your mutator may need to set multiple attributes on the underlying model. To do so, you may return an array from the `set` closure. Each key in the array should correspond with an underlying attribute / database column associated with the model: -->
어떤 경우에는 mutator에서 내부적으로 여러 속성을 동시에 설정해야 할 수도 있습니다. 이럴 때는, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델에서 대응되는 속성/데이터베이스 컬럼과 일치해야 합니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
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
attribute casting은 accessor나 mutator를 별도로 정의하지 않고도 유사한 기능을 제공합니다. 모델의 `$casts` 속성을 사용하면 속성을 일반적으로 많이 사용하는 데이터 타입으로 자동 변환할 수 있습니다.

<!-- The `$casts` property should be an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are: -->
`$casts` 속성은, 속성명을 키로 하고 casting할 타입을 값으로 갖는 배열이어야 합니다. 지원되는 cast 타입은 다음과 같습니다.

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
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

<!-- </div> -->
</div>

<!-- To demonstrate attribute casting, let's cast the `is_admin` attribute, which is stored in our database as an integer (`0` or `1`) to a boolean value: -->
예를 들어, 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언 값으로 casting해보겠습니다.

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
이렇게 cast를 정의하면, 데이터베이스에 값이 정수로 저장되어 있더라도 `is_admin` 속성은 항상 불리언으로 변환되어 접근할 수 있습니다.

```
$user = App\Models\User::find(1);

if ($user->is_admin) {
    //
}
```

<!-- If you need to add a new, temporary cast at runtime, you may use the `mergeCasts` method. These cast definitions will be added to any of the casts already defined on the model: -->
런타임에 임시로 새로운 cast를 추가하고 싶을 때는 `mergeCasts` 메서드를 사용할 수 있습니다. 이렇게 추가된 cast는 기존 cast에 덧붙여집니다.

```
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 casting되지 않습니다. 또한, 관계명과 동일한 이름의 속성 또는 cast는 절대 정의하지 않아야 합니다.

<a name="stringable-casting"></a>
<!-- #### Stringable Casting -->
#### Stringable Casting

<!-- You may use the `Illuminate\Database\Eloquent\Casts\AsStringable` cast class to cast a model attribute to a [fluent `Illuminate\Support\Stringable` object](/docs/9.x/helpers#fluent-strings-method-list): -->
`Illuminate\Database\Eloquent\Casts\AsStringable` cast 클래스를 사용하면 모델 속성을 [fluent `Illuminate\Support\Stringable` object](/docs/9.x/helpers#fluent-strings-method-list)로 변환할 수 있습니다.

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
<!-- ### Array & JSON Casting -->
### Array & JSON Casting

<!-- The `array` cast is particularly useful when working with columns that are stored as serialized JSON. For example, if your database has a `JSON` or `TEXT` field type that contains serialized JSON, adding the `array` cast to that attribute will automatically deserialize the attribute to a PHP array when you access it on your Eloquent model: -->
`array` cast는 직렬화된 JSON으로 저장된 컬럼을 다룰 때 매우 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 타입 컬럼이 있고 직렬화된 JSON 데이터가 들어있다면, 해당 속성에 `array` cast를 추가하면 Eloquent 모델에서 접근할 때 자동으로 PHP 배열로 역직렬화해줍니다.

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
이렇게 cast를 정의하면, `options` 속성에 접근할 때 JSON에서 PHP 배열로 자동 변환됩니다. 또한, `options` 속성에 배열 값을 설정하면 자동으로 JSON으로 직렬화되어 데이터베이스에 저장됩니다.

```
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

<!-- To update a single field of a JSON attribute with a more terse syntax, you may use the `->` operator when calling the `update` method: -->
JSON 속성의 개별 필드만 간결하게 업데이트하고 싶을 때는, `update` 메서드 사용 시 `->` 연산자를 활용할 수 있습니다.

```
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
<!-- #### Array Object & Collection Casting -->
#### Array Object & Collection Casting

<!-- Although the standard `array` cast is sufficient for many applications, it does have some disadvantages. Since the `array` cast returns a primitive type, it is not possible to mutate an offset of the array directly. For example, the following code will trigger a PHP error: -->
일반적인 `array` cast로도 충분한 경우가 많지만, 이 방식에는 몇 가지 단점이 있습니다. `array` cast는 단순한 원시 타입을 반환하므로, 다음처럼 배열의 일부 요소만 직접 수정하면 PHP 에러가 발생할 수 있습니다.

```
$user = User::find(1);

$user->options['key'] = $value;
```

<!-- To solve this, Laravel offers an `AsArrayObject` cast that casts your JSON attribute to an [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) class. This feature is implemented using Laravel's [custom cast](#custom-casts) implementation, which allows Laravel to intelligently cache and transform the mutated object such that individual offsets may be modified without triggering a PHP error. To use the `AsArrayObject` cast, simply assign it to an attribute: -->
이 문제를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 변환하는 `AsArrayObject` cast를 제공합니다. 이 기능은 Laravel의 [custom cast](#custom-casts) 구현을 활용하여, Laravel이 변이된 객체를 지능적으로 캐싱 및 변환하므로 PHP 에러를 발생시키지 않고 개별 오프셋을 변경할 수 있습니다. `AsArrayObject` cast를 사용하려면, 다음과 같이 속성에 할당하기만 하면 됩니다.

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

<!-- Similarly, Laravel offers an `AsCollection` cast that casts your JSON attribute to a Laravel [Collection](/docs/9.x/collections) instance: -->
비슷하게, Laravel은 `AsCollection` cast도 제공합니다. 이 cast는 JSON 속성을 Laravel [Collection](/docs/9.x/collections) 인스턴스로 변환합니다.

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

<a name="date-casting"></a>
<!-- ### Date Casting -->
### Date Casting

<!-- By default, Eloquent will cast the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which extends the PHP `DateTime` class and provides an assortment of helpful methods. You may cast additional date attributes by defining additional date casts within your model's `$casts` property array. Typically, dates should be cast using the `datetime` or `immutable_datetime` cast types. -->
기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 casting합니다. Carbon은 PHP `DateTime` 클래스를 확장하며, 다양한 유용한 메서드들을 제공합니다. 추가적인 날짜 속성이 있다면, 모델의 `$casts` 배열에 추가로 날짜 cast를 정의할 수 있습니다. 보통 `datetime` 또는 `immutable_datetime` cast 타입을 사용합니다.

<!-- When defining a `date` or `datetime` cast, you may also specify the date's format. This format will be used when the [model is serialized to an array or JSON](/docs/9.x/eloquent-serialization): -->
`date` 또는 `datetime` cast를 정의할 때, 날짜 포맷도 같이 지정할 수 있습니다. 지정한 포맷은 [model is serialized to an array or JSON](/docs/9.x/eloquent-serialization) 사용됩니다.

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
날짜로 cast된 컬럼에는 유닉스 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스를 모두 저장할 수 있습니다. 값은 적절하게 변환되어 데이터베이스에 저장됩니다.

<!-- You may customize the default serialization format for all of your model's dates by defining a `serializeDate` method on your model. This method does not affect how your dates are formatted for storage in the database: -->
모델의 모든 날짜 속성에 대해 기본 직렬화 포맷을 커스터마이징하고 싶다면, 모델에 `serializeDate` 메서드를 정의하면 됩니다. 이 메서드는 데이터베이스 저장 포맷에는 영향을 주지 않습니다.

```
/**
 * Prepare a date for array / JSON serialization.
 *
 * @param  \DateTimeInterface  $date
 * @return string
 */
protected function serializeDate(DateTimeInterface $date)
{
    return $date->format('Y-m-d');
}
```

<!-- To specify the format that should be used when actually storing a model's dates within your database, you should define a `$dateFormat` property on your model: -->
모델의 날짜 속성을 실제로 데이터베이스에 저장할 때 사용할 포맷을 지정하려면, 모델에 `$dateFormat` 속성을 정의해야 합니다.

```
/**
 * The storage format of the model's date columns.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
<!-- #### Date Casting, Serialization, & Timezones -->
#### Date Casting, Serialization, & Timezones

<!-- By default, the `date` and `datetime` casts will serialize dates to a UTC ISO-8601 date string (`1986-05-28T21:05:54.000000Z`), regardless of the timezone specified in your application's `timezone` configuration option. You are strongly encouraged to always use this serialization format, as well as to store your application's dates in the UTC timezone by not changing your application's `timezone` configuration option from its default `UTC` value. Consistently using the UTC timezone throughout your application will provide the maximum level of interoperability with other date manipulation libraries written in PHP and JavaScript. -->
기본적으로 `date`와 `datetime` cast는 애플리케이션의 `timezone` 설정과 무관하게, 날짜를 UTC ISO-8601 문자열(`1986-05-28T21:05:54.000000Z`)로 직렬화합니다. 다른 PHP/JavaScript 라이브러리와의 호환성을 극대화하려면 이 형식과 UTC 타임존을 항상 사용하는 것이 권장됩니다. 즉, 애플리케이션의 `timezone` 설정을 기본값인 `UTC`로 유지하는 것이 바람직합니다.

<!-- If a custom format is applied to the `date` or `datetime` cast, such as `datetime:Y-m-d H:i:s`, the inner timezone of the Carbon instance will be used during date serialization. Typically, this will be the timezone specified in your application's `timezone` configuration option. -->
만약 `date` 또는 `datetime` cast에 `datetime:Y-m-d H:i:s`와 같이 커스텀 포맷을 적용하면, 직렬화 시 Carbon 인스턴스의 내부 타임존이 적용됩니다. 이는 일반적으로 애플리케이션의 `timezone` 설정을 따릅니다.

<a name="enum-casting"></a>
<!-- ### Enum Casting -->
### Enum Casting

> [!WARNING]
> Enum casting은 PHP 8.1 이상에서만 사용할 수 있습니다.

<!-- Eloquent also allows you to cast your attribute values to PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `$casts` property array: -->
Eloquent는 속성 값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php) 타입으로도 casting할 수 있습니다. 속성 키와 Enum 클래스를 모델의 `$casts` 배열에 지정하면 됩니다.

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
이렇게 cast를 정의하면, 해당 속성을 조회하거나 설정할 때 자동으로 Enum 타입으로 변환됩니다.

```
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
<!-- #### Casting Arrays Of Enums -->
#### Casting Arrays Of Enums

<!-- Sometimes you may need your model to store an array of enum values within a single column. To accomplish this, you may utilize the `AsEnumArrayObject` or `AsEnumCollection` casts provided by Laravel: -->
모델이 하나의 컬럼에 Enum 값들을 배열로 저장해야 하는 경우도 있습니다. 이때는 Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` cast를 사용할 수 있습니다.

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

<!-- The `encrypted` cast will encrypt a model's attribute value using Laravel's built-in [encryption](/docs/9.x/encryption) features. In addition, the `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, and `AsEncryptedCollection` casts work like their unencrypted counterparts; however, as you might expect, the underlying value is encrypted when stored in your database. -->
`encrypted` cast를 사용하면 모델의 속성 값을 Laravel의 내장 [encryption](/docs/9.x/encryption)으로 암호화할 수 있습니다. 마찬가지로, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등은 암호화되지 않은 cast와 거의 동일하게 동작하지만, 값이 데이터베이스에 저장될 때 암호화된다는 점이 다릅니다.

<!-- As the final length of the encrypted text is not predictable and is longer than its plain text counterpart, make sure the associated database column is of `TEXT` type or larger. In addition, since the values are encrypted in the database, you will not be able to query or search encrypted attribute values. -->
암호화된 텍스트는 원본보다 길고, 예측할 수 없는 길이를 갖습니다. 따라서 해당 컬럼은 반드시 `TEXT` 타입 이상으로 만들어야 합니다. 또한, 암호화된 컬럼은 데이터베이스에서 직접 조회하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
<!-- #### Key Rotation -->
#### Key Rotation

<!-- As you may know, Laravel encrypts strings using the `key` configuration value specified in your application's `app` configuration file. Typically, this value corresponds to the value of the `APP_KEY` environment variable. If you need to rotate your application's encryption key, you will need to manually re-encrypt your encrypted attributes using the new key. -->
Laravel은 애플리케이션의 `app` 설정 파일의 `key` 설정값, 즉 보통 `APP_KEY` 환경 변수로 지정된 값을 이용해서 문자열을 암호화합니다. 만약 암호화 키를 변경해야 한다면, 새 키로 암호화된 속성 값을 직접 다시 암호화해 주어야 합니다.

<a name="query-time-casting"></a>
<!-- ### Query Time Casting -->
### Query Time Casting

<!-- Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query: -->
때로는 특정 쿼리 실행 시 임시로 casting을 적용해야 할 수 있습니다. 예를 들어, 테이블에서 원시 값을 select할 때 다음과 같은 쿼리를 작성할 수 있습니다.

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
이 쿼리의 결과로 얻은 `last_posted_at` 속성의 값은 단순한 문자열입니다. 이 속성에 쿼리 실행 시점에 `datetime` cast를 적용하고 싶다면, `withCasts` 메서드를 사용하면 됩니다.

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
Laravel은 다양한 내장 cast 타입을 제공하지만, 필요에 따라 직접 cast 타입을 정의할 수 있습니다. cast 클래스를 만들려면 `make:cast` 아티즌 명령어를 실행하세요. 새 cast 클래스는 `app/Casts` 디렉터리에 생성됩니다.

```shell
php artisan make:cast Json
```

<!-- All custom cast classes implement the `CastsAttributes` interface. Classes that implement this interface must define a `get` and `set` method. The `get` method is responsible for transforming a raw value from the database into a cast value, while the `set` method should transform a cast value into a raw value that can be stored in the database. As an example, we will re-implement the built-in `json` cast type as a custom cast type: -->
모든 커스텀 cast 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현하는 클래스는 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스에서 조회한 값을 변환하고, `set` 메서드는 변환된 값을 데이터베이스에 저장 가능한 원시 값으로 가공하는 역할을 합니다. 다음은 내장 `json` cast 타입을 직접 다시 구현하는 예시입니다.

```
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Json implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  mixed  $value
     * @param  array  $attributes
     * @return array
     */
    public function get($model, $key, $value, $attributes)
    {
        return json_decode($value, true);
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  array  $value
     * @param  array  $attributes
     * @return string
     */
    public function set($model, $key, $value, $attributes)
    {
        return json_encode($value);
    }
}
```

<!-- Once you have defined a custom cast type, you may attach it to a model attribute using its class name: -->
커스텀 cast 타입을 정의한 뒤, 해당 클래스명을 사용해 모델 속성에 cast를 지정할 수 있습니다.

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
값을 단순한 원시 타입으로만 casting할 수 있는 것은 아닙니다. 객체로도 casting할 수 있습니다. 값을 객체로 casting하는 커스텀 cast를 정의하는 방법은 원시 타입과 매우 비슷하지만, `set` 메서드는 원시 값의 배열을 반환해야 하며, 이들 값이 모델에 원시 값으로 저장됩니다.

<!-- As an example, we will define a custom cast class that casts multiple model values into a single `Address` value object. We will assume the `Address` value has two public properties: `lineOne` and `lineTwo`: -->
예를 들어, 여러 모델 값을 하나의 `Address` 값 객체로 변환하는 커스텀 cast 클래스를 작성하겠습니다. 여기에서 `Address` 값은 `lineOne`과 `lineTwo`라는 두 개의 공개 속성을 가진다고 가정합니다.

```
<?php

namespace App\Casts;

use App\ValueObjects\Address as AddressValueObject;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use InvalidArgumentException;

class Address implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  mixed  $value
     * @param  array  $attributes
     * @return \App\ValueObjects\Address
     */
    public function get($model, $key, $value, $attributes)
    {
        return new AddressValueObject(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  \App\ValueObjects\Address  $value
     * @param  array  $attributes
     * @return array
     */
    public function set($model, $key, $value, $attributes)
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
값 객체로 casting하면, 해당 객체의 값 변화가 생길 경우 모델을 저장할 때 자동으로 모델에 적용됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이 있다면, 해당 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="array-json-serialization"></a>
<!-- ### Array / JSON Serialization -->
### Array / JSON Serialization

<!-- When an Eloquent model is converted to an array or JSON using the `toArray` and `toJson` methods, your custom cast value objects will typically be serialized as well as long as they implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces. However, when using value objects provided by third-party libraries, you may not have the ability to add these interfaces to the object. -->
Eloquent 모델을 `toArray` 또는 `toJson` 메서드로 배열이나 JSON으로 변환할 때, 커스텀 cast 값 객체도 보통 직렬화됩니다. 단, 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다. 그렇지만, 서드파티 라이브러리에서 제공하는 값을 사용할 경우 이 인터페이스를 직접 구현할 수 없는 경우도 있습니다.

<!-- Therefore, you may specify that your custom cast class will be responsible for serializing the value object. To do so, your custom cast class should implement the `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` interface. This interface states that your class should contain a `serialize` method which should return the serialized form of your value object: -->
이런 경우, 커스텀 cast 클래스에서 값 객체의 직렬화를 직접 처리하도록 할 수 있습니다. 이를 위해서, 커스텀 cast 클래스에 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하면 됩니다. 이 인터페이스에서는 `serialize` 메서드를 구현해야 하며, 이 메서드가 직렬화된 형태를 반환하게 됩니다.

```
/**
 * Get the serialized representation of the value.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  mixed  $value
 * @param  array  $attributes
 * @return mixed
 */
public function serialize($model, string $key, $value, array $attributes)
{
    return (string) $value;
}
```

<a name="inbound-casting"></a>
<!-- ### Inbound Casting -->
### Inbound Casting

<!-- Occasionally, you may need to write a custom cast class that only transforms values that are being set on the model and does not perform any operations when attributes are being retrieved from the model. -->
때로는 모델에 값을 설정할 때만 값을 변환하는 커스텀 cast가 필요할 수 있습니다. 조회할 때는 아무런 변환을 하지 않는 경우입니다.

<!-- Inbound only custom casts should implement the `CastsInboundAttributes` interface, which only requires a `set` method to be defined. The `make:cast` Artisan command may be invoked with the `--inbound` option to generate an inbound only cast class: -->
이런 인바운드 전용 커스텀 cast는 `CastsInboundAttributes` 인터페이스만 구현하면 되고, 이 경우 `set` 메서드만 정의하면 됩니다. `make:cast` 아티즌 명령어에 `--inbound` 옵션을 주면 인바운드 전용 cast 클래스를 생성할 수 있습니다.

```shell
php artisan make:cast Hash --inbound
```

<!-- A classic example of an inbound only cast is a "hashing" cast. For example, we may define a cast that hashes inbound values via a given algorithm: -->
대표적인 예가 "해싱(hashing)" cast입니다. 아래는 지정된 알고리즘으로 들어오는 값을 해싱하는 cast 예시입니다.

```
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;

class Hash implements CastsInboundAttributes
{
    /**
     * The hashing algorithm.
     *
     * @var string
     */
    protected $algorithm;

    /**
     * Create a new cast class instance.
     *
     * @param  string|null  $algorithm
     * @return void
     */
    public function __construct($algorithm = null)
    {
        $this->algorithm = $algorithm;
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  array  $value
     * @param  array  $attributes
     * @return string
     */
    public function set($model, $key, $value, $attributes)
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
모델에 커스텀 cast를 지정할 때, 클래스명 뒤에 `:`로 구분해 파라미터를 넘길 수 있으며, 다수의 파라미터는 콤마로 구분합니다. 이 파라미터는 cast 클래스의 생성자로 전달됩니다.

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
애플리케이션의 값 객체가 자체적으로 커스텀 cast 클래스를 정의하게 하고 싶을 수도 있습니다. 이 경우, 모델에서 커스텀 cast 클래스 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 지정할 수 있습니다.

```
use App\Models\Address;

protected $casts = [
    'address' => Address::class,
];
```

<!-- Objects that implement the `Castable` interface must define a `castUsing` method that returns the class name of the custom caster class that is responsible for casting to and from the `Castable` class: -->
`Castable` 인터페이스를 구현한 객체는 반드시 `castUsing` 메서드를 정의해야 하며, 이 메서드에서 `Castable` 클래스로의 casting 및 역casting을 담당하는 커스텀 caster 클래스명을 반환해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * Get the name of the caster class to use when casting from / to this cast target.
     *
     * @param  array  $arguments
     * @return string
     */
    public static function castUsing(array $arguments)
    {
        return AddressCast::class;
    }
}
```

<!-- When using `Castable` classes, you may still provide arguments in the `$casts` definition. The arguments will be passed to the `castUsing` method: -->
`Castable` 클래스를 사용할 때도 `$casts` 정의에서 인자를 넘길 수 있습니다. 이 인자들은 `castUsing` 메서드로 전달됩니다.

```
use App\Models\Address;

protected $casts = [
    'address' => Address::class.':argument',
];
```

<a name="anonymous-cast-classes"></a>
<!-- #### Castables & Anonymous Cast Classes -->
#### Castables & Anonymous Cast Classes

<!-- By combining "castables" with PHP's [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php), you may define a value object and its casting logic as a single castable object. To accomplish this, return an anonymous class from your value object's `castUsing` method. The anonymous class should implement the `CastsAttributes` interface: -->
"Castable(Castables)"을 PHP의 [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php)와 결합하면, 값 객체와 그 값의 casting 로직을 한 번에 정의할 수 있습니다. 이렇게 하려면 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하세요. 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * Get the caster class to use when casting from / to this cast target.
     *
     * @param  array  $arguments
     * @return object|string
     */
    public static function castUsing(array $arguments)
    {
        return new class implements CastsAttributes
        {
            public function get($model, $key, $value, $attributes)
            {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set($model, $key, $value, $attributes)
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
