# Eloquent: 뮤테이터와 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [액세서와 뮤테이터](#accessors-and-mutators)
    - [액세서 정의하기](#defining-an-accessor)
    - [뮤테이터 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [바이너리 캐스팅](#binary-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화된 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 매개변수](#cast-parameters)
    - [캐스트 값 비교](#comparing-cast-values)
    - [Castables](#castables)

<a name="introduction"></a>
## 소개 (Introduction)

액세서, 뮤테이터, 속성 캐스팅을 사용하면 모델 인스턴스에서 Eloquent 속성 값을 가져오거나 설정할 때 그 값을 변환할 수 있습니다. 예를 들어, 어떤 값을 데이터베이스에 저장할 때 [Laravel encrypter](/docs/13.x/encryption)를 사용해 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화하고 싶을 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 액세서와 뮤테이터 (Accessors and Mutators)

<a name="defining-an-accessor"></a>
### 액세서 정의하기

액세서는 Eloquent 속성 값에 접근할 때 그 값을 변환합니다. 액세서를 정의하려면 모델에서 접근 가능한 속성을 나타내는 protected 메서드를 생성합니다. 적용 가능한 경우, 이 메서드 이름은 실제 기반 모델 속성 / 데이터베이스 컬럼의 "camel case" 표현과 일치해야 합니다.

이 예제에서는 `first_name` 속성에 대한 액세서를 정의합니다. `first_name` 속성 값을 가져오려고 할 때 Eloquent가 이 액세서를 자동으로 호출합니다. 모든 속성 액세서 / 뮤테이터 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 반환 타입 힌트를 선언해야 합니다.

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

모든 액세서 메서드는 속성에 어떻게 접근할지, 그리고 선택적으로 어떻게 변경할지를 정의하는 `Attribute` 인스턴스를 반환합니다. 이 예제에서는 속성에 접근하는 방법만 정의하고 있습니다. 이를 위해 `Attribute` 클래스 생성자에 `get` 인수를 전달합니다.

보시다시피 컬럼의 원래 값이 액세서로 전달되므로, 값을 조작한 뒤 반환할 수 있습니다. 액세서의 값에 접근하려면 모델 인스턴스에서 `first_name` 속성에 그대로 접근하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이렇게 계산된 값을 모델의 배열 / JSON 표현에 추가하고 싶다면 [해당 값을 append해야 합니다](/docs/13.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

때로는 액세서가 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 수 있습니다. 이를 위해 `get` 클로저는 두 번째 인수로 `$attributes`를 받을 수 있습니다. 이 값은 클로저에 자동으로 전달되며, 모델의 현재 모든 속성을 담은 배열을 포함합니다.

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
#### 액세서 캐싱

액세서에서 값 객체를 반환할 때, 값 객체에 적용한 변경 사항은 모델이 저장되기 전에 자동으로 모델에 다시 동기화됩니다. 이는 Eloquent가 액세서에서 반환된 인스턴스를 보관해, 액세서가 호출될 때마다 같은 인스턴스를 반환할 수 있기 때문에 가능합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만 문자열이나 불리언 같은 원시 값에 대해서도 캐싱을 활성화하고 싶을 때가 있습니다. 특히 계산 비용이 큰 경우에 유용합니다. 이를 위해 액세서를 정의할 때 `shouldCache` 메서드를 호출할 수 있습니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

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
### 뮤테이터 정의하기

뮤테이터는 Eloquent 속성 값이 설정될 때 그 값을 변환합니다. 뮤테이터를 정의하려면 속성을 정의할 때 `set` 인수를 제공하면 됩니다. `first_name` 속성에 대한 뮤테이터를 정의해 보겠습니다. 이 뮤테이터는 모델에서 `first_name` 속성 값을 설정하려고 할 때 자동으로 호출됩니다.

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

뮤테이터 클로저는 속성에 설정되는 값을 전달받습니다. 따라서 해당 값을 조작한 뒤 조작된 값을 반환할 수 있습니다. 이 뮤테이터를 사용하려면 Eloquent 모델에서 `first_name` 속성을 설정하기만 하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예제에서 `set` 콜백은 `Sally` 값을 인수로 호출됩니다. 그러면 뮤테이터는 이름에 `strtolower` 함수를 적용하고, 그 결과 값을 모델 내부의 `$attributes` 배열에 설정합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변경하기

때로는 뮤테이터가 기반 모델의 여러 속성을 설정해야 할 수 있습니다. 이를 위해 `set` 클로저에서 배열을 반환할 수 있습니다. 배열의 각 키는 모델과 연결된 기반 속성 / 데이터베이스 컬럼과 일치해야 합니다.

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

속성 캐스팅은 모델에 추가 메서드를 정의하지 않아도 액세서와 뮤테이터와 비슷한 기능을 제공합니다. 대신 모델의 `casts` 메서드는 속성을 일반적인 데이터 타입으로 변환하는 편리한 방법을 제공합니다.

`casts` 메서드는 배열을 반환해야 하며, 키는 캐스팅할 속성 이름이고 값은 해당 컬럼을 캐스팅하려는 타입입니다. 지원되는 캐스트 타입은 다음과 같습니다.

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

속성 캐스팅을 보여주기 위해, 데이터베이스에는 정수(`0` 또는 `1`)로 저장되는 `is_admin` 속성을 불리언 값으로 캐스팅해 보겠습니다.

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

캐스트를 정의한 뒤에는 기반 값이 데이터베이스에 정수로 저장되어 있더라도, `is_admin` 속성에 접근할 때 항상 불리언으로 캐스팅됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 새로운 임시 캐스트를 추가해야 한다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 캐스트 정의는 모델에 이미 정의된 캐스트에 추가됩니다.

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null`인 속성은 캐스팅되지 않습니다. 또한 연관관계와 같은 이름을 가진 캐스트(또는 속성)를 정의해서는 안 되며, 모델의 기본 키에 캐스트를 할당해서도 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면 모델 속성을 [fluent Illuminate\Support\Stringable 객체](/docs/13.x/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다.

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

`array` 캐스트는 직렬화된 JSON으로 저장되는 컬럼을 다룰 때 특히 유용합니다. 예를 들어 데이터베이스에 직렬화된 JSON을 포함하는 `JSON` 또는 `TEXT` 필드 타입이 있다면, 해당 속성에 `array` 캐스트를 추가했을 때 Eloquent 모델에서 접근하면 자동으로 PHP 배열로 역직렬화됩니다.

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

캐스트가 정의되면 `options` 속성에 접근할 수 있으며, 이 속성은 JSON에서 PHP 배열로 자동 역직렬화됩니다. `options` 속성 값을 설정할 때는 전달한 배열이 저장을 위해 다시 JSON으로 자동 직렬화됩니다.

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 필드를 더 간결한 문법으로 업데이트하려면, [해당 속성을 대량 할당 가능하게 만들고](/docs/13.x/eloquent#mass-assignment-json-columns) `update` 메서드를 호출할 때 `->` 연산자를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 Unicode

배열 속성을 이스케이프되지 않은 Unicode 문자로 JSON에 저장하고 싶다면 `json:unicode` 캐스트를 사용할 수 있습니다.

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
#### 배열 객체 및 컬렉션 캐스팅

표준 `array` 캐스트는 많은 애플리케이션에서 충분하지만 몇 가지 단점도 있습니다. `array` 캐스트는 원시 타입을 반환하므로 배열의 오프셋을 직접 변경할 수 없습니다. 예를 들어 다음 코드는 PHP 오류를 발생시킵니다.

```php
$user = User::find(1);

$user->options['key'] = $value;
```
이를 해결하기 위해 Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 Laravel의 [커스텀 캐스트](#custom-casts) 구현을 사용하여 만들어졌으며, Laravel이 변경된 객체를 지능적으로 캐시하고 변환할 수 있게 해 줍니다. 따라서 개별 오프셋을 수정해도 PHP 오류가 발생하지 않습니다. `AsArrayObject` 캐스트를 사용하려면 속성에 할당하기만 하면 됩니다.

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

마찬가지로 Laravel은 JSON 속성을 Laravel [Collection](/docs/13.x/collections) 인스턴스로 캐스팅하는 `AsCollection` 캐스트를 제공합니다.

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

`AsCollection` 캐스트가 Laravel의 기본 컬렉션 클래스 대신 커스텀 컬렉션 클래스를 인스턴스화하도록 하려면, 컬렉션 클래스 이름을 캐스트 인수로 제공할 수 있습니다.

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

`of` 메서드를 사용하면 컬렉션의 [mapInto 메서드](/docs/13.x/collections#method-mapinto)를 통해 컬렉션 항목을 지정한 클래스로 매핑해야 함을 나타낼 수 있습니다.

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
### 바이너리 캐스팅

Eloquent 모델에 자동 증가 ID 컬럼과 함께 [바이너리 타입](/docs/13.x/migrations#column-method-binary)의 `uuid` 또는 `ulid` 컬럼이 있다면, `AsBinary` 캐스트를 사용하여 값을 바이너리 표현으로 자동 캐스팅하거나 바이너리 표현에서 다시 캐스팅할 수 있습니다.

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

모델에 캐스트를 정의한 후에는 UUID / ULID 속성값을 객체 인스턴스나 문자열로 설정할 수 있습니다. Eloquent는 해당 값을 자동으로 바이너리 표현으로 캐스팅합니다. 속성값을 조회할 때는 항상 일반 텍스트 문자열 값을 받게 됩니다.

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at` 및 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. Carbon은 PHP의 `DateTime` 클래스를 확장하며 다양한 유용한 메서드를 제공합니다. 모델의 `casts` 메서드 안에 추가 날짜 캐스트를 정의하여 다른 날짜 속성도 캐스팅할 수 있습니다. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` 캐스트 타입을 사용해 캐스팅해야 합니다.

`date` 또는 `datetime` 캐스트를 정의할 때 날짜 형식도 지정할 수 있습니다. 이 형식은 [모델이 배열 또는 JSON으로 직렬화될 때](/docs/13.x/eloquent-serialization) 사용됩니다.

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

컬럼이 날짜로 캐스팅되면, 해당 모델 속성값을 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime` / `Carbon` 인스턴스로 설정할 수 있습니다. 날짜 값은 올바르게 변환되어 데이터베이스에 저장됩니다.

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
#### 날짜 캐스팅, 직렬화 및 시간대

기본적으로 `date` 및 `datetime` 캐스트는 애플리케이션의 `timezone` 설정 옵션에 지정된 시간대와 관계없이 날짜를 UTC ISO-8601 날짜 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화합니다. 이 직렬화 형식을 항상 사용하는 것이 강력히 권장되며, 애플리케이션의 `timezone` 설정 옵션을 기본값인 `UTC`에서 변경하지 않음으로써 애플리케이션의 날짜를 UTC 시간대로 저장하는 것도 권장됩니다. 애플리케이션 전체에서 UTC 시간대를 일관되게 사용하면 PHP와 JavaScript로 작성된 다른 날짜 조작 라이브러리와의 상호 운용성을 가장 높은 수준으로 확보할 수 있습니다.

`datetime:Y-m-d H:i:s`와 같이 `date` 또는 `datetime` 캐스트에 커스텀 형식이 적용된 경우, 날짜 직렬화 과정에서 Carbon 인스턴스 내부의 시간대가 사용됩니다. 일반적으로 이는 애플리케이션의 `timezone` 설정 옵션에 지정된 시간대입니다. 다만 `created_at` 및 `updated_at` 같은 `timestamp` 컬럼은 이 동작에서 제외되며, 애플리케이션의 시간대 설정과 관계없이 항상 UTC로 포맷된다는 점에 유의해야 합니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)로 캐스팅하는 것도 허용합니다. 이를 위해 모델의 `casts` 메서드에 캐스팅하려는 속성과 enum을 지정할 수 있습니다.

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

모델에 캐스트를 정의하고 나면, 해당 속성과 상호작용할 때 지정된 속성은 자동으로 enum으로 캐스팅되거나 enum에서 다시 캐스팅됩니다.

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

때로는 모델이 단일 컬럼 안에 enum 값 배열을 저장해야 할 수 있습니다. 이를 위해 Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 활용할 수 있습니다.

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

`encrypted` 캐스트는 Laravel의 내장 [암호화](/docs/13.x/encryption) 기능을 사용하여 모델의 속성값을 암호화합니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트는 암호화되지 않은 대응 항목과 동일하게 동작합니다. 다만 예상할 수 있듯이, 데이터베이스에 저장될 때 내부 값이 암호화됩니다.

암호화된 텍스트의 최종 길이는 예측할 수 없고 일반 텍스트보다 길기 때문에, 관련 데이터베이스 컬럼이 `TEXT` 타입 이상인지 확인해야 합니다. 또한 값이 데이터베이스에서 암호화되므로, 암호화된 속성값을 쿼리하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
#### 키 교체

알고 있듯이 Laravel은 애플리케이션의 `app` 설정 파일에 지정된 `key` 설정 값을 사용하여 문자열을 암호화합니다. 일반적으로 이 값은 `APP_KEY` 환경 변수의 값에 해당합니다. 애플리케이션의 암호화 키를 교체해야 한다면 [점진적으로 처리할 수 있습니다](/docs/13.x/encryption#gracefully-rotating-encryption-keys).

<a name="query-time-casting"></a>
### 쿼리 실행 시점 캐스팅

테이블에서 원시 값을 선택하는 경우처럼, 쿼리를 실행하는 동안 캐스트를 적용해야 할 때가 있습니다. 예를 들어 다음 쿼리를 살펴보겠습니다.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리 결과의 `last_posted_at` 속성은 단순한 문자열입니다. 쿼리를 실행할 때 이 속성에 `datetime` 캐스트를 적용할 수 있다면 좋을 것입니다. 다행히 `withCasts` 메서드를 사용하여 이를 수행할 수 있습니다.

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

Laravel에는 다양하고 유용한 내장 캐스트 타입이 있습니다. 하지만 때로는 직접 캐스트 타입을 정의해야 할 수도 있습니다. 캐스트를 만들려면 `make:cast` Artisan 명령어를 실행합니다. 새 캐스트 클래스는 `app/Casts` 디렉터리에 배치됩니다.

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현합니다. 이 인터페이스를 구현하는 클래스는 `get` 및 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스의 원시 값을 캐스트된 값으로 변환하는 역할을 하며, `set` 메서드는 캐스트된 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환해야 합니다. 예제로 내장 `json` 캐스트 타입을 커스텀 캐스트 타입으로 다시 구현해 보겠습니다.

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

커스텀 캐스트 타입을 정의한 후에는 클래스 이름을 사용하여 모델 속성에 연결할 수 있습니다.

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

값을 기본 타입으로 캐스팅하는 것에만 제한되지 않습니다. 값을 객체로 캐스팅할 수도 있습니다. 값을 객체로 캐스팅하는 커스텀 캐스트를 정의하는 방식은 기본 타입으로 캐스팅하는 방식과 매우 비슷합니다. 다만 값 객체가 둘 이상의 데이터베이스 컬럼을 포함하는 경우, `set` 메서드는 모델에 설정될 원시 저장 가능 값으로 사용할 키 / 값 쌍의 배열을 반환해야 합니다. 값 객체가 단일 컬럼에만 영향을 준다면, 저장 가능한 값을 그대로 반환하면 됩니다.

예제로 여러 모델 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 정의해 보겠습니다. `Address` 값 객체에는 두 개의 공개 속성인 `lineOne`과 `lineTwo`가 있다고 가정하겠습니다.

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
값 객체로 캐스팅할 때, 값 객체에 가한 변경 사항은 모델이 저장되기 전에 자동으로 모델에 다시 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 JSON 또는 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성이 해석될 때, Eloquent는 해당 값을 캐시합니다. 따라서 그 속성에 다시 접근하면 동일한 객체 인스턴스가 반환됩니다.

커스텀 캐스트 클래스의 객체 캐싱 동작을 비활성화하고 싶다면, 커스텀 캐스트 클래스에 public `withoutObjectCaching` 속성을 선언할 수 있습니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델이 `toArray` 및 `toJson` 메서드를 사용해 배열 또는 JSON으로 변환될 때, 커스텀 캐스트 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하고 있다면 일반적으로 함께 직렬화됩니다. 하지만 서드파티 라이브러리가 제공하는 값 객체를 사용할 때는 해당 인터페이스를 객체에 추가할 수 없을 수도 있습니다.

따라서 커스텀 캐스트 클래스가 값 객체의 직렬화를 담당하도록 지정할 수 있습니다. 이렇게 하려면 커스텀 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스는 클래스에 값 객체의 직렬화된 형태를 반환하는 `serialize` 메서드가 있어야 한다고 명시합니다:

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

때로는 모델에 설정되는 값만 변환하고, 모델에서 속성을 가져올 때는 아무 작업도 수행하지 않는 커스텀 캐스트 클래스를 작성해야 할 수 있습니다.

인바운드 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `set` 메서드만 정의하면 됩니다. `make:cast` Artisan 명령어에 `--inbound` 옵션을 함께 사용하면 인바운드 전용 캐스트 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast AsHash --inbound
```

인바운드 전용 캐스트의 대표적인 예는 "해싱" 캐스트입니다. 예를 들어, 주어진 알고리즘을 통해 인바운드 값을 해싱하는 캐스트를 정의할 수 있습니다:

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
### 캐스트 매개변수

모델에 커스텀 캐스트를 연결할 때, `:` 문자를 사용해 클래스명과 구분하고 여러 매개변수는 쉼표로 구분하여 캐스트 매개변수를 지정할 수 있습니다. 이 매개변수는 캐스트 클래스의 생성자에 전달됩니다:

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

주어진 두 캐스트 값이 변경되었는지 판단하기 위해 어떻게 비교해야 하는지 정의하고 싶다면, 커스텀 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현할 수 있습니다. 이를 통해 Eloquent가 어떤 값을 변경된 것으로 간주하고, 모델이 업데이트될 때 데이터베이스에 저장할지 세밀하게 제어할 수 있습니다.

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
### Castable 객체

애플리케이션의 값 객체가 자체 커스텀 캐스트 클래스를 정의하도록 하고 싶을 수 있습니다. 커스텀 캐스트 클래스를 모델에 연결하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하는 값 객체 클래스를 연결할 수도 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현하는 객체는 `Castable` 클래스와 상호 변환하는 캐스팅을 담당할 커스텀 캐스터 클래스의 클래스명을 반환하는 `castUsing` 메서드를 정의해야 합니다:

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
#### Castable 객체와 익명 캐스트 클래스

"castable"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 함께 사용하면, 값 객체와 그 캐스팅 로직을 하나의 castable 객체로 정의할 수 있습니다. 이를 구현하려면 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환합니다. 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

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
