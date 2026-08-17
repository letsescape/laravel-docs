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
Laravel은 테스트를 염두에 두고 만들어졌습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)을 사용한 테스트 지원이 기본으로 포함되어 있으며, 애플리케이션을 위한 `phpunit.xml` 파일도 이미 설정되어 있습니다. 또한 프레임워크에는 애플리케이션을 표현력 있게 테스트할 수 있는 편리한 헬퍼 메서드가 함께 제공됩니다.

<!-- By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services. -->
기본적으로 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 디렉터리가 포함되어 있습니다. 단위 테스트는 코드의 매우 작고 격리된 부분에 집중하는 테스트입니다. 실제로 대부분의 단위 테스트는 하나의 메서드에 집중하는 경우가 많습니다. "Unit" 테스트 디렉터리 안의 테스트는 Laravel 애플리케이션을 부팅하지 않으므로 애플리케이션의 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

<!-- Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.** -->
기능 테스트는 여러 객체가 서로 상호작용하는 방식이나 JSON 엔드포인트로 보내는 전체 HTTP 요청까지 포함하여 코드의 더 큰 부분을 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트여야 합니다. 이런 유형의 테스트는 시스템 전체가 의도한 대로 동작하고 있다는 가장 큰 확신을 제공합니다.**

<!-- An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` commands to run your tests. -->
`Feature`와 `Unit` 테스트 디렉터리에는 모두 `ExampleTest.php` 파일이 제공됩니다. 새 Laravel 애플리케이션을 설치한 후에는 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 실행할 수 있습니다.

<a name="environment"></a>
<!-- ## Environment -->
## Environment

<!-- When running tests, Laravel will automatically set the [configuration environment](/docs/13.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver so that no session or cache data will be persisted while testing. -->
테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 때문에 [configuration environment](/docs/13.x/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 Laravel은 세션과 캐시를 자동으로 `array` 드라이버로 설정하여 테스트 중에는 세션이나 캐시 데이터가 유지되지 않도록 합니다.

<!-- You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests! -->
필요하다면 다른 테스트 환경 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 지워야 합니다!

<a name="the-env-testing-environment-file"></a>
<!-- #### The `.env.testing` Environment File -->
#### The `.env.testing` Environment File

<!-- In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running Pest and PHPUnit tests or executing Artisan commands with the `--env=testing` option. -->
추가로 프로젝트 루트에 `.env.testing` 파일을 만들 수 있습니다. 이 파일은 Pest와 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션으로 Artisan 명령어를 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
<!-- ## Creating Tests -->
## Creating Tests

<!-- To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory: -->
새 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용합니다. 기본적으로 테스트는 `tests/Feature` 디렉터리에 배치됩니다.

```shell
php artisan make:test UserTest
```

<!-- If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command: -->
`tests/Unit` 디렉터리 안에 테스트를 생성하고 싶다면 `make:test` 명령어를 실행할 때 `--unit` 옵션을 사용할 수 있습니다.

```shell
php artisan make:test UserTest --unit
```

<!-- If you have a test class that mostly relies on Laravel's testing features, but a specific test method does not need the framework booted, you may apply the `#[UnitTest]` attribute to that method to skip booting the application for just that test. -->
Laravel의 테스트 기능에 대부분 의존하는 테스트 클래스가 있지만, 특정 테스트 메서드에서는 프레임워크를 부팅할 필요가 없다면 해당 메서드에 `#[UnitTest]` 속성을 적용하여 그 테스트에서만 애플리케이션 부팅을 건너뛸 수 있습니다.

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
> 테스트 스텁은 [stub publishing](/docs/13.x/artisan#stub-customization)를 사용하여 사용자 정의할 수 있습니다.

<!-- Once the test has been generated, you may define test as you normally would using Pest or PHPUnit. To run your tests, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` command from your terminal: -->
테스트가 생성되면 평소처럼 Pest 또는 PHPUnit을 사용하여 테스트를 정의할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행합니다.

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
> 테스트 클래스 안에서 직접 `setUp` / `tearDown` 메서드를 정의하는 경우, 부모 클래스의 해당 `parent::setUp()` / `parent::tearDown()` 메서드를 반드시 호출해야 합니다. 일반적으로 직접 작성한 `setUp` 메서드의 시작 부분에서 `parent::setUp()`을 호출하고, `tearDown` 메서드의 끝부분에서 `parent::tearDown()`을 호출해야 합니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- As mentioned previously, once you've written tests, you may run them using `pest` or `phpunit`: -->
앞서 언급했듯이 테스트를 작성한 후에는 `pest` 또는 `phpunit`을 사용하여 실행할 수 있습니다.

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

<!-- In addition to the `pest` or `phpunit` commands, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging: -->
`pest` 또는 `phpunit` 명령어 외에도 `test` Artisan 명령어를 사용하여 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발과 디버깅을 더 쉽게 할 수 있도록 자세한 테스트 보고서를 제공합니다.

```shell
php artisan test
```

<!-- Any arguments that can be passed to the `pest` or `phpunit` commands may also be passed to the Artisan `test` command: -->
`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 전달할 수 있습니다.

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
<!-- ### Running Tests in Parallel -->
### Running Tests in Parallel

<!-- By default, Laravel and Pest / PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, you should install the `brianium/paratest` Composer package as a "dev" dependency. Then, include the `--parallel` option when executing the `test` Artisan command: -->
기본적으로 Laravel과 Pest / PHPUnit은 테스트를 단일 프로세스 안에서 순차적으로 실행합니다. 하지만 여러 프로세스에서 동시에 테스트를 실행하면 테스트 실행 시간을 크게 줄일 수 있습니다. 시작하려면 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그런 다음 `test` Artisan 명령어를 실행할 때 `--parallel` 옵션을 포함합니다.

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

<!-- By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option: -->
기본적으로 Laravel은 사용 중인 머신에서 사용할 수 있는 CPU 코어 수만큼 프로세스를 생성합니다. 하지만 `--processes` 옵션을 사용하여 프로세스 수를 조정할 수 있습니다.

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 테스트를 병렬로 실행할 때는 일부 Pest / PHPUnit 옵션(예: `--do-not-cache-result`)을 사용할 수 없을 수 있습니다.

<a name="parallel-testing-and-databases"></a>
<!-- #### Parallel Testing and Databases -->
#### Parallel Testing and Databases

<!-- As long as you have configured a primary database connection, Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases. -->
기본 데이터베이스 연결을 설정해 두었다면, Laravel은 테스트를 실행하는 각 병렬 프로세스마다 테스트 데이터베이스를 생성하고 마이그레이션하는 작업을 자동으로 처리합니다. 테스트 데이터베이스에는 프로세스마다 고유한 프로세스 토큰이 접미사로 붙습니다. 예를 들어 병렬 테스트 프로세스가 두 개라면 Laravel은 `your_db_test_1`과 `your_db_test_2` 테스트 데이터베이스를 생성하고 사용합니다.

<!-- By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option: -->
기본적으로 테스트 데이터베이스는 `test` Artisan 명령어 호출 사이에도 유지되므로 이후 `test` 실행에서 다시 사용할 수 있습니다. 하지만 `--recreate-databases` 옵션을 사용하면 테스트 데이터베이스를 다시 생성할 수 있습니다.

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
<!-- #### Parallel Testing Hooks -->
#### Parallel Testing Hooks

<!-- Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes. -->
때로는 여러 테스트 프로세스가 안전하게 사용할 수 있도록 애플리케이션 테스트에서 사용하는 특정 리소스를 준비해야 할 수 있습니다.

<!-- Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively: -->
`ParallelTesting` 파사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 전달된 클로저는 각각 프로세스 토큰과 현재 테스트 케이스를 담고 있는 `$token` 및 `$testCase` 변수를 받습니다.

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
애플리케이션 테스트 코드의 다른 위치에서 현재 병렬 프로세스 "토큰"에 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스를 위한 고유한 문자열 식별자이며, 병렬 테스트 프로세스 간에 리소스를 분리하는 데 사용할 수 있습니다. 예를 들어 Laravel은 각 병렬 테스트 프로세스가 생성한 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 추가합니다.

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
<!-- ### Reporting Test Coverage -->
### Reporting Test Coverage

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

<!-- When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command: -->
애플리케이션 테스트를 실행할 때 테스트 케이스가 실제로 애플리케이션 코드를 커버하고 있는지, 그리고 테스트 실행 중 애플리케이션 코드가 얼마나 사용되는지 확인하고 싶을 수 있습니다. 이를 수행하려면 `test` 명령어를 호출할 때 `--coverage` 옵션을 제공하면 됩니다.

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
<!-- #### Enforcing a Minimum Coverage Threshold -->
#### Enforcing a Minimum Coverage Threshold

<!-- You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met: -->
`--min` 옵션을 사용하여 애플리케이션의 최소 테스트 커버리지 임계값을 정의할 수 있습니다. 이 임계값을 충족하지 못하면 테스트 스위트가 실패합니다.

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
<!-- ### Profiling Tests -->
### Profiling Tests

<!-- The Artisan test runner also includes a convenient mechanism for listing your application's slowest tests. Invoke the `test` command with the `--profile` option to be presented with a list of your ten slowest tests, allowing you to easily investigate which tests can be improved to speed up your test suite: -->
Artisan 테스트 러너에는 애플리케이션에서 가장 느린 테스트를 나열하는 편리한 기능도 포함되어 있습니다. `--profile` 옵션과 함께 `test` 명령어를 호출하면 가장 느린 테스트 10개의 목록이 표시되므로, 테스트 스위트의 실행 속도를 높이기 위해 어떤 테스트를 개선할 수 있는지 쉽게 조사할 수 있습니다.

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- When running tests, Laravel boots the application for each individual test method. Without a cached configuration file, each configuration file in your application must be loaded at the start of a test. To build the configuration once and re-use it for all tests in a single run, you may use the `Illuminate\Foundation\Testing\WithCachedConfig` trait: -->
테스트를 실행할 때 Laravel은 각 테스트 메서드마다 애플리케이션을 부팅합니다. 캐시된 설정 파일이 없으면 테스트를 시작할 때마다 애플리케이션의 각 설정 파일을 로드해야 합니다. 설정을 한 번 빌드한 뒤 한 번의 실행에서 모든 테스트에 재사용하려면 `Illuminate\Foundation\Testing\WithCachedConfig` 트레이트를 사용할 수 있습니다.

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
