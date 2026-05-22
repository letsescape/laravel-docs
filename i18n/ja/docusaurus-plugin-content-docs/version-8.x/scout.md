# Laravel Scout (Laravel Scout)

- [Introduction](#introduction)
- [Installation](#installation)
    - [ドライバの前提条件](#driver-prerequisites)
    - [Queueing](#queueing)
- [Configuration](#configuration)
    - [モデルインデックスの構成](#configuring-model-indexes)
    - [検索可能なデータの構成](#configuring-searchable-data)
    - [モデルIDの構成](#configuring-the-model-id)
    - [ユーザーの識別](#identifying-users)
- [地域開発](#local-development)
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
- [ビルダマクロ](#builder-macros)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Scout](https://github.com/laravel/scout) は、[Eloquent モデル](/docs/{{version}}/eloquent) に全文検索を追加するためのシンプルなドライバベースのソリューションを提供します。 Scout はモデル オブザーバを使用して、検索インデックスを Eloquent レコードと自動的に同期させます。

現在、Scout には [Algolia](https://www.algolia.com/) ドライバと [MeiliSearch](https://www.meilisearch.com) ドライバが同梱されています。さらに、Scout には、ローカル開発用途向けに設計された「コレクション」ドライバが含まれており、外部の依存関係やサードパーティのサービスを必要としません。さらに、カスタム ドライバの作成は簡単で、独自の検索実装を使用して Scout を自由に拡張できます。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを介して Scout をインストールします。

    composer require laravel/scout

Scout をインストールした後、`vendor:publish` Artisan コマンドを使用して Scout 構成ファイルを公開する必要があります。このコマンドは、`scout.php` 構成ファイルをアプリケーションの `config` ディレクトリに公開します。

    php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"

最後に、検索可能にしたいモデルに `Laravel\Scout\Searchable` トレイトを追加します。このトレイトは、モデルと検索ドライバの同期を自動的に維持するモデル オブザーバを登録します。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;
    }

<a name="driver-prerequisites"></a>
### ドライバの前提条件

<a name="algolia"></a>
#### アルゴリア

Algolia ドライバを使用する場合は、`config/scout.php` 構成ファイルで Algolia `id` および `secret` 資格情報を構成する必要があります。認証情報を設定したら、Composer パッケージ マネージャーを介して Algolia PHP SDK をインストールする必要もあります。

    composer require algolia/algoliasearch-client-php

<a name="meilisearch"></a>
#### メイリサーチ

[MeiliSearch](https://www.meilisearch.com) は、非常に高速なオープンソースの検索エンジンです。 MeiliSearch をローカル マシンにインストールする方法がわからない場合は、Laravel が公式にサポートする Docker 開発環境である [Laravel Sail](/docs/{{version}}/sail#meilisearch) を使用できます。

MeiliSearch ドライバを使用する場合は、Composer パッケージ マネージャーを介して Meil​​iSearch PHP SDK をインストールする必要があります。

    composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle

次に、アプリケーションの `.env` ファイル内で、`SCOUT_DRIVER` 環境変数と Meil​​iSearch `host` および `key` 資格情報を設定します。

    SCOUT_DRIVER=meilisearch
    MEILISEARCH_HOST=http://127.0.0.1:7700
    MEILISEARCH_KEY=masterKey

MeiliSearch の詳細については、[MeiliSearch ドキュメント](https://docs.meilisearch.com/learn/getting_started/quick_start.html) を参照してください。

さらに、[バイナリ互換性に関する Meil​​iSearch のドキュメント](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch) を確認して、MeiliSearch バイナリ バージョンと互換性のある `meilisearch/meilisearch-php` のバージョンをインストールしていることを確認する必要があります。

> {note} Meil​​iSearch を利用するアプリケーションで Scout をアップグレードする場合は、常に Meil​​iSearch サービス自体に [追加の重大な変更を確認する](https://github.com/meilisearch/MeiliSearch/releases) する必要があります。

<a name="queueing"></a>
### キューイング

Scout を使用することが厳密に必須ではありませんが、ライブラリを使用する前に [キュードライバ](/docs/{{version}}/queues) を構成することを強く検討する必要があります。キューワーカーを実行すると、Scout はモデル情報を検索インデックスに同期するすべての操作をキューに入れることができるため、アプリケーションの Web インターフェイスの応答時間が大幅に向上します。

キュードライバを構成したら、`config/scout.php` 構成ファイルの `queue` オプションの値を `true` に設定します。

    'queue' => true,

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
         *
         * @return string
         */
        public function searchableAs()
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
         * @return array
         */
        public function toSearchableArray()
        {
            $array = $this->toArray();

            // Customize the data array...

            return $array;
        }
    }

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

<a name="identifying-users"></a>
### ユーザーの識別

Scout では、[Algolia](https://algolia.com) を使用するときにユーザーを自動識別することもできます。認証されたユーザーを検索操作に関連付けると、Algolia のダッシュボード内で検索分析を表示するときに役立つ場合があります。ユーザー識別を有効にするには、アプリケーションの `.env` ファイルで `SCOUT_IDENTIFY` 環境変数を `true` として定義します。

    SCOUT_IDENTIFY=true

この機能を有効にすると、リクエストの IP アドレスと認証されたユーザーのプライマリ識別子も Algolia に渡されるため、このデータはユーザーによって行われた検索リクエストに関連付けられます。

<a name="local-development"></a>
## 地域開発 (Local Development)

ローカル開発中に Algolia または Meil​​iSearch 検索エンジンを自由に使用できますが、「コレクション」エンジンから始めるほうが便利であると思われる場合があります。収集エンジンは、「where」句と既存のデータベースからの結果に対するコレクション フィルタリングを使用して、クエリに該当する検索結果を決定します。このエンジンを使用する場合、検索可能なモデルはローカル データベースから取得されるだけなので、検索可能なモデルに「インデックス」を付ける必要はありません。

収集エンジンを使用するには、単に `SCOUT_DRIVER` 環境変数の値を `collection` に設定するか、アプリケーションの `scout` 構成ファイルで `collection` ドライバを直接指定します。

```ini
SCOUT_DRIVER=collection
```

コレクション ドライバを優先ドライバとして指定したら、モデルに対して [検索クエリの実行](#searching) を開始できます。コレクション エンジンを使用する場合、Algolia インデックスや Meil​​iSearch インデックスのシードに必要なインデックス作成など、検索エンジンのインデックス作成は不要です。

<a name="indexing"></a>
## インデックス作成 (Indexing)

<a name="batch-import"></a>
### バッチインポート

既存のプロジェクトに Scout をインストールする場合は、インデックスにインポートする必要があるデータベース レコードがすでに存在する可能性があります。 Scout は、既存のすべてのレコードを検索インデックスにインポートするために使用できる `scout:import` Artisan コマンドを提供します。

    php artisan scout:import "App\Models\Post"

`flush` コマンドを使用して、モデルのすべてのレコードを検索インデックスから削除できます。

    php artisan scout:flush "App\Models\Post"

<a name="modifying-the-import-query"></a>
#### インポートクエリの変更

バッチインポート用にすべてのモデルを取得するために使用されるクエリを変更したい場合は、モデルに `makeAllSearchableUsing` メソッドを定義できます。ここは、モデルをインポートする前に必要となる可能性のある積極的な関係の読み込みを追加するのに最適な場所です。

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

> {tip} `searchable` メソッドは、「upsert」操作とみなすことができます。つまり、モデル レコードがすでにインデックスに存在する場合、それは更新されます。検索インデックスに存在しない場合は、インデックスに追加されます。

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
     *
     * @return bool
     */
    public function shouldBeSearchable()
    {
        return $this->isPublished();
    }

`shouldBeSearchable` メソッドは、`save` および `create` メソッド、クエリ、または関係を通じてモデルを操作する場合にのみ適用されます。 `searchable` メソッドを使用してモデルまたはコレクションを直接検索可能にすると、`shouldBeSearchable` メソッドの結果がオーバーライドされます。

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

`whereIn` メソッドを使用して、特定の値のセットに対して結果を制限できます。

    $orders = Order::search('Star Trek')->whereIn(
        'status', ['paid', 'open']
    )->get();

検索インデックスはリレーショナル データベースではないため、より高度な "where" 句は現在サポートされていません。

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

> {tip} `forceDelete` を使用して論理的に削除されたモデルが完全に削除されると、Scout はそのモデルを検索インデックスから自動的に削除します。

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

エンジンが登録されたら、アプリケーションの `config/scout.php` 構成ファイルでデフォルトの Scout `driver` として指定できます。

    'driver' => 'mysql',

<a name="builder-macros"></a>
## ビルダマクロ (Builder Macros)

カスタム Scout 検索ビルダ メソッドを定義したい場合は、`Laravel\Scout\Builder` クラスの `macro` メソッドを使用できます。通常、「マクロ」は [サービスプロバイダの](/docs/{{version}}/providers) `boot` メソッド内で定義する必要があります。

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

`macro` 関数は、最初の引数としてマクロ名を、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャーは、`Laravel\Scout\Builder` 実装からマクロ名を呼び出すときに実行されます。

    use App\Models\Order;

    Order::search('Star Trek')->count();

