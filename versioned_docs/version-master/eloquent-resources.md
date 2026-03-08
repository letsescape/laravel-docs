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
    - [리소스 타입 및 ID](#jsonapi-resource-type-and-id)
    - [Sparse Fieldsets와 Include](#jsonapi-sparse-fieldsets-and-includes)
    - [링크와 메타](#jsonapi-links-and-meta)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때 Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 변환 계층이 필요한 경우가 있습니다. 예를 들어, 일부 사용자에게만 특정 속성을 보여주고 싶거나, 모델의 JSON 표현에 항상 특정 연관관계를 포함시키고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 변환하는 작업을 표현력 있게, 그리고 쉽게 할 수 있도록 도와줍니다.

물론, 언제든지 Eloquent 모델이나 컬렉션의 `toJson` 메서드를 사용해 JSON으로 변환할 수 있습니다. 하지만 Eloquent 리소스는 모델과 그 연관관계의 JSON 직렬화에 있어 훨씬 세밀하고 강력한 제어를 제공합니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면, `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉토리에 생성됩니다. 리소스 클래스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스뿐만 아니라, 모델 컬렉션 전체를 변환하는 역할을 하는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 해당 리소스 컬렉션 전체에 관련된 링크나 기타 메타 정보를 포함시킬 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스를 생성할 때 `--collection` 플래그를 사용하세요. 또는, 리소스 이름에 `Collection`이라는 단어를 포함시키면 Laravel이 컬렉션 리소스로 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이 절은 리소스와 리소스 컬렉션에 대한 대략적인 개요입니다. 리소스의 강력한 커스터마이징 기능에 대해 더 깊이 이해하고 싶다면 이 문서의 다른 절을 꼭 읽어보시기 바랍니다.

여러 옵션을 직접 사용해보기에 앞서, 우선 Laravel에서 리소스를 어떻게 활용하는지 간단히 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환이 필요한 단일 모델을 나타냅니다. 예를 들어, 아래와 같이 간단한 `UserResource` 리소스 클래스가 있습니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트나 컨트롤러 메서드에서 리소스가 응답으로 반환될 때 JSON으로 변환되어야 할 속성의 배열을 반환합니다.

모델의 속성에는 `$this` 변수를 통해 직접 접근이 가능합니다. 리소스 클래스가 속성과 메서드 접근을 내부 모델로 프록시 처리하기 때문입니다. 리소스를 정의했다면, 이제 라우트나 컨트롤러에서 해당 리소스를 반환할 수 있습니다. 리소스는 생성자에 모델 인스턴스를 받습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

더 편하게는 모델의 `toResource` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크의 규칙을 따라 자동으로 해당 모델의 리소스를 찾아 반환합니다:

```php
return User::findOrFail($id)->toResource();
```

`toResource` 메서드를 호출하면, Laravel은 모델의 이름과 일치하며, (필요 시) `Resource`로 끝나는 리소스 클래스를 모델 네임스페이스와 가까운 `Http\Resources` 네임스페이스에서 찾으려고 시도합니다.

만약 리소스 클래스가 이 명명 규칙을 따르지 않거나, 다른 네임스페이스에 위치한다면, 모델에 `UseResource` 속성을 사용해 기본 리소스를 지정할 수 있습니다:

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

또는, `toResource` 메서드에 리소스 클래스를 직접 지정할 수도 있습니다:

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
### 리소스 컬렉션

여러 개의 리소스나 페이지네이션된 결과를 반환할 때는, 라우트나 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용해야 합니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

혹은 더 간편하게, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 프레임워크는 규칙을 따라 자동으로 적절한 리소스 컬렉션을 찾아 반환합니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection`으로 끝나는 리소스 컬렉션 클래스를 모델 네임스페이스와 가까운 `Http\Resources` 네임스페이스에서 찾으려고 시도합니다.

리소스 컬렉션 클래스가 이 명명 규칙을 따르지 않거나, 다른 네임스페이스에 있다면, 모델에 `UseResourceCollection` 속성을 사용해 기본 리소스 컬렉션을 지정할 수 있습니다:

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

또는, `toResourceCollection` 메서드에 리소스 컬렉션 클래스를 직접 지정할 수도 있습니다:

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션

기본적으로 리소스 컬렉션은 컬렉션과 함께 반환되어야 할 커스텀 메타데이터를 추가할 수 없습니다. 컬렉션 응답을 커스터마이징하고 싶다면, 컬렉션 자체를 표현하는 전용 리소스를 생성하세요:

```shell
php artisan make:resource UserCollection
```

생성된 리소스 컬렉션 클래스에서 응답에 포함할 메타데이터를 쉽게 정의할 수 있습니다:

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

리소스 컬렉션을 정의한 후에는, 이를 라우트나 컨트롤러에서 그대로 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수도 있습니다. 이 경우도 프레임워크가 규칙에 따라 자동으로 리소스 컬렉션을 찾아 사용합니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection`으로 끝나는 리소스 컬렉션 클래스를 해당 네임스페이스에서 찾으려고 시도합니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존

리소스 컬렉션을 라우트에서 반환하면, Laravel은 기본적으로 컬렉션의 키를 숫자 순서대로 다시 설정합니다. 하지만, 리소스 클래스에 `PreserveKeys` 속성을 지정하여 원본 컬렉션의 키를 유지할 수 있습니다:

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

`preserveKeys` 속성을 `true`로 지정하면, 라우트나 컨트롤러에서 컬렉션을 반환할 때 컬렉션의 키가 그대로 보존됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 내부 리소스 클래스 커스터마이즈

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 리소스 클래스로 매핑한 결과로 자동 채워집니다. 이때, 단수형 리소스 클래스는 컬렉션 클래스명에서 끝단 `Collection`만 제거한 형태로 추정됩니다. 또한, 개인 취향에 따라 단수형 리소스 클래스는 `Resource`로 끝날 수도, 아닐 수도 있습니다.

예를 들어, `UserCollection`은 각 사용자 인스턴스를 `UserResource`로 매핑하려고 시도합니다. 만약 이 동작을 커스터마이즈하고 싶다면, 리소스 컬렉션에 `Collects` 속성을 사용하세요:

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
## 리소스 작성

> [!NOTE]
> [개념 개요](#concept-overview) 절을 먼저 읽어보시길 권장합니다. 이 절은 그 이후에 읽는 것이 이해에 도움이 됩니다.

리소스는 주어진 모델을 배열 형태로 변환하는 역할만 합니다. 따라서 각 리소스는 모델의 속성을 API 친화적인 배열로 변환하기 위한 `toArray` 메서드를 가지고 있으며, 이를 통해 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있습니다:

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

리소스를 정의한 후에는 라우트 또는 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 연관관계

응답에 관련 리소스를 포함하고 싶다면, `toArray` 메서드에서 반환하는 배열에 연관 데이터를 추가할 수 있습니다. 아래 예시에서는 사용자의 블로그 포스트들을 `PostResource` 리소스의 `collection` 메서드를 활용하여 포함합니다:

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
> 연관관계를 이미 로드한 경우에만 포함하고 싶다면 [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 여러 모델(컬렉션 전체)을 배열로 변환합니다. 하지만 모든 모델마다 리소스 컬렉션 클래스를 반드시 정의할 필요는 없습니다. Eloquent 모델 컬렉션은 `toResourceCollection` 메서드를 제공하여 "임시" 리소스 컬렉션을 바로 생성할 수 있습니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

하지만 컬렉션 응답에 메타데이터 등을 커스터마이즈 해야 한다면, 직접 리소스 컬렉션 클래스를 정의해야 합니다:

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

단일 리소스와 마찬가지로, 리소스 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection`으로 끝나는 리소스 컬렉션 클래스를 해당 네임스페이스에서 찾으려고 시도합니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로 가장 바깥쪽 리소스 응답은 JSON으로 변환될 때 `data` 키로 래핑됩니다. 예를 들어, 보통의 리소스 컬렉션 응답은 다음과 같습니다:

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

만약 바깥쪽 리소스의 래핑을 비활성화하고 싶다면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에 대해 `withoutWrapping` 메서드를 호출해야 합니다. 일반적으로 이 방법은 `AppServiceProvider`나, 애플리케이션의 모든 요청에서 항상 로딩되는 [서비스 프로바이더](/docs/master/providers) 내에서 호출하는 것이 좋습니다:

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
> `withoutWrapping` 메서드는 가장 바깥쪽 응답에만 영향을 미치며, 직접 리소스 컬렉션에서 수동으로 추가한 `data` 키는 제거해주지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

리소스의 연관관계가 어떻게 래핑될지 자유롭게 결정할 수 있습니다. 중첩 여부와 상관없이 모든 리소스 컬렉션을 `data` 키로 래핑하려면, 리소스마다 컬렉션 클래스를 별도로 정의하고 반환값을 `data` 키에 넣으세요.

혹시 이렇게 하면 바깥쪽 리소스가 `data` 키로 두 번 래핑되지 않을까 걱정할 수 있지만, Laravel은 절대 리소스가 중복으로 래핑되는 일이 없도록 처리하므로 중첩 수준에 관계없이 안심하고 코드를 작성할 수 있습니다:

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

페이지네이션된 컬렉션을 리소스 응답으로 반환할 때는, `withoutWrapping` 메서드가 호출되었더라도 Laravel이 항상 `data` 키로 리소스 데이터를 감쌉니다. 이는 페이지네이터의 상태를 담는 `meta`, `links` 키가 항상 포함되기 때문입니다:

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

Laravel 페이지네이터 인스턴스를 리소스의 `collection` 메서드에 전달하거나, 커스텀 리소스 컬렉션에 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는 페이지네이터의 `toResourceCollection` 메서드를 사용하면, 페이지네이션된 모델의 관련 리소스 컬렉션을 자동으로 찾아 반환합니다:

```php
return User::paginate()->toResourceCollection();
```

페이지네이션 응답은 항상 `meta` 및 `links` 키를 포함하여 페이지네이터 상태를 반환합니다:

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
#### 페이지네이션 정보 커스터마이즈

페이지네이션 응답의 `links`나 `meta` 키에 포함되는 정보를 커스터마이즈하려면, 리소스에 `paginationInformation` 메서드를 추가하세요. 이 메서드는 `$paginated` 데이터와, `links` 및 `meta` 키가 포함된 `$default` 정보를 인자로 받습니다:

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

특정 조건에 따라 리소스 응답에 속성을 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 경우에만 값을 포함하고 싶을 수 있습니다. 이러한 상황을 도와주는 다양한 헬퍼 메서드가 Laravel에 제공됩니다. `when` 메서드를 사용하여 조건부로 속성을 응답에 추가할 수 있습니다:

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

위 예시에서 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 `secret` 키가 최종 리소스 응답에 포함됩니다. `false`라면 `secret` 키는 클라이언트로 전송되기 전에 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 구성할 때 조건문을 쓰지 않고도 리소스를 효과적으로 정의할 수 있습니다.

`when` 메서드의 두 번째 인자로 클로저를 전달하면, 조건이 `true`일 때만 값을 계산할 수 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 해당 속성이 실제로 모델에 존재할 때만 포함시킵니다:

```php
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드는 해당 속성이 null이 아닐 때만 포함시킵니다:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

여러 속성이 동일한 조건에 따라 포함되어야 할 때는 `mergeWhen` 메서드를 사용하여, 조건이 `true`일 때만 그룹으로 응답에 포함할 수 있습니다:

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

마찬가지로 조건이 `false`라면 해당 속성들은 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열과 숫자 키가 혼합된 배열이나, 순차적으로 정렬되지 않은 숫자 키 배열 내부에서는 사용하지 않아야 합니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성뿐만 아니라, 모델에 연관관계가 이미 로드되었을 때만 리소스 응답에 포함시킬 수도 있습니다. 이를 통해 컨트롤러가 어떤 연관관계를 로드할지 결정하고, 리소스 클래스에서는 실제로 로드된 것만 간단하게 포함할 수 있습니다. 이 방식은 리소스 내부에서 "N+1" 쿼리 문제를 예방하는 데도 도움이 됩니다.

`whenLoaded` 메서드는 연관관계가 실제로 모델에 로드되어 있는 경우에만 응답 배열에 포함시켜줍니다. 불필요한 쿼리가 발생하지 않도록, 연관관계 자체가 아니라 이름을 전달해야 합니다:

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

예시에서, 해당 연관관계가 로드되지 않았다면, `posts` 키는 클라이언트로 전송되기 전에 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 카운트

연관관계뿐만 아니라, 연관관계의 "카운트"도 로드 여부에 따라 조건부로 포함시킬 수 있습니다:

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드를 사용하면, 연관관계의 카운트가 모델에 로드되어 있을 때만 리소스 응답에 포함됩니다. 카운트가 없다면, 해당 키는 응답에서 제거됩니다:

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

이외에도, `avg`, `sum`, `min`, `max` 등 다양한 집계 정보도 `whenAggregated` 메서드를 사용해 조건부로 포함시킬 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보

연관관계 정보뿐 아니라, 다대다(many-to-many) 관계의 중간(pivot) 테이블 데이터를 조건부로 응답에 포함시킬 수도 있습니다. 이를 위해 `whenPivotLoaded` 메서드를 사용합니다. 첫 번째 인자로 피벗 테이블 이름을, 두 번째 인자로는 피벗 정보가 존재할 때 반환할 값을 생성하는 클로저를 넘깁니다:

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

연관관계가 [커스텀 중간 테이블 모델](/docs/master/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, 첫 번째 인자로 중간 테이블 모델 인스턴스를 전달할 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

만약 피벗 테이블의 accessor가 `pivot`이 아니라면, `whenPivotLoadedAs` 메서드를 사용할 수 있습니다:

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

일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타데이터를 추가하도록 요구합니다. 여기에는 리소스 자신 또는 관련 리소스에 대한 `links`나, 리소스 자체에 대한 정보가 포함될 수 있습니다. 리소스에 추가 메타데이터가 필요하다면, 이를 `toArray` 메서드 내에 포함시킬 수 있습니다. 예를 들어, 리소스 컬렉션을 변환할 때 `links` 정보를 포함시킬 수 있습니다:

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

추가 메타데이터가 포함된 경우, 페이지네이션 응답에서 Laravel이 자동으로 추가하는 `links`나 `meta` 키와 충돌하지 않습니다. 직접 정의한 `links`는 페이지네이터가 제공하는 링크와 병합되어 반환됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타데이터

때때로, 오직 최상위 리소스 응답에만 특정 메타데이터를 포함하고 싶을 때가 있습니다. 주로 응답 전체에 관한 정보를 포함할 때 사용합니다. 이를 위해 리소스 클래스에 `with` 메서드를 추가하면 됩니다. 이 메서드는 변환되는 리소스가 최상위 리소스일 때에만 포함할 메타데이터의 배열을 반환해야 합니다:

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

라우트나 컨트롤러에서 리소스를 생성할 때, 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 리소스 응답에 포함할 데이터를 배열로 받습니다:

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="jsonapi-resources"></a>
## JSON:API 리소스

Laravel은 [JSON:API 스펙](https://jsonapi.org/)을 준수하는 응답을 생성하는 `JsonApiResource` 리소스 클래스를 제공합니다. 이 클래스는 표준 `JsonResource`를 확장하며, 리소스 오브젝트 구조, 연관관계, sparse fieldsets, include 파라미터 관리, `Content-Type` 헤더(`application/vnd.api+json`) 자동 설정까지 처리합니다.

> [!NOTE]
> Laravel의 JSON:API 리소스는 응답 직렬화만 담당합니다. 필터나 정렬 등 JSON:API 쿼리 파라미터 파싱이 필요하다면, [Spatie의 Laravel Query Builder](https://spatie.be/docs/laravel-query-builder/v6/introduction) 패키지 사용을 추천합니다.

<a name="generating-jsonapi-resources"></a>
### JSON:API 리소스 생성

JSON:API 리소스를 생성하려면 `make:resource` Artisan 명령어에 `--json-api` 플래그를 추가하세요:

```shell
php artisan make:resource PostResource --json-api
```

생성된 클래스는 `Illuminate\Http\Resources\JsonApi\JsonApiResource`를 확장하며, 속성 및 연관관계를 정의하는 `$attributes`, `$relationships` 프로퍼티가 이미 포함되어 있습니다:

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

JSON:API 리소스는 표준 리소스처럼 라우트와 컨트롤러에서 반환할 수 있습니다:

```php
use App\Http\Resources\PostResource;
use App\Models\Post;

Route::get('/api/posts/{post}', function (Post $post) {
    return new PostResource($post);
});
```

혹은 모델의 `toResource` 메서드를 사용할 수도 있습니다:

```php
Route::get('/api/posts/{post}', function (Post $post) {
    return $post->toResource();
});
```

그러면 다음과 같은 JSON:API 스펙을 준수한 응답이 반환됩니다:

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

JSON:API 리소스 컬렉션을 반환하려면, `collection` 또는 `toResourceCollection` 메서드를 사용하세요:

```php
return PostResource::collection(Post::all());

return Post::all()->toResourceCollection();
```

<a name="defining-jsonapi-attributes"></a>
### 속성 정의

JSON:API 리소스에 포함할 속성을 정의하는 방법은 두 가지가 있습니다.

가장 간단한 방법은 리소스에서 `$attributes` 프로퍼티에 속성명을 나열하는 것입니다. 값은 내부 모델에서 직접 읽어옵니다:

```php
public $attributes = [
    'title',
    'body',
    'created_at',
];
```

좀 더 세밀하게 속성을 제어하고 싶다면, 리소스의 `toAttributes` 메서드를 오버라이드할 수 있습니다:

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

JSON:API 리소스는 JSON:API 스펙에 따라 연관관계도 정의할 수 있습니다. 연관관계는 클라이언트가 `include` 쿼리 파라미터로 요청할 때에만 직렬화됩니다.

#### `$relationships` 프로퍼티

리소스에서 `$relationships` 프로퍼티에 포함 가능한 연관관계를 나열합니다:

```php
public $relationships = [
    'author',
    'comments',
];
```

값에 연관관계 이름을 나열하면 Laravel이 해당 Eloquent 연관관계를 찾아 적절한 리소스 클래스를 자동으로 추론합니다. 별도의 리소스 클래스를 지정하고 싶다면, 키/클래스 쌍의 형태로 지정할 수 있습니다:

```php
use App\Http\Resources\UserResource;

public $relationships = [
    'author' => UserResource::class,
    'comments',
];
```

또는, `toRelationships` 메서드를 오버라이드할 수 있습니다:

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

#### 연관관계 Include

클라이언트는 `include` 쿼리 파라미터를 사용해 관련 리소스를 요청할 수 있습니다:

```
GET /api/posts/1?include=author,comments
```

이렇게 하면 `relationships` 키에 리소스 식별자 오브젝트가, 상위 `included` 배열에는 실제 리소스 오브젝트가 포함됩니다:

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

중첩된 연관관계도 dot notation을 사용해 요청할 수 있습니다:

```
GET /api/posts/1?include=comments.author
```

<a name="jsonapi-relationship-depth"></a>
#### 연관관계 깊이 제한

기본적으로 중첩 연관관계 include의 깊이는 최대값이 제한되어 있습니다. 이 한계를 변경하고 싶다면, 보통 서비스 프로바이더에서 `maxRelationshipDepth` 메서드를 설정하세요:

```php
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

JsonApiResource::maxRelationshipDepth(3);
```

<a name="jsonapi-resource-type-and-id"></a>
### 리소스 타입 및 ID

기본적으로 리소스의 `type`은 리소스 클래스 이름에서 유추합니다. 예를 들어, `PostResource`는 `posts` 타입, `BlogPostResource`는 `blog-posts` 타입입니다. ID는 모델의 기본키에서 가져옵니다.

만약 이 값을 커스터마이징해야 한다면, 리소스의 `toType` 및 `toId` 메서드를 오버라이드하세요:

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

이 기능은 `AuthorResource`가 `User` 모델을 감싸면서 실제로는 타입을 `authors`로 출력해야 할 때 등 유용하게 쓰입니다.

<a name="jsonapi-sparse-fieldsets-and-includes"></a>
### Sparse Fieldsets와 Include

JSON:API 리소스는 [sparse fieldsets](https://jsonapi.org/format/#fetching-sparse-fieldsets)을 지원합니다. 클라이언트는 `fields` 쿼리 파라미터를 통해 리소스 타입별로 속성만 특정할 수 있습니다:

```
GET /api/posts?fields[posts]=title,created_at&fields[users]=name
```

이렇게 하면 `posts` 리소스는 `title`, `created_at`만, `users` 리소스는 `name` 속성만 응답에 포함됩니다.

<a name="jsonapi-ignoring-query-string"></a>
#### 쿼리스트링 무시

특정 리소스 응답에 대해 sparse fieldset 필터링을 비활성화하려면, `ignoreFieldsAndIncludesInQueryString` 메서드를 호출하세요:

```php
return $post->toResource()
    ->ignoreFieldsAndIncludesInQueryString();
```

<a name="jsonapi-including-previously-loaded-relationships"></a>
#### 미리 로드된 연관관계 포함

기본적으로 연관관계는 쿼리문자열의 `include` 파라미터로만 응답에 포함됩니다. 이미 eager load된 모든 연관관계를 쿼리스트링과 관계없이 응답에 포함시키려면, `includePreviouslyLoadedRelationships` 메서드를 호출하세요:

```php
return $post->load('author', 'comments')
    ->toResource()
    ->includePreviouslyLoadedRelationships();
```

<a name="jsonapi-links-and-meta"></a>
### 링크와 메타

JSON:API 리소스 오브젝트에 링크 및 메타 정보를 추가하려면, 리소스 클래스에서 `toLinks`, `toMeta` 메서드를 오버라이드하세요:

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

이렇게 하면 응답의 리소스 오브젝트에 `links`, `meta` 키가 추가되어 다음과 같이 표현됩니다:

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
## 리소스 응답

지금까지 살펴본 것처럼, 리소스는 라우트와 컨트롤러에서 바로 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만, HTTP 응답이 클라이언트로 전송되기 전에 헤더 등 응답을 커스터마이징해야 할 수도 있습니다. 이를 위해 두 가지 방법이 있습니다. 첫째는, 리소스에 `response` 메서드를 체이닝해 사용하는 방법입니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답 헤더를 직접 제어할 수 있습니다:

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

또는, 리소스 내부에 `withResponse` 메서드를 정의해 사용할 수 있습니다. 이 메서드는 해당 리소스가 최상위 리소스로 응답될 때 호출됩니다:

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