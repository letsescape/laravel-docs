# Eloquent: 직렬화 (Eloquent: Serialization)

- [소개](#introduction)
- [모델 및 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화하기](#serializing-to-arrays)
    - [JSON으로 직렬화하기](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel로 API를 구축할 때, 모델과 연관관계를 배열 또는 JSON으로 변환해야 할 일이 자주 있습니다. Eloquent는 이런 변환을 간편하게 처리할 수 있는 여러 메서드와, 직렬화된 모델에서 어떤 속성을 포함할지 제어할 수 있는 기능을 제공합니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 훨씬 더 강력하게 제어하고 싶다면, [Eloquent API 리소스](/docs/master/eloquent-resources) 문서를 참조하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화 (Serializing Models and Collections)

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기 (Serializing to Arrays)

모델과 로드된 [연관관계](/docs/master/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용합니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 모든 연관관계(그리고 연관관계의 연관관계까지)도 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

모델의 속성만 배열로 변환하고 연관관계는 포함하지 않으려면 `attributesToArray` 메서드를 사용할 수 있습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

[컬렉션](/docs/master/eloquent-collections) 전체를 배열로 변환하려면, 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기 (Serializing to JSON)

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`와 마찬가지로, `toJson` 메서드도 재귀적으로 동작해 모든 속성과 연관관계를 JSON으로 변환합니다. 또한, [PHP에서 지원하는](https://secure.php.net/manual/en/function.json-encode.php) 모든 JSON 인코딩 옵션을 지정할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는, 모델이나 컬렉션을 문자열로 캐스팅하면 `toJson` 메서드가 자동으로 호출됩니다.

```php
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 변환될 때 자동으로 JSON으로 직렬화되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. 라라벨은 라우트 또는 컨트롤러에서 반환되는 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

#### 연관관계 (Relationships)

Eloquent 모델이 JSON으로 변환될 때 로드된 연관관계는 자동으로 JSON 객체의 속성으로 포함됩니다. 또한, Eloquent 연관관계 메서드는 "카멜 케이스(camel case)"로 정의되지만, 연관관계의 JSON 속성명은 "스네이크 케이스(snake case)"로 변환되어 표시됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기 (Hiding Attributes From JSON)

때로는 비밀번호처럼 특정 속성이 모델의 배열 및 JSON 표현에서 제외되길 원할 수 있습니다. 이럴 경우, 모델에 `Hidden` 어트리뷰트를 사용하면 됩니다. `Hidden` 어트리뷰트에 나열된 속성은 직렬화된 모델에 포함되지 않습니다.

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
> 연관관계도 숨기려면 Eloquent 모델의 `Hidden` 어트리뷰트에 연관관계의 메서드명을 추가하면 됩니다.

또는, `Visible` 어트리뷰트를 사용해 모델 배열 및 JSON 표현에 포함시킬 속성의 "허용 목록"을 정의할 수 있습니다.  `Visible` 어트리뷰트에 포함되지 않은 모든 속성은 배열 또는 JSON에서 숨겨집니다.

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

#### 속성 가시성 임시 변경하기

일반적으로 숨겨진 속성을 특정 모델 인스턴스에서만 보이도록 하고 싶다면 `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

반대로, 일반적으로 보이는 속성을 일시적으로 숨기고 싶을 때는 `makeHidden`이나 `mergeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

모든 visible 또는 hidden 속성을 임시로 완전히 덮어쓰고 싶다면 각각 `setVisible`, `setHidden` 메서드를 사용할 수 있습니다.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기 (Appending Values to JSON)

때로는, 모델을 배열이나 JSON으로 변환할 때 데이터베이스 컬럼에 존재하지 않는 속성을 추가하고 싶을 수 있습니다. 이럴 때 먼저 해당 값에 대한 [접근자(Accessor)](/docs/master/eloquent-mutators)를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자(admin)인지 여부를 확인합니다.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

접근자를 항상 모델의 배열 및 JSON 표현에 포함시키고 싶다면, 모델에 `Appends` 어트리뷰트를 사용합니다. 접근자 PHP 메서드는 "카멜 케이스"로 정의되더라도, 속성명은 "스네이크 케이스"로 작성된 직렬화 이름을 사용해야 합니다.

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

`appends` 목록에 해당 속성을 추가하면, 모델의 배열 및 JSON 표현 모두에 포함됩니다. `appends` 배열 내 속성도 모델에서 지정한 `visible`, `hidden` 설정이 적용됩니다.

#### 런타임에 값 추가하기

실행 중에 추가적인 속성을 모델 인스턴스에 덧붙이고 싶다면 `append` 또는 `mergeAppends` 메서드를 사용할 수 있습니다. `setAppends` 메서드를 사용하면 지정한 모델 인스턴스에 대해 모든 추가 속성 배열을 덮어쓸 수도 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

반대로, 모델에서 모든 추가 속성을 제거하고 싶다면 `withoutAppends` 메서드를 사용합니다.

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화 (Date Serialization)

#### 기본 날짜 포맷 커스터마이즈하기

기본 직렬화 날짜 포맷을 변경하고 싶다면, `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 저장되는 날짜 포맷에는 영향을 주지 않습니다.

```php
/**
 * 배열 / JSON 직렬화용 날짜 포맷 처리
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

#### 개별 속성별 날짜 포맷 커스터마이즈하기

Eloquent의 개별 날짜 속성 직렬화 포맷을 변경하려면 모델의 [cast 선언](/docs/master/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정할 수 있습니다.

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
