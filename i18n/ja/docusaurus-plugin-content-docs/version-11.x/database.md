# データベース: はじめに (Database: Getting Started)

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [読み取りおよび書き込み接続](#read-and-write-connections)
- [SQLクエリの実行](#running-queries)
    - [複数のデータベース接続の使用](#using-multiple-database-connections)
    - [クエリイベントのリスニング](#listening-for-query-events)
    - [累積クエリ時間の監視](#monitoring-cumulative-query-time)
- [データベーストランザクション](#database-transactions)
- [データベース CLI への接続](#connecting-to-the-database-cli)
- [データベースを検査する](#inspecting-your-databases)
- [データベースの監視](#monitoring-your-databases)

<a name="introduction"></a>
## 導入 (Introduction)

ほとんどすべての最新の Web アプリケーションはデータベースと対話します。 Laravel では、生の SQL、[流暢なクエリビルダ](/docs/{{version}}/queries)、および [Eloquent ORM](/docs/{{version}}/eloquent) を使用して、サポートされているさまざまなデータベース間でデータベースとの対話を非常に簡単にします。現在、Laravel は次の 5 つのデータベースのファーストパーティ サポートを提供しています。

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([バージョンポリシー](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([バージョンポリシー](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([バージョンポリシー](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([バージョンポリシー](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

さらに、MongoDB は、MongoDB によって公式に保守されている `mongodb/laravel-mongodb` パッケージを通じてサポートされています。詳細については、[Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) のドキュメントを参照してください。

<a name="configuration"></a>
### 構成

Laravel のデータベース サービスの設定は、アプリケーションの `config/database.php` 設定ファイルにあります。このファイルでは、すべてのデータベース接続を定義したり、デフォルトで使用する接続を指定したりできます。このファイル内の構成オプションのほとんどは、アプリケーションの環境変数の値によって決まります。 Laravel でサポートされているほとんどのデータベース システムの例は、このファイルで提供されています。

デフォルトでは、Laravel のサンプル [環境設定](/docs/{{version}}/configuration#environment-configuration) は、ローカル マシン上で Laravel アプリケーションを開発するための Docker 構成である [Laravel Sail](/docs/{{version}}/sail) で使用する準備ができています。ただし、ローカル データベースの必要に応じてデータベース構成を自由に変更できます。

<a name="sqlite-configuration"></a>
#### SQLiteの構成

SQLite データベースは、ファイル システム上の単一のファイル内に含まれています。ターミナルで `touch` コマンド `touch database/database.sqlite` を使用して、新しい SQLite データベースを作成できます。データベースの作成後、`DB_DATABASE` 環境変数にデータベースへの絶対パスを指定することで、このデータベースを指すように環境変数を簡単に構成できます。

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

デフォルトでは、SQLite 接続に対して外部キー制約が有効になっています。それらを無効にしたい場合は、`DB_FOREIGN_KEYS` 環境変数を `false` に設定する必要があります。

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]  
> [Laravelインストーラー](/docs/{{version}}/installation#creating-a-laravel-project) を使用して Laravel アプリケーションを作成し、データベースとして SQLite を選択した場合、Laravel は自動的に `database/database.sqlite` ファイルを作成し、デフォルトの [データベースの移行](/docs/{{version}}/migrations) を実行します。

<a name="mssql-configuration"></a>
#### Microsoft SQLサーバーの構成

Microsoft SQL Server データベースを使用するには、`sqlsrv` および `pdo_sqlsrv` PHP 拡張機能と、Microsoft SQL ODBC ドライバなどの必要な依存関係がインストールされていることを確認する必要があります。

<a name="configuration-using-urls"></a>
#### URLを使用した設定

通常、データベース接続は、`host`、`database`、`username`、`password` などの複数の構成値を使用して構成されます。これらの各構成値には、対応する独自の環境変数があります。つまり、運用サーバーでデータベース接続情報を構成する場合は、いくつかの環境変数を管理する必要があります。

AWS や Heroku などの一部のマネージド データベース プロバイダは、データベースのすべての接続情報を単一の文字列に含む単一のデータベース "URL" を提供します。データベース URL の例は次のようになります。

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

これらの URL は通常、標準のスキーマ規則に従っています。

```html
driver://username:password@host:port/database?options
```

便宜上、Laravel は複数の構成オプションを使用してデータベースを構成する代わりに、これらの URL をサポートしています。 `url` (または対応する `DB_URL` 環境変数) 構成オプションが存在する場合、データベース接続と資格情報の抽出に使用されます。

<a name="read-and-write-connections"></a>
### 読み取りおよび書き込み接続

場合によっては、あるデータベース接続を SELECT ステートメントに使用し、別のデータベース接続を INSERT、UPDATE、および DELETE ステートメントに使用したい場合があります。 Laravel を使用するとこれが簡単になり、生のクエリ、クエリビルダ、または Eloquent ORM を使用しているかどうかに関係なく、常に適切な接続が使用されます。

読み取り/書き込み接続をどのように構成する必要があるかを確認するには、次の例を見てみましょう。

    'mysql' => [
        'read' => [
            'host' => [
                '192.168.1.1',
                '196.168.1.2',
            ],
        ],
        'write' => [
            'host' => [
                '196.168.1.3',
            ],
        ],
        'sticky' => true,

        'database' => env('DB_DATABASE', 'laravel'),
        'username' => env('DB_USERNAME', 'root'),
        'password' => env('DB_PASSWORD', ''),
        'unix_socket' => env('DB_SOCKET', ''),
        'charset' => env('DB_CHARSET', 'utf8mb4'),
        'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),
        'prefix' => '',
        'prefix_indexes' => true,
        'strict' => true,
        'engine' => null,
        'options' => extension_loaded('pdo_mysql') ? array_filter([
            PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
        ]) : [],
    ],

3 つのキー (`read`、`write`、および `sticky`) が構成配列に追加されていることに注意してください。 `read` キーと `write` キーには、単一のキー `host` を含む配列値があります。 `read` および `write` 接続の残りのデータベース オプションは、メインの `mysql` 構成配列からマージされます。

メインの `mysql` 配列の値をオーバーライドする場合は、`read` 配列と `write` 配列に項目を配置するだけで済みます。したがって、この場合、`192.168.1.1` は「読み取り」接続のホストとして使用され、`192.168.1.3` は「書き込み」接続に使用されます。メインの `mysql` 配列内のデータベース資格情報、プレフィックス、文字セット、およびその他のすべてのオプションは、両方の接続間で共有されます。 `host` 構成配列に複数の値が存在する場合、リクエストごとにデータベース ホストがランダムに選択されます。

<a name="the-sticky-option"></a>
#### `sticky` オプション

`sticky` オプションは、現在のリクエスト サイクル中にデータベースに書き込まれたレコードの即時読み取りを許可するために使用できる *オプション* の値です。 `sticky` オプションが有効で、現在のリクエスト サイクル中にデータベースに対して「書き込み」操作が実行された場合、それ以降の「読み取り」操作では「書き込み」接続が使用されます。これにより、リクエスト サイクル中に書き込まれたデータは、同じリクエスト中にデータベースから即座に読み戻されることが保証されます。これがアプリケーションにとって望ましい動作であるかどうかを判断するのはあなた次第です。

<a name="running-queries"></a>
## SQLクエリの実行 (Running SQL Queries)

データベース接続を構成したら、`DB` ファサードを使用してクエリを実行できます。 `DB` ファサードは、`select`、`update`、`insert`、`delete`、および `statement` の各タイプのクエリのメソッドを提供します。

<a name="running-a-select-query"></a>
#### 選択クエリの実行

基本的な SELECT クエリを実行するには、`DB` ファサードで `select` メソッドを使用できます。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * Show a list of all of the application's users.
         */
        public function index(): View
        {
            $users = DB::select('select * from users where active = ?', [1]);

            return view('user.index', ['users' => $users]);
        }
    }

`select` メソッドに渡される最初の引数は SQL クエリで、2 番目の引数はクエリにバインドする必要があるパラメータ バインディングです。通常、これらは `where` 句制約の値です。パラメーター バインディングにより、SQL インジェクションに対する保護が提供されます。

`select` メソッドは常に `array` の結果を返します。配列内の各結果は、データベースからのレコードを表す PHP `stdClass` オブジェクトになります。

    use Illuminate\Support\Facades\DB;

    $users = DB::select('select * from users');

    foreach ($users as $user) {
        echo $user->name;
    }

<a name="selecting-scalar-values"></a>
#### スカラー値の選択

場合によっては、データベース クエリの結果が単一のスカラー値になることがあります。 Laravel では、レコード オブジェクトからクエリのスカラー結果を取得する必要があるのではなく、`scalar` メソッドを使用してこの値を直接取得できます。

    $burgers = DB::scalar(
        "select count(case when food = 'burger' then 1 end) as burgers from menu"
    );

<a name="selecting-multiple-result-sets"></a>
#### 複数の結果セットの選択

アプリケーションが複数の結果セットを返すストアド プロシージャを呼び出す場合、`selectResultSets` メソッドを使用して、ストアド プロシージャによって返されるすべての結果セットを取得できます。

    [$options, $notifications] = DB::selectResultSets(
        "CALL get_user_options_and_notifications(?)", $request->user()->id
    );

<a name="using-named-bindings"></a>
#### 名前付きバインディングの使用

`?` を使用してパラメーター バインディングを表す代わりに、名前付きバインディングを使用してクエリを実行できます。

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

<a name="running-an-insert-statement"></a>
#### Insert ステートメントの実行

`insert` ステートメントを実行するには、`DB` ファサードで `insert` メソッドを使用できます。 `select` と同様、このメソッドは SQL クエリを最初の引数として受け入れ、バインディングを 2 番目の引数として受け入れます。

    use Illuminate\Support\Facades\DB;

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);

<a name="running-an-update-statement"></a>
#### Update ステートメントの実行

データベース内の既存のレコードを更新するには、`update` メソッドを使用する必要があります。ステートメントによって影響を受ける行の数は、次のメソッドによって返されます。

    use Illuminate\Support\Facades\DB;

    $affected = DB::update(
        'update users set votes = 100 where name = ?',
        ['Anita']
    );

<a name="running-a-delete-statement"></a>
#### 削除ステートメントの実行

データベースからレコードを削除するには、`delete` メソッドを使用する必要があります。 `update` と同様に、影響を受ける行数が次のメソッドによって返されます。

    use Illuminate\Support\Facades\DB;

    $deleted = DB::delete('delete from users');

<a name="running-a-general-statement"></a>
#### 一般的なステートメントの実行

一部のデータベース ステートメントは値を返しません。これらのタイプの操作の場合、`DB` ファサードで `statement` メソッドを使用できます。

    DB::statement('drop table users');

<a name="running-an-unprepared-statement"></a>
#### 準備されていないステートメントの実行

値をバインドせずに SQL ステートメントを実行したい場合があります。これを実現するには、`DB` ファサードの `unprepared` メソッドを使用できます。

    DB::unprepared('update users set votes = 100 where name = "Dries"');

> [!WARNING]  
> 準備されていないステートメントはパラメーターをバインドしないため、SQL インジェクションに対して脆弱になる可能性があります。準備されていないステートメント内でユーザー制御の値を許可しないでください。

<a name="implicit-commits-in-transactions"></a>
#### 暗黙的なコミット

トランザクション内で `DB` ファサードの `statement` メソッドと `unprepared` メソッドを使用する場合は、[暗黙的なコミット](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) を引き起こすステートメントを避けるように注意する必要があります。これらのステートメントにより、データベース エンジンはトランザクション全体を間接的にコミットし、Laravel はデータベースのトランザクション レベルを認識しなくなります。このようなステートメントの例は、データベース テーブルの作成です。

    DB::unprepared('create table a (col varchar(1) null)');

暗黙的なコミットをトリガーする [すべてのステートメントのリスト](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) については、MySQL マニュアルを参照してください。

<a name="using-multiple-database-connections"></a>
### 複数のデータベース接続の使用

アプリケーションが `config/database.php` 構成ファイルで複数の接続を定義している場合、`DB` ファサードによって提供される `connection` メソッドを介して各接続にアクセスできます。 `connection` メソッドに渡される接続名は、`config/database.php` 構成ファイルにリストされている接続、または `config` ヘルパを使用して実行時に構成された接続の 1 つに対応する必要があります。

    use Illuminate\Support\Facades\DB;

    $users = DB::connection('sqlite')->select(/* ... */);

接続インスタンスで `getPdo` メソッドを使用して、接続の生の基礎となる PDO インスタンスにアクセスできます。

    $pdo = DB::connection()->getPdo();

<a name="listening-for-query-events"></a>
### クエリイベントのリスニング

アプリケーションによって実行される SQL クエリごとに呼び出されるクロージャーを指定したい場合は、`DB` ファサードの `listen` メソッドを使用できます。このメソッドは、クエリのログ記録やデバッグに役立ちます。 [サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッドでクエリ リスナ クロージャを登録できます。

    <?php

    namespace App\Providers;

    use Illuminate\Database\Events\QueryExecuted;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         */
        public function register(): void
        {
            // ...
        }

        /**
         * Bootstrap any application services.
         */
        public function boot(): void
        {
            DB::listen(function (QueryExecuted $query) {
                // $query->sql;
                // $query->bindings;
                // $query->time;
                // $query->toRawSql();
            });
        }
    }

<a name="monitoring-cumulative-query-time"></a>
### 累積クエリ時間の監視

最新の Web アプリケーションの一般的なパフォーマンスのボトルネックは、データベースのクエリに費やす時間です。ありがたいことに、Laravel は、1 回のリクエスト中にデータベースのクエリに時間がかかりすぎる場合に、選択したクロージャまたはコールバックを呼び出すことができます。まず、クエリ時間のしきい値 (ミリ秒単位) とクロージャーを `whenQueryingForLongerThan` メソッドに指定します。このメソッドは、[サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッドで呼び出すことができます。

    <?php

    namespace App\Providers;

    use Illuminate\Database\Connection;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;
    use Illuminate\Database\Events\QueryExecuted;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         */
        public function register(): void
        {
            // ...
        }

        /**
         * Bootstrap any application services.
         */
        public function boot(): void
        {
            DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
                // Notify development team...
            });
        }
    }

<a name="database-transactions"></a>
## データベーストランザクション (Database Transactions)

`DB` ファサードによって提供される `transaction` メソッドを使用して、データベース トランザクション内で一連の操作を実行できます。トランザクション クロージャ内で例外がスローされた場合、トランザクションは自動的にロールバックされ、例外が再スローされます。クロージャが正常に実行されると、トランザクションは自動的にコミットされます。 `transaction` メソッドを使用している間は、手動でのロールバックやコミットについて心配する必要はありません。

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    });

<a name="handling-deadlocks"></a>
#### デッドロックの処理

`transaction` メソッドは、デッドロックが発生したときにトランザクションを再試行する回数を定義するオプションの 2 番目の引数を受け入れます。これらの試行がすべて完了すると、例外がスローされます。

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    }, 5);

<a name="manually-using-transactions"></a>
#### トランザクションを手動で使用する

トランザクションを手動で開始し、ロールバックとコミットを完全に制御したい場合は、`DB` ファサードによって提供される `beginTransaction` メソッドを使用できます。

    use Illuminate\Support\Facades\DB;

    DB::beginTransaction();

`rollBack` メソッドを使用してトランザクションをロールバックできます。

    DB::rollBack();

最後に、`commit` メソッドを使用してトランザクションをコミットできます。

    DB::commit();

> [!NOTE]  
> `DB` ファサードのトランザクション メソッドは、[クエリビルダ](/docs/{{version}}/queries) と [Eloquent ORM](/docs/{{version}}/eloquent) の両方のトランザクションを制御します。

<a name="connecting-to-the-database-cli"></a>
## データベース CLI への接続 (Connecting to the Database CLI)

データベースの CLI に接続したい場合は、`db` Artisan コマンドを使用できます。

```shell
php artisan db
```

必要に応じて、データベース接続名を指定して、デフォルトの接続ではないデータベース接続に接続できます。

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## データベースを検査する (Inspecting Your Databases)

`db:show` および `db:table` Artisan コマンドを使用すると、データベースとそれに関連するテーブルに関する貴重な洞察を得ることができます。データベースのサイズ、タイプ、開いている接続の数、テーブルの概要などのデータベースの概要を表示するには、`db:show` コマンドを使用します。

```shell
php artisan db:show
```

`--database` オプションを使用してコマンドにデータベース接続名を指定することで、どのデータベース接続を検査するかを指定できます。

```shell
php artisan db:show --database=pgsql
```

コマンドの出力にテーブルの行数とデータベース ビューの詳細を含めたい場合は、`--counts` オプションと `--views` オプションをそれぞれ指定できます。大規模なデータベースでは、行数の取得と詳細の表示が遅くなることがあります。

```shell
php artisan db:show --counts --views
```

さらに、次の `Schema` メソッドを使用してデータベースを検査することもできます。

    use Illuminate\Support\Facades\Schema;

    $tables = Schema::getTables();
    $views = Schema::getViews();
    $columns = Schema::getColumns('users');
    $indexes = Schema::getIndexes('users');
    $foreignKeys = Schema::getForeignKeys('users');

アプリケーションのデフォルト接続ではないデータベース接続を検査したい場合は、`connection` メソッドを使用できます。

    $columns = Schema::connection('sqlite')->getColumns('users');

<a name="table-overview"></a>
#### テーブルの概要

データベース内の個々のテーブルの概要を取得したい場合は、`db:table` Artisan コマンドを実行できます。このコマンドは、列、タイプ、属性、キー、インデックスなどのデータベース テーブルの概要を表示します。

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## データベースの監視 (Monitoring Your Databases)

`db:monitor` Artisan コマンドを使用すると、データベースが指定された数を超えるオープン接続を管理している場合に `Illuminate\Database\Events\DatabaseBusy` イベントを送出するように Laravel に指示できます。

まず、`db:monitor` コマンドを [毎分走る](/docs/{{version}}/scheduling) にスケジュールする必要があります。このコマンドは、監視するデータベース接続構成の名前と、イベントを送出する前に許容されるオープン接続の最大数を受け入れます。

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

このコマンドをスケジュールするだけでは、開いている接続の数を警告する通知をトリガーするのに十分ではありません。コマンドが、オープン接続数がしきい値を超えるデータベースを検出すると、`DatabaseBusy` イベントが送出されます。あなたまたは開発チームに通知を送信するには、アプリケーションの `AppServiceProvider` 内でこのイベントをリッスンする必要があります。

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new DatabaseApproachingMaxConnections(
                $event->connectionName,
                $event->connections
            ));
    });
}
```

