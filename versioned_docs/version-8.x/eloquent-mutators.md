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

<!-- Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/8.x/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model. -->
accessor, mutator, 그리고 attribute casting은 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 해당 값을 변환할 수 있도록 해줍니다. 예를 들어, [Laravel encrypter](/docs/8.x/encryption)를 이용해 값을 데이터베이스에 저장할 때 암호화하고, Eloquent 모델에서 해당 속성을 조회할 때 자동으로 복호화할 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델에서 접근할 때 자동으로 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
<!-- ## Accessors & Mutators -->
## Accessors & Mutators

<a name="defining-an-accessor"></a>
<!-- ### Defining An Accessor -->
### Defining An Accessor

<!-- An accessor transforms an Eloquent attribute value when it is accessed. To define an accessor, create a `get{Attribute}Attribute` method on your model where `{Attribute}` is the "studly" cased name of the column you wish to access. -->
accessor는 Eloquent 속성 값을 접근할 때 값을 변환하는 기능입니다. accessor를 정의하려면 모델에 `get{Attribute}Attribute` 형태의 메서드를 추가합니다. 여기서 `{Attribute}`는 접근하고 싶은 컬럼명을 StudlyCase(첫 글자 대문자, 캐멀케이스와 유사함)로 작성합니다.

<!-- In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute: -->
아래 예시에서는 `first_name` 속성에 대한 accessor를 정의합니다. 이 accessor는 Eloquent에서 `first_name` 값을 가져오려고 할 때 자동으로 호출됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the user's first name.
     *
     * @param  string  $value
     * @return string
     */
    public function getFirstNameAttribute($value)
    {
        return ucfirst($value);
    }
}
```

<!-- As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the accessor, you may simply access the `first_name` attribute on a model instance: -->
보시는 것처럼, 컬럼의 원래 값이 accessor로 전달되므로 원하는 대로 가공해서 반환할 수 있습니다. accessor 값을 사용하려면 단순히 모델 인스턴스에서 `first_name` 속성을 가져오면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

<!-- You are not limited to interacting with a single attribute within your accessor. You may also use accessors to return new, computed values from existing attributes: -->
accessor는 단일 속성에만 한정되지 않습니다. 여러 속성을 조합하거나 새롭게 결합한 계산 결과를 반환하도록 accessor를 활용할 수 있습니다.

```
/**
 * Get the user's full name.
 *
 * @return string
 */
public function getFullNameAttribute()
{
    return "{$this->first_name} {$this->last_name}";
}
```

> [!TIP]
> 계산된 속성이 모델의 배열 또는 JSON 표현에 포함되게 하려면, [you will need to append them](/docs/8.x/eloquent-serialization#appending-values-to-json).

<a name="defining-a-mutator"></a>
<!-- ### Defining A Mutator -->
### Defining A Mutator

<!-- A mutator transforms an Eloquent attribute value when it is set. To define a mutator, define a `set{Attribute}Attribute` method on your model where `{Attribute}` is the "studly" cased name of the column you wish to access. -->
mutator는 Eloquent 속성의 값을 설정(할당)할 때 해당 값을 변환합니다. mutator를 정의하려면 모델에 `set{Attribute}Attribute` 형태로 메서드를 추가합니다. `{Attribute}`에는 대문자로 시작하는 컬럼명을 사용해야 합니다.

<!-- Let's define a mutator for the `first_name` attribute. This mutator will be automatically called when we attempt to set the value of the `first_name` attribute on the model: -->
예를 들어, `first_name` 속성에 대해 mutator를 정의하겠습니다. 이 mutator는 모델에서 `first_name` 값을 설정할 때 자동으로 호출됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Set the user's first name.
     *
     * @param  string  $value
     * @return void
     */
    public function setFirstNameAttribute($value)
    {
        $this->attributes['first_name'] = strtolower($value);
    }
}
```

<!-- The mutator will receive the value that is being set on the attribute, allowing you to manipulate the value and set the manipulated value on the Eloquent model's internal `$attributes` property. To use our mutator, we only need to set the `first_name` attribute on an Eloquent model: -->
mutator는 속성에 할당하려는 값을 인수로 받아 변환한 후, Eloquent 모델의 내부 `$attributes` 속성에 해당 값을 저장하면 됩니다. mutator를 활용하려면 단순히 모델의 `first_name` 속성을 할당하면 됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

<!-- In this example, the `setFirstNameAttribute` function will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its resulting value in the internal `$attributes` array. -->
위 예시에서 `setFirstNameAttribute` 메서드는 `Sally`를 인수로 받아, `strtolower` 함수를 적용한 후 그 결과를 내부 `$attributes` 배열에 저장합니다.

<a name="attribute-casting"></a>
<!-- ## Attribute Casting -->
## Attribute Casting

<!-- Attribute casting provides functionality similar to accessors and mutators without requiring you to define any additional methods on your model. Instead, your model's `$casts` property provides a convenient method of converting attributes to common data types. -->
attribute casting은 accessor나 mutator와 유사한 기능을 제공하지만, 모델에 별도의 메서드를 정의할 필요가 없습니다. 대신, 모델의 `$casts` 속성을 사용하면 속성 값을 일반적으로 많이 사용하는 데이터 타입으로 간편하게 변환할 수 있습니다.

<!-- The `$casts` property should be an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are: -->
`$casts` 속성은 배열이어야 하며, 배열의 키는 casting 대상 속성명, 값은 변환하려는 타입입니다. 지원되는 casting 타입은 다음과 같습니다.

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
- `decimal:`<code>&lt;digits&gt;</code>
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
- `decimal:`<code>&lt;digits&gt;</code>
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
attribute casting의 예시로, 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언 값으로 변환해봅니다.

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
이렇게 casting을 정의하면, 데이터베이스에 정수로 저장되어 있어도 `is_admin` 속성에 접근할 때 항상 불리언 타입으로 변환된 값을 받을 수 있습니다.

```
$user = App\Models\User::find(1);

if ($user->is_admin) {
    //
}
```

<!-- If you need to add a new, temporary cast at runtime, you may use the `mergeCasts` method. These cast definitions will be added to any of the casts already defined on the model: -->
실행 중에 임시로 새로운 cast를 추가해야 할 경우, `mergeCasts` 메서드를 사용하여 기존 casting 정의에 추가할 수 있습니다.

```
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!NOTE]
> 값이 `null`인 속성은 casting되지 않습니다. 그리고, 연관관계와 이름이 같은 속성(혹은 cast)은 절대 정의하지 않아야 합니다.

<a name="stringable-casting"></a>
<!-- #### Stringable Casting -->
#### Stringable Casting

<!-- You may use the `Illuminate\Database\Eloquent\Casts\AsStringable` cast class to cast a model attribute to a [fluent `Illuminate\Support\Stringable` object](/docs/8.x/helpers#fluent-strings-method-list): -->
모델 속성을 [fluent `Illuminate\Support\Stringable` object](/docs/8.x/helpers#fluent-strings-method-list)로 casting하려면 `Illuminate\Database\Eloquent\Casts\AsStringable` cast 클래스를 사용할 수 있습니다.

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
`array` cast는 직렬화된 JSON 문자열로 저장된 컬럼을 사용할 때 매우 유용합니다. 데이터베이스의 `JSON` 또는 `TEXT` 타입 컬럼에 직렬화된 JSON이 저장되어 있다면, `array` cast를 속성에 적용하여 해당 값을 Eloquent 모델에서 접근할 때 자동으로 PHP 배열로 변환할 수 있습니다.

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
casting을 정의하면, `options` 속성에 접근할 때마다 JSON이 자동으로 PHP 배열로 변환됩니다. `options` 속성에 값을 설정하면, 전달한 배열이 자동으로 JSON 문자열로 변환되어 저장됩니다.

```
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

<!-- To update a single field of a JSON attribute with a more terse syntax, you may use the `->` operator when calling the `update` method: -->
JSON 속성의 단일 필드를 더 간단하게 업데이트하려면 `update` 메서드 호출 시 `->` 연산자를 사용할 수 있습니다.

```
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
<!-- #### Array Object & Collection Casting -->
#### Array Object & Collection Casting

<!-- Although the standard `array` cast is sufficient for many applications, it does have some disadvantages. Since the `array` cast returns a primitive type, it is not possible to mutate an offset of the array directly. For example, the following code will trigger a PHP error: -->
기본 `array` cast만으로 충분한 경우가 많지만, 몇 가지 단점이 있습니다. `array` cast는 프리미티브 타입을 반환하기 때문에, 배열의 오프셋(인덱스) 값을 직접 변경할 수 없습니다. 예를 들어, 다음 코드에서는 에러가 발생합니다.

```
$user = User::find(1);

$user->options['key'] = $value;
```

<!-- To solve this, Laravel offers an `AsArrayObject` cast that casts your JSON attribute to an [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) class. This feature is implemented using Laravel's [custom cast](#custom-casts) implementation, which allows Laravel to intelligently cache and transform the mutated object such that individual offsets may be modified without triggering a PHP error. To use the `AsArrayObject` cast, simply assign it to an attribute: -->
이 문제를 해결하기 위해 Laravel에서는 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 JSON 속성을 변환해주는 `AsArrayObject` cast를 제공합니다. 이 기능은 Laravel의 [custom cast](#custom-casts) 구현을 이용하여, Laravel이 변이된 객체를 지능적으로 캐싱 및 변환하므로 PHP 오류를 발생시키지 않고 각 오프셋 값을 변경할 수 있습니다. `AsArrayObject` cast를 사용하려면, 단순히 해당 속성에 cast 클래스를 지정하면 됩니다.

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

<!-- Similarly, Laravel offers an `AsCollection` cast that casts your JSON attribute to a Laravel [Collection](/docs/8.x/collections) instance: -->
마찬가지로, Laravel에서는 JSON 속성을 [Collection](/docs/8.x/collections) 인스턴스로 변환해주는 `AsCollection` cast도 제공합니다.

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
<a id="#date-casting" data-translation-alias="true"></a>
<!-- ### Date Casting -->
### Date Casting

<!-- By default, Eloquent will cast the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which extends the PHP `DateTime` class and provides an assortment of helpful methods. You may cast additional date attributes by defining additional date casts within your model's `$casts` property array. Typically, dates should be cast using the `datetime` or `immutable_datetime` cast types. -->
기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 객체로 casting합니다. Carbon은 PHP의 `DateTime` 클래스를 확장한 라이브러리로, 다양한 날짜 관련 유틸리티 기능을 제공합니다. 모델의 `$casts` 속성 배열에 추가적으로 다른 날짜 속성들을 등록해서 자동으로 casting하도록 할 수 있습니다. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` casting 타입으로 변환하는 것이 권장됩니다.

<!-- When defining a `date` or `datetime` cast, you may also specify the date's format. This format will be used when the [model is serialized to an array or JSON](/docs/8.x/eloquent-serialization): -->
`date` 또는 `datetime` cast를 정의할 때, 날짜 형식을 지정할 수도 있습니다. 이 형식은 [model is serialized to an array or JSON](/docs/8.x/eloquent-serialization) 적용됩니다.

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
날짜 타입으로 casting된 컬럼에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 직접 할당할 수 있습니다. 각 값은 데이터베이스에 저장되기 전에 올바르게 변환됩니다.

<!-- You may customize the default serialization format for all of your model's dates by defining a `serializeDate` method on your model. This method does not affect how your dates are formatted for storage in the database: -->
모델의 모든 날짜 컬럼에 대한 기본 직렬화 포맷을 바꾸고 싶다면, 모델에 `serializeDate` 메서드를 정의할 수 있습니다. 이 메서드는 데이터베이스에 실제로 저장될 포맷에는 영향을 주지 않습니다.

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
모델의 날짜 컬럼이 데이터베이스에 실제로 저장될 때의 형식을 명시하려면 `$dateFormat` 속성을 모델에 정의하세요.

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
기본적으로 `date`와 `datetime` cast는 애플리케이션의 `timezone` 설정값과 관계없이 UTC ISO-8601 날짜 문자열(`1986-05-28T21:05:54.000000Z`)로 직렬화됩니다. 이 직렬화 포맷을 항상 사용하고, 애플리케이션의 `timezone` 설정을 기본값인 `UTC`에서 변경하지 않은 채로 애플리케이션의 날짜를 UTC 타임존으로 저장할 것을 강력히 권장합니다. 이렇게 하면 PHP, JavaScript 등 다양한 날짜 라이브러리와 최대한 호환성을 확보할 수 있기 때문입니다.

<!-- If a custom format is applied to the `date` or `datetime` cast, such as `datetime:Y-m-d H:i:s`, the inner timezone of the Carbon instance will be used during date serialization. Typically, this will be the timezone specified in your application's `timezone` configuration option. -->
다만, `date` 또는 `datetime` cast에 사용자 지정 포맷(`datetime:Y-m-d H:i:s` 등)을 적용하면, Carbon 인스턴스의 내부 타임존이 직렬화 시 사용됩니다(일반적으로 애플리케이션의 `timezone` 설정값을 따릅니다).

<a name="enum-casting"></a>
<!-- ### Enum Casting -->
### Enum Casting

> [!NOTE]
> Enum casting 기능은 PHP 8.1 이상에서만 사용할 수 있습니다.

<!-- Eloquent also allows you to cast your attribute values to PHP enums. To accomplish this, you may specify the attribute and enum you wish to cast in your model's `$casts` property array: -->
Eloquent에서는 속성 값을 PHP의 enum(열거형) 타입으로 변환해줄 수 있습니다. 이를 위해 모델의 `$casts` 배열에 속성과 enum 클래스를 지정합니다.

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
casting을 정의하면 해당 속성은 접근/설정할 때 자동으로 enum 타입으로 변환되어 다룰 수 있습니다.

```
if ($server->status == ServerStatus::provisioned) {
    $server->status = ServerStatus::ready;

    $server->save();
}
```

<a name="encrypted-casting"></a>
<!-- ### Encrypted Casting -->
### Encrypted Casting

<!-- The `encrypted` cast will encrypt a model's attribute value using Laravel's built-in [encryption](/docs/8.x/encryption) features. In addition, the `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, and `AsEncryptedCollection` casts work like their unencrypted counterparts; however, as you might expect, the underlying value is encrypted when stored in your database. -->
`encrypted` cast는 모델의 속성 값을 Laravel 내장 [encryption](/docs/8.x/encryption) 기능으로 암호화해서 데이터베이스에 저장하고, 조회 시 자동 복호화해줍니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection`과 같은 cast들은 암호화되지 않은 cast와 동일하게 동작하며, 단지 데이터베이스에는 암호화해서 저장만 합니다.

<!-- As the final length of the encrypted text is not predictable and is longer than its plain text counterpart, make sure the associated database column is of `TEXT` type or larger. In addition, since the values are encrypted in the database, you will not be able to query or search encrypted attribute values. -->
암호화된 텍스트의 길이는 예측할 수 없으며, 원래 데이터보다 길기 때문에 해당 컬럼의 타입은 반드시 `TEXT` 이상이어야 합니다. 또한, 암호화된 속성 값은 데이터베이스에서 직접 검색하거나 쿼리할 수 없습니다.

<a name="query-time-casting"></a>
<!-- ### Query Time Casting -->
### Query Time Casting

<!-- Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query: -->
때로는 쿼리를 실행할 때, 예를 들어 테이블에서 직접 계산한 값을 조회한 뒤 타입 casting을 적용하고 싶을 수 있습니다. 아래와 같은 쿼리 예시를 봅시다.

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
이 쿼리의 결과로 반환되는 `last_posted_at` 속성은 단순 문자열이 됩니다. 이럴 땐, 쿼리 실행 시 `datetime` casting을 적용하면 더 편리합니다. 이를 위해 `withCasts` 메서드를 사용할 수 있습니다.

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

<!-- Laravel has a variety of built-in, helpful cast types; however, you may occasionally need to define your own cast types. You may accomplish this by defining a class that implements the `CastsAttributes` interface. -->
Laravel은 다양한 기본 제공 casting 타입을 지원하지만, 때로는 직접 원하는 방식의 casting 타입을 정의해야 할 수도 있습니다. 이를 위해 `CastsAttributes` 인터페이스를 구현하는 클래스를 만들면 됩니다.

<!-- Classes that implement this interface must define a `get` and `set` method. The `get` method is responsible for transforming a raw value from the database into a cast value, while the `set` method should transform a cast value into a raw value that can be stored in the database. As an example, we will re-implement the built-in `json` cast type as a custom cast type: -->
이 인터페이스를 구현한 클래스는 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스에서 조회한 원시 값을 casting된 값으로 변환해주고, `set` 메서드는 casting된 값을 원시 값 형태로 변환해 데이터베이스에 저장할 수 있도록 반환합니다. 아래 예시는 내장 `json` casting 타입을 직접 구현한 예입니다.

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
커스텀 cast 클래스를 만들었으면, 해당 속성에 클래스명을 사용하여 cast를 지정할 수 있습니다.

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
속성 값을 항상 원시 타입으로만 변환하는 것은 아닙니다. 값을 객체로도 변환할 수 있습니다. 객체로 casting하는 커스텀 cast 클래스를 정의하는 방식은 원시 타입과 거의 동일하지만, 이때 `set` 메서드는 "저장 가능한(원시)" 값들을 키/값 배열로 반환해야 합니다.

<!-- As an example, we will define a custom cast class that casts multiple model values into a single `Address` value object. We will assume the `Address` value has two public properties: `lineOne` and `lineTwo`: -->
예를 들어, 여러 모델 값을 하나의 `Address` 값 객체로 변환하는 커스텀 cast 클래스를 만들어봅니다. 여기서는 `Address` 객체에 `lineOne`, `lineTwo`라는 두 개의 공개 속성이 있다고 가정합니다.

```
<?php

namespace App\Casts;

use App\Models\Address as AddressModel;
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
     * @return \App\Models\Address
     */
    public function get($model, $key, $value, $attributes)
    {
        return new AddressModel(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  \App\Models\Address  $value
     * @param  array  $attributes
     * @return array
     */
    public function set($model, $key, $value, $attributes)
    {
        if (! $value instanceof AddressModel) {
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
값 객체로 변환할 경우, 해당 값 객체의 속성 변경 사항은 모델 저장 전에 자동으로 모델에 동기화됩니다.

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!TIP]
> 값 객체가 포함된 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이 있다면, 값 객체에 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 반드시 구현해야 합니다.

<a name="array-json-serialization"></a>
<!-- ### Array / JSON Serialization -->
### Array / JSON Serialization

<!-- When an Eloquent model is converted to an array or JSON using the `toArray` and `toJson` methods, your custom cast value objects will typically be serialized as well as long as they implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces. However, when using value objects provided by third-party libraries, you may not have the ability to add these interfaces to the object. -->
Eloquent 모델을 `toArray` 혹은 `toJson` 메서드로 배열 또는 JSON으로 변환할 때, 커스텀 cast 값 객체도 일반적으로 직렬화됩니다(단, 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable`을 구현해야 함). 하지만 외부 라이브러리의 값 객체처럼 직접 인터페이스를 구현할 수 없는 경우도 있습니다.

<!-- Therefore, you may specify that your custom cast class will be responsible for serializing the value object. To do so, your custom cast class should implement the `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` interface. This interface states that your class should contain a `serialize` method which should return the serialized form of your value object: -->
이런 경우, 커스텀 cast 클래스가 값 객체의 직렬화까지 담당하게 할 수 있습니다. 이때는 커스텀 cast 클래스에서 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스는 커스텀 클래스에 `serialize` 메서드를 구현할 것을 요구합니다. 이 메서드는 값 객체를 직렬화 형태로 반환해야 합니다.

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

<!-- Occasionally, you may need to write a custom cast that only transforms values that are being set on the model and does not perform any operations when attributes are being retrieved from the model. A classic example of an inbound only cast is a "hashing" cast. Inbound only custom casts should implement the `CastsInboundAttributes` interface, which only requires a `set` method to be defined. -->
간혹 모델의 속성 값을 **입력(할당)**할 때만 변환하고 조회할 때는 별도로 변환을 적용하지 않는 커스텀 cast가 필요할 때도 있습니다. 대표적인 예시가 "해싱" cast입니다. 입력 전용 casting을 구현하려면 `CastsInboundAttributes` 인터페이스를 구현하면 됩니다. 이때는 `set` 메서드만 구현하면 됩니다.

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
커스텀 cast를 모델에 연결할 때, 클래스명 뒤에 `:` 문자를 사용해 파라미터를 전달할 수 있습니다. 여러 개의 파라미터는 쉼표(,)로 구분하며, 이 값들은 cast 클래스의 생성자에서 받을 수 있습니다.

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
애플리케이션에서 사용되는 값 객체가 자체적으로 커스텀 cast 클래스를 정의해야 할 때가 있습니다. 이런 경우, 모델에 커스텀 cast 클래스를 직접 지정하지 않고, 값 객체 클래스 자체가 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하도록 할 수 있습니다.

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
`Castable` 클래스 사용 시에도 `$casts` 속성에 파라미터를 넘길 수 있고, 이 파라미터들은 `castUsing` 메서드로 전달됩니다.

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
"Castable" 기능과 PHP의 [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php)를 조합해 값 객체와 해당 값 객체의 casting 로직을 하나의 Castable 오브젝트로 정의할 수도 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 이 익명 클래스는 `CastsAttributes` 인터페이스를 반드시 구현해야 합니다.

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
