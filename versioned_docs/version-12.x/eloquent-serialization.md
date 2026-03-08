# 일러퀀트: 직렬화 (Eloquent: Serialization)

- [소개](#introduction)
- [모델과 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화](#serializing-to-arrays)
    - [JSON으로 직렬화](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel로 API를 개발할 때, 모델과 연관관계(relationships)를 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 쉽게 할 수 있는 편리한 메서드를 제공하며, 모델의 직렬화된 표현에 포함되는 속성을 제어할 수 있는 방법도 제공합니다.

> [!NOTE]
> Eloquent 모델 및 컬렉션의 JSON 직렬화를 더욱 강력하게 처리하려면, [Eloquent API 리소스](/docs/12.x/eloquent-resources) 문서를 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
## 모델과 컬렉션 직렬화 (Serializing Models and Collections)

<a name="serializing-to-arrays"></a>
### 배열로 직렬화 (Serializing to Arrays)

모델과 로드된 [연관관계](/docs/12.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용합니다. 이 메서드는 재귀적으로 동작하여 모든 속성과 연관관계(연관관계의 연관관계까지 포함)를 배열로 변환합니다:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드는 모델의 속성만 배열로 변환하며, 연관관계는 포함하지 않습니다:

```php
$user = User::first();

return $user->attributesToArray();
```

또한, 전체 [컬렉션](/docs/12.x/eloquent-collections)을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화 (Serializing to JSON)

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`와 마찬가지로, `toJson`도 재귀적으로 모든 속성과 연관관계를 JSON으로 변환합니다. 또한 [PHP에서 지원하는](https://secure.php.net/manual/en/function.json-encode.php) 모든 JSON 인코딩 옵션을 지정할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는 모델이나 컬렉션을 문자열로 캐스팅하면 자동으로 `toJson` 메서드가 호출됩니다:

```php
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 캐스팅될 때 자동으로 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 일러퀀트 객체를 바로 반환할 수 있습니다. 라라벨은 라우트나 컨트롤러에서 반환된 일러퀀트 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관관계

일러퀀트 모델이 JSON으로 변환될 때, 로드된 연관관계도 자동으로 JSON 객체의 속성으로 포함됩니다. 참고로 일러퀀트의 연관관계 메서드는 “카멜 케이스(camel case)”로 정의되어 있지만, JSON 속성명은 “스네이크 케이스(snake case)”로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기 (Hiding Attributes From JSON)

경우에 따라 비밀번호처럼 모델의 배열 또는 JSON 표현에 포함하지 않고 싶은 속성이 있을 수 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 배열에 나열된 속성들은 직렬화된 표현에서 제외됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화 시 숨겨져야 할 속성.
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 연관관계를 숨기려면, 연관관계의 메서드명을 일러퀀트 모델의 `$hidden` 속성에 추가하십시오.

반대로, `visible` 속성을 사용하여 배열과 JSON 표현에 반드시 포함해야 할 속성의 “허용 목록”을 정의할 수도 있습니다. `$visible` 배열에 포함되지 않은 속성들은 모델이 배열이나 JSON으로 변환될 때 숨겨집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에 표시되어야 할 속성.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 일시적으로 속성 표시/숨김 변경하기

일반적으로 숨겨지는 속성을 특정 모델 인스턴스에서만 임시로 보이게 하려면, `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible`은 모델 인스턴스를 반환합니다:

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

반대로, 기본적으로 보이는 속성을 임시로 숨기고 싶다면 `makeHidden` 또는 `mergeHidden` 메서드를 사용할 수 있습니다:

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

보이거나 숨겨지는 모든 속성을 일시적으로 오버라이드하려면 `setVisible` 및 `setHidden` 메서드를 각각 사용할 수 있습니다:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기 (Appending Values to JSON)

가끔 모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼에 직접 대응되는 속성이 없는 값을 추가하고 싶을 수 있습니다. 이런 경우, 먼저 해당 값에 대한 [접근자(accessor)](/docs/12.x/eloquent-mutators)를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자인지 여부를 반환.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

접근자를 항상 모델의 배열 및 JSON 표현에 포함하고 싶다면, 모델의 `appends` 속성에 속성명을 추가합니다. 주의할 점은 속성명은 일반적으로 “스네이크 케이스” 형태로 참조된다는 것입니다. (접근자 메서드는 PHP에서 “카멜 케이스”로 정의됩니다.)

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 형태에 추가할 접근자의 목록.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

이렇게 `appends` 목록에 속성이 추가되면, 해당 속성은 모델의 배열 및 JSON 표현 모두에 포함됩니다. `appends` 배열의 속성은 모델에서 설정된 `visible` 및 `hidden` 설정도 그대로 따릅니다.

<a name="appending-at-run-time"></a>
#### 실행 중에 추가 속성 붙이기

실행 중에 특정 모델 인스턴스에 추가 속성을 붙이고 싶다면, `append` 또는 `mergeAppends` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드를 사용해 해당 인스턴스의 추가 속성 전체 배열을 오버라이드할 수도 있습니다:

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

반대로, 모델에서 모든 추가 속성을 제거하고 싶다면 `withoutAppends` 메서드를 사용하세요:

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화 (Date Serialization)

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이즈

기본 날짜 직렬화 형식을 커스터마이즈하려면 `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 날짜가 저장되는 형식에는 영향을 주지 않습니다:

```php
/**
 * 배열 / JSON 직렬화를 위한 날짜 포맷 정의.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 각 속성별 날짜 포맷 커스터마이즈

특정 일러퀀트 날짜 속성별로 직렬화 포맷을 정의하려면, 모델의 [캐스트 선언](/docs/12.x/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정하면 됩니다:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
