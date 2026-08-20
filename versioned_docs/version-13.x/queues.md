<!-- # Queues -->
# Queues

- [Introduction](#introduction)
    - [Connections vs. Queues](#connections-vs-queues)
    - [Driver Notes and Prerequisites](#driver-prerequisites)
- [Creating Jobs](#creating-jobs)
    - [Generating Job Classes](#generating-job-classes)
    - [Class Structure](#class-structure)
    - [Unique Jobs](#unique-jobs)
    - [Debounced Jobs](#debounced-jobs)
    - [Encrypted Jobs](#encrypted-jobs)
- [Job Middleware](#job-middleware)
    - [Rate Limiting](#rate-limiting)
    - [Preventing Job Overlaps](#preventing-job-overlaps)
    - [Throttling Exceptions](#throttling-exceptions)
    - [Releasing Jobs](#releasing-jobs)
    - [Skipping Jobs](#skipping-jobs)
- [Dispatching Jobs](#dispatching-jobs)
    - [Delayed Dispatching](#delayed-dispatching)
    - [Synchronous Dispatching](#synchronous-dispatching)
    - [Bulk Dispatching](#bulk-dispatching)
    - [Preparing Jobs Before Dispatch](#preparing-jobs-before-dispatch)
    - [Jobs & Database Transactions](#jobs-and-database-transactions)
    - [Job Chaining](#job-chaining)
    - [Customizing The Queue and Connection](#customizing-the-queue-and-connection)
    - [Specifying Max Job Attempts / Timeout Values](#max-job-attempts-and-timeout)
    - [SQS FIFO and Fair Queues](#sqs-fifo-and-fair-queues)
    - [Queue Failover](#queue-failover)
    - [Error Handling](#error-handling)
- [Job Batching](#job-batching)
    - [Defining Batchable Jobs](#defining-batchable-jobs)
    - [Dispatching Batches](#dispatching-batches)
    - [Chains and Batches](#chains-and-batches)
    - [Adding Jobs to Batches](#adding-jobs-to-batches)
    - [Inspecting Batches](#inspecting-batches)
    - [Cancelling Batches](#cancelling-batches)
    - [Batch Failures](#batch-failures)
    - [Pruning Batches](#pruning-batches)
    - [Storing Batches in DynamoDB](#storing-batches-in-dynamodb)
- [Queueing Closures](#queueing-closures)
- [Running the Queue Worker](#running-the-queue-worker)
    - [The `queue:work` Command](#the-queue-work-command)
    - [Queue Priorities](#queue-priorities)
    - [Queue Workers and Deployment](#queue-workers-and-deployment)
    - [Reacting to Worker Signals](#reacting-to-worker-signals)
    - [Job Expirations and Timeouts](#job-expirations-and-timeouts)
    - [Pausing and Resuming Queue Workers](#pausing-and-resuming-queue-workers)
- [Supervisor Configuration](#supervisor-configuration)
- [Dealing With Failed Jobs](#dealing-with-failed-jobs)
    - [Cleaning Up After Failed Jobs](#cleaning-up-after-failed-jobs)
    - [Retrying Failed Jobs](#retrying-failed-jobs)
    - [Ignoring Missing Models](#ignoring-missing-models)
    - [Pruning Failed Jobs](#pruning-failed-jobs)
    - [Storing Failed Jobs in DynamoDB](#storing-failed-jobs-in-dynamodb)
    - [Disabling Failed Job Storage](#disabling-failed-job-storage)
    - [Failed Job Events](#failed-job-events)
- [Clearing Jobs From Queues](#clearing-jobs-from-queues)
- [Monitoring Your Queues](#monitoring-your-queues)
- [Testing](#testing)
    - [Faking a Subset of Jobs](#faking-a-subset-of-jobs)
    - [Testing Job Chains](#testing-job-chains)
    - [Testing Job Batches](#testing-job-batches)
    - [Testing Job / Queue Interactions](#testing-job-queue-interactions)
- [Job Events](#job-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- While building your web application, you may have some tasks, such as parsing and storing an uploaded CSV file, that take too long to perform during a typical web request. Thankfully, Laravel allows you to easily create queued jobs that may be processed in the background. By moving time intensive tasks to a queue, your application can respond to web requests with blazing speed and provide a better user experience to your customers. -->
웹 애플리케이션을 만들다 보면 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼 일반적인 웹 요청 중에 처리하기에는 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel을 사용하면 백그라운드에서 처리할 수 있는 큐 잡을 쉽게 만들 수 있습니다. 시간이 많이 드는 작업을 큐로 옮기면 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있고, 사용자에게 더 나은 경험을 제공할 수 있습니다.

<!-- Laravel queues provide a unified queueing API across a variety of different queue backends, such as [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), or even a relational database. -->
Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 같은 다양한 큐 백엔드 전반에 걸쳐 통합된 큐잉 API를 제공합니다.

<!-- Laravel's queue configuration options are stored in your application's `config/queue.php` configuration file. In this file, you will find connection configurations for each of the queue drivers that are included with the framework, including the database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), and [Beanstalkd](https://beanstalkd.github.io/) drivers, as well as a synchronous driver that will execute jobs immediately (for use during development or testing). A `null` queue driver is also included which discards queued jobs. -->
Laravel의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버의 연결 설정이 들어 있습니다. 여기에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버뿐 아니라 잡을 즉시 실행하는 동기 드라이버도 포함됩니다. 동기 드라이버는 개발이나 테스트 중에 사용할 수 있습니다. 큐에 들어온 잡을 버리는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis로 구동되는 큐를 위한 아름다운 대시보드이자 설정 시스템입니다. 자세한 내용은 전체 [Horizon documentation](/docs/13.x/horizon)을 참고하세요.

<a name="connections-vs-queues"></a>
<!-- ### Connections vs. Queues -->
### Connections vs. Queues

<!-- Before getting started with Laravel queues, it is important to understand the distinction between "connections" and "queues". In your `config/queue.php` configuration file, there is a `connections` configuration array. This option defines the connections to backend queue services such as Amazon SQS, Beanstalk, or Redis. However, any given queue connection may have multiple "queues" which may be thought of as different stacks or piles of queued jobs. -->
Laravel 큐를 시작하기 전에 "connections"와 "queues"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스에 대한 연결을 정의합니다. 하지만 하나의 큐 연결은 여러 "큐"를 가질 수 있으며, 이는 서로 다른 큐 잡의 스택이나 더미로 생각할 수 있습니다.

<!-- Note that each connection configuration example in the `queue` configuration file contains a `queue` attribute. This is the default queue that jobs will be dispatched to when they are sent to a given connection. In other words, if you dispatch a job without explicitly defining which queue it should be dispatched to, the job will be placed on the queue that is defined in the `queue` attribute of the connection configuration: -->
`queue` 설정 파일의 각 연결 설정 예제에는 `queue` 속성이 포함되어 있습니다. 이는 해당 연결로 잡이 전송될 때 잡이 디스패치될 기본 큐입니다. 다시 말해, 잡을 디스패치하면서 어느 큐로 보낼지 명시적으로 정의하지 않으면 해당 잡은 연결 설정의 `queue` 속성에 정의된 큐에 배치됩니다.

```php
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```

<!-- Some applications may not need to ever push jobs onto multiple queues, instead preferring to have one simple queue. However, pushing jobs to multiple queues can be especially useful for applications that wish to prioritize or segment how jobs are processed, since the Laravel queue worker allows you to specify which queues it should process by priority. For example, if you push jobs to a `high` queue, you may run a worker that gives them higher processing priority: -->
어떤 애플리케이션은 여러 큐에 잡을 넣을 필요 없이 단순한 큐 하나만 사용하는 편을 선호할 수 있습니다. 하지만 잡 처리 방식에 우선순위를 두거나 구분하고 싶은 애플리케이션에서는 여러 큐에 잡을 넣는 방식이 특히 유용합니다. Laravel 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어 `high` 큐에 잡을 넣는다면, 해당 잡을 더 높은 처리 우선순위로 다루는 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Notes and Prerequisites -->
### Driver Notes and Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- In order to use the `database` queue driver, you will need a database table to hold the jobs. Typically, this is included in Laravel's default `0001_01_01_000002_create_jobs_table.php` [database migration](/docs/13.x/migrations); however, if your application does not contain this migration, you may use the `make:queue-table` Artisan command to create it: -->
`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [database migration](/docs/13.x/migrations)에 포함되어 있습니다. 하지만 애플리케이션에 이 마이그레이션이 없다면 `make:queue-table` Artisan 명령어를 사용해 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- In order to use the `redis` queue driver, you should configure a Redis database connection in your `config/database.php` configuration file. -->
`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에서 Redis 데이터베이스 연결을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 `serializer` 및 `compression` Redis 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
<!-- ##### Redis Cluster -->
##### Redis Cluster

<!-- If your Redis queue connection uses a [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering), your queue names must contain a [key hash tag](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags). This is required in order to ensure all of the Redis keys for a given queue are placed into the same hash slot: -->
Redis 큐 연결이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에는 [key hash tag](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이는 특정 큐에 대한 모든 Redis 키가 같은 해시 슬롯에 배치되도록 보장하기 위해 필요합니다.

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', '{default}'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => null,
    'after_commit' => false,
],
```

<a name="blocking"></a>
<!-- ##### Blocking -->
##### Blocking

<!-- When using the Redis queue, you may use the `block_for` configuration option to specify how long the driver should wait for a job to become available before iterating through the worker loop and re-polling the Redis database. -->
Redis 큐를 사용할 때는 `block_for` 설정 옵션을 사용하여, 잡이 사용 가능해질 때까지 드라이버가 얼마나 기다린 뒤 워커 루프를 반복하고 Redis 데이터베이스를 다시 폴링할지 지정할 수 있습니다.

<!-- Adjusting this value based on your queue load can be more efficient than continually polling the Redis database for new jobs. For instance, you may set the value to `5` to indicate that the driver should block for five seconds while waiting for a job to become available: -->
큐 부하에 맞춰 이 값을 조정하면 새 잡을 찾기 위해 Redis 데이터베이스를 계속 폴링하는 것보다 더 효율적일 수 있습니다. 예를 들어 값을 `5`로 설정하면 드라이버가 잡이 사용 가능해지기를 기다리는 동안 5초 동안 블로킹하도록 지정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', 'default'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => 5,
    'after_commit' => false,
],
```

> [!WARNING]
> `block_for`를 `0`으로 설정하면 큐 워커가 잡을 사용할 수 있을 때까지 무기한 차단됩니다. 또한 다음 잡이 처리될 때까지 `SIGTERM`과 같은 신호도 처리되지 않습니다.

<a name="sqs-overflow-storage"></a>
<!-- #### SQS Overflow Storage -->
#### SQS Overflow Storage

<!-- Amazon SQS limits the maximum size of a queued message payload. If you need to dispatch jobs with payloads that may exceed this limit, you may configure Laravel to store oversized SQS payloads in a cache store and send a pointer through SQS instead. To enable this feature, add an `overflow` array to your SQS queue connection configuration: -->
Amazon SQS는 큐에 들어가는 메시지 페이로드의 최대 크기를 제한합니다. 이 제한을 초과할 수 있는 페이로드를 가진 잡을 디스패치해야 한다면, Laravel이 너무 큰 SQS 페이로드를 캐시 저장소에 저장하고 SQS를 통해 포인터를 보내도록 설정할 수 있습니다. 이 기능을 활성화하려면 SQS 큐 연결 설정에 `overflow` 배열을 추가합니다:

```php
'sqs' => [
    'driver' => 'sqs',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'prefix' => env('SQS_PREFIX', 'https://sqs.us-east-1.amazonaws.com/your-account-id'),
    'queue' => env('SQS_QUEUE', 'default'),
    'suffix' => env('SQS_SUFFIX'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'after_commit' => false,
    'overflow' => [
        'enabled' => env('SQS_OVERFLOW_ENABLED', false),
        'store' => env('SQS_OVERFLOW_STORE'),
        'always' => false,
        'delete_after_processing' => true,
        'flush_on_clear' => env('SQS_OVERFLOW_FLUSH_ON_CLEAR', false),
    ],
],
```

<!-- When overflow storage is enabled, Laravel will store payloads that are at least 1 MB in the configured cache store. If the `always` option is `true`, every SQS payload will be stored in the cache store regardless of its size. Since queued jobs will need to retrieve their payloads from the cache store when they are processed, you should choose a store that can retain the payloads until your workers process them. By default, stored payloads are deleted after their jobs have been successfully processed and deleted from SQS. -->
오버플로 저장소가 활성화되면 Laravel은 크기가 1MB 이상인 페이로드를 설정된 캐시 저장소에 저장합니다. `always` 옵션이 `true`이면 모든 SQS 페이로드가 크기와 관계없이 캐시 저장소에 저장됩니다. 큐에 들어간 잡은 처리될 때 캐시 저장소에서 페이로드를 가져와야 하므로, 워커가 잡을 처리할 때까지 페이로드를 보관할 수 있는 저장소를 선택해야 합니다. 기본적으로 저장된 페이로드는 해당 잡이 성공적으로 처리되고 SQS에서 삭제된 후 제거됩니다.

<!-- If the `flush_on_clear` option is `true`, the configured overflow cache store will be flushed when the `queue:clear` command clears the SQS queue. Since flushing a cache store may remove all items from that store, you should configure SQS overflow storage to use a dedicated cache store when enabling this option. -->
`flush_on_clear` 옵션이 `true`이면 `queue:clear` 명령어가 SQS 큐를 비울 때 설정된 오버플로 캐시 저장소도 비워집니다. 캐시 저장소를 비우면 해당 저장소의 모든 항목이 제거될 수 있으므로, 이 옵션을 활성화할 때는 SQS 오버플로 저장소가 전용 캐시 저장소를 사용하도록 설정해야 합니다.

<a name="other-driver-prerequisites"></a>
<!-- #### Other Driver Prerequisites -->
#### Other Driver Prerequisites

<!-- The following dependencies are needed for the listed queue drivers. These dependencies may be installed via the Composer package manager: -->
아래 큐 드라이버를 사용하려면 다음 의존성이 필요합니다. 이 의존성은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

<div class="content-list" markdown="1">

<!-- - Amazon SQS: `aws/aws-sdk-php ~3.0` - Beanstalkd: `pda/pheanstalk ~5.0` - Redis: `predis/predis ~3.0` or phpredis PHP extension - [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb` -->
- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~3.0` 또는 phpredis PHP extension
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
<!-- ## Creating Jobs -->
## Creating Jobs

<a name="generating-job-classes"></a>
<!-- ### Generating Job Classes -->
### Generating Job Classes

<!-- By default, all of the queueable jobs for your application are stored in the `app/Jobs` directory. If the `app/Jobs` directory doesn't exist, it will be created when you run the `make:job` Artisan command: -->
기본적으로 애플리케이션의 모든 큐잉 가능한 잡은 `app/Jobs` 디렉터리에 저장됩니다. `app/Jobs` 디렉터리가 없다면 `make:job` Artisan 명령어를 실행할 때 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

<!-- The generated class will implement the `Illuminate\Contracts\Queue\ShouldQueue` interface, indicating to Laravel that the job should be pushed onto the queue to run asynchronously. -->
생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현합니다. 이는 해당 잡이 비동기로 실행되도록 큐에 넣어야 한다는 것을 Laravel에 알려줍니다.

> [!NOTE]
> 잡 스텁은 [stub publishing](/docs/13.x/artisan#stub-customization)을 사용해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
<!-- ### Class Structure -->
### Class Structure

<!-- Job classes are very simple, normally containing only a `handle` method that is invoked when the job is processed by the queue. To get started, let's take a look at an example job class. In this example, we'll pretend we manage a podcast publishing service and need to process the uploaded podcast files before they are published: -->
잡 클래스는 매우 단순합니다. 일반적으로 큐가 잡을 처리할 때 호출되는 `handle` 메서드만 포함합니다. 시작하기 위해 예제 잡 클래스를 살펴보겠습니다. 이 예제에서는 팟캐스트 게시 서비스를 운영하고 있으며, 업로드된 팟캐스트 파일을 게시하기 전에 처리해야 한다고 가정합니다.

```php
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
```

<!-- In this example, note that we were able to pass an [Eloquent model](/docs/13.x/eloquent) directly into the queued job's constructor. Because of the `Queueable` trait that the job is using, Eloquent models and their loaded relationships will be gracefully serialized and unserialized when the job is processing. -->
이 예제에서는 [Eloquent model](/docs/13.x/eloquent)을 큐에 등록된 잡의 생성자에 직접 전달할 수 있다는 점에 주목하시기 바랍니다. 잡에서 사용하는 `Queueable` 트레이트 덕분에 Eloquent 모델과 로드된 연관관계는 잡이 처리될 때 안전하게 직렬화되고 역직렬화됩니다.

<!-- If your queued job accepts an Eloquent model in its constructor, only the identifier for the model will be serialized onto the queue. When the job is actually handled, the queue system will automatically re-retrieve the full model instance and its loaded relationships from the database. This approach to model serialization allows for much smaller job payloads to be sent to your queue driver. -->
큐 잡이 생성자에서 Eloquent 모델을 받는 경우, 큐에는 해당 모델의 식별자만 직렬화됩니다. 잡이 실제로 처리될 때 큐 시스템은 데이터베이스에서 전체 모델 인스턴스와 로드된 연관관계를 자동으로 다시 조회합니다. 이러한 모델 직렬화 방식 덕분에 큐 드라이버로 전송되는 잡 페이로드를 훨씬 작게 유지할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
<!-- #### `handle` Method Dependency Injection -->
#### `handle` Method Dependency Injection

<!-- The `handle` method is invoked when the job is processed by the queue. Note that we are able to type-hint dependencies on the `handle` method of the job. The Laravel [service container](/docs/13.x/container) automatically injects these dependencies. -->
`handle` 메서드는 잡이 큐에서 처리될 때 호출됩니다. 잡의 `handle` 메서드에서 의존성에 타입 힌트를 지정할 수 있다는 점에 유의하세요. Laravel [service container](/docs/13.x/container)가 이러한 의존성을 자동으로 주입합니다.

<!-- If you would like to take total control over how the container injects dependencies into the `handle` method, you may use the container's `bindMethod` method. The `bindMethod` method accepts a callback which receives the job and the container. Within the callback, you are free to invoke the `handle` method however you wish. Typically, you should call this method from the `boot` method of your `App\Providers\AppServiceProvider` [service provider](/docs/13.x/providers): -->
컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하려면 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod` 메서드는 잡과 컨테이너를 전달받는 콜백을 인수로 받습니다. 콜백 내에서는 원하는 방식으로 `handle` 메서드를 자유롭게 호출할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\AppServiceProvider` [service provider](/docs/13.x/providers)의 `boot` 메서드에서 호출해야 합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원시 이미지 콘텐츠)는 큐에 등록할 잡에 전달하기 전에 `base64_encode` 함수를 통해 전달해야 합니다. 그렇지 않으면 큐에 등록할 때 잡이 JSON으로 제대로 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
<!-- #### Queued Relationships -->
#### Queued Relationships

<!-- Because all loaded Eloquent model relationships also get serialized when a job is queued, the serialized job string can sometimes become quite large. Furthermore, when a job is deserialized and model relationships are re-retrieved from the database, they will be retrieved in their entirety. Any previous relationship constraints that were applied before the model was serialized during the job queueing process will not be applied when the job is deserialized. Therefore, if you wish to work with a subset of a given relationship, you should re-constrain that relationship within your queued job. -->
잡이 큐에 들어갈 때 로드된 모든 Eloquent 모델 연관관계도 함께 직렬화되므로, 직렬화된 잡 문자열이 때때로 상당히 커질 수 있습니다. 또한 잡이 역직렬화되고 모델 연관관계가 데이터베이스에서 다시 조회될 때 해당 연관관계는 전체가 조회됩니다. 잡 큐잉 과정에서 모델이 직렬화되기 전에 적용되었던 이전 연관관계 제약 조건은 잡이 역직렬화될 때 적용되지 않습니다. 따라서 특정 연관관계의 일부만 사용하고 싶다면 큐 잡 안에서 해당 연관관계에 다시 제약 조건을 적용해야 합니다.

<!-- Or, to prevent relations from being serialized, you can call the `withoutRelations` method on the model when setting a property value. This method will return an instance of the model without its loaded relationships: -->
또는 연관관계가 직렬화되지 않도록 하려면 속성 값을 설정할 때 모델에서 `withoutRelations` 메서드를 호출할 수 있습니다. 이 메서드는 로드된 연관관계가 없는 모델 인스턴스를 반환합니다.

```php
/**
 * Create a new job instance.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

<!-- If you only need to remove specific relations while keeping the rest, you may use the `withoutRelation` method: -->
나머지는 유지하면서 특정 연관관계만 제거해야 한다면 `withoutRelation` 메서드를 사용할 수 있습니다.

```php
$this->podcast = $podcast->withoutRelation('comments');
```

<!-- If you are using [PHP constructor property promotion](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion) and would like to indicate that an Eloquent model should not have its relations serialized, you may use the `WithoutRelations` attribute: -->
[PHP constructor property promotion](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하면서 Eloquent 모델의 연관관계가 직렬화되지 않아야 함을 나타내고 싶다면 `WithoutRelations` 속성을 사용할 수 있습니다.

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * Create a new job instance.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

<!-- For convenience, if you wish to serialize all models without relationships, you may apply the `WithoutRelations` attribute to the entire class instead of applying the attribute to each model: -->
편의를 위해 모든 모델을 연관관계 없이 직렬화하고 싶다면 각 모델에 속성을 적용하는 대신 클래스 전체에 `WithoutRelations` 속성을 적용할 수 있습니다.

```php
<?php

namespace App\Jobs;

use App\Models\DistributionPlatform;
use App\Models\Podcast;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\WithoutRelations;

#[WithoutRelations]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

<!-- If a job receives a collection or array of Eloquent models instead of a single model, the models within that collection will not have their relationships restored when the job is deserialized and executed. This is to prevent excessive resource usage on jobs that deal with large numbers of models. -->
잡이 단일 모델 대신 Eloquent 모델 컬렉션이나 배열을 받는 경우, 해당 컬렉션 안의 모델은 잡이 역직렬화되어 실행될 때 연관관계가 복원되지 않습니다. 이는 많은 수의 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위한 것입니다.

<a name="unique-jobs"></a>
<!-- ### Unique Jobs -->
### Unique Jobs

> [!WARNING]
> 고유 잡은 [locks](/docs/13.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 고유 잡 제약 조건은 배치 내 잡에는 적용되지 않습니다.

<!-- Sometimes, you may want to ensure that only one instance of a specific job is on the queue at any point in time. You may do so by implementing the `ShouldBeUnique` interface on your job class. This interface does not require you to define any additional methods on your class: -->
때로는 특정 잡의 인스턴스가 어느 시점에도 큐에 하나만 존재하도록 보장하고 싶을 수 있습니다. 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 그렇게 할 수 있습니다. 이 인터페이스는 클래스에 추가 메서드를 정의할 것을 요구하지 않습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

<!-- In the example above, the `UpdateSearchIndex` job is unique. So, the job will not be dispatched if another instance of the job is already on the queue and has not finished processing. -->
위 예제에서 `UpdateSearchIndex` 잡은 고유합니다. 따라서 해당 잡의 다른 인스턴스가 이미 큐에 있고 아직 처리가 끝나지 않았다면, 새 잡은 디스패치되지 않습니다.

<!-- In certain cases, you may want to define a specific "key" that makes the job unique or you may want to specify a timeout beyond which the job no longer stays unique. To accomplish this, you may use the `UniqueFor` attribute and define a `uniqueId` method on your job class: -->
특정한 경우에는 잡을 고유하게 만드는 특정 "키"를 정의하고 싶거나, 잡이 더 이상 고유 상태를 유지하지 않는 타임아웃을 지정하고 싶을 수 있습니다. 이를 위해 `UniqueFor` 속성을 사용하고 잡 클래스에 `uniqueId` 메서드를 정의할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Queue\Attributes\UniqueFor;

#[UniqueFor(3600)]
class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * Get the unique ID for the job.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```
<!-- In the example above, the `UpdateSearchIndex` job is unique by a product ID. So, any new dispatches of the job with the same product ID will be ignored until the existing job has completed processing. In addition, if the existing job is not processed within one hour, the unique lock will be released and another job with the same unique key can be dispatched to the queue. -->
위 예제에서 `UpdateSearchIndex` 잡은 제품 ID를 기준으로 고유합니다. 따라서 같은 제품 ID를 가진 새 잡 디스패치는 기존 잡 처리가 완료될 때까지 무시됩니다. 또한 기존 잡이 한 시간 안에 처리되지 않으면 고유 락이 해제되고, 같은 고유 키를 가진 다른 잡을 큐에 디스패치할 수 있습니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버 또는 컨테이너에서 잡을 디스패치한다면, Laravel이 잡의 고유 여부를 정확하게 판단할 수 있도록 모든 서버가 동일한 중앙 캐시 서버와 통신하는지 확인해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
<!-- #### Keeping Jobs Unique Until Processing Begins -->
#### Keeping Jobs Unique Until Processing Begins

<!-- By default, unique jobs are "unlocked" after a job completes processing or fails all of its retry attempts. However, there may be situations where you would like your job to unlock immediately before it is processed. To accomplish this, your job should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract: -->
기본적으로 고유 잡은 잡 처리가 완료되거나 모든 재시도 시도가 실패한 뒤 "잠금 해제"됩니다. 하지만 잡이 처리되기 직전에 즉시 잠금 해제되기를 원하는 상황도 있을 수 있습니다. 이를 위해 잡은 `ShouldBeUnique` 계약 대신 `ShouldBeUniqueUntilProcessing` 계약을 구현해야 합니다.

```php
<?php

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

<!-- Behind the scenes, when a `ShouldBeUnique` job is dispatched, Laravel attempts to acquire a [lock](/docs/13.x/cache#atomic-locks) with the `uniqueId` key. If the lock is already held, the job is not dispatched. This lock is released when the job completes processing or fails all of its retry attempts. By default, Laravel will use the default cache driver to obtain this lock. However, if you wish to use another driver for acquiring the lock, you may define a `uniqueVia` method that returns the cache driver that should be used: -->
내부적으로 `ShouldBeUnique` 잡이 디스패치되면 Laravel은 `uniqueId` 키로 [lock](/docs/13.x/cache#atomic-locks)을 획득하려고 시도합니다. 이미 락이 유지되고 있다면 잡은 디스패치되지 않습니다. 이 락은 잡의 처리가 완료되거나 모든 재시도 횟수를 소진하고 실패하면 해제됩니다. 기본적으로 Laravel은 이 락을 획득할 때 기본 캐시 드라이버를 사용합니다. 하지만 락을 획득하는 데 다른 드라이버를 사용하려면 사용할 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique job lock.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 잡의 동시 처리만 제한하려는 경우에는 대신 [WithoutOverlapping](/docs/13.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="debounced-jobs"></a>
<!-- ### Debounced Jobs -->
### Debounced Jobs

<!-- Sometimes, you may want to ensure that when the same job is dispatched many times in a short window, only the latest dispatch actually executes. You may do so by adding the `DebounceFor` attribute to your job: -->
때로는 동일한 작업이 짧은 시간 동안 여러 번 dispatch될 때, 가장 마지막 dispatch만 실제로 실행되도록 보장하고 싶을 수 있습니다. 이를 위해 작업에 `DebounceFor` 속성을 추가할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\DebounceFor;

#[DebounceFor(30)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(public int $productId)
    {
    }

    /**
     * Get the debounce ID for the job.
     */
    public function debounceId(): string
    {
        return (string) $this->productId;
    }
}
```

<!-- In the example above, repeatedly dispatching `UpdateSearchIndex` for the same product within `30` seconds will debounce the job so that only the latest dispatch runs. -->
위 예시에서는 동일한 상품에 대해 `30`초 안에 `UpdateSearchIndex`를 반복해서 dispatch하면 작업이 debounce되어, 가장 마지막 dispatch만 실행됩니다.

<!-- If you would like to cap how long a frequently re-dispatched job can be deferred, you may provide the `maxWait` argument to the `DebounceFor` attribute: -->
자주 다시 dispatch되는 작업이 지연될 수 있는 최대 시간을 제한하려면 `DebounceFor` 속성에 `maxWait` 인수를 제공할 수 있습니다.

```php
#[DebounceFor(30, maxWait: 120)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    // ...
}
```

<!-- You may customize the cache store used for debounce tracking by defining a `debounceVia` method on your job: -->
작업에 `debounceVia` 메서드를 정의하여 debounce 추적에 사용할 cache store를 직접 지정할 수 있습니다.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

public function debounceVia(): Repository
{
    return Cache::driver('redis');
}
```

<!-- If a debounced job is superseded by a newer dispatch, Laravel will dispatch the `Illuminate\Queue\Events\JobDebounced` event and remove the superseded job from the queue. -->
debounce된 작업이 더 새로운 dispatch로 대체되면, Laravel은 `Illuminate\Queue\Events\JobDebounced` 이벤트를 dispatch하고 대체된 작업을 큐에서 제거합니다.

> [!WARNING]
> 디바운스된 잡과 고유 잡은 함께 사용할 수 없습니다. `DebounceFor` 속성을 사용하는 잡은 `ShouldBeUnique`를 구현해서는 안 됩니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버 또는 컨테이너에서 디바운스된 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버와 통신하는지 확인해야 합니다.

<a name="encrypted-jobs"></a>
<!-- ### Encrypted Jobs -->
### Encrypted Jobs

<!-- Laravel allows you to ensure the privacy and integrity of a job's data via [encryption](/docs/13.x/encryption). To get started, simply add the `ShouldBeEncrypted` interface to the job class. Once this interface has been added to the class, Laravel will automatically encrypt your job before pushing it onto a queue: -->
Laravel은 [encryption](/docs/13.x/encryption)을 통해 잡 데이터의 기밀성과 무결성을 보장할 수 있습니다. 시작하려면 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 클래스에 이 인터페이스를 추가하면 Laravel은 큐에 넣기 전에 잡을 자동으로 암호화합니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class UpdateSearchIndex implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a name="job-middleware"></a>
<!-- ## Job Middleware -->
## Job Middleware

<!-- Job middleware allow you to wrap custom logic around the execution of queued jobs, reducing boilerplate in the jobs themselves. For example, consider the following `handle` method which leverages Laravel's Redis rate limiting features to allow only one job to process every five seconds: -->
잡 미들웨어를 사용하면 큐에 등록된 잡의 실행 전후에 사용자 정의 로직을 감쌀 수 있어, 잡 자체의 반복 코드를 줄일 수 있습니다. 예를 들어, 다음 `handle` 메서드는 Laravel의 Redis 처리율 제한 기능을 활용하여 5초마다 하나의 잡만 처리되도록 합니다.

```php
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
```

<!-- While this code is valid, the implementation of the `handle` method becomes noisy since it is cluttered with Redis rate limiting logic. In addition, this rate limiting logic must be duplicated for any other jobs that we want to rate limit. Instead of rate limiting in the handle method, we could define a job middleware that handles rate limiting: -->
이 코드는 유효하지만, `handle` 메서드 구현이 Redis 처리율 제한 로직으로 복잡해져 읽기 어려워집니다. 또한 처리율 제한이 필요한 다른 잡마다 이 로직을 중복해서 작성해야 합니다. handle 메서드 안에서 처리율을 제한하는 대신, 처리율 제한을 담당하는 잡 미들웨어를 정의할 수 있습니다.

```php
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
```

<!-- As you can see, like [route middleware](/docs/13.x/middleware), job middleware receive the job being processed and a callback that should be invoked to continue processing the job. -->
보시다시피 [route middleware](/docs/13.x/middleware)와 마찬가지로 잡 미들웨어는 처리 중인 잡과 잡 처리를 계속하려면 호출해야 하는 콜백을 전달받습니다.

<!-- You can generate a new job middleware class using the `make:job-middleware` Artisan command. After creating job middleware, they may be attached to a job by returning them from the job's `middleware` method. This method does not exist on jobs scaffolded by the `make:job` Artisan command, so you will need to manually add it to your job class: -->
`make:job-middleware` Artisan 명령어를 사용하여 새로운 잡 미들웨어 클래스를 생성할 수 있습니다. 잡 미들웨어를 만든 뒤에는 잡의 `middleware` 메서드에서 반환하여 잡에 연결할 수 있습니다. 이 메서드는 `make:job` Artisan 명령어로 스캐폴딩된 잡에는 존재하지 않으므로, 잡 클래스에 직접 추가해야 합니다.

```php
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
```

> [!NOTE]
> 잡 미들웨어는 [queueable event listeners](/docs/13.x/events#queued-event-listeners), [mailables](/docs/13.x/mail#queueing-mail), [notifications](/docs/13.x/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
<!-- ### Rate Limiting -->
### Rate Limiting

<!-- Although we just demonstrated how to write your own rate limiting job middleware, Laravel actually includes a rate limiting middleware that you may utilize to rate limit jobs. Like [route rate limiters](/docs/13.x/routing#defining-rate-limiters), job rate limiters are defined using the `RateLimiter` facade's `for` method. -->
방금 직접 레이트 리미팅 잡 미들웨어를 작성하는 방법을 살펴봤지만, Laravel에는 잡의 실행 속도를 제한하는 데 사용할 수 있는 레이트 리미팅 미들웨어가 실제로 포함되어 있습니다. [route rate limiters](/docs/13.x/routing#defining-rate-limiters)와 마찬가지로 잡 레이트 리미터는 `RateLimiter` 파사드의 `for` 메서드를 사용해 정의합니다.

<!-- For example, you may wish to allow users to backup their data once per hour while imposing no such limit on premium customers. To accomplish this, you may define a `RateLimiter` in the `boot` method of your `AppServiceProvider`: -->
예를 들어, 일반 사용자는 한 시간에 한 번만 데이터를 백업할 수 있도록 제한하되, 프리미엄 고객에게는 이러한 제한을 적용하지 않고 싶을 수 있습니다. 이를 위해 `AppServiceProvider`의 `boot` 메서드에서 `RateLimiter`를 정의할 수 있습니다.

```php
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
```

<!-- In the example above, we defined an hourly rate limit; however, you may easily define a rate limit based on minutes using the `perMinute` method. In addition, you may pass any value you wish to the `by` method of the rate limit; however, this value is most often used to segment rate limits by customer: -->
위 예시에서는 시간 단위 처리율 제한을 정의했습니다. 하지만 `perMinute` 메서드를 사용하면 분 단위 처리율 제한도 쉽게 정의할 수 있습니다. 또한 처리율 제한의 `by` 메서드에는 원하는 어떤 값이든 전달할 수 있지만, 이 값은 주로 고객별로 처리율 제한을 나누는 데 사용됩니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

<!-- Once you have defined your rate limit, you may attach the rate limiter to your job using the `Illuminate\Queue\Middleware\RateLimited` middleware. Each time the job exceeds the rate limit, this middleware will release the job back to the queue with an appropriate delay based on the rate limit duration: -->
처리율 제한을 정의한 뒤에는 `Illuminate\Queue\Middleware\RateLimited` middleware를 사용하여 rate limiter를 작업에 연결할 수 있습니다. 작업이 처리율 제한을 초과할 때마다 이 middleware는 처리율 제한 기간에 따라 적절한 지연 시간을 적용하여 작업을 다시 큐로 반환합니다.

```php
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
```

<!-- Releasing a rate limited job back onto the queue will still increment the job's total number of `attempts`. You may wish to tune your `Tries` and `MaxExceptions` attributes on your job class accordingly. Or, you may wish to use the [retryUntil method](#time-based-attempts) to define the amount of time until the job should no longer be attempted. -->
처리율 제한으로 작업이 다시 큐에 반환되더라도, 작업의 총 `attempts` 횟수는 증가합니다. 따라서 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 그에 맞게 조정하는 것이 좋습니다. 또는 [retryUntil method](#time-based-attempts)를 사용하여 작업을 더 이상 시도하지 않을 시간을 정의할 수도 있습니다.

<!-- Using the `releaseAfter` method, you may also specify the number of seconds that must elapse before the released job will be attempted again: -->
`releaseAfter` 메서드를 사용하면 반환된 작업을 다시 시도하기 전에 지나야 하는 초 단위 시간을 지정할 수도 있습니다.

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

<!-- If you do not want a job to be retried when it is rate limited, you may use the `dontRelease` method: -->
작업이 처리율 제한에 걸렸을 때 다시 시도하지 않게 하려면 `dontRelease` 메서드를 사용할 수 있습니다.

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

<a name="rate-limiting-with-redis"></a>
<!-- #### Rate Limiting With Redis -->
#### Rate Limiting With Redis

<!-- If you are using Redis, you may use the `Illuminate\Queue\Middleware\RateLimitedWithRedis` middleware, which is fine-tuned for Redis and more efficient than the basic rate limiting middleware: -->
Redis를 사용하고 있다면 `Illuminate\Queue\Middleware\RateLimitedWithRedis` middleware를 사용할 수 있습니다. 이 middleware는 Redis에 맞게 조정되어 있으며 기본 처리율 제한 middleware보다 더 효율적입니다.

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

<!-- The `connection` method may be used to specify which Redis connection the middleware should use: -->
`connection` 메서드를 사용하면 미들웨어가 사용할 Redis 연결을 지정할 수 있습니다:

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a name="preventing-job-overlaps"></a>
<!-- ### Preventing Job Overlaps -->
### Preventing Job Overlaps

<!-- Laravel includes an `Illuminate\Queue\Middleware\WithoutOverlapping` middleware that allows you to prevent job overlaps based on an arbitrary key. This can be helpful when a queued job is modifying a resource that should only be modified by one job at a time. -->
Laravel에는 임의의 키를 기준으로 작업의 중복 실행을 방지할 수 있는 `Illuminate\Queue\Middleware\WithoutOverlapping` middleware가 포함되어 있습니다. 큐 작업이 한 번에 하나의 작업만 수정해야 하는 리소스를 수정하는 경우 유용합니다.

<!-- For example, let's imagine you have a queued job that updates a user's credit score and you want to prevent credit score update job overlaps for the same user ID. To accomplish this, you can return the `WithoutOverlapping` middleware from your job's `middleware` method: -->
예를 들어, 사용자의 신용 점수를 업데이트하는 큐 작업이 있고 동일한 사용자 ID에 대해 신용 점수 업데이트 작업이 중복 실행되지 않도록 하고 싶다고 가정해 보겠습니다. 이를 위해 작업의 `middleware` 메서드에서 `WithoutOverlapping` middleware를 반환할 수 있습니다.

```php
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
```

<!-- Releasing an overlapping job back onto the queue will still increment the job's total number of attempts. You may wish to tune your `Tries` and `MaxExceptions` attributes on your job class accordingly. For example, leaving `Tries` to 1 as it is by default would prevent any overlapping job from being retried later. -->
중복 실행되는 작업을 다시 큐에 반환하더라도 작업의 총 시도 횟수는 증가합니다. 따라서 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 그에 맞게 조정하는 것이 좋습니다. 예를 들어 기본값처럼 `Tries`를 1로 두면, 중복 실행된 작업은 나중에 다시 시도되지 않습니다.

<!-- Any overlapping jobs of the same type will be released back to the queue. You may also specify the number of seconds that must elapse before the released job will be attempted again: -->
같은 타입의 모든 중복 작업은 다시 큐로 반환됩니다. 또한 반환된 작업을 다시 시도하기 전에 지나야 하는 초 단위 시간을 지정할 수도 있습니다.

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

<!-- If you wish to immediately delete any overlapping jobs so that they will not be retried, you may use the `dontRelease` method: -->
중복 실행되는 작업을 즉시 삭제하여 다시 시도되지 않게 하려면 `dontRelease` 메서드를 사용할 수 있습니다.

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

<!-- The `WithoutOverlapping` middleware is powered by Laravel's atomic lock feature. Sometimes, your job may unexpectedly fail or timeout in such a way that the lock is not released. Therefore, you may explicitly define a lock expiration time using the `expireAfter` method. For example, the example below will instruct Laravel to release the `WithoutOverlapping` lock three minutes after the job has started processing: -->
`WithoutOverlapping` middleware는 Laravel의 atomic lock 기능을 기반으로 동작합니다. 때로는 작업이 예기치 않게 실패하거나 timeout되어 lock이 해제되지 않을 수 있습니다. 따라서 `expireAfter` 메서드를 사용해 lock 만료 시간을 명시적으로 정의할 수 있습니다. 예를 들어 아래 예시는 작업 처리가 시작된 지 3분 후 Laravel이 `WithoutOverlapping` lock을 해제하도록 지시합니다.

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어를 사용하려면 [locks](/docs/13.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>
<!-- #### Sharing Lock Keys Across Job Classes -->
#### Sharing Lock Keys Across Job Classes

<!-- By default, the `WithoutOverlapping` middleware will only prevent overlapping jobs of the same class. So, although two different job classes may use the same lock key, they will not be prevented from overlapping. However, you can instruct Laravel to apply the key across job classes using the `shared` method: -->
기본적으로 `WithoutOverlapping` middleware는 같은 클래스의 작업끼리만 중복 실행을 방지합니다. 따라서 서로 다른 두 작업 클래스가 같은 lock key를 사용하더라도, 서로 중복 실행되는 것은 방지되지 않습니다. 하지만 `shared` 메서드를 사용하면 Laravel이 해당 키를 작업 클래스 전체에 적용하도록 지시할 수 있습니다.

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
<!-- ### Throttling Exceptions -->
### Throttling Exceptions

<!-- Laravel includes a `Illuminate\Queue\Middleware\ThrottlesExceptions` middleware that allows you to throttle exceptions. Once the job throws a given number of exceptions, all further attempts to execute the job are delayed until a specified time interval lapses. This middleware is particularly useful for jobs that interact with third-party services that are unstable. -->
Laravel에는 예외 발생을 throttle할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` middleware가 포함되어 있습니다. 작업이 지정된 횟수만큼 예외를 던지면, 이후의 모든 작업 실행 시도는 지정된 시간 간격이 지날 때까지 지연됩니다. 이 middleware는 불안정한 서드파티 서비스와 상호작용하는 작업에 특히 유용합니다.

<!-- For example, let's imagine a queued job that interacts with a third-party API that begins throwing exceptions. To throttle exceptions, you can return the `ThrottlesExceptions` middleware from your job's `middleware` method. Typically, this middleware should be paired with a job that implements [time based attempts](#time-based-attempts): -->
예를 들어, 예외를 던지기 시작한 서드파티 API와 상호작용하는 큐 작업이 있다고 가정해 보겠습니다. 예외를 throttle하려면 작업의 `middleware` 메서드에서 `ThrottlesExceptions` middleware를 반환할 수 있습니다. 일반적으로 이 middleware는 [time based attempts](#time-based-attempts)를 구현한 작업과 함께 사용해야 합니다.

```php
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
    return now()->plus(minutes: 30);
}
```

<!-- The first constructor argument accepted by the middleware is the number of exceptions the job can throw before being throttled, while the second constructor argument is the number of seconds that should elapse before the job is attempted again once it has been throttled. In the code example above, if the job throws 10 consecutive exceptions, we will wait 5 minutes before attempting the job again, constrained by the 30-minute time limit. -->
middleware가 받는 첫 번째 생성자 인수는 작업이 throttle되기 전에 던질 수 있는 예외 횟수이며, 두 번째 생성자 인수는 작업이 throttle된 후 다시 시도되기 전에 지나야 하는 초 단위 시간입니다. 위 코드 예시에서 작업이 연속으로 10번 예외를 던지면, 30분 시간 제한 안에서 5분을 기다린 뒤 작업을 다시 시도합니다.

<!-- When a job throws an exception but the exception threshold has not yet been reached, the job will typically be retried immediately. However, you may specify the number of minutes such a job should be delayed by calling the `backoff` method when attaching the middleware to the job: -->
잡에서 예외가 발생했지만 예외 임계값에 아직 도달하지 않았다면 일반적으로 해당 잡은 즉시 재시도됩니다. 그러나 잡에 미들웨어를 연결할 때 `backoff` 메서드를 호출하면 해당 잡의 재시도까지 지연할 시간을 분 단위로 지정할 수 있습니다:

```php
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
```

<!-- The `backoff` method also accepts a closure that receives the thrown exception, allowing the delay to be determined dynamically: -->
`backoff` 메서드는 던져진 예외를 받는 클로저도 허용하므로, 지연 시간을 동적으로 결정할 수 있습니다:

```php
use App\Exceptions\RateLimitedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;
use Throwable;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(
        fn (Throwable $throwable) => $throwable instanceof RateLimitedException
            ? $throwable->retryAfterMinutes()
            : 5
    )];
}
```

<!-- Internally, this middleware uses Laravel's cache system to implement rate limiting, and the job's class name is utilized as the cache "key". You may override this key by calling the `by` method when attaching the middleware to your job. This may be useful if you have multiple jobs interacting with the same third-party service and you would like them to share a common throttling "bucket" ensuring they respect a single shared limit: -->
내부적으로 이 미들웨어는 Laravel의 캐시 시스템을 사용하여 속도 제한을 구현하며, 작업의 클래스명이 캐시 "key"로 사용됩니다. 작업에 미들웨어를 연결할 때 `by` 메서드를 호출하여 이 키를 재정의할 수 있습니다. 같은 서드파티 서비스와 상호작용하는 여러 작업이 있고, 이 작업들이 하나의 공유 제한을 지키도록 공통 제한 "bucket"을 공유하게 만들고 싶을 때 유용할 수 있습니다.

```php
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
```

<!-- By default, this middleware will throttle every exception. You can modify this behavior by invoking the `when` method when attaching the middleware to your job. The exception will then only be throttled if the closure provided to the `when` method returns `true`: -->
기본적으로 이 미들웨어는 모든 예외를 제한합니다. 작업에 미들웨어를 연결할 때 `when` 메서드를 호출하여 이 동작을 수정할 수 있습니다. 그러면 `when` 메서드에 제공한 클로저가 `true`를 반환하는 경우에만 예외가 제한됩니다.

```php
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
```

<!-- Unlike the `when` method, which releases the job back onto the queue or throws an exception, the `deleteWhen` method allows you to delete the job entirely when a given exception occurs: -->
작업을 다시 큐로 반환하거나 예외를 던지는 `when` 메서드와 달리, `deleteWhen` 메서드를 사용하면 특정 예외가 발생했을 때 작업을 완전히 삭제할 수 있습니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

<!-- If you would like to have the throttled exceptions reported to your application's exception handler, you can do so by invoking the `report` method when attaching the middleware to your job. Optionally, you may provide a closure to the `report` method and the exception will only be reported if the given closure returns `true`: -->
제한된 예외를 애플리케이션의 예외 핸들러에 보고하고 싶다면, 작업에 미들웨어를 연결할 때 `report` 메서드를 호출하면 됩니다. 선택 사항으로 `report` 메서드에 클로저를 제공할 수 있으며, 이 경우 주어진 클로저가 `true`를 반환할 때만 예외가 보고됩니다.

```php
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
```

<a name="throttling-exceptions-with-redis"></a>
<!-- #### Throttling Exceptions With Redis -->
#### Throttling Exceptions With Redis

<!-- If you are using Redis, you may use the `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` middleware, which is fine-tuned for Redis and more efficient than the basic exception throttling middleware: -->
Redis를 사용하고 있다면 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 Redis에 맞게 세밀하게 조정되어 있으며, 기본 예외 제한 미들웨어보다 더 효율적입니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

<!-- The `connection` method may be used to specify which Redis connection the middleware should use: -->
`connection` 메서드를 사용하면 미들웨어에서 사용할 Redis 연결을 지정할 수 있습니다:

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a name="releasing-jobs"></a>
<!-- ### Releasing Jobs -->
### Releasing Jobs

<!-- The `Release` middleware allows you to release a job back onto the queue without executing it. The `Release::when` method will release the job if the given condition evaluates to `true`, while the `Release::unless` method will release the job if the condition evaluates to `false`: -->
`Release` 미들웨어를 사용하면 잡을 실행하지 않고 큐로 다시 반환할 수 있습니다. `Release::when` 메서드는 주어진 조건이 `true`로 평가되면 잡을 반환하고, `Release::unless` 메서드는 조건이 `false`로 평가되면 잡을 반환합니다:

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when($condition, releaseAfter: 60),
    ];
}
```

<!-- Releasing a job back onto the queue will still increment the job's total number of attempts. You may wish to tune your `Tries` and `MaxExceptions` attributes on your job class accordingly. -->
잡을 큐로 다시 반환해도 잡의 총 시도 횟수는 계속 증가합니다. 이에 맞게 잡 클래스의 `Tries`와 `MaxExceptions` 속성을 조정하는 것이 좋을 수 있습니다.

<!-- You can also pass a `Closure` to the `when` and `unless` methods for more complex conditional evaluation: -->
더 복잡한 조건 평가를 위해 `when` 및 `unless` 메서드에 `Closure`를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when(function (): bool {
            return ! $this->order->isPaid();
        }, releaseAfter: 60),
    ];
}
```

<a name="skipping-jobs"></a>
<!-- ### Skipping Jobs -->
### Skipping Jobs

<!-- The `Skip` middleware allows you to specify that a job should be skipped / deleted without needing to modify the job's logic. The `Skip::when` method will delete the job if the given condition evaluates to `true`, while the `Skip::unless` method will delete the job if the condition evaluates to `false`: -->
`Skip` 미들웨어를 사용하면 작업의 로직을 수정하지 않고도 작업을 건너뛰거나 삭제하도록 지정할 수 있습니다. `Skip::when` 메서드는 주어진 조건이 `true`로 평가되면 작업을 삭제하고, `Skip::unless` 메서드는 조건이 `false`로 평가되면 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

<!-- You can also pass a `Closure` to the `when` and `unless` methods for more complex conditional evaluation: -->
더 복잡한 조건 평가를 위해 `when` 및 `unless` 메서드에 `Closure`를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```

<a name="dispatching-jobs"></a>
<!-- ## Dispatching Jobs -->
## Dispatching Jobs

<!-- Once you have written your job class, you may dispatch it using the `dispatch` method on the job itself. The arguments passed to the `dispatch` method will be given to the job's constructor: -->
작업 클래스를 작성한 후에는 작업 자체의 `dispatch` 메서드를 사용하여 디스패치할 수 있습니다. `dispatch` 메서드에 전달된 인수는 작업의 생성자에 전달됩니다.

```php
<?php

namespace App\Http\Controllers;

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
```

<!-- If you would like to conditionally dispatch a job, you may use the `dispatchIf` and `dispatchUnless` methods: -->
조건부로 작업을 디스패치하고 싶다면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

<!-- In new Laravel applications, the `database` connection is defined as the default queue. You may specify a different default queue connection by changing the `QUEUE_CONNECTION` environment variable in your application's `.env` file. -->
새 Laravel 애플리케이션에서는 `database` 연결이 기본 큐로 정의되어 있습니다. 애플리케이션의 `.env` 파일에서 `QUEUE_CONNECTION` 환경 변수를 변경하여 다른 기본 큐 연결을 지정할 수 있습니다.

<a name="delayed-dispatching"></a>
<!-- ### Delayed Dispatching -->
### Delayed Dispatching

<!-- If you would like to specify that a job should not be immediately available for processing by a queue worker, you may use the `delay` method when dispatching the job. For example, let's specify that a job should not be available for processing until 10 minutes after it has been dispatched: -->
작업이 큐 워커에 의해 즉시 처리 가능한 상태가 되지 않도록 지정하고 싶다면, 작업을 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업이 디스패치된 후 10분이 지나기 전까지 처리 가능한 상태가 되지 않도록 지정해 보겠습니다.

```php
<?php

namespace App\Http\Controllers;

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
            ->delay(now()->plus(minutes: 10));

        return redirect('/podcasts');
    }
}
```

<!-- In some cases, jobs may have a default delay configured. If you need to bypass this delay and dispatch a job for immediate processing, you may use the `withoutDelay` method: -->
경우에 따라 작업에 기본 지연 시간이 설정되어 있을 수 있습니다. 이 지연 시간을 우회하고 작업을 즉시 처리하도록 디스패치해야 한다면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스의 최대 지연 시간은 15분입니다.

<a name="synchronous-dispatching"></a>
<!-- ### Synchronous Dispatching -->
### Synchronous Dispatching

<!-- If you would like to dispatch a job immediately (synchronously), you may use the `dispatchSync` method. When using this method, the job will not be queued and will be executed immediately within the current process: -->
작업을 즉시, 즉 동기적으로 디스패치하고 싶다면 `dispatchSync` 메서드를 사용할 수 있습니다. 이 메서드를 사용하면 작업은 큐에 들어가지 않고 현재 프로세스 안에서 즉시 실행됩니다.

```php
<?php

namespace App\Http\Controllers;

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
```

<a name="deferred-dispatching"></a>
<!-- #### Deferred Dispatching -->
#### Deferred Dispatching

<!-- Using deferred synchronous dispatching, you can dispatch a job to be processed during the current process, but after the HTTP response has been sent to the user. This allows you to process "queued" jobs synchronously without slowing down your user's application experience. To defer the execution of a synchronous job, dispatch the job to the `deferred` connection: -->
지연된 동기 디스패치를 사용하면 현재 프로세스에서 작업을 처리하도록 디스패치하되, HTTP 응답이 사용자에게 전송된 뒤에 처리되도록 할 수 있습니다. 이를 통해 사용자의 애플리케이션 경험을 느리게 만들지 않으면서 "큐에 들어간" 작업을 동기적으로 처리할 수 있습니다. 동기 작업의 실행을 지연하려면 작업을 `deferred` 연결로 디스패치하십시오.

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```

<!-- The `deferred` connection also serves as the default [failover queue](#queue-failover). -->
`deferred` 연결은 기본 [failover queue](#queue-failover)로도 사용됩니다.

<!-- Similarly, the `background` connection processes jobs after the HTTP response has been sent to the user; however, the job is processed in a separately spawned PHP process, allowing the PHP-FPM / application worker to be available to handle another incoming HTTP request: -->
마찬가지로 `background` 연결도 HTTP 응답이 사용자에게 전송된 뒤 작업을 처리합니다. 다만 이 경우 작업은 별도로 생성된 PHP 프로세스에서 처리되므로, PHP-FPM / 애플리케이션 워커는 다른 들어오는 HTTP 요청을 처리할 수 있는 상태가 됩니다.

```php
RecordDelivery::dispatch($order)->onConnection('background');
```

<a name="bulk-dispatching"></a>
<!-- ### Bulk Dispatching -->
### Bulk Dispatching

<!-- If you need to dispatch many independent jobs at once and do not need [batch](#job-batching) tracking or callbacks, you may use the `bulk` method of the `Bus` facade. Laravel will group the jobs by their configured queue connection and queue name and push each group to the appropriate queue in bulk: -->
한 번에 많은 독립적인 잡을 디스패치해야 하고 [batch](#job-batching) 추적이나 콜백이 필요하지 않다면, `Bus` 파사드의 `bulk` 메서드를 사용할 수 있습니다. Laravel은 설정된 큐 연결과 큐 이름에 따라 잡을 그룹화한 뒤, 각 그룹을 적절한 큐에 대량으로 푸시합니다.

```php
use App\Jobs\ProcessUser;
use Illuminate\Support\Facades\Bus;

Bus::bulk(
    $users->map(fn ($user) => new ProcessUser($user))
);
```

<a name="preparing-jobs-before-dispatch"></a>
<!-- ### Preparing Jobs Before Dispatch -->
### Preparing Jobs Before Dispatch

<!-- If a job needs to prepare or inspect its state before it is pushed onto the queue, the job may implement the `Illuminate\Contracts\Queue\PreparesForDispatch` interface. Laravel will invoke the job's `prepareForDispatch` method before dispatching the job. If this method returns `false`, the job will not be dispatched: -->
잡이 큐에 푸시되기 전에 자신의 상태를 준비하거나 검사해야 한다면, 잡은 `Illuminate\Contracts\Queue\PreparesForDispatch` 인터페이스를 구현할 수 있습니다. Laravel은 잡을 디스패치하기 전에 잡의 `prepareForDispatch` 메서드를 호출합니다. 이 메서드가 `false`를 반환하면 잡은 디스패치되지 않습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\PreparesForDispatch;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Cache;

class SyncPodcasts implements PreparesForDispatch, ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public array $podcastIds,
    ) {}

    /**
     * Prepare the job before dispatching.
     */
    public function prepareForDispatch(): bool
    {
        return collect($this->podcastIds)
            ->reject(fn (int $id) => Cache::has("podcast-syncing:{$id}"))
            ->isNotEmpty();
    }
}
```

<a name="jobs-and-database-transactions"></a>
<!-- ### Jobs & Database Transactions -->
### Jobs & Database Transactions

<!-- While it is perfectly fine to dispatch jobs within database transactions, you should take special care to ensure that your job will actually be able to execute successfully. When dispatching a job within a transaction, it is possible that the job will be processed by a worker before the parent transaction has committed. When this happens, any updates you have made to models or database records during the database transaction(s) may not yet be reflected in the database. In addition, any models or database records created within the transaction(s) may not exist in the database. -->
데이터베이스 트랜잭션 안에서 작업을 디스패치하는 것 자체는 전혀 문제가 없지만, 작업이 실제로 성공적으로 실행될 수 있는지 각별히 주의해야 합니다. 트랜잭션 안에서 작업을 디스패치할 때, 부모 트랜잭션이 커밋되기 전에 워커가 해당 작업을 처리할 수 있습니다. 이런 일이 발생하면 데이터베이스 트랜잭션 중에 모델이나 데이터베이스 레코드에 적용한 업데이트가 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한 트랜잭션 안에서 생성한 모델이나 데이터베이스 레코드가 아직 데이터베이스에 존재하지 않을 수도 있습니다.

<!-- Thankfully, Laravel provides several methods of working around this problem. First, you may set the `after_commit` connection option in your queue connection's configuration array: -->
다행히 Laravel은 이 문제를 우회할 수 있는 여러 메서드를 제공합니다. 먼저 큐 연결의 설정 배열에서 `after_commit` 연결 옵션을 설정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

<!-- When the `after_commit` option is `true`, you may dispatch jobs within database transactions; however, Laravel will wait until the open parent database transactions have been committed before actually dispatching the job. Of course, if no database transactions are currently open, the job will be dispatched immediately. -->
`after_commit` 옵션이 `true`이면 데이터베이스 트랜잭션 안에서 작업을 디스패치할 수 있습니다. 다만 Laravel은 열려 있는 부모 데이터베이스 트랜잭션이 커밋될 때까지 기다린 뒤 실제로 작업을 디스패치합니다. 물론 현재 열려 있는 데이터베이스 트랜잭션이 없다면 작업은 즉시 디스패치됩니다.

<!-- If a transaction is rolled back due to an exception that occurs during the transaction, the jobs that were dispatched during that transaction will be discarded. -->
트랜잭션 중에 발생한 예외로 인해 트랜잭션이 롤백되면, 해당 트랜잭션 중에 디스패치된 작업은 폐기됩니다.

> [!NOTE]
> `after_commit` 설정 옵션을 `true`로 설정하면 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후 큐에 등록된 이벤트 리스너, 메일러블, 알림 및 브로드캐스트 이벤트도 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
<!-- #### Specifying Commit Dispatch Behavior Inline -->
#### Specifying Commit Dispatch Behavior Inline

<!-- If you do not set the `after_commit` queue connection configuration option to `true`, you may still indicate that a specific job should be dispatched after all open database transactions have been committed. To accomplish this, you may chain the `afterCommit` method onto your dispatch operation: -->
`after_commit` 큐 연결 설정 옵션을 `true`로 설정하지 않았더라도, 특정 작업이 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 뒤 디스패치되어야 한다고 지정할 수 있습니다. 이를 위해 디스패치 작업에 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

<!-- Likewise, if the `after_commit` configuration option is set to `true`, you may indicate that a specific job should be dispatched immediately without waiting for any open database transactions to commit: -->
반대로 `after_commit` 설정 옵션이 `true`로 설정되어 있더라도, 특정 작업은 열려 있는 데이터베이스 트랜잭션의 커밋을 기다리지 않고 즉시 디스패치되어야 한다고 지정할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
<!-- ### Job Chaining -->
### Job Chaining

<!-- Job chaining allows you to specify a list of queued jobs that should be run in sequence after the primary job has executed successfully. If one job in the sequence fails, the rest of the jobs will not be run. To execute a queued job chain, you may use the `chain` method provided by the `Bus` facade. Laravel's command bus is a lower-level component that queued job dispatching is built on top of: -->
작업 체이닝을 사용하면 기본 작업이 성공적으로 실행된 뒤 순서대로 실행되어야 하는 큐 작업 목록을 지정할 수 있습니다. 순서 안의 어느 한 작업이 실패하면 나머지 작업은 실행되지 않습니다. 큐 작업 체인을 실행하려면 `Bus` 파사드가 제공하는 `chain` 메서드를 사용할 수 있습니다. Laravel의 command bus는 큐 작업 디스패치가 그 위에 구축되어 있는 더 저수준의 컴포넌트입니다.

```php
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
작업 클래스 인스턴스를 체이닝하는 것 외에도 클로저를 체이닝할 수 있습니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(/* ... */);
    },
])->dispatch();
```

> [!WARNING]
> 잡 내부에서 `$this->delete()` 메서드를 사용해 잡을 삭제해도 연결된 잡이 처리되는 것을 막을 수 없습니다. 체인 내의 잡이 실패한 경우에만 체인의 실행이 중단됩니다.

<a name="chain-connection-queue"></a>
<!-- #### Chain Connection and Queue -->
#### Chain Connection and Queue

<!-- If you would like to specify the connection and queue that should be used for the chained jobs, you may use the `onConnection` and `onQueue` methods. These methods specify the queue connection and queue name that should be used unless the queued job is explicitly assigned a different connection / queue: -->
체이닝된 작업에 사용할 연결과 큐를 지정하고 싶다면 `onConnection`과 `onQueue` 메서드를 사용할 수 있습니다. 이 메서드들은 큐 작업에 다른 연결 / 큐가 명시적으로 할당되어 있지 않은 한 사용할 큐 연결과 큐 이름을 지정합니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
<!-- #### Adding Jobs to the Chain -->
#### Adding Jobs to the Chain

<!-- Occasionally, you may need to prepend or append a job to an existing job chain from within another job in that chain. You may accomplish this using the `prependToChain` and `appendToChain` methods: -->
때로는 체인 안의 다른 작업 내부에서 기존 작업 체인의 앞이나 뒤에 작업을 추가해야 할 수 있습니다. `prependToChain`과 `appendToChain` 메서드를 사용하여 이를 수행할 수 있습니다.

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
<!-- #### Chain Failures -->
#### Chain Failures

<!-- When chaining jobs, you may use the `catch` method to specify a closure that should be invoked if a job within the chain fails. The given callback will receive the `Throwable` instance that caused the job failure: -->
작업을 체이닝할 때 `catch` 메서드를 사용하여 체인 안의 작업이 실패했을 때 호출될 클로저를 지정할 수 있습니다. 주어진 콜백은 작업 실패의 원인이 된 `Throwable` 인스턴스를 받습니다.

```php
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
> 체인 콜백은 직렬화된 후 Laravel 큐에서 나중에 실행되므로, 체인 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
<!-- ### Customizing the Queue and Connection -->
### Customizing the Queue and Connection

<a name="dispatching-to-a-particular-queue"></a>
<!-- #### Dispatching to a Particular Queue -->
#### Dispatching to a Particular Queue

<!-- By pushing jobs to different queues, you may "categorize" your queued jobs and even prioritize how many workers you assign to various queues. Keep in mind, this does not push jobs to different queue "connections" as defined by your queue configuration file, but only to specific queues within a single connection. To specify the queue, use the `onQueue` method when dispatching the job: -->
작업을 서로 다른 큐에 넣으면 큐에 들어간 작업을 "분류"할 수 있으며, 각 큐에 몇 개의 워커를 할당할지도 우선순위에 따라 조정할 수 있습니다. 단, 이는 큐 설정 파일에 정의된 서로 다른 큐 "연결"로 작업을 보내는 것이 아니라, 하나의 연결 안에 있는 특정 큐로만 보내는 것임을 기억해야 합니다. 큐를 지정하려면 작업을 디스패치할 때 `onQueue` 메서드를 사용합니다.

```php
<?php

namespace App\Http\Controllers;

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
```

<!-- Alternatively, you may specify the job's queue by calling the `onQueue` method within the job's constructor: -->
또는 작업의 생성자 안에서 `onQueue` 메서드를 호출하여 작업의 큐를 지정할 수도 있습니다.

```php
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
```

<a name="dispatching-to-a-particular-connection"></a>
<!-- #### Dispatching to a Particular Connection -->
#### Dispatching to a Particular Connection

<!-- If your application interacts with multiple queue connections, you may specify which connection to push a job to using the `onConnection` method: -->
애플리케이션이 여러 큐 연결과 상호작용한다면, `onConnection` 메서드를 사용하여 작업을 어떤 연결로 보낼지 지정할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

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
```

<!-- You may chain the `onConnection` and `onQueue` methods together to specify the connection and the queue for a job: -->
`onConnection` 메서드와 `onQueue` 메서드를 함께 체이닝하여 작업의 연결과 큐를 지정할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

<!-- Alternatively, you may specify the job's connection by calling the `onConnection` method within the job's constructor: -->
또는 작업의 생성자 안에서 `onConnection` 메서드를 호출하여 작업의 연결을 지정할 수도 있습니다.

```php
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
```

<a name="queue-routing"></a>
<!-- #### Queue Routing -->
#### Queue Routing

<!-- You may use the `Queue` facade's `route` method to define a default connection and queue for specific job classes. This is useful when you want to ensure certain jobs always use specific queues without needing to specify the connection or queue on the job. -->
`Queue` 파사드의 `route` 메서드를 사용하여 특정 작업 클래스에 대한 기본 연결과 큐를 정의할 수 있습니다. 특정 작업이 항상 지정된 큐를 사용하도록 보장하고 싶지만, 작업마다 연결이나 큐를 직접 지정하고 싶지는 않을 때 유용합니다.

<!-- In addition to routing specific job classes, you may also pass an interface, trait, or parent class to the `route` method. When you do this, any job that implements the interface, uses the trait, or extends the parent class will automatically use the configured connection and queue. -->
특정 작업 클래스를 라우팅하는 것 외에도, 인터페이스, 트레이트, 부모 클래스를 `route` 메서드에 전달할 수 있습니다. 이렇게 하면 해당 인터페이스를 구현하거나, 트레이트를 사용하거나, 부모 클래스를 상속하는 모든 작업이 설정된 연결과 큐를 자동으로 사용합니다.

<!-- Typically, you should call the `route` method from the `boot` method of a service provider: -->
일반적으로 서비스 프로바이더의 `boot` 메서드에서 `route` 메서드를 호출해야 합니다.

```php
use App\Concerns\RequiresVideo;
use App\Jobs\ProcessPodcast;
use App\Jobs\ProcessVideo;
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
    Queue::route(RequiresVideo::class, queue: 'video');
}
```

<!-- When a connection is specified without a queue, the job will be sent to the default queue: -->
큐 없이 연결만 지정하면 작업은 기본 큐로 전송됩니다.

```php
Queue::route(ProcessPodcast::class, connection: 'redis');
```

<!-- You may also route multiple job classes at once by passing an array to the `route` method: -->
`route` 메서드에 배열을 전달하여 여러 작업 클래스를 한 번에 라우팅할 수도 있습니다.

```php
Queue::route([
    ProcessPodcast::class => ['podcasts', 'redis'], // Queue and connection
    ProcessVideo::class => 'videos', // Queue only (uses default connection)
]);
```

> [!NOTE]
> 큐 라우팅은 잡별로 해당 잡에서 계속 재정의할 수 있습니다.

<a name="max-job-attempts-and-timeout"></a>
<!-- ### Specifying Max Job Attempts / Timeout Values -->
### Specifying Max Job Attempts / Timeout Values

<a name="max-attempts"></a>
<!-- #### Max Attempts -->
#### Max Attempts

<!-- Job attempts are a core concept of Laravel's queue system and power many advanced features. While they may seem confusing at first, it's important to understand how they work before modifying the default configuration. -->
작업 시도 횟수는 Laravel 큐 시스템의 핵심 개념이며, 여러 고급 기능의 기반이 됩니다. 처음에는 혼란스러울 수 있지만, 기본 설정을 변경하기 전에 이 개념이 어떻게 동작하는지 이해하는 것이 중요합니다.

<!-- When a job is dispatched, it is pushed onto the queue. A worker then picks it up and attempts to execute it. This is a job attempt. -->
작업이 디스패치되면 큐에 추가됩니다. 이후 워커가 해당 작업을 가져와 실행을 시도합니다. 이것이 작업 시도입니다.

<!-- However, an attempt does not necessarily mean the job's `handle` method was executed. Attempts can also be "consumed" in several ways: -->
하지만 시도 횟수가 증가했다고 해서 반드시 작업의 `handle` 메서드가 실행되었다는 뜻은 아닙니다. 시도 횟수는 다음과 같은 방식으로도 "소모"될 수 있습니다.

<div class="content-list" markdown="1">

<!-- - The job encounters an unhandled exception during execution. - The job is manually released back to the queue using `$this->release()`. - Middleware such as `WithoutOverlapping` or `RateLimited` fails to acquire a lock and releases the job. - The job timed out. - The job's `handle` method runs and completes without throwing an exception. -->
- 잡 실행 중 처리되지 않은 예외가 발생합니다.
- `$this->release()`를 사용해 잡을 수동으로 큐에 다시 반환합니다.
- `WithoutOverlapping` 또는 `RateLimited`와 같은 미들웨어가 락을 획득하지 못해 잡을 반환합니다.
- 잡 실행 시간이 초과됩니다.
- 잡의 `handle` 메서드가 실행되고 예외를 발생시키지 않은 채 완료됩니다.

</div>

<!-- You likely do not want to keep attempting a job indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a job may be attempted. -->
대부분의 경우 작업을 무한정 계속 시도하고 싶지는 않을 것입니다. 따라서 Laravel은 작업을 몇 번까지 또는 얼마 동안 시도할 수 있는지 지정하는 여러 방법을 제공합니다.

> [!NOTE]
> 기본적으로 Laravel은 잡을 한 번만 시도합니다. 잡에서 `WithoutOverlapping` 또는 `RateLimited`와 같은 미들웨어를 사용하거나 수동으로 잡을 다시 릴리스하는 경우에는 `tries` 옵션을 통해 허용되는 시도 횟수를 늘려야 할 가능성이 높습니다.

<!-- One approach to specifying the maximum number of times a job may be attempted is via the `--tries` switch on the Artisan command line. This will apply to all jobs processed by the worker unless the job being processed specifies the number of times it may be attempted: -->
작업을 시도할 수 있는 최대 횟수를 지정하는 한 가지 방법은 Artisan 명령줄에서 `--tries` 스위치를 사용하는 것입니다. 처리 중인 작업 자체에서 시도 횟수를 지정하지 않는 한, 이 값은 워커가 처리하는 모든 작업에 적용됩니다.

```shell
php artisan queue:work --tries=3
```

<!-- If a job exceeds its maximum number of attempts, it will be considered a "failed" job. For more information on handling failed jobs, consult the [failed job documentation](#dealing-with-failed-jobs). If `--tries=0` is provided to the `queue:work` command, the job will be retried indefinitely. -->
작업이 최대 시도 횟수를 초과하면 "실패한" 작업으로 간주됩니다. 실패한 작업을 처리하는 방법에 대한 자세한 내용은 [failed job documentation](#dealing-with-failed-jobs)를 참고하십시오. `queue:work` 명령어에 `--tries=0`을 제공하면 작업을 무기한 재시도합니다.

<!-- You may take a more granular approach by defining the maximum number of times a job may be attempted on the job class itself using the `Tries` attribute. If the maximum number of attempts is specified on the job, it will take precedence over the `--tries` value provided on the command line: -->
작업 클래스 자체에 `Tries` 속성을 정의하여 작업을 시도할 수 있는 최대 횟수를 더 세밀하게 지정할 수도 있습니다. 작업에 최대 시도 횟수가 지정되어 있으면 명령줄에서 제공한 `--tries` 값보다 우선합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Tries;

#[Tries(5)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

<!-- If you need dynamic control over a particular job's maximum attempts, you may define a `tries` method on the job: -->
특정 작업의 최대 시도 횟수를 동적으로 제어해야 한다면, 작업에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * Determine number of times the job may be attempted.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
<!-- #### Time Based Attempts -->
#### Time Based Attempts

<!-- As an alternative to defining how many times a job may be attempted before it fails, you may define a time at which the job should no longer be attempted. This allows a job to be attempted any number of times within a given time frame. To define the time at which a job should no longer be attempted, add a `retryUntil` method to your job class. This method should return a `DateTime` instance: -->
작업이 실패하기 전에 몇 번까지 시도할 수 있는지 정의하는 대신, 작업을 더 이상 시도하지 않아야 하는 시점을 정의할 수도 있습니다. 이렇게 하면 주어진 시간 범위 안에서 작업을 원하는 만큼 여러 번 시도할 수 있습니다. 작업을 더 이상 시도하지 않아야 하는 시점을 정의하려면 작업 클래스에 `retryUntil` 메서드를 추가합니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 10);
}
```

<!-- If both `retryUntil` and `tries` are defined, Laravel gives precedence to the `retryUntil` method. -->
`retryUntil`과 `tries`가 모두 정의되어 있으면 Laravel은 `retryUntil` 메서드를 우선합니다.

> [!NOTE]
> [queued event listeners](/docs/13.x/events#queued-event-listeners)와 [queued notifications](/docs/13.x/notifications#queueing-notifications)에 `Tries` 속성을 정의하거나 `retryUntil` 메서드를 정의할 수도 있습니다.

<a name="max-exceptions"></a>
<!-- #### Max Exceptions -->
#### Max Exceptions

<!-- Sometimes you may wish to specify that a job may be attempted many times, but should fail if the retries are triggered by a given number of unhandled exceptions (as opposed to being released by the `release` method directly). To accomplish this, you may use the `Tries` and `MaxExceptions` attributes on your job class: -->
때로는 작업을 여러 번 시도할 수 있도록 하되, 재시도가 특정 횟수의 처리되지 않은 예외 때문에 발생한 경우에는 실패하도록 지정하고 싶을 수 있습니다. 이는 `release` 메서드로 직접 다시 큐에 반환한 경우와 구분됩니다. 이를 위해 작업 클래스에 `Tries` 및 `MaxExceptions` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Support\Facades\Redis;

#[Tries(25)]
#[MaxExceptions(3)]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

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
```

<!-- In this example, the job is released for ten seconds if the application is unable to obtain a Redis lock and will continue to be retried up to 25 times. However, the job will fail if three unhandled exceptions are thrown by the job. -->
이 예제에서는 애플리케이션이 Redis 락을 획득하지 못하면 작업을 10초 뒤에 다시 시도하도록 큐에 반환하며, 최대 25번까지 계속 재시도합니다. 하지만 작업에서 처리되지 않은 예외가 세 번 발생하면 해당 작업은 실패합니다.

<a name="stopping-retries-by-exception"></a>
<!-- #### Stopping Retries by Exception -->
#### Stopping Retries by Exception

<!-- Sometimes an exception indicates that a queued job should fail immediately instead of being released for another attempt. You may configure exception types that should stop job retries using the `dontRetry` exception method in your application's `bootstrap/app.php` file: -->
때로는 예외가 발생했을 때 큐 작업을 다시 시도하도록 반환하지 않고 즉시 실패시켜야 하는 경우가 있습니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `dontRetry` 예외 메서드를 사용하여 작업 재시도를 중단해야 하는 예외 타입을 구성할 수 있습니다:

```php
use App\Exceptions\InvalidPodcastSourceException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetry([
        InvalidPodcastSourceException::class,
    ]);
})
```

<!-- If you need more control over when retries should stop, you may provide a closure to the `dontRetryWhen` method. When the closure returns `true`, the job will be marked as failed and will not be retried: -->
재시도를 언제 중단할지 더 세밀하게 제어해야 한다면, `dontRetryWhen` 메서드에 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 해당 작업은 실패로 표시되며 다시 시도되지 않습니다:

```php
use App\Exceptions\PodcastProcessingException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetryWhen(function (PodcastProcessingException $e) {
        return $e->reason() === 'Subscription expired';
    });
})
```

<a name="timeout"></a>
<!-- #### Timeout -->
#### Timeout

<!-- Often, you know roughly how long you expect your queued jobs to take. For this reason, Laravel allows you to specify a "timeout" value. By default, the timeout value is 60 seconds. If a job is processing for longer than the number of seconds specified by the timeout value, the worker processing the job will exit with an error. Typically, the worker will be restarted automatically by a [process manager configured on your server](#supervisor-configuration). -->
대개 큐 작업이 대략 얼마나 오래 걸릴지 알고 있습니다. 이런 이유로 Laravel은 "타임아웃" 값을 지정할 수 있도록 합니다. 기본 타임아웃 값은 60초입니다. 작업이 타임아웃 값으로 지정된 초 수보다 오래 처리되고 있으면, 해당 작업을 처리하던 워커가 오류와 함께 종료됩니다. 일반적으로 워커는 [process manager configured on your server](#supervisor-configuration)에 의해 자동으로 다시 시작됩니다.

<!-- The maximum number of seconds that jobs can run may be specified using the `--timeout` switch on the Artisan command line: -->
작업이 실행될 수 있는 최대 초 수는 Artisan 명령줄에서 `--timeout` 스위치를 사용하여 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

<!-- If the job exceeds its maximum attempts by continually timing out, it will be marked as failed. -->
작업이 계속 타임아웃되어 최대 시도 횟수를 초과하면 실패한 것으로 표시됩니다.

<!-- You may also define the maximum number of seconds a job should be allowed to run using the `Timeout` attribute on the job class. If the timeout is specified on the job, it will take precedence over any timeout specified on the command line: -->
작업 클래스에 `Timeout` 속성을 사용하여 작업이 실행될 수 있는 최대 초 수를 정의할 수도 있습니다. 작업에 타임아웃이 지정되어 있으면 명령줄에서 지정한 타임아웃보다 우선합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

<!-- Sometimes, IO blocking processes such as sockets or outgoing HTTP connections may not respect your specified timeout. Therefore, when using these features, you should always attempt to specify a timeout using their APIs as well. For example, when using [Guzzle](https://docs.guzzlephp.org), you should always specify a connection and request timeout value. -->
소켓이나 외부 HTTP 연결처럼 IO를 블로킹하는 프로세스는 지정한 타임아웃을 따르지 않을 수 있습니다. 따라서 이러한 기능을 사용할 때는 해당 API에서도 항상 타임아웃을 지정하려고 해야 합니다. 예를 들어 [Guzzle](https://docs.guzzlephp.org)을 사용할 때는 항상 연결 타임아웃과 요청 타임아웃 값을 지정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 기능이 설치되어 있어야 합니다. 또한 잡의 "timeout" 값은 항상 ["retry after"](#job-expiration) 값보다 작아야 합니다. 그렇지 않으면 잡이 실제 실행을 완료하거나 타임아웃되기 전에 다시 시도될 수 있습니다. `queue:work` 명령어를 `--once` 옵션과 함께 호출하면 `--timeout` 옵션이 적용되지 않습니다.

<a name="failing-on-timeout"></a>
<!-- #### Failing on Timeout -->
#### Failing on Timeout

<!-- If you would like to indicate that a job should be marked as [failed](#dealing-with-failed-jobs) on timeout, you may use the `FailOnTimeout` attribute on the job class: -->
타임아웃이 발생했을 때 작업을 [failed](#dealing-with-failed-jobs)으로 표시하고 싶다면, 작업 클래스에 `FailOnTimeout` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

> [!NOTE]
> 기본적으로 잡 시간이 초과되면 시도 횟수 1회를 소모하고 큐로 다시 반환됩니다(재시도가 허용된 경우). 하지만 시간 초과 시 잡이 실패하도록 설정하면 tries에 설정된 값과 관계없이 재시도되지 않습니다.

<a name="sqs-fifo-and-fair-queues"></a>
<!-- ### SQS FIFO and Fair Queues -->
### SQS FIFO and Fair Queues

<!-- Laravel supports [Amazon SQS FIFO (First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) and [fair](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html) queues. FIFO queues allow you to process jobs in the exact order they were sent while ensuring exactly-once processing through message deduplication. -->
Laravel은 [Amazon SQS FIFO (First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) 큐와 [fair](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html) 큐를 지원합니다. FIFO 큐를 사용하면 작업이 전송된 정확한 순서대로 처리할 수 있으며, 메시지 중복 제거를 통해 정확히 한 번만 처리되도록 보장할 수 있습니다.

<!-- FIFO queues require a message group ID to determine which jobs can be processed in parallel. Jobs with the same group ID are processed sequentially, while messages with different group IDs can be processed concurrently. -->
FIFO 큐는 어떤 작업을 병렬로 처리할 수 있는지 결정하기 위해 메시지 그룹 ID가 필요합니다. 같은 그룹 ID를 가진 작업은 순차적으로 처리되고, 서로 다른 그룹 ID를 가진 메시지는 동시에 처리될 수 있습니다.

<!-- Laravel provides a fluent `onGroup` method to specify the message group ID when dispatching jobs: -->
Laravel은 작업을 디스패치할 때 메시지 그룹 ID를 지정할 수 있도록 유창한 `onGroup` 메서드를 제공합니다.

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```

<!-- SQS FIFO queues support message deduplication to ensure exactly-once processing. Implement a `deduplicationId` method in your job class to provide a custom deduplication ID: -->
SQS FIFO 큐는 정확히 한 번만 처리되도록 보장하기 위해 메시지 중복 제거를 지원합니다. 사용자 정의 중복 제거 ID를 제공하려면 작업 클래스에 `deduplicationId` 메서드를 구현합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessSubscriptionRenewal implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's deduplication ID.
     */
    public function deduplicationId(): string
    {
        return "renewal-{$this->subscription->id}";
    }
}
```

<a name="fair-queues"></a>
<!-- #### Fair Queues -->
#### Fair Queues

<!-- If you are using an SQS standard queue, setting a message group enables fair queueing. In other words, once you assign groups, SQS will use them to maintain fair delivery across tenants / workloads. No additional Laravel configuration is required. -->
SQS 표준 큐를 사용하는 경우 메시지 그룹을 설정하면 공정 큐잉이 활성화됩니다. 즉, 그룹을 할당하면 SQS는 이를 사용하여 테넌트 / 워크로드 간에 공정한 전달을 유지합니다. 추가적인 Laravel 설정은 필요하지 않습니다.

<!-- Instead of calling `onGroup` at dispatch time, you may also define a `messageGroup` method directly on the job: -->
디스패치 시점에 `onGroup`을 호출하는 대신, 작업에 직접 `messageGroup` 메서드를 정의할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessOrder implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return "customer-{$this->order->customer_id}";
    }
}
```

<a name="fifo-listeners-mail-and-notifications"></a>
<!-- #### FIFO Listeners, Mail, and Notifications -->
#### FIFO Listeners, Mail, and Notifications

<!-- When utilizing FIFO queues, you will also need to define message groups on listeners, mail, and notifications. Alternatively, you can dispatch queued instances of these objects to a non-FIFO queue. -->
FIFO 큐를 사용할 때는 리스너, 메일, 알림에도 메시지 그룹을 정의해야 합니다. 또는 이러한 객체의 큐 인스턴스를 FIFO가 아닌 큐로 디스패치할 수도 있습니다.

<!-- To define the message group for a [queued event listener](/docs/13.x/events#queued-event-listeners), define a `messageGroup` method on the listener. You may also optionally define a `deduplicationId` method: -->
[queued event listener](/docs/13.x/events#queued-event-listeners)의 메시지 그룹을 정의하려면 리스너에 `messageGroup` 메서드를 정의합니다. 선택적으로 `deduplicationId` 메서드도 정의할 수 있습니다:

```php
<?php

namespace App\Listeners;

class SendShipmentNotification
{
    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return 'shipments';
    }

    /**
     * Get the job's deduplication ID.
     */
    public function deduplicationId(): string
    {
        return "shipment-notification-{$this->shipment->id}";
    }
}
```

<!-- When sending a [mail message](/docs/13.x/mail) that is going to be queued on a FIFO queue, you should invoke the `onGroup` method and optionally the `withDeduplicator` method when sending the notification: -->
FIFO 큐에 추가될 [mail message](/docs/13.x/mail)를 보낼 때는 알림을 전송하면서 `onGroup` 메서드와 선택적으로 `withDeduplicator` 메서드를 호출해야 합니다:

```php
use App\Mail\InvoicePaid;
use Illuminate\Support\Facades\Mail;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```

<!-- When sending a [notification](/docs/13.x/notifications) that is going to be queued on a FIFO queue, you should invoke the `onGroup` method and optionally the `withDeduplicator` method when sending the notification: -->
FIFO 큐에 추가될 [notification](/docs/13.x/notifications)을 보낼 때는 알림을 전송하면서 `onGroup` 메서드를 호출하고, 선택적으로 `withDeduplicator` 메서드도 호출해야 합니다:

```php
use App\Notifications\InvoicePaid;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```

<a name="queue-failover"></a>
<!-- ### Queue Failover -->
### Queue Failover

<!-- The `failover` queue driver provides automatic failover functionality when pushing jobs to the queue. If the primary queue connection of the `failover` configuration fails for any reason, Laravel will automatically attempt to push the job to the next configured connection in the list. This is particularly useful for ensuring high availability in production environments where queue reliability is critical. -->
`failover` 큐 드라이버는 작업을 큐에 넣을 때 자동 장애 조치 기능을 제공합니다. `failover` 설정의 기본 큐 연결이 어떤 이유로든 실패하면, Laravel은 설정된 목록의 다음 연결로 작업을 넣으려고 자동으로 시도합니다. 이는 큐 안정성이 중요한 프로덕션 환경에서 높은 가용성을 보장하는 데 특히 유용합니다.

<!-- To configure a failover queue connection, specify the `failover` driver and provide an array of connection names to attempt in order. By default, Laravel includes an example failover configuration in your application's `config/queue.php` configuration file: -->
장애 조치 큐 연결을 설정하려면 `failover` 드라이버를 지정하고, 순서대로 시도할 연결 이름 배열을 제공합니다. 기본적으로 Laravel은 애플리케이션의 `config/queue.php` 설정 파일에 예시 장애 조치 설정을 포함합니다.

```php
'failover' => [
    'driver' => 'failover',
    'connections' => [
        'redis',
        'database',
        'sync',
    ],
],
```

<!-- Once you have configured a connection that uses the `failover` driver, you will need to set the failover connection as your default queue connection in your application's `.env` file to make use of the failover functionality: -->
`failover` 드라이버를 사용하는 연결을 설정한 뒤에는, 장애 조치 기능을 사용하기 위해 애플리케이션의 `.env` 파일에서 장애 조치 연결을 기본 큐 연결로 설정해야 합니다.

```ini
QUEUE_CONNECTION=failover
```

<!-- Next, start at least one worker for each connection in your failover connection list: -->
다음으로, 장애 조치 연결 목록에 있는 각 연결마다 최소 하나의 워커를 시작합니다.

```bash
php artisan queue:work redis
php artisan queue:work database
```

> [!NOTE]
> `sync`, `background` 또는 `deferred` 큐 드라이버를 사용하는 연결에서는 해당 드라이버가 현재 PHP 프로세스 내에서 잡을 처리하므로 워커를 실행할 필요가 없습니다.

<!-- When a queue connection operation fails and failover is activated, Laravel will dispatch the `Illuminate\Queue\Events\QueueFailedOver` event, allowing you to report or log that a queue connection has failed. -->
큐 연결 작업이 실패하여 장애 조치가 활성화되면, Laravel은 `Illuminate\Queue\Events\QueueFailedOver` 이벤트를 디스패치합니다. 이를 통해 큐 연결 실패를 보고하거나 로그로 남길 수 있습니다.

> [!NOTE]
> Laravel Horizon을 사용하는 경우 Horizon은 Redis 큐만 관리한다는 점을 기억하세요. 장애 조치 목록에 `database`가 포함되어 있다면 Horizon과 함께 일반적인 `php artisan queue:work database` 프로세스도 실행해야 합니다.

<a name="error-handling"></a>
<!-- ### Error Handling -->
### Error Handling

<!-- If an exception is thrown while the job is being processed, the job will automatically be released back onto the queue so it may be attempted again. The job will continue to be released until it has been attempted the maximum number of times allowed by your application. The maximum number of attempts is defined by the `--tries` switch used on the `queue:work` Artisan command. Alternatively, the maximum number of attempts may be defined on the job class itself. More information on running the queue worker [can be found below](#running-the-queue-worker). -->
작업이 처리되는 동안 예외가 발생하면, 해당 작업은 다시 시도될 수 있도록 자동으로 큐에 다시 반환됩니다. 작업은 애플리케이션에서 허용한 최대 시도 횟수에 도달할 때까지 계속 다시 반환됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령어에서 사용하는 `--tries` 스위치로 정의됩니다. 또는 작업 클래스 자체에 최대 시도 횟수를 정의할 수도 있습니다. 큐 워커 실행에 대한 자세한 정보는 [can be found below](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
<!-- #### Manually Releasing a Job -->
#### Manually Releasing a Job

<!-- Sometimes you may wish to manually release a job back onto the queue so that it can be attempted again at a later time. You may accomplish this by calling the `release` method: -->
때로는 나중에 다시 시도할 수 있도록 작업을 수동으로 큐에 다시 반환하고 싶을 수 있습니다. 이는 `release` 메서드를 호출하여 수행할 수 있습니다.

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

<!-- By default, the `release` method will release the job back onto the queue for immediate processing. However, you may instruct the queue to not make the job available for processing until a given number of seconds has elapsed by passing an integer or date instance to the `release` method: -->
기본적으로 `release` 메서드는 작업을 즉시 처리할 수 있도록 큐에 다시 반환합니다. 하지만 `release` 메서드에 정수나 날짜 인스턴스를 전달하면, 지정한 초가 지난 뒤에야 작업을 처리할 수 있도록 큐에 지시할 수 있습니다.

```php
$this->release(10);

$this->release(now()->plus(seconds: 10));
```

<a name="manually-failing-a-job"></a>
<!-- #### Manually Failing a Job -->
#### Manually Failing a Job

<!-- Occasionally you may need to manually mark a job as "failed". To do so, you may call the `fail` method: -->
때로는 작업을 수동으로 "실패" 상태로 표시해야 할 수 있습니다. 이를 위해 `fail` 메서드를 호출할 수 있습니다.

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

<!-- If you would like to mark your job as failed because of an exception that you have caught, you may pass the exception to the `fail` method. Or, for convenience, you may pass a string error message which will be converted to an exception for you: -->
잡은 예외 때문에 작업을 실패로 표시하려는 경우, 해당 예외를 `fail` 메서드에 전달할 수 있습니다. 또는 편의를 위해 문자열 오류 메시지를 전달할 수 있으며, 이 메시지는 자동으로 예외로 변환됩니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 잡에 대한 자세한 내용은 [documentation on dealing with job failures](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
<!-- #### Failing Jobs on Specific Exceptions -->
#### Failing Jobs on Specific Exceptions

<!-- The `FailOnException` [job middleware](#job-middleware) allows you to short-circuit retries when specific exceptions are thrown. This allows retrying on transient exceptions such as external API errors, but failing the job permanently on persistent exceptions, such as a user's permissions being revoked: -->
`FailOnException` [job middleware](#job-middleware)를 사용하면 특정 예외가 발생했을 때 재시도를 중단할 수 있습니다. 이를 통해 외부 API 오류처럼 일시적인 예외에서는 재시도하되, 사용자의 권한이 취소된 경우처럼 지속적인 예외에서는 작업을 영구적으로 실패 처리할 수 있습니다.

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

#[Tries(3)]
class SyncChatHistory implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $this->user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$this->user->uuid}"
        );

        // ...
    }

    /**
     * Get the middleware the job should pass through.
     */
    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```

<a name="job-batching"></a>
<!-- ## Job Batching -->
## Job Batching

<!-- Laravel's job batching feature allows you to easily execute a group of jobs in parallel and then perform some action when the batch of jobs has completed executing. -->
Laravel의 작업 배치 처리 기능을 사용하면 작업 그룹을 병렬로 쉽게 실행하고, 해당 작업 배치의 실행이 완료된 뒤 어떤 동작을 수행할 수 있습니다.

<!-- Before getting started, you should create a database migration to build a table which will contain meta information about your job batches, such as their completion percentage. This migration may be generated using the `make:queue-batches-table` Artisan command: -->
시작하기 전에 작업 배치에 대한 메타 정보, 예를 들어 완료율 같은 정보를 담을 테이블을 만들기 위한 데이터베이스 마이그레이션을 생성해야 합니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령어를 사용해 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
<!-- ### Defining Batchable Jobs -->
### Defining Batchable Jobs

<!-- To define a batchable job, you should [create a queueable job](#creating-jobs) as normal; however, you should add the `Illuminate\Bus\Batchable` trait to the job class. This trait provides access to a `batch` method which may be used to retrieve the current batch that the job is executing within: -->
배치 가능한 작업을 정의하려면 일반적인 방식으로 [create a queueable job](#creating-jobs)합니다. 다만 작업 클래스에 `Illuminate\Bus\Batchable` 트레이트를 추가해야 합니다. 이 트레이트는 현재 작업이 실행되고 있는 배치를 가져오는 데 사용할 수 있는 `batch` 메서드에 접근할 수 있게 해줍니다.

```php
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
```

<a name="dispatching-batches"></a>
<!-- ### Dispatching Batches -->
### Dispatching Batches

<!-- To dispatch a batch of jobs, you should use the `batch` method of the `Bus` facade. Of course, batching is primarily useful when combined with completion callbacks. So, you may use the `then`, `catch`, and `finally` methods to define completion callbacks for the batch. Each of these callbacks will receive an `Illuminate\Bus\Batch` instance when they are invoked. -->
작업 배치를 디스패치하려면 `Bus` 파사드의 `batch` 메서드를 사용합니다. 물론 배치 처리는 완료 콜백과 함께 사용할 때 가장 유용합니다. 따라서 `then`, `catch`, `finally` 메서드를 사용해 배치의 완료 콜백을 정의할 수 있습니다. 이러한 각 콜백은 호출될 때 `Illuminate\Bus\Batch` 인스턴스를 전달받습니다.

<!-- When running multiple queue workers, the jobs in the batch will be processed in parallel. Therefore, the order in which the jobs complete may not be the same as the order in which they were added to the batch. Consult our documentation on [job chains and batches](#chains-and-batches) for information on how to run a series of jobs in sequence. -->
여러 큐 워커를 실행하는 경우, 배치 안의 작업은 병렬로 처리됩니다. 따라서 작업이 완료되는 순서는 배치에 추가된 순서와 같지 않을 수 있습니다. 일련의 작업을 순서대로 실행하는 방법은 [job chains and batches](#chains-and-batches) 문서를 참고하십시오.

<!-- In this example, we will imagine we are queueing a batch of jobs that each process a given number of rows from a CSV file: -->
이 예제에서는 CSV 파일에서 지정된 수의 행을 각각 처리하는 작업 배치를 큐에 넣는 상황을 가정합니다.

```php
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
    // Batch job failure detected...
})->finally(function (Batch $batch) {
    // The batch has finished executing...
})->dispatch();

return $batch->id;
```

<!-- The batch's ID, which may be accessed via the `$batch->id` property, may be used to [query the Laravel command bus](#inspecting-batches) for information about the batch after it has been dispatched. -->
`$batch->id` 속성으로 접근할 수 있는 배치의 ID는 배치가 디스패치된 뒤 해당 배치 정보를 [query the Laravel command bus](#inspecting-batches)하는 데 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화된 후 Laravel 큐에 의해 나중에 실행되므로 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다. 또한 배치 잡은 데이터베이스 트랜잭션으로 래핑되므로 암시적 커밋을 발생시키는 데이터베이스 문을 잡 내에서 실행해서는 안 됩니다.

<a name="naming-batches"></a>
<!-- #### Naming Batches -->
#### Naming Batches

<!-- Some tools such as [Laravel Horizon](/docs/13.x/horizon) and [Laravel Telescope](/docs/13.x/telescope) may provide more user-friendly debug information for batches if batches are named. To assign an arbitrary name to a batch, you may call the `name` method while defining the batch: -->
[Laravel Horizon](/docs/13.x/horizon) 및 [Laravel Telescope](/docs/13.x/telescope)와 같은 일부 도구는 배치에 이름을 지정하면 배치에 대해 더 이해하기 쉬운 디버그 정보를 제공할 수 있습니다. 배치를 임의의 이름으로 지정하려면 배치를 정의할 때 `name` 메서드를 호출하면 됩니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
<!-- #### Batch Connection and Queue -->
#### Batch Connection and Queue

<!-- If you would like to specify the connection and queue that should be used for the batched jobs, you may use the `onConnection` and `onQueue` methods. All batched jobs must execute within the same connection and queue: -->
배치 작업에 사용할 연결과 큐를 지정하려면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 연결과 큐 안에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
<!-- ### Chains and Batches -->
### Chains and Batches

<!-- You may define a set of [chained jobs](#job-chaining) within a batch by placing the chained jobs within an array. For example, we may execute two job chains in parallel and execute a callback when both job chains have finished processing: -->
배치 안에 [chained jobs](#job-chaining) 집합을 정의하려면, 체인 작업을 배열 안에 넣으면 됩니다. 예를 들어 두 개의 작업 체인을 병렬로 실행하고, 두 작업 체인이 모두 처리를 마쳤을 때 콜백을 실행할 수 있습니다.

```php
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
    // All jobs completed successfully...
})->dispatch();
```

<!-- Conversely, you may run batches of jobs within a [chain](#job-chaining) by defining batches within the chain. For example, you could first run a batch of jobs to release multiple podcasts then a batch of jobs to send the release notifications: -->
반대로, [chain](#job-chaining) 안에서 배치를 정의하여 작업 배치를 실행할 수도 있습니다. 예를 들어 먼저 여러 팟캐스트를 공개하는 작업 배치를 실행한 뒤, 공개 알림을 보내는 작업 배치를 실행할 수 있습니다.

```php
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
```

<a name="adding-jobs-to-batches"></a>
<!-- ### Adding Jobs to Batches -->
### Adding Jobs to Batches

<!-- Sometimes it may be useful to add additional jobs to a batch from within a batched job. This pattern can be useful when you need to batch thousands of jobs which may take too long to dispatch during a web request. So, instead, you may wish to dispatch an initial batch of "loader" jobs that hydrate the batch with even more jobs: -->
때로는 배치 작업 안에서 해당 배치에 추가 작업을 더하는 것이 유용할 수 있습니다. 이 패턴은 수천 개의 작업을 배치로 처리해야 하는데, 웹 요청 중에 모두 디스패치하기에는 시간이 너무 오래 걸릴 수 있을 때 유용합니다. 이런 경우 먼저 "loader" 작업으로 이루어진 초기 배치를 디스패치하고, 이 작업들이 배치에 더 많은 작업을 채우도록 할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import Contacts')->dispatch();
```

<!-- In this example, we will use the `LoadImportBatch` job to hydrate the batch with additional jobs. To accomplish this, we may use the `add` method on the batch instance that may be accessed via the job's `batch` method: -->
이 예제에서는 `LoadImportBatch` 작업을 사용해 배치에 추가 작업을 채웁니다. 이를 수행하려면 작업의 `batch` 메서드를 통해 접근할 수 있는 배치 인스턴스에서 `add` 메서드를 사용할 수 있습니다.

```php
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
```

> [!WARNING]
> 동일한 배치에 속한 잡 내부에서만 배치에 잡을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
<!-- ### Inspecting Batches -->
### Inspecting Batches

<!-- The `Illuminate\Bus\Batch` instance that is provided to batch completion callbacks has a variety of properties and methods to assist you in interacting with and inspecting a given batch of jobs: -->
배치 완료 콜백에 전달되는 `Illuminate\Bus\Batch` 인스턴스는 주어진 작업 배치와 상호작용하고 이를 살펴보는 데 도움이 되는 다양한 속성과 메서드를 제공합니다.

```php
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
모든 `Illuminate\Bus\Batch` 인스턴스는 JSON으로 직렬화할 수 있습니다. 즉, 애플리케이션의 라우트에서 직접 반환하여 완료 진행률을 포함한 배치 정보를 담은 JSON 페이로드를 가져올 수 있습니다. 이를 사용하면 애플리케이션 UI에서 배치의 완료 진행률 정보를 쉽게 표시할 수 있습니다.

<!-- To retrieve a batch by its ID, you may use the `Bus` facade's `findBatch` method: -->
ID로 배치를 가져오려면 `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
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
때로는 주어진 배치의 실행을 취소해야 할 수 있습니다. 이는 `Illuminate\Bus\Batch` 인스턴스에서 `cancel` 메서드를 호출하여 처리할 수 있습니다.

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    if ($this->user->exceedsImportLimit()) {
        $this->batch()->cancel();

        return;
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```

<!-- As you may have noticed in the previous examples, batched jobs should typically determine if their corresponding batch has been cancelled before continuing execution. However, for convenience, you may assign the `SkipIfBatchCancelled` [middleware](#job-middleware) to the job instead. As its name indicates, this middleware will instruct Laravel to not process the job if its corresponding batch has been cancelled: -->
앞선 예제에서 보았듯이, 배치 작업은 일반적으로 실행을 계속하기 전에 해당 배치가 취소되었는지 확인해야 합니다. 다만 편의를 위해 작업에 `SkipIfBatchCancelled` [middleware](#job-middleware)를 지정할 수도 있습니다. 이름에서 알 수 있듯이, 이 미들웨어는 해당 배치가 취소된 경우 Laravel이 작업을 처리하지 않도록 지시합니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
<!-- ### Batch Failures -->
### Batch Failures

<!-- When a batched job fails, the `catch` callback (if assigned) will be invoked. This callback is only invoked for the first job that fails within the batch. -->
배치 작업이 실패하면 `catch` 콜백이 지정되어 있는 경우 호출됩니다. 이 콜백은 배치 안에서 처음 실패한 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>
<!-- #### Allowing Failures -->
#### Allowing Failures

<!-- When a job within a batch fails, Laravel will automatically mark the batch as "cancelled". If you wish, you may disable this behavior so that a job failure does not automatically mark the batch as cancelled. This may be accomplished by calling the `allowFailures` method while dispatching the batch: -->
배치 안의 작업이 실패하면 Laravel은 자동으로 배치를 "cancelled" 상태로 표시합니다. 원한다면 이 동작을 비활성화하여 작업 실패가 배치를 자동으로 취소 상태로 만들지 않도록 할 수 있습니다. 배치를 디스패치할 때 `allowFailures` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->allowFailures()->dispatch();
```

<!-- You may optionally provide a closure to the `allowFailures` method, which will be executed on each job failure: -->
선택적으로 `allowFailures` 메서드에 클로저를 전달할 수 있으며, 이 클로저는 각 작업 실패 시 실행됩니다.

```php
$batch = Bus::batch([
    // ...
])->allowFailures(function (Batch $batch, $exception) {
    // Handle individual job failures...
})->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
<!-- #### Retrying Failed Batch Jobs -->
#### Retrying Failed Batch Jobs

<!-- For convenience, Laravel provides a `queue:retry-batch` Artisan command that allows you to easily retry all of the failed jobs for a given batch. This command accepts the UUID of the batch whose failed jobs should be retried: -->
편의를 위해 Laravel은 주어진 배치에서 실패한 모든 작업을 쉽게 다시 시도할 수 있는 `queue:retry-batch` Artisan 명령어를 제공합니다. 이 명령어는 실패한 작업을 다시 시도할 배치의 UUID를 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
<!-- ### Pruning Batches -->
### Pruning Batches

<!-- Without pruning, the `job_batches` table can accumulate records very quickly. To mitigate this, you should [schedule](/docs/13.x/scheduling) the `queue:prune-batches` Artisan command to run daily: -->
정리하지 않으면 `job_batches` 테이블에 레코드가 매우 빠르게 쌓일 수 있습니다. 이를 완화하려면 `queue:prune-batches` Artisan 명령어가 매일 실행되도록 [schedule](/docs/13.x/scheduling)해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

<!-- By default, all finished batches that are more than 24 hours old will be pruned. You may use the `hours` option when calling the command to determine how long to retain batch data. For example, the following command will delete all batches that finished over 48 hours ago: -->
기본적으로 완료된 지 24시간이 지난 모든 배치는 정리됩니다. 명령어를 호출할 때 `hours` 옵션을 사용하여 배치 데이터를 얼마나 오래 보관할지 결정할 수 있습니다. 예를 들어 다음 명령어는 48시간보다 더 전에 완료된 모든 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

<!-- Sometimes, your `job_batches` table may accumulate batch records for batches that never completed successfully, such as batches where a job failed and that job was never retried successfully. You may instruct the `queue:prune-batches` command to prune these unfinished batch records using the `unfinished` option: -->
때로는 작업이 실패했고 해당 작업이 다시 성공적으로 시도되지 않은 배치처럼, 성공적으로 완료되지 않은 배치의 레코드가 `job_batches` 테이블에 쌓일 수 있습니다. `unfinished` 옵션을 사용하면 `queue:prune-batches` 명령어가 이러한 미완료 배치 레코드를 정리하도록 지시할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

<!-- Likewise, your `job_batches` table may also accumulate batch records for cancelled batches. You may instruct the `queue:prune-batches` command to prune these cancelled batch records using the `cancelled` option: -->
마찬가지로 `job_batches` 테이블에는 취소된 배치의 레코드도 쌓일 수 있습니다. `cancelled` 옵션을 사용하면 `queue:prune-batches` 명령어가 이러한 취소된 배치 레코드를 정리하도록 지시할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
<!-- ### Storing Batches in DynamoDB -->
### Storing Batches in DynamoDB

<!-- Laravel also provides support for storing batch meta information in [DynamoDB](https://aws.amazon.com/dynamodb) instead of a relational database. However, you will need to manually create a DynamoDB table to store all of the batch records. -->
Laravel은 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 메타 정보를 저장하는 기능도 지원합니다. 다만 모든 배치 레코드를 저장할 DynamoDB 테이블은 직접 생성해야 합니다.

<!-- Typically, this table should be named `job_batches`, but you should name the table based on the value of the `queue.batching.table` configuration value within your application's `queue` configuration file. -->
일반적으로 이 테이블의 이름은 `job_batches`여야 하지만, 애플리케이션의 `queue` 설정 파일 안에 있는 `queue.batching.table` 설정 값에 따라 테이블 이름을 지정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
<!-- #### DynamoDB Batch Table Configuration -->
#### DynamoDB Batch Table Configuration

<!-- The `job_batches` table should have a string primary partition key named `application` and a string primary sort key named `id`. The `application` portion of the key will contain your application's name as defined by the `name` configuration value within your application's `app` configuration file. Since the application name is part of the DynamoDB table's key, you can use the same table to store job batches for multiple Laravel applications. -->
`job_batches` 테이블에는 `application`이라는 문자열 기본 파티션 키와 `id`라는 문자열 기본 정렬 키가 있어야 합니다. 키의 `application` 부분에는 애플리케이션의 `app` 설정 파일 안에 있는 `name` 설정 값으로 정의된 애플리케이션 이름이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블 키의 일부이므로, 동일한 테이블을 사용하여 여러 Laravel 애플리케이션의 작업 배치를 저장할 수 있습니다.

<!-- In addition, you may define `ttl` attribute for your table if you would like to take advantage of [automatic batch pruning](#pruning-batches-in-dynamodb). -->
또한 [automatic batch pruning](#pruning-batches-in-dynamodb)를 활용하려면 테이블에 `ttl` 속성을 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
<!-- #### DynamoDB Configuration -->
#### DynamoDB Configuration

<!-- Next, install the AWS SDK so that your Laravel application can communicate with Amazon DynamoDB: -->
다음으로 Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

<!-- Then, set the `queue.batching.driver` configuration option's value to `dynamodb`. In addition, you should define `key`, `secret`, and `region` configuration options within the `batching` configuration array. These options will be used to authenticate with AWS. When using the `dynamodb` driver, the `queue.batching.database` configuration option is unnecessary: -->
그런 다음 `queue.batching.driver` 설정 옵션 값을 `dynamodb`로 설정합니다. 또한 `batching` 설정 배열 안에 `key`, `secret`, `region` 설정 옵션을 정의해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.batching.database` 설정 옵션이 필요하지 않습니다.

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
<!-- #### Pruning Batches in DynamoDB -->
#### Pruning Batches in DynamoDB

<!-- When utilizing [DynamoDB](https://aws.amazon.com/dynamodb) to store job batch information, the typical pruning commands used to prune batches stored in a relational database will not work. Instead, you may utilize [DynamoDB's native TTL functionality](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) to automatically remove records for old batches. -->
작업 배치 정보를 저장하는 데 [DynamoDB](https://aws.amazon.com/dynamodb)를 사용하는 경우, 관계형 데이터베이스에 저장된 배치를 정리할 때 사용하는 일반적인 정리 명령어는 동작하지 않습니다. 대신 [DynamoDB's native TTL functionality](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 사용하여 오래된 배치의 레코드를 자동으로 제거할 수 있습니다.

<!-- If you defined your DynamoDB table with a `ttl` attribute, you may define configuration parameters to instruct Laravel how to prune batch records. The `queue.batching.ttl_attribute` configuration value defines the name of the attribute holding the TTL, while the `queue.batching.ttl` configuration value defines the number of seconds after which a batch record can be removed from the DynamoDB table, relative to the last time the record was updated: -->
DynamoDB 테이블에 `ttl` 속성을 정의했다면, Laravel이 배치 레코드를 어떻게 정리해야 하는지 지시하는 설정 매개변수를 정의할 수 있습니다. `queue.batching.ttl_attribute` 설정 값은 TTL을 담고 있는 속성의 이름을 정의하며, `queue.batching.ttl` 설정 값은 레코드가 마지막으로 업데이트된 시간을 기준으로 몇 초 후에 배치 레코드를 DynamoDB 테이블에서 제거할 수 있는지 정의합니다.

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
<!-- ## Queueing Closures -->
## Queueing Closures

<!-- Instead of dispatching a job class to the queue, you may also dispatch a closure. This is great for quick, simple tasks that need to be executed outside of the current request cycle. When dispatching closures to the queue, the closure's code content is cryptographically signed so that it cannot be modified in transit: -->
작업 클래스를 큐에 디스패치하는 대신 클로저를 디스패치할 수도 있습니다. 이는 현재 요청 사이클 밖에서 실행되어야 하는 빠르고 단순한 작업에 적합합니다. 클로저를 큐에 디스패치할 때 클로저의 코드 내용은 암호학적으로 서명되므로 전송 중에 수정될 수 없습니다.

```php
use App\Models\Podcast;

$podcast = Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

<!-- To assign a name to the queued closure which may be used by queue reporting dashboards, as well as be displayed by the `queue:work` command, you may use the `name` method: -->
큐 보고 대시보드에서 사용할 수 있고 `queue:work` 명령어에도 표시되는 큐 클로저 이름을 지정하려면 `name` 메서드를 사용할 수 있습니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

<!-- Using the `catch` method, you may provide a closure that should be executed if the queued closure fails to complete successfully after exhausting all of your queue's [configured retry attempts](#max-job-attempts-and-timeout): -->
`catch` 메서드를 사용하면 큐에 등록된 클로저가 큐의 [configured retry attempts](#max-job-attempts-and-timeout)를 모두 소진한 뒤에도 성공적으로 완료되지 못했을 때 실행할 클로저를 제공할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

> [!WARNING]
> `catch` 콜백은 직렬화된 후 Laravel 큐에 의해 나중에 실행되므로 `catch` 콜백 안에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="running-the-queue-worker"></a>
<!-- ## Running the Queue Worker -->
## Running the Queue Worker

<a name="the-queue-work-command"></a>
<!-- ### The `queue:work` Command -->
### The `queue:work` Command

<!-- Laravel includes an Artisan command that will start a queue worker and process new jobs as they are pushed onto the queue. You may run the worker using the `queue:work` Artisan command. Note that once the `queue:work` command has started, it will continue to run until it is manually stopped or you close your terminal: -->
Laravel에는 큐 워커를 시작하고 큐에 새 작업이 추가될 때 이를 처리하는 Artisan 명령어가 포함되어 있습니다. `queue:work` Artisan 명령어를 사용하여 워커를 실행할 수 있습니다. `queue:work` 명령어가 시작되면 직접 중지하거나 터미널을 닫을 때까지 계속 실행된다는 점에 유의하십시오.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 영구적으로 실행하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용해 큐 워커가 중지되지 않도록 해야 합니다.

<!-- You may include the `-v` flag when invoking the `queue:work` command if you would like the processed job IDs, connection names, and queue names to be included in the command's output: -->
처리된 작업 ID, 연결 이름, 큐 이름을 명령어 출력에 포함하려면 `queue:work` 명령어를 실행할 때 `-v` 플래그를 포함할 수 있습니다.

```shell
php artisan queue:work -v
```

<!-- Remember, queue workers are long-lived processes and store the booted application state in memory. As a result, they will not notice changes in your code base after they have been started. So, during your deployment process, be sure to [restart your queue workers](#queue-workers-and-deployment). In addition, remember that any static state created or modified by your application will not be automatically reset between jobs. -->
큐 워커는 오래 실행되는 프로세스이며 부팅된 애플리케이션 상태를 메모리에 저장한다는 점을 기억하십시오. 따라서 시작된 이후에는 코드베이스의 변경 사항을 감지하지 못합니다. 그러므로 배포 과정에서 반드시 [restart your queue workers](#queue-workers-and-deployment)해야 합니다. 또한 애플리케이션에서 생성하거나 수정한 모든 정적 상태는 작업 사이에 자동으로 초기화되지 않는다는 점도 기억해야 합니다.

<!-- Alternatively, you may run the `queue:listen` command. When using the `queue:listen` command, you don't have to manually restart the worker when you want to reload your updated code or reset the application state; however, this command is significantly less efficient than the `queue:work` command: -->
또는 `queue:listen` 명령어를 실행할 수 있습니다. `queue:listen` 명령어를 사용하면 업데이트된 코드를 다시 로드하거나 애플리케이션 상태를 초기화하고 싶을 때 워커를 수동으로 재시작할 필요가 없습니다. 하지만 이 명령어는 `queue:work` 명령어보다 훨씬 비효율적입니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
<!-- #### Running Multiple Queue Workers -->
#### Running Multiple Queue Workers

<!-- To assign multiple workers to a queue and process jobs concurrently, you should simply start multiple `queue:work` processes. This can either be done locally via multiple tabs in your terminal or in production using your process manager's configuration settings. [When using Supervisor](#supervisor-configuration), you may use the `numprocs` configuration value. -->
하나의 큐에 여러 워커를 할당하고 작업을 동시에 처리하려면 여러 `queue:work` 프로세스를 시작하면 됩니다. 로컬에서는 터미널의 여러 탭을 통해 실행할 수 있고, 프로덕션에서는 프로세스 매니저의 설정을 통해 실행할 수 있습니다. [When using Supervisor](#supervisor-configuration)는 `numprocs` 설정 값을 사용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
<!-- #### Specifying the Connection and Queue -->
#### Specifying the Connection and Queue

<!-- You may also specify which queue connection the worker should utilize. The connection name passed to the `work` command should correspond to one of the connections defined in your `config/queue.php` configuration file: -->
워커가 사용할 큐 연결도 지정할 수 있습니다. `work` 명령어에 전달하는 연결 이름은 `config/queue.php` 설정 파일에 정의된 연결 중 하나와 일치해야 합니다.

```shell
php artisan queue:work redis
```

<!-- By default, the `queue:work` command only processes jobs for the default queue on a given connection. However, you may customize your queue worker even further by only processing particular queues for a given connection. For example, if all of your emails are processed in an `emails` queue on your `redis` queue connection, you may issue the following command to start a worker that only processes that queue: -->
기본적으로 `queue:work` 명령어는 주어진 연결에서 기본 큐의 작업만 처리합니다. 하지만 주어진 연결의 특정 큐만 처리하도록 큐 워커를 더 세밀하게 사용자 정의할 수 있습니다. 예를 들어 모든 이메일이 `redis` 큐 연결의 `emails` 큐에서 처리된다면, 다음 명령어를 실행하여 해당 큐만 처리하는 워커를 시작할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
<!-- #### Processing a Specified Number of Jobs -->
#### Processing a Specified Number of Jobs

<!-- The `--once` option may be used to instruct the worker to only process a single job from the queue: -->
`--once` 옵션을 사용하면 워커가 큐에서 단일 작업만 처리하도록 지시할 수 있습니다.

```shell
php artisan queue:work --once
```

<!-- The `--max-jobs` option may be used to instruct the worker to process the given number of jobs and then exit. This option may be useful when combined with [Supervisor](#supervisor-configuration) so that your workers are automatically restarted after processing a given number of jobs, releasing any memory they may have accumulated: -->
`--max-jobs` 옵션을 사용하면 워커가 지정한 수의 작업을 처리한 뒤 종료하도록 지시할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용할 때 유용할 수 있습니다. 지정된 수의 작업을 처리한 뒤 워커가 자동으로 재시작되므로, 워커가 누적했을 수 있는 메모리를 해제할 수 있습니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
<!-- #### Processing All Queued Jobs and Then Exiting -->
#### Processing All Queued Jobs and Then Exiting

<!-- The `--stop-when-empty` option may be used to instruct the worker to process all jobs and then exit gracefully. This option can be useful when processing Laravel queues within a Docker container if you wish to shutdown the container after the queue is empty: -->
`--stop-when-empty` 옵션을 사용하면 워커가 모든 작업을 처리한 뒤 정상적으로 종료하도록 지시할 수 있습니다. Docker 컨테이너 안에서 Laravel 큐를 처리하고 있고 큐가 비면 컨테이너를 종료하고 싶을 때 유용할 수 있습니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
<!-- #### Processing Jobs for a Given Number of Seconds -->
#### Processing Jobs for a Given Number of Seconds

<!-- The `--max-time` option may be used to instruct the worker to process jobs for the given number of seconds and then exit. This option may be useful when combined with [Supervisor](#supervisor-configuration) so that your workers are automatically restarted after processing jobs for a given amount of time, releasing any memory they may have accumulated: -->
`--max-time` 옵션을 사용하면 워커가 지정한 초 동안 작업을 처리한 뒤 종료하도록 지시할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용할 때 유용할 수 있습니다. 지정된 시간 동안 작업을 처리한 뒤 워커가 자동으로 재시작되므로, 워커가 누적했을 수 있는 메모리를 해제할 수 있습니다.

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
<!-- #### Worker Sleep Duration -->
#### Worker Sleep Duration

<!-- When jobs are available on the queue, the worker will keep processing jobs with no delay in between jobs. However, the `sleep` option determines how many seconds the worker will "sleep" if there are no jobs available. Of course, while sleeping, the worker will not process any new jobs: -->
큐에 처리할 작업이 있으면 워커는 작업 사이에 지연 없이 계속 작업을 처리합니다. 하지만 처리할 작업이 없을 때 워커가 몇 초 동안 "sleep"할지는 `sleep` 옵션이 결정합니다. 물론 대기 중인 동안 워커는 새 작업을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode and Queues -->
#### Maintenance Mode and Queues

<!-- While your application is in [maintenance mode](/docs/13.x/configuration#maintenance-mode), no queued jobs will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
애플리케이션이 [maintenance mode](/docs/13.x/configuration#maintenance-mode)인 동안에는 큐에 대기 중인 잡을 처리하지 않습니다. 애플리케이션이 유지 관리 모드에서 벗어나면 잡은 평소와 같이 계속 처리됩니다.

<!-- To force your queue workers to process jobs even if maintenance mode is enabled, you may use `--force` option: -->
유지 관리 모드가 활성화되어 있어도 큐 워커가 작업을 처리하도록 강제하려면 `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
<!-- #### Resource Considerations -->
#### Resource Considerations

<!-- Daemon queue workers do not "reboot" the framework before processing each job. Therefore, you should release any heavy resources after each job completes. For example, if you are doing [image manipulation](/docs/13.x/images) with the [GD library](https://www.php.net/manual/en/book.image.php), you should free the memory with `imagedestroy` when you are done processing the image. -->
데몬 큐 워커는 각 잡을 처리하기 전에 프레임워크를 "재부팅"하지 않습니다. 따라서 각 잡이 완료된 후에는 무거운 리소스를 해제해야 합니다. 예를 들어 [image manipulation](/docs/13.x/images)을 위해 [GD library](https://www.php.net/manual/en/book.image.php)를 사용한다면, 이미지 처리를 마친 후 `imagedestroy`로 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
<!-- ### Queue Priorities -->
### Queue Priorities

<!-- Sometimes you may wish to prioritize how your queues are processed. For example, in your `config/queue.php` configuration file, you may set the default `queue` for your `redis` connection to `low`. However, occasionally you may wish to push a job to a `high` priority queue like so: -->
때로는 큐가 처리되는 방식에 우선순위를 지정하고 싶을 수 있습니다. 예를 들어 `config/queue.php` 설정 파일에서 `redis` 연결의 기본 `queue`를 `low`로 설정할 수 있습니다. 하지만 때때로 다음과 같이 작업을 `high` 우선순위 큐로 푸시하고 싶을 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

<!-- To start a worker that verifies that all of the `high` queue jobs are processed before continuing to any jobs on the `low` queue, pass a comma-delimited list of queue names to the `work` command: -->
`low` 큐의 작업을 계속 처리하기 전에 모든 `high` 큐 작업이 처리되었는지 확인하는 워커를 시작하려면, 큐 이름을 쉼표로 구분한 목록으로 `work` 명령어에 전달합니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
<!-- ### Queue Workers and Deployment -->
### Queue Workers and Deployment

<!-- Since queue workers are long-lived processes, they will not notice changes to your code without being restarted. So, the simplest way to deploy an application using queue workers is to restart the workers during your deployment process. You may gracefully restart all of the workers by issuing the `queue:restart` command: -->
큐 워커는 오래 실행되는 프로세스이므로 재시작하지 않으면 코드 변경 사항을 감지하지 못합니다. 따라서 큐 워커를 사용하는 애플리케이션을 배포하는 가장 간단한 방법은 배포 과정에서 워커를 재시작하는 것입니다. `queue:restart` 명령어를 실행하여 모든 워커를 정상적으로 재시작할 수 있습니다.

```shell
php artisan queue:restart
```

<!-- This command will instruct all queue workers to gracefully exit after they finish processing their current job so that no existing jobs are lost. Since the queue workers will exit when the `queue:restart` command is executed, you should be running a process manager such as [Supervisor](#supervisor-configuration) to automatically restart the queue workers. -->
이 명령어는 기존 작업이 손실되지 않도록 모든 큐 워커에게 현재 작업 처리를 마친 뒤 정상적으로 종료하라고 지시합니다. `queue:restart` 명령어가 실행되면 큐 워커가 종료되므로, 큐 워커를 자동으로 재시작하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 매니저를 실행하고 있어야 합니다.

> [!NOTE]
> 큐는 재시작 신호를 저장하는 데 [cache](/docs/13.x/cache)를 사용하므로, 이 기능을 사용하기 전에 애플리케이션에 캐시 드라이버가 올바르게 구성되어 있는지 확인해야 합니다.

<a name="reacting-to-worker-signals"></a>
<!-- ### Reacting to Worker Signals -->
### Reacting to Worker Signals

<!-- When a queue worker receives a termination signal such as `SIGQUIT`, `SIGTERM`, or `SIGINT` while processing a job, the worker will finish its current job before exiting. However, your job may need to react to the signal before the process is stopped by your server or container orchestrator. For example, a long-running import job may need to stop pulling new records and save its current progress. -->
큐 워커가 잡을 처리하는 동안 `SIGQUIT`, `SIGTERM`, `SIGINT` 같은 종료 시그널을 받으면, 워커는 현재 잡을 끝낸 후 종료됩니다. 하지만 서버나 컨테이너 오케스트레이터가 프로세스를 중지하기 전에 잡이 시그널에 반응해야 할 수도 있습니다. 예를 들어 오래 실행되는 가져오기 잡은 새 레코드 가져오기를 중단하고 현재 진행 상황을 저장해야 할 수 있습니다.

<!-- To react to worker signals from within a job, implement the `Illuminate\Contracts\Queue\Interruptible` interface and define an `interrupted` method on your job. The signal number received by the worker will be passed to the `interrupted` method: -->
잡 내부에서 워커 시그널에 반응하려면 `Illuminate\Contracts\Queue\Interruptible` 인터페이스를 구현하고 잡에 `interrupted` 메서드를 정의합니다. 워커가 받은 시그널 번호가 `interrupted` 메서드에 전달됩니다:

```php
<?php

namespace App\Jobs;

use App\Models\Import;
use Illuminate\Contracts\Queue\Interruptible;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportProducts implements ShouldQueue, Interruptible
{
    use Queueable;

    protected bool $shouldStop = false;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Import $import,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        foreach ($this->import->pendingRows() as $row) {
            if ($this->shouldStop) {
                break;
            }

            // Import the product row...
        }

        $this->import->saveProgress();
    }

    /**
     * Handle a signal received by the queue worker.
     */
    public function interrupted(int $signal): void
    {
        $this->shouldStop = true;
    }
}
```

<!-- The `interrupted` method is only invoked when the worker receives a process signal while the job is currently running. It is not a replacement for [timeouts](#worker-timeouts) or the job's [`failed` method](#cleaning-up-after-failed-jobs). -->
`interrupted` 메서드는 잡이 현재 실행 중일 때 워커가 프로세스 시그널을 받은 경우에만 호출됩니다. 이는 [timeouts](#worker-timeouts)이나 잡의 [`failed` method](#cleaning-up-after-failed-jobs)를 대체하지 않습니다.

<a name="job-expirations-and-timeouts"></a>
<!-- ### Job Expirations and Timeouts -->
### Job Expirations and Timeouts

<a name="job-expiration"></a>
<!-- #### Job Expiration -->
#### Job Expiration

<!-- In your `config/queue.php` configuration file, each queue connection defines a `retry_after` option. This option specifies how many seconds the queue connection should wait before retrying a job that is being processed. For example, if the value of `retry_after` is set to `90`, the job will be released back onto the queue if it has been processing for 90 seconds without being released or deleted. Typically, you should set the `retry_after` value to the maximum number of seconds your jobs should reasonably take to complete processing. -->
`config/queue.php` 설정 파일에서 각 큐 연결은 `retry_after` 옵션을 정의합니다. 이 옵션은 처리 중인 작업을 다시 시도하기 전에 큐 연결이 몇 초 동안 기다려야 하는지를 지정합니다. 예를 들어 `retry_after` 값이 `90`으로 설정되어 있으면, 작업이 큐에 반환되거나 삭제되지 않은 상태로 90초 동안 처리되고 있을 때 해당 작업은 다시 큐로 반환됩니다. 일반적으로 `retry_after` 값은 작업이 합리적으로 완료되는 데 걸릴 수 있는 최대 시간(초)으로 설정해야 합니다.

> [!WARNING]
> `retry_after` 값을 포함하지 않는 유일한 큐 연결은 Amazon SQS입니다. SQS는 AWS 콘솔에서 관리하는 [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)을 기준으로 잡을 재시도합니다.

<a name="worker-timeouts"></a>
<!-- #### Worker Timeouts -->
#### Worker Timeouts

<!-- The `queue:work` Artisan command exposes a `--timeout` option. By default, the `--timeout` value is 60 seconds. If a job is processing for longer than the number of seconds specified by the timeout value, the worker processing the job will exit with an error. Typically, the worker will be restarted automatically by a [process manager configured on your server](#supervisor-configuration): -->
`queue:work` Artisan 명령어는 `--timeout` 옵션을 제공합니다. 기본적으로 `--timeout` 값은 60초입니다. 작업이 타임아웃 값으로 지정한 시간보다 오래 처리되면, 해당 작업을 처리하던 워커는 오류와 함께 종료됩니다. 일반적으로 워커는 [process manager configured on your server](#supervisor-configuration)에 의해 자동으로 다시 시작됩니다.

```shell
php artisan queue:work --timeout=60
```

<!-- The `retry_after` configuration option and the `--timeout` CLI option are different, but work together to ensure that jobs are not lost and that jobs are only successfully processed once. -->
`retry_after` 설정 옵션과 `--timeout` CLI 옵션은 서로 다르지만, 함께 동작하여 작업이 유실되지 않도록 하고 작업이 한 번만 성공적으로 처리되도록 보장합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 설정값보다 몇 초 이상 짧아야 합니다. 이렇게 하면 멈춘 잡을 처리 중인 워커가 잡을 다시 시도하기 전에 항상 종료됩니다. `--timeout` 옵션이 `retry_after` 설정값보다 길면 잡이 두 번 처리될 수 있습니다.

<a name="pausing-and-resuming-queue-workers"></a>
<!-- ### Pausing and Resuming Queue Workers -->
### Pausing and Resuming Queue Workers

<!-- Sometimes you may need to temporarily prevent a queue worker from processing new jobs without stopping the worker entirely. For example, you may want to pause job processing during system maintenance. Laravel provides the `queue:pause` and `queue:continue` Artisan commands to pause and resume queue workers. -->
때로는 워커를 완전히 중지하지 않고, 큐 워커가 새 작업을 처리하지 못하도록 일시적으로 막아야 할 수 있습니다. 예를 들어 시스템 유지보수 중에는 작업 처리를 일시 중지하고 싶을 수 있습니다. Laravel은 큐 워커를 일시 중지하고 재개할 수 있도록 `queue:pause` 및 `queue:continue` Artisan 명령어를 제공합니다.

<!-- To pause a specific queue, provide the queue connection name and the queue name: -->
특정 큐를 일시 중지하려면 큐 연결 이름과 큐 이름을 전달합니다.

```shell
php artisan queue:pause database:default
```

<!-- In this example, `database` is the queue connection name and `default` is the queue name. Once a queue is paused, any workers processing jobs from that queue will continue to finish their current job, but will not pick up any new jobs until the queue is resumed. -->
이 예제에서 `database`는 큐 연결 이름이고 `default`는 큐 이름입니다. 큐가 일시 중지되면 해당 큐에서 작업을 처리 중인 워커는 현재 작업을 계속 완료하지만, 큐가 재개될 때까지 새 작업을 가져오지 않습니다.

<!-- To pause job processing for every queue on every connection, use the `--all` option: -->
모든 연결의 모든 큐에서 잡 처리를 일시 중지하려면 `--all` 옵션을 사용합니다:

```shell
php artisan queue:pause --all
```

<!-- To resume processing jobs on a paused queue, use the `queue:continue` command: -->
일시 중지된 큐에서 작업 처리를 재개하려면 `queue:continue` 명령어를 사용합니다.

```shell
php artisan queue:continue database:default
```

<!-- To resume job processing for every queue on every connection, use the `--all` option with the `queue:resume` command: -->
모든 연결의 모든 큐에서 잡 처리를 재개하려면 `queue:resume` 명령어와 함께 `--all` 옵션을 사용합니다:

```shell
php artisan queue:resume --all
```

<!-- After resuming a queue, workers will begin processing new jobs from that queue immediately. Resuming all queues does not resume queues that were paused individually. Note that pausing a queue does not stop the worker process itself - it only prevents the worker from processing new jobs from the specified queue. -->
큐를 재개하면 워커는 즉시 해당 큐의 새 잡 처리를 시작합니다. 모든 큐를 재개해도 개별적으로 일시 중지된 큐까지 재개되지는 않습니다. 큐를 일시 중지해도 워커 프로세스 자체가 중지되는 것은 아닙니다. 지정한 큐에서 새 잡을 처리하지 못하게 할 뿐입니다.

<a name="worker-restart-and-pause-signals"></a>
<!-- #### Worker Restart and Pause Signals -->
#### Worker Restart and Pause Signals

<!-- By default, queue workers poll the cache driver for restart and pause signals on each job iteration. While this polling is essential for responding to `queue:restart` and `queue:pause` commands, it does introduce a small performance overhead. -->
기본적으로 큐 워커는 각 작업 반복마다 재시작 및 일시 중지 신호가 있는지 캐시 드라이버를 폴링합니다. 이 폴링은 `queue:restart` 및 `queue:pause` 명령어에 응답하는 데 필수적이지만, 약간의 성능 오버헤드를 발생시킵니다.

<!-- If you need to optimize performance and don't require these interruption features, you may disable this polling globally by calling the `withoutInterruptionPolling` method on the `Queue` facade. This should typically be done in the `boot` method of your `AppServiceProvider`: -->
성능을 최적화해야 하고 이러한 중단 기능이 필요하지 않다면, `Queue` 파사드의 `withoutInterruptionPolling` 메서드를 호출하여 이 폴링을 전역으로 비활성화할 수 있습니다. 일반적으로 이 작업은 `AppServiceProvider`의 `boot` 메서드에서 수행해야 합니다.

```php
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Queue::withoutInterruptionPolling();
}
```

<!-- Alternatively, you may disable restart or pause polling individually by setting the static `$restartable` or `$pausable` properties on the `Illuminate\Queue\Worker` class: -->
또는 `Illuminate\Queue\Worker` 클래스의 정적 `$restartable` 또는 `$pausable` 속성을 설정하여 재시작 또는 일시 중지 폴링을 각각 비활성화할 수 있습니다.

```php
use Illuminate\Queue\Worker;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Worker::$restartable = false;
    Worker::$pausable = false;
}
```

> [!WARNING]
> 인터럽트 폴링을 비활성화하면 워커는 비활성화된 기능에 따라 `queue:restart` 또는 `queue:pause` 명령에 응답하지 않습니다.

<a name="supervisor-configuration"></a>
<!-- ## Supervisor Configuration -->
## Supervisor Configuration

<!-- In production, you need a way to keep your `queue:work` processes running. A `queue:work` process may stop running for a variety of reasons, such as an exceeded worker timeout or the execution of the `queue:restart` command. -->
프로덕션 환경에서는 `queue:work` 프로세스가 계속 실행되도록 유지하는 방법이 필요합니다. `queue:work` 프로세스는 워커 타임아웃 초과나 `queue:restart` 명령어 실행 등 다양한 이유로 중지될 수 있습니다.

<!-- For this reason, you need to configure a process monitor that can detect when your `queue:work` processes exit and automatically restart them. In addition, process monitors can allow you to specify how many `queue:work` processes you would like to run concurrently. Supervisor is a process monitor commonly used in Linux environments and we will discuss how to configure it in the following documentation. -->
이러한 이유로 `queue:work` 프로세스가 종료되는 것을 감지하고 자동으로 다시 시작할 수 있는 프로세스 모니터를 설정해야 합니다. 또한 프로세스 모니터를 사용하면 동시에 실행할 `queue:work` 프로세스 수를 지정할 수 있습니다. Supervisor는 Linux 환경에서 흔히 사용되는 프로세스 모니터이며, 다음 문서에서 설정 방법을 설명합니다.

<a name="installing-supervisor"></a>
<!-- #### Installing Supervisor -->
#### Installing Supervisor

<!-- Supervisor is a process monitor for the Linux operating system, and will automatically restart your `queue:work` processes if they fail. To install Supervisor on Ubuntu, you may use the following command: -->
Supervisor는 Linux 운영 체제용 프로세스 모니터이며, `queue:work` 프로세스가 실패하면 자동으로 다시 시작합니다. Ubuntu에 Supervisor를 설치하려면 다음 명령어를 사용할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor를 직접 구성하고 관리하는 일이 부담스럽게 느껴진다면, Laravel 큐 워커를 실행하기 위한 완전 관리형 플랫폼을 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 사용해 보세요.

<a name="configuring-supervisor"></a>
<!-- #### Configuring Supervisor -->
#### Configuring Supervisor

<!-- Supervisor configuration files are typically stored in the `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `laravel-worker.conf` file that starts and monitors `queue:work` processes: -->
Supervisor 설정 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 안에서 프로세스를 어떻게 모니터링해야 하는지 supervisor에 알려주는 설정 파일을 원하는 만큼 만들 수 있습니다. 예를 들어 `queue:work` 프로세스를 시작하고 모니터링하는 `laravel-worker.conf` 파일을 만들어 보겠습니다.

```ini
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/app.com/artisan queue:work --sleep=3 --tries=3 --max-time=3600
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
이 예제에서 `numprocs` 지시어는 Supervisor에게 여덟 개의 `queue:work` 프로세스를 실행하고 모두 모니터링하며, 실패하면 자동으로 다시 시작하도록 지시합니다. 설정의 `command` 지시어는 원하는 큐 연결과 워커 옵션에 맞게 변경해야 합니다.

> [!WARNING]
> `stopwaitsecs`의 값이 가장 오래 실행되는 잡에 소요되는 시간(초)보다 큰지 확인해야 합니다. 그렇지 않으면 Supervisor가 잡 처리가 끝나기 전에 잡을 종료할 수 있습니다.

<a name="starting-supervisor"></a>
<!-- #### Starting Supervisor -->
#### Starting Supervisor

<!-- Once the configuration file has been created, you may update the Supervisor configuration and start the processes using the following commands: -->
설정 파일을 만든 후에는 다음 명령어를 사용하여 Supervisor 설정을 갱신하고 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

<!-- For more information on Supervisor, consult the [Supervisor documentation](http://supervisord.org/index.html). -->
Supervisor에 대한 자세한 내용은 [Supervisor documentation](http://supervisord.org/index.html)를 참고하십시오.

<a name="dealing-with-failed-jobs"></a>
<!-- ## Dealing With Failed Jobs -->
## Dealing With Failed Jobs

<!-- Sometimes your queued jobs will fail. Don't worry, things don't always go as planned! Laravel includes a convenient way to [specify the maximum number of times a job should be attempted](#max-job-attempts-and-timeout). After an asynchronous job has exceeded this number of attempts, it will be inserted into the `failed_jobs` database table. [Synchronously dispatched jobs](/docs/13.x/queues#synchronous-dispatching) that fail are not stored in this table and their exceptions are immediately handled by the application. -->
큐에 등록한 잡이 실패하는 경우가 있습니다. 걱정하지 마세요. 항상 일이 계획대로 진행되지는 않습니다! Laravel은 [specify the maximum number of times a job should be attempted](#max-job-attempts-and-timeout)할 수 있는 편리한 방법을 제공합니다. 비동기 잡이 이 시도 횟수를 초과하면 `failed_jobs` 데이터베이스 테이블에 삽입됩니다. 실패한 [Synchronously dispatched jobs](/docs/13.x/queues#synchronous-dispatching)는 이 테이블에 저장되지 않으며, 해당 예외는 애플리케이션에서 즉시 처리합니다.

<!-- A migration to create the `failed_jobs` table is typically already present in new Laravel applications. However, if your application does not contain a migration for this table, you may use the `make:queue-failed-table` command to create the migration: -->
`failed_jobs` 테이블을 생성하는 마이그레이션은 일반적으로 새 Laravel 애플리케이션에 이미 포함되어 있습니다. 하지만 애플리케이션에 이 테이블을 위한 마이그레이션이 없다면 `make:queue-failed-table` 명령어를 사용하여 마이그레이션을 만들 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

<!-- When running a [queue worker](#running-the-queue-worker) process, you may specify the maximum number of times a job should be attempted using the `--tries` switch on the `queue:work` command. If you do not specify a value for the `--tries` option, jobs will only be attempted once or as many times as specified by the job class' `Tries` attribute: -->
[queue worker](#running-the-queue-worker) 프로세스를 실행할 때 `queue:work` 명령어의 `--tries` 스위치를 사용하여 작업을 시도할 최대 횟수를 지정할 수 있습니다. `--tries` 옵션 값을 지정하지 않으면 작업은 한 번만 시도되거나, 작업 클래스의 `Tries` 속성에 지정된 횟수만큼 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

<!-- Using the `--backoff` option, you may specify how many seconds Laravel should wait before retrying a job that has encountered an exception. By default, a job is immediately released back onto the queue so that it may be attempted again: -->
`--backoff` 옵션을 사용하면 예외가 발생한 작업을 다시 시도하기 전에 Laravel이 몇 초 동안 기다려야 하는지 지정할 수 있습니다. 기본적으로 작업은 즉시 다시 큐로 반환되어 다시 시도될 수 있습니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

<!-- If you would like to configure how many seconds Laravel should wait before retrying a job that has encountered an exception on a per-job basis, you may use the `Backoff` attribute on your job class: -->
예외가 발생한 작업을 다시 시도하기 전에 Laravel이 몇 초 동안 기다려야 하는지를 작업별로 설정하고 싶다면, 작업 클래스에서 `Backoff` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

<!-- If you require more complex logic for determining the job's backoff time, you may define a `backoff` method on your job class: -->
작업의 backoff 시간을 결정하기 위해 더 복잡한 로직이 필요하다면, 작업 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the job.
 */
public function backoff(): int
{
    return 3;
}
```

<!-- You may easily configure "exponential" backoffs by defining an array of backoff values. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining: -->
backoff 값 배열을 정의하여 "지수적" backoff를 쉽게 설정할 수 있습니다. 이 예제에서 재시도 지연 시간은 첫 번째 재시도에는 1초, 두 번째 재시도에는 5초, 세 번째 재시도에는 10초이며, 남은 시도가 더 있다면 이후 모든 재시도에는 10초가 적용됩니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Backoff;

#[Backoff([1, 5, 10])]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

<a name="cleaning-up-after-failed-jobs"></a>
<!-- ### Cleaning Up After Failed Jobs -->
### Cleaning Up After Failed Jobs

<!-- When a particular job fails, you may want to send an alert to your users or revert any actions that were partially completed by the job. To accomplish this, you may define a `failed` method on your job class. The `Throwable` instance that caused the job to fail will be passed to the `failed` method: -->
특정 작업이 실패하면 사용자에게 알림을 보내거나, 작업에서 부분적으로 완료된 동작을 되돌리고 싶을 수 있습니다. 이를 위해 작업 클래스에 `failed` 메서드를 정의할 수 있습니다. 작업 실패의 원인이 된 `Throwable` 인스턴스가 `failed` 메서드에 전달됩니다.

```php
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
```

> [!WARNING]
> `failed` 메서드를 호출하기 전에 잡의 새 인스턴스가 생성되므로, `handle` 메서드 내에서 발생했을 수 있는 모든 클래스 프로퍼티 수정 사항은 손실됩니다.

<!-- A failed job is not necessarily one that encountered an unhandled exception. A job may also be considered failed when it has exhausted all of its allowed attempts. These attempts can be consumed in several ways: -->
실패한 작업이 반드시 처리되지 않은 예외를 만난 작업만을 의미하지는 않습니다. 허용된 모든 시도 횟수를 소진한 작업도 실패한 것으로 간주될 수 있습니다. 이러한 시도 횟수는 여러 방식으로 소모될 수 있습니다.

<div class="content-list" markdown="1">

<!-- - The job timed out. - The job encounters an unhandled exception during execution. - The job is released back to the queue either manually or by a middleware. -->
- 잡 실행 시간이 초과되었습니다.
- 잡을 실행하는 동안 처리되지 않은 예외가 발생했습니다.
- 잡이 수동으로 또는 미들웨어에 의해 큐로 반환되었습니다.

</div>

<!-- If the final attempt fails due to an exception thrown during job execution, that exception will be passed to the job's `failed` method. However, if the job fails because it has reached the maximum number of allowed attempts, the `$exception` will be an instance of `Illuminate\Queue\MaxAttemptsExceededException`. Similarly, if the job fails due to exceeding the configured timeout, the `$exception` will be an instance of `Illuminate\Queue\TimeoutExceededException`. -->
마지막 시도가 작업 실행 중 발생한 예외 때문에 실패했다면, 해당 예외가 작업의 `failed` 메서드에 전달됩니다. 하지만 작업이 허용된 최대 시도 횟수에 도달해서 실패했다면 `$exception`은 `Illuminate\Queue\MaxAttemptsExceededException`의 인스턴스가 됩니다. 마찬가지로 설정된 타임아웃을 초과해서 작업이 실패했다면 `$exception`은 `Illuminate\Queue\TimeoutExceededException`의 인스턴스가 됩니다.

<a name="retrying-failed-jobs"></a>
<!-- ### Retrying Failed Jobs -->
### Retrying Failed Jobs

<!-- To view all of the failed jobs that have been inserted into your `failed_jobs` database table, you may use the `queue:failed` Artisan command: -->
`failed_jobs` 데이터베이스 테이블에 삽입된 모든 실패한 작업을 보려면 `queue:failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:failed
```

<!-- The `queue:failed` command will list the job ID, connection, queue, failure time, and other information about the job. The job ID may be used to retry the failed job. For instance, to retry a failed job that has an ID of `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`, issue the following command: -->
`queue:failed` 명령어는 작업 ID, 연결, 큐, 실패 시간 및 작업에 대한 기타 정보를 나열합니다. 작업 ID는 실패한 작업을 다시 시도하는 데 사용할 수 있습니다. 예를 들어 ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패한 작업을 다시 시도하려면 다음 명령어를 실행합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

<!-- If necessary, you may pass multiple IDs to the command: -->
필요하다면 명령어에 여러 ID를 전달할 수 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

<!-- You may also retry all of the failed jobs for a particular queue: -->
특정 큐의 모든 실패한 작업을 다시 시도할 수도 있습니다.

```shell
php artisan queue:retry --queue=name
```

<!-- To retry all of your failed jobs, execute the `queue:retry` command and pass `all` as the ID: -->
모든 실패한 작업을 다시 시도하려면 `queue:retry` 명령어를 실행하고 ID로 `all`을 전달합니다.

```shell
php artisan queue:retry all
```

<!-- If you would like to delete a failed job, you may use the `queue:forget` command: -->
실패한 작업을 삭제하고 싶다면 `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/13.x/horizon)을 사용할 때는 실패한 잡을 삭제하려면 `queue:forget` 명령어 대신 `horizon:forget` 명령어를 사용해야 합니다.

<!-- To delete all of your failed jobs from the `failed_jobs` table, you may use the `queue:flush` command: -->
`failed_jobs` 테이블에서 모든 실패한 작업을 삭제하려면 `queue:flush` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:flush
```

<!-- The `queue:flush` command removes all failed job records from your queue, no matter how old the failed job is. You may use the `--hours` option to only delete jobs that failed a certain number of hours ago or earlier: -->
`queue:flush` 명령어는 실패한 작업이 얼마나 오래되었는지와 관계없이 큐에서 모든 실패한 작업 레코드를 제거합니다. `--hours` 옵션을 사용하면 특정 시간 전 또는 그보다 더 이전에 실패한 작업만 삭제할 수 있습니다.

```shell
php artisan queue:flush --hours=48
```

<a name="ignoring-missing-models"></a>
<!-- ### Ignoring Missing Models -->
### Ignoring Missing Models

<!-- When injecting an Eloquent model into a job, the model is automatically serialized before being placed on the queue and re-retrieved from the database when the job is processed. However, if the model has been deleted while the job was waiting to be processed by a worker, your job may fail with a `ModelNotFoundException`. -->
Eloquent 모델을 작업에 주입하면, 모델은 큐에 들어가기 전에 자동으로 직렬화되고 작업이 처리될 때 데이터베이스에서 다시 조회됩니다. 하지만 작업이 워커에 의해 처리되기를 기다리는 동안 모델이 삭제되었다면, 작업은 `ModelNotFoundException`으로 실패할 수 있습니다.

<!-- For convenience, you may choose to automatically delete jobs with missing models using the `DeleteWhenMissingModels` attribute on your job class. When this attribute is present, Laravel will quietly discard the job without raising an exception: -->
편의를 위해 작업 클래스에서 `DeleteWhenMissingModels` 속성을 사용하여 누락된 모델이 있는 작업을 자동으로 삭제하도록 선택할 수 있습니다. 이 속성이 있으면 Laravel은 예외를 발생시키지 않고 작업을 조용히 폐기합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\DeleteWhenMissingModels;

#[DeleteWhenMissingModels]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

<a name="pruning-failed-jobs"></a>
<!-- ### Pruning Failed Jobs -->
### Pruning Failed Jobs

<!-- You may prune the records in your application's `failed_jobs` table by invoking the `queue:prune-failed` Artisan command: -->
`queue:prune-failed` Artisan 명령어를 호출하여 애플리케이션의 `failed_jobs` 테이블에 있는 레코드를 정리할 수 있습니다.

```shell
php artisan queue:prune-failed
```

<!-- By default, all the failed job records that are more than 24 hours old will be pruned. If you provide the `--hours` option to the command, only the failed job records that were inserted within the last N number of hours will be retained. For example, the following command will delete all the failed job records that were inserted more than 48 hours ago: -->
기본적으로 24시간보다 오래된 모든 실패한 작업 레코드가 정리됩니다. 명령어에 `--hours` 옵션을 제공하면, 최근 N시간 이내에 삽입된 실패한 작업 레코드만 유지됩니다. 예를 들어 다음 명령어는 48시간보다 더 전에 삽입된 모든 실패한 작업 레코드를 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
<!-- ### Storing Failed Jobs in DynamoDB -->
### Storing Failed Jobs in DynamoDB

<!-- Laravel also provides support for storing your failed job records in [DynamoDB](https://aws.amazon.com/dynamodb) instead of a relational database table. However, you must manually create a DynamoDB table to store all of the failed job records. Typically, this table should be named `failed_jobs`, but you should name the table based on the value of the `queue.failed.table` configuration value within your application's `queue` configuration file. -->
Laravel은 실패한 작업 레코드를 관계형 데이터베이스 테이블 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 기능도 지원합니다. 하지만 모든 실패한 작업 레코드를 저장할 DynamoDB 테이블은 직접 만들어야 합니다. 일반적으로 이 테이블 이름은 `failed_jobs`여야 하지만, 애플리케이션의 `queue` 설정 파일 안에 있는 `queue.failed.table` 설정 값에 따라 테이블 이름을 정해야 합니다.

<!-- The `failed_jobs` table should have a string primary partition key named `application` and a string primary sort key named `uuid`. The `application` portion of the key will contain your application's name as defined by the `name` configuration value within your application's `app` configuration file. Since the application name is part of the DynamoDB table's key, you can use the same table to store failed jobs for multiple Laravel applications. -->
`failed_jobs` 테이블에는 `application`이라는 문자열 기본 파티션 키와 `uuid`라는 문자열 기본 정렬 키가 있어야 합니다. 키의 `application` 부분에는 애플리케이션의 `app` 설정 파일 안에 있는 `name` 설정 값으로 정의된 애플리케이션 이름이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블 키의 일부이므로, 같은 테이블을 사용하여 여러 Laravel 애플리케이션의 실패한 작업을 저장할 수 있습니다.

<!-- In addition, ensure that you install the AWS SDK so that your Laravel application can communicate with Amazon DynamoDB: -->
또한 Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

<!-- Next, set the `queue.failed.driver` configuration option's value to `dynamodb`. In addition, you should define `key`, `secret`, and `region` configuration options within the failed job configuration array. These options will be used to authenticate with AWS. When using the `dynamodb` driver, the `queue.failed.database` configuration option is unnecessary: -->
다음으로 `queue.failed.driver` 설정 옵션 값을 `dynamodb`로 설정합니다. 또한 실패한 작업 설정 배열 안에 `key`, `secret`, `region` 설정 옵션을 정의해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.failed.database` 설정 옵션이 필요하지 않습니다.

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
`queue.failed.driver` 설정 옵션 값을 `null`로 설정하여 Laravel이 실패한 작업을 저장하지 않고 폐기하도록 지시할 수 있습니다. 일반적으로 이는 `QUEUE_FAILED_DRIVER` 환경 변수를 통해 설정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
<!-- ### Failed Job Events -->
### Failed Job Events

<!-- If you would like to register an event listener that will be invoked when a job fails, you may use the `Queue` facade's `failing` method. For example, we may attach a closure to this event from the `boot` method of the `AppServiceProvider` that is included with Laravel: -->
작업이 실패했을 때 호출될 이벤트 리스너를 등록하고 싶다면 `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어 Laravel에 포함된 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트에 클로저를 연결할 수 있습니다.

```php
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
```

<a name="clearing-jobs-from-queues"></a>
<!-- ## Clearing Jobs From Queues -->
## Clearing Jobs From Queues

> [!NOTE]
> [Horizon](/docs/13.x/horizon)을 사용하는 경우 큐에서 잡을 삭제하려면 `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용해야 합니다.

<!-- If you would like to delete all jobs from the default queue of the default connection, you may do so using the `queue:clear` Artisan command: -->
기본 연결의 기본 큐에서 모든 작업을 삭제하려면 `queue:clear` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

<!-- You may also provide the `connection` argument and `queue` option to delete jobs from a specific connection and queue: -->
특정 연결과 큐에서 작업을 삭제하려면 `connection` 인수와 `queue` 옵션을 함께 제공할 수도 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 잡을 삭제하는 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 사용할 수 있습니다. 또한 SQS 메시지 삭제 프로세스에는 최대 60초가 걸리므로, 큐를 비운 후 최대 60초 이내에 SQS 큐로 전송된 잡도 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
<!-- ## Monitoring Your Queues -->
## Monitoring Your Queues

<!-- If your queue receives a sudden influx of jobs, it could become overwhelmed, leading to a long wait time for jobs to complete. If you wish, Laravel can alert you when your queue job count exceeds a specified threshold. -->
큐에 작업이 갑자기 많이 들어오면 큐가 감당하기 어려워지고, 작업이 완료되기까지 대기 시간이 길어질 수 있습니다. 원한다면 Laravel이 큐 작업 수가 지정한 임계값을 초과했을 때 알림을 보내도록 설정할 수 있습니다.

<!-- To get started, you should schedule the `queue:monitor` command to [run every minute](/docs/13.x/scheduling). The command accepts the names of the queues you wish to monitor as well as your desired job count threshold: -->
시작하려면 `queue:monitor` 명령어가 [run every minute](/docs/13.x/scheduling) 실행되도록 예약해야 합니다. 이 명령어는 모니터링할 큐 이름과 원하는 잡 수 임계값을 인수로 받습니다:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

<!-- Scheduling this command alone is not enough to trigger a notification alerting you of the queue's overwhelmed status. When the command encounters a queue that has a job count exceeding your threshold, an `Illuminate\Queue\Events\QueueBusy` event will be dispatched. You may listen for this event within your application's `AppServiceProvider` in order to send a notification to you or your development team: -->
이 명령어를 스케줄링하는 것만으로는 큐가 과부하 상태라는 알림이 자동으로 전송되지 않습니다. 명령어가 작업 수가 임계값을 초과한 큐를 발견하면 `Illuminate\Queue\Events\QueueBusy` 이벤트가 디스패치됩니다. 이 이벤트를 애플리케이션의 `AppServiceProvider`에서 수신하여 자신이나 개발팀에 알림을 보낼 수 있습니다.

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
                $event->connectionName,
                $event->queue,
                $event->size
            ));
    });
}
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When testing code that dispatches jobs, you may wish to instruct Laravel to not actually execute the job itself, since the job's code can be tested directly and separately of the code that dispatches it. Of course, to test the job itself, you may instantiate a job instance and invoke the `handle` method directly in your test. -->
작업을 디스패치하는 코드를 테스트할 때는 작업 자체가 실제로 실행되지 않도록 Laravel에 지시하고 싶을 수 있습니다. 작업의 코드는 해당 작업을 디스패치하는 코드와 분리해서 직접 테스트할 수 있기 때문입니다. 물론 작업 자체를 테스트하려면 테스트에서 작업 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

<!-- You may use the `Queue` facade's `fake` method to prevent queued jobs from actually being pushed to the queue. After calling the `Queue` facade's `fake` method, you may then assert that the application attempted to push jobs to the queue: -->
큐 작업이 실제로 큐에 푸시되지 않도록 하려면 `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. `Queue` 파사드의 `fake` 메서드를 호출한 뒤에는 애플리케이션이 작업을 큐에 푸시하려고 시도했는지 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // Perform order shipping...

    // Assert that no jobs were pushed...
    Queue::assertNothingPushed();

    // Assert a job was pushed to a given queue...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // Assert a job was pushed
    Queue::assertPushed(ShipOrder::class);

    // Assert a job was pushed exactly once...
    Queue::assertPushedOnce(ShipOrder::class);

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);

    // Assert a job was not pushed...
    Queue::assertNotPushed(AnotherJob::class);

    // Assert that a closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert that a closure was not pushed...
    Queue::assertClosureNotPushed();

    // Assert the total number of jobs that were pushed...
    Queue::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
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

        // Assert a job was pushed
        Queue::assertPushed(ShipOrder::class);

        // Assert a job was pushed exactly once...
        Queue::assertPushedOnce(ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushedTimes(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);

        // Assert that a closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert that a closure was not pushed...
        Queue::assertClosureNotPushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```

<!-- You may pass a closure to the `assertPushed`, `assertNotPushed`, `assertClosurePushed`, or `assertClosureNotPushed` methods in order to assert that a job was pushed that passes a given "truth test". If at least one job was pushed that passes the given truth test then the assertion will be successful: -->
`assertPushed`, `assertNotPushed`, `assertClosurePushed`, `assertClosureNotPushed` 메서드에는 클로저를 전달하여, 지정한 truth test(참 여부를 판별하는 조건)를 통과하는 작업이 푸시되었는지 검증할 수 있습니다. 지정한 조건을 통과하는 작업이 하나 이상 푸시되었다면 검증은 성공합니다.

```php
use Illuminate\Queue\CallQueuedClosure;

Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});

Queue::assertClosurePushed(function (CallQueuedClosure $job) {
    return $job->name === 'validate-order';
});
```

<a name="faking-a-subset-of-jobs"></a>
<!-- ### Faking a Subset of Jobs -->
### Faking a Subset of Jobs

<!-- If you only need to fake specific jobs while allowing your other jobs to execute normally, you may pass the class names of the jobs that should be faked to the `fake` method: -->
다른 작업은 정상적으로 실행되도록 두고 특정 작업만 가짜 처리해야 한다면, 가짜 처리할 작업의 클래스 이름을 `fake` 메서드에 전달할 수 있습니다.

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);
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
    Queue::assertPushedTimes(ShipOrder::class, 2);
}
```

<!-- You may fake all jobs except for a set of specified jobs using the `except` method: -->
`except` 메서드를 사용하면 지정한 작업 집합을 제외한 모든 작업을 가짜 처리할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
<!-- ### Testing Job Chains -->
### Testing Job Chains

<!-- To test job chains, you will need to utilize the `Bus` facade's faking capabilities. The `Bus` facade's `assertChained` method may be used to assert that a [chain of jobs](/docs/13.x/queues#job-chaining) was dispatched. The `assertChained` method accepts an array of chained jobs as its first argument: -->
잡 체인을 테스트하려면 `Bus` 파사드의 페이크 기능을 사용해야 합니다. `Bus` 파사드의 `assertChained` 메서드를 사용하면 [chain of jobs](/docs/13.x/queues#job-chaining)이 디스패치되었는지 확인할 수 있습니다. `assertChained` 메서드는 체인으로 연결된 잡의 배열을 첫 번째 인수로 받습니다:

```php
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
```

<!-- As you can see in the example above, the array of chained jobs may be an array of the job's class names. However, you may also provide an array of actual job instances. When doing so, Laravel will ensure that the job instances are of the same class and have the same property values of the chained jobs dispatched by your application: -->
위 예제에서 볼 수 있듯이, 체인으로 연결된 작업 배열은 작업의 클래스 이름 배열일 수 있습니다. 하지만 실제 작업 인스턴스 배열을 제공할 수도 있습니다. 이 경우 Laravel은 애플리케이션에서 디스패치한 체인 작업과 제공된 작업 인스턴스가 같은 클래스이며 같은 속성 값을 가지는지 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

<!-- You may use the `assertDispatchedWithoutChain` method to assert that a job was pushed without a chain of jobs: -->
작업이 작업 체인 없이 푸시되었는지 검증하려면 `assertDispatchedWithoutChain` 메서드를 사용할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
<!-- #### Testing Chain Modifications -->
#### Testing Chain Modifications

<!-- If a chained job [prepends or appends jobs to an existing chain](#adding-jobs-to-the-chain), you may use the job's `assertHasChain` method to assert that the job has the expected chain of remaining jobs: -->
체인으로 연결된 작업이 [prepends or appends jobs to an existing chain](#adding-jobs-to-the-chain)한다면, 해당 작업의 `assertHasChain` 메서드를 사용하여 작업에 예상한 나머지 작업 체인이 있는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

<!-- The `assertDoesntHaveChain` method may be used to assert that the job's remaining chain is empty: -->
작업의 남은 체인이 비어 있는지 검증하려면 `assertDoesntHaveChain` 메서드를 사용할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
<!-- #### Testing Chained Batches -->
#### Testing Chained Batches

<!-- If your job chain [contains a batch of jobs](#chains-and-batches), you may assert that the chained batch matches your expectations by inserting a `Bus::chainedBatch` definition within your chain assertion: -->
작업 체인에 [contains a batch of jobs](#chains-and-batches) 있다면, 체인 검증 안에 `Bus::chainedBatch` 정의를 삽입하여 체인된 배치가 기대한 내용과 일치하는지 검증할 수 있습니다.

```php
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
```

<a name="testing-job-batches"></a>
<!-- ### Testing Job Batches -->
### Testing Job Batches

<!-- The `Bus` facade's `assertBatched` method may be used to assert that a [batch of jobs](/docs/13.x/queues#job-batching) was dispatched. The closure given to the `assertBatched` method receives an instance of `Illuminate\Bus\PendingBatch`, which may be used to inspect the jobs within the batch: -->
`Bus` 파사드의 `assertBatched` 메서드를 사용하면 [batch of jobs](/docs/13.x/queues#job-batching)가 디스패치되었는지 확인할 수 있습니다. `assertBatched` 메서드에 전달한 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 받으며, 이 인스턴스를 사용해 배치 내 잡을 검사할 수 있습니다:

```php
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'Import CSV' &&
           $batch->jobs->count() === 10;
});
```

<!-- The `hasJobs` method may be used on the pending batch to verify that the batch contains the expected jobs. The method accepts an array of job instances, class names, or closures: -->
대기 중인 배치에 예상한 작업이 포함되어 있는지 확인하려면 해당 배치에서 `hasJobs` 메서드를 사용할 수 있습니다. 이 메서드는 작업 인스턴스, 클래스 이름, 클로저로 구성된 배열을 받습니다.

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        new ProcessCsvRow(row: 1),
        new ProcessCsvRow(row: 2),
        new ProcessCsvRow(row: 3),
    ]);
});
```

<!-- When using closures, the closure will receive the job instance. The expected job type will be inferred from the closure's type hint: -->
클로저를 사용할 때 클로저는 작업 인스턴스를 받습니다. 예상되는 작업 타입은 클로저의 타입 힌트에서 추론됩니다.

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        fn (ProcessCsvRow $job) => $job->row === 1,
        fn (ProcessCsvRow $job) => $job->row === 2,
        fn (ProcessCsvRow $job) => $job->row === 3,
    ]);
});
```

<!-- You may use the `assertBatchCount` method to assert that a given number of batches were dispatched: -->
주어진 개수의 배치가 디스패치되었는지 검증하려면 `assertBatchCount` 메서드를 사용할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

<!-- You may use `assertNothingBatched` to assert that no batches were dispatched: -->
배치가 전혀 디스패치되지 않았는지 검증하려면 `assertNothingBatched`를 사용할 수 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
<!-- #### Testing Job / Batch Interaction -->
#### Testing Job / Batch Interaction

<!-- In addition, you may occasionally need to test an individual job's interaction with its underlying batch. For example, you may need to test if a job cancelled further processing for its batch. To accomplish this, you need to assign a fake batch to the job via the `withFakeBatch` method. The `withFakeBatch` method returns a tuple containing the job instance and the fake batch: -->
또한 개별 작업이 기반 배치와 어떻게 상호작용하는지 테스트해야 할 때도 있습니다. 예를 들어, 어떤 작업이 해당 배치의 이후 처리를 취소했는지 테스트해야 할 수 있습니다. 이를 위해서는 `withFakeBatch` 메서드를 통해 작업에 가짜 배치를 할당해야 합니다. `withFakeBatch` 메서드는 작업 인스턴스와 가짜 배치를 포함하는 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
<!-- ### Testing Job / Queue Interactions -->
### Testing Job / Queue Interactions

<!-- Sometimes, you may need to test that a queued job [releases itself back onto the queue](#manually-releasing-a-job). Or, you may need to test that the job deleted itself. You may test these queue interactions by instantiating the job and invoking the `withFakeQueueInteractions` method. -->
때로는 큐에 들어간 작업이 스스로 큐에 다시 반환되는지([releases itself back onto the queue](#manually-releasing-a-job)) 테스트해야 할 수 있습니다. 또는 작업이 자기 자신을 삭제했는지 테스트해야 할 수도 있습니다. 이러한 큐 상호작용은 작업을 인스턴스화하고 `withFakeQueueInteractions` 메서드를 호출하여 테스트할 수 있습니다.

<!-- Once the job's queue interactions have been faked, you may invoke the `handle` method on the job. After invoking the job, various assertion methods are available to verify the job's queue interactions: -->
작업의 큐 상호작용을 가짜 처리한 뒤에는 작업의 `handle` 메서드를 호출할 수 있습니다. 작업을 호출한 뒤에는 다양한 검증 메서드를 사용하여 작업의 큐 상호작용을 확인할 수 있습니다.

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
<!-- ## Job Events -->
## Job Events

<!-- Using the `before` and `after` methods on the `Queue` [facade](/docs/13.x/facades), you may specify callbacks to be executed before or after a queued job is processed. These callbacks are a great opportunity to perform additional logging or increment statistics for a dashboard. Typically, you should call these methods from the `boot` method of a [service provider](/docs/13.x/providers). For example, we may use the `AppServiceProvider` that is included with Laravel: -->
`Queue` [facade](/docs/13.x/facades)의 `before` 및 `after` 메서드를 사용하면 큐 작업이 처리되기 전이나 후에 실행할 콜백을 지정할 수 있습니다. 이러한 콜백은 추가 로깅을 수행하거나 대시보드의 통계 수치를 증가시키는 데 유용합니다. 일반적으로 [service provider](/docs/13.x/providers)의 `boot` 메서드에서 이러한 메서드를 호출해야 합니다. 예를 들어 Laravel에 포함된 `AppServiceProvider`를 사용할 수 있습니다:

```php
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
```

<!-- Using the `looping` method on the `Queue` [facade](/docs/13.x/facades), you may specify callbacks that execute before the worker attempts to fetch a job from a queue. For example, you might register a closure to rollback any transactions that were left open by a previously failed job: -->
`Queue` [facade](/docs/13.x/facades)의 `looping` 메서드를 사용하면 워커가 큐에서 잡을 가져오기 전에 실행할 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 잡이 열어 둔 채로 남긴 트랜잭션을 롤백하는 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```

<!-- Laravel also dispatches an `Illuminate\Queue\Events\WorkerIdle` event when a queue worker is unable to retrieve a job from the queue: -->
Laravel은 큐 워커가 큐에서 잡을 가져오지 못할 때도 `Illuminate\Queue\Events\WorkerIdle` 이벤트를 디스패치합니다:

```php
use Illuminate\Queue\Events\WorkerIdle;
use Illuminate\Support\Facades\Event;

Event::listen(function (WorkerIdle $event) {
    // $event->connectionName
    // $event->queue
    // $event->workerOptions
});
```
