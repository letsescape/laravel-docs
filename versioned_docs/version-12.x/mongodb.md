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

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb)는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로, 높은 쓰기 부하(분석 또는 IoT에 유용)와 높은 가용성(자동 장애 조치 기능을 갖춘 복제 세트 구성이 용이한 점) 때문에 많이 사용됩니다. 또한 데이터베이스를 수평 확장하기 위한 샤딩(sharding)을 쉽게 할 수 있고, 집계, 텍스트 검색, 지리 공간 쿼리 등을 위한 강력한 쿼리 언어를 제공합니다.

SQL 데이터베이스처럼 행과 열로 이루어진 테이블에 데이터를 저장하는 대신, MongoDB 데이터베이스의 각 레코드는 BSON이라는 이진 표현 방식으로 설명되는 문서(document)입니다. 애플리케이션은 이 정보를 JSON 형식으로 읽어올 수 있습니다. MongoDB는 문서, 배열, 내장 문서, 이진 데이터 등 다양한 데이터 타입을 지원합니다.

Laravel과 함께 MongoDB를 사용하기 전에, `mongodb/laravel-mongodb` 패키지를 Composer를 통해 설치하고 사용하는 것을 권장합니다. `laravel-mongodb` 패키지는 MongoDB에서 공식적으로 관리하며, PHP가 MongoDB 드라이버를 통해 네이티브로 MongoDB를 지원하지만, [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 패키지는 Eloquent 및 Laravel의 다른 기능들과 더 풍부하게 통합할 수 있게 해줍니다:

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## 설치 (Installation)

<a name="mongodb-driver"></a>
### MongoDB 드라이버 (MongoDB Driver)

MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장(extension)이 필요합니다. 로컬 개발 환경에서 [Laravel Herd](https://herd.laravel.com)를 사용하거나 `php.new`로 PHP를 설치한 경우, 이미 이 확장이 시스템에 설치되어 있습니다. 하지만 수동으로 확장을 설치해야 한다면, PECL을 통해 설치할 수 있습니다:

```shell
pecl install mongodb
```

MongoDB PHP 확장 설치에 관한 자세한 내용은 [MongoDB PHP 확장 설치 가이드](https://www.php.net/manual/en/mongodb.installation.php)를 참고하세요.

<a name="starting-a-mongodb-server"></a>
### MongoDB 서버 시작하기 (Starting a MongoDB Server)

MongoDB Community Server는 로컬에서 MongoDB를 실행할 때 사용할 수 있으며, Windows, macOS, Linux 또는 Docker 컨테이너로 설치 가능합니다. MongoDB 설치 방법은 [공식 MongoDB Community 설치 가이드](https://docs.mongodb.com/manual/administration/install-community/)를 참고하세요.

MongoDB 서버의 연결 문자열(connection string)은 `.env` 파일에 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

클라우드 환경에서 MongoDB를 호스팅하려면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)를 고려할 수 있습니다. 애플리케이션에서 로컬로 MongoDB Atlas 클러스터에 접속하려면, [클러스터의 네트워크 설정에 본인의 IP 주소를 추가](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다.

MongoDB Atlas 연결 문자열도 `.env` 파일에 다음과 같이 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Laravel MongoDB 패키지 설치 (Install the Laravel MongoDB Package)

마지막으로, Composer를 사용해 Laravel MongoDB 패키지를 설치하세요:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]
> `mongodb` PHP 확장이 설치되어 있지 않으면 이 패키지 설치가 실패합니다. PHP 설정은 CLI와 웹 서버에서 다를 수 있으므로, 두 환경 모두에서 확장이 활성화되어 있는지 반드시 확인하세요.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 `config/database.php` 설정 파일에서 MongoDB 연결을 구성할 수 있습니다. 이 파일 내에서 `mongodb` 드라이버를 사용하는 `mongodb` 연결을 추가하세요:

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

설정을 완료하면, 애플리케이션 내에서 `mongodb` 패키지와 데이터베이스 연결을 사용하여 다음과 같은 강력한 기능들을 활용할 수 있습니다:

- [Eloquent 사용하기](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/) : Eloquent 모델을 MongoDB 컬렉션에 저장할 수 있습니다. 일반적인 Eloquent 기능 외에도, Laravel MongoDB 패키지는 내장된 관계(embedded relationships) 같은 추가 기능을 제공합니다. 또한 MongoDB 드라이버에 직접 접근할 수 있어 원시 쿼리(Raw Query)나 집계 파이프라인 같은 작업을 수행할 수 있습니다.
- [복잡한 쿼리 작성하기](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) : 쿼리 빌더를 사용해 복잡한 쿼리를 작성할 수 있습니다.
- `mongodb` [캐시 드라이버](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) : MongoDB의 TTL 인덱스 같은 기능을 활용하여 만료된 캐시 항목을 자동으로 삭제하도록 최적화되어 있습니다.
- [큐 작업 등록 및 처리](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) : `mongodb` 큐 드라이버를 이용해 작업을 대기열에 등록하고 처리할 수 있습니다.
- [GridFS에 파일 저장하기](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/) : [Flysystem의 GridFS 어댑터](https://flysystem.thephpleague.com/docs/adapter/gridfs/)를 통해 파일 저장소로 활용할 수 있습니다.
- 대부분의 데이터베이스 연결이나 Eloquent를 사용하는 서드파티 패키지도 MongoDB와 함께 사용할 수 있습니다.

MongoDB와 Laravel을 활용하는 방법을 더 배우려면 MongoDB의 [빠른 시작 가이드](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/)를 참고하세요.