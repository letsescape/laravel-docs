<!-- # Queues -->
# Queues

- [Introduction](#introduction)
    - [Connections vs. Queues](#connections-vs-queues)
    - [Driver Notes and Prerequisites](#driver-prerequisites)
- [Creating Jobs](#creating-jobs)
    - [Generating Job Classes](#generating-job-classes)
    - [Class Structure](#class-structure)
    - [Unique Jobs](#unique-jobs)
    - [Encrypted Jobs](#encrypted-jobs)
- [Job Middleware](#job-middleware)
    - [Rate Limiting](#rate-limiting)
    - [Preventing Job Overlaps](#preventing-job-overlaps)
    - [Throttling Exceptions](#throttling-exceptions)
    - [Skipping Jobs](#skipping-jobs)
- [Dispatching Jobs](#dispatching-jobs)
    - [Delayed Dispatching](#delayed-dispatching)
    - [Synchronous Dispatching](#synchronous-dispatching)
    - [Jobs & Database Transactions](#jobs-and-database-transactions)
    - [Job Chaining](#job-chaining)
    - [Customizing The Queue and Connection](#customizing-the-queue-and-connection)
    - [Specifying Max Job Attempts / Timeout Values](#max-job-attempts-and-timeout)
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
    - [Job Expirations and Timeouts](#job-expirations-and-timeouts)
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
웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하거나 저장하는 등 일반적인 웹 요청 중에 처리하기에는 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히도 Laravel은 이러한 작업을 쉽게 백그라운드에서 처리할 수 있도록 큐에 담아 실행하는 잡 작업을 지원합니다. 시간 소요가 큰 작업을 큐로 분리하면 애플리케이션이 웹 요청에 훨씬 빠르게 응답할 수 있어 사용자 경험도 크게 향상됩니다.

<!-- Laravel queues provide a unified queueing API across a variety of different queue backends, such as [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), or even a relational database. -->
Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 그리고 관계형 데이터베이스 등 다양한 큐 백엔드를 아우르는 통합된 큐 API를 제공합니다.

<!-- Laravel's queue configuration options are stored in your application's `config/queue.php` configuration file. In this file, you will find connection configurations for each of the queue drivers that are included with the framework, including the database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), and [Beanstalkd](https://beanstalkd.github.io/) drivers, as well as a synchronous driver that will execute jobs immediately (for use during local development). A `null` queue driver is also included which discards queued jobs. -->
큐 설정 옵션들은 애플리케이션의 `config/queue.php` 설정 파일에 보관되어 있습니다. 이 파일에는 database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 프레임워크에 기본 내장된 각 큐 드라이버에 대한 연결(커넥션) 설정이 미리 정의되어 있습니다. 또한, 잡을 즉시 실행하는 시크로너스(synchronous) 드라이버(로컬 개발 환경에서 사용)를 비롯해 큐에 담긴 잡을 폐기하는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel은 이제 Redis 기반 큐를 위한 강력한 대시보드 및 설정 시스템인 Horizon도 제공합니다. 더 자세한 정보는 [Horizon documentation](/docs/11.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
<!-- ### Connections vs. Queues -->
### Connections vs. Queues

<!-- Before getting started with Laravel queues, it is important to understand the distinction between "connections" and "queues". In your `config/queue.php` configuration file, there is a `connections` configuration array. This option defines the connections to backend queue services such as Amazon SQS, Beanstalk, or Redis. However, any given queue connection may have multiple "queues" which may be thought of as different stacks or piles of queued jobs. -->
Laravel 큐를 사용하기 전에 반드시 "커넥션(connection)"과 "큐(queue)"의 차이를 이해해야 합니다. `config/queue.php` 설정 파일 내에는 `connections`라는 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 연결 정보를 정의합니다. 단, 하나의 큐 커넥션에는 여러 개의 “큐”가 존재할 수 있습니다. 각 큐는 여러 잡이 쌓여 있는 별도의 스택 또는 집합으로 생각하면 됩니다.

<!-- Note that each connection configuration example in the `queue` configuration file contains a `queue` attribute. This is the default queue that jobs will be dispatched to when they are sent to a given connection. In other words, if you dispatch a job without explicitly defining which queue it should be dispatched to, the job will be placed on the queue that is defined in the `queue` attribute of the connection configuration: -->
`queue` 설정 파일의 각 커넥션 설정 예제에는 `queue` 속성이 포함되어 있습니다. 이는 해당 커넥션에 잡이 디스패치될 때 기본적으로 사용되는 큐를 의미합니다. 즉, 디스패치 시 어떤 큐에 넣을지 명시하지 않으면 커넥션 설정의 `queue`에 정의된 큐에 잡이 쌓이게 됩니다.

```
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```

<!-- Some applications may not need to ever push jobs onto multiple queues, instead preferring to have one simple queue. However, pushing jobs to multiple queues can be especially useful for applications that wish to prioritize or segment how jobs are processed, since the Laravel queue worker allows you to specify which queues it should process by priority. For example, if you push jobs to a `high` queue, you may run a worker that gives them higher processing priority: -->
일부 애플리케이션은 단일 큐만 사용하는 단순한 구조를 가질 수 있습니다. 그러나 복수의 큐로 잡을 분산시키면 잡의 우선순위 지정이나 목적에 따라 잡 처리 방식을 세분화할 수 있어 매우 유용합니다. Laravel의 큐 워커는 처리할 큐의 우선순위를 지정할 수 있기 때문입니다. 예를 들어, `high`라는 큐에 잡을 몰아서 넣을 경우, 해당 큐를 우선적으로 처리하는 워커를 아래와 같이 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Notes and Prerequisites -->
### Driver Notes and Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- In order to use the `database` queue driver, you will need a database table to hold the jobs. Typically, this is included in Laravel's default `0001_01_01_000002_create_jobs_table.php` [database migration](/docs/11.x/migrations); however, if your application does not contain this migration, you may use the `make:queue-table` Artisan command to create it: -->
`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 [database migration](/docs/11.x/migrations) 파일인 `0001_01_01_000002_create_jobs_table.php`에 이 테이블이 포함되어 있습니다. 만약 실제 애플리케이션에 이 마이그레이션 파일이 없다면, `make:queue-table` 아티즌 명령어로 직접 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- In order to use the `redis` queue driver, you should configure a Redis database connection in your `config/database.php` configuration file. -->
`redis` 큐 드라이버를 사용하려면, 반드시 `config/database.php` 설정 파일에서 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]
> `serializer`와 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원하지 않습니다.

<!-- **Redis Cluster** -->
**Redis 클러스터**

<!-- If your Redis queue connection uses a Redis Cluster, your queue names must contain a [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags). This is required in order to ensure all of the Redis keys for a given queue are placed into the same hash slot: -->
Redis 큐 커넥션이 Redis 클러스터를 사용하는 경우, 큐 이름에 반드시 [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags)가 포함되어야 합니다. 이는 동일한 큐에 대한 모든 Redis 키가 같은 해시 슬롯에 저장되도록 보장하기 위해 필요합니다.

```
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', '{default}'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => null,
    'after_commit' => false,
],
```

<!-- **Blocking** -->
**블로킹(Blocking)**

<!-- When using the Redis queue, you may use the `block_for` configuration option to specify how long the driver should wait for a job to become available before iterating through the worker loop and re-polling the Redis database. -->
Redis 큐를 사용할 때는 `block_for` 설정 옵션을 사용하여 잡이 대기 중일 때 큐 워커 루프가 Redis를 재폴링(반복 조회)하기 전, 얼마나 대기할지 지정할 수 있습니다.

<!-- Adjusting this value based on your queue load can be more efficient than continually polling the Redis database for new jobs. For instance, you may set the value to `5` to indicate that the driver should block for five seconds while waiting for a job to become available: -->
이 값을 큐 적재량에 맞게 조절하면, 지속적으로 Redis에서 새 잡을 폴링하는 것보다 효율적으로 처리할 수 있습니다. 예를 들어, 값을 `5`로 설정하면 잡이 대기 중일 때 최대 5초 동안 대기하도록 지정할 수 있습니다.

```
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
> `block_for` 값을 `0`으로 설정하면 워커가 잡이 생길 때까지 무한정 블로킹됩니다. 이 경우, `SIGTERM`과 같은 종료 신호가 다음 잡이 처리될 때까지 처리되지 않으니 주의하세요.

<a name="other-driver-prerequisites"></a>
<!-- #### Other Driver Prerequisites -->
#### Other Driver Prerequisites

<!-- The following dependencies are needed for the listed queue drivers. These dependencies may be installed via the Composer package manager: -->
아래의 큐 드라이버를 사용할 때는 각각의 추가 패키지가 필요합니다. 이 의존성 패키지들은 Composer 패키지 매니저로 설치할 수 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` or phpredis PHP extension
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`
-->
- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<!-- </div> -->
</div>

<a name="creating-jobs"></a>
<!-- ## Creating Jobs -->
## Creating Jobs

<a name="generating-job-classes"></a>
<!-- ### Generating Job Classes -->
### Generating Job Classes

<!-- By default, all of the queueable jobs for your application are stored in the `app/Jobs` directory. If the `app/Jobs` directory doesn't exist, it will be created when you run the `make:job` Artisan command: -->
기본적으로 애플리케이션의 모든 큐에 넣을 수 있는 잡 클래스는 `app/Jobs` 디렉터리에 저장됩니다. 만약 `app/Jobs` 디렉터리가 없다면, `make:job` 아티즌 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

<!-- The generated class will implement the `Illuminate\Contracts\Queue\ShouldQueue` interface, indicating to Laravel that the job should be pushed onto the queue to run asynchronously. -->
생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이는 Laravel에 해당 잡이 비동기적으로 큐에 쌓여 실행되어야 함을 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [stub publishing](/docs/11.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
<!-- ### Class Structure -->
### Class Structure

<!-- Job classes are very simple, normally containing only a `handle` method that is invoked when the job is processed by the queue. To get started, let's take a look at an example job class. In this example, we'll pretend we manage a podcast publishing service and need to process the uploaded podcast files before they are published: -->
잡 클래스는 매우 단순하며, 일반적으로 큐에서 잡을 처리할 때 호출되는 `handle` 메서드만 포함되어 있습니다. 예를 들어, 팟캐스트 발행 서비스를 운영하면서 업로드된 팟캐스트 파일을 게시 전에 처리해야 하는 상황을 살펴봅시다.

```
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

<!-- In this example, note that we were able to pass an [Eloquent model](/docs/11.x/eloquent) directly into the queued job's constructor. Because of the `Queueable` trait that the job is using, Eloquent models and their loaded relationships will be gracefully serialized and unserialized when the job is processing. -->
위 예제에서 알 수 있듯, 우리는 [Eloquent model](/docs/11.x/eloquent) 인스턴스를 잡 생성자에 직접 전달할 수 있습니다. 잡에 `Queueable` 트레이트를 사용하면 모델과 연관된 로드된 관계까지도 직렬화/역직렬화가 안전하게 처리됩니다.

<!-- If your queued job accepts an Eloquent model in its constructor, only the identifier for the model will be serialized onto the queue. When the job is actually handled, the queue system will automatically re-retrieve the full model instance and its loaded relationships from the database. This approach to model serialization allows for much smaller job payloads to be sent to your queue driver. -->
잡 생성자에서 Eloquent 모델을 받으면 큐에는 해당 모델의 식별자만 저장됩니다. 실제로 잡이 처리될 때 큐 시스템이 자동으로 전체 모델 인스턴스와 그에 로드된 관계 데이터를 데이터베이스에서 다시 가져옵니다. 이런 방식의 모델 직렬화 덕분에 큐에 전달되는 잡 데이터 크기가 훨씬 작아집니다.

<a name="handle-method-dependency-injection"></a>
<!-- #### `handle` Method Dependency Injection -->
#### `handle` Method Dependency Injection

<!-- The `handle` method is invoked when the job is processed by the queue. Note that we are able to type-hint dependencies on the `handle` method of the job. The Laravel [service container](/docs/11.x/container) automatically injects these dependencies. -->
잡이 큐에서 처리될 때 `handle` 메서드가 호출됩니다. 이때 `handle` 메서드에 다양한 클래스 타입 의존성을 타입힌트로 지정할 수 있습니다. Laravel의 [service container](/docs/11.x/container)는 이 의존성을 자동으로 주입해 줍니다.

<!-- If you would like to take total control over how the container injects dependencies into the `handle` method, you may use the container's `bindMethod` method. The `bindMethod` method accepts a callback which receives the job and the container. Within the callback, you are free to invoke the `handle` method however you wish. Typically, you should call this method from the `boot` method of your `App\Providers\AppServiceProvider` [service provider](/docs/11.x/providers): -->
서비스 컨테이너의 의존성 주입 동작을 완전히 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod` 메서드는 콜백을 받아, 내부에서 잡과 컨테이너를 전달받아 원하는 방식으로 `handle` 메서드를 호출할 수 있도록 해줍니다. 일반적으로 이 설정은 `App\Providers\AppServiceProvider` [service provider](/docs/11.x/providers)의 `boot` 메서드에서 수행합니다.

```
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 이미지 원본 데이터 등)는 잡에 전달하기 전에 반드시 `base64_encode` 함수로 인코딩해야 합니다. 그렇지 않으면 잡을 큐에 저장할 때 JSON으로 정상적으로 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
<!-- #### Queued Relationships -->
#### Queued Relationships

<!-- Because all loaded Eloquent model relationships also get serialized when a job is queued, the serialized job string can sometimes become quite large. Furthermore, when a job is deserialized and model relationships are re-retrieved from the database, they will be retrieved in their entirety. Any previous relationship constraints that were applied before the model was serialized during the job queueing process will not be applied when the job is deserialized. Therefore, if you wish to work with a subset of a given relationship, you should re-constrain that relationship within your queued job. -->
큐에 저장되는 잡은 직렬화할 때 Eloquent 모델에 로드된 모든 관계도 함께 직렬화됩니다. 그래서 직렬화된 잡 데이터 크기가 커질 수 있습니다. 또한, 잡이 역직렬화되어 실행될 때 연관된 관계를 데이터베이스에서 다시 조회하게 되는데, 이때는 큐에 들어가기 전 모델에 적용했던 관계 조건이 유지되지 않습니다. 따라서 특정 관계의 일부 데이터만 필요하다면, 잡 내에서 다시 관계 쿼리 조건을 적용해야 합니다.

<!-- Or, to prevent relations from being serialized, you can call the `withoutRelations` method on the model when setting a property value. This method will return an instance of the model without its loaded relationships: -->
또는 아예 관계 데이터가 직렬화되지 않도록, 프로퍼티 값을 설정할 때 `withoutRelations` 메서드를 사용할 수도 있습니다. 이 메서드는 로드된 모든 관계를 제외한 모델 인스턴스를 반환합니다.

```
/**
 * Create a new job instance.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

<!-- If you are using PHP constructor property promotion and would like to indicate that an Eloquent model should not have its relations serialized, you may use the `WithoutRelations` attribute: -->
만약 PHP 생성자 프로퍼티 프로모션 문법을 사용 중이라면, Eloquent 모델의 관계 직렬화를 방지하기 위해 `WithoutRelations` 속성을 사용할 수 있습니다.

```
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * Create a new job instance.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

<!-- If a job receives a collection or array of Eloquent models instead of a single model, the models within that collection will not have their relationships restored when the job is deserialized and executed. This is to prevent excessive resource usage on jobs that deal with large numbers of models. -->
잡 생성자에서 단일 모델이 아닌 컬렉션이나 배열로 모델 여러 개를 받고 있다면, 잡이 역직렬화되어 실행될 때 이들 모델 내부의 관계는 복원되지 않습니다. 이는 대규모 모델 컬렉션을 다루는 잡에서 불필요한 리소스 소모를 막기 위한 조치입니다.

<a name="unique-jobs"></a>
<!-- ### Unique Jobs -->
### Unique Jobs

> [!WARNING]
> 유니크 잡은 [locks](/docs/11.x/cache#atomic-locks) 기능을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버에서만 지원됩니다. 또한, 유니크 잡 제약은 배치 처리되는 잡에는 적용되지 않습니다.

<!-- Sometimes, you may want to ensure that only one instance of a specific job is on the queue at any point in time. You may do so by implementing the `ShouldBeUnique` interface on your job class. This interface does not require you to define any additional methods on your class: -->
특정 잡이 한 번에 큐에 여러 개 쌓이지 않도록, 특정 잡의 인스턴스가 오직 하나만 존재하도록 만들고 싶을 때가 있습니다. 이럴 때는 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드를 추가할 필요는 없습니다.

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
위 예제에서처럼, `UpdateSearchIndex` 잡이 유니크로 지정되면, 동일한 잡이 큐에 이미 있거나 처리 중일 경우 추가로 디스패치되지 않습니다.

<!-- In certain cases, you may want to define a specific "key" that makes the job unique or you may want to specify a timeout beyond which the job no longer stays unique. To accomplish this, you may define `uniqueId` and `uniqueFor` properties or methods on your job class: -->
상황에 따라 잡의 유니크함을 결정하는 고유 "키"를 지정하거나, 유니크 상태 유지 시간(타임아웃)을 따로 지정할 수도 있습니다. 이를 위해 잡 클래스에 `uniqueId` 및 `uniqueFor` 프로퍼티/메서드를 정의하면 됩니다.

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
     * Get the unique ID for the job.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

<!-- In the example above, the `UpdateSearchIndex` job is unique by a product ID. So, any new dispatches of the job with the same product ID will be ignored until the existing job has completed processing. In addition, if the existing job is not processed within one hour, the unique lock will be released and another job with the same unique key can be dispatched to the queue. -->
이 예시에서는, `UpdateSearchIndex` 잡이 상품 ID 단위로 유니크하게 동작합니다. 즉, 동일한 상품 ID로 새로운 잡이 디스패치되더라도 기존 잡이 처리 완료 전에는 무시됩니다. 또, 한 시간(3600초) 내에 기존 잡이 처리되지 못하면 락이 해제되고 동일한 키의 새로운 잡을 큐에 넣을 수 있습니다.

> [!WARNING]
> 여러 웹서버나 컨테이너에서 잡을 디스패치할 경우, 모든 서버가 동일한 중앙 캐시 서버와 연결되어 있어야 Laravel이 유니크 잡 여부를 정확히 판별할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
<!-- #### Keeping Jobs Unique Until Processing Begins -->
#### Keeping Jobs Unique Until Processing Begins

<!-- By default, unique jobs are "unlocked" after a job completes processing or fails all of its retry attempts. However, there may be situations where you would like your job to unlock immediately before it is processed. To accomplish this, your job should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract: -->
기본적으로, 유니크 잡은 처리 완료되거나 모든 재시도 횟수 초과 시 "언락"됩니다. 그러나 잡이 실제로 처리되기 직전에 바로 언락하고 싶을 수도 있습니다. 이런 경우에는 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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

<!-- Behind the scenes, when a `ShouldBeUnique` job is dispatched, Laravel attempts to acquire a [lock](/docs/11.x/cache#atomic-locks) with the `uniqueId` key. If the lock is not acquired, the job is not dispatched. This lock is released when the job completes processing or fails all of its retry attempts. By default, Laravel will use the default cache driver to obtain this lock. However, if you wish to use another driver for acquiring the lock, you may define a `uniqueVia` method that returns the cache driver that should be used: -->
내부적으로 `ShouldBeUnique` 잡이 디스패치될 때, Laravel은 `uniqueId` 키로 [lock](/docs/11.x/cache#atomic-locks)을 시도합니다. 락 획득에 실패하면 잡이 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도를 소진하면 해제됩니다. 기본적으로 Laravel은 기본 캐시 드라이버를 활용해 이 락을 관리합니다. 만약 다른 캐시 드라이버를 사용하고 싶다면, 잡 클래스에 `uniqueVia` 메서드를 정의하여 반환값으로 사용할 캐시 드라이버를 지정할 수 있습니다.

```
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
```

> [!NOTE]
> 단순히 잡의 동시 실행을 제한하고 싶을 경우, [`WithoutOverlapping`](/docs/11.x/queues#preventing-job-overlaps) 잡 미들웨어 사용을 권장합니다.

<a name="encrypted-jobs"></a>
<!-- ### Encrypted Jobs -->
### Encrypted Jobs

<!-- Laravel allows you to ensure the privacy and integrity of a job's data via [encryption](/docs/11.x/encryption). To get started, simply add the `ShouldBeEncrypted` interface to the job class. Once this interface has been added to the class, Laravel will automatically encrypt your job before pushing it onto a queue: -->
Laravel은 잡 데이터의 프라이버시와 무결성을 [encryption](/docs/11.x/encryption)를 통해 보장할 수 있습니다. 사용 방법은 매우 간단하게, 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스를 추가한 순간부터 Laravel이 해당 잡을 큐에 푸시하기 전 자동으로 암호화합니다.

```
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
잡 미들웨어를 사용하면 큐에 담긴 잡 실행 전후에 원하는 커스텀 로직을 쉽게 감쌀 수 있어, 각 잡 클래스 내부의 반복적인 코드 작성을 크게 줄일 수 있습니다. 예를 들어, Laravel의 Redis 속도 제한(rate limiting) 기능을 활용해 5초마다 1개 잡만 처리되도록 하는 아래와 같은 `handle` 메서드를 생각해 봅시다.

```
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

<!-- While this code is valid, the implementation of the `handle` method becomes noisy since it is cluttered with Redis rate limiting logic. In addition, this rate limiting logic must be duplicated for any other jobs that we want to rate limit. -->
이 코드는 유효하지만, `handle` 메서드에 Redis 속도 제한 로직이 뒤섞여 있어 잡 로직이 복잡해 보일 수 있습니다. 또한, 여러 잡에서 똑같은 속도 제한 로직을 반복해야 할 수도 있습니다.

<!-- Instead of rate limiting in the handle method, we could define a job middleware that handles rate limiting. Laravel does not have a default location for job middleware, so you are welcome to place job middleware anywhere in your application. In this example, we will place the middleware in an `app/Jobs/Middleware` directory: -->
이런 경우 `handle` 메서드에서 직접 속도 제한을 구현하기보다, 별도의 잡 미들웨어로 분리해 관리하는 것이 훨씬 낫습니다. Laravel은 잡 미들웨어 위치를 따로 정하지 않았으니, 프로젝트 내부 원하는 곳에 두어도 무방합니다. 예를 들어 `app/Jobs/Middleware` 디렉터리에 미들웨어 클래스를 둘 수 있습니다.

```
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

<!-- As you can see, like [route middleware](/docs/11.x/middleware), job middleware receive the job being processed and a callback that should be invoked to continue processing the job. -->
[route middleware](/docs/11.x/middleware)와 마찬가지로, 잡 미들웨어는 현재 처리 중인 잡과 후속 처리를 위한 콜백을 인자로 받습니다.

<!-- After creating job middleware, they may be attached to a job by returning them from the job's `middleware` method. This method does not exist on jobs scaffolded by the `make:job` Artisan command, so you will need to manually add it to your job class: -->
잡 미들웨어를 만든 뒤에는, 잡 클래스의 `middleware` 메서드에서 해당 미들웨어를 반환하면 적용할 수 있습니다. 이 메서드는 `make:job` 명령어로 생성된 잡 클래스에는 기본적으로 없으니, 수동으로 추가해야 합니다.

```
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
> 잡 미들웨어는 큐에 넣을 수 있는 이벤트 리스너, 메일러블, 알림(notification)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
<!-- ### Rate Limiting -->
### Rate Limiting

<!-- Although we just demonstrated how to write your own rate limiting job middleware, Laravel actually includes a rate limiting middleware that you may utilize to rate limit jobs. Like [route rate limiters](/docs/11.x/routing#defining-rate-limiters), job rate limiters are defined using the `RateLimiter` facade's `for` method. -->
방금 예제처럼 직접 속도 제한 미들웨어를 작성할 수도 있지만, Laravel에는 이미 잡 속도 제한을 위한 미들웨어가 내장되어 있습니다. [route rate limiters](/docs/11.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

<!-- For example, you may wish to allow users to backup their data once per hour while imposing no such limit on premium customers. To accomplish this, you may define a `RateLimiter` in the `boot` method of your `AppServiceProvider`: -->
예를 들어, 사용자가 1시간에 한 번씩만 백업하도록 제한하고, 프리미엄 고객에게는 제한을 두지 않으려면, `AppServiceProvider`의 `boot` 메서드에서 아래와 같이 `RateLimiter`를 정의할 수 있습니다.

```
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
위 예제는 시간 단위 제한이지만, `perMinute` 메서드를 사용해 분 단위 제한도 쉽게 설정할 수 있습니다. `by` 메서드에는 아무 값이나 전달할 수 있는데, 일반적으로 고객별로 속도 제한을 구분할 때 자주 활용합니다.

```
return Limit::perMinute(50)->by($job->user->id);
```

<!-- Once you have defined your rate limit, you may attach the rate limiter to your job using the `Illuminate\Queue\Middleware\RateLimited` middleware. Each time the job exceeds the rate limit, this middleware will release the job back to the queue with an appropriate delay based on the rate limit duration. -->
속도 제한자를 정의했다면, 이제 해당 잡에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 붙여 적용할 수 있습니다. 잡이 속도 제한을 초과할 때마다, 이 미들웨어는 정해진 제한 시간만큼 딜레이를 두고 잡을 다시 큐에 반환합니다.

```
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

<!-- Releasing a rate limited job back onto the queue will still increment the job's total number of `attempts`. You may wish to tune your `tries` and `maxExceptions` properties on your job class accordingly. Or, you may wish to use the [`retryUntil` method](#time-based-attempts) to define the amount of time until the job should no longer be attempted. -->
이처럼 속도 제한으로 인해 잡이 큐에 다시 반환될 때도 잡의 전체 `attempts` 횟수는 증가합니다. 필요하다면 잡 클래스의 `tries` 및 `maxExceptions` 프로퍼티, 혹은 [`retryUntil` method](#time-based-attempts)를 적절히 조정해야 할 수도 있습니다.

<!-- If you do not want a job to be retried when it is rate limited, you may use the `dontRelease` method: -->
속도 제한 때문에 잡을 아예 다시 시도하지 않게 하고 싶다면 `dontRelease` 메서드를 사용하면 됩니다.

```
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

> [!NOTE]
> Redis를 사용할 경우, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어도 사용할 수 있습니다. 이 미들웨어는 Redis에 최적화되어 있으며, 기본 속도 제한 미들웨어보다 더 효율적입니다.

<a name="preventing-job-overlaps"></a>
<!-- ### Preventing Job Overlaps -->
### Preventing Job Overlaps

<!-- Laravel includes an `Illuminate\Queue\Middleware\WithoutOverlapping` middleware that allows you to prevent job overlaps based on an arbitrary key. This can be helpful when a queued job is modifying a resource that should only be modified by one job at a time. -->
Laravel에는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있어, 임의의 키 값을 기준으로 잡의 중복 실행을 막을 수 있습니다. 예를 들어 한 번에 한 잡만 특정 리소스를 수정해야 할 때 유용합니다.

<!-- For example, let's imagine you have a queued job that updates a user's credit score and you want to prevent credit score update job overlaps for the same user ID. To accomplish this, you can return the `WithoutOverlapping` middleware from your job's `middleware` method: -->
예를 들어, 사용자의 신용 점수를 갱신하는 잡의 중복 실행을 같은 사용자 ID 기준으로 막고 싶다면, 잡의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 아래처럼 추가할 수 있습니다.

```
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

<!-- Any overlapping jobs of the same type will be released back to the queue. You may also specify the number of seconds that must elapse before the released job will be attempted again: -->
동일한 종류의 중첩 잡은 다시 큐로 반환됩니다. 반환된 뒤 얼마 뒤에 재시도할지 초 단위로 지정할 수도 있습니다.

```
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
중복 잡을 다시 시도하지 않고 즉시 삭제하려면 `dontRelease` 메서드를 사용할 수 있습니다.

```
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
`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락(atomic lock) 기능을 기반으로 동작합니다. 잡이 예기치 않게 실패하거나 타임아웃 나는 경우 락이 해제되지 않을 수 있으므로, `expireAfter` 메서드로 명시적으로 락 만료 시간을 지정하는 것이 좋습니다. 예를 들어 아래 예시는 잡 실행 시작 3분(180초) 후에 `WithoutOverlapping` 락이 자동 해제되도록 합니다.

```
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
> `WithoutOverlapping` 미들웨어를 사용하려면 [locks](/docs/11.x/cache#atomic-locks) 기능을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버만이 원자적 락을 사용할 수 있습니다.

<a name="sharing-lock-keys"></a>

<!-- #### Sharing Lock Keys Across Job Classes -->
#### Sharing Lock Keys Across Job Classes

<!-- By default, the `WithoutOverlapping` middleware will only prevent overlapping jobs of the same class. So, although two different job classes may use the same lock key, they will not be prevented from overlapping. However, you can instruct Laravel to apply the key across job classes using the `shared` method: -->
기본적으로, `WithoutOverlapping` 미들웨어는 동일한 클래스의 중첩 실행만 방지합니다. 즉, 서로 다른 두 잡 클래스가 같은 lock key를 사용하더라도 중첩 실행이 막히지 않습니다. 하지만, `shared` 메서드를 사용하여 Laravel이 이 key를 여러 잡 클래스에 걸쳐 적용하도록 지시할 수 있습니다.

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
Laravel에는 예외 발생 횟수를 제한할 수 있도록 해주는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 포함되어 있습니다. 잡이 정해진 횟수만큼 예외를 발생시키면, 지정한 시간 간격이 경과할 때까지 해당 잡의 추가 실행 시도가 지연됩니다. 이 미들웨어는 특히 외부 서비스 등 불안정한 시스템과 상호작용하는 잡에서 유용하게 사용됩니다.

<!-- For example, let's imagine a queued job that interacts with a third-party API that begins throwing exceptions. To throttle exceptions, you can return the `ThrottlesExceptions` middleware from your job's `middleware` method. Typically, this middleware should be paired with a job that implements [time based attempts](#time-based-attempts): -->
예를 들어, 외부 API와 상호작용하는 큐 잡이 있지만 예외가 반복적으로 발생한다고 가정해 보겠습니다. 예외를 제한하려면 잡의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 일반적으로 이 미들웨어는 [time based attempts](#time-based-attempts)가 구현된 잡과 함께 사용하면 좋습니다.

```
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
```

<!-- The first constructor argument accepted by the middleware is the number of exceptions the job can throw before being throttled, while the second constructor argument is the number of seconds that should elapse before the job is attempted again once it has been throttled. In the code example above, if the job throws 10 consecutive exceptions, we will wait 5 minutes before attempting the job again, constrained by the 30-minute time limit. -->
이 미들웨어의 첫 번째 생성자 인자는 예외가 얼마만큼 연속해서 발생할 경우 제한(throttling)을 시작할지를, 두 번째 인자는 제한이 시작된 뒤 잡을 다시 시도하기 전에 대기해야 하는 시간(초 단위)입니다. 위의 예제에서는, 잡이 10번 연속 예외를 던지면 5분 동안 대기한 뒤, 최대 30분이라는 시간 제한 내에서만 다시 시도합니다.

<!-- When a job throws an exception but the exception threshold has not yet been reached, the job will typically be retried immediately. However, you may specify the number of minutes such a job should be delayed by calling the `backoff` method when attaching the middleware to the job: -->
잡이 예외를 발생시켰으나 아직 제한(throttling) 임계치에 도달하지 않았다면, 보통 즉시 다시 시도하게 됩니다. 그러나 미들웨어에 `backoff` 메서드를 호출해 잡이 다시 시도되기 전 몇 분 동안 지연시킬지 지정할 수 있습니다.

```
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

<!-- Internally, this middleware uses Laravel's cache system to implement rate limiting, and the job's class name is utilized as the cache "key". You may override this key by calling the `by` method when attaching the middleware to your job. This may be useful if you have multiple jobs interacting with the same third-party service and you would like them to share a common throttling "bucket": -->
이 미들웨어는 내부적으로 Laravel의 캐시 시스템을 활용하여 제한 기능을 구현하며, 잡의 클래스명이 캐시 "key"로 사용됩니다. 만약 여러 잡이 동일한 외부 서비스를 사용할 경우, 캐시 key를 공유하여 예외 제한 "버킷"을 공유하도록 `by` 메서드로 key를 지정할 수 있습니다.

```
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

<!-- By default, this middleware will throttle every exception. You can modify this behaviour by invoking the `when` method when attaching the middleware to your job. The exception will then only be throttled if closure provided to the `when` method returns `true`: -->
기본적으로 이 미들웨어는 발생하는 모든 예외를 제한합니다. `when` 메서드를 이용하여 미들웨어를 잡에 부착할 때 조건을 지정하면, `when` 메서드에 지정한 클로저 함수가 `true`를 반환하는 경우에만 예외 제한이 적용되도록 동작을 변경할 수 있습니다.

```
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

<!-- If you would like to have the throttled exceptions reported to your application's exception handler, you can do so by invoking the `report` method when attaching the middleware to your job. Optionally, you may provide a closure to the `report` method and the exception will only be reported if the given closure returns `true`: -->
또한 제한된 예외를 애플리케이션의 예외 핸들러에 보고하도록 하고 싶다면, `report` 메서드를 미들웨어에 연결하면 됩니다. 옵션으로 `report` 메서드에 클로저를 전달할 수 있는데, 이 클로저가 `true`를 반환하는 경우에만 예외가 보고됩니다.

```
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

> [!NOTE]
> Redis를 사용하는 경우, 더 효율적으로 동작하도록 튜닝된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 기본 예외 제한 미들웨어보다 Redis 환경에 최적화되어 있습니다.

<a name="skipping-jobs"></a>
<!-- ### Skipping Jobs -->
### Skipping Jobs

<!-- The `Skip` middleware allows you to specify that a job should be skipped / deleted without needing to modify the job's logic. The `Skip::when` method will delete the job if the given condition evaluates to `true`, while the `Skip::unless` method will delete the job if the condition evaluates to `false`: -->
`Skip` 미들웨어를 사용하면 잡 로직을 수정하지 않고도 잡을 스킵(건너뛰기) 또는 삭제하도록 지정할 수 있습니다. `Skip::when` 메서드는 전달된 조건이 `true`가 되면 잡을 삭제하고, `Skip::unless` 메서드는 조건이 `false`가 되면 잡을 삭제합니다.

```
use Illuminate\Queue\Middleware\Skip;

/**
* Get the middleware the job should pass through.
*/
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

<!-- You can also pass a `Closure` to the `when` and `unless` methods for more complex conditional evaluation: -->
더 복잡한 조건식을 위해서는 `when`과 `unless` 메서드에 `Closure`를 전달할 수도 있습니다.

```
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
잡 클래스를 작성했다면, 해당 잡 클래스에서 `dispatch` 메서드를 이용해 잡을 큐에 보낼 수 있습니다. 이때 `dispatch`에 전달된 인수는 잡 생성자에 그대로 전달됩니다.

```
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
```

<!-- If you would like to conditionally dispatch a job, you may use the `dispatchIf` and `dispatchUnless` methods: -->
만약 조건에 따라 잡을 디스패치하고 싶다면, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

<!-- In new Laravel applications, the `sync` driver is the default queue driver. This driver executes jobs synchronously in the foreground of the current request, which is often convenient during local development. If you would like to actually begin queueing jobs for background processing, you may specify a different queue driver within your application's `config/queue.php` configuration file. -->
새로운 Laravel 애플리케이션에서는 기본 큐 드라이버가 `sync`로 설정되어 있습니다. 이 드라이버는 현재 요청의 포그라운드에서 잡을 동기적으로(즉시) 실행하므로, 로컬 개발 환경에서 매우 편리합니다. 잡을 백그라운드로 실제 큐잉하여 처리하려면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정해야 합니다.

<a name="delayed-dispatching"></a>
<!-- ### Delayed Dispatching -->
### Delayed Dispatching

<!-- If you would like to specify that a job should not be immediately available for processing by a queue worker, you may use the `delay` method when dispatching the job. For example, let's specify that a job should not be available for processing until 10 minutes after it has been dispatched: -->
잡을 즉시 처리하지 않고 일정 시간 후에만 큐 워커가 처리 가능하도록 하려면, 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 잡이 디스패치된 후 10분이 지난 뒤에만 처리하도록 하려면 다음과 같이 작성합니다.

```
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
```

<!-- In some cases, jobs may have a default delay configured. If you need to bypass this delay and dispatch a job for immediate processing, you may use the `withoutDelay` method: -->
경우에 따라, 잡에 기본 지연(delay)이 설정되어 있을 수도 있습니다. 이 기본 지연을 무시하고 즉시 잡을 디스패치하려면, `withoutDelay` 메서드를 사용하시면 됩니다.

```
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 시간이 15분으로 제한되어 있습니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
<!-- #### Dispatching After the Response is Sent to the Browser -->
#### Dispatching After the Response is Sent to the Browser

<!-- Alternatively, the `dispatchAfterResponse` method delays dispatching a job until after the HTTP response is sent to the user's browser if your web server is using FastCGI. This will still allow the user to begin using the application even though a queued job is still executing. This should typically only be used for jobs that take about a second, such as sending an email. Since they are processed within the current HTTP request, jobs dispatched in this fashion do not require a queue worker to be running in order for them to be processed: -->
`dispatchAfterResponse` 메서드는 웹 서버가 FastCGI를 사용하는 경우, HTTP 응답이 사용자의 브라우저에 전송된 후에 잡을 디스패치하도록 지연시킬 수 있습니다. 이를 통해 사용자가 애플리케이션을 바로 사용할 수 있도록 하고, 잡은 그 뒤에 실행됩니다. 일반적으로 1초 이내에 끝나는 짧은 잡(예: 메일 발송)에만 사용하는 것이 좋습니다. 이 방식을 사용할 때는 별도의 큐 워커가 실행 중이지 않아도 현재 HTTP 요청 내에서 잡 처리가 완료됩니다.

```
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

<!-- You may also `dispatch` a closure and chain the `afterResponse` method onto the `dispatch` helper to execute a closure after the HTTP response has been sent to the browser: -->
또한, 클로저 자체를 `dispatch`할 수도 있으며, `dispatch` 헬퍼에 `afterResponse` 메서드를 체인으로 연결하여 응답이 전송된 뒤에 클로저가 실행되도록 만들 수도 있습니다.

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
잡을 즉시(동기적으로) 실행하고 싶다면, `dispatchSync` 메서드를 사용할 수 있습니다. 이 메서드를 사용하면 잡이 큐에 저장되지 않고 바로 현재 프로세스 내에서 실행됩니다.

```
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
```

<a name="jobs-and-database-transactions"></a>
<!-- ### Jobs & Database Transactions -->
### Jobs & Database Transactions

<!-- While it is perfectly fine to dispatch jobs within database transactions, you should take special care to ensure that your job will actually be able to execute successfully. When dispatching a job within a transaction, it is possible that the job will be processed by a worker before the parent transaction has committed. When this happens, any updates you have made to models or database records during the database transaction(s) may not yet be reflected in the database. In addition, any models or database records created within the transaction(s) may not exist in the database. -->
데이터베이스 트랜잭션 내에서 잡을 디스패치하는 것은 문제되지 않습니다. 하지만 잡이 실제로 정상적으로 실행될 수 있도록 주의해야 합니다. 트랜잭션 내에서 잡을 디스패치하면, 잡이 부모 트랜잭션이 커밋되기 전에 워커에 의해 처리될 수 있습니다. 이런 경우, 트랜잭션 도중에 변경한 모델이나 데이터베이스 레코드가 실제 데이터베이스에 반영되지 않았을 수도 있습니다. 또한, 트랜잭션 내에서 생성된 모델이나 레코드가 아직 데이터베이스에 존재하지 않을 수도 있습니다.

<!-- Thankfully, Laravel provides several methods of working around this problem. First, you may set the `after_commit` connection option in your queue connection's configuration array: -->
다행히 Laravel에서는 이 문제를 해결할 수 있는 방법을 몇 가지 제공합니다. 먼저, 큐 커넥션 설정 배열에서 `after_commit` 옵션을 설정할 수 있습니다.

```
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

<!-- When the `after_commit` option is `true`, you may dispatch jobs within database transactions; however, Laravel will wait until the open parent database transactions have been committed before actually dispatching the job. Of course, if no database transactions are currently open, the job will be dispatched immediately. -->
`after_commit` 옵션이 `true`로 되어 있으면, 트랜잭션 내에서 잡을 디스패치해도 부모 데이터베이스 트랜잭션이 모두 커밋된 후에 실제로 잡이 디스패치됩니다. 만약 현재 열린 트랜잭션이 없다면, 잡은 즉시 디스패치됩니다.

<!-- If a transaction is rolled back due to an exception that occurs during the transaction, the jobs that were dispatched during that transaction will be discarded. -->
트랜잭션 도중 예외가 발생하여 롤백되는 경우, 해당 트랜잭션 내에서 디스패치된 잡은 모두 삭제됩니다.

> [!NOTE]
> `after_commit` 옵션을 `true`로 설정하면, 모든 큐 기반 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트도 모든 데이터베이스 트랜잭션 커밋이 완료된 후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
<!-- #### Specifying Commit Dispatch Behavior Inline -->
#### Specifying Commit Dispatch Behavior Inline

<!-- If you do not set the `after_commit` queue connection configuration option to `true`, you may still indicate that a specific job should be dispatched after all open database transactions have been committed. To accomplish this, you may chain the `afterCommit` method onto your dispatch operation: -->
`after_commit` 큐 커넥션 옵션을 `true`로 설정하지 않더라도, 특정 잡만 모든 열린 데이터베이스 트랜잭션이 커밋된 후 디스패치되도록 지정할 수 있습니다. 이때는 디스패치 시 `afterCommit` 메서드를 체인으로 연결하면 됩니다.

```
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

<!-- Likewise, if the `after_commit` configuration option is set to `true`, you may indicate that a specific job should be dispatched immediately without waiting for any open database transactions to commit: -->
마찬가지로, `after_commit` 설정 옵션이 `true`로 설정되어 있더라도, 특정 잡만 열린 데이터베이스 트랜잭션이 커밋되기를 기다리지 않고 즉시 디스패치되도록 지정할 수 있습니다.

```
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
<!-- ### Job Chaining -->
### Job Chaining

<!-- Job chaining allows you to specify a list of queued jobs that should be run in sequence after the primary job has executed successfully. If one job in the sequence fails, the rest of the jobs will not be run. To execute a queued job chain, you may use the `chain` method provided by the `Bus` facade. Laravel's command bus is a lower level component that queued job dispatching is built on top of: -->
잡 체이닝을 사용하면, 하나의 주 잡(primary job)이 성공적으로 실행된 후 연속해서 실행되어야 하는 잡들의 목록을 지정할 수 있습니다. 체인 내의 잡 중 하나라도 실패하면, 나머지 잡은 실행되지 않습니다. 잡 체인을 실행하려면 `Bus` 파사드에서 제공하는 `chain` 메서드를 사용하면 됩니다. Laravel의 커맨드 버스(command bus)는 잡 큐잉의 기반이 되는 하위 레벨 컴포넌트입니다.

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
잡 클래스 인스턴스 뿐 아니라, 클로저도 체인에 포함할 수 있습니다.

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
> 잡 내에서 `$this->delete()` 메서드로 잡을 삭제해도, 연결된 체인 잡의 실행은 막을 수 없습니다. 체인의 다음 잡 실행은 체인 내의 잡이 실패한 경우에만 중단됩니다.

<a name="chain-connection-queue"></a>
<!-- #### Chain Connection and Queue -->
#### Chain Connection and Queue

<!-- If you would like to specify the connection and queue that should be used for the chained jobs, you may use the `onConnection` and `onQueue` methods. These methods specify the queue connection and queue name that should be used unless the queued job is explicitly assigned a different connection / queue: -->
체인으로 연결된 잡들에 사용할 큐 커넥션(connection)과 큐 이름(queue)을 지정하고 싶다면, 각각 `onConnection`과 `onQueue` 메서드를 사용하면 됩니다. 이 메서드로 지정한 값이 잡의 커넥션/큐 관련 별도 설정이 없는 한 기본값으로 적용됩니다.

```
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
때로는 체인 내의 잡 처리 중, 현재 체인에 잡을 앞에(prepend) 또는 뒤에(append) 추가해야 할 수도 있습니다. 이럴 때는 `prependToChain`와 `appendToChain` 메서드를 사용할 수 있습니다.

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
잡 체인이 실행되다가 특정 잡에서 실패가 발생할 경우 실행할 클로저를 `catch` 메서드로 지정할 수 있습니다. 이 콜백은 잡 실패를 일으킨 `Throwable` 인스턴스를 전달받습니다.

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
> 체인 콜백은 직렬화(serialized)되어 나중에 큐에서 실행되기 때문에, 콜백 내에서 `$this` 변수를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
<!-- ### Customizing the Queue and Connection -->
### Customizing the Queue and Connection

<a name="dispatching-to-a-particular-queue"></a>
<!-- #### Dispatching to a Particular Queue -->
#### Dispatching to a Particular Queue

<!-- By pushing jobs to different queues, you may "categorize" your queued jobs and even prioritize how many workers you assign to various queues. Keep in mind, this does not push jobs to different queue "connections" as defined by your queue configuration file, but only to specific queues within a single connection. To specify the queue, use the `onQueue` method when dispatching the job: -->
잡을 서로 다른 큐로 보내면 잡을 "카테고리"별로 관리할 수 있을 뿐 아니라, 각각의 큐에 워커를 얼마나 할당할지 우선순위를 지정할 수 있습니다. (이 방식은 큐 설정 파일에 정의된 큐 "커넥션" 단위가 아니라, 하나의 커넥션 내부의 여러 큐 단위로만 동작함을 유의하세요.) 잡을 특정 큐로 보내려면, 디스패치 시 `onQueue` 메서드를 사용하면 됩니다.

```
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
```

<!-- Alternatively, you may specify the job's queue by calling the `onQueue` method within the job's constructor: -->
또 다른 방법으로, 잡 생성자 안에서 `onQueue`를 호출해 잡의 큐 이름을 지정할 수도 있습니다.

```
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
애플리케이션이 여러 큐 커넥션을 사용할 경우, `onConnection` 메서드를 사용해서 잡을 보낼 커넥션을 지정할 수 있습니다.

```
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
```

<!-- You may chain the `onConnection` and `onQueue` methods together to specify the connection and the queue for a job: -->
`onConnection`과 `onQueue`를 체인 형태로 연결해서 큐 커넥션과 큐 이름을 같이 지정할 수도 있습니다.

```
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

<!-- Alternatively, you may specify the job's connection by calling the `onConnection` method within the job's constructor: -->
또는, 잡 생성자 안에서 `onConnection`을 호출해 잡의 커넥션을 설정할 수도 있습니다.

```
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

<a name="max-job-attempts-and-timeout"></a>

<!-- ### Specifying Max Job Attempts / Timeout Values -->
### Specifying Max Job Attempts / Timeout Values

<a name="max-attempts"></a>
<!-- #### Max Attempts -->
#### Max Attempts

<!-- If one of your queued jobs is encountering an error, you likely do not want it to keep retrying indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a job may be attempted. -->
큐에 등록된 작업 중 하나에서 오류가 발생한다면, 무한정 재시도를 계속하도록 두고 싶진 않을 것입니다. Laravel에서는 작업이 시도되는 횟수나 기간을 지정하는 다양한 방법을 제공합니다.

<!-- One approach to specifying the maximum number of times a job may be attempted is via the `--tries` switch on the Artisan command line. This will apply to all jobs processed by the worker unless the job being processed specifies the number of times it may be attempted: -->
가장 간단히, 아티즌 명령어의 `--tries` 옵션을 사용해 워커가 처리하는 모든 작업에 대해 최대 시도 횟수를 지정할 수 있습니다. 다만, 작업 클래스에서 별도로 시도 횟수를 지정했다면 그 값을 우선적으로 사용합니다.

```shell
php artisan queue:work --tries=3
```

<!-- If a job exceeds its maximum number of attempts, it will be considered a "failed" job. For more information on handling failed jobs, consult the [failed job documentation](#dealing-with-failed-jobs). If `--tries=0` is provided to the `queue:work` command, the job will be retried indefinitely. -->
작업이 최대 시도 횟수에 도달하면 해당 작업은 "실패(failed)"로 간주됩니다. 실패한 작업의 처리에 관한 자세한 내용은 [failed job documentation](#dealing-with-failed-jobs) 문서를 참고하십시오. 만약 `queue:work` 명령어에 `--tries=0`을 지정하면 작업은 무한정 재시도됩니다.

<!-- You may take a more granular approach by defining the maximum number of times a job may be attempted on the job class itself. If the maximum number of attempts is specified on the job, it will take precedence over the `--tries` value provided on the command line: -->
더 세밀하게, 작업 클래스 자체에서 최대 시도 횟수를 지정할 수도 있습니다. 이 경우, 해당 작업에 지정된 값이 명령줄에서 지정한 `--tries` 값보다 우선 적용됩니다.

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

<!-- If you need dynamic control over a particular job's maximum attempts, you may define a `tries` method on the job: -->
특정 작업의 최대 시도 횟수를 동적으로 제어하고 싶다면, 작업 클래스에 `tries` 메서드를 추가할 수도 있습니다.

```
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
작업이 실패 처리되기까지 몇 번이나 시도할지 대신, 언제까지 이 작업을 더 이상 재시도하지 않을지 종료 시점을 지정할 수도 있습니다. 이렇게 하면 지정한 시간 내에서는 몇 번이든 재시도할 수 있습니다. 종료 시점을 지정하려면 작업 클래스에 `retryUntil` 메서드를 추가합니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```
use DateTime;

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

> [!NOTE]
> [queued event listeners](/docs/11.x/events#queued-event-listeners)에서도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
<!-- #### Max Exceptions -->
#### Max Exceptions

<!-- Sometimes you may wish to specify that a job may be attempted many times, but should fail if the retries are triggered by a given number of unhandled exceptions (as opposed to being released by the `release` method directly). To accomplish this, you may define a `maxExceptions` property on your job class: -->
경우에 따라, 작업이 여러 번 시도되는 것은 허용하지만, 정해진 횟수만큼 처리되지 않은 예외가 발생하면 실패한 것으로 간주하고 싶을 때가 있습니다(`release` 메서드로 직접 큐에 반환된 경우는 제외). 이를 위해 작업 클래스에 `maxExceptions` 속성을 정의할 수 있습니다.

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
위 예제에서는, 애플리케이션에서 Redis 잠금을 얻지 못하면 작업이 10초 뒤에 다시 시도되도록 큐에 반환되고, 최대 25번까지 재시도됩니다. 하지만 작업에서 3번의 미처리 예외가 발생하면 해당 작업은 실패 처리됩니다.

<a name="timeout"></a>
<!-- #### Timeout -->
#### Timeout

<!-- Often, you know roughly how long you expect your queued jobs to take. For this reason, Laravel allows you to specify a "timeout" value. By default, the timeout value is 60 seconds. If a job is processing for longer than the number of seconds specified by the timeout value, the worker processing the job will exit with an error. Typically, the worker will be restarted automatically by a [process manager configured on your server](#supervisor-configuration). -->
일반적으로 큐 작업이 어느 정도 시간 내에 끝날지 예상이 가능합니다. Laravel은 이를 위해 "타임아웃" 값을 지정할 수 있도록 합니다. 기본 타임아웃은 60초입니다. 만약 작업이 지정한 초 수를 초과해 동작한다면, 작업을 처리하는 워커가 오류와 함께 종료됩니다. 대부분의 경우 [process manager configured on your server](#supervisor-configuration)에서 워커가 자동으로 재시작됩니다.

<!-- The maximum number of seconds that jobs can run may be specified using the `--timeout` switch on the Artisan command line: -->
작업이 동작할 수 있는 최대 초 단위 시간은 아티즌 명령어의 `--timeout` 옵션으로 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

<!-- If the job exceeds its maximum attempts by continually timing out, it will be marked as failed. -->
작업이 타임아웃이 반복되어 최대 시도 횟수를 초과하면, 해당 작업은 실패로 간주됩니다.

<!-- You may also define the maximum number of seconds a job should be allowed to run on the job class itself. If the timeout is specified on the job, it will take precedence over any timeout specified on the command line: -->
또한, 작업 클래스에서 직접 개별 작업의 허용 실행 시간을 지정할 수 있습니다. 작업 클래스에서 타임아웃을 지정한 경우, 명령줄에서 지정한 값보다 작업 클래스의 값이 우선 적용됩니다.

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
소켓이나 외부 HTTP 연결 등 I/O 블로킹 프로세스에서는 지정한 타임아웃이 무시될 수 있으므로, 이런 기능을 사용할 때는 각 API에서 별도의 타임아웃 값을 반드시 지정해야 합니다. 예를 들어 Guzzle을 사용할 때는 반드시 연결 및 요청에 대한 타임아웃 값을 지정하십시오.

> [!WARNING]
> 작업 타임아웃을 지정하려면 `pcntl` PHP 확장 모듈이 설치되어 있어야 합니다. 또한, 작업의 "타임아웃" 값은 항상 ["retry after"](#job-expiration) 값보다 작아야 합니다. 그렇지 않으면 작업이 실제로 완료되거나 타임아웃되기 전에 다시 시도될 수 있습니다.

<a name="failing-on-timeout"></a>
<!-- #### Failing on Timeout -->
#### Failing on Timeout

<!-- If you would like to indicate that a job should be marked as [failed](#dealing-with-failed-jobs) on timeout, you may define the `$failOnTimeout` property on the job class: -->
작업이 타임아웃되면 [failed](#dealing-with-failed-jobs)으로 표시하도록 하려면, 작업 클래스에 `$failOnTimeout` 속성을 설정하세요.

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
작업이 처리되는 도중 예외가 발생하면, 해당 작업은 자동으로 큐에 다시 반환되어 재시도됩니다. 이 작업은 최대 시도 횟수에 도달할 때까지 반복되며, 최대 시도 횟수는 `queue:work` 아티즌 명령어의 `--tries` 옵션 또는 작업 클래스의 시도 횟수 설정에 따라 결정됩니다. 큐 워커 실행에 대한 더 자세한 내용은 [can be found below](#running-the-queue-worker) 문단을 참고하세요.

<a name="manually-releasing-a-job"></a>
<!-- #### Manually Releasing a Job -->
#### Manually Releasing a Job

<!-- Sometimes you may wish to manually release a job back onto the queue so that it can be attempted again at a later time. You may accomplish this by calling the `release` method: -->
때때로 작업을 직접 큐에 다시 반환하여, 나중에 다시 시도할 수 있도록 하고 싶을 수도 있습니다. 이때는 `release` 메서드를 호출하면 됩니다.

```
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
`release` 메서드는 기본적으로 작업을 즉시 큐에 다시 반환합니다. 하지만, `release` 메서드에 정수값이나 날짜 인스턴스를 인자로 전달하여 지정한 초 수 만큼 시간이 지난 후에 처리하도록 할 수도 있습니다.

```
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
<!-- #### Manually Failing a Job -->
#### Manually Failing a Job

<!-- Occasionally you may need to manually mark a job as "failed". To do so, you may call the `fail` method: -->
가끔은 작업을 수동으로 "실패" 처리해야 할 경우가 있습니다. 이럴 땐 `fail` 메서드를 호출하면 됩니다.

```
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
예외를 직접 캐치해서 작업을 실패 처리하고 싶다면, `fail` 메서드에 예외 객체를 전달할 수 있으며, 문자열 에러 메시지를 전달하면 자동으로 예외로 변환되어 처리됩니다.

```
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 더 자세한 내용은 [documentation on dealing with job failures](#dealing-with-failed-jobs)를 확인하세요.

<a name="job-batching"></a>
<!-- ## Job Batching -->
## Job Batching

<!-- Laravel's job batching feature allows you to easily execute a batch of jobs and then perform some action when the batch of jobs has completed executing. Before getting started, you should create a database migration to build a table which will contain meta information about your job batches, such as their completion percentage. This migration may be generated using the `make:queue-batches-table` Artisan command: -->
Laravel의 작업 일괄 처리 기능을 사용하면 여러 작업을 한 번에 실행하고, 일괄 처리가 완료된 후 원하는 작업을 손쉽게 실행할 수 있습니다. 먼저, 일괄 작업의 진행률 등 메타 정보를 저장하는 테이블을 데이터베이스에 생성해야 하며, 이를 위해 `make:queue-batches-table` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
<!-- ### Defining Batchable Jobs -->
### Defining Batchable Jobs

<!-- To define a batchable job, you should [create a queueable job](#creating-jobs) as normal; however, you should add the `Illuminate\Bus\Batchable` trait to the job class. This trait provides access to a `batch` method which may be used to retrieve the current batch that the job is executing within: -->
일괄 처리가 가능한 작업을 정의하려면, [create a queueable job](#creating-jobs)과 동일하게 작업 클래스를 만들되, 클래스에 `Illuminate\Bus\Batchable` 트레이트를 추가하세요. 이 트레이트를 사용하면 `batch` 메서드를 통해 현재 작업이 소속된 일괄 처리(batch)에 접근할 수 있습니다.

```
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

<!-- To dispatch a batch of jobs, you should use the `batch` method of the `Bus` facade. Of course, batching is primarily useful when combined with completion callbacks. So, you may use the `then`, `catch`, and `finally` methods to define completion callbacks for the batch. Each of these callbacks will receive an `Illuminate\Bus\Batch` instance when they are invoked. In this example, we will imagine we are queueing a batch of jobs that each process a given number of rows from a CSV file: -->
여러 작업을 일괄 처리(batch)로 디스패치하려면, `Bus` 파사드의 `batch` 메서드를 사용하세요. 일괄 처리는 주로 작업 완료 후 실행되는 콜백과 함께 사용할 때 유용합니다. 따라서 `then`, `catch`, `finally` 메서드를 이용해 일괄 처리에 대한 완료 콜백을 정의할 수 있습니다. 각 콜백에는 `Illuminate\Bus\Batch` 인스턴스가 전달됩니다. 아래 예제는 CSV 파일의 구간별로 여러 작업을 일괄 처리(batching)하는 상황을 가정하고 있습니다.

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
```

<!-- The batch's ID, which may be accessed via the `$batch->id` property, may be used to [query the Laravel command bus](#inspecting-batches) for information about the batch after it has been dispatched. -->
`$batch->id`는 배치의 ID이며, [query the Laravel command bus](#inspecting-batches)를 통해 배치 정보를 조회할 때 사용합니다.

> [!WARNING]
> 배치 콜백은 직렬화된 후 Laravel 큐에서 나중에 실행되므로, 콜백 내에서는 `$this` 변수를 사용하면 안 됩니다. 또한, 일괄처리 작업은 데이터베이스 트랜잭션 내에서 실행되기 때문에 트랜잭션을 암묵적으로 커밋하는 데이터베이스 구문은 작업 내에서 실행하면 안 됩니다.

<a name="naming-batches"></a>
<!-- #### Naming Batches -->
#### Naming Batches

<!-- Some tools such as Laravel Horizon and Laravel Telescope may provide more user-friendly debug information for batches if batches are named. To assign an arbitrary name to a batch, you may call the `name` method while defining the batch: -->
Laravel Horizon이나 Laravel Telescope와 같은 도구에서는 배치에 이름이 있을 경우 디버깅 정보를 더 친절하게 제공합니다. 임의의 이름을 배치에 지정하려면, 배치 정의 시 `name` 메서드를 호출하세요.

```
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
배치 내 모든 작업에 적용할 큐 연결(connection) 및 큐 이름을 지정하려면, `onConnection`, `onQueue` 메서드를 사용하세요. 모든 배치 작업은 동일한 커넥션 및 큐 내에서 실행되어야 합니다.

```
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
[chained jobs](#job-chaining) 여러 개를 하나의 배치 내에 배열로 담으면 여러 체인 작업을 병렬로 실행하고, 두 체인이 모두 완료되었을 때 콜백을 실행할 수 있습니다.

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

<!-- Conversely, you may run batches of jobs within a [chain](#job-chaining) by defining batches within the chain. For example, you could first run a batch of jobs to release multiple podcasts then a batch of jobs to send the release notifications: -->
반대로, [chain](#job-chaining) 내에 여러 개의 배치를 넣어서 순차적으로 실행할 수도 있습니다. 예를 들어, 여러 팟캐스트를 먼저 배치로 공개한 다음, 각 공개 알림을 발송하는 일괄 작업을 체인으로 실행할 수 있습니다.

```
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
경우에 따라, 일괄 처리 중인 작업 내에서 추가 작업을 같은 배치에 동적으로 등록할 필요가 있습니다. 이를 활용하면 수천 개의 작업을 웹 요청 중에 한 번에 처리하는 대신, "로더" 작업을 먼저 일괄로 디스패치하고, 그 작업이 추가 작업을 동일 배치에 주입하는 방식이 가능합니다.

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
위 예제에서 `LoadImportBatch` 작업 안에서 추가 작업을 해당 배치에 주입합니다. 이를 위해서는 작업의 `batch` 메서드로 획득한 배치 인스턴스에서 `add` 메서드를 사용하면 됩니다.

```
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
> 동적으로 추가할 작업은 반드시 같은 배치에 속해 있는 작업 내에서만 추가할 수 있습니다.

<a name="inspecting-batches"></a>
<!-- ### Inspecting Batches -->
### Inspecting Batches

<!-- The `Illuminate\Bus\Batch` instance that is provided to batch completion callbacks has a variety of properties and methods to assist you in interacting with and inspecting a given batch of jobs: -->
배치 완료 콜백에서 전달받은 `Illuminate\Bus\Batch` 인스턴스는 다양한 속성과 메서드로 해당 배치에 대한 정보를 조회하고 상호작용할 수 있도록 도와줍니다.

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
`Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 애플리케이션의 라우트에서 직접 반환하면 배치의 진행률 등 정보를 포함한 JSON 응답을 받을 수 있습니다. 이를 활용하면 UI에 배치 진행 정보를 쉽게 표시할 수 있습니다.

<!-- To retrieve a batch by its ID, you may use the `Bus` facade's `findBatch` method: -->
배치 ID로 배치를 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용하세요.

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
특정 배치의 실행을 취소해야 할 때는, `Illuminate\Bus\Batch` 인스턴스에서 `cancel` 메서드를 호출하면 됩니다.

```
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
```

<!-- As you may have noticed in the previous examples, batched jobs should typically determine if their corresponding batch has been cancelled before continuing execution. However, for convenience, you may assign the `SkipIfBatchCancelled` [middleware](#job-middleware) to the job instead. As its name indicates, this middleware will instruct Laravel to not process the job if its corresponding batch has been cancelled: -->
앞선 예제들에서 볼 수 있듯, 일반적으로 일괄 처리 작업에서는 실행 중인 배치가 취소되었는지 확인한 뒤 진행하는 것이 좋습니다. 하지만 더 편리하게, [middleware](#job-middleware)인 `SkipIfBatchCancelled`를 작업에 지정해 둘 수도 있습니다. 이 미들웨어를 지정하면, 해당 배치가 취소된 경우 Laravel이 자동으로 작업 실행을 건너뜁니다.

```
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
배치 작업이 실패할 경우, (지정되어 있다면) `catch` 콜백이 실행됩니다. 이 콜백은 배치 내에서 처음 실패한 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>
<!-- #### Allowing Failures -->
#### Allowing Failures

<!-- When a job within a batch fails, Laravel will automatically mark the batch as "cancelled". If you wish, you may disable this behavior so that a job failure does not automatically mark the batch as cancelled. This may be accomplished by calling the `allowFailures` method while dispatching the batch: -->
배치 내 작업이 실패하면 Laravel에서는 기본적으로 해당 배치를 "취소됨" 상태로 표시합니다. 하지만, 원한다면 이 동작을 비활성화하고, 작업 실패가 배치 전체의 취소로 자동 연결되지 않도록 할 수 있습니다. 배치 디스패치 시 `allowFailures` 메서드를 호출하면 됩니다.

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
Laravel은 실패한 배치 작업 전체를 손쉽게 재시도할 수 있도록 `queue:retry-batch` 아티즌 명령어를 제공합니다. `queue:retry-batch` 명령어에는 재시도할 배치의 UUID를 전달합니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
<!-- ### Pruning Batches -->
### Pruning Batches

<!-- Without pruning, the `job_batches` table can accumulate records very quickly. To mitigate this, you should [schedule](/docs/11.x/scheduling) the `queue:prune-batches` Artisan command to run daily: -->
별도의 정리를 하지 않으면 `job_batches` 테이블에 기록이 빠르게 누적될 수 있습니다. 이를 방지하려면, [schedule](/docs/11.x/scheduling)를 사용해 `queue:prune-batches` 아티즌 명령어를 매일 실행되도록 등록하는 것이 좋습니다.

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

<!-- By default, all finished batches that are more than 24 hours old will be pruned. You may use the `hours` option when calling the command to determine how long to retain batch data. For example, the following command will delete all batches that finished over 48 hours ago: -->
기본적으로 24시간 이상 지난 완료된 배치가 모두 정리됩니다. 명령어 호출 시 `hours` 옵션을 지정해 배치 데이터를 얼마 동안 보관할지 조절할 수 있습니다. 다음 예제는 48시간 이상 지난 완료 배치를 삭제합니다.

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

<!-- Sometimes, your `jobs_batches` table may accumulate batch records for batches that never completed successfully, such as batches where a job failed and that job was never retried successfully. You may instruct the `queue:prune-batches` command to prune these unfinished batch records using the `unfinished` option: -->
경우에 따라, `jobs_batches` 테이블에는 한 번도 완전히 완료되지 않은 배치(예: 작업 실패 후 성공적으로 재시도되지 않은 배치)에 대한 기록이 누적되기도 합니다. `queue:prune-batches` 명령어의 `unfinished` 옵션을 사용해 이런 미완료 배치 레코드도 지정된 시간 이후 자동 정리할 수 있습니다.

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

<!-- Likewise, your `jobs_batches` table may also accumulate batch records for cancelled batches. You may instruct the `queue:prune-batches` command to prune these cancelled batch records using the `cancelled` option: -->
마찬가지로, `jobs_batches` 테이블에는 취소된 배치에 대한 기록도 누적될 수 있습니다. `queue:prune-batches` 명령어의 `cancelled` 옵션을 활용해, 일정 시간이 지난 취소 배치 레코드도 정리할 수 있습니다.

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>

<!-- ### Storing Batches in DynamoDB -->
### Storing Batches in DynamoDB

<!-- Laravel also provides support for storing batch meta information in [DynamoDB](https://aws.amazon.com/dynamodb) instead of a relational database. However, you will need to manually create a DynamoDB table to store all of the batch records. -->
Laravel은 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 메타 정보를 저장하는 것도 지원합니다. 단, 모든 배치 레코드를 저장할 DynamoDB 테이블은 직접 수동으로 생성해야 합니다.

<!-- Typically, this table should be named `job_batches`, but you should name the table based on the value of the `queue.batching.table` configuration value within your application's `queue` configuration file. -->
일반적으로 이 테이블의 이름은 `job_batches`로 지정하지만, 애플리케이션의 `queue` 설정 파일 내 `queue.batching.table` 구성값에 따라 테이블 이름을 설정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
<!-- #### DynamoDB Batch Table Configuration -->
#### DynamoDB Batch Table Configuration

<!-- The `job_batches` table should have a string primary partition key named `application` and a string primary sort key named `id`. The `application` portion of the key will contain your application's name as defined by the `name` configuration value within your application's `app` configuration file. Since the application name is part of the DynamoDB table's key, you can use the same table to store job batches for multiple Laravel applications. -->
`job_batches` 테이블에는 문자열 기본 파티션 키인 `application`과 문자열 기본 정렬 키인 `id`가 있어야 합니다. `application` 키에는 애플리케이션의 `app` 설정 파일에 정의된 `name` 구성값이 들어갑니다. DynamoDB 테이블의 키에 애플리케이션 이름이 포함되므로, 여러 Laravel 애플리케이션의 잡 배치를 하나의 테이블에 함께 저장할 수 있습니다.

<!-- In addition, you may define `ttl` attribute for your table if you would like to take advantage of [automatic batch pruning](#pruning-batches-in-dynamodb). -->
또한 [automatic batch pruning](#pruning-batches-in-dynamodb) 기능을 활용하려면 테이블에 `ttl` 속성을 추가로 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
<!-- #### DynamoDB Configuration -->
#### DynamoDB Configuration

<!-- Next, install the AWS SDK so that your Laravel application can communicate with Amazon DynamoDB: -->
다음으로, Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

<!-- Then, set the `queue.batching.driver` configuration option's value to `dynamodb`. In addition, you should define `key`, `secret`, and `region` configuration options within the `batching` configuration array. These options will be used to authenticate with AWS. When using the `dynamodb` driver, the `queue.batching.database` configuration option is unnecessary: -->
그런 다음, `queue.batching.driver` 구성 옵션의 값을 `dynamodb`로 설정합니다. 추가로, `batching` 설정 배열 내에 `key`, `secret`, `region` 구성 옵션을 정의해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.batching.database` 구성 옵션이 필요하지 않습니다:

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
[DynamoDB](https://aws.amazon.com/dynamodb)에 잡 배치 정보를 저장할 때는, 관계형 데이터베이스에 저장된 배치 정보를 정리할 때 사용하는 일반적인 정리 명령어를 사용할 수 없습니다. 대신 [DynamoDB's native TTL functionality](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용해, 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

<!-- If you defined your DynamoDB table with a `ttl` attribute, you may define configuration parameters to instruct Laravel how to prune batch records. The `queue.batching.ttl_attribute` configuration value defines the name of the attribute holding the TTL, while the `queue.batching.ttl` configuration value defines the number of seconds after which a batch record can be removed from the DynamoDB table, relative to the last time the record was updated: -->
DynamoDB 테이블에 `ttl` 속성을 정의했다면, Laravel에 배치 레코드 정리 방법을 지시하는 추가 구성 파라미터를 정의할 수 있습니다. `queue.batching.ttl_attribute` 구성값은 TTL 값을 저장할 속성명을 정의하며, `queue.batching.ttl` 구성값은 레코드가 마지막으로 업데이트된 시점 기준으로 몇 초 후에 해당 배치 레코드를 DynamoDB 테이블에서 삭제할 수 있는지 설정합니다:

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
잡 클래스를 큐에 디스패치하는 대신 클로저를 직접 큐에 보낼 수도 있습니다. 이 기능은 단순하고 빠르게 실행해야 하며, 현재 요청 사이클 밖에서 처리해야 하는 작업에 유용합니다. 클로저를 큐에 디스패치할 때는, 클로저의 코드 내용이 암호화 서명되어 전송 중에 수정될 수 없습니다.

```
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

<!-- Using the `catch` method, you may provide a closure that should be executed if the queued closure fails to complete successfully after exhausting all of your queue's [configured retry attempts](#max-job-attempts-and-timeout): -->
`catch` 메서드를 활용하면, 큐에 적재된 클로저가 [configured retry attempts](#max-job-attempts-and-timeout)를 모두 소진하고도 성공하지 못했을 때 실행되는 클로저를 정의할 수 있습니다.

```
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

> [!WARNING]
> `catch` 콜백은 직렬화되어 Laravel 큐가 나중에 실행하기 때문에, `catch` 콜백 안에서는 `$this` 변수를 사용하지 않아야 합니다.

<a name="running-the-queue-worker"></a>
<!-- ## Running the Queue Worker -->
## Running the Queue Worker

<a name="the-queue-work-command"></a>
<!-- ### The `queue:work` Command -->
### The `queue:work` Command

<!-- Laravel includes an Artisan command that will start a queue worker and process new jobs as they are pushed onto the queue. You may run the worker using the `queue:work` Artisan command. Note that once the `queue:work` command has started, it will continue to run until it is manually stopped or you close your terminal: -->
Laravel에는 큐 워커를 시작해 새로 들어오는 작업들을 처리할 수 있는 Artisan 명령어가 내장되어 있습니다. `queue:work` Artisan 명령어로 워커를 실행하면, 해당 명령어가 실행되는 동안 큐에 작업이 들어올 때마다 계속해서 작업을 처리합니다. `queue:work` 명령어는 수동으로 중지하거나 터미널을 닫기 전까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 항상 실행되도록 유지하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용해야 하며, 큐 워커가 중단되지 않고 계속 동작하도록 해야 합니다.

<!-- You may include the `-v` flag when invoking the `queue:work` command if you would like the processed job IDs to be included in the command's output: -->
`queue:work` 명령어 실행 시 `-v` 플래그를 추가하면, 처리된 작업 ID가 명령어의 출력 결과에 포함됩니다.

```shell
php artisan queue:work -v
```

<!-- Remember, queue workers are long-lived processes and store the booted application state in memory. As a result, they will not notice changes in your code base after they have been started. So, during your deployment process, be sure to [restart your queue workers](#queue-workers-and-deployment). In addition, remember that any static state created or modified by your application will not be automatically reset between jobs. -->
큐 워커는 장시간 실행되는 프로세스이므로 현재 부팅된 애플리케이션 상태를 메모리에 저장합니다. 즉, 워커가 이미 시작된 이후 코드베이스에 변경이 있어도 이를 감지하지 못합니다. 따라서 배포 과정 중에는 [restart your queue workers](#queue-workers-and-deployment)해야 합니다. 또한, 애플리케이션 내에서 생성하거나 변경된 정적(static) 상태는 작업 간에 자동으로 초기화되지 않는 점도 기억해야 합니다.

<!-- Alternatively, you may run the `queue:listen` command. When using the `queue:listen` command, you don't have to manually restart the worker when you want to reload your updated code or reset the application state; however, this command is significantly less efficient than the `queue:work` command: -->
대신 `queue:listen` 명령어를 사용할 수도 있습니다. `queue:listen` 명령어를 사용하는 경우, 코드가 업데이트되거나 애플리케이션 상태를 리셋하려면 워커를 직접 재시작할 필요가 없습니다. 하지만 이 명령어는 `queue:work` 명령어에 비해 성능이 떨어집니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
<!-- #### Running Multiple Queue Workers -->
#### Running Multiple Queue Workers

<!-- To assign multiple workers to a queue and process jobs concurrently, you should simply start multiple `queue:work` processes. This can either be done locally via multiple tabs in your terminal or in production using your process manager's configuration settings. [When using Supervisor](#supervisor-configuration), you may use the `numprocs` configuration value. -->
큐에 여러 워커를 할당해 동시에 작업을 처리하고 싶다면, `queue:work` 프로세스를 여러 개 실행하면 됩니다. 이는 로컬에서는 터미널의 여러 탭을 활용해 실행할 수 있고, 운영 환경에서는 프로세스 관리자의 설정을 이용해 가능합니다. [When using Supervisor](#supervisor-configuration)에는 `numprocs` 설정 값을 사용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
<!-- #### Specifying the Connection and Queue -->
#### Specifying the Connection and Queue

<!-- You may also specify which queue connection the worker should utilize. The connection name passed to the `work` command should correspond to one of the connections defined in your `config/queue.php` configuration file: -->
워커가 사용해야 할 큐 연결(connection)도 직접 지정할 수 있습니다. `work` 명령어에 전달하는 연결 이름은 `config/queue.php` 설정 파일에 정의된 연결 중 하나와 일치해야 합니다.

```shell
php artisan queue:work redis
```

<!-- By default, the `queue:work` command only processes jobs for the default queue on a given connection. However, you may customize your queue worker even further by only processing particular queues for a given connection. For example, if all of your emails are processed in an `emails` queue on your `redis` queue connection, you may issue the following command to start a worker that only processes that queue: -->
기본적으로 `queue:work` 명령어는 지정한 연결의 기본 큐에 있는 작업만 처리합니다. 하지만 특정 큐만 처리하도록 워커를 더욱 세밀하게 구성할 수도 있습니다. 예를 들어, 모든 이메일 작업이 `redis` 연결의 `emails` 큐로 분리되어 있다면, 해당 큐만 처리하는 워커를 다음과 같이 실행할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
<!-- #### Processing a Specified Number of Jobs -->
#### Processing a Specified Number of Jobs

<!-- The `--once` option may be used to instruct the worker to only process a single job from the queue: -->
`--once` 옵션을 사용하면, 워커가 큐에서 단 하나의 작업만 처리하도록 할 수 있습니다.

```shell
php artisan queue:work --once
```

<!-- The `--max-jobs` option may be used to instruct the worker to process the given number of jobs and then exit. This option may be useful when combined with [Supervisor](#supervisor-configuration) so that your workers are automatically restarted after processing a given number of jobs, releasing any memory they may have accumulated: -->
`--max-jobs` 옵션으로 워커가 지정한 개수만큼 작업을 처리한 뒤 종료하도록 설정할 수도 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용하면, 작업을 일정 개수 이상 처리한 후 자동으로 워커를 재시작해 누적된 메모리를 해제하고자 할 때 유용합니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
<!-- #### Processing All Queued Jobs and Then Exiting -->
#### Processing All Queued Jobs and Then Exiting

<!-- The `--stop-when-empty` option may be used to instruct the worker to process all jobs and then exit gracefully. This option can be useful when processing Laravel queues within a Docker container if you wish to shutdown the container after the queue is empty: -->
`--stop-when-empty` 옵션을 사용하면, 워커가 큐에 남아있는 모든 작업을 처리한 뒤 정상적으로 종료합니다. 이 옵션은 Laravel 큐를 Docker 컨테이너 내에서 처리할 때, 큐가 모두 비워지면 컨테이너를 종료하고 싶을 때 유용하게 사용할 수 있습니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
<!-- #### Processing Jobs for a Given Number of Seconds -->
#### Processing Jobs for a Given Number of Seconds

<!-- The `--max-time` option may be used to instruct the worker to process jobs for the given number of seconds and then exit. This option may be useful when combined with [Supervisor](#supervisor-configuration) so that your workers are automatically restarted after processing jobs for a given amount of time, releasing any memory they may have accumulated: -->
`--max-time` 옵션을 사용하면 워커가 지정한 초(seconds) 동안만 작업을 처리한 후 종료하도록 할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 활용하여, 워커가 일정 시간 구동된 뒤 자동으로 재시작해 누적된 메모리 점유를 해소하도록 할 수 있습니다.

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
<!-- #### Worker Sleep Duration -->
#### Worker Sleep Duration

<!-- When jobs are available on the queue, the worker will keep processing jobs with no delay in between jobs. However, the `sleep` option determines how many seconds the worker will "sleep" if there are no jobs available. Of course, while sleeping, the worker will not process any new jobs: -->
큐에 대기 중인 작업이 있으면, 워커는 작업 간 지연 없이 계속 작업을 처리합니다. 하지만 `sleep` 옵션은 큐에 작업이 없을 때 워커가 몇 초 동안 "대기"할 것인지 설정합니다. 워커가 대기 중일 때는 새로운 작업을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode and Queues -->
#### Maintenance Mode and Queues

<!-- While your application is in [maintenance mode](/docs/11.x/configuration#maintenance-mode), no queued jobs will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
애플리케이션이 [maintenance mode](/docs/11.x/configuration#maintenance-mode)일 때는 큐 작업이 처리되지 않습니다. 애플리케이션이 유지보수 모드에서 벗어나면 작업이 평소와 같이 처리됩니다.

<!-- To force your queue workers to process jobs even if maintenance mode is enabled, you may use `--force` option: -->
유지보수 모드 중에도 큐 워커가 작업을 계속 처리하게 하려면, `--force` 옵션을 사용할 수 있습니다:

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
<!-- #### Resource Considerations -->
#### Resource Considerations

<!-- Daemon queue workers do not "reboot" the framework before processing each job. Therefore, you should release any heavy resources after each job completes. For example, if you are doing image manipulation with the GD library, you should free the memory with `imagedestroy` when you are done processing the image. -->
데몬 큐 워커는 각 작업을 처리하기 전에 프레임워크를 다시 "부팅"하지 않습니다. 따라서 각 작업이 끝난 후 무거운 리소스는 직접 해제해 주어야 합니다. 예를 들어 GD 라이브러리로 이미지 처리 작업을 한다면, 이미지 처리 후 `imagedestroy`를 통해 메모리를 반드시 해제해야 합니다.

<a name="queue-priorities"></a>
<!-- ### Queue Priorities -->
### Queue Priorities

<!-- Sometimes you may wish to prioritize how your queues are processed. For example, in your `config/queue.php` configuration file, you may set the default `queue` for your `redis` connection to `low`. However, occasionally you may wish to push a job to a `high` priority queue like so: -->
큐 작업 처리에 우선순위를 두고 싶을 때가 있습니다. 예를 들어, `config/queue.php` 구성 파일에서 `redis` 연결의 기본 `queue`를 `low`로 설정했다고 해도, 때때로 높은 우선순위 큐인 `high`에 작업을 보낼 수 있습니다.

```
dispatch((new Job)->onQueue('high'));
```

<!-- To start a worker that verifies that all of the `high` queue jobs are processed before continuing to any jobs on the `low` queue, pass a comma-delimited list of queue names to the `work` command: -->
`work` 명령어에 쉼표로 구분된 큐 이름 리스트를 넘기면, `high` 큐의 작업을 모두 처리한 뒤에야 `low` 큐의 작업을 시작하도록 워커를 설정할 수 있습니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
<!-- ### Queue Workers and Deployment -->
### Queue Workers and Deployment

<!-- Since queue workers are long-lived processes, they will not notice changes to your code without being restarted. So, the simplest way to deploy an application using queue workers is to restart the workers during your deployment process. You may gracefully restart all of the workers by issuing the `queue:restart` command: -->
큐 워커는 장시간 실행되는 프로세스이므로, 코드를 변경하더라도 워커가 자동으로 이를 감지하지 못합니다. 따라서 큐 워커가 있는 애플리케이션을 배포할 때는, 배포 과정 중 워커를 재시작하는 것이 가장 쉽고 안전한 방법입니다. 워커를 모두 정상적으로 재시작하려면 `queue:restart` 명령어를 실행하십시오.

```shell
php artisan queue:restart
```

<!-- This command will instruct all queue workers to gracefully exit after they finish processing their current job so that no existing jobs are lost. Since the queue workers will exit when the `queue:restart` command is executed, you should be running a process manager such as [Supervisor](#supervisor-configuration) to automatically restart the queue workers. -->
이 명령어는 각 워커가 현재 처리 중인 작업까지 마친 후 정상적으로 종료하도록 지시합니다. 따라서 처리 중인 작업이 유실되지 않습니다. `queue:restart` 명령어 실행 후 워커는 모두 종료되기 때문에, [Supervisor](#supervisor-configuration)와 같은 프로세스 관리자로 자동 재시작되도록 설정해야 합니다.

> [!NOTE]
> 큐는 [cache](/docs/11.x/cache)를 활용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 반드시 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
<!-- ### Job Expirations and Timeouts -->
### Job Expirations and Timeouts

<a name="job-expiration"></a>
<!-- #### Job Expiration -->
#### Job Expiration

<!-- In your `config/queue.php` configuration file, each queue connection defines a `retry_after` option. This option specifies how many seconds the queue connection should wait before retrying a job that is being processed. For example, if the value of `retry_after` is set to `90`, the job will be released back onto the queue if it has been processing for 90 seconds without being released or deleted. Typically, you should set the `retry_after` value to the maximum number of seconds your jobs should reasonably take to complete processing. -->
`config/queue.php` 설정 파일에서, 각 큐 연결에는 `retry_after` 옵션이 있습니다. 이 옵션은 잡이 처리 중일 때, 정해진 초(seconds)만큼 기다렸다가 다시 시도(재시도)해야 할 시점을 지정합니다. 예를 들어 `retry_after` 값을 `90`으로 설정하면, 해당 작업이 90초 동안 처리되고도 큐에 반환(release)되거나 삭제(delete)되지 않을 경우 다시 큐로 되돌아가게 됩니다. 일반적으로, `retry_after` 값은 작업이 합리적으로 완료하는 데 걸리는 최대 시간에 맞춰야 합니다.

> [!WARNING]
> `retry_after` 값을 포함하지 않는 유일한 큐 연결은 Amazon SQS입니다. SQS는 AWS 콘솔에서 관리하는 [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)에 따라 자동으로 잡 재시도를 관리합니다.

<a name="worker-timeouts"></a>
<!-- #### Worker Timeouts -->
#### Worker Timeouts

<!-- The `queue:work` Artisan command exposes a `--timeout` option. By default, the `--timeout` value is 60 seconds. If a job is processing for longer than the number of seconds specified by the timeout value, the worker processing the job will exit with an error. Typically, the worker will be restarted automatically by a [process manager configured on your server](#supervisor-configuration): -->
`queue:work` Artisan 명령어에는 `--timeout` 옵션이 있습니다. 기본적으로 `--timeout` 값은 60초입니다. 지정한 타임아웃 시간보다 오래 작업이 처리될 경우, 해당 작업을 담당하는 워커는 오류와 함께 종료됩니다. 보통 서버에 [process manager configured on your server](#supervisor-configuration)에 의해 워커가 자동으로 재시작됩니다.

```shell
php artisan queue:work --timeout=60
```

<!-- The `retry_after` configuration option and the `--timeout` CLI option are different, but work together to ensure that jobs are not lost and that jobs are only successfully processed once. -->
`retry_after` 구성 옵션과 `--timeout` CLI 옵션은 서로 다르지만, 두 옵션은 작업이 유실되지 않고 단 한 번만 성공적으로 처리되도록 함께 동작합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 값보다 최소 몇 초 이상 더 짧아야 합니다. 그래야 워커가 멈춘(frozen) 작업을 재시도하기 전 반드시 종료되도록 보장할 수 있습니다. 만약 `--timeout` 값이 `retry_after`보다 길다면, 작업이 두 번 처리되는 문제가 생길 수 있습니다.

<a name="supervisor-configuration"></a>
<!-- ## Supervisor Configuration -->
## Supervisor Configuration

<!-- In production, you need a way to keep your `queue:work` processes running. A `queue:work` process may stop running for a variety of reasons, such as an exceeded worker timeout or the execution of the `queue:restart` command. -->
운영 환경에서는 `queue:work` 프로세스가 항상 실행되도록 유지할 방법이 필요합니다. `queue:work` 프로세스는 워커 타임아웃 초과나 `queue:restart` 명령 실행 등 다양한 이유로 중지될 수 있기 때문입니다.

<!-- For this reason, you need to configure a process monitor that can detect when your `queue:work` processes exit and automatically restart them. In addition, process monitors can allow you to specify how many `queue:work` processes you would like to run concurrently. Supervisor is a process monitor commonly used in Linux environments and we will discuss how to configure it in the following documentation. -->
따라서, `queue:work` 프로세스가 종료되었을 때 이를 감지하여 자동으로 재시작시키는 프로세스 모니터를 반드시 구성해야 합니다. 또, 프로세스 모니터를 사용하면 동시에 몇 개의 `queue:work` 프로세스를 실행할지도 직접 지정할 수 있습니다. Supervisor는 리눅스 환경에서 널리 사용되는 프로세스 모니터이며, 아래에서 Supervisor 설치 및 설정 방법을 안내합니다.

<a name="installing-supervisor"></a>
<!-- #### Installing Supervisor -->
#### Installing Supervisor

<!-- Supervisor is a process monitor for the Linux operating system, and will automatically restart your `queue:work` processes if they fail. To install Supervisor on Ubuntu, you may use the following command: -->
Supervisor는 리눅스 운영체제에서 동작하는 프로세스 모니터로, `queue:work` 프로세스가 실패하면 자동으로 재시작해줍니다. Ubuntu에서는 아래 명령어로 Supervisor를 설치할 수 있습니다:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> 직접 Supervisor를 구성하고 관리하는 것이 부담스럽다면, [Laravel Forge](https://forge.laravel.com) 사용을 고려해 보십시오. Forge는 운영 환경의 Laravel 프로젝트를 위해 Supervisor를 자동으로 설치 및 설정해줍니다.

<a name="configuring-supervisor"></a>
<!-- #### Configuring Supervisor -->
#### Configuring Supervisor

<!-- Supervisor configuration files are typically stored in the `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `laravel-worker.conf` file that starts and monitors `queue:work` processes: -->
Supervisor 설정 파일은 보통 `/etc/supervisor/conf.d` 디렉터리에 위치합니다. 이 디렉터리 내에 여러 설정 파일을 생성해, supervisor가 각 프로세스를 어떻게 관리할지 지정할 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 생성해 `queue:work` 프로세스를 실행 및 관리하도록 할 수 있습니다.

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
여기서 `numprocs` 설정은 Supervisor가 8개의 `queue:work` 프로세스를 실행 및 모니터하며, 실패하면 자동으로 재시작함을 의미합니다. 설정 파일의 `command` 항목은 실제 사용할 큐 연결명 및 워커 옵션에 맞게 수정해야 합니다.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 걸리는 작업의 실행 시간보다 반드시 커야 합니다. 그렇지 않으면 Supervisor가 해당 작업을 마치기도 전에 종료시킬 수 있습니다.

<a name="starting-supervisor"></a>
<!-- #### Starting Supervisor -->
#### Starting Supervisor

<!-- Once the configuration file has been created, you may update the Supervisor configuration and start the processes using the following commands: -->
설정 파일을 작성한 뒤, 다음 명령어로 Supervisor 설정을 갱신하고 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

<!-- For more information on Supervisor, consult the [Supervisor documentation](http://supervisord.org/index.html). -->
Supervisor에 대한 더 자세한 내용은 [Supervisor documentation](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
<!-- ## Dealing With Failed Jobs -->
## Dealing With Failed Jobs

<!-- Sometimes your queued jobs will fail. Don't worry, things don't always go as planned! Laravel includes a convenient way to [specify the maximum number of times a job should be attempted](#max-job-attempts-and-timeout). After an asynchronous job has exceeded this number of attempts, it will be inserted into the `failed_jobs` database table. [Synchronously dispatched jobs](/docs/11.x/queues#synchronous-dispatching) that fail are not stored in this table and their exceptions are immediately handled by the application. -->
큐에 적재된 잡이 실패하는 상황도 발생할 수 있습니다. 걱정하지 마세요! Laravel은 [specify the maximum number of times a job should be attempted](#max-job-attempts-and-timeout) 등 실패한 잡을 효율적으로 관리할 수 있는 기능을 제공합니다. 비동기로 실행되는 작업이 지정된 최대 시도 횟수를 초과하면, 해당 작업은 `failed_jobs` 데이터베이스 테이블에 저장됩니다. [Synchronously dispatched jobs](/docs/11.x/queues#synchronous-dispatching)이 실패한 경우에는 이 테이블에 저장되지 않고, 예외가 즉시 애플리케이션에서 처리됩니다.

<!-- A migration to create the `failed_jobs` table is typically already present in new Laravel applications. However, if your application does not contain a migration for this table, you may use the `make:queue-failed-table` command to create the migration: -->
`failed_jobs` 테이블을 생성하는 마이그레이션 파일은 일반적으로 새로운 Laravel 애플리케이션에 포함되어 있습니다. 만약 애플리케이션에 이 테이블용 마이그레이션이 없다면, `make:queue-failed-table` 명령어로 쉽게 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

<!-- When running a [queue worker](#running-the-queue-worker) process, you may specify the maximum number of times a job should be attempted using the `--tries` switch on the `queue:work` command. If you do not specify a value for the `--tries` option, jobs will only be attempted once or as many times as specified by the job class' `$tries` property: -->
[queue worker](#running-the-queue-worker) 프로세스를 실행할 때는, `queue:work` 명령어에 `--tries` 옵션을 추가해 작업별 최대 시도 횟수를 지정할 수 있습니다. `--tries` 옵션에 값을 지정하지 않으면, 각 잡 클래스의 `$tries` 속성값이나 기본값에 따라 단 한 번만 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

<!-- Using the `--backoff` option, you may specify how many seconds Laravel should wait before retrying a job that has encountered an exception. By default, a job is immediately released back onto the queue so that it may be attempted again: -->
또한 `--backoff` 옵션을 활용해, 예외 발생 후 작업을 재시도하기 전 Laravel이 기다릴 초(seconds)를 지정할 수 있습니다. 기본적으로는 작업이 즉시 큐에 다시 반환되어 재시도됩니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

<!-- If you would like to configure how many seconds Laravel should wait before retrying a job that has encountered an exception on a per-job basis, you may do so by defining a `backoff` property on your job class: -->
특정 작업별로 예외 발생 후 재시도 대기 시간을 개별 설정하려는 경우, 잡 클래스에 `backoff` 속성을 직접 정의할 수 있습니다:

```
/**
 * The number of seconds to wait before retrying the job.
 *
 * @var int
 */
public $backoff = 3;
```

<!-- If you require more complex logic for determining the job's backoff time, you may define a `backoff` method on your job class: -->
더 복잡한 재시도 대기 시간 로직이 필요하다면, 잡 클래스에 `backoff` 메서드를 정의할 수도 있습니다:

```
/**
* Calculate the number of seconds to wait before retrying the job.
*/
public function backoff(): int
{
    return 3;
}
```

<!-- You may easily configure "exponential" backoffs by returning an array of backoff values from the `backoff` method. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining: -->
"지수형(exponential)" 백오프(재시도 지연)를 설정하려면, `backoff` 메서드에서 대기 시간 값을 배열로 반환하면 됩니다. 예를 들어 첫 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 이후는 계속 10초씩 대기하도록 할 수 있습니다:

```
/**
* Calculate the number of seconds to wait before retrying the job.
*
* @return array<int, int>
*/
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
<!-- ### Cleaning Up After Failed Jobs -->
### Cleaning Up After Failed Jobs

<!-- When a particular job fails, you may want to send an alert to your users or revert any actions that were partially completed by the job. To accomplish this, you may define a `failed` method on your job class. The `Throwable` instance that caused the job to fail will be passed to the `failed` method: -->
특정 작업이 실패할 경우, 사용자의 알림을 보내거나 작업 도중 일부만 실행된 기능들을 되돌리는 등의 후처리가 필요할 수 있습니다. 이를 위해, 잡 클래스에 `failed` 메서드를 정의하면 됩니다. 이때 작업이 실패하게 만든 `Throwable` 인스턴스가 `failed` 메서드로 전달됩니다.

```
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
> `failed` 메서드가 호출될 때는 잡의 새로운 인스턴스가 생성됩니다. 따라서 `handle` 메서드에서 변경한 클래스 속성(property)의 변경 내용은 사라집니다.

<a name="retrying-failed-jobs"></a>
<!-- ### Retrying Failed Jobs -->
### Retrying Failed Jobs

<!-- To view all of the failed jobs that have been inserted into your `failed_jobs` database table, you may use the `queue:failed` Artisan command: -->
`failed_jobs` 테이블에 저장된 모든 실패한 작업 내역은 `queue:failed` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan queue:failed
```

<!-- The `queue:failed` command will list the job ID, connection, queue, failure time, and other information about the job. The job ID may be used to retry the failed job. For instance, to retry a failed job that has an ID of `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`, issue the following command: -->
`queue:failed` 명령어는 작업의 ID, 연결 정보, 큐 이름, 실패 시간 등 관련 정보를 표시합니다. 출력되는 작업 ID는 재시도 명령어에 사용할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패한 작업을 재시도하려면 아래와 같이 명령어를 실행하면 됩니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

<!-- If necessary, you may pass multiple IDs to the command: -->
여러 작업을 한 번에 재시도하려면, 여러 ID를 공백으로 구분해 전달할 수 있습니다:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

<!-- You may also retry all of the failed jobs for a particular queue: -->
특정 큐의 모든 실패 잡을 재시도할 때는 다음과 같이 할 수 있습니다:

```shell
php artisan queue:retry --queue=name
```

<!-- To retry all of your failed jobs, execute the `queue:retry` command and pass `all` as the ID: -->
모든 실패한 작업을 재시도하려면, `queue:retry` 명령어에 `all`을 ID 대신 전달하세요:

```shell
php artisan queue:retry all
```

<!-- If you would like to delete a failed job, you may use the `queue:forget` command: -->
특정 실패한 작업을 삭제하고 싶을 때는 `queue:forget` 명령을 사용할 수 있습니다:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/11.x/horizon)을 사용하는 경우에는, `queue:forget` 대신 `horizon:forget` 명령어를 사용해야 합니다.

<!-- To delete all of your failed jobs from the `failed_jobs` table, you may use the `queue:flush` command: -->
`failed_jobs` 테이블의 모든 레코드를 삭제하려면 `queue:flush` 명령을 사용합니다:

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
<!-- ### Ignoring Missing Models -->
### Ignoring Missing Models

<!-- When injecting an Eloquent model into a job, the model is automatically serialized before being placed on the queue and re-retrieved from the database when the job is processed. However, if the model has been deleted while the job was waiting to be processed by a worker, your job may fail with a `ModelNotFoundException`. -->
Eloquent 모델을 작업에 직접 삽입할 경우, 해당 모델은 큐에 저장되기 전에 자동으로 직렬화되고, 작업 처리 시 데이터베이스에서 다시 조회됩니다. 다만, 작업이 처리 대기 중일 때 해당 모델이 삭제된 경우, 해당 작업은 `ModelNotFoundException`과 함께 실패할 수 있습니다.

<!-- For convenience, you may choose to automatically delete jobs with missing models by setting your job's `deleteWhenMissingModels` property to `true`. When this property is set to `true`, Laravel will quietly discard the job without raising an exception: -->
편의를 위해, 작업 클래스의 `deleteWhenMissingModels` 속성을 `true`로 지정할 수 있습니다. 이 속성이 `true`로 설정되어 있으면, 모델이 존재하지 않을 경우 Laravel이 예외를 발생하지 않고 조용히 해당 작업을 삭제합니다.

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
`queue:prune-failed` Artisan 명령어를 실행해 애플리케이션의 `failed_jobs` 테이블에 저장된 레코드를 정리할 수 있습니다.

```shell
php artisan queue:prune-failed
```

<!-- By default, all the failed job records that are more than 24 hours old will be pruned. If you provide the `--hours` option to the command, only the failed job records that were inserted within the last N number of hours will be retained. For example, the following command will delete all the failed job records that were inserted more than 48 hours ago: -->
기본적으로 24시간이 지난 모든 실패 작업 레코드가 정리됩니다. `--hours` 옵션을 사용하면, 최근 N시간 이내에 삽입된 작업만 남기고 그보다 오래된 레코드만 삭제합니다. 예를 들어, 최근 48시간 이내의 실패 작업만 남기고 싶다면 다음과 같이 실행합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
<!-- ### Storing Failed Jobs in DynamoDB -->
### Storing Failed Jobs in DynamoDB

<!-- Laravel also provides support for storing your failed job records in [DynamoDB](https://aws.amazon.com/dynamodb) instead of a relational database table. However, you must manually create a DynamoDB table to store all of the failed job records. Typically, this table should be named `failed_jobs`, but you should name the table based on the value of the `queue.failed.table` configuration value within your application's `queue` configuration file. -->
Laravel은 관계형 데이터베이스 테이블 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 실패한 작업 레코드를 저장하는 것도 지원합니다. 단, 모든 실패한 작업 레코드를 저장할 DynamoDB 테이블은 직접 수동으로 생성해야 합니다. 테이블 이름은 보통 `failed_jobs`이지만, 애플리케이션 `queue` 설정 파일 내의 `queue.failed.table` 구성값에 따라 이름을 결정해야 합니다.

<!-- The `failed_jobs` table should have a string primary partition key named `application` and a string primary sort key named `uuid`. The `application` portion of the key will contain your application's name as defined by the `name` configuration value within your application's `app` configuration file. Since the application name is part of the DynamoDB table's key, you can use the same table to store failed jobs for multiple Laravel applications. -->
`failed_jobs` 테이블에는 문자열 기본 파티션 키인 `application`과 문자열 기본 정렬 키인 `uuid`가 있어야 합니다. `application` 키에는 애플리케이션의 `app` 설정 파일에 정의된 `name` 값이 들어갑니다. 이렇게 하면 여러 Laravel 애플리케이션의 실패한 작업도 하나의 테이블에 함께 저장할 수 있습니다.

<!-- In addition, ensure that you install the AWS SDK so that your Laravel application can communicate with Amazon DynamoDB: -->
또한, Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 반드시 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

<!-- Next, set the `queue.failed.driver` configuration option's value to `dynamodb`. In addition, you should define `key`, `secret`, and `region` configuration options within the failed job configuration array. These options will be used to authenticate with AWS. When using the `dynamodb` driver, the `queue.failed.database` configuration option is unnecessary: -->
그런 다음, `queue.failed.driver` 구성 옵션의 값을 `dynamodb`로 지정합니다. 추가로, 실패 작업 설정 배열 내에 `key`, `secret`, `region` 옵션을 지정해야 하며, 이 값은 AWS 인증에 사용됩니다. `dynamodb` 드라이버 사용할 때는 `queue.failed.database` 구성 옵션은 필요하지 않습니다.

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
실패한 작업을 저장하지 않고 바로 삭제하려면, `queue.failed.driver` 구성 옵션 값을 `null`로 설정하십시오. 일반적으로 `QUEUE_FAILED_DRIVER` 환경 변수로 지정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
<!-- ### Failed Job Events -->
### Failed Job Events

<!-- If you would like to register an event listener that will be invoked when a job fails, you may use the `Queue` facade's `failing` method. For example, we may attach a closure to this event from the `boot` method of the `AppServiceProvider` that is included with Laravel: -->
잡이 실패했을 때 호출되는 이벤트 리스너를 등록하려면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, Laravel에 기본 포함된 `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 이벤트를 붙일 수 있습니다.

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
> [Horizon](/docs/11.x/horizon)을 사용할 때는 `queue:clear` 명령어 대신 `horizon:clear` 명령어로 큐의 작업을 삭제해야 합니다.

<!-- If you would like to delete all jobs from the default queue of the default connection, you may do so using the `queue:clear` Artisan command: -->
기본 연결의 기본 큐에서 모든 작업을 삭제하려면, 아티즌의 `queue:clear` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

<!-- You may also provide the `connection` argument and `queue` option to delete jobs from a specific connection and queue: -->
특정 연결 및 큐에서 작업을 삭제하려면 `connection` 인수와 `queue` 옵션을 함께 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 삭제하는 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 사용할 수 있습니다. 또한 SQS의 메시지 삭제 처리는 최대 60초까지 소요될 수 있으므로, 큐를 비운 이후 60초 이내에 SQS에 전송된 작업도 같이 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
<!-- ## Monitoring Your Queues -->
## Monitoring Your Queues

<!-- If your queue receives a sudden influx of jobs, it could become overwhelmed, leading to a long wait time for jobs to complete. If you wish, Laravel can alert you when your queue job count exceeds a specified threshold. -->
만약 큐에 작업이 갑자기 대량으로 몰리면 큐가 과부하되어 각 작업의 완료 대기 시간이 길어질 수 있습니다. 원한다면, 큐에 쌓인 작업 수가 특정 임계치(Threshold)를 넘어서면 Laravel이 이를 알림으로 통지하도록 설정할 수 있습니다.

<!-- To get started, you should schedule the `queue:monitor` command to [run every minute](/docs/11.x/scheduling). The command accepts the names of the queues you wish to monitor as well as your desired job count threshold: -->
먼저, `queue:monitor` 명령어를 [run every minute](/docs/11.x/scheduling)되도록 스케줄링해야 합니다. 이 명령어는 모니터링하고 싶은 큐 이름들과 임계치 작업 수를 파라미터로 받을 수 있습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

<!-- Scheduling this command alone is not enough to trigger a notification alerting you of the queue's overwhelmed status. When the command encounters a queue that has a job count exceeding your threshold, an `Illuminate\Queue\Events\QueueBusy` event will be dispatched. You may listen for this event within your application's `AppServiceProvider` in order to send a notification to you or your development team: -->
이 명령어만 스케줄링해도 자동으로 알림이 발송되지는 않습니다. 큐에 쌓인 작업 수가 임계치를 넘기면, `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 리스닝하여, 여러분 또는 개발팀에 알림을 발송하도록 구현할 수 있습니다.

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
<!-- ## Testing -->
## Testing

<!-- When testing code that dispatches jobs, you may wish to instruct Laravel to not actually execute the job itself, since the job's code can be tested directly and separately of the code that dispatches it. Of course, to test the job itself, you may instantiate a job instance and invoke the `handle` method directly in your test. -->
작업을 디스패치(dispatch)하는 코드를 테스트할 때, 작업이 실제로 실행되지는 않도록 Laravel에 지시하고 싶을 수 있습니다. 작업 내부의 코드는 별도의 단위 테스트로 바로 테스트할 수 있기 때문입니다. 작업 그 자체를 테스트하고 싶다면 테스트 코드 안에서 작업 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

<!-- You may use the `Queue` facade's `fake` method to prevent queued jobs from actually being pushed to the queue. After calling the `Queue` facade's `fake` method, you may then assert that the application attempted to push jobs to the queue: -->
큐에 들어가는 작업의 실제 푸시를 막으려면 `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. `Queue` 파사드의 `fake` 메서드를 호출한 뒤, 애플리케이션이 큐에 작업을 올리려고 시도했다는 사실만을 assert로 검증할 수 있습니다.

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

<!-- You may pass a closure to the `assertPushed` or `assertNotPushed` methods in order to assert that a job was pushed that passes a given "truth test". If at least one job was pushed that passes the given truth test then the assertion will be successful: -->
`assertPushed` 또는 `assertNotPushed` 메서드에 클로저(Closure)를 전달하여, 지정한 "진위 테스트(truth test)"를 통과하는 작업이 실제로 푸시되었는지 검증할 수 있습니다. 조건에 맞는 작업이 하나라도 푸시되었다면 assert는 성공합니다.

```
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
<!-- ### Faking a Subset of Jobs -->
### Faking a Subset of Jobs

<!-- If you only need to fake specific jobs while allowing your other jobs to execute normally, you may pass the class names of the jobs that should be faked to the `fake` method: -->
특정 작업들만 페이크로 처리하고, 다른 작업은 실제로 실행되게 하려면, `fake` 메서드에 가짜로 처리할 작업 클래스명을 배열로 전달합니다.

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

<!-- You may fake all jobs except for a set of specified jobs using the `except` method: -->
반대로, 지정한 작업들을 제외한 나머지 작업만 fake로 처리하려면 `except` 메서드를 사용할 수 있습니다.

```
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
<!-- ### Testing Job Chains -->
### Testing Job Chains

<!-- To test job chains, you will need to utilize the `Bus` facade's faking capabilities. The `Bus` facade's `assertChained` method may be used to assert that a [chain of jobs](/docs/11.x/queues#job-chaining) was dispatched. The `assertChained` method accepts an array of chained jobs as its first argument: -->
작업 체인(Chained Job)을 테스트하려면 `Bus` 파사드의 fake 기능을 활용해야 합니다. `Bus` 파사드의 `assertChained` 메서드는 [chain of jobs](/docs/11.x/queues#job-chaining)이 실제로 디스패치되었는지 검증할 수 있습니다. `assertChained` 메서드는 첫 번째 인자로 체인에 들어갈 작업 클래스명을 배열로 전달받습니다.

```
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
위 예시처럼, 체인 배열에 작업의 클래스명을 나열할 수도 있고, 실제 작업 인스턴스 배열을 쓸 수도 있습니다. 인스턴스를 사용할 때는, Laravel이 해당 인스턴스의 클래스와 속성(property) 값이 실제로 디스패치된 체인의 것과 일치하는지 검사합니다.

```
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

<!-- You may use the `assertDispatchedWithoutChain` method to assert that a job was pushed without a chain of jobs: -->
체인 없이 개별적으로 푸시된 작업을 검증하려면 `assertDispatchedWithoutChain` 메서드를 사용할 수 있습니다.

```
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
<!-- #### Testing Chain Modifications -->
#### Testing Chain Modifications

<!-- If a chained job [prepends or appends jobs to an existing chain](#adding-jobs-to-the-chain), you may use the job's `assertHasChain` method to assert that the job has the expected chain of remaining jobs: -->
만약 체인에 속한 작업이 [prepends or appends jobs to an existing chain](#adding-jobs-to-the-chain)한다면, 해당 작업의 `assertHasChain` 메서드를 이용하여 남은 체인이 예상대로 되어 있는지 검증할 수 있습니다.

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
남은 체인에 아무 작업도 없음을 검증하려면 `assertDoesntHaveChain` 메서드를 사용합니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
<!-- #### Testing Chained Batches -->
#### Testing Chained Batches

<!-- If your job chain [contains a batch of jobs](#chains-and-batches), you may assert that the chained batch matches your expectations by inserting a `Bus::chainedBatch` definition within your chain assertion: -->
작업 체인이 [contains a batch of jobs](#chains-and-batches)를 포함할 경우, 체인 검증 배열에 `Bus::chainedBatch` 정의를 넣어서 해당 배치가 예상과 일치하는지 확인할 수 있습니다.

```
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

<!-- The `Bus` facade's `assertBatched` method may be used to assert that a [batch of jobs](/docs/11.x/queues#job-batching) was dispatched. The closure given to the `assertBatched` method receives an instance of `Illuminate\Bus\PendingBatch`, which may be used to inspect the jobs within the batch: -->
`Bus` 파사드의 `assertBatched` 메서드를 사용하면 [batch of jobs](/docs/11.x/queues#job-batching)가 실제로 디스패치 되었는지 검사할 수 있습니다. `assertBatched`에 넘기는 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 전달받으며, 이를 통해 배치에 포함된 작업들을 검사할 수 있습니다.

```
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

<!-- You may use the `assertBatchCount` method to assert that a given number of batches were dispatched: -->
디스패치된 배치의 개수를 검사하려면 `assertBatchCount`를 사용할 수 있습니다.

```
Bus::assertBatchCount(3);
```

<!-- You may use `assertNothingBatched` to assert that no batches were dispatched: -->
배치가 아무것도 디스패치되지 않았음을 assert 하려면 `assertNothingBatched`를 사용합니다.

```
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
<!-- #### Testing Job / Batch Interaction -->
#### Testing Job / Batch Interaction

<!-- In addition, you may occasionally need to test an individual job's interaction with its underlying batch. For example, you may need to test if a job cancelled further processing for its batch. To accomplish this, you need to assign a fake batch to the job via the `withFakeBatch` method. The `withFakeBatch` method returns a tuple containing the job instance and the fake batch: -->
때때로, 개별 작업이 속한 배치와 상호작용하는 부분(예: 작업이 전체 배치의 다음 실행을 취소하는지 등)을 테스트하고 싶을 수 있습니다. 이를 위해 `withFakeBatch` 메서드로 가짜 배치를 작업에 할당해야 하며, `withFakeBatch` 메서드는 작업 인스턴스와 가짜 배치가 들어있는 튜플을 반환합니다.

```
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
<!-- ### Testing Job / Queue Interactions -->
### Testing Job / Queue Interactions

<!-- Sometimes, you may need to test that a queued job [releases itself back onto the queue](#manually-releasing-a-job). Or, you may need to test that the job deleted itself. You may test these queue interactions by instantiating the job and invoking the `withFakeQueueInteractions` method. -->
때로는 큐에 등록된 작업이 스스로 큐에 다시 반환되는지([releases itself back onto the queue](#manually-releasing-a-job)), 또는 작업 자체를 삭제하는지 테스트해야 하는 상황이 있습니다. 이때 작업 인스턴스를 생성해 `withFakeQueueInteractions` 메서드를 호출하여 큐와의 상호작용을 가짜로 만들 수 있습니다.

<!-- Once the job's queue interactions have been faked, you may invoke the `handle` method on the job. After invoking the job, the `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, and `assertNotFailed` methods may be used to make assertions against the job's queue interactions: -->
작업의 큐 상호작용을 fake로 만들고 나면, 바로 `handle` 메서드를 호출하면 됩니다. 이후 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등 다양한 assert 메서드를 이용해 큐와의 실제 상호작용을 검증할 수 있습니다.

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

<!-- Using the `before` and `after` methods on the `Queue` [facade](/docs/11.x/facades), you may specify callbacks to be executed before or after a queued job is processed. These callbacks are a great opportunity to perform additional logging or increment statistics for a dashboard. Typically, you should call these methods from the `boot` method of a [service provider](/docs/11.x/providers). For example, we may use the `AppServiceProvider` that is included with Laravel: -->
`Queue` [facade](/docs/11.x/facades)의 `before` 및 `after` 메서드를 사용하면, 큐에 들어간 작업이 처리되기 전이나 후에 실행될 콜백을 지정할 수 있습니다. 이 콜백은 추가 로깅을 하거나, 대시보드 통계를 올리는 데 유용합니다. 일반적으로 이런 메서드는 [service provider](/docs/11.x/providers)의 `boot` 메서드에서 호출합니다. 예시로, Laravel에 기본 제공되는 `AppServiceProvider`에서 아래와 같이 사용할 수 있습니다.

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

<!-- Using the `looping` method on the `Queue` [facade](/docs/11.x/facades), you may specify callbacks that execute before the worker attempts to fetch a job from a queue. For example, you might register a closure to rollback any transactions that were left open by a previously failed job: -->
`Queue` [facade](/docs/11.x/facades)의 `looping` 메서드를 사용하면, 워커가 큐에서 작업을 가져오기 전에 실행되는 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 작업 때문에 종료되지 않은 데이터베이스 트랜잭션을 롤백하기 위해 아래와 같이 클로저를 등록할 수도 있습니다.

```
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```
