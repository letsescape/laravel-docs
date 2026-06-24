<!-- # Eloquent: API Resources -->
# Eloquent: API Resources

- [Introduction](#introduction)
- [Generating Resources](#generating-resources)
- [Concept Overview](#concept-overview)
    - [Resource Collections](#resource-collections)
- [Writing Resources](#writing-resources)
    - [Data Wrapping](#data-wrapping)
    - [Pagination](#pagination)
    - [Conditional Attributes](#conditional-attributes)
    - [Conditional Relationships](#conditional-relationships)
    - [Adding Meta Data](#adding-meta-data)
- [JSON:API Resources](#jsonapi-resources)
    - [Generating JSON:API Resources](#generating-jsonapi-resources)
    - [Defining Attributes](#defining-jsonapi-attributes)
    - [Defining Relationships](#defining-jsonapi-relationships)
    - [Resource Type and ID](#jsonapi-resource-type-and-id)
    - [Sparse Fieldsets and Includes](#jsonapi-sparse-fieldsets-and-includes)
    - [Links and Meta](#jsonapi-links-and-meta)
- [Resource Responses](#resource-responses)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When building an API, you may need a transformation layer that sits between your Eloquent models and the JSON responses that are actually returned to your application's users. For example, you may wish to display certain attributes for a subset of users and not others, or you may wish to always include certain relationships in the JSON representation of your models. Eloquent's resource classes allow you to expressively and easily transform your models and model collections into JSON. -->
API를 만들 때는 Eloquent 모델과 애플리케이션 사용자에게 실제로 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어 일부 사용자에게만 특정 속성을 표시하고 다른 사용자에게는 표시하지 않거나, 모델의 JSON 표현에 특정 연관관계를 항상 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 쉽고 표현력 있게 변환할 수 있도록 해줍니다.

<!-- Of course, you may always convert Eloquent models or collections to JSON using their `toJson` methods; however, Eloquent resources provide more granular and robust control over the JSON serialization of your models and their relationships. -->
물론 Eloquent 모델이나 컬렉션은 언제든지 `toJson` 메서드를 사용해 JSON으로 변환할 수 있습니다. 하지만 Eloquent 리소스는 모델과 그 연관관계의 JSON 직렬화를 더 세밀하고 견고하게 제어할 수 있게 해줍니다.

<a name="generating-resources"></a>
<!-- ## Generating Resources -->
## Generating Resources

<!-- To generate a resource class, you may use the `make:resource` Artisan command. By default, resources will be placed in the `app/Http/Resources` directory of your application. Resources extend the `Illuminate\Http\Resources\Json\JsonResource` class: -->
리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 배치됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다.

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- In addition to generating resources that transform individual models, you may generate resources that are responsible for transforming collections of models. This allows your JSON responses to include links and other meta information that is relevant to an entire collection of a given resource. -->
개별 모델을 변환하는 리소스뿐만 아니라, 모델 컬렉션을 변환하는 역할을 하는 리소스도 생성할 수 있습니다. 이를 사용하면 JSON 응답에 특정 리소스의 전체 컬렉션과 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

<!-- To create a resource collection, you should use the `--collection` flag when creating the resource. Or, including the word `Collection` in the resource name will indicate to Laravel that it should create a collection resource. Collection resources extend the `Illuminate\Http\Resources\Json\ResourceCollection` class: -->
리소스 컬렉션을 만들려면 리소스를 생성할 때 `--collection` 플래그를 사용해야 합니다. 또는 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel은 컬렉션 리소스를 생성해야 한다고 판단합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다.

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

> [!NOTE]
> 이 내용은 리소스와 리소스 컬렉션에 대한 상위 수준의 개요입니다. 리소스가 제공하는 커스터마이징 기능과 강력함을 더 깊이 이해하려면 이 문서의 다른 섹션도 읽어보는 것을 적극 권장합니다.

<!-- Before diving into all of the options available to you when writing resources, let's first take a high-level look at how resources are used within Laravel. A resource class represents a single model that needs to be transformed into a JSON structure. For example, here is a simple `UserResource` resource class: -->
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

<!-- Every resource class defines a `toArray` method which returns the array of attributes that should be converted to JSON when the resource is returned as a response from a route or controller method. -->
모든 리소스 클래스는 `toArray` 메서드를 정의합니다. 이 메서드는 리소스가 라우트나 컨트롤러 메서드에서 응답으로 반환될 때 JSON으로 변환되어야 하는 속성 배열을 반환합니다.

<!-- Note that we can access model properties directly from the `$this` variable. This is because a resource class will automatically proxy property and method access down to the underlying model for convenient access. Once the resource is defined, it may be returned from a route or controller. The resource accepts the underlying model instance via its constructor: -->
`$this` 변수에서 모델 속성에 직접 접근할 수 있다는 점에 주목하세요. 이는 리소스 클래스가 편리한 접근을 위해 속성과 메서드 접근을 내부 모델로 자동 프록시하기 때문입니다. 리소스를 정의한 후에는 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스는 생성자를 통해 내부 모델 인스턴스를 받습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<!-- For convenience, you may use the model's `toResource` method, which will use framework conventions to automatically discover the model's underlying resource: -->
편의를 위해 모델의 `toResource` 메서드를 사용할 수도 있습니다. 이 메서드는 프레임워크 규칙을 사용해 모델의 기본 리소스를 자동으로 찾아냅니다.

```php
return User::findOrFail($id)->toResource();
```

<!-- When invoking the `toResource` method, Laravel will attempt to locate a resource that matches the model's name and is optionally suffixed with `Resource` within the `Http\Resources` namespace closest to the model's namespace. -->
`toResource` 메서드를 호출하면 Laravel은 모델 이름과 일치하고, 선택적으로 `Resource` 접미사가 붙은 리소스를 모델의 네임스페이스에 가장 가까운 `Http\Resources` 네임스페이스 안에서 찾으려고 시도합니다.

<!-- If your resource class doesn't follow this naming convention or is located in a different namespace, you may specify the default resource for the model using the `UseResource` attribute: -->
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

<!-- Alternatively, you may specify resource class by passing it to the `toResource` method: -->
또는 `toResource` 메서드에 리소스 클래스를 전달해 지정할 수도 있습니다.

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
<!-- ### Resource Collections -->
### Resource Collections

<!-- If you are returning a collection of resources or a paginated response, you should use the `collection` method provided by your resource class when creating the resource instance in your route or controller: -->
리소스 컬렉션이나 페이지네이션된 응답을 반환하는 경우, 라우트나 컨트롤러에서 리소스 인스턴스를 만들 때 리소스 클래스가 제공하는 `collection` 메서드를 사용해야 합니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- Or, for convenience, you may use the Eloquent collection's `toResourceCollection` method, which will use framework conventions to automatically discover the model's underlying resource collection: -->
또는 편의를 위해 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 규칙을 사용해 모델의 기본 리소스 컬렉션을 자동으로 찾아냅니다.

```php
return User::all()->toResourceCollection();
```

<!-- When invoking the `toResourceCollection` method, Laravel will attempt to locate a resource collection that matches the model's name and is suffixed with `Collection` within the `Http\Resources` namespace closest to the model's namespace. -->
`toResourceCollection` 메서드를 호출하면 Laravel은 모델 이름과 일치하고 `Collection` 접미사가 붙은 리소스 컬렉션을 모델의 네임스페이스에 가장 가까운 `Http\Resources` 네임스페이스 안에서 찾으려고 시도합니다.

<!-- If your resource collection class doesn't follow this naming convention or is located in a different namespace, you may specify the default resource collection for the model using the `UseResourceCollection` attribute: -->
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

<!-- Alternatively, you may specify the resource collection class by passing it to the `toResourceCollection` method: -->
또는 `toResourceCollection` 메서드에 리소스 컬렉션 클래스를 전달해 지정할 수도 있습니다.

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
<!-- #### Custom Resource Collections -->
#### Custom Resource Collections

<!-- By default, resource collections do not allow any addition of custom meta data that may need to be returned with your collection. If you would like to customize the resource collection response, you may create a dedicated resource to represent the collection: -->
기본적으로 리소스 컬렉션은 컬렉션과 함께 반환해야 할 커스텀 메타데이터를 추가하는 기능을 제공하지 않습니다. 리소스 컬렉션 응답을 커스터마이징하려면 컬렉션을 나타내는 전용 리소스를 만들 수 있습니다.

```shell
php artisan make:resource UserCollection
```

<!-- Once the resource collection class has been generated, you may easily define any meta data that should be included with the response: -->
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

<!-- After defining your resource collection, it may be returned from a route or controller: -->
리소스 컬렉션을 정의한 후에는 라우트나 컨트롤러에서 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<!-- Or, for convenience, you may use the Eloquent collection's `toResourceCollection` method, which will use framework conventions to automatically discover the model's underlying resource collection: -->
또는 편의를 위해 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 규칙을 사용해 모델의 기본 리소스 컬렉션을 자동으로 찾아냅니다.

```php
return User::all()->toResourceCollection();
```

<!-- When invoking the `toResourceCollection` method, Laravel will attempt to locate a resource collection that matches the model's name and is suffixed with `Collection` within the `Http\Resources` namespace closest to the model's namespace. -->
`toResourceCollection` 메서드를 호출하면 Laravel은 모델 이름과 일치하고 `Collection` 접미사가 붙은 리소스 컬렉션을 모델의 네임스페이스에 가장 가까운 `Http\Resources` 네임스페이스 안에서 찾으려고 시도합니다.

<a name="preserving-collection-keys"></a>
<!-- #### Preserving Collection Keys -->
#### Preserving Collection Keys

<!-- When returning a resource collection from a route, Laravel resets the collection's keys so that they are in numerical order. However, you may use the `PreserveKeys` attribute on your resource class indicating whether a collection's original keys should be preserved: -->
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

<!-- When the `preserveKeys` property is set to `true`, collection keys will be preserved when the collection is returned from a route or controller: -->
`preserveKeys` 속성이 `true`로 설정되면, 라우트나 컨트롤러에서 컬렉션을 반환할 때 컬렉션 키가 보존됩니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
<!-- #### Customizing the Underlying Resource Class -->
#### Customizing the Underlying Resource Class

<!-- Typically, the `$this->collection` property of a resource collection is automatically populated with the result of mapping each item of the collection to its singular resource class. The singular resource class is assumed to be the collection's class name without the trailing `Collection` portion of the class name. In addition, depending on your personal preference, the singular resource class may or may not be suffixed with `Resource`. -->
일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단일 리소스 클래스는 컬렉션 클래스 이름에서 끝의 `Collection` 부분을 제거한 이름으로 간주됩니다. 또한 개인적인 선호에 따라 단일 리소스 클래스에는 `Resource` 접미사가 붙을 수도 있고 붙지 않을 수도 있습니다.

<!-- For example, `UserCollection` will attempt to map the given user instances into the `UserResource` resource. To customize this behavior, you may use the `Collects` attribute on your resource collection: -->
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
<!-- ## Writing Resources -->
## Writing Resources

> [!NOTE]
> 아직 [concept overview](#concept-overview)를 읽지 않았다면, 이 문서를 계속 읽기 전에 먼저 읽어보는 것을 적극 권장합니다.

<!-- Resources only need to transform a given model into an array. So, each resource contains a `toArray` method which translates your model's attributes into an API friendly array that can be returned from your application's routes or controllers: -->
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

<!-- Once a resource has been defined, it may be returned directly from a route or controller: -->
리소스가 정의되면 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- If you would like to include related resources in your response, you may add them to the array returned by your resource's `toArray` method. In this example, we will use the `PostResource` resource's `collection` method to add the user's blog posts to the resource response: -->
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
> 이미 로드된 경우에만 연관관계를 포함하고 싶다면 [conditional relationships](#conditional-relationships) 문서를 확인하세요.

<a name="writing-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- While resources transform a single model into an array, resource collections transform a collection of models into an array. However, it is not absolutely necessary to define a resource collection class for each one of your models since all Eloquent model collections provide a `toResourceCollection` method to generate an "ad-hoc" resource collection on the fly: -->
리소스가 단일 모델을 배열로 변환한다면, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 모든 Eloquent 모델 컬렉션은 즉석에서 "임시" 리소스 컬렉션을 생성하는 `toResourceCollection` 메서드를 제공하므로, 각 모델마다 리소스 컬렉션 클래스를 반드시 정의할 필요는 없습니다.

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

<!-- However, if you need to customize the meta data returned with the collection, it is necessary to define your own resource collection: -->
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
<!-- Like singular resources, resource collections may be returned directly from routes or controllers: -->
단일 리소스와 마찬가지로, 리소스 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<!-- Or, for convenience, you may use the Eloquent collection's `toResourceCollection` method, which will use framework conventions to automatically discover the model's underlying resource collection: -->
또는 편의를 위해 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 관례를 사용해 모델의 기반 리소스 컬렉션을 자동으로 찾습니다.

```php
return User::all()->toResourceCollection();
```

<!-- When invoking the `toResourceCollection` method, Laravel will attempt to locate a resource collection that matches the model's name and is suffixed with `Collection` within the `Http\Resources` namespace closest to the model's namespace. -->
`toResourceCollection` 메서드를 호출하면 Laravel은 모델의 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스 안에서, 모델 이름과 일치하고 뒤에 `Collection`이 붙은 리소스 컬렉션을 찾으려고 시도합니다.

<a name="data-wrapping"></a>
<!-- ### Data Wrapping -->
### Data Wrapping

<!-- By default, your outermost resource is wrapped in a `data` key when the resource response is converted to JSON. So, for example, a typical resource collection response looks like the following: -->
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

<!-- If you would like to disable the wrapping of the outermost resource, you should invoke the `withoutWrapping` method on the base `Illuminate\Http\Resources\Json\JsonResource` class. Typically, you should call this method from your `AppServiceProvider` or another [service provider](/docs/master/providers) that is loaded on every request to your application: -->
최상위 리소스 래핑을 비활성화하려면 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출해야 합니다. 일반적으로 이 메서드는 애플리케이션의 모든 요청에서 로드되는 `AppServiceProvider` 또는 다른 [service provider](/docs/master/providers)에서 호출해야 합니다.

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
<!-- #### Wrapping Nested Resources -->
#### Wrapping Nested Resources

<!-- You have total freedom to determine how your resource's relationships are wrapped. If you would like all resource collections to be wrapped in a `data` key, regardless of their nesting, you should define a resource collection class for each resource and return the collection within a `data` key. -->
리소스의 연관관계를 어떻게 래핑할지는 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션이 중첩 위치와 관계없이 `data` 키로 감싸지도록 하려면, 각 리소스마다 리소스 컬렉션 클래스를 정의하고 컬렉션을 `data` 키 안에서 반환해야 합니다.

<!-- You may be wondering if this will cause your outermost resource to be wrapped in two `data` keys. Don't worry, Laravel will never let your resources be accidentally double-wrapped, so you don't have to be concerned about the nesting level of the resource collection you are transforming: -->
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
<!-- #### Data Wrapping and Pagination -->
#### Data Wrapping and Pagination

<!-- When returning paginated collections via a resource response, Laravel will wrap your resource data in a `data` key even if the `withoutWrapping` method has been called. This is because paginated responses always contain `meta` and `links` keys with information about the paginator's state: -->
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
<!-- ### Pagination -->
### Pagination

<!-- You may pass a Laravel paginator instance to the `collection` method of a resource or to a custom resource collection: -->
Laravel paginator 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

<!-- Or, for convenience, you may use the paginator's `toResourceCollection` method, which will use framework conventions to automatically discover the paginated model's underlying resource collection: -->
또는 편의를 위해 paginator의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크 관례를 사용해 페이지네이션된 모델의 기반 리소스 컬렉션을 자동으로 찾습니다.

```php
return User::paginate()->toResourceCollection();
```

<!-- Paginated responses always contain `meta` and `links` keys with information about the paginator's state: -->
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
<!-- #### Customizing the Pagination Information -->
#### Customizing the Pagination Information

<!-- If you would like to customize the information included in the `links` or `meta` keys of the pagination response, you may define a `paginationInformation` method on the resource. This method will receive the `$paginated` data and the array of `$default` information, which is an array containing the `links` and `meta` keys: -->
페이지네이션 응답의 `links` 키나 `meta` 키에 포함되는 정보를 커스터마이징하려면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 `links` 키와 `meta` 키를 포함하는 배열인 `$default` 정보 배열을 받습니다.

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
<!-- ### Conditional Attributes -->
### Conditional Attributes

<!-- Sometimes you may wish to only include an attribute in a resource response if a given condition is met. For example, you may wish to only include a value if the current user is an "administrator". Laravel provides a variety of helper methods to assist you in this situation. The `when` method may be used to conditionally add an attribute to a resource response: -->
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

<!-- In this example, the `secret` key will only be returned in the final resource response if the authenticated user's `isAdmin` method returns `true`. If the method returns `false`, the `secret` key will be removed from the resource response before it is sent to the client. The `when` method allows you to expressively define your resources without resorting to conditional statements when building the array. -->
이 예제에서 `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환하는 경우에만 최종 리소스 응답에 포함됩니다. 메서드가 `false`를 반환하면 `secret` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 만들 때 조건문을 직접 작성하지 않고도 리소스를 표현력 있게 정의할 수 있습니다.

<!-- The `when` method also accepts a closure as its second argument, allowing you to calculate the resulting value only if the given condition is `true`: -->
`when` 메서드는 두 번째 인수로 클로저도 받을 수 있습니다. 이를 사용하면 주어진 조건이 `true`일 때만 결과 값을 계산할 수 있습니다.

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

<!-- The `whenHas` method may be used to include an attribute if it is actually present on the underlying model: -->
`whenHas` 메서드는 기반 모델에 실제로 해당 속성이 존재하는 경우에만 속성을 포함할 때 사용할 수 있습니다.

```php
'name' => $this->whenHas('name'),
```

<!-- Additionally, the `whenNotNull` method may be used to include an attribute in the resource response if the attribute is not null: -->
또한 `whenNotNull` 메서드는 속성이 null이 아닐 때만 리소스 응답에 속성을 포함하는 데 사용할 수 있습니다.

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
<!-- #### Merging Conditional Attributes -->
#### Merging Conditional Attributes

<!-- Sometimes you may have several attributes that should only be included in the resource response based on the same condition. In this case, you may use the `mergeWhen` method to include the attributes in the response only when the given condition is `true`: -->
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

<!-- Again, if the given condition is `false`, these attributes will be removed from the resource response before it is sent to the client. -->
마찬가지로 주어진 조건이 `false`이면, 이러한 속성은 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 섞인 배열 안에서 사용하면 안 됩니다. 또한 숫자 키가 순차적으로 정렬되어 있지 않은 배열 안에서도 사용하면 안 됩니다.

<a name="conditional-relationships"></a>
<!-- ### Conditional Relationships -->
### Conditional Relationships

<!-- In addition to conditionally loading attributes, you may conditionally include relationships on your resource responses based on if the relationship has already been loaded on the model. This allows your controller to decide which relationships should be loaded on the model and your resource can easily include them only when they have actually been loaded. Ultimately, this makes it easier to avoid "N+1" query problems within your resources. -->
속성을 조건부로 로드하는 것뿐만 아니라, 모델에 연관관계가 이미 로드되어 있는지에 따라 리소스 응답에 연관관계를 조건부로 포함할 수 있습니다. 이렇게 하면 컨트롤러가 모델에 어떤 연관관계를 로드할지 결정하고, 리소스는 실제로 로드된 연관관계만 쉽게 포함할 수 있습니다. 결과적으로 리소스 안에서 "N+1" 쿼리 문제를 더 쉽게 피할 수 있습니다.

<!-- The `whenLoaded` method may be used to conditionally load a relationship. In order to avoid unnecessarily loading relationships, this method accepts the name of the relationship instead of the relationship itself: -->
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

<!-- In this example, if the relationship has not been loaded, the `posts` key will be removed from the resource response before it is sent to the client. -->
이 예제에서 연관관계가 로드되지 않았다면, `posts` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
<!-- #### Conditional Relationship Counts -->
#### Conditional Relationship Counts

<!-- In addition to conditionally including relationships, you may conditionally include relationship "counts" on your resource responses based on if the relationship's count has been loaded on the model: -->
연관관계를 조건부로 포함하는 것뿐만 아니라, 모델에 연관관계의 "개수"가 로드되어 있는지에 따라 리소스 응답에 연관관계 개수를 조건부로 포함할 수 있습니다.

```php
new UserResource($user->loadCount('posts'));
```

<!-- The `whenCounted` method may be used to conditionally include a relationship's count in your resource response. This method avoids unnecessarily including the attribute if the relationships' count is not present: -->
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

<!-- In this example, if the `posts` relationship's count has not been loaded, the `posts_count` key will be removed from the resource response before it is sent to the client. -->
이 예제에서 `posts` 연관관계의 개수가 로드되지 않았다면, `posts_count` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

<!-- Other types of aggregates, such as `avg`, `sum`, `min`, and `max` may also be conditionally loaded using the `whenAggregated` method: -->
`avg`, `sum`, `min`, `max` 같은 다른 유형의 집계도 `whenAggregated` 메서드를 사용해 조건부로 로드할 수 있습니다.

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
<!-- #### Conditional Pivot Information -->
#### Conditional Pivot Information

<!-- In addition to conditionally including relationship information in your resource responses, you may conditionally include data from the intermediate tables of many-to-many relationships using the `whenPivotLoaded` method. The `whenPivotLoaded` method accepts the name of the pivot table as its first argument. The second argument should be a closure that returns the value to be returned if the pivot information is available on the model: -->
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

<!-- If your relationship is using a [custom intermediate table model](/docs/master/eloquent-relationships#defining-custom-intermediate-table-models), you may pass an instance of the intermediate table model as the first argument to the `whenPivotLoaded` method: -->
연관관계가 [custom intermediate table model](/docs/master/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하고 있다면, 중간 테이블 모델의 인스턴스를 `whenPivotLoaded` 메서드의 첫 번째 인수로 전달할 수 있습니다.

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

<!-- If your intermediate table is using an accessor other than `pivot`, you may use the `whenPivotLoadedAs` method: -->
중간 테이블이 `pivot`이 아닌 다른 accessor를 사용한다면 `whenPivotLoadedAs` 메서드를 사용할 수 있습니다.

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
<!-- ### Adding Meta Data -->
### Adding Meta Data

<!-- Some JSON API standards require the addition of meta data to your resource and resource collections responses. This often includes things like `links` to the resource or related resources, or meta data about the resource itself. If you need to return additional meta data about a resource, include it in your `toArray` method. For example, you might include `links` information when transforming a resource collection: -->
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

<!-- When returning additional meta data from your resources, you never have to worry about accidentally overriding the `links` or `meta` keys that are automatically added by Laravel when returning paginated responses. Any additional `links` you define will be merged with the links provided by the paginator. -->
리소스에서 추가 메타데이터를 반환할 때, 페이지네이션된 응답을 반환할 때 Laravel이 자동으로 추가하는 `links` 또는 `meta` 키를 실수로 덮어쓸까 걱정할 필요는 없습니다. 직접 정의한 추가 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
<!-- #### Top Level Meta Data -->
#### Top Level Meta Data

<!-- Sometimes you may wish to only include certain meta data with a resource response if the resource is the outermost resource being returned. Typically, this includes meta information about the response as a whole. To define this meta data, add a `with` method to your resource class. This method should return an array of meta data to be included with the resource response only when the resource is the outermost resource being transformed: -->
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
<!-- #### Adding Meta Data When Constructing Resources -->
#### Adding Meta Data When Constructing Resources

<!-- You may also add top-level data when constructing resource instances in your route or controller. The `additional` method, which is available on all resources, accepts an array of data that should be added to the resource response: -->
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
<!-- ## JSON:API Resources -->
## JSON:API Resources

<!-- Laravel ships with `JsonApiResource`, a resource class that produces responses compliant with the [JSON:API specification](https://jsonapi.org/). It extends the standard `JsonResource` class and automatically handles resource object structure, relationships, sparse fieldsets, includes, and sets the `Content-Type` header to `application/vnd.api+json`. -->
Laravel은 [JSON:API specification](https://jsonapi.org/)를 준수하는 응답을 생성하는 리소스 클래스인 `JsonApiResource`를 제공합니다. 이 클래스는 표준 `JsonResource` 클래스를 확장하며 리소스 객체 구조, 연관관계, sparse fieldsets(스파스 필드셋), 포함 항목을 자동으로 처리하고, `Content-Type` 헤더를 `application/vnd.api+json`으로 설정합니다.

> [!NOTE]
> Laravel의 JSON:API 리소스는 응답의 직렬화를 처리합니다. 필터나 정렬처럼 들어오는 JSON:API 쿼리 파라미터도 파싱해야 한다면, [Spatie's Laravel Query Builder](https://spatie.be/docs/laravel-query-builder/v6/introduction)가 훌륭한 보조 패키지입니다.

<a name="generating-jsonapi-resources"></a>
<!-- ### Generating JSON:API Resources -->
### Generating JSON:API Resources

<!-- To generate a JSON:API resource, use the `make:resource` Artisan command with the `--json-api` flag: -->
JSON:API 리소스를 생성하려면 `--json-api` 플래그와 함께 `make:resource` Artisan 명령어를 사용하십시오.

```shell
php artisan make:resource PostResource --json-api
```

<!-- The generated class will extend `Illuminate\Http\Resources\JsonApi\JsonApiResource` and include `$attributes` and `$relationships` properties for you to define: -->
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

<!-- JSON:API resources may be returned from routes and controllers just like standard resources: -->
JSON:API 리소스는 표준 리소스와 마찬가지로 라우트와 컨트롤러에서 반환할 수 있습니다.

```php
use App\Http\Resources\PostResource;
use App\Models\Post;

Route::get('/api/posts/{post}', function (Post $post) {
    return new PostResource($post);
});
```

<!-- Or, for convenience, you may use the model's `toResource` method: -->
또는 편의를 위해 모델의 `toResource` 메서드를 사용할 수 있습니다.

```php
Route::get('/api/posts/{post}', function (Post $post) {
    return $post->toResource();
});
```

<!-- This will produce a JSON:API compliant response: -->
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

<!-- To return a collection of JSON:API resources, use the `collection` method or the `toResourceCollection` convenience method: -->
JSON:API 리소스 컬렉션을 반환하려면 `collection` 메서드 또는 편의 메서드인 `toResourceCollection`을 사용하십시오.

```php
return PostResource::collection(Post::all());

return Post::all()->toResourceCollection();
```

<a name="defining-jsonapi-attributes"></a>
<!-- ### Defining Attributes -->
### Defining Attributes

<!-- There are two ways to define which attributes are included in your JSON:API resource. -->
JSON:API 리소스에 포함할 속성을 정의하는 방법은 두 가지입니다.

<!-- The simplest approach is to define an `$attributes` property on your resource. You may list attribute names as values, which will be read directly from the underlying model: -->
가장 간단한 방법은 리소스에 `$attributes` 속성을 정의하는 것입니다. 속성 이름을 값으로 나열하면, 내부 모델에서 직접 읽어 옵니다.

```php
public $attributes = [
    'title',
    'body',
    'created_at',
];
```

<!-- Or, for full control over the resource's attributes, you may override the `toAttributes` method on the resource: -->
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
<!-- ### Defining Relationships -->
### Defining Relationships

<!-- JSON:API resources support defining relationships that follow the JSON:API specification. Relationships are only serialized when requested by the client via the `include` query parameter. -->
JSON:API 리소스는 JSON:API 명세를 따르는 연관관계 정의를 지원합니다. 연관관계는 클라이언트가 `include` 쿼리 파라미터를 통해 요청한 경우에만 직렬화됩니다.

<!-- #### The `$relationships` Property -->
#### The `$relationships` Property

<!-- You may define your resource's includable relationships via the `$relationships` property on your resource: -->
리소스에 포함 가능한 연관관계는 `$relationships` 속성으로 정의할 수 있습니다.

```php
public $relationships = [
    'author',
    'comments',
];
```

<!-- When listing a relationship name as a value, Laravel will resolve the corresponding Eloquent relationship and automatically discover the appropriate resource class. If you need to specify the resource class explicitly, you may define the relationship as a key / class pair: -->
연관관계 이름을 값으로 나열하면 Laravel은 해당 Eloquent 연관관계를 해석하고 적절한 리소스 클래스를 자동으로 찾아냅니다. 리소스 클래스를 명시적으로 지정해야 한다면 연관관계를 키 / 클래스 쌍으로 정의할 수 있습니다.

```php
use App\Http\Resources\UserResource;

public $relationships = [
    'author' => UserResource::class,
    'comments',
];
```

<!-- Alternatively, you may override the `toRelationships` method on the resource: -->
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

<!-- #### Including Relationships -->
#### Including Relationships

<!-- Clients may request related resources using the `include` query parameter: -->
클라이언트는 `include` 쿼리 파라미터를 사용해 관련 리소스를 요청할 수 있습니다.

```
GET /api/posts/1?include=author,comments
```

<!-- This produces a response with resource identifier objects in the `relationships` key and full resource objects in the top-level `included` array: -->
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

<!-- Nested relationships may be included using dot notation: -->
중첩된 연관관계는 점 표기법을 사용해 포함할 수 있습니다.

```
GET /api/posts/1?include=comments.author
```

<a name="jsonapi-relationship-depth"></a>
<!-- #### Relationship Depth -->
#### Relationship Depth

<!-- By default, nested relationship includes are limited to a maximum depth. You may customize this limit using the `maxRelationshipDepth` method, typically in one of you application's service provider: -->
기본적으로 중첩된 연관관계 포함은 최대 깊이로 제한됩니다. 일반적으로 애플리케이션의 서비스 프로바이더 중 하나에서 `maxRelationshipDepth` 메서드를 사용해 이 제한을 사용자 지정할 수 있습니다.

```php
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

JsonApiResource::maxRelationshipDepth(3);
```

<a name="jsonapi-resource-type-and-id"></a>
<!-- ### Resource Type and ID -->
### Resource Type and ID

<!-- By default, the resource's `type` is derived from the resource class name. For example, `PostResource` produces the type `posts` and `BlogPostResource` produces `blog-posts`. The resource's `id` is resolved from the model's primary key. -->
기본적으로 리소스의 `type`은 리소스 클래스 이름에서 파생됩니다. 예를 들어 `PostResource`는 `posts` 타입을 생성하고, `BlogPostResource`는 `blog-posts` 타입을 생성합니다. 리소스의 `id`는 모델의 기본 키에서 해석됩니다.

<!-- If you need to customize these values, you may override the `toType` and `toId` methods on your resource: -->
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

<!-- This is particularly useful when a resource's type should differ from its class name, such as when an `AuthorResource` wraps a `User` model and should output the type `authors`. -->
이 기능은 리소스 타입이 클래스 이름과 달라야 할 때 특히 유용합니다. 예를 들어 `AuthorResource`가 `User` 모델을 감싸지만 `authors` 타입을 출력해야 하는 경우가 그렇습니다.

<a name="jsonapi-sparse-fieldsets-and-includes"></a>
<!-- ### Sparse Fieldsets and Includes -->
### Sparse Fieldsets and Includes

<!-- JSON:API resources support [sparse fieldsets](https://jsonapi.org/format/#fetching-sparse-fieldsets), allowing clients to request only specific attributes for each resource type using the `fields` query parameter: -->
JSON:API 리소스는 [sparse fieldsets](https://jsonapi.org/format/#fetching-sparse-fieldsets)을 지원합니다. 이를 통해 클라이언트는 `fields` 쿼리 파라미터를 사용해 각 리소스 타입에 대해 특정 속성만 요청할 수 있습니다.

```
GET /api/posts?fields[posts]=title,created_at&fields[users]=name
```

<!-- This will only include the `title` and `created_at` attributes for `posts` resources, and the `name` attribute for `users` resources. -->
이 경우 `posts` 리소스에는 `title`과 `created_at` 속성만 포함되고, `users` 리소스에는 `name` 속성만 포함됩니다.

<a name="jsonapi-ignoring-query-string"></a>
<!-- #### Ignoring the Query String -->
#### Ignoring the Query String

<!-- If you would like to disable sparse fieldset filtering for a given resource response, you may call the `ignoreFieldsAndIncludesInQueryString` method: -->
특정 리소스 응답에서 sparse fieldset 필터링을 비활성화하려면 `ignoreFieldsAndIncludesInQueryString` 메서드를 호출할 수 있습니다.

```php
return $post->toResource()
    ->ignoreFieldsAndIncludesInQueryString();
```

<a name="jsonapi-including-previously-loaded-relationships"></a>
<!-- #### Including Previously Loaded Relationships -->
#### Including Previously Loaded Relationships

<!-- By default, relationships are only included in the response when requested via the `include` query parameter. If you would like to include all previously eager-loaded relationships regardless of the query string, you may call the `includePreviouslyLoadedRelationships` method: -->
기본적으로 연관관계는 `include` 쿼리 파라미터를 통해 요청된 경우에만 응답에 포함됩니다. 쿼리 문자열과 관계없이 이전에 eager load(즉시 로딩)된 모든 연관관계를 포함하려면 `includePreviouslyLoadedRelationships` 메서드를 호출할 수 있습니다.

```php
return $post->load('author', 'comments')
    ->toResource()
    ->includePreviouslyLoadedRelationships();
```

<a name="jsonapi-links-and-meta"></a>
<!-- ### Links and Meta -->
### Links and Meta

<!-- You may add links and meta information to your JSON:API resource objects by overriding the `toLinks` and `toMeta` methods on the resource: -->
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

<!-- This will add `links` and `meta` keys to the resource object in the response: -->
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
<!-- ## Resource Responses -->
## Resource Responses

<!-- As you have already read, resources may be returned directly from routes and controllers: -->
앞서 살펴본 것처럼, 리소스는 라우트와 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

<!-- However, sometimes you may need to customize the outgoing HTTP response before it is sent to the client. There are two ways to accomplish this. First, you may chain the `response` method onto the resource. This method will return an `Illuminate\Http\JsonResponse` instance, giving you full control over the response's headers: -->
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

<!-- Alternatively, you may define a `withResponse` method within the resource itself. This method will be called when the resource is returned as the outermost resource in a response: -->
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
