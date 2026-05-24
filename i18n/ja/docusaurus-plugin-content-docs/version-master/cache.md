# キャッシュ (Cache)

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [ドライバの前提条件](#driver-prerequisites)
- [キャッシュの使用量](#cache-usage)
    - [キャッシュインスタンスの取得](#obtaining-a-cache-instance)
    - [キャッシュからアイテムを取得する](#retrieving-items-from-the-cache)
    - [アイテムをキャッシュに保存する](#storing-items-in-the-cache)
    - [アイテムの寿命を延長する](#extending-item-lifetime)
    - [キャッシュからのアイテムの削除](#removing-items-from-the-cache)
    - [キャッシュのメモ化](#cache-memoization)
    - [キャッシュヘルパ](#the-cache-helper)
- [キャッシュタグ](#cache-tags)
- [アトミックロック](#atomic-locks)
    - [ロックの管理](#managing-locks)
    - [プロセス全体でのロックの管理](#managing-locks-across-processes)
    - [同時実行の制限](#concurrency-limiting)
- [キャッシュフェイルオーバー](#cache-failover)
- [カスタム キャッシュ ドライバの追加](#adding-custom-cache-drivers)
    - [ドライバの作成](#writing-the-driver)
    - [ドライバを登録する](#registering-the-driver)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

アプリケーションによって実行されるデータの取得または処理タスクの中には、CPU に負荷がかかるものや、完了までに数秒かかるものもあります。この場合、同じデータに対する後続のリクエストですぐに取得できるように、取得したデータを一時的にキャッシュするのが一般的です。キャッシュされたデータは通常、[Memcached](https://memcached.org) や [Redis](https://redis.io) などの非常に高速なデータ ストアに保存されます。

ありがたいことに、Laravel はさまざまなキャッシュ バックエンドに表現力豊かな統合 API を提供しており、その超高速データ取得を活用して Web アプリケーションを高速化できます。

<a name="configuration"></a>
## 構成 (Configuration)

アプリケーションのキャッシュ構成ファイルは、`config/cache.php` にあります。このファイルでは、アプリケーション全体でデフォルトで使用するキャッシュ ストアを指定できます。 Laravel は、[Memcached](https://memcached.org)、[Redis](https://redis.io)、[DynamoDB](https://aws.amazon.com/dynamodb) などの一般的なキャッシュ バックエンドやリレーショナル データベースをそのままサポートしています。さらに、ファイル ベースのキャッシュ ドライバも利用でき、`array` および `null` キャッシュ ドライバは自動テストに便利なキャッシュ バックエンドを提供します。

キャッシュ構成ファイルには、検討できる他のさまざまなオプションも含まれています。デフォルトでは、Laravel は `database` キャッシュドライバを使用するように構成されており、シリアル化されたキャッシュされたオブジェクトがアプリケーションのデータベースに保存されます。

<a name="driver-prerequisites"></a>
### ドライバの前提条件

<a name="prerequisites-database"></a>
#### データベース

`database` キャッシュ ドライバを使用する場合、キャッシュ データを含むデータベース テーブルが必要になります。通常、これはLaravelのデフォルトの`0001_01_01_000001_create_cache_table.php` [データベースの移行](/docs/{{version}}/migrations)に含まれています。ただし、アプリケーションにこの移行が含まれていない場合は、`make:cache-table` Artisan コマンドを使用して移行を作成できます。

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached ドライバを使用するには、[Memcached PECL パッケージ](https://pecl.php.net/package/memcached) をインストールする必要があります。すべての Memcached サーバーを `config/cache.php` 構成ファイルにリストすることができます。このファイルには、すぐに使用できる `memcached.servers` エントリがすでに含まれています。

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => env('MEMCACHED_HOST', '127.0.0.1'),
            'port' => env('MEMCACHED_PORT', 11211),
            'weight' => 100,
        ],
    ],
],
```

必要に応じて、`host` オプションを UNIX ソケット パスに設定できます。これを行う場合、`port` オプションを `0` に設定する必要があります。

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],
],
```

<a name="redis"></a>
#### レディス

Laravel で Redis キャッシュを使用する前に、PECL 経由で PhpRedis PHP 拡張機能をインストールするか、Composer 経由で `predis/predis` パッケージ (~2.0) をインストールする必要があります。 [Laravel Sail](/docs/{{version}}/sail) には、この拡張機能がすでに含まれています。さらに、[Laravel Cloud](https://cloud.laravel.com) や [Laravel Forge](https://forge.laravel.com) などの公式 Laravel アプリケーション プラットフォームには、デフォルトで PhpRedis 拡張機能がインストールされています。

Redis の構成の詳細については、[Laravelのドキュメントページ](/docs/{{version}}/redis#configuration) を参照してください。

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) キャッシュ ドライバを使用する前に、すべてのキャッシュ データを保存する DynamoDB テーブルを作成する必要があります。通常、このテーブルには `cache` という名前を付ける必要があります。ただし、`cache` 構成ファイル内の `stores.dynamodb.table` 構成値の値に基づいてテーブルに名前を付ける必要があります。テーブル名は、`DYNAMODB_CACHE_TABLE` 環境変数を介して設定することもできます。

このテーブルには、アプリケーションの `cache` 構成ファイル内の `stores.dynamodb.attributes.key` 構成項目の値に対応する名前を持つ文字列パーティション キーも必要です。デフォルトでは、パーティション キーの名前は `key` である必要があります。

通常、DynamoDB は有効期限切れのアイテムをテーブルから積極的に削除しません。したがって、テーブル上で [生存時間 (TTL) を有効にする](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) を実行する必要があります。テーブルの TTL 設定を構成するときは、TTL 属性名を `expires_at` に設定する必要があります。

次に、Laravel アプリケーションが DynamoDB と通信できるように AWS SDK をインストールします。

```shell
composer require aws/aws-sdk-php
```

さらに、DynamoDB キャッシュ ストア設定オプションに値が指定されていることを確認する必要があります。通常、`AWS_ACCESS_KEY_ID` や `AWS_SECRET_ACCESS_KEY` などのオプションは、アプリケーションの `.env` 構成ファイルで定義する必要があります。

```php
'dynamodb' => [
    'driver' => 'dynamodb',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => env('DYNAMODB_CACHE_TABLE', 'cache'),
    'endpoint' => env('DYNAMODB_ENDPOINT'),
],
```

<a name="mongodb"></a>
#### モンゴDB

MongoDB を使用している場合、`mongodb` キャッシュ ドライバは公式 `mongodb/laravel-mongodb` パッケージによって提供され、`mongodb` データベース接続を使用して構成できます。 MongoDB は TTL インデックスをサポートしており、期限切れのキャッシュ アイテムを自動的にクリアするために使用できます。

MongoDB の構成の詳細については、MongoDB [キャッシュとロックのドキュメント](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) を参照してください。

<a name="cache-usage"></a>
## キャッシュの使用量 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### キャッシュインスタンスの取得

キャッシュ ストア インスタンスを取得するには、`Cache` ファサードを使用できます。これは、このドキュメント全体で使用するものです。 `Cache` ファサードは、Laravel キャッシュ コントラクトの基礎となる実装への便利で簡潔なアクセスを提供します。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show a list of all users of the application.
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```

<a name="accessing-multiple-cache-stores"></a>
#### 複数のキャッシュ ストアへのアクセス

`Cache` ファサードを使用すると、`store` メソッド経由でさまざまなキャッシュ ストアにアクセスできます。 `store` メソッドに渡されるキーは、`cache` 構成ファイルの `stores` 構成配列にリストされているストアの 1 つに対応する必要があります。

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
### キャッシュからアイテムを取得する

`Cache` ファサードの `get` メソッドは、キャッシュから項目を取得するために使用されます。項目がキャッシュに存在しない場合は、`null` が返されます。必要に応じて、項目が存在しない場合に返されるデフォルト値を指定する 2 番目の引数を `get` メソッドに渡すことができます。

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

クロージャをデフォルト値として渡すこともできます。指定された項目がキャッシュに存在しない場合は、クロージャの結果が返されます。クロージャーを渡すと、データベースまたは他の外部サービスからのデフォルト値の取得を延期できます。

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### アイテムの存在を判断する

`has` メソッドを使用して、アイテムがキャッシュに存在するかどうかを確認できます。項目が存在するが、その値が `null` である場合、このメソッドは `false` も返します。

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 値の増減

`increment` メソッドと `decrement` メソッドは、キャッシュ内の整数項目の値を調整するために使用できます。これらのメソッドはどちらも、項目の値を増減する量を示すオプションの 2 番目の引数を受け入れます。

```php
// Initialize the value if it does not exist...
Cache::add('key', 0, now()->plus(hours: 4));

// Increment or decrement the value...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 取得と保存

キャッシュから項目を取得したい場合がありますが、要求された項目が存在しない場合はデフォルト値を保存することもできます。たとえば、すべてのユーザーをキャッシュから取得したり、ユーザーが存在しない場合はデータベースから取得してキャッシュに追加したりすることができます。これは、`Cache::remember` メソッドを使用して実行できます。

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

項目がキャッシュに存在しない場合、`remember` メソッドに渡されたクロージャが実行され、その結果がキャッシュに配置されます。

`rememberForever` メソッドを使用して、キャッシュからアイテムを取得したり、アイテムが存在しない場合は永久に保存したりできます。

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### 再検証中に失効する

`Cache::remember` メソッドを使用する場合、キャッシュされた値の有効期限が切れていると、一部のユーザーは応答時間が遅くなる可能性があります。特定の種類のデータの場合、キャッシュされた値がバックグラウンドで再計算されている間、部分的に古いデータを提供できるようにすると、キャッシュされた値の計算中に一部のユーザーが応答時間の低下を経験するのを防ぐことができると便利です。これは、「再検証中に失効する」パターンと呼ばれることが多く、`Cache::flexible` メソッドはこのパターンの実装を提供します。

この柔軟なメソッドは、キャッシュされた値が「新しい」とみなされる期間と、いつ「古くなった」とみなされるかを指定する配列を受け入れます。配列の最初の値はキャッシュが新しいとみなされる秒数を表し、2 番目の値は再計算が必要になるまで古いデータとして提供できる期間を定義します。

新しい期間内 (最初の値の前) にリクエストが行われた場合、キャッシュは再計算されずにすぐに返されます。古い期間 (2 つの値の間) にリクエストが行われた場合、古い値がユーザーに提供され、応答がユーザーに送信された後にキャッシュされた値を更新するために [遅延関数](/docs/{{version}}/helpers#deferred-functions) が登録されます。 2 番目の値の後にリクエストが行われた場合、キャッシュは期限切れとみなされ、値はすぐに再計算されます。その結果、ユーザーの応答が遅くなる可能性があります。

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 取得と削除

キャッシュから項目を取得してからその項目を削除する必要がある場合は、`pull` メソッドを使用できます。 `get` メソッドと同様に、項目がキャッシュに存在しない場合は `null` が返されます。

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### アイテムをキャッシュに保存する

`Cache` ファサードで `put` メソッドを使用して、アイテムをキャッシュに保存できます。

```php
Cache::put('key', 'value', $seconds = 10);
```

保管時間が `put` メソッドに渡されない場合、アイテムは無期限に保管されます。

```php
Cache::put('key', 'value');
```

秒数を整数として渡す代わりに、キャッシュされたアイテムの有効期限を表す `DateTime` インスタンスを渡すこともできます。

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 存在しない場合は保存する

`add` メソッドは、アイテムがキャッシュ ストアに存在しない場合にのみ、アイテムをキャッシュに追加します。項目が実際にキャッシュに追加される場合、メソッドは `true` を返します。それ以外の場合、メソッドは `false` を返します。 `add` メソッドはアトミック操作です。

```php
Cache::add('key', 'value', $seconds);
```

<a name="extending-item-lifetime"></a>
### アイテムの寿命を延長する

`touch` メソッドを使用すると、既存のキャッシュ アイテムの有効期間 (TTL) を延長できます。キャッシュ項目が存在し、その有効期限が正常に延長された場合、`touch` メソッドは `true` を返します。項目がキャッシュに存在しない場合、メソッドは `false` を返します。

```php
Cache::touch('key', 3600);
```

`DateTimeInterface`、`DateInterval`、または `Carbon` インスタンスを指定して、正確な有効期限を指定できます。

```php
Cache::touch('key', now()->addHours(2));
```

<a name="storing-items-forever"></a>
#### アイテムを永久に保管する

`forever` メソッドを使用して、アイテムをキャッシュに永続的に保存できます。これらのアイテムは期限切れにならないため、`forget` メソッドを使用してキャッシュから手動で削除する必要があります。

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached ドライバを使用している場合、キャッシュがサイズ制限に達すると、「永久に」保存されている項目が削除される可能性があります。

<a name="removing-items-from-the-cache"></a>
### キャッシュからのアイテムの削除

`forget` メソッドを使用して、キャッシュから項目を削除できます。

```php
Cache::forget('key');
```

ゼロまたは負の有効期限秒数を指定してアイテムを削除することもできます。

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` メソッドを使用してキャッシュ全体をクリアできます。

```php
Cache::flush();
```

`flushLocks` メソッドを使用して、キャッシュ内のすべてのアトミック ロックをクリアできます。

```php
Cache::flushLocks();
```

> [!WARNING]
> キャッシュをフラッシュすると、設定されたキャッシュの「プレフィックス」が考慮されず、キャッシュからすべてのエントリが削除されます。他のアプリケーションによって共有されているキャッシュをクリアするときは、この点を慎重に検討してください。

<a name="cache-memoization"></a>
### キャッシュのメモ化

Laravel の `memo` キャッシュ ドライバを使用すると、単一のリクエストまたはジョブの実行中に、解決されたキャッシュ値をメモリに一時的に保存できます。これにより、同じ実行内でキャッシュ ヒットが繰り返されることがなくなり、パフォーマンスが大幅に向上します。

メモ化されたキャッシュを使用するには、`memo` メソッドを呼び出します。

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` メソッドは、オプションでキャッシュ ストアの名前を受け入れます。これは、メモ化されたドライバが修飾する基になるキャッシュ ストアを指定します。

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

特定のキーに対する最初の `get` 呼び出しではキャッシュ ストアから値が取得されますが、同じリクエストまたはジョブ内での後続の呼び出しではメモリから値が取得されます。

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```

キャッシュ値を変更するメソッド (`put`、`increment`、`remember` など) を呼び出すと、メモ化されたキャッシュは自動的にメモ化された値を忘れ、変更メソッドの呼び出しを基になるキャッシュ ストアに委任します。

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```

<a name="the-cache-helper"></a>
### キャッシュヘルパ

`Cache` ファサードの使用に加えて、グローバル `cache` 関数を使用して、キャッシュ経由でデータを取得および保存することもできます。単一の文字列引数を指定して `cache` 関数を呼び出すと、指定されたキーの値が返されます。

```php
$value = cache('key');
```

キーと値のペアの配列と有効期限を関数に指定すると、指定された期間、値がキャッシュに保存されます。

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

`cache` 関数を引数なしで呼び出すと、`Illuminate\Contracts\Cache\Factory` 実装のインスタンスが返され、他のキャッシュ メソッドを呼び出すことができます。

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> グローバル `cache` 関数への呼び出しをテストするときは、[ファサードのテスト](/docs/{{version}}/mocking#mocking-facades) であるかのように `Cache::shouldReceive` メソッドを使用できます。

<a name="cache-tags"></a>
## キャッシュタグ (Cache Tags)

> [!WARNING]
> `file`、`dynamodb`、または `database` キャッシュ ドライバを使用する場合、キャッシュ タグはサポートされません。

<a name="storing-tagged-cache-items"></a>
### タグ付きキャッシュ項目の保存

キャッシュ タグを使用すると、キャッシュ内の関連アイテムにタグを付けて、特定のタグが割り当てられているすべてのキャッシュされた値をフラッシュできます。タグ名の順序付き配列を渡すことで、タグ付きキャッシュにアクセスできます。たとえば、タグ付きキャッシュにアクセスし、キャッシュ内の値を `put` してみましょう。

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### タグ付きキャッシュ項目へのアクセス

タグを介して保存されたアイテムには、値の保存に使用されたタグも提供しないとアクセスできません。タグ付きキャッシュ アイテムを取得するには、同じ順序のタグ リストを `tags` メソッドに渡し、取得するキーを指定して `get` メソッドを呼び出します。

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### タグ付きキャッシュ項目の削除

タグまたはタグのリストが割り当てられているすべての項目をフラッシュできます。たとえば、次のコードは、`people`、`authors`、またはその両方でタグ付けされたすべてのキャッシュを削除します。したがって、`Anne` と `John` の両方がキャッシュから削除されます。

```php
Cache::tags(['people', 'authors'])->flush();
```

対照的に、以下のコードは、`authors` でタグ付けされたキャッシュされた値のみを削除するため、`Anne` は削除されますが、`John` は削除されません。

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## アトミックロック (Atomic Locks)

> [!WARNING]
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<a name="managing-locks"></a>
### ロックの管理

アトミック ロックを使用すると、競合状態を気にせずに分散ロックを操作できます。たとえば、[Laravel Cloud](https://cloud.laravel.com) はアトミック ロックを使用して、サーバー上で一度に 1 つのリモート タスクのみが実行されるようにします。 `Cache::lock` メソッドを使用してロックを作成および管理できます。

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

`get` メソッドはクロージャーも受け入れます。クロージャーが実行されると、Laravel は自動的にロックを解放します。

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

リクエストした時点でロックが利用できない場合は、Laravel に指定した秒数待機するように指示できます。指定された制限時間内にロックを取得できない場合は、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // Lock acquired after waiting a maximum of 5 seconds...
} catch (LockTimeoutException $e) {
    // Unable to acquire lock...
} finally {
    $lock->release();
}
```

上記の例は、`block` メソッドにクロージャーを渡すことで簡略化できます。クロージャがこのメソッドに渡されると、Laravel は指定された秒数の間ロックの取得を試み、クロージャが実行されると自動的にロックを解放します。

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
### プロセス全体でのロックの管理

場合によっては、あるプロセスでロックを取得し、別のプロセスでロックを解放したい場合があります。たとえば、Web リクエスト中にロックを取得し、そのリクエストによってトリガーされたキューに入れられたジョブの終了時にロックを解放したい場合があります。このシナリオでは、ジョブが指定されたトークンを使用してロックを再インスタンス化できるように、ロックのスコープ指定された「所有者トークン」をキューに入れられたジョブに渡す必要があります。

以下の例では、ロックが正常に取得された場合に、キューに入れられたジョブをディスパッチします。さらに、ロックの `owner` メソッドを介して、ロックの所有者トークンをキューに入れられたジョブに渡します。

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

アプリケーションの `ProcessPodcast` ジョブ内で、所有者トークンを使用してロックを復元および解放できます。

```php
Cache::restoreLock('processing', $this->owner)->release();
```

現在の所有者を考慮せずにロックを解放したい場合は、`forceRelease` メソッドを使用できます。

```php
Cache::lock('processing')->forceRelease();
```

<a name="concurrency-limiting"></a>
### 同時実行の制限

Laravel のアトミック ロック機能は、クロージャの同時実行を制限するいくつかの方法も提供します。インフラストラクチャ全体で 1 つのインスタンスのみの実行を許可する場合は、`withoutOverlapping` を使用します。

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```

デフォルトでは、ロックはクロージャの実行が完了するまで保持され、メソッドはロックを取得するまで最大 10 秒待機します。追加の引数を使用してこれらの値をカスタマイズできます。

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```

指定された待機時間内にロックを取得できない場合は、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

並列処理を制御したい場合は、`funnel` メソッドを使用して最大同時実行数を設定します。 `funnel` メソッドは、ロックをサポートするキャッシュ ドライバで動作します。

```php
Cache::funnel('foo')
    ->limit(3)
    ->releaseAfter(60)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired...
    }, function () {
        // Could not acquire concurrency lock...
    });
```

`funnel` キーは、制限されているリソースを識別します。 `limit` メソッドは、最大同時実行数を定義します。 `releaseAfter` メソッドは、取得したスロットが自動的に解放される前に、安全タイムアウトを秒単位で設定します。 `block` メソッドは、使用可能なスロットを待機する秒数を設定します。

失敗クロージャを提供する代わりに例外によってタイムアウトを処理したい場合は、2 番目のクロージャを省略できます。指定された待機時間内にロックを取得できない場合は、`Illuminate\Cache\Limiters\LimiterTimeoutException` がスローされます。

```php
use Illuminate\Cache\Limiters\LimiterTimeoutException;

try {
    Cache::funnel('foo')
        ->limit(3)
        ->releaseAfter(60)
        ->block(10)
        ->then(function () {
            // Concurrency lock acquired...
        });
} catch (LimiterTimeoutException $e) {
    // Unable to acquire concurrency lock...
}
```

同時実行リミッターに特定のキャッシュ ストアを使用したい場合は、目的のストアで `funnel` メソッドを呼び出すことができます。

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```

> [!NOTE]
> `funnel` メソッドでは、キャッシュ ストアが `Illuminate\Contracts\Cache\LockProvider` インターフェイスを実装する必要があります。ロックをサポートしていないキャッシュ ストアで `funnel` を使用しようとすると、`BadMethodCallException` がスローされます。

<a name="cache-failover"></a>
## キャッシュフェイルオーバー (Cache Failover)

`failover` キャッシュ ドライバは、キャッシュとの対話時に自動フェイルオーバー機能を提供します。 `failover` ストアのプライマリ キャッシュ ストアが何らかの理由で失敗した場合、Laravel はリスト内の次に設定されているストアを自動的に使用しようとします。これは、キャッシュの信頼性が重要な実稼働環境で高可用性を確保する場合に特に役立ちます。

フェイルオーバー キャッシュ ストアを構成するには、`failover` ドライバを指定し、順番に試行するストア名の配列を指定します。デフォルトでは、Laravel にはアプリケーションの `config/cache.php` 構成ファイルにサンプルのフェイルオーバー構成が含まれています。

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` ドライバを使用するストアを構成したら、フェイルオーバー機能を利用するには、アプリケーションの `.env` ファイルでフェイルオーバー ストアをデフォルトのキャッシュ ストアとして設定する必要があります。

```ini
CACHE_STORE=failover
```

キャッシュストア操作が失敗し、フェイルオーバーがアクティブ化されると、Laravel は `Illuminate\Cache\Events\CacheFailedOver` イベントを送出し、キャッシュストアが失敗したことをレポートまたはログに記録できるようにします。

<a name="adding-custom-cache-drivers"></a>
## カスタム キャッシュ ドライバの追加 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### ドライバの作成

カスタム キャッシュ ドライバを作成するには、まず `Illuminate\Contracts\Cache\Store` [contract](/docs/{{version}}/contracts) を実装する必要があります。したがって、MongoDB キャッシュの実装は次のようになります。

```php
<?php

namespace App\Extensions;

use Illuminate\Contracts\Cache\Store;

class MongoStore implements Store
{
    public function get($key) {}
    public function many(array $keys) {}
    public function put($key, $value, $seconds) {}
    public function putMany(array $values, $seconds) {}
    public function increment($key, $value = 1) {}
    public function decrement($key, $value = 1) {}
    public function forever($key, $value) {}
    public function forget($key) {}
    public function flush() {}
    public function getPrefix() {}
}
```

MongoDB 接続を使用してこれらの各メソッドを実装するだけです。これらの各メソッドの実装方法の例については、[Laravelフレームワークのソースコード](https://github.com/laravel/framework) の `Illuminate\Cache\MemcachedStore` を参照してください。実装が完了したら、`Cache` ファサードの `extend` メソッドを呼び出して、カスタム ドライバの登録を完了できます。

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> カスタム キャッシュ ドライバ コードをどこに配置するか迷っている場合は、`app` ディレクトリ内に `Extensions` 名前空間を作成できます。ただし、Laravel には厳格なアプリケーション構造はなく、好みに応じてアプリケーションを自由に編成できることに注意してください。

<a name="registering-the-driver"></a>
### ドライバを登録する

カスタム キャッシュ ドライバを Laravel に登録するには、`Cache` ファサードで `extend` メソッドを使用します。他のサービスプロバイダは `boot` メソッド内でキャッシュされた値を読み取ろうとする可能性があるため、`booting` コールバック内でカスタム ドライバを登録します。 `booting` コールバックを使用すると、アプリケーションのサービスプロバイダで `boot` メソッドが呼び出される直前、ただしすべてのサービスプロバイダで `register` メソッドが呼び出された後、カスタム ドライバが確実に登録されます。アプリケーションの `App\Providers\AppServiceProvider` クラスの `register` メソッド内に `booting` コールバックを登録します。

```php
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function (Application $app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // ...
    }
}
```

`extend` メソッドに渡される最初の引数はドライバの名前です。これは、`config/cache.php` 構成ファイルの `driver` オプションに対応します。 2 番目の引数は、`Illuminate\Cache\Repository` インスタンスを返すクロージャです。クロージャには、[サービスコンテナ](/docs/{{version}}/container) のインスタンスである `$app` インスタンスが渡されます。

拡張機能が登録されたら、アプリケーションの `config/cache.php` 構成ファイル内の `CACHE_STORE` 環境変数または `default` オプションを拡張機能の名前に更新します。

<a name="events"></a>
## イベント (Events)

すべてのキャッシュ操作でコードを実行するには、キャッシュによってディスパッチされるさまざまな [events](/docs/{{version}}/events) をリッスンできます。

<div class="overflow-auto">

| イベント名                                      |
|-------------------------------------------------|
| `Illuminate\Cache\Events\CacheFlushed`          |
| `Illuminate\Cache\Events\CacheFlushing`         |
| `Illuminate\Cache\Events\CacheFlushFailed`      |
| `Illuminate\Cache\Events\CacheLocksFlushed`     |
| `Illuminate\Cache\Events\CacheLocksFlushing`    |
| `Illuminate\Cache\Events\CacheLocksFlushFailed` |
| `Illuminate\Cache\Events\CacheHit`              |
| `Illuminate\Cache\Events\CacheMissed`           |
| `Illuminate\Cache\Events\ForgettingKey`         |
| `Illuminate\Cache\Events\KeyForgetFailed`       |
| `Illuminate\Cache\Events\KeyForgotten`          |
| `Illuminate\Cache\Events\KeyWriteFailed`        |
| `Illuminate\Cache\Events\KeyWritten`            |
| `Illuminate\Cache\Events\RetrievingKey`         |
| `Illuminate\Cache\Events\RetrievingManyKeys`    |
| `Illuminate\Cache\Events\WritingKey`            |
| `Illuminate\Cache\Events\WritingManyKeys`       |

</div>

パフォーマンスを向上させるには、アプリケーションの `config/cache.php` 構成ファイル内の特定のキャッシュ ストアの `events` 構成オプションを `false` に設定して、キャッシュ イベントを無効にすることができます。

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```

