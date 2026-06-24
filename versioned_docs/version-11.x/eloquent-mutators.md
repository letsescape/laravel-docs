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

<!-- Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/11.x/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model. -->
accessor, 변조자(mutator), 그리고 속성(attribute) casting을 통해 Eloquent 모델 인스턴스에서 속성 값을 읽거나 쓸 때 자유롭게 변환할 수 있습니다. 예를 들어, [Laravel encrypter](/docs/11.x/encryption)을 사용해 값을 데이터베이스에 저장할 때 암호화하고, 모델에서 해당 속성에 접근할 때 자동으로 복호화되도록 할 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 변환할 수도 있습니다.

<a name="accessors-and-mutators"></a>
<!-- ## Accessors and Mutators -->
## Accessors and Mutators

<a name="defining-an-accessor"></a>
<!-- ### Defining an Accessor -->
### Defining an Accessor

<!-- An accessor transforms an Eloquent attribute value when it is accessed. To define an accessor, create a protected method on your model to represent the accessible attribute. This method name should correspond to the "camel case" representation of the true underlying model attribute / database column when applicable. -->
accessor는 Eloquent 속성의 값을 읽을 때 자동으로 변환해주는 메서드입니다. accessor를 정의하려면, 모델 안에 해당 속성을 나타내는 보호된(protected) 메서드를 생성합니다. 이 메서드의 이름은 가능하다면 실제 모델 속성/데이터베이스 컬럼명을 "카멜 케이스(camel case)"로 표기해야 합니다.

<!-- In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute. All attribute accessor / mutator methods must declare a return type-hint of `Illuminate\Database\Eloquent\Casts\Attribute`: -->
아래 예시에서는 `first_name` 속성에 accessor를 정의합니다. 이 accessor는 Eloquent가 `first_name` 속성 값을 읽으려고 할 때마다 자동으로 호출됩니다. 모든 어트리뷰트 accessor/변조자 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 반환해야 합니다.

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
모든 accessor 메서드는 속성을 접근(읽기), 선택적으로 변조(쓰기)하는 방법을 정의한 `Attribute` 인스턴스를 반환합니다. 위 예시에서는 속성을 읽는(get) 방법만 정의하고 있습니다. `Attribute` 클래스 생성자에 `get` 인자를 전달해 이를 지정합니다.

<!-- As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the accessor, you may simply access the `first_name` attribute on a model instance: -->
위 코드에서 볼 수 있듯이, accessor에는 컬럼의 원래 값이 전달되어 값의 조작 및 반환이 가능합니다. accessor의 값을 사용하려면, 모델 인스턴스의 `first_name` 속성에 직접 접근하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이렇게 가공된(computed) 값을 모델의 배열/JSON 표현에 포함하고 싶으면, [you will need to append them](/docs/11.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
<!-- #### Building Value Objects From Multiple Attributes -->
#### Building Value Objects From Multiple Attributes

<!-- Sometimes your accessor may need to transform multiple model attributes into a single "value object". To do so, your `get` closure may accept a second argument of `$attributes`, which will be automatically supplied to the closure and will contain an array of all of the model's current attributes: -->
때로는 accessor에서 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 수 있습니다. 이를 위해, `get` 클로저에 두 번째 인자 `$attributes`를 지정할 수 있습니다. 이 인자는 모델의 현재 모든 속성 배열이 자동으로 전달됩니다.

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
accessor에서 값 객체(value object)를 반환하면, 해당 객체의 값이 변경되는 경우 모델이 저장되기 전 자동으로 변경된 내용이 동기화됩니다. 이는 Eloquent가 accessor가 반환한 객체 인스턴스를 재사용(캐싱)하기 때문에 가능합니다. 같은 accessor에 여러 번 접근해도 항상 동일 인스턴스를 반환받습니다.

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

<!-- However, you may sometimes wish to enable caching for primitive values like strings and booleans, particularly if they are computationally intensive. To accomplish this, you may invoke the `shouldCache` method when defining your accessor: -->
하지만 문자열, 불리언 등 기본값(primitive value)에 대해서도, 복잡한 연산이 필요한 경우 캐싱을 활성화하고 싶을 수 있습니다. 이럴 때는 accessor 정의 시 `shouldCache` 메서드를 호출하면 됩니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

<!-- If you would like to disable the object caching behavior of attributes, you may invoke the `withoutObjectCaching` method when defining the attribute: -->
반대로, 객체 인스턴스 캐싱을 비활성화하려면 accessor 정의 시 `withoutObjectCaching` 메서드를 사용할 수 있습니다.

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
변조자(mutator)는 Eloquent 속성에 값을 쓸 때 자동으로 변환해주는 메서드입니다. 변조자를 정의하려면, 속성 정의 시 `set` 인자를 사용하면 됩니다. 아래는 `first_name` 속성에 변조자를 정의한 예시입니다. 이 변조자는 모델의 `first_name` 속성에 값을 대입할 때마다 자동으로 호출됩니다.

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
변조자 클로저는 대입하려는 값을 인자로 받아, 가공한 값을 반환하면 됩니다. 이 변조자를 사용하려면, Eloquent 모델에서 단순히 `first_name` 속성에 값을 할당하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

<!-- In this example, the `set` callback will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its resulting value in the model's internal `$attributes` array. -->
위 예시에서는 `set` 콜백이 `Sally` 값을 받아, `strtolower` 함수를 적용한 값을 모델의 내부 `$attributes` 배열에 저장하게 됩니다.

<a name="mutating-multiple-attributes"></a>
<!-- #### Mutating Multiple Attributes -->
#### Mutating Multiple Attributes

<!-- Sometimes your mutator may need to set multiple attributes on the underlying model. To do so, you may return an array from the `set` closure. Each key in the array should correspond with an underlying attribute / database column associated with the model: -->
경우에 따라 변조자에서 여러 속성을 한 번에 변경해야 할 수 있습니다. 이럴 때는, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델의 실제 속성/데이터베이스 컬럼명과 일치해야 합니다.

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

<!-- Attribute casting provides functionality similar to accessors and mutators without requiring you to define any additional methods on your model. Instead, your model's `casts` method provides a convenient way of converting attributes to common data types. -->
attribute casting은 accessor 및 변조자와 유사한 기능을 제공하지만, 모델에 별도의 메서드를 정의할 필요 없이 간단히 속성을 원하는 데이터 타입으로 변환할 수 있습니다. 모델의 `casts` 메서드를 사용하면 데이터를 쉽게 변환할 수 있습니다.

<!-- The `casts` method should return an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are: -->
`casts` 메서드는 casting할 속성명을 키, 변환할 타입을 값으로 갖는 배열을 반환해야 합니다. 지원되는 casting 타입은 다음과 같습니다.

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
attribute casting 예제를 살펴보겠습니다. 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언 값으로 변환해봅니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'is_admin' => 'boolean',
        ];
    }
}
```

<!-- After defining the cast, the `is_admin` attribute will always be cast to a boolean when you access it, even if the underlying value is stored in the database as an integer: -->
이렇게 casting을 정의하면, 데이터베이스에 저장된 값이 정수여도 Eloquent에서 `is_admin` 속성을 읽을 때마다 항상 불리언 타입으로 변환됩니다.

```
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

<!-- If you need to add a new, temporary cast at runtime, you may use the `mergeCasts` method. These cast definitions will be added to any of the casts already defined on the model: -->
런타임에 새로운 임시 casting을 추가해야 할 때는, `mergeCasts` 메서드를 사용할 수 있습니다. 이 메서드로 추가한 casting 정보는 기존에 모델에 정의된 casting과 합쳐집니다.

```
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 casting되지 않습니다. 또한, 관계명과 동일한 이름의 속성에 cast를 정의하거나, 모델 기본키에 cast를 지정해서는 안 됩니다.

<a name="stringable-casting"></a>
<!-- #### Stringable Casting -->
#### Stringable Casting

<!-- You may use the `Illuminate\Database\Eloquent\Casts\AsStringable` cast class to cast a model attribute to a [fluent `Illuminate\Support\Stringable` object](/docs/11.x/strings#fluent-strings-method-list): -->
모델 속성을 [fluent `Illuminate\Support\Stringable` object](/docs/11.x/strings#fluent-strings-method-list)로 변환하려면, `Illuminate\Database\Eloquent\Casts\AsStringable` cast 클래스를 사용할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'directory' => AsStringable::class,
        ];
    }
}
```

<a name="array-and-json-casting"></a>
<!-- ### Array and JSON Casting -->
### Array and JSON Casting

<!-- The `array` cast is particularly useful when working with columns that are stored as serialized JSON. For example, if your database has a `JSON` or `TEXT` field type that contains serialized JSON, adding the `array` cast to that attribute will automatically deserialize the attribute to a PHP array when you access it on your Eloquent model: -->
`array` casting은 직렬화된(serialized) JSON 형태로 저장된 데이터에 특히 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 타입 컬럼에 직렬화된 JSON이 저장되어 있다면, 해당 속성에 단순히 `array` casting을 지정하면 모델에서 해당 속성에 접근할 때 자동으로 PHP 배열로 변환됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => 'array',
        ];
    }
}
```

<!-- Once the cast is defined, you may access the `options` attribute and it will automatically be deserialized from JSON into a PHP array. When you set the value of the `options` attribute, the given array will automatically be serialized back into JSON for storage: -->
casting을 지정하면, `options` 속성에 접근할 때 자동으로 JSON이 PHP 배열로 변환됩니다. 반대로 `options` 속성에 배열을 할당하면 자동으로 JSON으로 직렬화되어 저장됩니다.

```
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

<!-- To update a single field of a JSON attribute with a more terse syntax, you may [make the attribute mass assignable](/docs/11.x/eloquent#mass-assignment-json-columns) and use the `->` operator when calling the `update` method: -->
JSON 속성의 특정 필드만 간결하게 업데이트하려면, [make the attribute mass assignable](/docs/11.x/eloquent#mass-assignment-json-columns) `update` 메서드에서 `->` 연산자를 사용할 수 있습니다.

```
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
<!-- #### Array Object and Collection Casting -->
#### Array Object and Collection Casting

<!-- Although the standard `array` cast is sufficient for many applications, it does have some disadvantages. Since the `array` cast returns a primitive type, it is not possible to mutate an offset of the array directly. For example, the following code will trigger a PHP error: -->
일반적인 `array` casting은 많은 경우에 충분하지만, 몇 가지 단점이 있습니다. `array` casting은 프리미티브 타입을 반환하기 때문에, 배열 오프셋(offset) 값을 직접 수정할 수 없습니다. 예를 들어, 아래 코드는 PHP 에러를 발생시킬 수 있습니다.

```
$user = User::find(1);

$user->options['key'] = $value;
```

<!-- To solve this, Laravel offers an `AsArrayObject` cast that casts your JSON attribute to an [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) class. This feature is implemented using Laravel's [custom cast](#custom-casts) implementation, which allows Laravel to intelligently cache and transform the mutated object such that individual offsets may be modified without triggering a PHP error. To use the `AsArrayObject` cast, simply assign it to an attribute: -->
이 문제를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 변환하는 `AsArrayObject` cast를 제공합니다. 이 기능은 Laravel의 [custom cast](#custom-casts) 구현을 활용하여, Laravel이 변형된 객체를 지능적으로 캐시 및 변환하므로 PHP 오류를 발생시키지 않고 개별 오프셋을 변경할 수 있습니다. `AsArrayObject` cast를 사용하려면, 다음과 같이 해당 속성에 할당하기만 하면 됩니다.

```
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsArrayObject::class,
    ];
}
```

<!-- Similarly, Laravel offers an `AsCollection` cast that casts your JSON attribute to a Laravel [Collection](/docs/11.x/collections) instance: -->
비슷하게, JSON 속성을 Laravel의 [Collection](/docs/11.x/collections) 인스턴스로 변환해주는 `AsCollection` cast도 제공됩니다.

```
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::class,
    ];
}
```

<!-- If you would like the `AsCollection` cast to instantiate a custom collection class instead of Laravel's base collection class, you may provide the collection class name as a cast argument: -->
`AsCollection` cast에 Laravel 기본 컬렉션 클래스가 아닌 원하는 커스텀 컬렉션 클래스를 사용하고 싶다면, cast 인자로 해당 클래스명을 전달하면 됩니다.

```
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::using(OptionCollection::class),
    ];
}
```

<a name="date-casting"></a>
<!-- ### Date Casting -->
### Date Casting

<!-- By default, Eloquent will cast the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which extends the PHP `DateTime` class and provides an assortment of helpful methods. You may cast additional date attributes by defining additional date casts within your model's `casts` method. Typically, dates should be cast using the `datetime` or `immutable_datetime` cast types. -->
Eloquent는 기본적으로 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 변환합니다. Carbon은 PHP의 `DateTime` 클래스를 확장해 다양한 편리한 메서드를 제공합니다. 추가적인 날짜 속성도 모델의 `casts` 메서드에서 직접 지정해 casting할 수 있습니다. 보통 날짜 관련 속성은 `datetime` 또는 `immutable_datetime` 타입으로 casting합니다.

<!-- When defining a `date` or `datetime` cast, you may also specify the date's format. This format will be used when the [model is serialized to an array or JSON](/docs/11.x/eloquent-serialization): -->
`date` 또는 `datetime` casting을 정의할 때, 날짜 형식(format)을 함께 지정할 수도 있습니다. 이 형식은 [model is serialized to an array or JSON](/docs/11.x/eloquent-serialization) 사용됩니다.

```
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'created_at' => 'datetime:Y-m-d',
    ];
}
```

<!-- When a column is cast as a date, you may set the corresponding model attribute value to a UNIX timestamp, date string (`Y-m-d`), date-time string, or a `DateTime` / `Carbon` instance. The date's value will be correctly converted and stored in your database. -->
속성이 날짜로 casting된 경우, 해당 모델 속성 값에 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 지정할 수 있습니다. 입력값이 자동으로 올바른 형식으로 변환되어 데이터베이스에 저장됩니다.

<!-- You may customize the default serialization format for all of your model's dates by defining a `serializeDate` method on your model. This method does not affect how your dates are formatted for storage in the database: -->
모델의 모든 날짜 필드 직렬화 기본 형식을 바꾸고 싶다면, `serializeDate` 메서드를 모델에 정의할 수 있습니다. 이 메서드는 데이터베이스에 실제로 저장되는 값의 형식에는 영향을 주지 않습니다.

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
실제 데이터베이스에 날짜를 저장할 때 사용할 형식을 지정하려면, 모델에 `$dateFormat` 속성을 정의해야 합니다.

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
기본적으로 `date`와 `datetime` cast는 애플리케이션의 `timezone` 설정과 관계없이 항상 UTC ISO-8601 날짜 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화합니다. 이 직렬화 포맷과 UTC 타임존을 모델의 날짜 처리 기본값으로 사용하는 것을 강력히 권장하며, 애플리케이션의 `timezone` 구성 옵션을 기본값인 `UTC`에서 변경하지 않는 것이 좋습니다. 일관되게 UTC를 사용하면 PHP와 JavaScript 등 다양한 라이브러리와의 호환성이 극대화됩니다.

<!-- If a custom format is applied to the `date` or `datetime` cast, such as `datetime:Y-m-d H:i:s`, the inner timezone of the Carbon instance will be used during date serialization. Typically, this will be the timezone specified in your application's `timezone` configuration option. However, it's important to note that `timestamp` columns such as `created_at` and `updated_at` are exempt from this behavior and are always formatted in UTC, regardless of the application's timezone setting. -->
만약 `date` 또는 `datetime` cast에 `datetime:Y-m-d H:i:s`와 같이 커스텀 포맷을 지정했다면, 직렬화 시 Carbon 인스턴스의 내부 타임존이 사용됩니다. 일반적으로 이 타임존은 애플리케이션의 `timezone` 설정을 따라갑니다. 단, `created_at`이나 `updated_at`과 같은 `timestamp` 컬럼은 이 특성의 예외로, 애플리케이션 타임존 설정과 관계없이 항상 UTC로 포맷됩니다.

<a name="enum-casting"></a>
<!-- ### Enum Casting -->
### Enum Casting

<!-- Eloquent also allows you to cast your attribute values to PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `casts` method: -->
Eloquent는 속성 값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)으로 casting하는 기능도 제공합니다. 이를 위해, 모델의 `casts` 메서드에 속성과 enum을 지정해주면 됩니다.

```
use App\Enums\ServerStatus;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'status' => ServerStatus::class,
    ];
}
```

<!-- Once you have defined the cast on your model, the specified attribute will be automatically cast to and from an enum when you interact with the attribute: -->
이렇게 casting을 정의하면, 해당 속성에 접근하거나 값을 저장하는 과정에서 자동으로 enum 객체로 변환됩니다.

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
한 컬럼에 여러 개의 enum 값을 배열로 저장해야 하는 경우도 있습니다. 이럴 때는 Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` cast를 사용할 수 있습니다.

```
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'statuses' => AsEnumCollection::of(ServerStatus::class),
    ];
}
```

<a name="encrypted-casting"></a>
<!-- ### Encrypted Casting -->
### Encrypted Casting

<!-- The `encrypted` cast will encrypt a model's attribute value using Laravel's built-in [encryption](/docs/11.x/encryption) features. In addition, the `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, and `AsEncryptedCollection` casts work like their unencrypted counterparts; however, as you might expect, the underlying value is encrypted when stored in your database. -->
`encrypted` cast는 Laravel 내장 [encryption](/docs/11.x/encryption)을 이용해 모델 속성 값을 암호화/복호화합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 역시 각각 평문 버전과 동일하게 동작하지만 기본적으로 데이터베이스에 저장할 때 암호화됩니다.

<!-- As the final length of the encrypted text is not predictable and is longer than its plain text counterpart, make sure the associated database column is of `TEXT` type or larger. In addition, since the values are encrypted in the database, you will not be able to query or search encrypted attribute values. -->
암호화된 텍스트의 길이는 예측할 수 없고 평문보다 훨씬 길어질 수 있으므로, 해당 컬럼은 `TEXT` 타입 또는 더 큰 타입이어야 합니다. 또한 값이 암호화되어 저장되므로, 데이터베이스에서 직접 쿼리하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
<!-- #### Key Rotation -->
#### Key Rotation

<!-- As you may know, Laravel encrypts strings using the `key` configuration value specified in your application's `app` configuration file. Typically, this value corresponds to the value of the `APP_KEY` environment variable. If you need to rotate your application's encryption key, you will need to manually re-encrypt your encrypted attributes using the new key. -->
Laravel은 애플리케이션의 `app` 설정 파일에 지정된 `key` 설정 값으로 문자열을 암호화합니다. 일반적으로 이 값은 `APP_KEY` 환경변수의 값에 해당합니다. 앱의 암호화 키를 변경(교체)해야 한다면, 기존 암호화된 속성 데이터를 새 키로 수동으로 다시 암호화해야 합니다.

<a name="query-time-casting"></a>
<!-- ### Query Time Casting -->
### Query Time Casting

<!-- Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query: -->
종종 쿼리를 실행할 때, 직접 셀렉트한(raw) 값을 즉석에서 casting해야 할 때가 있습니다. 아래와 같은 쿼리를 예로 들어보겠습니다.

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
위 쿼리에서 결과로 나오는 `last_posted_at` 속성은 단순 문자열입니다. 쿼리 실행 시점에 이 속성에 `datetime` casting을 적용할 수 있다면 훨씬 좋을 것입니다. 다행히, `withCasts` 메서드를 사용하면 이를 쉽게 실현할 수 있습니다.

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
Laravel에는 다양한 내장 cast 타입이 제공되지만, 때로는 직접 커스텀 cast 타입을 정의해야 할 수도 있습니다. cast를 생성하려면 `make:cast` 아티즌 명령어를 실행합니다. 새롭게 생성된 cast 클래스는 `app/Casts` 디렉터리에 위치하게 됩니다.

```shell
php artisan make:cast Json
```

<!-- All custom cast classes implement the `CastsAttributes` interface. Classes that implement this interface must define a `get` and `set` method. The `get` method is responsible for transforming a raw value from the database into a cast value, while the `set` method should transform a cast value into a raw value that can be stored in the database. As an example, we will re-implement the built-in `json` cast type as a custom cast type: -->
모든 커스텀 cast 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현하는 클래스에서는 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스에서 가져온 원시 값을 cast 값으로 변환하는 역할을 하며, `set` 메서드는 cast 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환합니다. 예를 들어, 내장된 `json` cast 타입을 커스텀 cast 타입으로 재구현해보겠습니다.

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
커스텀 cast 타입을 정의한 후에는, 해당 클래스명을 이용해 모델 속성에 cast를 지정할 수 있습니다.

```
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => Json::class,
        ];
    }
}
```

<a name="value-object-casting"></a>
<!-- ### Value Object Casting -->
### Value Object Casting

<!-- You are not limited to casting values to primitive types. You may also cast values to objects. Defining custom casts that cast values to objects is very similar to casting to primitive types; however, the `set` method should return an array of key / value pairs that will be used to set raw, storable values on the model. -->
값을 기본 데이터 타입뿐 아니라 객체로도 casting할 수 있습니다. 값을 객체로 casting하는 커스텀 cast를 정의하는 방법은 기본 타입을 casting하는 방법과 거의 비슷하지만, `set` 메서드는 모델에 저장될 원시 값을 키/값 쌍의 배열로 반환해야 합니다.

<!-- As an example, we will define a custom cast class that casts multiple model values into a single `Address` value object. We will assume the `Address` value has two public properties: `lineOne` and `lineTwo`: -->
예를 들어, 여러 모델 값을 하나의 `Address` 값 객체로 casting하는 커스텀 cast 클래스를 정의해보겠습니다. 여기서는 `Address` 값 객체가 두 개의 public 속성 `lineOne`과 `lineTwo`를 갖고 있다고 가정합니다.

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
값 객체로 casting할 경우, 값 객체에서 속성이 변경되더라도 모델이 저장되기 전에 자동으로 모델에 반영됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체가 포함된 Eloquent 모델을 JSON이나 배열로 직렬화(serialize)할 계획이 있다면, 해당 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하는 것이 좋습니다.

<a name="value-object-caching"></a>
<!-- #### Value Object Caching -->
#### Value Object Caching

<!-- When attributes that are cast to value objects are resolved, they are cached by Eloquent. Therefore, the same object instance will be returned if the attribute is accessed again. -->
값 객체로 casting된 속성이 resolve(해결)될 때, Eloquent에서 이 객체를 캐시합니다. 따라서 동일한 속성에 다시 접근할 경우 항상 같은 객체 인스턴스가 반환됩니다.

<!-- If you would like to disable the object caching behavior of custom cast classes, you may declare a public `withoutObjectCaching` property on your custom cast class: -->
커스텀 cast 클래스의 객체 캐싱 동작을 비활성화하고 싶다면, 커스텀 cast 클래스에 public 속성인 `withoutObjectCaching`을 선언하면 됩니다.

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
Eloquent 모델을 `toArray` 혹은 `toJson` 메서드로 배열이나 JSON으로 변환할 때, 커스텀 cast 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현한다면, 해당 객체도 직렬화되어 출력됩니다. 하지만, 외부 라이브러리에서 제공하는 값 객체를 사용할 경우 이 인터페이스를 직접 추가할 수 없을 수도 있습니다.

<!-- Therefore, you may specify that your custom cast class will be responsible for serializing the value object. To do so, your custom cast class should implement the `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` interface. This interface states that your class should contain a `serialize` method which should return the serialized form of your value object: -->
이럴 때는 커스텀 cast 클래스에서 값 객체의 직렬화를 직접 처리하도록 지정할 수 있습니다. 이를 위해, 커스텀 cast 클래스에서 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현합니다. 이 인터페이스는 클래스가 `serialize` 메서드를 포함해야 함을 의미하며, 이 메서드는 값 객체의 직렬화된 결과를 반환해야 합니다.

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
가끔은 모델에 값을 저장할 때에만 변환 처리를 하고, 모델에서 값을 조회할 때는 아무런 처리를 하지 않는 커스텀 cast가 필요할 수 있습니다.

<!-- Inbound only custom casts should implement the `CastsInboundAttributes` interface, which only requires a `set` method to be defined. The `make:cast` Artisan command may be invoked with the `--inbound` option to generate an inbound only cast class: -->
인바운드 전용 커스텀 cast는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 오직 `set` 메서드만 정의하면 됩니다. 인바운드 전용 cast 클래스를 생성하려면 `make:cast` 아티즌 명령어 사용 시 `--inbound` 옵션을 지정하면 됩니다.

```shell
php artisan make:cast Hash --inbound
```

<!-- A classic example of an inbound only cast is a "hashing" cast. For example, we may define a cast that hashes inbound values via a given algorithm: -->
인바운드 전용 cast의 대표적인 예시는 "해시" cast입니다. 예를 들어, 전달받은 값을 지정한 알고리즘으로 해싱하는 cast를 만들 수 있습니다.

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
모델에 커스텀 cast를 지정할 때, 클래스명 뒤에 `:` 문자로 구분하여 파라미터(여러 개라면 쉼표로 구분)를 전달할 수 있습니다. 이렇게 지정한 파라미터는 cast 클래스의 생성자로 전달됩니다.

```
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'secret' => Hash::class.':sha256',
    ];
}
```

<a name="castables"></a>
<!-- ### Castables -->
### Castables

<!-- You may want to allow your application's value objects to define their own custom cast classes. Instead of attaching the custom cast class to your model, you may alternatively attach a value object class that implements the `Illuminate\Contracts\Database\Eloquent\Castable` interface: -->
애플리케이션의 값 객체가 스스로 커스텀 cast 클래스를 지정하도록 하고 싶을 때가 있습니다. 이럴 때는 커스텀 cast 클래스를 모델에 직접 지정하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 지정할 수 있습니다.

```
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

<!-- Objects that implement the `Castable` interface must define a `castUsing` method that returns the class name of the custom caster class that is responsible for casting to and from the `Castable` class: -->
`Castable` 인터페이스를 구현하는 객체는 반드시 `castUsing` 메서드를 정의해야 하며, 이 메서드는 `Castable` 클래스로의 casting 및 역casting을 담당하는 커스텀 caster 클래스의 클래스명을 반환해야 합니다.

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

<!-- When using `Castable` classes, you may still provide arguments in the `casts` method definition. The arguments will be passed to the `castUsing` method: -->
`Castable` 클래스를 사용할 때도, `casts` 메서드 정의에서 파라미터를 전달할 수 있습니다. 이 파라미터들은 `castUsing` 메서드로 전달됩니다.

```
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class.':argument',
    ];
}
```

<a name="anonymous-cast-classes"></a>
<!-- #### Castables & Anonymous Cast Classes -->
#### Castables & Anonymous Cast Classes

<!-- By combining "castables" with PHP's [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php), you may define a value object and its casting logic as a single castable object. To accomplish this, return an anonymous class from your value object's `castUsing` method. The anonymous class should implement the `CastsAttributes` interface: -->
"Castable"과 PHP의 [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php)를 조합하면, 값 객체의 casting 로직을 하나의 Castable 객체로 정의할 수 있습니다. 이를 실현하려면 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 익명 클래스는 반드시 `CastsAttributes` 인터페이스를 구현해야 합니다.

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
