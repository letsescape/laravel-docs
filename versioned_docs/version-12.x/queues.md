# 큐 (Queues)

- [소개](#introduction)
    - [Connections vs. Queues](#connections-vs-queues)
    - [Driver Notes and Prerequisites](#driver-prerequisites)
- [Job 생성](#creating-jobs)
    - [Job 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [Unique Jobs](#unique-jobs)
    - [암호화된 Job](#encrypted-jobs)
- [Job Middleware](#job-middleware)
    - [Rate Limiting](#rate-limiting)
    - [Job 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [Job 건너뛰기](#skipping-jobs)
- [Job 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [Jobs & Database Transactions](#jobs-and-database-transactions)
    - [Job 체이닝](#job-chaining)
    - [Queue와 Connection 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 설정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 Fair Queues](#sqs-fifo-and-fair-queues)
    - [Queue Failover](#queue-failover)
    - [에러 처리](#error-handling)
- [Job Batching](#job-batching)
    - [Batchable Job 정의](#defining-batchable-jobs)
    - [Batch 디스패치](#dispatching-batches)
    - [Chains와 Batches](#chains-and-batches)
    - [Batch에 Job 추가](#adding-jobs-to-batches)
    - [Batch 정보 확인](#inspecting-batches)
    - [Batch 취소](#cancelling-batches)
    - [Batch 실패 처리](#batch-failures)
    - [Batch 정리](#pruning-batches)
    - [DynamoDB에 Batch 저장](#storing-batches-in-dynamodb)
- [Closure 큐잉](#queueing-closures)
- [Queue Worker 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [Queue 우선순위](#queue-priorities)
    - [Queue Worker와 배포](#queue-workers-and-deployment)
    - [Job 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [Queue Worker 일시 정지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 Job 처리](#dealing-with-failed-jobs)
    - [실패한 Job 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 Job 재시도](#retrying-failed-jobs)
    - [없는 모델 무시](#ignoring-missing-models)
    - [실패한 Job 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패 Job 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 Job 저장 비활성화](#disabling-failed-job-storage)
    - [실패 Job 이벤트](#failed-job-events)
- [Queue에서 Job 삭제](#clearing-jobs-from-queues)
- [Queue 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 Job만 Fake 처리](#faking-a-subset-of-jobs)
    - [Job 체인 테스트](#testing-job-chains)
    - [Job Batch 테스트](#testing-job-batches)
    - [Job / Queue 상호작용 테스트](#testing-job-queue-interactions)
- [Job 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼 **일반적인 웹 요청 안에서 처리하기에는 시간이 오래 걸리는 작업**이 존재합니다.  

Laravel은 이러한 작업을 **큐(Queue)에 넣어 백그라운드에서 처리**할 수 있는 기능을 제공합니다. 시간이 오래 걸리는 작업을 큐로 이동시키면 애플리케이션은 훨씬 빠르게 웹 요청에 응답할 수 있고, 사용자에게 더 좋은 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드를 **하나의 통합된 API**로 사용할 수 있게 해줍니다.

Laravel의 큐 설정은 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 프레임워크에서 제공하는 다양한 큐 드라이버에 대한 연결 설정이 포함되어 있습니다.

대표적으로 다음 드라이버가 포함됩니다.

- database
- [Amazon SQS](https://aws.amazon.com/sqs/)
- [Redis](https://redis.io)
- [Beanstalkd](https://beanstalkd.github.io/)
- synchronous driver (개발 및 테스트용 즉시 실행)
- `null` driver (큐 작업을 버림)

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon documentation](/docs/12.x/horizon)을 참고하십시오.

---

<a name="connections-vs-queues"></a>
### Connections vs. Queues

Laravel 큐를 시작하기 전에 **"connection"과 "queue"의 차이**를 이해하는 것이 중요합니다.

`config/queue.php` 파일에는 `connections` 설정 배열이 있습니다. 이 설정은 Amazon SQS, Beanstalkd, Redis 같은 **백엔드 큐 서비스와의 연결(connection)** 을 정의합니다.

하지만 **하나의 connection 안에는 여러 개의 queue가 존재할 수 있습니다.**  
queue는 말 그대로 **작업(Job)이 쌓이는 서로 다른 스택 또는 작업 목록**이라고 생각할 수 있습니다.

`queue` 설정 파일을 보면 각 connection 설정에 `queue` 속성이 포함되어 있습니다. 이 값은 해당 connection으로 Job을 디스패치할 때 **기본적으로 사용되는 queue 이름**입니다.

즉, 특정 queue를 지정하지 않고 Job을 디스패치하면 해당 connection의 기본 queue로 들어갑니다.

```php
use App\Jobs\ProcessPodcast;

// 기본 connection의 기본 queue로 전송...
ProcessPodcast::dispatch();

// 기본 connection의 "emails" queue로 전송...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 하나의 단순한 큐만 사용해도 충분할 수 있습니다. 하지만 여러 큐를 사용하면 **작업의 우선순위나 유형별 분리**가 가능해집니다.

예를 들어 `high` 큐에 중요한 작업을 넣고, worker가 해당 큐를 먼저 처리하도록 할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

위 명령은 다음 순서로 작업을 처리합니다.

1. `high` 큐 작업
2. `default` 큐 작업

---

<a name="driver-prerequisites"></a>
### 드라이버 참고 사항 및 사전 요구사항 (Driver Notes and Prerequisites)

<a name="database"></a>
#### Database

`database` 큐 드라이버를 사용하려면 **job을 저장할 데이터베이스 테이블**이 필요합니다.

일반적으로 Laravel 기본 프로젝트에는 다음 migration이 이미 포함되어 있습니다.

`0001_01_01_000002_create_jobs_table.php`

만약 없다면 다음 Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

---

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에서 **Redis 연결을 설정**해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

---

<a name="redis-cluster"></a>
##### Redis Cluster

Redis 연결이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우 **queue 이름에 key hash tag가 포함되어야 합니다.**

이는 동일한 queue의 Redis 키가 **같은 hash slot에 배치되도록 하기 위해 필요합니다.**

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

---

<a name="blocking"></a>
##### Blocking

Redis 큐를 사용할 때 `block_for` 옵션을 사용하면 **새로운 Job이 도착할 때까지 대기할 시간**을 지정할 수 있습니다.

worker가 계속 Redis를 폴링하는 대신 일정 시간 동안 대기하도록 하면 더 효율적일 수 있습니다.

예를 들어 다음 설정은 **최대 5초 동안 Job을 기다립니다.**

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
> `block_for` 값을 `0`으로 설정하면 Job이 생길 때까지 **무한 대기**합니다. 이 경우 `SIGTERM` 같은 종료 신호가 다음 Job이 실행되기 전까지 처리되지 않을 수 있습니다.

---

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 요구사항

다음 큐 드라이버를 사용하려면 해당 Composer 패키지가 필요합니다.

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP extension
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`