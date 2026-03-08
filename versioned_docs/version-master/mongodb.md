# MongoDB

- [소개](#introduction)
- [설치](#installation)
    - [MongoDB 드라이버](#mongodb-driver)
    - [MongoDB 서버 시작하기](#starting-a-mongodb-server)
    - [Laravel MongoDB 패키지 설치](#install-the-laravel-mongodb-package)
- [설정](#configuration)
- [기능](#features)

<a name="introduction"></a>
## 소개 (Introduction)

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb)는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로, 높은 쓰기 부하(분석이나 IoT에 유용)와 높은 가용성(자동 장애 조치를 지원하는 복제 세트 설정 용이성) 때문에 많이 사용됩니다. 또한, 수평 확장을 위해 데이터베이스 샤딩을 쉽게 할 수 있으며, 집계, 텍스트 검색 또는 지리 공간 쿼리를 수행할 수 있는 강력한 쿼리 언어를 제공합니다.

SQL 데이터베이스처럼 행과 열로 된 테이블에 데이터를 저장하는 대신, MongoDB의 각 레코드는 BSON(Binary JSON)이라는 데이터 바이너리 표현 방식으로 설명된 문서입니다. 애플리케이션은 이 정보를 JSON 형식으로 조회할 수 있습니다. 문서, 배열, 중첩 문서, 바이너리 데이터 등 다양한 데이터 타입을 지원합니다.

Laravel에서 MongoDB를 사용하기 전에, Composer를 통해 `mongodb/laravel-mongodb` 패키지를 설치하고 사용하는 것을 권장합니다. MongoDB 드라이버는 PHP에서 기본적으로 지원하지만, `laravel-mongodb` 패키지는 Eloquent와 Laravel의 다른 기능과 더 풍부하게 통합되어 공식적으로 MongoDB에서 유지 관리합니다.

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## 설치 (Installation)

<a name="mongodb-driver"></a>
### MongoDB 드라이버 (MongoDB Driver)

MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장 모듈이 필요합니다. [Laravel Herd](https://herd.laravel.com)를 사용해 로컬에서 개발하거나 `php.new`로 PHP를 설치했다면, 이미 시스템에 이 확장이 설치되어 있습니다. 수동으로 설치해야 하는 경우, PECL을 사용하여 설치할 수 있습니다:

```shell
pecl install mongodb
```

MongoDB PHP 확장 설치에 관한 자세한 내용은 [MongoDB PHP extension installation instructions](https://www.php.net/manual/en/mongodb.installation.php)를 참고하세요.

<a name="starting-a-mongodb-server"></a>
### MongoDB 서버 시작하기 (Starting a MongoDB Server)

MongoDB Community Server는 로컬에서 MongoDB를 실행할 때 사용할 수 있으며, Windows, macOS, Linux 또는 Docker 컨테이너로 설치 가능합니다. MongoDB 설치 방법에 대해서는 [공식 MongoDB Community 설치 가이드](https://docs.mongodb.com/manual/administration/install-community/)를 참고하세요.

MongoDB 서버의 연결 문자열은 `.env` 파일에 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

클라우드에서 MongoDB를 호스팅하려면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)를 사용하는 것을 고려해 보십시오. 애플리케이션에서 로컬 환경에서 MongoDB Atlas 클러스터에 접근하려면, 프로젝트의 IP 접근 목록에 [본인 IP 주소를 추가](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다.

MongoDB Atlas 연결 문자열도 `.env` 파일에 다음과 같이 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Laravel MongoDB 패키지 설치 (Install the Laravel MongoDB Package)

마지막으로, Composer를 사용해 Laravel MongoDB 패키지를 설치합니다:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]
> `mongodb` PHP 확장 모듈이 설치되어 있지 않으면 이 패키지 설치는 실패합니다. CLI와 웹 서버의 PHP 설정이 다를 수 있으니, 두 환경 모두에서 확장 모듈이 활성화되어 있는지 확인하십시오.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 `config/database.php` 설정 파일에서 MongoDB 연결을 구성할 수 있습니다. 이 파일 내의 `connections` 배열에 `mongodb` 드라이버를 사용하는 연결을 추가하세요:

```php
'connections' => [
    'mongodb' => [
        'driver' => 'mongodb',
        'dsn' => env('MONGODB_URI', 'mongodb://localhost:27017'),
        'database' => env('MONGODB_DATABASE', 'laravel_app'),
    ],
],
```

<a name="features"></a>
## 기능 (Features)

설정이 완료되면, `mongodb` 패키지와 데이터베이스 연결을 통해 다양한 강력한 기능을 애플리케이션에서 활용할 수 있습니다:

- [Eloquent 사용](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/): 모델을 MongoDB 컬렉션에 저장할 수 있습니다. 표준 Eloquent 기능 외에도, Laravel MongoDB 패키지는 임베디드 연관관계(embedded relationships) 같은 추가 기능을 제공합니다. 또한 이 패키지는 MongoDB 드라이버에 직접 접근할 수 있어 원시 쿼리(raw queries)나 집계 파이프라인(aggregation pipelines) 같은 작업도 수행할 수 있습니다.
- [복잡한 쿼리 작성](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/)을 위한 쿼리 빌더 제공.
- `mongodb` [캐시 드라이버](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)는 TTL 인덱스 같은 MongoDB 기능을 최적화하여 만료된 캐시 항목을 자동으로 삭제합니다.
- `mongodb` 큐 드라이버를 사용한 [큐 작업 디스패치 및 처리](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/).
- [GridFS에 파일 저장](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/)을 위한 [Flysystem용 GridFS 어댑터](https://flysystem.thephpleague.com/docs/adapter/gridfs/) 지원.
- 대부분의 데이터베이스 연결이나 Eloquent를 사용하는 서드파티 패키지는 MongoDB와 함께 사용할 수 있습니다.

MongoDB와 Laravel 사용법에 대해 더 배우려면 MongoDB의 [빠른 시작 가이드](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/)를 참고하세요.