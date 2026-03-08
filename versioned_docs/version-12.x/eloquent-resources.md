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
    - [메타 데이터 추가](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때, Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 위치하는 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자 집합에 대해서만 일부 속성을 노출하거나, 항상 특정 연관관계를 모델의 JSON 표현에 포함하고 싶을 때가 있습니다. Eloquent의 리소스 클래스는 이러한 모델과 모델 컬렉션을 JSON으로 변환하는 과정을 더욱 표현력 있고 쉽게 처리할 수 있도록 해줍니다.

물론, Eloquent 모델 또는 컬렉션의 `toJson` 메서드를 사용하여 언제든지 JSON으로 변환할 수 있습니다. 그러나 Eloquent 리소스는 모델과 그 연관관계의 JSON 직렬화에 대해 더 세밀하고 강력한 제어를 제공합니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용하면 됩니다. 기본적으로 생성된 리소스는 애플리케이션의 `app/Http/Resources` 디렉토리에 위치하게 됩니다. 리소스 클래스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 외에도, 모델의 컬렉션을 변환하는 역할을 하는 리소스도 생성할 수 있습니다. 이를 통해 응답되는 JSON에 해당 리소스 전체 컬렉션에 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스를 생성할 때 `--collection` 플래그를 사용해야 합니다. 또는 리소스 이름에 `Collection`이라는 단어를 포함시키면, Laravel은 이를 컬렉션 리소스로 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이 부분은 리소스 및 리소스 컬렉션의 고수준 개요입니다. 리소스가 제공하는 커스터마이징과 강력한 기능을 더 깊이 이해하려면 문서의 다른 섹션도 꼭 읽어보시기 바랍니다.

리소스를 직접 작성하는 다양한 방법을 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 간단히 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 클래스입니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 해당 리소스가 라우트나 컨트롤러 메서드에서 응답으로 반환될 때 JSON으로 변환되어야 할 속성의 배열을 반환합니다.

여기서 `$this` 변수로 모델의 속성에 바로 접근할 수 있다는 점에 주목하세요. 이는 리소스 클래스가 속성 및 메서드 접근을 자동으로 하위 모델로 프록시하기 때문에 가능한 일입니다. 이렇게 정의된 리소스는 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스 생성자에는 변환할 모델 인스턴스를 넣으면 됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

편의상, 모델의 `toResource` 메서드를 사용할 수도 있습니다. 이 메서드는 프레임워크 규칙에 따라 해당 모델에서 사용할 수 있는 리소스를 자동으로 찾습니다:

```php
return User::findOrFail($id)->toResource();
```

`toResource` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Resource`로 끝나는 리소스를 해당 모델 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스에서 찾으려 시도합니다.

만약 리소스 클래스가 이 네이밍 규칙을 따르지 않거나, 다른 네임스페이스에 위치한다면, 모델에 `UseResource` 속성을 사용하여 기본 리소스를 지정할 수 있습니다:

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

또는, `toResource` 메서드에 리소스 클래스를 직접 전달하여 사용할 수도 있습니다:

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스들의 컬렉션이나 페이지네이션된 응답을 반환하는 경우, 라우트나 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용하여 리소스 인스턴스를 생성해야 합니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

또는, 편의상 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수도 있으며, 이 메서드는 프레임워크 규칙에 따라 해당 모델의 기본 리소스 컬렉션을 자동으로 찾습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection`으로 끝나는 리소스 컬렉션을 해당 모델 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스에서 찾으려 시도합니다.

리소스 컬렉션 클래스가 이 규칙을 따르지 않거나 다른 네임스페이스에 위치한다면, 모델에 `UseResourceCollection` 속성을 정의하여 지정할 수 있습니다:

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

또는, `toResourceCollection` 메서드에 리소스 컬렉션 클래스를 직접 전달해 사용할 수 있습니다:

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션

기본적으로 리소스 컬렉션은 추가적인 커스텀 메타 데이터를 반환할 수 없습니다. 컬렉션과 함께 반환해야 하는 메타 데이터를 커스터마이징하고 싶을 때에는, 전용 리소스 컬렉션 클래스를 생성해야 합니다:

```shell
php artisan make:resource UserCollection
```

생성된 리소스 컬렉션 클래스에서 응답에 포함시킬 메타 데이터를 쉽게 정의할 수 있습니다:

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

커스텀 리소스 컬렉션을 정의한 후, 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

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

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection`으로 끝나는 리소스 컬렉션을 해당 모델 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스에서 찾으려 시도합니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 기본적으로 컬렉션의 키를 숫자 순서대로 재정렬합니다. 그러나 원래의 컬렉션 키를 그대로 유지하려면, 리소스 클래스에 `preserveKeys` 속성을 추가하면 됩니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Indicates if the resource's collection keys should be preserved.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys` 속성을 `true`로 설정하면, 컬렉션이 라우트나 컨트롤러에서 반환될 때 컬렉션의 키가 유지됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이징

보통, 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 아이템을 단수형 리소스 클래스에 매핑한 결과로 자동 세팅됩니다. 단수형 리소스 클래스는 컬렉션 클래스의 이름에서 마지막 `Collection` 부분을 제외한 이름으로 추정됩니다. 추가적으로, 단수형 리소스 클래스 이름에는 `Resource` 접미사가 붙거나 붙지 않을 수 있습니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스들을 `UserResource` 리소스로 매핑합니다. 이 동작을 커스터마이징하려면, 컬렉션 리소스의 `$collects` 속성을 오버라이드하면 됩니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * The resource that this resource collects.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성

> [!NOTE]
> 아직 [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 계속 읽기 전에 먼저 해당 내용을 살펴볼 것을 권장합니다.

리소스는 주어진 모델을 배열로 변환하기만 하면 됩니다. 즉, 각 리소스에는 모델의 속성을 API에 적합한 배열 형태로 변환하는 `toArray` 메서드가 포함되어 있으며, 이 배열은 애플리케이션의 라우트나 컨트롤러에서 반환될 수 있습니다:

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

리소스가 정의되면, 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 연관관계

리소스 응답에 연관 리소스를 포함하고자 한다면, 리소스의 `toArray` 메서드에서 반환하는 배열에 추가하면 됩니다. 이 예시에서는 `PostResource`의 `collection` 메서드를 사용하여 사용자의 블로그 게시글을 리소스 응답에 포함시킵니다:

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
> 연관관계를 이미 로드했을 때만 포함하고 싶다면 [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션 작성

리소스는 단일 모델을 배열로 변환하는 반면, 리소스 컬렉션은 모델의 컬렉션을 배열로 변환합니다. 하지만 모든 모델별로 리소스 컬렉션 클래스를 반드시 정의할 필요는 없습니다. Eloquent 모델 컬렉션은 모두 `toResourceCollection` 메서드를 제공하므로, 즉석에서 "임시" 리소스 컬렉션을 생성할 수 있습니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

컬렉션과 함께 반환할 메타 데이터를 커스터마이징해야 한다면, 직접 리소스 컬렉션 클래스를 정의해야 합니다:

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

단수형 리소스처럼, 리소스 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는, Eloquent 컬렉션의 `toResourceCollection` 메서드를 이용할 수 있습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름에 일치하고 `Collection` 접미사가 붙은 리소스 컬렉션을 네임스페이스 내에서 자동으로 찾으려 합니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 최상위 리소스는 JSON으로 변환될 때 `data` 키로 감싸집니다. 예를 들어, 일반적인 리소스 컬렉션의 응답은 다음과 같습니다:

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

최상위 리소스의 래핑을 비활성화 하고 싶다면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출하면 됩니다. 보통, 이 메서드는 `AppServiceProvider` 또는 애플리케이션의 모든 요청에 로드되는 [서비스 프로바이더](/docs/12.x/providers)에서 호출해야 합니다:

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
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 미치며, 리소스 컬렉션에서 직접 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

리소스의 연관관계가 어떻게 래핑될지는 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션을 중첩과 상관없이 `data` 키로 래핑하려면, 각 리소스를 위한 리소스 컬렉션 클래스를 정의하고 이 컬렉션을 `data` 키 안에 반환하면 됩니다.

혹시 이렇게 하면 최상위 리소스가 `data` 키로 두 번 감싸지지 않을까 걱정할 수 있습니다. 걱정하지 마세요, Laravel은 리소스가 실수로 이중 래핑되는 것을 방지하므로, 리소스 컬렉션의 중첩 레벨에 대해 신경 쓸 필요가 없습니다:

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

리소스 응답으로 페이지네이션된 컬렉션을 반환할 때는, `withoutWrapping` 메서드가 호출된 경우에도 Laravel은 항상 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이지네이션된 응답에는 페이지네이터의 상태 정보를 담는 `meta`와 `links` 키가 항상 포함되기 때문입니다:

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

Laravel 페이지네이터 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는, 페이지네이터의 `toResourceCollection` 메서드를 사용하여 해당 모델의 리소스 컬렉션을 자동으로 찾을 수 있습니다:

```php
return User::paginate()->toResourceCollection();
```

페이지네이션된 응답에는 항상 페이지네이터의 상태 정보를 담는 `meta`와 `links` 키가 포함됩니다:

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

페이지네이션 결과의 `links` 또는 `meta`에 포함될 정보를 커스터마이징하고자 한다면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와, `links` 및 `meta` 키를 포함하는 `$default` 정보 배열을 인자로 받습니다:

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

특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶은 경우가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때만 값을 포함하고 싶다면, Laravel이 제공하는 다양한 헬퍼 메서드를 활용할 수 있습니다. `when` 메서드는 조건에 따라 속성을 리소스 응답에 표현적으로 추가할 수 있게 해줍니다:

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

이 예시에서 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환하는 경우에만 최종 리소스 응답에 `secret` 키가 포함됩니다. `false`일 경우, `secret` 키는 클라이언트로 보내지기 전 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 구성할 때 조건문을 작성하지 않고도 리소스를 깔끔하게 정의할 수 있습니다.

`when` 메서드는 두 번째 인수로 클로저를 받아, 조건이 `true`일 때만 결과 값을 계산하도록 할 수도 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

모델에 실제로 속성이 존재할 때만 포함하려면, `whenHas` 메서드를 사용할 수 있습니다:

```php
'name' => $this->whenHas('name'),
```

속성이 `null`이 아닐 때만 리소스 응답에 포함하려면, `whenNotNull` 메서드를 사용하세요:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

여러 속성을 동일한 조건에 따라 한 번에 포함하고 싶은 경우, `mergeWhen` 메서드를 사용하세요. 이 메서드는 조건이 참일 때만 여러 속성을 병합하여 응답에 추가합니다:

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

여기서 주어진 조건이 `false`라면, 해당 속성들은 클라이언트로 전송되기 전 리소스 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 섞여있는 배열, 또는 순차적이지 않은 숫자 키 배열 내에서 사용하면 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성을 조건에 따라 로드하는 것 외에도, 모델에 연관관계가 이미 로드되어 있을 때만 리소스 응답에 연관관계를 포함시킬 수도 있습니다. 이를 통해 컨트롤러에서 어떤 연관관계를 미리 로드할지 결정하고, 리소스에서는 실제로 로드된 경우에만 포함할 수 있습니다. 이 방법은 리소스 내에서 "N+1" 쿼리 문제를 방지하는 데 도움이 됩니다.

`whenLoaded` 메서드는 연관관계가 로드된 경우에만 조건부로 포함시킬 수 있습니다. 이 메서드는 연관관계 객체 대신 이름을 인수로 받으므로 불필요한 로드를 방지합니다:

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

이 예시에서, 연관관계가 로드되어 있지 않으면 `posts` 키는 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 카운트

연관관계를 조건에 따라 포함시키는 것처럼, 연관관계의 "카운트"도 모델에 이미 해당 카운트가 로드된 경우에만 리소스 응답에 포함시킬 수 있습니다:

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 연관관계의 카운트가 존재할 때만 리소스 응답에 해당 속성을 조건부로 포함시켜줍니다. 이 메서드는 관계의 카운트가 있을 때만 포함하도록 해 불필요한 출력 방지를 도와줍니다:

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

이 예시에서, `posts` 연관관계의 카운트가 로드되지 않았다면 `posts_count` 키는 응답에서 제거됩니다.

`avg`, `sum`, `min`, `max`와 같은 다른 집계 유형도 `whenAggregated` 메서드로 조건부로 포함할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 중간 테이블(pivot) 정보

연관관계 정보 뿐만 아니라, 다대다 관계의 중간 테이블에 있는 데이터를 조건부로 포함할 때는 `whenPivotLoaded` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 피벗 테이블 이름을, 두 번째 인수로는 사용할 값 반환용 클로저를 전달합니다:

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

연관관계가 [커스텀 중간 테이블 모델](/docs/12.x/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, `whenPivotLoaded` 메서드의 첫 번째 인수로 해당 중간 테이블 모델 인스턴스를 전달할 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블이 `pivot` 이외의 어세서명을 사용하는 경우, `whenPivotLoadedAs` 메서드를 사용할 수 있습니다:

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
### 메타 데이터 추가

일부 JSON API 표준에서는 리소스 또는 리소스 컬렉션 응답에 메타 데이터를 추가할 것을 요구합니다. 대표적으로는 해당 리소스 또는 관련 리소스에 대한 `links`나 리소스 자체의 메타 정보 등이 있습니다. 리소스에 추가 메타 데이터를 반환해야 한다면, `toArray` 메서드 내에 포함시키면 됩니다. 예를 들어, 리소스 컬렉션을 변환할 때 `links` 정보를 추가할 수 있습니다:

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

리소스에서 추가적인 메타 데이터를 반환할 때, Laravel이 페이지네이션 응답에 자동으로 추가하는 `links`나 `meta` 키를 실수로 덮어쓸 걱정은 하지 않아도 됩니다. 개발자가 직접 정의한 추가 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

최상위 리소스가 반환될 때만 특정 메타 데이터를 리소스 응답에 포함하고 싶은 경우가 있습니다. 일반적으로 전체 응답에 대한 정보가 여기에 해당됩니다. 이 메타 데이터를 정의하려면, 리소스 클래스에 `with` 메서드를 추가하면 됩니다. 이 메서드는 리소스가 변환될 때 최상위 리소스인 경우에만 포함될 메타 데이터 배열을 반환해야 합니다:

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
#### 리소스 생성 시 메타 데이터 추가

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터를 추가할 수 있습니다. 모든 리소스에서 제공되는 `additional` 메서드는 응답과 함께 추가해야 할 데이터를 배열로 받습니다:

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
## 리소스 응답

앞서 살펴본 것처럼, 리소스는 라우트와 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만 때로는 클라이언트로 전송되기 전에 HTTP 응답을 커스터마이즈해야 할 수도 있습니다. 이를 위한 두 가지 방법이 있습니다. 첫째, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답의 헤더를 완전히 제어할 수 있습니다:

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

또는, 리소스 내에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 응답에서 최상위 리소스로 반환될 때 호출됩니다:

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