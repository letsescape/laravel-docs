# Eloquent: 변이자와 타입 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [접근자와 변이자](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변이자 정의하기](#defining-a-mutator)
- [속성 타입 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [이진(Binary) 캐스팅](#binary-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열/JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스트 값 비교](#comparing-cast-values)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개 (Introduction)

접근자(accessor), 변이자(mutator), 그리고 속성 타입 캐스팅(attribute casting)은 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 해당 값을 원하는 대로 변환할 수 있도록 해줍니다. 예를 들어, [Laravel 암호화 시스템](/docs/12.x/encryption)을 사용해 데이터베이스에 저장할 때 값을 암호화하고, Eloquent 모델에서 속성을 조회할 때 자동으로 복호화하여 사용할 수 있습니다. 또는, 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 조회할 때 배열로 변환할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자와 변이자 (Accessors and Mutators)

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 Eloquent 속성의 값을 조회할 때 변환하는 역할을 합니다. 접근자를 정의하려면, 모델에 보호된(protected) 메서드를 만들어 해당 속성을 나타내세요. 이 메서드의 이름은 실제 모델 속성 또는 데이터베이스 컬럼의 "카멜 케이스(camel case)" 표현과 일치해야 합니다.

예를 들어, 여기서는 `first_name` 속성에 대한 접근자를 정의합니다. 이 접근자는 Eloquent가 `first_name` 속성 값을 조회할 때 자동으로 호출됩니다. 모든 속성 접근자/변이자 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입 힌트를 반환해야 합니다:

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

모든 접근자 메서드는 속성을 어떻게 접근(조회)할지, 그리고 선택적으로 변이(설정)할지 정의하는 `Attribute` 인스턴스를 반환합니다. 위 예시에서는 속성을 조회할 때 어떻게 변환할지(`get` 인자만 전달)만 정의하고 있습니다.

보시다시피, 컬럼의 원래 값이 접근자에 전달되어 값을 원하는 대로 조작할 수 있습니다. 접근자 값을 조회하려면, 모델 인스턴스에서 `first_name` 속성을 그냥 사용하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이와 같이 계산된 값을 모델의 배열/JSON 표현에 포함시키고 싶다면, [직접 값을 추가해야](/docs/12.x/eloquent-serialization#appending-values-to-json) 합니다.

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성에서 값 객체 빌드하기

접근자가 여러 모델 속성을 결합해 하나의 "값 객체(value object)"로 변환해야 하는 경우도 있습니다. 이때는 `get` 클로저의 두 번째 인자로 `$attributes`를 받아, 현재 모델의 모든 속성을 배열로 받을 수 있습니다:

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
#### 접근자 캐싱

접근자에서 반환되는 값 객체에 대해 값을 변경했을 때, 이 변경 사항은 모델이 저장되기 전에 자동으로 동기화됩니다. 이는 Eloquent가 접근자에서 반환된 인스턴스를 내부적으로 보존하고, 접근자가 여러 번 호출되어도 동일한 인스턴스를 반환하기 때문입니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

한편, 문자열이나 불리언과 같은 프리미티브 값에 대해서도, 계산 비용이 크다면 캐싱을 활성화하고 싶을 수 있습니다. 이럴 경우, 접근자 정의 시 `shouldCache` 메서드를 사용할 수 있습니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 값 객체의 캐싱 기능을 비활성화하고 싶다면 접근자 정의 시 `withoutObjectCaching` 메서드를 사용할 수 있습니다:

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
### 변이자 정의하기

변이자는 Eloquent 속성 값을 설정할 때 변환합니다. 변이자를 정의하려면, Attribute 정의 시 `set` 인자를 제공합니다. 이 예시에서는 `first_name` 속성에 대한 변이자를 정의합니다. 이 변이자는 속성 값을 모델에 설정하려고 할 때 자동으로 호출됩니다:

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

변이자 클로저에는 속성에 지정하려는 값이 전달됩니다. 이 값을 원하는 대로 조작해서 반환하면 됩니다. 예를 들어 사용 시에는, Eloquent 모델의 `first_name` 속성에 값을 설정하기만 하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 예시에서 `set` 콜백은 `Sally` 값을 전달받아 `strtolower` 함수를 적용하고, 처리 결과 값을 모델의 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변이하기

가끔 변이자가 모델의 여러 속성 값을 동시에 설정해야 할 수도 있습니다. 이럴 때는 `set` 클로저에서 배열을 반환하세요. 배열의 각 키는 모델의 실제 속성명(데이터베이스 컬럼명)에 대응합니다:

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
## 속성 타입 캐스팅 (Attribute Casting)

속성 타입 캐스팅은 접근자와 변이자와 유사한 기능을 제공하지만, 추가 메서드 정의 없이 더 간편하게 사용할 수 있습니다. 모델의 `casts` 메서드에서 속성명을 키, 변환할 타입명을 값으로 하는 배열을 반환하면 속성에 타입 캐스팅이 적용됩니다.

지원되는 캐스트 타입은 아래와 같습니다:

<div class="content-list" markdown="1">

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

</div>

예를 들어, 데이터베이스에 정수(0 또는 1)로 저장된 `is_admin` 속성을 불리언(boolean) 값으로 변환하려면 아래와 같이 작성합니다:

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

이렇게 캐스트를 지정하면, 데이터베이스에 저장된 값이 정수여도 항상 불리언으로 사용하게 됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 일시적으로 새로운 타입 캐스트를 추가하고 싶다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 메서드는 기존에 정의된 캐스트에 새 캐스트를 병합합니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 캐스트되지 않습니다. 또한, 연관관계와 같은 이름의 캐스트(또는 속성)를 정의하거나, 모델의 기본 키에 캐스트를 지정해서는 안됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하여 모델 속성을 [fluent Illuminate\Support\Stringable 객체](/docs/12.x/strings#fluent-strings-method-list)로 변환할 수 있습니다:

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
### 배열 및 JSON 캐스팅

`array` 캐스트는 직렬화된 JSON 형태로 저장된 컬럼을 사용할 때 특히 유용합니다. 데이터베이스에 `JSON` 또는 `TEXT` 타입 컬럼에 JSON 문자열이 저장되어 있다면, `array` 캐스트를 적용하면 해당 속성을 Eloquent 모델에서 PHP 배열로 자동 변환/역변환할 수 있습니다:

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

캐스트가 정의되면, `options` 속성에 접근하면 JSON에서 PHP 배열로 자동 역직렬화됩니다. 값을 할당할 때도 배열을 지정하면 자동으로 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 개별 필드를 더 쉽게 업데이트하려면, [컬럼을 대량 할당 가능(mass assignable)하게 만들고](/docs/12.x/eloquent#mass-assignment-json-columns) `update` 메서드에서 `->` 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 저장할 때 유니코드 문자를 이스케이프하지 않고 JSON으로 저장하고 싶다면, `json:unicode` 캐스트를 사용할 수 있습니다:

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
#### ArrayObject 및 Collection 캐스팅

기본 `array` 캐스트는 대부분 상황에서 충분하지만, 배열 오프셋을 직접 변경할 수 없는 한계가 있습니다. 예를 들어, 다음 코드는 PHP 에러를 일으킵니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해 Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 Laravel의 [커스텀 캐스트](#custom-casts)로 구현되어 있기 때문에, 오프셋 단위로 값을 손쉽게 변경하며, 변이 객체도 자동으로 처리됩니다. 사용 예시는 다음과 같습니다:

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

또한, Laravel은 JSON 속성을 Laravel [컬렉션](/docs/12.x/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 지원합니다:

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

`AsCollection` 캐스트로 Laravel의 기본 컬렉션 클래스 대신 커스텀 컬렉션 클래스를 사용하고 싶다면, 캐스트 인자로 클래스명을 넘기면 됩니다:

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

`of` 메서드를 사용해 컬렉션의 각 항목을 지정한 클래스로 변환할 수 있습니다(컬렉션의 [mapInto 메서드](/docs/12.x/collections#method-mapinto) 활용):

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

컬렉션을 객체로 매핑할 때, 해당 객체는 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현해야 데이터베이스에 JSON으로 직렬화될 때 올바르게 처리됩니다:

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
### 이진(Binary) 캐스팅

Eloquent 모델에 [binary 타입](/docs/12.x/migrations#column-method-binary)의 `uuid`나 `ulid` 컬럼이 있고, 별도의 자동 증가 ID 컬럼이 있을 때 `AsBinary` 캐스트를 사용하면 값의 이진 표현을 손쉽게 변환할 수 있습니다:

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

캐스트를 지정하면, UUID/ULID 속성을 객체나 문자열로 지정해도 Eloquent가 자동으로 이진(binary) 표현으로 변환해 저장합니다. 값을 조회할 때는 항상 일반 텍스트 값(문자열)로 반환됩니다:

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 변환합니다. Carbon은 PHP `DateTime` 클래스를 확장한 강력한 날짜 처리 라이브러리입니다. 추가로 날짜 속성을 캐스팅하려면, `casts` 메서드에 해당 속성과 캐스트 타입을 지정해 주세요. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` 캐스트 타입을 사용합니다.

`date` 혹은 `datetime` 캐스트를 정의할 때, 날짜 포맷을 지정할 수도 있습니다. 이 포맷은 [모델이 배열이나 JSON으로 직렬화될 때](/docs/12.x/eloquent-serialization) 사용됩니다:

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

날짜로 캐스트된 컬럼은 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스 등 다양한 값 형태로 지정할 수 있습니다. 지정한 값은 적절하게 변환되어 데이터베이스에 저장됩니다.

모델의 날짜 직렬화 기본 포맷을 변경하고 싶다면, 모델에 `serializeDate` 메서드를 정의하면 됩니다(데이터베이스 저장 포맷과는 무관):

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

모델의 날짜 컬럼이 실제 DB에 저장될 때 사용할 포맷을 지정하려면, 모델에 `$dateFormat` 속성을 설정합니다:

```php
/**
 * The storage format of the model's date columns.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date` 및 `datetime` 캐스트는 애플리케이션의 `timezone` 설정과 무관하게 날짜를 UTC ISO-8601 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화합니다. 최대 수준의 상호운용성을 위해 기본값인 `UTC` 타임존 설정을 변경하지 않고, 이 직렬화 포맷을 사용할 것을 권장합니다. 이렇게 하면, PHP나 JavaScript 등 다양한 라이브러리와 날짜 연동이 쉬워집니다.

만약 `date`나 `datetime` 캐스트에 커스텀 포맷(`datetime:Y-m-d H:i:s` 등)이 지정되면, 직렬화 시 Carbon 인스턴스의 내부 타임존을 사용합니다. 이때 주로 애플리케이션의 `timezone` 설정을 따르게 됩니다. 단, `created_at`, `updated_at` 등 `timestamp` 컬럼은 애플리케이션 타임존과 무관하게 항상 UTC로 직렬화됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent에서는 속성 값을 PHP [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로 캐스팅할 수 있습니다. 모델의 `casts` 메서드에서 속성명과 해당 Enum 클래스를 지정하세요:

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

캐스트가 정의되면, 해당 속성에 값을 지정하거나 조회할 때 자동으로 Enum 인스턴스로 변환됩니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

하나의 컬럼에 Enum 값의 배열을 저장하고자 할 때는 Laravel에서 제공하는 `AsEnumArrayObject` 혹은 `AsEnumCollection` 캐스트를 사용할 수 있습니다:

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
### 암호화 캐스팅

`encrypted` 캐스트는 모델의 속성 값을 Laravel의 [암호화 기능](/docs/12.x/encryption)으로 암호화하여 저장합니다. 또한, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트는 기본(암호화되지 않은) 캐스트 기능과 동일하게 동작하되, 값이 데이터베이스에 저장될 때 암호화됩니다.

암호화된 문자열은 평문보다 더 길고, 정확한 길이를 예측할 수 없으므로, 해당 컬럼은 `TEXT` 타입이나 그보다 큰 타입으로 지정해야 합니다. 또한, 값이 암호화되어 저장되므로, 이 값을 기준으로 쿼리하거나 검색하는 것은 불가능합니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

Laravel은 애플리케이션의 `app` 설정 파일에 정의된 `key` 값을 사용해서 문자열을 암호화합니다. 보통 이 값은 `APP_KEY` 환경 변수와 일치합니다. 애플리케이션의 암호화 키를 교체해야 한다면, [안전하게 교체하는 방법](/docs/12.x/encryption#gracefully-rotating-encryption-keys)을 참고하세요.

<a name="query-time-casting"></a>
### 쿼리 타임 캐스팅

쿼리 실행시, 예를 들어 테이블에서 raw 값을 선택하는 경우 캐스트를 적용하고 싶을 때가 있습니다. 아래 예시를 참고하세요:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리로 얻은 결과의 `last_posted_at` 속성은 단순 문자열입니다. 이 값을 바로 `datetime` 캐스트로 다루고 싶다면, `withCasts` 메서드를 활용할 수 있습니다:

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
## 커스텀 캐스트 (Custom Casts)

Laravel에는 유용한 내장 캐스트 타입이 많이 있지만, 상황에 따라 사용자 정의 캐스트 타입을 만들어야 할 때가 있습니다. 캐스트를 생성하려면 `make:cast` Artisan 명령어를 실행하세요. 새 캐스트 클래스는 `app/Casts` 디렉토리에 생성됩니다:

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스의 원시 값을 캐스트 값으로 변환하고, `set` 메서드는 캐스트 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환합니다. 내장 `json` 캐스트 타입을 예시로, 아래와 같이 커스텀 캐스트 클래스를 구현할 수 있습니다:

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

커스텀 캐스트 타입을 정의한 뒤에는, 클래스명을 속성에 지정하여 사용합니다:

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
### 값 객체 캐스팅

캐스트 타입은 프리미티브 타입뿐만 아니라 객체로도 적용할 수 있습니다. 여러 데이터베이스 컬럼을 결합한 값 객체로 캐스팅하는 것도 가능합니다. 만약 값 객체가 여러 컬럼에 걸친 속성을 가진다면, `set` 메서드는 각각의 키/값 쌍을 배열로 반환해야 하고, 단일 컬럼만 다룬다면 저장될 단일 값을 반환하면 됩니다.

예를 들어, 두 개의 모델 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 아래처럼 정의할 수 있습니다:

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

값 객체로 캐스팅할 때, 값 객체에서 변경 사항이 발생하면 모델이 저장되기 전에 자동으로 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함한 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성은 Eloquent가 내부적으로 캐싱하므로, 해당 속성에 여러 번 접근해도 항상 동일한 인스턴스를 반환합니다.

이 캐싱 동작을 비활성화하고 싶다면 커스텀 캐스트 클래스에 public 속성인 `withoutObjectCaching`을 선언하면 됩니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열/JSON 직렬화

Eloquent 모델을 `toArray` 또는 `toJson` 메서드로 배열이나 JSON으로 변환하면, 커스텀 캐스트 값 객체도 직렬화됩니다(값 객체가 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현한 경우). 그러나, 외부 라이브러리의 값 객체처럼 직접 인터페이스를 추가할 수 없는 상황이 있을 수 있습니다.

이런 경우에는 커스텀 캐스트 클래스에서 직접 직렬화 로직을 구현할 수 있습니다. `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고, `serialize` 메서드를 정의하세요:

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
### 인바운드 캐스팅

가끔은 모델의 값을 설정할 때만 동작하고, 값을 조회할 때는 아무 작업도 하지 않는 커스텀 캐스트가 필요할 때가 있습니다.

이런 인바운드 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, `set` 메서드만 정의하면 됩니다. Artisan의 `make:cast` 명령어에 `--inbound` 옵션을 추가해 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast AsHash --inbound
```

가장 대표적인 예는 비밀번호 등 "해싱" 캐스트입니다. 예를 들어, 아래와 같이 값이 저장될 때만 특정 함수(해시 알고리즘 등)를 적용할 수 있습니다:

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
### 캐스트 파라미터

커스텀 캐스트를 모델에 지정할 때, 클래스명 뒤에 `:` 문자를 사용하고 여러 파라미터를 쉼표로 구분하여 전달할 수 있습니다. 파라미터는 캐스트 클래스의 생성자에 순서대로 전달됩니다:

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
### 캐스트 값 비교

두 캐스트 값이 변경되었는지 여부(동등한지) 판단 방식을 직접 정의하고 싶다면, 커스텀 캐스트 클래스에서 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현하세요. 이를 통해 모델 업데이트 시 어떤 값이 "변경"되었는지 세밀하게 제어할 수 있습니다.

이 인터페이스는 `compare` 메서드를 요구하며, 동일하면 `true`를 반환해야 합니다:

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
### 캐스터블(Castables)

애플리케이션의 값 객체가 자신만의 커스텀 캐스트 클래스를 결정하도록 구성할 수 있습니다. 커스텀 캐스트 클래스를 모델에 직접 지정하는 대신, 값 객체 클래스 자체가 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하고 있으면 됩니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는, `Castable` 클래스로부터 캐스팅할 때/캐스팅할 때 어떤 커스텀 캐스터 클래스를 사용할지 결정하는 `castUsing` 메서드를 정의해야 합니다:

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

`Castable` 클래스를 사용할 때, `casts` 정의에 추가 인자를 함께 줄 수도 있습니다. 이 인자들은 `castUsing` 메서드에 전달됩니다:

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
#### 캐스터블 & 익명(Anonymous) 캐스트 클래스

"캐스터블"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합하여, 값 객체와 캐스트 로직을 하나의 객체로 정의할 수 있습니다. 이를 위해, 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하세요. 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

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
