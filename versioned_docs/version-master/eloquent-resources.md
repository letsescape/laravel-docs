# Eloquent: API 리소스 (Eloquent: API Resources)

- [소개](#introduction)
- [리소스 생성](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성](#writing-resources)
    - [데이터 래핑](#data-wrapping)
    - [페이지네이션](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 연관관계](#conditional-relationships)
    - [메타데이터 추가](#adding-meta-data)
- [JSON:API 리소스](#jsonapi-resources)
    - [JSON:API 리소스 생성](#generating-jsonapi-resources)
    - [속성 정의](#defining-jsonapi-attributes)
    - [연관관계 정의](#defining-jsonapi-relationships)
    - [리소스 타입과 ID](#jsonapi-resource-type-and-id)
    - [희소 필드셋과 포함](#jsonapi-sparse-fieldsets-and-includes)
    - [링크와 메타](#jsonapi-links-and-meta)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개 (Introduction)

API를 만들 때는 Eloquent 모델과 애플리케이션 사용자에게 실제로 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어 일부 사용자에게만 특정 속성을 표시하고 다른 사용자에게는 표시하지 않거나, 모델의 JSON 표현에 특정 연관관계를 항상 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 쉽고 표현력 있게 변환할 수 있도록 해줍니다.

물론 Eloquent 모델이나 컬렉션은 언제든지 `toJson` 메서드를 사용해 JSON으로 변환할 수 있습니다. 하지만 Eloquent 리소스는 모델과 그 연관관계의 JSON 직렬화를 더 세밀하고 견고하게 제어할 수 있게 해줍니다.

<a name="generating-resources"></a>
## 리소스 생성 (Generating Resources)

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 배치됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다.

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스뿐만 아니라, 모델 컬렉션을 변환하는 역할을 하는 리소스도 생성할 수 있습니다. 이를 사용하면 JSON 응답에 특정 리소스의 전체 컬렉션과 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 만들려면 리소스를 생성할 때 `--collection` 플래그를 사용해야 합니다. 또는 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel은 컬렉션 리소스를 생성해야 한다고 판단합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다.

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

> [!NOTE]
> 이 내용은 리소스와 리소스 컬렉션에 대한 상위 수준의 개요입니다. 리소스가 제공하는 커스터마이징 기능과 강력함을 더 깊이 이해하려면 이 문서의 다른 섹션도 읽어보는 것을 적극 권장합니다.

리소스를 작성할 때 사용할 수 있는 모든 옵션을 자세히 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 큰 흐름부터 알아보겠습니다. 리소스 클래스는 JSON 구조로 변환해야 하는 단일 모델을 나타냅니다. 예를 들어 다음은 간단한 `UserResource` 리소스 클래스입니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```

모든 리소스 클래스는 `toArray` 메서드를 정의합니다. 이 메서드는 리소스가 라우트나 컨트롤러 메서드에서 응답으로 반환될 때 JSON으로 변환되어야 하는 속성 배열을 반환합니다.

`$this` 변수에서 모델 속성에 직접 접근할 수 있다는 점에 주목하세요. 이는 리소스 클래스가 편리한 접근을 위해 속성과 메서드 접근을 내부 모델로 자동 프록시하기 때문입니다. 리소스를 정의한 후에는 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스는 생성자를 통해 내부 모델 인스턴스를 받습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

편의를 위해 모델의 `toResource` 메서드를 사용할 수도 있습니다. 이 메서드는 프레임워크 규칙을 사용해 모델의 기본 리소스를 자동으로 찾아냅니다.

```php
return User::findOrFail($id)->toResource();
```

`toResource` 메서드를 호출하면 Laravel은 모델 이름과 일치하고, 선택적으로 `Resource` 접미사가 붙은 리소스를 모델의 네임스페이스에 가장 가까운 `Http\Resources` 네임스페이스 안에서 찾으려고 시도합니다.

리소스 클래스가 이 이름 지정 규칙을 따르지 않거나 다른 네임스페이스에 있다면, `UseResource` 속성을 사용해 모델의 기본 리소스를 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserResource;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResource;

#[UseResource(CustomUserResource::class)]
class User extends Model
{
    // ...
}
```

또는 `toResource` 메서드에 리소스 클래스를 전달해 지정할 수도 있습니다.

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스 컬렉션이나 페이지네이션된 응답을 반환하는 경우, 라우트나 컨트롤러에서 리소스 인스턴스를 만들 때 리소스 클래스가 제공하는 `collection` 메서드를 사용해야 합니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

또는 편의를 위해 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 규칙을 사용해 모델의 기본 리소스 컬렉션을 자동으로 찾아냅니다.

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면 Laravel은 모델 이름과 일치하고 `Collection` 접미사가 붙은 리소스 컬렉션을 모델의 네임스페이스에 가장 가까운 `Http\Resources` 네임스페이스 안에서 찾으려고 시도합니다.

리소스 컬렉션 클래스가 이 이름 지정 규칙을 따르지 않거나 다른 네임스페이스에 있다면, `UseResourceCollection` 속성을 사용해 모델의 기본 리소스 컬렉션을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserCollection;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResourceCollection;

#[UseResourceCollection(CustomUserCollection::class)]
class User extends Model
{
    // ...
}
```

또는 `toResourceCollection` 메서드에 리소스 컬렉션 클래스를 전달해 지정할 수도 있습니다.

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션

기본적으로 리소스 컬렉션은 컬렉션과 함께 반환해야 할 커스텀 메타데이터를 추가하는 기능을 제공하지 않습니다. 리소스 컬렉션 응답을 커스터마이징하려면 컬렉션을 나타내는 전용 리소스를 만들 수 있습니다.

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면, 응답에 포함해야 하는 메타데이터를 쉽게 정의할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<int|string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```

리소스 컬렉션을 정의한 후에는 라우트나 컨트롤러에서 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는 편의를 위해 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 규칙을 사용해 모델의 기본 리소스 컬렉션을 자동으로 찾아냅니다.

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면 Laravel은 모델 이름과 일치하고 `Collection` 접미사가 붙은 리소스 컬렉션을 모델의 네임스페이스에 가장 가까운 `Http\Resources` 네임스페이스 안에서 찾으려고 시도합니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존

라우트에서 리소스 컬렉션을 반환할 때 Laravel은 컬렉션의 키를 숫자 순서가 되도록 재설정합니다. 하지만 리소스 클래스에 `PreserveKeys` 속성을 사용해 컬렉션의 원래 키를 보존해야 하는지 지정할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Attributes\PreserveKeys;
use Illuminate\Http\Resources\Json\JsonResource;

#[PreserveKeys]
class UserResource extends JsonResource
{
    // ...
}
```

`preserveKeys` 속성이 `true`로 설정되면, 라우트나 컨트롤러에서 컬렉션을 반환할 때 컬렉션 키가 보존됩니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 내부 리소스 클래스 커스터마이징

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단일 리소스 클래스는 컬렉션 클래스 이름에서 끝의 `Collection` 부분을 제거한 이름으로 간주됩니다. 또한 개인적인 선호에 따라 단일 리소스 클래스에는 `Resource` 접미사가 붙을 수도 있고 붙지 않을 수도 있습니다.

예를 들어 `UserCollection`은 전달된 사용자 인스턴스를 `UserResource` 리소스로 매핑하려고 시도합니다. 이 동작을 커스터마이징하려면 리소스 컬렉션에 `Collects` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Attributes\Collects;
use Illuminate\Http\Resources\Json\ResourceCollection;

#[Collects(Member::class)]
class UserCollection extends ResourceCollection
{
    // ...
}
```

<a name="writing-resources"></a>
## 리소스 작성 (Writing Resources)

> [!NOTE]
> 아직 [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 계속 읽기 전에 먼저 읽어보는 것을 적극 권장합니다.

리소스는 주어진 모델을 배열로 변환하기만 하면 됩니다. 따라서 각 리소스에는 모델의 속성을 API에 적합한 배열로 변환하는 `toArray` 메서드가 포함됩니다. 이 배열은 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```

리소스가 정의되면 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 연관관계

응답에 관련 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드가 반환하는 배열에 해당 리소스를 추가할 수 있습니다. 이 예제에서는 `PostResource` 리소스의 `collection` 메서드를 사용해 사용자의 블로그 게시물을 리소스 응답에 추가합니다.

```php
use App\Http\Resources\PostResource;
use Illuminate\Http\Request;

/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->posts),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

> [!NOTE]
> 이미 로드된 경우에만 연관관계를 포함하고 싶다면 [조건부 연관관계](#conditional-relationships) 문서를 확인하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스가 단일 모델을 배열로 변환한다면, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 모든 Eloquent 모델 컬렉션은 즉석에서 "임시" 리소스 컬렉션을 생성하는 `toResourceCollection` 메서드를 제공하므로, 각 모델마다 리소스 컬렉션 클래스를 반드시 정의할 필요는 없습니다.

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

하지만 컬렉션과 함께 반환되는 메타데이터를 커스터마이징해야 한다면, 직접 리소스 컬렉션을 정의해야 합니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```
단일 리소스와 마찬가지로, 리소스 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는 편의를 위해 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 관례를 사용해 모델의 기반 리소스 컬렉션을 자동으로 찾습니다.

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면 Laravel은 모델의 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스 안에서, 모델 이름과 일치하고 뒤에 `Collection`이 붙은 리소스 컬렉션을 찾으려고 시도합니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로 최상위 리소스는 리소스 응답이 JSON으로 변환될 때 `data` 키로 감싸집니다. 예를 들어 일반적인 리소스 컬렉션 응답은 다음과 같습니다.

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ]
}
```

최상위 리소스 래핑을 비활성화하려면 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출해야 합니다. 일반적으로 이 메서드는 애플리케이션의 모든 요청에서 로드되는 `AppServiceProvider` 또는 다른 [서비스 프로바이더](/docs/master/providers)에서 호출해야 합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 주며, 직접 만든 리소스 컬렉션에 수동으로 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

리소스의 연관관계를 어떻게 래핑할지는 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션이 중첩 위치와 관계없이 `data` 키로 감싸지도록 하려면, 각 리소스마다 리소스 컬렉션 클래스를 정의하고 컬렉션을 `data` 키 안에서 반환해야 합니다.

이렇게 하면 최상위 리소스가 두 개의 `data` 키로 감싸지는지 궁금할 수 있습니다. 걱정하지 않아도 됩니다. Laravel은 리소스가 실수로 이중 래핑되지 않도록 처리하므로, 변환 중인 리소스 컬렉션의 중첩 수준을 신경 쓸 필요가 없습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return ['data' => $this->collection];
    }
}
```

<a name="data-wrapping-and-pagination"></a>
#### 데이터 래핑과 페이지네이션

페이지네이션된 컬렉션을 리소스 응답으로 반환할 때는 `withoutWrapping` 메서드가 호출되었더라도 Laravel이 리소스 데이터를 `data` 키로 감쌉니다. 페이지네이션된 응답에는 항상 paginator의 상태 정보를 담은 `meta` 키와 `links` 키가 포함되기 때문입니다.

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ],
    "links":{
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="pagination"></a>
### 페이지네이션

Laravel paginator 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는 편의를 위해 paginator의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 관례를 사용해 페이지네이션된 모델의 기반 리소스 컬렉션을 자동으로 찾습니다.

```php
return User::paginate()->toResourceCollection();
```

페이지네이션된 응답에는 항상 paginator의 상태 정보를 담은 `meta` 키와 `links` 키가 포함됩니다.

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ],
    "links":{
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="customizing-the-pagination-information"></a>
#### 페이지네이션 정보 커스터마이징

페이지네이션 응답의 `links` 키나 `meta` 키에 포함되는 정보를 커스터마이징하려면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 `$default` 정보 배열을 받습니다. `$default`는 `links` 키와 `meta` 키를 포함하는 배열입니다.

```php
/**
 * Customize the pagination information for the resource.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  array  $paginated
 * @param  array  $default
 * @return array
 */
public function paginationInformation($request, $paginated, $default)
{
    $default['links']['custom'] = 'https://example.com';

    return $default;
}
```

<a name="conditional-attributes"></a>
### 조건부 속성

때로는 특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어 현재 사용자가 "관리자"일 때만 값을 포함하고 싶을 수 있습니다. Laravel은 이런 상황을 돕기 위해 다양한 헬퍼 메서드를 제공합니다. `when` 메서드는 리소스 응답에 속성을 조건부로 추가할 때 사용할 수 있습니다.

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'secret' => $this->when($request->user()->isAdmin(), 'secret-value'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

이 예제에서 `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환하는 경우에만 최종 리소스 응답에 포함됩니다. 메서드가 `false`를 반환하면 `secret` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 만들 때 조건문을 직접 작성하지 않고도 리소스를 표현력 있게 정의할 수 있습니다.

`when` 메서드는 두 번째 인수로 클로저도 받을 수 있습니다. 이를 사용하면 주어진 조건이 `true`일 때만 결과 값을 계산할 수 있습니다.

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 기반 모델에 실제로 해당 속성이 존재하는 경우에만 속성을 포함할 때 사용할 수 있습니다.

```php
'name' => $this->whenHas('name'),
```

또한 `whenNotNull` 메서드는 속성이 null이 아닐 때만 리소스 응답에 속성을 포함하는 데 사용할 수 있습니다.

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

때로는 같은 조건에 따라 리소스 응답에 포함되어야 하는 속성이 여러 개 있을 수 있습니다. 이 경우 `mergeWhen` 메서드를 사용해 주어진 조건이 `true`일 때만 해당 속성을 응답에 포함할 수 있습니다.

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        $this->mergeWhen($request->user()->isAdmin(), [
            'first-secret' => 'value',
            'second-secret' => 'value',
        ]),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

마찬가지로 주어진 조건이 `false`이면, 이러한 속성은 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 섞인 배열 안에서 사용하면 안 됩니다. 또한 숫자 키가 순차적으로 정렬되어 있지 않은 배열 안에서도 사용하면 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성을 조건부로 로드하는 것뿐만 아니라, 모델에 연관관계가 이미 로드되어 있는지에 따라 리소스 응답에 연관관계를 조건부로 포함할 수 있습니다. 이렇게 하면 컨트롤러가 모델에 어떤 연관관계를 로드할지 결정하고, 리소스는 실제로 로드된 연관관계만 쉽게 포함할 수 있습니다. 결과적으로 리소스 안에서 "N+1" 쿼리 문제를 더 쉽게 피할 수 있습니다.

`whenLoaded` 메서드는 연관관계를 조건부로 로드할 때 사용할 수 있습니다. 불필요하게 연관관계를 로드하지 않기 위해, 이 메서드는 연관관계 자체가 아니라 연관관계의 이름을 받습니다.

```php
use App\Http\Resources\PostResource;

/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->whenLoaded('posts')),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

이 예제에서 연관관계가 로드되지 않았다면, `posts` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 개수

연관관계를 조건부로 포함하는 것뿐만 아니라, 모델에 연관관계의 "개수"가 로드되어 있는지에 따라 리소스 응답에 연관관계 개수를 조건부로 포함할 수 있습니다.

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 리소스 응답에 연관관계 개수를 조건부로 포함할 때 사용할 수 있습니다. 이 메서드는 연관관계 개수가 존재하지 않는 경우 속성을 불필요하게 포함하지 않도록 해줍니다.

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts_count' => $this->whenCounted('posts'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

이 예제에서 `posts` 연관관계의 개수가 로드되지 않았다면, `posts_count` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

`avg`, `sum`, `min`, `max` 같은 다른 유형의 집계도 `whenAggregated` 메서드를 사용해 조건부로 로드할 수 있습니다.

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보

리소스 응답에 연관관계 정보를 조건부로 포함하는 것뿐만 아니라, `whenPivotLoaded` 메서드를 사용해 다대다 연관관계의 중간 테이블에 있는 데이터를 조건부로 포함할 수 있습니다. `whenPivotLoaded` 메서드는 첫 번째 인수로 피벗 테이블의 이름을 받습니다. 두 번째 인수는 모델에서 피벗 정보를 사용할 수 있을 때 반환할 값을 반환하는 클로저여야 합니다.

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoaded('role_user', function () {
            return $this->pivot->expires_at;
        }),
    ];
}
```

연관관계가 [커스텀 중간 테이블 모델](/docs/master/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하고 있다면, 중간 테이블 모델의 인스턴스를 `whenPivotLoaded` 메서드의 첫 번째 인수로 전달할 수 있습니다.

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블이 `pivot`이 아닌 다른 접근자를 사용한다면 `whenPivotLoadedAs` 메서드를 사용할 수 있습니다.

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoadedAs('subscription', 'role_user', function () {
            return $this->subscription->expires_at;
        }),
    ];
}
```
<a name="adding-meta-data"></a>
### 메타데이터 추가

일부 JSON API 표준에서는 리소스와 리소스 컬렉션 응답에 메타데이터를 추가해야 합니다. 여기에는 리소스나 관련 리소스로 연결되는 `links`, 또는 리소스 자체에 대한 메타데이터가 포함되는 경우가 많습니다. 리소스에 대한 추가 메타데이터를 반환해야 한다면 `toArray` 메서드에 포함하십시오. 예를 들어 리소스 컬렉션을 변환할 때 `links` 정보를 포함할 수 있습니다.

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'data' => $this->collection,
        'links' => [
            'self' => 'link-value',
        ],
    ];
}
```

리소스에서 추가 메타데이터를 반환할 때, 페이지네이션된 응답을 반환할 때 Laravel이 자동으로 추가하는 `links` 또는 `meta` 키를 실수로 덮어쓸까 걱정할 필요는 없습니다. 직접 정의한 추가 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타데이터

때로는 반환되는 리소스 중 해당 리소스가 가장 바깥쪽 리소스일 때만 특정 메타데이터를 리소스 응답에 포함하고 싶을 수 있습니다. 일반적으로 여기에는 응답 전체에 대한 메타 정보가 포함됩니다. 이 메타데이터를 정의하려면 리소스 클래스에 `with` 메서드를 추가하십시오. 이 메서드는 리소스가 변환되는 가장 바깥쪽 리소스일 때만 리소스 응답에 포함할 메타데이터 배열을 반환해야 합니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return parent::toArray($request);
    }

    /**
     * Get additional data that should be returned with the resource array.
     *
     * @return array<string, mixed>
     */
    public function with(Request $request): array
    {
        return [
            'meta' => [
                'key' => 'value',
            ],
        ];
    }
}
```

<a name="adding-meta-data-when-constructing-resources"></a>
#### 리소스 생성 시 메타데이터 추가

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터를 추가할 수 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 리소스 응답에 추가할 데이터 배열을 인수로 받습니다.

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="jsonapi-resources"></a>
## JSON:API 리소스 (JSON:API Resources)

Laravel은 [JSON:API 명세](https://jsonapi.org/)를 준수하는 응답을 생성하는 리소스 클래스인 `JsonApiResource`를 제공합니다. 이 클래스는 표준 `JsonResource` 클래스를 확장하며 리소스 객체 구조, 연관관계, sparse fieldsets(스파스 필드셋), 포함 항목을 자동으로 처리하고, `Content-Type` 헤더를 `application/vnd.api+json`으로 설정합니다.

> [!NOTE]
> Laravel의 JSON:API 리소스는 응답의 직렬화를 처리합니다. 필터나 정렬처럼 들어오는 JSON:API 쿼리 파라미터도 파싱해야 한다면, [Spatie의 Laravel Query Builder](https://spatie.be/docs/laravel-query-builder/v6/introduction)가 훌륭한 보조 패키지입니다.

<a name="generating-jsonapi-resources"></a>
### JSON:API 리소스 생성

JSON:API 리소스를 생성하려면 `--json-api` 플래그와 함께 `make:resource` Artisan 명령어를 사용하십시오.

```shell
php artisan make:resource PostResource --json-api
```

생성된 클래스는 `Illuminate\Http\Resources\JsonApi\JsonApiResource`를 확장하며, 정의할 수 있도록 `$attributes`와 `$relationships` 속성이 포함됩니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

class PostResource extends JsonApiResource
{
    /**
     * The resource's attributes.
     */
    public $attributes = [
        // ...
    ];

    /**
     * The resource's relationships.
     */
    public $relationships = [
        // ...
    ];
}
```

JSON:API 리소스는 표준 리소스와 마찬가지로 라우트와 컨트롤러에서 반환할 수 있습니다.

```php
use App\Http\Resources\PostResource;
use App\Models\Post;

Route::get('/api/posts/{post}', function (Post $post) {
    return new PostResource($post);
});
```

또는 편의를 위해 모델의 `toResource` 메서드를 사용할 수 있습니다.

```php
Route::get('/api/posts/{post}', function (Post $post) {
    return $post->toResource();
});
```

그러면 JSON:API를 준수하는 응답이 생성됩니다.

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World",
            "body": "This is my first post."
        }
    }
}
```

JSON:API 리소스 컬렉션을 반환하려면 `collection` 메서드 또는 편의 메서드인 `toResourceCollection`을 사용하십시오.

```php
return PostResource::collection(Post::all());

return Post::all()->toResourceCollection();
```

<a name="defining-jsonapi-attributes"></a>
### 속성 정의

JSON:API 리소스에 포함할 속성을 정의하는 방법은 두 가지입니다.

가장 간단한 방법은 리소스에 `$attributes` 속성을 정의하는 것입니다. 속성 이름을 값으로 나열하면, 내부 모델에서 직접 읽어 옵니다.

```php
public $attributes = [
    'title',
    'body',
    'created_at',
];
```

또는 리소스 속성을 완전히 제어하려면 리소스에서 `toAttributes` 메서드를 오버라이드할 수 있습니다.

```php
/**
 * Get the resource's attributes.
 *
 * @return array<string, mixed>
 */
public function toAttributes(Request $request): array
{
    return [
        'title' => $this->title,
        'body' => $this->body,
        'is_published' => $this->published_at !== null,
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

<a name="defining-jsonapi-relationships"></a>
### 연관관계 정의

JSON:API 리소스는 JSON:API 명세를 따르는 연관관계 정의를 지원합니다. 연관관계는 클라이언트가 `include` 쿼리 파라미터를 통해 요청한 경우에만 직렬화됩니다.

#### `$relationships` 속성

리소스에 포함 가능한 연관관계는 `$relationships` 속성으로 정의할 수 있습니다.

```php
public $relationships = [
    'author',
    'comments',
];
```

연관관계 이름을 값으로 나열하면 Laravel은 해당 Eloquent 연관관계를 해석하고 적절한 리소스 클래스를 자동으로 찾아냅니다. 리소스 클래스를 명시적으로 지정해야 한다면 연관관계를 키 / 클래스 쌍으로 정의할 수 있습니다.

```php
use App\Http\Resources\UserResource;

public $relationships = [
    'author' => UserResource::class,
    'comments',
];
```

또는 리소스에서 `toRelationships` 메서드를 오버라이드할 수 있습니다.

```php
/**
 * Get the resource's relationships.
 */
public function toRelationships(Request $request): array
{
    return [
        'author' => UserResource::class,
        'comments',
    ];
}
```

#### 연관관계 포함

클라이언트는 `include` 쿼리 파라미터를 사용해 관련 리소스를 요청할 수 있습니다.

```
GET /api/posts/1?include=author,comments
```

그러면 `relationships` 키에는 리소스 식별자 객체가, 최상위 `included` 배열에는 전체 리소스 객체가 포함된 응답이 생성됩니다.

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "relationships": {
            "author": {
                "data": {
                    "id": "1",
                    "type": "users"
                }
            },
            "comments": {
                "data": [
                    {
                        "id": "1",
                        "type": "comments"
                    }
                ]
            }
        }
    },
    "included": [
        {
            "id": "1",
            "type": "users",
            "attributes": {
                "name": "Taylor Otwell"
            }
        },
        {
            "id": "1",
            "type": "comments",
            "attributes": {
                "body": "Great post!"
            }
        }
    ]
}
```

중첩된 연관관계는 점 표기법을 사용해 포함할 수 있습니다.

```
GET /api/posts/1?include=comments.author
```

<a name="jsonapi-relationship-depth"></a>
#### 연관관계 깊이

기본적으로 중첩된 연관관계 포함은 최대 깊이로 제한됩니다. 일반적으로 애플리케이션의 서비스 프로바이더 중 하나에서 `maxRelationshipDepth` 메서드를 사용해 이 제한을 사용자 지정할 수 있습니다.

```php
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

JsonApiResource::maxRelationshipDepth(3);
```

<a name="jsonapi-resource-type-and-id"></a>
### 리소스 타입과 ID

기본적으로 리소스의 `type`은 리소스 클래스 이름에서 파생됩니다. 예를 들어 `PostResource`는 `posts` 타입을 생성하고, `BlogPostResource`는 `blog-posts` 타입을 생성합니다. 리소스의 `id`는 모델의 기본 키에서 해석됩니다.

이 값을 사용자 지정해야 한다면 리소스에서 `toType`과 `toId` 메서드를 오버라이드할 수 있습니다.

```php
/**
 * Get the resource's type.
 */
public function toType(Request $request): string
{
    return 'articles';
}

/**
 * Get the resource's ID.
 */
public function toId(Request $request): string
{
    return (string) $this->uuid;
}
```

이 기능은 리소스 타입이 클래스 이름과 달라야 할 때 특히 유용합니다. 예를 들어 `AuthorResource`가 `User` 모델을 감싸지만 `authors` 타입을 출력해야 하는 경우가 그렇습니다.

<a name="jsonapi-sparse-fieldsets-and-includes"></a>
### 스파스 필드셋과 포함 항목

JSON:API 리소스는 [sparse fieldsets(스파스 필드셋)](https://jsonapi.org/format/#fetching-sparse-fieldsets)을 지원합니다. 이를 통해 클라이언트는 `fields` 쿼리 파라미터를 사용해 각 리소스 타입에 대해 특정 속성만 요청할 수 있습니다.

```
GET /api/posts?fields[posts]=title,created_at&fields[users]=name
```

이 경우 `posts` 리소스에는 `title`과 `created_at` 속성만 포함되고, `users` 리소스에는 `name` 속성만 포함됩니다.

<a name="jsonapi-ignoring-query-string"></a>
#### 쿼리 문자열 무시

특정 리소스 응답에서 sparse fieldset 필터링을 비활성화하려면 `ignoreFieldsAndIncludesInQueryString` 메서드를 호출할 수 있습니다.

```php
return $post->toResource()
    ->ignoreFieldsAndIncludesInQueryString();
```

<a name="jsonapi-including-previously-loaded-relationships"></a>
#### 이전에 로드된 연관관계 포함

기본적으로 연관관계는 `include` 쿼리 파라미터를 통해 요청된 경우에만 응답에 포함됩니다. 쿼리 문자열과 관계없이 이전에 eager load(즉시 로딩)된 모든 연관관계를 포함하려면 `includePreviouslyLoadedRelationships` 메서드를 호출할 수 있습니다.

```php
return $post->load('author', 'comments')
    ->toResource()
    ->includePreviouslyLoadedRelationships();
```

<a name="jsonapi-links-and-meta"></a>
### 링크와 메타

리소스에서 `toLinks`와 `toMeta` 메서드를 오버라이드하여 JSON:API 리소스 객체에 링크와 메타 정보를 추가할 수 있습니다.

```php
/**
 * Get the resource's links.
 */
public function toLinks(Request $request): array
{
    return [
        'self' => route('api.posts.show', $this->resource),
    ];
}

/**
 * Get the resource's meta information.
 */
public function toMeta(Request $request): array
{
    return [
        'readable_created_at' => $this->created_at->diffForHumans(),
    ];
}
```

그러면 응답의 리소스 객체에 `links`와 `meta` 키가 추가됩니다.
```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "links": {
            "self": "https://example.com/api/posts/1"
        },
        "meta": {
            "readable_created_at": "2 hours ago"
        }
    }
}
```

<a name="resource-responses"></a>
## 리소스 응답 (Resource Responses)

앞서 살펴본 것처럼, 리소스는 라우트와 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만 때로는 클라이언트로 전송되기 전에 나가는 HTTP 응답을 사용자 정의해야 할 수 있습니다. 이를 수행하는 방법은 두 가지가 있습니다. 먼저 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답의 헤더를 완전히 제어할 수 있습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return User::find(1)
        ->toResource()
        ->response()
        ->header('X-Value', 'True');
});
```

또는 리소스 자체 안에 `withResponse` 메서드를 정의할 수 있습니다. 이 메서드는 리소스가 응답의 최상위 리소스로 반환될 때 호출됩니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
        ];
    }

    /**
     * Customize the outgoing response for the resource.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```
