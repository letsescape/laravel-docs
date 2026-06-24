<!-- # Testing: Getting Started -->
# Testing: Getting Started

- [Introduction](#introduction)
- [Environment](#environment)
- [Creating Tests](#creating-tests)
- [Running Tests](#running-tests)
    - [Running Tests in Parallel](#running-tests-in-parallel)
    - [Reporting Test Coverage](#reporting-test-coverage)
    - [Profiling Tests](#profiling-tests)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel is built with testing in mind. In fact, support for testing with PHPUnit is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications. -->
Laravel はテストを念頭に置いて構築されています。実際、PHPUnit を使用したテストのサポートはすぐに組み込まれており、アプリケーション用に `phpunit.xml` ファイルがすでにセットアップされています。このフレームワークには、アプリケーションを表現的にテストできる便利なヘルパ メソッドも付属しています。

<!-- By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services. -->
デフォルトでは、アプリケーションの `tests` ディレクトリには、`Feature` と `Unit` の 2 つのディレクトリが含まれています。単体テストは、コードの非常に小さく分離された部分に焦点を当てたテストです。実際、ほとんどの単体テストはおそらく 1 つのメソッドに焦点を当てています。 「Unit」テストディレクトリ内のテストはLaravelアプリケーションを起動しないため、アプリケーションのデータベースや他のフレームワークサービスにアクセスできません。

<!-- Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.** -->
機能テストでは、複数のオブジェクトが相互に対話する方法や、JSON エンドポイントへの完全な HTTP リクエストなど、コードの大部分をテストする場合があります。 **通常、テストのほとんどは機能テストである必要があります。これらのタイプのテストは、システム全体が意図したとおりに機能していることを最も確信できます。**

<!-- An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/phpunit` or `php artisan test` commands to run your tests. -->
`ExampleTest.php` ファイルは、`Feature` テスト ディレクトリと `Unit` テスト ディレクトリの両方に提供されます。新しい Laravel アプリケーションをインストールした後、`vendor/bin/phpunit` または `php artisan test` コマンドを実行してテストを実行します。

<a name="environment"></a>
<!-- ## Environment -->
## Environment

<!-- When running tests, Laravel will automatically set the [configuration environment](/docs/10.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver so that no session or cache data will be persisted while testing. -->
テストを実行すると、`phpunit.xml` ファイルで定義された環境変数により、Laravel は自動的に [configuration environment](/docs/10.x/configuration#environment-configuration) を `testing` に設定します。また、Laravel はセッションとキャッシュを `array` ドライバに自動的に構成するため、テスト中にセッションやキャッシュのデータは保持されません。

<!-- You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests! -->
必要に応じて、他のテスト環境構成値を自由に定義できます。 `testing` 環境変数はアプリケーションの `phpunit.xml` ファイルで構成できますが、テストを実行する前に、`config:clear` Artisan コマンドを使用して構成キャッシュを必ずクリアしてください。

<a name="the-env-testing-environment-file"></a>
<!-- #### The `.env.testing` Environment File -->
#### The `.env.testing` Environment File

<!-- In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running PHPUnit tests or executing Artisan commands with the `--env=testing` option. -->
さらに、プロジェクトのルートに `.env.testing` ファイルを作成することもできます。このファイルは、PHPUnit テストを実行するとき、または `--env=testing` オプションを指定して Artisan コマンドを実行するときに、`.env` ファイルの代わりに使用されます。

<a name="the-creates-application-trait"></a>
<!-- #### The `CreatesApplication` Trait -->
#### The `CreatesApplication` Trait

<!-- Laravel includes a `CreatesApplication` trait that is applied to your application's base `TestCase` class. This trait contains a `createApplication` method that bootstraps the Laravel application before running your tests. It's important that you leave this trait at its original location as some features, such as Laravel's parallel testing feature, depend on it. -->
Laravel には、アプリケーションの基本 `TestCase` クラスに適用される `CreatesApplication` トレイトが含まれています。このトレイトには、テストを実行する前に Laravel アプリケーションをブートストラップする `createApplication` メソッドが含まれています。 Laravel の並列テスト機能などの一部の機能はこのトレイトに依存しているため、このトレイトを元の場所に残しておくことが重要です。

<a name="creating-tests"></a>
<!-- ## Creating Tests -->
## Creating Tests

<!-- To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory: -->
新しいテスト ケースを作成するには、`make:test` Artisan コマンドを使用します。デフォルトでは、テストは `tests/Feature` ディレクトリに配置されます。

```shell
php artisan make:test UserTest
```

<!-- If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command: -->
`tests/Unit` ディレクトリ内にテストを作成したい場合は、`make:test` コマンドを実行するときに `--unit` オプションを使用できます。

```shell
php artisan make:test UserTest --unit
```

<!-- If you would like to create a [Pest PHP](https://pestphp.com) test, you may provide the `--pest` option to the `make:test` command: -->
[Pest PHP](https://pestphp.com) テストを作成したい場合は、`--pest` オプションを `make:test` コマンドに指定できます。

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!NOTE]
> テスト スタブは、[stub publishing](/docs/10.x/artisan#stub-customization) を使用してカスタマイズできます。

<!-- Once the test has been generated, you may define test methods as you normally would using [PHPUnit](https://phpunit.de). To run your tests, execute the `vendor/bin/phpunit` or `php artisan test` command from your terminal: -->
テストが生成されたら、通常 [PHPUnit](https://phpunit.de) を使用するのと同じようにテスト メソッドを定義できます。テストを実行するには、端末から `vendor/bin/phpunit` または `php artisan test` コマンドを実行します。

```
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
<!-- ## Running Tests -->
## Running Tests

<!-- As mentioned previously, once you've written tests, you may run them using `phpunit`: -->
前述したように、テストを作成したら、`phpunit` を使用してテストを実行できます。

```shell
./vendor/bin/phpunit
```

<!-- In addition to the `phpunit` command, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging: -->
`phpunit` コマンドに加えて、`test` Artisan コマンドを使用してテストを実行することもできます。 Artisan テスト ランナーは、開発とデバッグを容易にするために詳細なテスト レポートを提供します。

```shell
php artisan test
```

<!-- Any arguments that can be passed to the `phpunit` command may also be passed to the Artisan `test` command: -->
`phpunit` コマンドに渡すことができる引数は、Artisan `test` コマンドにも渡すことができます。

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
<!-- ### Running Tests in Parallel -->
### Running Tests in Parallel

<!-- By default, Laravel and PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, you should install the `brianium/paratest` Composer package as a "dev" dependency. Then, include the `--parallel` option when executing the `test` Artisan command: -->
デフォルトでは、Laravel と PHPUnit は単一プロセス内でテストを順番に実行します。ただし、複数のプロセス間でテストを同時に実行すると、テストの実行にかかる時間を大幅に短縮できる場合があります。まず、`brianium/paratest` Composer パッケージを「dev」依存関係としてインストールする必要があります。次に、`test` Artisan コマンドを実行するときに、`--parallel` オプションを含めます。

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

<!-- By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option: -->
デフォルトでは、Laravel はマシン上で利用可能な CPU コアと同じ数のプロセスを作成します。ただし、`--processes` オプションを使用してプロセスの数を調整できます。

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> テストを並行して実行する場合、一部の PHPUnit オプション (`--do-not-cache-result` など) が使用できない場合があります。

<a name="parallel-testing-and-databases"></a>
<!-- #### Parallel Testing and Databases -->
#### Parallel Testing and Databases

<!-- As long as you have configured a primary database connection, Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases. -->
プライマリデータベース接続を設定している限り、Laravel はテストを実行している並列プロセスごとにテストデータベースの作成と移行を自動的に処理します。テスト データベースには、プロセスごとに一意のプロセス トークンが接尾辞として付けられます。たとえば、2 つの並列テスト プロセスがある場合、Laravel は `your_db_test_1` および `your_db_test_2` テスト データベースを作成して使用します。

<!-- By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option: -->
デフォルトでは、テスト データベースは `test` Artisan コマンドの呼び出し間で保持されるため、後続の `test` 呼び出しで再度使用できます。ただし、`--recreate-databases` オプションを使用してそれらを再作成することはできます。

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
<!-- #### Parallel Testing Hooks -->
#### Parallel Testing Hooks

<!-- Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes. -->
場合によっては、アプリケーションのテストで使用される特定のリソースを、複数のテスト プロセスで安全に使用できるように準備する必要がある場合があります。

<!-- Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively: -->
`ParallelTesting` ファサードを使用すると、プロセスまたはテスト ケースの `setUp` および `tearDown` で実行されるコードを指定できます。指定されたクロージャは、それぞれプロセス トークンと現在のテスト ケースを含む `$token` 変数と `$testCase` 変数を受け取ります。

```
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
<!-- #### Accessing the Parallel Testing Token -->
#### Accessing the Parallel Testing Token

<!-- If you would like to access the current parallel process "token" from any other location in your application's test code, you may use the `token` method. This token is a unique, string identifier for an individual test process and may be used to segment resources across parallel test processes. For example, Laravel automatically appends this token to the end of the test databases created by each parallel testing process: -->
アプリケーションのテスト コード内の他の場所から現在の並列プロセスの「トークン」にアクセスしたい場合は、`token` メソッドを使用できます。このトークンは、個々のテスト プロセスの一意の文字列識別子であり、並列テスト プロセス全体でリソースをセグメント化するために使用できます。たとえば、Laravel は、各並列テスト プロセスによって作成されたテスト データベースの末尾にこのトークンを自動的に追加します。

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
<!-- ### Reporting Test Coverage -->
### Reporting Test Coverage

> [!WARNING]
> この機能には、[Xdebug](https://xdebug.org) または [PCOV](https://pecl.php.net/package/pcov) が必要です。

<!-- When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command: -->
アプリケーション テストを実行するとき、テスト ケースが実際にアプリケーション コードをカバーしているかどうか、およびテストの実行時に使用されるアプリケーション コードの量を確認することができます。これを実現するには、`test` コマンドを呼び出すときに `--coverage` オプションを指定できます。

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
<!-- #### Enforcing a Minimum Coverage Threshold -->
#### Enforcing a Minimum Coverage Threshold

<!-- You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met: -->
`--min` オプションを使用して、アプリケーションの最小テスト カバレッジしきい値を定義できます。このしきい値が満たされていない場合、テスト スイートは失敗します。

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
<!-- ### Profiling Tests -->
### Profiling Tests

<!-- The Artisan test runner also includes a convenient mechanism for listing your application's slowest tests. Invoke the `test` command with the `--profile` option to be presented with a list of your ten slowest tests, allowing you to easily investigate which tests can be improved to speed up your test suite: -->
Artisan テスト ランナーには、アプリケーションの最も遅いテストをリストするための便利なメカニズムも含まれています。 `--profile` オプションを指定して `test` コマンドを呼び出すと、最も遅い 10 個のテストのリストが表示され、テスト スイートを高速化するためにどのテストを改善できるかを簡単に調査できます。

```shell
php artisan test --profile
```

