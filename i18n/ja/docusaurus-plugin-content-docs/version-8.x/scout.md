<!-- # Laravel Scout -->
# Laravel Scout

- [Introduction](#introduction)
- [Installation](#installation)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Queueing](#queueing)
- [Configuration](#configuration)
    - [Configuring Model Indexes](#configuring-model-indexes)
    - [Configuring Searchable Data](#configuring-searchable-data)
    - [Configuring The Model ID](#configuring-the-model-id)
    - [Identifying Users](#identifying-users)
- [Local Development](#local-development)
- [Indexing](#indexing)
    - [Batch Import](#batch-import)
    - [Adding Records](#adding-records)
    - [Updating Records](#updating-records)
    - [Removing Records](#removing-records)
    - [Pausing Indexing](#pausing-indexing)
    - [Conditionally Searchable Model Instances](#conditionally-searchable-model-instances)
- [Searching](#searching)
    - [Where Clauses](#where-clauses)
    - [Pagination](#pagination)
    - [Soft Deleting](#soft-deleting)
    - [Customizing Engine Searches](#customizing-engine-searches)
- [Custom Engines](#custom-engines)
- [Builder Macros](#builder-macros)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Scout](https://github.com/laravel/scout) provides a simple, driver based solution for adding full-text search to your [Eloquent models](/docs/8.x/eloquent). Using model observers, Scout will automatically keep your search indexes in sync with your Eloquent records. -->
[Laravel Scout](https://github.com/laravel/scout) は、[Eloquent models](/docs/8.x/eloquent) に全文検索を追加するためのシンプルなドライバベースのソリューションを提供します。 Scout はモデル オブザーバを使用して、検索インデックスを Eloquent レコードと自動的に同期させます。

<!-- Currently, Scout ships with [Algolia](https://www.algolia.com/) and [MeiliSearch](https://www.meilisearch.com) drivers. In addition, Scout includes a "collection" driver that is designed for local development usage and does not require any external dependencies or third-party services. Furthermore, writing custom drivers is simple and you are free to extend Scout with your own search implementations. -->
現在、Scout には [Algolia](https://www.algolia.com/) ドライバと [MeiliSearch](https://www.meilisearch.com) ドライバが同梱されています。さらに、Scout には、ローカル開発用途向けに設計された「コレクション」ドライバが含まれており、外部の依存関係やサードパーティのサービスを必要としません。さらに、カスタム ドライバの作成は簡単で、独自の検索実装を使用して Scout を自由に拡張できます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Scout via the Composer package manager: -->
まず、Composer パッケージ マネージャーを介して Scout をインストールします。

```
composer require laravel/scout
```

<!-- After installing Scout, you should publish the Scout configuration file using the `vendor:publish` Artisan command. This command will publish the `scout.php` configuration file to your application's `config` directory: -->
Scout をインストールした後、`vendor:publish` Artisan コマンドを使用して Scout 構成ファイルを公開する必要があります。このコマンドは、`scout.php` 構成ファイルをアプリケーションの `config` ディレクトリに公開します。

```
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

<!-- Finally, add the `Laravel\Scout\Searchable` trait to the model you would like to make searchable. This trait will register a model observer that will automatically keep the model in sync with your search driver: -->
最後に、検索可能にしたいモデルに `Laravel\Scout\Searchable` トレイトを追加します。このトレイトは、モデルと検索ドライバの同期を自動的に維持するモデル オブザーバを登録します。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
}
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="algolia"></a>
<!-- #### Algolia -->
#### Algolia

<!-- When using the Algolia driver, you should configure your Algolia `id` and `secret` credentials in your `config/scout.php` configuration file. Once your credentials have been configured, you will also need to install the Algolia PHP SDK via the Composer package manager: -->
Algolia ドライバを使用する場合は、`config/scout.php` 構成ファイルで Algolia `id` および `secret` 資格情報を構成する必要があります。認証情報を設定したら、Composer パッケージ マネージャーを介して Algolia PHP SDK をインストールする必要もあります。

```
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
<!-- #### MeiliSearch -->
#### MeiliSearch

<!-- [MeiliSearch](https://www.meilisearch.com) is a blazingly fast and open source search engine. If you aren't sure how to install MeiliSearch on your local machine, you may use [Laravel Sail](/docs/8.x/sail#meilisearch), Laravel's officially supported Docker development environment. -->
[MeiliSearch](https://www.meilisearch.com) は、非常に高速なオープンソースの検索エンジンです。 MeiliSearch をローカル マシンにインストールする方法がわからない場合は、Laravel が公式にサポートする Docker 開発環境である [Laravel Sail](/docs/8.x/sail#meilisearch) を使用できます。

<!-- When using the MeiliSearch driver you will need to install the MeiliSearch PHP SDK via the Composer package manager: -->
MeiliSearch ドライバを使用する場合は、Composer パッケージ マネージャーを介して Meil​​iSearch PHP SDK をインストールする必要があります。

```
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

<!-- Then, set the `SCOUT_DRIVER` environment variable as well as your MeiliSearch `host` and `key` credentials within your application's `.env` file: -->
次に、アプリケーションの `.env` ファイル内で、`SCOUT_DRIVER` 環境変数と Meil​​iSearch `host` および `key` 資格情報を設定します。

```
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

<!-- For more information regarding MeiliSearch, please consult the [MeiliSearch documentation](https://docs.meilisearch.com/learn/getting_started/quick_start.html). -->
MeiliSearch の詳細については、[MeiliSearch documentation](https://docs.meilisearch.com/learn/getting_started/quick_start.html) を参照してください。

<!-- In addition, you should ensure that you install a version of `meilisearch/meilisearch-php` that is compatible with your MeiliSearch binary version by reviewing [MeiliSearch's documentation regarding binary compatibility](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch). -->
さらに、[MeiliSearch's documentation regarding binary compatibility](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch) を確認して、MeiliSearch バイナリ バージョンと互換性のある `meilisearch/meilisearch-php` のバージョンをインストールしていることを確認する必要があります。

> [!NOTE]
> Meil​​iSearch を利用するアプリケーションで Scout をアップグレードする場合は、常に Meil​​iSearch サービス自体に [review any additional breaking changes](https://github.com/meilisearch/MeiliSearch/releases) する必要があります。

<a name="queueing"></a>
<!-- ### Queueing -->
### Queueing

<!-- While not strictly required to use Scout, you should strongly consider configuring a [queue driver](/docs/8.x/queues) before using the library. Running a queue worker will allow Scout to queue all operations that sync your model information to your search indexes, providing much better response times for your application's web interface. -->
Scout を使用することが厳密に必須ではありませんが、ライブラリを使用する前に [queue driver](/docs/8.x/queues) を構成することを強く検討する必要があります。キューワーカーを実行すると、Scout はモデル情報を検索インデックスに同期するすべての操作をキューに入れることができるため、アプリケーションの Web インターフェイスの応答時間が大幅に向上します。

<!-- Once you have configured a queue driver, set the value of the `queue` option in your `config/scout.php` configuration file to `true`: -->
キュードライバを構成したら、`config/scout.php` 構成ファイルの `queue` オプションの値を `true` に設定します。

```
'queue' => true,
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="configuring-model-indexes"></a>
<!-- ### Configuring Model Indexes -->
### Configuring Model Indexes

<!-- Each Eloquent model is synced with a given search "index", which contains all of the searchable records for that model. In other words, you can think of each index like a MySQL table. By default, each model will be persisted to an index matching the model's typical "table" name. Typically, this is the plural form of the model name; however, you are free to customize the model's index by overriding the `searchableAs` method on the model: -->
各 Eloquent モデルは、そのモデルの検索可能なすべてのレコードを含む特定の検索「インデックス」と同期されます。つまり、各インデックスを MySQL テーブルのように考えることができます。デフォルトでは、各モデルは、モデルの一般的な「テーブル」名に一致するインデックスに保存されます。通常、これはモデル名の複数形です。ただし、モデルの `searchableAs` メソッドをオーバーライドすることで、モデルのインデックスを自由にカスタマイズできます。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the name of the index associated with the model.
     *
     * @return string
     */
    public function searchableAs()
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
<!-- ### Configuring Searchable Data -->
### Configuring Searchable Data

<!-- By default, the entire `toArray` form of a given model will be persisted to its search index. If you would like to customize the data that is synchronized to the search index, you may override the `toSearchableArray` method on the model: -->
デフォルトでは、特定のモデルの `toArray` フォーム全体が検索インデックスに保存されます。検索インデックスに同期されるデータをカスタマイズしたい場合は、モデルの `toSearchableArray` メソッドをオーバーライドできます。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the indexable data array for the model.
     *
     * @return array
     */
    public function toSearchableArray()
    {
        $array = $this->toArray();

        // Customize the data array...

        return $array;
    }
}
```

<a name="configuring-the-model-id"></a>
<!-- ### Configuring The Model ID -->
### Configuring The Model ID

<!-- By default, Scout will use the primary key of the model as model's unique ID / key that is stored in the search index. If you need to customize this behavior, you may override the `getScoutKey` and the `getScoutKeyName` methods on the model: -->
デフォルトでは、Scout はモデルの主キーを、検索インデックスに保存されるモデルの一意の ID/キーとして使用します。この動作をカスタマイズする必要がある場合は、モデルの `getScoutKey` メソッドと `getScoutKeyName` メソッドをオーバーライドできます。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the value used to index the model.
     *
     * @return mixed
     */
    public function getScoutKey()
    {
        return $this->email;
    }

    /**
     * Get the key name used to index the model.
     *
     * @return mixed
     */
    public function getScoutKeyName()
    {
        return 'email';
    }
}
```

<a name="identifying-users"></a>
<!-- ### Identifying Users -->
### Identifying Users

<!-- Scout also allows you to auto identify users when using [Algolia](https://algolia.com). Associating the authenticated user with search operations may be helpful when viewing your search analytics within Algolia's dashboard. You can enable user identification by defining a `SCOUT_IDENTIFY` environment variable as `true` in your application's `.env` file: -->
Scout では、[Algolia](https://algolia.com) を使用するときにユーザーを自動識別することもできます。認証されたユーザーを検索操作に関連付けると、Algolia のダッシュボード内で検索分析を表示するときに役立つ場合があります。ユーザー識別を有効にするには、アプリケーションの `.env` ファイルで `SCOUT_IDENTIFY` 環境変数を `true` として定義します。

```
SCOUT_IDENTIFY=true
```

<!-- Enabling this feature this will also pass the request's IP address and your authenticated user's primary identifier to Algolia so this data is associated with any search request that is made by the user. -->
この機能を有効にすると、リクエストの IP アドレスと認証されたユーザーのプライマリ識別子も Algolia に渡されるため、このデータはユーザーによって行われた検索リクエストに関連付けられます。

<a name="local-development"></a>
<!-- ## Local Development -->
## Local Development

<!-- While you are free to use the Algolia or MeiliSearch search engines during local development, you may find it more convenient to get started with the "collection" engine. The collection engine will use "where" clauses and collection filtering on results from your existing database to determine the applicable search results for your query. When using this engine, it is not necessary to "index" your searchable models, as they will simply be retrieved from your local database. -->
ローカル開発中に Algolia または Meil​​iSearch 検索エンジンを自由に使用できますが、「コレクション」エンジンから始めるほうが便利であると思われる場合があります。収集エンジンは、「where」句と既存のデータベースからの結果に対するコレクション フィルタリングを使用して、クエリに該当する検索結果を決定します。このエンジンを使用する場合、検索可能なモデルはローカル データベースから取得されるだけなので、検索可能なモデルに「インデックス」を付ける必要はありません。

<!-- To use the collection engine, you may simply set the value of the `SCOUT_DRIVER` environment variable to `collection`, or specify the `collection` driver directly in your application's `scout` configuration file: -->
収集エンジンを使用するには、単に `SCOUT_DRIVER` 環境変数の値を `collection` に設定するか、アプリケーションの `scout` 構成ファイルで `collection` ドライバを直接指定します。

```ini
SCOUT_DRIVER=collection
```

<!-- Once you have specified the collection driver as your preferred driver, you may start [executing search queries](#searching) against your models. Search engine indexing, such as the indexing needed to seed Algolia or MeiliSearch indexes, is unnecessary when using the collection engine. -->
コレクション ドライバを優先ドライバとして指定したら、モデルに対して [executing search queries](#searching) を開始できます。コレクション エンジンを使用する場合、Algolia インデックスや Meil​​iSearch インデックスのシードに必要なインデックス作成など、検索エンジンのインデックス作成は不要です。

<a name="indexing"></a>
<!-- ## Indexing -->
## Indexing

<a name="batch-import"></a>
<!-- ### Batch Import -->
### Batch Import

<!-- If you are installing Scout into an existing project, you may already have database records you need to import into your indexes. Scout provides a `scout:import` Artisan command that you may use to import all of your existing records into your search indexes: -->
既存のプロジェクトに Scout をインストールする場合は、インデックスにインポートする必要があるデータベース レコードがすでに存在する可能性があります。 Scout は、既存のすべてのレコードを検索インデックスにインポートするために使用できる `scout:import` Artisan コマンドを提供します。

```
php artisan scout:import "App\Models\Post"
```

<!-- The `flush` command may be used to remove all of a model's records from your search indexes: -->
`flush` コマンドを使用して、モデルのすべてのレコードを検索インデックスから削除できます。

```
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
<!-- #### Modifying The Import Query -->
#### Modifying The Import Query

<!-- If you would like to modify the query that is used to retrieve all of your models for batch importing, you may define a `makeAllSearchableUsing` method on your model. This is a great place to add any eager relationship loading that may be necessary before importing your models: -->
バッチインポート用にすべてのモデルを取得するために使用されるクエリを変更したい場合は、モデルに `makeAllSearchableUsing` メソッドを定義できます。ここは、モデルをインポートする前に必要となる可能性のある積極的な関係の読み込みを追加するのに最適な場所です。

```
/**
 * Modify the query used to retrieve models when making all of the models searchable.
 *
 * @param  \Illuminate\Database\Eloquent\Builder  $query
 * @return \Illuminate\Database\Eloquent\Builder
 */
protected function makeAllSearchableUsing($query)
{
    return $query->with('author');
}
```

<a name="adding-records"></a>
<!-- ### Adding Records -->
### Adding Records

<!-- Once you have added the `Laravel\Scout\Searchable` trait to a model, all you need to do is `save` or `create` a model instance and it will automatically be added to your search index. If you have configured Scout to [use queues](#queueing) this operation will be performed in the background by your queue worker: -->
`Laravel\Scout\Searchable` トレイトをモデルに追加したら、モデル インスタンスに `save` または `create` を追加するだけで、検索インデックスに自動的に追加されます。 Scout を [use queues](#queueing) に構成した場合、この操作はキューワーカーによってバックグラウンドで実行されます。

```
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
<!-- #### Adding Records Via Query -->
#### Adding Records Via Query

<!-- If you would like to add a collection of models to your search index via an Eloquent query, you may chain the `searchable` method onto the Eloquent query. The `searchable` method will [chunk the results](/docs/8.x/eloquent#chunking-results) of the query and add the records to your search index. Again, if you have configured Scout to use queues, all of the chunks will be imported in the background by your queue workers: -->
Eloquent クエリを介してモデルのコレクションを検索インデックスに追加したい場合は、`searchable` メソッドを Eloquent クエリにチェーンできます。 `searchable` メソッドは、クエリの [chunk the results](/docs/8.x/eloquent#chunking-results) を実行し、レコードを検索インデックスに追加します。繰り返しますが、キューを使用するように Scout を構成している場合、すべてのチャンクがキューワーカーによってバックグラウンドでインポートされます。

```
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

<!-- You may also call the `searchable` method on an Eloquent relationship instance: -->
Eloquent リレーションシップ インスタンスで `searchable` メソッドを呼び出すこともできます。

```
$user->orders()->searchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to add the model instances to their corresponding index: -->
または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `searchable` メソッドを呼び出して、モデル インスタンスを対応するインデックスに追加することもできます。

```
$orders->searchable();
```

> [!TIP]
> `searchable` メソッドは、「upsert」操作とみなすことができます。つまり、モデル レコードがすでにインデックスに存在する場合、それは更新されます。検索インデックスに存在しない場合は、インデックスに追加されます。

<a name="updating-records"></a>
<!-- ### Updating Records -->
### Updating Records

<!-- To update a searchable model, you only need to update the model instance's properties and `save` the model to your database. Scout will automatically persist the changes to your search index: -->
検索可能なモデルを更新するには、モデル インスタンスのプロパティとデータベースのモデルを `save` 更新するだけです。 Scout は、検索インデックスへの変更を自動的に永続化します。

```
use App\Models\Order;

$order = Order::find(1);

// Update the order...

$order->save();
```

<!-- You may also invoke the `searchable` method on an Eloquent query instance to update a collection of models. If the models do not exist in your search index, they will be created: -->
Eloquent クエリ インスタンスで `searchable` メソッドを呼び出して、モデルのコレクションを更新することもできます。モデルが検索インデックスに存在しない場合は、作成されます。

```
Order::where('price', '>', 100)->searchable();
```

<!-- If you would like to update the search index records for all of the models in a relationship, you may invoke the `searchable` on the relationship instance: -->
関係内のすべてのモデルの検索インデックス レコードを更新したい場合は、関係インスタンスで `searchable` を呼び出します。

```
$user->orders()->searchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to update the model instances in their corresponding index: -->
または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `searchable` メソッドを呼び出して、対応するインデックス内のモデル インスタンスを更新することもできます。

```
$orders->searchable();
```

<a name="removing-records"></a>
<!-- ### Removing Records -->
### Removing Records

<!-- To remove a record from your index you may simply `delete` the model from the database. This may be done even if you are using [soft deleted](/docs/8.x/eloquent#soft-deleting) models: -->
インデックスからレコードを削除するには、データベースからモデルを `delete` するだけです。これは、[soft deleted](/docs/8.x/eloquent#soft-deleting) モデルを使用している場合でも実行できます。

```
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

<!-- If you do not want to retrieve the model before deleting the record, you may use the `unsearchable` method on an Eloquent query instance: -->
レコードを削除する前にモデルを取得したくない場合は、Eloquent クエリ インスタンスで `unsearchable` メソッドを使用できます。

```
Order::where('price', '>', 100)->unsearchable();
```

<!-- If you would like to remove the search index records for all of the models in a relationship, you may invoke the `unsearchable` on the relationship instance: -->
関係内のすべてのモデルの検索インデックス レコードを削除したい場合は、関係インスタンスで `unsearchable` を呼び出します。

```
$user->orders()->unsearchable();
```

<!-- Or, if you already have a collection of Eloquent models in memory, you may call the `unsearchable` method on the collection instance to remove the model instances from their corresponding index: -->
または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `unsearchable` メソッドを呼び出して、対応するインデックスからモデル インスタンスを削除することもできます。

```
$orders->unsearchable();
```

<a name="pausing-indexing"></a>
<!-- ### Pausing Indexing -->
### Pausing Indexing

<!-- Sometimes you may need to perform a batch of Eloquent operations on a model without syncing the model data to your search index. You may do this using the `withoutSyncingToSearch` method. This method accepts a single closure which will be immediately executed. Any model operations that occur within the closure will not be synced to the model's index: -->
場合によっては、モデル データを検索インデックスに同期せずに、モデルに対して Eloquent 操作のバッチを実行する必要がある場合があります。これは、`withoutSyncingToSearch` メソッドを使用して行うことができます。このメソッドは、ただちに実行される単一のクロージャを受け入れます。クロージャ内で発生するモデル操作はモデルのインデックスに同期されません。

```
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // Perform model actions...
});
```

<a name="conditionally-searchable-model-instances"></a>
<!-- ### Conditionally Searchable Model Instances -->
### Conditionally Searchable Model Instances

<!-- Sometimes you may need to only make a model searchable under certain conditions. For example, imagine you have `App\Models\Post` model that may be in one of two states: "draft" and "published". You may only want to allow "published" posts to be searchable. To accomplish this, you may define a `shouldBeSearchable` method on your model: -->
場合によっては、特定の条件下でのみモデルを検索可能にすることが必要な場合があります。たとえば、「ドラフト」と「公開」の 2 つの状態のいずれかにある `App\Models\Post` モデルがあるとします。 「公開された」投稿のみを検索可能にしたい場合があります。これを実現するには、モデルに `shouldBeSearchable` メソッドを定義します。

```
/**
 * Determine if the model should be searchable.
 *
 * @return bool
 */
public function shouldBeSearchable()
{
    return $this->isPublished();
}
```

<!-- The `shouldBeSearchable` method is only applied when manipulating models through the `save` and `create` methods, queries, or relationships. Directly making models or collections searchable using the `searchable` method will override the result of the `shouldBeSearchable` method. -->
`shouldBeSearchable` メソッドは、`save` および `create` メソッド、クエリ、または関係を通じてモデルを操作する場合にのみ適用されます。 `searchable` メソッドを使用してモデルまたはコレクションを直接検索可能にすると、`shouldBeSearchable` メソッドの結果がオーバーライドされます。

<a name="searching"></a>
<!-- ## Searching -->
## Searching

<!-- You may begin searching a model using the `search` method. The search method accepts a single string that will be used to search your models. You should then chain the `get` method onto the search query to retrieve the Eloquent models that match the given search query: -->
`search` メソッドを使用してモデルの検索を開始できます。検索メソッドは、モデルの検索に使用される単一の文字列を受け入れます。次に、`get` メソッドを検索クエリに連鎖させて、指定された検索クエリに一致する Eloquent モデルを取得する必要があります。

```
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

<!-- Since Scout searches return a collection of Eloquent models, you may even return the results directly from a route or controller and they will automatically be converted to JSON: -->
Scout 検索では Eloquent モデルのコレクションが返されるため、ルートまたはコントローラから直接結果を返すこともでき、結果は自動的に JSON に変換されます。

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

<!-- If you would like to get the raw search results before they are converted to Eloquent models, you may use the `raw` method: -->
Eloquent モデルに変換される前に生の検索結果を取得したい場合は、`raw` メソッドを使用できます。

```
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
<!-- #### Custom Indexes -->
#### Custom Indexes

<!-- Search queries will typically be performed on the index specified by the model's [`searchableAs`](#configuring-model-indexes) method. However, you may use the `within` method to specify a custom index that should be searched instead: -->
検索クエリは通常、モデルの [`searchableAs`](#configuring-model-indexes) メソッドで指定されたインデックスに対して実行されます。ただし、代わりに `within` メソッドを使用して、検索するカスタム インデックスを指定することもできます。

```
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
<!-- ### Where Clauses -->
### Where Clauses

<!-- Scout allows you to add simple "where" clauses to your search queries. Currently, these clauses only support basic numeric equality checks and are primarily useful for scoping search queries by an owner ID: -->
Scout を使用すると、検索クエリに単純な「where」句を追加できます。現在、これらの句は基本的な数値の等価性チェックのみをサポートしており、主に所有者 ID による検索クエリの範囲を指定する場合に役立ちます。

```
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

<!-- You may use the `whereIn` method to constrain results against a given set of values: -->
`whereIn` メソッドを使用して、特定の値のセットに対して結果を制限できます。

```
$orders = Order::search('Star Trek')->whereIn(
    'status', ['paid', 'open']
)->get();
```

<!-- Since a search index is not a relational database, more advanced "where" clauses are not currently supported. -->
検索インデックスはリレーショナル データベースではないため、より高度な "where" 句は現在サポートされていません。

<a name="pagination"></a>
<!-- ### Pagination -->
### Pagination

<!-- In addition to retrieving a collection of models, you may paginate your search results using the `paginate` method. This method will return an `Illuminate\Pagination\LengthAwarePaginator` instance just as if you had [paginated a traditional Eloquent query](/docs/8.x/pagination): -->
モデルのコレクションを取得するだけでなく、`paginate` メソッドを使用して検索結果をページ分割することもできます。このメソッドは、[paginated a traditional Eloquent query](/docs/8.x/pagination) がある場合と同様に、`Illuminate\Pagination\LengthAwarePaginator` インスタンスを返します。

```
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

<!-- You may specify how many models to retrieve per page by passing the amount as the first argument to the `paginate` method: -->
`paginate` メソッドの最初の引数として量を渡すことで、ページごとに取得するモデルの数を指定できます。

```
$orders = Order::search('Star Trek')->paginate(15);
```

<!-- Once you have retrieved the results, you may display the results and render the page links using [Blade](/docs/8.x/blade) just as if you had paginated a traditional Eloquent query: -->
結果を取得したら、従来の Eloquent クエリをページ分割した場合と同じように、[Blade](/docs/8.x/blade) を使用して結果を表示し、ページ リンクをレンダリングできます。

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

<!-- Of course, if you would like to retrieve the pagination results as JSON, you may return the paginator instance directly from a route or controller: -->
もちろん、ページネーションの結果を JSON として取得したい場合は、ルートまたはコントローラから直接ページネータ インスタンスを返すこともできます。

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

<a name="soft-deleting"></a>
<!-- ### Soft Deleting -->
### Soft Deleting

<!-- If your indexed models are [soft deleting](/docs/8.x/eloquent#soft-deleting) and you need to search your soft deleted models, set the `soft_delete` option of the `config/scout.php` configuration file to `true`: -->
インデックス付きモデルが [soft deleting](/docs/8.x/eloquent#soft-deleting) で、論理的に削除されたモデルを検索する必要がある場合は、`config/scout.php` 構成ファイルの `soft_delete` オプションを `true` に設定します。

```
'soft_delete' => true,
```

<!-- When this configuration option is `true`, Scout will not remove soft deleted models from the search index. Instead, it will set a hidden `__soft_deleted` attribute on the indexed record. Then, you may use the `withTrashed` or `onlyTrashed` methods to retrieve the soft deleted records when searching: -->
この構成オプションが `true` の場合、Scout は検索インデックスから論理的に削除されたモデルを削除しません。代わりに、インデックス付きレコードに非表示の `__soft_deleted` 属性を設定します。次に、検索時に `withTrashed` メソッドまたは `onlyTrashed` メソッドを使用して、論理的に削除されたレコードを取得できます。

```
use App\Models\Order;

// Include trashed records when retrieving results...
$orders = Order::search('Star Trek')->withTrashed()->get();

// Only include trashed records when retrieving results...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!TIP]
> `forceDelete` を使用して論理的に削除されたモデルが完全に削除されると、Scout はそのモデルを検索インデックスから自動的に削除します。

<a name="customizing-engine-searches"></a>
<!-- ### Customizing Engine Searches -->
### Customizing Engine Searches

<!-- If you need to perform advanced customization of the search behavior of an engine you may pass a closure as the second argument to the `search` method. For example, you could use this callback to add geo-location data to your search options before the search query is passed to Algolia: -->
エンジンの検索動作の高度なカスタマイズを実行する必要がある場合は、`search` メソッドの 2 番目の引数としてクロージャーを渡すことができます。たとえば、このコールバックを使用して、検索クエリが Algolia に渡される前に、地理的位置データを検索オプションに追加できます。

```
use Algolia\AlgoliaSearch\SearchIndex;
use App\Models\Order;

Order::search(
    'Star Trek',
    function (SearchIndex $algolia, string $query, array $options) {
        $options['body']['query']['bool']['filter']['geo_distance'] = [
            'distance' => '1000km',
            'location' => ['lat' => 36, 'lon' => 111],
        ];

        return $algolia->search($query, $options);
    }
)->get();
```

<a name="custom-engines"></a>
<!-- ## Custom Engines -->
## Custom Engines

<a name="writing-the-engine"></a>
<!-- #### Writing The Engine -->
#### Writing The Engine

<!-- If one of the built-in Scout search engines doesn't fit your needs, you may write your own custom engine and register it with Scout. Your engine should extend the `Laravel\Scout\Engines\Engine` abstract class. This abstract class contains eight methods your custom engine must implement: -->
組み込みの Scout 検索エンジンの 1 つがニーズに合わない場合は、独自のカスタム エンジンを作成して Scout に登録できます。エンジンは `Laravel\Scout\Engines\Engine` 抽象クラスを拡張する必要があります。この抽象クラスには、カスタム エンジンが実装する必要がある 8 つのメソッドが含まれています。

```
use Laravel\Scout\Builder;

abstract public function update($models);
abstract public function delete($models);
abstract public function search(Builder $builder);
abstract public function paginate(Builder $builder, $perPage, $page);
abstract public function mapIds($results);
abstract public function map(Builder $builder, $results, $model);
abstract public function getTotalCount($results);
abstract public function flush($model);
```

<!-- You may find it helpful to review the implementations of these methods on the `Laravel\Scout\Engines\AlgoliaEngine` class. This class will provide you with a good starting point for learning how to implement each of these methods in your own engine. -->
`Laravel\Scout\Engines\AlgoliaEngine` クラスでのこれらのメソッドの実装を確認すると役立つ場合があります。このクラスは、これらの各メソッドを独自のエンジンに実装する方法を学習するための良い出発点となります。

<a name="registering-the-engine"></a>
<!-- #### Registering The Engine -->
#### Registering The Engine

<!-- Once you have written your custom engine, you may register it with Scout using the `extend` method of the Scout engine manager. Scout's engine manager may be resolved from the Laravel service container. You should call the `extend` method from the `boot` method of your `App\Providers\AppServiceProvider` class or any other service provider used by your application: -->
カスタム エンジンを作成したら、Scout エンジン マネージャーの `extend` メソッドを使用して、Scout に登録できます。 Scout のエンジン マネージャーは、Laravel サービスコンテナーから解決される場合があります。 `App\Providers\AppServiceProvider` クラスの `boot` メソッド、またはアプリケーションで使用される他のサービスプロバイダから `extend` メソッドを呼び出す必要があります。

```
use App\ScoutExtensions\MySqlSearchEngine
use Laravel\Scout\EngineManager;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

<!-- Once your engine has been registered, you may specify it as your default Scout `driver` in your application's `config/scout.php` configuration file: -->
エンジンが登録されたら、アプリケーションの `config/scout.php` 構成ファイルでデフォルトの Scout `driver` として指定できます。

```
'driver' => 'mysql',
```

<a name="builder-macros"></a>
<!-- ## Builder Macros -->
## Builder Macros

<!-- If you would like to define a custom Scout search builder method, you may use the `macro` method on the `Laravel\Scout\Builder` class. Typically, "macros" should be defined within a [service provider's](/docs/8.x/providers) `boot` method: -->
カスタム Scout 検索ビルダ メソッドを定義したい場合は、`Laravel\Scout\Builder` クラスの `macro` メソッドを使用できます。通常、「マクロ」は [service provider's](/docs/8.x/providers) `boot` メソッド内で定義する必要があります。

```
use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;
use Laravel\Scout\Builder;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Builder::macro('count', function () {
        return $this->engine()->getTotalCount(
            $this->engine()->search($this)
        );
    });
}
```

<!-- The `macro` function accepts a macro name as its first argument and a closure as its second argument. The macro's closure will be executed when calling the macro name from a `Laravel\Scout\Builder` implementation: -->
`macro` 関数は、最初の引数としてマクロ名を、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャーは、`Laravel\Scout\Builder` 実装からマクロ名を呼び出すときに実行されます。

```
use App\Models\Order;

Order::search('Star Trek')->count();
```

