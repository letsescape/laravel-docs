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
API를 구축할 때, Eloquent 모델과 실제로 사용자에게 반환되는 JSON 응답 사이에서 동작하는 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자들에게만 일부 속성을 표시하고 싶거나, 항상 모델의 특정 연관관계를 JSON 표현에 포함시키고 싶을 수 있습니다. Eloquent의 리소스 클래스는 이러한 변환을 명확하고 손쉽게 할 수 있게 해줍니다.

<!-- Of course, you may always convert Eloquent models or collections to JSON using their `toJson` methods; however, Eloquent resources provide more granular and robust control over the JSON serialization of your models and their relationships. -->
물론, Eloquent 모델 또는 컬렉션의 `toJson` 메서드를 사용해 직접 JSON으로 변환할 수도 있습니다. 하지만 Eloquent 리소스를 사용하면 모델과 그 연관관계의 JSON 직렬화 과정을 더욱 세밀하고 강력하게 제어할 수 있습니다.

<a name="generating-resources"></a>
<!-- ## Generating Resources -->
## Generating Resources

<!-- To generate a resource class, you may use the `make:resource` Artisan command. By default, resources will be placed in the `app/Http/Resources` directory of your application. Resources extend the `Illuminate\Http\Resources\Json\JsonResource` class: -->
리소스 클래스를 생성하려면, `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 생성됩니다. 리소스 클래스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다.

```
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- In addition to generating resources that transform individual models, you may generate resources that are responsible for transforming collections of models. This allows your JSON responses to include links and other meta information that is relevant to an entire collection of a given resource. -->
개별 모델을 변환하는 리소스뿐만 아니라, 모델 컬렉션을 변환하는 데 특화된 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 해당 리소스 전체 컬렉션과 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

<!-- To create a resource collection, you should use the `--collection` flag when creating the resource. Or, including the word `Collection` in the resource name will indicate to Laravel that it should create a collection resource. Collection resources extend the `Illuminate\Http\Resources\Json\ResourceCollection` class: -->
컬렉션 리소스를 생성하려면 리소스 생성 시 `--collection` 플래그를 사용하면 됩니다. 또는 리소스 이름에 `Collection`이 포함되어 있으면 Laravel은 해당 리소스가 컬렉션 리소스임을 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다.

```
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

> [!TIP]
> 이 섹션은 리소스 및 리소스 컬렉션에 대한 상위 개념을 다룹니다. 리소스의 커스터마이징 및 다양한 기능에 대해 더 깊이 이해하고 싶다면, 문서의 다른 섹션도 꼭 읽어보시기 바랍니다.

<!-- Before diving into all of the options available to you when writing resources, let's first take a high-level look at how resources are used within Laravel. A resource class represents a single model that needs to be transformed into a JSON structure. For example, here is a simple `UserResource` resource class: -->
리소스를 작성할 때 활용할 수 있는 다양한 옵션을 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환이 필요한 단일 모델을 나타냅니다. 예를 들어, 다음은 `UserResource`라는 간단한 리소스 클래스의 예시입니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
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
각 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 해당 리소스를 라우트나 컨트롤러 메서드에서 응답으로 반환할 때 JSON으로 변환되어야 할 속성들의 배열을 반환합니다.

<!-- Note that we can access model properties directly from the `$this` variable. This is because a resource class will automatically proxy property and method access down to the underlying model for convenient access. Once the resource is defined, it may be returned from a route or controller. The resource accepts the underlying model instance via its constructor: -->
리소스 클래스 내에서 `$this` 변수로 모델의 속성에 직접 접근할 수 있습니다. 이는 리소스 클래스가 프로퍼티 및 메서드 접근 권한을 자동으로 내부 모델에 전달해주기 때문입니다. 정의한 리소스는 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다. 리소스 생성자에는 변환 대상이 되는 모델 인스턴스를 전달합니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
<!-- ### Resource Collections -->
### Resource Collections

<!-- If you are returning a collection of resources or a paginated response, you should use the `collection` method provided by your resource class when creating the resource instance in your route or controller: -->
여러 리소스가 담긴 컬렉션이나 페이지네이션 응답을 반환할 때는 라우트나 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용하여 인스턴스를 생성하는 것이 좋습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- Note that this does not allow any addition of custom meta data that may need to be returned with your collection. If you would like to customize the resource collection response, you may create a dedicated resource to represent the collection: -->
이 방법으로는 컬렉션과 함께 반환될 커스텀 메타데이터를 추가할 수 없습니다. 컬렉션 응답에 맞춤형 데이터를 포함시키고 싶다면 컬렉션 전용 리소스 클래스를 따로 생성해야 합니다.

```
php artisan make:resource UserCollection
```

<!-- Once the resource collection class has been generated, you may easily define any meta data that should be included with the response: -->
생성된 컬렉션 리소스 클래스에서는 응답과 함께 포함시킬 메타데이터를 쉽게 정의할 수 있습니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
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
정의한 컬렉션 리소스는 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다.

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
라우트에서 리소스 컬렉션을 반환하면, Laravel은 기본적으로 컬렉션의 키를 숫자 순서대로 재정렬합니다. 그러나 컬렉션의 원래 키를 그대로 유지하려면 리소스 클래스에 `preserveKeys` 속성을 추가하면 됩니다.

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
`preserveKeys` 속성이 `true`로 설정된 경우, 라우트나 컨트롤러에서 컬렉션을 반환할 때 컬렉션의 키가 그대로 반영됩니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
<!-- #### Customizing The Underlying Resource Class -->
#### Customizing The Underlying Resource Class

<!-- Typically, the `$this->collection` property of a resource collection is automatically populated with the result of mapping each item of the collection to its singular resource class. The singular resource class is assumed to be the collection's class name without the trailing `Collection` portion of the class name. In addition, depending on your personal preference, the singular resource class may or may not be suffixed with `Resource`. -->
일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 아이템을 단수형 리소스 클래스로 매핑한 결과로 자동 채워집니다. 이때 단수형 리소스 클래스는 컬렉션 클래스의 이름에서 `Collection`을 제거한 이름(또는 필요에 따라 `Resource` 접미사가 붙기도 함)으로 추정합니다.

<!-- For example, `UserCollection` will attempt to map the given user instances into the `UserResource` resource. To customize this behavior, you may override the `$collects` property of your resource collection: -->
예를 들어, `UserCollection`은 전달된 각 유저 인스턴스를 `UserResource`로 변환합니다. 이 동작 방식을 커스터마이즈하고 싶다면, 컬렉션 리소스 클래스의 `$collects` 속성을 오버라이드하면 됩니다.

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

> [!TIP]
> [concept overview](#concept-overview) 섹션을 아직 읽지 않았다면, 이 문서를 계속 진행하기 전에 꼭 읽어보시기를 권장합니다.

<!-- In essence, resources are simple. They only need to transform a given model into an array. So, each resource contains a `toArray` method which translates your model's attributes into an API friendly array that can be returned from your application's routes or controllers: -->
리소스의 본질은 매우 단순합니다. 주어진 모델을 배열로 변환하기만 하면 됩니다. 각 리소스는 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메서드를 포함합니다. 이 배열은 애플리케이션의 라우트 또는 컨트롤러에서 반환할 수 있습니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
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
정의한 리소스는 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- If you would like to include related resources in your response, you may add them to the array returned by your resource's `toArray` method. In this example, we will use the `PostResource` resource's `collection` method to add the user's blog posts to the resource response: -->
응답에 관련 리소스(연관관계된 데이터)를 함께 포함하고 싶다면, `toArray` 메서드의 반환 배열에 해당 리소스를 추가하면 됩니다. 예를 들어, `PostResource`의 `collection` 메서드를 사용해 사용자의 블로그 게시글 정보를 포함시킬 수 있습니다.

```
use App\Http\Resources\PostResource;

/**
 * Transform the resource into an array.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
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

> [!TIP]
> 연관관계를 로드된 경우에만 포함하려면, [conditional relationships](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- While resources transform a single model into an array, resource collections transform a collection of models into an array. However, it is not absolutely necessary to define a resource collection class for each one of your models since all resources provide a `collection` method to generate an "ad-hoc" resource collection on the fly: -->
단일 리소스는 하나의 모델을 배열로 변환하지만, 리소스 컬렉션은 여러 모델의 컬렉션을 배열로 변환합니다. 모든 모델마다 별도의 리소스 컬렉션 클래스를 정의할 필요는 없습니다. 모든 리소스는 `collection` 메서드를 제공하므로, 해당 리소스를 즉석에서 컬렉션 형태로 쉽게 만들 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- However, if you need to customize the meta data returned with the collection, it is necessary to define your own resource collection: -->
하지만 컬렉션과 함께 반환할 메타데이터를 커스터마이즈해야 한다면, 별도의 컬렉션 리소스를 직접 정의해야 합니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
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
단수형 리소스와 마찬가지로 컬렉션 리소스 역시 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

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
기본적으로 최상위 리소스가 JSON으로 변환될 때, 응답은 `data` 키로 감싸져 반환됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같이 보입니다.

```
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com",
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com",
        }
    ]
}
```

<!-- If you would like to use a custom key instead of `data`, you may define a `$wrap` attribute on the resource class: -->
`data` 대신 다른 키를 사용하고 싶으면 리소스 클래스에 `$wrap` 속성을 정의하면 됩니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * The "data" wrapper that should be applied.
     *
     * @var string
     */
    public static $wrap = 'user';
}
```

<!-- If you would like to disable the wrapping of the outermost resource, you should invoke the `withoutWrapping` method on the base `Illuminate\Http\Resources\Json\JsonResource` class. Typically, you should call this method from your `AppServiceProvider` or another [service provider](/docs/8.x/providers) that is loaded on every request to your application: -->
최상위 리소스의 래핑을 아예 비활성화하고 싶으면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출해야 합니다. 보통 이 메서드는 `AppServiceProvider` 또는 모든 요청에서 로드되는 [service provider](/docs/8.x/providers)에서 호출해야 합니다.

```
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!NOTE]
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 미치며, 직접 리소스 컬렉션 내에 추가한 `data` 키는 제거되지 않습니다.

<a name="wrapping-nested-resources"></a>
<!-- #### Wrapping Nested Resources -->
#### Wrapping Nested Resources

<!-- You have total freedom to determine how your resource's relationships are wrapped. If you would like all resource collections to be wrapped in a `data` key, regardless of their nesting, you should define a resource collection class for each resource and return the collection within a `data` key. -->
리소스의 연관관계(즉, 중첩된 리소스)가 어떻게 감싸질지는 직접 결정할 수 있습니다. 중첩 여부에 관계없이 모든 리소스 컬렉션을 `data` 키로 감싸고 싶다면, 각 리소스마다 컬렉션 리소스 클래스를 만들어 반환 시 `data` 키로 래핑하면 됩니다.

<!-- You may be wondering if this will cause your outermost resource to be wrapped in two `data` keys. Don't worry, Laravel will never let your resources be accidentally double-wrapped, so you don't have to be concerned about the nesting level of the resource collection you are transforming: -->
혹시 최상위 리소스가 `data` 키로 두 번 감싸지게 되지 않을까 걱정할 수도 있겠지만, Laravel은 리소스가 실수로 중복 감싸짐이 발생하지 않도록 자동으로 처리해 줍니다. 따라서 컬렉션 리소스의 중첩 레벨에 신경 쓸 필요가 없습니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return ['data' => $this->collection];
    }
}
```

<a name="data-wrapping-and-pagination"></a>
<!-- #### Data Wrapping And Pagination -->
#### Data Wrapping And Pagination

<!-- When returning paginated collections via a resource response, Laravel will wrap your resource data in a `data` key even if the `withoutWrapping` method has been called. This is because paginated responses always contain `meta` and `links` keys with information about the paginator's state: -->
페이지네이션이 적용된 컬렉션을 리소스 응답으로 반환할 때는, 비록 `withoutWrapping` 메서드를 호출했더라도 Laravel은 항상 데이터를 `data` 키로 감싸서 반환합니다. 이는 페이지네이션 응답이 항상 `meta` 와 `links` 키를 포함하기 때문입니다.

```
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com",
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com",
        }
    ],
    "links":{
        "first": "http://example.com/pagination?page=1",
        "last": "http://example.com/pagination?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/pagination",
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
Laravel의 페이지네이터 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 건네줄 수 있습니다.

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

<!-- Paginated responses always contain `meta` and `links` keys with information about the paginator's state: -->
페이지네이션 응답은 항상 페이지네이터의 상태 정보를 담은 `meta`와 `links` 키를 포함합니다.

```
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com",
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com",
        }
    ],
    "links":{
        "first": "http://example.com/pagination?page=1",
        "last": "http://example.com/pagination?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/pagination",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="conditional-attributes"></a>
<!-- ### Conditional Attributes -->
### Conditional Attributes

<!-- Sometimes you may wish to only include an attribute in a resource response if a given condition is met. For example, you may wish to only include a value if the current user is an "administrator". Laravel provides a variety of helper methods to assist you in this situation. The `when` method may be used to conditionally add an attribute to a resource response: -->
특정 조건이 충족될 때만 리소스 응답에 속성을 포함시키고 싶은 경우가 있습니다. 예를 들어, 현재 사용자가 "관리자"인 경우에만 특정 값을 포함하고 싶을 수 있습니다. 이런 상황에서 사용할 수 있는 다양한 헬퍼 메서드가 제공됩니다. `when` 메서드는 특정 조건이 참일 때만 속성을 리소스 응답에 포함할 수 있도록 해줍니다.

```
use Illuminate\Support\Facades\Auth;

/**
 * Transform the resource into an array.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'secret' => $this->when(Auth::user()->isAdmin(), 'secret-value'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

<!-- In this example, the `secret` key will only be returned in the final resource response if the authenticated user's `isAdmin` method returns `true`. If the method returns `false`, the `secret` key will be removed from the resource response before it is sent to the client. The `when` method allows you to expressively define your resources without resorting to conditional statements when building the array. -->
위 예시에서 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환하는 경우에만 최종 리소스 응답에 `secret` 키가 포함됩니다. 만약 `false`를 반환하면, `secret` 키는 클라이언트로 반환되기 전 리소스 응답에서 자동으로 제거됩니다. `when` 메서드를 사용하면 조건문 없이도 더욱 명확하게 속성의 포함 여부를 정의할 수 있습니다.

<!-- The `when` method also accepts a closure as its second argument, allowing you to calculate the resulting value only if the given condition is `true`: -->
또한 `when` 메서드의 두 번째 인자로 클로저를 전달할 수도 있는데, 이 경우 주어진 조건이 `true`일 때만 해당 값을 계산합니다.

```
'secret' => $this->when(Auth::user()->isAdmin(), function () {
    return 'secret-value';
}),
```

<a name="merging-conditional-attributes"></a>
<!-- #### Merging Conditional Attributes -->
#### Merging Conditional Attributes

<!-- Sometimes you may have several attributes that should only be included in the resource response based on the same condition. In this case, you may use the `mergeWhen` method to include the attributes in the response only when the given condition is `true`: -->
여러 개의 속성이 동일한 조건에서만 응답에 포함되어야 할 때가 있습니다. 이런 경우 `mergeWhen` 메서드를 사용하면, 주어진 조건이 `true`일 때에만 해당 속성들을 한 번에 응답에 추가할 수 있습니다.

```
/**
 * Transform the resource into an array.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        $this->mergeWhen(Auth::user()->isAdmin(), [
            'first-secret' => 'value',
            'second-secret' => 'value',
        ]),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

<!-- Again, if the given condition is `false`, these attributes will be removed from the resource response before it is sent to the client. -->
조건이 `false`인 경우, 이 속성들은 리소스 응답에서 자동으로 제거되어 클라이언트로 전송되지 않습니다.

> [!NOTE]
> `mergeWhen` 메서드는 문자 키와 숫자 키가 혼합된 배열이나, 순차적으로 정렬되지 않은 숫자 키 배열에서는 사용하지 않는 것이 좋습니다.

<a name="conditional-relationships"></a>
<!-- ### Conditional Relationships -->
### Conditional Relationships

<!-- In addition to conditionally loading attributes, you may conditionally include relationships on your resource responses based on if the relationship has already been loaded on the model. This allows your controller to decide which relationships should be loaded on the model and your resource can easily include them only when they have actually been loaded. Ultimately, this makes it easier to avoid "N+1" query problems within your resources. -->
속성뿐 아니라, 연관관계를 미리 로드한 경우에만 리소스 응답에 포함시키고 싶을 수도 있습니다. 이렇게 하면 컨트롤러에서 어떤 연관관계를 가져올지 결정하고, 리소스에서는 실제로 로드된 경우에만 응답에 포함할 수 있습니다. 결과적으로 리소스를 사용할 때 N+1 쿼리 문제를 효과적으로 피할 수 있습니다.

<!-- The `whenLoaded` method may be used to conditionally load a relationship. In order to avoid unnecessarily loading relationships, this method accepts the name of the relationship instead of the relationship itself: -->
`whenLoaded` 메서드를 사용하면 연관관계의 이름을 전달하여, 해당 연관관계가 이미 로드된 경우에만 응답에 포함할 수 있습니다. (연관관계 객체가 아닌 '이름'을 전달해야 불필요하게 쿼리를 실행하지 않습니다.)

```
use App\Http\Resources\PostResource;

/**
 * Transform the resource into an array.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
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
이 예시에서 해당 연관관계가 로드되지 않았다면, 클라이언트로 응답이 전송되기 전에 `posts` 키가 리소스 응답에서 제거됩니다.

<a name="conditional-pivot-information"></a>
<!-- #### Conditional Pivot Information -->
#### Conditional Pivot Information

<!-- In addition to conditionally including relationship information in your resource responses, you may conditionally include data from the intermediate tables of many-to-many relationships using the `whenPivotLoaded` method. The `whenPivotLoaded` method accepts the name of the pivot table as its first argument. The second argument should be a closure that returns the value to be returned if the pivot information is available on the model: -->
연관관계 데이터뿐 아니라 다대다(many-to-many) 연관관계에서 중간 테이블(피벗 테이블) 정보를 `whenPivotLoaded` 메서드를 사용해 조건부로 리소스 응답에 포함할 수도 있습니다. `whenPivotLoaded` 메서드는 첫 번째 인자로 피벗 테이블명을, 두 번째 인자로는 해당 피벗 정보가 모델에 제공된 경우 반환할 값을 전달하는 클로저를 받습니다.

```
/**
 * Transform the resource into an array.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
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

<!-- If your relationship is using a [custom intermediate table model](/docs/8.x/eloquent-relationships#defining-custom-intermediate-table-models), you may pass an instance of the intermediate table model as the first argument to the `whenPivotLoaded` method: -->
[custom intermediate table model](/docs/8.x/eloquent-relationships#defining-custom-intermediate-table-models)를 사용하는 경우, `whenPivotLoaded` 메서드의 첫 번째 인자로 중간 테이블 모델 인스턴스를 전달할 수 있습니다.

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

<!-- If your intermediate table is using an accessor other than `pivot`, you may use the `whenPivotLoadedAs` method: -->
중간 테이블의 accessor가 `pivot`이 아닌 다른 이름을 사용하는 경우에는 `whenPivotLoadedAs` 메서드를 활용할 수 있습니다.

```
/**
 * Transform the resource into an array.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
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

<!-- Some JSON API standards require the addition of meta data to your resource and resource collections responses. This often includes things like `links` to the resource or related resources, or meta data about the resource itself. If you need to return additional meta data about a resource, include it in your `toArray` method. For example, you might include `link` information when transforming a resource collection: -->
일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타데이터를 추가해야 할 수도 있습니다. 여기에는 리소스나 관련 리소스에 대한 `links`, 또는 리소스 자체에 대한 메타 정보 등이 포함될 수 있습니다. 추가 메타데이터를 반환해야 한다면, `toArray` 메서드 내에 해당 정보를 포함시키면 됩니다. 예를 들어, 리소스 컬렉션을 변환할 때 `link` 정보를 포함할 수 있습니다.

```
/**
 * Transform the resource into an array.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
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
추가 메타데이터를 리소스에서 반환할 때, 페이지네이션 응답에 자동으로 추가되는 `links`나 `meta`를 덮어쓸까 걱정할 필요가 없습니다. 직접 정의한 `links`는 페이지네이터에서 제공하는 링크와 자동으로 병합됩니다.

<a name="top-level-meta-data"></a>
<!-- #### Top Level Meta Data -->
#### Top Level Meta Data

<!-- Sometimes you may wish to only include certain meta data with a resource response if the resource is the outermost resource being returned. Typically, this includes meta information about the response as a whole. To define this meta data, add a `with` method to your resource class. This method should return an array of meta data to be included with the resource response only when the resource is the outermost resource being transformed: -->
때로는 리소스가 최상위로 반환되는 경우에만 특정 메타데이터를 응답에 포함시키고 싶을 수 있습니다. 주로 응답 전체에 대한 메타 정보 등이 이에 해당합니다. 이런 메타데이터를 정의하려면 리소스 클래스에 `with` 메서드를 추가하면 됩니다. 이 메서드는 리소스가 최상위로 변환될 때만 함께 반환되는 메타데이터 배열을 반환합니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return parent::toArray($request);
    }

    /**
     * Get additional data that should be returned with the resource array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function with($request)
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
라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 추가적인 최상위 데이터를 넣어줄 수도 있습니다. 모든 리소스에서 사용 가능한 `additional` 메서드는 응답에 함께 추가할 데이터를 배열 형태로 받을 수 있습니다.

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
앞서 살펴본 것처럼, 리소스는 라우트와 컨트롤러에서 직접 반환할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<!-- However, sometimes you may need to customize the outgoing HTTP response before it is sent to the client. There are two ways to accomplish this. First, you may chain the `response` method onto the resource. This method will return an `Illuminate\Http\JsonResponse` instance, giving you full control over the response's headers: -->
하지만 경우에 따라, 클라이언트로 전달되기 전에 HTTP 응답을 커스터마이즈해야 할 수 있습니다. 이를 위한 방법은 두 가지가 있습니다. 먼저, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답 헤더 등의 세부 설정을 자유롭게 변경할 수 있습니다.

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
또는, 리소스 클래스 내에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 최상위 리소스로 응답될 때 호출됩니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return [
            'id' => $this->id,
        ];
    }

    /**
     * Customize the outgoing response for the resource.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Illuminate\Http\Response  $response
     * @return void
     */
    public function withResponse($request, $response)
    {
        $response->header('X-Value', 'True');
    }
}
```
