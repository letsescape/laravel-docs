# 同時実行性 (Concurrency)

- [Introduction](#introduction)
- [同時タスクの実行](#running-concurrent-tasks)
- [同時実行タスクの延期](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 導入 (Introduction)

場合によっては、相互に依存しないいくつかの遅いタスクを実行する必要がある場合があります。多くの場合、タスクを同時に実行することで大幅なパフォーマンスの向上を実現できます。 Laravel の `Concurrency` ファサードは、クロージャを同時に実行するためのシンプルで便利な API を提供します。

<a name="how-it-works"></a>
#### 仕組み

Laravel は、指定されたクロージャをシリアル化し、隠された Artisan CLI コマンドにディスパッチすることで同時実行性を実現します。このコマンドは、クロージャをシリアル化解除して、独自の PHP プロセス内で呼び出します。クロージャが呼び出された後、結果の値は親プロセスにシリアル化されて戻されます。

`Concurrency` ファサードは、`process` (デフォルト)、`fork`、および `sync` の 3 つのドライバをサポートします。

`fork` ドライバは、デフォルトの `process` ドライバと比較してパフォーマンスが向上していますが、PHP は Web リクエスト中のフォークをサポートしていないため、PHP の CLI コンテキスト内でのみ使用できます。 `fork` ドライバを使用する前に、`spatie/fork` パッケージをインストールする必要があります。

```shell
composer require spatie/fork
```

`sync` ドライバは、すべての同時実行性を無効にして、親プロセス内で指定されたクロージャを順番に実行するだけのテスト中に主に役立ちます。

<a name="running-concurrent-tasks"></a>
## 同時タスクの実行 (Running Concurrent Tasks)

同時タスクを実行するには、`Concurrency` ファサードの `run` メソッドを呼び出します。 `run` メソッドは、子 PHP プロセスで同時に実行する必要があるクロージャの配列を受け入れます。

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

特定のドライバを使用するには、`driver` メソッドを使用できます。

```php
$results = Concurrency::driver('fork')->run(...);
```

または、デフォルトの同時実行ドライバを変更するには、`config:publish` Artisan コマンドを使用して `concurrency` 構成ファイルを公開し、ファイル内の `default` オプションを更新する必要があります。

```shell
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
## 同時実行タスクの延期 (Deferring Concurrent Tasks)

クロージャの配列を同時に実行したいが、それらのクロージャによって返される結果には興味がない場合は、`defer` メソッドの使用を検討する必要があります。 `defer` メソッドが呼び出されたとき、指定されたクロージャはすぐには実行されません。代わりに、Laravel は HTTP 応答がユーザーに送信された後にクロージャーを同時に実行します。

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```

