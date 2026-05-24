# データベース: 移行 (Database: Migrations)

- [Introduction](#introduction)
- [移行の生成](#generating-migrations)
    - [移行を潰す](#squashing-migrations)
- [移行構造](#migration-structure)
- [移行の実行](#running-migrations)
    - [移行のロールバック](#rolling-back-migrations)
- [Tables](#tables)
    - [テーブルの作成](#creating-tables)
    - [テーブルの更新](#updating-tables)
    - [テーブルの名前変更/削除](#renaming-and-dropping-tables)
- [Columns](#columns)
    - [列の作成](#creating-columns)
    - [利用可能な列のタイプ](#available-column-types)
    - [列修飾子](#column-modifiers)
    - [列の変更](#modifying-columns)
    - [列名の変更](#renaming-columns)
    - [列の削除](#dropping-columns)
- [Indexes](#indexes)
    - [インデックスの作成](#creating-indexes)
    - [インデックスの名前変更](#renaming-indexes)
    - [インデックスの削除](#dropping-indexes)
    - [外部キー制約](#foreign-key-constraints)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

移行はデータベースのバージョン管理のようなもので、チームがアプリケーションのデータベース スキーマ定義を定義して共有できるようにします。ソース管理から変更を取り込んだ後、ローカル データベース スキーマに列を手動で追加するようにチームメイトに指示しなければならなかった場合は、データベースの移行によって解決される問題に直面したことがあるでしょう。

Laravel `Schema` [facade](/docs/{{version}}/facades) は、Laravel でサポートされているすべてのデータベース システムにわたってテーブルを作成および操作するためのデータベースに依存しないサポートを提供します。通常、移行ではこのファサードを使用してデータベースのテーブルと列を作成および変更します。

<a name="generating-migrations"></a>
## 移行の生成 (Generating Migrations)

`make:migration` [Artisan コマンド](/docs/{{version}}/artisan) を使用してデータベース移行を生成できます。新しい移行は、`database/migrations` ディレクトリに配置されます。各移行ファイル名には、Laravel が移行の順序を決定できるようにするタイムスタンプが含まれています。

```shell
php artisan make:migration create_flights_table
```

Laravel は移行の名前を使用して、テーブルの名前と、移行によって新しいテーブルが作成されるかどうかを推測しようとします。 Laravel が移行名からテーブル名を決定できる場合、Laravel は生成された移行ファイルに指定されたテーブルを事前に入力します。それ以外の場合は、移行ファイルにテーブルを手動で指定するだけです。

生成された移行のカスタム パスを指定したい場合は、`make:migration` コマンドを実行するときに `--path` オプションを使用できます。指定されたパスは、アプリケーションのベース パスに対する相対パスである必要があります。

> **注記**
> 移行スタブは、[スタブ発行](/docs/{{version}}/artisan#stub-customization) を使用してカスタマイズできます。

<a name="squashing-migrations"></a>
### 移行を潰す

アプリケーションを構築すると、時間の経過とともにさらに多くの移行が蓄積される可能性があります。これにより、数百もの移行が行われる可能性があり、`database/migrations` ディレクトリが肥大化する可能性があります。必要に応じて、移行を単一の SQL ファイルに「圧縮」することもできます。まず、`schema:dump` コマンドを実行します。

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

このコマンドを実行すると、Laravel はアプリケーションの `database/schema` ディレクトリに「スキーマ」ファイルを書き込みます。スキーマ ファイルの名前はデータベース接続に対応します。ここで、他の移行が実行されていないときにデータベースを移行しようとすると、Laravel は、使用しているデータベース接続のスキーマ ファイルの SQL ステートメントを最初に実行します。スキーマファイルのステートメントを実行した後、Laravel はスキーマダンプの一部ではなかった残りの移行を実行します。

アプリケーションのテストでローカル開発中に通常使用するデータベース接続とは異なるデータベース接続を使用する場合は、テストでデータベースを構築できるように、そのデータベース接続を使用してスキーマ ファイルをダンプしていることを確認する必要があります。ローカル開発中に通常使用するデータベース接続をダンプした後でこれを実行するとよいでしょう。

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

チームの他の新しい開発者がアプリケーションの初期データベース構造を迅速に作成できるように、データベース スキーマ ファイルをソース管理にコミットする必要があります。

> **警告**
> 移行スカッシングは、MySQL、PostgreSQL、および SQLite データベースでのみ利用可能であり、データベースのコマンドライン クライアントを利用します。スキーマ ダンプはインメモリ SQLite データベースに復元できない場合があります。

<a name="migration-structure"></a>
## 移行構造 (Migration Structure)

移行クラスには、`up` と `down` の 2 つのメソッドが含まれています。 `up` メソッドは、新しいテーブル、列、またはインデックスをデータベースに追加するために使用されますが、`down` メソッドは、`up` メソッドによって実行された操作を元に戻す必要があります。

これらの両方のメソッド内で、Laravel スキーマ ビルダを使用して、テーブルを表現的に作成および変更できます。 `Schema` ビルダ、[ドキュメントを確認してください](#creating-tables) で使用できるすべてのメソッドについて学習するには。たとえば、次の移行では `flights` テーブルが作成されます。

    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    return new class extends Migration
    {
        /**
         * Run the migrations.
         *
         * @return void
         */
        public function up()
        {
            Schema::create('flights', function (Blueprint $table) {
                $table->id();
                $table->string('name');
                $table->string('airline');
                $table->timestamps();
            });
        }

        /**
         * Reverse the migrations.
         *
         * @return void
         */
        public function down()
        {
            Schema::drop('flights');
        }
    };

<a name="setting-the-migration-connection"></a>
#### 移行接続の設定

移行がアプリケーションのデフォルトのデータベース接続以外のデータベース接続と対話する場合は、移行の `$connection` プロパティを設定する必要があります。

    /**
     * The database connection that should be used by the migration.
     *
     * @var string
     */
    protected $connection = 'pgsql';

    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        //
    }

<a name="running-migrations"></a>
## 移行の実行 (Running Migrations)

未処理の移行をすべて実行するには、`migrate` Artisan コマンドを実行します。

```shell
php artisan migrate
```

これまでにどの移行が実行されたかを確認したい場合は、`migrate:status` Artisan コマンドを使用できます。

```shell
php artisan migrate:status
```

移行によって実行される SQL ステートメントを実際に実行せずに確認したい場合は、`--pretend` フラグを `migrate` コマンドに指定できます。

```shell
php artisan migrate --pretend
```

#### 移行実行の分離

アプリケーションを複数のサーバーにデプロイし、デプロイメント プロセスの一環として移行を実行している場合、2 つのサーバーが同時にデータベースを移行しようとすることは望ましくありません。これを回避するには、`migrate` コマンドを呼び出すときに `isolated` オプションを使用できます。

`isolated` オプションが指定されている場合、Laravel は移行の実行を試行する前に、アプリケーションのキャッシュドライバを使用してアトミックロックを取得します。ロックが保持されている間に `migrate` コマンドを実行しようとする他の試みはすべて実行されません。ただし、コマンドは引き続き正常終了ステータス コードで終了します。

```shell
php artisan migrate --isolated
```

> **警告**
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<a name="forcing-migrations-to-run-in-production"></a>
#### 本番環境での強制的な移行の実行

一部の移行操作は破壊的なものであり、データが失われる可能性があります。運用データベースに対してこれらのコマンドを実行しないようにするために、コマンドを実行する前に確認を求めるメッセージが表示されます。プロンプトを表示せずにコマンドを強制的に実行するには、`--force` フラグを使用します。

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 移行のロールバック

最新の移行操作をロールバックするには、`rollback` Artisan コマンドを使用できます。このコマンドは、移行の最後の「バッチ」をロールバックします。これには複数の移行ファイルが含まれる場合があります。

```shell
php artisan migrate:rollback
```

`step` オプションを `rollback` コマンドに指定すると、限られた数の移行をロールバックできます。たとえば、次のコマンドは最後の 5 つの移行をロールバックします。

```shell
php artisan migrate:rollback --step=5
```

`migrate:reset` コマンドは、アプリケーションのすべての移行をロールバックします。

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 単一のコマンドを使用したロールバックと移行

`migrate:refresh` コマンドは、すべての移行をロールバックしてから、`migrate` コマンドを実行します。このコマンドはデータベース全体を効果的に再作成します。

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

`refresh` コマンドに `step` オプションを指定すると、限られた数の移行をロールバックして再移行できます。たとえば、次のコマンドは、最後の 5 つの移行をロールバックして再移行します。

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### すべてのテーブルを削除して移行する

`migrate:fresh` コマンドは、データベースからすべてのテーブルを削除してから、`migrate` コマンドを実行します。

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

> **警告**
> `migrate:fresh` コマンドは、プレフィックスに関係なく、すべてのデータベース テーブルを削除します。他のアプリケーションと共有されるデータベース上で開発する場合、このコマンドは注意して使用する必要があります。

<a name="tables"></a>
## テーブル (Tables)

<a name="creating-tables"></a>
### テーブルの作成

新しいデータベース テーブルを作成するには、`Schema` ファサードで `create` メソッドを使用します。 `create` メソッドは 2 つの引数を受け入れます。1 つ目はテーブルの名前で、2 つ目は新しいテーブルの定義に使用できる `Blueprint` オブジェクトを受け取るクロージャです。

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::create('users', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->string('email');
        $table->timestamps();
    });

テーブルを作成するときは、スキーマ ビルダの [列メソッド](#creating-columns) のいずれかを使用してテーブルの列を定義できます。

<a name="checking-for-table-column-existence"></a>
#### テーブル/カラムの存在を確認する

`hasTable` および `hasColumn` メソッドを使用して、テーブルまたは列の存在を確認できます。

    if (Schema::hasTable('users')) {
        // The "users" table exists...
    }

    if (Schema::hasColumn('users', 'email')) {
        // The "users" table exists and has an "email" column...
    }

<a name="database-connection-table-options"></a>
#### データベース接続とテーブルのオプション

アプリケーションのデフォルト接続ではないデータベース接続でスキーマ操作を実行する場合は、`connection` メソッドを使用します。

    Schema::connection('sqlite')->create('users', function (Blueprint $table) {
        $table->id();
    });

さらに、他のいくつかのプロパティとメソッドを使用して、テーブル作成の他の側面を定義することもできます。 `engine` プロパティは、MySQL の使用時にテーブルのストレージ エンジンを指定するために使用できます。

    Schema::create('users', function (Blueprint $table) {
        $table->engine = 'InnoDB';

        // ...
    });

`charset` プロパティと `collation` プロパティは、MySQL の使用時に作成されるテーブルの文字セットと照合順序を指定するために使用できます。

    Schema::create('users', function (Blueprint $table) {
        $table->charset = 'utf8mb4';
        $table->collation = 'utf8mb4_unicode_ci';

        // ...
    });

`temporary` メソッドを使用して、テーブルを「一時的」にする必要があることを示すことができます。一時テーブルは現在の接続のデータベース セッションにのみ表示され、接続が閉じられると自動的に削除されます。

    Schema::create('calculations', function (Blueprint $table) {
        $table->temporary();

        // ...
    });

データベース テーブルに「コメント」を追加したい場合は、テーブル インスタンスで `comment` メソッドを呼び出します。テーブル コメントは現在、MySQL と Postgres でのみサポートされています。

    Schema::create('calculations', function (Blueprint $table) {
        $table->comment('Business calculations');

        // ...
    });

<a name="updating-tables"></a>
### テーブルの更新

`Schema` ファサードの `table` メソッドを使用して、既存のテーブルを更新できます。 `create` メソッドと同様に、`table` メソッドは 2 つの引数を受け入れます。テーブルの名前と、テーブルに列またはインデックスを追加するために使用できる `Blueprint` インスタンスを受け取るクロージャです。

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="renaming-and-dropping-tables"></a>
### テーブルの名前変更/削除

既存のデータベーステーブルの名前を変更するには、`rename` メソッドを使用します。

    use Illuminate\Support\Facades\Schema;

    Schema::rename($from, $to);

既存のテーブルを削除するには、`drop` メソッドまたは `dropIfExists` メソッドを使用できます。

    Schema::drop('users');

    Schema::dropIfExists('users');

<a name="renaming-tables-with-foreign-keys"></a>
#### 外部キーを使用したテーブルの名前変更

テーブルの名前を変更する前に、Laravel に規則に基づいた名前を割り当てるのではなく、テーブルの外部キー制約に明示的な名前が移行ファイルに含まれていることを確認する必要があります。それ以外の場合、外部キー制約名は古いテーブル名を参照します。

<a name="columns"></a>
## コラム (Columns)

<a name="creating-columns"></a>
### 列の作成

`Schema` ファサードの `table` メソッドを使用して、既存のテーブルを更新できます。 `create` メソッドと同様に、`table` メソッドは 2 つの引数を受け入れます。テーブルの名前と、テーブルに列を追加するために使用できる `Illuminate\Database\Schema\Blueprint` インスタンスを受け取るクロージャです。

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="available-column-types"></a>
### 利用可能な列のタイプ

スキーマ ビルダ ブループリントは、データベース テーブルに追加できるさまざまな種類の列に対応するさまざまなメソッドを提供します。使用可能な各メソッドを次の表に示します。

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<div class="collection-method-list" markdown="1">

[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[binary](#column-method-binary)
[boolean](#column-method-boolean)
[char](#column-method-char)
[dateTimeTz](#column-method-dateTimeTz)
[dateTime](#column-method-dateTime)
[date](#column-method-date)
[decimal](#column-method-decimal)
[double](#column-method-double)
[enum](#column-method-enum)
[float](#column-method-float)
[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[geometryCollection](#column-method-geometryCollection)
[geometry](#column-method-geometry)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[ipAddress](#column-method-ipAddress)
[json](#column-method-json)
[jsonb](#column-method-jsonb)
[lineString](#column-method-lineString)
[longText](#column-method-longText)
[macAddress](#column-method-macAddress)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[mediumText](#column-method-mediumText)
[morphs](#column-method-morphs)
[multiLineString](#column-method-multiLineString)
[multiPoint](#column-method-multiPoint)
[multiPolygon](#column-method-multiPolygon)
[nullableMorphs](#column-method-nullableMorphs)
[nullableTimestamps](#column-method-nullableTimestamps)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)
[point](#column-method-point)
[polygon](#column-method-polygon)
[rememberToken](#column-method-rememberToken)
[set](#column-method-set)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[softDeletesTz](#column-method-softDeletesTz)
[softDeletes](#column-method-softDeletes)
[string](#column-method-string)
[text](#column-method-text)
[timeTz](#column-method-timeTz)
[time](#column-method-time)
[timestampTz](#column-method-timestampTz)
[timestamp](#column-method-timestamp)
[timestampsTz](#column-method-timestampsTz)
[timestamps](#column-method-timestamps)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[tinyText](#column-method-tinyText)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedDecimal](#column-method-unsignedDecimal)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)
[ulidMorphs](#column-method-ulidMorphs)
[uuidMorphs](#column-method-uuidMorphs)
[ulid](#column-method-ulid)
[uuid](#column-method-uuid)
[year](#column-method-year)

</div>

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()` {.collection-method .first-collection-method}

`bigIncrements` メソッドは、自動インクリメントする `UNSIGNED BIGINT` (主キー) と同等の列を作成します。

    $table->bigIncrements('id');

<a name="column-method-bigInteger"></a>
#### `bigInteger()` {.collection-method}

`bigInteger` メソッドは、`BIGINT` と同等の列を作成します。

    $table->bigInteger('votes');

<a name="column-method-binary"></a>
#### `binary()` {.collection-method}

`binary` メソッドは、`BLOB` と同等の列を作成します。

    $table->binary('photo');

<a name="column-method-boolean"></a>
#### `boolean()` {.collection-method}

`boolean` メソッドは、`BOOLEAN` と同等の列を作成します。

    $table->boolean('confirmed');

<a name="column-method-char"></a>
#### `char()` {.collection-method}

`char` メソッドは、指定された長さの `CHAR` と同等の列を作成します。

    $table->char('name', 100);

<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()` {.collection-method}

`dateTimeTz` メソッドは、オプションの精度 (合計桁数) を使用して、`DATETIME` (タイムゾーンあり) と同等の列を作成します。

    $table->dateTimeTz('created_at', $precision = 0);

<a name="column-method-dateTime"></a>
#### `dateTime()` {.collection-method}

`dateTime` メソッドは、オプションの精度 (合計桁数) を使用して、`DATETIME` と同等の列を作成します。

    $table->dateTime('created_at', $precision = 0);

<a name="column-method-date"></a>
#### `date()` {.collection-method}

`date` メソッドは、`DATE` と同等の列を作成します。

    $table->date('created_at');

<a name="column-method-decimal"></a>
#### `decimal()` {.collection-method}

`decimal` メソッドは、指定された精度 (合計桁数) と位取り (10 進数の桁数) を持つ `DECIMAL` と同等の列を作成します。

    $table->decimal('amount', $precision = 8, $scale = 2);

<a name="column-method-double"></a>
#### `double()` {.collection-method}

`double` メソッドは、指定された精度 (合計桁数) と位取り (10 進数の桁数) を持つ `DOUBLE` と同等の列を作成します。

    $table->double('amount', 8, 2);

<a name="column-method-enum"></a>
#### `enum()` {.collection-method}

`enum` メソッドは、指定された有効な値を使用して `ENUM` と同等の列を作成します。

    $table->enum('difficulty', ['easy', 'hard']);

<a name="column-method-float"></a>
#### `float()` {.collection-method}

`float` メソッドは、指定された精度 (合計桁数) と位取り (10 進数の桁数) を持つ `FLOAT` と同等の列を作成します。

    $table->float('amount', 8, 2);

<a name="column-method-foreignId"></a>
#### `foreignId()` {.collection-method}

`foreignId` メソッドは、`UNSIGNED BIGINT` と同等の列を作成します。

    $table->foreignId('user_id');

<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()` {.collection-method}

`foreignIdFor` メソッドは、指定されたモデル クラスに `{column}_id UNSIGNED BIGINT` と同等の列を追加します。

    $table->foreignIdFor(User::class);

<a name="column-method-foreignUlid"></a>
#### `foreignUlid()` {.collection-method}

`foreignUlid` メソッドは、`ULID` と同等の列を作成します。

    $table->foreignUlid('user_id');

<a name="column-method-foreignUuid"></a>
#### `foreignUuid()` {.collection-method}

`foreignUuid` メソッドは、`UUID` と同等の列を作成します。

    $table->foreignUuid('user_id');

<a name="column-method-geometryCollection"></a>
#### `geometryCollection()` {.collection-method}

`geometryCollection` メソッドは、`GEOMETRYCOLLECTION` と同等の列を作成します。

    $table->geometryCollection('positions');

<a name="column-method-geometry"></a>
#### `geometry()` {.collection-method}

`geometry` メソッドは、`GEOMETRY` と同等の列を作成します。

    $table->geometry('positions');

<a name="column-method-id"></a>
#### `id()` {.collection-method}

`id` メソッドは、`bigIncrements` メソッドのエイリアスです。デフォルトでは、このメソッドは `id` 列を作成します。ただし、列に別の名前を割り当てたい場合は、列名を渡すことができます。

    $table->id();

<a name="column-method-increments"></a>
#### `increments()` {.collection-method}

`increments` メソッドは、自動インクリメントする `UNSIGNED INTEGER` と同等の列を主キーとして作成します。

    $table->increments('id');

<a name="column-method-integer"></a>
#### `integer()` {.collection-method}

`integer` メソッドは、`INTEGER` と同等の列を作成します。

    $table->integer('votes');

<a name="column-method-ipAddress"></a>
#### `ipAddress()` {.collection-method}

`ipAddress` メソッドは、`VARCHAR` と同等の列を作成します。

    $table->ipAddress('visitor');

<a name="column-method-json"></a>
#### `json()` {.collection-method}

`json` メソッドは、`JSON` と同等の列を作成します。

    $table->json('options');

<a name="column-method-jsonb"></a>
#### `jsonb()` {.collection-method}

`jsonb` メソッドは、`JSONB` と同等の列を作成します。

    $table->jsonb('options');

<a name="column-method-lineString"></a>
#### `lineString()` {.collection-method}

`lineString` メソッドは、`LINESTRING` と同等の列を作成します。

    $table->lineString('positions');

<a name="column-method-longText"></a>
#### `longText()` {.collection-method}

`longText` メソッドは、`LONGTEXT` と同等の列を作成します。

    $table->longText('description');

<a name="column-method-macAddress"></a>
#### `macAddress()` {.collection-method}

`macAddress` メソッドは、MAC アドレスを保持するための列を作成します。 PostgreSQL などの一部のデータベース システムには、このタイプのデータ専用の列タイプがあります。他のデータベース システムでは、文字列と同等の列が使用されます。

    $table->macAddress('device');

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()` {.collection-method}

`mediumIncrements` メソッドは、自動インクリメントする `UNSIGNED MEDIUMINT` と同等の列を主キーとして作成します。

    $table->mediumIncrements('id');

<a name="column-method-mediumInteger"></a>
#### `mediumInteger()` {.collection-method}

`mediumInteger` メソッドは、`MEDIUMINT` と同等の列を作成します。

    $table->mediumInteger('votes');

<a name="column-method-mediumText"></a>
#### `mediumText()` {.collection-method}

`mediumText` メソッドは、`MEDIUMTEXT` と同等の列を作成します。

    $table->mediumText('description');

<a name="column-method-morphs"></a>
#### `morphs()` {.collection-method}

`morphs` メソッドは、`{column}_id` `UNSIGNED BIGINT` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

このメソッドは、多態性 [Eloquent リレーション](/docs/{{version}}/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

    $table->morphs('taggable');

<a name="column-method-multiLineString"></a>
#### `multiLineString()` {.collection-method}

`multiLineString` メソッドは、`MULTILINESTRING` と同等の列を作成します。

    $table->multiLineString('positions');

<a name="column-method-multiPoint"></a>
#### `multiPoint()` {.collection-method}

`multiPoint` メソッドは、`MULTIPOINT` と同等の列を作成します。

    $table->multiPoint('positions');

<a name="column-method-multiPolygon"></a>
#### `multiPolygon()` {.collection-method}

`multiPolygon` メソッドは、`MULTIPOLYGON` と同等の列を作成します。

    $table->multiPolygon('positions');

<a name="column-method-nullableTimestamps"></a>
#### `nullableTimestamps()` {.collection-method}

`nullableTimestamps` メソッドは、[timestamps](#column-method-timestamps) メソッドのエイリアスです。

    $table->nullableTimestamps(0);

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()` {.collection-method}

このメソッドは [morphs](#column-method-morphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

    $table->nullableMorphs('taggable');

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()` {.collection-method}

このメソッドは [ulidMorphs](#column-method-ulidMorphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

    $table->nullableUlidMorphs('taggable');

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()` {.collection-method}

このメソッドは [uuidMorphs](#column-method-uuidMorphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

    $table->nullableUuidMorphs('taggable');

<a name="column-method-point"></a>
#### `point()` {.collection-method}

`point` メソッドは、`POINT` と同等の列を作成します。

    $table->point('position');

<a name="column-method-polygon"></a>
#### `polygon()` {.collection-method}

`polygon` メソッドは、`POLYGON` と同等の列を作成します。

    $table->polygon('position');

<a name="column-method-rememberToken"></a>
#### `rememberToken()` {.collection-method}

`rememberToken` メソッドは、現在の「remember me」 [認証トークン](/docs/{{version}}/authentication#remembering-users) を格納するための、null 許容の `VARCHAR(100)` と同等の列を作成します。

    $table->rememberToken();

<a name="column-method-set"></a>
#### `set()` {.collection-method}

`set` メソッドは、指定された有効な値のリストを使用して、`SET` と同等の列を作成します。

    $table->set('flavors', ['strawberry', 'vanilla']);

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()` {.collection-method}

`smallIncrements` メソッドは、自動インクリメントする `UNSIGNED SMALLINT` と同等の列を主キーとして作成します。

    $table->smallIncrements('id');

<a name="column-method-smallInteger"></a>
#### `smallInteger()` {.collection-method}

`smallInteger` メソッドは、`SMALLINT` と同等の列を作成します。

    $table->smallInteger('votes');

<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()` {.collection-method}

`softDeletesTz` メソッドは、オプションの精度 (合計桁数) を持つ、NULL 許容の `deleted_at` `TIMESTAMP` (タイムゾーンあり) と同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

    $table->softDeletesTz($column = 'deleted_at', $precision = 0);

<a name="column-method-softDeletes"></a>
#### `softDeletes()` {.collection-method}

`softDeletes` メソッドは、オプションの精度 (合計桁数) を持つ NULL 許容の `deleted_at` `TIMESTAMP` 同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

    $table->softDeletes($column = 'deleted_at', $precision = 0);

<a name="column-method-string"></a>
#### `string()` {.collection-method}

`string` メソッドは、指定された長さの `VARCHAR` と同等の列を作成します。

    $table->string('name', 100);

<a name="column-method-text"></a>
#### `text()` {.collection-method}

`text` メソッドは、`TEXT` と同等の列を作成します。

    $table->text('description');

<a name="column-method-timeTz"></a>
#### `timeTz()` {.collection-method}

`timeTz` メソッドは、オプションの精度 (合計桁数) を使用して、`TIME` (タイムゾーンあり) と同等の列を作成します。

    $table->timeTz('sunrise', $precision = 0);

<a name="column-method-time"></a>
#### `time()` {.collection-method}

`time` メソッドは、オプションの精度 (合計桁数) を使用して、`TIME` と同等の列を作成します。

    $table->time('sunrise', $precision = 0);

<a name="column-method-timestampTz"></a>
#### `timestampTz()` {.collection-method}

`timestampTz` メソッドは、オプションの精度 (合計桁数) を使用して、`TIMESTAMP` (タイムゾーンあり) と同等の列を作成します。

    $table->timestampTz('added_at', $precision = 0);

<a name="column-method-timestamp"></a>
#### `timestamp()` {.collection-method}

`timestamp` メソッドは、オプションの精度 (合計桁数) を使用して、`TIMESTAMP` と同等の列を作成します。

    $table->timestamp('added_at', $precision = 0);

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()` {.collection-method}

`timestampsTz` メソッドは、オプションの精度 (合計桁数) を使用して、`created_at` および `updated_at` `TIMESTAMP` (タイムゾーン付き) と同等の列を作成します。

    $table->timestampsTz($precision = 0);

<a name="column-method-timestamps"></a>
#### `timestamps()` {.collection-method}

`timestamps` メソッドは、オプションの精度 (合計桁数) で、`created_at` および `updated_at` `TIMESTAMP` と同等の列を作成します。

    $table->timestamps($precision = 0);

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()` {.collection-method}

`tinyIncrements` メソッドは、自動インクリメントする `UNSIGNED TINYINT` と同等の列を主キーとして作成します。

    $table->tinyIncrements('id');

<a name="column-method-tinyInteger"></a>
#### `tinyInteger()` {.collection-method}

`tinyInteger` メソッドは、`TINYINT` と同等の列を作成します。

    $table->tinyInteger('votes');

<a name="column-method-tinyText"></a>
#### `tinyText()` {.collection-method}

`tinyText` メソッドは、`TINYTEXT` と同等の列を作成します。

    $table->tinyText('notes');

<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()` {.collection-method}

`unsignedBigInteger` メソッドは、`UNSIGNED BIGINT` と同等の列を作成します。

    $table->unsignedBigInteger('votes');

<a name="column-method-unsignedDecimal"></a>
#### `unsignedDecimal()` {.collection-method}

`unsignedDecimal` メソッドは、オプションの精度 (合計桁数) とスケール (10 進数の桁数) を使用して、`UNSIGNED DECIMAL` と同等の列を作成します。

    $table->unsignedDecimal('amount', $precision = 8, $scale = 2);

<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()` {.collection-method}

`unsignedInteger` メソッドは、`UNSIGNED INTEGER` と同等の列を作成します。

    $table->unsignedInteger('votes');

<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()` {.collection-method}

`unsignedMediumInteger` メソッドは、`UNSIGNED MEDIUMINT` と同等の列を作成します。

    $table->unsignedMediumInteger('votes');

<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()` {.collection-method}

`unsignedSmallInteger` メソッドは、`UNSIGNED SMALLINT` と同等の列を作成します。

    $table->unsignedSmallInteger('votes');

<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()` {.collection-method}

`unsignedTinyInteger` メソッドは、`UNSIGNED TINYINT` と同等の列を作成します。

    $table->unsignedTinyInteger('votes');

<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()` {.collection-method}

`ulidMorphs` メソッドは、`{column}_id` `CHAR(26)` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

このメソッドは、ULID 識別子を使用する多態性 [Eloquent リレーション](/docs/{{version}}/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

    $table->ulidMorphs('taggable');

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()` {.collection-method}

`uuidMorphs` メソッドは、`{column}_id` `CHAR(36)` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

このメソッドは、UUID 識別子を使用する多態性 [Eloquent リレーション](/docs/{{version}}/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

    $table->uuidMorphs('taggable');

<a name="column-method-ulid"></a>
#### `ulid()` {.collection-method}

`ulid` メソッドは、`ULID` と同等の列を作成します。

    $table->ulid('id');

<a name="column-method-uuid"></a>
#### `uuid()` {.collection-method}

`uuid` メソッドは、`UUID` と同等の列を作成します。

    $table->uuid('id');

<a name="column-method-year"></a>
#### `year()` {.collection-method}

`year` メソッドは、`YEAR` と同等の列を作成します。

    $table->year('birth_year');

<a name="column-modifiers"></a>
### 列修飾子

上記の列タイプに加えて、データベース テーブルに列を追加するときに使用できる列「修飾子」がいくつかあります。たとえば、列を「NULL 可能」にするには、`nullable` メソッドを使用します。

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->nullable();
    });

次の表には、使用可能な列修飾子がすべて含まれています。このリストには、[インデックス修飾子](#creating-indexes) は含まれていません。

修飾子 |  説明
--------  |  -----------
`->after('column')` |  列を別の列の「後」に配置します (MySQL)。
`->autoIncrement()` |  INTEGER 列を自動インクリメント (主キー) として設定します。
`->charset('utf8mb4')` |  カラムの文字セットを指定します (MySQL)。
`->collation('utf8mb4_unicode_ci')` |  列の照合順序を指定します (MySQL/PostgreSQL/SQL Server)。
`->comment('my comment')` |  列にコメントを追加します (MySQL/PostgreSQL)。
`->default($value)` |  列の「デフォルト」値を指定します。
`->first()` |  テーブル (MySQL) の「最初」に列を配置します。
`->from($integer)` |  自動インクリメントフィールドの開始値を設定します (MySQL / PostgreSQL)。
`->invisible()` |  列を `SELECT *` クエリに対して「非表示」にします (MySQL)。
`->nullable($value = true)` |  NULL 値を列に挿入できるようにします。
`->storedAs($expression)` |  格納された生成列を作成します (MySQL / PostgreSQL)。
`->unsigned()` |  INTEGER 列を UNSIGNED として設定します (MySQL)。
`->useCurrent()` |  デフォルト値として CURRENT_TIMESTAMP を使用するように TIMESTAMP 列を設定します。
`->useCurrentOnUpdate()` |  レコードの更新時に CURRENT_TIMESTAMP を使用するように TIMESTAMP 列を設定します。
`->virtualAs($expression)` |  仮想生成列 (MySQL / PostgreSQL / SQLite) を作成します。
`->generatedAs($expression)` |  シーケンス オプションを指定して ID 列を作成します (PostgreSQL)。
`->always()` |  ID 列の入力に対するシーケンス値の優先順位を定義します (PostgreSQL)。
`->isGeometry()` |  空間列タイプを `geometry` に設定します。デフォルトのタイプは `geography` (PostgreSQL) です。

<a name="default-expressions"></a>
#### デフォルトの式

`default` 修飾子は、値または `Illuminate\Database\Query\Expression` インスタンスを受け入れます。 `Expression` インスタンスを使用すると、Laravel が値を引用符で囲むことがなくなり、データベース固有の関数を使用できるようになります。これが特に役立つ状況の 1 つは、JSON 列にデフォルト値を割り当てる必要がある場合です。

    <?php

    use Illuminate\Support\Facades\Schema;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Database\Query\Expression;
    use Illuminate\Database\Migrations\Migration;

    return new class extends Migration
    {
        /**
         * Run the migrations.
         *
         * @return void
         */
        public function up()
        {
            Schema::create('flights', function (Blueprint $table) {
                $table->id();
                $table->json('movies')->default(new Expression('(JSON_ARRAY())'));
                $table->timestamps();
            });
        }
    };

> **警告**
> デフォルトの式のサポートは、データベース ドライバ、データベース バージョン、およびフィールド タイプによって異なります。データベースのドキュメントを参照してください。さらに、生の `default` 式 (`DB::raw` を使用) と、`change` メソッドによる列の変更を組み合わせることはできません。

<a name="column-order"></a>
#### 列の順序

MySQL データベースを使用する場合、`after` メソッドを使用して、スキーマ内の既存の列の後に列を追加できます。

    $table->after('password', function ($table) {
        $table->string('address_line1');
        $table->string('address_line2');
        $table->string('city');
    });

<a name="modifying-columns"></a>
### 列の変更

<a name="prerequisites"></a>
#### 前提条件

列を変更する前に、Composer パッケージ マネージャーを使用して `doctrine/dbal` パッケージをインストールする必要があります。 Doctrine DBAL ライブラリは、列の現在の状態を判断し、要求された変更を列に加えるために必要な SQL クエリを作成するために使用されます。

    composer require doctrine/dbal

`timestamp` メソッドを使用して作成された列を変更する場合は、アプリケーションの `config/database.php` 構成ファイルに次の構成も追加する必要があります。

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> **警告**
> アプリケーションが Microsoft SQL Server を使用している場合は、必ず `doctrine/dbal:^3.0` をインストールしてください。

<a name="updating-column-attributes"></a>
#### 列属性の更新

`change` メソッドを使用すると、既存の列のタイプと属性を変更できます。たとえば、`string` 列のサイズを増やしたい場合があります。 `change` メソッドの動作を確認するには、`name` 列のサイズを 25 から 50 に増やしてみましょう。これを実現するには、単に列の新しい状態を定義してから、`change` メソッドを呼び出します。

    Schema::table('users', function (Blueprint $table) {
        $table->string('name', 50)->change();
    });

列を NULL 可能に変更することもできます。

    Schema::table('users', function (Blueprint $table) {
        $table->string('name', 50)->nullable()->change();
    });

> **警告**
> 次の列タイプを変更できます: `bigInteger`、`binary`、`boolean`、`char`、`date`、`dateTime`、`dateTimeTz`、`decimal`、`double`、 `integer`、`json`、`longText`、`mediumText`、`smallInteger`、`string`、`text`、`time`、`tinyText`、 `unsignedBigInteger`、`unsignedInteger`、`unsignedSmallInteger`、および `uuid`。  `timestamp` 列を変更するには、「[教義タイプを登録する必要があります](#prerequisites)」と入力します。

<a name="renaming-columns"></a>
### 列名の変更

列の名前を変更するには、スキーマ ビルダが提供する `renameColumn` メソッドを使用できます。

    Schema::table('users', function (Blueprint $table) {
        $table->renameColumn('from', 'to');
    });

<a name="renaming-columns-on-legacy-databases"></a>
#### レガシーデータベースの列名の変更

次のリリースのいずれかよりも古いデータベース インストールを実行している場合は、列の名前を変更する前に、Composer パッケージ マネージャーを介して `doctrine/dbal` ライブラリがインストールされていることを確認する必要があります。

<div class="content-list" markdown="1">

- MySQL < `8.0.3`
- マリアDB < `10.5.2`
- SQLite < `3.25.0`

</div>

<a name="dropping-columns"></a>
### 列の削除

列を削除するには、スキーマ ビルダで `dropColumn` メソッドを使用できます。

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn('votes');
    });

列名の配列を `dropColumn` メソッドに渡すことで、テーブルから複数の列を削除できます。

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn(['votes', 'avatar', 'location']);
    });


<a name="dropping-columns-on-legacy-databases"></a>
#### レガシーデータベースでの列の削除

`3.35.0` より前のバージョンの SQLite を実行している場合は、`dropColumn` メソッドを使用する前に、Composer パッケージ マネージャーを介して `doctrine/dbal` パッケージをインストールする必要があります。このパッケージの使用中に、1 回の移行内で複数の列を削除または変更することはサポートされていません。

<a name="available-command-aliases"></a>
#### 使用可能なコマンドエイリアス

Laravel は、一般的なタイプの列の削除に関連する便利なメソッドをいくつか提供しています。これらの各方法については、次の表で説明します。

コマンド |  説明
-------  |  -----------
`$table->dropMorphs('morphable');` |  `morphable_id` 列と `morphable_type` 列を削除します。
`$table->dropRememberToken();` |  `remember_token` 列を削除します。
`$table->dropSoftDeletes();` |  `deleted_at` 列を削除します。
`$table->dropSoftDeletesTz();` |  `dropSoftDeletes()` メソッドの別名。
`$table->dropTimestamps();` |  `created_at` 列と `updated_at` 列を削除します。
`$table->dropTimestampsTz();` |  `dropTimestamps()` メソッドの別名。

<a name="indexes"></a>
## インデックス (Indexes)

<a name="creating-indexes"></a>
### インデックスの作成

Laravel スキーマ ビルダは、いくつかの種類のインデックスをサポートしています。次の例では、新しい `email` 列を作成し、その値が一意である必要があることを指定します。インデックスを作成するには、`unique` メソッドを列定義に連鎖させます。

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->unique();
    });

あるいは、列を定義した後にインデックスを作成することもできます。これを行うには、スキーマ ビルダ ブループリントで `unique` メソッドを呼び出す必要があります。このメソッドは、一意のインデックスを受け取る列の名前を受け入れます。

    $table->unique('email');

列の配列をインデックス メソッドに渡して、複合 (または複合) インデックスを作成することもできます。

    $table->index(['account_id', 'created_at']);

インデックスを作成するとき、Laravel はテーブル、列名、インデックスの種類に基づいてインデックス名を自動的に生成しますが、メソッドに 2 番目の引数を渡してインデックス名を自分で指定することもできます。

    $table->unique('email', 'unique_email');

<a name="available-index-types"></a>
#### 利用可能なインデックスの種類

Laravel のスキーマ ビルダ ブループリント クラスは、Laravel でサポートされる各タイプのインデックスを作成するためのメソッドを提供します。各インデックス メソッドは、オプションの 2 番目の引数を受け入れてインデックスの名前を指定します。省略した場合、名前はインデックスに使用されるテーブルと列の名前、およびインデックス タイプから派生します。使用可能な各インデックス方法については、次の表で説明します。

コマンド |  説明
-------  |  -----------
`$table->primary('id');` |  主キーを追加します。
`$table->primary(['id', 'parent_id']);` |  複合キーを追加します。
`$table->unique('email');` |  一意のインデックスを追加します。
`$table->index('state');` |  インデックスを追加します。
`$table->fullText('body');` |  全文インデックスを追加します (MySQL/PostgreSQL)。
`$table->fullText('body')->language('english');` |  指定した言語 (PostgreSQL) の全文インデックスを追加します。
`$table->spatialIndex('location');` |  空間インデックスを追加します (SQLite を除く)。

<a name="index-lengths-mysql-mariadb"></a>
#### インデックスの長さと MySQL / MariaDB

デフォルトでは、Laravel は `utf8mb4` 文字セットを使用します。 5.7.7 リリースより古いバージョンの MySQL または 10.2.2 リリースより古い MariaDB を実行している場合、MySQL がインデックスを作成できるように、移行によって生成されるデフォルトの文字列の長さを手動で構成する必要がある場合があります。 `App\Providers\AppServiceProvider` クラスの `boot` メソッド内で `Schema::defaultStringLength` メソッドを呼び出すことで、デフォルトの文字列の長さを構成できます。

    use Illuminate\Support\Facades\Schema;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Schema::defaultStringLength(191);
    }

あるいは、データベースの `innodb_large_prefix` オプションを有効にすることもできます。このオプションを適切に有効にする方法については、データベースのドキュメントを参照してください。

<a name="renaming-indexes"></a>
### インデックスの名前変更

インデックスの名前を変更するには、スキーマ ビルダ ブループリントによって提供される `renameIndex` メソッドを使用できます。このメソッドは、現在のインデックス名を最初の引数として受け入れ、目的の名前を 2 番目の引数として受け入れます。

    $table->renameIndex('from', 'to')

> **警告**
> アプリケーションが SQLite データベースを利用している場合は、`renameIndex` メソッドを使用する前に、Composer パッケージ マネージャーを介して `doctrine/dbal` パッケージをインストールする必要があります。

<a name="dropping-indexes"></a>
### インデックスの削除

インデックスを削除するには、インデックスの名前を指定する必要があります。デフォルトでは、Laravel はテーブル名、インデックス付き列の名前、インデックスタイプに基づいてインデックス名を自動的に割り当てます。以下にいくつかの例を示します。

コマンド |  説明
-------  |  -----------
`$table->dropPrimary('users_id_primary');` |  「users」テーブルから主キーを削除します。
`$table->dropUnique('users_email_unique');` |  「users」テーブルから一意のインデックスを削除します。
`$table->dropIndex('geo_state_index');` |  「geo」テーブルから基本インデックスを削除します。
`$table->dropFullText('posts_body_fulltext');` |  「posts」テーブルから全文インデックスを削除します。
`$table->dropSpatialIndex('geo_location_spatialindex');` |  「geo」テーブルから空間インデックスを削除します (SQLite を除く)。

インデックスを削除するメソッドに列の配列を渡すと、テーブル名、列、インデックス タイプに基づいて従来のインデックス名が生成されます。

    Schema::table('geo', function (Blueprint $table) {
        $table->dropIndex(['state']); // Drops index 'geo_state_index'
    });

<a name="foreign-key-constraints"></a>
### 外部キー制約

Laravel は、データベース レベルで参照整合性を強制するために使用される外部キー制約の作成のサポートも提供します。たとえば、`users` テーブルの `id` 列を参照する `posts` テーブルの `user_id` 列を定義してみましょう。

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('posts', function (Blueprint $table) {
        $table->unsignedBigInteger('user_id');

        $table->foreign('user_id')->references('id')->on('users');
    });

この構文はかなり冗長であるため、Laravel では、より良い開発者エクスペリエンスを提供するために、規則を使用する追加の簡潔なメソッドが提供されています。 `foreignId` メソッドを使用して列を作成する場合、上記の例は次のように書き換えることができます。

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained();
    });

`foreignId` メソッドは `UNSIGNED BIGINT` と同等の列を作成しますが、`constrained` メソッドは規則を使用して参照されるテーブルと列の名前を決定します。テーブル名が Laravel の規則と一致しない場合は、引数としてテーブル名を `constrained` メソッドに渡すことでテーブル名を指定できます。

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained('users');
    });

制約の「削除時」プロパティと「更新時」プロパティに必要なアクションを指定することもできます。

    $table->foreignId('user_id')
          ->constrained()
          ->onUpdate('cascade')
          ->onDelete('cascade');

これらのアクションには、代替の表現力豊かな構文も提供されています。

方法 |  説明
-------  |  -----------
`$table->cascadeOnUpdate();` |更新はカスケードする必要があります。
`$table->restrictOnUpdate();`|更新は制限されるべきです。
`$table->cascadeOnDelete();` |削除はカスケードする必要があります。
`$table->restrictOnDelete();`|削除は制限する必要があります。
`$table->nullOnDelete();` |削除では、外部キーの値を null に設定する必要があります。

追加の [列修飾子](#column-modifiers) は、`constrained` メソッドの前に呼び出す必要があります。

    $table->foreignId('user_id')
          ->nullable()
          ->constrained();

<a name="dropping-foreign-keys"></a>
#### 外部キーの削除

外部キーを削除するには、`dropForeign` メソッドを使用して、削除する外部キー制約の名前を引数として渡します。外部キー制約では、インデックスと同じ命名規則が使用されます。つまり、外部キー制約名は、制約内のテーブル名と列名に基づいて、その後に「\_foreign」サフィックスが付加されます。

    $table->dropForeign('posts_user_id_foreign');

あるいは、外部キーを保持する列名を含む配列を `dropForeign` メソッドに渡すこともできます。配列は、Laravel の制約命名規則を使用して外部キー制約名に変換されます。

    $table->dropForeign(['user_id']);

<a name="toggling-foreign-key-constraints"></a>
#### 外部キー制約の切り替え

次の方法を使用して、移行内で外部キー制約を有効または無効にすることができます。

    Schema::enableForeignKeyConstraints();

    Schema::disableForeignKeyConstraints();

    Schema::withoutForeignKeyConstraints(function () {
        // Constraints disabled within this closure...
    });

> **警告**
> SQLite はデフォルトで外部キー制約を無効にします。 SQLite を使用する場合は、移行で SQLite を作成する前に、データベース構成で [外部キーのサポートを有効にする](/docs/{{version}}/database#configuration) を実行してください。さらに、SQLite はテーブルおよび [テーブルが変更された場合ではない](https://www.sqlite.org/omitted.html) の作成時に外部キーのみをサポートします。

<a name="events"></a>
## イベント (Events)

便宜上、各移行操作では [event](/docs/{{version}}/events) がディスパッチされます。次のイベントはすべて、基本 `Illuminate\Database\Events\MigrationEvent` クラスを拡張します。

クラス |説明
-------|-------
| `Illuminate\Database\Events\MigrationsStarted` | 移行のバッチが実行されようとしています。 |
| `Illuminate\Database\Events\MigrationsEnded` | 移行のバッチの実行が終了しました。 |
| `Illuminate\Database\Events\MigrationStarted` | 単一の移行が実行されようとしています。 |
| `Illuminate\Database\Events\MigrationEnded` | 1 つの移行の実行が終了しました。 |
| `Illuminate\Database\Events\SchemaDumped` | データベース スキーマ ダンプが完了しました。 |
| `Illuminate\Database\Events\SchemaLoaded` | 既存のデータベース スキーマ ダンプがロードされました。 |

