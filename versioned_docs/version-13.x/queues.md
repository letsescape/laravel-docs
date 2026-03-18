# 큐 (Queues)

- [소개](#introduction)
    - [연결 대 큐](#connections-vs-queues)
    - [드라이버 참고 사항 및 전제 조건](#driver-prerequisites)
- [작업 생성](#creating-jobs)
    - [작업 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 작업](#unique-jobs)
    - [암호화된 작업](#encrypted-jobs)
- [작업 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [작업 중복 방지](#preventing-job-overlaps)
    - [제한 예외](#throttling-exceptions)
    - [작업 건너뛰기](#skipping-jobs)
- [디스패치 작업](#dispatching-jobs)
    - [지연된 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [작업 및 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [작업 체인](#job-chaining)
    - [큐 및 연결 사용자 지정](#customizing-the-queue-and-connection)
    - [최대 작업 시도 횟수/시간 초과 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정한 큐](#sqs-fifo-and-fair-queues)
    - [큐 장애 조치](#queue-failover)
    - [오류 처리](#error-handling)
- [작업 배치](#job-batching)
    - [배치 가능 작업 정의](#defining-batchable-jobs)
    - [디스패치 배치](#dispatching-batches)
    - [체인 및 배치](#chains-and-batches)
    - [배치에 작업 추가](#adding-jobs-to-batches)
    - [배치 검사](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [큐잉 클로저](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커 및 배포](#queue-workers-and-deployment)
    - [작업 만료 및 시간 초과](#job-expirations-and-timeouts)
    - [큐 워커 일시 중지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 구성](#supervisor-configuration)
- [작업 실패 처리](#dealing-with-failed-jobs)
    - [작업 실패 후 정리](#cleaning-up-after-failed-jobs)
    - [재시도 실패 작업](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 작업 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 작업 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 작업 저장소 비활성화](#disabling-failed-job-storage)
    - [실패한 작업 이벤트](#failed-job-events)
- [큐에서 작업 지우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [작업의 하위 집합 위조](#faking-a-subset-of-jobs)
    - [작업 체인 테스트](#testing-job-chains)
    - [작업 배치 테스트](#testing-job-batches)
    - [작업 / 큐 상호 작용 테스트](#testing-job-queue-interactions)
- [작업 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 구축하는 동안 업로드된 CSV 파일을 구문 분석하고 저장하는 등 일반적인 웹 요청 중에 수행하는 데 시간이 너무 오래 걸리는 일부 작업이 있을 수 있습니다. 다행히도 Laravel을 사용하면 백그라운드에서 처리할 수 있는 대기 중인 작업을 쉽게 생성할 수 있습니다. 시간 집약적인 작업을 큐로 이동하면 애플리케이션이 엄청난 속도로 웹 요청에 응답하고 고객에게 더 나은 사용자 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) 또는 관계형 데이터베이스와 같은 다양한 큐 백엔드에서 통합 큐 API를 제공합니다.

Laravel의 큐 구성 옵션은 애플리케이션의 `config/queue.php` 구성 파일에 저장됩니다. 이 파일에서는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) 및 [Beanstalkd](https://beanstalkd.github.io/)를 포함하여 프레임워크에 포함된 각 큐 드라이버에 대한 연결 구성을 찾을 수 있습니다. 드라이버 및 작업을 즉시 실행하는 동기식 드라이버(개발 또는 테스트에 사용). 대기 중인 작업을 삭제하는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon는 Redis 기반 큐를 위한 아름다운 대시보드 및 구성 시스템입니다. 자세한 내용은 전체 [Horizon 문서](/docs/13.x/horizon)를 확인하세요.

<a name="connections-vs-queues"></a>
### 연결 대 큐

Laravel 큐를 시작하기 전에 "연결"과 "큐"의 차이점을 이해하는 것이 중요합니다. `config/queue.php` 구성 파일에는 `connections` 구성 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk 또는 Redis와 같은 백엔드 큐 서비스에 대한 연결을 정의합니다. 그러나 특정 큐 연결에는 대기 중인 작업의 서로 다른 스택 또는 더미로 간주될 수 있는 여러 개의 "큐"가 있을 수 있습니다.

`queue` 구성 파일의 각 연결 구성 예에는 `queue` 속성이 포함되어 있습니다. 이는 지정된 연결로 전송될 때 작업이 디스패치가 되는 기본 큐입니다. 즉, 어떤 큐를 디스패치로 지정해야 하는지 명시적으로 정의하지 않고 작업을 디스패치하는 경우 작업은 연결 구성의 `queue` 속성에 정의된 큐에 배치됩니다.

```php
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 응용 프로그램은 작업을 여러 큐에 푸시할 필요가 없으며 대신 하나의 간단한 큐를 선호할 수 있습니다. 그러나 작업을 여러 큐에 푸시하는 것은 작업 처리 방법의 우선 순위를 지정하거나 분할하려는 애플리케이션에 특히 유용할 수 있습니다. 예를 들어 작업을 `high` 큐에 푸시하는 경우 더 높은 처리 우선순위를 제공하는 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고 사항 및 전제 조건

<a name="database"></a>
#### 데이터 베이스

`database` 큐 드라이버를 사용하려면 작업을 보관할 데이터베이스 테이블이 필요합니다. 일반적으로 이는 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/13.x/migrations)에 포함되어 있습니다. 그러나 애플리케이션에 이 마이그레이션이 포함되어 있지 않으면 `make:queue-table` Artisan 명령을 사용하여 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 구성 파일에서 Redis 데이터베이스 연결을 구성해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 연결이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우 큐 이름에는 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이는 특정 큐에 대한 모든 Redis 키가 동일한 해시 슬롯에 배치되도록 하기 위해 필요합니다.

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
##### 블로킹

Redis 큐를 사용할 때 `block_for` 구성 옵션을 사용하여 드라이버가 워커 루프를 반복하고 Redis 데이터베이스를 다시 폴링하기 전에 작업이 사용 가능해질 때까지 기다려야 하는 시간을 지정할 수 있습니다.

큐 로드를 기반으로 이 값을 조정하는 것은 새로운 작업에 대해 Redis 데이터베이스를 지속적으로 폴링하는 것보다 더 효율적일 수 있습니다. 예를 들어 작업이 사용 가능해질 때까지 기다리는 동안 드라이버가 5초 동안 차단되어야 함을 나타내기 위해 값을 `5`로 설정할 수 있습니다.

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
> `block_for`를 `0`로 설정하면 작업을 사용할 수 있을 때까지 큐 워커가 무기한 차단됩니다. 이는 또한 다음 작업이 처리될 때까지 `SIGTERM`와 같은 신호가 처리되는 것을 방지합니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 전제 조건

나열된 큐 드라이버에는 다음 종속성이 필요합니다. 이러한 종속성은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

<div class="content-list" markdown="1">

- 아마존 SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 작업 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 작업 클래스 생성

기본적으로 애플리케이션의 큐 가능 작업은 모두 `app/Jobs` 디렉터리에 저장됩니다. `app/Jobs` 디렉터리가 없으면 `make:job` Artisan 명령을 실행할 때 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여 비동기식으로 실행하려면 작업을 큐에 푸시해야 함을 Laravel에 나타냅니다.

> [!NOTE]
> 작업 스텁은 [스텁 게시](/docs/13.x/artisan#stub-customization)를 사용하여 사용자 지정할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

작업 클래스는 매우 간단하며 일반적으로 작업이 큐에 의해 처리될 때 호출되는 `handle` 메서드만 포함합니다. 시작하려면 작업 클래스 예제를 살펴보겠습니다. 이 예에서는 팟캐스트 게시 서비스를 관리하고 업로드된 팟캐스트 파일을 게시하기 전에 처리해야 한다고 가정합니다.

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

이 예에서는 [Eloquent 모델](/docs/13.x/eloquent)를 대기 중인 작업의 생성자에 직접 전달할 수 있었습니다. 작업이 사용하는 `Queueable` 특성으로 인해 Eloquent 모델 및 해당 로드된 관계는 작업이 처리될 때 정상적으로 직렬화되고 직렬화 해제됩니다.

대기 중인 작업이 생성자에서 Eloquent 모델을 허용하는 경우 모델의 식별자만 큐에 직렬화됩니다. 작업이 실제로 처리되면 큐 시스템은 데이터베이스에서 전체 모델 인스턴스와 로드된 관계를 자동으로 다시 검색합니다. 모델 직렬화에 대한 이러한 접근 방식을 사용하면 훨씬 더 작은 작업 페이로드를 큐 드라이버로 보낼 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 종속성 주입

작업이 큐에 의해 처리될 때 `handle` 메서드가 호출됩니다. 작업의 `handle` 메서드에 대한 종속성을 유형 힌트로 표시할 수 있습니다. Laravel [서비스 컨테이너](/docs/13.x/container)는 이러한 종속성을 자동으로 주입합니다.

컨테이너가 `handle` 메서드에 종속성을 주입하는 방법을 완전히 제어하려면 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod` 메서드는 작업 및 컨테이너를 수신하는 콜백을 허용합니다. 콜백 내에서 원하는 대로 `handle` 메서드를 자유롭게 호출할 수 있습니다. 일반적으로 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/13.x/providers)의 `boot` 메서드에서 이 메서드를 호출해야 합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 콘텐츠와 같은 바이너리 데이터는 대기 중인 작업에 전달되기 전에 `base64_encode` 함수를 통해 전달되어야 합니다. 그렇지 않으면 작업이 큐에 배치될 때 JSON로 제대로 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 대기 중인 관계

작업이 큐에 추가되면 로드된 모든 Eloquent 모델 관계도 직렬화되므로 직렬화된 작업 문자열이 때때로 상당히 커질 수 있습니다. 또한 작업이 역직렬화되고 모델 관계가 데이터베이스에서 다시 검색되면 전체가 검색됩니다. 작업 큐 프로세스 중에 모델이 직렬화되기 전에 적용된 이전 관계 제약 조건은 작업이 역직렬화될 때 적용되지 않습니다. 따라서 특정 관계의 하위 집합으로 작업하려면 큐에 있는 작업 내에서 해당 관계를 다시 제한해야 합니다.

또는 관계가 직렬화되는 것을 방지하려면 속성 값을 설정할 때 모델에서 `withoutRelations` 메서드를 호출할 수 있습니다. 이 메서드는 로드된 관계 없이 모델의 인스턴스를 반환합니다.

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

[PHP 생성자 속성 승격](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하고 있고 Eloquent 모델의 관계가 직렬화되어서는 안 된다는 것을 표시하고 싶다면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

편의를 위해 관계 없이 모든 모델을 직렬화하려는 경우 각 모델에 속성을 적용하는 대신 전체 클래스에 `WithoutRelations` 속성을 적용할 수 있습니다.

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

작업이 단일 모델 대신 Eloquent 모델의 컬렉션 또는 배열을 수신하는 경우 해당 컬렉션 내의 모델은 작업이 역직렬화되고 실행될 때 관계가 복원되지 않습니다. 이는 대량의 모델을 처리하는 작업에서 과도한 리소스 사용을 방지하기 위한 것입니다.

<a name="unique-jobs"></a>
### 고유 작업

> [!WARNING]
> 고유한 작업에는 [잠금](/docs/13.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file` 및 `array` 캐시 드라이버는 원자 잠금을 지원합니다.

> [!WARNING]
> 고유한 작업 제약 조건은 배치 내의 작업에 적용되지 않습니다.

때로는 특정 작업의 인스턴스 하나만 특정 시점에 큐에 있는지 확인하고 싶을 수도 있습니다. 작업 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스에서는 클래스에 추가 메서드를 정의할 필요가 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위의 예에서 `UpdateSearchIndex` 작업은 고유합니다. 따라서 작업의 다른 인스턴스가 이미 큐에 있고 처리가 완료되지 않은 경우 작업은 디스패치가 아닙니다.

어떤 경우에는 작업을 고유하게 만드는 특정 "키"를 정의하거나 작업이 더 이상 고유한 상태를 유지하지 않는 시간 초과를 지정할 수 있습니다. 이를 위해 작업 클래스에 `UniqueFor` 속성을 사용하고 `uniqueId` 메서드를 정의할 수 있습니다.

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

위 예에서 `UpdateSearchIndex` 작업은 제품 ID를 기준으로 고유합니다. 따라서 동일한 제품 ID를 가진 작업이 새로 디스패치되면 기존 작업의 처리가 끝날 때까지 무시됩니다. 또한 기존 작업이 1시간 이내에 처리되지 않으면 고유 잠금이 해제되어 동일한 고유 키를 가진 다른 작업을 다시 큐에 디스패치할 수 있습니다.

> [!WARNING]
> 여러 웹 서버 또는 컨테이너에서 애플리케이션 디스패치 작업을 사용하는 경우 Laravel가 작업이 고유한지 정확하게 확인할 수 있도록 모든 서버가 동일한 중앙 캐시 서버와 통신하는지 확인해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리가 시작될 때까지 작업을 고유하게 유지

기본적으로 고유한 작업은 작업이 처리를 완료하거나 모든 재시도 시도에 실패한 후 "잠금 해제"됩니다. 그러나 작업이 처리되기 직전에 잠금 해제되기를 원하는 상황이 있을 수 있습니다. 이를 달성하려면 작업은 `ShouldBeUnique` 계약 대신 `ShouldBeUniqueUntilProcessing` 계약을 구현해야 합니다.

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
#### 고유한 작업 잠금 장치

뒤에서는 `ShouldBeUnique` 작업이 디스패치일 때 Laravel가 `uniqueId` 키를 사용하여 [잠금](/docs/13.x/cache#atomic-locks)을 획득하려고 시도합니다. 잠금이 이미 유지된 경우 작업은 디스패치가 아닙니다. 이 잠금은 작업이 처리를 완료하거나 모든 재시도 시도에 실패하면 해제됩니다. 기본적으로 Laravel는 기본 캐시 드라이버를 사용하여 이 잠금을 획득합니다. 그러나 잠금 획득을 위해 다른 드라이버를 사용하려는 경우 사용해야 하는 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다.

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
> 작업의 동시 처리만 제한해야 하는 경우 [WithoutOverlapping](/docs/13.x/queues#preventing-job-overlaps) 작업 미들웨어를 대신 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 작업

Laravel을 사용하면 [암호화](/docs/13.x/encryption)를 통해 작업 데이터의 개인정보 보호와 무결성을 보장할 수 있습니다. 시작하려면 작업 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 이 인터페이스가 클래스에 추가되면 Laravel는 작업을 큐에 푸시하기 전에 자동으로 암호화합니다.

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
## 작업 미들웨어 (Job Middleware)

작업 미들웨어를 사용하면 큐에 있는 작업 실행에 대한 사용자 지정 논리를 래핑하여 작업 자체의 상용구를 줄일 수 있습니다. 예를 들어, Laravel의 Redis 속도 제한 기능을 활용하여 5초마다 하나의 작업만 처리할 수 있도록 하는 다음 `handle` 메서드를 고려해 보세요.

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

이 코드는 유효하지만 `handle` 메서드의 구현은 Redis 속도 제한 논리로 인해 복잡해지기 때문에 잡음이 발생합니다. 또한 이 속도 제한 논리는 속도를 제한하려는 다른 작업에 대해 복제되어야 합니다. 핸들 메서드의 속도 제한 대신 속도 제한을 처리하는 작업 미들웨어를 정의할 수 있습니다.

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

보시다시피 [라우트 미들웨어](/docs/13.x/middleware), 작업 미들웨어는 처리 중인 작업과 작업 처리를 계속하기 위해 호출해야 하는 콜백을 수신합니다.

`make:job-middleware` Artisan 명령을 사용하여 새 작업 미들웨어 클래스를 생성할 수 있습니다. 작업 미들웨어를 생성한 후 작업의 `middleware` 메서드에서 반환하여 작업에 연결할 수 있습니다. 이 메서드는 `make:job` Artisan 명령으로 스캐폴드된 작업에 존재하지 않으므로 작업 클래스에 수동으로 추가해야 합니다.

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
> 작업 미들웨어는 [큐에 넣을 수 있는 이벤트 리스너](/docs/13.x/events#queued-event-listeners), [메일 가능 항목](/docs/13.x/mail#queueing-mail) 및 [알림](/docs/13.x/notifications#queueing-notifications)에 할당할 수도 있습니다.

<a name="rate-limiting"></a>
### 속도 제한

방금 속도 제한 작업 미들웨어를 작성하는 방법을 시연했지만, Laravel에는 실제로 작업 속도 제한에 활용할 수 있는 속도 제한 미들웨어가 포함되어 있습니다. [라우트 속도 제한기](/docs/13.x/routing#defining-rate-limiters)와 마찬가지로 작업 속도 제한기는 `RateLimiter` 파사드의 `for` 메서드를 사용하여 정의됩니다.

예를 들어, 프리미엄 고객에게는 제한을 두지 않고 사용자가 시간당 한 번씩 데이터를 백업하도록 허용할 수 있습니다. 이를 수행하려면 `AppServiceProvider`의 `boot` 메서드에서 `RateLimiter`를 정의하면 됩니다.

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

위의 예에서는 시간당 요금 제한을 정의했습니다. 그러나 `perMinute` 메서드를 사용하면 분을 기준으로 속도 제한을 쉽게 정의할 수 있습니다. 또한 속도 제한의 `by` 메서드에 원하는 값을 전달할 수 있습니다. 그러나 이 값은 고객별로 비율 제한을 분할하는 데 가장 자주 사용됩니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한을 정의한 후에는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하여 속도 제한기를 작업에 연결할 수 있습니다. 작업이 속도 제한을 초과할 때마다 이 미들웨어는 속도 제한 기간에 따라 적절한 지연을 통해 작업을 큐로 다시 해제합니다.

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

속도가 제한된 작업을 큐에 다시 릴리스하면 작업의 총 `attempts` 수가 계속 증가합니다. 그에 따라 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 조정할 수 있습니다. 또는 [retryUntil 메서드](#time-based-attempts)를 사용하여 작업이 더 이상 시도되지 않을 때까지의 시간을 정의할 수 있습니다.

`releaseAfter` 메서드를 사용하면 릴리스된 작업이 다시 시도되기 전에 경과해야 하는 시간(초)을 지정할 수도 있습니다.

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

속도가 제한되어 있을 때 작업을 재시도하지 않으려면 `dontRelease` 메서드를 사용할 수 있습니다.

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
#### Redis를 사용한 속도 제한

Redis를 사용하는 경우 Redis에 맞게 미세 조정되고 기본 속도 제한 미들웨어보다 더 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

`connection` 메서드는 미들웨어가 사용해야 하는 Redis 연결을 지정하는 데 사용될 수 있습니다.

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a name="preventing-job-overlaps"></a>
### 작업 중복 방지

Laravel에는 임의의 키를 기반으로 작업 중복을 방지할 수 있는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 포함되어 있습니다. 이는 큐에 있는 작업이 한 번에 하나의 작업에 의해서만 수정되어야 하는 리소스를 수정할 때 도움이 될 수 있습니다.

예를 들어 사용자의 신용 점수를 업데이트하는 대기 중인 작업이 있고 동일한 사용자 ID에 대해 신용 점수 업데이트 작업이 겹치는 것을 방지하려고 한다고 가정해 보겠습니다. 이를 수행하려면 작업의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하면 됩니다.

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

겹치는 작업을 큐에 다시 놓아도 작업의 총 시도 횟수는 계속 증가합니다. 이에 따라 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 조정할 수 있습니다. 예를 들어 기본값인 `Tries`를 1로 두면 나중에 작업이 중복되더라도 재시도되지 않습니다.

동일한 유형의 중복된 작업은 큐로 다시 릴리스됩니다. 릴리스된 작업이 다시 시도되기 전에 경과해야 하는 시간(초)을 지정할 수도 있습니다.

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

중복되는 작업을 즉시 삭제하여 재시도되지 않도록 하려면 `dontRelease` 메서드를 사용할 수 있습니다.

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

`WithoutOverlapping` 미들웨어는 Laravel의 원자 잠금 기능으로 구동됩니다. 때로는 작업이 예기치 않게 실패하거나 시간 초과되어 잠금이 해제되지 않을 수도 있습니다. 따라서 `expireAfter` 메서드를 사용하여 잠금 만료 시간을 명시적으로 정의할 수 있습니다. 예를 들어, 아래 예에서는 작업이 처리를 시작한 후 3분 후에 `WithoutOverlapping` 잠금을 해제하도록 Laravel에 지시합니다.

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
> `WithoutOverlapping` 미들웨어에는 [잠금](/docs/13.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file` 및 `array` 캐시 드라이버는 원자 잠금을 지원합니다.

<a name="sharing-lock-keys"></a>
#### 작업 클래스 전체에서 잠금 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 작업 중첩을 방지합니다. 따라서 두 개의 다른 작업 클래스가 동일한 잠금 키를 사용할 수 있지만 중복되는 것은 방지되지 않습니다. 그러나 `shared` 메서드를 사용하여 작업 클래스 전체에 키를 적용하도록 Laravel에 지시할 수 있습니다.

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
### 제한 예외

Laravel에는 예외를 제한할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 포함되어 있습니다. 작업이 지정된 수의 예외를 발생시키면 작업을 실행하려는 모든 추가 시도는 지정된 시간 간격이 경과할 때까지 지연됩니다. 이 미들웨어는 불안정한 타사 서비스와 상호 작용하는 작업에 특히 유용합니다.

예를 들어 예외를 발생시키기 시작하는 타사 API와 상호 작용하는 대기 중인 작업을 상상해 보겠습니다. 예외를 조절하려면 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 일반적으로 이 미들웨어는 [시간 기반 시도](#time-based-attempts)를 구현하는 작업과 쌍을 이루어야 합니다.

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

미들웨어에서 허용하는 첫 번째 생성자 인수는 조절되기 전에 작업이 발생할 수 있는 예외 수이고, 두 번째 생성자 인수는 조절된 후 작업이 다시 시도되기 전에 경과해야 하는 시간(초)입니다. 위의 코드 예제에서 작업이 10개의 연속 예외를 발생시키는 경우 30분 시간 제한으로 인해 작업을 다시 시도하기 전에 5분을 기다립니다.

작업에서 예외가 발생했지만 예외 임계값에 아직 도달하지 않은 경우 일반적으로 작업이 즉시 재시도됩니다. 그러나 미들웨어를 작업에 연결할 때 `backoff` 메서드를 호출하여 작업이 지연되어야 하는 시간(분)을 지정할 수 있습니다.

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

내부적으로 이 미들웨어는 Laravel의 캐시 시스템을 사용하여 속도 제한을 구현하며 작업의 클래스 이름은 캐시 "키"로 활용됩니다. 미들웨어를 작업에 연결할 때 `by` 메서드를 호출하여 이 키를 재정의할 수 있습니다. 이는 동일한 타사 서비스와 상호 작용하는 여러 작업이 있고 단일 공유 제한을 준수하도록 공통 제한 "버킷"을 공유하려는 경우 유용할 수 있습니다.

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

기본적으로 이 미들웨어는 모든 예외를 제한합니다. 미들웨어를 작업에 연결할 때 `when` 메서드를 호출하여 이 동작을 수정할 수 있습니다. 그러면 `when` 메서드에 제공된 클로저가 `true`를 반환하는 경우에만 예외가 조절됩니다.

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

작업을 큐로 다시 해제하거나 예외를 발생시키는 `when` 메서드과 달리, `deleteWhen` 메서드를 사용하면 주어진 예외가 발생할 때 작업을 완전히 삭제할 수 있습니다.

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

제한된 예외가 애플리케이션의 예외 처리기에 보고되도록 하려면 미들웨어를 작업에 연결할 때 `report` 메서드를 호출하면 됩니다. 선택적으로 `report` 메서드에 클로저를 제공할 수 있으며, 지정된 클로저가 `true`를 반환하는 경우에만 예외가 보고됩니다.

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
#### Redis를 사용한 제한 예외

Redis를 사용하는 경우 Redis에 맞게 미세 조정되고 기본 예외 조절 미들웨어보다 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

`connection` 메서드는 미들웨어가 사용해야 하는 Redis 연결을 지정하는 데 사용될 수 있습니다.

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a name="skipping-jobs"></a>
### 작업 건너뛰기

`Skip` 미들웨어를 사용하면 작업의 논리를 수정할 필요 없이 작업을 건너뛰거나 삭제해야 함을 지정할 수 있습니다. `Skip::when` 메서드는 주어진 조건이 `true`로 평가되면 작업을 삭제하고, 조건이 `false`로 평가되면 `Skip::unless` 메서드는 작업을 삭제합니다.

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

더 복잡한 조건부 평가를 위해 `Closure`를 `when` 및 `unless` 메서드에 전달할 수도 있습니다.

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
## 디스패치 작업 (Dispatching Jobs)

작업 클래스를 작성한 후에는 작업 자체에서 `dispatch` 메서드를 사용하여 디스패치할 수 있습니다. `dispatch` 메서드에 전달된 인수는 작업의 생성자에 제공됩니다.

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

조건부로 디스패치 및 작업을 수행하려면 `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 Laravel 애플리케이션에서는 `database` 연결이 기본 큐로 정의됩니다. 애플리케이션의 `.env` 파일에서 `QUEUE_CONNECTION` 환경 변수를 변경하여 다른 기본 큐 연결을 지정할 수 있습니다.

<a name="delayed-dispatching"></a>
### 지연된 디스패치

작업을 큐 워커 처리에 즉시 사용할 수 없도록 지정하려면 디스패치가 작업인 경우 `delay` 메서드를 사용할 수 있습니다. 예를 들어 디스패치가 발생한 후 10분이 지나야 작업을 처리할 수 있도록 지정해 보겠습니다.

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

경우에 따라 작업에 기본 지연이 구성되어 있을 수 있습니다. 즉각적인 처리를 위해 이 지연을 우회하고 디스패치 a 작업이 필요한 경우 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스의 최대 지연 시간은 15분입니다.

<a name="synchronous-dispatching"></a>
### 동기식 디스패치

작업을 즉시(동기적으로) 디스패치하려면 `dispatchSync` 메서드를 사용할 수 있습니다. 이 메서드를 사용하면 작업이 큐에 추가되지 않고 현재 프로세스 내에서 즉시 실행됩니다.

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
#### 지연된 디스패치

지연된 동기식 디스패치를 사용하면 현재 프로세스 중에 디스패치 및 작업을 처리할 수 있지만 HTTP 응답이 사용자에게 전송된 후에는 가능합니다. 이를 통해 사용자의 애플리케이션 경험을 저하시키지 않고 "큐에 있는" 작업을 동기식으로 처리할 수 있습니다. 동기식 작업, 디스패치 및 작업의 실행을 `deferred` 연결로 연기하려면 다음을 수행하세요.

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```

`deferred` 연결은 기본 [장애 조치 큐](#queue-failover) 역할도 합니다.

마찬가지로 HTTP 응답이 사용자에게 전송된 후 `background` 연결은 작업을 처리합니다. 그러나 작업은 별도로 생성된 PHP 프로세스에서 처리되므로 PHP-FPM/애플리케이션 워커를 사용하여 들어오는 다른 HTTP 요청을 처리할 수 있습니다.

```php
RecordDelivery::dispatch($order)->onConnection('background');
```

<a name="jobs-and-database-transactions"></a>
### 작업 및 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 디스패치 작업에는 문제가 없지만 작업이 실제로 성공적으로 실행될 수 있도록 특별한 주의를 기울여야 합니다. 트랜잭션 내에서 디스패치가 작업인 경우 상위 트랜잭션이 커밋되기 전에 작업이 워커에 의해 처리될 수 있습니다. 이런 일이 발생하면 데이터베이스 트랜잭션 중에 모델 또는 데이터베이스 레코드에 대해 수행한 업데이트가 아직 데이터베이스에 반영되지 않을 수 있습니다. 또한 트랜잭션 내에서 생성된 모델 또는 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수도 있습니다.

다행히 Laravel는 이 문제를 해결하는 여러 가지 방법을 제공합니다. 먼저 큐 연결의 구성 배열에서 `after_commit` 연결 옵션을 설정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`인 경우 데이터베이스 트랜잭션 내에서 디스패치 작업을 수행할 수 있습니다. 그러나 Laravel는 실제로 작업을 디스패치하기 전에 열린 상위 데이터베이스 트랜잭션이 커밋될 때까지 기다립니다. 물론 현재 열려 있는 데이터베이스 트랜잭션이 없으면 작업은 즉시 디스패치가 됩니다.

트랜잭션 중 발생한 예외로 인해 트랜잭션이 롤백되는 경우 해당 트랜잭션 중 디스패치였던 작업은 삭제됩니다.

> [!NOTE]
> `after_commit` 구성 옵션을 `true`로 설정하면 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후 큐에 있는 모든 이벤트 리스너, 메일 가능 항목, 알림 및 브로드캐스트 이벤트가 디스패치가 됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 디스패치 동작 인라인 지정

`after_commit` 큐 연결 구성 옵션을 `true`로 설정하지 않은 경우 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후에도 특정 작업이 디스패치여야 함을 나타낼 수 있습니다. 이를 달성하려면 `afterCommit` 메서드를 디스패치 작업에 연결할 수 있습니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

마찬가지로, `after_commit` 구성 옵션이 `true`로 설정된 경우 열려 있는 데이터베이스 트랜잭션이 커밋될 때까지 기다리지 않고 특정 작업이 즉시 디스패치가 되어야 함을 나타낼 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체인

작업 체인을 사용하면 기본 작업이 성공적으로 실행된 후 순서대로 실행되어야 하는 대기 중인 작업 목록을 지정할 수 있습니다. 시퀀스의 작업 하나가 실패하면 작업의 나머지 부분은 실행되지 않습니다. 큐에 있는 작업 체인을 실행하려면 `Bus` 파사드에서 제공하는 `chain` 메서드를 사용할 수 있습니다. Laravel의 명령 버스는 대기 중인 하위 수준 컴포넌트입니다. 작업 디스패치는 다음 요소 위에 구축됩니다.

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

작업 클래스 인스턴스를 연결하는 것 외에도 클로저를 연결할 수도 있습니다.

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
> 작업 내에서 `$this->delete()` 메서드를 사용하여 작업을 삭제해도 연결된 작업이 처리되는 것을 방지할 수 없습니다. 체인의 작업이 실패하는 경우에만 체인 실행이 중지됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐

연결된 작업에 사용해야 하는 연결 및 큐를 지정하려면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 이러한 방법은 대기 중인 작업이 명시적으로 다른 연결/큐에 할당되지 않는 한 사용해야 하는 큐 연결 및 큐 이름을 지정합니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가

경우에 따라 해당 체인의 다른 작업 내에서 기존 작업 체인에 작업을 추가하거나 추가해야 할 수도 있습니다. `prependToChain` 및 `appendToChain` 메서드를 사용하여 이 작업을 수행할 수 있습니다.

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
#### 체인 실패

작업을 연결할 때 `catch` 메서드를 사용하여 체인 내의 작업이 실패할 경우 호출되어야 하는 클로저를 지정할 수 있습니다. 지정된 콜백은 작업 오류를 일으킨 `Throwable` 인스턴스를 수신합니다.

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
> 체인 콜백은 나중에 Laravel 큐에 의해 직렬화되고 실행되므로 체인 콜백 내에서 `$this` 변수를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 연결 사용자 지정

<a name="dispatching-to-a-particular-queue"></a>
#### 디스패치를 특정 큐로

작업을 다른 큐에 푸시하면 큐에 있는 작업을 "분류"할 수 있으며 다양한 큐에 할당하는 워커 수의 우선 순위를 지정할 수도 있습니다. 이는 작업을 큐 구성 파일에 정의된 다른 큐 "연결"로 푸시하는 것이 아니라 단일 연결 내의 특정 큐에만 푸시한다는 점을 명심하세요. 큐를 지정하려면 디스패치가 작업일 때 `onQueue` 메서드를 사용하세요.

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

또는 작업 생성자 내에서 `onQueue` 메서드를 호출하여 작업의 큐를 지정할 수도 있습니다.

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
#### 디스패치를 특정 연결로

애플리케이션이 여러 큐 연결과 상호 작용하는 경우 `onConnection` 메서드를 사용하여 작업을 푸시할 연결을 지정할 수 있습니다.

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

작업에 대한 연결과 큐를 지정하기 위해 `onConnection` 및 `onQueue` 메서드를 함께 연결할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는 작업 생성자 내에서 `onConnection` 메서드를 호출하여 작업의 연결을 지정할 수도 있습니다.

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
#### 큐 라우팅

`Queue` 파사드의 `route` 메서드를 사용하면 특정 작업 클래스에 대한 기본 연결과 큐를 정의할 수 있습니다. 이는 개별 작업마다 연결이나 큐를 지정하지 않고도 특정 작업이 항상 지정된 큐를 사용하도록 보장하고 싶을 때 유용합니다.

특정 작업 클래스뿐 아니라 인터페이스, 트레이트, 부모 클래스도 `route` 메서드에 전달할 수 있습니다. 이렇게 하면 해당 인터페이스를 구현하거나, 트레이트를 사용하거나, 부모 클래스를 확장하는 모든 작업이 자동으로 구성된 연결과 큐를 사용하게 됩니다.

일반적으로 `route` 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 좋습니다:

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

큐 이름 없이 연결만 지정하면 해당 작업은 기본 큐로 전송됩니다:

```php
Queue::route(ProcessPodcast::class, connection: 'redis');
```

배열을 전달하여 여러 작업 클래스를 한 번에 라우팅할 수도 있습니다:

```php
Queue::route([
    ProcessPodcast::class => ['podcasts', 'redis'], // Queue and connection
    ProcessVideo::class => 'videos', // Queue only (uses default connection)
]);
```

> [!NOTE]
> 큐 라우팅은 여전히 작업 단위로 개별 오버라이드할 수 있습니다.

<a name="max-job-attempts-and-timeout"></a>
### 최대 작업 시도 횟수/시간 초과 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수

작업 시도는 Laravel 큐 시스템의 핵심 개념이며 많은 고급 기능을 지원합니다. 처음에는 혼란스러워 보일 수 있지만 기본 구성을 수정하기 전에 작동 방식을 이해하는 것이 중요합니다.

작업이 디스패치이면 큐로 푸시됩니다. 그러면 워커가 이를 선택하여 실행을 시도합니다. 이것은 작업 시도입니다.

그러나 시도가 반드시 작업의 `handle` 메서드가 실행되었음을 의미하는 것은 아닙니다. 시도는 여러 가지 방법으로 "소모"될 수도 있습니다.

<div class="content-list" markdown="1">

- 작업은 실행 중에 처리되지 않은 예외가 발생합니다.
- 작업은 `$this->release()`를 사용하여 수동으로 큐로 다시 해제됩니다.
- `WithoutOverlapping` 또는 `RateLimited`와 같은 미들웨어는 잠금 획득에 실패하고 작업을 해제합니다.
- 작업이 시간 초과되었습니다.
- 작업의 `handle` 메서드는 예외를 발생시키지 않고 실행되고 완료됩니다.

</div>

작업을 무기한으로 계속 시도하고 싶지는 않을 것입니다. 따라서 Laravel는 작업을 시도할 수 있는 횟수 또는 기간을 지정하는 다양한 방법을 제공합니다.

> [!NOTE]
> 기본적으로 Laravel는 작업을 한 번만 시도합니다. 작업이 `WithoutOverlapping` 또는 `RateLimited`와 같은 미들웨어를 사용하거나 작업을 수동으로 해제하는 경우 `tries` 옵션을 통해 허용되는 시도 횟수를 늘려야 할 가능성이 높습니다.

작업이 시도될 수 있는 최대 횟수를 지정하는 한 가지 방법은 Artisan 명령줄의 `--tries` 스위치를 사용하는 것입니다. 이는 처리 중인 작업이 시도할 수 있는 횟수를 지정하지 않는 한 워커에서 처리되는 모든 작업에 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면 "실패한" 작업으로 간주됩니다. 실패한 작업 처리에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참조하세요. `--tries=0`가 `queue:work` 명령에 제공되면 작업이 무기한 재시도됩니다.

작업 클래스 자체에서 `Tries` 속성을 사용해 작업이 시도될 수 있는 최대 횟수를 정의하면 보다 세밀하게 제어할 수 있습니다. 작업에 최대 시도 횟수가 지정된 경우 명령줄에 제공된 `--tries` 값보다 우선합니다.

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

특정 작업의 최대 시도 횟수에 대한 동적 제어가 필요한 경우 작업에 `tries` 메서드를 정의할 수 있습니다.

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
#### 시간 기반 시도

작업이 실패하기 전에 시도할 수 있는 횟수를 정의하는 대신 작업을 더 이상 시도하지 않아야 하는 시간을 정의할 수 있습니다. 이를 통해 주어진 시간 내에 작업을 여러 번 시도할 수 있습니다. 작업을 더 이상 시도하지 않아야 하는 시간을 정의하려면 작업 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

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

`retryUntil` 및 `tries`가 모두 정의된 경우 Laravel는 `retryUntil` 메서드에 우선 순위를 부여합니다.

> [!NOTE]
> [대기 중인 이벤트 리스너](/docs/13.x/events#queued-event-listeners) 및 [대기 중인 알림](/docs/13.x/notifications#queueing-notifications)에는 `Tries` 속성 또는 `retryUntil` 메서드를 정의할 수도 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외

때로는 작업을 여러 번 시도할 수 있지만 지정된 수의 처리되지 않은 예외에 의해 재시도가 트리거되는 경우, 즉 `release` 메서드로 직접 해제된 경우가 아니라면 실패하도록 지정하고 싶을 수 있습니다. 이를 위해 작업 클래스에 `Tries` 및 `MaxExceptions` 속성을 사용할 수 있습니다.

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

이 예에서는 애플리케이션이 Redis 잠금을 얻을 수 없는 경우 작업이 10초 동안 해제되고 최대 25회까지 계속 재시도됩니다. 그러나 작업에서 처리되지 않은 세 가지 예외가 발생하면 작업이 실패합니다.

<a name="timeout"></a>
#### 시간 초과

큐에 있는 작업의 예상 소요 시간을 대략적으로 아는 경우가 많습니다. 이러한 이유로 Laravel을 사용하면 "시간 초과" 값을 지정할 수 있습니다. 기본적으로 시간 초과 값은 60초입니다. 작업이 시간 초과 값으로 지정된 시간(초)보다 오랫동안 처리하는 경우 작업을 처리하는 워커는 오류와 함께 종료됩니다. 일반적으로 워커는 [서버에 구성된 프로세스 관리자](#supervisor-configuration)에 의해 자동으로 다시 시작됩니다.

작업이 실행할 수 있는 최대 시간(초)은 Artisan 명령줄의 `--timeout` 스위치를 사용하여 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 지속적으로 시간 초과되어 최대 시도 횟수를 초과하는 경우 실패한 것으로 표시됩니다.

또한 작업 클래스에 `Timeout` 속성을 사용해 작업 실행을 허용할 최대 시간(초)을 정의할 수도 있습니다. 작업에 시간 초과가 지정된 경우 명령줄에 지정된 시간 초과보다 우선합니다.

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

때로는 소켓이나 나가는 HTTP 연결과 같은 IO 차단 프로세스가 지정된 시간 초과를 준수하지 않을 수 있습니다. 따라서 이러한 기능을 사용할 때는 항상 해당 API를 사용하여 시간 제한을 지정해야 합니다. 예를 들어 [Guzzle](https://docs.guzzlephp.org)를 사용하는 경우 항상 연결 및 요청 시간 초과 값을 지정해야 합니다.

> [!WARNING]
> 작업 시간 제한을 지정하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장을 설치해야 합니다. 또한 작업의 "시간 초과" 값은 항상 ["재시도"](#job-expiration) 값보다 작아야 합니다. 그렇지 않으면 실제로 실행이 완료되거나 시간이 초과되기 전에 작업이 다시 시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 시간 초과로 인한 실패

시간 초과 시 작업이 [실패](#dealing-with-failed-jobs)로 표시되어야 함을 나타내려면 작업 클래스에 `FailOnTimeout` 속성을 사용할 수 있습니다.

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
> 기본적으로 작업이 시간 초과되면 한 번의 시도를 소비하고 큐로 다시 해제됩니다(재시도가 허용되는 경우). 그러나 시간 초과 시 실패하도록 작업을 구성하면 시도에 설정된 값에 관계없이 재시도되지 않습니다.

<a name="sqs-fifo-and-fair-queues"></a>
### SQS FIFO 및 공정한 큐

Laravel는 [Amazon SQS FIFO(선입선출)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) 큐를 지원하므로 메시지 중복 제거를 통해 정확히 한 번만 처리하는 동시에 전송된 정확한 순서대로 작업을 처리할 수 있습니다.

FIFO 큐에는 병렬로 처리할 수 있는 작업을 결정하기 위해 메시지 그룹 ID가 필요합니다. 동일한 그룹 ID를 가진 작업은 순차적으로 처리되고, 다른 그룹 ID를 가진 메시지는 동시에 처리될 수 있습니다.

Laravel는 디스패치 작업일 때 메시지 그룹 ID를 지정하는 유연한 `onGroup` 메서드를 제공합니다.

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```

SQS FIFO 큐는 메시지 중복 제거를 지원하여 정확히 한 번만 처리되도록 보장합니다. 사용자 지정 중복 제거 ID를 제공하려면 작업 클래스에서 `deduplicationId` 메서드를 구현하십시오.

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

<a name="fifo-listeners-mail-and-notifications"></a>
#### FIFO 리스너, 메일 및 알림

FIFO 큐를 활용하는 경우 리스너, 메일 및 알림에 대한 메시지 그룹도 정의해야 합니다. 또는 이러한 개체의 큐에 있는 인스턴스를 디스패치하여 비FIFO 큐로 보낼 수 있습니다.

[큐에 있는 이벤트 리스너](/docs/13.x/events#queued-event-listeners)에 대한 메시지 그룹을 정의하려면 리스너에 `messageGroup` 메서드를 정의하세요. 선택적으로 `deduplicationId` 메서드를 정의할 수도 있습니다.

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

FIFO 큐에 대기할 [메일 메시지](/docs/13.x/mail)를 보낼 때 알림을 보낼 때 `onGroup` 메서드를 호출하고 선택적으로 `withDeduplicator` 메서드를 호출해야 합니다.

```php
use App\Mail\InvoicePaid;
use Illuminate\Support\Facades\Mail;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```

FIFO 큐에 대기할 [알림](/docs/13.x/notifications)을 보낼 때 알림을 보낼 때 `onGroup` 메서드를 호출하고 선택적으로 `withDeduplicator` 메서드를 호출해야 합니다.

```php
use App\Notifications\InvoicePaid;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```

<a name="queue-failover"></a>
### 큐 장애 조치

`failover` 큐 드라이버는 작업을 큐에 푸시할 때 자동 장애 조치 기능을 제공합니다. 어떤 이유로든 `failover` 구성의 기본 큐 연결이 실패하면 Laravel는 자동으로 작업을 목록의 다음 구성된 연결로 푸시하려고 시도합니다. 이는 큐 신뢰성이 중요한 생산 환경에서 고가용성을 보장하는 데 특히 유용합니다.

장애 조치 큐 연결을 구성하려면 `failover` 드라이버를 지정하고 순서대로 시도할 연결 이름 배열을 제공합니다. 기본적으로 Laravel에는 애플리케이션의 `config/queue.php` 구성 파일에 장애 조치 구성 예시가 포함되어 있습니다.

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

`failover` 드라이버를 사용하는 연결을 구성한 후에는 장애 조치 기능을 활용하려면 애플리케이션의 `.env` 파일에서 장애 조치 연결을 기본 큐 연결로 설정해야 합니다.

```ini
QUEUE_CONNECTION=failover
```

그런 다음 장애 조치 연결 목록의 각 연결에 대해 하나 이상의 워커를 시작합니다.

```bash
php artisan queue:work redis
php artisan queue:work database
```

> [!NOTE]
> 드라이버가 현재 PHP 프로세스 내에서 작업을 처리하므로 `sync`, `background` 또는 `deferred` 큐 드라이버를 사용하여 연결하는 경우 워커를 실행할 필요가 없습니다.

큐 연결 작업이 실패하고 장애 조치가 활성화되면 Laravel는 디스패치를 `Illuminate\Queue\Events\QueueFailedOver` 이벤트로 지정하여 큐 연결이 실패했음을 보고하거나 기록할 수 있습니다.

> [!NOTE]
> Laravel Horizon를 사용하는 경우 Horizon는 Redis 큐만 관리한다는 점을 기억하세요. 장애 조치 목록에 `database`가 포함된 경우 Horizon와 함께 일반 `php artisan queue:work database` 프로세스를 실행해야 합니다.

<a name="error-handling"></a>
### 오류 처리

작업이 처리되는 동안 예외가 발생하면 작업이 자동으로 큐로 다시 해제되어 다시 시도할 수 있습니다. 작업은 애플리케이션에서 허용하는 최대 횟수까지 시도될 때까지 계속해서 릴리스됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령에 사용되는 `--tries` 스위치에 의해 정의됩니다. 또는 작업 클래스 자체에서 최대 시도 횟수를 정의할 수도 있습니다. 큐 워커 실행에 대한 자세한 내용은 [아래에서 확인할 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업 수동 해제

때로는 나중에 다시 시도할 수 있도록 수동으로 작업을 큐에 다시 릴리스할 수도 있습니다. `release` 메서드를 호출하여 이를 수행할 수 있습니다:

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

기본적으로 `release` 메서드은 즉각적인 처리를 위해 작업을 다시 큐로 해제합니다. 그러나 정수 또는 날짜 인스턴스를 `release` 메서드에 전달하여 지정된 시간(초)이 경과할 때까지 작업을 처리할 수 없도록 큐에 지시할 수 있습니다.

```php
$this->release(10);

$this->release(now()->plus(seconds: 10));
```

<a name="manually-failing-a-job"></a>
#### 작업 수동 실패

때때로 작업을 "실패"로 수동으로 표시해야 할 수도 있습니다. 그렇게 하려면 `fail` 메서드를 호출하면 됩니다:

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

발생한 예외로 인해 작업을 실패한 것으로 표시하려면 해당 예외를 `fail` 메서드에 전달할 수 있습니다. 또는 편의를 위해 예외로 변환될 문자열 오류 메시지를 전달할 수도 있습니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 자세한 내용은 [작업 실패 처리에 대한 문서](#dealing-with-failed-jobs)를 확인하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외로 인해 작업 실패

`FailOnException` [작업 미들웨어](#job-middleware)를 사용하면 특정 예외가 발생할 때 단락 재시도를 수행할 수 있습니다. 이를 통해 외부 API 오류와 같은 일시적인 예외에 대해 재시도할 수 있지만 사용자 권한 취소와 같은 지속적인 예외에 대해서는 영구적으로 작업에 실패할 수 있습니다.

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

class SyncChatHistory implements ShouldQueue
{
    use Queueable;

    public $tries = 3;

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
## 작업 배치 (Job Batching)

Laravel의 작업 배치 기능을 사용하면 작업의 배치를 쉽게 실행한 다음 작업의 배치 실행이 완료되면 일부 작업을 수행할 수 있습니다. 시작하기 전에 마이그레이션 데이터베이스를 생성하여 완료율과 같은 작업 배치에 대한 메타 정보가 포함된 테이블을 구축해야 합니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령을 사용하여 생성될 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능 작업 정의

배치 가능 작업을 정의하려면 정상적으로 [큐에 넣을 수 있는 작업을 생성](#creating-jobs)해야 합니다. 그러나 작업 클래스에 `Illuminate\Bus\Batchable` 특성을 추가해야 합니다. 이 특성은 작업이 실행 중인 현재 배치를 검색하는 데 사용할 수 있는 `batch` 메서드에 대한 액세스를 제공합니다.

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
### 디스패치 배치

디스패치 또는 작업의 배치를 수행하려면 `Bus` 파사드의 `batch` 메서드를 사용해야 합니다. 물론 배치는 완료 콜백과 결합될 때 주로 유용합니다. 따라서 `then`, `catch` 및 `finally` 메서드를 사용하여 배치에 대한 완료 콜백을 정의할 수 있습니다. 이러한 각 콜백은 호출될 때 `Illuminate\Bus\Batch` 인스턴스를 수신합니다.

여러 개의 큐 워커를 실행하는 경우 배치의 작업이 병렬로 처리됩니다. 따라서 작업이 완료되는 순서는 배치에 추가된 순서와 동일하지 않을 수 있습니다. 일련의 작업을 순서대로 실행하는 방법에 대한 자세한 내용은 [작업 체인 및 배치](#chains-and-batches)에 대한 설명서를 참조하세요.

이 예에서는 각각 CSV 파일에서 지정된 수의 행을 처리하는 작업의 배치를 큐에 추가한다고 가정합니다.

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

`$batch->id` 속성을 통해 액세스할 수 있는 배치의 ID는 디스패치가 된 후 배치에 대한 정보를 얻기 위해 [쿼리 Laravel 명령 버스](#inspecting-batches)에 사용될 수 있습니다.

> [!WARNING]
> 배치 콜백은 나중에 Laravel 큐에 의해 직렬화되고 실행되므로 콜백 내에서 `$this` 변수를 사용하면 안 됩니다. 또한 배치 처리된 작업은 데이터베이스 트랜잭션 내에 래핑되므로 암시적 커밋을 트리거하는 데이터베이스 문은 작업 내에서 실행되어서는 안 됩니다.

<a name="naming-batches"></a>
#### 배치로 명명

[Laravel Horizon](/docs/13.x/horizon) 및 [Laravel 망원경](/docs/13.x/telescope)과 같은 일부 도구는 배치라는 이름이 지정된 경우 배치에 대한 보다 사용자 친화적인 디버그 정보를 제공할 수 있습니다. 배치에 임의의 이름을 할당하려면 배치를 정의하는 동안 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 연결 및 큐

배치 처리된 작업에 사용해야 하는 연결 및 큐를 지정하려면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 배치 처리된 모든 작업은 동일한 연결 및 큐 내에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인 및 배치

배열 내에 연결된 작업을 배치하여 배치 내에서 [연결된 작업](#job-chaining) 집합을 정의할 수 있습니다. 예를 들어 두 개의 작업 체인을 병렬로 실행하고 두 작업 체인 모두 처리가 완료되면 콜백을 실행할 수 있습니다.

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

반대로 체인 내에서 배치를 정의하여 [체인](#job-chaining) 내에서 작업의 배치를 실행할 수 있습니다. 예를 들어, 먼저 작업의 배치를 실행하여 여러 팟캐스트를 릴리스한 다음 작업의 배치를 실행하여 릴리스 알림을 보낼 수 있습니다.

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
### 배치에 작업 추가

때로는 배치 처리된 작업 내에서 배치에 추가 작업을 추가하는 것이 유용할 수 있습니다. 이 패턴은 웹 요청 중에 디스패치에 너무 오랜 시간이 걸릴 수 있는 수천 개의 작업을 배치해야 할 때 유용할 수 있습니다. 따라서 대신 배치를 더 많은 작업으로 수화하는 "로더" 작업의 초기 배치를 디스패치로 설정할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import Contacts')->dispatch();
```

이 예에서는 `LoadImportBatch` 작업을 사용하여 추가 작업으로 배치를 수화합니다. 이를 달성하기 위해 작업의 `batch` 메서드를 통해 액세스할 수 있는 배치 인스턴스에서 `add` 메서드를 사용할 수 있습니다.

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
> 동일한 배치에 속하는 작업 내에서만 작업을 배치에 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 검사

배치 완료 콜백에 제공되는 `Illuminate\Bus\Batch` 인스턴스에는 작업의 지정된 배치와 상호 작용하고 검사하는 데 도움이 되는 다양한 속성과 메서드가 있습니다.

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
#### 라우트에서 배치 반환

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화 가능합니다. 즉, 애플리케이션의 라우트 중 하나에서 직접 반환하여 완료 진행 상황을 포함하여 배치에 대한 정보가 포함된 JSON 페이로드를 검색할 수 있습니다. 이를 통해 애플리케이션 UI에 배치의 완료 진행 상황에 대한 정보를 표시하는 것이 편리합니다.

ID로 배치를 검색하려면 `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소

때로는 특정 배치 실행을 취소해야 할 수도 있습니다. 이는 `Illuminate\Bus\Batch` 인스턴스에서 `cancel` 메서드를 호출하여 수행할 수 있습니다.

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

이전 예에서 알 수 있듯이 배치 처리된 작업은 일반적으로 실행을 계속하기 전에 해당 배치가 취소되었는지 확인해야 합니다. 그러나 편의상 `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 작업에 대신 할당할 수 있습니다. 이름에서 알 수 있듯이 이 미들웨어는 해당 배치가 취소된 경우 작업을 처리하지 않도록 Laravel에 지시합니다.

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
### 배치 실패

배치 처리된 작업이 실패하면 `catch` 콜백(할당된 경우)이 호출됩니다. 이 콜백은 배치 내에서 실패한 첫 번째 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용

배치 내의 작업에 오류가 발생하면 Laravel는 자동으로 배치를 "취소됨"으로 표시합니다. 원하는 경우 작업 오류로 인해 배치가 취소된 것으로 자동으로 표시되지 않도록 이 동작을 비활성화할 수 있습니다. 이는 `allowFailures` 메서드를 호출하고 디스패치는 배치를 호출하여 수행할 수 있습니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->allowFailures()->dispatch();
```

선택적으로 각 작업 실패 시 실행되는 `allowFailures` 메서드에 대한 클로저를 제공할 수 있습니다.

```php
$batch = Bus::batch([
    // ...
])->allowFailures(function (Batch $batch, $exception) {
    // Handle individual job failures...
})->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 재시도 실패 배치 작업

편의를 위해 Laravel는 지정된 배치에 대해 실패한 모든 작업을 쉽게 재시도할 수 있는 `queue:retry-batch` Artisan 명령을 제공합니다. 이 명령은 실패한 작업을 재시도해야 하는 배치의 UUID를 승인합니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 정리

정리하지 않고도 `job_batches` 테이블은 매우 빠르게 레코드를 축적할 수 있습니다. 이 문제를 완화하려면 `queue:prune-batches` Artisan 명령이 매일 실행되도록 [예약](/docs/13.x/scheduling)해야 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로 24시간이 지난 모든 완료된 배치는 정리됩니다. 배치 데이터를 보존할 기간을 결정하기 위해 명령을 호출할 때 `hours` 옵션을 사용할 수 있습니다. 예를 들어, 다음 명령은 48시간 전에 완료된 모든 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

때로는 작업이 실패하고 작업이 성공적으로 재시도되지 않은 배치와 같이 성공적으로 완료되지 않은 배치에 대한 배치 레코드가 `jobs_batches` 테이블에 누적될 수 있습니다. `unfinished` 옵션을 사용하여 완료되지 않은 배치 레코드를 정리하도록 `queue:prune-batches` 명령에 지시할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, `jobs_batches` 테이블에는 취소된 배치에 대한 배치 레코드가 누적될 수도 있습니다. `cancelled` 옵션을 사용하여 취소된 배치 레코드를 정리하도록 `queue:prune-batches` 명령에 지시할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장

Laravel는 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 메타 정보를 저장하는 기능도 지원합니다. 그러나 모든 배치 레코드를 저장하려면 DynamoDB 테이블을 수동으로 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`로 지정되어야 하지만 애플리케이션의 `queue` 구성 파일에 있는 `queue.batching.table` 구성 값을 기반으로 테이블 이름을 지정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

`job_batches` 테이블에는 `application`라는 문자열 기본 파티션 키와 `id`라는 문자열 기본 정렬 키가 있어야 합니다. 키의 `application` 부분에는 애플리케이션의 `app` 구성 파일 내 `name` 구성 값으로 정의된 애플리케이션 이름이 포함됩니다. 애플리케이션 이름은 DynamoDB 테이블 키의 일부이므로 동일한 테이블을 사용하여 여러 Laravel 애플리케이션에 대한 작업 배치를 저장할 수 있습니다.

또한 [자동 배치 정리](#pruning-batches-in-dynamodb)를 활용하려는 경우 테이블에 대해 `ttl` 속성을 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 구성

다음으로, Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

그런 다음 `queue.batching.driver` 구성 옵션의 값을 `dynamodb`로 설정합니다. 또한 `batching` 구성 배열 내에서 `key`, `secret` 및 `region` 구성 옵션을 정의해야 합니다. 이러한 옵션은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용하는 경우 `queue.batching.database` 구성 옵션이 필요하지 않습니다.

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
#### DynamoDB에서 배치 가지치기

[DynamoDB](https://aws.amazon.com/dynamodb)를 활용하여 작업 배치 정보를 저장하는 경우 관계형 데이터베이스에 저장된 배치를 정리하는 데 사용되는 일반적인 정리 명령이 작동하지 않습니다. 대신, [DynamoDB의 기본 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용하여 이전 배치에 대한 기록을 자동으로 제거할 수 있습니다.

`ttl` 속성을 사용하여 DynamoDB 테이블을 정의한 경우 구성 매개변수를 정의하여 Laravel에 배치 레코드 정리 방법을 지시할 수 있습니다. `queue.batching.ttl_attribute` 구성 값은 TTL을 보유하는 속성의 이름을 정의하는 반면, `queue.batching.ttl` 구성 값은 레코드가 마지막으로 업데이트된 시간을 기준으로 배치 레코드가 DynamoDB 테이블에서 제거될 수 있는 시간(초)을 정의합니다.

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
## 큐잉 클로저 (Queueing Closures)

디스패치 클래스를 큐로 변경하는 대신 디스패치 클로저를 사용할 수도 있습니다. 이는 현재 요청 주기 외부에서 실행해야 하는 빠르고 간단한 작업에 적합합니다. 디스패치가 큐에 클로저되면 클로저의 코드 내용이 암호화되어 서명되므로 전송 중에 수정할 수 없습니다.

```php
use App\Models\Podcast;

$podcast = Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐 보고 대시보드에서 사용할 수 있을 뿐만 아니라 `queue:work` 명령으로 표시할 수 있는 큐 종료에 이름을 할당하려면 `name` 메서드를 사용할 수 있습니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

`catch` 메서드를 사용하면 큐의 [구성된 재시도 시도](#max-job-attempts-and-timeout)를 모두 소진한 후 대기 중인 클로저가 성공적으로 완료되지 못한 경우 실행되어야 하는 클로저를 제공할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

> [!WARNING]
> `catch` 콜백은 나중에 Laravel 큐에 의해 직렬화되고 실행되므로 `catch` 콜백 내에서 `$this` 변수를 사용하면 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행 (Running the Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령

Laravel에는 큐 워커를 시작하고 큐에 푸시되는 새 작업을 처리하는 Artisan 명령이 포함되어 있습니다. `queue:work` Artisan 명령을 사용하여 워커를 실행할 수 있습니다. `queue:work` 명령이 시작되면 수동으로 중지하거나 터미널을 닫을 때까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 영구적으로 실행하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용하여 큐 워커 실행이 중지되지 않는지 확인해야 합니다.

처리된 작업 ID, 연결 이름 및 큐 이름을 명령 출력에 포함시키려는 경우 `queue:work` 명령을 호출할 때 `-v` 플래그를 포함할 수 있습니다.

```shell
php artisan queue:work -v
```

큐 워커는 수명이 긴 프로세스이며 부팅된 애플리케이션 상태를 메모리에 저장한다는 점을 기억하세요. 결과적으로 시작된 후에는 코드 베이스의 변경 사항을 알 수 없습니다. 따라서 배포 프로세스 중에 [큐 워커를 다시 시작](#queue-workers-and-deployment)하세요. 또한 애플리케이션에서 생성하거나 수정한 정적 상태는 작업 간에 자동으로 재설정되지 않습니다.

또는 `queue:listen` 명령을 실행할 수도 있습니다. `queue:listen` 명령을 사용할 때 업데이트된 코드를 다시 로드하거나 애플리케이션 상태를 재설정하려는 경우 워커를 수동으로 다시 시작할 필요가 없습니다. 그러나 이 명령은 `queue:work` 명령보다 훨씬 덜 효율적입니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 개의 큐 워커 실행

여러 워커를 큐에 할당하고 작업을 동시에 처리하려면 여러 `queue:work` 프로세스를 시작하기만 하면 됩니다. 이는 터미널의 여러 탭을 통해 로컬로 수행하거나 프로세스 관리자의 구성 설정을 사용하여 프로덕션에서 수행할 수 있습니다. [Supervisor 사용시](#supervisor-configuration) `numprocs` 구성 값을 사용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
#### 연결 및 큐 지정

워커가 어떤 큐 연결을 활용해야 하는지 지정할 수도 있습니다. `work` 명령에 전달된 연결 이름은 `config/queue.php` 구성 파일에 정의된 연결 중 하나와 일치해야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령은 지정된 연결에서 기본 큐에 대한 작업만 처리합니다. 그러나 특정 연결에 대해 특정 큐만 처리하여 큐 워커를 더욱 맞춤화할 수도 있습니다. 예를 들어 모든 이메일이 `redis` 큐 연결의 `emails` 큐에서 처리되는 경우 다음 명령을 실행하여 해당 큐만 처리하는 워커를 시작할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정된 수의 작업 처리

`--once` 옵션은 큐에서 단일 작업만 처리하도록 워커에 지시하는 데 사용될 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션은 워커에게 주어진 수의 작업을 처리한 다음 종료하도록 지시하는 데 사용될 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 결합하여 워커가 주어진 수의 작업을 처리한 후 자동으로 다시 시작되어 축적된 메모리를 해제할 때 유용할 수 있습니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 대기 중인 모든 작업을 처리한 후 종료

`--stop-when-empty` 옵션을 사용하면 워커에 모든 작업을 처리한 다음 정상적으로 종료하도록 지시할 수 있습니다. 이 옵션은 큐가 비어 있는 후 컨테이너를 종료하려는 경우 Docker 컨테이너 내에서 Laravel 큐를 처리할 때 유용할 수 있습니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 주어진 시간(초) 동안 작업 처리

`--max-time` 옵션을 사용하면 워커에 지정된 시간(초) 동안 작업을 처리한 다음 종료하도록 지시할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 결합하여 워커가 일정 시간 동안 작업을 처리한 후 자동으로 다시 시작되어 축적된 메모리를 해제할 때 유용할 수 있습니다.

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 수면 시간

큐에서 작업을 사용할 수 있는 경우 워커는 작업 사이에 지연 없이 작업을 계속 처리합니다. 그러나 `sleep` 옵션은 사용 가능한 작업이 없는 경우 워커가 "휴면"하는 시간(초)을 결정합니다. 물론, 잠자는 동안 워커는 새로운 작업을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지 관리 모드 및 큐

애플리케이션이 [유지 관리 모드](/docs/13.x/configuration#maintenance-mode)에 있는 동안에는 대기 중인 작업이 처리되지 않습니다. 애플리케이션이 유지 관리 모드를 벗어나면 작업은 계속 정상적으로 처리됩니다.

유지 관리 모드가 활성화된 경우에도 큐 워커가 작업을 처리하도록 하려면 `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 자원 고려사항

데몬 큐 워커는 각 작업을 처리하기 전에 프레임워크를 "재부팅"하지 않습니다. 따라서 각 작업이 완료된 후에 과도한 리소스를 해제해야 합니다. 예를 들어 [GD 라이브러리](https://www.php.net/manual/en/book.image.php)로 이미지 조작을 하는 경우, 이미지 처리가 끝나면 `imagedestroy`로 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

때로는 큐 처리 방법의 우선순위를 정하고 싶을 수도 있습니다. 예를 들어, `config/queue.php` 구성 파일에서 `redis` 연결에 대한 기본 `queue`를 `low`로 설정할 수 있습니다. 그러나 때로는 다음과 같이 작업을 `high` 우선순위 큐로 푸시할 수도 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`low` 큐에서 작업을 계속 진행하기 전에 모든 `high` 큐 작업이 처리되었는지 확인하는 워커를 시작하려면 쉼표로 구분된 큐 이름 목록을 `work` 명령에 전달합니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커 및 배포

큐 워커는 수명이 긴 프로세스이므로 다시 시작하지 않으면 코드 변경 사항을 알 수 없습니다. 따라서 큐 워커를 사용하여 애플리케이션을 배포하는 가장 간단한 방법은 배포 프로세스 중에 워커를 다시 시작하는 것입니다. `queue:restart` 명령을 실행하여 모든 워커를 정상적으로 다시 시작할 수 있습니다.

```shell
php artisan queue:restart
```

이 명령은 기존 작업이 손실되지 않도록 모든 큐 워커가 현재 작업 처리를 마친 후 정상적으로 종료하도록 지시합니다. 큐 워커는 `queue:restart` 명령이 실행될 때 종료되므로 [Supervisor](#supervisor-configuration)와 같은 프로세스 관리자를 실행하여 큐 워커를 자동으로 다시 시작해야 합니다.

> [!NOTE]
> 큐는 [캐시](/docs/13.x/cache)를 사용하여 재시작 신호를 저장하므로 이 기능을 사용하기 전에 캐시 드라이버가 애플리케이션에 대해 올바르게 구성되었는지 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료 및 시간 초과

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php` 구성 파일에서 각 큐 연결은 `retry_after` 옵션을 정의합니다. 이 옵션은 처리 중인 작업을 재시도하기 전에 큐 연결이 대기해야 하는 시간(초)을 지정합니다. 예를 들어, `retry_after` 값이 `90`로 설정된 경우 작업은 해제되거나 삭제되지 않고 90초 동안 처리된 경우 큐로 다시 해제됩니다. 일반적으로 `retry_after` 값을 작업이 처리를 완료하는 데 합리적으로 걸리는 최대 시간(초)으로 설정해야 합니다.

> [!WARNING]
> `retry_after` 값을 포함하지 않는 유일한 큐 연결은 Amazon SQS입니다. SQS는 AWS 콘솔 내에서 관리되는 [기본 표시 제한 시간](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)을 기반으로 작업을 다시 시도합니다.

<a name="worker-timeouts"></a>
#### 워커 시간 초과

`queue:work` Artisan 명령은 `--timeout` 옵션을 노출합니다. 기본적으로 `--timeout` 값은 60초입니다. 작업이 시간 초과 값으로 지정된 시간(초)보다 오랫동안 처리하는 경우 작업을 처리하는 워커는 오류와 함께 종료됩니다. 일반적으로 워커는 [서버에 구성된 프로세스 관리자](#supervisor-configuration)에 의해 자동으로 다시 시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 구성 옵션과 `--timeout` CLI 옵션은 서로 다르지만 함께 작동하여 작업이 손실되지 않고 작업이 한 번만 성공적으로 처리되도록 합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 구성 값보다 몇 초 이상 짧아야 합니다. 이렇게 하면 작업이 재시도되기 전에 고정된 작업을 처리하는 워커가 항상 종료됩니다. `--timeout` 옵션이 `retry_after` 구성 값보다 길면 작업이 두 번 처리될 수 있습니다.

<a name="pausing-and-resuming-queue-workers"></a>
### 큐 워커 일시 중지 및 재개

때로는 워커를 완전히 중지하지 않고 큐 워커가 새 작업을 처리하는 것을 일시적으로 방지해야 할 수도 있습니다. 예를 들어 시스템 유지 관리 중에 작업 처리를 일시 중지할 수 있습니다. Laravel는 큐 워커를 일시 중지하고 재개하는 `queue:pause` 및 `queue:continue` Artisan 명령을 제공합니다.

특정 큐를 일시 중지하려면 큐 연결 이름과 큐 이름을 제공하세요.

```shell
php artisan queue:pause database:default
```

이 예에서 `database`는 큐 연결 이름이고 `default`는 큐 이름입니다. 큐가 일시 중지되면 해당 큐에서 작업을 처리하는 모든 워커는 현재 작업을 계속 완료하지만 큐가 재개될 때까지 새로운 작업을 선택하지 않습니다.

일시 중지된 큐에서 작업 처리를 재개하려면 `queue:continue` 명령을 사용합니다.

```shell
php artisan queue:continue database:default
```

큐를 재개한 후 워커는 즉시 해당 큐에서 새 작업 처리를 시작합니다. 큐를 일시 중지해도 워커 프로세스 자체가 중지되지는 않습니다. 단지 워커가 지정된 큐에서 새 작업을 처리하는 것을 방지할 뿐입니다.

<a name="worker-restart-and-pause-signals"></a>
#### 워커 재시작 및 일시 정지 신호

기본적으로 큐 워커는 각 작업 반복에서 다시 시작 및 일시 중지 신호에 대해 캐시 드라이버를 폴링합니다. 이 폴링은 `queue:restart` 및 `queue:pause` 명령에 응답하는 데 필수적이지만 약간의 성능 오버헤드가 발생합니다.

성능을 최적화해야 하고 이러한 중단 기능이 필요하지 않은 경우 `Queue` 파사드에서 `withoutInterruptionPolling` 메서드를 호출하여 이 폴링을 전역적으로 비활성화할 수 있습니다. 이 작업은 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 수행되어야 합니다.

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

또는 `Illuminate\Queue\Worker` 클래스에서 정적 `$restartable` 또는 `$pausable` 속성을 설정하여 개별적으로 폴링 다시 시작 또는 일시 중지를 비활성화할 수 있습니다.

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
> 중단 폴링이 비활성화되면 워커는 `queue:restart` 또는 `queue:pause` 명령에 응답하지 않습니다(비활성화된 기능에 따라 다름).

<a name="supervisor-configuration"></a>
## Supervisor 구성 (Supervisor Configuration)

프로덕션에서는 `queue:work` 프로세스를 계속 실행하는 방법이 필요합니다. `queue:work` 프로세스는 워커 시간 초과 또는 `queue:restart` 명령 실행과 같은 다양한 이유로 실행이 중지될 수 있습니다.

이러한 이유로 `queue:work` 프로세스 종료 시기를 감지하고 자동으로 다시 시작할 수 있는 프로세스 모니터를 구성해야 합니다. 또한 프로세스 모니터를 사용하면 동시에 실행하려는 `queue:work` 프로세스 수를 지정할 수 있습니다. Supervisor는 Linux 환경에서 일반적으로 사용되는 프로세스 모니터이며 다음 문서에서 이를 구성하는 방법에 대해 설명합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영 체제용 프로세스 모니터이며, 실패할 경우 `queue:work` 프로세스를 자동으로 다시 시작합니다. Ubuntu에 Supervisor를 설치하려면 다음 명령을 사용할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor를 직접 구성하고 관리하는 것이 부담스럽다면 Laravel 큐 워커 실행을 위한 완전 관리형 플랫폼을 제공하는 [Laravel Cloud](https://cloud.laravel.com) 사용을 고려해 보세요.

<a name="configuring-supervisor"></a>
#### Supervisor 구성

Supervisor 구성 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 내에서 프로세스를 모니터링하는 방법을 감독자에게 지시하는 구성 파일을 원하는 만큼 생성할 수 있습니다. 예를 들어, `queue:work` 프로세스를 시작하고 모니터링하는 `laravel-worker.conf` 파일을 만들어 보겠습니다.

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

이 예에서 `numprocs` 지시문은 Supervisor에 8개의 `queue:work` 프로세스를 실행하고 모두 모니터링하여 실패할 경우 자동으로 다시 시작하도록 지시합니다. 원하는 큐 연결 및 워커 옵션을 반영하도록 구성의 `command` 지시문을 변경해야 합니다.

> [!WARNING]
> `stopwaitsecs`의 값이 가장 오래 실행되는 작업에서 소비하는 시간(초)보다 큰지 확인해야 합니다. 그렇지 않으면 Supervisor는 처리가 완료되기 전에 작업을 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작 중

구성 파일이 생성되면 다음 명령을 사용하여 Supervisor 구성을 업데이트하고 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 자세한 내용은 [Supervisor 문서](http://supervisord.org/index.html)를 참조하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리하기 (Dealing With Failed Jobs)

대기 중인 작업이 실패하는 경우도 있습니다. 걱정하지 마세요. 일이 항상 계획대로 진행되는 것은 아닙니다! Laravel에는 [작업을 시도해야 하는 최대 횟수를 지정](#max-job-attempts-and-timeout)하는 편리한 방법이 포함되어 있습니다. 비동기식 작업이 이 시도 횟수를 초과하면 `failed_jobs` 데이터베이스 테이블에 삽입됩니다. 실패한 [동기적으로 디스패치 작업](/docs/13.x/queues#synchronous-dispatching)는 이 테이블에 저장되지 않으며 해당 예외는 애플리케이션에서 즉시 처리됩니다.

`failed_jobs` 테이블을 생성하기 위한 마이그레이션은 일반적으로 새로운 Laravel 애플리케이션에 이미 존재합니다. 그러나 애플리케이션에 이 테이블에 대한 마이그레이션이 포함되어 있지 않은 경우 `make:queue-failed-table` 명령을 사용하여 마이그레이션을 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때 `queue:work` 명령의 `--tries` 스위치를 사용하여 작업을 시도해야 하는 최대 횟수를 지정할 수 있습니다. `--tries` 옵션에 대한 값을 지정하지 않으면 작업은 한 번만 시도되거나 작업 클래스의 `$tries` 속성에 지정된 횟수만큼 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면 예외가 발생한 작업을 재시도하기 전에 Laravel가 기다려야 하는 시간(초)을 지정할 수 있습니다. 기본적으로 작업은 다시 시도할 수 있도록 즉시 큐로 다시 해제됩니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

작업별로 예외가 발생한 작업을 재시도하기 전에 Laravel가 기다려야 하는 시간(초)을 구성하려면 작업 클래스에 `backoff` 속성을 정의하면 됩니다.

```php
/**
 * The number of seconds to wait before retrying the job.
 *
 * @var int
 */
public $backoff = 3;
```

작업의 백오프 시간을 결정하기 위해 더 복잡한 로직이 필요한 경우 작업 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the job.
 */
public function backoff(): int
{
    return 3;
}
```

`backoff` 메서드에서 백오프 값 배열을 반환하여 "지수" 백오프를 쉽게 구성할 수 있습니다. 이 예에서 재시도 지연은 첫 번째 재시도의 경우 1초, 두 번째 재시도의 경우 5초, 세 번째 재시도의 경우 10초, 남은 시도가 더 있는 경우 모든 후속 재시도의 경우 10초입니다.

```php
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
### 작업 실패 후 정리

특정 작업이 실패하면 사용자에게 경고를 보내거나 작업에 의해 부분적으로 완료된 작업을 되돌릴 수 있습니다. 이를 수행하려면 작업 클래스에 `failed` 메서드를 정의하면 됩니다. 작업 실패를 초래한 `Throwable` 인스턴스는 `failed` 메서드로 전달됩니다.

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
> 작업의 새 인스턴스는 `failed` 메서드를 호출하기 전에 인스턴스화됩니다. 따라서 `handle` 메서드 내에서 발생한 모든 클래스 속성 수정 사항은 손실됩니다.

실패한 작업이 반드시 처리되지 않은 예외가 발생한 것은 아닙니다. 작업은 허용된 시도를 모두 소진한 경우 실패한 것으로 간주될 수도 있습니다. 이러한 시도는 여러 가지 방법으로 사용될 수 있습니다.

<div class="content-list" markdown="1">

- 작업의 시간이 초과되었습니다.
- 작업은 실행 중에 처리되지 않은 예외가 발생합니다.
- 작업은 수동으로 또는 미들웨어에 의해 큐로 다시 릴리스됩니다.

</div>

작업 실행 중에 발생한 예외로 인해 최종 시도가 실패하는 경우 해당 예외는 작업의 `failed` 메서드에 전달됩니다. 그러나 허용된 최대 시도 횟수에 도달하여 작업이 실패하는 경우 `$exception`는 `Illuminate\Queue\MaxAttemptsExceededException`의 인스턴스가 됩니다. 마찬가지로 구성된 시간 초과로 인해 작업이 실패하는 경우 `$exception`는 `Illuminate\Queue\TimeoutExceededException`의 인스턴스가 됩니다.

<a name="retrying-failed-jobs"></a>
### 재시도 실패 작업

`failed_jobs` 데이터베이스 테이블에 삽입된 모든 실패한 작업을 뷰하려면 `queue:failed` Artisan 명령을 사용할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령은 작업 ID, 연결, 큐, 오류 시간 및 작업에 대한 기타 정보를 나열합니다. 작업 ID는 실패한 작업을 재시도하는 데 사용될 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패한 작업을 재시도하려면 다음 명령을 실행하십시오.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요한 경우 여러 ID를 명령에 전달할 수 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐에 대해 실패한 작업을 모두 다시 시도할 수도 있습니다.

```shell
php artisan queue:retry --queue=name
```

실패한 작업을 모두 다시 시도하려면 `queue:retry` 명령을 실행하고 `all`를 ID로 전달합니다.

```shell
php artisan queue:retry all
```

실패한 작업을 삭제하려면 `queue:forget` 명령을 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/13.x/horizon)를 사용할 때 `queue:forget` 명령 대신 `horizon:forget` 명령을 사용하여 실패한 작업을 삭제해야 합니다.

`failed_jobs` 테이블에서 실패한 작업을 모두 삭제하려면 `queue:flush` 명령을 사용할 수 있습니다.

```shell
php artisan queue:flush
```

`queue:flush` 명령은 실패한 작업이 얼마나 오래되었는지에 관계없이 큐에서 실패한 모든 작업 레코드를 제거합니다. `--hours` 옵션을 사용하면 특정 시간 이전에 실패한 작업만 삭제할 수 있습니다.

```shell
php artisan queue:flush --hours=48
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시

Eloquent 모델을 작업에 주입하면 모델은 큐에 배치되기 전에 자동으로 직렬화되고 작업이 처리될 때 데이터베이스에서 다시 검색됩니다. 그러나 작업이 워커의 처리를 기다리는 동안 모델이 삭제된 경우 작업이 `ModelNotFoundException`로 인해 실패할 수 있습니다.

편의를 위해 작업의 `deleteWhenMissingModels` 속성을 `true`로 설정하여 모델이 누락된 작업을 자동으로 삭제하도록 선택할 수 있습니다. 이 속성이 `true`로 설정되면 Laravel는 예외를 발생시키지 않고 작업을 조용히 삭제합니다.

```php
/**
 * Delete the job if its models no longer exist.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 작업 정리

`queue:prune-failed` Artisan 명령을 호출하여 애플리케이션의 `failed_jobs` 테이블에 있는 레코드를 정리할 수 있습니다.

```shell
php artisan queue:prune-failed
```

기본적으로 24시간이 넘은 실패한 작업 레코드는 모두 정리됩니다. 명령에 `--hours` 옵션을 제공하면 마지막 N 시간 내에 삽입된 실패한 작업 레코드만 유지됩니다. 예를 들어, 다음 명령은 48시간 이상 전에 삽입되어 실패한 모든 작업 레코드를 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패한 작업 저장

Laravel는 실패한 작업 레코드를 관계형 데이터베이스 테이블 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 기능도 지원합니다. 그러나 실패한 모든 작업 레코드를 저장하려면 DynamoDB 테이블을 수동으로 생성해야 합니다. 일반적으로 이 테이블의 이름은 `failed_jobs`로 지정되어야 하지만 애플리케이션의 `queue` 구성 파일에 있는 `queue.failed.table` 구성 값을 기반으로 테이블 이름을 지정해야 합니다.

`failed_jobs` 테이블에는 `application`라는 문자열 기본 파티션 키와 `uuid`라는 문자열 기본 정렬 키가 있어야 합니다. 키의 `application` 부분에는 애플리케이션의 `app` 구성 파일 내 `name` 구성 값으로 정의된 애플리케이션 이름이 포함됩니다. 애플리케이션 이름은 DynamoDB 테이블 키의 일부이므로 동일한 테이블을 사용하여 여러 Laravel 애플리케이션에 대해 실패한 작업을 저장할 수 있습니다.

또한 Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

다음으로 `queue.failed.driver` 구성 옵션의 값을 `dynamodb`로 설정합니다. 또한 실패한 작업 구성 배열 내에서 `key`, `secret` 및 `region` 구성 옵션을 정의해야 합니다. 이러한 옵션은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용하는 경우 `queue.failed.database` 구성 옵션이 필요하지 않습니다.

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
### 실패한 작업 저장소 비활성화

`queue.failed.driver` 구성 옵션의 값을 `null`로 설정하여 실패한 작업을 저장하지 않고 삭제하도록 Laravel에 지시할 수 있습니다. 일반적으로 이는 `QUEUE_FAILED_DRIVER` 환경 변수를 통해 수행될 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 작업 이벤트 실패

작업이 실패할 때 호출될 이벤트 리스너를 등록하려면 `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, Laravel에 포함된 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트에 클로저를 연결할 수 있습니다.

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
## 큐에서 작업 지우기 (Clearing Jobs From Queues)

> [!NOTE]
> [Horizon](/docs/13.x/horizon)를 사용할 때 `queue:clear` 명령 대신 큐에서 작업을 지우려면 `horizon:clear` 명령을 사용해야 합니다.

기본 연결의 기본 큐에서 모든 작업을 삭제하려면 `queue:clear` Artisan 명령을 사용하면 됩니다.

```shell
php artisan queue:clear
```

특정 연결 및 큐에서 작업을 삭제하기 위해 `connection` 인수와 `queue` 옵션을 제공할 수도 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 지우는 것은 SQS, Redis 및 데이터베이스 큐 드라이버에만 사용할 수 있습니다. 또한 SQS 메시지 삭제 프로세스에는 최대 60초가 소요되므로 큐를 삭제한 후 최대 60초 후에 SQS 큐로 전송된 작업도 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

큐에 작업이 갑자기 유입되면 압도되어 작업이 완료될 때까지 기다리는 시간이 길어질 수 있습니다. 원하는 경우 Laravel는 큐 작업 수가 지정된 임계값을 초과할 때 경고할 수 있습니다.

시작하려면 `queue:monitor` 명령을 [1분마다 실행](/docs/13.x/scheduling)하도록 예약해야 합니다. 이 명령은 모니터링하려는 큐의 이름과 원하는 작업 개수 임계값을 허용합니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령을 예약하는 것만으로는 큐의 압도 상태를 경고하는 알림을 트리거하는 데 충분하지 않습니다. 명령이 임계값을 초과하는 작업 수가 있는 큐를 발견하면 `Illuminate\Queue\Events\QueueBusy` 이벤트는 디스패치가 됩니다. 귀하 또는 개발 팀에 알림을 보내기 위해 애플리케이션의 `AppServiceProvider` 내에서 이 이벤트를 들을 수 있습니다.

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
## 테스트 (Testing)

디스패치 작업 코드를 테스트할 때 실제로 작업 자체를 실행하지 않도록 Laravel에 지시할 수 있습니다. 왜냐하면 작업 코드는 디스패치 코드와 별도로 직접 테스트할 수 있기 때문입니다. 물론 작업 자체를 테스트하려면 작업 인스턴스를 인스턴스화하고 테스트에서 `handle` 메서드를 직접 호출할 수 있습니다.

큐에 있는 작업이 실제로 큐로 푸시되는 것을 방지하기 위해 `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. `Queue` 파사드의 `fake` 메서드를 호출한 후, 애플리케이션이 작업을 큐에 푸시하려고 시도했다고 주장할 수 있습니다:

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

주어진 "진실 테스트"를 통과한 작업이 푸시되었음을 주장하기 위해 `assertPushed`, `assertNotPushed`, `assertClosurePushed` 또는 `assertClosureNotPushed` 메서드에 클로저를 전달할 수 있습니다. 주어진 진실 테스트를 통과하는 하나 이상의 작업이 푸시되면 어설션이 성공합니다.

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
### 작업의 하위 집합 위조

다른 작업이 정상적으로 실행되도록 허용하면서 특정 작업만 위조해야 하는 경우, 위조해야 하는 작업의 클래스 이름을 `fake` 메서드에 전달할 수 있습니다.

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

`except` 메서드를 사용하여 지정된 작업 세트를 제외한 모든 작업을 위조할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 작업 체인 테스트

작업 체인을 테스트하려면 `Bus` 파사드의 위조 기능을 활용해야 합니다. `Bus` 파사드의 `assertChained` 메서드는 [작업의 체인](/docs/13.x/queues#job-chaining)이 디스패치임을 주장하는데 사용될 수 있습니다. `assertChained` 메서드는 연결된 작업 배열을 첫 번째 인수로 허용합니다.

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

위의 예에서 볼 수 있듯이 연결된 작업의 배열은 작업의 클래스 이름 배열일 수 있습니다. 그러나 실제 작업 인스턴스 배열을 제공할 수도 있습니다. 이렇게 하면 Laravel는 작업 인스턴스가 애플리케이션에 의해 연결된 작업 디스패치의 클래스와 속성 값이 동일한지 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

작업 체인 없이 작업이 푸시되었음을 확인하기 위해 `assertDispatchedWithoutChain` 메서드를 사용할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 테스트 체인 수정

연결된 작업이 [기존 체인에 작업을 추가하거나 추가](#adding-jobs-to-the-chain)하는 경우 작업의 `assertHasChain` 메서드를 사용하여 작업에 나머지 작업의 예상 체인이 있음을 확인할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` 메서드는 작업의 나머지 체인이 비어 있음을 확인하는 데 사용될 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 연결된 배치 테스트

작업 체인이 [작업의 배치를 포함](#chains-and-batches)하는 경우 체인 어설션 내에 `Bus::chainedBatch` 정의를 삽입하여 연결된 배치가 예상과 일치한다고 어설션할 수 있습니다.

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
### 작업 배치 테스트

`Bus` 파사드의 `assertBatched` 메서드는 [작업의 배치](/docs/13.x/queues#job-batching)가 디스패치임을 주장하는데 사용될 수 있습니다. `assertBatched` 메서드에 제공된 클로저는 배치 내의 작업을 검사하는 데 사용될 수 있는 `Illuminate\Bus\PendingBatch`의 인스턴스를 수신합니다.

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

`hasJobs` 메서드는 보류 중인 배치에서 사용되어 배치에 예상된 작업이 포함되어 있는지 확인할 수 있습니다. 이 메서드는 작업 인스턴스, 클래스 이름 또는 클로저의 배열을 허용합니다.

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        new ProcessCsvRow(row: 1),
        new ProcessCsvRow(row: 2),
        new ProcessCsvRow(row: 3),
    ]);
});
```

클로저를 사용할 때 클로저는 작업 인스턴스를 수신합니다. 예상되는 작업 유형은 클로저의 유형 힌트에서 추론됩니다:

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        fn (ProcessCsvRow $job) => $job->row === 1,
        fn (ProcessCsvRow $job) => $job->row === 2,
        fn (ProcessCsvRow $job) => $job->row === 3,
    ]);
});
```

`assertBatchCount` 메서드를 사용하여 주어진 배치 수가 디스패치인지 확인할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

`assertNothingBatched`를 사용하여 배치가 디스패치가 아니라는 것을 주장할 수 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 작업 / 배치 상호 작용 테스트

또한 때때로 개별 작업과 기본 배치의 상호 작용을 테스트해야 할 수도 있습니다. 예를 들어, 작업이 배치에 대한 추가 처리를 취소했는지 테스트해야 할 수도 있습니다. 이를 수행하려면 `withFakeBatch` 메서드를 통해 가짜 배치를 작업에 할당해야 합니다. `withFakeBatch` 메서드는 작업 인스턴스와 가짜 배치를 포함하는 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업 / 큐 상호 작용 테스트

때로는 대기 중인 작업이 [큐에 다시 릴리스](#manually-releasing-a-job)되는지 테스트해야 할 수도 있습니다. 또는 작업이 자체적으로 삭제되었는지 테스트해야 할 수도 있습니다. 작업을 인스턴스화하고 `withFakeQueueInteractions` 메서드를 호출하여 이러한 큐 상호 작용을 테스트할 수 있습니다.

작업의 큐 상호작용이 위조되면 작업에서 `handle` 메서드를 호출할 수 있습니다. 작업을 호출한 후 다양한 assertion 메서드를 사용하여 작업의 큐 상호작용을 확인할 수 있습니다.

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
## 작업 이벤트 (Job Events)

`Queue` [facade](/docs/13.x/facades)에서 `before` 및 `after` 메서드를 사용하면 큐에 있는 작업이 처리되기 전이나 후에 실행될 콜백을 지정할 수 있습니다. 이러한 콜백은 대시보드에 대한 추가 로깅 또는 증분 통계를 수행할 수 있는 좋은 기회입니다. 일반적으로 [서비스 프로바이더](/docs/13.x/providers)의 `boot` 메서드에서 이러한 메서드를 호출해야 합니다. 예를 들어, Laravel에 포함된 `AppServiceProvider`를 사용할 수 있습니다.

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

`Queue` [facade](/docs/13.x/facades)에서 `looping` 메서드를 사용하면 워커가 큐에서 작업을 가져오려고 시도하기 전에 실행되는 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 작업에 의해 열려 있던 트랜잭션을 롤백하기 위해 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```
