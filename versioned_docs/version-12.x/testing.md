<!-- # Testing: Getting Started -->
# Testing: Getting Started

- [Introduction](#introduction)
- [Environment](#environment)
- [Creating Tests](#creating-tests)
- [Running Tests](#running-tests)
    - [Running Tests in Parallel](#running-tests-in-parallel)
    - [Reporting Test Coverage](#reporting-test-coverage)
    - [Profiling Tests](#profiling-tests)
- [Configuration Caching](#configuration-caching)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel is built with testing in mind. In fact, support for testing with [Pest](https://pestphp.com) and [PHPUnit](https://phpunit.de) is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications. -->
Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com) 및 [PHPUnit](https://phpunit.de)을 활용한 테스트가 기본적으로 지원되며, `phpunit.xml` 파일도 이미 애플리케이션에 설정되어 있습니다. 프레임워크는 애플리케이션을 효과적으로 테스트할 수 있도록 다양한 헬퍼 메서드도 제공합니다.

<!-- By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services. -->
기본적으로 애플리케이션의 `tests` 디렉토리에는 `Feature`와 `Unit`이라는 두 개의 하위 디렉토리가 존재합니다. 단위 테스트(Unit test)는 코드의 매우 작은, 분리된 부분에 집중하는 테스트입니다. 대부분의 경우 단위 테스트는 하나의 메서드만을 검증합니다. "Unit" 테스트 디렉토리에 위치한 테스트들은 Laravel 애플리케이션을 부트하지 않으므로, 애플리케이션의 데이터베이스나 기타 프레임워크 서비스에 접근할 수 없습니다.

<!-- Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.** -->
기능 테스트(Feature test)는 여러 오브젝트 간의 상호작용이나, 심지어 전체 HTTP 요청이 JSON 엔드포인트에 도달하는 모습까지 좀 더 큰 코드 범위를 검증할 수 있습니다. **일반적으로 테스트의 대부분은 기능 테스트로 작성하는 것이 좋습니다. 이러한 테스트가 시스템 전체가 의도한 대로 동작하는지 가장 높은 신뢰도로 보장합니다.**

<!-- An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` commands to run your tests. -->
`Feature` 및 `Unit` 테스트 디렉토리 모두에 `ExampleTest.php` 파일이 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는, `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
<!-- ## Environment -->
## Environment

<!-- When running tests, Laravel will automatically set the [configuration environment](/docs/12.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver so that no session or cache data will be persisted while testing. -->
테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 [configuration environment](/docs/12.x/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 세션과 캐시도 `array` 드라이버로 자동 설정하여, 테스트 실행 중에는 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

<!-- You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests! -->
필요에 따라 기타 테스트 환경 관련 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 지정할 수 있고, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 지워야 합니다!

<a name="the-env-testing-environment-file"></a>
<!-- #### The `.env.testing` Environment File -->
#### The `.env.testing` Environment File

<!-- In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running Pest and PHPUnit tests or executing Artisan commands with the `--env=testing` option. -->
추가로, 프로젝트의 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest와 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션과 함께 Artisan 명령어를 사용할 때 `.env` 파일 대신 참조됩니다.

<a name="creating-tests"></a>
<!-- ## Creating Tests -->
## Creating Tests

<!-- To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory: -->
새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용합니다. 기본적으로 생성되는 테스트는 `tests/Feature` 디렉토리에 위치합니다:

```shell
php artisan make:test UserTest
```

<!-- If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command: -->
`tests/Unit` 디렉토리 내에 테스트를 생성하고 싶다면, `make:test` 명령어를 실행할 때 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁은 [stub publishing](/docs/12.x/artisan#stub-customization)을 통해 수정할 수 있습니다.

<!-- Once the test has been generated, you may define test as you normally would using Pest or PHPUnit. To run your tests, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` command from your terminal: -->
테스트가 생성되면, Pest 또는 PHPUnit을 이용해 테스트를 작성할 수 있습니다. 테스트 실행은 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어로 수행합니다:

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
> 테스트 클래스 내부에 직접 `setUp` / `tearDown` 메서드를 정의한다면, 반드시 상위 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 일반적으로는 `setUp`에서 가장 처음 `parent::setUp()`을, `tearDown`에서 마지막에 `parent::tearDown()`을 호출하는 것이 좋습니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- As mentioned previously, once you've written tests, you may run them using `pest` or `phpunit`: -->
앞서 설명한 대로, 테스트를 작성한 후에는 `pest` 또는 `phpunit`을 사용해 테스트를 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

<!-- In addition to the `pest` or `phpunit` commands, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging: -->
`pest`나 `phpunit` 명령 외에도, `test` Artisan 명령어로도 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발과 디버깅을 더 용이하게 해주는 상세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

<!-- Any arguments that can be passed to the `pest` or `phpunit` commands may also be passed to the Artisan `test` command: -->
`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 그대로 사용할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
<!-- ### Running Tests in Parallel -->
### Running Tests in Parallel

<!-- By default, Laravel and Pest / PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, you should install the `brianium/paratest` Composer package as a "dev" dependency. Then, include the `--parallel` option when executing the `test` Artisan command: -->
기본적으로 Laravel과 Pest / PHPUnit은 한 개의 프로세스 안에서 순차적으로 테스트를 실행합니다. 하지만 테스트를 여러 프로세스에서 동시에 실행하면 테스트 소요 시간을 크게 단축할 수 있습니다. 먼저, `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그리고 `test` Artisan 명령어 실행 시 `--parallel` 옵션을 추가합니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

<!-- By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option: -->
기본적으로 Laravel은 현재 머신의 CPU 코어 수 만큼 프로세스를 생성합니다. 필요하다면 `--processes` 옵션으로 프로세스 수를 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬 테스트 실행 시, 일부 Pest / PHPUnit 옵션(`--do-not-cache-result` 등)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
<!-- #### Parallel Testing and Databases -->
#### Parallel Testing and Databases

<!-- As long as you have configured a primary database connection, Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases. -->
기본 데이터베이스 연결이 구성되어 있다면, Laravel은 테스트를 병렬로 실행하는 각 프로세스마다 자동으로 별도의 테스트 데이터베이스를 생성 및 마이그레이션합니다. 테스트 데이터베이스 이름은 각 프로세스 별로 고유한 토큰이 접미사로 붙으며 구분됩니다. 예를 들어 두 개의 병렬 테스트 프로세스가 있다면, Laravel은 `your_db_test_1`과 `your_db_test_2` 데이터베이스를 생성하여 사용합니다.

<!-- By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option: -->
기본적으로 테스트 데이터베이스는 여러 번의 `test` Artisan 명령 호출 사이에도 유지되어, 이후 `test` 실행에서도 재사용할 수 있습니다. 하지만, 언제든지 `--recreate-databases` 옵션으로 데이터베이스를 새로 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
<!-- #### Parallel Testing Hooks -->
#### Parallel Testing Hooks

<!-- Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes. -->
가끔은 애플리케이션 테스트에서 사용하는 특정 자원을 여러 테스트 프로세스에서 안전하게 사용할 수 있도록 미리 준비해야 할 경우가 있습니다.

<!-- Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively: -->
`ParallelTesting` 파사드를 사용하면, 프로세스 또는 테스트 케이스별 `setUp`과 `tearDown`에 실행할 코드를 지정할 수 있습니다. 전달되는 클로저는 프로세스 토큰을 담은 `$token` 변수와 현재 테스트 케이스를 나타내는 `$testCase` 변수를 인자로 받습니다:

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
<!-- #### Accessing the Parallel Testing Token -->
#### Accessing the Parallel Testing Token

<!-- If you would like to access the current parallel process "token" from any other location in your application's test code, you may use the `token` method. This token is a unique, string identifier for an individual test process and may be used to segment resources across parallel test processes. For example, Laravel automatically appends this token to the end of the test databases created by each parallel testing process: -->
애플리케이션의 테스트 코드 다른 어느 곳에서든, 현재 병렬 프로세스의 "토큰"에 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스를 식별하는 고유한 문자열이며, 병렬 테스트 실행 환경에서 자원을 구분 관리하는 데 사용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스에서 생성하는 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 붙입니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
<!-- ### Reporting Test Coverage -->
### Reporting Test Coverage

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

<!-- When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command: -->
애플리케이션 테스트를 실행할 때 실제로 테스트 코드가 애플리케이션 코드를 얼마나 커버하고 있는지, 각 테스트가 얼마나 많은 코드를 사용하는지 확인하고 싶을 수 있습니다. 이를 위해, `test` 명령어 실행 시 `--coverage` 옵션을 제공할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
<!-- #### Enforcing a Minimum Coverage Threshold -->
#### Enforcing a Minimum Coverage Threshold

<!-- You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met: -->
`--min` 옵션을 사용하면 애플리케이션의 최소 테스트 커버리지 기준을 설정할 수 있습니다. 지정한 기준에 미치지 못하면 테스트가 실패합니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
<!-- ### Profiling Tests -->
### Profiling Tests

<!-- The Artisan test runner also includes a convenient mechanism for listing your application's slowest tests. Invoke the `test` command with the `--profile` option to be presented with a list of your ten slowest tests, allowing you to easily investigate which tests can be improved to speed up your test suite: -->
Artisan 테스트 러너는 애플리케이션에서 가장 느린 테스트 목록을 확인할 수 있는 편리한 기능도 제공합니다. `test` 명령어에 `--profile` 옵션을 추가하면, 가장 오래 걸리는 상위 10개의 테스트 목록을 확인할 수 있어, 테스트 속도를 향상시켜야 하는 부분을 쉽게 파악할 수 있습니다:

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- When running tests, Laravel boots the application for each individual test method.  Without a cached configuration file, each configuration file in your application must be loaded at the start of a test. To build the configuration once and re-use it for all tests in a single run, you may use the `Illuminate\Foundation\Testing\WithCachedConfig` trait: -->
테스트를 실행할 때, Laravel은 개별 테스트 메서드마다 애플리케이션을 부트합니다. 설정 파일이 캐시되어 있지 않다면, 테스트 시작 시마다 모든 설정 파일을 다시 읽어야 하므로 느려질 수 있습니다. 한 번 설정을 만들어 모든 테스트에서 재사용하고 싶다면, `Illuminate\Foundation\Testing\WithCachedConfig` 트레이트를 사용할 수 있습니다:

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
