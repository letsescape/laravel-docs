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
API를 개발할 때, Eloquent 모델과 사용자가 실제로 받게 되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자에게만 일부 속성을 보여주고 싶거나, 모델의 JSON 표현에 항상 특정 연관관계를 포함하고 싶을 때가 있을 수 있습니다. Eloquent의 리소스 클래스는 모델 및 모델 컬렉션을 JSON으로 변환하는 작업을 명확하고 쉽게 처리할 수 있도록 도와줍니다.

<!-- Of course, you may always convert Eloquent models or collections to JSON using their `toJson` methods; however, Eloquent resources provide more granular and robust control over the JSON serialization of your models and their relationships. -->
물론, Eloquent 모델이나 컬렉션에 있는 `toJson` 메서드를 사용해 JSON으로 바로 변환할 수도 있습니다. 하지만, Eloquent 리소스를 사용하면 모델과 연관관계의 JSON 직렬화 과정을 더욱 세밀하고 견고하게 제어할 수 있습니다.

<a name="generating-resources"></a>
<!-- ## Generating Resources -->
## Generating Resources

<!-- To generate a resource class, you may use the `make:resource` Artisan command. By default, resources will be placed in the `app/Http/Resources` directory of your application. Resources extend the `Illuminate\Http\Resources\Json\JsonResource` class: -->
리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스 파일은 애플리케이션의 `app/Http/Resources` 디렉토리에 생성됩니다. 리소스 클래스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다.

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- In addition to generating resources that transform individual models, you may generate resources that are responsible for transforming collections of models. This allows your JSON responses to include links and other meta information that is relevant to an entire collection of a given resource. -->
개별 모델을 변환하는 리소스뿐만 아니라, 여러 모델로 이루어진 컬렉션을 변환하는 리소스도 만들 수 있습니다. 컬렉션 리소스를 통해, JSON 응답에 전체 컬렉션에 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

<!-- To create a resource collection, you should use the `--collection` flag when creating the resource. Or, including the word `Collection` in the resource name will indicate to Laravel that it should create a collection resource. Collection resources extend the `Illuminate\Http\Resources\Json\ResourceCollection` class: -->
컬렉션 리소스를 생성하려면, 리소스 생성 시 `--collection` 플래그를 사용하면 됩니다. 또는, 리소스 이름에 `Collection`이라는 단어를 포함시키면 Laravel이 컬렉션 리소스를 생성하도록 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속받습니다.

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

> [!NOTE]
> 이 부분은 리소스와 리소스 컬렉션에 관한 높은 수준의 개요입니다. 리소스가 제공하는 확장성 및 커스터마이징에 대해 더 깊이 이해하려면 이 문서의 다른 섹션들도 꼭 읽어보시기 바랍니다.

<!-- Before diving into all of the options available to you when writing resources, let's first take a high-level look at how resources are used within Laravel. A resource class represents a single model that needs to be transformed into a JSON structure. For example, here is a simple `UserResource` resource class: -->
리소스 작성 시 활용할 수 있는 다양한 옵션을 살펴보기 전에, Laravel에서 리소스를 어떻게 사용하는지 먼저 간단히 알아보겠습니다. 리소스 클래스는 JSON 구조로 변환이 필요한 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다.

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
모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트나 컨트롤러 메서드에서 리소스가 응답으로 반환될 때 JSON으로 변환될 속성 배열을 반환합니다.

<!-- Note that we can access model properties directly from the `$this` variable. This is because a resource class will automatically proxy property and method access down to the underlying model for convenient access. Once the resource is defined, it may be returned from a route or controller. The resource accepts the underlying model instance via its constructor: -->
여기서 `$this` 변수로 모델 속성에 바로 접근할 수 있는 이유는, 리소스 클래스가 속성이나 메서드 접근을 자동으로 내부 모델에 위임하기 때문입니다. 이렇게 정의한 리소스는 라우트나 컨트롤러에서 바로 반환할 수 있으며, 생성자에서 해당 모델 인스턴스를 전달받습니다.

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
여러 개의 리소스, 또는 페이지네이션된 응답을 반환할 때는, 라우트나 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용해 인스턴스를 만들어야 합니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- Note that this does not allow any addition of custom meta data that may need to be returned with your collection. If you would like to customize the resource collection response, you may create a dedicated resource to represent the collection: -->
이 방법은 컬렉션에 함께 반환해야 하는 커스텀 메타 데이터를 추가할 수는 없습니다. 컬렉션 응답에 커스텀 데이터를 추가하려면, 컬렉션을 표현하는 전용 리소스를 생성해야 합니다.

```shell
php artisan make:resource UserCollection
```

<!-- Once the resource collection class has been generated, you may easily define any meta data that should be included with the response: -->
컬렉션 리소스가 생성되면, 응답에 포함해야 할 메타 데이터도 다음과 같이 정의할 수 있습니다.

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
이렇게 정의한 리소스 컬렉션은 다음과 같이 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

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
리소스 컬렉션을 라우트에서 반환할 때 Laravel은 기본적으로 컬렉션의 키를 0부터 시작하는 순차적인 숫자 키로 재설정합니다. 그러나, 컬렉션의 원래 키를 그대로 유지하고 싶다면 리소스 클래스에 `preserveKeys` 속성을 추가하여 설정하면 됩니다.

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
`preserveKeys` 속성을 `true`로 설정하면, 컬렉션을 라우트나 컨트롤러에서 반환할 때 컬렉션의 키가 원래대로 유지됩니다.

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
일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목이 단일 리소스 클래스로 매핑된 결과로 자동 채워집니다. 기본적으로 컬렉션 리소스의 클래스명에서 `Collection`을 뺀 이름이 단일 리소스 클래스로 간주됩니다. 또한, 개발자의 선호에 따라 단일 리소스 클래스에 `Resource` 접미사가 붙을 수도 있고 그렇지 않을 수도 있습니다.

<!-- For example, `UserCollection` will attempt to map the given user instances into the `UserResource` resource. To customize this behavior, you may override the `$collects` property of your resource collection: -->
예를 들어, `UserCollection`은 전달된 사용자 인스턴스들을 `UserResource`로 매핑합니다. 이러한 동작을 커스터마이즈하려면 `$collects` 속성을 오버라이드하면 됩니다.

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
> [concept overview](#concept-overview) 섹션을 아직 읽지 않았다면, 이 문서를 계속 읽기 전에 해당 내용을 먼저 읽어보시는 것을 적극 권장합니다.

<!-- In essence, resources are simple. They only need to transform a given model into an array. So, each resource contains a `toArray` method which translates your model's attributes into an API friendly array that can be returned from your application's routes or controllers: -->
본질적으로 리소스는 매우 단순합니다. 주어진 모델을 배열로 변환만 하면 되기 때문입니다. 각 리소스에는 `toArray` 메서드가 포함되어 있으며, 이 메서드는 모델의 속성을 API에 적합한 배열로 변환해 라우트나 컨트롤러에서 반환할 수 있도록 만듭니다.

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
이렇게 리소스를 정의하면 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

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
응답에 연관된 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드의 반환 배열에 추가하면 됩니다. 아래 예시는 `PostResource`의 `collection` 메서드를 활용해 사용자의 블로그 게시글을 리소스 응답에 담은 예시입니다.

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

> [!NOTE]
> 연관관계를 모델에 이미 로드한 경우에만 포함하고 싶다면 [conditional relationships](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- While resources transform a single model into an array, resource collections transform a collection of models into an array. However, it is not absolutely necessary to define a resource collection class for each one of your models since all resources provide a `collection` method to generate an "ad-hoc" resource collection on the fly: -->
단일 모델을 배열로 변환하는 리소스와 달리, 리소스 컬렉션은 모델 컬렉션 전체를 배열로 변환합니다. 하지만, 모든 모델마다 반드시 별도의 리소스 컬렉션 클래스를 만들 필요는 없습니다. 모든 리소스 클래스에 `collection` 메서드가 내장되어 있으므로, 즉석에서 "임시(ad-hoc)" 리소스 컬렉션을 쉽게 생성할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- However, if you need to customize the meta data returned with the collection, it is necessary to define your own resource collection: -->
하지만 컬렉션에 메타 데이터를 추가하거나 응답 구조를 커스터마이즈하고자 한다면, 반드시 직접 리소스 컬렉션 클래스를 정의해야 합니다.

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
단일 리소스와 마찬가지로, 리소스 컬렉션 역시 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

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
기본적으로, 최상위 리소스는 JSON으로 변환될 때 `data`라는 키로 감쌉니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다.

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

<!-- If you would like to use a custom key instead of `data`, you may define a `$wrap` attribute on the resource class: -->
만약 `data` 대신 커스텀 키를 사용하고 싶다면, 리소스 클래스에 `$wrap` 속성을 정의하면 됩니다.

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * The "data" wrapper that should be applied.
     *
     * @var string|null
     */
    public static $wrap = 'user';
}
```

<!-- If you would like to disable the wrapping of the outermost resource, you should invoke the `withoutWrapping` method on the base `Illuminate\Http\Resources\Json\JsonResource` class. Typically, you should call this method from your `AppServiceProvider` or another [service provider](/docs/9.x/providers) that is loaded on every request to your application: -->
최상위 리소스의 래핑을 아예 비활성화하고 싶다면 기본 리소스 클래스인 `Illuminate\Http\Resources\Json\JsonResource`에서 `withoutWrapping` 메서드를 호출해주면 됩니다. 일반적으로 이 메서드는 모든 요청에서 로드되는 `AppServiceProvider`나 [service provider](/docs/9.x/providers)에서 호출하는 것이 좋습니다.

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

> [!WARNING]
> `withoutWrapping` 메서드는 오직 최상위 응답에만 영향을 미치며, 직접 수동으로 추가한 컬렉션 내의 `data` 키에 대해서는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
<!-- #### Wrapping Nested Resources -->
#### Wrapping Nested Resources

<!-- You have total freedom to determine how your resource's relationships are wrapped. If you would like all resource collections to be wrapped in a `data` key, regardless of their nesting, you should define a resource collection class for each resource and return the collection within a `data` key. -->
리소스의 연관관계가 어떻게 래핑될지는 자유롭게 정할 수 있습니다. 모든 리소스 컬렉션이 중첩 여부와 상관 없이 무조건 `data` 키로 감싸지게 하려면, 각 리소스에 대해 리소스 컬렉션 클래스를 생성하고, 해당 컬렉션을 `data` 키 안에 반환하면 됩니다.

<!-- You may be wondering if this will cause your outermost resource to be wrapped in two `data` keys. Don't worry, Laravel will never let your resources be accidentally double-wrapped, so you don't have to be concerned about the nesting level of the resource collection you are transforming: -->
혹시 이렇게 하면 최상위 리소스가 `data` 키로 두 번 감싸질까봐 걱정이 될 수 있지만, Laravel은 중첩 수준과 상관 없이 리소스가 이중 래핑되는 일을 방지하므로 안심하고 사용할 수 있습니다.

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
리소스 응답에서 페이지네이션된 컬렉션을 반환할 때는, `withoutWrapping` 메서드를 호출하더라도 Laravel은 리소스 데이터를 반드시 `data` 키로 감쌉니다. 이는 페이지네이션 응답에 항상 `meta` 및 `links` 키(페이지네이터의 상태 정보를 담음)가 함께 포함되기 때문입니다.

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
Laravel 페이지네이터 인스턴스를 리소스의 `collection` 메서드 또는 커스텀 리소스 컬렉션에 바로 전달할 수 있습니다.

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

<!-- Paginated responses always contain `meta` and `links` keys with information about the paginator's state: -->
페이지네이션이 적용된 응답에는 항상 페이지네이터의 상태 정보를 담은 `meta`와 `links` 키가 포함됩니다.

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
특정 조건일 때만 리소스 응답에 속성을 포함시키고 싶은 경우가 종종 있습니다. 예를 들어 현재 사용자가 "관리자"일 때만 특정 값을 보내고 싶을 때 활용하면 됩니다. Laravel은 이런 상황에서 사용할 수 있는 다양한 헬퍼 메서드를 제공합니다. 가장 많이 사용하는 것은 `when` 메서드로, 조건이 참일 때만 속성을 리소스 응답에 추가할 수 있습니다.

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
        'secret' => $this->when($request->user()->isAdmin(), 'secret-value'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

<!-- In this example, the `secret` key will only be returned in the final resource response if the authenticated user's `isAdmin` method returns `true`. If the method returns `false`, the `secret` key will be removed from the resource response before it is sent to the client. The `when` method allows you to expressively define your resources without resorting to conditional statements when building the array. -->
위 예시에서, 로그인한 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 `secret` 키가 최종 리소스 응답에 포함됩니다. 만약 `false`를 반환하면, `secret` 키는 응답에서 제거됩니다. `when` 메서드를 활용하면, 배열 빌드 시 조건문 없이도 선언적으로 리소스를 구성할 수 있습니다.

<!-- The `when` method also accepts a closure as its second argument, allowing you to calculate the resulting value only if the given condition is `true`: -->
`when` 메서드의 두 번째 인자로 클로저도 전달할 수 있어서, 주어진 조건이 `true`일 때만 값을 계산하거나 반환할 수 있습니다.

```
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

<!-- The `whenHas` method may be used to include an attribute if it is actually present on the underlying model: -->
모델에 실제로 속성이 존재할 때만 응답에 포함하고 싶다면 `whenHas` 메서드를 사용할 수 있습니다.

```
'name' => $this->whenHas('name'),
```

<!-- Additionally, the `whenNotNull` method may be used to include an attribute in the resource response if the attribute is not null: -->
속성이 null이 아닐 때만 응답에 포함하고 싶다면 `whenNotNull` 메서드를 활용합니다.

```
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
<!-- #### Merging Conditional Attributes -->
#### Merging Conditional Attributes

<!-- Sometimes you may have several attributes that should only be included in the resource response based on the same condition. In this case, you may use the `mergeWhen` method to include the attributes in the response only when the given condition is `true`: -->
동일한 조건에 따라 여러 속성을 한 번에 응답에 포함해야 할 수도 있습니다. 이럴 때는 `mergeWhen` 메서드를 이용해, 지정한 조건이 `true`일 때만 여러 속성을 묶어 응답에 포함시킬 수 있습니다.

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
다시 말하지만, 주어진 조건이 `false`인 경우에는 해당 속성들이 클라이언트로 보내지기 전 리소스 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 혼합된 배열, 혹은 정렬이 순차적이지 않은 숫자 키 배열 내부에서는 사용하지 않는 것이 좋습니다.

<a name="conditional-relationships"></a>
<!-- ### Conditional Relationships -->
### Conditional Relationships

<!-- In addition to conditionally loading attributes, you may conditionally include relationships on your resource responses based on if the relationship has already been loaded on the model. This allows your controller to decide which relationships should be loaded on the model and your resource can easily include them only when they have actually been loaded. Ultimately, this makes it easier to avoid "N+1" query problems within your resources. -->
속성 외에도, 연관관계를 모델에 이미 로드했는지에 따라 선택적으로 리소스 응답에 포함할 수 있습니다. 이렇게 하면, 로드가 필요한 연관관계를 컨트롤러에서 직접 결정하고, 리소스에서는 실제로 로드된 경우에만 연관관계를 쉽게 응답에 포함할 수 있습니다. 궁극적으로, 리소스 사용 시 "N+1" 쿼리 문제를 예방하기 쉬워집니다.

<!-- The `whenLoaded` method may be used to conditionally load a relationship. In order to avoid unnecessarily loading relationships, this method accepts the name of the relationship instead of the relationship itself: -->
연관관계를 조건부로 포함하고 싶을 때는 `whenLoaded` 메서드를 사용할 수 있습니다. 이 메서드는 불필요한 쿼리 실행을 막기 위해, 연관관계 자체가 아니라 연관관계의 이름을 인자로 전달합니다.

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
이 예시에서 만약 해당 연관관계가 로드되어 있지 않다면, `posts` 키가 최종 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
<!-- #### Conditional Relationship Counts -->
#### Conditional Relationship Counts

<!-- In addition to conditionally including relationships, you may conditionally include relationship "counts" on your resource responses based on if the relationship's count has been loaded on the model: -->
연관관계 자체뿐만 아니라, 해당 연관관계의 "카운트" 정보도 로드 유무에 따라 조건적으로 응답에 포함시킬 수 있습니다.

```
new UserResource($user->loadCount('posts'));
```

<!-- The `whenCounted` method may be used to conditionally include a relationship's count in your resource response. This method avoids unnecessarily including the attribute if the relationships' count is not present: -->
`whenCounted` 메서드를 사용하면, 연관관계의 카운트가 모델에 로드되어 있을 때만 응답에 포함할 수 있습니다. 카운트가 없는 경우 해당 속성은 포함되지 않습니다.

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
        'posts_count' => $this->whenCounted('posts'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

<!-- In this example, if the `posts` relationship's count has not been loaded, the `posts_count` key will be removed from the resource response before it is sent to the client. -->
여기서도 `posts` 연관관계의 카운트가 로드되어 있지 않으면, `posts_count` 키는 응답에서 빠집니다.

<a name="conditional-pivot-information"></a>
<!-- #### Conditional Pivot Information -->
#### Conditional Pivot Information

<!-- In addition to conditionally including relationship information in your resource responses, you may conditionally include data from the intermediate tables of many-to-many relationships using the `whenPivotLoaded` method. The `whenPivotLoaded` method accepts the name of the pivot table as its first argument. The second argument should be a closure that returns the value to be returned if the pivot information is available on the model: -->
다대다(Many-to-Many) 관계의 중간 테이블에서 가져오는 데이터를 리소스 응답에 조건적으로 포함하고 싶을 때는 `whenPivotLoaded` 메서드를 사용할 수 있습니다. `whenPivotLoaded` 메서드는 첫 번째 인자로 피벗 테이블 이름을, 두 번째 인자로 클로저를 받아, 피벗 정보가 실제 모델에 존재할 때만 값을 반환합니다.

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

<!-- If your relationship is using a [custom intermediate table model](/docs/9.x/eloquent-relationships#defining-custom-intermediate-table-models), you may pass an instance of the intermediate table model as the first argument to the `whenPivotLoaded` method: -->
[custom intermediate table model](/docs/9.x/eloquent-relationships#defining-custom-intermediate-table-models)을 사용 중이라면, `whenPivotLoaded` 메서드의 첫 번째 인자로 중간 테이블 모델 인스턴스를 전달할 수 있습니다.

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

<!-- If your intermediate table is using an accessor other than `pivot`, you may use the `whenPivotLoadedAs` method: -->
중간 테이블에서 기본 accessor(`pivot`) 외의 명칭을 사용하는 경우에는 `whenPivotLoadedAs` 메서드를 쓸 수 있습니다.

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
일부 JSON API 표준에서는 리소스나 리소스 컬렉션 응답에 메타 데이터를 추가해야 할 수도 있습니다. 메타 데이터에는 해당 리소스 또는 관련 리소스에 대한 `links` 정보, 리소스 자체에 대한 정보 등이 포함될 수 있습니다. 리소스에 메타 데이터를 추가하려면, 단순히 `toArray` 메서드에서 배열에 함께 포함시키면 됩니다. 예를 들어, 리소스 컬렉션에 `link` 정보를 포함할 수 있습니다.

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
리소스에서 메타 데이터를 추가해 응답할 때, Laravel이 페이지네이션 응답에서 자동으로 추가하는 `links` 또는 `meta` 키와 충돌하는 것을 걱정할 필요는 없습니다. 직접 정의한 추가 `links`는 페이지네이터가 제공하는 링크와 병합되어 반환됩니다.

<a name="top-level-meta-data"></a>
<!-- #### Top Level Meta Data -->
#### Top Level Meta Data

<!-- Sometimes you may wish to only include certain meta data with a resource response if the resource is the outermost resource being returned. Typically, this includes meta information about the response as a whole. To define this meta data, add a `with` method to your resource class. This method should return an array of meta data to be included with the resource response only when the resource is the outermost resource being transformed: -->
경우에 따라, 특정 메타 데이터를 리소스 응답의 최상위(가장 바깥쪽)에서만 포함하고 싶은 상황이 생길 수 있습니다. 보통 이러한 메타 정보는 응답 전체에 대한 정보입니다. 이때는, 리소스 클래스에 `with` 메서드를 추가하여 최상위 리소스일 때만 함께 반환할 메타 데이터를 정의할 수 있습니다.

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
라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때, 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 리소스 응답에 함께 추가될 데이터를 배열로 인자로 받습니다.

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
지금까지 살펴본 것처럼, 리소스는 라우트와 컨트롤러에서 바로 반환할 수 있습니다.

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<!-- However, sometimes you may need to customize the outgoing HTTP response before it is sent to the client. There are two ways to accomplish this. First, you may chain the `response` method onto the resource. This method will return an `Illuminate\Http\JsonResponse` instance, giving you full control over the response's headers: -->
하지만, 경우에 따라 응답이 클라이언트에 전달되기 전에 HTTP 응답을 커스터마이즈해야 하는 상황도 있습니다. 이를 위해 두 가지 방법을 사용할 수 있습니다. 첫째, 리소스에 `response` 메서드를 체이닝하면 됩니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답 헤더를 자유롭게 제어할 수 있습니다.

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
또 다른 방법으로, 리소스 클래스 안에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 해당 리소스가 응답의 최상위로 반환될 때 호출됩니다.

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
