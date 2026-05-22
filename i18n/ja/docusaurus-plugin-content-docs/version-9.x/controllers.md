# コントローラ (Controllers)

- [Introduction](#introduction)
- [コントローラの作成](#writing-controllers)
    - [基本的なコントローラ](#basic-controllers)
    - [シングルアクションコントローラ](#single-action-controllers)
- [コントローラミドルウェア](#controller-middleware)
- [リソースコントローラ](#resource-controllers)
    - [部分的なリソースルート](#restful-partial-resource-routes)
    - [ネストされたリソース](#restful-nested-resources)
    - [リソースルートの命名](#restful-naming-resource-routes)
    - [リソースルートパラメータの命名](#restful-naming-resource-route-parameters)
    - [リソースルートのスコープ設定](#restful-scoping-resource-routes)
    - [リソース URI のローカライズ](#restful-localizing-resource-uris)
    - [リソースコントローラの補足](#restful-supplementing-resource-controllers)
    - [シングルトンリソースコントローラ](#singleton-resource-controllers)
- [依存関係の注入とコントローラ](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 導入 (Introduction)

すべてのリクエスト処理ロジックをルート ファイル内のクロージャとして定義する代わりに、「コントローラ」クラスを使用してこの動作を整理したい場合があります。コントローラは、関連するリクエスト処理ロジックを 1 つのクラスにグループ化できます。たとえば、`UserController` クラスは、ユーザーの表示、作成、更新、削除など、ユーザーに関連するすべての受信リクエストを処理する場合があります。デフォルトでは、コントローラは `app/Http/Controllers` ディレクトリに保存されます。

<a name="writing-controllers"></a>
## コントローラの作成 (Writing Controllers)

<a name="basic-controllers"></a>
### 基本的なコントローラ

基本的なコントローラの例を見てみましょう。コントローラは、Laravel に含まれる基本コントローラ クラス `App\Http\Controllers\Controller` を拡張していることに注意してください。

    <?php

    namespace App\Http\Controllers;
    
    use App\Models\User;

    class UserController extends Controller
    {
        /**
         * Show the profile for a given user.
         *
         * @param  int  $id
         * @return \Illuminate\View\View
         */
        public function show($id)
        {
            return view('user.profile', [
                'user' => User::findOrFail($id)
            ]);
        }
    }

次のように、このコントローラ メソッドへのルートを定義できます。

    use App\Http\Controllers\UserController;

    Route::get('/user/{id}', [UserController::class, 'show']);

受信リクエストが指定されたルート URI と一致すると、`App\Http\Controllers\UserController` クラスの `show` メソッドが呼び出され、ルート パラメーターがメソッドに渡されます。

> **注記**
> コントローラは基本クラスを拡張するために**必要ありません**。ただし、`middleware` メソッドや `authorize` メソッドなどの便利な機能にはアクセスできません。

<a name="single-action-controllers"></a>
### シングルアクションコントローラ

コントローラのアクションが特に複雑な場合は、コントローラ クラス全体をその 1 つのアクション専用にすると便利な場合があります。これを実現するには、コントローラ内で単一の `__invoke` メソッドを定義します。

    <?php

    namespace App\Http\Controllers;
    
    use App\Models\User;

    class ProvisionServer extends Controller
    {
        /**
         * Provision a new web server.
         *
         * @return \Illuminate\Http\Response
         */
        public function __invoke()
        {
            // ...
        }
    }

シングルアクションコントローラのルートを登録する場合、コントローラメソッドを指定する必要はありません。代わりに、単にコントローラの名前をルーターに渡すこともできます。

    use App\Http\Controllers\ProvisionServer;

    Route::post('/server', ProvisionServer::class);

`make:controller` Artisan コマンドの `--invokable` オプションを使用して、呼び出し可能なコントローラを生成できます。

```shell
php artisan make:controller ProvisionServer --invokable
```

> **注記**
> コントローラ スタブは、[スタブ発行](/docs/{{version}}/artisan#stub-customization) を使用してカスタマイズできます。

<a name="controller-middleware"></a>
## コントローラミドルウェア (Controller Middleware)

[Middleware](/docs/{{version}}/middleware) は、ルート ファイル内のコントローラのルートに割り当てることができます。

    Route::get('profile', [UserController::class, 'show'])->middleware('auth');

または、コントローラのコンストラクター内でミドルウェアを指定すると便利な場合があります。コントローラのコンストラクター内で `middleware` メソッドを使用すると、コントローラのアクションにミドルウェアを割り当てることができます。

    class UserController extends Controller
    {
        /**
         * Instantiate a new controller instance.
         *
         * @return void
         */
        public function __construct()
        {
            $this->middleware('auth');
            $this->middleware('log')->only('index');
            $this->middleware('subscribed')->except('store');
        }
    }

コントローラでは、クロージャーを使用してミドルウェアを登録することもできます。これにより、ミドルウェア クラス全体を定義せずに、単一のコントローラのインライン ミドルウェアを定義する便利な方法が提供されます。

    $this->middleware(function ($request, $next) {
        return $next($request);
    });

<a name="resource-controllers"></a>
## リソースコントローラ (Resource Controllers)

アプリケーション内の各 Eloquent モデルを「リソース」と考えると、アプリケーション内の各リソースに対して同じ一連のアクションを実行するのが一般的です。たとえば、アプリケーションに `Photo` モデルと `Movie` モデルが含まれていると想像してください。ユーザーはこれらのリソースを作成、読み取り、更新、または削除できる可能性があります。

この一般的なユースケースのため、Laravel リソースルーティングは、1 行のコードで典型的な作成、読み取り、更新、および削除 (「CRUD」) ルートをコントローラに割り当てます。まず、`make:controller` Artisan コマンドの `--resource` オプションを使用して、これらのアクションを処理するコントローラをすばやく作成できます。

```shell
php artisan make:controller PhotoController --resource
```

このコマンドは、`app/Http/Controllers/PhotoController.php` にコントローラを生成します。コントローラには、使用可能なリソース操作ごとにメソッドが含まれます。次に、コントローラを指すリソース ルートを登録できます。

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class);

この 1 つのルート宣言により、リソースに対するさまざまなアクションを処理するための複数のルートが作成されます。生成されたコントローラには、これらのアクションごとにスタブ化されたメソッドがすでに含まれています。 `route:list` Artisan コマンドを実行すると、アプリケーションのルートの概要をいつでも簡単に取得できることに注意してください。

配列を `resources` メソッドに渡すことで、多くのリソース コントローラを一度に登録することもできます。

    Route::resources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

<a name="actions-handled-by-resource-controller"></a>
#### リソースコントローラによって処理されるアクション

動詞      | URI                    | アクション       | 路線名
----------|------------------------|--------------|---------------------
得る       | `/photos`              | 索引        | 写真.インデックス
得る       | `/photos/create`       | 作成する       | 写真.作成
役職      | `/photos`              | 店        | 写真.ストア
得る       | `/photos/{photo}`      | 見せる         | 写真.ショー
得る       | `/photos/{photo}/edit` | 編集         | 写真.編集
パット/パッチ | `/photos/{photo}`      | アップデート       | 写真.更新
消去    | `/photos/{photo}`      | 破壊する      | 写真.破壊

<a name="customizing-missing-model-behavior"></a>
#### 欠落モデルの動作のカスタマイズ

通常、暗黙的にバインドされたリソース モデルが見つからない場合は、404 HTTP 応答が生成されます。ただし、リソース ルートを定義するときに `missing` メソッドを呼び出すことで、この動作をカスタマイズできます。 `missing` メソッドは、リソースのルートのいずれにも暗黙的にバインドされたモデルが見つからない場合に呼び出されるクロージャを受け入れます。

    use App\Http\Controllers\PhotoController;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Redirect;

    Route::resource('photos', PhotoController::class)
            ->missing(function (Request $request) {
                return Redirect::route('photos.index');
            });

<a name="soft-deleted-models"></a>
#### ソフト削除されたモデル

通常、暗黙的なモデル バインディングでは、[ソフト削除されました](/docs/{{version}}/eloquent#soft-deleting) になったモデルは取得されず、代わりに 404 HTTP 応答が返されます。ただし、リソース ルートを定義するときに `withTrashed` メソッドを呼び出すことで、論理的に削除されたモデルを許可するようにフレームワークに指示できます。

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->withTrashed();

引数なしで `withTrashed` を呼び出すと、`show`、`edit`、および `update` リソース ルートの論理的に削除されたモデルが許可されます。配列を `withTrashed` メソッドに渡すことで、これらのルートのサブセットを指定できます。

    Route::resource('photos', PhotoController::class)->withTrashed(['show']);

<a name="specifying-the-resource-model"></a>
#### リソースモデルの指定

[ルートモデルバインディング](/docs/{{version}}/routing#route-model-binding) を使用していて、リソース コントローラのメソッドでモデル インスタンスのタイプヒントを取得したい場合は、コントローラの生成時に `--model` オプションを使用できます。

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### フォームリクエストの生成

リソース コントローラを生成するときに `--requests` オプションを指定して、コントローラのストレージおよび更新メソッドに対して [フォームリクエストクラス](/docs/{{version}}/validation#form-request-validation) を生成するように Artisan に指示できます。

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 部分的なリソースルート

リソース ルートを宣言するとき、デフォルト アクションの完全なセットの代わりに、コントローラが処理する必要があるアクションのサブセットを指定できます。

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->only([
        'index', 'show'
    ]);

    Route::resource('photos', PhotoController::class)->except([
        'create', 'store', 'update', 'destroy'
    ]);

<a name="api-resource-routes"></a>
#### APIリソースルート

API によって使用されるリソース ルートを宣言する場合、一般的に、`create` や `edit` などの HTML テンプレートを提示するルートを除外する必要があります。便宜上、`apiResource` メソッドを使用して、これら 2 つのルートを自動的に除外できます。

    use App\Http\Controllers\PhotoController;

    Route::apiResource('photos', PhotoController::class);

配列を `apiResources` メソッドに渡すことで、多くの API リソース コントローラを一度に登録できます。

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\PostController;

    Route::apiResources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

`create` メソッドまたは `edit` メソッドを含まない API リソース コントローラを迅速に生成するには、`make:controller` コマンドの実行時に `--api` スイッチを使用します。

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### ネストされたリソース

場合によっては、ネストされたリソースへのルートを定義する必要があるかもしれません。たとえば、写真リソースには、写真に添付できる複数のコメントがある場合があります。リソース コントローラをネストするには、ルート宣言で「ドット」表記を使用できます。

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class);

このルートは、次のような URI でアクセスできるネストされたリソースを登録します。

    /photos/{photo}/comments/{comment}

<a name="scoping-nested-resources"></a>
#### ネストされたリソースのスコープ設定

Laravel の [暗黙的なモデルバインディング](/docs/{{version}}/routing#implicit-model-binding-scoping) 機能は、解決された子モデルが親モデルに属していることが確認されるように、ネストされたバインディングを自動的にスコープ設定できます。ネストされたリソースを定義するときに `scoped` メソッドを使用すると、自動スコープを有効にしたり、子リソースを取得するフィールドを Laravel に指示したりできます。これを実現する方法の詳細については、[リソースルートのスコープ設定](#restful-scoping-resource-routes) のドキュメントを参照してください。

<a name="shallow-nesting"></a>
#### 浅いネスティング

多くの場合、子 ID はすでに一意の識別子であるため、URI 内に親 ID と子 ID の両方を含める必要は必ずしもありません。自動インクリメント主キーなどの一意の識別子を使用して URI セグメント内のモデルを識別する場合、「浅いネスト」の使用を選択できます。

    use App\Http\Controllers\CommentController;

    Route::resource('photos.comments', CommentController::class)->shallow();

このルート定義では、次のルートが定義されます。

動詞      | URI                               | アクション       | 路線名
----------|-----------------------------------|--------------|---------------------
得る       | `/photos/{photo}/comments`        | 索引        | 写真.コメント.インデックス
得る       | `/photos/{photo}/comments/create` | 作成する       | 写真.コメント.作成
役職      | `/photos/{photo}/comments`        | 店        | 写真.コメント.ストア
得る       | `/comments/{comment}`             | 見せる         | コメント.ショー
得る       | `/comments/{comment}/edit`        | 編集         | コメント.編集
パット/パッチ | `/comments/{comment}`             | アップデート       | コメント.更新
消去    | `/comments/{comment}`             | 破壊する      | コメント.破壊

<a name="restful-naming-resource-routes"></a>
### リソースルートの命名

デフォルトでは、すべてのリソース コントローラ アクションにはルート名が付いています。ただし、希望のルート名を含む `names` 配列を渡すことで、これらの名前をオーバーライドできます。

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->names([
        'create' => 'photos.build'
    ]);

<a name="restful-naming-resource-route-parameters"></a>
### リソースルートパラメータの命名

デフォルトでは、`Route::resource` はリソース名の「単数化」バージョンに基づいてリソース ルートのルート パラメーターを作成します。これは、`parameters` メソッドを使用してリソースごとに簡単にオーバーライドできます。 `parameters` メソッドに渡される配列は、リソース名とパラメーター名の連想配列である必要があります。

    use App\Http\Controllers\AdminUserController;

    Route::resource('users', AdminUserController::class)->parameters([
        'users' => 'admin_user'
    ]);

上記の例では、リソースの `show` ルートに対して次の URI を生成します。

    /users/{admin_user}

<a name="restful-scoping-resource-routes"></a>
### リソースルートのスコープ設定

Laravel の [スコープ指定された暗黙的なモデル バインディング](/docs/{{version}}/routing#implicit-model-binding-scoping) 機能は、解決された子モデルが親モデルに属していることが確認されるように、ネストされたバインディングを自動的にスコープ設定できます。ネストされたリソースを定義するときに `scoped` メソッドを使用すると、自動スコープを有効にしたり、子リソースを取得するフィールドを Laravel に指示したりできます。

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class)->scoped([
        'comment' => 'slug',
    ]);

このルートは、次のような URI でアクセスできるスコープ付きのネストされたリソースを登録します。

    /photos/{photo}/comments/{comment:slug}

カスタムのキー付き暗黙的バインディングをネストされたルートパラメーターとして使用する場合、Laravel は、親の関係名を推測する規則を使用して、親によってネストされたモデルを取得するためにクエリのスコープを自動的に設定します。この場合、`Photo` モデルには、`Comment` モデルを取得するために使用できる `comments` (ルート パラメーター名の複数形) という名前のリレーションシップがあると想定されます。

<a name="restful-localizing-resource-uris"></a>
### リソース URI のローカライズ

デフォルトでは、`Route::resource` は英語の動詞と複数形ルールを使用してリソース URI を作成します。 `create` および `edit` アクション動詞をローカライズする必要がある場合は、`Route::resourceVerbs` メソッドを使用できます。これは、アプリケーションの `App\Providers\RouteServiceProvider` 内の `boot` メソッドの先頭で行うことができます。

    /**
     * Define your route model bindings, pattern filters, etc.
     *
     * @return void
     */
    public function boot()
    {
        Route::resourceVerbs([
            'create' => 'crear',
            'edit' => 'editar',
        ]);

        // ...
    }

Laravelのpluralizerは[ニーズに基づいて構成できるいくつかの異なる言語](/docs/{{version}}/localization#pluralization-language)をサポートしています。動詞と複数形言語をカスタマイズすると、`Route::resource('publicacion', PublicacionController::class)` などのリソース ルート登録によって次の URI が生成されます。

    /publicacion/crear

    /publicacion/{publicaciones}/editar

<a name="restful-supplementing-resource-controllers"></a>
### リソースコントローラの補足

リソース ルートのデフォルト セットを超えて追加のルートをリソース コントローラに追加する必要がある場合は、`Route::resource` メソッドを呼び出す前にそれらのルートを定義する必要があります。そうしないと、`resource` メソッドで定義されたルートが、補助ルートよりも意図せず優先される可能性があります。

    use App\Http\Controller\PhotoController;

    Route::get('/photos/popular', [PhotoController::class, 'popular']);
    Route::resource('photos', PhotoController::class);

> **注記**
> コントローラに集中することを忘れないでください。一般的なリソース アクションのセット以外のメソッドが日常的に必要な場合は、コントローラを 2 つの小さなコントローラに分割することを検討してください。

<a name="singleton-resource-controllers"></a>
### シングルトンリソースコントローラ

場合によっては、アプリケーションにインスタンスが 1 つしかないリソースが存在することがあります。たとえば、ユーザーの「プロフィール」は編集または更新できますが、ユーザーは複数の「プロフィール」を持つことはできません。同様に、画像には 1 つの「サムネイル」が含まれる場合があります。これらのリソースは「シングルトン リソース」と呼ばれます。これは、リソースのインスタンスが 1 つだけ存在できることを意味します。これらのシナリオでは、「シングルトン」リソース コントローラを登録できます。

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

上記のシングルトン リソース定義により、次のルートが登録されます。ご覧のとおり、「作成」ルートはシングルトン リソースには登録されておらず、リソースのインスタンスは 1 つしか存在しないため、登録されたルートは識別子を受け入れません。

動詞      | URI                               | アクション       | 路線名
----------|-----------------------------------|--------------|---------------------
得る       | `/profile`                        | 見せる         | プロフィール.ショー
得る       | `/profile/edit`                   | 編集         | プロフィール.編集
パット/パッチ | `/profile`                        | アップデート       | プロフィール.更新

シングルトン リソースは、標準リソース内にネストすることもできます。

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

この例では、`photos` リソースはすべての [標準リソースルート](#actions-handled-by-resource-controller) を受け取ります。ただし、`thumbnail` リソースは、次のルートを持つシングルトン リソースになります。

| 動詞      | URI                              | アクション  | 路線名               |
|-----------|----------------------------------|---------|--------------------------|
| 得る       | `/photos/{photo}/thumbnail`      | 見せる    | 写真.サムネイル.ショー    |
| 得る       | `/photos/{photo}/thumbnail/edit` | 編集    | 写真.サムネイル.編集    |
| パット/パッチ | `/photos/{photo}/thumbnail`      | アップデート  | 写真.サムネイル.更新  |

<a name="creatable-singleton-resources"></a>
#### 作成可能なシングルトン リソース

場合によっては、シングルトン リソースの作成ルートと保存ルートを定義することが必要になる場合があります。これを実現するには、シングルトン リソース ルートを登録するときに `creatable` メソッドを呼び出すことができます。

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

この例では、以下の経路が登録されます。ご覧のとおり、`DELETE` ルートも作成可能なシングルトン リソースに登録されます。

| 動詞      | URI                                | アクション  | 路線名               |
|-----------|------------------------------------|---------|--------------------------|
| 得る       | `/photos/{photo}/thumbnail/create` | 作成する  | 写真.サムネイル.作成  |
| 役職      | `/photos/{photo}/thumbnail`        | 店   | 写真.サムネイル.ストア   |
| 得る       | `/photos/{photo}/thumbnail`        | 見せる    | 写真.サムネイル.ショー    |
| 得る       | `/photos/{photo}/thumbnail/edit`   | 編集    | 写真.サムネイル.編集    |
| パット/パッチ | `/photos/{photo}/thumbnail`        | アップデート  | 写真.サムネイル.更新  |
| 消去    | `/photos/{photo}/thumbnail`        | 破壊する | 写真.サムネイル.破壊 |

Laravel にシングルトン リソースの `DELETE` ルートを登録させたいが、作成ルートやストレージ ルートは登録しない場合は、`destroyable` メソッドを利用できます。

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### APIシングルトンリソース

`apiSingleton` メソッドは、API 経由で操作されるシングルトン リソースを登録するために使用できます。これにより、`create` ルートと `edit` ルートが不要になります。

```php
Route::apiSingleton('profile', ProfileController::class);
```

もちろん、API シングルトン リソースは `creatable` である場合もあります。これにより、リソースの `store` ルートと `destroy` ルートが登録されます。

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 依存関係の注入とコントローラ (Dependency Injection & Controllers)

<a name="constructor-injection"></a>
#### コンストラクターのインジェクション

Laravel [サービスコンテナ](/docs/{{version}}/container) は、すべての Laravel コントローラを解決するために使用されます。その結果、コントローラがコンストラクターで必要とする依存関係をタイプヒントで指定できるようになります。宣言された依存関係は自動的に解決され、コントローラ インスタンスに挿入されます。

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * The user repository instance.
         */
        protected $users;

        /**
         * Create a new controller instance.
         *
         * @param  \App\Repositories\UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }
    }

<a name="method-injection"></a>
#### メソッドインジェクション

コンストラクターのインジェクションに加えて、コントローラのメソッドに対するタイプヒントの依存関係を指定することもできます。メソッド インジェクションの一般的な使用例は、コントローラ メソッドに `Illuminate\Http\Request` インスタンスを挿入することです。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * Store a new user.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function store(Request $request)
        {
            $name = $request->name;

            //
        }
    }

コントローラ メソッドがルート パラメーターからの入力も期待している場合は、他の依存関係の後にルート引数をリストします。たとえば、ルートが次のように定義されているとします。

    use App\Http\Controllers\UserController;

    Route::put('/user/{id}', [UserController::class, 'update']);

次のようにコントローラ メソッドを定義することで、`Illuminate\Http\Request` をタイプヒントし、`id` パラメーターにアクセスすることができます。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * Update the given user.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  string  $id
         * @return \Illuminate\Http\Response
         */
        public function update(Request $request, $id)
        {
            //
        }
    }

