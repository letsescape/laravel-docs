# テスト: はじめに (Testing: Getting Started)

- [Introduction](#introduction)
- [Environment](#environment)
- [テストの作成](#creating-tests)
- [テストの実行](#running-tests)
    - [テストの並列実行](#running-tests-in-parallel)
    - [テスト範囲のレポート](#reporting-test-coverage)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel はテストを念頭に置いて構築されています。実際、PHPUnit を使用したテストのサポートはすぐに組み込まれており、アプリケーション用に `phpunit.xml` ファイルがすでにセットアップされています。このフレームワークには、アプリケーションを表現的にテストできる便利なヘルパ メソッドも付属しています。

デフォルトでは、アプリケーションの `tests` ディレクトリには、`Feature` と `Unit` の 2 つのディレクトリが含まれています。単体テストは、コードの非常に小さく分離された部分に焦点を当てたテストです。実際、ほとんどの単体テストはおそらく 1 つのメソッドに焦点を当てています。 「Unit」テストディレクトリ内のテストはLaravelアプリケーションを起動しないため、アプリケーションのデータベースや他のフレームワークサービスにアクセスできません。

機能テストでは、複数のオブジェクトが相互に対話する方法や、JSON エンドポイントへの完全な HTTP リクエストなど、コードの大部分をテストする場合があります。 **通常、テストのほとんどは機能テストである必要があります。これらのタイプのテストは、システム全体が意図したとおりに機能していることを最も確信できます。**

`ExampleTest.php` ファイルは、`Feature` テスト ディレクトリと `Unit` テスト ディレクトリの両方に提供されます。新しい Laravel アプリケーションをインストールした後、`vendor/bin/phpunit` または `php artisan test` コマンドを実行してテストを実行します。

<a name="environment"></a>
## 環境 (Environment)

テストを実行すると、`phpunit.xml` ファイルで定義された環境変数により、Laravel は自動的に [構成環境](/docs/{{version}}/configuration#environment-configuration) を `testing` に設定します。 Laravel は、テスト中にセッションとキャッシュを `array` ドライバに自動的に構成します。つまり、テスト中にセッション データやキャッシュ データは保持されません。

必要に応じて、他のテスト環境構成値を自由に定義できます。 `testing` 環境変数はアプリケーションの `phpunit.xml` ファイルで構成できますが、テストを実行する前に、`config:clear` Artisan コマンドを使用して構成キャッシュを必ずクリアしてください。

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 環境ファイル

さらに、プロジェクトのルートに `.env.testing` ファイルを作成することもできます。このファイルは、PHPUnit テストを実行するとき、または `--env=testing` オプションを指定して Artisan コマンドを実行するときに、`.env` ファイルの代わりに使用されます。

<a name="the-creates-application-trait"></a>
#### `CreatesApplication` 特性

Laravel には、アプリケーションの基本 `TestCase` クラスに適用される `CreatesApplication` トレイトが含まれています。このトレイトには、テストを実行する前に Laravel アプリケーションをブートストラップする `createApplication` メソッドが含まれています。 Laravel の並列テスト機能などの一部の機能はこのトレイトに依存しているため、このトレイトを元の場所に残しておくことが重要です。

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

[害虫PHP](https://pestphp.com) テストを作成したい場合は、`--pest` オプションを `make:test` コマンドに指定できます。

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> **注記**
> テスト スタブは、[スタブ発行](/docs/{{version}}/artisan#stub-customization) を使用してカスタマイズできます。

テストが生成されたら、通常 [PHPUnit](https://phpunit.de) を使用するのと同じようにテスト メソッドを定義できます。テストを実行するには、端末から `vendor/bin/phpunit` または `php artisan test` コマンドを実行します。

    <?php

    namespace Tests\Unit;

    use PHPUnit\Framework\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * A basic test example.
         *
         * @return void
         */
        public function test_basic_test()
        {
            $this->assertTrue(true);
        }
    }

> **警告**
> テスト クラス内で独自の `setUp` / `tearDown` メソッドを定義する場合は、必ず親クラスでそれぞれの `parent::setUp()` / `parent::tearDown()` メソッドを呼び出してください。

<a name="running-tests"></a>
## テストの実行 (Running Tests)

前述したように、テストを作成したら、`phpunit` を使用してテストを実行できます。

```shell
./vendor/bin/phpunit
```

`phpunit` コマンドに加えて、`test` Artisan コマンドを使用してテストを実行することもできます。 Artisan テスト ランナーは、開発とデバッグを容易にするために詳細なテスト レポートを提供します。

```shell
php artisan test
```

`phpunit` コマンドに渡すことができる引数は、Artisan `test` コマンドにも渡すことができます。

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### テストの並列実行

デフォルトでは、Laravel と PHPUnit は単一プロセス内でテストを順番に実行します。ただし、複数のプロセスでテストを同時に実行すると、テストの実行時間を大幅に短縮できます。開始するには、アプリケーションが `nunomaduro/collision` パッケージのバージョン `^5.3` 以上に依存していることを確認してください。次に、`test` Artisan コマンドを実行するときに `--parallel` オプションを含めます。

```shell
php artisan test --parallel
```

デフォルトでは、Laravel はマシン上で利用可能な CPU コアと同じ数のプロセスを作成します。ただし、`--processes` オプションを使用してプロセスの数を調整できます。

```shell
php artisan test --parallel --processes=4
```

> **警告**
> テストを並行して実行する場合、一部の PHPUnit オプション (`--do-not-cache-result` など) が使用できない場合があります。

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

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Artisan;
    use Illuminate\Support\Facades\ParallelTesting;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            ParallelTesting::setUpProcess(function ($token) {
                // ...
            });

            ParallelTesting::setUpTestCase(function ($token, $testCase) {
                // ...
            });

            // Executed when a test database is created...
            ParallelTesting::setUpTestDatabase(function ($database, $token) {
                Artisan::call('db:seed');
            });

            ParallelTesting::tearDownTestCase(function ($token, $testCase) {
                // ...
            });

            ParallelTesting::tearDownProcess(function ($token) {
                // ...
            });
        }
    }

<a name="accessing-the-parallel-testing-token"></a>
#### 並列テスト トークンへのアクセス

アプリケーションのテスト コード内の他の場所から現在の並列プロセスの「トークン」にアクセスしたい場合は、`token` メソッドを使用できます。このトークンは、個々のテスト プロセスの一意の文字列識別子であり、並列テスト プロセス全体でリソースをセグメント化するために使用できます。たとえば、Laravel は、各並列テスト プロセスによって作成されたテスト データベースの末尾にこのトークンを自動的に追加します。

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### テスト範囲のレポート

> **警告**
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

