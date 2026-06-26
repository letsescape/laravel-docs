<!-- # MongoDB -->
# MongoDB

- [Introduction](#introduction)
- [Installation](#installation)
    - [MongoDB Driver](#mongodb-driver)
    - [Starting a MongoDB Server](#starting-a-mongodb-server)
    - [Install the Laravel MongoDB Package](#install-the-laravel-mongodb-package)
- [Configuration](#configuration)
- [Features](#features)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb) is one of the most popular NoSQL document-oriented database, used for its high write load (useful for analytics or IoT) and high availability (easy to set replica sets with automatic failover). It can also shard the database easily for horizontal scalability and has a powerful query language for doing aggregation, text search or geospatial queries. -->
[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb)는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로, 높은 쓰기 부하(분석 또는 IoT에 유용)와 높은 가용성(자동 장애 조치 기능을 갖춘 복제 세트 구성이 용이한 점) 때문에 많이 사용됩니다. 또한 데이터베이스를 수평 확장하기 위한 샤딩(sharding)을 쉽게 할 수 있고, 집계, 텍스트 검색, 지리 공간 쿼리 등을 위한 강력한 쿼리 언어를 제공합니다.

<!-- Instead of storing data in tables of rows or columns like SQL databases, each record in a MongoDB database is a document described in BSON, a binary representation of the data. Applications can then retrieve this information in a JSON format. It supports a wide variety of data types, including documents, arrays, embedded documents, and binary data. -->
SQL 데이터베이스처럼 행과 열로 이루어진 테이블에 데이터를 저장하는 대신, MongoDB 데이터베이스의 각 레코드는 BSON이라는 이진 표현 방식으로 설명되는 문서(document)입니다. 애플리케이션은 이 정보를 JSON 형식으로 읽어올 수 있습니다. MongoDB는 문서, 배열, 내장 문서, 이진 데이터 등 다양한 데이터 타입을 지원합니다.

<!-- Before using MongoDB with Laravel, we recommend installing and using the `mongodb/laravel-mongodb` package via Composer. The `laravel-mongodb` package is officially maintained by MongoDB, and while MongoDB is natively supported by PHP through the MongoDB driver, the [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) package provides a richer integration with Eloquent and other Laravel features: -->
Laravel과 함께 MongoDB를 사용하기 전에, `mongodb/laravel-mongodb` 패키지를 Composer를 통해 설치하고 사용하는 것을 권장합니다. `laravel-mongodb` 패키지는 MongoDB에서 공식적으로 관리하며, PHP가 MongoDB 드라이버를 통해 네이티브로 MongoDB를 지원하지만, [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 패키지는 Eloquent 및 Laravel의 다른 기능들과 더 풍부하게 통합할 수 있게 해줍니다:

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<a name="mongodb-driver"></a>
<!-- ### MongoDB Driver -->
### MongoDB Driver

<!-- To connect to a MongoDB database, the `mongodb` PHP extension is required. If you are developing locally using [Laravel Herd](https://herd.laravel.com) or installed PHP via `php.new`, you already have this extension installed on your system. However, if you need to install the extension manually, you may do so via PECL: -->
MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장(extension)이 필요합니다. 로컬 개발 환경에서 [Laravel Herd](https://herd.laravel.com)를 사용하거나 `php.new`로 PHP를 설치한 경우, 이미 이 확장이 시스템에 설치되어 있습니다. 하지만 수동으로 확장을 설치해야 한다면, PECL을 통해 설치할 수 있습니다:

```shell
pecl install mongodb
```

<!-- For more information on installing the MongoDB PHP extension, check out the [MongoDB PHP extension installation instructions](https://www.php.net/manual/en/mongodb.installation.php). -->
MongoDB PHP 확장 설치에 관한 자세한 내용은 [MongoDB PHP extension installation instructions](https://www.php.net/manual/en/mongodb.installation.php)를 참고하세요.

<a name="starting-a-mongodb-server"></a>
<!-- ### Starting a MongoDB Server -->
### Starting a MongoDB Server

<!-- The MongoDB Community Server can be used to run MongoDB locally and is available for installation on Windows, macOS, Linux, or as a Docker container. To learn how to install MongoDB, please refer to the [official MongoDB Community installation guide](https://docs.mongodb.com/manual/administration/install-community/). -->
MongoDB Community Server는 로컬에서 MongoDB를 실행할 때 사용할 수 있으며, Windows, macOS, Linux 또는 Docker 컨테이너로 설치 가능합니다. MongoDB 설치 방법은 [official MongoDB Community installation guide](https://docs.mongodb.com/manual/administration/install-community/)를 참고하세요.

<!-- The connection string for the MongoDB server can be set in your `.env` file: -->
MongoDB 서버의 연결 문자열(connection string)은 `.env` 파일에 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

<!--
For hosting MongoDB in the cloud, consider using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
To access a MongoDB Atlas cluster locally from your application, you will need to [add your own IP address in the cluster's network settings](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) to the project's IP Access List.
-->
클라우드 환경에서 MongoDB를 호스팅하려면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)를 고려할 수 있습니다. 애플리케이션에서 로컬로 MongoDB Atlas 클러스터에 접속하려면, [add your own IP address in the cluster's network settings](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다.

<!-- The connection string for MongoDB Atlas can also be set in your `.env` file: -->
MongoDB Atlas 연결 문자열도 `.env` 파일에 다음과 같이 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
<!-- ### Install the Laravel MongoDB Package -->
### Install the Laravel MongoDB Package

<!-- Finally, use Composer to install the Laravel MongoDB package: -->
마지막으로, Composer를 사용해 Laravel MongoDB 패키지를 설치하세요:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]
> `mongodb` PHP 확장이 설치되어 있지 않으면 이 패키지 설치가 실패합니다. PHP 설정은 CLI와 웹 서버에서 다를 수 있으므로, 두 환경 모두에서 확장이 활성화되어 있는지 반드시 확인하세요.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- You may configure your MongoDB connection via your application's `config/database.php` configuration file. Within this file, add a `mongodb` connection that utilizes the `mongodb` driver: -->
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
<!-- ## Features -->
## Features

<!-- Once your configuration is complete, you can use the `mongodb` package and database connection in your application to leverage a variety of powerful features: -->
설정을 완료하면, 애플리케이션 내에서 `mongodb` 패키지와 데이터베이스 연결을 사용하여 다음과 같은 강력한 기능들을 활용할 수 있습니다:

<!--
- [Using Eloquent](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/), models can be stored in MongoDB collections. In addition to the standard Eloquent features, the Laravel MongoDB package provides additional features such as embedded relationships. The package also provides direct access to the MongoDB driver, which can be used to execute operations such as raw queries and aggregation pipelines.
- [Write complex queries](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) using the query builder.
- [Similarity / vector search](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/fundamentals/vector-search/) using vector embeddings and the `vectorSearch` Eloquent method.
- The `mongodb` [cache driver](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) is optimized to use MongoDB features such as TTL indexes to automatically clear expired cache entries.
- [Dispatch and process queued jobs](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) with the `mongodb` queue driver.
- [Storing files in GridFS](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/), via the [GridFS Adapter for Flysystem](https://flysystem.thephpleague.com/docs/adapter/gridfs/).
- [Full-text search](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/scout/) using the `mongodb` Scout engine.
- Most third party packages using a database connection or Eloquent can be used with MongoDB.
-->
- [Using Eloquent](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/), Eloquent 모델을 MongoDB 컬렉션에 저장할 수 있습니다. 일반적인 Eloquent 기능 외에도, Laravel MongoDB 패키지는 embedded relationships 같은 추가 기능을 제공합니다. 또한 MongoDB 드라이버에 직접 접근할 수 있어 raw queries나 aggregation pipelines 같은 작업을 수행할 수 있습니다.
- [Write complex queries](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) 쿼리 빌더를 사용해 복잡한 쿼리를 작성할 수 있습니다.
- [Similarity / vector search](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/fundamentals/vector-search/) 벡터 임베딩과 `vectorSearch` Eloquent 메서드를 사용한 유사도 / 벡터 검색입니다.
- `mongodb` [cache driver](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)는 TTL 인덱스 같은 MongoDB 기능을 활용해 만료된 캐시 항목을 자동으로 지우도록 최적화되어 있습니다.
- [Dispatch and process queued jobs](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/)를 `mongodb` queue driver로 디스패치하고 처리할 수 있습니다.
- [Storing files in GridFS](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/)를 [GridFS Adapter for Flysystem](https://flysystem.thephpleague.com/docs/adapter/gridfs/)을 통해 수행할 수 있습니다.
- [Full-text search](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/scout/)를 `mongodb` Scout engine으로 사용할 수 있습니다.
- 데이터베이스 연결이나 Eloquent를 사용하는 대부분의 서드파티 패키지도 MongoDB와 함께 사용할 수 있습니다.

<!-- To continue learning how to use MongoDB and Laravel, refer to MongoDB's [Quick Start guide](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/). -->
MongoDB와 Laravel을 활용하는 방법을 더 배우려면 MongoDB의 [Quick Start guide](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/)를 참고하세요.
