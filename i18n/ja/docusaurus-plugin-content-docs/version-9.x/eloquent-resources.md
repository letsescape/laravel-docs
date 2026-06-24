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
API を構築するときは、Eloquent モデルと実際にアプリケーションのユーザーに返される JSON 応答の間に位置する変換レイヤーが必要になる場合があります。たとえば、ユーザーのサブセットに対して特定の属性を表示し、その他の属性は表示しないようにしたい場合や、モデルの JSON 表現に特定の関係を常に含めたい場合があります。 Eloquent のリソース クラスを使用すると、モデルとモデル コレクションを表現力豊かかつ簡単に JSON に変換できます。

<!-- Of course, you may always convert Eloquent models or collections to JSON using their `toJson` methods; however, Eloquent resources provide more granular and robust control over the JSON serialization of your models and their relationships. -->
もちろん、`toJson` メソッドを使用して、いつでも Eloquent モデルまたはコレクションを JSON に変換できます。ただし、Eloquent リソースでは、モデルとその関係の JSON シリアル化をより詳細かつ堅牢に制御できます。

<a name="generating-resources"></a>
<!-- ## Generating Resources -->
## Generating Resources

<!-- To generate a resource class, you may use the `make:resource` Artisan command. By default, resources will be placed in the `app/Http/Resources` directory of your application. Resources extend the `Illuminate\Http\Resources\Json\JsonResource` class: -->
リソース クラスを生成するには、`make:resource` Artisan コマンドを使用できます。デフォルトでは、リソースはアプリケーションの `app/Http/Resources` ディレクトリに配置されます。リソースは `Illuminate\Http\Resources\Json\JsonResource` クラスを拡張します。

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- In addition to generating resources that transform individual models, you may generate resources that are responsible for transforming collections of models. This allows your JSON responses to include links and other meta information that is relevant to an entire collection of a given resource. -->
個々のモデルを変換するリソースを生成することに加えて、モデルのコレクションを変換するリソースを生成することもできます。これにより、JSON 応答に、特定のリソースのコレクション全体に関連するリンクやその他のメタ情報を含めることができます。

<!-- To create a resource collection, you should use the `--collection` flag when creating the resource. Or, including the word `Collection` in the resource name will indicate to Laravel that it should create a collection resource. Collection resources extend the `Illuminate\Http\Resources\Json\ResourceCollection` class: -->
リソース コレクションを作成するには、リソースの作成時に `--collection` フラグを使用する必要があります。または、リソース名に `Collection` という単語を含めると、コレクション リソースを作成する必要があることが Laravel に示されます。コレクション リソースは、`Illuminate\Http\Resources\Json\ResourceCollection` クラスを拡張します。

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

> [!NOTE]
> これは、リソースとリソース コレクションの概要です。リソースによって提供されるカスタマイズと機能をより深く理解するために、このドキュメントの他のセクションを読むことを強くお勧めします。

<!-- Before diving into all of the options available to you when writing resources, let's first take a high-level look at how resources are used within Laravel. A resource class represents a single model that needs to be transformed into a JSON structure. For example, here is a simple `UserResource` resource class: -->
リソースを作成するときに利用できるすべてのオプションを詳しく説明する前に、まず Laravel 内でリソースがどのように使用されるかを概要から見てみましょう。リソース クラスは、JSON 構造に変換する必要がある単一のモデルを表します。たとえば、単純な `UserResource` リソース クラスを次に示します。

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
すべてのリソース クラスは、リソースがルートまたはコントローラ メソッドからの応答として返されるときに JSON に変換する必要がある属性の配列を返す `toArray` メソッドを定義します。

<!-- Note that we can access model properties directly from the `$this` variable. This is because a resource class will automatically proxy property and method access down to the underlying model for convenient access. Once the resource is defined, it may be returned from a route or controller. The resource accepts the underlying model instance via its constructor: -->
`$this` 変数からモデル プロパティに直接アクセスできることに注意してください。これは、アクセスを容易にするために、リソース クラスがプロパティとメソッドへのアクセスを基になるモデルに自動的にプロキシするためです。リソースが定義されると、ルートまたはコントローラから返されることがあります。リソースは、コンストラクターを介して基礎となるモデル インスタンスを受け入れます。

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
リソースのコレクションまたはページ分割された応答を返す場合は、ルートまたはコントローラでリソース インスタンスを作成するときに、リソース クラスによって提供される `collection` メソッドを使用する必要があります。

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- Note that this does not allow any addition of custom meta data that may need to be returned with your collection. If you would like to customize the resource collection response, you may create a dedicated resource to represent the collection: -->
これにより、コレクションとともに返す必要があるカスタム メタ データを追加できないことに注意してください。リソース コレクションの応答をカスタマイズしたい場合は、コレクションを表す専用のリソースを作成できます。

```shell
php artisan make:resource UserCollection
```

<!-- Once the resource collection class has been generated, you may easily define any meta data that should be included with the response: -->
リソース コレクション クラスが生成されたら、応答に含めるメタデータを簡単に定義できます。

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
リソース コレクションを定義すると、ルートまたはコントローラから返される場合があります。

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
ルートからリソースコレクションを返すとき、Laravel はコレクションのキーを番号順になるようにリセットします。ただし、コレクションの元のキーを保持する必要があるかどうかを示す `preserveKeys` プロパティをリソース クラスに追加できます。

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
`preserveKeys` プロパティが `true` に設定されている場合、コレクションがルートまたはコントローラから返されるときにコレクション キーが保存されます。

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
通常、リソース コレクションの `$this->collection` プロパティには、コレクションの各項目をその単一のリソース クラスにマッピングした結果が自動的に設定されます。単数形のリソース クラスは、クラス名の末尾の `Collection` 部分を除いたコレクションのクラス名とみなされます。さらに、個人の好みに応じて、単数形リソース クラスの接尾辞として `Resource` を付けることも付けないこともできます。

<!-- For example, `UserCollection` will attempt to map the given user instances into the `UserResource` resource. To customize this behavior, you may override the `$collects` property of your resource collection: -->
たとえば、`UserCollection` は、指定されたユーザー インスタンスを `UserResource` リソースにマップしようとします。この動作をカスタマイズするには、リソース コレクションの `$collects` プロパティをオーバーライドします。

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
> まだ [concept overview](#concept-overview) を読んでいない場合は、このドキュメントに進む前に読むことを強くお勧めします。

<!-- In essence, resources are simple. They only need to transform a given model into an array. So, each resource contains a `toArray` method which translates your model's attributes into an API friendly array that can be returned from your application's routes or controllers: -->
本質的に、リソースはシンプルです。指定されたモデルを配列に変換するだけで済みます。したがって、各リソースには、モデルの属性をアプリケーションのルートまたはコントローラから返せる API フレンドリーな配列に変換する `toArray` メソッドが含まれています。

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
リソースが定義されると、ルートまたはコントローラから直接返されることがあります。

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
関連リソースを応答に含めたい場合は、リソースの `toArray` メソッドによって返される配列にそれらのリソースを追加できます。この例では、`PostResource` リソースの `collection` メソッドを使用して、ユーザーのブログ投稿をリソース応答に追加します。

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
> すでにロードされている場合にのみリレーションシップを含めたい場合は、[conditional relationships](#conditional-relationships) のドキュメントを確認してください。

<a name="writing-resource-collections"></a>
<!-- #### Resource Collections -->
#### Resource Collections

<!-- While resources transform a single model into an array, resource collections transform a collection of models into an array. However, it is not absolutely necessary to define a resource collection class for each one of your models since all resources provide a `collection` method to generate an "ad-hoc" resource collection on the fly: -->
リソースが単一のモデルを配列に変換するのに対し、リソース コレクションはモデルのコレクションを配列に変換します。ただし、すべてのリソースがオンザフライで「アドホック」リソース コレクションを生成する `collection` メソッドを提供しているため、モデルごとにリソース コレクション クラスを定義することが絶対に必要というわけではありません。

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

<!-- However, if you need to customize the meta data returned with the collection, it is necessary to define your own resource collection: -->
ただし、コレクションとともに返されるメタデータをカスタマイズする必要がある場合は、独自のリソース コレクションを定義する必要があります。

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
単一リソースと同様に、リソース コレクションはルートまたはコントローラから直接返される場合があります。

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
デフォルトでは、リソース応答が JSON に変換されるときに、最も外側のリソースは `data` キーでラップされます。たとえば、一般的なリソース収集の応答は次のようになります。

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
`data` の代わりにカスタム キーを使用したい場合は、リソース クラスに `$wrap` 属性を定義できます。

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
最も外側のリソースのラッピングを無効にしたい場合は、基本 `Illuminate\Http\Resources\Json\JsonResource` クラスで `withoutWrapping` メソッドを呼び出す必要があります。通常、このメソッドは、`AppServiceProvider` またはアプリケーションへのリクエストごとにロードされる別の [service provider](/docs/9.x/providers) から呼び出す必要があります。

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
> `withoutWrapping` メソッドは最も外側の応答にのみ影響し、独自のリソース コレクションに手動で追加した `data` キーは削除されません。

<a name="wrapping-nested-resources"></a>
<!-- #### Wrapping Nested Resources -->
#### Wrapping Nested Resources

<!-- You have total freedom to determine how your resource's relationships are wrapped. If you would like all resource collections to be wrapped in a `data` key, regardless of their nesting, you should define a resource collection class for each resource and return the collection within a `data` key. -->
リソースの関係をどのようにラップするかを完全に自由に決定できます。すべてのリソース コレクションを `data` キーでラップしたい場合は、ネストに関係なく、リソースごとにリソース コレクション クラスを定義し、コレクションを `data` キー内で返す必要があります。

<!-- You may be wondering if this will cause your outermost resource to be wrapped in two `data` keys. Don't worry, Laravel will never let your resources be accidentally double-wrapped, so you don't have to be concerned about the nesting level of the resource collection you are transforming: -->
これにより、最も外側のリソースが 2 つの `data` キーでラップされることになるのではないかと疑問に思われるかもしれません。心配しないでください。Laravel ではリソースが誤って二重ラップされることは決してないので、変換しているリソース コレクションのネスト レベルを気にする必要はありません。

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
リソース応答経由でページ分割されたコレクションを返すとき、Laravel は、`withoutWrapping` メソッドが呼び出されている場合でも、リソースデータを `data` キーでラップします。これは、ページ分割された応答には、ページネータの状態に関する情報を含む `meta` キーと `links` キーが常に含まれるためです。

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
Laravel ページネータ インスタンスをリソースの `collection` メソッドまたはカスタム リソース コレクションに渡すことができます。

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

<!-- Paginated responses always contain `meta` and `links` keys with information about the paginator's state: -->
ページ分割された応答には、ページネータの状態に関する情報を含む `meta` キーと `links` キーが常に含まれます。

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
場合によっては、特定の条件が満たされた場合にのみリソース応答に属性を含めたい場合があります。たとえば、現在のユーザーが「管理者」である場合にのみ値を含めることができます。 Laravel は、この状況を支援するさまざまなヘルパ メソッドを提供します。 `when` メソッドは、リソース応答に条件付きで属性を追加するために使用できます。

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
この例では、認証されたユーザーの `isAdmin` メソッドが `true` を返した場合にのみ、最終リソース応答で `secret` キーが返されます。メソッドが `false` を返した場合、リソース応答がクライアントに送信される前に、リソース応答から `secret` キーが削除されます。 `when` メソッドを使用すると、配列の構築時に条件ステートメントに頼ることなく、リソースを表現的に定義できます。

<!-- The `when` method also accepts a closure as its second argument, allowing you to calculate the resulting value only if the given condition is `true`: -->
`when` メソッドは 2 番目の引数としてクロージャーも受け入れ、指定された条件が `true` の場合にのみ結果の値を計算できます。

```
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

<!-- The `whenHas` method may be used to include an attribute if it is actually present on the underlying model: -->
属性が基になるモデルに実際に存在する場合、`whenHas` メソッドを使用して属性を含めることができます。

```
'name' => $this->whenHas('name'),
```

<!-- Additionally, the `whenNotNull` method may be used to include an attribute in the resource response if the attribute is not null: -->
さらに、属性が null でない場合は、`whenNotNull` メソッドを使用してリソース応答に属性を含めることができます。

```
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
<!-- #### Merging Conditional Attributes -->
#### Merging Conditional Attributes

<!-- Sometimes you may have several attributes that should only be included in the resource response based on the same condition. In this case, you may use the `mergeWhen` method to include the attributes in the response only when the given condition is `true`: -->
場合によっては、同じ条件に基づいてリソース応答にのみ含めるべき複数の属性がある場合があります。この場合、指定された条件が `true` の場合にのみ、`mergeWhen` メソッドを使用して属性を応答に含めることができます。

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
繰り返しますが、指定された条件が `false` の場合、これらの属性は、クライアントに送信される前にリソース応答から削除されます。

> [!WARNING]
> `mergeWhen` メソッドは、文字列キーと数値キーが混在する配列内では使用しないでください。さらに、連続して順序付けされていない数値キーを含む配列内で使用しないでください。

<a name="conditional-relationships"></a>
<!-- ### Conditional Relationships -->
### Conditional Relationships

<!-- In addition to conditionally loading attributes, you may conditionally include relationships on your resource responses based on if the relationship has already been loaded on the model. This allows your controller to decide which relationships should be loaded on the model and your resource can easily include them only when they have actually been loaded. Ultimately, this makes it easier to avoid "N+1" query problems within your resources. -->
条件付きで属性を読み込むだけでなく、関係がモデルに既に読み込まれているかどうかに基づいて、リソース応答に関係を条件付きで含めることができます。これにより、コントローラはどのリレーションシップをモデルにロードするかを決定できるようになり、実際にロードされた場合にのみリソースにリレーションシップを簡単に含めることができます。最終的に、これにより、リソース内での「N+1」クエリの問題を回避しやすくなります。

<!-- The `whenLoaded` method may be used to conditionally load a relationship. In order to avoid unnecessarily loading relationships, this method accepts the name of the relationship instead of the relationship itself: -->
`whenLoaded` メソッドを使用して、関係を条件付きでロードできます。不必要な関係の読み込みを避けるために、このメソッドは関係自体ではなく関係の名前を受け入れます。

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
この例では、関係がロードされていない場合、リソース応答がクライアントに送信される前に、リソース応答から `posts` キーが削除されます。

<a name="conditional-relationship-counts"></a>
<!-- #### Conditional Relationship Counts -->
#### Conditional Relationship Counts

<!-- In addition to conditionally including relationships, you may conditionally include relationship "counts" on your resource responses based on if the relationship's count has been loaded on the model: -->
関係を条件付きで含めるだけでなく、関係のカウントがモデルに読み込まれているかどうかに基づいて、リソース応答に関係の「カウント」を条件付きで含めることができます。

```
new UserResource($user->loadCount('posts'));
```

<!-- The `whenCounted` method may be used to conditionally include a relationship's count in your resource response. This method avoids unnecessarily including the attribute if the relationships' count is not present: -->
`whenCounted` メソッドを使用すると、リソース応答に関係のカウントを条件付きで含めることができます。このメソッドは、関係の数が存在しない場合に属性を不必要に含めることを回避します。

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
この例では、`posts` 関係のカウントがロードされていない場合、リソース応答がクライアントに送信される前に、`posts_count` キーがリソース応答から削除されます。

<a name="conditional-pivot-information"></a>
<!-- #### Conditional Pivot Information -->
#### Conditional Pivot Information

<!-- In addition to conditionally including relationship information in your resource responses, you may conditionally include data from the intermediate tables of many-to-many relationships using the `whenPivotLoaded` method. The `whenPivotLoaded` method accepts the name of the pivot table as its first argument. The second argument should be a closure that returns the value to be returned if the pivot information is available on the model: -->
リソース応答に関係情報を条件付きで含めるだけでなく、`whenPivotLoaded` メソッドを使用して多対多関係の中間テーブルからのデータを条件付きで含めることもできます。 `whenPivotLoaded` メソッドは、ピボット テーブルの名前を最初の引数として受け入れます。 2 番目の引数は、モデルでピボット情報が利用可能な場合に返される値を返すクロージャである必要があります。

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
リレーションシップで [custom intermediate table model](/docs/9.x/eloquent-relationships#defining-custom-intermediate-table-models) を使用している場合は、中間テーブル モデルのインスタンスを最初の引数として `whenPivotLoaded` メソッドに渡すことができます。

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

<!-- If your intermediate table is using an accessor other than `pivot`, you may use the `whenPivotLoadedAs` method: -->
中間テーブルが `pivot` 以外のaccessorを使用している場合は、`whenPivotLoadedAs` メソッドを使用できます。

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
一部の JSON API 標準では、リソースおよびリソース コレクションの応答にメタデータを追加する必要があります。これには、多くの場合、リソースまたは関連リソースに対する `links` のようなもの、またはリソース自体に関するメタデータが含まれます。リソースに関する追加のメタデータを返す必要がある場合は、それを `toArray` メソッドに含めます。たとえば、リソース コレクションを変換するときに、`link` 情報を含めることができます。

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
リソースから追​​加のメタデータを返す場合、ページ分割された応答を返すときに Laravel によって自動的に追加される `links` キーまたは `meta` キーを誤ってオーバーライドすることを心配する必要はありません。追加で定義した `links` は、ページネータによって提供されるリンクとマージされます。

<a name="top-level-meta-data"></a>
<!-- #### Top Level Meta Data -->
#### Top Level Meta Data

<!-- Sometimes you may wish to only include certain meta data with a resource response if the resource is the outermost resource being returned. Typically, this includes meta information about the response as a whole. To define this meta data, add a `with` method to your resource class. This method should return an array of meta data to be included with the resource response only when the resource is the outermost resource being transformed: -->
リソースが返される最も外側のリソースである場合、リソース応答に特定のメタデータのみを含めたい場合があります。通常、これには応答全体に関するメタ情報が含まれます。このメタデータを定義するには、リソース クラスに `with` メソッドを追加します。このメソッドは、リソースが変換される最も外側のリソースである場合にのみ、リソース応答に含まれるメタデータの配列を返す必要があります。

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
ルートまたはコントローラでリソース インスタンスを構築するときに、トップレベルのデータを追加することもできます。すべてのリソースで使用できる `additional` メソッドは、リソース応答に追加する必要があるデータの配列を受け入れます。

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
すでに読んだとおり、リソースはルートとコントローラから直接返される場合があります。

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<!-- However, sometimes you may need to customize the outgoing HTTP response before it is sent to the client. There are two ways to accomplish this. First, you may chain the `response` method onto the resource. This method will return an `Illuminate\Http\JsonResponse` instance, giving you full control over the response's headers: -->
ただし、送信 HTTP 応答をクライアントに送信する前にカスタマイズする必要がある場合があります。これを実現するには 2 つの方法があります。まず、`response` メソッドをリソースにチェーンします。このメソッドは `Illuminate\Http\JsonResponse` インスタンスを返し、応答のヘッダーを完全に制御できるようになります。

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
あるいは、リソース自体内で `withResponse` メソッドを定義することもできます。このメソッドは、リソースが応答の最も外側のリソースとして返されるときに呼び出されます。

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

