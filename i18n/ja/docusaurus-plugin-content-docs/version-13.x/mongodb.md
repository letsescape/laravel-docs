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
[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb) は、最も人気のある NoSQL ドキュメント指向データベースの 1 つで、高い書き込み負荷 (分析や IoT に便利) と高可用性 (自動フェイルオーバーを備えたレプリカ セットの設定が簡単) のために使用されます。また、データベースを簡単にシャーディングして水平方向のスケーラビリティを実現し、集計、テキスト検索、地理空間クエリを実行するための強力なクエリ言語を備えています。

<!-- Instead of storing data in tables of rows or columns like SQL databases, each record in a MongoDB database is a document described in BSON, a binary representation of the data. Applications can then retrieve this information in a JSON format. It supports a wide variety of data types, including documents, arrays, embedded documents, and binary data. -->
SQL データベースのように行または列のテーブルにデータを保存するのではなく、MongoDB データベースの各レコードは、データのバイナリ表現である BSON で記述されたドキュメントです。アプリケーションはこの情報を JSON 形式で取得できます。ドキュメント、配列、埋め込みドキュメント、バイナリ データなど、さまざまなデータ型をサポートします。

<!-- Before using MongoDB with Laravel, we recommend installing and using the `mongodb/laravel-mongodb` package via Composer. The `laravel-mongodb` package is officially maintained by MongoDB, and while MongoDB is natively supported by PHP through the MongoDB driver, the [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) package provides a richer integration with Eloquent and other Laravel features: -->
Laravel で MongoDB を使用する前に、Composer 経由で `mongodb/laravel-mongodb` パッケージをインストールして使用することをお勧めします。 `laravel-mongodb` パッケージは MongoDB によって公式に保守されており、MongoDB は MongoDB ドライバを通じて PHP によってネイティブにサポートされていますが、[Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) パッケージは Eloquent および他の Laravel 機能とのより充実した統合を提供します。

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
MongoDB データベースに接続するには、`mongodb` PHP 拡張機能が必要です。 [Laravel Herd](https://herd.laravel.com) を使用してローカルで開発している場合、または `php.new` 経由で PHP をインストールしている場合は、この拡張機能はすでにシステムにインストールされています。ただし、拡張機能を手動でインストールする必要がある場合は、PECL 経由でインストールできます。

```shell
pecl install mongodb
```

<!-- For more information on installing the MongoDB PHP extension, check out the [MongoDB PHP extension installation instructions](https://www.php.net/manual/en/mongodb.installation.php). -->
MongoDB PHP 拡張機能のインストールの詳細については、[MongoDB PHP extension installation instructions](https://www.php.net/manual/en/mongodb.installation.php) を確認してください。

<a name="starting-a-mongodb-server"></a>
<!-- ### Starting a MongoDB Server -->
### Starting a MongoDB Server

<!-- The MongoDB Community Server can be used to run MongoDB locally and is available for installation on Windows, macOS, Linux, or as a Docker container. To learn how to install MongoDB, please refer to the [official MongoDB Community installation guide](https://docs.mongodb.com/manual/administration/install-community/). -->
MongoDB Community Server は、MongoDB をローカルで実行するために使用でき、Windows、macOS、Linux にインストールするか、Docker コンテナーとして使用できます。 MongoDB のインストール方法については、[official MongoDB Community installation guide](https://docs.mongodb.com/manual/administration/install-community/) を参照してください。

<!-- The connection string for the MongoDB server can be set in your `.env` file: -->
MongoDB サーバーの接続文字列は、`.env` ファイルで設定できます。

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

<!--
For hosting MongoDB in the cloud, consider using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
To access a MongoDB Atlas cluster locally from your application, you will need to [add your own IP address in the cluster's network settings](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) to the project's IP Access List.
-->
クラウドで MongoDB をホストする場合は、[MongoDB Atlas](https://www.mongodb.com/cloud/atlas) の使用を検討してください。
アプリケーションからローカルで MongoDB Atlas クラスターにアクセスするには、プロジェクトの IP アクセス リストに [add your own IP address in the cluster's network settings](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) する必要があります。

<!-- The connection string for MongoDB Atlas can also be set in your `.env` file: -->
MongoDB Atlas の接続文字列は、`.env` ファイルで設定することもできます。

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
<!-- ### Install the Laravel MongoDB Package -->
### Install the Laravel MongoDB Package

<!-- Finally, use Composer to install the Laravel MongoDB package: -->
最後に、Composer を使用して Laravel MongoDB パッケージをインストールします。

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]
> `mongodb` PHP 拡張機能がインストールされていない場合、パッケージのこのインストールは失敗します。 PHP 設定は CLI と Web サーバー間で異なる場合があるため、両方の設定で拡張機能が有効になっていることを確認してください。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- You may configure your MongoDB connection via your application's `config/database.php` configuration file. Within this file, add a `mongodb` connection that utilizes the `mongodb` driver: -->
アプリケーションの `config/database.php` 構成ファイルを介して MongoDB 接続を構成できます。このファイル内に、`mongodb` ドライバを利用する `mongodb` 接続を追加します。

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
構成が完了したら、アプリケーションで `mongodb` パッケージとデータベース接続を使用して、さまざまな強力な機能を活用できます。

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
- [Using Eloquent](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/)、モデルは MongoDB コレクションに保存できます。標準の Eloquent 機能に加えて、Laravel MongoDB パッケージは埋め込みリレーションシップなどの追加機能を提供します。このパッケージは MongoDB ドライバへの直接アクセスも提供しており、raw クエリや aggregation pipelines などの操作を実行するために使用できます。

- クエリビルダを使用して [Write complex queries](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) を作成できます。

- [Similarity / vector search](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/fundamentals/vector-search/) は、vector embeddings と `vectorSearch` Eloquent メソッドを使用します。

- `mongodb` [cache driver](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) は、TTL インデックスなどの MongoDB 機能を活用して、期限切れのキャッシュエントリを自動的に削除するよう最適化されています。

- `mongodb` queue driver を使って、[Dispatch and process queued jobs](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) できます。

- [Storing files in GridFS](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/) は、[GridFS Adapter for Flysystem](https://flysystem.thephpleague.com/docs/adapter/gridfs/) を通じて行います。

- `mongodb` Scout engine を使って、[Full-text search](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/scout/) を利用できます。

- データベース接続または Eloquent を使用するほとんどのサードパーティパッケージは、MongoDB で使用できます。

<!-- To continue learning how to use MongoDB and Laravel, refer to MongoDB's [Quick Start guide](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/). -->
MongoDB と Laravel の使用方法を学習し続けるには、MongoDB の [Quick Start guide](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/) を参照してください。
