# モンゴDB (MongoDB)

- [Introduction](#introduction)
- [Installation](#installation)
    - [MongoDBドライバ](#mongodb-driver)
    - [MongoDB サーバーの起動](#starting-a-mongodb-server)
    - [Laravel MongoDB パッケージをインストールする](#install-the-laravel-mongodb-package)
- [Configuration](#configuration)
- [Features](#features)

<a name="introduction"></a>
## 導入 (Introduction)

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb) は、最も人気のある NoSQL ドキュメント指向データベースの 1 つで、高い書き込み負荷 (分析や IoT に便利) と高可用性 (自動フェイルオーバーを備えたレプリカ セットの設定が簡単) のために使用されます。また、データベースを簡単にシャーディングして水平方向のスケーラビリティを実現し、集計、テキスト検索、地理空間クエリを実行するための強力なクエリ言語を備えています。

SQL データベースのように行または列のテーブルにデータを保存するのではなく、MongoDB データベースの各レコードは、データのバイナリ表現である BSON で記述されたドキュメントです。アプリケーションはこの情報を JSON 形式で取得できます。ドキュメント、配列、埋め込みドキュメント、バイナリ データなど、さまざまなデータ型をサポートします。

Laravel で MongoDB を使用する前に、Composer 経由で `mongodb/laravel-mongodb` パッケージをインストールして使用することをお勧めします。 `laravel-mongodb` パッケージは MongoDB によって公式に保守されており、MongoDB は MongoDB ドライバを通じて PHP によってネイティブにサポートされていますが、[Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) パッケージは Eloquent および他の Laravel 機能とのより充実した統合を提供します。

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## インストール (Installation)

<a name="mongodb-driver"></a>
### MongoDBドライバ

MongoDB データベースに接続するには、`mongodb` PHP 拡張機能が必要です。 [LaravelのHerd](https://herd.laravel.com) を使用してローカルで開発している場合、または `php.new` 経由で PHP をインストールしている場合は、この拡張機能はすでにシステムにインストールされています。ただし、拡張機能を手動でインストールする必要がある場合は、PECL 経由でインストールできます。

```shell
pecl install mongodb
```

MongoDB PHP 拡張機能のインストールの詳細については、[MongoDB PHP 拡張機能のインストール手順](https://www.php.net/manual/en/mongodb.installation.php) を確認してください。

<a name="starting-a-mongodb-server"></a>
### MongoDB サーバーの起動

MongoDB Community Server は、MongoDB をローカルで実行するために使用でき、Windows、macOS、Linux にインストールするか、Docker コンテナーとして使用できます。 MongoDB のインストール方法については、[公式 MongoDB コミュニティ インストール ガイド](https://docs.mongodb.com/manual/administration/install-community/) を参照してください。

MongoDB サーバーの接続文字列は、`.env` ファイルで設定できます。

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

クラウドで MongoDB をホストする場合は、[MongoDB Atlas](https://www.mongodb.com/cloud/atlas) の使用を検討してください。
アプリケーションからローカルで MongoDB Atlas クラスターにアクセスするには、プロジェクトの IP アクセス リストに [クラスターのネットワーク設定に独自の IP アドレスを追加します](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) する必要があります。

MongoDB Atlas の接続文字列は、`.env` ファイルで設定することもできます。

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Laravel MongoDB パッケージをインストールする

最後に、Composer を使用して Laravel MongoDB パッケージをインストールします。

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]  
> `mongodb` PHP 拡張機能がインストールされていない場合、パッケージのこのインストールは失敗します。 PHP 設定は CLI と Web サーバー間で異なる場合があるため、両方の設定で拡張機能が有効になっていることを確認してください。

<a name="configuration"></a>
## 構成 (Configuration)

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
## 特徴 (Features)

構成が完了したら、アプリケーションで `mongodb` パッケージとデータベース接続を使用して、さまざまな強力な機能を活用できます。

- [Eloquentの使用](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/)、モデルは MongoDB コレクションに保存できます。標準の Eloquent 機能に加えて、Laravel MongoDB パッケージは埋め込みリレーションシップなどの追加機能を提供します。このパッケージは、MongoDB ドライバへの直接アクセスも提供し、生のクエリや集計パイプラインなどの操作を実行するために使用できます。
- クエリビルダを使用した [複雑なクエリを作成する](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/)。
- `mongodb` [キャッシュドライバ](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) は、TTL インデックスなどの MongoDB 機能を使用して期限切れのキャッシュ エントリを自動的にクリアするように最適化されています。
- [キューに入れられたジョブをディスパッチして処理する](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) と `mongodb` キュー ドライバ。
- [GridFS へのファイルの保存](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/gridfs/)、[フライシステム用 GridFS アダプター](https://flysystem.thephpleague.com/docs/adapter/gridfs/) 経由。
- データベース接続または Eloquent を使用するほとんどのサードパーティ パッケージは、MongoDB で使用できます。

MongoDB と Laravel の使用方法を学習し続けるには、MongoDB の [クイックスタートガイド](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/) を参照してください。

