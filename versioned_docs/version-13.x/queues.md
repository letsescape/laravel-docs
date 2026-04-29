# 큐 (Queues)

- [소개](#introduction)
    - [연결과 큐](#connections-vs-queues)
    - [드라이버 참고 사항 및 사전 요구 사항](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡](#unique-jobs)
    - [디바운스된 잡](#debounced-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 스로틀링](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 연결 사용자 지정](#customizing-the-queue-and-connection)
    - [최대 잡 시도 횟수 / 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO와 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 장애 조치](#queue-failover)
    - [오류 처리](#error-handling)
- [잡 배치](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 검사](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료와 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시 중지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 이후 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 Fake 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡 / 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 만들다 보면 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼 일반적인 웹 요청 중에 처리하기에는 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel을 사용하면 백그라운드에서 처리할 수 있는 큐 잡을 쉽게 만들 수 있습니다. 시간이 많이 드는 작업을 큐로 옮기면 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있고, 사용자에게 더 나은 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 같은 다양한 큐 백엔드 전반에 걸쳐 통합된 큐잉 API를 제공합니다.

Laravel의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버의 연결 설정이 들어 있습니다. 여기에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버뿐 아니라 잡을 즉시 실행하는 동기 드라이버도 포함됩니다. 동기 드라이버는 개발이나 테스트 중에 사용할 수 있습니다. 큐에 들어온 잡을 버리는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 보기 좋은 대시보드이자 설정 시스템입니다. 자세한 내용은 전체 [Horizon 문서](/docs/13.x/horizon)를 확인하세요.

<a name="connections-vs-queues"></a>
### 연결과 큐

Laravel 큐를 시작하기 전에 "connections"와 "queues"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스에 대한 연결을 정의합니다. 하지만 하나의 큐 연결은 여러 "큐"를 가질 수 있으며, 이는 서로 다른 큐 잡의 스택이나 더미로 생각할 수 있습니다.

`queue` 설정 파일의 각 연결 설정 예제에는 `queue` 속성이 포함되어 있습니다. 이는 해당 연결로 잡이 전송될 때 잡이 디스패치될 기본 큐입니다. 다시 말해, 잡을 디스패치하면서 어느 큐로 보낼지 명시적으로 정의하지 않으면 해당 잡은 연결 설정의 `queue` 속성에 정의된 큐에 배치됩니다.

```php
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 여러 큐에 잡을 넣을 필요 없이 단순한 큐 하나만 사용하는 편을 선호할 수 있습니다. 하지만 잡 처리 방식에 우선순위를 두거나 구분하고 싶은 애플리케이션에서는 여러 큐에 잡을 넣는 방식이 특히 유용합니다. Laravel 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어 `high` 큐에 잡을 넣는다면, 해당 잡을 더 높은 처리 우선순위로 다루는 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고 사항 및 사전 요구 사항

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/13.x/migrations)에 포함되어 있습니다. 하지만 애플리케이션에 이 마이그레이션이 없다면 `make:queue-table` Artisan 명령어로 만들 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에서 Redis 데이터베이스 연결을 설정해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 연결이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에는 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이는 특정 큐에 대한 모든 Redis 키가 같은 해시 슬롯에 배치되도록 보장하기 위해 필요합니다.

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

Redis 큐를 사용할 때는 `block_for` 설정 옵션을 사용하여, 잡이 사용 가능해질 때까지 드라이버가 얼마나 기다린 뒤 워커 루프를 반복하고 Redis 데이터베이스를 다시 폴링할지 지정할 수 있습니다.

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
> `block_for`를 `0`으로 설정하면 잡이 사용 가능해질 때까지 큐 워커가 무기한 블로킹됩니다. 또한 이 경우 다음 잡이 처리될 때까지 `SIGTERM` 같은 시그널이 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 요구 사항

아래 큐 드라이버를 사용하려면 다음 의존성이 필요합니다. 이 의존성은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 애플리케이션의 모든 큐잉 가능한 잡은 `app/Jobs` 디렉터리에 저장됩니다. `app/Jobs` 디렉터리가 없다면 `make:job` Artisan 명령어를 실행할 때 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현합니다. 이는 해당 잡이 비동기로 실행되도록 큐에 넣어야 한다는 것을 Laravel에 알려줍니다.

> [!NOTE]
> 잡 스텁은 [스텁 게시](/docs/13.x/artisan#stub-customization)를 사용하여 사용자 지정할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

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

이 예제에서 [Eloquent 모델](/docs/13.x/eloquent)을 큐 잡의 생성자에 직접 전달할 수 있었다는 점에 주목하세요. 잡이 사용하는 `Queueable` 트레이트 덕분에, 잡이 처리될 때 Eloquent 모델과 로드된 연관관계가 자연스럽게 직렬화되고 역직렬화됩니다.

큐 잡이 생성자에서 Eloquent 모델을 받는 경우, 큐에는 해당 모델의 식별자만 직렬화됩니다. 잡이 실제로 처리될 때 큐 시스템은 데이터베이스에서 전체 모델 인스턴스와 로드된 연관관계를 자동으로 다시 조회합니다. 이러한 모델 직렬화 방식 덕분에 큐 드라이버로 전송되는 잡 페이로드를 훨씬 작게 유지할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 잡이 큐에 의해 처리될 때 호출됩니다. 잡의 `handle` 메서드에 의존성을 타입 힌트로 지정할 수 있다는 점에 주목하세요. Laravel [서비스 컨테이너](/docs/13.x/container)가 이러한 의존성을 자동으로 주입합니다.

컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하고 싶다면 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod` 메서드는 잡과 컨테이너를 받는 콜백을 인수로 받습니다. 콜백 안에서는 원하는 방식으로 `handle` 메서드를 자유롭게 호출할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/13.x/providers)의 `boot` 메서드에서 호출해야 합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 내용 같은 바이너리 데이터는 큐 잡에 전달하기 전에 `base64_encode` 함수를 거쳐야 합니다. 그렇지 않으면 큐에 배치될 때 잡이 JSON으로 제대로 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 들어가는 연관관계

잡이 큐에 들어갈 때 로드된 모든 Eloquent 모델 연관관계도 함께 직렬화되므로, 직렬화된 잡 문자열이 때때로 상당히 커질 수 있습니다. 또한 잡이 역직렬화되고 모델 연관관계가 데이터베이스에서 다시 조회될 때 해당 연관관계는 전체가 조회됩니다. 잡 큐잉 과정에서 모델이 직렬화되기 전에 적용되었던 이전 연관관계 제약 조건은 잡이 역직렬화될 때 적용되지 않습니다. 따라서 특정 연관관계의 일부만 사용하고 싶다면 큐 잡 안에서 해당 연관관계에 다시 제약 조건을 적용해야 합니다.

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

나머지는 유지하면서 특정 연관관계만 제거해야 한다면 `withoutRelation` 메서드를 사용할 수 있습니다.

```php
$this->podcast = $podcast->withoutRelation('comments');
```

[PHP 생성자 속성 승격](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하면서 Eloquent 모델의 연관관계가 직렬화되지 않아야 함을 나타내고 싶다면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

잡이 단일 모델 대신 Eloquent 모델 컬렉션이나 배열을 받는 경우, 해당 컬렉션 안의 모델은 잡이 역직렬화되어 실행될 때 연관관계가 복원되지 않습니다. 이는 많은 수의 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위한 것입니다.

<a name="unique-jobs"></a>
### 고유 잡

> [!WARNING]
> 고유 잡에는 [락](/docs/13.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 atomic lock을 지원합니다.

> [!WARNING]
> 고유 잡 제약 조건은 배치 안의 잡에는 적용되지 않습니다.

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

위 예제에서 `UpdateSearchIndex` 잡은 고유합니다. 따라서 해당 잡의 다른 인스턴스가 이미 큐에 있고 아직 처리가 끝나지 않았다면, 새 잡은 디스패치되지 않습니다.

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
위 예제에서 `UpdateSearchIndex` 잡은 제품 ID를 기준으로 고유합니다. 따라서 같은 제품 ID를 가진 새 잡 디스패치는 기존 잡 처리가 완료될 때까지 무시됩니다. 또한 기존 잡이 한 시간 안에 처리되지 않으면 고유 락이 해제되고, 같은 고유 키를 가진 다른 잡을 큐에 디스패치할 수 있습니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, Laravel이 잡의 고유 여부를 정확히 판단할 수 있도록 모든 서버가 같은 중앙 캐시 서버와 통신하는지 확인해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리가 시작될 때까지만 잡을 고유하게 유지하기

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
#### 고유 잡 락

내부적으로 `ShouldBeUnique` 잡이 디스패치되면 Laravel은 `uniqueId` 키로 [락](/docs/13.x/cache#atomic-locks)을 획득하려고 시도합니다. 이미 락이 잡혀 있다면 잡은 디스패치되지 않습니다. 이 락은 잡 처리가 완료되거나 모든 재시도 시도가 실패하면 해제됩니다. 기본적으로 Laravel은 이 락을 얻기 위해 기본 캐시 드라이버를 사용합니다. 하지만 락을 얻는 데 다른 드라이버를 사용하고 싶다면, 사용할 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다.

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
> 작업의 동시 처리를 제한하기만 하면 되는 경우, 대신 [WithoutOverlapping](/docs/13.x/queues#preventing-job-overlaps) 작업 middleware를 사용하십시오.

<a name="debounced-jobs"></a>
### 디바운스된 작업

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

위 예시에서는 동일한 상품에 대해 `30`초 안에 `UpdateSearchIndex`를 반복해서 dispatch하면 작업이 debounce되어, 가장 마지막 dispatch만 실행됩니다.

자주 다시 dispatch되는 작업이 지연될 수 있는 최대 시간을 제한하려면 `DebounceFor` 속성에 `maxWait` 인수를 제공할 수 있습니다.

```php
#[DebounceFor(30, maxWait: 120)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    // ...
}
```

작업에 `debounceVia` 메서드를 정의하여 debounce 추적에 사용할 cache store를 직접 지정할 수 있습니다.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

public function debounceVia(): Repository
{
    return Cache::driver('redis');
}
```

debounce된 작업이 더 새로운 dispatch로 대체되면, Laravel은 `Illuminate\Queue\Events\JobDebounced` 이벤트를 dispatch하고 대체된 작업을 큐에서 제거합니다.

> [!WARNING]
> Debounced jobs와 unique jobs는 함께 사용할 수 없습니다. `DebounceFor` 속성을 사용하는 작업은 `ShouldBeUnique`를 구현해서는 안 됩니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버 또는 컨테이너에서 debounce된 작업을 dispatch하는 경우, 모든 서버가 동일한 중앙 cache 서버와 통신하도록 해야 합니다.

<a name="encrypted-jobs"></a>
### 암호화된 작업

Laravel은 [암호화](/docs/13.x/encryption)를 통해 작업 데이터의 개인정보 보호와 무결성을 보장할 수 있도록 합니다. 시작하려면 작업 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 이 인터페이스가 클래스에 추가되면, Laravel은 작업을 큐에 push하기 전에 자동으로 암호화합니다.

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
## 작업 Middleware (Job Middleware)

작업 middleware를 사용하면 큐 작업 실행 전후에 사용자 정의 로직을 감쌀 수 있어, 작업 자체에 반복 코드가 줄어듭니다. 예를 들어, 다음 `handle` 메서드는 Laravel의 Redis 처리율 제한 기능을 활용하여 5초마다 하나의 작업만 처리되도록 합니다.

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

이 코드는 유효하지만, `handle` 메서드 구현이 Redis 처리율 제한 로직으로 복잡해져 읽기 어려워집니다. 또한 처리율 제한이 필요한 다른 작업마다 이 로직을 중복해서 작성해야 합니다. `handle` 메서드 안에서 처리율을 제한하는 대신, 처리율 제한을 담당하는 작업 middleware를 정의할 수 있습니다.

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

보시는 것처럼 [route middleware](/docs/13.x/middleware)와 마찬가지로, 작업 middleware는 처리 중인 작업과 작업 처리를 계속 진행하기 위해 호출해야 하는 callback을 받습니다.

`make:job-middleware` Artisan 명령어를 사용하여 새로운 작업 middleware 클래스를 생성할 수 있습니다. 작업 middleware를 만든 뒤에는 작업의 `middleware` 메서드에서 반환하여 작업에 연결할 수 있습니다. 이 메서드는 `make:job` Artisan 명령어로 스캐폴딩된 작업에는 존재하지 않으므로, 작업 클래스에 직접 추가해야 합니다.

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
> 작업 middleware는 [queueable event listeners](/docs/13.x/events#queued-event-listeners), [mailables](/docs/13.x/mail#queueing-mail), [notifications](/docs/13.x/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 처리율 제한

방금 직접 처리율 제한 작업 middleware를 작성하는 방법을 살펴보았지만, Laravel에는 실제로 작업의 처리율을 제한하는 데 사용할 수 있는 처리율 제한 middleware가 포함되어 있습니다. [route rate limiters](/docs/13.x/routing#defining-rate-limiters)와 마찬가지로, 작업 rate limiter는 `RateLimiter` facade의 `for` 메서드를 사용하여 정의합니다.

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

위 예시에서는 시간 단위 처리율 제한을 정의했습니다. 하지만 `perMinute` 메서드를 사용하면 분 단위 처리율 제한도 쉽게 정의할 수 있습니다. 또한 처리율 제한의 `by` 메서드에는 원하는 어떤 값이든 전달할 수 있지만, 이 값은 주로 고객별로 처리율 제한을 나누는 데 사용됩니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

처리율 제한을 정의한 뒤에는 `Illuminate\Queue\Middleware\RateLimited` middleware를 사용하여 rate limiter를 작업에 연결할 수 있습니다. 작업이 처리율 제한을 초과할 때마다 이 middleware는 처리율 제한 기간에 따라 적절한 지연 시간을 적용하여 작업을 다시 큐로 release합니다.

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

처리율 제한으로 작업이 다시 큐에 release되더라도, 작업의 총 `attempts` 횟수는 증가합니다. 따라서 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 그에 맞게 조정하는 것이 좋습니다. 또는 [retryUntil 메서드](#time-based-attempts)를 사용하여 작업을 더 이상 시도하지 않을 시간을 정의할 수도 있습니다.

`releaseAfter` 메서드를 사용하면 release된 작업을 다시 시도하기 전에 지나야 하는 초 단위 시간을 지정할 수도 있습니다.

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
#### Redis로 처리율 제한하기

Redis를 사용하고 있다면 `Illuminate\Queue\Middleware\RateLimitedWithRedis` middleware를 사용할 수 있습니다. 이 middleware는 Redis에 맞게 조정되어 있으며 기본 처리율 제한 middleware보다 더 효율적입니다.

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

`connection` 메서드를 사용하여 middleware가 사용할 Redis connection을 지정할 수 있습니다.

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a name="preventing-job-overlaps"></a>
### 작업 중복 실행 방지

Laravel에는 임의의 키를 기준으로 작업의 중복 실행을 방지할 수 있는 `Illuminate\Queue\Middleware\WithoutOverlapping` middleware가 포함되어 있습니다. 큐 작업이 한 번에 하나의 작업만 수정해야 하는 리소스를 수정하는 경우 유용합니다.

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

중복 실행되는 작업을 다시 큐에 release하더라도 작업의 총 시도 횟수는 증가합니다. 따라서 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 그에 맞게 조정하는 것이 좋습니다. 예를 들어 기본값처럼 `Tries`를 1로 두면, 중복 실행된 작업은 나중에 다시 시도되지 않습니다.

같은 타입의 모든 중복 작업은 다시 큐로 release됩니다. 또한 release된 작업을 다시 시도하기 전에 지나야 하는 초 단위 시간을 지정할 수도 있습니다.

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
> `WithoutOverlapping` middleware는 [locks](/docs/13.x/cache#atomic-locks)를 지원하는 cache driver가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` cache driver가 atomic lock을 지원합니다.

<a name="sharing-lock-keys"></a>
#### 작업 클래스 간 lock key 공유

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
### 예외 스로틀링

Laravel에는 예외 발생을 throttle할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` middleware가 포함되어 있습니다. 작업이 지정된 횟수만큼 예외를 던지면, 이후의 모든 작업 실행 시도는 지정된 시간 간격이 지날 때까지 지연됩니다. 이 middleware는 불안정한 서드파티 서비스와 상호작용하는 작업에 특히 유용합니다.

예를 들어, 예외를 던지기 시작한 서드파티 API와 상호작용하는 큐 작업이 있다고 가정해 보겠습니다. 예외를 throttle하려면 작업의 `middleware` 메서드에서 `ThrottlesExceptions` middleware를 반환할 수 있습니다. 일반적으로 이 middleware는 [시간 기반 시도](#time-based-attempts)를 구현한 작업과 함께 사용해야 합니다.

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

middleware가 받는 첫 번째 생성자 인수는 작업이 throttle되기 전에 던질 수 있는 예외 횟수이며, 두 번째 생성자 인수는 작업이 throttle된 후 다시 시도되기 전에 지나야 하는 초 단위 시간입니다. 위 코드 예시에서 작업이 연속으로 10번 예외를 던지면, 30분 시간 제한 안에서 5분을 기다린 뒤 작업을 다시 시도합니다.

작업이 예외를 던졌지만 예외 임계값에 아직 도달하지 않은 경우, 일반적으로 작업은 즉시 다시 시도됩니다. 하지만 작업에 middleware를 연결할 때 `backoff` 메서드를 호출하여 이러한 작업을 몇 분 동안 지연할지 지정할 수 있습니다.
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

작업을 다시 큐로 릴리스하거나 예외를 던지는 `when` 메서드와 달리, `deleteWhen` 메서드를 사용하면 특정 예외가 발생했을 때 작업을 완전히 삭제할 수 있습니다.

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
#### Redis로 예외 제한하기

Redis를 사용하고 있다면 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 Redis에 맞게 세밀하게 조정되어 있으며, 기본 예외 제한 미들웨어보다 더 효율적입니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

`connection` 메서드를 사용하여 미들웨어가 사용할 Redis 연결을 지정할 수 있습니다.

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a name="skipping-jobs"></a>
### 작업 건너뛰기

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

더 복잡한 조건 평가가 필요하다면 `when`과 `unless` 메서드에 `Closure`를 전달할 수도 있습니다.

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
## 작업 디스패치하기 (Dispatching Jobs)

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

조건부로 작업을 디스패치하고 싶다면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새 Laravel 애플리케이션에서는 `database` 연결이 기본 큐로 정의되어 있습니다. 애플리케이션의 `.env` 파일에서 `QUEUE_CONNECTION` 환경 변수를 변경하여 다른 기본 큐 연결을 지정할 수 있습니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치

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

경우에 따라 작업에 기본 지연 시간이 설정되어 있을 수 있습니다. 이 지연 시간을 우회하고 작업을 즉시 처리하도록 디스패치해야 한다면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스의 최대 지연 시간은 15분입니다.

<a name="synchronous-dispatching"></a>
### 동기 디스패치

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
#### 지연된 디스패치

지연된 동기 디스패치를 사용하면 현재 프로세스에서 작업을 처리하도록 디스패치하되, HTTP 응답이 사용자에게 전송된 뒤에 처리되도록 할 수 있습니다. 이를 통해 사용자의 애플리케이션 경험을 느리게 만들지 않으면서 "큐에 들어간" 작업을 동기적으로 처리할 수 있습니다. 동기 작업의 실행을 지연하려면 작업을 `deferred` 연결로 디스패치하십시오.

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```

`deferred` 연결은 기본 [장애 조치 큐](#queue-failover)로도 사용됩니다.

마찬가지로 `background` 연결도 HTTP 응답이 사용자에게 전송된 뒤 작업을 처리합니다. 다만 이 경우 작업은 별도로 생성된 PHP 프로세스에서 처리되므로, PHP-FPM / 애플리케이션 워커는 다른 들어오는 HTTP 요청을 처리할 수 있는 상태가 됩니다.

```php
RecordDelivery::dispatch($order)->onConnection('background');
```

<a name="jobs-and-database-transactions"></a>
### 작업과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 작업을 디스패치하는 것 자체는 전혀 문제가 없지만, 작업이 실제로 성공적으로 실행될 수 있는지 각별히 주의해야 합니다. 트랜잭션 안에서 작업을 디스패치할 때, 부모 트랜잭션이 커밋되기 전에 워커가 해당 작업을 처리할 수 있습니다. 이런 일이 발생하면 데이터베이스 트랜잭션 중에 모델이나 데이터베이스 레코드에 적용한 업데이트가 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한 트랜잭션 안에서 생성한 모델이나 데이터베이스 레코드가 아직 데이터베이스에 존재하지 않을 수도 있습니다.

다행히 Laravel은 이 문제를 우회할 수 있는 여러 메서드를 제공합니다. 먼저 큐 연결의 설정 배열에서 `after_commit` 연결 옵션을 설정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`이면 데이터베이스 트랜잭션 안에서 작업을 디스패치할 수 있습니다. 다만 Laravel은 열려 있는 부모 데이터베이스 트랜잭션이 커밋될 때까지 기다린 뒤 실제로 작업을 디스패치합니다. 물론 현재 열려 있는 데이터베이스 트랜잭션이 없다면 작업은 즉시 디스패치됩니다.

트랜잭션 중에 발생한 예외로 인해 트랜잭션이 롤백되면, 해당 트랜잭션 중에 디스패치된 작업은 폐기됩니다.

> [!NOTE]
> `after_commit` 설정 옵션을 `true`로 설정하면 큐에 들어간 이벤트 리스너, mailable, 알림, 브로드캐스트 이벤트도 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 뒤 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 디스패치 동작을 인라인으로 지정하기

`after_commit` 큐 연결 설정 옵션을 `true`로 설정하지 않았더라도, 특정 작업이 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 뒤 디스패치되어야 한다고 지정할 수 있습니다. 이를 위해 디스패치 작업에 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로 `after_commit` 설정 옵션이 `true`로 설정되어 있더라도, 특정 작업은 열려 있는 데이터베이스 트랜잭션의 커밋을 기다리지 않고 즉시 디스패치되어야 한다고 지정할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝

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
> 작업 안에서 `$this->delete()` 메서드를 사용하여 작업을 삭제해도 체이닝된 작업이 처리되는 것을 막지는 않습니다. 체인은 체인 안의 작업이 실패한 경우에만 실행을 중단합니다.

<a name="chain-connection-queue"></a>
#### 체인 연결과 큐

체이닝된 작업에 사용할 연결과 큐를 지정하고 싶다면 `onConnection`과 `onQueue` 메서드를 사용할 수 있습니다. 이 메서드들은 큐 작업에 다른 연결 / 큐가 명시적으로 할당되어 있지 않은 한 사용할 큐 연결과 큐 이름을 지정합니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

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
#### 체인 실패

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
> 체인 콜백은 직렬화된 뒤 Laravel 큐에서 나중에 실행되므로, 체인 콜백 안에서 `$this` 변수를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치하기

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
#### 특정 연결로 디스패치하기

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

`onConnection` 메서드와 `onQueue` 메서드를 함께 체이닝하여 작업의 연결과 큐를 지정할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

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
#### 큐 라우팅

`Queue` 파사드의 `route` 메서드를 사용하여 특정 작업 클래스에 대한 기본 연결과 큐를 정의할 수 있습니다. 특정 작업이 항상 지정된 큐를 사용하도록 보장하고 싶지만, 작업마다 연결이나 큐를 직접 지정하고 싶지는 않을 때 유용합니다.

특정 작업 클래스를 라우팅하는 것 외에도, 인터페이스, 트레이트, 부모 클래스를 `route` 메서드에 전달할 수 있습니다. 이렇게 하면 해당 인터페이스를 구현하거나, 트레이트를 사용하거나, 부모 클래스를 상속하는 모든 작업이 설정된 연결과 큐를 자동으로 사용합니다.

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

큐 없이 연결만 지정하면 작업은 기본 큐로 전송됩니다.

```php
Queue::route(ProcessPodcast::class, connection: 'redis');
```

`route` 메서드에 배열을 전달하여 여러 작업 클래스를 한 번에 라우팅할 수도 있습니다.

```php
Queue::route([
    ProcessPodcast::class => ['podcasts', 'redis'], // Queue and connection
    ProcessVideo::class => 'videos', // Queue only (uses default connection)
]);
```

> [!NOTE]
> 큐 라우팅은 여전히 각 작업 단위에서 작업이 재정의할 수 있습니다.

<a name="max-job-attempts-and-timeout"></a>
### 최대 작업 시도 횟수 / 타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수

작업 시도 횟수는 Laravel 큐 시스템의 핵심 개념이며, 여러 고급 기능의 기반이 됩니다. 처음에는 혼란스러울 수 있지만, 기본 설정을 변경하기 전에 이 개념이 어떻게 동작하는지 이해하는 것이 중요합니다.

작업이 디스패치되면 큐에 추가됩니다. 이후 워커가 해당 작업을 가져와 실행을 시도합니다. 이것이 작업 시도입니다.

하지만 시도 횟수가 증가했다고 해서 반드시 작업의 `handle` 메서드가 실행되었다는 뜻은 아닙니다. 시도 횟수는 다음과 같은 방식으로도 "소모"될 수 있습니다.

<div class="content-list" markdown="1">

- 작업 실행 중 처리되지 않은 예외가 발생합니다.
- `$this->release()`를 사용하여 작업을 수동으로 큐에 다시 돌려보냅니다.
- `WithoutOverlapping` 또는 `RateLimited` 같은 Middleware가 락을 획득하지 못하고 작업을 다시 큐에 돌려보냅니다.
- 작업이 타임아웃됩니다.
- 작업의 `handle` 메서드가 실행되고 예외를 던지지 않은 채 완료됩니다.

</div>

대부분의 경우 작업을 무한정 계속 시도하고 싶지는 않을 것입니다. 따라서 Laravel은 작업을 몇 번까지 또는 얼마 동안 시도할 수 있는지 지정하는 여러 방법을 제공합니다.

> [!NOTE]
> 기본적으로 Laravel은 작업을 한 번만 시도합니다. 작업이 `WithoutOverlapping` 또는 `RateLimited` 같은 Middleware를 사용하거나, 작업을 수동으로 다시 큐에 돌려보내는 경우에는 `tries` 옵션을 통해 허용되는 시도 횟수를 늘려야 할 가능성이 높습니다.

작업을 시도할 수 있는 최대 횟수를 지정하는 한 가지 방법은 Artisan 명령줄에서 `--tries` 스위치를 사용하는 것입니다. 처리 중인 작업 자체에서 시도 횟수를 지정하지 않는 한, 이 값은 워커가 처리하는 모든 작업에 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면 "실패한" 작업으로 간주됩니다. 실패한 작업을 처리하는 방법에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하십시오. `queue:work` 명령어에 `--tries=0`을 제공하면 작업을 무기한 재시도합니다.

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
#### 시간 기반 시도

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

`retryUntil`과 `tries`가 모두 정의되어 있으면 Laravel은 `retryUntil` 메서드를 우선합니다.

> [!NOTE]
> [큐에 넣는 이벤트 리스너](/docs/13.x/events#queued-event-listeners)와 [큐에 넣는 알림](/docs/13.x/notifications#queueing-notifications)에도 `Tries` 속성 또는 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수

때로는 작업을 여러 번 시도할 수 있도록 하되, 재시도가 특정 횟수의 처리되지 않은 예외 때문에 발생한 경우에는 실패하도록 지정하고 싶을 수 있습니다. 이는 `release` 메서드로 직접 다시 큐에 돌려보낸 경우와 구분됩니다. 이를 위해 작업 클래스에 `Tries` 및 `MaxExceptions` 속성을 사용할 수 있습니다.

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

이 예제에서는 애플리케이션이 Redis 락을 획득하지 못하면 작업을 10초 동안 다시 큐에 돌려보내며, 최대 25번까지 계속 재시도합니다. 하지만 작업에서 처리되지 않은 예외가 세 번 발생하면 해당 작업은 실패합니다.

<a name="timeout"></a>
#### 타임아웃

대개 큐 작업이 대략 얼마나 오래 걸릴지 알고 있습니다. 이런 이유로 Laravel은 "타임아웃" 값을 지정할 수 있도록 합니다. 기본 타임아웃 값은 60초입니다. 작업이 타임아웃 값으로 지정된 초 수보다 오래 처리되고 있으면, 해당 작업을 처리하던 워커가 오류와 함께 종료됩니다. 일반적으로 워커는 [서버에 설정된 프로세스 관리자](#supervisor-configuration)에 의해 자동으로 다시 시작됩니다.

작업이 실행될 수 있는 최대 초 수는 Artisan 명령줄에서 `--timeout` 스위치를 사용하여 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 계속 타임아웃되어 최대 시도 횟수를 초과하면 실패한 것으로 표시됩니다.

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

소켓이나 외부 HTTP 연결처럼 IO를 블로킹하는 프로세스는 지정한 타임아웃을 따르지 않을 수 있습니다. 따라서 이러한 기능을 사용할 때는 해당 API에서도 항상 타임아웃을 지정하려고 해야 합니다. 예를 들어 [Guzzle](https://docs.guzzlephp.org)을 사용할 때는 항상 연결 타임아웃과 요청 타임아웃 값을 지정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장이 설치되어 있어야 합니다. 또한 작업의 "타임아웃" 값은 항상 해당 작업의 ["retry after"](#job-expiration) 값보다 작아야 합니다. 그렇지 않으면 작업이 실제로 실행을 끝내거나 타임아웃되기 전에 다시 시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

타임아웃이 발생했을 때 작업을 [실패한 작업](#dealing-with-failed-jobs)으로 표시하고 싶다면, 작업 클래스에 `FailOnTimeout` 속성을 사용할 수 있습니다.

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
> 기본적으로 작업이 타임아웃되면 시도 횟수 하나를 소모하고 다시 큐로 돌려보내집니다(재시도가 허용된 경우). 하지만 작업을 타임아웃 시 실패하도록 설정하면 `tries`에 설정된 값과 관계없이 재시도되지 않습니다.

<a name="sqs-fifo-and-fair-queues"></a>
### SQS FIFO와 공정 큐

Laravel은 [Amazon SQS FIFO (First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) 큐와 [공정](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html) 큐를 지원합니다. FIFO 큐를 사용하면 작업이 전송된 정확한 순서대로 처리할 수 있으며, 메시지 중복 제거를 통해 정확히 한 번만 처리되도록 보장할 수 있습니다.

FIFO 큐는 어떤 작업을 병렬로 처리할 수 있는지 결정하기 위해 메시지 그룹 ID가 필요합니다. 같은 그룹 ID를 가진 작업은 순차적으로 처리되고, 서로 다른 그룹 ID를 가진 메시지는 동시에 처리될 수 있습니다.

Laravel은 작업을 디스패치할 때 메시지 그룹 ID를 지정할 수 있도록 유창한 `onGroup` 메서드를 제공합니다.

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```

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
#### 공정 큐

SQS 표준 큐를 사용하는 경우 메시지 그룹을 설정하면 공정 큐잉이 활성화됩니다. 즉, 그룹을 할당하면 SQS는 이를 사용하여 테넌트 / 워크로드 간에 공정한 전달을 유지합니다. 추가적인 Laravel 설정은 필요하지 않습니다.

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
#### FIFO 리스너, 메일 및 알림

FIFO 큐를 사용할 때는 리스너, 메일, 알림에도 메시지 그룹을 정의해야 합니다. 또는 이러한 객체의 큐 인스턴스를 FIFO가 아닌 큐로 디스패치할 수도 있습니다.

[큐에 등록되는 이벤트 리스너](/docs/13.x/events#queued-event-listeners)의 메시지 그룹을 정의하려면 리스너에 `messageGroup` 메서드를 정의합니다. 선택적으로 `deduplicationId` 메서드도 정의할 수 있습니다.

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

FIFO 큐에서 처리될 [메일 메시지](/docs/13.x/mail)를 보낼 때는 `onGroup` 메서드를 호출해야 하며, 선택적으로 `withDeduplicator` 메서드도 호출할 수 있습니다.

```php
use App\Mail\InvoicePaid;
use Illuminate\Support\Facades\Mail;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```

FIFO 큐에서 처리될 [알림](/docs/13.x/notifications)을 보낼 때는 `onGroup` 메서드를 호출해야 하며, 선택적으로 `withDeduplicator` 메서드도 호출할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```

<a name="queue-failover"></a>
### 큐 장애 조치

`failover` 큐 드라이버는 작업을 큐에 넣을 때 자동 장애 조치 기능을 제공합니다. `failover` 설정의 기본 큐 연결이 어떤 이유로든 실패하면, Laravel은 설정된 목록의 다음 연결로 작업을 넣으려고 자동으로 시도합니다. 이는 큐 안정성이 중요한 프로덕션 환경에서 높은 가용성을 보장하는 데 특히 유용합니다.

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

`failover` 드라이버를 사용하는 연결을 설정한 뒤에는, 장애 조치 기능을 사용하기 위해 애플리케이션의 `.env` 파일에서 장애 조치 연결을 기본 큐 연결로 설정해야 합니다.

```ini
QUEUE_CONNECTION=failover
```

다음으로, 장애 조치 연결 목록에 있는 각 연결마다 최소 하나의 워커를 시작합니다.

```bash
php artisan queue:work redis
php artisan queue:work database
```

> [!NOTE]
> `sync`, `background`, `deferred` 큐 드라이버를 사용하는 연결에는 워커를 실행할 필요가 없습니다. 이러한 드라이버는 현재 PHP 프로세스 안에서 작업을 처리하기 때문입니다.

큐 연결 작업이 실패하여 장애 조치가 활성화되면, Laravel은 `Illuminate\Queue\Events\QueueFailedOver` 이벤트를 디스패치합니다. 이를 통해 큐 연결 실패를 보고하거나 로그로 남길 수 있습니다.

> [!NOTE]
> Laravel Horizon을 사용하는 경우, Horizon은 Redis 큐만 관리한다는 점을 기억하십시오. 장애 조치 목록에 `database`가 포함되어 있다면 Horizon과 함께 일반 `php artisan queue:work database` 프로세스도 실행해야 합니다.

<a name="error-handling"></a>
### 오류 처리

작업이 처리되는 동안 예외가 발생하면, 해당 작업은 다시 시도될 수 있도록 자동으로 큐에 다시 반환됩니다. 작업은 애플리케이션에서 허용한 최대 시도 횟수에 도달할 때까지 계속 다시 반환됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령어에서 사용하는 `--tries` 스위치로 정의됩니다. 또는 작업 클래스 자체에 최대 시도 횟수를 정의할 수도 있습니다. 큐 워커 실행에 대한 자세한 정보는 [아래에서 확인할 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업 수동 반환

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

기본적으로 `release` 메서드는 작업을 즉시 처리할 수 있도록 큐에 다시 반환합니다. 하지만 `release` 메서드에 정수나 날짜 인스턴스를 전달하면, 지정한 초가 지난 뒤에야 작업을 처리할 수 있도록 큐에 지시할 수 있습니다.

```php
$this->release(10);

$this->release(now()->plus(seconds: 10));
```

<a name="manually-failing-a-job"></a>
#### 작업 수동 실패 처리

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

잡은 예외 때문에 작업을 실패로 표시하려는 경우, 해당 예외를 `fail` 메서드에 전달할 수 있습니다. 또는 편의를 위해 문자열 오류 메시지를 전달할 수 있으며, 이 메시지는 자동으로 예외로 변환됩니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 자세한 정보는 [작업 실패 처리 문서](#dealing-with-failed-jobs)를 참고하십시오.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외에서 작업 실패 처리

`FailOnException` [작업 미들웨어](#job-middleware)를 사용하면 특정 예외가 발생했을 때 재시도를 중단할 수 있습니다. 이를 통해 외부 API 오류처럼 일시적인 예외에서는 재시도하되, 사용자의 권한이 취소된 경우처럼 지속적인 예외에서는 작업을 영구적으로 실패 처리할 수 있습니다.

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
## 작업 배치 처리 (Job Batching)

Laravel의 작업 배치 처리 기능을 사용하면 작업 그룹을 병렬로 쉽게 실행하고, 해당 작업 배치의 실행이 완료된 뒤 어떤 동작을 수행할 수 있습니다.

시작하기 전에 작업 배치에 대한 메타 정보, 예를 들어 완료율 같은 정보를 담을 테이블을 만들기 위한 데이터베이스 마이그레이션을 생성해야 합니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령어를 사용해 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 작업 정의

배치 가능한 작업을 정의하려면 일반적인 방식으로 [큐에 넣을 수 있는 작업을 생성](#creating-jobs)합니다. 다만 작업 클래스에 `Illuminate\Bus\Batchable` 트레이트를 추가해야 합니다. 이 트레이트는 현재 작업이 실행되고 있는 배치를 가져오는 데 사용할 수 있는 `batch` 메서드에 접근할 수 있게 해줍니다.

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
### 배치 디스패치

작업 배치를 디스패치하려면 `Bus` 파사드의 `batch` 메서드를 사용합니다. 물론 배치 처리는 완료 콜백과 함께 사용할 때 가장 유용합니다. 따라서 `then`, `catch`, `finally` 메서드를 사용해 배치의 완료 콜백을 정의할 수 있습니다. 이러한 각 콜백은 호출될 때 `Illuminate\Bus\Batch` 인스턴스를 전달받습니다.

여러 큐 워커를 실행하는 경우, 배치 안의 작업은 병렬로 처리됩니다. 따라서 작업이 완료되는 순서는 배치에 추가된 순서와 같지 않을 수 있습니다. 일련의 작업을 순서대로 실행하는 방법은 [작업 체인과 배치](#chains-and-batches) 문서를 참고하십시오.

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

`$batch->id` 속성으로 접근할 수 있는 배치의 ID는 배치가 디스패치된 뒤 해당 배치 정보를 [Laravel command bus에 조회](#inspecting-batches)하는 데 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화된 뒤 나중에 Laravel 큐에서 실행되므로, 콜백 안에서 `$this` 변수를 사용해서는 안 됩니다. 또한 배치 작업은 데이터베이스 트랜잭션 안에서 감싸져 실행되므로, 암묵적 커밋을 유발하는 데이터베이스 문을 작업 안에서 실행해서는 안 됩니다.

<a name="naming-batches"></a>
#### 배치 이름 지정

[Laravel Horizon](/docs/13.x/horizon), [Laravel Telescope](/docs/13.x/telescope) 같은 일부 도구는 배치에 이름이 지정되어 있으면 더 사용자 친화적인 디버그 정보를 제공할 수 있습니다. 배치에 임의의 이름을 지정하려면 배치를 정의할 때 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 연결 및 큐

배치 작업에 사용할 연결과 큐를 지정하려면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 연결과 큐 안에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치

배치 안에 [체인으로 연결된 작업](#job-chaining) 집합을 정의하려면, 체인 작업을 배열 안에 넣으면 됩니다. 예를 들어 두 개의 작업 체인을 병렬로 실행하고, 두 작업 체인이 모두 처리를 마쳤을 때 콜백을 실행할 수 있습니다.

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

반대로, [체인](#job-chaining) 안에서 배치를 정의하여 작업 배치를 실행할 수도 있습니다. 예를 들어 먼저 여러 팟캐스트를 릴리스하는 작업 배치를 실행한 뒤, 릴리스 알림을 보내는 작업 배치를 실행할 수 있습니다.

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
> 같은 배치에 속한 작업 안에서만 해당 배치에 작업을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 살펴보기

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
#### 라우트에서 배치 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON으로 직렬화할 수 있습니다. 즉, 애플리케이션의 라우트에서 직접 반환하여 완료 진행률을 포함한 배치 정보를 담은 JSON 페이로드를 가져올 수 있습니다. 이를 사용하면 애플리케이션 UI에서 배치의 완료 진행률 정보를 쉽게 표시할 수 있습니다.

ID로 배치를 가져오려면 `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소하기

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
### 배치 실패

배치 작업이 실패하면 `catch` 콜백이 지정되어 있는 경우 호출됩니다. 이 콜백은 배치 안에서 처음 실패한 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용하기

배치 안의 작업이 실패하면 Laravel은 자동으로 배치를 "cancelled" 상태로 표시합니다. 원한다면 이 동작을 비활성화하여 작업 실패가 배치를 자동으로 취소 상태로 만들지 않도록 할 수 있습니다. 배치를 디스패치할 때 `allowFailures` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->allowFailures()->dispatch();
```

선택적으로 `allowFailures` 메서드에 클로저를 전달할 수 있으며, 이 클로저는 각 작업 실패 시 실행됩니다.

```php
$batch = Bus::batch([
    // ...
])->allowFailures(function (Batch $batch, $exception) {
    // Handle individual job failures...
})->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 다시 시도하기

편의를 위해 Laravel은 주어진 배치에서 실패한 모든 작업을 쉽게 다시 시도할 수 있는 `queue:retry-batch` Artisan 명령어를 제공합니다. 이 명령어는 실패한 작업을 다시 시도할 배치의 UUID를 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 정리하기

정리하지 않으면 `job_batches` 테이블에 레코드가 매우 빠르게 쌓일 수 있습니다. 이를 완화하려면 `queue:prune-batches` Artisan 명령어가 매일 실행되도록 [schedule](/docs/13.x/scheduling)에 등록해야 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로 완료된 지 24시간이 지난 모든 배치는 정리됩니다. 명령어를 호출할 때 `hours` 옵션을 사용하여 배치 데이터를 얼마나 오래 보관할지 결정할 수 있습니다. 예를 들어 다음 명령어는 48시간보다 더 전에 완료된 모든 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

때로는 작업이 실패했고 해당 작업이 다시 성공적으로 시도되지 않은 배치처럼, 성공적으로 완료되지 않은 배치의 레코드가 `job_batches` 테이블에 쌓일 수 있습니다. `unfinished` 옵션을 사용하면 `queue:prune-batches` 명령어가 이러한 미완료 배치 레코드를 정리하도록 지시할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로 `job_batches` 테이블에는 취소된 배치의 레코드도 쌓일 수 있습니다. `cancelled` 옵션을 사용하면 `queue:prune-batches` 명령어가 이러한 취소된 배치 레코드를 정리하도록 지시할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장하기

Laravel은 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 메타 정보를 저장하는 기능도 지원합니다. 다만 모든 배치 레코드를 저장할 DynamoDB 테이블은 직접 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`여야 하지만, 애플리케이션의 `queue` 설정 파일 안에 있는 `queue.batching.table` 설정 값에 따라 테이블 이름을 지정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 설정

`job_batches` 테이블에는 `application`이라는 문자열 기본 파티션 키와 `id`라는 문자열 기본 정렬 키가 있어야 합니다. 키의 `application` 부분에는 애플리케이션의 `app` 설정 파일 안에 있는 `name` 설정 값으로 정의된 애플리케이션 이름이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블 키의 일부이므로, 동일한 테이블을 사용하여 여러 Laravel 애플리케이션의 작업 배치를 저장할 수 있습니다.

또한 [자동 배치 정리](#pruning-batches-in-dynamodb)를 활용하려면 테이블에 `ttl` 속성을 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로 Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

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
#### DynamoDB에서 배치 정리하기

작업 배치 정보를 저장하는 데 [DynamoDB](https://aws.amazon.com/dynamodb)를 사용하는 경우, 관계형 데이터베이스에 저장된 배치를 정리할 때 사용하는 일반적인 정리 명령어는 동작하지 않습니다. 대신 [DynamoDB의 네이티브 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 사용하여 오래된 배치의 레코드를 자동으로 제거할 수 있습니다.

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
## 클로저 큐잉 (Queueing Closures)

작업 클래스를 큐에 디스패치하는 대신 클로저를 디스패치할 수도 있습니다. 이는 현재 요청 사이클 밖에서 실행되어야 하는 빠르고 단순한 작업에 적합합니다. 클로저를 큐에 디스패치할 때 클로저의 코드 내용은 암호학적으로 서명되므로 전송 중에 수정될 수 없습니다.

```php
use App\Models\Podcast;

$podcast = Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐 보고 대시보드에서 사용할 수 있고 `queue:work` 명령어에도 표시되는 큐 클로저 이름을 지정하려면 `name` 메서드를 사용할 수 있습니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

`catch` 메서드를 사용하면 큐에 등록된 클로저가 큐의 [설정된 재시도 횟수](#max-job-attempts-and-timeout)를 모두 소진한 뒤에도 성공적으로 완료되지 못했을 때 실행할 클로저를 제공할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

> [!WARNING]
> `catch` 콜백은 직렬화된 뒤 나중에 Laravel 큐에서 실행되므로, `catch` 콜백 안에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기 (Running the Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel에는 큐 워커를 시작하고 큐에 새 작업이 추가될 때 이를 처리하는 Artisan 명령어가 포함되어 있습니다. `queue:work` Artisan 명령어를 사용하여 워커를 실행할 수 있습니다. `queue:work` 명령어가 시작되면 직접 중지하거나 터미널을 닫을 때까지 계속 실행된다는 점에 유의하십시오.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 계속 실행 상태로 유지하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용하여 큐 워커가 중지되지 않도록 해야 합니다.

처리된 작업 ID, 연결 이름, 큐 이름을 명령어 출력에 포함하려면 `queue:work` 명령어를 실행할 때 `-v` 플래그를 포함할 수 있습니다.

```shell
php artisan queue:work -v
```

큐 워커는 오래 실행되는 프로세스이며 부팅된 애플리케이션 상태를 메모리에 저장한다는 점을 기억하십시오. 따라서 시작된 이후에는 코드베이스의 변경 사항을 감지하지 못합니다. 그러므로 배포 과정에서 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해야 합니다. 또한 애플리케이션에서 생성하거나 수정한 모든 정적 상태는 작업 사이에 자동으로 초기화되지 않는다는 점도 기억해야 합니다.

또는 `queue:listen` 명령어를 실행할 수 있습니다. `queue:listen` 명령어를 사용하면 업데이트된 코드를 다시 로드하거나 애플리케이션 상태를 초기화하고 싶을 때 워커를 수동으로 재시작할 필요가 없습니다. 하지만 이 명령어는 `queue:work` 명령어보다 훨씬 비효율적입니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

하나의 큐에 여러 워커를 할당하고 작업을 동시에 처리하려면 여러 `queue:work` 프로세스를 시작하면 됩니다. 로컬에서는 터미널의 여러 탭을 통해 실행할 수 있고, 프로덕션에서는 프로세스 매니저의 설정을 통해 실행할 수 있습니다. [Supervisor를 사용할 때](#supervisor-configuration)는 `numprocs` 설정 값을 사용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
#### 연결과 큐 지정하기

워커가 사용할 큐 연결도 지정할 수 있습니다. `work` 명령어에 전달하는 연결 이름은 `config/queue.php` 설정 파일에 정의된 연결 중 하나와 일치해야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령어는 주어진 연결에서 기본 큐의 작업만 처리합니다. 하지만 주어진 연결의 특정 큐만 처리하도록 큐 워커를 더 세밀하게 사용자 정의할 수 있습니다. 예를 들어 모든 이메일이 `redis` 큐 연결의 `emails` 큐에서 처리된다면, 다음 명령어를 실행하여 해당 큐만 처리하는 워커를 시작할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정한 수의 작업 처리하기

`--once` 옵션을 사용하면 워커가 큐에서 단일 작업만 처리하도록 지시할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션을 사용하면 워커가 지정한 수의 작업을 처리한 뒤 종료하도록 지시할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용할 때 유용할 수 있습니다. 지정된 수의 작업을 처리한 뒤 워커가 자동으로 재시작되므로, 워커가 누적했을 수 있는 메모리를 해제할 수 있습니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐에 있는 모든 작업을 처리한 뒤 종료하기

`--stop-when-empty` 옵션을 사용하면 워커가 모든 작업을 처리한 뒤 정상적으로 종료하도록 지시할 수 있습니다. Docker 컨테이너 안에서 Laravel 큐를 처리하고 있고 큐가 비면 컨테이너를 종료하고 싶을 때 유용할 수 있습니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정한 초 동안 작업 처리하기

`--max-time` 옵션을 사용하면 워커가 지정한 초 동안 작업을 처리한 뒤 종료하도록 지시할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용할 때 유용할 수 있습니다. 지정된 시간 동안 작업을 처리한 뒤 워커가 자동으로 재시작되므로, 워커가 누적했을 수 있는 메모리를 해제할 수 있습니다.

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 대기 시간

큐에 처리할 작업이 있으면 워커는 작업 사이에 지연 없이 계속 작업을 처리합니다. 하지만 처리할 작업이 없을 때 워커가 몇 초 동안 "sleep"할지는 `sleep` 옵션이 결정합니다. 물론 대기 중인 동안 워커는 새 작업을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지 관리 모드와 큐

애플리케이션이 [maintenance mode](/docs/13.x/configuration#maintenance-mode)에 있는 동안에는 큐에 등록된 작업이 처리되지 않습니다. 애플리케이션이 유지 관리 모드에서 벗어나면 작업은 평소처럼 계속 처리됩니다.

유지 관리 모드가 활성화되어 있어도 큐 워커가 작업을 처리하도록 강제하려면 `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 고려 사항

데몬 큐 워커는 각 작업을 처리하기 전에 프레임워크를 "reboot"하지 않습니다. 따라서 각 작업이 완료된 뒤 무거운 리소스를 해제해야 합니다. 예를 들어 [GD library](https://www.php.net/manual/en/book.image.php)를 사용하여 이미지 조작을 수행하는 경우, 이미지 처리가 끝나면 `imagedestroy`로 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

때로는 큐가 처리되는 방식에 우선순위를 지정하고 싶을 수 있습니다. 예를 들어 `config/queue.php` 설정 파일에서 `redis` 연결의 기본 `queue`를 `low`로 설정할 수 있습니다. 하지만 때때로 다음과 같이 작업을 `high` 우선순위 큐로 푸시하고 싶을 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`low` 큐의 작업을 계속 처리하기 전에 모든 `high` 큐 작업이 처리되었는지 확인하는 워커를 시작하려면, 큐 이름을 쉼표로 구분한 목록으로 `work` 명령어에 전달합니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

큐 워커는 오래 실행되는 프로세스이므로 재시작하지 않으면 코드 변경 사항을 감지하지 못합니다. 따라서 큐 워커를 사용하는 애플리케이션을 배포하는 가장 간단한 방법은 배포 과정에서 워커를 재시작하는 것입니다. `queue:restart` 명령어를 실행하여 모든 워커를 정상적으로 재시작할 수 있습니다.

```shell
php artisan queue:restart
```

이 명령어는 기존 작업이 손실되지 않도록 모든 큐 워커에게 현재 작업 처리를 마친 뒤 정상적으로 종료하라고 지시합니다. `queue:restart` 명령어가 실행되면 큐 워커가 종료되므로, 큐 워커를 자동으로 재시작하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 매니저를 실행하고 있어야 합니다.

> [!NOTE]
> 큐는 재시작 신호를 저장하기 위해 [cache](/docs/13.x/cache)를 사용하므로, 이 기능을 사용하기 전에 애플리케이션에 캐시 드라이버가 제대로 설정되어 있는지 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료와 시간 제한

<a name="job-expiration"></a>
#### 작업 만료
`config/queue.php` 설정 파일에서 각 큐 연결은 `retry_after` 옵션을 정의합니다. 이 옵션은 처리 중인 작업을 다시 시도하기 전에 큐 연결이 몇 초 동안 기다려야 하는지를 지정합니다. 예를 들어 `retry_after` 값이 `90`으로 설정되어 있으면, 작업이 해제되거나 삭제되지 않은 상태로 90초 동안 처리되고 있을 때 해당 작업은 다시 큐로 반환됩니다. 일반적으로 `retry_after` 값은 작업이 합리적으로 완료되는 데 걸릴 수 있는 최대 시간(초)으로 설정해야 합니다.

> [!WARNING]
> `retry_after` 값을 포함하지 않는 유일한 큐 연결은 Amazon SQS입니다. SQS는 AWS 콘솔에서 관리되는 [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)을 기준으로 작업을 다시 시도합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` Artisan 명령어는 `--timeout` 옵션을 제공합니다. 기본적으로 `--timeout` 값은 60초입니다. 작업이 타임아웃 값으로 지정한 시간보다 오래 처리되면, 해당 작업을 처리하던 워커는 오류와 함께 종료됩니다. 일반적으로 워커는 [서버에 설정된 프로세스 관리자](#supervisor-configuration)에 의해 자동으로 다시 시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정 옵션과 `--timeout` CLI 옵션은 서로 다르지만, 함께 동작하여 작업이 유실되지 않도록 하고 작업이 한 번만 성공적으로 처리되도록 보장합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 설정 값보다 최소 몇 초 이상 짧아야 합니다. 이렇게 하면 멈춘 작업을 처리 중인 워커가 작업이 다시 시도되기 전에 항상 종료됩니다. `--timeout` 옵션이 `retry_after` 설정 값보다 길면 작업이 두 번 처리될 수 있습니다.

<a name="pausing-and-resuming-queue-workers"></a>
### 큐 워커 일시 중지 및 재개

때로는 워커를 완전히 중지하지 않고, 큐 워커가 새 작업을 처리하지 못하도록 일시적으로 막아야 할 수 있습니다. 예를 들어 시스템 유지보수 중에는 작업 처리를 일시 중지하고 싶을 수 있습니다. Laravel은 큐 워커를 일시 중지하고 재개할 수 있도록 `queue:pause` 및 `queue:continue` Artisan 명령어를 제공합니다.

특정 큐를 일시 중지하려면 큐 연결 이름과 큐 이름을 전달합니다.

```shell
php artisan queue:pause database:default
```

이 예제에서 `database`는 큐 연결 이름이고 `default`는 큐 이름입니다. 큐가 일시 중지되면 해당 큐에서 작업을 처리 중인 워커는 현재 작업을 계속 완료하지만, 큐가 재개될 때까지 새 작업을 가져오지 않습니다.

일시 중지된 큐에서 작업 처리를 재개하려면 `queue:continue` 명령어를 사용합니다.

```shell
php artisan queue:continue database:default
```

큐를 재개하면 워커는 즉시 해당 큐에서 새 작업 처리를 시작합니다. 큐를 일시 중지해도 워커 프로세스 자체가 중지되는 것은 아닙니다. 지정한 큐에서 새 작업을 처리하지 못하도록 막을 뿐입니다.

<a name="worker-restart-and-pause-signals"></a>
#### 워커 재시작 및 일시 중지 신호

기본적으로 큐 워커는 각 작업 반복마다 재시작 및 일시 중지 신호가 있는지 캐시 드라이버를 폴링합니다. 이 폴링은 `queue:restart` 및 `queue:pause` 명령어에 응답하는 데 필수적이지만, 약간의 성능 오버헤드를 발생시킵니다.

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
> 중단 폴링이 비활성화되면 워커는 비활성화된 기능에 따라 `queue:restart` 또는 `queue:pause` 명령어에 응답하지 않습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정 (Supervisor Configuration)

프로덕션 환경에서는 `queue:work` 프로세스가 계속 실행되도록 유지하는 방법이 필요합니다. `queue:work` 프로세스는 워커 타임아웃 초과나 `queue:restart` 명령어 실행 등 다양한 이유로 중지될 수 있습니다.

이러한 이유로 `queue:work` 프로세스가 종료되는 것을 감지하고 자동으로 다시 시작할 수 있는 프로세스 모니터를 설정해야 합니다. 또한 프로세스 모니터를 사용하면 동시에 실행할 `queue:work` 프로세스 수를 지정할 수 있습니다. Supervisor는 Linux 환경에서 흔히 사용되는 프로세스 모니터이며, 다음 문서에서 설정 방법을 설명합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영 체제용 프로세스 모니터이며, `queue:work` 프로세스가 실패하면 자동으로 다시 시작합니다. Ubuntu에 Supervisor를 설치하려면 다음 명령어를 사용할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor를 직접 설정하고 관리하는 일이 부담스럽다면 [Laravel Cloud](https://cloud.laravel.com) 사용을 고려해 보십시오. Laravel Cloud는 Laravel 큐 워커를 실행할 수 있는 완전 관리형 플랫폼을 제공합니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정하기

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

이 예제에서 `numprocs` 지시어는 Supervisor에게 여덟 개의 `queue:work` 프로세스를 실행하고 모두 모니터링하며, 실패하면 자동으로 다시 시작하도록 지시합니다. 설정의 `command` 지시어는 원하는 큐 연결과 워커 옵션에 맞게 변경해야 합니다.

> [!WARNING]
> `stopwaitsecs` 값이 가장 오래 실행되는 작업이 사용하는 시간(초)보다 큰지 확인해야 합니다. 그렇지 않으면 Supervisor가 작업 처리가 끝나기 전에 해당 작업을 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일을 만든 후에는 다음 명령어를 사용하여 Supervisor 설정을 갱신하고 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 자세한 내용은 [Supervisor 문서](http://supervisord.org/index.html)를 참고하십시오.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리하기 (Dealing With Failed Jobs)

때로는 큐에 등록된 작업이 실패할 수 있습니다. 걱정하지 마십시오. 모든 일이 항상 계획대로 진행되지는 않습니다! Laravel에는 [작업을 시도할 최대 횟수를 지정](#max-job-attempts-and-timeout)하는 편리한 방법이 포함되어 있습니다. 비동기 작업이 이 시도 횟수를 초과하면 `failed_jobs` 데이터베이스 테이블에 삽입됩니다. 실패한 [동기적으로 디스패치된 작업](/docs/13.x/queues#synchronous-dispatching)은 이 테이블에 저장되지 않으며, 예외는 애플리케이션에서 즉시 처리됩니다.

`failed_jobs` 테이블을 생성하는 마이그레이션은 일반적으로 새 Laravel 애플리케이션에 이미 포함되어 있습니다. 하지만 애플리케이션에 이 테이블을 위한 마이그레이션이 없다면 `make:queue-failed-table` 명령어를 사용하여 마이그레이션을 만들 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때 `queue:work` 명령어의 `--tries` 스위치를 사용하여 작업을 시도할 최대 횟수를 지정할 수 있습니다. `--tries` 옵션 값을 지정하지 않으면 작업은 한 번만 시도되거나, 작업 클래스의 `Tries` 속성에 지정된 횟수만큼 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면 예외가 발생한 작업을 다시 시도하기 전에 Laravel이 몇 초 동안 기다려야 하는지 지정할 수 있습니다. 기본적으로 작업은 즉시 다시 큐로 반환되어 다시 시도될 수 있습니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

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
### 실패한 작업 이후 정리하기

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
> `failed` 메서드를 호출하기 전에 작업의 새 인스턴스가 생성됩니다. 따라서 `handle` 메서드 안에서 발생했을 수 있는 클래스 속성 변경 사항은 사라집니다.

실패한 작업이 반드시 처리되지 않은 예외를 만난 작업만을 의미하지는 않습니다. 허용된 모든 시도 횟수를 소진한 작업도 실패한 것으로 간주될 수 있습니다. 이러한 시도 횟수는 여러 방식으로 소모될 수 있습니다.

<div class="content-list" markdown="1">

- 작업이 타임아웃되었습니다.
- 작업 실행 중 처리되지 않은 예외가 발생했습니다.
- 작업이 수동으로 또는 Middleware에 의해 다시 큐로 반환되었습니다.

</div>

마지막 시도가 작업 실행 중 발생한 예외 때문에 실패했다면, 해당 예외가 작업의 `failed` 메서드에 전달됩니다. 하지만 작업이 허용된 최대 시도 횟수에 도달해서 실패했다면 `$exception`은 `Illuminate\Queue\MaxAttemptsExceededException`의 인스턴스가 됩니다. 마찬가지로 설정된 타임아웃을 초과해서 작업이 실패했다면 `$exception`은 `Illuminate\Queue\TimeoutExceededException`의 인스턴스가 됩니다.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 다시 시도하기

`failed_jobs` 데이터베이스 테이블에 삽입된 모든 실패한 작업을 보려면 `queue:failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어는 작업 ID, 연결, 큐, 실패 시간 및 작업에 대한 기타 정보를 나열합니다. 작업 ID는 실패한 작업을 다시 시도하는 데 사용할 수 있습니다. 예를 들어 ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패한 작업을 다시 시도하려면 다음 명령어를 실행합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 명령어에 여러 ID를 전달할 수 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐의 모든 실패한 작업을 다시 시도할 수도 있습니다.

```shell
php artisan queue:retry --queue=name
```

모든 실패한 작업을 다시 시도하려면 `queue:retry` 명령어를 실행하고 ID로 `all`을 전달합니다.

```shell
php artisan queue:retry all
```

실패한 작업을 삭제하고 싶다면 `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/13.x/horizon)을 사용할 때는 실패한 작업을 삭제하기 위해 `queue:forget` 명령어 대신 `horizon:forget` 명령어를 사용해야 합니다.

`failed_jobs` 테이블에서 모든 실패한 작업을 삭제하려면 `queue:flush` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:flush
```

`queue:flush` 명령어는 실패한 작업이 얼마나 오래되었는지와 관계없이 큐에서 모든 실패한 작업 레코드를 제거합니다. `--hours` 옵션을 사용하면 특정 시간 전 또는 그보다 더 이전에 실패한 작업만 삭제할 수 있습니다.

```shell
php artisan queue:flush --hours=48
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시하기

Eloquent 모델을 작업에 주입하면, 모델은 큐에 들어가기 전에 자동으로 직렬화되고 작업이 처리될 때 데이터베이스에서 다시 조회됩니다. 하지만 작업이 워커에 의해 처리되기를 기다리는 동안 모델이 삭제되었다면, 작업은 `ModelNotFoundException`으로 실패할 수 있습니다.

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
### 실패한 작업 정리하기

`queue:prune-failed` Artisan 명령어를 호출하여 애플리케이션의 `failed_jobs` 테이블에 있는 레코드를 정리할 수 있습니다.

```shell
php artisan queue:prune-failed
```

기본적으로 24시간보다 오래된 모든 실패한 작업 레코드가 정리됩니다. 명령어에 `--hours` 옵션을 제공하면, 최근 N시간 이내에 삽입된 실패한 작업 레코드만 유지됩니다. 예를 들어 다음 명령어는 48시간보다 더 전에 삽입된 모든 실패한 작업 레코드를 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패한 작업 저장하기

Laravel은 실패한 작업 레코드를 관계형 데이터베이스 테이블 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 기능도 지원합니다. 하지만 모든 실패한 작업 레코드를 저장할 DynamoDB 테이블은 직접 만들어야 합니다. 일반적으로 이 테이블 이름은 `failed_jobs`여야 하지만, 애플리케이션의 `queue` 설정 파일 안에 있는 `queue.failed.table` 설정 값에 따라 테이블 이름을 정해야 합니다.

`failed_jobs` 테이블에는 `application`이라는 문자열 기본 파티션 키와 `uuid`라는 문자열 기본 정렬 키가 있어야 합니다. 키의 `application` 부분에는 애플리케이션의 `app` 설정 파일 안에 있는 `name` 설정 값으로 정의된 애플리케이션 이름이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블 키의 일부이므로, 같은 테이블을 사용하여 여러 Laravel 애플리케이션의 실패한 작업을 저장할 수 있습니다.

또한 Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

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
### 실패한 작업 저장 비활성화하기

`queue.failed.driver` 설정 옵션 값을 `null`로 설정하여 Laravel이 실패한 작업을 저장하지 않고 폐기하도록 지시할 수 있습니다. 일반적으로 이는 `QUEUE_FAILED_DRIVER` 환경 변수를 통해 설정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 작업 이벤트

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
## 큐에서 작업 비우기 (Clearing Jobs From Queues)

> [!NOTE]
> [Horizon](/docs/13.x/horizon)을 사용할 때는 큐에서 작업을 비우기 위해 `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용해야 합니다.

기본 연결의 기본 큐에서 모든 작업을 삭제하려면 `queue:clear` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결과 큐에서 작업을 삭제하려면 `connection` 인수와 `queue` 옵션을 함께 제공할 수도 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 비우는 기능은 SQS, Redis, database 큐 드라이버에서만 사용할 수 있습니다. 또한 SQS 메시지 삭제 과정은 최대 60초가 걸리므로, 큐를 비운 뒤 최대 60초 안에 SQS 큐로 전송된 작업도 함께 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

큐에 작업이 갑자기 많이 들어오면 큐가 감당하기 어려워지고, 작업이 완료되기까지 대기 시간이 길어질 수 있습니다. 원한다면 Laravel이 큐 작업 수가 지정한 임계값을 초과했을 때 알림을 보내도록 설정할 수 있습니다.

시작하려면 `queue:monitor` 명령어가 [매분 실행](/docs/13.x/scheduling)되도록 스케줄링해야 합니다. 이 명령어는 모니터링할 큐 이름과 원하는 작업 수 임계값을 인수로 받습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

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
## 테스트 (Testing)

작업을 디스패치하는 코드를 테스트할 때는 작업 자체가 실제로 실행되지 않도록 Laravel에 지시하고 싶을 수 있습니다. 작업의 코드는 해당 작업을 디스패치하는 코드와 분리해서 직접 테스트할 수 있기 때문입니다. 물론 작업 자체를 테스트하려면 테스트에서 작업 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

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
### 일부 작업만 가짜 처리하기

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

`except` 메서드를 사용하면 지정한 작업 집합을 제외한 모든 작업을 가짜 처리할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 작업 체인 테스트

작업 체인을 테스트하려면 `Bus` 파사드의 가짜 처리 기능을 사용해야 합니다. `Bus` 파사드의 `assertChained` 메서드는 [작업 체인](/docs/13.x/queues#job-chaining)이 디스패치되었는지 검증하는 데 사용할 수 있습니다. `assertChained` 메서드는 첫 번째 인수로 체인으로 연결된 작업 배열을 받습니다.

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

위 예제에서 볼 수 있듯이, 체인으로 연결된 작업 배열은 작업의 클래스 이름 배열일 수 있습니다. 하지만 실제 작업 인스턴스 배열을 제공할 수도 있습니다. 이 경우 Laravel은 애플리케이션에서 디스패치한 체인 작업과 제공된 작업 인스턴스가 같은 클래스이며 같은 속성 값을 가지는지 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

작업이 작업 체인 없이 푸시되었는지 검증하려면 `assertDispatchedWithoutChain` 메서드를 사용할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

체인으로 연결된 작업이 [기존 체인의 앞이나 뒤에 작업을 추가](#adding-jobs-to-the-chain)한다면, 해당 작업의 `assertHasChain` 메서드를 사용하여 작업에 예상한 나머지 작업 체인이 있는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

작업의 남은 체인이 비어 있는지 검증하려면 `assertDoesntHaveChain` 메서드를 사용할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인된 배치 테스트

작업 체인에 [작업 배치가 포함되어](#chains-and-batches) 있다면, 체인 검증 안에 `Bus::chainedBatch` 정의를 삽입하여 체인된 배치가 기대한 내용과 일치하는지 검증할 수 있습니다.

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

`Bus` 파사드의 `assertBatched` 메서드는 [작업 배치](/docs/13.x/queues#job-batching)가 디스패치되었는지 검증하는 데 사용할 수 있습니다. `assertBatched` 메서드에 전달하는 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 받으며, 이 인스턴스를 사용하여 배치 안의 작업을 검사할 수 있습니다.

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

주어진 개수의 배치가 디스패치되었는지 검증하려면 `assertBatchCount` 메서드를 사용할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

배치가 전혀 디스패치되지 않았는지 검증하려면 `assertNothingBatched`를 사용할 수 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 작업과 배치 상호작용 테스트

또한 개별 작업이 기반 배치와 어떻게 상호작용하는지 테스트해야 할 때도 있습니다. 예를 들어, 어떤 작업이 해당 배치의 이후 처리를 취소했는지 테스트해야 할 수 있습니다. 이를 위해서는 `withFakeBatch` 메서드를 통해 작업에 가짜 배치를 할당해야 합니다. `withFakeBatch` 메서드는 작업 인스턴스와 가짜 배치를 포함하는 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업과 큐 상호작용 테스트

때로는 큐에 들어간 작업이 [자기 자신을 다시 큐로 릴리스](#manually-releasing-a-job)하는지 테스트해야 할 수 있습니다. 또는 작업이 자기 자신을 삭제했는지 테스트해야 할 수도 있습니다. 이러한 큐 상호작용은 작업을 인스턴스화하고 `withFakeQueueInteractions` 메서드를 호출하여 테스트할 수 있습니다.

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
## 작업 이벤트 (Job Events)

`Queue` [파사드](/docs/13.x/facades)의 `before` 및 `after` 메서드를 사용하면 큐 작업이 처리되기 전이나 후에 실행할 콜백을 지정할 수 있습니다. 이러한 콜백은 추가 로깅을 수행하거나 대시보드 통계를 증가시키기에 좋은 지점입니다. 일반적으로 이 메서드들은 [서비스 프로바이더](/docs/13.x/providers)의 `boot` 메서드에서 호출해야 합니다. 예를 들어 Laravel에 포함된 `AppServiceProvider`를 사용할 수 있습니다.

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
`Queue` [파사드](/docs/13.x/facades)의 `looping` 메서드를 사용하면 워커가 큐에서 작업을 가져오려고 시도하기 전에 실행할 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 작업으로 인해 열린 상태로 남아 있는 트랜잭션을 롤백하도록 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```
