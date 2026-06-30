<!-- # Queues -->
# Queues

- [Introduction](#introduction)
    - [Connections Vs. Queues](#connections-vs-queues)
    - [Driver Notes & Prerequisites](#driver-prerequisites)
- [Creating Jobs](#creating-jobs)
    - [Generating Job Classes](#generating-job-classes)
    - [Class Structure](#class-structure)
    - [Unique Jobs](#unique-jobs)
- [Job Middleware](#job-middleware)
    - [Rate Limiting](#rate-limiting)
    - [Preventing Job Overlaps](#preventing-job-overlaps)
    - [Throttling Exceptions](#throttling-exceptions)
- [Dispatching Jobs](#dispatching-jobs)
    - [Delayed Dispatching](#delayed-dispatching)
    - [Synchronous Dispatching](#synchronous-dispatching)
    - [Jobs & Database Transactions](#jobs-and-database-transactions)
    - [Job Chaining](#job-chaining)
    - [Customizing The Queue & Connection](#customizing-the-queue-and-connection)
    - [Specifying Max Job Attempts / Timeout Values](#max-job-attempts-and-timeout)
    - [Error Handling](#error-handling)
- [Job Batching](#job-batching)
    - [Defining Batchable Jobs](#defining-batchable-jobs)
    - [Dispatching Batches](#dispatching-batches)
    - [Adding Jobs To Batches](#adding-jobs-to-batches)
    - [Inspecting Batches](#inspecting-batches)
    - [Cancelling Batches](#cancelling-batches)
    - [Batch Failures](#batch-failures)
    - [Pruning Batches](#pruning-batches)
- [Queueing Closures](#queueing-closures)
- [Running The Queue Worker](#running-the-queue-worker)
    - [The `queue:work` Command](#the-queue-work-command)
    - [Queue Priorities](#queue-priorities)
    - [Queue Workers & Deployment](#queue-workers-and-deployment)
    - [Job Expirations & Timeouts](#job-expirations-and-timeouts)
- [Supervisor Configuration](#supervisor-configuration)
- [Dealing With Failed Jobs](#dealing-with-failed-jobs)
    - [Cleaning Up After Failed Jobs](#cleaning-up-after-failed-jobs)
    - [Retrying Failed Jobs](#retrying-failed-jobs)
    - [Ignoring Missing Models](#ignoring-missing-models)
    - [Pruning Failed Jobs](#pruning-failed-jobs)
    - [Storing Failed Jobs In DynamoDB](#storing-failed-jobs-in-dynamodb)
    - [Disabling Failed Job Storage](#disabling-failed-job-storage)
    - [Failed Job Events](#failed-job-events)
- [Clearing Jobs From Queues](#clearing-jobs-from-queues)
- [Monitoring Your Queues](#monitoring-your-queues)
- [Job Events](#job-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- While building your web application, you may have some tasks, such as parsing and storing an uploaded CSV file, that take too long to perform during a typical web request. Thankfully, Laravel allows you to easily create queued jobs that may be processed in the background. By moving time intensive tasks to a queue, your application can respond to web requests with blazing speed and provide a better user experience to your customers. -->
Web アプリケーションの構築中に、アップロードされた CSV ファイルの解析や保存など、通常の Web リクエストでは実行するには時間がかかりすぎるタスクがいくつか発生する場合があります。ありがたいことに、Laravel ではバックグラウンドで処理できるキューに入れられたジョブを簡単に作成できます。時間のかかるタスクをキューに移動することで、アプリケーションは Web リクエストに驚異的な速度で応答し、顧客により良いユーザー エクスペリエンスを提供できるようになります。

<!-- Laravel queues provide a unified queueing API across a variety of different queue backends, such as [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), or even a relational database. -->
Laravel キューは、[Amazon SQS](https://aws.amazon.com/sqs/)、[Redis](https://redis.io)、さらにはリレーショナル データベースなど、さまざまな異なるキュー バックエンドにわたって統合されたキュー API を提供します。

<!-- Laravel's queue configuration options are stored in your application's `config/queue.php` configuration file. In this file, you will find connection configurations for each of the queue drivers that are included with the framework, including the database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), and [Beanstalkd](https://beanstalkd.github.io/) drivers, as well as a synchronous driver that will execute jobs immediately (for use during local development). A `null` queue driver is also included which discards queued jobs. -->
Laravel のキュー構成オプションは、アプリケーションの `config/queue.php` 構成ファイルに保存されます。このファイルには、データベース、[Amazon SQS](https://aws.amazon.com/sqs/)、[Redis](https://redis.io)、[Beanstalkd](https://beanstalkd.github.io/) ドライバ、および (ローカル開発中に使用する) ジョブを即時に実行する同期ドライバなど、フレームワークに含まれる各キュー ドライバの接続構成が含まれています。キューに入れられたジョブを破棄する `null` キュー ドライバも含まれています。

> [!NOTE]
> Laravel は、Redis を利用したキュー用の美しいダッシュボードおよび構成システムである Horizon を提供するようになりました。詳細については、[Horizon documentation](/docs/9.x/horizon) の全文をご覧ください。

<a name="connections-vs-queues"></a>
<!-- ### Connections Vs. Queues -->
### Connections Vs. Queues

<!-- Before getting started with Laravel queues, it is important to understand the distinction between "connections" and "queues". In your `config/queue.php` configuration file, there is a `connections` configuration array. This option defines the connections to backend queue services such as Amazon SQS, Beanstalk, or Redis. However, any given queue connection may have multiple "queues" which may be thought of as different stacks or piles of queued jobs. -->
Laravel キューを使い始める前に、「接続」と「キュー」の違いを理解することが重要です。 `config/queue.php` 構成ファイルには、`connections` 構成配列があります。このオプションは、Amazon SQS、Beanstalk、Redis などのバックエンド キュー サービスへの接続を定義します。ただし、特定のキュー接続には、キューに入れられたジョブの異なるスタックまたは山とみなされる複数の「キュー」がある場合があります。

<!-- Note that each connection configuration example in the `queue` configuration file contains a `queue` attribute. This is the default queue that jobs will be dispatched to when they are sent to a given connection. In other words, if you dispatch a job without explicitly defining which queue it should be dispatched to, the job will be placed on the queue that is defined in the `queue` attribute of the connection configuration: -->
`queue` 構成ファイル内の各接続構成例には、`queue` 属性が含まれていることに注意してください。これは、ジョブが特定の接続に送信されるときにディスパッチされるデフォルトのキューです。つまり、ジョブをディスパッチするキューを明示的に定義せずにジョブをディスパッチすると、ジョブは接続構成の `queue` 属性で定義されたキューに配置されます。

```
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```

<!-- Some applications may not need to ever push jobs onto multiple queues, instead preferring to have one simple queue. However, pushing jobs to multiple queues can be especially useful for applications that wish to prioritize or segment how jobs are processed, since the Laravel queue worker allows you to specify which queues it should process by priority. For example, if you push jobs to a `high` queue, you may run a worker that gives them higher processing priority: -->
アプリケーションによっては、ジョブを複数のキューにプッシュする必要がなく、代わりに 1 つの単純なキューを持つことを好む場合があります。ただし、Laravel キューワーカーでは優先度によってどのキューを処理するかを指定できるため、ジョブを複数のキューにプッシュすることは、ジョブの処理方法に優先順位を付けたり、分割したりしたいアプリケーションにとって特に便利です。たとえば、ジョブを `high` キューにプッシュする場合、より高い処理優先度を与えるワーカーを実行できます。

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Notes & Prerequisites -->
### Driver Notes & Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- In order to use the `database` queue driver, you will need a database table to hold the jobs. To generate a migration that creates this table, run the `queue:table` Artisan command. Once the migration has been created, you may migrate your database using the `migrate` command: -->
`database` キュー ドライバを使用するには、ジョブを保持するデータベース テーブルが必要です。このテーブルを作成する移行を生成するには、`queue:table` Artisan コマンドを実行します。移行が作成されたら、`migrate` コマンドを使用してデータベースを移行できます。

```shell
php artisan queue:table

php artisan migrate
```

<!-- Finally, don't forget to instruct your application to use the `database` driver by updating the `QUEUE_CONNECTION` variable in your application's `.env` file: -->
最後に、アプリケーションの `.env` ファイル内の `QUEUE_CONNECTION` 変数を更新して、`database` ドライバを使用するようにアプリケーションに指示することを忘れないでください。

```
QUEUE_CONNECTION=database
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- In order to use the `redis` queue driver, you should configure a Redis database connection in your `config/database.php` configuration file. -->
`redis` キュー ドライバを使用するには、`config/database.php` 構成ファイルで Redis データベース接続を構成する必要があります。

<!-- **Redis Cluster** -->
**Redis クラスター**

<!-- If your Redis queue connection uses a Redis Cluster, your queue names must contain a [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags). This is required in order to ensure all of the Redis keys for a given queue are placed into the same hash slot: -->
Redis キュー接続で Redis クラスターを使用する場合、キュー名には [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags) が含まれている必要があります。これは、特定のキューのすべての Redis キーが同じハッシュ スロットに配置されるようにするために必要です。

```
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => '{default}',
    'retry_after' => 90,
],
```

<!-- **Blocking** -->
**ブロッキング**

<!-- When using the Redis queue, you may use the `block_for` configuration option to specify how long the driver should wait for a job to become available before iterating through the worker loop and re-polling the Redis database. -->
Redis キューを使用する場合、`block_for` 構成オプションを使用して、ドライバがワーカー ループを繰り返して Redis データベースを再ポーリングする前に、ジョブが使用可能になるまで待機する時間を指定できます。

<!-- Adjusting this value based on your queue load can be more efficient than continually polling the Redis database for new jobs. For instance, you may set the value to `5` to indicate that the driver should block for five seconds while waiting for a job to become available: -->
キューの負荷に基づいてこの値を調整すると、新しいジョブを求めて Redis データベースを継続的にポーリングするよりも効率的になる場合があります。たとえば、値を `5` に設定して、ジョブが使用可能になるまでドライバが 5 秒間ブロックされるように指定できます。

```
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => 'default',
    'retry_after' => 90,
    'block_for' => 5,
],
```

> [!WARNING]
> `block_for` を `0` に設定すると、ジョブが使用可能になるまでキューワーカーが無期限にブロックされます。これにより、次のジョブが処理されるまで、`SIGTERM` などのシグナルが処理されなくなります。

<a name="other-driver-prerequisites"></a>
<!-- #### Other Driver Prerequisites -->
#### Other Driver Prerequisites

<!-- The following dependencies are needed for the listed queue drivers. These dependencies may be installed via the Composer package manager: -->
リストされているキュー ドライバには次の依存関係が必要です。これらの依存関係は、Composer パッケージ マネージャーを介してインストールできます。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~4.0`
- Redis: `predis/predis ~1.0` or phpredis PHP extension
-->
- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~4.0`
- Redis: `predis/predis ~1.0` または phpredis PHP 拡張機能

<!-- </div> -->
</div>

<a name="creating-jobs"></a>
<!-- ## Creating Jobs -->
## Creating Jobs

<a name="generating-job-classes"></a>
<!-- ### Generating Job Classes -->
### Generating Job Classes

<!-- By default, all of the queueable jobs for your application are stored in the `app/Jobs` directory. If the `app/Jobs` directory doesn't exist, it will be created when you run the `make:job` Artisan command: -->
デフォルトでは、アプリケーションのキューに入れられるジョブはすべて、`app/Jobs` ディレクトリに保存されます。 `app/Jobs` ディレクトリが存在しない場合は、`make:job` Artisan コマンドを実行すると作成されます。

```shell
php artisan make:job ProcessPodcast
```

<!-- The generated class will implement the `Illuminate\Contracts\Queue\ShouldQueue` interface, indicating to Laravel that the job should be pushed onto the queue to run asynchronously. -->
生成されたクラスは `Illuminate\Contracts\Queue\ShouldQueue` インターフェイスを実装し、非同期で実行するにはジョブをキューにプッシュする必要があることを Laravel に示します。

> [!NOTE]
> ジョブ スタブは、[stub publishing](/docs/9.x/artisan#stub-customization) を使用してカスタマイズできます。

<a name="class-structure"></a>
<!-- ### Class Structure -->
### Class Structure

<!-- Job classes are very simple, normally containing only a `handle` method that is invoked when the job is processed by the queue. To get started, let's take a look at an example job class. In this example, we'll pretend we manage a podcast publishing service and need to process the uploaded podcast files before they are published: -->
ジョブ クラスは非常に単純で、通常はジョブがキューによって処理されるときに呼び出される `handle` メソッドのみを含みます。まず、ジョブ クラスの例を見てみましょう。この例では、ポッドキャスト公開サービスを管理しており、アップロードされたポッドキャスト ファイルを公開前に処理する必要があると仮定します。

```
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * The podcast instance.
     *
     * @var \App\Models\Podcast
     */
    public $podcast;

    /**
     * Create a new job instance.
     *
     * @param  App\Models\Podcast  $podcast
     * @return void
     */
    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }

    /**
     * Execute the job.
     *
     * @param  App\Services\AudioProcessor  $processor
     * @return void
     */
    public function handle(AudioProcessor $processor)
    {
        // Process uploaded podcast...
    }
}
```

<!-- In this example, note that we were able to pass an [Eloquent model](/docs/9.x/eloquent) directly into the queued job's constructor. Because of the `SerializesModels` trait that the job is using, Eloquent models and their loaded relationships will be gracefully serialized and unserialized when the job is processing. -->
この例では、[Eloquent model](/docs/9.x/eloquent) をキューに入れられたジョブのコンストラクターに直接渡すことができたことに注目してください。ジョブが使用している `SerializesModels` トレイトにより、Eloquent モデルとそのロードされた関係は、ジョブの処理中に正常にシリアル化およびシリアル化解除されます。

<!-- If your queued job accepts an Eloquent model in its constructor, only the identifier for the model will be serialized onto the queue. When the job is actually handled, the queue system will automatically re-retrieve the full model instance and its loaded relationships from the database. This approach to model serialization allows for much smaller job payloads to be sent to your queue driver. -->
キューに入れられたジョブがコンストラクターで Eloquent モデルを受け入れる場合、モデルの識別子のみがキューにシリアル化されます。ジョブが実際に処理されると、キュー システムは完全なモデル インスタンスとそのロードされた関係をデータベースから自動的に再取得します。モデルのシリアル化に対するこのアプローチにより、はるかに小さいジョブ ペイロードをキュー ドライバに送信できるようになります。

<a name="handle-method-dependency-injection"></a>
<!-- #### `handle` Method Dependency Injection -->
#### `handle` Method Dependency Injection

<!-- The `handle` method is invoked when the job is processed by the queue. Note that we are able to type-hint dependencies on the `handle` method of the job. The Laravel [service container](/docs/9.x/container) automatically injects these dependencies. -->
`handle` メソッドは、ジョブがキューによって処理されるときに呼び出されます。ジョブの `handle` メソッドに対する依存関係をタイプヒントできることに注意してください。 Laravel [service container](/docs/9.x/container) はこれらの依存関係を自動的に挿入します。

<!-- If you would like to take total control over how the container injects dependencies into the `handle` method, you may use the container's `bindMethod` method. The `bindMethod` method accepts a callback which receives the job and the container. Within the callback, you are free to invoke the `handle` method however you wish. Typically, you should call this method from the `boot` method of your `App\Providers\AppServiceProvider` [service provider](/docs/9.x/providers): -->
コンテナーが依存関係を `handle` メソッドに挿入する方法を完全に制御したい場合は、コンテナーの `bindMethod` メソッドを使用できます。 `bindMethod` メソッドは、ジョブとコンテナーを受け取るコールバックを受け入れます。コールバック内では、必要に応じて `handle` メソッドを自由に呼び出すことができます。通常、このメソッドは、`App\Providers\AppServiceProvider` [service provider](/docs/9.x/providers) の `boot` メソッドから呼び出す必要があります。

```
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function ($job, $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 未処理の画像コンテンツなどのバイナリ データは、キューに入れられたジョブに渡す前に、`base64_encode` 関数を介して渡す必要があります。そうしないと、ジョブがキューに配置されるときに JSON に適切にシリアル化されない可能性があります。

<a name="handling-relationships"></a>
<!-- #### Queued Relationships -->
#### Queued Relationships

<!-- Because loaded relationships also get serialized, the serialized job string can sometimes become quite large. To prevent relations from being serialized, you can call the `withoutRelations` method on the model when setting a property value. This method will return an instance of the model without its loaded relationships: -->
ロードされた関係もシリアル化されるため、シリアル化されたジョブ文字列が非常に大きくなる場合があります。リレーションがシリアル化されないようにするには、プロパティ値を設定するときにモデルで `withoutRelations` メソッドを呼び出します。このメソッドは、ロードされた関係を持たないモデルのインスタンスを返します。

```
/**
 * Create a new job instance.
 *
 * @param  \App\Models\Podcast  $podcast
 * @return void
 */
public function __construct(Podcast $podcast)
{
    $this->podcast = $podcast->withoutRelations();
}
```

<!-- Furthermore, when a job is deserialized and model relationships are re-retrieved from the database, they will be retrieved in their entirety. Any previous relationship constraints that were applied before the model was serialized during the job queueing process will not be applied when the job is deserialized. Therefore, if you wish to work with a subset of a given relationship, you should re-constrain that relationship within your queued job. -->
さらに、ジョブが逆シリアル化され、モデルの関係がデータベースから再取得されると、それらは完全に取得されます。ジョブキューイング プロセス中にモデルがシリアル化される前に適用された以前の関係制約は、ジョブが逆シリアル化されると適用されません。したがって、特定の関係のサブセットを操作したい場合は、キューに入れられたジョブ内でその関係を再制約する必要があります。

<a name="unique-jobs"></a>
<!-- ### Unique Jobs -->
### Unique Jobs

> [!WARNING]
> 固有のジョブには、[locks](/docs/9.x/cache#atomic-locks) をサポートするキャッシュ ドライバが必要です。現在、`memcached`、`redis`、`dynamodb`、`database`、`file`、および `array` キャッシュ ドライバはアトミック ロックをサポートしています。さらに、固有のジョブ制約はバッチ内のジョブには適用されません。

<!-- Sometimes, you may want to ensure that only one instance of a specific job is on the queue at any point in time. You may do so by implementing the `ShouldBeUnique` interface on your job class. This interface does not require you to define any additional methods on your class: -->
場合によっては、特定のジョブのインスタンスが常に 1 つだけキューに存在するようにしたい場合があります。これを行うには、ジョブ クラスに `ShouldBeUnique` インターフェイスを実装します。このインターフェイスでは、クラスに追加のメソッドを定義する必要はありません。

```
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...
}
```

<!-- In the example above, the `UpdateSearchIndex` job is unique. So, the job will not be dispatched if another instance of the job is already on the queue and has not finished processing. -->
上の例では、`UpdateSearchIndex` ジョブは一意です。したがって、ジョブの別のインスタンスがすでにキュー上にあり、処理が完了していない場合、ジョブはディスパッチされません。

<!-- In certain cases, you may want to define a specific "key" that makes the job unique or you may want to specify a timeout beyond which the job no longer stays unique. To accomplish this, you may define `uniqueId` and `uniqueFor` properties or methods on your job class: -->
場合によっては、ジョブを一意にする特定の「キー」を定義したり、ジョブが一意でなくなるタイムアウトを指定したりすることができます。これを実現するには、ジョブ クラスで `uniqueId` および `uniqueFor` プロパティまたはメソッドを定義します。

```
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
     * The unique ID of the job.
     *
     * @return string
     */
    public function uniqueId()
    {
        return $this->product->id;
    }
}
```

<!-- In the example above, the `UpdateSearchIndex` job is unique by a product ID. So, any new dispatches of the job with the same product ID will be ignored until the existing job has completed processing. In addition, if the existing job is not processed within one hour, the unique lock will be released and another job with the same unique key can be dispatched to the queue. -->
上の例では、`UpdateSearchIndex` ジョブは製品 ID によって一意です。したがって、同じ製品 ID を持つジョブの新しいディスパッチは、既存のジョブの処理が完了するまで無視されます。さらに、既存のジョブが 1 時間以内に処理されない場合、一意のロックが解除され、同じ一意のキーを持つ別のジョブがキューにディスパッチされる可能性があります。

> [!WARNING]
> アプリケーションが複数の Web サーバーまたはコンテナーからジョブをディスパッチする場合は、Laravel がジョブが一意であるかどうかを正確に判断できるように、すべてのサーバーが同じ中央キャッシュ サーバーと通信していることを確認する必要があります。

<a name="keeping-jobs-unique-until-processing-begins"></a>
<!-- #### Keeping Jobs Unique Until Processing Begins -->
#### Keeping Jobs Unique Until Processing Begins

<!-- By default, unique jobs are "unlocked" after a job completes processing or fails all of its retry attempts. However, there may be situations where you would like your job to unlock immediately before it is processed. To accomplish this, your job should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract: -->
デフォルトでは、ジョブが処理を完了するか、すべての再試行に失敗すると、固有のジョブは「ロック解除」されます。ただし、ジョブが処理される直前にロックを解除したい場合もあります。これを実現するには、ジョブで `ShouldBeUnique` コントラクトの代わりに `ShouldBeUniqueUntilProcessing` コントラクトを実装する必要があります。

```
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-job-locks"></a>
<!-- #### Unique Job Locks -->
#### Unique Job Locks

<!-- Behind the scenes, when a `ShouldBeUnique` job is dispatched, Laravel attempts to acquire a [lock](/docs/9.x/cache#atomic-locks) with the `uniqueId` key. If the lock is not acquired, the job is not dispatched. This lock is released when the job completes processing or fails all of its retry attempts. By default, Laravel will use the default cache driver to obtain this lock. However, if you wish to use another driver for acquiring the lock, you may define a `uniqueVia` method that returns the cache driver that should be used: -->
バックグラウンドでは、`ShouldBeUnique` ジョブがディスパッチされると、Laravel は `uniqueId` キーを使用して [lock](/docs/9.x/cache#atomic-locks) を取得しようとします。ロックが取得されない場合、ジョブはディスパッチされません。このロックは、ジョブの処理が完了するか、すべての再試行が失敗すると解放されます。デフォルトでは、Laravel はデフォルトのキャッシュドライバを使用してこのロックを取得します。ただし、ロックの取得に別のドライバを使用したい場合は、使用するキャッシュ ドライバを返す `uniqueVia` メソッドを定義できます。

```
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...

    /**
     * Get the cache driver for the unique job lock.
     *
     * @return \Illuminate\Contracts\Cache\Repository
     */
    public function uniqueVia()
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> ジョブの同時処理を制限する必要があるだけの場合は、代わりに [`WithoutOverlapping`](/docs/9.x/queues#preventing-job-overlaps) ジョブ ミドルウェアを使用してください。

<a name="job-middleware"></a>
<!-- ## Job Middleware -->
## Job Middleware

<!-- Job middleware allow you to wrap custom logic around the execution of queued jobs, reducing boilerplate in the jobs themselves. For example, consider the following `handle` method which leverages Laravel's Redis rate limiting features to allow only one job to process every five seconds: -->
ジョブ ミドルウェアを使用すると、キューに入れられたジョブの実行にカスタム ロジックをラップして、ジョブ自体の定型文を減らすことができます。たとえば、Laravel の Redis レート制限機能を活用して、5 秒ごとに 1 つのジョブのみの処理を許可する次の `handle` メソッドを考えてみましょう。

```
use Illuminate\Support\Facades\Redis;

/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');

        // Handle job...
    }, function () {
        // Could not obtain lock...

        return $this->release(5);
    });
}
```

<!-- While this code is valid, the implementation of the `handle` method becomes noisy since it is cluttered with Redis rate limiting logic. In addition, this rate limiting logic must be duplicated for any other jobs that we want to rate limit. -->
このコードは有効ですが、`handle` メソッドの実装には Redis レート制限ロジックが混在しているため、ノイズが多くなります。さらに、このレート制限ロジックは、レート制限したい他のジョブに対しても複製する必要があります。

<!-- Instead of rate limiting in the handle method, we could define a job middleware that handles rate limiting. Laravel does not have a default location for job middleware, so you are welcome to place job middleware anywhere in your application. In this example, we will place the middleware in an `app/Jobs/Middleware` directory: -->
handle メソッドでレート制限を行う代わりに、レート制限を処理するジョブ ミドルウェアを定義できます。 Laravel にはジョブミドルウェアのデフォルトの場所がないため、アプリケーション内のどこにでもジョブミドルウェアを配置できます。この例では、ミドルウェアを `app/Jobs/Middleware` ディレクトリに配置します。

```
<?php

namespace App\Jobs\Middleware;

use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * Process the queued job.
     *
     * @param  mixed  $job
     * @param  callable  $next
     * @return mixed
     */
    public function handle($job, $next)
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
```

<!-- As you can see, like [route middleware](/docs/9.x/middleware), job middleware receive the job being processed and a callback that should be invoked to continue processing the job. -->
ご覧のとおり、[route middleware](/docs/9.x/middleware) のように、ジョブ ミドルウェアは、処理中のジョブと、ジョブの処理を続行するために呼び出されるコールバックを受け取ります。

<!-- After creating job middleware, they may be attached to a job by returning them from the job's `middleware` method. This method does not exist on jobs scaffolded by the `make:job` Artisan command, so you will need to manually add it to your job class: -->
ジョブ ミドルウェアを作成した後、ジョブの `middleware` メソッドからそれらを返すことによって、ジョブ ミドルウェアをジョブにアタッチできます。このメソッドは、`make:job` Artisan コマンドによってスキャフォールディングされたジョブには存在しないため、ジョブ クラスに手動で追加する必要があります。

```
use App\Jobs\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new RateLimited];
}
```

> [!NOTE]
> ジョブ ミドルウェアは、キュー可能なイベント リスナ、メール可能ファイル、および通知に割り当てることもできます。

<a name="rate-limiting"></a>
<!-- ### Rate Limiting -->
### Rate Limiting

<!-- Although we just demonstrated how to write your own rate limiting job middleware, Laravel actually includes a rate limiting middleware that you may utilize to rate limit jobs. Like [route rate limiters](/docs/9.x/routing#defining-rate-limiters), job rate limiters are defined using the `RateLimiter` facade's `for` method. -->
独自のレート制限ジョブ ミドルウェアを作成する方法を説明しましたが、実際には、Laravel にはジョブのレート制限に利用できるレート制限ミドルウェアが含まれています。 [route rate limiters](/docs/9.x/routing#defining-rate-limiters) と同様に、ジョブ レート リミッターは、`RateLimiter` ファサードの `for` メソッドを使用して定義されます。

<!-- For example, you may wish to allow users to backup their data once per hour while imposing no such limit on premium customers. To accomplish this, you may define a `RateLimiter` in the `boot` method of your `AppServiceProvider`: -->
たとえば、プレミアム顧客にはそのような制限を課さず、ユーザーが 1 時間に 1 回データをバックアップできるようにしたい場合があります。これを実現するには、`AppServiceProvider` の `boot` メソッドで `RateLimiter` を定義できます。

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    RateLimiter::for('backups', function ($job) {
        return $job->user->vipCustomer()
                    ? Limit::none()
                    : Limit::perHour(1)->by($job->user->id);
    });
}
```

<!-- In the example above, we defined an hourly rate limit; however, you may easily define a rate limit based on minutes using the `perMinute` method. In addition, you may pass any value you wish to the `by` method of the rate limit; however, this value is most often used to segment rate limits by customer: -->
上の例では、時間当たりのレート制限を定義しました。ただし、`perMinute` メソッドを使用すると、分に基づいてレート制限を簡単に定義できます。さらに、レート制限の `by` メソッドに任意の値を渡すことができます。ただし、この値は、顧客ごとにレート制限を分割するために最もよく使用されます。

```
return Limit::perMinute(50)->by($job->user->id);
```

<!-- Once you have defined your rate limit, you may attach the rate limiter to your backup job using the `Illuminate\Queue\Middleware\RateLimited` middleware. Each time the job exceeds the rate limit, this middleware will release the job back to the queue with an appropriate delay based on the rate limit duration. -->
レート制限を定義したら、`Illuminate\Queue\Middleware\RateLimited` ミドルウェアを使用してバックアップ ジョブにレート リミッターを付加できます。ジョブがレート制限を超えるたびに、このミドルウェアはレート制限の期間に基づいて適切な遅延を設けてジョブをキューに戻します。

```
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new RateLimited('backups')];
}
```

<!-- Releasing a rate limited job back onto the queue will still increment the job's total number of `attempts`. You may wish to tune your `tries` and `maxExceptions` properties on your job class accordingly. Or, you may wish to use the [`retryUntil` method](#time-based-attempts) to define the amount of time until the job should no longer be attempted. -->
レート制限されたジョブをキューに解放しても、ジョブの合計数 `attempts` は増加します。それに応じて、ジョブ クラスの `tries` プロパティと `maxExceptions` プロパティを調整することもできます。または、[`retryUntil` method](#time-based-attempts) を使用して、ジョブが試行されなくなるまでの時間を定義することもできます。

<!-- If you do not want a job to be retried when it is rate limited, you may use the `dontRelease` method: -->
レートが制限されているときにジョブを再試行したくない場合は、`dontRelease` メソッドを使用できます。

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis を使用している場合は、`Illuminate\Queue\Middleware\RateLimitedWithRedis` ミドルウェアを使用できます。これは Redis 用に微調整されており、基本的なレート制限ミドルウェアよりも効率的です。

<a name="preventing-job-overlaps"></a>
<!-- ### Preventing Job Overlaps -->
### Preventing Job Overlaps

<!-- Laravel includes an `Illuminate\Queue\Middleware\WithoutOverlapping` middleware that allows you to prevent job overlaps based on an arbitrary key. This can be helpful when a queued job is modifying a resource that should only be modified by one job at a time. -->
Laravel には、任意のキーに基づいてジョブの重複を防止できる `Illuminate\Queue\Middleware\WithoutOverlapping` ミドルウェアが含まれています。これは、キューに入れられたジョブが、一度に 1 つのジョブのみによって変更されるべきリソースを変更する場合に役立ちます。

<!-- For example, let's imagine you have a queued job that updates a user's credit score and you want to prevent credit score update job overlaps for the same user ID. To accomplish this, you can return the `WithoutOverlapping` middleware from your job's `middleware` method: -->
たとえば、ユーザーのクレジット スコアを更新するキューに入れられたジョブがあり、同じユーザー ID に対してクレジット スコア更新ジョブが重複しないようにしたいとします。これを実現するには、ジョブの `middleware` メソッドから `WithoutOverlapping` ミドルウェアを返すことができます。

```
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new WithoutOverlapping($this->user->id)];
}
```

<!-- Any overlapping jobs of the same type will be released back to the queue. You may also specify the number of seconds that must elapse before the released job will be attempted again: -->
同じタイプの重複するジョブはキューに戻されます。解放されたジョブが再試行されるまでに経過する必要がある秒数を指定することもできます。

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

<!-- If you wish to immediately delete any overlapping jobs so that they will not be retried, you may use the `dontRelease` method: -->
再試行されないように重複するジョブをすぐに削除したい場合は、`dontRelease` メソッドを使用できます。

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

<!-- The `WithoutOverlapping` middleware is powered by Laravel's atomic lock feature. Sometimes, your job may unexpectedly fail or timeout in such a way that the lock is not released. Therefore, you may explicitly define a lock expiration time using the `expireAfter` method. For example, the example below will instruct Laravel to release the `WithoutOverlapping` lock three minutes after the job has started processing: -->
`WithoutOverlapping` ミドルウェアは、Laravel のアトミック ロック機能を利用しています。場合によっては、ロックが解放されずにジョブが予期せず失敗したり、タイムアウトになったりすることがあります。したがって、`expireAfter` メソッドを使用して、ロックの有効期限を明示的に定義できます。たとえば、以下の例は、ジョブの処理が開始されてから 3 分後に `WithoutOverlapping` ロックを解放するように Laravel に指示します。

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` ミドルウェアには、[locks](/docs/9.x/cache#atomic-locks) をサポートするキャッシュ ドライバが必要です。現在、`memcached`、`redis`、`dynamodb`、`database`、`file`、および `array` キャッシュ ドライバはアトミック ロックをサポートしています。

<a name="sharing-lock-keys"></a>
<!-- #### Sharing Lock Keys Across Job Classes -->
#### Sharing Lock Keys Across Job Classes

<!-- By default, the `WithoutOverlapping` middleware will only prevent overlapping jobs of the same class. So, although two different job classes may use the same lock key, they will not be prevented from overlapping. However, you can instruct Laravel to apply the key across job classes using the `shared` method: -->
デフォルトでは、`WithoutOverlapping` ミドルウェアは、同じクラスの重複ジョブのみを防止します。したがって、2 つの異なるジョブ クラスが同じロック キーを使用することはできますが、それらの重複は防止されません。ただし、`shared` メソッドを使用して、ジョブ クラス全体にキーを適用するように Laravel に指示できます。

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    // ...


    public function middleware()
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    // ...


    public function middleware()
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```

<a name="throttling-exceptions"></a>
<!-- ### Throttling Exceptions -->
### Throttling Exceptions

<!-- Laravel includes a `Illuminate\Queue\Middleware\ThrottlesExceptions` middleware that allows you to throttle exceptions. Once the job throws a given number of exceptions, all further attempts to execute the job are delayed until a specified time interval lapses. This middleware is particularly useful for jobs that interact with third-party services that are unstable. -->
Laravel には、例外を抑制できる `Illuminate\Queue\Middleware\ThrottlesExceptions` ミドルウェアが含まれています。ジョブが指定された数の例外をスローすると、それ以降のジョブの実行試行は、指定された時間が経過するまで遅延されます。このミドルウェアは、不安定なサードパーティ サービスと対話するジョブに特に役立ちます。

<!-- For example, let's imagine a queued job that interacts with a third-party API that begins throwing exceptions. To throttle exceptions, you can return the `ThrottlesExceptions` middleware from your job's `middleware` method. Typically, this middleware should be paired with a job that implements [time based attempts](#time-based-attempts): -->
たとえば、例外をスローし始めるサードパーティ API と対話する、キューに入れられたジョブを想像してみましょう。例外を抑制するには、ジョブの `middleware` メソッドから `ThrottlesExceptions` ミドルウェアを返すことができます。通常、このミドルウェアは、[time based attempts](#time-based-attempts) を実装するジョブと組み合わせる必要があります。

```
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new ThrottlesExceptions(10, 5)];
}

/**
 * Determine the time at which the job should timeout.
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(5);
}
```

<!-- The first constructor argument accepted by the middleware is the number of exceptions the job can throw before being throttled, while the second constructor argument is the number of minutes that should elapse before the job is attempted again once it has been throttled. In the code example above, if the job throws 10 exceptions within 5 minutes, we will wait 5 minutes before attempting the job again. -->
ミドルウェアによって受け入れられる最初のコンストラクター引数は、ジョブが調整される前にスローできる例外の数です。一方、2 番目のコンストラクター引数は、ジョブが調整された後にジョブが再試行されるまでに経過する必要がある分数です。上記のコード例では、ジョブが 5 分以内に 10 個の例外をスローした場合、5 分間待ってからジョブを再試行します。

<!-- When a job throws an exception but the exception threshold has not yet been reached, the job will typically be retried immediately. However, you may specify the number of minutes such a job should be delayed by calling the `backoff` method when attaching the middleware to the job: -->
ジョブが例外をスローしたが、まだ例外しきい値に達していない場合、ジョブは通常、すぐに再試行されます。ただし、ミドルウェアをジョブにアタッチするときに `backoff` メソッドを呼び出すことで、そのようなジョブを遅延させる分数を指定できます。

```
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new ThrottlesExceptions(10, 5))->backoff(5)];
}
```

<!-- Internally, this middleware uses Laravel's cache system to implement rate limiting, and the job's class name is utilized as the cache "key". You may override this key by calling the `by` method when attaching the middleware to your job. This may be useful if you have multiple jobs interacting with the same third-party service and you would like them to share a common throttling "bucket": -->
内部的には、このミドルウェアは Laravel のキャッシュ システムを使用してレート制限を実装し、ジョブのクラス名がキャッシュの「キー」として利用されます。ミドルウェアをジョブにアタッチするときに `by` メソッドを呼び出すことで、このキーをオーバーライドできます。これは、同じサードパーティ サービスと対話する複数のジョブがあり、それらのジョブに共通の調整「バケット」を共有したい場合に便利です。

```
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new ThrottlesExceptions(10, 10))->by('key')];
}
```

> [!NOTE]
> Redis を使用している場合は、`Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` ミドルウェアを使用できます。これは Redis 用に微調整されており、基本的な例外調整ミドルウェアよりも効率的です。

<a name="dispatching-jobs"></a>
<!-- ## Dispatching Jobs -->
## Dispatching Jobs

<!-- Once you have written your job class, you may dispatch it using the `dispatch` method on the job itself. The arguments passed to the `dispatch` method will be given to the job's constructor: -->
ジョブ クラスを作成したら、ジョブ自体で `dispatch` メソッドを使用してジョブ クラスをディスパッチできます。 `dispatch` メソッドに渡される引数は、ジョブのコンストラクターに渡されます。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);
    }
}
```

<!-- If you would like to conditionally dispatch a job, you may use the `dispatchIf` and `dispatchUnless` methods: -->
条件付きでジョブをディスパッチしたい場合は、`dispatchIf` メソッドと `dispatchUnless` メソッドを使用できます。

```
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

<!-- In new Laravel applications, the `sync` driver is the default queue driver. This driver executes jobs synchronously in the foreground of the current request, which is often convenient during local development. If you would like to actually begin queueing jobs for background processing, you may specify a different queue driver within your application's `config/queue.php` configuration file. -->
新しい Laravel アプリケーションでは、`sync` ドライバがデフォルトのキュードライバです。このドライバは、現在のリクエストのフォアグラウンドでジョブを同期的に実行します。これは、ローカル開発中に便利なことがよくあります。実際にバックグラウンド処理のためにジョブのキューイングを開始したい場合は、アプリケーションの `config/queue.php` 構成ファイル内で別のキュー ドライバを指定できます。

<a name="delayed-dispatching"></a>
<!-- ### Delayed Dispatching -->
### Delayed Dispatching

<!-- If you would like to specify that a job should not be immediately available for processing by a queue worker, you may use the `delay` method when dispatching the job. For example, let's specify that a job should not be available for processing until 10 minutes after it has been dispatched: -->
ジョブをキューワーカーによる処理にすぐに使用できないように指定したい場合は、ジョブをディスパッチするときに `delay` メソッドを使用できます。たとえば、ジョブがディスパッチされてから 10 分が経過するまではジョブを処理できないように指定しましょう。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)
                    ->delay(now()->addMinutes(10));
    }
}
```

> [!WARNING]
> Amazon SQS キュー サービスの最大遅延時間は 15 分です。

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
<!-- #### Dispatching After The Response Is Sent To Browser -->
#### Dispatching After The Response Is Sent To Browser

<!-- Alternatively, the `dispatchAfterResponse` method delays dispatching a job until after the HTTP response is sent to the user's browser if your web server is using FastCGI. This will still allow the user to begin using the application even though a queued job is still executing. This should typically only be used for jobs that take about a second, such as sending an email. Since they are processed within the current HTTP request, jobs dispatched in this fashion do not require a queue worker to be running in order for them to be processed: -->
あるいは、Web サーバーが FastCGI を使用している場合、`dispatchAfterResponse` メソッドは、HTTP 応答がユーザーのブラウザーに送信されるまでジョブのディスパッチを遅らせます。これにより、キューに入れられたジョブがまだ実行中であっても、ユーザーはアプリケーションの使用を開始できます。これは通常、電子メールの送信など、約 1 秒かかるジョブにのみ使用してください。これらは現在の HTTP リクエスト内で処理されるため、この方法でディスパッチされたジョブは、処理するためにキューワーカーを実行する必要はありません。

```
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

<!-- You may also `dispatch` a closure and chain the `afterResponse` method onto the `dispatch` helper to execute a closure after the HTTP response has been sent to the browser: -->
また、`dispatch` クロージャーを作成し、`afterResponse` メソッドを `dispatch` ヘルパにチェーンして、HTTP 応答がブラウザーに送信された後にクロージャーを実行することもできます。

```
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
<!-- ### Synchronous Dispatching -->
### Synchronous Dispatching

<!-- If you would like to dispatch a job immediately (synchronously), you may use the `dispatchSync` method. When using this method, the job will not be queued and will be executed immediately within the current process: -->
ジョブをすぐに (同期的に) ディスパッチしたい場合は、`dispatchSync` メソッドを使用できます。この方法を使用すると、ジョブはキューに入れられず、現在のプロセス内ですぐに実行されます。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);
    }
}
```

<a name="jobs-and-database-transactions"></a>
<!-- ### Jobs & Database Transactions -->
### Jobs & Database Transactions

<!-- While it is perfectly fine to dispatch jobs within database transactions, you should take special care to ensure that your job will actually be able to execute successfully. When dispatching a job within a transaction, it is possible that the job will be processed by a worker before the parent transaction has committed. When this happens, any updates you have made to models or database records during the database transaction(s) may not yet be reflected in the database. In addition, any models or database records created within the transaction(s) may not exist in the database. -->
データベース トランザクション内でジョブをディスパッチすることはまったく問題ありませんが、ジョブが実際に正常に実行できることを確認するために特別な注意を払う必要があります。トランザクション内でジョブをディスパッチする場合、親トランザクションがコミットされる前にジョブがワーカーによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに加えた更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。

<!-- Thankfully, Laravel provides several methods of working around this problem. First, you may set the `after_commit` connection option in your queue connection's configuration array: -->
ありがたいことに、Laravel はこの問題を回避する方法をいくつか提供しています。まず、キュー接続の構成配列で `after_commit` 接続オプションを設定します。

```
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

<!-- When the `after_commit` option is `true`, you may dispatch jobs within database transactions; however, Laravel will wait until the open parent database transactions have been committed before actually dispatching the job. Of course, if no database transactions are currently open, the job will be dispatched immediately. -->
`after_commit` オプションが `true` の場合、データベース トランザクション内でジョブをディスパッチできます。ただし、Laravel は、実際にジョブをディスパッチする前に、開いている親データベースのトランザクションがコミットされるまで待機します。もちろん、現在開いているデータベース トランザクションがない場合、ジョブはすぐにディスパッチされます。

<!-- If a transaction is rolled back due to an exception that occurs during the transaction, the jobs that were dispatched during that transaction will be discarded. -->
トランザクション中に発生した例外によりトランザクションがロールバックされた場合、そのトランザクション中にディスパッチされたジョブは破棄されます。

> [!NOTE]
> `after_commit` 構成オプションを `true` に設定すると、開いているすべてのデータベース トランザクションがコミットされた後に、キューに入れられたイベント リスナ、メール可能ファイル、通知、およびブロードキャスト イベントもディスパッチされます。

<a name="specifying-commit-dispatch-behavior-inline"></a>
<!-- #### Specifying Commit Dispatch Behavior Inline -->
#### Specifying Commit Dispatch Behavior Inline

<!-- If you do not set the `after_commit` queue connection configuration option to `true`, you may still indicate that a specific job should be dispatched after all open database transactions have been committed. To accomplish this, you may chain the `afterCommit` method onto your dispatch operation: -->
`after_commit` キュー接続構成オプションを `true` に設定しない場合でも、開いているすべてのデータベース トランザクションがコミットされた後に特定のジョブをディスパッチする必要があることを示すことができます。これを実現するには、`afterCommit` メソッドをディスパッチ操作に連鎖させます。

```
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

<!-- Likewise, if the `after_commit` configuration option is set to `true`, you may indicate that a specific job should be dispatched immediately without waiting for any open database transactions to commit: -->
同様に、`after_commit` 構成オプションが `true` に設定されている場合は、開いているデータベース トランザクションがコミットされるのを待たずに、特定のジョブを直ちにディスパッチする必要があることを指定できます。

```
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
<!-- ### Job Chaining -->
### Job Chaining

<!-- Job chaining allows you to specify a list of queued jobs that should be run in sequence after the primary job has executed successfully. If one job in the sequence fails, the rest of the jobs will not be run. To execute a queued job chain, you may use the `chain` method provided by the `Bus` facade. Laravel's command bus is a lower level component that queued job dispatching is built on top of: -->
ジョブ チェーンを使用すると、プライマリ ジョブが正常に実行された後に順番に実行する必要がある、キューに入れられたジョブのリストを指定できます。シーケンス内の 1 つのジョブが失敗すると、残りのジョブは実行されません。キューに入れられたジョブ チェーンを実行するには、`Bus` ファサードによって提供される `chain` メソッドを使用できます。 Laravel のコマンド バスは、キューに入れられたジョブのディスパッチがその上に構築される下位レベルのコンポーネントです。

```
use App\Jobs\OptimizePodcast;
use App\Jobs\ProcessPodcast;
use App\Jobs\ReleasePodcast;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->dispatch();
```

<!-- In addition to chaining job class instances, you may also chain closures: -->
ジョブ クラス インスタンスをチェーンすることに加えて、クロージャをチェーンすることもできます。

```
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(/* ... */);
    },
])->dispatch();
```

> [!WARNING]
> ジョブ内で `$this->delete()` メソッドを使用してジョブを削除しても、チェーンされたジョブの処理は妨げられません。チェーンは、チェーン内のジョブが失敗した場合にのみ実行を停止します。

<a name="chain-connection-queue"></a>
<!-- #### Chain Connection & Queue -->
#### Chain Connection & Queue

<!-- If you would like to specify the connection and queue that should be used for the chained jobs, you may use the `onConnection` and `onQueue` methods. These methods specify the queue connection and queue name that should be used unless the queued job is explicitly assigned a different connection / queue: -->
連鎖ジョブに使用する接続とキューを指定したい場合は、`onConnection` メソッドと `onQueue` メソッドを使用できます。これらのメソッドは、キューに入れられたジョブに別の接続/キューが明示的に割り当てられていない限り、使用する必要があるキュー接続とキュー名を指定します。

```
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="chain-failures"></a>
<!-- #### Chain Failures -->
#### Chain Failures

<!-- When chaining jobs, you may use the `catch` method to specify a closure that should be invoked if a job within the chain fails. The given callback will receive the `Throwable` instance that caused the job failure: -->
ジョブをチェーンする場合、`catch` メソッドを使用して、チェーン内のジョブが失敗した場合に呼び出されるクロージャーを指定できます。指定されたコールバックは、ジョブの失敗の原因となった `Throwable` インスタンスを受け取ります。

```
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // A job within the chain has failed...
})->dispatch();
```

> [!WARNING]
> チェーン コールバックはシリアル化され、後で Laravel キューによって実行されるため、チェーン コールバック内で `$this` 変数を使用しないでください。

<a name="customizing-the-queue-and-connection"></a>
<!-- ### Customizing The Queue & Connection -->
### Customizing The Queue & Connection

<a name="dispatching-to-a-particular-queue"></a>
<!-- #### Dispatching To A Particular Queue -->
#### Dispatching To A Particular Queue

<!-- By pushing jobs to different queues, you may "categorize" your queued jobs and even prioritize how many workers you assign to various queues. Keep in mind, this does not push jobs to different queue "connections" as defined by your queue configuration file, but only to specific queues within a single connection. To specify the queue, use the `onQueue` method when dispatching the job: -->
ジョブを異なるキューにプッシュすることで、キューに入れられたジョブを「分類」し、さまざまなキューに割り当てるワーカーの数に優先順位を付けることもできます。これは、キュー構成ファイルで定義されている別のキュー「接続」にジョブをプッシュするのではなく、単一の接続内の特定のキューにのみジョブをプッシュすることに注意してください。キューを指定するには、ジョブをディスパッチするときに `onQueue` メソッドを使用します。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');
    }
}
```

<!-- Alternatively, you may specify the job's queue by calling the `onQueue` method within the job's constructor: -->
あるいは、ジョブのコンストラクター内で `onQueue` メソッドを呼び出して、ジョブのキューを指定することもできます。

```
<?php

namespace App\Jobs;

 use Illuminate\Bus\Queueable;
 use Illuminate\Contracts\Queue\ShouldQueue;
 use Illuminate\Foundation\Bus\Dispatchable;
 use Illuminate\Queue\InteractsWithQueue;
 use Illuminate\Queue\SerializesModels;

class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
<!-- #### Dispatching To A Particular Connection -->
#### Dispatching To A Particular Connection

<!-- If your application interacts with multiple queue connections, you may specify which connection to push a job to using the `onConnection` method: -->
アプリケーションが複数のキュー接続と対話する場合は、`onConnection` メソッドを使用してジョブをプッシュする接続を指定できます。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');
    }
}
```

<!-- You may chain the `onConnection` and `onQueue` methods together to specify the connection and the queue for a job: -->
`onConnection` メソッドと `onQueue` メソッドを連鎖させて、ジョブの接続とキューを指定できます。

```
ProcessPodcast::dispatch($podcast)
              ->onConnection('sqs')
              ->onQueue('processing');
```

<!-- Alternatively, you may specify the job's connection by calling the `onConnection` method within the job's constructor: -->
あるいは、ジョブのコンストラクター内で `onConnection` メソッドを呼び出して、ジョブの接続を指定することもできます。

```
<?php

namespace App\Jobs;

 use Illuminate\Bus\Queueable;
 use Illuminate\Contracts\Queue\ShouldQueue;
 use Illuminate\Foundation\Bus\Dispatchable;
 use Illuminate\Queue\InteractsWithQueue;
 use Illuminate\Queue\SerializesModels;

class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>
<!-- ### Specifying Max Job Attempts / Timeout Values -->
### Specifying Max Job Attempts / Timeout Values

<a name="max-attempts"></a>
<!-- #### Max Attempts -->
#### Max Attempts

<!-- If one of your queued jobs is encountering an error, you likely do not want it to keep retrying indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a job may be attempted. -->
キューに入れられたジョブの 1 つでエラーが発生した場合、そのジョブが無期限に再試行され続けることは望ましくありません。したがって、Laravel では、ジョブを試行する回数や期間を指定するさまざまな方法が提供されています。

<!-- One approach to specifying the maximum number of times a job may be attempted is via the `--tries` switch on the Artisan command line. This will apply to all jobs processed by the worker unless the job being processed specifies the number of times it may be attempted: -->
ジョブの最大試行回数を指定する方法の 1 つは、Artisan コマンド ラインの `--tries` スイッチを使用することです。これは、処理中のジョブで試行回数が指定されていない限り、ワーカーによって処理されるすべてのジョブに適用されます。

```shell
php artisan queue:work --tries=3
```

<!-- If a job exceeds its maximum number of attempts, it will be considered a "failed" job. For more information on handling failed jobs, consult the [failed job documentation](#dealing-with-failed-jobs). If `--tries=0` is provided to the `queue:work` command, the job will be retried indefinitely. -->
ジョブが最大試行回数を超えた場合、そのジョブは「失敗した」ジョブとみなされます。失敗したジョブの処理の詳細については、[failed job documentation](#dealing-with-failed-jobs) を参照してください。 `--tries=0` が `queue:work` コマンドに指定された場合、ジョブは無期限に再試行されます。

<!-- You may take a more granular approach by defining the maximum number of times a job may be attempted on the job class itself. If the maximum number of attempts is specified on the job, it will take precedence over the `--tries` value provided on the command line: -->
ジョブ クラス自体でジョブを試行できる最大回数を定義することで、より詳細なアプローチを採用することもできます。ジョブで最大試行回数が指定されている場合は、コマンド ラインで指定した `--tries` 値よりも優先されます。

```
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
```

<a name="time-based-attempts"></a>
<!-- #### Time Based Attempts -->
#### Time Based Attempts

<!-- As an alternative to defining how many times a job may be attempted before it fails, you may define a time at which the job should no longer be attempted. This allows a job to be attempted any number of times within a given time frame. To define the time at which a job should no longer be attempted, add a `retryUntil` method to your job class. This method should return a `DateTime` instance: -->
ジョブが失敗するまでに何回試行できるかを定義する代わりに、ジョブを試行しなくなる時間を定義することもできます。これにより、指定された時間枠内でジョブを何度でも試行できます。ジョブを試行しなくなる時刻を定義するには、`retryUntil` メソッドをジョブ クラスに追加します。このメソッドは `DateTime` インスタンスを返す必要があります。

```
/**
 * Determine the time at which the job should timeout.
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(10);
}
```

> [!NOTE]
> [queued event listeners](/docs/9.x/events#queued-event-listeners) で `tries` プロパティまたは `retryUntil` メソッドを定義することもできます。

<a name="max-exceptions"></a>
<!-- #### Max Exceptions -->
#### Max Exceptions

<!-- Sometimes you may wish to specify that a job may be attempted many times, but should fail if the retries are triggered by a given number of unhandled exceptions (as opposed to being released by the `release` method directly). To accomplish this, you may define a `maxExceptions` property on your job class: -->
場合によっては、ジョブを何度も試行できるが、(`release` メソッドによって直接解放されるのではなく) 指定された数の未処理の例外によって再試行がトリガーされた場合は失敗するように指定したい場合があります。これを実現するには、ジョブ クラスで `maxExceptions` プロパティを定義します。

```
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
     *
     * @return void
     */
    public function handle()
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // Lock obtained, process the podcast...
        }, function () {
            // Unable to obtain lock...
            return $this->release(10);
        });
    }
}
```

<!-- In this example, the job is released for ten seconds if the application is unable to obtain a Redis lock and will continue to be retried up to 25 times. However, the job will fail if three unhandled exceptions are thrown by the job. -->
この例では、アプリケーションが Redis ロックを取得できない場合、ジョブは 10 秒間解放され、最大 25 回まで再試行され続けます。ただし、ジョブによって 3 つの未処理の例外がスローされた場合、ジョブは失敗します。

<a name="timeout"></a>
<!-- #### Timeout -->
#### Timeout

> [!WARNING]
> ジョブのタイムアウトを指定するには、`pcntl` PHP 拡張機能をインストールする必要があります。

<!-- Often, you know roughly how long you expect your queued jobs to take. For this reason, Laravel allows you to specify a "timeout" value. By default, the timeout value is 60 seconds. If a job is processing for longer than the number of seconds specified by the timeout value, the worker processing the job will exit with an error. Typically, the worker will be restarted automatically by a [process manager configured on your server](#supervisor-configuration). -->
多くの場合、キューに入れられたジョブにかかる時間がおおよそわかっています。このため、Laravel では「タイムアウト」値を指定できます。デフォルトでは、タイムアウト値は 60 秒です。ジョブの処理がタイムアウト値で指定された秒数を超えた場合、ジョブを処理しているワーカーはエラーで終了します。通常、ワーカーは [process manager configured on your server](#supervisor-configuration) によって自動的に再起動されます。

<!-- The maximum number of seconds that jobs can run may be specified using the `--timeout` switch on the Artisan command line: -->
ジョブを実行できる最大秒数は、Artisan コマンド ラインで `--timeout` スイッチを使用して指定できます。

```shell
php artisan queue:work --timeout=30
```

<!-- If the job exceeds its maximum attempts by continually timing out, it will be marked as failed. -->
ジョブがタイムアウトを繰り返して最大試行回数を超えると、ジョブは失敗としてマークされます。

<!-- You may also define the maximum number of seconds a job should be allowed to run on the job class itself. If the timeout is specified on the job, it will take precedence over any timeout specified on the command line: -->
ジョブ クラス自体でジョブの実行を許可する最大秒数を定義することもできます。ジョブでタイムアウトが指定されている場合は、コマンド ラインで指定されたタイムアウトよりも優先されます。

```
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
```

<!-- Sometimes, IO blocking processes such as sockets or outgoing HTTP connections may not respect your specified timeout. Therefore, when using these features, you should always attempt to specify a timeout using their APIs as well. For example, when using Guzzle, you should always specify a connection and request timeout value. -->
場合によっては、ソケットや発信 HTTP 接続などの IO ブロック プロセスが、指定されたタイムアウトを尊重しないことがあります。したがって、これらの機能を使用するときは、常にその API も使用してタイムアウトを指定するようにしてください。たとえば、Guzzle を使用する場合は、常に接続とリクエストのタイムアウト値を指定する必要があります。

<a name="failing-on-timeout"></a>
<!-- #### Failing On Timeout -->
#### Failing On Timeout

<!-- If you would like to indicate that a job should be marked as [failed](#dealing-with-failed-jobs) on timeout, you may define the `$failOnTimeout` property on the job class: -->
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
<!-- ### Error Handling -->
### Error Handling

<!-- If an exception is thrown while the job is being processed, the job will automatically be released back onto the queue so it may be attempted again. The job will continue to be released until it has been attempted the maximum number of times allowed by your application. The maximum number of attempts is defined by the `--tries` switch used on the `queue:work` Artisan command. Alternatively, the maximum number of attempts may be defined on the job class itself. More information on running the queue worker [can be found below](#running-the-queue-worker). -->
ジョブの処理中に例外がスローされた場合、ジョブは自動的にキューに解放され、再試行できるようになります。ジョブは、アプリケーションで許可されている最大回数試行されるまで解放され続けます。最大試行回数は、`queue:work` Artisan コマンドで使用される `--tries` スイッチによって定義されます。あるいは、最大試行回数をジョブ クラス自体に定義することもできます。キューワーカー [can be found below](#running-the-queue-worker) の実行に関する詳細情報。

<a name="manually-releasing-a-job"></a>
<!-- #### Manually Releasing A Job -->
#### Manually Releasing A Job

<!-- Sometimes you may wish to manually release a job back onto the queue so that it can be attempted again at a later time. You may accomplish this by calling the `release` method: -->
場合によっては、ジョブを手動で解放してキューに戻し、後で再試行できるようにしたい場合があります。これを行うには、`release` メソッドを呼び出します。

```
/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    // ...

    $this->release();
}
```

<!-- By default, the `release` method will release the job back onto the queue for immediate processing. However, by passing an integer to the `release` method you may instruct the queue to not make the job available for processing until a given number of seconds has elapsed: -->
デフォルトでは、`release` メソッドはジョブをキューに解放して即時処理します。ただし、整数を `release` メソッドに渡すことで、指定した秒数が経過するまでジョブを処理できないようにキューに指示できます。

```
$this->release(10);
```

<a name="manually-failing-a-job"></a>
<!-- #### Manually Failing A Job -->
#### Manually Failing A Job

<!-- Occasionally you may need to manually mark a job as "failed". To do so, you may call the `fail` method: -->
場合によっては、ジョブを手動で「失敗」としてマークする必要がある場合があります。これを行うには、`fail` メソッドを呼び出します。

```
/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    // ...

    $this->fail();
}
```

<!-- If you would like to mark your job as failed because of an exception that you have caught, you may pass the exception to the `fail` method. Or, for convenience, you may pass a string error message which will be converted to an exception for you: -->
キャッチした例外のためにジョブを失敗としてマークしたい場合は、例外を `fail` メソッドに渡すことができます。または、便宜上、例外に変換される文字列エラー メッセージを渡すこともできます。

```
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 失敗したジョブの詳細については、[documentation on dealing with job failures](#dealing-with-failed-jobs) を確認してください。

<a name="job-batching"></a>
<!-- ## Job Batching -->
## Job Batching

<!-- Laravel's job batching feature allows you to easily execute a batch of jobs and then perform some action when the batch of jobs has completed executing. Before getting started, you should create a database migration to build a table to contain meta information about your job batches, such as their completion percentage. This migration may be generated using the `queue:batches-table` Artisan command: -->
Laravel のジョブバッチ機能を使用すると、ジョブのバッチを簡単に実行し、ジョブのバッチの実行が完了したときに何らかのアクションを実行できます。開始する前に、データベース移行を作成して、完了率などのジョブ バッチに関するメタ情報を含むテーブルを構築する必要があります。この移行は、`queue:batches-table` Artisan コマンドを使用して生成できます。

```shell
php artisan queue:batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
<!-- ### Defining Batchable Jobs -->
### Defining Batchable Jobs

<!-- To define a batchable job, you should [create a queueable job](#creating-jobs) as normal; however, you should add the `Illuminate\Bus\Batchable` trait to the job class. This trait provides access to a `batch` method which may be used to retrieve the current batch that the job is executing within: -->
バッチ可能ジョブを定義するには、通常どおり [create a queueable job](#creating-jobs) を実行する必要があります。ただし、ジョブ クラスに `Illuminate\Bus\Batchable` 特性を追加する必要があります。この特性は、ジョブが実行されている現在のバッチを取得するために使用できる `batch` メソッドへのアクセスを提供します。

```
<?php

namespace App\Jobs;

use Illuminate\Bus\Batchable;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ImportCsv implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        if ($this->batch()->cancelled()) {
            // Determine if the batch has been cancelled...

            return;
        }

        // Import a portion of the CSV file...
    }
}
```

<a name="dispatching-batches"></a>
<!-- ### Dispatching Batches -->
### Dispatching Batches

<!-- To dispatch a batch of jobs, you should use the `batch` method of the `Bus` facade. Of course, batching is primarily useful when combined with completion callbacks. So, you may use the `then`, `catch`, and `finally` methods to define completion callbacks for the batch. Each of these callbacks will receive an `Illuminate\Bus\Batch` instance when they are invoked. In this example, we will imagine we are queueing a batch of jobs that each process a given number of rows from a CSV file: -->
ジョブのバッチをディスパッチするには、`Bus` ファサードの `batch` メソッドを使用する必要があります。もちろん、バッチ処理は主に完了コールバックと組み合わせると便利です。したがって、`then`、`catch`、および `finally` メソッドを使用して、バッチの完了コールバックを定義できます。これらの各コールバックは、呼び出されるときに `Illuminate\Bus\Batch` インスタンスを受け取ります。この例では、CSV ファイルの指定された行数をそれぞれ処理するジョブのバッチをキューに入れていると想定します。

```
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
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->catch(function (Batch $batch, Throwable $e) {
    // First batch job failure detected...
})->finally(function (Batch $batch) {
    // The batch has finished executing...
})->dispatch();

return $batch->id;
```

<!-- The batch's ID, which may be accessed via the `$batch->id` property, may be used to [query the Laravel command bus](#inspecting-batches) for information about the batch after it has been dispatched. -->
`$batch->id` プロパティを介してアクセスできるバッチの ID は、発送後のバッチに関する情報を得るために [query the Laravel command bus](#inspecting-batches) に使用できます。

> [!WARNING]
> バッチコールバックはシリアル化され、後でLaravelキューによって実行されるため、コールバック内で`$this`変数を使用しないでください。

<a name="naming-batches"></a>
<!-- #### Naming Batches -->
#### Naming Batches

<!-- Some tools such as Laravel Horizon and Laravel Telescope may provide more user-friendly debug information for batches if batches are named. To assign an arbitrary name to a batch, you may call the `name` method while defining the batch: -->
Laravel Horizon や Laravel Telescope などの一部のツールでは、バッチに名前が付けられている場合、バッチのより使いやすいデバッグ情報が提供される場合があります。バッチに任意の名前を割り当てるには、バッチの定義中に `name` メソッドを呼び出すことができます。

```
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
<!-- #### Batch Connection & Queue -->
#### Batch Connection & Queue

<!-- If you would like to specify the connection and queue that should be used for the batched jobs, you may use the `onConnection` and `onQueue` methods. All batched jobs must execute within the same connection and queue: -->
バッチジョブに使用する接続とキューを指定したい場合は、`onConnection` メソッドと `onQueue` メソッドを使用できます。すべてのバッチ ジョブは、同じ接続およびキュー内で実行する必要があります。

```
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-within-batches"></a>
<!-- #### Chains Within Batches -->
#### Chains Within Batches

<!-- You may define a set of [chained jobs](#job-chaining) within a batch by placing the chained jobs within an array. For example, we may execute two job chains in parallel and execute a callback when both job chains have finished processing: -->
チェーンされたジョブを配列内に配置することで、バッチ内で [chained jobs](#job-chaining) のセットを定義できます。たとえば、2 つのジョブ チェーンを並行して実行し、両方のジョブ チェーンの処理が完了したときにコールバックを実行できます。

```
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
```

<a name="adding-jobs-to-batches"></a>
<!-- ### Adding Jobs To Batches -->
### Adding Jobs To Batches

<!-- Sometimes it may be useful to add additional jobs to a batch from within a batched job. This pattern can be useful when you need to batch thousands of jobs which may take too long to dispatch during a web request. So, instead, you may wish to dispatch an initial batch of "loader" jobs that hydrate the batch with even more jobs: -->
場合によっては、バッチ処理されたジョブ内からバッチにジョブを追加すると便利な場合があります。このパターンは、Web リクエスト中にディスパッチするのに時間がかかりすぎる可能性がある数千のジョブをバッチ処理する必要がある場合に役立ちます。したがって、代わりに、バッチにさらに多くのジョブを追加する「ローダー」ジョブの最初のバッチをディスパッチすることもできます。

```
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import Contacts')->dispatch();
```

<!-- In this example, we will use the `LoadImportBatch` job to hydrate the batch with additional jobs. To accomplish this, we may use the `add` method on the batch instance that may be accessed via the job's `batch` method: -->
この例では、`LoadImportBatch` ジョブを使用して、追加のジョブでバッチをハイドレートします。これを実現するには、ジョブの `batch` メソッドを介してアクセスできるバッチ インスタンスで `add` メソッドを使用します。

```
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    if ($this->batch()->cancelled()) {
        return;
    }

    $this->batch()->add(Collection::times(1000, function () {
        return new ImportContacts;
    }));
}
```

> [!WARNING]
> ジョブをバッチに追加できるのは、同じバッチに属するジョブ内からのみです。

<a name="inspecting-batches"></a>
<!-- ### Inspecting Batches -->
### Inspecting Batches

<!-- The `Illuminate\Bus\Batch` instance that is provided to batch completion callbacks has a variety of properties and methods to assist you in interacting with and inspecting a given batch of jobs: -->
バッチ完了コールバックに提供される `Illuminate\Bus\Batch` インスタンスには、特定のジョブのバッチの操作と検査を支援するさまざまなプロパティとメソッドがあります。

```
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
```

<a name="returning-batches-from-routes"></a>
<!-- #### Returning Batches From Routes -->
#### Returning Batches From Routes

<!-- All `Illuminate\Bus\Batch` instances are JSON serializable, meaning you can return them directly from one of your application's routes to retrieve a JSON payload containing information about the batch, including its completion progress. This makes it convenient to display information about the batch's completion progress in your application's UI. -->
すべての `Illuminate\Bus\Batch` インスタンスは JSON シリアル化可能です。つまり、アプリケーションのルートの 1 つから直接インスタンスを返し、完了の進行状況など、バッチに関する情報を含む JSON ペイロードを取得できます。これにより、バッチの完了の進行状況に関する情報をアプリケーションの UI に表示するのが便利になります。

<!-- To retrieve a batch by its ID, you may use the `Bus` facade's `findBatch` method: -->
ID でバッチを取得するには、`Bus` ファサードの `findBatch` メソッドを使用できます。

```
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
<!-- ### Cancelling Batches -->
### Cancelling Batches

<!-- Sometimes you may need to cancel a given batch's execution. This can be accomplished by calling the `cancel` method on the `Illuminate\Bus\Batch` instance: -->
場合によっては、特定のバッチの実行をキャンセルする必要がある場合があります。これは、`Illuminate\Bus\Batch` インスタンスで `cancel` メソッドを呼び出すことで実現できます。

```
/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    if ($this->user->exceedsImportLimit()) {
        return $this->batch()->cancel();
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```

<!-- As you may have noticed in the previous examples, batched jobs should typically determine if their corresponding batch has been cancelled before continuing execution. However, for convenience, you may assign the `SkipIfBatchCancelled` [middleware](#job-middleware) to the job instead. As its name indicates, this middleware will instruct Laravel to not process the job if its corresponding batch has been cancelled: -->
前の例でお気づきかと思いますが、バッチ処理されたジョブは通常、実行を続行する前に、対応するバッチがキャンセルされたかどうかを判断する必要があります。ただし、便宜上、代わりに `SkipIfBatchCancelled` [middleware](#job-middleware) をジョブに割り当てることもできます。その名前が示すように、このミドルウェアは、対応するバッチがキャンセルされた場合にジョブを処理しないように Laravel に指示します。

```
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
<!-- ### Batch Failures -->
### Batch Failures

<!-- When a batched job fails, the `catch` callback (if assigned) will be invoked. This callback is only invoked for the first job that fails within the batch. -->
バッチ処理されたジョブが失敗すると、`catch` コールバック (割り当てられている場合) が呼び出されます。このコールバックは、バッチ内で失敗した最初のジョブに対してのみ呼び出されます。

<a name="allowing-failures"></a>
<!-- #### Allowing Failures -->
#### Allowing Failures

<!-- When a job within a batch fails, Laravel will automatically mark the batch as "cancelled". If you wish, you may disable this behavior so that a job failure does not automatically mark the batch as cancelled. This may be accomplished by calling the `allowFailures` method while dispatching the batch: -->
バッチ内のジョブが失敗すると、Laravel は自動的にバッチを「キャンセル」としてマークします。必要に応じて、ジョブの失敗によってバッチが自動的にキャンセルとしてマークされないように、この動作を無効にすることができます。これは、バッチのディスパッチ中に `allowFailures` メソッドを呼び出すことで実現できます。

```
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
<!-- #### Retrying Failed Batch Jobs -->
#### Retrying Failed Batch Jobs

<!-- For convenience, Laravel provides a `queue:retry-batch` Artisan command that allows you to easily retry all of the failed jobs for a given batch. The `queue:retry-batch` command accepts the UUID of the batch whose failed jobs should be retried: -->
便宜上、Laravel には、特定のバッチで失敗したすべてのジョブを簡単に再試行できる `queue:retry-batch` Artisan コマンドが用意されています。 `queue:retry-batch` コマンドは、失敗したジョブを再試行する必要があるバッチの UUID を受け入れます。

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
<!-- ### Pruning Batches -->
### Pruning Batches

<!-- Without pruning, the `job_batches` table can accumulate records very quickly. To mitigate this, you should [schedule](/docs/9.x/scheduling) the `queue:prune-batches` Artisan command to run daily: -->
プルーニングを行わない場合、`job_batches` テーブルは非常に迅速にレコードを蓄積できます。これを軽減するには、[schedule](/docs/9.x/scheduling) `queue:prune-batches` Artisan コマンドを毎日実行する必要があります。

```
$schedule->command('queue:prune-batches')->daily();
```

<!-- By default, all finished batches that are more than 24 hours old will be pruned. You may use the `hours` option when calling the command to determine how long to retain batch data. For example, the following command will delete all batches that finished over 48 hours ago: -->
デフォルトでは、24 時間以上経過した完了したバッチはすべて削除されます。コマンドを呼び出すときに `hours` オプションを使用して、バッチ データを保持する期間を決定できます。たとえば、次のコマンドは 48 時間以上前に終了したすべてのバッチを削除します。

```
$schedule->command('queue:prune-batches --hours=48')->daily();
```

<!-- Sometimes, your `jobs_batches` table may accumulate batch records for batches that never completed successfully, such as batches where a job failed and that job was never retried successfully. You may instruct the `queue:prune-batches` command to prune these unfinished batch records using the `unfinished` option: -->
場合によっては、`jobs_batches` テーブルに、ジョブが失敗し、そのジョブが正常に再試行されなかったバッチなど、正常に完了しなかったバッチのバッチ レコードが蓄積されることがあります。 `unfinished` オプションを使用して、これらの未完了のバッチ レコードを削除するように `queue:prune-batches` コマンドに指示できます。

```
$schedule->command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

<!-- Likewise, your `jobs_batches` table may also accumulate batch records for cancelled batches. You may instruct the `queue:prune-batches` command to prune these cancelled batch records using the `cancelled` option: -->
同様に、`jobs_batches` テーブルにも、キャンセルされたバッチのバッチ レコードが蓄積される場合があります。 `cancelled` オプションを使用して、これらのキャンセルされたバッチ レコードを削除するように `queue:prune-batches` コマンドに指示できます。

```
$schedule->command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="queueing-closures"></a>
<!-- ## Queueing Closures -->
## Queueing Closures

<!-- Instead of dispatching a job class to the queue, you may also dispatch a closure. This is great for quick, simple tasks that need to be executed outside of the current request cycle. When dispatching closures to the queue, the closure's code content is cryptographically signed so that it can not be modified in transit: -->
ジョブ クラスをキューにディスパッチする代わりに、クロージャをディスパッチすることもできます。これは、現在のリクエスト サイクルの外で実行する必要がある迅速で単純なタスクに最適です。クロージャをキューにディスパッチするとき、クロージャのコード コンテンツは暗号的に署名されるため、転送中に変更することはできません。

```
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

<!-- Using the `catch` method, you may provide a closure that should be executed if the queued closure fails to complete successfully after exhausting all of your queue's [configured retry attempts](#max-job-attempts-and-timeout): -->
`catch` メソッドを使用すると、キューの [configured retry attempts](#max-job-attempts-and-timeout) をすべて使い果たした後にキューに入れられたクロージャが正常に完了しなかった場合に実行されるクロージャを指定できます。

```
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

> [!WARNING]
> `catch` コールバックはシリアル化され、後で Laravel キューによって実行されるため、`catch` コールバック内で `$this` 変数を使用しないでください。

<a name="running-the-queue-worker"></a>
<!-- ## Running The Queue Worker -->
## Running The Queue Worker

<a name="the-queue-work-command"></a>
<!-- ### The `queue:work` Command -->
### The `queue:work` Command

<!-- Laravel includes an Artisan command that will start a queue worker and process new jobs as they are pushed onto the queue. You may run the worker using the `queue:work` Artisan command. Note that once the `queue:work` command has started, it will continue to run until it is manually stopped or you close your terminal: -->
Laravel には、キューワーカーを起動し、新しいジョブがキューにプッシュされるときに処理する Artisan コマンドが含まれています。 `queue:work` Artisan コマンドを使用してワーカーを実行できます。 `queue:work` コマンドが開始されると、手動で停止するかターミナルを閉じるまで実行が継続されることに注意してください。

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` プロセスをバックグラウンドで永続的に実行し続けるには、[Supervisor](#supervisor-configuration) などのプロセス モニターを使用して、キューワーカーの実行が停止しないようにする必要があります。

<!-- You may include the `-v` flag when invoking the `queue:work` command if you would like the processed job IDs to be included in the command's output: -->
処理されたジョブ ID をコマンドの出力に含めたい場合は、`queue:work` コマンドを呼び出すときに `-v` フラグを含めることができます。

```shell
php artisan queue:work -v
```

<!-- Remember, queue workers are long-lived processes and store the booted application state in memory. As a result, they will not notice changes in your code base after they have been started. So, during your deployment process, be sure to [restart your queue workers](#queue-workers-and-deployment). In addition, remember that any static state created or modified by your application will not be automatically reset between jobs. -->
キューワーカーは存続期間の長いプロセスであり、起動されたアプリケーションの状態をメモリに保存することに注意してください。その結果、開始後のコードベースの変更に気付かなくなります。したがって、展開プロセス中は、必ず [restart your queue workers](#queue-workers-and-deployment) を行ってください。さらに、アプリケーションによって作成または変更された静的状態は、ジョブ間で自動的にリセットされないことに注意してください。

<!-- Alternatively, you may run the `queue:listen` command. When using the `queue:listen` command, you don't have to manually restart the worker when you want to reload your updated code or reset the application state; however, this command is significantly less efficient than the `queue:work` command: -->
あるいは、`queue:listen` コマンドを実行することもできます。 `queue:listen` コマンドを使用すると、更新されたコードをリロードしたり、アプリケーションの状態をリセットしたりするときに、ワーカーを手動で再起動する必要がありません。ただし、このコマンドは `queue:work` コマンドよりも効率が大幅に低くなります。

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
<!-- #### Running Multiple Queue Workers -->
#### Running Multiple Queue Workers

<!-- To assign multiple workers to a queue and process jobs concurrently, you should simply start multiple `queue:work` processes. This can either be done locally via multiple tabs in your terminal or in production using your process manager's configuration settings. [When using Supervisor](#supervisor-configuration), you may use the `numprocs` configuration value. -->
複数のワーカーをキューに割り当ててジョブを同時に処理するには、複数の `queue:work` プロセスを開始するだけです。これは、ターミナルの複数のタブを使用してローカルで実行することも、プロセス マネージャーの構成設定を使用して運用環境で実行することもできます。 [When using Supervisor](#supervisor-configuration)、`numprocs` 構成値を使用できます。

<a name="specifying-the-connection-queue"></a>
<!-- #### Specifying The Connection & Queue -->
#### Specifying The Connection & Queue

<!-- You may also specify which queue connection the worker should utilize. The connection name passed to the `work` command should correspond to one of the connections defined in your `config/queue.php` configuration file: -->
ワーカーがどのキュー接続を使用するかを指定することもできます。 `work` コマンドに渡される接続名は、`config/queue.php` 構成ファイルで定義された接続の 1 つに対応する必要があります。

```shell
php artisan queue:work redis
```

<!-- By default, the `queue:work` command only processes jobs for the default queue on a given connection. However, you may customize your queue worker even further by only processing particular queues for a given connection. For example, if all of your emails are processed in an `emails` queue on your `redis` queue connection, you may issue the following command to start a worker that only processes that queue: -->
デフォルトでは、`queue:work` コマンドは、指定された接続上のデフォルト キューのジョブのみを処理します。ただし、特定の接続の特定のキューのみを処理することで、キューワーカーをさらにカスタマイズすることもできます。たとえば、すべての電子メールが `redis` キュー接続の `emails` キューで処理される場合、次のコマンドを発行して、そのキューのみを処理するワーカーを開始できます。

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
<!-- #### Processing A Specified Number Of Jobs -->
#### Processing A Specified Number Of Jobs

<!-- The `--once` option may be used to instruct the worker to only process a single job from the queue: -->
`--once` オプションを使用すると、キューから 1 つのジョブのみを処理するようにワーカーに指示できます。

```shell
php artisan queue:work --once
```

<!-- The `--max-jobs` option may be used to instruct the worker to process the given number of jobs and then exit. This option may be useful when combined with [Supervisor](#supervisor-configuration) so that your workers are automatically restarted after processing a given number of jobs, releasing any memory they may have accumulated: -->
`--max-jobs` オプションを使用すると、指定された数のジョブを処理して終了するようにワーカーに指示できます。このオプションは、[Supervisor](#supervisor-configuration) と組み合わせると便利です。これにより、指定された数のジョブの処理後にワーカーが自動的に再起動され、ワー​​カーが蓄積したメモリが解放されます。

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
<!-- #### Processing All Queued Jobs & Then Exiting -->
#### Processing All Queued Jobs & Then Exiting

<!-- The `--stop-when-empty` option may be used to instruct the worker to process all jobs and then exit gracefully. This option can be useful when processing Laravel queues within a Docker container if you wish to shutdown the container after the queue is empty: -->
`--stop-when-empty` オプションを使用すると、すべてのジョブを処理して正常に終了するようにワーカーに指示できます。このオプションは、Docker コンテナ内で Laravel キューを処理するときに、キューが空になった後にコンテナをシャットダウンする場合に便利です。

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
<!-- #### Processing Jobs For A Given Number Of Seconds -->
#### Processing Jobs For A Given Number Of Seconds

<!-- The `--max-time` option may be used to instruct the worker to process jobs for the given number of seconds and then exit. This option may be useful when combined with [Supervisor](#supervisor-configuration) so that your workers are automatically restarted after processing jobs for a given amount of time, releasing any memory they may have accumulated: -->
`--max-time` オプションを使用すると、指定された秒数の間ジョブを処理してから終了するようにワーカーに指示できます。このオプションは、[Supervisor](#supervisor-configuration) と組み合わせると便利です。これにより、一定時間ジョブを処理した後にワーカーが自動的に再起動され、ワー​​カーが蓄積したメモリが解放されます。

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
<!-- #### Worker Sleep Duration -->
#### Worker Sleep Duration

<!-- When jobs are available on the queue, the worker will keep processing jobs with no delay in between jobs. However, the `sleep` option determines how many seconds the worker will "sleep" if there are no jobs available. Of course, while sleeping, the worker will not process any new jobs: -->
ジョブがキューにある場合、ワーカーはジョブ間に遅延なくジョブの処理を続けます。ただし、`sleep` オプションは、利用可能なジョブがない場合にワーカーが「スリープ」する秒数を決定します。もちろん、ワーカーは寝ている間は新しいジョブを処理しません。

```shell
php artisan queue:work --sleep=3
```

<a name="resource-considerations"></a>
<!-- #### Resource Considerations -->
#### Resource Considerations

<!-- Daemon queue workers do not "reboot" the framework before processing each job. Therefore, you should release any heavy resources after each job completes. For example, if you are doing image manipulation with the GD library, you should free the memory with `imagedestroy` when you are done processing the image. -->
デーモン キューワーカーは、各ジョブを処理する前にフレームワークを「再起動」しません。したがって、各ジョブが完了したら、重いリソースを解放する必要があります。たとえば、GD ライブラリを使用して画像操作を行っている場合、画像の処理が完了したら、`imagedestroy` を使用してメモリを解放する必要があります。

<a name="queue-priorities"></a>
<!-- ### Queue Priorities -->
### Queue Priorities

<!-- Sometimes you may wish to prioritize how your queues are processed. For example, in your `config/queue.php` configuration file, you may set the default `queue` for your `redis` connection to `low`. However, occasionally you may wish to push a job to a `high` priority queue like so: -->
場合によっては、キューの処理方法に優先順位を付けたい場合があります。たとえば、`config/queue.php` 構成ファイルで、`redis` 接続のデフォルトの `queue` を `low` に設定できます。ただし、場合によっては、次のようにジョブを `high` 優先キューにプッシュしたい場合があります。

```
dispatch((new Job)->onQueue('high'));
```

<!-- To start a worker that verifies that all of the `high` queue jobs are processed before continuing to any jobs on the `low` queue, pass a comma-delimited list of queue names to the `work` command: -->
`low` キュー上のジョブを続行する前に、すべての `high` キュー ジョブが処理されたことを検証するワーカーを開始するには、キュー名のカンマ区切りリストを `work` コマンドに渡します。

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
<!-- ### Queue Workers & Deployment -->
### Queue Workers & Deployment

<!-- Since queue workers are long-lived processes, they will not notice changes to your code without being restarted. So, the simplest way to deploy an application using queue workers is to restart the workers during your deployment process. You may gracefully restart all of the workers by issuing the `queue:restart` command: -->
キューワーカーは存続期間の長いプロセスであるため、再起動されなければコードの変更に気づきません。したがって、キューワーカーを使用してアプリケーションをデプロイする最も簡単な方法は、デプロイメント プロセス中にワーカーを再起動することです。 `queue:restart` コマンドを発行すると、すべてのワーカーを正常に再起動できます。

```shell
php artisan queue:restart
```

<!-- This command will instruct all queue workers to gracefully exit after they finish processing their current job so that no existing jobs are lost. Since the queue workers will exit when the `queue:restart` command is executed, you should be running a process manager such as [Supervisor](#supervisor-configuration) to automatically restart the queue workers. -->
このコマンドは、既存のジョブが失われないように、すべてのキューワーカーに現在のジョブの処理が完了した後に正常に終了するように指示します。 `queue:restart` コマンドが実行されるとキューワーカーは終了するため、キューワーカーを自動的に再起動するには、[Supervisor](#supervisor-configuration) などのプロセス マネージャーを実行する必要があります。

> [!NOTE]
> キューは [cache](/docs/9.x/cache) を使用して再起動信号を保存するため、この機能を使用する前に、キャッシュ ドライバがアプリケーションに対して適切に構成されていることを確認する必要があります。

<a name="job-expirations-and-timeouts"></a>
<!-- ### Job Expirations & Timeouts -->
### Job Expirations & Timeouts

<a name="job-expiration"></a>
<!-- #### Job Expiration -->
#### Job Expiration

<!-- In your `config/queue.php` configuration file, each queue connection defines a `retry_after` option. This option specifies how many seconds the queue connection should wait before retrying a job that is being processed. For example, if the value of `retry_after` is set to `90`, the job will be released back onto the queue if it has been processing for 90 seconds without being released or deleted. Typically, you should set the `retry_after` value to the maximum number of seconds your jobs should reasonably take to complete processing. -->
`config/queue.php` 構成ファイルでは、各キュー接続が `retry_after` オプションを定義します。このオプションは、処理中のジョブを再試行する前にキュー接続が待機する秒数を指定します。たとえば、`retry_after` の値が `90` に設定されている場合、ジョブは解放または削除されずに 90 秒間処理されていた場合、キューに解放されます。通常、`retry_after` 値は、ジョブの処理が完了するまでに合理的にかかる最大秒数に設定する必要があります。

> [!WARNING]
> `retry_after` 値が含まれない唯一のキュー接続は、Amazon SQS です。 SQS は、AWS コンソール内で管理される [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) に基づいてジョブを再試行します。

<a name="worker-timeouts"></a>
<!-- #### Worker Timeouts -->
#### Worker Timeouts

<!-- The `queue:work` Artisan command exposes a `--timeout` option. By default, the `--timeout` value is 60 seconds. If a job is processing for longer than the number of seconds specified by the timeout value, the worker processing the job will exit with an error. Typically, the worker will be restarted automatically by a [process manager configured on your server](#supervisor-configuration): -->
`queue:work` Artisan コマンドは、`--timeout` オプションを公開します。デフォルトでは、`--timeout` 値は 60 秒です。ジョブの処理がタイムアウト値で指定された秒数を超えた場合、ジョブを処理しているワーカーはエラーで終了します。通常、ワーカーは [process manager configured on your server](#supervisor-configuration) によって自動的に再起動されます。

```shell
php artisan queue:work --timeout=60
```

<!-- The `retry_after` configuration option and the `--timeout` CLI option are different, but work together to ensure that jobs are not lost and that jobs are only successfully processed once. -->
`retry_after` 構成オプションと `--timeout` CLI オプションは異なりますが、連携してジョブが失われず、ジョブが 1 回だけ正常に処理されるようにします。

> [!WARNING]
> `--timeout` 値は、常に `retry_after` 構成値より少なくとも数秒短くする必要があります。これにより、凍結されたジョブを処理するワーカーは、ジョブが再試行される前に必ず終了されます。 `--timeout` オプションが `retry_after` 構成値より長い場合、ジョブが 2 回処理される可能性があります。

<a name="supervisor-configuration"></a>
<!-- ## Supervisor Configuration -->
## Supervisor Configuration

<!-- In production, you need a way to keep your `queue:work` processes running. A `queue:work` process may stop running for a variety of reasons, such as an exceeded worker timeout or the execution of the `queue:restart` command. -->
運用環境では、`queue:work` プロセスを実行し続ける方法が必要です。 `queue:work` プロセスは、ワーカー タイムアウトの超過や `queue:restart` コマンドの実行など、さまざまな理由で実行を停止することがあります。

<!-- For this reason, you need to configure a process monitor that can detect when your `queue:work` processes exit and automatically restart them. In addition, process monitors can allow you to specify how many `queue:work` processes you would like to run concurrently. Supervisor is a process monitor commonly used in Linux environments and we will discuss how to configure it in the following documentation. -->
このため、`queue:work` プロセスの終了を検出し、自動的に再起動できるプロセス モニターを構成する必要があります。さらに、プロセス モニターを使用すると、同時に実行する `queue:work` プロセスの数を指定できます。 Supervisor は Linux 環境で一般的に使用されるプロセス モニターであり、その構成方法については次のドキュメントで説明します。

<a name="installing-supervisor"></a>
<!-- #### Installing Supervisor -->
#### Installing Supervisor

<!-- Supervisor is a process monitor for the Linux operating system, and will automatically restart your `queue:work` processes if they fail. To install Supervisor on Ubuntu, you may use the following command: -->
Supervisorは Linux オペレーティング システムのプロセス モニターであり、`queue:work` プロセスが失敗した場合に自動的に再起動します。 Ubuntu に Supervisor をインストールするには、次のコマンドを使用できます。

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor を自分で設定および管理するのが大変だと思われる場合は、実稼働 Laravel プロジェクト用に Supervisor を自動的にインストールして設定する [Laravel Forge](https://forge.laravel.com) の使用を検討してください。

<a name="configuring-supervisor"></a>
<!-- #### Configuring Supervisor -->
#### Configuring Supervisor

<!-- Supervisor configuration files are typically stored in the `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `laravel-worker.conf` file that starts and monitors `queue:work` processes: -->
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

<!-- In this example, the `numprocs` directive will instruct Supervisor to run eight `queue:work` processes and monitor all of them, automatically restarting them if they fail. You should change the `command` directive of the configuration to reflect your desired queue connection and worker options. -->
この例では、`numprocs` ディレクティブは、8 つの `queue:work` プロセスを実行してすべてを監視し、失敗した場合は自動的に再起動するようにSupervisorに指示します。必要なキュー接続とワーカー オプションを反映するには、構成の `command` ディレクティブを変更する必要があります。

> [!WARNING]
> `stopwaitsecs` の値が、最も長く実行されているジョブで消費される秒数よりも大きいことを確認する必要があります。そうしないと、Supervisorがジョブの処理が完了する前にジョブを強制終了する可能性があります。

<a name="starting-supervisor"></a>
<!-- #### Starting Supervisor -->
#### Starting Supervisor

<!-- Once the configuration file has been created, you may update the Supervisor configuration and start the processes using the following commands: -->
設定ファイルが作成されたら、次のコマンドを使用してスーパーバイザ設定を更新し、プロセスを開始できます。

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start laravel-worker:*
```

<!-- For more information on Supervisor, consult the [Supervisor documentation](http://supervisord.org/index.html). -->
スーパーバイザの詳細については、[Supervisor documentation](http://supervisord.org/index.html) を参照してください。

<a name="dealing-with-failed-jobs"></a>
<!-- ## Dealing With Failed Jobs -->
## Dealing With Failed Jobs

<!-- Sometimes your queued jobs will fail. Don't worry, things don't always go as planned! Laravel includes a convenient way to [specify the maximum number of times a job should be attempted](#max-job-attempts-and-timeout). After an asynchronous job has exceeded this number of attempts, it will be inserted into the `failed_jobs` database table. [Synchronously dispatched jobs](/docs/9.x/queues#synchronous-dispatching) that fail are not stored in this table and their exceptions are immediately handled by the application. -->
場合によっては、キューに入れられたジョブが失敗することがあります。心配しないでください、物事は常に計画どおりに進むわけではありません。 Laravel には、[specify the maximum number of times a job should be attempted](#max-job-attempts-and-timeout) への便利な方法が含まれています。非同期ジョブはこの試行回数を超えると、`failed_jobs` データベース テーブルに挿入されます。失敗した [Synchronously dispatched jobs](/docs/9.x/queues#synchronous-dispatching) はこのテーブルに格納されず、その例外はアプリケーションによって即座に処理されます。

<!-- A migration to create the `failed_jobs` table is typically already present in new Laravel applications. However, if your application does not contain a migration for this table, you may use the `queue:failed-table` command to create the migration: -->
`failed_jobs` テーブルを作成するための移行は、通常、新しい Laravel アプリケーションにすでに存在しています。ただし、アプリケーションにこのテーブルの移行が含まれていない場合は、`queue:failed-table` コマンドを使用して移行を作成できます。

```shell
php artisan queue:failed-table

php artisan migrate
```

<!-- When running a [queue worker](#running-the-queue-worker) process, you may specify the maximum number of times a job should be attempted using the `--tries` switch on the `queue:work` command. If you do not specify a value for the `--tries` option, jobs will only be attempted once or as many times as specified by the job class' `$tries` property: -->
[queue worker](#running-the-queue-worker) プロセスを実行する場合、`queue:work` コマンドの `--tries` スイッチを使用して、ジョブの試行の最大回数を指定できます。 `--tries` オプションの値を指定しない場合、ジョブは 1 回だけ、またはジョブ クラスの `$tries` プロパティで指定された回数だけ試行されます。

```shell
php artisan queue:work redis --tries=3
```

<!-- Using the `--backoff` option, you may specify how many seconds Laravel should wait before retrying a job that has encountered an exception. By default, a job is immediately released back onto the queue so that it may be attempted again: -->
`--backoff` オプションを使用すると、例外が発生したジョブを再試行する前に Laravel が待機する秒数を指定できます。デフォルトでは、ジョブはすぐにキューに戻され、再試行できるようになります。

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

<!-- If you would like to configure how many seconds Laravel should wait before retrying a job that has encountered an exception on a per-job basis, you may do so by defining a `backoff` property on your job class: -->
例外が発生したジョブを再試行する前に Laravel が待機する秒数をジョブごとに設定したい場合は、ジョブ クラスで `backoff` プロパティを定義することで設定できます。

```
/**
 * The number of seconds to wait before retrying the job.
 *
 * @var int
 */
public $backoff = 3;
```

<!-- If you require more complex logic for determining the job's backoff time, you may define a `backoff` method on your job class: -->
ジョブのバックオフ時間を決定するためにより複雑なロジックが必要な場合は、ジョブ クラスで `backoff` メソッドを定義できます。

```
/**
* Calculate the number of seconds to wait before retrying the job.
*
* @return int
*/
public function backoff()
{
    return 3;
}
```

<!-- You may easily configure "exponential" backoffs by returning an array of backoff values from the `backoff` method. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, and 10 seconds for the third retry: -->
`backoff` メソッドからバックオフ値の配列を返すことで、「指数関数的」バックオフを簡単に構成できます。この例では、再試行遅延は最初の再試行では 1 秒、2 回目の再試行では 5 秒、3 回目の再試行では 10 秒になります。

```
/**
* Calculate the number of seconds to wait before retrying the job.
*
* @return array
*/
public function backoff()
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
<!-- ### Cleaning Up After Failed Jobs -->
### Cleaning Up After Failed Jobs

<!-- When a particular job fails, you may want to send an alert to your users or revert any actions that were partially completed by the job. To accomplish this, you may define a `failed` method on your job class. The `Throwable` instance that caused the job to fail will be passed to the `failed` method: -->
特定のジョブが失敗した場合、ユーザーにアラートを送信したり、ジョブによって部分的に完了したアクションを元に戻したりすることができます。これを実現するには、ジョブ クラスで `failed` メソッドを定義します。ジョブの失敗の原因となった `Throwable` インスタンスは、`failed` メソッドに渡されます。

```
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Throwable;

class ProcessPodcast implements ShouldQueue
{
    use InteractsWithQueue, Queueable, SerializesModels;

    /**
     * The podcast instance.
     *
     * @var \App\Podcast
     */
    public $podcast;

    /**
     * Create a new job instance.
     *
     * @param  \App\Models\Podcast  $podcast
     * @return void
     */
    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }

    /**
     * Execute the job.
     *
     * @param  \App\Services\AudioProcessor  $processor
     * @return void
     */
    public function handle(AudioProcessor $processor)
    {
        // Process uploaded podcast...
    }

    /**
     * Handle a job failure.
     *
     * @param  \Throwable  $exception
     * @return void
     */
    public function failed(Throwable $exception)
    {
        // Send user notification of failure, etc...
    }
}
```

> [!WARNING]
> ジョブの新しいインスタンスは、`failed` メソッドを呼び出す前にインスタンス化されます。したがって、`handle` メソッド内で行われたクラス プロパティの変更は失われます。

<a name="retrying-failed-jobs"></a>
<!-- ### Retrying Failed Jobs -->
### Retrying Failed Jobs

<!-- To view all of the failed jobs that have been inserted into your `failed_jobs` database table, you may use the `queue:failed` Artisan command: -->
`failed_jobs` データベース テーブルに挿入された失敗したジョブをすべて表示するには、`queue:failed` Artisan コマンドを使用できます。

```shell
php artisan queue:failed
```

<!-- The `queue:failed` command will list the job ID, connection, queue, failure time, and other information about the job. The job ID may be used to retry the failed job. For instance, to retry a failed job that has an ID of `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`, issue the following command: -->
`queue:failed` コマンドは、ジョブ ID、接続、キュー、失敗時間、およびジョブに関するその他の情報をリストします。ジョブ ID は、失敗したジョブを再試行するために使用できます。たとえば、`ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece` の ID を持つ失敗したジョブを再試行するには、次のコマンドを発行します。

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

<!-- If necessary, you may pass multiple IDs to the command: -->
必要に応じて、コマンドに複数の ID を渡すことができます。

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

<!-- You may also retry all of the failed jobs for a particular queue: -->
特定のキューに対して失敗したジョブをすべて再試行することもできます。

```shell
php artisan queue:retry --queue=name
```

<!-- To retry all of your failed jobs, execute the `queue:retry` command and pass `all` as the ID: -->
失敗したジョブをすべて再試行するには、`queue:retry` コマンドを実行し、ID として `all` を渡します。

```shell
php artisan queue:retry all
```

<!-- If you would like to delete a failed job, you may use the `queue:forget` command: -->
失敗したジョブを削除したい場合は、`queue:forget` コマンドを使用できます。

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/9.x/horizon) を使用する場合、失敗したジョブを削除するには、`queue:forget` コマンドの代わりに `horizon:forget` コマンドを使用する必要があります。

<!-- To delete all of your failed jobs from the `failed_jobs` table, you may use the `queue:flush` command: -->
失敗したジョブをすべて `failed_jobs` テーブルから削除するには、`queue:flush` コマンドを使用します。

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
<!-- ### Ignoring Missing Models -->
### Ignoring Missing Models

<!-- When injecting an Eloquent model into a job, the model is automatically serialized before being placed on the queue and re-retrieved from the database when the job is processed. However, if the model has been deleted while the job was waiting to be processed by a worker, your job may fail with a `ModelNotFoundException`. -->
Eloquent モデルをジョブに挿入すると、モデルはキューに置かれる前に自動的にシリアル化され、ジョブの処理時にデータベースから再取得されます。ただし、ジョブがワーカーによる処理を待機している間にモデルが削除された場合、ジョブは `ModelNotFoundException` で失敗する可能性があります。

<!-- For convenience, you may choose to automatically delete jobs with missing models by setting your job's `deleteWhenMissingModels` property to `true`. When this property is set to `true`, Laravel will quietly discard the job without raising an exception: -->
便宜上、ジョブの `deleteWhenMissingModels` プロパティを `true` に設定することで、モデルが欠落しているジョブを自動的に削除することを選択できます。このプロパティが `true` に設定されている場合、Laravel は例外を発生させずに静かにジョブを破棄します。

```
/**
 * Delete the job if its models no longer exist.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
<!-- ### Pruning Failed Jobs -->
### Pruning Failed Jobs

<!-- You may prune the records in your application's `failed_jobs` table by invoking the `queue:prune-failed` Artisan command: -->
`queue:prune-failed` Artisan コマンドを呼び出して、アプリケーションの `failed_jobs` テーブル内のレコードを削除できます。

```shell
php artisan queue:prune-failed
```

<!-- By default, all the failed job records that are more than 24 hours old will be pruned. If you provide the `--hours` option to the command, only the failed job records that were inserted within the last N number of hours will be retained. For example, the following command will delete all the failed job records that were inserted more than 48 hours ago: -->
デフォルトでは、24 時間以上経過した失敗したジョブ レコードはすべて削除されます。コマンドに `--hours` オプションを指定すると、過去 N 時間以内に挿入された失敗したジョブ レコードのみが保持されます。たとえば、次のコマンドは、48 時間以上前に挿入された失敗したジョブ レコードをすべて削除します。

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
<!-- ### Storing Failed Jobs In DynamoDB -->
### Storing Failed Jobs In DynamoDB

<!-- Laravel also provides support for storing your failed job records in [DynamoDB](https://aws.amazon.com/dynamodb) instead of a relational database table. However, you must create a DynamoDB table to store all of the failed job records. Typically, this table should be named `failed_jobs`, but you should name the table based on the value of the `queue.failed.table` configuration value within your application's `queue` configuration file. -->
Laravel は、失敗したジョブ レコードをリレーショナル データベース テーブルではなく [DynamoDB](https://aws.amazon.com/dynamodb) に保存するサポートも提供します。ただし、失敗したジョブ レコードをすべて保存するには、DynamoDB テーブルを作成する必要があります。通常、このテーブルには `failed_jobs` という名前を付ける必要がありますが、アプリケーションの `queue` 構成ファイル内の `queue.failed.table` 構成値の値に基づいてテーブルに名前を付ける必要があります。

<!-- The `failed_jobs` table should have a string primary partition key named `application` and a string primary sort key named `uuid`. The `application` portion of the key will contain your application's name as defined by the `name` configuration value within your application's `app` configuration file. Since the application name is part of the DynamoDB table's key, you can use the same table to store failed jobs for multiple Laravel applications. -->
`failed_jobs` テーブルには、`application` という名前の文字列プライマリ パーティション キーと、`uuid` という名前の文字列プライマリ ソート キーが必要です。キーの `application` 部分には、アプリケーションの `app` 構成ファイル内の `name` 構成値で定義されたアプリケーションの名前が含まれます。アプリケーション名は DynamoDB テーブルのキーの一部であるため、同じテーブルを使用して複数の Laravel アプリケーションの失敗したジョブを保存できます。

<!-- In addition, ensure that you install the AWS SDK so that your Laravel application can communicate with Amazon DynamoDB: -->
さらに、Laravel アプリケーションが Amazon DynamoDB と通信できるように、必ず AWS SDK をインストールしてください。

```shell
composer require aws/aws-sdk-php
```

<!-- Next, set the `queue.failed.driver` configuration option's value to `dynamodb`. In addition, you should define `key`, `secret`, and `region` configuration options within the failed job configuration array. These options will be used to authenticate with AWS. When using the `dynamodb` driver, the `queue.failed.database` configuration option is unnecessary: -->
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
<!-- ### Disabling Failed Job Storage -->
### Disabling Failed Job Storage

<!-- You may instruct Laravel to discard failed jobs without storing them by setting the `queue.failed.driver` configuration option's value to `null`. Typically, this may be accomplished via the `QUEUE_FAILED_DRIVER` environment variable: -->
`queue.failed.driver` 構成オプションの値を `null` に設定することで、失敗したジョブを保存せずに破棄するように Laravel に指示できます。通常、これは `QUEUE_FAILED_DRIVER` 環境変数を介して実現できます。

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
<!-- ### Failed Job Events -->
### Failed Job Events

<!-- If you would like to register an event listener that will be invoked when a job fails, you may use the `Queue` facade's `failing` method. For example, we may attach a closure to this event from the `boot` method of the `AppServiceProvider` that is included with Laravel: -->
ジョブが失敗したときに呼び出されるイベント リスナを登録したい場合は、`Queue` ファサードの `failing` メソッドを使用できます。たとえば、Laravel に含まれる `AppServiceProvider` の `boot` メソッドからこのイベントにクロージャーをアタッチできます。

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

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
        Queue::failing(function (JobFailed $event) {
            // $event->connectionName
            // $event->job
            // $event->exception
        });
    }
}
```

<a name="clearing-jobs-from-queues"></a>
<!-- ## Clearing Jobs From Queues -->
## Clearing Jobs From Queues

> [!NOTE]
> [Horizon](/docs/9.x/horizon) を使用する場合は、`queue:clear` コマンドの代わりに、`horizon:clear` コマンドを使用してキューからジョブをクリアする必要があります。

<!-- If you would like to delete all jobs from the default queue of the default connection, you may do so using the `queue:clear` Artisan command: -->
デフォルト接続のデフォルトキューからすべてのジョブを削除したい場合は、`queue:clear` Artisan コマンドを使用して削除できます。

```shell
php artisan queue:clear
```

<!-- You may also provide the `connection` argument and `queue` option to delete jobs from a specific connection and queue: -->
`connection` 引数と `queue` オプションを指定して、特定の接続とキューからジョブを削除することもできます。

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> キューからのジョブのクリアは、SQS、Redis、およびデータベース キュー ドライバでのみ使用できます。さらに、SQS メッセージの削除プロセスには最大 60 秒かかるため、キューをクリアしてから最大 60 秒以内に SQS キューに送信されたジョブも削除される可能性があります。

<a name="monitoring-your-queues"></a>
<!-- ## Monitoring Your Queues -->
## Monitoring Your Queues

<!-- If your queue receives a sudden influx of jobs, it could become overwhelmed, leading to a long wait time for jobs to complete. If you wish, Laravel can alert you when your queue job count exceeds a specified threshold. -->
キューにジョブが突然殺到すると、キューが過剰になり、ジョブが完了するまでの待ち時間が長くなる可能性があります。必要に応じて、Laravel はキューのジョブ数が指定されたしきい値を超えたときに警告を発することができます。

<!-- To get started, you should schedule the `queue:monitor` command to [run every minute](/docs/9.x/scheduling). The command accepts the names of the queues you wish to monitor as well as your desired job count threshold: -->
まず、`queue:monitor` コマンドを [run every minute](/docs/9.x/scheduling) にスケジュールする必要があります。このコマンドは、監視するキューの名前と、必要なジョブ数のしきい値を受け入れます。

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

<!-- Scheduling this command alone is not enough to trigger a notification alerting you of the queue's overwhelmed status. When the command encounters a queue that has a job count exceeding your threshold, an `Illuminate\Queue\Events\QueueBusy` event will be dispatched. You may listen for this event within your application's `EventServiceProvider` in order to send a notification to you or your development team: -->
このコマンドをスケジュールするだけでは、キューの超過ステータスを警告する通知をトリガーするには十分ではありません。コマンドがしきい値を超えるジョブ数を含むキューを検出すると、`Illuminate\Queue\Events\QueueBusy` イベントが送出されます。あなたまたは開発チームに通知を送信するために、アプリケーションの `EventServiceProvider` 内でこのイベントをリッスンできます。

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Register any other events for your application.
 *
 * @return void
 */
public function boot()
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

<a name="job-events"></a>
<!-- ## Job Events -->
## Job Events

<!-- Using the `before` and `after` methods on the `Queue` [facade](/docs/9.x/facades), you may specify callbacks to be executed before or after a queued job is processed. These callbacks are a great opportunity to perform additional logging or increment statistics for a dashboard. Typically, you should call these methods from the `boot` method of a [service provider](/docs/9.x/providers). For example, we may use the `AppServiceProvider` that is included with Laravel: -->
`Queue` [facade](/docs/9.x/facades) で `before` メソッドと `after` メソッドを使用すると、キューに入れられたジョブの処理前または後に実行されるコールバックを指定できます。これらのコールバックは、追加のログを実行したり、ダッシュボードの統計を増分したりする絶好の機会です。通常、これらのメソッドは、[service provider](/docs/9.x/providers) の `boot` メソッドから呼び出す必要があります。たとえば、Laravel に含まれる `AppServiceProvider` を使用できます。

```
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
```

<!-- Using the `looping` method on the `Queue` [facade](/docs/9.x/facades), you may specify callbacks that execute before the worker attempts to fetch a job from a queue. For example, you might register a closure to rollback any transactions that were left open by a previously failed job: -->
`Queue` [facade](/docs/9.x/facades) で `looping` メソッドを使用すると、ワーカーがキューからジョブをフェッチしようとする前に実行するコールバックを指定できます。たとえば、以前に失敗したジョブによってオープンされたままになっているトランザクションをロールバックするクロージャを登録できます。

```
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```

