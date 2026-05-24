# レディス (Redis)

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Clusters](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis との対話](#interacting-with-redis)
    - [Transactions](#transactions)
    - [コマンドのパイプライン化](#pipelining-commands)
- [パブ/サブ](#pubsub)

<a name="introduction"></a>
## 導入 (Introduction)

[Redis](https://redis.io) は、オープンソースの高度な Key-Value ストアです。キーには [strings](https://redis.io/docs/latest/develop/data-types/strings/)、[hashes](https://redis.io/docs/latest/develop/data-types/hashes/)、[lists](https://redis.io/docs/latest/develop/data-types/lists/)、[sets](https://redis.io/docs/latest/develop/data-types/sets/)、[ソートされたセット](https://redis.io/docs/latest/develop/data-types/sorted-sets/) を含めることができるため、データ構造サーバーと呼ばれることがよくあります。

Laravel で Redis を使用する前に、PECL 経由で [PhpRedis](https://github.com/phpredis/phpredis) PHP 拡張機能をインストールして使用することをお勧めします。この拡張機能は、「ユーザーランド」PHP パッケージに比べてインストールが複雑ですが、Redis を頻繁に使用するアプリケーションではパフォーマンスが向上する可能性があります。 [Laravel Sail](/docs/{{version}}/sail) を使用している場合、この拡張機能はアプリケーションの Docker コンテナーにすでにインストールされています。

PhpRedis 拡張機能をインストールできない場合は、Composer 経由で `predis/predis` パッケージをインストールできます。 Predis は、完全に PHP で書かれた Redis クライアントであり、追加の拡張機能は必要ありません。

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 構成 (Configuration)

`config/database.php` 構成ファイルを介してアプリケーションの Redis 設定を構成できます。このファイル内には、アプリケーションで使用される Redis サーバーを含む `redis` 配列が表示されます。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

        'cache' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_CACHE_DB', 1),
        ],

    ],

Redis 接続を表す単一の URL を定義しない限り、構成ファイルで定義された各 Redis サーバーには、名前、ホスト、およびポートが必要です。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'url' => 'tcp://127.0.0.1:6379?database=0',
        ],

        'cache' => [
            'url' => 'tls://user:password@127.0.0.1:6380?database=1',
        ],

    ],

<a name="configuring-the-connection-scheme"></a>
#### 接続スキームの構成

デフォルトでは、Redis クライアントは Redis サーバーに接続するときに `tcp` スキームを使用します。ただし、Redis サーバーの構成配列で `scheme` 構成オプションを指定することで、TLS / SSL 暗号化を使用できます。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'scheme' => 'tls',
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

    ],

<a name="clusters"></a>
### クラスター

アプリケーションが Redis サーバーのクラスターを利用している場合は、Redis 構成の `clusters` キー内でこれらのクラスターを定義する必要があります。この構成キーはデフォルトでは存在しないため、アプリケーションの `config/database.php` 構成ファイル内に作成する必要があります。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'clusters' => [
            'default' => [
                [
                    'host' => env('REDIS_HOST', 'localhost'),
                    'password' => env('REDIS_PASSWORD'),
                    'port' => env('REDIS_PORT', 6379),
                    'database' => 0,
                ],
            ],
        ],

    ],

デフォルトでは、クラスターはノード全体でクライアント側のシャーディングを実行し、ノードをプールして大量の使用可能な RAM を作成できるようにします。ただし、クライアント側のシャーディングはフェイルオーバーを処理しません。したがって、これは主に、別のプライマリ データ ストアから利用できる一時的なキャッシュ データに適しています。

クライアント側シャーディングの代わりにネイティブ Redis クラスタリングを使用したい場合は、アプリケーションの `config/database.php` 構成ファイル内で `options.cluster` 構成値を `redis` に設定することでこれを指定できます。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'cluster' => env('REDIS_CLUSTER', 'redis'),
        ],

        'clusters' => [
            // ...
        ],

    ],

<a name="predis"></a>
### プレディス

アプリケーションが Predis パッケージ経由で Redis と対話できるようにする場合は、`REDIS_CLIENT` 環境変数の値が `predis` であることを確認する必要があります。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'predis'),

        // ...
    ],

デフォルトの `host`、`port`、`database`、および `password` サーバー構成オプションに加えて、Predis は、各 Redis サーバーに定義できる追加の [接続パラメータ](https://github.com/nrk/predis/wiki/Connection-Parameters) をサポートします。これらの追加の構成オプションを利用するには、アプリケーションの `config/database.php` 構成ファイル内の Redis サーバー構成に追加します。

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_write_timeout' => 60,
    ],

<a name="the-redis-facade-alias"></a>
#### Redis ファサードのエイリアス

Laravel の `config/app.php` 構成ファイルには、フレームワークによって登録されるすべてのクラス エイリアスを定義する `aliases` 配列が含まれています。デフォルトでは、`Redis` エイリアスは含まれません。これは、PhpRedis 拡張機能によって提供される `Redis` クラス名と競合するためです。 Predis クライアントを使用していて、`Redis` エイリアスを追加したい場合は、アプリケーションの `config/app.php` 構成ファイルの `aliases` 配列にエイリアスを追加できます。

    'aliases' => Facade::defaultAliases()->merge([
        'Redis' => Illuminate\Support\Facades\Redis::class,
    ])->toArray(),

<a name="phpredis"></a>
### PhpRedis

デフォルトでは、Laravel は PhpRedis 拡張機能を使用して Redis と通信します。 Laravel が Redis と通信するために使用するクライアントは、`redis.client` 構成オプションの値によって決まります。これは通常、`REDIS_CLIENT` 環境変数の値を反映します。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        // Rest of Redis configuration...
    ],

デフォルトの `scheme`、`host`、`port`、`database`、および `password` サーバー構成オプションに加えて、PhpRedis は次の追加接続パラメータをサポートします: `name`、`persistent`、`persistent_id`、 `prefix`、`read_timeout`、`retry_interval`、`timeout`、および `context`。 `config/database.php` 構成ファイル内の Redis サーバー構成に、次のオプションのいずれかを追加できます。

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_timeout' => 60,
        'context' => [
            // 'auth' => ['username', 'secret'],
            // 'stream' => ['verify_peer' => false],
        ],
    ],

<a name="phpredis-serialization"></a>
#### PhpRedis のシリアル化と圧縮

PhpRedis 拡張機能は、さまざまなシリアライザーや圧縮アルゴリズムを使用するように構成することもできます。これらのアルゴリズムは、Redis 構成の `options` 配列を介して構成できます。

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'serializer' => Redis::SERIALIZER_MSGPACK,
            'compression' => Redis::COMPRESSION_LZ4,
        ],

        // Rest of Redis configuration...
    ],

現在サポートされているシリアライザーには、`Redis::SERIALIZER_NONE` (デフォルト)、`Redis::SERIALIZER_PHP`、`Redis::SERIALIZER_JSON`、`Redis::SERIALIZER_IGBINARY`、および `Redis::SERIALIZER_MSGPACK` が含まれます。

サポートされている圧縮アルゴリズムには、`Redis::COMPRESSION_NONE` (デフォルト)、`Redis::COMPRESSION_LZF`、`Redis::COMPRESSION_ZSTD`、および `Redis::COMPRESSION_LZ4` があります。

<a name="interacting-with-redis"></a>
## Redis との対話 (Interacting With Redis)

`Redis` [facade](/docs/{{version}}/facades) でさまざまなメソッドを呼び出すことで、Redis と対話できます。 `Redis` ファサードは動的メソッドをサポートしています。つまり、ファサードで任意の [Redisコマンド](https://redis.io/commands) を呼び出すことができ、コマンドは Redis に直接渡されます。この例では、`Redis` ファサードで `get` メソッドを呼び出して、Redis `GET` コマンドを呼び出します。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\Redis;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         */
        public function show(string $id): View
        {
            return view('user.profile', [
                'user' => Redis::get('user:profile:'.$id)
            ]);
        }
    }

上で述べたように、`Redis` ファサードで Redis のコマンドを呼び出すことができます。 Laravel はマジック メソッドを使用してコマンドを Redis サーバーに渡します。 Redis コマンドが引数を必要とする場合は、それらをファサードの対応するメソッドに渡す必要があります。

    use Illuminate\Support\Facades\Redis;

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

あるいは、`Redis` ファサードの `command` メソッドを使用してサーバーにコマンドを渡すこともできます。このメソッドは、最初の引数としてコマンドの名前を受け取り、2 番目の引数として値の配列を受け取ります。

    $values = Redis::command('lrange', ['name', 5, 10]);

<a name="using-multiple-redis-connections"></a>
#### 複数の Redis 接続の使用

アプリケーションの `config/database.php` 構成ファイルを使用すると、複数の Redis 接続/サーバーを定義できます。 `Redis` ファサードの `connection` メソッドを使用して、特定の Redis 接続への接続を取得できます。

    $redis = Redis::connection('connection-name');

デフォルトの Redis 接続のインスタンスを取得するには、追加の引数を指定せずに `connection` メソッドを呼び出すことができます。

    $redis = Redis::connection();

<a name="transactions"></a>
### 取引

`Redis` ファサードの `transaction` メソッドは、Redis のネイティブ `MULTI` および `EXEC` コマンドの便利なラッパーを提供します。 `transaction` メソッドは、唯一の引数としてクロージャを受け入れます。このクロージャは Redis 接続インスタンスを受け取り、このインスタンスに対して必要なコマンドを発行できます。クロージャ内で発行されるすべての Redis コマンドは、単一のアトミック トランザクションで実行されます。

    use Redis;
    use Illuminate\Support\Facades;

    Facades\Redis::transaction(function (Redis $redis) {
        $redis->incr('user_visits', 1);
        $redis->incr('total_visits', 1);
    });

> [!WARNING]  
> Redis トランザクションを定義する場合、Redis 接続から値を取得することはできません。トランザクションは単一のアトミックな操作として実行され、その操作はクロージャー全体がコマンドの実行を完了するまで実行されないことに注意してください。

#### Lua スクリプト

`eval` メソッドは、単一のアトミック操作で複数の Redis コマンドを実行する別の方法を提供します。ただし、`eval` メソッドには、操作中に Redis キー値を操作して検査できるという利点があります。 Redis スクリプトは [Lua プログラミング言語](https://www.lua.org) に記述されます。

`eval` メソッドは最初は少し怖いかもしれませんが、緊張を解くための基本的な例を見ていきます。 `eval` メソッドは複数の引数を必要とします。まず、Lua スクリプトを (文字列として) メソッドに渡す必要があります。次に、スクリプトが対話するキーの数を (整数として) 渡す必要があります。第三に、それらのキーの名前を渡す必要があります。最後に、スクリプト内でアクセスする必要があるその他の追加の引数を渡すことができます。

この例では、カウンタをインクリメントし、その新しい値を検査し、最初のカウンタの値が 5 より大きい場合は 2 番目のカウンタをインクリメントします。最後に、最初のカウンターの値を返します。

    $value = Redis::eval(<<<'LUA'
        local counter = redis.call("incr", KEYS[1])

        if counter > 5 then
            redis.call("incr", KEYS[2])
        end

        return counter
    LUA, 2, 'first-counter', 'second-counter');

> [!WARNING]  
> Redis スクリプトの詳細については、[Redis のドキュメント](https://redis.io/commands/eval) を参照してください。

<a name="pipelining-commands"></a>
### コマンドのパイプライン化

場合によっては、数十の Redis コマンドを実行する必要がある場合があります。コマンドごとに Redis サーバーへのネットワーク トリップを行う代わりに、`pipeline` メソッドを使用できます。 `pipeline` メソッドは、Redis インスタンスを受け取るクロージャーという 1 つの引数を受け入れます。すべてのコマンドをこの Redis インスタンスに発行すると、それらはすべて Redis サーバーに同時に送信され、サーバーへのネットワーク トリップが削減されます。コマンドは発行された順序で引き続き実行されます。

    use Redis;
    use Illuminate\Support\Facades;

    Facades\Redis::pipeline(function (Redis $pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## パブ/サブ (Pub / Sub)

Laravel は、Redis `publish` および `subscribe` コマンドへの便利なインターフェイスを提供します。これらの Redis コマンドを使用すると、特定の「チャネル」でメッセージをリッスンできます。別のアプリケーションから、または別のプログラミング言語を使用してメッセージをチャネルにパブリッシュすると、アプリケーションとプロセス間の通信が容易になります。

まず、`subscribe` メソッドを使用してチャネル リスナを設定しましょう。 `subscribe` メソッドを呼び出すと長時間実行プロセスが開始されるため、このメソッド呼び出しを [Artisan コマンド](/docs/{{version}}/artisan) 内に配置します。

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Support\Facades\Redis;

    class RedisSubscribe extends Command
    {
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'redis:subscribe';

        /**
         * The console command description.
         *
         * @var string
         */
        protected $description = 'Subscribe to a Redis channel';

        /**
         * Execute the console command.
         */
        public function handle(): void
        {
            Redis::subscribe(['test-channel'], function (string $message) {
                echo $message;
            });
        }
    }

ここで、`publish` メソッドを使用してメッセージをチャネルにパブリッシュできます。

    use Illuminate\Support\Facades\Redis;

    Route::get('/publish', function () {
        // ...

        Redis::publish('test-channel', json_encode([
            'name' => 'Adam Wathan'
        ]));
    });

<a name="wildcard-subscriptions"></a>
#### ワイルドカード サブスクリプション

`psubscribe` メソッドを使用すると、ワイルドカード チャネルをサブスクライブできます。これは、すべてのチャネル上のすべてのメッセージをキャッチするのに便利です。チャネル名は、提供されたクロージャの 2 番目の引数として渡されます。

    Redis::psubscribe(['*'], function (string $message, string $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function (string $message, string $channel) {
        echo $message;
    });

