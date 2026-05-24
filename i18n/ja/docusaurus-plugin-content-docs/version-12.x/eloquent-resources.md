# Eloquent: API リソース (Eloquent: API Resources)

- [Introduction](#introduction)
- [リソースの生成](#generating-resources)
- [コンセプトの概要](#concept-overview)
    - [リソースコレクション](#resource-collections)
- [執筆リソース](#writing-resources)
    - [データラッピング](#data-wrapping)
    - [Pagination](#pagination)
    - [条件付き属性](#conditional-attributes)
    - [条件付き関係](#conditional-relationships)
    - [メタデータの追加](#adding-meta-data)
- [リソースの応答](#resource-responses)

<a name="introduction"></a>
## 導入 (Introduction)

API を構築するときは、Eloquent モデルと実際にアプリケーションのユーザーに返される JSON 応答の間に位置する変換レイヤーが必要になる場合があります。たとえば、ユーザーのサブセットに対して特定の属性を表示し、その他の属性は表示しないようにしたい場合や、モデルの JSON 表現に特定の関係を常に含めたい場合があります。 Eloquent のリソース クラスを使用すると、モデルとモデル コレクションを表現力豊かかつ簡単に JSON に変換できます。

もちろん、`toJson` メソッドを使用して、いつでも Eloquent モデルまたはコレクションを JSON に変換できます。ただし、Eloquent リソースでは、モデルとその関係の JSON シリアル化をより詳細かつ堅牢に制御できます。

<a name="generating-resources"></a>
## リソースの生成 (Generating Resources)

リソース クラスを生成するには、`make:resource` Artisan コマンドを使用できます。デフォルトでは、リソースはアプリケーションの `app/Http/Resources` ディレクトリに配置されます。リソースは `Illuminate\Http\Resources\Json\JsonResource` クラスを拡張します。

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### リソースコレクション

個々のモデルを変換するリソースを生成することに加えて、モデルのコレクションを変換するリソースを生成することもできます。これにより、JSON 応答に、特定のリソースのコレクション全体に関連するリンクやその他のメタ情報を含めることができます。

リソース コレクションを作成するには、リソースの作成時に `--collection` フラグを使用する必要があります。または、リソース名に `Collection` という単語を含めると、コレクション リソースを作成する必要があることが Laravel に示されます。コレクション リソースは、`Illuminate\Http\Resources\Json\ResourceCollection` クラスを拡張します。

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## コンセプトの概要 (Concept Overview)

> [!NOTE]
> これは、リソースとリソース コレクションの概要です。リソースによって提供されるカスタマイズと機能をより深く理解するために、このドキュメントの他のセクションを読むことを強くお勧めします。

リソースを作成するときに利用できるすべてのオプションを詳しく説明する前に、まず Laravel 内でリソースがどのように使用されるかを概要から見てみましょう。リソース クラスは、JSON 構造に変換する必要がある単一のモデルを表します。たとえば、単純な `UserResource` リソース クラスを次に示します。

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

すべてのリソース クラスは、リソースがルートまたはコントローラ メソッドからの応答として返されるときに JSON に変換する必要がある属性の配列を返す `toArray` メソッドを定義します。

`$this` 変数からモデル プロパティに直接アクセスできることに注意してください。これは、アクセスを容易にするために、リソース クラスがプロパティとメソッドへのアクセスを基になるモデルに自動的にプロキシするためです。リソースが定義されると、ルートまたはコントローラから返されることがあります。リソースは、コンストラクターを介して基礎となるモデル インスタンスを受け入れます。

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

便宜上、モデルの `toResource` メソッドを使用することもできます。このメソッドは、フレームワーク規則を使用して、モデルの基礎となるリソースを自動的に検出します。

```php
return User::findOrFail($id)->toResource();
```

`toResource` メソッドを呼び出すと、Laravel は、モデルの名前空間に最も近い `Http\Resources` 名前空間内で、モデルの名前と一致し、オプションで `Resource` のサフィックスが付けられたリソースを見つけようとします。

リソース クラスがこの命名規則に従っていない場合、または別の名前空間に配置されている場合は、`UseResource` 属性を使用してモデルのデフォルトのリソースを指定できます。

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

あるいは、リソース クラスを `toResource` メソッドに渡して指定することもできます。

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
### リソースコレクション

リソースのコレクションまたはページ分割された応答を返す場合は、ルートまたはコントローラでリソース インスタンスを作成するときに、リソース クラスによって提供される `collection` メソッドを使用する必要があります。

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

または、便宜上、Eloquent コレクションの `toResourceCollection` メソッドを使用することもできます。このメソッドは、フレームワーク規則を使用して、モデルの基礎となるリソース コレクションを自動的に検出します。

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` メソッドを呼び出すと、Laravel は、モデルの名前空間に最も近い `Http\Resources` 名前空間内で、モデルの名前に一致し、接尾辞が `Collection` であるリソース コレクションを見つけようとします。

リソース コレクション クラスがこの命名規則に従っていない場合、または別の名前空間に配置されている場合は、`UseResourceCollection` 属性を使用してモデルのデフォルトのリソース コレクションを指定できます。

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

あるいは、リソース コレクション クラスを `toResourceCollection` メソッドに渡して指定することもできます。

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
#### カスタムリソースコレクション

デフォルトでは、リソース コレクションでは、コレクションとともに返す必要があるカスタム メタ データを追加することはできません。リソース コレクションの応答をカスタマイズしたい場合は、コレクションを表す専用のリソースを作成できます。

```shell
php artisan make:resource UserCollection
```

リソース コレクション クラスが生成されたら、応答に含めるメタデータを簡単に定義できます。

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

リソース コレクションを定義すると、ルートまたはコントローラから返される場合があります。

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

または、便宜上、Eloquent コレクションの `toResourceCollection` メソッドを使用することもできます。このメソッドは、フレームワーク規則を使用して、モデルの基礎となるリソース コレクションを自動的に検出します。

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` メソッドを呼び出すと、Laravel は、モデルの名前空間に最も近い `Http\Resources` 名前空間内で、モデルの名前に一致し、接尾辞が `Collection` であるリソース コレクションを見つけようとします。

<a name="preserving-collection-keys"></a>
#### コレクションキーの保存

ルートからリソースコレクションを返すとき、Laravel はコレクションのキーを番号順になるようにリセットします。ただし、コレクションの元のキーを保持する必要があるかどうかを示す `preserveKeys` プロパティをリソース クラスに追加できます。

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

`preserveKeys` プロパティが `true` に設定されている場合、コレクションがルートまたはコントローラから返されるときにコレクション キーが保存されます。

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 基礎となるリソースクラスのカスタマイズ

通常、リソース コレクションの `$this->collection` プロパティには、コレクションの各項目をその単一のリソース クラスにマッピングした結果が自動的に設定されます。単数形のリソース クラスは、クラス名の末尾の `Collection` 部分を除いたコレクションのクラス名とみなされます。さらに、個人の好みに応じて、単数形リソース クラスの接尾辞として `Resource` を付けることも付けないこともできます。

たとえば、`UserCollection` は、指定されたユーザー インスタンスを `UserResource` リソースにマップしようとします。この動作をカスタマイズするには、リソース コレクションの `$collects` プロパティをオーバーライドします。

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
## 執筆リソース (Writing Resources)

> [!NOTE]
> まだ [コンセプトの概要](#concept-overview) を読んでいない場合は、このドキュメントに進む前に読むことを強くお勧めします。

リソースは、指定されたモデルを配列に変換するだけで済みます。したがって、各リソースには、モデルの属性をアプリケーションのルートまたはコントローラから返せる API フレンドリーな配列に変換する `toArray` メソッドが含まれています。

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

リソースが定義されると、ルートまたはコントローラから直接返されることがあります。

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 人間関係

関連リソースを応答に含めたい場合は、リソースの `toArray` メソッドによって返される配列にそれらのリソースを追加できます。この例では、`PostResource` リソースの `collection` メソッドを使用して、ユーザーのブログ投稿をリソース応答に追加します。

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
> すでにロードされている場合にのみリレーションシップを含めたい場合は、[条件付き関係](#conditional-relationships) のドキュメントを確認してください。

<a name="writing-resource-collections"></a>
#### リソースコレクション

リソースが単一のモデルを配列に変換するのに対し、リソース コレクションはモデルのコレクションを配列に変換します。ただし、すべての Eloquent モデル コレクションは、オンザフライで「アドホック」リソース コレクションを生成する `toResourceCollection` メソッドを提供しているため、モデルごとにリソース コレクション クラスを定義することが絶対に必要というわけではありません。

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

ただし、コレクションとともに返されるメタデータをカスタマイズする必要がある場合は、独自のリソース コレクションを定義する必要があります。

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

単一リソースと同様に、リソース コレクションはルートまたはコントローラから直接返される場合があります。

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

または、便宜上、Eloquent コレクションの `toResourceCollection` メソッドを使用することもできます。このメソッドは、フレームワーク規則を使用して、モデルの基礎となるリソース コレクションを自動的に検出します。

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` メソッドを呼び出すと、Laravel は、モデルの名前空間に最も近い `Http\Resources` 名前空間内で、モデルの名前に一致し、接尾辞が `Collection` であるリソース コレクションを見つけようとします。

<a name="data-wrapping"></a>
### データラッピング

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

最も外側のリソースのラッピングを無効にしたい場合は、基本 `Illuminate\Http\Resources\Json\JsonResource` クラスで `withoutWrapping` メソッドを呼び出す必要があります。通常、このメソッドは、`AppServiceProvider` またはアプリケーションへのリクエストごとにロードされる別の [サービスプロバイダ](/docs/{{version}}/providers) から呼び出す必要があります。

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
> `withoutWrapping` メソッドは最も外側の応答にのみ影響し、独自のリソース コレクションに手動で追加した `data` キーは削除されません。

<a name="wrapping-nested-resources"></a>
#### ネストされたリソースのラッピング

リソースの関係をどのようにラップするかを完全に自由に決定できます。すべてのリソース コレクションを `data` キーでラップしたい場合は、ネストに関係なく、リソースごとにリソース コレクション クラスを定義し、コレクションを `data` キー内で返す必要があります。

これにより、最も外側のリソースが 2 つの `data` キーでラップされることになるのではないかと疑問に思われるかもしれません。心配しないでください。Laravel ではリソースが誤って二重ラップされることは決してないので、変換しているリソース コレクションのネスト レベルを気にする必要はありません。

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
#### データのラッピングとページネーション

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
### ページネーション

Laravel ページネータ インスタンスをリソースの `collection` メソッドまたはカスタム リソース コレクションに渡すことができます。

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

または、便宜上、ページネーションの `toResourceCollection` メソッドを使用することもできます。このメソッドは、フレームワーク規則を使用して、ページ分割されたモデルの基になるリソース コレクションを自動的に検出します。

```php
return User::paginate()->toResourceCollection();
```

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
#### ページネーション情報のカスタマイズ

ページネーション応答の `links` キーまたは `meta` キーに含まれる情報をカスタマイズしたい場合は、リソース上で `paginationInformation` メソッドを定義できます。このメソッドは、`$paginated` データと、`links` キーと `meta` キーを含む配列である `$default` 情報の配列を受け取ります。

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
### 条件付き属性

場合によっては、特定の条件が満たされた場合にのみリソース応答に属性を含めたい場合があります。たとえば、現在のユーザーが「管理者」である場合にのみ値を含めることができます。 Laravel は、この状況を支援するさまざまなヘルパ メソッドを提供します。 `when` メソッドは、リソース応答に条件付きで属性を追加するために使用できます。

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

この例では、認証されたユーザーの `isAdmin` メソッドが `true` を返した場合にのみ、最終リソース応答で `secret` キーが返されます。メソッドが `false` を返した場合、リソース応答がクライアントに送信される前に、リソース応答から `secret` キーが削除されます。 `when` メソッドを使用すると、配列の構築時に条件ステートメントに頼ることなく、リソースを表現的に定義できます。

`when` メソッドは 2 番目の引数としてクロージャーも受け入れ、指定された条件が `true` の場合にのみ結果の値を計算できます。

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

属性が基になるモデルに実際に存在する場合、`whenHas` メソッドを使用して属性を含めることができます。

```php
'name' => $this->whenHas('name'),
```

さらに、属性が null でない場合は、`whenNotNull` メソッドを使用してリソース応答に属性を含めることができます。

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 条件付き属性の結合

場合によっては、同じ条件に基づいてリソース応答にのみ含めるべき複数の属性がある場合があります。この場合、指定された条件が `true` の場合にのみ、`mergeWhen` メソッドを使用して属性を応答に含めることができます。

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

繰り返しますが、指定された条件が `false` の場合、これらの属性は、クライアントに送信される前にリソース応答から削除されます。

> [!WARNING]
> `mergeWhen` メソッドは、文字列キーと数値キーが混在する配列内では使用しないでください。さらに、連続して順序付けされていない数値キーを含む配列内で使用しないでください。

<a name="conditional-relationships"></a>
### 条件付き関係

条件付きで属性を読み込むだけでなく、関係がモデルに既に読み込まれているかどうかに基づいて、リソース応答に関係を条件付きで含めることができます。これにより、コントローラはどのリレーションシップをモデルにロードするかを決定できるようになり、実際にロードされた場合にのみリソースにリレーションシップを簡単に含めることができます。最終的に、これにより、リソース内での「N+1」クエリの問題を回避しやすくなります。

`whenLoaded` メソッドを使用して、関係を条件付きでロードできます。不必要な関係の読み込みを避けるために、このメソッドは関係自体ではなく関係の名前を受け入れます。

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

この例では、関係がロードされていない場合、リソース応答がクライアントに送信される前に、リソース応答から `posts` キーが削除されます。

<a name="conditional-relationship-counts"></a>
#### 条件付き関係の数

関係を条件付きで含めるだけでなく、関係のカウントがモデルに読み込まれているかどうかに基づいて、リソース応答に関係の「カウント」を条件付きで含めることができます。

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` メソッドを使用すると、リソース応答に関係のカウントを条件付きで含めることができます。このメソッドは、関係の数が存在しない場合に属性を不必要に含めることを回避します。

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

この例では、`posts` 関係のカウントがロードされていない場合、リソース応答がクライアントに送信される前に、`posts_count` キーがリソース応答から削除されます。

`avg`、`sum`、`min`、`max` などの他のタイプの集計も、`whenAggregated` メソッドを使用して条件付きでロードできます。

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 条件付きピボット情報

リソース応答に関係情報を条件付きで含めるだけでなく、`whenPivotLoaded` メソッドを使用して多対多関係の中間テーブルからのデータを条件付きで含めることもできます。 `whenPivotLoaded` メソッドは、ピボット テーブルの名前を最初の引数として受け入れます。 2 番目の引数は、モデルでピボット情報が利用可能な場合に返される値を返すクロージャである必要があります。

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

リレーションシップで [カスタム中間テーブルモデル](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models) を使用している場合は、中間テーブル モデルのインスタンスを最初の引数として `whenPivotLoaded` メソッドに渡すことができます。

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

中間テーブルが `pivot` 以外のアクセサーを使用している場合は、`whenPivotLoadedAs` メソッドを使用できます。

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
### メタデータの追加

一部の JSON API 標準では、リソースおよびリソース コレクションの応答にメタデータを追加する必要があります。これには、多くの場合、リソースまたは関連リソースに対する `links` のようなもの、またはリソース自体に関するメタデータが含まれます。リソースに関する追加のメタデータを返す必要がある場合は、それを `toArray` メソッドに含めます。たとえば、リソース コレクションを変換するときに、`links` 情報を含めることができます。

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

リソースから追​​加のメタデータを返す場合、ページ分割された応答を返すときに Laravel によって自動的に追加される `links` キーまたは `meta` キーを誤ってオーバーライドすることを心配する必要はありません。追加で定義した `links` は、ページネータによって提供されるリンクとマージされます。

<a name="top-level-meta-data"></a>
#### トップレベルのメタデータ

リソースが返される最も外側のリソースである場合、リソース応答に特定のメタデータのみを含めたい場合があります。通常、これには応答全体に関するメタ情報が含まれます。このメタデータを定義するには、リソース クラスに `with` メソッドを追加します。このメソッドは、リソースが変換される最も外側のリソースである場合にのみ、リソース応答に含まれるメタデータの配列を返す必要があります。

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
#### リソース構築時のメタデータの追加

ルートまたはコントローラでリソース インスタンスを構築するときに、トップレベルのデータを追加することもできます。すべてのリソースで使用できる `additional` メソッドは、リソース応答に追加する必要があるデータの配列を受け入れます。

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
## リソースの応答 (Resource Responses)

すでに読んだとおり、リソースはルートとコントローラから直接返される場合があります。

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

ただし、送信 HTTP 応答をクライアントに送信する前にカスタマイズする必要がある場合があります。これを実現するには 2 つの方法があります。まず、`response` メソッドをリソースにチェーンします。このメソッドは `Illuminate\Http\JsonResponse` インスタンスを返し、応答のヘッダーを完全に制御できるようになります。

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

あるいは、リソース自体内で `withResponse` メソッドを定義することもできます。このメソッドは、リソースが応答の最も外側のリソースとして返されるときに呼び出されます。

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

