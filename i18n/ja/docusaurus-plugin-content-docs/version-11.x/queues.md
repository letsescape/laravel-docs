# キュー (Queues)

- [Introduction](#introduction)
    - [接続とキュー](#connections-vs-queues)
    - [ドライバの注意事項と前提条件](#driver-prerequisites)
- [雇用の創出](#creating-jobs)
    - [ジョブクラスの生成](#generating-job-classes)
    - [クラス構造](#class-structure)
    - [ユニークなジョブ](#unique-jobs)
    - [暗号化されたジョブ](#encrypted-jobs)
- [ジョブミドルウェア](#job-middleware)
    - [レート制限](#rate-limiting)
    - [ジョブの重複を防ぐ](#preventing-job-overlaps)
    - [スロットリング例外](#throttling-exceptions)
    - [ジョブのスキップ](#skipping-jobs)
- [仕事の派遣](#dispatching-jobs)
    - [派遣の遅れ](#delayed-dispatching)
    - [同期ディスパッチング](#synchronous-dispatching)
    - [ジョブとデータベーストランザクション](#jobs-and-database-transactions)
    - [ジョブチェーン](#job-chaining)
    - [キューと接続のカスタマイズ](#customizing-the-queue-and-connection)
    - [最大ジョブ試行数/タイムアウト値の指定](#max-job-attempts-and-timeout)
    - [エラー処理](#error-handling)
- [ジョブのバッチ処理](#job-batching)
    - [バッチ可能ジョブの定義](#defining-batchable-jobs)
    - [バッチの発送](#dispatching-batches)
    - [チェーンとバッチ](#chains-and-batches)
    - [バッチへのジョブの追加](#adding-jobs-to-batches)
    - [バッチの検査](#inspecting-batches)
    - [バッチのキャンセル](#cancelling-batches)
    - [バッチの失敗](#batch-failures)
    - [バッチのプルーニング](#pruning-batches)
    - [DynamoDB へのバッチの保存](#storing-batches-in-dynamodb)
- [キューの閉鎖](#queueing-closures)
- [キューワーカーの実行](#running-the-queue-worker)
    - [`queue:work` コマンド](#the-queue-work-command)
    - [キューの優先順位](#queue-priorities)
    - [キューワーカーとデプロイメント](#queue-workers-and-deployment)
    - [ジョブの有効期限とタイムアウト](#job-expirations-and-timeouts)
- [スーパーバイザの構成](#supervisor-configuration)
- [失敗したジョブへの対処](#dealing-with-failed-jobs)
    - [失敗したジョブのクリーンアップ](#cleaning-up-after-failed-jobs)
    - [失敗したジョブの再試行](#retrying-failed-jobs)
    - [欠落しているモデルの無視](#ignoring-missing-models)
    - [失敗したジョブのプルーニング](#pruning-failed-jobs)
    - [失敗したジョブを DynamoDB に保存する](#storing-failed-jobs-in-dynamodb)
    - [失敗したジョブの保存を無効にする](#disabling-failed-job-storage)
    - [失敗したジョブイベント](#failed-job-events)
- [キューからジョブをクリアする](#clearing-jobs-from-queues)
- [キューの監視](#monitoring-your-queues)
- [Testing](#testing)
    - [ジョブのサブセットを偽装する](#faking-a-subset-of-jobs)
    - [ジョブチェーンのテスト](#testing-job-chains)
    - [ジョブバッチのテスト](#testing-job-batches)
    - [ジョブ/キューの相互作用のテスト](#testing-job-queue-interactions)
- [ジョブイベント](#job-events)

<a name="introduction"></a>
## 導入 (Introduction)

Web アプリケーションの構築中に、アップロードされた CSV ファイルの解析や保存など、通常の Web リクエストでは実行するには時間がかかりすぎるタスクがいくつか発生する場合があります。ありがたいことに、Laravel ではバックグラウンドで処理できるキューに入れられたジョブを簡単に作成できます。時間のかかるタスクをキューに移動することで、アプリケーションは Web リクエストに驚異的な速度で応答し、顧客により良いユーザー エクスペリエンスを提供できるようになります。

Laravel キューは、[アマゾンSQS](https://aws.amazon.com/sqs/)、[Redis](https://redis.io)、さらにはリレーショナル データベースなど、さまざまな異なるキュー バックエンドにわたって統合されたキュー API を提供します。

Laravel のキュー構成オプションは、アプリケーションの `config/queue.php` 構成ファイルに保存されます。このファイルには、データベース、[アマゾンSQS](https://aws.amazon.com/sqs/)、[Redis](https://redis.io)、[Beanstalkd](https://beanstalkd.github.io/) ドライバ、および (ローカル開発中に使用する) ジョブを即時に実行する同期ドライバなど、フレームワークに含まれる各キュー ドライバの接続構成が含まれています。キューに入れられたジョブを破棄する `null` キュー ドライバも含まれています。

> [!NOTE]  
> Laravel は、Redis を利用したキュー用の美しいダッシュボードおよび構成システムである Horizon を提供するようになりました。詳細については、[Horizon のドキュメント](/docs/{{version}}/horizon) の全文をご覧ください。

<a name="connections-vs-queues"></a>
### 接続とキュー

Laravel キューを使い始める前に、「接続」と「キュー」の違いを理解することが重要です。 `config/queue.php` 構成ファイルには、`connections` 構成配列があります。このオプションは、Amazon SQS、Beanstalk、Redis などのバックエンド キュー サービスへの接続を定義します。ただし、特定のキュー接続には、キューに入れられたジョブの異なるスタックまたは山とみなされる複数の「キュー」がある場合があります。

`queue` 構成ファイル内の各接続構成例には、`queue` 属性が含まれていることに注意してください。これは、ジョブが特定の接続に送信されるときにディスパッチされるデフォルトのキューです。つまり、ジョブをディスパッチするキューを明示的に定義せずにジョブをディスパッチすると、ジョブは接続構成の `queue` 属性で定義されたキューに配置されます。

    use App\Jobs\ProcessPodcast;

    // This job is sent to the default connection's default queue...
    ProcessPodcast::dispatch();

    // This job is sent to the default connection's "emails" queue...
    ProcessPodcast::dispatch()->onQueue('emails');

アプリケーションによっては、ジョブを複数のキューにプッシュする必要がなく、代わりに 1 つの単純なキューを持つことを好む場合があります。ただし、Laravel キューワーカーでは優先度によってどのキューを処理するかを指定できるため、ジョブを複数のキューにプッシュすることは、ジョブの処理方法に優先順位を付けたり、分割したりしたいアプリケーションにとって特に便利です。たとえば、ジョブを `high` キューにプッシュする場合、より高い処理優先度を与えるワーカーを実行できます。

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### ドライバの注意事項と前提条件

<a name="database"></a>
#### データベース

`database` キュー ドライバを使用するには、ジョブを保持するデータベース テーブルが必要です。通常、これはLaravelのデフォルトの`0001_01_01_000002_create_jobs_table.php` [データベースの移行](/docs/{{version}}/migrations)に含まれています。ただし、アプリケーションにこの移行が含まれていない場合は、`make:queue-table` Artisan コマンドを使用して移行を作成できます。

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### レディス

`redis` キュー ドライバを使用するには、`config/database.php` 構成ファイルで Redis データベース接続を構成する必要があります。

> [!WARNING]  
> `serializer` および `compression` Redis オプションは、`redis` キュー ドライバではサポートされていません。

**Redis クラスター**

Redis キュー接続で Redis クラスターを使用する場合、キュー名には [キーハッシュタグ](https://redis.io/docs/reference/cluster-spec/#hash-tags) が含まれている必要があります。これは、特定のキューのすべての Redis キーが同じハッシュ スロットに配置されるようにするために必要です。

    'redis' => [
        'driver' => 'redis',
        'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
        'queue' => env('REDIS_QUEUE', '{default}'),
        'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
        'block_for' => null,
        'after_commit' => false,
    ],

**ブロッキング**

Redis キューを使用する場合、`block_for` 構成オプションを使用して、ドライバがワーカー ループを繰り返して Redis データベースを再ポーリングする前に、ジョブが使用可能になるまで待機する時間を指定できます。

キューの負荷に基づいてこの値を調整すると、新しいジョブを求めて Redis データベースを継続的にポーリングするよりも効率的になる場合があります。たとえば、値を `5` に設定して、ジョブが使用可能になるまでドライバが 5 秒間ブロックされるように指定できます。

    'redis' => [
        'driver' => 'redis',
        'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
        'queue' => env('REDIS_QUEUE', 'default'),
        'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
        'block_for' => 5,
        'after_commit' => false,
    ],

> [!WARNING]  
> `block_for` を `0` に設定すると、ジョブが使用可能になるまでキューワーカーが無期限にブロックされます。これにより、次のジョブが処理されるまで、`SIGTERM` などのシグナルが処理されなくなります。

<a name="other-driver-prerequisites"></a>
#### その他のドライバの前提条件

リストされているキュー ドライバには次の依存関係が必要です。これらの依存関係は、Composer パッケージ マネージャーを介してインストールできます。

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- 豆の木: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` または phpredis PHP 拡張機能
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 雇用の創出 (Creating Jobs)

<a name="generating-job-classes"></a>
### ジョブクラスの生成

デフォルトでは、アプリケーションのキューに入れられるジョブはすべて、`app/Jobs` ディレクトリに保存されます。 `app/Jobs` ディレクトリが存在しない場合は、`make:job` Artisan コマンドを実行すると作成されます。

```shell
php artisan make:job ProcessPodcast
```

生成されたクラスは `Illuminate\Contracts\Queue\ShouldQueue` インターフェイスを実装し、非同期で実行するにはジョブをキューにプッシュする必要があることを Laravel に示します。

> [!NOTE]  
> ジョブ スタブは、[スタブ発行](/docs/{{version}}/artisan#stub-customization) を使用してカスタマイズできます。

<a name="class-structure"></a>
### クラス構造

ジョブ クラスは非常に単純で、通常はジョブがキューによって処理されるときに呼び出される `handle` メソッドのみを含みます。まず、ジョブ クラスの例を見てみましょう。この例では、ポッドキャスト公開サービスを管理しており、アップロードされたポッドキャスト ファイルを公開前に処理する必要があると仮定します。

    <?php

    namespace App\Jobs;

    use App\Models\Podcast;
    use App\Services\AudioProcessor;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Foundation\Queue\Queueable;

    class ProcessPodcast implements ShouldQueue
    {
        use Queueable;

        /**
         * Create a new job instance.
         */
        public function __construct(
            public Podcast $podcast,
        ) {}

        /**
         * Execute the job.
         */
        public function handle(AudioProcessor $processor): void
        {
            // Process uploaded podcast...
        }
    }

この例では、[Eloquent モデル](/docs/{{version}}/eloquent) をキューに入れられたジョブのコンストラクターに直接渡すことができたことに注目してください。ジョブが使用している `Queueable` トレイトにより、Eloquent モデルとそのロードされた関係は、ジョブの処理中に正常にシリアル化およびシリアル化解除されます。

キューに入れられたジョブがコンストラクターで Eloquent モデルを受け入れる場合、モデルの識別子のみがキューにシリアル化されます。ジョブが実際に処理されると、キュー システムは完全なモデル インスタンスとそのロードされた関係をデータベースから自動的に再取得します。モデルのシリアル化に対するこのアプローチにより、はるかに小さいジョブ ペイロードをキュー ドライバに送信できるようになります。

<a name="handle-method-dependency-injection"></a>
#### `handle` メソッドの依存関係の注入

`handle` メソッドは、ジョブがキューによって処理されるときに呼び出されます。ジョブの `handle` メソッドに対する依存関係をタイプヒントできることに注意してください。 Laravel [サービスコンテナ](/docs/{{version}}/container) はこれらの依存関係を自動的に挿入します。

コンテナーが依存関係を `handle` メソッドに挿入する方法を完全に制御したい場合は、コンテナーの `bindMethod` メソッドを使用できます。 `bindMethod` メソッドは、ジョブとコンテナーを受け取るコールバックを受け入れます。コールバック内では、必要に応じて `handle` メソッドを自由に呼び出すことができます。通常、このメソッドは、`App\Providers\AppServiceProvider` [サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッドから呼び出す必要があります。

    use App\Jobs\ProcessPodcast;
    use App\Services\AudioProcessor;
    use Illuminate\Contracts\Foundation\Application;

    $this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
        return $job->handle($app->make(AudioProcessor::class));
    });

> [!WARNING]  
> 未処理の画像コンテンツなどのバイナリ データは、キューに入れられたジョブに渡す前に、`base64_encode` 関数を介して渡す必要があります。そうしないと、ジョブがキューに配置されるときに JSON に適切にシリアル化されない可能性があります。

<a name="handling-relationships"></a>
#### キューに入れられた関係

ジョブがキューに入れられると、ロードされたすべての Eloquent モデルの関係もシリアル化されるため、シリアル化されたジョブ文字列が非常に大きくなる場合があります。さらに、ジョブが逆シリアル化され、モデルの関係がデータベースから再取得されると、それらは完全に取得されます。ジョブキューイング プロセス中にモデルがシリアル化される前に適用された以前の関係制約は、ジョブが逆シリアル化されると適用されません。したがって、特定の関係のサブセットを操作したい場合は、キューに入れられたジョブ内でその関係を再制約する必要があります。

または、リレーションがシリアル化されないようにするには、プロパティ値を設定するときにモデルで `withoutRelations` メソッドを呼び出します。このメソッドは、ロードされた関係を持たないモデルのインスタンスを返します。

    /**
     * Create a new job instance.
     */
    public function __construct(
        Podcast $podcast,
    ) {
        $this->podcast = $podcast->withoutRelations();
    }

PHP コンストラクター プロパティのプロモーションを使用していて、Eloquent モデルのリレーションをシリアル化する必要がないことを示したい場合は、`WithoutRelations` 属性を使用できます。

    use Illuminate\Queue\Attributes\WithoutRelations;

    /**
     * Create a new job instance.
     */
    public function __construct(
        #[WithoutRelations]
        public Podcast $podcast,
    ) {}

ジョブが単一のモデルではなく Eloquent モデルのコレクションまたは配列を受け取った場合、ジョブが逆シリアル化されて実行されたときに、そのコレクション内のモデルの関係は復元されません。これは、多数のモデルを処理するジョブでの過剰なリソースの使用を防ぐためです。

<a name="unique-jobs"></a>
### ユニークなジョブ

> [!WARNING]  
> 固有のジョブには、[locks](/docs/{{version}}/cache#atomic-locks) をサポートするキャッシュ ドライバが必要です。現在、`memcached`、`redis`、`dynamodb`、`database`、`file`、および `array` キャッシュ ドライバはアトミック ロックをサポートしています。さらに、固有のジョブ制約はバッチ内のジョブには適用されません。

場合によっては、特定のジョブのインスタンスが常に 1 つだけキューに存在するようにしたい場合があります。これを行うには、ジョブ クラスに `ShouldBeUnique` インターフェイスを実装します。このインターフェイスでは、クラスに追加のメソッドを定義する必要はありません。

    <?php

    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Contracts\Queue\ShouldBeUnique;

    class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
    {
        ...
    }

上の例では、`UpdateSearchIndex` ジョブは一意です。したがって、ジョブの別のインスタンスがすでにキュー上にあり、処理が完了していない場合、ジョブはディスパッチされません。

場合によっては、ジョブを一意にする特定の「キー」を定義したり、ジョブが一意でなくなるタイムアウトを指定したりすることができます。これを実現するには、ジョブ クラスで `uniqueId` および `uniqueFor` プロパティまたはメソッドを定義します。

    <?php

    use App\Models\Product;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Contracts\Queue\ShouldBeUnique;

    class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
    {
        /**
         * The product instance.
         *
         * @var \App\Product
         */
        public $product;

        /**
         * The number of seconds after which the job's unique lock will be released.
         *
         * @var int
         */
        public $uniqueFor = 3600;

        /**
         * Get the unique ID for the job.
         */
        public function uniqueId(): string
        {
            return $this->product->id;
        }
    }

上の例では、`UpdateSearchIndex` ジョブは製品 ID によって一意です。したがって、同じ製品 ID を持つジョブの新しいディスパッチは、既存のジョブの処理が完了するまで無視されます。さらに、既存のジョブが 1 時間以内に処理されない場合、一意のロックが解除され、同じ一意のキーを持つ別のジョブがキューにディスパッチされる可能性があります。

> [!WARNING]  
> アプリケーションが複数の Web サーバーまたはコンテナーからジョブをディスパッチする場合は、Laravel がジョブが一意であるかどうかを正確に判断できるように、すべてのサーバーが同じ中央キャッシュ サーバーと通信していることを確認する必要があります。

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 処理が開始されるまでジョブを固有に保つ

デフォルトでは、ジョブが処理を完了するか、すべての再試行に失敗すると、固有のジョブは「ロック解除」されます。ただし、ジョブが処理される直前にロックを解除したい場合もあります。これを実現するには、ジョブで `ShouldBeUnique` コントラクトの代わりに `ShouldBeUniqueUntilProcessing` コントラクトを実装する必要があります。

    <?php

    use App\Models\Product;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

    class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
    {
        // ...
    }

<a name="unique-job-locks"></a>
#### ユニークなジョブロック

バックグラウンドでは、`ShouldBeUnique` ジョブがディスパッチされると、Laravel は `uniqueId` キーを使用して [lock](/docs/{{version}}/cache#atomic-locks) を取得しようとします。ロックが取得されない場合、ジョブはディスパッチされません。このロックは、ジョブの処理が完了するか、すべての再試行が失敗すると解放されます。デフォルトでは、Laravel はデフォルトのキャッシュドライバを使用してこのロックを取得します。ただし、ロックの取得に別のドライバを使用したい場合は、使用するキャッシュ ドライバを返す `uniqueVia` メソッドを定義できます。

    use Illuminate\Contracts\Cache\Repository;
    use Illuminate\Support\Facades\Cache;

    class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
    {
        ...

        /**
         * Get the cache driver for the unique job lock.
         */
        public function uniqueVia(): Repository
        {
            return Cache::driver('redis');
        }
    }

> [!NOTE]  
> ジョブの同時処理を制限する必要があるだけの場合は、代わりに [`WithoutOverlapping`](/docs/{{version}}/queues#preventing-job-overlaps) ジョブ ミドルウェアを使用してください。

<a name="encrypted-jobs"></a>
### 暗号化されたジョブ

Laravel を使用すると、[encryption](/docs/{{version}}/encryption) 経由でジョブのデータのプライバシーと整合性を確保できます。開始するには、`ShouldBeEncrypted` インターフェイスをジョブ クラスに追加するだけです。このインターフェースがクラスに追加されると、Laravel はジョブをキューにプッシュする前に自動的に暗号化します。

    <?php

    use Illuminate\Contracts\Queue\ShouldBeEncrypted;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class UpdateSearchIndex implements ShouldQueue, ShouldBeEncrypted
    {
        // ...
    }

<a name="job-middleware"></a>
## ジョブミドルウェア (Job Middleware)

ジョブ ミドルウェアを使用すると、キューに入れられたジョブの実行にカスタム ロジックをラップして、ジョブ自体の定型文を減らすことができます。たとえば、Laravel の Redis レート制限機能を活用して、5 秒ごとに 1 つのジョブのみの処理を許可する次の `handle` メソッドを考えてみましょう。

    use Illuminate\Support\Facades\Redis;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
            info('Lock obtained...');

            // Handle job...
        }, function () {
            // Could not obtain lock...

            return $this->release(5);
        });
    }

このコードは有効ですが、`handle` メソッドの実装には Redis レート制限ロジックが混在しているため、ノイズが多くなります。さらに、このレート制限ロジックは、レート制限したい他のジョブに対しても複製する必要があります。

handle メソッドでレート制限を行う代わりに、レート制限を処理するジョブ ミドルウェアを定義できます。 Laravel にはジョブミドルウェアのデフォルトの場所がないため、アプリケーション内のどこにでもジョブミドルウェアを配置できます。この例では、ミドルウェアを `app/Jobs/Middleware` ディレクトリに配置します。

    <?php

    namespace App\Jobs\Middleware;

    use Closure;
    use Illuminate\Support\Facades\Redis;

    class RateLimited
    {
        /**
         * Process the queued job.
         *
         * @param  \Closure(object): void  $next
         */
        public function handle(object $job, Closure $next): void
        {
            Redis::throttle('key')
                ->block(0)->allow(1)->every(5)
                ->then(function () use ($job, $next) {
                    // Lock obtained...
    
                    $next($job);
                }, function () use ($job) {
                    // Could not obtain lock...
    
                    $job->release(5);
                });
        }
    }

ご覧のとおり、[ルートミドルウェア](/docs/{{version}}/middleware) のように、ジョブ ミドルウェアは、処理中のジョブと、ジョブの処理を続行するために呼び出されるコールバックを受け取ります。

ジョブ ミドルウェアを作成した後、ジョブの `middleware` メソッドからそれらを返すことによって、ジョブ ミドルウェアをジョブにアタッチできます。このメソッドは、`make:job` Artisan コマンドによってスキャフォールディングされたジョブには存在しないため、ジョブ クラスに手動で追加する必要があります。

    use App\Jobs\Middleware\RateLimited;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [new RateLimited];
    }

> [!NOTE]  
> ジョブ ミドルウェアは、キュー可能なイベント リスナ、メール可能ファイル、および通知に割り当てることもできます。

<a name="rate-limiting"></a>
### レート制限

独自のレート制限ジョブ ミドルウェアを作成する方法を説明しましたが、実際には、Laravel にはジョブのレート制限に利用できるレート制限ミドルウェアが含まれています。 [ルートレートリミッター](/docs/{{version}}/routing#defining-rate-limiters) と同様に、ジョブ レート リミッターは、`RateLimiter` ファサードの `for` メソッドを使用して定義されます。

たとえば、プレミアム顧客にはそのような制限を課さず、ユーザーが 1 時間に 1 回データをバックアップできるようにしたい場合があります。これを実現するには、`AppServiceProvider` の `boot` メソッドで `RateLimiter` を定義できます。

    use Illuminate\Cache\RateLimiting\Limit;
    use Illuminate\Support\Facades\RateLimiter;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        RateLimiter::for('backups', function (object $job) {
            return $job->user->vipCustomer()
                ? Limit::none()
                : Limit::perHour(1)->by($job->user->id);
        });
    }

上の例では、時間当たりのレート制限を定義しました。ただし、`perMinute` メソッドを使用すると、分に基づいてレート制限を簡単に定義できます。さらに、レート制限の `by` メソッドに任意の値を渡すことができます。ただし、この値は、顧客ごとにレート制限を分割するために最もよく使用されます。

    return Limit::perMinute(50)->by($job->user->id);

レート制限を定義したら、`Illuminate\Queue\Middleware\RateLimited` ミドルウェアを使用してジョブにレート制限を適用できます。ジョブがレート制限を超えるたびに、このミドルウェアはレート制限の期間に基づいて適切な遅延を設けてジョブをキューに戻します。

    use Illuminate\Queue\Middleware\RateLimited;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [new RateLimited('backups')];
    }

レート制限されたジョブをキューに解放しても、ジョブの合計数 `attempts` は増加します。それに応じて、ジョブ クラスの `tries` プロパティと `maxExceptions` プロパティを調整することもできます。または、[`retryUntil`メソッド](#time-based-attempts) を使用して、ジョブが試行されなくなるまでの時間を定義することもできます。

レートが制限されているときにジョブを再試行したくない場合は、`dontRelease` メソッドを使用できます。

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new RateLimited('backups'))->dontRelease()];
    }

> [!NOTE]  
> Redis を使用している場合は、`Illuminate\Queue\Middleware\RateLimitedWithRedis` ミドルウェアを使用できます。これは Redis 用に微調整されており、基本的なレート制限ミドルウェアよりも効率的です。

<a name="preventing-job-overlaps"></a>
### ジョブの重複を防ぐ

Laravel には、任意のキーに基づいてジョブの重複を防止できる `Illuminate\Queue\Middleware\WithoutOverlapping` ミドルウェアが含まれています。これは、キューに入れられたジョブが、一度に 1 つのジョブのみによって変更されるべきリソースを変更する場合に役立ちます。

たとえば、ユーザーのクレジット スコアを更新するキューに入れられたジョブがあり、同じユーザー ID に対してクレジット スコア更新ジョブが重複しないようにしたいとします。これを実現するには、ジョブの `middleware` メソッドから `WithoutOverlapping` ミドルウェアを返すことができます。

    use Illuminate\Queue\Middleware\WithoutOverlapping;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [new WithoutOverlapping($this->user->id)];
    }

同じタイプの重複するジョブはキューに戻されます。解放されたジョブが再試行されるまでに経過する必要がある秒数を指定することもできます。

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
    }

再試行されないように重複するジョブをすぐに削除したい場合は、`dontRelease` メソッドを使用できます。

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new WithoutOverlapping($this->order->id))->dontRelease()];
    }

`WithoutOverlapping` ミドルウェアは、Laravel のアトミック ロック機能を利用しています。場合によっては、ロックが解放されずにジョブが予期せず失敗したり、タイムアウトになったりすることがあります。したがって、`expireAfter` メソッドを使用して、ロックの有効期限を明示的に定義できます。たとえば、以下の例は、ジョブの処理が開始されてから 3 分後に `WithoutOverlapping` ロックを解放するように Laravel に指示します。

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
    }

> [!WARNING]  
> `WithoutOverlapping` ミドルウェアには、[locks](/docs/{{version}}/cache#atomic-locks) をサポートするキャッシュ ドライバが必要です。現在、`memcached`、`redis`、`dynamodb`、`database`、`file`、および `array` キャッシュ ドライバはアトミック ロックをサポートしています。

<a name="sharing-lock-keys"></a>
#### ジョブクラス間でのロックキーの共有

デフォルトでは、`WithoutOverlapping` ミドルウェアは、同じクラスの重複ジョブのみを防止します。したがって、2 つの異なるジョブ クラスが同じロック キーを使用することはできますが、それらの重複は防止されません。ただし、`shared` メソッドを使用して、ジョブ クラス全体にキーを適用するように Laravel に指示できます。

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```

<a name="throttling-exceptions"></a>
### スロットリング例外

Laravel には、例外を抑制できる `Illuminate\Queue\Middleware\ThrottlesExceptions` ミドルウェアが含まれています。ジョブが指定された数の例外をスローすると、それ以降のジョブの実行試行は、指定された時間が経過するまで遅延されます。このミドルウェアは、不安定なサードパーティ サービスと対話するジョブに特に役立ちます。

たとえば、例外をスローし始めるサードパーティ API と対話する、キューに入れられたジョブを想像してみましょう。例外を抑制するには、ジョブの `middleware` メソッドから `ThrottlesExceptions` ミドルウェアを返すことができます。通常、このミドルウェアは、[時間ベースの試行](#time-based-attempts) を実装するジョブと組み合わせる必要があります。

    use DateTime;
    use Illuminate\Queue\Middleware\ThrottlesExceptions;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [new ThrottlesExceptions(10, 5 * 60)];
    }

    /**
     * Determine the time at which the job should timeout.
     */
    public function retryUntil(): DateTime
    {
        return now()->addMinutes(30);
    }

ミドルウェアによって受け入れられる最初のコンストラクター引数は、ジョブが調整される前にスローできる例外の数です。一方、2 番目のコンストラクター引数は、ジョブが調整された後にジョブが再試行されるまでに経過する必要がある秒数です。上記のコード例では、ジョブが 10 回連続して例外をスローした場合、30 分の時間制限による制約を受けて、5 分間待ってからジョブを再試行します。

ジョブが例外をスローしたが、まだ例外しきい値に達していない場合、ジョブは通常、すぐに再試行されます。ただし、ミドルウェアをジョブにアタッチするときに `backoff` メソッドを呼び出すことで、そのようなジョブを遅延させる分数を指定できます。

    use Illuminate\Queue\Middleware\ThrottlesExceptions;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
    }

内部的には、このミドルウェアは Laravel のキャッシュ システムを使用してレート制限を実装し、ジョブのクラス名がキャッシュの「キー」として利用されます。ミドルウェアをジョブにアタッチするときに `by` メソッドを呼び出すことで、このキーをオーバーライドできます。これは、同じサードパーティ サービスと対話する複数のジョブがあり、それらのジョブに共通の調整「バケット」を共有したい場合に便利です。

    use Illuminate\Queue\Middleware\ThrottlesExceptions;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
    }

デフォルトでは、このミドルウェアはすべての例外を抑制します。この動作は、ミドルウェアをジョブにアタッチするときに `when` メソッドを呼び出すことで変更できます。例外は、`when` メソッドに提供されたクロージャが `true` を返した場合にのみスロットリングされます。

    use Illuminate\Http\Client\HttpClientException;
    use Illuminate\Queue\Middleware\ThrottlesExceptions;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new ThrottlesExceptions(10, 10 * 60))->when(
            fn (Throwable $throwable) => $throwable instanceof HttpClientException
        )];
    }

調整された例外をアプリケーションの例外ハンドラーに報告したい場合は、ミドルウェアをジョブにアタッチするときに `report` メソッドを呼び出すことで実行できます。オプションで、`report` メソッドにクロージャを提供すると、指定されたクロージャが `true` を返した場合にのみ例外が報告されます。

    use Illuminate\Http\Client\HttpClientException;
    use Illuminate\Queue\Middleware\ThrottlesExceptions;

    /**
     * Get the middleware the job should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [(new ThrottlesExceptions(10, 10 * 60))->report(
            fn (Throwable $throwable) => $throwable instanceof HttpClientException
        )];
    }

> [!NOTE]  
> Redis を使用している場合は、`Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` ミドルウェアを使用できます。これは Redis 用に微調整されており、基本的な例外調整ミドルウェアよりも効率的です。

<a name="skipping-jobs"></a>
### ジョブのスキップ

`Skip` ミドルウェアを使用すると、ジョブのロジックを変更することなく、ジョブをスキップ/削除するように指定できます。 `Skip::when` メソッドは、指定された条件が `true` と評価される場合にジョブを削除します。一方、`Skip::unless` メソッドは、条件が `false` と評価される場合にジョブを削除します。

    use Illuminate\Queue\Middleware\Skip;

    /**
    * ジョブが通過するミドルウェアを取得します。
    */
    public function middleware(): array
    {
        return [
            Skip::when($someCondition),
        ];
    }

より複雑な条件評価のために、`Closure` を `when` メソッドと `unless` メソッドに渡すこともできます。

    use Illuminate\Queue\Middleware\Skip;

    /**
    * ジョブが通過するミドルウェアを取得します。
    */
    public function middleware(): array
    {
        return [
            Skip::when(function (): bool {
                return $this->shouldSkip();
            }),
        ];
    }

<a name="dispatching-jobs"></a>
## 仕事の派遣 (Dispatching Jobs)

ジョブ クラスを作成したら、ジョブ自体で `dispatch` メソッドを使用してジョブ クラスをディスパッチできます。 `dispatch` メソッドに渡される引数は、ジョブのコンストラクターに渡されます。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Jobs\ProcessPodcast;
    use App\Models\Podcast;
    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class PodcastController extends Controller
    {
        /**
         * Store a new podcast.
         */
        public function store(Request $request): RedirectResponse
        {
            $podcast = Podcast::create(/* ... */);

            // ...

            ProcessPodcast::dispatch($podcast);

            return redirect('/podcasts');
        }
    }

条件付きでジョブをディスパッチしたい場合は、`dispatchIf` メソッドと `dispatchUnless` メソッドを使用できます。

    ProcessPodcast::dispatchIf($accountActive, $podcast);

    ProcessPodcast::dispatchUnless($accountSuspended, $podcast);

新しい Laravel アプリケーションでは、`sync` ドライバがデフォルトのキュードライバです。このドライバは、現在のリクエストのフォアグラウンドでジョブを同期的に実行します。これは、ローカル開発中に便利なことがよくあります。実際にバックグラウンド処理のためにジョブのキューイングを開始したい場合は、アプリケーションの `config/queue.php` 構成ファイル内で別のキュー ドライバを指定できます。

<a name="delayed-dispatching"></a>
### 派遣の遅れ

ジョブをキューワーカーによる処理にすぐに使用できないように指定したい場合は、ジョブをディスパッチするときに `delay` メソッドを使用できます。たとえば、ジョブがディスパッチされてから 10 分が経過するまではジョブを処理できないように指定しましょう。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Jobs\ProcessPodcast;
    use App\Models\Podcast;
    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class PodcastController extends Controller
    {
        /**
         * Store a new podcast.
         */
        public function store(Request $request): RedirectResponse
        {
            $podcast = Podcast::create(/* ... */);

            // ...

            ProcessPodcast::dispatch($podcast)
                ->delay(now()->addMinutes(10));

            return redirect('/podcasts');
        }
    }

場合によっては、ジョブにデフォルトの遅延が設定されている場合があります。この遅延を回避し、即時に処理するためにジョブをディスパッチする必要がある場合は、`withoutDelay` メソッドを使用できます。

    ProcessPodcast::dispatch($podcast)->withoutDelay();

> [!WARNING]  
> Amazon SQS キュー サービスの最大遅延時間は 15 分です。

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 応答がブラウザに送信された後のディスパッチ

あるいは、Web サーバーが FastCGI を使用している場合、`dispatchAfterResponse` メソッドは、HTTP 応答がユーザーのブラウザーに送信されるまでジョブのディスパッチを遅らせます。これにより、キューに入れられたジョブがまだ実行中であっても、ユーザーはアプリケーションの使用を開始できます。これは通常、電子メールの送信など、約 1 秒かかるジョブにのみ使用してください。これらは現在の HTTP リクエスト内で処理されるため、この方法でディスパッチされたジョブは、処理するためにキューワーカーを実行する必要はありません。

    use App\Jobs\SendNotification;

    SendNotification::dispatchAfterResponse();

また、`dispatch` クロージャーを作成し、`afterResponse` メソッドを `dispatch` ヘルパにチェーンして、HTTP 応答がブラウザーに送信された後にクロージャーを実行することもできます。

    use App\Mail\WelcomeMessage;
    use Illuminate\Support\Facades\Mail;

    dispatch(function () {
        Mail::to('taylor@example.com')->send(new WelcomeMessage);
    })->afterResponse();

<a name="synchronous-dispatching"></a>
### 同期ディスパッチング

ジョブをすぐに (同期的に) ディスパッチしたい場合は、`dispatchSync` メソッドを使用できます。この方法を使用すると、ジョブはキューに入れられず、現在のプロセス内ですぐに実行されます。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Jobs\ProcessPodcast;
    use App\Models\Podcast;
    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class PodcastController extends Controller
    {
        /**
         * Store a new podcast.
         */
        public function store(Request $request): RedirectResponse
        {
            $podcast = Podcast::create(/* ... */);

            // Create podcast...

            ProcessPodcast::dispatchSync($podcast);

            return redirect('/podcasts');
        }
    }

<a name="jobs-and-database-transactions"></a>
### ジョブとデータベーストランザクション

データベース トランザクション内でジョブをディスパッチすることはまったく問題ありませんが、ジョブが実際に正常に実行できることを確認するために特別な注意を払う必要があります。トランザクション内でジョブをディスパッチする場合、親トランザクションがコミットされる前にジョブがワーカーによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに加えた更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。

ありがたいことに、Laravel はこの問題を回避する方法をいくつか提供しています。まず、キュー接続の構成配列で `after_commit` 接続オプションを設定します。

    'redis' => [
        'driver' => 'redis',
        // ...
        'after_commit' => true,
    ],

`after_commit` オプションが `true` の場合、データベース トランザクション内でジョブをディスパッチできます。ただし、Laravel は、実際にジョブをディスパッチする前に、開いている親データベースのトランザクションがコミットされるまで待機します。もちろん、現在開いているデータベース トランザクションがない場合、ジョブはすぐにディスパッチされます。

トランザクション中に発生した例外によりトランザクションがロールバックされた場合、そのトランザクション中にディスパッチされたジョブは破棄されます。

> [!NOTE]  
> `after_commit` 構成オプションを `true` に設定すると、開いているすべてのデータベース トランザクションがコミットされた後に、キューに入れられたイベント リスナ、メール可能ファイル、通知、およびブロードキャスト イベントもディスパッチされます。

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### インラインでのコミット・ディスパッチ動作の指定

`after_commit` キュー接続構成オプションを `true` に設定しない場合でも、開いているすべてのデータベース トランザクションがコミットされた後に特定のジョブをディスパッチする必要があることを示すことができます。これを実現するには、`afterCommit` メソッドをディスパッチ操作に連鎖させます。

    use App\Jobs\ProcessPodcast;

    ProcessPodcast::dispatch($podcast)->afterCommit();

同様に、`after_commit` 構成オプションが `true` に設定されている場合は、開いているデータベース トランザクションがコミットされるのを待たずに、特定のジョブを直ちにディスパッチする必要があることを指定できます。

    ProcessPodcast::dispatch($podcast)->beforeCommit();

<a name="job-chaining"></a>
### ジョブチェーン

ジョブ チェーンを使用すると、プライマリ ジョブが正常に実行された後に順番に実行する必要がある、キューに入れられたジョブのリストを指定できます。シーケンス内の 1 つのジョブが失敗すると、残りのジョブは実行されません。キューに入れられたジョブ チェーンを実行するには、`Bus` ファサードによって提供される `chain` メソッドを使用できます。 Laravel のコマンド バスは、キューに入れられたジョブのディスパッチがその上に構築される下位レベルのコンポーネントです。

    use App\Jobs\OptimizePodcast;
    use App\Jobs\ProcessPodcast;
    use App\Jobs\ReleasePodcast;
    use Illuminate\Support\Facades\Bus;

    Bus::chain([
        new ProcessPodcast,
        new OptimizePodcast,
        new ReleasePodcast,
    ])->dispatch();

ジョブ クラス インスタンスをチェーンすることに加えて、クロージャをチェーンすることもできます。

    Bus::chain([
        new ProcessPodcast,
        new OptimizePodcast,
        function () {
            Podcast::update(/* ... */);
        },
    ])->dispatch();

> [!WARNING]  
> ジョブ内で `$this->delete()` メソッドを使用してジョブを削除しても、チェーンされたジョブの処理は妨げられません。チェーンは、チェーン内のジョブが失敗した場合にのみ実行を停止します。

<a name="chain-connection-queue"></a>
#### チェーン接続とキュー

連鎖ジョブに使用する接続とキューを指定したい場合は、`onConnection` メソッドと `onQueue` メソッドを使用できます。これらのメソッドは、キューに入れられたジョブに別の接続/キューが明示的に割り当てられていない限り、使用する必要があるキュー接続とキュー名を指定します。

    Bus::chain([
        new ProcessPodcast,
        new OptimizePodcast,
        new ReleasePodcast,
    ])->onConnection('redis')->onQueue('podcasts')->dispatch();

<a name="adding-jobs-to-the-chain"></a>
#### チェーンへのジョブの追加

場合によっては、既存のジョブ チェーンに、そのチェーン内の別のジョブ内からジョブを追加または追加する必要が生じることがあります。これは、`prependToChain` メソッドと `appendToChain` メソッドを使用して実行できます。

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    // Prepend to the current chain, run job immediately after current job...
    $this->prependToChain(new TranscribePodcast);

    // Append to the current chain, run job at end of chain...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 連鎖障害

ジョブをチェーンする場合、`catch` メソッドを使用して、チェーン内のジョブが失敗した場合に呼び出されるクロージャーを指定できます。指定されたコールバックは、ジョブの失敗の原因となった `Throwable` インスタンスを受け取ります。

    use Illuminate\Support\Facades\Bus;
    use Throwable;

    Bus::chain([
        new ProcessPodcast,
        new OptimizePodcast,
        new ReleasePodcast,
    ])->catch(function (Throwable $e) {
        // A job within the chain has failed...
    })->dispatch();

> [!WARNING]  
> チェーン コールバックはシリアル化され、後で Laravel キューによって実行されるため、チェーン コールバック内で `$this` 変数を使用しないでください。

<a name="customizing-the-queue-and-connection"></a>
### キューと接続のカスタマイズ

<a name="dispatching-to-a-particular-queue"></a>
#### 特定のキューへのディスパッチ

ジョブを異なるキューにプッシュすることで、キューに入れられたジョブを「分類」し、さまざまなキューに割り当てるワーカーの数に優先順位を付けることもできます。これは、キュー構成ファイルで定義されている別のキュー「接続」にジョブをプッシュするのではなく、単一の接続内の特定のキューにのみジョブをプッシュすることに注意してください。キューを指定するには、ジョブをディスパッチするときに `onQueue` メソッドを使用します。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Jobs\ProcessPodcast;
    use App\Models\Podcast;
    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class PodcastController extends Controller
    {
        /**
         * Store a new podcast.
         */
        public function store(Request $request): RedirectResponse
        {
            $podcast = Podcast::create(/* ... */);

            // Create podcast...

            ProcessPodcast::dispatch($podcast)->onQueue('processing');

            return redirect('/podcasts');
        }
    }

あるいは、ジョブのコンストラクター内で `onQueue` メソッドを呼び出して、ジョブのキューを指定することもできます。

    <?php

    namespace App\Jobs;

     use Illuminate\Contracts\Queue\ShouldQueue;
     use Illuminate\Foundation\Queue\Queueable;

    class ProcessPodcast implements ShouldQueue
    {
        use Queueable;

        /**
         * Create a new job instance.
         */
        public function __construct()
        {
            $this->onQueue('processing');
        }
    }

<a name="dispatching-to-a-particular-connection"></a>
#### 特定の接続へのディスパッチ

アプリケーションが複数のキュー接続と対話する場合は、`onConnection` メソッドを使用してジョブをプッシュする接続を指定できます。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Jobs\ProcessPodcast;
    use App\Models\Podcast;
    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class PodcastController extends Controller
    {
        /**
         * Store a new podcast.
         */
        public function store(Request $request): RedirectResponse
        {
            $podcast = Podcast::create(/* ... */);

            // Create podcast...

            ProcessPodcast::dispatch($podcast)->onConnection('sqs');

            return redirect('/podcasts');
        }
    }

`onConnection` メソッドと `onQueue` メソッドを連鎖させて、ジョブの接続とキューを指定できます。

    ProcessPodcast::dispatch($podcast)
        ->onConnection('sqs')
        ->onQueue('processing');

あるいは、ジョブのコンストラクター内で `onConnection` メソッドを呼び出して、ジョブの接続を指定することもできます。

    <?php

    namespace App\Jobs;

     use Illuminate\Contracts\Queue\ShouldQueue;
     use Illuminate\Foundation\Queue\Queueable;

    class ProcessPodcast implements ShouldQueue
    {
        use Queueable;

        /**
         * Create a new job instance.
         */
        public function __construct()
        {
            $this->onConnection('sqs');
        }
    }

<a name="max-job-attempts-and-timeout"></a>
### 最大ジョブ試行数/タイムアウト値の指定

<a name="max-attempts"></a>
#### 最大試行回数

キューに入れられたジョブの 1 つでエラーが発生した場合、そのジョブが無期限に再試行され続けることは望ましくありません。したがって、Laravel では、ジョブを試行する回数や期間を指定するさまざまな方法が提供されています。

ジョブの最大試行回数を指定する方法の 1 つは、Artisan コマンド ラインの `--tries` スイッチを使用することです。これは、処理中のジョブで試行回数が指定されていない限り、ワーカーによって処理されるすべてのジョブに適用されます。

```shell
php artisan queue:work --tries=3
```

ジョブが最大試行回数を超えた場合、そのジョブは「失敗した」ジョブとみなされます。失敗したジョブの処理の詳細については、[失敗したジョブの文書化](#dealing-with-failed-jobs) を参照してください。 `--tries=0` が `queue:work` コマンドに指定された場合、ジョブは無期限に再試行されます。

ジョブ クラス自体でジョブを試行できる最大回数を定義することで、より詳細なアプローチを採用することもできます。ジョブで最大試行回数が指定されている場合は、コマンド ラインで指定した `--tries` 値よりも優先されます。

    <?php

    namespace App\Jobs;

    class ProcessPodcast implements ShouldQueue
    {
        /**
         * The number of times the job may be attempted.
         *
         * @var int
         */
        public $tries = 5;
    }

特定のジョブの最大試行回数を動的に制御する必要がある場合は、ジョブに `tries` メソッドを定義できます。

    /**
     * Determine number of times the job may be attempted.
     */
    public function tries(): int
    {
        return 5;
    }

<a name="time-based-attempts"></a>
#### 時間ベースの試行

ジョブが失敗するまでに何回試行できるかを定義する代わりに、ジョブを試行しなくなる時間を定義することもできます。これにより、指定された時間枠内でジョブを何度でも試行できます。ジョブを試行しなくなる時刻を定義するには、`retryUntil` メソッドをジョブ クラスに追加します。このメソッドは `DateTime` インスタンスを返す必要があります。

    use DateTime;

    /**
     * Determine the time at which the job should timeout.
     */
    public function retryUntil(): DateTime
    {
        return now()->addMinutes(10);
    }

> [!NOTE]  
> [キューに入れられたイベントリスナ](/docs/{{version}}/events#queued-event-listeners) で `tries` プロパティまたは `retryUntil` メソッドを定義することもできます。

<a name="max-exceptions"></a>
#### 最大例外数

場合によっては、ジョブを何度も試行できるが、(`release` メソッドによって直接解放されるのではなく) 指定された数の未処理の例外によって再試行がトリガーされた場合は失敗するように指定したい場合があります。これを実現するには、ジョブ クラスで `maxExceptions` プロパティを定義します。

    <?php

    namespace App\Jobs;

    use Illuminate\Support\Facades\Redis;

    class ProcessPodcast implements ShouldQueue
    {
        /**
         * The number of times the job may be attempted.
         *
         * @var int
         */
        public $tries = 25;

        /**
         * The maximum number of unhandled exceptions to allow before failing.
         *
         * @var int
         */
        public $maxExceptions = 3;

        /**
         * Execute the job.
         */
        public function handle(): void
        {
            Redis::throttle('key')->allow(10)->every(60)->then(function () {
                // Lock obtained, process the podcast...
            }, function () {
                // Unable to obtain lock...
                return $this->release(10);
            });
        }
    }

この例では、アプリケーションが Redis ロックを取得できない場合、ジョブは 10 秒間解放され、最大 25 回まで再試行され続けます。ただし、ジョブによって 3 つの未処理の例外がスローされた場合、ジョブは失敗します。

<a name="timeout"></a>
#### タイムアウト

多くの場合、キューに入れられたジョブにかかる時間がおおよそわかっています。このため、Laravel では「タイムアウト」値を指定できます。デフォルトでは、タイムアウト値は 60 秒です。ジョブの処理がタイムアウト値で指定された秒数を超えた場合、ジョブを処理しているワーカーはエラーで終了します。通常、ワーカーは [サーバー上に設定されたプロセスマネージャー](#supervisor-configuration) によって自動的に再起動されます。

ジョブを実行できる最大秒数は、Artisan コマンド ラインで `--timeout` スイッチを使用して指定できます。

```shell
php artisan queue:work --timeout=30
```

ジョブがタイムアウトを繰り返して最大試行回数を超えると、ジョブは失敗としてマークされます。

ジョブ クラス自体でジョブの実行を許可する最大秒数を定義することもできます。ジョブでタイムアウトが指定されている場合は、コマンド ラインで指定されたタイムアウトよりも優先されます。

    <?php

    namespace App\Jobs;

    class ProcessPodcast implements ShouldQueue
    {
        /**
         * The number of seconds the job can run before timing out.
         *
         * @var int
         */
        public $timeout = 120;
    }

場合によっては、ソケットや発信 HTTP 接続などの IO ブロック プロセスが、指定されたタイムアウトを尊重しないことがあります。したがって、これらの機能を使用するときは、常にその API も使用してタイムアウトを指定するようにしてください。たとえば、Guzzle を使用する場合は、常に接続とリクエストのタイムアウト値を指定する必要があります。

> [!WARNING]  
> ジョブのタイムアウトを指定するには、`pcntl` PHP 拡張機能をインストールする必要があります。さらに、ジョブの「タイムアウト」値は常に [「後で再試行してください」](#job-expiration) 値よりも小さい必要があります。そうしないと、ジョブが実際に実行を終了するかタイムアウトになる前に再試行される可能性があります。

<a name="failing-on-timeout"></a>
#### タイムアウトで失敗する

タイムアウト時にジョブを [failed](#dealing-with-failed-jobs) としてマークする必要があることを示したい場合は、ジョブ クラスで `$failOnTimeout` プロパティを定義できます。

```php
/**
 * Indicate if the job should be marked as failed on timeout.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### エラー処理

ジョブの処理中に例外がスローされた場合、ジョブは自動的にキューに解放され、再試行できるようになります。ジョブは、アプリケーションで許可されている最大回数試行されるまで解放され続けます。最大試行回数は、`queue:work` Artisan コマンドで使用される `--tries` スイッチによって定義されます。あるいは、最大試行回数をジョブ クラス自体に定義することもできます。キューワーカー [以下で見つけることができます](#running-the-queue-worker) の実行に関する詳細情報。

<a name="manually-releasing-a-job"></a>
#### ジョブを手動でリリースする

場合によっては、ジョブを手動で解放してキューに戻し、後で再試行できるようにしたい場合があります。これを行うには、`release` メソッドを呼び出します。

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        // ...

        $this->release();
    }

デフォルトでは、`release` メソッドはジョブをキューに解放して即時処理します。ただし、整数または日付インスタンスを `release` メソッドに渡すことで、指定した秒数が経過するまでジョブを処理できないようにキューに指示できます。

    $this->release(10);

    $this->release(now()->addSeconds(10));

<a name="manually-failing-a-job"></a>
#### ジョブを手動で失敗する

場合によっては、ジョブを手動で「失敗」としてマークする必要がある場合があります。これを行うには、`fail` メソッドを呼び出します。

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        // ...

        $this->fail();
    }

キャッチした例外のためにジョブを失敗としてマークしたい場合は、例外を `fail` メソッドに渡すことができます。または、便宜上、例外に変換される文字列エラー メッセージを渡すこともできます。

    $this->fail($exception);

    $this->fail('Something went wrong.');

> [!NOTE]  
> 失敗したジョブの詳細については、[ジョブの失敗への対処に関するドキュメント](#dealing-with-failed-jobs) を確認してください。

<a name="job-batching"></a>
## ジョブのバッチ処理 (Job Batching)

Laravel のジョブバッチ機能を使用すると、ジョブのバッチを簡単に実行し、ジョブのバッチの実行が完了したときに何らかのアクションを実行できます。開始する前に、データベース移行を作成して、完了率などのジョブ バッチに関するメタ情報を含むテーブルを構築する必要があります。この移行は、`make:queue-batches-table` Artisan コマンドを使用して生成できます。

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### バッチ可能ジョブの定義

バッチ可能ジョブを定義するには、通常どおり [キュー可能なジョブを作成する](#creating-jobs) を実行する必要があります。ただし、ジョブ クラスに `Illuminate\Bus\Batchable` 特性を追加する必要があります。この特性は、ジョブが実行されている現在のバッチを取得するために使用できる `batch` メソッドへのアクセスを提供します。

    <?php

    namespace App\Jobs;

    use Illuminate\Bus\Batchable;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Foundation\Queue\Queueable;

    class ImportCsv implements ShouldQueue
    {
        use Batchable, Queueable;

        /**
         * Execute the job.
         */
        public function handle(): void
        {
            if ($this->batch()->cancelled()) {
                // Determine if the batch has been cancelled...

                return;
            }

            // Import a portion of the CSV file...
        }
    }

<a name="dispatching-batches"></a>
### バッチの発送

ジョブのバッチをディスパッチするには、`Bus` ファサードの `batch` メソッドを使用する必要があります。もちろん、バッチ処理は主に完了コールバックと組み合わせると便利です。したがって、`then`、`catch`、および `finally` メソッドを使用して、バッチの完了コールバックを定義できます。これらの各コールバックは、呼び出されるときに `Illuminate\Bus\Batch` インスタンスを受け取ります。この例では、CSV ファイルの指定された行数をそれぞれ処理するジョブのバッチをキューに入れていると想定します。

    use App\Jobs\ImportCsv;
    use Illuminate\Bus\Batch;
    use Illuminate\Support\Facades\Bus;
    use Throwable;

    $batch = Bus::batch([
        new ImportCsv(1, 100),
        new ImportCsv(101, 200),
        new ImportCsv(201, 300),
        new ImportCsv(301, 400),
        new ImportCsv(401, 500),
    ])->before(function (Batch $batch) {
        // The batch has been created but no jobs have been added...
    })->progress(function (Batch $batch) {
        // A single job has completed successfully...
    })->then(function (Batch $batch) {
        // All jobs completed successfully...
    })->catch(function (Batch $batch, Throwable $e) {
        // First batch job failure detected...
    })->finally(function (Batch $batch) {
        // The batch has finished executing...
    })->dispatch();

    return $batch->id;

`$batch->id` プロパティを介してアクセスできるバッチの ID は、発送後のバッチに関する情報を得るために [Laravelコマンドバスをクエリする](#inspecting-batches) に使用できます。

> [!WARNING]  
> バッチコールバックはシリアル化され、後でLaravelキューによって実行されるため、コールバック内で`$this`変数を使用しないでください。さらに、バッチ ジョブはデータベース トランザクション内でラップされるため、暗黙的なコミットをトリガーするデータベース ステートメントはジョブ内で実行しないでください。

<a name="naming-batches"></a>
#### バッチに名前を付ける

Laravel Horizon や Laravel Telescope などの一部のツールでは、バッチに名前が付けられている場合、バッチのより使いやすいデバッグ情報が提供される場合があります。バッチに任意の名前を割り当てるには、バッチの定義中に `name` メソッドを呼び出すことができます。

    $batch = Bus::batch([
        // ...
    ])->then(function (Batch $batch) {
        // All jobs completed successfully...
    })->name('Import CSV')->dispatch();

<a name="batch-connection-queue"></a>
#### バッチ接続とキュー

バッチジョブに使用する接続とキューを指定したい場合は、`onConnection` メソッドと `onQueue` メソッドを使用できます。すべてのバッチ ジョブは、同じ接続およびキュー内で実行する必要があります。

    $batch = Bus::batch([
        // ...
    ])->then(function (Batch $batch) {
        // All jobs completed successfully...
    })->onConnection('redis')->onQueue('imports')->dispatch();

<a name="chains-and-batches"></a>
### チェーンとバッチ

チェーンされたジョブを配列内に配置することで、バッチ内で [連鎖したジョブ](#job-chaining) のセットを定義できます。たとえば、2 つのジョブ チェーンを並行して実行し、両方のジョブ チェーンの処理が完了したときにコールバックを実行できます。

    use App\Jobs\ReleasePodcast;
    use App\Jobs\SendPodcastReleaseNotification;
    use Illuminate\Bus\Batch;
    use Illuminate\Support\Facades\Bus;

    Bus::batch([
        [
            new ReleasePodcast(1),
            new SendPodcastReleaseNotification(1),
        ],
        [
            new ReleasePodcast(2),
            new SendPodcastReleaseNotification(2),
        ],
    ])->then(function (Batch $batch) {
        // ...
    })->dispatch();

逆に、チェーン内でバッチを定義することにより、[chain](#job-chaining) 内でジョブのバッチを実行することもできます。たとえば、最初にジョブのバッチを実行して複数のポッドキャストをリリースし、次にジョブのバッチを実行してリリース通知を送信できます。

    use App\Jobs\FlushPodcastCache;
    use App\Jobs\ReleasePodcast;
    use App\Jobs\SendPodcastReleaseNotification;
    use Illuminate\Support\Facades\Bus;

    Bus::chain([
        new FlushPodcastCache,
        Bus::batch([
            new ReleasePodcast(1),
            new ReleasePodcast(2),
        ]),
        Bus::batch([
            new SendPodcastReleaseNotification(1),
            new SendPodcastReleaseNotification(2),
        ]),
    ])->dispatch();

<a name="adding-jobs-to-batches"></a>
### バッチへのジョブの追加

場合によっては、バッチ処理されたジョブ内からバッチにジョブを追加すると便利な場合があります。このパターンは、Web リクエスト中にディスパッチするのに時間がかかりすぎる可能性がある数千のジョブをバッチ処理する必要がある場合に役立ちます。したがって、代わりに、バッチにさらに多くのジョブを追加する「ローダー」ジョブの最初のバッチをディスパッチすることもできます。

    $batch = Bus::batch([
        new LoadImportBatch,
        new LoadImportBatch,
        new LoadImportBatch,
    ])->then(function (Batch $batch) {
        // All jobs completed successfully...
    })->name('Import Contacts')->dispatch();

この例では、`LoadImportBatch` ジョブを使用して、追加のジョブでバッチをハイドレートします。これを実現するには、ジョブの `batch` メソッドを介してアクセスできるバッチ インスタンスで `add` メソッドを使用します。

    use App\Jobs\ImportContacts;
    use Illuminate\Support\Collection;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            return;
        }

        $this->batch()->add(Collection::times(1000, function () {
            return new ImportContacts;
        }));
    }

> [!WARNING]  
> ジョブをバッチに追加できるのは、同じバッチに属するジョブ内からのみです。

<a name="inspecting-batches"></a>
### バッチの検査

バッチ完了コールバックに提供される `Illuminate\Bus\Batch` インスタンスには、特定のジョブのバッチの操作と検査を支援するさまざまなプロパティとメソッドがあります。

    // The UUID of the batch...
    $batch->id;

    // The name of the batch (if applicable)...
    $batch->name;

    // The number of jobs assigned to the batch...
    $batch->totalJobs;

    // The number of jobs that have not been processed by the queue...
    $batch->pendingJobs;

    // The number of jobs that have failed...
    $batch->failedJobs;

    // The number of jobs that have been processed thus far...
    $batch->processedJobs();

    // The completion percentage of the batch (0-100)...
    $batch->progress();

    // Indicates if the batch has finished executing...
    $batch->finished();

    // Cancel the execution of the batch...
    $batch->cancel();

    // Indicates if the batch has been cancelled...
    $batch->cancelled();

<a name="returning-batches-from-routes"></a>
#### ルートからバッチを返す

すべての `Illuminate\Bus\Batch` インスタンスは JSON シリアル化可能です。つまり、アプリケーションのルートの 1 つから直接インスタンスを返し、完了の進行状況など、バッチに関する情報を含む JSON ペイロードを取得できます。これにより、バッチの完了の進行状況に関する情報をアプリケーションの UI に表示するのが便利になります。

ID でバッチを取得するには、`Bus` ファサードの `findBatch` メソッドを使用できます。

    use Illuminate\Support\Facades\Bus;
    use Illuminate\Support\Facades\Route;

    Route::get('/batch/{batchId}', function (string $batchId) {
        return Bus::findBatch($batchId);
    });

<a name="cancelling-batches"></a>
### バッチのキャンセル

場合によっては、特定のバッチの実行をキャンセルする必要がある場合があります。これは、`Illuminate\Bus\Batch` インスタンスで `cancel` メソッドを呼び出すことで実現できます。

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        if ($this->user->exceedsImportLimit()) {
            return $this->batch()->cancel();
        }

        if ($this->batch()->cancelled()) {
            return;
        }
    }

前の例でお気づきかと思いますが、バッチ処理されたジョブは通常、実行を続行する前に、対応するバッチがキャンセルされたかどうかを判断する必要があります。ただし、便宜上、代わりに `SkipIfBatchCancelled` [middleware](#job-middleware) をジョブに割り当てることもできます。その名前が示すように、このミドルウェアは、対応するバッチがキャンセルされた場合にジョブを処理しないように Laravel に指示します。

    use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

    /**
     * Get the middleware the job should pass through.
     */
    public function middleware(): array
    {
        return [new SkipIfBatchCancelled];
    }

<a name="batch-failures"></a>
### バッチの失敗

バッチ処理されたジョブが失敗すると、`catch` コールバック (割り当てられている場合) が呼び出されます。このコールバックは、バッチ内で失敗した最初のジョブに対してのみ呼び出されます。

<a name="allowing-failures"></a>
#### 失敗を許容する

バッチ内のジョブが失敗すると、Laravel は自動的にバッチを「キャンセル」としてマークします。必要に応じて、ジョブの失敗によってバッチが自動的にキャンセルとしてマークされないように、この動作を無効にすることができます。これは、バッチのディスパッチ中に `allowFailures` メソッドを呼び出すことで実現できます。

    $batch = Bus::batch([
        // ...
    ])->then(function (Batch $batch) {
        // All jobs completed successfully...
    })->allowFailures()->dispatch();

<a name="retrying-failed-batch-jobs"></a>
#### 失敗したバッチジョブの再試行

便宜上、Laravel には、特定のバッチで失敗したすべてのジョブを簡単に再試行できる `queue:retry-batch` Artisan コマンドが用意されています。 `queue:retry-batch` コマンドは、失敗したジョブを再試行する必要があるバッチの UUID を受け入れます。

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### バッチのプルーニング

プルーニングを行わない場合、`job_batches` テーブルは非常に迅速にレコードを蓄積できます。これを軽減するには、[schedule](/docs/{{version}}/scheduling) `queue:prune-batches` Artisan コマンドを毎日実行する必要があります。

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('queue:prune-batches')->daily();

デフォルトでは、24 時間以上経過した完了したバッチはすべて削除されます。コマンドを呼び出すときに `hours` オプションを使用して、バッチ データを保持する期間を決定できます。たとえば、次のコマンドは 48 時間以上前に終了したすべてのバッチを削除します。

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('queue:prune-batches --hours=48')->daily();

場合によっては、`jobs_batches` テーブルに、ジョブが失敗し、そのジョブが正常に再試行されなかったバッチなど、正常に完了しなかったバッチのバッチ レコードが蓄積されることがあります。 `unfinished` オプションを使用して、これらの未完了のバッチ レコードを削除するように `queue:prune-batches` コマンドに指示できます。

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();

同様に、`jobs_batches` テーブルにも、キャンセルされたバッチのバッチ レコードが蓄積される場合があります。 `cancelled` オプションを使用して、これらのキャンセルされたバッチ レコードを削除するように `queue:prune-batches` コマンドに指示できます。

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB へのバッチの保存

Laravel は、リレーショナル データベースの代わりに [DynamoDB](https://aws.amazon.com/dynamodb) にバッチ メタ情報を保存するためのサポートも提供します。ただし、すべてのバッチ レコードを保存するには、DynamoDB テーブルを手動で作成する必要があります。

通常、このテーブルには `job_batches` という名前を付ける必要がありますが、アプリケーションの `queue` 構成ファイル内の `queue.batching.table` 構成値の値に基づいてテーブルに名前を付ける必要があります。

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB バッチテーブルの設定

`job_batches` テーブルには、`application` という名前の文字列プライマリ パーティション キーと、`id` という名前の文字列プライマリ ソート キーが必要です。キーの `application` 部分には、アプリケーションの `app` 構成ファイル内の `name` 構成値で定義されたアプリケーションの名前が含まれます。アプリケーション名は DynamoDB テーブルのキーの一部であるため、同じテーブルを使用して複数の Laravel アプリケーションのジョブ バッチを保存できます。

さらに、[自動バッチプルーニング](#pruning-batches-in-dynamodb) を利用したい場合は、テーブルに `ttl` 属性を定義できます。

<a name="dynamodb-configuration"></a>
#### DynamoDB の構成

次に、Laravel アプリケーションが Amazon DynamoDB と通信できるように AWS SDK をインストールします。

```shell
composer require aws/aws-sdk-php
```

次に、`queue.batching.driver` 構成オプションの値を `dynamodb` に設定します。さらに、`batching` 構成配列内で `key`、`secret`、および `region` 構成オプションを定義する必要があります。これらのオプションは、AWS での認証に使用されます。 `dynamodb` ドライバを使用する場合、`queue.batching.database` 構成オプションは不要です。

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```

<a name="pruning-batches-in-dynamodb"></a>
#### DynamoDB でのバッチのプルーニング

[DynamoDB](https://aws.amazon.com/dynamodb) を使用してジョブ バッチ情報を保存する場合、リレーショナル データベースに保存されているバッチのプルーニングに使用される一般的なプルーニング コマンドは機能しません。代わりに、[DynamoDB のネイティブ TTL 機能](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) を利用して、古いバッチのレコードを自動的に削除できます。

`ttl` 属性を使用して DynamoDB テーブルを定義した場合は、設定パラメータを定義して、Laravel にバッチレコードのプルーニング方法を指示できます。 `queue.batching.ttl_attribute` 設定値は、TTL を保持する属性の名前を定義します。一方、`queue.batching.ttl` 設定値は、バッチ レコードが DynamoDB テーブルから削除されるまでの秒数を、レコードが最後に更新された時刻と相対的に定義します。

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7 days...
],
```

<a name="queueing-closures"></a>
## キューの閉鎖 (Queueing Closures)

ジョブ クラスをキューにディスパッチする代わりに、クロージャをディスパッチすることもできます。これは、現在のリクエスト サイクルの外で実行する必要がある迅速で単純なタスクに最適です。クロージャをキューにディスパッチするとき、クロージャのコード コンテンツは暗号的に署名されるため、転送中に変更することはできません。

    $podcast = App\Podcast::find(1);

    dispatch(function () use ($podcast) {
        $podcast->publish();
    });

`catch` メソッドを使用すると、キューの [設定された再試行回数](#max-job-attempts-and-timeout) をすべて使い果たした後にキューに入れられたクロージャが正常に完了しなかった場合に実行されるクロージャを指定できます。

    use Throwable;

    dispatch(function () use ($podcast) {
        $podcast->publish();
    })->catch(function (Throwable $e) {
        // This job has failed...
    });

> [!WARNING]  
> `catch` コールバックはシリアル化され、後で Laravel キューによって実行されるため、`catch` コールバック内で `$this` 変数を使用しないでください。

<a name="running-the-queue-worker"></a>
## キューワーカーの実行 (Running the Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` コマンド

Laravel には、キューワーカーを起動し、新しいジョブがキューにプッシュされるときに処理する Artisan コマンドが含まれています。 `queue:work` Artisan コマンドを使用してワーカーを実行できます。 `queue:work` コマンドが開始されると、手動で停止するかターミナルを閉じるまで実行が継続されることに注意してください。

```shell
php artisan queue:work
```

> [!NOTE]  
> `queue:work` プロセスをバックグラウンドで永続的に実行し続けるには、[Supervisor](#supervisor-configuration) などのプロセス モニターを使用して、キューワーカーの実行が停止しないようにする必要があります。

処理されたジョブ ID をコマンドの出力に含めたい場合は、`queue:work` コマンドを呼び出すときに `-v` フラグを含めることができます。

```shell
php artisan queue:work -v
```

キューワーカーは存続期間の長いプロセスであり、起動されたアプリケーションの状態をメモリに保存することに注意してください。その結果、開始後のコードベースの変更に気付かなくなります。したがって、展開プロセス中は、必ず [キューワーカーを再起動します](#queue-workers-and-deployment) を行ってください。さらに、アプリケーションによって作成または変更された静的状態は、ジョブ間で自動的にリセットされないことに注意してください。

あるいは、`queue:listen` コマンドを実行することもできます。 `queue:listen` コマンドを使用すると、更新されたコードをリロードしたり、アプリケーションの状態をリセットしたりするときに、ワーカーを手動で再起動する必要がありません。ただし、このコマンドは `queue:work` コマンドよりも効率が大幅に低くなります。

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 複数のキューワーカーの実行

複数のワーカーをキューに割り当ててジョブを同時に処理するには、複数の `queue:work` プロセスを開始するだけです。これは、ターミナルの複数のタブを使用してローカルで実行することも、プロセス マネージャーの構成設定を使用して運用環境で実行することもできます。 [Supervisorを使用する場合](#supervisor-configuration)、`numprocs` 構成値を使用できます。

<a name="specifying-the-connection-queue"></a>
#### 接続とキューの指定

ワーカーがどのキュー接続を使用するかを指定することもできます。 `work` コマンドに渡される接続名は、`config/queue.php` 構成ファイルで定義された接続の 1 つに対応する必要があります。

```shell
php artisan queue:work redis
```

デフォルトでは、`queue:work` コマンドは、指定された接続上のデフォルト キューのジョブのみを処理します。ただし、特定の接続の特定のキューのみを処理することで、キューワーカーをさらにカスタマイズすることもできます。たとえば、すべての電子メールが `redis` キュー接続の `emails` キューで処理される場合、次のコマンドを発行して、そのキューのみを処理するワーカーを開始できます。

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 指定した数のジョブを処理する

`--once` オプションを使用すると、キューから 1 つのジョブのみを処理するようにワーカーに指示できます。

```shell
php artisan queue:work --once
```

`--max-jobs` オプションを使用すると、指定された数のジョブを処理して終了するようにワーカーに指示できます。このオプションは、[Supervisor](#supervisor-configuration) と組み合わせると便利です。これにより、指定された数のジョブの処理後にワーカーが自動的に再起動され、ワー​​カーが蓄積したメモリが解放されます。

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### キューに入れられたすべてのジョブを処理して終了する

`--stop-when-empty` オプションを使用すると、すべてのジョブを処理して正常に終了するようにワーカーに指示できます。このオプションは、Docker コンテナ内で Laravel キューを処理するときに、キューが空になった後にコンテナをシャットダウンする場合に便利です。

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 指定された秒数でジョブを処理する

`--max-time` オプションを使用すると、指定された秒数の間ジョブを処理してから終了するようにワーカーに指示できます。このオプションは、[Supervisor](#supervisor-configuration) と組み合わせると便利です。これにより、一定時間ジョブを処理した後にワーカーが自動的に再起動され、ワー​​カーが蓄積したメモリが解放されます。

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 労働者の睡眠時間

ジョブがキューにある場合、ワーカーはジョブ間に遅延なくジョブの処理を続けます。ただし、`sleep` オプションは、利用可能なジョブがない場合にワーカーが「スリープ」する秒数を決定します。もちろん、ワーカーは寝ている間は新しいジョブを処理しません。

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### メンテナンスモードとキュー

アプリケーションが [メンテナンスモード](/docs/{{version}}/configuration#maintenance-mode) にある間は、キューに入れられたジョブは処理されません。アプリケーションがメンテナンス モードを終了しても、ジョブは通常どおり処理され続けます。

メンテナンス モードが有効になっている場合でもキューワーカーにジョブを強制的に処理させるには、`--force` オプションを使用できます。

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### リソースに関する考慮事項

デーモン キューワーカーは、各ジョブを処理する前にフレームワークを「再起動」しません。したがって、各ジョブが完了したら、重いリソースを解放する必要があります。たとえば、GD ライブラリを使用して画像操作を行っている場合、画像の処理が完了したら、`imagedestroy` を使用してメモリを解放する必要があります。

<a name="queue-priorities"></a>
### キューの優先順位

場合によっては、キューの処理方法に優先順位を付けたい場合があります。たとえば、`config/queue.php` 構成ファイルで、`redis` 接続のデフォルトの `queue` を `low` に設定できます。ただし、場合によっては、次のようにジョブを `high` 優先キューにプッシュしたい場合があります。

    dispatch((new Job)->onQueue('high'));

`low` キュー上のジョブを続行する前に、すべての `high` キュー ジョブが処理されたことを検証するワーカーを開始するには、キュー名のカンマ区切りリストを `work` コマンドに渡します。

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### キューワーカーとデプロイメント

キューワーカーは存続期間の長いプロセスであるため、再起動されなければコードの変更に気づきません。したがって、キューワーカーを使用してアプリケーションをデプロイする最も簡単な方法は、デプロイメント プロセス中にワーカーを再起動することです。 `queue:restart` コマンドを発行すると、すべてのワーカーを正常に再起動できます。

```shell
php artisan queue:restart
```

このコマンドは、既存のジョブが失われないように、すべてのキューワーカーに現在のジョブの処理が完了した後に正常に終了するように指示します。 `queue:restart` コマンドが実行されるとキューワーカーは終了するため、キューワーカーを自動的に再起動するには、[Supervisor](#supervisor-configuration) などのプロセス マネージャーを実行する必要があります。

> [!NOTE]  
> キューは [cache](/docs/{{version}}/cache) を使用して再起動信号を保存するため、この機能を使用する前に、キャッシュ ドライバがアプリケーションに対して適切に構成されていることを確認する必要があります。

<a name="job-expirations-and-timeouts"></a>
### ジョブの有効期限とタイムアウト

<a name="job-expiration"></a>
#### ジョブの有効期限

`config/queue.php` 構成ファイルでは、各キュー接続が `retry_after` オプションを定義します。このオプションは、処理中のジョブを再試行する前にキュー接続が待機する秒数を指定します。たとえば、`retry_after` の値が `90` に設定されている場合、ジョブは解放または削除されずに 90 秒間処理されていた場合、キューに解放されます。通常、`retry_after` 値は、ジョブの処理が完了するまでに合理的にかかる最大秒数に設定する必要があります。

> [!WARNING]  
> `retry_after` 値が含まれない唯一のキュー接続は、Amazon SQS です。 SQS は、AWS コンソール内で管理される [デフォルトの可視性タイムアウト](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) に基づいてジョブを再試行します。

<a name="worker-timeouts"></a>
#### ワーカーのタイムアウト

`queue:work` Artisan コマンドは、`--timeout` オプションを公開します。デフォルトでは、`--timeout` 値は 60 秒です。ジョブの処理がタイムアウト値で指定された秒数を超えた場合、ジョブを処理しているワーカーはエラーで終了します。通常、ワーカーは [サーバー上に設定されたプロセスマネージャー](#supervisor-configuration) によって自動的に再起動されます。

```shell
php artisan queue:work --timeout=60
```

`retry_after` 構成オプションと `--timeout` CLI オプションは異なりますが、連携してジョブが失われず、ジョブが 1 回だけ正常に処理されるようにします。

> [!WARNING]  
> `--timeout` 値は、常に `retry_after` 構成値より少なくとも数秒短くする必要があります。これにより、凍結されたジョブを処理するワーカーは、ジョブが再試行される前に必ず終了されます。 `--timeout` オプションが `retry_after` 構成値より長い場合、ジョブが 2 回処理される可能性があります。

<a name="supervisor-configuration"></a>
## スーパーバイザの構成 (Supervisor Configuration)

運用環境では、`queue:work` プロセスを実行し続ける方法が必要です。 `queue:work` プロセスは、ワーカー タイムアウトの超過や `queue:restart` コマンドの実行など、さまざまな理由で実行を停止することがあります。

このため、`queue:work` プロセスの終了を検出し、自動的に再起動できるプロセス モニターを構成する必要があります。さらに、プロセス モニターを使用すると、同時に実行する `queue:work` プロセスの数を指定できます。 Supervisor は Linux 環境で一般的に使用されるプロセス モニターであり、その構成方法については次のドキュメントで説明します。

<a name="installing-supervisor"></a>
#### スーパーバイザのインス​​トール

Supervisorは Linux オペレーティング システムのプロセス モニターであり、`queue:work` プロセスが失敗した場合に自動的に再起動します。 Ubuntu に Supervisor をインストールするには、次のコマンドを使用できます。

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> Supervisor を自分で設定および管理するのが大変だと思われる場合は、実稼働 Laravel プロジェクト用に Supervisor を自動的にインストールして設定する [Laravel Forge](https://forge.laravel.com) の使用を検討してください。

<a name="configuring-supervisor"></a>
#### スーパーバイザの構成

スーパーバイザ設定ファイルは通常、`/etc/supervisor/conf.d` ディレクトリに保存されます。このディレクトリ内に、スーパーバイザにプロセスの監視方法を指示する構成ファイルをいくつでも作成できます。たとえば、`queue:work` プロセスを開始および監視する `laravel-worker.conf` ファイルを作成してみましょう。

```ini
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/app.com/artisan queue:work sqs --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=forge
numprocs=8
redirect_stderr=true
stdout_logfile=/home/forge/app.com/worker.log
stopwaitsecs=3600
```

この例では、`numprocs` ディレクティブは、8 つの `queue:work` プロセスを実行してすべてを監視し、失敗した場合は自動的に再起動するようにSupervisorに指示します。必要なキュー接続とワーカー オプションを反映するには、構成の `command` ディレクティブを変更する必要があります。

> [!WARNING]  
> `stopwaitsecs` の値が、最も長く実行されているジョブで消費される秒数よりも大きいことを確認する必要があります。そうしないと、Supervisorがジョブの処理が完了する前にジョブを強制終了する可能性があります。

<a name="starting-supervisor"></a>
#### スーパーバイザの開始

設定ファイルが作成されたら、次のコマンドを使用してスーパーバイザ設定を更新し、プロセスを開始できます。

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

スーパーバイザの詳細については、[Supervisorの文書](http://supervisord.org/index.html) を参照してください。

<a name="dealing-with-failed-jobs"></a>
## 失敗したジョブへの対処 (Dealing With Failed Jobs)

場合によっては、キューに入れられたジョブが失敗することがあります。心配しないでください、物事は常に計画どおりに進むわけではありません。 Laravel には、[ジョブを試行する最大回数を指定します](#max-job-attempts-and-timeout) への便利な方法が含まれています。非同期ジョブはこの試行回数を超えると、`failed_jobs` データベース テーブルに挿入されます。失敗した [同期的にディスパッチされたジョブ](/docs/{{version}}/queues#synchronous-dispatching) はこのテーブルに格納されず、その例外はアプリケーションによって即座に処理されます。

`failed_jobs` テーブルを作成するための移行は、通常、新しい Laravel アプリケーションにすでに存在しています。ただし、アプリケーションにこのテーブルの移行が含まれていない場合は、`make:queue-failed-table` コマンドを使用して移行を作成できます。

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[キューワーカー](#running-the-queue-worker) プロセスを実行する場合、`queue:work` コマンドの `--tries` スイッチを使用して、ジョブの試行の最大回数を指定できます。 `--tries` オプションの値を指定しない場合、ジョブは 1 回だけ、またはジョブ クラスの `$tries` プロパティで指定された回数だけ試行されます。

```shell
php artisan queue:work redis --tries=3
```

`--backoff` オプションを使用すると、例外が発生したジョブを再試行する前に Laravel が待機する秒数を指定できます。デフォルトでは、ジョブはすぐにキューに戻され、再試行できるようになります。

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

例外が発生したジョブを再試行する前に Laravel が待機する秒数をジョブごとに設定したい場合は、ジョブ クラスで `backoff` プロパティを定義することで設定できます。

    /**
     * The number of seconds to wait before retrying the job.
     *
     * @var int
     */
    public $backoff = 3;

ジョブのバックオフ時間を決定するためにより複雑なロジックが必要な場合は、ジョブ クラスで `backoff` メソッドを定義できます。

    /**
    * ジョブを再試行するまでに待機する秒数を計算します。
    */
    public function backoff(): int
    {
        return 3;
    }

`backoff` メソッドからバックオフ値の配列を返すことで、「指数関数的」バックオフを簡単に構成できます。この例では、再試行の遅​​延は、最初の再試行では 1 秒、2 回目の再試行では 5 秒、3 回目の再試行では 10 秒、さらに試行が残っている場合はその後の再試行ごとに 10 秒になります。

    /**
    * ジョブを再試行するまでに待機する秒数を計算します。
    *
    * @return array<int, int>
    */
    public function backoff(): array
    {
        return [1, 5, 10];
    }

<a name="cleaning-up-after-failed-jobs"></a>
### 失敗したジョブのクリーンアップ

特定のジョブが失敗した場合、ユーザーにアラートを送信したり、ジョブによって部分的に完了したアクションを元に戻したりすることができます。これを実現するには、ジョブ クラスで `failed` メソッドを定義します。ジョブの失敗の原因となった `Throwable` インスタンスは、`failed` メソッドに渡されます。

    <?php

    namespace App\Jobs;

    use App\Models\Podcast;
    use App\Services\AudioProcessor;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Foundation\Queue\Queueable;
    use Throwable;

    class ProcessPodcast implements ShouldQueue
    {
        use Queueable;

        /**
         * Create a new job instance.
         */
        public function __construct(
            public Podcast $podcast,
        ) {}

        /**
         * Execute the job.
         */
        public function handle(AudioProcessor $processor): void
        {
            // Process uploaded podcast...
        }

        /**
         * Handle a job failure.
         */
        public function failed(?Throwable $exception): void
        {
            // Send user notification of failure, etc...
        }
    }

> [!WARNING]  
> ジョブの新しいインスタンスは、`failed` メソッドを呼び出す前にインスタンス化されます。したがって、`handle` メソッド内で行われたクラス プロパティの変更は失われます。

<a name="retrying-failed-jobs"></a>
### 失敗したジョブの再試行

`failed_jobs` データベース テーブルに挿入された失敗したジョブをすべて表示するには、`queue:failed` Artisan コマンドを使用できます。

```shell
php artisan queue:failed
```

`queue:failed` コマンドは、ジョブ ID、接続、キュー、失敗時間、およびジョブに関するその他の情報をリストします。ジョブ ID は、失敗したジョブを再試行するために使用できます。たとえば、`ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece` の ID を持つ失敗したジョブを再試行するには、次のコマンドを発行します。

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

必要に応じて、コマンドに複数の ID を渡すことができます。

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

特定のキューに対して失敗したジョブをすべて再試行することもできます。

```shell
php artisan queue:retry --queue=name
```

失敗したジョブをすべて再試行するには、`queue:retry` コマンドを実行し、ID として `all` を渡します。

```shell
php artisan queue:retry all
```

失敗したジョブを削除したい場合は、`queue:forget` コマンドを使用できます。

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]  
> [Horizon](/docs/{{version}}/horizon) を使用する場合、失敗したジョブを削除するには、`queue:forget` コマンドの代わりに `horizon:forget` コマンドを使用する必要があります。

失敗したジョブをすべて `failed_jobs` テーブルから削除するには、`queue:flush` コマンドを使用します。

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 欠落しているモデルの無視

Eloquent モデルをジョブに挿入すると、モデルはキューに置かれる前に自動的にシリアル化され、ジョブの処理時にデータベースから再取得されます。ただし、ジョブがワーカーによる処理を待機している間にモデルが削除された場合、ジョブは `ModelNotFoundException` で失敗する可能性があります。

便宜上、ジョブの `deleteWhenMissingModels` プロパティを `true` に設定することで、モデルが欠落しているジョブを自動的に削除することを選択できます。このプロパティが `true` に設定されている場合、Laravel は例外を発生させずに静かにジョブを破棄します。

    /**
     * Delete the job if its models no longer exist.
     *
     * @var bool
     */
    public $deleteWhenMissingModels = true;

<a name="pruning-failed-jobs"></a>
### 失敗したジョブのプルーニング

`queue:prune-failed` Artisan コマンドを呼び出して、アプリケーションの `failed_jobs` テーブル内のレコードを削除できます。

```shell
php artisan queue:prune-failed
```

デフォルトでは、24 時間以上経過した失敗したジョブ レコードはすべて削除されます。コマンドに `--hours` オプションを指定すると、過去 N 時間以内に挿入された失敗したジョブ レコードのみが保持されます。たとえば、次のコマンドは、48 時間以上前に挿入された失敗したジョブ レコードをすべて削除します。

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### 失敗したジョブを DynamoDB に保存する

Laravel は、失敗したジョブ レコードをリレーショナル データベース テーブルではなく [DynamoDB](https://aws.amazon.com/dynamodb) に保存するサポートも提供します。ただし、失敗したジョブ レコードをすべて保存するには、DynamoDB テーブルを手動で作成する必要があります。通常、このテーブルには `failed_jobs` という名前を付ける必要がありますが、アプリケーションの `queue` 構成ファイル内の `queue.failed.table` 構成値の値に基づいてテーブルに名前を付ける必要があります。

`failed_jobs` テーブルには、`application` という名前の文字列プライマリ パーティション キーと、`uuid` という名前の文字列プライマリ ソート キーが必要です。キーの `application` 部分には、アプリケーションの `app` 構成ファイル内の `name` 構成値で定義されたアプリケーションの名前が含まれます。アプリケーション名は DynamoDB テーブルのキーの一部であるため、同じテーブルを使用して複数の Laravel アプリケーションの失敗したジョブを保存できます。

さらに、Laravel アプリケーションが Amazon DynamoDB と通信できるように、必ず AWS SDK をインストールしてください。

```shell
composer require aws/aws-sdk-php
```

次に、`queue.failed.driver` 構成オプションの値を `dynamodb` に設定します。さらに、失敗したジョブ構成配列内で `key`、`secret`、および `region` 構成オプションを定義する必要があります。これらのオプションは、AWS での認証に使用されます。 `dynamodb` ドライバを使用する場合、`queue.failed.database` 構成オプションは不要です。

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```

<a name="disabling-failed-job-storage"></a>
### 失敗したジョブの保存を無効にする

`queue.failed.driver` 構成オプションの値を `null` に設定することで、失敗したジョブを保存せずに破棄するように Laravel に指示できます。通常、これは `QUEUE_FAILED_DRIVER` 環境変数を介して実現できます。

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 失敗したジョブイベント

ジョブが失敗したときに呼び出されるイベント リスナを登録したい場合は、`Queue` ファサードの `failing` メソッドを使用できます。たとえば、Laravel に含まれる `AppServiceProvider` の `boot` メソッドからこのイベントにクロージャーをアタッチできます。

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Queue;
    use Illuminate\Support\ServiceProvider;
    use Illuminate\Queue\Events\JobFailed;

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
            Queue::failing(function (JobFailed $event) {
                // $event->connectionName
                // $event->job
                // $event->exception
            });
        }
    }

<a name="clearing-jobs-from-queues"></a>
## キューからジョブをクリアする (Clearing Jobs From Queues)

> [!NOTE]  
> [Horizon](/docs/{{version}}/horizon) を使用する場合は、`queue:clear` コマンドの代わりに、`horizon:clear` コマンドを使用してキューからジョブをクリアする必要があります。

デフォルト接続のデフォルトキューからすべてのジョブを削除したい場合は、`queue:clear` Artisan コマンドを使用して削除できます。

```shell
php artisan queue:clear
```

`connection` 引数と `queue` オプションを指定して、特定の接続とキューからジョブを削除することもできます。

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]  
> キューからのジョブのクリアは、SQS、Redis、およびデータベース キュー ドライバでのみ使用できます。さらに、SQS メッセージの削除プロセスには最大 60 秒かかるため、キューをクリアしてから最大 60 秒以内に SQS キューに送信されたジョブも削除される可能性があります。

<a name="monitoring-your-queues"></a>
## キューの監視 (Monitoring Your Queues)

キューにジョブが突然殺到すると、キューが過剰になり、ジョブが完了するまでの待ち時間が長くなる可能性があります。必要に応じて、Laravel はキューのジョブ数が指定されたしきい値を超えたときに警告を発することができます。

まず、`queue:monitor` コマンドを [毎分走る](/docs/{{version}}/scheduling) にスケジュールする必要があります。このコマンドは、監視するキューの名前と、必要なジョブ数のしきい値を受け入れます。

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

このコマンドをスケジュールするだけでは、キューの超過ステータスを警告する通知をトリガーするには十分ではありません。コマンドがしきい値を超えるジョブ数を含むキューを検出すると、`Illuminate\Queue\Events\QueueBusy` イベントが送出されます。あなたまたは開発チームに通知を送信するために、アプリケーションの `AppServiceProvider` 内でこのイベントをリッスンできます。

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (QueueBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new QueueHasLongWaitTime(
                $event->connection,
                $event->queue,
                $event->size
            ));
    });
}
```

<a name="testing"></a>
## テスト (Testing)

ジョブをディスパッチするコードをテストする場合、ジョブのコードは、それをディスパッチするコードとは別に直接テストできるため、実際にはジョブ自体を実行しないように Laravel に指示することができます。もちろん、ジョブ自体をテストするために、ジョブ インスタンスをインスタンス化し、テスト内で `handle` メソッドを直接呼び出すこともできます。

`Queue` ファサードの `fake` メソッドを使用して、キューに入れられたジョブが実際にキューにプッシュされるのを防ぐことができます。 `Queue` ファサードの `fake` メソッドを呼び出した後、アプリケーションがジョブをキューにプッシュしようとしたことをアサートできます。

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // Perform order shipping...

    // Assert that no jobs were pushed...
    Queue::assertNothingPushed();

    // Assert a job was pushed to a given queue...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);

    // Assert a job was not pushed...
    Queue::assertNotPushed(AnotherJob::class);

    // Assert that a Closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert the total number of jobs that were pushed...
    Queue::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Queue::fake();

        // Perform order shipping...

        // Assert that no jobs were pushed...
        Queue::assertNothingPushed();

        // Assert a job was pushed to a given queue...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushed(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);

        // Assert that a Closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```

特定の「真実テスト」に合格するジョブがプッシュされたことをアサートするために、`assertPushed` メソッドまたは `assertNotPushed` メソッドにクロージャーを渡すことができます。指定された真実テストに合格する少なくとも 1 つのジョブがプッシュされた場合、アサーションは成功します。

    Queue::assertPushed(function (ShipOrder $job) use ($order) {
        return $job->order->id === $order->id;
    });

<a name="faking-a-subset-of-jobs"></a>
### ジョブのサブセットを偽装する

他のジョブを通常どおり実行できるようにしながら、特定のジョブのみを偽装する必要がある場合は、偽装するジョブのクラス名を `fake` メソッドに渡すことができます。

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

`except` メソッドを使用すると、指定したジョブのセットを除くすべてのジョブを偽装できます。

    Queue::fake()->except([
        ShipOrder::class,
    ]);

<a name="testing-job-chains"></a>
### ジョブチェーンのテスト

ジョブ チェーンをテストするには、`Bus` ファサードの偽装機能を利用する必要があります。 `Bus` ファサードの `assertChained` メソッドを使用して、[仕事の連鎖](/docs/{{version}}/queues#job-chaining) がディスパッチされたことをアサートできます。 `assertChained` メソッドは、最初の引数としてチェーンされたジョブの配列を受け入れます。

    use App\Jobs\RecordShipment;
    use App\Jobs\ShipOrder;
    use App\Jobs\UpdateInventory;
    use Illuminate\Support\Facades\Bus;

    Bus::fake();

    // ...

    Bus::assertChained([
        ShipOrder::class,
        RecordShipment::class,
        UpdateInventory::class
    ]);

上の例でわかるように、チェーンされたジョブの配列は、ジョブのクラス名の配列である場合があります。ただし、実際のジョブ インスタンスの配列を提供することもできます。これを行うと、Laravel はジョブ インスタンスが同じクラスであり、アプリケーションによってディスパッチされたチェーン ジョブのプロパティ値が同じであることを確認します。

    Bus::assertChained([
        new ShipOrder,
        new RecordShipment,
        new UpdateInventory,
    ]);

`assertDispatchedWithoutChain` メソッドを使用して、ジョブがチェーンなしでプッシュされたことをアサートできます。

    Bus::assertDispatchedWithoutChain(ShipOrder::class);

<a name="testing-chain-modifications"></a>
#### チェーンの変更のテスト

チェーンされたジョブ [ジョブを既存のチェーンの先頭または末尾に追加します](#adding-jobs-to-the-chain) の場合、ジョブの `assertHasChain` メソッドを使用して、ジョブに予想される残りのジョブのチェーンがあることをアサートできます。

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` メソッドを使用して、ジョブの残りのチェーンが空であることをアサートできます。

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 連鎖バッチのテスト

ジョブ チェーンが [ジョブのバッチが含まれています](#chains-and-batches) の場合、チェーン アサーション内に `Bus::chainedBatch` 定義を挿入することで、チェーンされたバッチが期待どおりであることをアサートできます。

    use App\Jobs\ShipOrder;
    use App\Jobs\UpdateInventory;
    use Illuminate\Bus\PendingBatch;
    use Illuminate\Support\Facades\Bus;

    Bus::assertChained([
        new ShipOrder,
        Bus::chainedBatch(function (PendingBatch $batch) {
            return $batch->jobs->count() === 3;
        }),
        new UpdateInventory,
    ]);

<a name="testing-job-batches"></a>
### ジョブバッチのテスト

`Bus` ファサードの `assertBatched` メソッドを使用して、[ジョブのバッチ](/docs/{{version}}/queues#job-batching) がディスパッチされたことをアサートできます。 `assertBatched` メソッドに指定されたクロージャは、バッチ内のジョブを検査するために使用される `Illuminate\Bus\PendingBatch` のインスタンスを受け取ります。

    use Illuminate\Bus\PendingBatch;
    use Illuminate\Support\Facades\Bus;

    Bus::fake();

    // ...

    Bus::assertBatched(function (PendingBatch $batch) {
        return $batch->name == 'import-csv' &&
               $batch->jobs->count() === 10;
    });

`assertBatchCount` メソッドを使用して、指定された数のバッチがディスパッチされたことをアサートできます。

    Bus::assertBatchCount(3);

`assertNothingBatched` を使用して、バッチがディスパッチされていないことをアサートできます。

    Bus::assertNothingBatched();

<a name="testing-job-batch-interaction"></a>
#### ジョブ/バッチインタラクションのテスト

さらに、場合によっては、個々のジョブとその基礎となるバッチとの対話をテストする必要があるかもしれません。たとえば、ジョブがそのバッチのさらなる処理をキャンセルしたかどうかをテストする必要がある場合があります。これを実現するには、`withFakeBatch` メソッドを介してジョブに偽のバッチを割り当てる必要があります。 `withFakeBatch` メソッドは、ジョブ インスタンスと偽のバッチを含むタプルを返します。

    [$job, $batch] = (new ShipOrder)->withFakeBatch();

    $job->handle();

    $this->assertTrue($batch->cancelled());
    $this->assertEmpty($batch->added);

<a name="testing-job-queue-interactions"></a>
### ジョブ/キューの相互作用のテスト

場合によっては、キューに入れられたジョブ [自分自身をキューに解放して戻します](#manually-releasing-a-job) をテストする必要があるかもしれません。または、ジョブ自体が削除されたかどうかをテストする必要がある場合があります。ジョブをインスタンス化し、`withFakeQueueInteractions` メソッドを呼び出すことで、これらのキューの対話をテストできます。

ジョブのキューの対話が偽装されると、ジョブに対して `handle` メソッドを呼び出すことができます。ジョブを呼び出した後、`assertReleased`、`assertDeleted`、`assertNotDeleted`、`assertFailed`、`assertFailedWith`、および `assertNotFailed` メソッドを使用して、ジョブのキューの相互作用に対するアサーションを行うことができます。

```php
use App\Exceptions\CorruptedAudioException;
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
$job->assertDeleted();
$job->assertNotDeleted();
$job->assertFailed();
$job->assertFailedWith(CorruptedAudioException::class);
$job->assertNotFailed();
```

<a name="job-events"></a>
## ジョブイベント (Job Events)

`Queue` [facade](/docs/{{version}}/facades) で `before` メソッドと `after` メソッドを使用すると、キューに入れられたジョブの処理前または後に実行されるコールバックを指定できます。これらのコールバックは、追加のログを実行したり、ダッシュボードの統計を増分したりする絶好の機会です。通常、これらのメソッドは、[サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッドから呼び出す必要があります。たとえば、Laravel に含まれる `AppServiceProvider` を使用できます。

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Queue;
    use Illuminate\Support\ServiceProvider;
    use Illuminate\Queue\Events\JobProcessed;
    use Illuminate\Queue\Events\JobProcessing;

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
            Queue::before(function (JobProcessing $event) {
                // $event->connectionName
                // $event->job
                // $event->job->payload()
            });

            Queue::after(function (JobProcessed $event) {
                // $event->connectionName
                // $event->job
                // $event->job->payload()
            });
        }
    }

`Queue` [facade](/docs/{{version}}/facades) で `looping` メソッドを使用すると、ワーカーがキューからジョブをフェッチしようとする前に実行するコールバックを指定できます。たとえば、以前に失敗したジョブによってオープンされたままになっているトランザクションをロールバックするクロージャを登録できます。

    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\Facades\Queue;

    Queue::looping(function () {
        while (DB::transactionLevel() > 0) {
            DB::rollBack();
        }
    });

