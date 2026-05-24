# キャッシュ (Cache)

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [ドライバの前提条件](#driver-prerequisites)
- [キャッシュの使用量](#cache-usage)
    - [キャッシュインスタンスの取得](#obtaining-a-cache-instance)
    - [キャッシュからアイテムを取得する](#retrieving-items-from-the-cache)
    - [アイテムをキャッシュに保存する](#storing-items-in-the-cache)
    - [キャッシュからのアイテムの削除](#removing-items-from-the-cache)
    - [キャッシュヘルパ](#the-cache-helper)
- [キャッシュタグ](#cache-tags)
    - [タグ付きキャッシュ項目の保存](#storing-tagged-cache-items)
    - [タグ付きキャッシュ項目へのアクセス](#accessing-tagged-cache-items)
    - [タグ付きキャッシュ項目の削除](#removing-tagged-cache-items)
- [アトミックロック](#atomic-locks)
    - [ドライバの前提条件](#lock-driver-prerequisites)
    - [ロックの管理](#managing-locks)
    - [プロセス全体でのロックの管理](#managing-locks-across-processes)
- [カスタム キャッシュ ドライバの追加](#adding-custom-cache-drivers)
    - [ドライバの作成](#writing-the-driver)
    - [ドライバを登録する](#registering-the-driver)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

アプリケーションによって実行されるデータの取得または処理タスクの中には、CPU に負荷がかかるものや、完了までに数秒かかるものもあります。この場合、同じデータに対する後続のリクエストですぐに取得できるように、取得したデータを一時的にキャッシュするのが一般的です。キャッシュされたデータは通常、[Memcached](https://memcached.org) や [Redis](https://redis.io) などの非常に高速なデータ ストアに保存されます。

ありがたいことに、Laravel はさまざまなキャッシュ バックエンドに表現力豊かな統合 API を提供しており、その超高速データ取得を活用して Web アプリケーションを高速化できます。

<a name="configuration"></a>
## 構成 (Configuration)

アプリケーションのキャッシュ構成ファイルは、`config/cache.php` にあります。このファイルでは、アプリケーション全体でデフォルトで使用するキャッシュ ドライバを指定できます。 Laravel は、[Memcached](https://memcached.org)、[Redis](https://redis.io)、[DynamoDB](https://aws.amazon.com/dynamodb) などの一般的なキャッシュ バックエンドやリレーショナル データベースをそのままサポートしています。さらに、ファイル ベースのキャッシュ ドライバも利用でき、`array` および "null" キャッシュ ドライバは自動テストに便利なキャッシュ バックエンドを提供します。

キャッシュ構成ファイルには、ファイル内に文書化されている他のさまざまなオプションも含まれているため、これらのオプションを必ず読んでください。デフォルトでは、Laravel は `file` キャッシュドライバを使用するように構成されており、シリアル化されたキャッシュされたオブジェクトがサーバーのファイルシステムに保存されます。大規模なアプリケーションの場合は、Memcached や Redis などのより堅牢なドライバを使用することをお勧めします。同じドライバに対して複数のキャッシュ構成を構成することもできます。

<a name="driver-prerequisites"></a>
### ドライバの前提条件

<a name="prerequisites-database"></a>
#### データベース

`database` キャッシュ ドライバを使用する場合は、キャッシュ アイテムを含むテーブルを設定する必要があります。以下の表に、`Schema` 宣言の例を示します。

    Schema::create('cache', function ($table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

> **注記**
> `php artisan cache:table` Artisan コマンドを使用して、適切なスキーマで移行を生成することもできます。

<a name="memcached"></a>
#### Memcached

Memcached ドライバを使用するには、[Memcached PECL パッケージ](https://pecl.php.net/package/memcached) をインストールする必要があります。すべての Memcached サーバーを `config/cache.php` 構成ファイルにリストすることができます。このファイルには、すぐに使用できる `memcached.servers` エントリがすでに含まれています。

    'memcached' => [
        'servers' => [
            [
                'host' => env('MEMCACHED_HOST', '127.0.0.1'),
                'port' => env('MEMCACHED_PORT', 11211),
                'weight' => 100,
            ],
        ],
    ],

必要に応じて、`host` オプションを UNIX ソケット パスに設定できます。これを行う場合、`port` オプションを `0` に設定する必要があります。

    'memcached' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],

<a name="redis"></a>
#### レディス

Laravel で Redis キャッシュを使用する前に、PECL 経由で PhpRedis PHP 拡張機能をインストールするか、Composer 経由で `predis/predis` パッケージ (~1.0) をインストールする必要があります。 [Laravel Sail](/docs/{{version}}/sail) には、この拡張機能がすでに含まれています。さらに、[Laravel Forge](https://forge.laravel.com) や [Laravel Vapor](https://vapor.laravel.com) などの公式の Laravel デプロイメント プラットフォームには、デフォルトで PhpRedis 拡張機能がインストールされています。

Redis の構成の詳細については、[Laravelのドキュメントページ](/docs/{{version}}/redis#configuration) を参照してください。

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) キャッシュ ドライバを使用する前に、すべてのキャッシュ データを保存する DynamoDB テーブルを作成する必要があります。通常、このテーブルには `cache` という名前を付ける必要があります。ただし、アプリケーションの `cache` 構成ファイル内の `stores.dynamodb.table` 構成値の値に基づいてテーブルに名前を付ける必要があります。

このテーブルには、アプリケーションの `cache` 構成ファイル内の `stores.dynamodb.attributes.key` 構成項目の値に対応する名前を持つ文字列パーティション キーも必要です。デフォルトでは、パーティション キーの名前は `key` である必要があります。

<a name="cache-usage"></a>
## キャッシュの使用量 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### キャッシュインスタンスの取得

キャッシュ ストア インスタンスを取得するには、`Cache` ファサードを使用できます。これは、このドキュメント全体で使用するものです。 `Cache` ファサードは、Laravel キャッシュ コントラクトの基礎となる実装への便利で簡潔なアクセスを提供します。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Support\Facades\Cache;

    class UserController extends Controller
    {
        /**
         * Show a list of all users of the application.
         *
         * @return Response
         */
        public function index()
        {
            $value = Cache::get('key');

            //
        }
    }

<a name="accessing-multiple-cache-stores"></a>
#### 複数のキャッシュ ストアへのアクセス

`Cache` ファサードを使用すると、`store` メソッド経由でさまざまなキャッシュ ストアにアクセスできます。 `store` メソッドに渡されるキーは、`cache` 構成ファイルの `stores` 構成配列にリストされているストアの 1 つに対応する必要があります。

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes

<a name="retrieving-items-from-the-cache"></a>
### キャッシュからアイテムを取得する

`Cache` ファサードの `get` メソッドは、キャッシュから項目を取得するために使用されます。項目がキャッシュに存在しない場合は、`null` が返されます。必要に応じて、項目が存在しない場合に返されるデフォルト値を指定する 2 番目の引数を `get` メソッドに渡すことができます。

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

クロージャをデフォルト値として渡すこともできます。指定された項目がキャッシュに存在しない場合は、クロージャの結果が返されます。クロージャーを渡すと、データベースまたは他の外部サービスからのデフォルト値の取得を延期できます。

    $value = Cache::get('key', function () {
        return DB::table(/* ... */)->get();
    });

<a name="checking-for-item-existence"></a>
#### アイテムの存在を確認する

`has` メソッドを使用して、アイテムがキャッシュに存在するかどうかを確認できます。項目が存在するが、その値が `null` である場合、このメソッドは `false` も返します。

    if (Cache::has('key')) {
        //
    }

<a name="incrementing-decrementing-values"></a>
#### 値の増減

`increment` メソッドと `decrement` メソッドは、キャッシュ内の整数項目の値を調整するために使用できます。これらのメソッドはどちらも、項目の値を増減する量を示すオプションの 2 番目の引数を受け入れます。

    Cache::increment('key');
    Cache::increment('key', $amount);
    Cache::decrement('key');
    Cache::decrement('key', $amount);

<a name="retrieve-store"></a>
#### 取得と保存

キャッシュから項目を取得したい場合がありますが、要求された項目が存在しない場合はデフォルト値を保存することもできます。たとえば、すべてのユーザーをキャッシュから取得したり、ユーザーが存在しない場合はデータベースから取得してキャッシュに追加したりすることができます。これは、`Cache::remember` メソッドを使用して実行できます。

    $value = Cache::remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

項目がキャッシュに存在しない場合、`remember` メソッドに渡されたクロージャが実行され、その結果がキャッシュに配置されます。

`rememberForever` メソッドを使用して、キャッシュからアイテムを取得したり、アイテムが存在しない場合は永久に保存したりできます。

    $value = Cache::rememberForever('users', function () {
        return DB::table('users')->get();
    });

<a name="retrieve-delete"></a>
#### 取得と削除

キャッシュから項目を取得してからその項目を削除する必要がある場合は、`pull` メソッドを使用できます。 `get` メソッドと同様に、項目がキャッシュに存在しない場合は `null` が返されます。

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### アイテムをキャッシュに保存する

`Cache` ファサードで `put` メソッドを使用して、アイテムをキャッシュに保存できます。

    Cache::put('key', 'value', $seconds = 10);

保管時間が `put` メソッドに渡されない場合、アイテムは無期限に保管されます。

    Cache::put('key', 'value');

秒数を整数として渡す代わりに、キャッシュされたアイテムの有効期限を表す `DateTime` インスタンスを渡すこともできます。

    Cache::put('key', 'value', now()->addMinutes(10));

<a name="store-if-not-present"></a>
#### 存在しない場合は保存する

`add` メソッドは、アイテムがキャッシュ ストアに存在しない場合にのみ、アイテムをキャッシュに追加します。項目が実際にキャッシュに追加される場合、メソッドは `true` を返します。それ以外の場合、メソッドは `false` を返します。 `add` メソッドはアトミック操作です。

    Cache::add('key', 'value', $seconds);

<a name="storing-items-forever"></a>
#### アイテムを永久に保管する

`forever` メソッドを使用して、アイテムをキャッシュに永続的に保存できます。これらのアイテムは期限切れにならないため、`forget` メソッドを使用してキャッシュから手動で削除する必要があります。

    Cache::forever('key', 'value');

> **注記**
> Memcached ドライバを使用している場合、キャッシュがサイズ制限に達すると、「永久に」保存されている項目が削除される可能性があります。

<a name="removing-items-from-the-cache"></a>
### キャッシュからのアイテムの削除

`forget` メソッドを使用して、キャッシュから項目を削除できます。

    Cache::forget('key');

ゼロまたは負の有効期限秒数を指定してアイテムを削除することもできます。

    Cache::put('key', 'value', 0);

    Cache::put('key', 'value', -5);

`flush` メソッドを使用してキャッシュ全体をクリアできます。

    Cache::flush();

> **警告**
> キャッシュをフラッシュすると、設定されたキャッシュの「プレフィックス」が考慮されず、キャッシュからすべてのエントリが削除されます。他のアプリケーションによって共有されているキャッシュをクリアするときは、この点を慎重に検討してください。

<a name="the-cache-helper"></a>
### キャッシュヘルパ

`Cache` ファサードの使用に加えて、グローバル `cache` 関数を使用して、キャッシュ経由でデータを取得および保存することもできます。単一の文字列引数を指定して `cache` 関数を呼び出すと、指定されたキーの値が返されます。

    $value = cache('key');

キーと値のペアの配列と有効期限を関数に指定すると、指定された期間、値がキャッシュに保存されます。

    cache(['key' => 'value'], $seconds);

    cache(['key' => 'value'], now()->addMinutes(10));

`cache` 関数を引数なしで呼び出すと、`Illuminate\Contracts\Cache\Factory` 実装のインスタンスが返され、他のキャッシュ メソッドを呼び出すことができます。

    cache()->remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

> **注記**
> グローバル `cache` 関数の呼び出しをテストするときは、[ファサードのテスト](/docs/{{version}}/mocking#mocking-facades) であるかのように `Cache::shouldReceive` メソッドを使用できます。

<a name="cache-tags"></a>
## キャッシュタグ (Cache Tags)

> **警告**
> `file`、`dynamodb`、または `database` キャッシュ ドライバを使用する場合、キャッシュ タグはサポートされません。さらに、「永久に」保存されるキャッシュを持つ複数のタグを使用する場合、古いレコードを自動的に削除する `memcached` などのドライバを使用すると、パフォーマンスが最高になります。

<a name="storing-tagged-cache-items"></a>
### タグ付きキャッシュ項目の保存

キャッシュ タグを使用すると、キャッシュ内の関連アイテムにタグを付けて、特定のタグが割り当てられているすべてのキャッシュされた値をフラッシュできます。タグ名の順序付き配列を渡すことで、タグ付きキャッシュにアクセスできます。たとえば、タグ付きキャッシュにアクセスし、キャッシュ内の値を `put` してみましょう。

    Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

    Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);

<a name="accessing-tagged-cache-items"></a>
### タグ付きキャッシュ項目へのアクセス

タグを介して保存されたアイテムには、値の保存に使用されたタグも提供しないとアクセスできません。タグ付きキャッシュ アイテムを取得するには、同じ順序で並べられたタグのリストを `tags` メソッドに渡し、取得するキーを指定して `get` メソッドを呼び出します。

    $john = Cache::tags(['people', 'artists'])->get('John');

    $anne = Cache::tags(['people', 'authors'])->get('Anne');

<a name="removing-tagged-cache-items"></a>
### タグ付きキャッシュ項目の削除

タグまたはタグのリストが割り当てられているすべての項目をフラッシュできます。たとえば、このステートメントは、`people`、`authors`、またはその両方でタグ付けされたすべてのキャッシュを削除します。したがって、`Anne` と `John` の両方がキャッシュから削除されます。

    Cache::tags(['people', 'authors'])->flush();

対照的に、このステートメントは、`authors` でタグ付けされたキャッシュされた値のみを削除するため、`Anne` は削除されますが、`John` は削除されません。

    Cache::tags('authors')->flush();

<a name="atomic-locks"></a>
## アトミックロック (Atomic Locks)

> **警告**
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<a name="lock-driver-prerequisites"></a>
### ドライバの前提条件

<a name="atomic-locks-prerequisites-database"></a>
#### データベース

`database` キャッシュ ドライバを使用する場合は、アプリケーションのキャッシュ ロックを含むテーブルをセットアップする必要があります。以下の表に、`Schema` 宣言の例を示します。

    Schema::create('cache_locks', function ($table) {
        $table->string('key')->primary();
        $table->string('owner');
        $table->integer('expiration');
    });

<a name="managing-locks"></a>
### ロックの管理

アトミック ロックを使用すると、競合状態を気にせずに分散ロックを操作できます。たとえば、[Laravel Forge](https://forge.laravel.com) はアトミック ロックを使用して、サーバー上で一度に 1 つのリモート タスクのみが実行されるようにします。 `Cache::lock` メソッドを使用してロックを作成および管理できます。

    use Illuminate\Support\Facades\Cache;

    $lock = Cache::lock('foo', 10);

    if ($lock->get()) {
        // Lock acquired for 10 seconds...

        $lock->release();
    }

`get` メソッドはクロージャーも受け入れます。クロージャーが実行されると、Laravel は自動的にロックを解放します。

    Cache::lock('foo', 10)->get(function () {
        // Lock acquired for 10 seconds and automatically released...
    });

リクエストした時点でロックが利用できない場合は、Laravel に指定した秒数待機するように指示できます。指定された制限時間内にロックを取得できない場合は、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

    use Illuminate\Contracts\Cache\LockTimeoutException;

    $lock = Cache::lock('foo', 10);

    try {
        $lock->block(5);

        // Lock acquired after waiting a maximum of 5 seconds...
    } catch (LockTimeoutException $e) {
        // Unable to acquire lock...
    } finally {
        optional($lock)->release();
    }

上記の例は、`block` メソッドにクロージャーを渡すことで簡略化できます。クロージャがこのメソッドに渡されると、Laravel は指定された秒数の間ロックの取得を試み、クロージャが実行されると自動的にロックを解放します。

    Cache::lock('foo', 10)->block(5, function () {
        // Lock acquired after waiting a maximum of 5 seconds...
    });

<a name="managing-locks-across-processes"></a>
### プロセス全体でのロックの管理

場合によっては、あるプロセスでロックを取得し、別のプロセスでロックを解放したい場合があります。たとえば、Web リクエスト中にロックを取得し、そのリクエストによってトリガーされたキューに入れられたジョブの終了時にロックを解放したい場合があります。このシナリオでは、ジョブが指定されたトークンを使用してロックを再インスタンス化できるように、ロックのスコープ指定された「所有者トークン」をキューに入れられたジョブに渡す必要があります。

以下の例では、ロックが正常に取得された場合に、キューに入れられたジョブをディスパッチします。さらに、ロックの `owner` メソッドを介して、ロックの所有者トークンをキューに入れられたジョブに渡します。

    $podcast = Podcast::find($id);

    $lock = Cache::lock('processing', 120);

    if ($lock->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

アプリケーションの `ProcessPodcast` ジョブ内で、所有者トークンを使用してロックを復元および解放できます。

    Cache::restoreLock('processing', $this->owner)->release();

現在の所有者を考慮せずにロックを解放したい場合は、`forceRelease` メソッドを使用できます。

    Cache::lock('processing')->forceRelease();

<a name="adding-custom-cache-drivers"></a>
## カスタム キャッシュ ドライバの追加 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### ドライバの作成

カスタム キャッシュ ドライバを作成するには、まず `Illuminate\Contracts\Cache\Store` [contract](/docs/{{version}}/contracts) を実装する必要があります。したがって、MongoDB キャッシュの実装は次のようになります。

    <?php

    namespace App\Extensions;

    use Illuminate\Contracts\Cache\Store;

    class MongoStore implements Store
    {
        public function get($key) {}
        public function many(array $keys) {}
        public function put($key, $value, $seconds) {}
        public function putMany(array $values, $seconds) {}
        public function increment($key, $value = 1) {}
        public function decrement($key, $value = 1) {}
        public function forever($key, $value) {}
        public function forget($key) {}
        public function flush() {}
        public function getPrefix() {}
    }

MongoDB 接続を使用してこれらの各メソッドを実装するだけです。これらの各メソッドの実装方法の例については、[Laravelフレームワークのソースコード](https://github.com/laravel/framework) の `Illuminate\Cache\MemcachedStore` を参照してください。実装が完了したら、`Cache` ファサードの `extend` メソッドを呼び出して、カスタム ドライバの登録を完了できます。

    Cache::extend('mongo', function ($app) {
        return Cache::repository(new MongoStore);
    });

> **注記**
> カスタム キャッシュ ドライバ コードをどこに配置するか迷っている場合は、`app` ディレクトリ内に `Extensions` 名前空間を作成できます。ただし、Laravel には厳格なアプリケーション構造はなく、好みに応じてアプリケーションを自由に編成できることに注意してください。

<a name="registering-the-driver"></a>
### ドライバを登録する

カスタム キャッシュ ドライバを Laravel に登録するには、`Cache` ファサードで `extend` メソッドを使用します。他のサービスプロバイダは `boot` メソッド内でキャッシュされた値を読み取ろうとする可能性があるため、`booting` コールバック内でカスタム ドライバを登録します。 `booting` コールバックを使用すると、アプリケーションのサービスプロバイダで `boot` メソッドが呼び出される直前、ただしすべてのサービスプロバイダで `register` メソッドが呼び出された後、カスタム ドライバが確実に登録されます。アプリケーションの `App\Providers\AppServiceProvider` クラスの `register` メソッド内に `booting` コールバックを登録します。

    <?php

    namespace App\Providers;

    use App\Extensions\MongoStore;
    use Illuminate\Support\Facades\Cache;
    use Illuminate\Support\ServiceProvider;

    class CacheServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            $this->app->booting(function () {
                 Cache::extend('mongo', function ($app) {
                     return Cache::repository(new MongoStore);
                 });
             });
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            //
        }
    }

`extend` メソッドに渡される最初の引数はドライバの名前です。これは、`config/cache.php` 構成ファイルの `driver` オプションに対応します。 2 番目の引数は、`Illuminate\Cache\Repository` インスタンスを返すクロージャです。クロージャには、[サービスコンテナ](/docs/{{version}}/container) のインスタンスである `$app` インスタンスが渡されます。

拡張機能が登録されたら、`config/cache.php` 構成ファイルの `driver` オプションを拡張機能の名前に更新します。

<a name="events"></a>
## イベント (Events)

すべてのキャッシュ操作でコードを実行するには、キャッシュによって起動される [events](/docs/{{version}}/events) をリッスンできます。通常、これらのイベント リスナはアプリケーションの `App\Providers\EventServiceProvider` クラス内に配置する必要があります。
    
    use App\Listeners\LogCacheHit;
    use App\Listeners\LogCacheMissed;
    use App\Listeners\LogKeyForgotten;
    use App\Listeners\LogKeyWritten;
    use Illuminate\Cache\Events\CacheHit;
    use Illuminate\Cache\Events\CacheMissed;
    use Illuminate\Cache\Events\KeyForgotten;
    use Illuminate\Cache\Events\KeyWritten;
    
    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        CacheHit::class => [
            LogCacheHit::class,
        ],

        CacheMissed::class => [
            LogCacheMissed::class,
        ],

        KeyForgotten::class => [
            LogKeyForgotten::class,
        ],

        KeyWritten::class => [
            LogKeyWritten::class,
        ],
    ];

