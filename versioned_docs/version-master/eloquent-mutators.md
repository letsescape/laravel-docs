<!-- # Eloquent: Mutators & Casting -->
# Eloquent: Mutators & Casting

- [Introduction](#introduction)
- [Accessors and Mutators](#accessors-and-mutators)
    - [Defining an Accessor](#defining-an-accessor)
    - [Defining a Mutator](#defining-a-mutator)
- [Attribute Casting](#attribute-casting)
    - [Array and JSON Casting](#array-and-json-casting)
    - [Binary Casting](#binary-casting)
    - [Date Casting](#date-casting)
    - [Enum Casting](#enum-casting)
    - [Encrypted Casting](#encrypted-casting)
    - [Query Time Casting](#query-time-casting)
- [Custom Casts](#custom-casts)
    - [Value Object Casting](#value-object-casting)
    - [Array / JSON Serialization](#array-json-serialization)
    - [Inbound Casting](#inbound-casting)
    - [Cast Parameters](#cast-parameters)
    - [Comparing Cast Values](#comparing-cast-values)
    - [Castables](#castables)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/master/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model. -->
accessor, mutator, attribute casting을 사용하면 모델 인스턴스에서 Eloquent 속성 값을 가져오거나 설정할 때 그 값을 변환할 수 있습니다. 예를 들어, 어떤 값을 데이터베이스에 저장할 때 [Laravel encrypter](/docs/master/encryption)를 사용해 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화하고 싶을 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
<!-- ## Accessors and Mutators -->
## Accessors and Mutators

<a name="defining-an-accessor"></a>
<!-- ### Defining an Accessor -->
### Defining an Accessor

<!-- An accessor transforms an Eloquent attribute value when it is accessed. To define an accessor, create a protected method on your model to represent the accessible attribute. This method name should correspond to the "camel case" representation of the true underlying model attribute / database column when applicable. -->
accessor는 Eloquent 속성 값에 접근할 때 그 값을 변환합니다. accessor를 정의하려면 모델에서 접근 가능한 속성을 나타내는 protected 메서드를 생성합니다. 적용 가능한 경우, 이 메서드 이름은 실제 기반 모델 속성 / 데이터베이스 컬럼의 "camel case" 표현과 일치해야 합니다.

<!-- In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute. All attribute accessor / mutator methods must declare a return type-hint of `Illuminate\Database\Eloquent\Casts\Attribute`: -->
이 예제에서는 `first_name` 속성에 대한 accessor를 정의합니다. `first_name` 속성 값을 가져오려고 할 때 Eloquent가 이 accessor를 자동으로 호출합니다. 모든 속성 accessor / mutator 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 반환 타입 힌트를 선언해야 합니다.

```php
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
모든 accessor 메서드는 속성에 어떻게 접근할지, 그리고 선택적으로 어떻게 변경할지를 정의하는 `Attribute` 인스턴스를 반환합니다. 이 예제에서는 속성에 접근하는 방법만 정의하고 있습니다. 이를 위해 `Attribute` 클래스 생성자에 `get` 인수를 전달합니다.

<!-- As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the accessor, you may simply access the `first_name` attribute on a model instance: -->
보시다시피 컬럼의 원래 값이 accessor로 전달되므로, 값을 조작한 뒤 반환할 수 있습니다. accessor의 값에 접근하려면 모델 인스턴스에서 `first_name` 속성에 그대로 접근하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이렇게 계산된 값을 모델의 배열 / JSON 표현에 추가하고 싶다면 [you will need to append them](/docs/master/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
<!-- #### Building Value Objects From Multiple Attributes -->
#### Building Value Objects From Multiple Attributes

<!-- Sometimes your accessor may need to transform multiple model attributes into a single "value object". To do so, your `get` closure may accept a second argument of `$attributes`, which will be automatically supplied to the closure and will contain an array of all of the model's current attributes: -->
때로는 accessor가 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 수 있습니다. 이를 위해 `get` 클로저는 두 번째 인수로 `$attributes`를 받을 수 있습니다. 이 값은 클로저에 자동으로 전달되며, 모델의 현재 모든 속성을 담은 배열을 포함합니다.

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
accessor에서 값 객체를 반환할 때, 값 객체에 적용한 변경 사항은 모델이 저장되기 전에 자동으로 모델에 다시 동기화됩니다. 이는 Eloquent가 accessor에서 반환된 인스턴스를 보관해, accessor가 호출될 때마다 같은 인스턴스를 반환할 수 있기 때문에 가능합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

<!-- However, you may sometimes wish to enable caching for primitive values like strings and booleans, particularly if they are computationally intensive. To accomplish this, you may invoke the `shouldCache` method when defining your accessor: -->
하지만 문자열이나 불리언 같은 원시 값에 대해서도 캐싱을 활성화하고 싶을 때가 있습니다. 특히 계산 비용이 큰 경우에 유용합니다. 이를 위해 accessor를 정의할 때 `shouldCache` 메서드를 호출할 수 있습니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

<!-- If you would like to disable the object caching behavior of attributes, you may invoke the `withoutObjectCaching` method when defining the attribute: -->
속성의 객체 캐싱 동작을 비활성화하고 싶다면, 속성을 정의할 때 `withoutObjectCaching` 메서드를 호출할 수 있습니다.

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
mutator는 Eloquent 속성 값이 설정될 때 그 값을 변환합니다. mutator를 정의하려면 속성을 정의할 때 `set` 인수를 제공하면 됩니다. `first_name` 속성에 대한 mutator를 정의해 보겠습니다. 이 mutator는 모델에서 `first_name` 속성 값을 설정하려고 할 때 자동으로 호출됩니다.

```php
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
mutator 클로저는 속성에 설정되는 값을 전달받습니다. 따라서 해당 값을 조작한 뒤 조작된 값을 반환할 수 있습니다. 이 mutator를 사용하려면 Eloquent 모델에서 `first_name` 속성을 설정하기만 하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

<!-- In this example, the `set` callback will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its resulting value in the model's internal `$attributes` array. -->
이 예제에서 `set` 콜백은 `Sally` 값을 인수로 호출됩니다. 그러면 mutator는 이름에 `strtolower` 함수를 적용하고, 그 결과 값을 모델 내부의 `$attributes` 배열에 설정합니다.

<a name="mutating-multiple-attributes"></a>
<!-- #### Mutating Multiple Attributes -->
#### Mutating Multiple Attributes

<!-- Sometimes your mutator may need to set multiple attributes on the underlying model. To do so, you may return an array from the `set` closure. Each key in the array should correspond with an underlying attribute / database column associated with the model: -->
때로는 mutator가 기반 모델의 여러 속성을 설정해야 할 수 있습니다. 이를 위해 `set` 클로저에서 배열을 반환할 수 있습니다. 배열의 각 키는 모델과 연결된 기반 속성 / 데이터베이스 컬럼과 일치해야 합니다.

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
attribute casting은 모델에 추가 메서드를 정의하지 않아도 accessor와 mutator와 비슷한 기능을 제공합니다. 대신 모델의 `casts` 메서드는 속성을 일반적인 데이터 타입으로 변환하는 편리한 방법을 제공합니다.

<!-- The `casts` method should return an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are: -->
`casts` 메서드는 배열을 반환해야 하며, 키는 casting할 속성 이름이고 값은 해당 컬럼을 casting하려는 타입입니다. 지원되는 cast 타입은 다음과 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `array`
- `AsFluent::class`
- `AsStringable::class`
- `AsUri::class`
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
- `AsFluent::class`
- `AsStringable::class`
- `AsUri::class`
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
attribute casting을 보여주기 위해, 데이터베이스에는 정수(`0` 또는 `1`)로 저장되는 `is_admin` 속성을 불리언 값으로 casting해 보겠습니다.

```php
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
cast를 정의한 뒤에는 기반 값이 데이터베이스에 정수로 저장되어 있더라도, `is_admin` 속성에 접근할 때 항상 불리언으로 casting됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

<!-- If you need to add a new, temporary cast at runtime, you may use the `mergeCasts` method. These cast definitions will be added to any of the casts already defined on the model: -->
런타임에 새로운 임시 cast를 추가해야 한다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 cast 정의는 모델에 이미 정의된 cast에 추가됩니다.

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null`인 속성은 casting되지 않습니다. 또한 연관관계와 같은 이름을 가진 cast(또는 속성)를 정의해서는 안 되며, 모델의 기본 키에 cast를 할당해서도 안 됩니다.

<a name="stringable-casting"></a>
<!-- #### Stringable Casting -->
#### Stringable Casting

<!-- You may use the `Illuminate\Database\Eloquent\Casts\AsStringable` cast class to cast a model attribute to a [fluent Illuminate\Support\Stringable object](/docs/master/strings#fluent-strings-method-list): -->
`Illuminate\Database\Eloquent\Casts\AsStringable` cast 클래스를 사용하면 모델 속성을 [fluent Illuminate\Support\Stringable object](/docs/master/strings#fluent-strings-method-list)로 casting할 수 있습니다.

```php
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
`array` cast는 직렬화된 JSON으로 저장되는 컬럼을 다룰 때 특히 유용합니다. 예를 들어 데이터베이스에 직렬화된 JSON을 포함하는 `JSON` 또는 `TEXT` 필드 타입이 있다면, 해당 속성에 `array` cast를 추가했을 때 Eloquent 모델에서 접근하면 자동으로 PHP 배열로 역직렬화됩니다.

```php
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
cast가 정의되면 `options` 속성에 접근할 수 있으며, 이 속성은 JSON에서 PHP 배열로 자동 역직렬화됩니다. `options` 속성 값을 설정할 때는 전달한 배열이 저장을 위해 다시 JSON으로 자동 직렬화됩니다.

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

<!-- To update a single field of a JSON attribute with a more terse syntax, you may [make the attribute mass assignable](/docs/master/eloquent#mass-assignment-json-columns) and use the `->` operator when calling the `update` method: -->
JSON 속성의 단일 필드를 더 간결한 문법으로 업데이트하려면, [make the attribute mass assignable](/docs/master/eloquent#mass-assignment-json-columns) `update` 메서드를 호출할 때 `->` 연산자를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
<!-- #### JSON and Unicode -->
#### JSON and Unicode

<!-- If you would like to store an array attribute as JSON with unescaped Unicode characters, you may use the `json:unicode` cast: -->
배열 속성을 이스케이프되지 않은 Unicode 문자로 JSON에 저장하고 싶다면 `json:unicode` cast를 사용할 수 있습니다.

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => 'json:unicode',
    ];
}
```

<a name="array-object-and-collection-casting"></a>
<!-- #### Array Object and Collection Casting -->
#### Array Object and Collection Casting

<!-- Although the standard `array` cast is sufficient for many applications, it does have some disadvantages. Since the `array` cast returns a primitive type, it is not possible to mutate an offset of the array directly. For example, the following code will trigger a PHP error: -->
표준 `array` cast는 많은 애플리케이션에서 충분하지만 몇 가지 단점도 있습니다. `array` cast는 원시 타입을 반환하므로 배열의 오프셋을 직접 변경할 수 없습니다. 예를 들어 다음 코드는 PHP 오류를 발생시킵니다.

```php
$user = User::find(1);

$user->options['key'] = $value;
```
<!-- To solve this, Laravel offers an `AsArrayObject` cast that casts your JSON attribute to an [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) class. This feature is implemented using Laravel's [custom cast](#custom-casts) implementation, which allows Laravel to intelligently cache and transform the mutated object such that individual offsets may be modified without triggering a PHP error. To use the `AsArrayObject` cast, simply assign it to an attribute: -->
이를 해결하기 위해 Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 casting하는 `AsArrayObject` cast를 제공합니다. 이 기능은 Laravel의 [custom cast](#custom-casts) 구현을 사용하여 만들어졌으며, Laravel이 변경된 객체를 지능적으로 캐시하고 변환할 수 있게 해 줍니다. 따라서 개별 오프셋을 수정해도 PHP 오류가 발생하지 않습니다. `AsArrayObject` cast를 사용하려면 속성에 할당하기만 하면 됩니다.

```php
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

<!-- Similarly, Laravel offers an `AsCollection` cast that casts your JSON attribute to a Laravel [Collection](/docs/master/collections) instance: -->
마찬가지로 Laravel은 JSON 속성을 Laravel [Collection](/docs/master/collections) 인스턴스로 casting하는 `AsCollection` cast를 제공합니다.

```php
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
`AsCollection` cast가 Laravel의 기본 컬렉션 클래스 대신 커스텀 컬렉션 클래스를 인스턴스화하도록 하려면, 컬렉션 클래스 이름을 cast 인수로 제공할 수 있습니다.

```php
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

<!-- The `of` method may be used to indicate collection items should be mapped into a given class via the collection's [mapInto method](/docs/master/collections#method-mapinto): -->
`of` 메서드를 사용하면 컬렉션의 [mapInto method](/docs/master/collections#method-mapinto)를 통해 컬렉션 항목을 지정한 클래스로 매핑해야 함을 나타낼 수 있습니다.

```php
use App\ValueObjects\Option;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::of(Option::class)
    ];
}
```

<!-- When mapping collections to objects, the object should implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces to define how their instances should be serialized into the database as JSON: -->
컬렉션을 객체로 매핑할 때, 해당 객체는 인스턴스가 데이터베이스에 JSON으로 직렬화되는 방식을 정의하기 위해 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Support\Arrayable;
use JsonSerializable;

class Option implements Arrayable, JsonSerializable
{
    public string $name;
    public mixed $value;
    public bool $isLocked;

    /**
     * Create a new Option instance.
     */
    public function __construct(array $data)
    {
        $this->name = $data['name'];
        $this->value = $data['value'];
        $this->isLocked = $data['is_locked'];
    }

    /**
     * Get the instance as an array.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'value' => $this->value,
            'is_locked' => $this->isLocked,
        ];
    }

    /**
     * Specify the data which should be serialized to JSON.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function jsonSerialize(): array
    {
        return $this->toArray();
    }
}
```

<a name="binary-casting"></a>
<!-- ### Binary Casting -->
### Binary Casting

<!-- If your Eloquent model has a [binary type](/docs/master/migrations#column-method-binary) `uuid` or `ulid` column in addition to your model's auto-incrementing ID column, you may use the `AsBinary` cast to automatically cast the value to and from its binary representation: -->
Eloquent 모델에 자동 증가 ID 컬럼과 함께 [binary type](/docs/master/migrations#column-method-binary)의 `uuid` 또는 `ulid` 컬럼이 있다면, `AsBinary` cast를 사용하여 값을 바이너리 표현으로 자동 casting하거나 바이너리 표현에서 다시 casting할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Casts\AsBinary;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'uuid' => AsBinary::uuid(),
        'ulid' => AsBinary::ulid(),
    ];
}
```

<!-- Once the cast has been defined on the model, you may set the UUID / ULID attribute value to an object instance or a string. Eloquent will automatically cast the value to its binary representation. When retrieving the attribute's value, you will always receive a plain-text string value: -->
모델에 cast를 정의한 후에는 UUID / ULID 속성값을 객체 인스턴스나 문자열로 설정할 수 있습니다. Eloquent는 해당 값을 자동으로 바이너리 표현으로 casting합니다. 속성값을 조회할 때는 항상 일반 텍스트 문자열 값을 받게 됩니다.

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```

<a name="date-casting"></a>
<!-- ### Date Casting -->
### Date Casting

<!-- By default, Eloquent will cast the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which extends the PHP `DateTime` class and provides an assortment of helpful methods. You may cast additional date attributes by defining additional date casts within your model's `casts` method. Typically, dates should be cast using the `datetime` or `immutable_datetime` cast types. -->
기본적으로 Eloquent는 `created_at` 및 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 casting합니다. Carbon은 PHP의 `DateTime` 클래스를 확장하며 다양한 유용한 메서드를 제공합니다. 모델의 `casts` 메서드 안에 추가 날짜 cast를 정의하여 다른 날짜 속성도 casting할 수 있습니다. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` cast 타입을 사용해 casting해야 합니다.

<!-- When defining a `date` or `datetime` cast, you may also specify the date's format. This format will be used when the [model is serialized to an array or JSON](/docs/master/eloquent-serialization): -->
`date` 또는 `datetime` cast를 정의할 때 날짜 형식도 지정할 수 있습니다. 이 형식은 [model is serialized to an array or JSON](/docs/master/eloquent-serialization) 사용됩니다.

```php
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
컬럼이 날짜로 casting되면, 해당 모델 속성값을 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime` / `Carbon` 인스턴스로 설정할 수 있습니다. 날짜 값은 올바르게 변환되어 데이터베이스에 저장됩니다.

<!-- You may customize the default serialization format for all of your model's dates by defining a `serializeDate` method on your model. This method does not affect how your dates are formatted for storage in the database: -->
모델에 `serializeDate` 메서드를 정의하여 모델의 모든 날짜에 대한 기본 직렬화 형식을 커스터마이징할 수 있습니다. 이 메서드는 데이터베이스 저장 시 날짜가 포맷되는 방식에는 영향을 주지 않습니다.

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<!-- To specify the format that should be used when actually storing a model's dates within your database, you should use the `dateFormat` argument on your model's `Table` attribute: -->
모델의 날짜를 데이터베이스에 실제로 저장할 때 사용할 형식을 지정하려면, 모델의 `Table` 속성에서 `dateFormat` 인수를 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Attributes\Table;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```

<a name="date-casting-and-timezones"></a>
<!-- #### Date Casting, Serialization, and Timezones -->
#### Date Casting, Serialization, and Timezones

<!-- By default, the `date` and `datetime` casts will serialize dates to a UTC ISO-8601 date string (`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`), regardless of the timezone specified in your application's `timezone` configuration option. You are strongly encouraged to always use this serialization format, as well as to store your application's dates in the UTC timezone by not changing your application's `timezone` configuration option from its default `UTC` value. Consistently using the UTC timezone throughout your application will provide the maximum level of interoperability with other date manipulation libraries written in PHP and JavaScript. -->
기본적으로 `date` 및 `datetime` cast는 애플리케이션의 `timezone` 설정 옵션에 지정된 시간대와 관계없이 날짜를 UTC ISO-8601 날짜 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화합니다. 이 직렬화 형식을 항상 사용하는 것이 강력히 권장되며, 애플리케이션의 `timezone` 설정 옵션을 기본값인 `UTC`에서 변경하지 않음으로써 애플리케이션의 날짜를 UTC 시간대로 저장하는 것도 권장됩니다. 애플리케이션 전체에서 UTC 시간대를 일관되게 사용하면 PHP와 JavaScript로 작성된 다른 날짜 조작 라이브러리와의 상호 운용성을 가장 높은 수준으로 확보할 수 있습니다.

<!-- If a custom format is applied to the `date` or `datetime` cast, such as `datetime:Y-m-d H:i:s`, the inner timezone of the Carbon instance will be used during date serialization. Typically, this will be the timezone specified in your application's `timezone` configuration option. However, it's important to note that `timestamp` columns such as `created_at` and `updated_at` are exempt from this behavior and are always formatted in UTC, regardless of the application's timezone setting. -->
`datetime:Y-m-d H:i:s`와 같이 `date` 또는 `datetime` cast에 커스텀 형식이 적용된 경우, 날짜 직렬화 과정에서 Carbon 인스턴스 내부의 시간대가 사용됩니다. 일반적으로 이는 애플리케이션의 `timezone` 설정 옵션에 지정된 시간대입니다. 다만 `created_at` 및 `updated_at` 같은 `timestamp` 컬럼은 이 동작에서 제외되며, 애플리케이션의 시간대 설정과 관계없이 항상 UTC로 포맷된다는 점에 유의해야 합니다.

<a name="enum-casting"></a>
<!-- ### Enum Casting -->
### Enum Casting

<!-- Eloquent also allows you to cast your attribute values to PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `casts` method: -->
Eloquent는 속성값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)로 casting하는 것도 허용합니다. 이를 위해 모델의 `casts` 메서드에 casting하려는 속성과 enum을 지정할 수 있습니다.

```php
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
모델에 cast를 정의하고 나면, 해당 속성과 상호작용할 때 지정된 속성은 자동으로 enum으로 casting되거나 enum에서 다시 casting됩니다.

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
<!-- #### Casting Arrays of Enums -->
#### Casting Arrays of Enums

<!-- Sometimes you may need your model to store an array of enum values within a single column. To accomplish this, you may utilize the `AsEnumArrayObject` or `AsEnumCollection` casts provided by Laravel: -->
때로는 모델이 단일 컬럼 안에 enum 값 배열을 저장해야 할 수 있습니다. 이를 위해 Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` cast를 활용할 수 있습니다.

```php
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

<!-- The `encrypted` cast will encrypt a model's attribute value using Laravel's built-in [encryption](/docs/master/encryption) features. In addition, the `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, and `AsEncryptedCollection` casts work like their unencrypted counterparts; however, as you might expect, the underlying value is encrypted when stored in your database. -->
`encrypted` cast는 Laravel의 내장 [encryption](/docs/master/encryption) 기능을 사용하여 모델의 속성값을 암호화합니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` cast는 암호화되지 않은 대응 항목과 동일하게 동작합니다. 다만 예상할 수 있듯이, 데이터베이스에 저장될 때 내부 값이 암호화됩니다.

<!-- As the final length of the encrypted text is not predictable and is longer than its plain text counterpart, make sure the associated database column is of `TEXT` type or larger. In addition, since the values are encrypted in the database, you will not be able to query or search encrypted attribute values. -->
암호화된 텍스트의 최종 길이는 예측할 수 없고 일반 텍스트보다 길기 때문에, 관련 데이터베이스 컬럼이 `TEXT` 타입 이상인지 확인해야 합니다. 또한 값이 데이터베이스에서 암호화되므로, 암호화된 속성값을 쿼리하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
<!-- #### Key Rotation -->
#### Key Rotation

<!-- As you may know, Laravel encrypts strings using the `key` configuration value specified in your application's `app` configuration file. Typically, this value corresponds to the value of the `APP_KEY` environment variable. If you need to rotate your application's encryption key, you may [gracefully do so](/docs/master/encryption#gracefully-rotating-encryption-keys). -->
알고 있듯이 Laravel은 애플리케이션의 `app` 설정 파일에 지정된 `key` 설정 값을 사용하여 문자열을 암호화합니다. 일반적으로 이 값은 `APP_KEY` 환경 변수의 값에 해당합니다. 애플리케이션의 암호화 키를 교체해야 한다면 [gracefully do so](/docs/master/encryption#gracefully-rotating-encryption-keys).

<a name="query-time-casting"></a>
<!-- ### Query Time Casting -->
### Query Time Casting

<!-- Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query: -->
테이블에서 원시 값을 선택하는 경우처럼, 쿼리를 실행하는 동안 cast를 적용해야 할 때가 있습니다. 예를 들어 다음 쿼리를 살펴보겠습니다.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

<!-- The `last_posted_at` attribute on the results of this query will be a simple string. It would be wonderful if we could apply a `datetime` cast to this attribute when executing the query. Thankfully, we may accomplish this using the `withCasts` method: -->
이 쿼리 결과의 `last_posted_at` 속성은 단순한 문자열입니다. 쿼리를 실행할 때 이 속성에 `datetime` cast를 적용할 수 있다면 좋을 것입니다. 다행히 `withCasts` 메서드를 사용하여 이를 수행할 수 있습니다.

```php
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
Laravel에는 다양하고 유용한 내장 cast 타입이 있습니다. 하지만 때로는 직접 cast 타입을 정의해야 할 수도 있습니다. cast를 만들려면 `make:cast` Artisan 명령어를 실행합니다. 새 cast 클래스는 `app/Casts` 디렉터리에 배치됩니다.

```shell
php artisan make:cast AsJson
```

<!-- All custom cast classes implement the `CastsAttributes` interface. Classes that implement this interface must define a `get` and `set` method. The `get` method is responsible for transforming a raw value from the database into a cast value, while the `set` method should transform a cast value into a raw value that can be stored in the database. As an example, we will re-implement the built-in `json` cast type as a custom cast type: -->
모든 커스텀 cast 클래스는 `CastsAttributes` 인터페이스를 구현합니다. 이 인터페이스를 구현하는 클래스는 `get` 및 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스의 원시 값을 cast된 값으로 변환하는 역할을 하며, `set` 메서드는 cast된 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환해야 합니다. 예제로 내장 `json` cast 타입을 커스텀 cast 타입으로 다시 구현해 보겠습니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class AsJson implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        return json_decode($value, true);
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
        return json_encode($value);
    }
}
```

<!-- Once you have defined a custom cast type, you may attach it to a model attribute using its class name: -->
커스텀 cast 타입을 정의한 후에는 클래스 이름을 사용하여 모델 속성에 연결할 수 있습니다.

```php
<?php

namespace App\Models;

use App\Casts\AsJson;
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
            'options' => AsJson::class,
        ];
    }
}
```

<a name="value-object-casting"></a>
<!-- ### Value Object Casting -->
### Value Object Casting

<!-- You are not limited to casting values to primitive types. You may also cast values to objects. Defining custom casts that cast values to objects is very similar to casting to primitive types; however, if your value object encompasses more than one database column, the `set` method must return an array of key / value pairs that will be used to set raw, storable values on the model. If your value object only affects a single column, you should simply return the storable value. -->
값을 기본 타입으로 casting하는 것에만 제한되지 않습니다. 값을 객체로 casting할 수도 있습니다. 값을 객체로 casting하는 커스텀 cast를 정의하는 방식은 기본 타입으로 casting하는 방식과 매우 비슷합니다. 다만 값 객체가 둘 이상의 데이터베이스 컬럼을 포함하는 경우, `set` 메서드는 모델에 설정될 원시 저장 가능 값으로 사용할 키 / 값 쌍의 배열을 반환해야 합니다. 값 객체가 단일 컬럼에만 영향을 준다면, 저장 가능한 값을 그대로 반환하면 됩니다.

<!-- As an example, we will define a custom cast class that casts multiple model values into a single `Address` value object. We will assume the `Address` value object has two public properties: `lineOne` and `lineTwo`: -->
예제로 여러 모델 값을 하나의 `Address` 값 객체로 casting하는 커스텀 cast 클래스를 정의해 보겠습니다. `Address` 값 객체에는 두 개의 공개 속성인 `lineOne`과 `lineTwo`가 있다고 가정하겠습니다.

```php
<?php

namespace App\Casts;

use App\ValueObjects\Address;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;
use InvalidArgumentException;

class AsAddress implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): Address {
        return new Address(
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
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        if (! $value instanceof Address) {
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
값 객체로 casting할 때, 값 객체에 가한 변경 사항은 모델이 저장되기 전에 자동으로 모델에 다시 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 JSON 또는 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
<!-- #### Value Object Caching -->
#### Value Object Caching

<!-- When attributes that are cast to value objects are resolved, they are cached by Eloquent. Therefore, the same object instance will be returned if the attribute is accessed again. -->
값 객체로 casting된 속성이 해석될 때, Eloquent는 해당 값을 캐시합니다. 따라서 그 속성에 다시 접근하면 동일한 객체 인스턴스가 반환됩니다.

<!-- If you would like to disable the object caching behavior of custom cast classes, you may declare a public `withoutObjectCaching` property on your custom cast class: -->
커스텀 cast 클래스의 객체 캐싱 동작을 비활성화하고 싶다면, 커스텀 cast 클래스에 public `withoutObjectCaching` 속성을 선언할 수 있습니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
<!-- ### Array / JSON Serialization -->
### Array / JSON Serialization

<!-- When an Eloquent model is converted to an array or JSON using the `toArray` and `toJson` methods, your custom cast value objects will typically be serialized as well as long as they implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces. However, when using value objects provided by third-party libraries, you may not have the ability to add these interfaces to the object. -->
Eloquent 모델이 `toArray` 및 `toJson` 메서드를 사용해 배열 또는 JSON으로 변환될 때, 커스텀 cast 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하고 있다면 일반적으로 함께 직렬화됩니다. 하지만 서드파티 라이브러리가 제공하는 값 객체를 사용할 때는 해당 인터페이스를 객체에 추가할 수 없을 수도 있습니다.

<!-- Therefore, you may specify that your custom cast class will be responsible for serializing the value object. To do so, your custom cast class should implement the `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` interface. This interface states that your class should contain a `serialize` method which should return the serialized form of your value object: -->
따라서 커스텀 cast 클래스가 값 객체의 직렬화를 담당하도록 지정할 수 있습니다. 이렇게 하려면 커스텀 cast 클래스가 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스는 클래스에 값 객체의 직렬화된 형태를 반환하는 `serialize` 메서드가 있어야 한다고 명시합니다:

```php
/**
 * Get the serialized representation of the value.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(
    Model $model,
    string $key,
    mixed $value,
    array $attributes,
): string {
    return (string) $value;
}
```

<a name="inbound-casting"></a>
<!-- ### Inbound Casting -->
### Inbound Casting

<!-- Occasionally, you may need to write a custom cast class that only transforms values that are being set on the model and does not perform any operations when attributes are being retrieved from the model. -->
때로는 모델에 설정되는 값만 변환하고, 모델에서 속성을 가져올 때는 아무 작업도 수행하지 않는 커스텀 cast 클래스를 작성해야 할 수 있습니다.

<!-- Inbound only custom casts should implement the `CastsInboundAttributes` interface, which only requires a `set` method to be defined. The `make:cast` Artisan command may be invoked with the `--inbound` option to generate an inbound only cast class: -->
인바운드 전용 커스텀 cast는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `set` 메서드만 정의하면 됩니다. `make:cast` Artisan 명령어에 `--inbound` 옵션을 함께 사용하면 인바운드 전용 cast 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast AsHash --inbound
```

<!-- A classic example of an inbound only cast is a "hashing" cast. For example, we may define a cast that hashes inbound values via a given algorithm: -->
인바운드 전용 cast의 대표적인 예는 "해싱" cast입니다. 예를 들어, 주어진 알고리즘을 통해 인바운드 값을 해싱하는 cast를 정의할 수 있습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
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
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
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
모델에 커스텀 cast를 연결할 때, `:` 문자를 사용해 클래스명과 구분하고 여러 매개변수는 쉼표로 구분하여 cast 매개변수를 지정할 수 있습니다. 이 매개변수는 cast 클래스의 생성자에 전달됩니다:

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'secret' => AsHash::class.':sha256',
    ];
}
```

<a name="comparing-cast-values"></a>
<!-- ### Comparing Cast Values -->
### Comparing Cast Values

<!-- If you would like to define how two given cast values should be compared to determine if they have been changed, your custom cast class may implement the `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` interface. This allows you to have fine-grained control over which values Eloquent considers changed and thus saves to the database when a model is updated. -->
주어진 두 cast 값이 변경되었는지 판단하기 위해 어떻게 비교해야 하는지 정의하고 싶다면, 커스텀 cast 클래스가 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현할 수 있습니다. 이를 통해 Eloquent가 어떤 값을 변경된 것으로 간주하고, 모델이 업데이트될 때 데이터베이스에 저장할지 세밀하게 제어할 수 있습니다.

<!-- This interface states that your class should contain a `compare` method which should return `true` if the given values are considered equal: -->
이 인터페이스는 클래스에 `compare` 메서드가 있어야 하며, 주어진 값이 같다고 판단되면 `true`를 반환해야 한다고 명시합니다:

```php
/**
 * Determine if the given values are equal.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  mixed  $firstValue
 * @param  mixed  $secondValue
 * @return bool
 */
public function compare(
    Model $model,
    string $key,
    mixed $firstValue,
    mixed $secondValue
): bool {
    return $firstValue === $secondValue;
}
```

<a name="castables"></a>
<!-- ### Castables -->
### Castables

<!-- You may want to allow your application's value objects to define their own custom cast classes. Instead of attaching the custom cast class to your model, you may alternatively attach a value object class that implements the `Illuminate\Contracts\Database\Eloquent\Castable` interface: -->
애플리케이션의 값 객체가 자체 커스텀 cast 클래스를 정의하도록 하고 싶을 수 있습니다. 커스텀 cast 클래스를 모델에 연결하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하는 값 객체 클래스를 연결할 수도 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

<!-- Objects that implement the `Castable` interface must define a `castUsing` method that returns the class name of the custom caster class that is responsible for casting to and from the `Castable` class: -->
`Castable` 인터페이스를 구현하는 객체는 `Castable` 클래스와 상호 변환하는 casting을 담당할 커스텀 caster 클래스의 클래스명을 반환하는 `castUsing` 메서드를 정의해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * Get the name of the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

<!-- When using `Castable` classes, you may still provide arguments in the `casts` method definition. The arguments will be passed to the `castUsing` method: -->
`Castable` 클래스를 사용할 때도 `casts` 메서드 정의에서 인수를 제공할 수 있습니다. 해당 인수는 `castUsing` 메서드로 전달됩니다:

```php
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
"castable"과 PHP의 [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php)를 함께 사용하면, 값 객체와 그 casting 로직을 하나의 castable 객체로 정의할 수 있습니다. 이를 구현하려면 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환합니다. 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

```php
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
            public function get(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): Address {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): array {
                return [
                    'address_line_one' => $value->lineOne,
                    'address_line_two' => $value->lineTwo,
                ];
            }
        };
    }
}
```
