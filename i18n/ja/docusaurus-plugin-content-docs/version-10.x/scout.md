# Laravel Scout (Laravel Scout)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Queueing](#queueing)
- [ドライバの前提条件](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [Configuration](#configuration)
    - [モデルインデックスの構成](#configuring-model-indexes)
    - [検索可能なデータの構成](#configuring-searchable-data)
    - [モデルIDの構成](#configuring-the-model-id)
    - [モデルごとの検索エンジンの構成](#configuring-search-engines-per-model)
    - [ユーザーの識別](#identifying-users)
- [データベース / コレクション エンジン](#database-and-collection-engines)
    - [データベースエンジン](#database-engine)
    - [収集エンジン](#collection-engine)
- [Indexing](#indexing)
    - [バッチインポート](#batch-import)
    - [レコードの追加](#adding-records)
    - [記録の更新](#updating-records)
    - [レコードの削除](#removing-records)
    - [インデックス作成の一時停止](#pausing-indexing)
    - [条件付きで検索可能なモデル インスタンス](#conditionally-searchable-model-instances)
- [Searching](#searching)
    - [Where句](#where-clauses)
    - [Pagination](#pagination)
    - [ソフト削除](#soft-deleting)
    - [エンジン検索のカスタマイズ](#customizing-engine-searches)
- [カスタムエンジン](#custom-engines)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Scout](https://github.com/laravel/scout) は、[Eloquent モデル](/docs/{{version}}/eloquent) に全文検索を追加するためのシンプルなドライバベースのソリューションを提供します。 Scout はモデル オブザーバを使用して、検索インデックスを Eloquent レコードと自動的に同期させます。

現在、Scout には、[Algolia](https://www.algolia.com/)、[Meilisearch](https://www.meilisearch.com)、[Typesense](https://typesense.org)、および MySQL / PostgreSQL (`database`) ドライバが同梱されています。さらに、Scout には、ローカル開発用途向けに設計された「コレクション」ドライバが含まれており、外部の依存関係やサードパーティのサービスを必要としません。さらに、カスタム ドライバの作成は簡単で、独自の検索実装を使用して Scout を自由に拡張できます。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを介して Scout をインストールします。

```shell
composer require laravel/scout
```

Scout をインストールした後、`vendor:publish` Artisan コマンドを使用して Scout 構成ファイルを公開する必要があります。このコマンドは、`scout.php` 構成ファイルをアプリケーションの `config` ディレクトリに公開します。

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

最後に、検索可能にしたいモデルに `Laravel\Scout\Searchable` トレイトを追加します。このトレイトは、モデルと検索ドライバの同期を自動的に維持するモデル オブザーバを登録します。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;
    }

<a name="queueing"></a>
### キューイング

Scout を使用することが厳密に必須ではありませんが、ライブラリを使用する前に [キュードライバ](/docs/{{version}}/queues) を構成することを強く検討する必要があります。キューワーカーを実行すると、Scout はモデル情報を検索インデックスに同期するすべての操作をキューに入れることができるため、アプリケーションの Web インターフェイスの応答時間が大幅に向上します。

キュードライバを構成したら、`config/scout.php` 構成ファイルの `queue` オプションの値を `true` に設定します。

    'queue' => true,

`queue` オプションが `false` に設定されている場合でも、Algolia や Meil​​isearch などの一部の Scout ドライバは常に非同期でレコードのインデックスを作成することに留意することが重要です。つまり、Laravel アプリケーション内でインデックス操作が完了したとしても、検索エンジン自体には新しいレコードや更新されたレコードがすぐに反映されない可能性があります。

Scout ジョブが使用する接続とキューを指定するには、`queue` 構成オプションを配列として定義できます。

    'queue' => [
        'connection' => 'redis',
        'queue' => 'scout'
    ],

もちろん、Scout ジョブが使用する接続とキューをカスタマイズする場合は、キューワーカーを実行して、その接続とキューでジョブを処理する必要があります。

    php artisan queue:work redis --queue=scout

<a name="driver-prerequisites"></a>
## ドライバの前提条件 (Driver Prerequisites)

<a name="algolia"></a>
### アルゴリア

Algolia ドライバを使用する場合は、`config/scout.php` 構成ファイルで Algolia `id` および `secret` 資格情報を構成する必要があります。認証情報を設定したら、Composer パッケージ マネージャーを介して Algolia PHP SDK をインストールする必要もあります。

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### メイリサーチ

[Meilisearch](https://www.meilisearch.com) は、非常に高速なオープンソースの検索エンジンです。 Meilisearch をローカル マシンにインストールする方法がわからない場合は、Laravel が公式にサポートする Docker 開発環境である [Laravel Sail](/docs/{{version}}/sail#meilisearch) を使用できます。

Meilisearch ドライバを使用する場合は、Composer パッケージ マネージャーを介して Meil​​isearch PHP SDK をインストールする必要があります。

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

次に、アプリケーションの `.env` ファイル内で、`SCOUT_DRIVER` 環境変数と Meil​​isearch `host` および `key` 資格情報を設定します。

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch の詳細については、[Meilisearch ドキュメント](https://docs.meilisearch.com/learn/getting_started/quick_start.html) を参照してください。

さらに、[バイナリ互換性に関する Meil​​isearch のドキュメント](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch) を確認して、Meilisearch バイナリ バージョンと互換性のある `meilisearch/meilisearch-php` のバージョンをインストールしていることを確認する必要があります。

> [!WARNING]  
> Meilisearch を利用するアプリケーションで Scout をアップグレードする場合は、常に Meil​​isearch サービス自体に [追加の重大な変更を確認する](https://github.com/meilisearch/Meilisearch/releases) を実行する必要があります。

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org) は超高速のオープンソース検索エンジンで、キーワード検索、セマンティック検索、地理検索、ベクトル検索をサポートしています。

[self-host](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) Typesense または [Typesense Cloud](https://cloud.typesense.org) を使用できます。

Scout で Typesense の使用を開始するには、Composer パッケージ マネージャーを介して Typesense PHP SDK をインストールします。

```shell
composer require typesense/typesense-php
```

次に、アプリケーションの .env ファイル内で `SCOUT_DRIVER` 環境変数と Typesense ホストおよび API キーの資格情報を設定します。

```env
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

必要に応じて、インストールのポート、パス、プロトコルを指定することもできます。

```env
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense コレクションの追加の設定とスキーマ定義は、アプリケーションの `config/scout.php` 構成ファイル内にあります。 Typesense の詳細については、[Typesense ドキュメント](https://typesense.org/docs/guide/#quick-start) を参照してください。

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense でのストレージ用のデータの準備

Typesense を利用する場合、検索可能なモデルは、モデルの主キーを文字列にキャストし、作成日を UNIX タイムスタンプにキャストする `toSearchableArray` メソッドを定義する必要があります。

```php
/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
public function toSearchableArray()
{
    return array_merge($this->toArray(),[
        'id' => (string) $this->id,
        'created_at' => $this->created_at->timestamp,
    ]);
}
```

また、アプリケーションの `config/scout.php` ファイルで Typesense コレクション スキーマを定義する必要があります。コレクション スキーマは、Typesense を介して検索可能な各フィールドのデータ型を記述します。利用可能なすべてのスキーマ オプションの詳細については、[Typesense ドキュメント](https://typesense.org/docs/latest/api/collections.html#schema-parameters) を参照してください。

Typesense コレクションのスキーマを定義した後に変更する必要がある場合は、`scout:flush` および `scout:import` を実行します。これにより、既存のインデックス付きデータがすべて削除され、スキーマが再作成されます。または、Typesense の API を使用して、インデックス付きデータを削除せずにコレクションのスキーマを変更することもできます。

検索可能なモデルが論理的に削除可能な場合は、アプリケーションの `config/scout.php` 構成ファイル内のモデルに対応する Typesense スキーマで `__soft_deleted` フィールドを定義する必要があります。

```php
User::class => [
    'collection-schema' => [
        'fields' => [
            // ...
            [
                'name' => '__soft_deleted',
                'type' => 'int32',
                'optional' => true,
            ],
        ],
    ],
],
```

<a name="typesense-dynamic-search-parameters"></a>
#### 動的検索パラメータ

Typesense を使用すると、`options` メソッド経由で検索操作を実行するときに、[検索パラメータ](https://typesense.org/docs/latest/api/search.html#search-parameters) を動的に変更できます。

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 構成 (Configuration)

<a name="configuring-model-indexes"></a>
### モデルインデックスの構成

各 Eloquent モデルは、そのモデルの検索可能なすべてのレコードを含む特定の検索「インデックス」と同期されます。つまり、各インデックスを MySQL テーブルのように考えることができます。デフォルトでは、各モデルは、モデルの一般的な「テーブル」名に一致するインデックスに保存されます。通常、これはモデル名の複数形です。ただし、モデルの `searchableAs` メソッドをオーバーライドすることで、モデルのインデックスを自由にカスタマイズできます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;

        /**
         * Get the name of the index associated with the model.
         */
        public function searchableAs(): string
        {
            return 'posts_index';
        }
    }

<a name="configuring-searchable-data"></a>
### 検索可能なデータの構成

デフォルトでは、特定のモデルの `toArray` フォーム全体が検索インデックスに保存されます。検索インデックスに同期されるデータをカスタマイズしたい場合は、モデルの `toSearchableArray` メソッドをオーバーライドできます。

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
         * @return array<string, mixed>
         */
        public function toSearchableArray(): array
        {
            $array = $this->toArray();

            // Customize the data array...

            return $array;
        }
    }

Meilisearch などの一部の検索エンジンは、正しいタイプのデータに対してフィルター操作 (`>`、`<` など) のみを実行します。したがって、これらの検索エンジンを使用し、検索可能なデータをカスタマイズするときは、数値が正しい型にキャストされていることを確認する必要があります。

    public function toSearchableArray()
    {
        return [
            'id' => (int) $this->id,
            'name' => $this->name,
            'price' => (float) $this->price,
        ];
    }

<a name="configuring-filterable-data-for-meilisearch"></a>
#### フィルタリング可能なデータとインデックスの設定を構成する (Meilisearch)

Scout の他のドライバとは異なり、Meilisearch では、フィルター可能な属性、並べ替え可能な属性、[その他のサポートされている設定フィールド](https://docs.meilisearch.com/reference/api/settings.html) などのインデックス検索設定を事前に定義する必要があります。

フィルター可能な属性は、Scout の `where` メソッドを呼び出すときにフィルター処理する予定の属性であり、並べ替え可能な属性は、Scout の `orderBy` メソッドを呼び出すときに並べ替える予定の属性です。インデックス設定を定義するには、アプリケーションの `scout` 構成ファイル内の `meilisearch` 構成エントリの `index-settings` 部分を調整します。

```php
use App\Models\User;
use App\Models\Flight;

'meilisearch' => [
    'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),
    'key' => env('MEILISEARCH_KEY', null),
    'index-settings' => [
        User::class => [
            'filterableAttributes'=> ['id', 'name', 'email'],
            'sortableAttributes' => ['created_at'],
            // Other settings fields...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

特定のインデックスの基礎となるモデルが論理的に削除可能で、`index-settings` 配列に含まれている場合、Scout はそのインデックス上の論理的に削除されたモデルのフィルター処理のサポートを自動的に組み込みます。ソフト削除可能なモデル インデックスに対して定義するフィルター可能または並べ替え可能な属性が他にない場合は、そのモデルの `index-settings` 配列に空のエントリを追加するだけで済みます。

```php
'index-settings' => [
    Flight::class => []
],
```

アプリケーションのインデックス設定を構成した後、`scout:sync-index-settings` Artisan コマンドを呼び出す必要があります。このコマンドは、Meilisearch に現在構成されているインデックス設定を通知します。便宜上、このコマンドを展開プロセスの一部にするとよいでしょう。

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### モデルIDの構成

デフォルトでは、Scout はモデルの主キーを、検索インデックスに保存されるモデルの一意の ID/キーとして使用します。この動作をカスタマイズする必要がある場合は、モデルの `getScoutKey` メソッドと `getScoutKeyName` メソッドをオーバーライドできます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class User extends Model
    {
        use Searchable;

        /**
         * Get the value used to index the model.
         */
        public function getScoutKey(): mixed
        {
            return $this->email;
        }

        /**
         * Get the key name used to index the model.
         */
        public function getScoutKeyName(): mixed
        {
            return 'email';
        }
    }

<a name="configuring-search-engines-per-model"></a>
### モデルごとの検索エンジンの構成

検索する場合、Scout は通常、アプリケーションの `scout` 構成ファイルで指定されたデフォルトの検索エンジンを使用します。ただし、特定のモデルの検索エンジンは、モデルの `searchableUsing` メソッドをオーバーライドすることで変更できます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Engines\Engine;
    use Laravel\Scout\EngineManager;
    use Laravel\Scout\Searchable;

    class User extends Model
    {
        use Searchable;

        /**
         * Get the engine used to index the model.
         */
        public function searchableUsing(): Engine
        {
            return app(EngineManager::class)->engine('meilisearch');
        }
    }

<a name="identifying-users"></a>
### ユーザーの識別

Scout では、[Algolia](https://algolia.com) を使用するときにユーザーを自動識別することもできます。認証されたユーザーを検索操作に関連付けると、Algolia のダッシュボード内で検索分析を表示するときに役立つ場合があります。ユーザー識別を有効にするには、アプリケーションの `.env` ファイルで `SCOUT_IDENTIFY` 環境変数を `true` として定義します。

```ini
SCOUT_IDENTIFY=true
```

この機能を有効にすると、リクエストの IP アドレスと認証されたユーザーのプライマリ識別子も Algolia に渡されるため、このデータはユーザーが行った検索リクエストに関連付けられます。

<a name="database-and-collection-engines"></a>
## データベース / コレクション エンジン (Database / Collection Engines)

<a name="database-engine"></a>
### データベースエンジン

> [!WARNING]  
> データベース エンジンは現在、MySQL と PostgreSQL をサポートしています。

アプリケーションが小規模から中規模のデータベースと対話する場合、またはワークロードが軽い場合は、Scout の「データベース」エンジンを使い始めるほうが便利であると思われる場合があります。データベース エンジンは、既存のデータベースからの結果をフィルタリングするときに「where like」句と全文インデックスを使用して、クエリに該当する検索結果を決定します。

データベース エンジンを使用するには、単に `SCOUT_DRIVER` 環境変数の値を `database` に設定するか、アプリケーションの `scout` 構成ファイルで `database` ドライバを直接指定します。

```ini
SCOUT_DRIVER=database
```

データベース エンジンを優先ドライバとして指定したら、[検索可能なデータを構成する](#configuring-searchable-data) を実行する必要があります。その後、モデルに対して [検索クエリの実行](#searching) を開始できます。データベース エンジンを使用する場合、Algolia、Meilisearch、または Typesense インデックスのシードに必要なインデックス作成などの検索エンジンのインデックス作成は不要です。

#### データベース検索戦略のカスタマイズ

デフォルトでは、データベース エンジンは、[検索可能として設定されている](#configuring-searchable-data) を持つすべてのモデル属性に対して「where like」クエリを実行します。ただし、状況によっては、パフォーマンスが低下する可能性があります。したがって、データベース エンジンの検索戦略は、指定された一部の列で全文検索クエリを使用するか、文字列全体 (`%example%`) 内を検索するのではなく、文字列のプレフィックス (`example%`) を検索するために「類似箇所」制約のみを使用するように構成できます。

この動作を定義するには、モデルの `toSearchableArray` メソッドに PHP 属性を割り当てることができます。追加の検索戦略動作が割り当てられていない列は、引き続きデフォルトの「where like」戦略を使用します。

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
#[SearchUsingPrefix(['id', 'email'])]
#[SearchUsingFullText(['bio'])]
public function toSearchableArray(): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'bio' => $this->bio,
    ];
}
```

> [!WARNING]  
> 列でフルテキスト クエリ制約を使用するように指定する前に、列に [全文インデックス](/docs/{{version}}/migrations#available-index-types) が割り当てられていることを確認してください。

<a name="collection-engine"></a>
### 収集エンジン

ローカル開発中は Algolia、Meilisearch、または Typesense 検索エンジンを自由に使用できますが、「コレクション」エンジンから始めるほうが便利な場合があります。収集エンジンは、「where」句と既存のデータベースからの結果に対するコレクション フィルタリングを使用して、クエリに該当する検索結果を決定します。このエンジンを使用する場合、検索可能なモデルはローカル データベースから取得されるだけなので、検索可能なモデルに「インデックス」を付ける必要はありません。

収集エンジンを使用するには、単に `SCOUT_DRIVER` 環境変数の値を `collection` に設定するか、アプリケーションの `scout` 構成ファイルで `collection` ドライバを直接指定します。

```ini
SCOUT_DRIVER=collection
```

コレクション ドライバを優先ドライバとして指定したら、モデルに対して [検索クエリの実行](#searching) を開始できます。コレクション エンジンを使用する場合、Algolia、Meilisearch、または Typesense インデックスのシードに必要なインデックス作成などの検索エンジンのインデックス作成は不要です。

#### データベースエンジンとの違い

一見すると、「データベース」エンジンと「コレクション」エンジンはかなり似ています。どちらもデータベースと直接対話して検索結果を取得します。ただし、収集エンジンは、一致するレコードを検索するためにフルテキスト インデックスや `LIKE` 句を利用しません。代わりに、考えられるすべてのレコードを取得し、Laravel の `Str::is` ヘルパを使用して、検索文字列がモデル属性値内に存在するかどうかを判断します。

コレクション エンジンは、Laravel でサポートされるすべてのリレーショナル データベース (SQLite および SQL Server を含む) で動作するため、最も移植性の高い検索エンジンです。ただし、Scout のデータベース エンジンよりも効率は劣ります。

<a name="indexing"></a>
## インデックス作成 (Indexing)

<a name="batch-import"></a>
### バッチインポート

既存のプロジェクトに Scout をインストールする場合は、インデックスにインポートする必要があるデータベース レコードがすでに存在する可能性があります。 Scout は、既存のすべてのレコードを検索インデックスにインポートするために使用できる `scout:import` Artisan コマンドを提供します。

```shell
php artisan scout:import "App\Models\Post"
```

`flush` コマンドを使用して、モデルのすべてのレコードを検索インデックスから削除できます。

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### インポートクエリの変更

バッチインポート用にすべてのモデルを取得するために使用されるクエリを変更したい場合は、モデルに `makeAllSearchableUsing` メソッドを定義できます。ここは、モデルをインポートする前に必要となる可能性のある積極的な関係の読み込みを追加するのに最適な場所です。

    use Illuminate\Database\Eloquent\Builder;

    /**
     * Modify the query used to retrieve models when making all of the models searchable.
     */
    protected function makeAllSearchableUsing(Builder $query): Builder
    {
        return $query->with('author');
    }

> [!WARNING]  
> `makeAllSearchableUsing` メソッドは、キューを使用してモデルをバッチ インポートする場合には適用できない場合があります。モデル コレクションがジョブによって処理される場合、関係は [復元されていない](/docs/{{version}}/queues#handling-relationships) になります。

<a name="adding-records"></a>
### レコードの追加

`Laravel\Scout\Searchable` トレイトをモデルに追加したら、モデル インスタンスに `save` または `create` を追加するだけで、検索インデックスに自動的に追加されます。 Scout を [キューを使用する](#queueing) に構成した場合、この操作はキューワーカーによってバックグラウンドで実行されます。

    use App\Models\Order;

    $order = new Order;

    // ...

    $order->save();

<a name="adding-records-via-query"></a>
#### クエリによるレコードの追加

Eloquent クエリを介してモデルのコレクションを検索インデックスに追加したい場合は、`searchable` メソッドを Eloquent クエリにチェーンできます。 `searchable` メソッドは、クエリの [結果をチャンク化する](/docs/{{version}}/eloquent#chunking-results) を実行し、レコードを検索インデックスに追加します。繰り返しますが、キューを使用するように Scout を構成している場合、すべてのチャンクがキューワーカーによってバックグラウンドでインポートされます。

    use App\Models\Order;

    Order::where('price', '>', 100)->searchable();

Eloquent リレーションシップ インスタンスで `searchable` メソッドを呼び出すこともできます。

    $user->orders()->searchable();

または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `searchable` メソッドを呼び出して、モデル インスタンスを対応するインデックスに追加することもできます。

    $orders->searchable();

> [!NOTE]  
> `searchable` メソッドは、「upsert」操作とみなすことができます。つまり、モデル レコードがすでにインデックスに存在する場合、それは更新されます。検索インデックスに存在しない場合は、インデックスに追加されます。

<a name="updating-records"></a>
### 記録の更新

検索可能なモデルを更新するには、モデル インスタンスのプロパティとデータベースのモデルを `save` 更新するだけです。 Scout は、検索インデックスへの変更を自動的に永続化します。

    use App\Models\Order;

    $order = Order::find(1);

    // Update the order...

    $order->save();

Eloquent クエリ インスタンスで `searchable` メソッドを呼び出して、モデルのコレクションを更新することもできます。モデルが検索インデックスに存在しない場合は、作成されます。

    Order::where('price', '>', 100)->searchable();

関係内のすべてのモデルの検索インデックス レコードを更新したい場合は、関係インスタンスで `searchable` を呼び出します。

    $user->orders()->searchable();

または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `searchable` メソッドを呼び出して、対応するインデックス内のモデル インスタンスを更新することもできます。

    $orders->searchable();

<a name="modifying-records-before-importing"></a>
#### インポート前のレコードの変更

場合によっては、モデルのコレクションを検索可能にする前に準備する必要がある場合があります。たとえば、関係データを検索インデックスに効率的に追加できるように、関係を一括ロードすることができます。これを実現するには、対応するモデルで `makeSearchableUsing` メソッドを定義します。

    use Illuminate\Database\Eloquent\Collection;

    /**
     * Modify the collection of models being made searchable.
     */
    public function makeSearchableUsing(Collection $models): Collection
    {
        return $models->load('author');
    }

<a name="removing-records"></a>
### レコードの削除

インデックスからレコードを削除するには、データベースからモデルを `delete` するだけです。これは、[ソフト削除されました](/docs/{{version}}/eloquent#soft-deleting) モデルを使用している場合でも実行できます。

    use App\Models\Order;

    $order = Order::find(1);

    $order->delete();

レコードを削除する前にモデルを取得したくない場合は、Eloquent クエリ インスタンスで `unsearchable` メソッドを使用できます。

    Order::where('price', '>', 100)->unsearchable();

関係内のすべてのモデルの検索インデックス レコードを削除したい場合は、関係インスタンスで `unsearchable` を呼び出します。

    $user->orders()->unsearchable();

または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `unsearchable` メソッドを呼び出して、対応するインデックスからモデル インスタンスを削除することもできます。

    $orders->unsearchable();

<a name="pausing-indexing"></a>
### インデックス作成の一時停止

場合によっては、モデル データを検索インデックスに同期せずに、モデルに対して Eloquent 操作のバッチを実行する必要がある場合があります。これは、`withoutSyncingToSearch` メソッドを使用して行うことができます。このメソッドは、ただちに実行される単一のクロージャを受け入れます。クロージャ内で発生するモデル操作はモデルのインデックスに同期されません。

    use App\Models\Order;

    Order::withoutSyncingToSearch(function () {
        // Perform model actions...
    });

<a name="conditionally-searchable-model-instances"></a>
### 条件付きで検索可能なモデル インスタンス

場合によっては、特定の条件下でのみモデルを検索可能にすることが必要な場合があります。たとえば、「ドラフト」と「公開」の 2 つの状態のいずれかにある `App\Models\Post` モデルがあるとします。 「公開された」投稿のみを検索可能にしたい場合があります。これを実現するには、モデルに `shouldBeSearchable` メソッドを定義します。

    /**
     * Determine if the model should be searchable.
     */
    public function shouldBeSearchable(): bool
    {
        return $this->isPublished();
    }

`shouldBeSearchable` メソッドは、`save` および `create` メソッド、クエリ、または関係を通じてモデルを操作する場合にのみ適用されます。 `searchable` メソッドを使用してモデルまたはコレクションを直接検索可能にすると、`shouldBeSearchable` メソッドの結果がオーバーライドされます。

> [!WARNING]  
> 検索可能なすべてのデータは常にデータベースに保存されるため、Scout の「データベース」エンジンを使用する場合、`shouldBeSearchable` メソッドは適用できません。データベース エンジンを使用するときに同様の動作を実現するには、代わりに [where 句](#where-clauses) を使用する必要があります。

<a name="searching"></a>
## 検索中 (Searching)

`search` メソッドを使用してモデルの検索を開始できます。検索メソッドは、モデルの検索に使用される単一の文字列を受け入れます。次に、`get` メソッドを検索クエリに連鎖させて、指定された検索クエリに一致する Eloquent モデルを取得する必要があります。

    use App\Models\Order;

    $orders = Order::search('Star Trek')->get();

Scout 検索では Eloquent モデルのコレクションが返されるため、ルートまたはコントローラから直接結果を返すこともでき、結果は自動的に JSON に変換されます。

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/search', function (Request $request) {
        return Order::search($request->search)->get();
    });

Eloquent モデルに変換される前に生の検索結果を取得したい場合は、`raw` メソッドを使用できます。

    $orders = Order::search('Star Trek')->raw();

<a name="custom-indexes"></a>
#### カスタムインデックス

検索クエリは通常、モデルの [`searchableAs`](#configuring-model-indexes) メソッドで指定されたインデックスに対して実行されます。ただし、代わりに `within` メソッドを使用して、検索するカスタム インデックスを指定することもできます。

    $orders = Order::search('Star Trek')
        ->within('tv_shows_popularity_desc')
        ->get();

<a name="where-clauses"></a>
### Where句

Scout を使用すると、検索クエリに単純な「where」句を追加できます。現在、これらの句は基本的な数値の等価性チェックのみをサポートしており、主に所有者 ID による検索クエリの範囲を指定する場合に役立ちます。

    use App\Models\Order;

    $orders = Order::search('Star Trek')->where('user_id', 1)->get();

さらに、`whereIn` メソッドを使用して、指定された列の値が指定された配列内に含まれていることを確認できます。

    $orders = Order::search('Star Trek')->whereIn(
        'status', ['open', 'paid']
    )->get();

`whereNotIn` メソッドは、指定された列の値が指定された配列に含まれていないことを検証します。

    $orders = Order::search('Star Trek')->whereNotIn(
        'status', ['closed']
    )->get();

検索インデックスはリレーショナル データベースではないため、より高度な "where" 句は現在サポートされていません。

> [!WARNING]  
> アプリケーションが Meil​​isearch を使用している場合は、Scout の「where」句を使用する前に、アプリケーションの [フィルタリング可能な属性](#configuring-filterable-data-for-meilisearch) を構成する必要があります。

<a name="pagination"></a>
### ページネーション

モデルのコレクションを取得するだけでなく、`paginate` メソッドを使用して検索結果をページ分割することもできます。このメソッドは、[従来の Eloquent クエリのページ分割](/docs/{{version}}/pagination) がある場合と同様に、`Illuminate\Pagination\LengthAwarePaginator` インスタンスを返します。

    use App\Models\Order;

    $orders = Order::search('Star Trek')->paginate();

`paginate` メソッドの最初の引数として量を渡すことで、ページごとに取得するモデルの数を指定できます。

    $orders = Order::search('Star Trek')->paginate(15);

結果を取得したら、従来の Eloquent クエリをページ分割した場合と同じように、[Blade](/docs/{{version}}/blade) を使用して結果を表示し、ページ リンクをレンダリングできます。

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

もちろん、ページネーションの結果を JSON として取得したい場合は、ルートまたはコントローラから直接ページネータ インスタンスを返すこともできます。

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        return Order::search($request->input('query'))->paginate(15);
    });

> [!WARNING]  
> 検索エンジンは Eloquent モデルのグローバル スコープ定義を認識しないため、Scout ページネーションを利用するアプリケーションではグローバル スコープを利用しないでください。または、Scout 経由で検索するときに、グローバル スコープの制約を再作成する必要があります。

<a name="soft-deleting"></a>
### ソフト削除

インデックス付きモデルが [ソフト削除](/docs/{{version}}/eloquent#soft-deleting) で、論理的に削除されたモデルを検索する必要がある場合は、`config/scout.php` 構成ファイルの `soft_delete` オプションを `true` に設定します。

    'soft_delete' => true,

この構成オプションが `true` の場合、Scout は検索インデックスから論理的に削除されたモデルを削除しません。代わりに、インデックス付きレコードに非表示の `__soft_deleted` 属性を設定します。次に、検索時に `withTrashed` メソッドまたは `onlyTrashed` メソッドを使用して、論理的に削除されたレコードを取得できます。

    use App\Models\Order;

    // Include trashed records when retrieving results...
    $orders = Order::search('Star Trek')->withTrashed()->get();

    // Only include trashed records when retrieving results...
    $orders = Order::search('Star Trek')->onlyTrashed()->get();

> [!NOTE]  
> 論理的に削除されたモデルが `forceDelete` を使用して完全に削除されると、Scout はそのモデルを検索インデックスから自動的に削除します。

<a name="customizing-engine-searches"></a>
### エンジン検索のカスタマイズ

エンジンの検索動作の高度なカスタマイズを実行する必要がある場合は、`search` メソッドの 2 番目の引数としてクロージャーを渡すことができます。たとえば、このコールバックを使用して、検索クエリが Algolia に渡される前に、地理的位置データを検索オプションに追加できます。

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

<a name="customizing-the-eloquent-results-query"></a>
#### Eloquent 結果クエリのカスタマイズ

Scout がアプリケーションの検索エンジンから一致する Eloquent モデルのリストを取得した後、Eloquent を使用して主キーによって一致するすべてのモデルを取得します。 `query` メソッドを呼び出して、このクエリをカスタマイズできます。 `query` メソッドは、Eloquent クエリビルダ インスタンスを引数として受け取るクロージャを受け入れます。

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

このコールバックは、関連するモデルがアプリケーションの検索エンジンからすでに取得された後に呼び出されるため、結果の「フィルタリング」には `query` メソッドを使用しないでください。代わりに、[where 句を調べる](#where-clauses) を使用する必要があります。

<a name="custom-engines"></a>
## カスタムエンジン (Custom Engines)

<a name="writing-the-engine"></a>
#### エンジンを書く

組み込みの Scout 検索エンジンの 1 つがニーズに合わない場合は、独自のカスタム エンジンを作成して Scout に登録できます。エンジンは `Laravel\Scout\Engines\Engine` 抽象クラスを拡張する必要があります。この抽象クラスには、カスタム エンジンが実装する必要がある 8 つのメソッドが含まれています。

    use Laravel\Scout\Builder;

    abstract public function update($models);
    abstract public function delete($models);
    abstract public function search(Builder $builder);
    abstract public function paginate(Builder $builder, $perPage, $page);
    abstract public function mapIds($results);
    abstract public function map(Builder $builder, $results, $model);
    abstract public function getTotalCount($results);
    abstract public function flush($model);

`Laravel\Scout\Engines\AlgoliaEngine` クラスでのこれらのメソッドの実装を確認すると役立つ場合があります。このクラスは、これらの各メソッドを独自のエンジンに実装する方法を学習するための良い出発点となります。

<a name="registering-the-engine"></a>
#### エンジンの登録

カスタム エンジンを作成したら、Scout エンジン マネージャーの `extend` メソッドを使用して、Scout に登録できます。 Scout のエンジン マネージャーは、Laravel サービスコンテナーから解決される場合があります。 `App\Providers\AppServiceProvider` クラスの `boot` メソッド、またはアプリケーションで使用される他のサービスプロバイダから `extend` メソッドを呼び出す必要があります。

    use App\ScoutExtensions\MySqlSearchEngine;
    use Laravel\Scout\EngineManager;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        resolve(EngineManager::class)->extend('mysql', function () {
            return new MySqlSearchEngine;
        });
    }

エンジンが登録されたら、アプリケーションの `config/scout.php` 構成ファイルでデフォルトの Scout `driver` として指定できます。

    'driver' => 'mysql',

