# Eloquent: 접근자, 변경자, 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [접근자와 변경자](#accessors-and-mutators)
    - [접근자 정의](#defining-an-accessor)
    - [변경자 정의](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [이진(Binary) 캐스팅](#binary-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화(Encrypted) 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [커스텀 캐스팅](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열/JSON 직렬화](#array-json-serialization)
    - [인바운드(Inbound) 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스트 값 비교](#comparing-cast-values)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개 (Introduction)

접근자(accessor), 변경자(mutator), 그리고 속성 캐스팅은 Eloquent 모델 인스턴스에서 속성 값을 가져오거나 설정할 때 그 값을 변환할 수 있도록 도와줍니다. 예를 들어, [Laravel Encrypter](/docs/master/encryption)로 값을 암호화하여 데이터베이스에 저장하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화하고 싶을 수도 있습니다. 또는 데이터베이스에 JSON 문자열로 저장된 값을 Eloquent 모델을 통해 접근할 때 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자와 변경자 (Accessors and Mutators)

<a name="defining-an-accessor"></a>
### 접근자 정의 (Defining an Accessor)

접근자는 Eloquent 속성 값에 접근할 때 해당 값을 변환합니다. 접근자를 정의하려면, 모델에 접근 가능한 속성을 나타내는 protected 메서드를 생성합니다. 이 메서드의 이름은 실제 모델 속성/데이터베이스 컬럼의 "카멜 케이스(camel case)" 형태와 일치해야 합니다(해당되는 경우).

예를 들어, `first_name` 속성에 대한 접근자를 정의해 보겠습니다. 이 접근자는 `first_name` 속성의 값을 가져올 때 Eloquent에 의해 자동으로 호출됩니다. 모든 속성 접근자/변경자 메서드는 `Illuminate\Database\Eloquent\Casts\Attribute` 타입의 반환 타입 힌트를 명시해야 합니다:

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

모든 접근자 메서드는 속성을 어떻게 가져올지(그리고 선택적으로 어떻게 변경할지)를 정의하는 `Attribute` 인스턴스를 반환합니다. 위의 예제에서는 속성을 어떻게 가져올지만 정의하고 있으며, 이를 위해 `Attribute` 클래스 생성자에 `get` 인수를 전달합니다.

보시는 것처럼, 컬럼의 원래 값이 접근자에 전달되므로 원하는 방식으로 값을 조작할 수 있습니다. 접근자 값을 사용하려면 모델 인스턴스에서 해당 속성에 간단히 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이런 식으로 계산된 값들도 모델의 배열/JSON 표현에 포함하고 싶다면, [별도로 append 해주어야 합니다](/docs/master/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성에서 값 객체(Value Object) 만들기

때로는 접근자가 여러 모델 속성을 하나의 "값 객체"로 변환해야 할 때가 있습니다. 이 경우, `get` 클로저에서 두 번째 인수인 `$attributes`를 받을 수 있으며, 이 인수에는 모델의 현재 모든 속성이 배열로 전달됩니다:

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

접근자에서 값 객체를 반환할 경우, 해당 값 객체를 변경하면 모델을 저장하기 전 자동으로 모델에 반영됩니다. 이는 Eloquent가 접근자가 반환한 인스턴스를 보관해두고 매번 동일한 인스턴스를 반환하기 때문에 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만, 계산 비용이 높은 문자열이나 불리언 등 기본값(primitive value)에 대해서도 캐싱을 활성화하고 싶을 때가 있을 수 있습니다. 이를 위해 접근자를 정의할 때 `shouldCache` 메서드를 사용할 수 있습니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

또한, 속성의 객체 캐싱 동작을 비활성화하고 싶다면, `withoutObjectCaching` 메서드를 사용할 수 있습니다:

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
### 변경자 정의 (Defining a Mutator)

변경자는 Eloquent 속성 값을 설정할 때 값을 변환합니다. 변경자를 정의하려면, 속성을 정의할 때 `set` 인수를 전달하면 됩니다. 예를 들어, `first_name` 속성에 대한 변경자를 정의해 보겠습니다. 이 변경자는 `first_name` 속성 값을 모델에 설정할 때 자동으로 호출됩니다:

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

변경자 클로저에는 실제로 속성에 저장될 값이 전달되며, 이 값을 원하는 방식으로 변환해서 반환할 수 있습니다. 변경자를 사용하려면 Eloquent 모델의 속성을 간단히 설정하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예제에서 `set` 콜백은 `Sally` 값을 인수로 받게 됩니다. 변경자는 `strtolower` 함수를 적용하여 소문자로 바꾸고, 그 결과를 모델 내부의 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변경하기

변경자가 기본 모델의 여러 속성을 한 번에 변경해야 할 때는, `set` 클로저에서 배열을 반환하면 됩니다. 이 배열의 각 키는 모델과 연결된 실제 속성이나 데이터베이스 컬럼과 일치해야 합니다:

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
## 속성 캐스팅 (Attribute Casting)

속성 캐스팅은 접근자와 변경자와 비슷한 기능을 제공하지만, 별도의 추가 메서드를 모델에 정의하지 않고도 속성을 일반적으로 많이 쓰이는 데이터 타입으로 변환해줍니다.

`casts` 메서드는 캐스팅할 속성명을 키로, 캐스팅 타입을 값으로 갖는 배열을 반환해야 합니다. 지원되는 캐스팅 타입은 다음과 같습니다:

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

속성 캐스팅 예시로, 데이터베이스에서 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언 값으로 캐스트해보겠습니다:

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

캐스트를 정의하면, 실제로는 데이터베이스에 정수로 저장되어 있더라도 항상 `is_admin` 속성을 불리언으로 사용할 수 있습니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 새로운 임시 캐스트를 추가해야 할 경우, `mergeCasts` 메서드를 사용할 수 있습니다. 이 정의는 기존 모델에 정의된 캐스트에 추가됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 캐스팅되지 않습니다. 또한, 연관관계(relationships)와 동일한 이름의 속성이나 모델의 기본 키(primary key)에는 캐스트를 정의하지 말아야 합니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

모델 속성을 [유연한(Fluent) Illuminate\Support\Stringable 객체](/docs/master/strings#fluent-strings-method-list)로 캐스트하려면 `Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용할 수 있습니다:

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
### 배열 및 JSON 캐스팅 (Array and JSON Casting)

`array` 캐스팅은 직렬화된 JSON 데이터가 저장된 컬럼을 처리할 때 유용합니다. 예를 들어, 데이터베이스에서 `JSON`이나 `TEXT` 필드 타입에 JSON 문자열이 저장되어 있다면, `array` 캐스팅을 통해 Eloquent 모델에서 해당 속성을 PHP 배열로 자동 역직렬화할 수 있습니다:

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

캐스트를 정의한 후에는, `options` 속성에 접근할 때 자동으로 JSON에서 PHP 배열로 역직렬화됩니다. 반대로, 배열을 `options`에 할당하면 자동으로 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 필드만 간단한 구문으로 업데이트하려면, [속성을 일괄 할당(mass assignable) 처리](/docs/master/eloquent#mass-assignment-json-columns)하고, `update` 메서드 호출 시 `->` 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 이스케이프되지 않은(unescaped) 유니코드 문자 기반 JSON으로 저장하고 싶다면 `json:unicode` 캐스팅을 사용하세요:

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
#### ArrayObject 및 컬렉션 캐스팅

기본 `array` 캐스팅이 대부분의 경우에 충분하지만, offset을 직접 변경할 수 없다는 단점이 있습니다. 예를 들어, 아래 코드는 PHP 에러를 발생시킵니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 변환해주는 `AsArrayObject` 캐스팅을 제공합니다. 이 기능은 [커스텀 캐스팅](#custom-casts) 기반으로 동작하며, 값을 개별적으로 수정할 수 있도록 해줍니다. 사용법은 다음과 같습니다:

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

마찬가지로, JSON 값을 Laravel [컬렉션](/docs/master/collections) 인스턴스로 변환해 주는 `AsCollection` 캐스팅도 있습니다:

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

`AsCollection` 캐스팅에 커스텀 컬렉션 클래스를 사용하고 싶다면, 캐스트 인수로 컬렉션 클래스명을 전달할 수 있습니다:

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

`of` 메서드를 사용하여 컬렉션의 각 아이템을 지정한 클래스로 매핑할 수도 있습니다(컬렉션의 [mapInto 메서드](/docs/master/collections#method-mapinto) 참조):

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

컬렉션을 객체로 매핑할 때, 해당 객체는 데이터베이스에 JSON으로 직렬화하는 방법을 정의하기 위해 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 반드시 구현해야 합니다:

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

Eloquent 모델에 [binary 타입](/docs/master/migrations#column-method-binary)의 `uuid`나 `ulid` 컬럼이 모델의 기본 자동증가 ID 컬럼과 함께 있다면, `AsBinary` 캐스트를 통해 값을 자동으로 이진(binary) 형태와 평문(string) 형태로 상호 변환할 수 있습니다:

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

캐스트를 모델에 정의한 뒤에는, UUID/ULID 속성에 객체나 문자열을 할당할 수 있습니다. Eloquent가 자동으로 이 값을 이진(binary)로 저장하고, 조회 시에는 항상 평문 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```

<a name="date-casting"></a>
### 날짜 캐스팅 (Date Casting)

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 자동 변환합니다. Carbon은 PHP의 `DateTime` 클래스를 확장한 라이브러리로, 다양한 날짜 관련 메서드를 제공합니다. 추가적으로 특정 속성을 날짜 타입으로 캐스트하려면, 모델의 `casts` 메서드에서 해당 속성을 `date`, `datetime`, `immutable_date`, `immutable_datetime` 등으로 지정하세요.

`date` 또는 `datetime` 캐스팅을 정의할 때, 날짜의 포맷도 함께 지정할 수 있습니다. 이 포맷은 [모델을 배열/JSON으로 직렬화할 때](/docs/master/eloquent-serialization) 사용됩니다:

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

컬럼을 날짜로 캐스트할 경우, 모델 속성에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 설정할 수 있습니다. Eloquent가 알아서 올바른 방식으로 데이터베이스에 저장합니다.

모든 날짜의 기본 직렬화 포맷을 변경하려면, 모델에 `serializeDate` 메서드를 정의하세요. 이 값은 데이터베이스에 저장되는 포맷에는 영향을 주지 않습니다:

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

데이터베이스에 실제로 저장할 날짜 포맷을 지정하고 싶다면, 모델의 `Table` 속성에서 `dateFormat` 인수를 사용하세요:

```php
use Illuminate\Database\Eloquent\Attributes\Table;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`, `datetime` 캐스트는 애플리케이션의 `timezone` 설정과 관계없이 날짜를 UTC ISO-8601 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화합니다. 이 UTC 포맷을 항상 사용하는 것이 권장되며, 애플리케이션의 `timezone` 설정을 기본값인 `UTC`로 유지하는 것도 권장됩니다. UTC를 사용하면 PHP, JavaScript 등 다른 날짜 라이브러리와의 호환성이 극대화됩니다.

커스텀 포맷(예: `datetime:Y-m-d H:i:s`)이 적용된 경우, Carbon 인스턴스 내부의 타임존(보통 `timezone` 설정에 지정된 값)이 직렬화에 사용됩니다. 단, `created_at`, `updated_at`과 같은 `timestamp` 컬럼은 이 동작의 예외로, 애플리케이션 타임존 설정과 무관하게 항상 UTC로 직렬화됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성 값을 PHP [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로도 캐스팅할 수 있습니다. 이를 위해, 모델의 `casts` 메서드에서 속성과 해당 Enum 클래스를 지정하세요:

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

캐스트를 정의한 후에는, 해당 속성은 Enum 타입으로 자동 변환되어 사용할 수 있습니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

하나의 컬럼에 Enum 값의 배열을 저장하고 싶을 때는, Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스팅을 사용할 수 있습니다:

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
### 암호화(Encrypted) 캐스팅

`encrypted` 캐스트는 모델 속성 값을 Laravel의 [내장 암호화 기능](/docs/master/encryption)으로 암호화하여 저장합니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스팅은 암호화 여부만 다르고 사용 방식은 기존과 동일합니다.

암호화된 텍스트의 최종 길이는 예측할 수 없으며, 평문보다 훨씬 길어질 수 있으므로 해당 데이터베이스 컬럼은 반드시 `TEXT` 타입 이상이어야 합니다. 또한 데이터베이스에 암호화되어 저장되므로 암호화된 속성 값으로는 질의(query)나 검색이 불가능합니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

Laravel은 애플리케이션의 `app` 설정 파일에 지정된 `key` 구성 값을 이용해 문자열을 암호화합니다. 보통 이 값은 `APP_KEY` 환경 변수와 연결되어 있습니다. 암호화 키를 교체할 필요가 있다면, [안전하게 키를 교체하세요](/docs/master/encryption#gracefully-rotating-encryption-keys).

<a name="query-time-casting"></a>
### 쿼리 타임 캐스팅 (Query Time Casting)

쿼리 실행 시(raw select 등) 캐스팅을 적용하고 싶은 경우가 있습니다. 예를 들어, 아래 쿼리를 살펴보세요:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

결과로 나오는 `last_posted_at`은 단순 문자열입니다. 여기에 `datetime` 캐스팅을 적용하고 싶다면, `withCasts` 메서드를 사용하면 됩니다:

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
## 커스텀 캐스팅 (Custom Casts)

Laravel에는 다양한 내장 캐스트 타입이 있지만, 필요에 따라 직접 커스텀 캐스트 타입을 정의할 수도 있습니다. 캐스트를 만들려면, `make:cast` Artisan 명령어를 실행하세요. 새 캐스트 클래스는 `app/Casts` 디렉터리에 생성됩니다:

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현한 클래스는 반드시 `get`, `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스에서 꺼낸 원시 값을 캐스트 값으로 변환하고, `set` 메서드는 캐스트 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환합니다. 예를 들어 기본 제공되는 `json` 캐스트 타입을 직접 구현해보면:

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

커스텀 캐스트 타입을 정의한 후에는 클래스명을 이용해 모델 속성에 캐스트를 연결할 수 있습니다:

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
### 값 객체 캐스팅 (Value Object Casting)

프리미티브 타입뿐만 아니라, 값을 객체로도 캐스팅할 수 있습니다. 값 객체로 캐스팅하는 커스텀 캐스트를 정의할 때 여러 데이터베이스 컬럼을 하나의 값 객체로 묶어 반환해야 할 수도 있습니다. 이때 `set` 메서드는 여러 컬럼에 저장할 수 있도록 키/값 쌍의 배열을 반환해야 합니다. 만약 값 객체가 단일 컬럼만 사용한다면, 저장 가능한 단일 값을 반환합니다.

예를 들어 두 개의 데이터베이스 값을 하나의 `Address` 값 객체로 변환하는 커스텀 캐스트 클래스를 정의해보겠습니다(`Address` 객체에는 `lineOne`, `lineTwo` 두 개의 public 속성이 있다고 가정):

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

값 객체로 캐스팅할 때는, 객체의 변경 사항이 자동으로 모델에 반영되고, 모델을 저장하면 함께 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체가 포함된 Eloquent 모델을 JSON이나 배열로 직렬화하려면, 해당 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하는 것이 좋습니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성은 Eloquent에서 일시적으로 캐싱됩니다. 따라서 해당 속성에 다시 접근하면 동일한 객체 인스턴스가 반환됩니다.

커스텀 캐스트 클래스에서 객체 캐싱을 비활성화하고 싶다면, 클래스에 public `withoutObjectCaching` 속성을 선언하면 됩니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열/JSON 직렬화 (Array / JSON Serialization)

Eloquent 모델을 `toArray`나 `toJson` 등으로 배열이나 JSON으로 변환할 때, 커스텀 캐스트 값 객체도 직렬화됩니다(단, `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스 구현 필요). 하지만, 서드파티 라이브러리의 객체라면 해당 인터페이스를 Implement할 수 없는 경우가 있습니다.

이럴 때 커스텀 캐스트 클래스에서 직접 직렬화 책임을 지도록 할 수 있습니다. 그러려면, 커스텀 캐스트 클래스에서 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고, `serialize` 메서드를 정의해야 합니다:

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
### 인바운드(Inbound) 캐스팅

특정 속성이 모델에 설정될 때만 변환이 필요하고, 조회할 때는 별도로 변환하지 않아도 된다면, 인바운드 전용 커스텀 캐스트 클래스를 만들 수 있습니다.

인바운드 전용 커스텀 캐스트 클래스는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 반드시 `set` 메서드만 정의하면 됩니다. Artisan의 `make:cast` 명령어에서 `--inbound` 옵션을 사용해 생성할 수 있습니다:

```shell
php artisan make:cast AsHash --inbound
```

고전적인 인바운드 캐스트 예시는 해싱(Hashing)입니다. 예를 들어, 특정 알고리즘으로 값을 해싱하는 캐스트를 아래와 같이 정의할 수 있습니다:

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
### 캐스트 파라미터 (Cast Parameters)

커스텀 캐스트를 모델에 연결할 때, 클래스명 다음에 `:` 문자로 구분해 파라미터를 지정할 수 있습니다. 여러 파라미터는 쉼표로 구분하며, 이 값들은 캐스트 클래스의 생성자에 전달됩니다:

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
### 캐스트 값 비교 (Comparing Cast Values)

두 캐스트 값이 변경되었는지 직접 정의하고 싶다면, 커스텀 캐스트 클래스에서 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현할 수 있습니다. 이를 통해 Eloquent가 어떤 값을 변경된 것으로 인식하고 데이터베이스에 저장할지 세밀하게 제어할 수 있습니다.

이 인터페이스는 `compare` 메서드를 요구하며, 주어진 두 값이 일치하면 `true`를 반환해야 합니다:

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

애플리케이션의 값 객체가 자체적으로 커스텀 캐스트 클래스를 정의하도록 할 수도 있습니다. 커스텀 캐스트 클래스를 모델에 직접 연결하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 연결할 수 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는 `castUsing` 메서드를 정의해야 하며, 이 메서드는 해당 값 객체로 변환(혹은 그 반대)할 커스텀 캐스터 클래스명을 반환해야 합니다:

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

`Castable` 클래스를 사용할 때에도, `casts` 메서드 정의에서 인자를 넘길 수 있으며, 이 인자는 `castUsing` 메서드로 전달됩니다:

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
#### 캐스터블 & 익명 캐스트 클래스

"캐스터블"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 함께 사용하면, 값 객체와 해당 캐스팅 로직을 하나의 객체로 정의할 수도 있습니다. 이때, 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

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