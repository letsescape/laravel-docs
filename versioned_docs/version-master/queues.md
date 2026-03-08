# 큐 (Queues)

- [소개](#introduction)
    - [Connections vs. Queues](#connections-vs-queues)
    - [드라이버 참고 사항 및 사전 요구 사항](#driver-prerequisites)
- [Job 생성](#creating-jobs)
    - [Job 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 Job (Unique Jobs)](#unique-jobs)
    - [암호화된 Job](#encrypted-jobs)
- [Job 미들웨어](#job-middleware)
    - [속도 제한 (Rate Limiting)](#rate-limiting)
    - [Job 중복 실행 방지](#preventing-job-overlaps)
    - [예외 발생 제한 (Throttling Exceptions)](#throttling-exceptions)
    - [Job 건너뛰기](#skipping-jobs)
- [Job 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [Job과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [Job 체이닝](#job-chaining)
    - [큐 및 연결 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 Failover](#queue-failover)
    - [에러 처리](#error-handling)
- [Job 배치 처리](#job-batching)
    - [배치 가능한 Job 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 Job 추가](#adding-jobs-to-batches)
    - [배치 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [Closure 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [Job 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시 중지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 Job 처리](#dealing-with-failed-jobs)
    - [실패한 Job 이후 정리](#cleaning-up-after-failed-jobs)
    - [실패한 Job 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 Job 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 Job 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 Job 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 Job 이벤트](#failed-job-events)
- [큐에서 Job 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 Job만 Fake 처리](#faking-a-subset-of-jobs)
    - [Job 체인 테스트](#testing-job-chains)
    - [Job 배치 테스트](#testing-job-batches)
    - [Job / Queue 상호작용 테스트](#testing-job-queue-interactions)
- [Job 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼, 일반적인 웹 요청 처리 시간 안에 수행하기에는 오래 걸리는 작업이 있을 수 있습니다. 다행히도 Laravel은 이러한 작업을 백그라운드에서 처리할 수 있는 **큐 기반 Job**을 쉽게 만들 수 있도록 지원합니다. 시간이 오래 걸리는 작업을 큐로 옮기면 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있고, 사용자 경험도 크게 향상됩니다.

Laravel 큐는 다양한 큐 백엔드에 대해 **통합된 큐 API**를 제공합니다. 예를 들어 다음과 같은 큐 시스템을 사용할 수 있습니다.

- [Amazon SQS](https://aws.amazon.com/sqs/)
- [Redis](https://redis.io)
- 관계형 데이터베이스

Laravel의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 Laravel에서 기본적으로 제공하는 여러 큐 드라이버에 대한 연결 설정이 포함되어 있습니다.

- database
- [Amazon SQS](https://aws.amazon.com/sqs/)
- [Redis](https://redis.io)
- [Beanstalkd](https://beanstalkd.github.io/)

또한 개발이나 테스트 환경에서 사용할 수 있도록 **Job을 즉시 실행하는 동기(sync) 드라이버**도 제공됩니다. 큐에 전달된 Job을 버리는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 강력한 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/master/horizon)를 참고하십시오.

<a name="connections-vs-queues"></a>
### Connections vs. Queues

Laravel 큐를 사용하기 전에 **connection(연결)**과 **queue(큐)**의 차이를 이해하는 것이 중요합니다.

`config/queue.php` 설정 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 같은 **큐 백엔드 서비스와의 연결**을 정의합니다.

하지만 하나의 큐 연결(connection) 안에는 여러 개의 **queue(큐)**가 존재할 수 있습니다. 큐는 쉽게 말해 **Job이 쌓이는 서로 다른 작업 스택**이라고 생각하면 됩니다.

`queue` 설정 파일에서 각 connection 설정에는 `queue` 속성이 있습니다. 이것은 해당 connection으로 Job을 디스패치할 때 기본적으로 사용되는 큐입니다.

즉, 어떤 큐로 보낼지 명시하지 않으면 해당 connection의 기본 큐로 Job이 전달됩니다.

```php
use App\Jobs\ProcessPodcast;

// 기본 connection의 기본 queue로 전송...
ProcessPodcast::dispatch();

// 기본 connection의 "emails" queue로 전송...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 하나의 큐만 사용해도 충분할 수 있습니다. 하지만 여러 큐를 사용하는 것은 매우 유용합니다. 특히 다음과 같은 경우에 도움이 됩니다.

- 작업 우선순위를 구분할 때
- 작업 유형을 분리할 때

Laravel의 큐 워커는 **처리할 큐의 우선순위**를 지정할 수 있기 때문입니다. 예를 들어 `high` 큐의 작업을 더 먼저 처리하도록 설정할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

이 경우 워커는 `high` 큐의 작업을 먼저 처리한 다음 `default` 큐 작업을 처리합니다.

<a name="driver-prerequisites"></a>
### 드라이버 참고 사항 및 사전 요구 사항 (Driver Notes and Prerequisites)

<a name="database"></a>
#### Database

`database` 큐 드라이버를 사용하려면 **Job을 저장할 데이터베이스 테이블**이 필요합니다.

일반적으로 Laravel 기본 마이그레이션에는 다음 파일이 포함되어 있습니다.

```
0001_01_01_000002_create_jobs_table.php
```

만약 이 마이그레이션이 없다면 `make:queue-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에서 Redis 연결을 설정해야 합니다.

> [!WARNING]
> Redis 옵션 중 `serializer`와 `compression`은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis Cluster

Redis 연결이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, **큐 이름에 key hash tag**가 포함되어야 합니다.

이렇게 해야 해당 큐와 관련된 모든 Redis 키가 동일한 hash slot에 저장됩니다.

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
##### Blocking

Redis 큐를 사용할 때 `block_for` 옵션을 사용하면 **Job이 도착할 때까지 대기할 시간**을 지정할 수 있습니다.

이 옵션은 Redis를 계속 polling 하는 것보다 효율적일 수 있습니다.

예를 들어 다음 설정은 **Job이 들어올 때까지 최대 5초 동안 대기**합니다.

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
> `block_for`를 `0`으로 설정하면 Job이 올 때까지 **무기한 대기**합니다. 이 경우 `SIGTERM` 같은 시스템 신호도 다음 Job이 처리될 때까지 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 요구 사항

다음 큐 드라이버를 사용하려면 해당 Composer 패키지를 설치해야 합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>