# アップグレードガイド (Upgrade Guide)

- [7.x から 8.0 へのアップグレード](#upgrade-8.0)

<a name="high-impact-changes"></a>
## 大きな影響を与える変更 (High Impact Changes)

<div class="content-list" markdown="1">

- [モデルファクトリー](#model-factories)
- [キュー `retryAfter` メソッド](#queue-retry-after-method)
- [キュー `timeoutAt` プロパティ](#queue-timeout-at-property)
- [キュー `allOnQueue` および `allOnConnection`](#queue-allOnQueue-allOnConnection)
- [ページネーションのデフォルト](#pagination-defaults)
- [シーダーおよびファクトリーの名前空間](#seeder-factory-namespaces)

</div>

<a name="medium-impact-changes"></a>
## 中程度の影響のある変更 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [PHP 7.3.0が必要](#php-7.3.0-required)
- [失敗したジョブテーブルのバッチサポート](#failed-jobs-table-batch-support)
- [メンテナンスモードのアップデート](#maintenance-mode-updates)
- [`php artisan down --message` オプション](#artisan-down-message)
- [`assertExactJson` メソッド](#assert-exact-json-method)

</div>

<a name="upgrade-8.0"></a>
## 7.x から 8.0 へのアップグレード (Upgrading To 8.0 From 7.x)

<a name="estimated-upgrade-time-15-minutes"></a>
#### アップグレードの推定時間: 15 分

> {note} 私たちは、考えられるすべての重大な変更を文書化するよう努めています。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。

<a name="php-7.3.0-required"></a>
### PHP 7.3.0が必要

**影響の可能性: 中**

新しい PHP の最小バージョンは 7.3.0 になりました。

<a name="updating-dependencies"></a>
### 依存関係の更新

`composer.json` ファイル内の次の依存関係を更新します。

<div class="content-list" markdown="1">

- `guzzlehttp/guzzle` ～ `^7.0.1`
- `facade/ignition` ～ `^2.3.6`
- `laravel/framework` ～ `^8.0`
- `laravel/ui` ～ `^3.0`
- `nunomaduro/collision` ～ `^5.0`
- `phpunit/phpunit` ～ `^9.0`

</div>

次のファーストパーティ パッケージには、Laravel 8 をサポートするための新しいメジャー リリースがあります。該当する場合は、アップグレードする前に、それぞれの個別のアップグレード ガイドを読む必要があります。

<div class="content-list" markdown="1">

- [ホライゾン v5.0](https://github.com/laravel/horizon/blob/master/UPGRADE.md)
- [Passport v10.0](https://github.com/laravel/passport/blob/master/UPGRADE.md)
- [Socialite v5.0](https://github.com/laravel/socialite/blob/master/UPGRADE.md)
- [Telescope v4.0](https://github.com/laravel/telescope/blob/master/UPGRADE.md)

</div>

さらに、Laravel インストーラーは、`composer create-project` と Laravel Jetstream をサポートするように更新されました。 4.0 より古いインストーラーは、2020 年 10 月以降機能しなくなります。できるだけ早くグローバル インストーラーを `^4.0` にアップグレードする必要があります。

最後に、アプリケーションで使用される他のサードパーティパッケージを調べて、Laravel 8 をサポートする適切なバージョンを使用していることを確認します。

<a name="collections"></a>
### コレクション

<a name="the-isset-method"></a>
#### `isset` メソッド

**影響の可能性: 低い**

一般的な PHP の動作と一致させるために、`Illuminate\Support\Collection` の `offsetExists` メソッドは、`array_key_exists` の代わりに `isset` を使用するように更新されました。これにより、`null` の値を持つコレクション項目を処理するときの動作が変わる可能性があります。

    $collection = collect([null]);

    // Laravel 7.x - true
    isset($collection[0]);

    // Laravel 8.x - false
    isset($collection[0]);

<a name="database"></a>
### データベース

<a name="seeder-factory-namespaces"></a>
#### シーダーおよびファクトリーの名前空間

**影響の可能性: 高**

シーダーとファクトリーには名前空間が設定されるようになりました。これらの変更に対応するには、`Database\Seeders` 名前空間をシーダー クラスに追加します。さらに、以前の `database/seeds` ディレクトリの名前を `database/seeders` に変更する必要があります。

    <?php

    namespace Database\Seeders;

    use App\Models\User;
    use Illuminate\Database\Seeder;

    class DatabaseSeeder extends Seeder
    {
        /**
         * Seed the application's database.
         *
         * @return void
         */
        public function run()
        {
            ...
        }
    }

`laravel/legacy-factories` パッケージの使用を選択した場合、ファクトリ クラスを変更する必要はありません。ただし、ファクトリーをアップグレードする場合は、それらのクラスに `Database\Factories` 名前空間を追加する必要があります。

次に、`composer.json` ファイルで、`autoload` セクションから `classmap` ブロックを削除し、新しい名前空間クラスのディレクトリ マッピングを追加します。

    "autoload": {
        "psr-4": {
            "App\\": "app/",
            "Database\\Factories\\": "database/factories/",
            "Database\\Seeders\\": "database/seeders/"
        }
    },

<a name="eloquent"></a>
### Eloquent

<a name="model-factories"></a>
#### モデルファクトリー

**影響の可能性: 高**

Laravel の [モデル工場](/docs/{{version}}/database-testing#defining-model-factories) 機能はクラスをサポートするために完全に書き直されており、Laravel 7.x スタイルのファクトリーとは互換性がありません。ただし、アップグレードプロセスを容易にするために、Laravel 8.x で既存のファクトリーを引き続き使用できるように、新しい `laravel/legacy-factories` パッケージが作成されました。このパッケージは Composer 経由でインストールできます。

    composer require laravel/legacy-factories

<a name="the-castable-interface"></a>
#### `Castable` インターフェイス

**影響の可能性: 低い**

`Castable` インターフェイスの `castUsing` メソッドが、引数の配列を受け入れるように更新されました。このインターフェースを実装している場合は、それに応じて実装を更新する必要があります。

    public static function castUsing(array $arguments);

<a name="increment-decrement-events"></a>
#### インクリメント/デクリメントイベント

**影響の可能性: 低い**

Eloquent モデル インスタンスで `increment` メソッドまたは `decrement` メソッドを実行するときに、適切な「更新」および「保存」関連のモデル イベントが送出されるようになりました。

<a name="events"></a>
### イベント

<a name="the-event-service-provider-class"></a>
#### `EventServiceProvider` クラス

**影響の可能性: 低い**

`App\Providers\EventServiceProvider` クラスに `register` 関数が含まれている場合は、このメソッドの先頭で `parent::register` を必ず呼び出す必要があります。そうしないと、アプリケーションのイベントは登録されません。

<a name="the-dispatcher-contract"></a>
#### `Dispatcher` 契約

**影響の可能性: 低い**

`Illuminate\Contracts\Events\Dispatcher` コントラクトの `listen` メソッドが更新され、`$listener` プロパティがオプションになりました。この変更は、リフレクションによる処理されたイベント タイプの自動検出をサポートするために行われました。このインターフェースを手動で実装している場合は、それに応じて実装を更新する必要があります。

    public function listen($events, $listener = null);

<a name="framework"></a>
### フレームワーク

<a name="maintenance-mode-updates"></a>
#### メンテナンスモードのアップデート

**影響の可能性: オプション**

Laravel の [メンテナンスモード](/docs/{{version}}/configuration#maintenance-mode) 機能は、Laravel 8.x で改善されました。メンテナンス モード テンプレートの事前レンダリングがサポートされるようになり、メンテナンス モード中にエンド ユーザーがエラーに遭遇する可能性がなくなりました。ただし、これをサポートするには、`public/index.php` ファイルに次の行を追加する必要があります。これらの行は、既存の `LARAVEL_START` 定数定義の直下に配置する必要があります。

    define('LARAVEL_START', microtime(true));

    if (file_exists($maintenance = __DIR__.'/../storage/framework/maintenance.php')) {
        require $maintenance;
    }

<a name="artisan-down-message"></a>
#### `php artisan down --message` オプション

**影響の可能性: 中**

`php artisan down` コマンドの `--message` オプションは削除されました。代わりに、選択したメッセージを含む [メンテナンス モード ビューの事前レンダリング](/docs/{{version}}/configuration#maintenance-mode) を検討してください。

<a name="php-artisan-serve-no-reload-option"></a>
#### `php artisan serve --no-reload` オプション

**影響の可能性: 低い**

`--no-reload` オプションが `php artisan serve` コマンドに追加されました。これにより、環境ファイルの変更が検出されたときにサーバーをリロードしないように組み込みサーバーに指示されます。このオプションは主に、CI 環境で Laravel Dusk テストを実行する場合に役立ちます。

<a name="manager-app-property"></a>
#### マネージャー `$app` プロパティ

**影響の可能性: 低い**

以前に非推奨となった `Illuminate\Support\Manager` クラスの `$app` プロパティは削除されました。このプロパティに依存していた場合は、代わりに `$container` プロパティを使用する必要があります。

<a name="the-elixir-helper"></a>
#### `elixir` ヘルパ

**影響の可能性: 低い**

以前に非推奨となった `elixir` ヘルパは削除されました。この方法をまだ使用しているアプリケーションは、[Laravel Mix](https://github.com/JeffreyWay/laravel-mix) にアップグレードすることをお勧めします。

<a name="mail"></a>
### 郵便

<a name="the-sendnow-method"></a>
#### `sendNow` メソッド

**影響の可能性: 低い**

以前に非推奨となった `sendNow` メソッドは削除されました。代わりに、`send` メソッドを使用してください。

<a name="pagination"></a>
### ページネーション

<a name="pagination-defaults"></a>
#### ページネーションのデフォルト

**影響の可能性: 高**

ページネータはデフォルトのスタイルに [Tailwind CSS フレームワーク](https://tailwindcss.com) を使用するようになりました。ブートストラップを引き続き使用するには、アプリケーションの `AppServiceProvider` の `boot` メソッドに次のメソッド呼び出しを追加する必要があります。

    use Illuminate\Pagination\Paginator;

    Paginator::useBootstrap();

<a name="queue"></a>
### 列

<a name="queue-retry-after-method"></a>
#### `retryAfter` メソッド

**影響の可能性: 高**

Laravel の他の機能との一貫性を保つために、キューに入れられたジョブ、メーラー、通知、リスナの `retryAfter` メソッドと `retryAfter` プロパティの名前が `backoff` に変更されました。アプリケーションの関連クラスでこのメソッド/プロパティの名前を更新する必要があります。

<a name="queue-timeout-at-property"></a>
#### `timeoutAt` プロパティ

**影響の可能性: 高**

キューに入れられたジョブ、通知、およびリスナの `timeoutAt` プロパティの名前が `retryUntil` に変更されました。アプリケーションの関連クラスでこのプロパティの名前を更新する必要があります。

<a name="queue-allOnQueue-allOnConnection"></a>
#### `allOnQueue()` / `allOnConnection()` メソッド

**影響の可能性: 高**

他のディスパッチ方法との一貫性を保つために、ジョブ チェーンで使用される `allOnQueue()` メソッドと `allOnConnection()` メソッドは削除されました。代わりに、`onQueue()` メソッドと `onConnection()` メソッドを使用することもできます。これらのメソッドは、`dispatch` メソッドを呼び出す前に呼び出す必要があります。

    ProcessPodcast::withChain([
        new OptimizePodcast,
        new ReleasePodcast
    ])->onConnection('redis')->onQueue('podcasts')->dispatch();

この変更は、`withChain` メソッドを使用するコードにのみ影響することに注意してください。グローバル `dispatch()` ヘルパを使用する場合、`allOnQueue()` および `allOnConnection()` は引き続き使用できます。

<a name="failed-jobs-table-batch-support"></a>
#### 失敗したジョブテーブルのバッチサポート

**影響の可能性: オプション**

Laravel 8.x の [ジョブのバッチ処理](/docs/{{version}}/queues#job-batching) 機能を使用する場合は、`failed_jobs` データベース テーブルを更新する必要があります。まず、新しい `uuid` 列をテーブルに追加する必要があります。

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('failed_jobs', function (Blueprint $table) {
        $table->string('uuid')->after('id')->nullable()->unique();
    });

次に、`queue` 構成ファイル内の `failed.driver` 構成オプションを `database-uuids` に更新する必要があります。

さらに、失敗した既存のジョブの UUID を生成することもできます。

    DB::table('failed_jobs')->whereNull('uuid')->cursor()->each(function ($job) {
        DB::table('failed_jobs')
            ->where('id', $job->id)
            ->update(['uuid' => (string) Illuminate\Support\Str::uuid()]);
    });

<a name="routing"></a>
### ルーティング

<a name="automatic-controller-namespace-prefixing"></a>
#### コントローラの名前空間の自動プレフィックス付け

**影響の可能性: オプション**

Laravel の以前のリリースでは、`RouteServiceProvider` クラスには、値 `App\Http\Controllers` を持つ `$namespace` プロパティが含まれていました。このプロパティの値は、`action` ヘルパを呼び出すときなど、コントローラ ルート宣言とコントローラ ルート URL生成に自動的にプレフィックスを付けるために使用されていました。

Laravel 8 では、このプロパティはデフォルトで `null` に設定されます。これにより、コントローラのルート宣言で標準の PHP 呼び出し可能構文を使用できるようになり、多くの IDE でコントローラ クラスへのジャンプのサポートが強化されます。

    use App\Http\Controllers\UserController;

    // Using PHP callable syntax...
    Route::get('/users', [UserController::class, 'index']);

    // Using string syntax...
    Route::get('/users', 'App\Http\Controllers\UserController@index');

ほとんどの場合、`RouteServiceProvider` には以前の値の `$namespace` プロパティが含まれているため、アップグレード中のアプリケーションには影響しません。ただし、新しい Laravel プロジェクトを作成してアプリケーションをアップグレードする場合、これは重大な変更として発生する可能性があります。

元の自動プレフィックス付きコントローラ ルーティングを引き続き使用したい場合は、`RouteServiceProvider` 内の `$namespace` プロパティの値を設定し、`boot` メソッド内のルート登録を更新して、`$namespace` プロパティを使用することができます。

    class RouteServiceProvider extends ServiceProvider
    {
        /**
         * The path to the "home" route for your application.
         *
         * This is used by Laravel authentication to redirect users after login.
         *
         * @var string
         */
        public const HOME = '/home';

        /**
         * If specified, this namespace is automatically applied to your controller routes.
         *
         * In addition, it is set as the URL generator's root namespace.
         *
         * @var string
         */
        protected $namespace = 'App\Http\Controllers';

        /**
         * Define your route model bindings, pattern filters, etc.
         *
         * @return void
         */
        public function boot()
        {
            $this->configureRateLimiting();

            $this->routes(function () {
                Route::middleware('web')
                    ->namespace($this->namespace)
                    ->group(base_path('routes/web.php'));

                Route::prefix('api')
                    ->middleware('api')
                    ->namespace($this->namespace)
                    ->group(base_path('routes/api.php'));
            });
        }

        /**
         * Configure the rate limiters for the application.
         *
         * @return void
         */
        protected function configureRateLimiting()
        {
            RateLimiter::for('api', function (Request $request) {
                return Limit::perMinute(60)->by(optional($request->user())->id ?: $request->ip());
            });
        }
    }

<a name="scheduling"></a>
### スケジュール設定

<a name="the-cron-expression-library"></a>
#### `cron-expression` ライブラリ

**影響の可能性: 低い**

Laravel の `dragonmantank/cron-expression` への依存関係が `2.x` から `3.x` に更新されました。 `cron-expression` ライブラリを直接操作しない限り、これによってアプリケーションに重大な変更が生じることはありません。このライブラリを直接操作している場合は、[変更ログ](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md) を確認してください。

<a name="session"></a>
### セッション

<a name="the-session-contract"></a>
#### `Session` 契約

**影響の可能性: 低い**

`Illuminate\Contracts\Session\Session` コントラクトは、新しい `pull` メソッドを受け取りました。このコントラクトを手動で実装している場合は、それに応じて実装を更新する必要があります。

    /**
     * Get the value of a given key and then forget it.
     *
     * @param  string  $key
     * @param  mixed  $default
     * @return mixed
     */
    public function pull($key, $default = null);

<a name="testing"></a>
### テスト

<a name="decode-response-json-method"></a>
#### `decodeResponseJson` メソッド

**影響の可能性: 低い**

`Illuminate\Testing\TestResponse` クラスに属する `decodeResponseJson` メソッドは引数を受け入れなくなりました。代わりに、`json` メソッドの使用を検討してください。

<a name="assert-exact-json-method"></a>
#### `assertExactJson` メソッド

**影響の可能性: 中**

`assertExactJson` メソッドでは、比較される配列の数値キーが一致し、同じ順序であることが必要になりました。数値キー付き配列の順序を同じにすることなく、JSON を配列と比較したい場合は、代わりに `assertSimilarJson` メソッドを使用できます。

<a name="validation"></a>
### 検証

<a name="database-rule-connections"></a>
### データベースルール接続

**影響の可能性: 低い**

`unique` ルールと `exists` ルールは、クエリを実行するときに Eloquent モデルの指定された接続名 (モデルの `getConnectionName` メソッドを介してアクセスされる) を尊重するようになりました。

<a name="miscellaneous"></a>
### その他

`laravel/laravel` [GitHub リポジトリ](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub比較ツール](https://github.com/laravel/laravel/compare/7.x...8.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

