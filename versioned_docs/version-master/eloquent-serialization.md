# Eloquent: 직렬화 (Eloquent: Serialization)

- [소개](#introduction)
- [모델과 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화하기](#serializing-to-arrays)
    - [JSON으로 직렬화하기](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel을 사용해 API를 만들 때 모델과 연관관계를 배열이나 JSON으로 변환해야 하는 경우가 자주 있습니다. Eloquent는 이러한 변환을 편리하게 수행하는 메서드를 제공하며, 모델의 직렬화된 표현에 어떤 속성을 포함할지도 제어할 수 있습니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더욱 견고하게 처리하려면 [Eloquent API 리소스](/docs/master/eloquent-resources) 문서를 확인하세요.

<a name="serializing-models-and-collections"></a>
## 모델과 컬렉션 직렬화 (Serializing Models and Collections)

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 로드된 [연관관계](/docs/master/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용해야 합니다. 이 메서드는 재귀적으로 동작하므로 모든 속성과 모든 연관관계(연관관계의 연관관계 포함)가 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드는 모델의 속성만 배열로 변환하고, 연관관계는 변환하지 않을 때 사용할 수 있습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

컬렉션 인스턴스에서 `toArray` 메서드를 호출하여 모델의 전체 [컬렉션](/docs/master/eloquent-collections)을 배열로 변환할 수도 있습니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용해야 합니다. `toArray`와 마찬가지로 `toJson` 메서드도 재귀적으로 동작하므로 모든 속성과 연관관계가 JSON으로 변환됩니다. 또한 [PHP에서 지원하는](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션을 지정할 수도 있습니다.

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는 모델이나 컬렉션을 문자열로 캐스팅할 수 있으며, 이 경우 모델이나 컬렉션의 `toJson` 메서드가 자동으로 호출됩니다.

```php
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 캐스팅될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관관계

Eloquent 모델이 JSON으로 변환되면, 로드된 연관관계는 JSON 객체의 속성으로 자동 포함됩니다. 또한 Eloquent 연관관계 메서드는 "camel case" 메서드 이름으로 정의되지만, 연관관계의 JSON 속성은 "snake case"가 됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기 (Hiding Attributes From JSON)

때로는 비밀번호와 같은 속성이 모델의 배열 또는 JSON 표현에 포함되지 않도록 제한하고 싶을 수 있습니다. 이를 위해 모델에서 `Hidden` 속성을 사용할 수 있습니다. `Hidden` 속성에 나열된 속성은 모델의 직렬화된 표현에 포함되지 않습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Model;

#[Hidden(['password'])]
class User extends Model
{
    // ...
}
```


> [!NOTE]
> 연관관계를 숨기려면 해당 연관관계의 메서드 이름을 Eloquent 모델의 `Hidden` 속성에 추가하세요.

또는 `Visible` 속성을 사용하여 모델의 배열 및 JSON 표현에 포함되어야 하는 속성의 "허용 목록"을 정의할 수 있습니다. `Visible` 속성에 없는 모든 속성은 모델이 배열이나 JSON으로 변환될 때 숨겨집니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Visible;
use Illuminate\Database\Eloquent\Model;

#[Visible(['first_name', 'last_name'])]
class User extends Model
{
    // ...
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 일시적으로 속성 표시 여부 수정하기

일반적으로 숨겨지는 일부 속성을 특정 모델 인스턴스에서 보이게 하려면 `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

마찬가지로, 일반적으로 보이는 일부 속성을 숨기고 싶다면 `makeHidden` 또는 `mergeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

표시되거나 숨겨지는 모든 속성을 일시적으로 재정의하려면 각각 `setVisible` 및 `setHidden` 메서드를 사용할 수 있습니다.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기 (Appending Values to JSON)

모델을 배열이나 JSON으로 변환할 때, 데이터베이스에 대응되는 컬럼이 없는 속성을 추가하고 싶을 때가 있습니다. 이를 위해 먼저 해당 값에 대한 [접근자](/docs/master/eloquent-mutators)를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

접근자가 항상 모델의 배열 및 JSON 표현에 추가되도록 하려면 모델에서 `Appends` 속성을 사용할 수 있습니다. 접근자의 PHP 메서드는 "camel case"로 정의되지만, 속성 이름은 일반적으로 직렬화된 표현인 "snake case"를 사용해 참조한다는 점에 유의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Appends;
use Illuminate\Database\Eloquent\Model;

#[Appends(['is_admin'])]
class User extends Model
{
    // ...
}
```

속성이 `appends` 목록에 추가되면 모델의 배열 및 JSON 표현에 모두 포함됩니다. `appends` 배열의 속성도 모델에 설정된 `visible` 및 `hidden` 설정을 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임에 추가하기

런타임에는 `append` 또는 `mergeAppends` 메서드를 사용하여 모델 인스턴스에 추가 속성을 덧붙이도록 지시할 수 있습니다. 또는 `setAppends` 메서드를 사용하여 특정 모델 인스턴스에 대해 추가되는 속성 전체 배열을 재정의할 수 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

마찬가지로, 모델에서 추가된 모든 속성을 제거하고 싶다면 `withoutAppends` 메서드를 사용할 수 있습니다.

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화 (Date Serialization)

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 형식 사용자 지정

`serializeDate` 메서드를 재정의하여 기본 직렬화 형식을 사용자 지정할 수 있습니다. 이 메서드는 날짜가 데이터베이스에 저장될 때의 형식에는 영향을 주지 않습니다.

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 형식 사용자 지정

모델의 [cast 선언](/docs/master/eloquent-mutators#attribute-casting)에 날짜 형식을 지정하여 개별 Eloquent 날짜 속성의 직렬화 형식을 사용자 지정할 수 있습니다.

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
