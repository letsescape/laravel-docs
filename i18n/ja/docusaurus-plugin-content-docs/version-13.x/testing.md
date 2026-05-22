# テスト: はじめに (Testing: Getting Started)

- [Introduction](#introduction)
- [Environment](#environment)
- [テストの作成](#creating-tests)
- [テストの実行](#running-tests)
    - [テストの並列実行](#running-tests-in-parallel)
    - [テスト範囲のレポート](#reporting-test-coverage)
    - [プロファイリングテスト](#profiling-tests)
- [構成のキャッシュ](#configuration-caching)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel はテストを念頭に置いて構築されています。実際、[Pest](https://pestphp.com) および [PHPUnit](https://phpunit.de) を使用したテストのサポートはすぐに組み込まれており、アプリケーション用に `phpunit.xml` ファイルがすでにセットアップされています。このフレームワークには、アプリケーションを表現的にテストできる便利なヘルパ メソッドも付属しています。

デフォルトでは、アプリケーションの `tests` ディレクトリには、`Feature` と `Unit` の 2 つのディレクトリが含まれています。単体テストは、コードの非常に小さく分離された部分に焦点を当てたテストです。実際、ほとんどの単体テストはおそらく 1 つのメソッドに焦点を当てています。 「Unit」テストディレクトリ内のテストはLaravelアプリケーションを起動しないため、アプリケーションのデータベースや他のフレームワークサービスにアクセスできません。

機能テストでは、複数のオブジェクトが相互に対話する方法や、JSON エンドポイントへの完全な HTTP リクエストなど、コードの大部分をテストする場合があります。 **通常、テストのほとんどは機能テストである必要があります。これらのタイプのテストは、システム全体が意図したとおりに機能していることを最も確信できます。**

`ExampleTest.php` ファイルは、`Feature` テスト ディレクトリと `Unit` テスト ディレクトリの両方に提供されます。新しい Laravel アプリケーションをインストールした後、`vendor/bin/pest`、`vendor/bin/phpunit`、または `php artisan test` コマンドを実行してテストを実行します。

<a name="environment"></a>
## 環境 (Environment)

テストを実行すると、`phpunit.xml` ファイルで定義された環境変数により、Laravel は自動的に [構成環境](/docs/{{version}}/configuration#environment-configuration) を `testing` に設定します。また、Laravel はセッションとキャッシュを `array` ドライバに自動的に構成するため、テスト中にセッションやキャッシュのデータは保持されません。

必要に応じて、他のテスト環境構成値を自由に定義できます。 `testing` 環境変数はアプリケーションの `phpunit.xml` ファイルで構成できますが、テストを実行する前に、`config:clear` Artisan コマンドを使用して構成キャッシュを必ずクリアしてください。

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 環境ファイル

さらに、プロジェクトのルートに `.env.testing` ファイルを作成することもできます。このファイルは、Pest および PHPUnit テストを実行するとき、または `--env=testing` オプションを指定して Artisan コマンドを実行するときに、`.env` ファイルの代わりに使用されます。

<a name="creating-tests"></a>
## テストの作成 (Creating Tests)

新しいテスト ケースを作成するには、`make:test` Artisan コマンドを使用します。デフォルトでは、テストは `tests/Feature` ディレクトリに配置されます。

```shell
php artisan make:test UserTest
```

`tests/Unit` ディレクトリ内にテストを作成したい場合は、`make:test` コマンドを実行するときに `--unit` オプションを使用できます。

```shell
php artisan make:test UserTest --unit
```

Laravel のテスト機能に主に依存するテストクラスがあるが、特定のテスト メソッドでフレームワークを起動する必要がない場合は、そのメソッドに `#[UnitTest]` 属性を適用して、そのテストのみのアプリケーションの起動をスキップできます。

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\Attributes\UnitTest;
use Tests\TestCase;

class LocationServiceTest extends TestCase
{
    public function test_get_coordinates_resolves_address(): void
    {
        // This test uses Laravel's testing features...
    }

    #[UnitTest]
    public function test_get_state_returns_state_from_abbreviation(): void
    {
        // This test runs without booting the application...
    }
}
```

> [!NOTE]
> テスト スタブは、[スタブ発行](/docs/{{version}}/artisan#stub-customization) を使用してカスタマイズできます。

テストが生成されたら、通常 Pest または PHPUnit を使用するのと同じようにテストを定義できます。テストを実行するには、端末から `vendor/bin/pest`、`vendor/bin/phpunit`、または `php artisan test` コマンドを実行します。

```php tab=Pest
<?php

test('basic', function () {
    expect(true)->toBeTrue();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> テスト クラス内で独自の `setUp` / `tearDown` メソッドを定義する場合は、必ず親クラスでそれぞれの `parent::setUp()` / `parent::tearDown()` メソッドを呼び出してください。通常、独自の `setUp` メソッドの開始時に `parent::setUp()` を呼び出し、`tearDown` メソッドの最後に `parent::tearDown()` を呼び出す必要があります。

<a name="running-tests"></a>
## テストの実行 (Running Tests)

前述したように、テストを作成したら、`pest` または `phpunit` を使用してテストを実行できます。

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest` または `phpunit` コマンドに加えて、`test` Artisan コマンドを使用してテストを実行することもできます。 Artisan テスト ランナーは、開発とデバッグを容易にするために詳細なテスト レポートを提供します。

```shell
php artisan test
```

`pest` または `phpunit` コマンドに渡すことができる引数は、Artisan `test` コマンドにも渡すことができます。

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### テストの並列実行

デフォルトでは、Laravel と Pest / PHPUnit は単一プロセス内でテストを順番に実行します。ただし、複数のプロセス間でテストを同時に実行すると、テストの実行にかかる時間を大幅に短縮できる場合があります。まず、`brianium/paratest` Composer パッケージを「dev」依存関係としてインストールする必要があります。次に、`test` Artisan コマンドを実行するときに、`--parallel` オプションを含めます。

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

デフォルトでは、Laravel はマシン上で利用可能な CPU コアと同じ数のプロセスを作成します。ただし、`--processes` オプションを使用してプロセスの数を調整できます。

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> テストを並行して実行する場合、一部の Pest / PHPUnit オプション (`--do-not-cache-result` など) が使用できない場合があります。

<a name="parallel-testing-and-databases"></a>
#### 並列テストとデータベース

プライマリデータベース接続を設定している限り、Laravel はテストを実行している並列プロセスごとにテストデータベースの作成と移行を自動的に処理します。テスト データベースには、プロセスごとに一意のプロセス トークンが接尾辞として付けられます。たとえば、2 つの並列テスト プロセスがある場合、Laravel は `your_db_test_1` および `your_db_test_2` テスト データベースを作成して使用します。

デフォルトでは、テスト データベースは `test` Artisan コマンドの呼び出し間で保持されるため、後続の `test` 呼び出しで再度使用できます。ただし、`--recreate-databases` オプションを使用してそれらを再作成することはできます。

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 並列テストフック

場合によっては、アプリケーションのテストで使用される特定のリソースを、複数のテスト プロセスで安全に使用できるように準備する必要がある場合があります。

`ParallelTesting` ファサードを使用すると、プロセスまたはテスト ケースの `setUp` および `tearDown` で実行されるコードを指定できます。指定されたクロージャは、それぞれプロセス トークンと現在のテスト ケースを含む `$token` 変数と `$testCase` 変数を受け取ります。

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;
use PHPUnit\Framework\TestCase;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        ParallelTesting::setUpProcess(function (int $token) {
            // ...
        });

        ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        // Executed when a test database is created...
        ParallelTesting::setUpTestDatabase(function (string $database, int $token) {
            Artisan::call('db:seed');
        });

        ParallelTesting::tearDownTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        ParallelTesting::tearDownProcess(function (int $token) {
            // ...
        });
    }
}
```

<a name="accessing-the-parallel-testing-token"></a>
#### 並列テストトークンへのアクセス

アプリケーションのテスト コード内の他の場所から現在の並列プロセスの「トークン」にアクセスしたい場合は、`token` メソッドを使用できます。このトークンは、個々のテスト プロセスの一意の文字列識別子であり、並列テスト プロセス全体でリソースをセグメント化するために使用できます。たとえば、Laravel は、各並列テスト プロセスによって作成されたテスト データベースの末尾にこのトークンを自動的に追加します。

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### テスト範囲のレポート

> [!WARNING]
> この機能には、[Xdebug](https://xdebug.org) または [PCOV](https://pecl.php.net/package/pcov) が必要です。

アプリケーション テストを実行するとき、テスト ケースが実際にアプリケーション コードをカバーしているかどうか、およびテストの実行時に使用されるアプリケーション コードの量を確認することができます。これを実現するには、`test` コマンドを呼び出すときに `--coverage` オプションを指定できます。

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 最小カバレッジしきい値の強制

`--min` オプションを使用して、アプリケーションの最小テスト カバレッジしきい値を定義できます。このしきい値が満たされていない場合、テスト スイートは失敗します。

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### プロファイリングテスト

Artisan テスト ランナーには、アプリケーションの最も遅いテストをリストするための便利なメカニズムも含まれています。 `--profile` オプションを指定して `test` コマンドを呼び出すと、最も遅い 10 個のテストのリストが表示され、テスト スイートを高速化するためにどのテストを改善できるかを簡単に調査できます。

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
## 構成のキャッシュ (Configuration Caching)

テストを実行するとき、Laravel は個々のテストメソッドごとにアプリケーションを起動します。  キャッシュされた構成ファイルがない場合、テストの開始時にアプリケーション内の各構成ファイルをロードする必要があります。構成を一度構築し、それを 1 回の実行ですべてのテストに再利用するには、`Illuminate\Foundation\Testing\WithCachedConfig` トレイトを使用できます。

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithCachedConfig;

pest()->use(WithCachedConfig::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithCachedConfig;
use Tests\TestCase;

class ConfigTest extends TestCase
{
    use WithCachedConfig;

    // ...
}
```

