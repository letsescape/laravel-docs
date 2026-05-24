# Laravel Scout (Laravel Scout)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Queueing](#queueing)
- [ドライバの前提条件](#driver-prerequisites)
- [Configuration](#configuration)
    - [検索可能なデータの構成](#configuring-searchable-data)
- [データベース / コレクション エンジン](#database-and-collection-engines)
    - [データベースエンジン](#database-engine)
    - [収集エンジン](#collection-engine)
- [サードパーティのエンジン構成](#third-party-engine-configuration)
    - [モデルインデックスの構成](#configuring-model-indexes)
    - [Algolia](#algolia-configuration)
    - [Meilisearch](#meilisearch-configuration)
    - [Typesense](#typesense-configuration)
- [サードパーティエンジンのインデックス作成](#indexing)
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

Scout には、MySQL / PostgreSQL フルテキスト インデックスと `LIKE` 句を使用して既存のデータベースを検索する組み込みの `database` エンジンが付属しており、外部サービスは必要ありません。ほとんどのアプリケーションで必要なのはこれだけです。 Laravel で利用可能なすべての検索オプションの概要については、[ドキュメントを検索する](/docs/{{version}}/search) を参照してください。

Scout には、タイプミス耐性、ファセット フィルター、大規模な地域検索などの機能が必要な場合に備えて、[Algolia](https://www.algolia.com/)、[Meilisearch](https://www.meilisearch.com)、[Typesense](https://typesense.org) のドライバも含まれています。 「コレクション」ドライバもローカル開発に使用でき、[カスタムエンジン](#custom-engines) も自由に作成できます。

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

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
}
```

<a name="queueing"></a>
### キューイング

`database` エンジンまたは `collection` エンジンではないエンジンを使用する場合は、ライブラリを使用する前に [キュードライバ](/docs/{{version}}/queues) を構成することを強く検討する必要があります。キューワーカーを実行すると、Scout はモデル情報を検索インデックスに同期するすべての操作をキューに入れることができるため、アプリケーションの Web インターフェイスの応答時間が大幅に向上します。

キュードライバを構成したら、`config/scout.php` 構成ファイルの `queue` オプションの値を `true` に設定します。

```php
'queue' => true,
```

`queue` オプションが `false` に設定されている場合でも、Algolia や Meil​​isearch などの一部の Scout ドライバは常に非同期でレコードのインデックスを作成することに留意することが重要です。言い換えれば、Laravel アプリケーション内でインデックス操作が完了したとしても、検索エンジン自体には新しいレコードや更新されたレコードがすぐに反映されない可能性があります。

Scout ジョブが使用する接続とキューを指定するには、`queue` 構成オプションを配列として定義できます。

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

もちろん、Scout ジョブが使用する接続とキューをカスタマイズする場合は、キューワーカーを実行して、その接続とキューでジョブを処理する必要があります。

```shell
php artisan queue:work redis --queue=scout
```

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

[Meilisearch](https://www.meilisearch.com) は、高速なオープンソースの検索エンジンです。 Meilisearch をローカル マシンにインストールする方法がわからない場合は、Laravel が公式にサポートする Docker 開発環境である [Laravel Sail](/docs/{{version}}/sail#meilisearch) を使用できます。

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

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/{{version}}/sail) を使用している場合は、Docker コンテナー名と一致するように `TYPESENSE_HOST` 環境変数を調整する必要がある場合があります。オプションで、インストールのポート、パス、プロトコルを指定することもできます。

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense コレクションの追加の設定とスキーマ定義は、アプリケーションの `config/scout.php` 構成ファイル内にあります。 Typesense の詳細については、[Typesense ドキュメント](https://typesense.org/docs/guide/#quick-start) を参照してください。

<a name="configuration"></a>
## 構成 (Configuration)

<a name="configuring-searchable-data"></a>
### 検索可能なデータの構成

デフォルトでは、特定のモデルの `toArray` フォーム全体が検索インデックスに保存されます。検索インデックスに同期されるデータをカスタマイズしたい場合は、モデルの `toSearchableArray` メソッドをオーバーライドできます。

```php
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
```

<a name="configuring-search-engines-per-model"></a>
#### モデルエンジンの構成

検索する場合、Scout は通常、アプリケーションの `scout` 構成ファイルで指定されたデフォルトの検索エンジンを使用します。ただし、特定のモデルの検索エンジンは、モデルの `searchableUsing` メソッドをオーバーライドすることで変更できます。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Engines\Engine;
use Laravel\Scout\Scout;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the engine used to index the model.
     */
    public function searchableUsing(): Engine
    {
        return Scout::engine('meilisearch');
    }
}
```

<a name="database-and-collection-engines"></a>
## データベース / コレクション エンジン (Database / Collection Engines)

<a name="database-engine"></a>
### データベースエンジン

> [!WARNING]
> データベース エンジンは現在、MySQL と PostgreSQL をサポートしており、どちらも高速な全文列インデックス作成をサポートします。

`database` エンジンは、MySQL / PostgreSQL フルテキスト インデックスと `LIKE` 句を使用して、既存のデータベースを直接検索します。多くのアプリケーションにとって、これは検索を追加する最も簡単で実用的な方法であり、外部サービスや追加のインフラストラクチャは必要ありません。

データベース エンジンを使用するには、`SCOUT_DRIVER` 環境変数を `database` に設定します。

```ini
SCOUT_DRIVER=database
```

構成が完了したら、[検索可能なデータを定義する](#configuring-searchable-data) を実行し、モデルに対して [検索クエリの実行](#searching) を開始できます。サードパーティ エンジンとは異なり、データベース エンジンは個別のインデックス作成手順を必要とせず、データベース テーブルを直接検索します。

#### データベース検索戦略のカスタマイズ

デフォルトでは、データベース エンジンは、[検索可能として設定されている](#configuring-searchable-data) を持つすべてのモデル属性に対して `LIKE` クエリを実行します。ただし、より効率的な検索戦略を特定の列に割り当てることができます。 `SearchUsingFullText` 属性はその列に対してデータベースのフルテキスト インデックスを使用しますが、`SearchUsingPrefix` は文字列全体 (`%example%`) 内を検索するのではなく、文字列の先頭 (`example%`) のみに一致します。

この動作を定義するには、モデルの `toSearchableArray` メソッドに PHP 属性を割り当てます。属性のない列は、引き続きデフォルトの `LIKE` 戦略を使用します。

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

「コレクション」エンジンは、迅速なプロトタイプ、非常に小さなデータセット (数百レコード)、またはテストの実行を目的としています。データベースからすべての可能なレコードを取得し、Laravel の `Str::is` ヘルパを使用してそれらを PHP でフィルタリングするため、インデックス作成やデータベース固有の機能は必要ありません。些細な使用例を超える場合は、代わりに [データベースエンジン](#database-engine) を使用する必要があります。

収集エンジンを使用するには、単に `SCOUT_DRIVER` 環境変数の値を `collection` に設定するか、アプリケーションの `scout` 構成ファイルで `collection` ドライバを直接指定します。

```ini
SCOUT_DRIVER=collection
```

コレクション ドライバを優先ドライバとして指定したら、モデルに対して [検索クエリの実行](#searching) を開始できます。コレクション エンジンを使用する場合、Algolia、Meilisearch、または Typesense インデックスのシードに必要なインデックス作成などの検索エンジンのインデックス作成は不要です。

#### データベースエンジンとの違い

データベース エンジンはフルテキスト インデックスと `LIKE` 句を使用して一致するレコードを効率的に検索しますが、コレクション エンジンはすべてのレコードを取得し、PHP でフィルタリングします。コレクション エンジンは、Laravel でサポートされるすべてのリレーショナル データベース (SQLite および SQL Server を含む) で動作するため、最も移植性の高いオプションです。ただし、データベース エンジンよりも効率が大幅に低いため、大規模なデータセットでは使用しないでください。

<a name="third-party-engine-configuration"></a>
## サードパーティのエンジン構成 (Third-Party Engine Configuration)

次の構成オプションは、Algolia、Meilisearch、Typesense などのサードパーティの検索エンジンを使用する場合にのみ関係します。 [データベースエンジン](#database-engine) を使用している場合は、このセクションをスキップしてください。

<a name="configuring-model-indexes"></a>
### モデルインデックスの構成

サードパーティ エンジンを使用する場合、各 Eloquent モデルは、そのモデルの検索可能なすべてのレコードを含む特定の検索「インデックス」と同期されます。デフォルトでは、各モデルは、モデルの一般的な「テーブル」名に一致するインデックスに保存されます。通常、これはモデル名の複数形です。ただし、モデルの `searchableAs` メソッドをオーバーライドすることで、モデルのインデックスを自由にカスタマイズできます。

```php
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
```

> [!NOTE]
> `searchableAs` メソッドは、常にモデルのデータベース テーブルを直接検索するデータベース エンジンを使用する場合には効果がありません。

<a name="configuring-the-model-id"></a>
#### モデルIDの構成

デフォルトでは、Scout はモデルの主キーを、検索インデックスに保存されるモデルの一意の ID/キーとして使用します。サードパーティ エンジンの使用時にこの動作をカスタマイズする必要がある場合は、モデルの `getScoutKey` メソッドと `getScoutKeyName` メソッドをオーバーライドできます。

```php
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
```

> [!NOTE]
> `getScoutKey` メソッドと `getScoutKeyName` メソッドは、常にモデルの主キーを使用するデータベース エンジンを使用する場合には効果がありません。

<a name="algolia-configuration"></a>
### アルゴリア

<a name="algolia-index-settings"></a>
#### インデックス設定

Algolia インデックスに追加の設定を構成することが必要になる場合があります。これらの設定は Algolia UI を介して管理できますが、場合によっては、アプリケーションの `config/scout.php` 構成ファイルから直接、インデックス構成の望ましい状態を管理する方が効率的です。

このアプローチにより、アプリケーションの自動展開パイプラインを通じてこれらの設定を展開できるため、手動による構成が回避され、複数の環境間での一貫性が確保されます。フィルター可能な属性、ランキング、ファセット、または [その他のサポートされている設定](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings) を構成できます。

まず、アプリケーションの `config/scout.php` 構成ファイルに各インデックスの設定を追加します。

```php
use App\Models\User;
use App\Models\Flight;

'algolia' => [
    'id' => env('ALGOLIA_APP_ID', ''),
    'secret' => env('ALGOLIA_SECRET', ''),
    'index-settings' => [
        User::class => [
            'searchableAttributes' => ['id', 'name', 'email'],
            'attributesForFaceting'=> ['filterOnly(email)'],
            // Other settings fields...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

特定のインデックスの基礎となるモデルが論理的に削除可能で、`index-settings` 配列に含まれている場合、Scout はそのインデックス上の論理的に削除されたモデルのファセットのサポートを自動的に組み込みます。ソフト削除可能なモデル インデックスに対して定義する他のファセット属性がない場合は、そのモデルの `index-settings` 配列に空のエントリを追加するだけで済みます。

```php
'index-settings' => [
    Flight::class => []
],
```

アプリケーションのインデックス設定を構成した後、`scout:sync-index-settings` Artisan コマンドを呼び出す必要があります。このコマンドは、現在構成されているインデックス設定を Algolia に通知します。便宜上、このコマンドを展開プロセスの一部にするとよいでしょう。

```shell
php artisan scout:sync-index-settings
```

<a name="algolia-identifying-users"></a>
#### ユーザーの識別

Scout を使用すると、Algolia の使用時にユーザーを自動識別できます。認証されたユーザーを検索操作に関連付けると、Algolia のダッシュボード内で検索分析を表示するときに役立つ場合があります。ユーザー識別を有効にするには、アプリケーションの `.env` ファイルで `SCOUT_IDENTIFY` 環境変数を `true` として定義します。

```ini
SCOUT_IDENTIFY=true
```

この機能を有効にすると、リクエストの IP アドレスと認証されたユーザーのプライマリ識別子も Algolia に渡されるため、このデータはユーザーが行った検索リクエストに関連付けられます。

<a name="meilisearch-configuration"></a>
### メイリサーチ

<a name="meilisearch-index-settings"></a>
#### インデックス設定

Meilisearch では、フィルター可能な属性、並べ替え可能な属性、[その他のサポートされている設定フィールド](https://docs.meilisearch.com/reference/api/settings.html) などのインデックス検索設定を事前に定義する必要があります。

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

<a name="meilisearch-data-types"></a>
#### 検索可能なデータ型

Meilisearch は、正しいタイプのデータに対してフィルター操作 (`>`、`<` など) のみを実行します。検索可能なデータをカスタマイズするときは、数値が正しい型にキャストされていることを確認する必要があります。

```php
public function toSearchableArray()
{
    return [
        'id' => (int) $this->id,
        'name' => $this->name,
        'price' => (float) $this->price,
    ];
}
```

<a name="typesense-configuration"></a>
### Typesense

<a name="typesense-searchable-data"></a>
#### 検索可能なデータの準備

Typesense を利用する場合、検索可能なモデルは、モデルの主キーを文字列にキャストし、作成日を UNIX タイムスタンプにキャストする `toSearchableArray` メソッドを定義する必要があります。

```php
/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
public function toSearchableArray(): array
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

<a name="indexing"></a>
## サードパーティエンジンのインデックス作成 (Third-Party Engine Indexing)

> [!NOTE]
> このセクションで説明するインデックス作成機能は、主にサードパーティ エンジン (Algolia、Meilisearch、または Typesense) を使用する場合に関係します。データベース エンジンはデータベース テーブルを直接検索するため、手動でインデックスを管理する必要はありません。

<a name="batch-import"></a>
### バッチインポート

既存のプロジェクトに Scout をインストールする場合は、インデックスにインポートする必要があるデータベース レコードがすでに存在する可能性があります。 Scout は、既存のすべてのレコードを検索インデックスにインポートするために使用できる `scout:import` Artisan コマンドを提供します。

```shell
php artisan scout:import "App\Models\Post"
```

`scout:queue-import` コマンドを使用すると、[キューに入れられたジョブ](/docs/{{version}}/queues) を使用して既存のレコードをすべてインポートできます。

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

`flush` コマンドを使用して、モデルのすべてのレコードを検索インデックスから削除できます。

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### インポートクエリの変更

バッチインポート用にすべてのモデルを取得するために使用されるクエリを変更したい場合は、モデルに `makeAllSearchableUsing` メソッドを定義できます。ここは、モデルをインポートする前に必要となる可能性のある積極的な関係の読み込みを追加するのに最適な場所です。

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * Modify the query used to retrieve models when making all of the models searchable.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> `makeAllSearchableUsing` メソッドは、キューを使用してモデルをバッチ インポートする場合には適用できない場合があります。モデル コレクションがジョブによって処理される場合、関係は [復元されていない](/docs/{{version}}/queues#handling-relationships) になります。

<a name="adding-records"></a>
### レコードの追加

`Laravel\Scout\Searchable` トレイトをモデルに追加したら、モデル インスタンスに `save` または `create` を追加するだけで、検索インデックスに自動的に追加されます。 Scout を [キューを使用する](#queueing) に構成した場合、この操作はキューワーカーによってバックグラウンドで実行されます。

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### クエリによるレコードの追加

Eloquent クエリを介してモデルのコレクションを検索インデックスに追加したい場合は、`searchable` メソッドを Eloquent クエリにチェーンできます。 `searchable` メソッドは、クエリの [結果をチャンク化する](/docs/{{version}}/eloquent#chunking-results) を実行し、レコードを検索インデックスに追加します。繰り返しますが、キューを使用するように Scout を構成している場合、すべてのチャンクがキューワーカーによってバックグラウンドでインポートされます。

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent リレーションシップ インスタンスで `searchable` メソッドを呼び出すこともできます。

```php
$user->orders()->searchable();
```

または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `searchable` メソッドを呼び出して、モデル インスタンスを対応するインデックスに追加することもできます。

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` メソッドは、「upsert」操作とみなすことができます。つまり、モデル レコードがすでにインデックスに存在する場合、それは更新されます。検索インデックスに存在しない場合は、インデックスに追加されます。

<a name="updating-records"></a>
### 記録の更新

検索可能なモデルを更新するには、モデル インスタンスのプロパティとデータベースのモデルを `save` 更新するだけです。 Scout は、検索インデックスへの変更を自動的に永続化します。

```php
use App\Models\Order;

$order = Order::find(1);

// Update the order...

$order->save();
```

Eloquent クエリ インスタンスで `searchable` メソッドを呼び出して、モデルのコレクションを更新することもできます。モデルが検索インデックスに存在しない場合は、作成されます。

```php
Order::where('price', '>', 100)->searchable();
```

関係内のすべてのモデルの検索インデックス レコードを更新したい場合は、関係インスタンスで `searchable` を呼び出します。

```php
$user->orders()->searchable();
```

または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `searchable` メソッドを呼び出して、対応するインデックス内のモデル インスタンスを更新することもできます。

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### インポート前のレコードの変更

場合によっては、モデルのコレクションを検索可能にする前に準備する必要がある場合があります。たとえば、関係データを検索インデックスに効率的に追加できるように、関係を一括ロードすることができます。これを実現するには、対応するモデルで `makeSearchableUsing` メソッドを定義します。

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * Modify the collection of models being made searchable.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="conditionally-updating-the-search-index"></a>
#### 検索インデックスを条件付きで更新する

デフォルトでは、Scout は、どの属性が変更されたかに関係なく、更新されたモデルのインデックスを再作成します。この動作をカスタマイズしたい場合は、モデルに `searchIndexShouldBeUpdated` メソッドを定義できます。

```php
/**
 * Determine if the search index should be updated.
 */
public function searchIndexShouldBeUpdated(): bool
{
    return $this->wasRecentlyCreated || $this->wasChanged(['title', 'body']);
}
```

<a name="removing-records"></a>
### レコードの削除

インデックスからレコードを削除するには、データベースからモデルを `delete` するだけです。これは、[ソフト削除されました](/docs/{{version}}/eloquent#soft-deleting) モデルを使用している場合でも実行できます。

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

レコードを削除する前にモデルを取得したくない場合は、Eloquent クエリ インスタンスで `unsearchable` メソッドを使用できます。

```php
Order::where('price', '>', 100)->unsearchable();
```

関係内のすべてのモデルの検索インデックス レコードを削除したい場合は、関係インスタンスで `unsearchable` を呼び出します。

```php
$user->orders()->unsearchable();
```

または、メモリ内に Eloquent モデルのコレクションがすでにある場合は、コレクション インスタンスで `unsearchable` メソッドを呼び出して、対応するインデックスからモデル インスタンスを削除することもできます。

```php
$orders->unsearchable();
```

対応するインデックスからすべてのモデル レコードを削除するには、`removeAllFromSearch` メソッドを呼び出します。

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### インデックス作成の一時停止

場合によっては、モデル データを検索インデックスに同期せずに、モデルに対して Eloquent 操作のバッチを実行する必要がある場合があります。これは、`withoutSyncingToSearch` メソッドを使用して行うことができます。このメソッドは、ただちに実行される単一のクロージャを受け入れます。クロージャ内で発生するモデル操作はモデルのインデックスに同期されません。

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // Perform model actions...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 条件付きで検索可能なモデル インスタンス

場合によっては、特定の条件下でのみモデルを検索可能にすることが必要な場合があります。たとえば、「ドラフト」と「公開」の 2 つの状態のいずれかにある `App\Models\Post` モデルがあるとします。 「公開された」投稿のみを検索可能にしたい場合があります。これを実現するには、モデルに `shouldBeSearchable` メソッドを定義します。

```php
/**
 * Determine if the model should be searchable.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` メソッドは、`save` および `create` メソッド、クエリ、または関係を通じてモデルを操作する場合にのみ適用されます。 `searchable` メソッドを使用してモデルまたはコレクションを直接検索可能にすると、`shouldBeSearchable` メソッドの結果がオーバーライドされます。

> [!WARNING]
> 検索可能なすべてのデータは常にデータベースに保存されるため、Scout の「データベース」エンジンを使用する場合、`shouldBeSearchable` メソッドは適用できません。データベース エンジンを使用するときに同様の動作を実現するには、代わりに [where 句](#where-clauses) を使用する必要があります。

<a name="searching"></a>
## 検索中 (Searching)

`search` メソッドを使用してモデルの検索を開始できます。検索メソッドは、モデルの検索に使用される単一の文字列を受け入れます。次に、`get` メソッドを検索クエリに連鎖させて、指定された検索クエリに一致する Eloquent モデルを取得する必要があります。

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 検索では Eloquent モデルのコレクションが返されるため、ルートまたはコントローラから直接結果を返すこともでき、結果は自動的に JSON に変換されます。

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

Eloquent モデルに変換される前に生の検索結果を取得したい場合は、`raw` メソッドを使用できます。

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### カスタムインデックス

サードパーティ エンジンを使用して検索する場合、通常、検索クエリはモデルの [searchableAs](#configuring-model-indexes) メソッドで指定されたインデックスに対して実行されます。ただし、代わりに `within` メソッドを使用して、検索するカスタム インデックスを指定することもできます。

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where句

Scout を使用すると、検索クエリに単純な「where」句を追加できます。現在、これらの句は基本的な等価性チェックのみをサポートしており、主に所有者 ID による検索クエリのスコープ設定に役立ちます。

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

さらに、`whereIn` メソッドを使用して、指定された列の値が指定された配列内に含まれていることを確認できます。

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` メソッドは、指定された列の値が指定された配列に含まれていないことを検証します。

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

> [!WARNING]
> アプリケーションが Meil​​isearch を使用している場合は、Scout の「where」句を使用する前に、アプリケーションの [フィルタリング可能な属性](#meilisearch-index-settings) を構成する必要があります。

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

サードパーティ エンジンを使用する場合、このコールバックは関連モデルが検索エンジンからすでに取得された後に呼び出されるため、結果の「フィルタリング」には使用しないでください。代わりに [where 句を調べる](#where-clauses) を使用してください。ただし、データベース エンジンを使用する場合、`query` メソッドの制約はデータベース クエリに直接適用されるため、フィルタリングにも使用できます。

<a name="pagination"></a>
### ページネーション

モデルのコレクションを取得するだけでなく、`paginate` メソッドを使用して検索結果をページ分割することもできます。このメソッドは、[従来の Eloquent クエリのページ分割](/docs/{{version}}/pagination) がある場合と同様に、`Illuminate\Pagination\LengthAwarePaginator` インスタンスを返します。

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

`paginate` メソッドの最初の引数として量を渡すことで、ページごとに取得するモデルの数を指定できます。

```php
$orders = Order::search('Star Trek')->paginate(15);
```

データベース エンジンを使用する場合は、`simplePaginate` メソッドを使用することもできます。ページ番号を表示できるように一致するレコードの総数を取得する `paginate` とは異なり、`simplePaginate` は現在のページの先に結果があるかどうかだけを判断するため、「前」と「次」のリンクのみが必要な大規模なデータセットの場合はより効率的になります。

```php
$orders = Order::search('Star Trek')->simplePaginate(15);
```

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

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 検索エンジンは Eloquent モデルのグローバル スコープ定義を認識しないため、Scout ページネーションを利用するアプリケーションではグローバル スコープを利用しないでください。または、Scout 経由で検索するときに、グローバル スコープの制約を再作成する必要があります。

<a name="soft-deleting"></a>
### ソフト削除

インデックス付きモデルが [ソフト削除](/docs/{{version}}/eloquent#soft-deleting) で、論理的に削除されたモデルを検索する必要がある場合は、`config/scout.php` 構成ファイルの `soft_delete` オプションを `true` に設定します。

```php
'soft_delete' => true,
```

この構成オプションが `true` の場合、Scout は検索インデックスから論理的に削除されたモデルを削除しません。代わりに、インデックス付きレコードに非表示の `__soft_deleted` 属性を設定します。次に、検索時に `withTrashed` メソッドまたは `onlyTrashed` メソッドを使用して、論理的に削除されたレコードを取得できます。

```php
use App\Models\Order;

// Include trashed records when retrieving results...
$orders = Order::search('Star Trek')->withTrashed()->get();

// Only include trashed records when retrieving results...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 論理的に削除されたモデルが `forceDelete` を使用して完全に削除されると、Scout はそのモデルを検索インデックスから自動的に削除します。

<a name="customizing-engine-searches"></a>
### エンジン検索のカスタマイズ

エンジンの検索動作の高度なカスタマイズを実行する必要がある場合は、`search` メソッドの 2 番目の引数としてクロージャーを渡すことができます。たとえば、このコールバックを使用して、検索クエリが Algolia に渡される前に、地理的位置データを検索オプションに追加できます。

```php
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
## カスタムエンジン (Custom Engines)

<a name="writing-the-engine"></a>
#### エンジンを書く

組み込みの Scout 検索エンジンの 1 つがニーズに合わない場合は、独自のカスタム エンジンを作成して Scout に登録できます。エンジンは `Laravel\Scout\Engines\Engine` 抽象クラスを拡張する必要があります。この抽象クラスには、カスタム エンジンが実装する必要がある 8 つのメソッドが含まれています。

```php
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

`Laravel\Scout\Engines\AlgoliaEngine` クラスでのこれらのメソッドの実装を確認すると役立つ場合があります。このクラスは、これらの各メソッドを独自のエンジンに実装する方法を学習するための良い出発点となります。

<a name="registering-the-engine"></a>
#### エンジンの登録

カスタム エンジンを作成したら、Scout エンジン マネージャーの `extend` メソッドを使用して、Scout に登録できます。 Scout のエンジン マネージャーは、Laravel サービスコンテナーから解決される場合があります。 `App\Providers\AppServiceProvider` クラスの `boot` メソッド、またはアプリケーションで使用される他のサービスプロバイダから `extend` メソッドを呼び出す必要があります。

```php
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
```

エンジンが登録されたら、アプリケーションの `config/scout.php` 構成ファイルでデフォルトの Scout `driver` として指定できます。

```php
'driver' => 'mysql',
```

