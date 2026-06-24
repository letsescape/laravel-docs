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
- [Resource Responses](#resource-responses)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When building an API, you may need a transformation layer that sits between your Eloquent models and the JSON responses that are actually returned to your application's users. For example, you may wish to display certain attributes for a subset of users and not others, or you may wish to always include certain relationships in the JSON representation of your models. Eloquent's resource classes allow you to expressively and easily transform your models and model collections into JSON. -->
API를 개발할 때, Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 위치하는 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자 그룹에만 일부 속성을 보여주고 싶거나, 항상 모델의 특정 연관관계를 JSON 표현에 포함하고 싶을 때가 있습니다. Eloquent의 리소스 클래스는 모델과 컬렉션을 JSON으로 변환하는 작업을 보다 쉽고 명확하게 할 수 있도록 도와줍니다.

<!-- Of course, you may always convert Eloquent models or collections to JSON using their `toJson` methods; however, Eloquent resources provide more granular and robust control over the JSON serialization of your models and their relationships. -->
물론, 항상 Eloquent 모델이나 컬렉션의 `toJson` 메서드를 사용하여 JSON으로 변환할 수도 있습니다. 하지만 Eloquent 리소스를 사용하면 모델과 해당 연관관계의 JSON 직렬화 과정을 더 세밀하게, 그리고 강력하게 제어할 수 있습니다.

<a name="generating-resources"></a>
<!-- ## Generating Resources -->
## Generating Resources

<!-- To generate a resource class, you may use the `make:resource` Artisan command. By default, resources will be placed in the `app/Http/Resources` directory of your application. Resources extend the `Illuminate\Http\Resources\Json\JsonResource` class: -->
리소스 클래스를 생성하려면, `make:resource` 아티즌 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉토리에 저장됩니다. 리소스 클래스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다.

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- In addition to generating resources that transform individual models, you may generate resources that are responsible for transforming collections of models. This allows your JSON responses to include links and other meta information that is relevant to an entire collection of a given resource. -->
개별 모델을 변환하는 리소스 이외에도, 모델 컬렉션 변환을 담당하는 리소스를 생성할 수 있습니다. 이렇게 하면 JSON 응답에 컬렉션 전체에 해당하는 링크나 기타 메타 정보를 포함시킬 수 있습니다.

<!-- To create a resource collection, you should use the `--collection` flag when creating the resource. Or, including the word `Collection` in the resource name will indicate to Laravel that it should create a collection resource. Collection resources extend the `Illuminate\Http\Resources\Json\ResourceCollection` class: -->
리소스 컬렉션을 생성하려면, 리소스 생성 시 `--collection` 플래그를 사용합니다. 또는 리소스 명에 `Collection`이라는 단어를 포함시키면 Laravel이 컬렉션 리소스로 인식하여 생성합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다.

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

> [!NOTE]
> 이 부분은 리소스와 리소스 컬렉션에 대한 전반적인 개요입니다. 리소스를 통해 얻을 수 있는 다양한 커스터마이징 기능과 강력한 기능을 더 깊이 이해하려면 다른 섹션들도 반드시 읽어보시기 바랍니다.

<!-- Before diving into all of the options available to you when writing resources, let's first take a high-level look at how resources are used within Laravel. A resource class represents a single model that needs to be transformed into a JSON structure. For example, here is a simple `UserResource` resource class: -->
리소스를 작성할 때 사용할 수 있는 다양한 옵션들을 살펴보기 전에, Laravel에서 리소스가 어떻게 사용되는지 고수준에서 먼저 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 표현합니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스 예제입니다.

```
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
모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트나 컨트롤러 메서드에서 리소스를 응답으로 반환할 때 JSON으로 변환되어야 하는 속성의 배열을 반환합니다.

<!-- Note that we can access model properties directly from the `$this` variable. This is because a resource class will automatically proxy property and method access down to the underlying model for convenient access. Once the resource is defined, it may be returned from a route or controller. The resource accepts the underlying model instance via its constructor: -->
모델 속성에 `$this` 변수를 통해 바로 접근할 수 있다는 점도 주목해야 합니다. 리소스 클래스는 속성 및 메서드 접근을 자동으로 내부 모델에 위임하기 때문에 편리하게 사용할 수 있습니다. 리소스를 정의한 뒤에는 라우트 또는 컨트롤러에서 바로 반환할 수 있습니다. 리소스는 생성자를 통해 내부 모델 인스턴스를 전달받습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
<!-- ### Resource Collections -->
### Resource Collections

<!-- If you are returning a collection of resources or a paginated response, you should use the `collection` method provided by your resource class when creating the resource instance in your route or controller: -->
리소스 컬렉션이나 페이지네이션된 응답을 반환할 경우, 라우트 또는 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용하여 리소스 인스턴스를 생성해야 합니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- Note that this does not allow any addition of custom meta data that may need to be returned with your collection. If you would like to customize the resource collection response, you may create a dedicated resource to represent the collection: -->
다만, 이 방식은 컬렉션과 함께 반환되어야 하는 커스텀 메타 데이터 등은 추가할 수 없습니다. 만약 리소스 컬렉션 응답을 커스터마이즈하고자 한다면, 컬렉션을 표현하는 전용 리소스를 생성하면 됩니다.

```shell
php artisan make:resource UserCollection
```

<!-- Once the resource collection class has been generated, you may easily define any meta data that should be included with the response: -->
리소스 컬렉션 클래스를 생성한 후, 응답에 포함되어야 하는 메타 데이터를 자유롭게 정의할 수 있습니다.

```
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
리소스 컬렉션을 정의한 뒤에는, 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
<!-- #### Preserving Collection Keys -->
#### Preserving Collection Keys

<!-- When returning a resource collection from a route, Laravel resets the collection's keys so that they are in numerical order. However, you may add a `preserveKeys` property to your resource class indicating whether a collection's original keys should be preserved: -->
라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서대로 재설정합니다. 하지만 리소스 클래스에 `preserveKeys` 속성을 추가하면 컬렉션의 원래 키를 유지할 것인지 지정할 수 있습니다.

```
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

<!-- When the `preserveKeys` property is set to `true`, collection keys will be preserved when the collection is returned from a route or controller: -->
`preserveKeys` 속성이 `true`로 설정된 경우, 컬렉션을 라우트나 컨트롤러에서 반환할 때 컬렉션의 키가 원본 그대로 유지됩니다.

```
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
일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단수형 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단수형 리소스 클래스는 컬렉션 클래스명에서 마지막 `Collection` 부분을 뺀 이름과 일치한다고 가정합니다. 또한, 개발자 취향에 따라 단수형 리소스 클래스명 뒤에 `Resource`가 붙어 있을 수도, 없을 수도 있습니다.

<!-- For example, `UserCollection` will attempt to map the given user instances into the `UserResource` resource. To customize this behavior, you may override the `$collects` property of your resource collection: -->
예를 들어, `UserCollection`은 주어진 유저 인스턴스를 `UserResource` 리소스로 변환하려 시도합니다. 이 동작을 커스터마이즈하고 싶을 때는, 리소스 컬렉션의 `$collects` 속성을 오버라이드하면 됩니다.

```
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
<!-- ## Writing Resources -->
## Writing Resources

> [!NOTE]
> [concept overview](#concept-overview)를 아직 읽지 않았다면, 이 문서를 진행하기 전에 먼저 읽어보시기를 강력히 권장합니다.

<!-- Resources only need to transform a given model into an array. So, each resource contains a `toArray` method which translates your model's attributes into an API friendly array that can be returned from your application's routes or controllers: -->
리소스는 주어진 모델을 배열로 변환만 하면 됩니다. 그래서 각 리소스는 `toArray` 메서드를 포함하고 있으며, 이 메서드는 모델의 속성을 API 친화적인 배열로 변환하여 라우트나 컨트롤러에서 응답으로 반환할 수 있게 해줍니다.

```
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
리소스를 정의했다면, 라우트 또는 컨트롤러에서 바로 반환할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- If you would like to include related resources in your response, you may add them to the array returned by your resource's `toArray` method. In this example, we will use the `PostResource` resource's `collection` method to add the user's blog posts to the resource response: -->
응답에 연관된 리소스를 포함하고자 한다면, 리소스의 `toArray` 메서드에서 반환하는 배열에 해당 연관관계를 추가하면 됩니다. 아래 예제에서는 사용자의 블로그 포스트를 응답에 추가하기 위해 `PostResource`의 `collection` 메서드를 사용합니다.

```
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
> 연관관계를 미리 로드되어 있는 경우에만 포함하고자 한다면, [conditional relationships](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- While resources transform a single model into an array, resource collections transform a collection of models into an array. However, it is not absolutely necessary to define a resource collection class for each one of your models since all resources provide a `collection` method to generate an "ad-hoc" resource collection on the fly: -->
리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 모든 모델마다 리소스 컬렉션 클래스를 반드시 만들어야 하는 것은 아닙니다. 모든 리소스는 `collection` 메서드를 제공하므로, 즉석에서 "임시 리소스 컬렉션"을 생성할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- However, if you need to customize the meta data returned with the collection, it is necessary to define your own resource collection: -->
하지만 컬렉션에 함께 반환할 메타 데이터를 커스터마이즈해야 할 경우에는, 직접 컬렉션 리소스를 정의할 필요가 있습니다.

```
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
단수형 리소스처럼, 리소스 컬렉션도 라우트 또는 컨트롤러에서 바로 반환할 수 있습니다.

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
<!-- ### Data Wrapping -->
### Data Wrapping

<!-- By default, your outermost resource is wrapped in a `data` key when the resource response is converted to JSON. So, for example, a typical resource collection response looks like the following: -->
기본적으로, 최상위 리소스는 리소스 응답이 JSON으로 변환될 때 `data` 키로 래핑(wrapping)됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다.

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

<!-- If you would like to disable the wrapping of the outermost resource, you should invoke the `withoutWrapping` method on the base `Illuminate\Http\Resources\Json\JsonResource` class. Typically, you should call this method from your `AppServiceProvider` or another [service provider](/docs/11.x/providers) that is loaded on every request to your application: -->
최상위 리소스의 래핑을 비활성화하고 싶다면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출하면 됩니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 혹은 매 요청마다 로드되는 [service provider](/docs/11.x/providers)에서 호출합니다.

```
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
> `withoutWrapping` 메서드는 오직 최상위 응답에만 영향을 주며, 직접 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
<!-- #### Wrapping Nested Resources -->
#### Wrapping Nested Resources

<!-- You have total freedom to determine how your resource's relationships are wrapped. If you would like all resource collections to be wrapped in a `data` key, regardless of their nesting, you should define a resource collection class for each resource and return the collection within a `data` key. -->
리소스의 연관관계가 어떻게 래핑될지는 전적으로 여러분이 결정할 수 있습니다. 모든 리소스 컬렉션을, 중첩 여부와 무관하게 `data` 키로 래핑하고 싶다면, 각 리소스별로 컬렉션 리소스 클래스를 정의하고 그 안에서 `data` 키에 컬렉션을 반환하면 됩니다.

<!-- You may be wondering if this will cause your outermost resource to be wrapped in two `data` keys. Don't worry, Laravel will never let your resources be accidentally double-wrapped, so you don't have to be concerned about the nesting level of the resource collection you are transforming: -->
혹시 이렇게 할 경우 최상위 리소스가 두 번 이상 `data`로 래핑될까 걱정할 수 있습니다. 걱정하지 않아도 됩니다. Laravel은 절대로 리소스가 중첩되어도 이중 래핑되는 일이 없도록 처리하므로, 리소스 컬렉션의 중첩 정도와 무관하게 걱정하지 않으셔도 됩니다.

```
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
리소스 응답으로 페이지네이션된 컬렉션을 반환할 때는, `withoutWrapping` 메서드를 호출했더라도 Laravel이 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이지네이션 응답이 항상 `meta` 및 `links` 키를 포함하여 페이지네이터의 상태 정보를 반환하기 때문입니다.

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
리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 Laravel 페이지네이터 인스턴스를 넘길 수 있습니다.

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

<!-- Paginated responses always contain `meta` and `links` keys with information about the paginator's state: -->
페이지네이션된 응답은 항상 페이지네이터의 상태 정보를 담은 `meta`와 `links` 키를 포함합니다.

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
페이지네이션 응답의 `links` 또는 `meta` 키에 포함되는 정보를 커스터마이즈하고 싶을 때는 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와, `links`와 `meta` 키를 포함하는 `$default` 배열을 전달받습니다.

```
/**
 * Customize the pagination information for the resource.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  array $paginated
 * @param  array $default
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
특정 조건이 만족될 때만 리소스 응답에 속성을 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 경우에만 특정 값을 포함하고 싶을 수 있습니다. Laravel은 이런 상황을 돕기 위한 여러 헬퍼 메서드를 제공합니다. `when` 메서드를 사용하면 조건에 따라 리소스 응답에 속성을 동적으로 추가할 수 있습니다.

```
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
위 예제에서 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 리소스 응답에 `secret` 키가 포함됩니다. 만약 메서드가 `false`를 반환하면, `secret` 키는 클라이언트로 보내기 전 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 만들면서 조건문을 추가하지 않아도 리소스를 매우 명확하게 정의할 수 있습니다.

<!-- The `when` method also accepts a closure as its second argument, allowing you to calculate the resulting value only if the given condition is `true`: -->
`when` 메서드의 두 번째 인자로 클로저를 넘기면, 주어진 조건이 `true`일 때에만 결과값을 계산하도록 만들 수 있습니다.

```
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

<!-- The `whenHas` method may be used to include an attribute if it is actually present on the underlying model: -->
`whenHas` 메서드는 내부 모델에 실제로 해당 속성이 존재할 때에만 속성을 포함합니다.

```
'name' => $this->whenHas('name'),
```

<!-- Additionally, the `whenNotNull` method may be used to include an attribute in the resource response if the attribute is not null: -->
또한, `whenNotNull` 메서드를 사용해서 속성 값이 null이 아닐 때에만 리소스 응답에 포함시킬 수 있습니다.

```
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>

<!-- #### Merging Conditional Attributes -->
#### Merging Conditional Attributes

<!-- Sometimes you may have several attributes that should only be included in the resource response based on the same condition. In this case, you may use the `mergeWhen` method to include the attributes in the response only when the given condition is `true`: -->
여러 속성을 동일한 조건에 따라 리소스 응답에 포함해야 하는 경우가 있습니다. 이럴 때는 `mergeWhen` 메서드를 사용하여, 해당 조건이 `true`일 때만 여러 속성을 응답에 포함시킬 수 있습니다.

```
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
여기서도 마찬가지로, 지정한 조건이 `false`라면 해당 속성들은 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 섞여 있는 배열 내에서 사용해서는 안 됩니다. 또한, 순차적으로 정렬되어 있지 않은 숫자 키 배열 내에서도 사용해서는 안 됩니다.

<a name="conditional-relationships"></a>
<!-- ### Conditional Relationships -->
### Conditional Relationships

<!-- In addition to conditionally loading attributes, you may conditionally include relationships on your resource responses based on if the relationship has already been loaded on the model. This allows your controller to decide which relationships should be loaded on the model and your resource can easily include them only when they have actually been loaded. Ultimately, this makes it easier to avoid "N+1" query problems within your resources. -->
속성의 조건부 로딩 뿐 아니라, 모델에 특정 연관관계가 이미 로드된 경우에만 이를 리소스 응답에 포함시킬 수 있습니다. 이를 통해 어떤 연관관계가 모델에 로드될지 컨트롤러에서 결정할 수 있고, 리소스에서는 실제로 로드된 경우에만 쉽게 포함시킬 수 있습니다. 궁극적으로, 이는 리소스 내부에서 "N+1" 쿼리 문제를 쉽게 피하도록 도와줍니다.

<!-- The `whenLoaded` method may be used to conditionally load a relationship. In order to avoid unnecessarily loading relationships, this method accepts the name of the relationship instead of the relationship itself: -->
`whenLoaded` 메서드를 사용하면 조건에 따라 연관관계를 로딩할 수 있습니다. 불필요하게 연관관계를 로딩하지 않기 위해, 이 메서드는 연관관계 객체가 아닌 연관관계의 이름을 인수로 받습니다.

```
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
이 예시에서, 연관관계가 로드되어 있지 않으면, `posts` 키는 클라이언트로 전송되기 전 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
<!-- #### Conditional Relationship Counts -->
#### Conditional Relationship Counts

<!-- In addition to conditionally including relationships, you may conditionally include relationship "counts" on your resource responses based on if the relationship's count has been loaded on the model: -->
연관관계 자체뿐 아니라, 연관관계의 "개수(Count)" 정보도 모델에 미리 로드되어 있는 경우에만 리소스 응답에 포함시킬 수 있습니다.

```
new UserResource($user->loadCount('posts'));
```

<!-- The `whenCounted` method may be used to conditionally include a relationship's count in your resource response. This method avoids unnecessarily including the attribute if the relationships' count is not present: -->
`whenCounted` 메서드를 사용하면 연관관계의 개수를 조건부로 리소스 응답에 포함할 수 있습니다. 이 메서드는 연관관계의 개수가 존재하지 않는 경우 불필요하게 속성을 포함하지 않습니다.

```
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
이 예시에서, `posts` 연관관계의 개수가 로드되어 있지 않으면 `posts_count` 키가 응답에서 제거되어 클라이언트로 전송되지 않습니다.

<!-- Other types of aggregates, such as `avg`, `sum`, `min`, and `max` may also be conditionally loaded using the `whenAggregated` method: -->
`avg`, `sum`, `min`, `max`와 같은 다른 종류의 집계 정보도 `whenAggregated` 메서드를 이용해 조건부로 로딩할 수 있습니다.

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
리소스 응답에서 연관관계 정보를 조건부로 포함하는 것 외에도, 다대다(many-to-many) 연관관계의 중간 테이블로부터 데이터를 `whenPivotLoaded` 메서드로 조건부로 포함할 수 있습니다. `whenPivotLoaded` 메서드의 첫 번째 인수는 피벗 테이블의 이름이며, 두 번째 인수는 피벗 정보가 모델에 존재할 때 반환할 값을 반환하는 클로저입니다.

```
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

<!-- If your relationship is using a [custom intermediate table model](/docs/11.x/eloquent-relationships#defining-custom-intermediate-table-models), you may pass an instance of the intermediate table model as the first argument to the `whenPivotLoaded` method: -->
연관관계에서 [custom intermediate table model](/docs/11.x/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, `whenPivotLoaded` 메서드의 첫 번째 인수로 중간 테이블 모델의 인스턴스를 전달할 수 있습니다.

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

<!-- If your intermediate table is using an accessor other than `pivot`, you may use the `whenPivotLoadedAs` method: -->
그리고 중간 테이블이 `pivot`이 아닌 다른 accessor를 사용할 경우에는 `whenPivotLoadedAs` 메서드를 사용할 수 있습니다.

```
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
일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타 데이터를 추가해야 하는 경우가 있습니다. 여기에는 종종 리소스에 대한 `links`나 관련 리소스, 또는 리소스 자체에 대한 메타 정보 등이 포함됩니다. 리소스에 추가 메타 데이터를 반환해야 한다면, `toArray` 메서드 내부에 포함시키면 됩니다. 예를 들어, 리소스 컬렉션을 변환하는 과정에서 `links` 정보를 포함시킬 수 있습니다.

```
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
리소스에서 추가적인 메타 데이터를 반환할 때는, Laravel이 페이징 응답을 반환하면서 자동으로 추가하는 `links`나 `meta` 키를 실수로 덮어쓸 걱정을 할 필요가 없습니다. 직접 정의한 모든 `links` 값은 페이지네이터가 제공하는 링크와 자동으로 병합됩니다.

<a name="top-level-meta-data"></a>
<!-- #### Top Level Meta Data -->
#### Top Level Meta Data

<!-- Sometimes you may wish to only include certain meta data with a resource response if the resource is the outermost resource being returned. Typically, this includes meta information about the response as a whole. To define this meta data, add a `with` method to your resource class. This method should return an array of meta data to be included with the resource response only when the resource is the outermost resource being transformed: -->
때때로 리소스가 "가장 바깥에 있는 리소스"로 반환될 때만 특정 메타 데이터를 응답에 추가하고 싶을 수 있습니다. 일반적으로 전체 응답에 대한 메타 정보가 이에 해당합니다. 이런 경우를 위해, 리소스 클래스에 `with` 메서드를 추가하면 됩니다. 이 메서드는 해당 리소스가 최상위 리소스로 변환될 때만 리소스 응답에 포함될 메타 데이터 배열을 반환해야 합니다.

```
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
또한, 라우트나 컨트롤러에서 리소스 인스턴스를 생성하는 시점에 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 응답에 추가할 데이터를 배열로 받아들입니다.

```
return (new UserCollection(User::all()->load('roles')))
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
<!-- ## Resource Responses -->
## Resource Responses

<!-- As you have already read, resources may be returned directly from routes and controllers: -->
앞서 살펴본 것처럼, 리소스는 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<!-- However, sometimes you may need to customize the outgoing HTTP response before it is sent to the client. There are two ways to accomplish this. First, you may chain the `response` method onto the resource. This method will return an `Illuminate\Http\JsonResponse` instance, giving you full control over the response's headers: -->
하지만 경우에 따라, 응답이 클라이언트로 전달되기 전에 HTTP 응답 객체를 커스터마이징해야 할 때가 있습니다. 이를 해결하는 방법은 두 가지가 있습니다. 첫 번째로, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답 헤더 등 전체 응답을 자유롭게 제어할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
        ->response()
        ->header('X-Value', 'True');
});
```

<!-- Alternatively, you may define a `withResponse` method within the resource itself. This method will be called when the resource is returned as the outermost resource in a response: -->
또 다른 방법으로는, 리소스 클래스 내부에 `withResponse` 메서드를 정의하는 것입니다. 이 메서드는 리소스가 응답의 최상위(가장 바깥) 리소스로 반환될 때 호출됩니다.

```
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