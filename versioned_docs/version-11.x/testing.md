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

<!-- Laravel is built with testing in mind. In fact, support for testing with [Pest](https://pestphp.com) and [PHPUnit](https://phpunit.de) is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications. -->
Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)을 이용한 테스트가 기본적으로 지원되며, 애플리케이션에는 이미 `phpunit.xml` 파일이 준비되어 있습니다. 또한, Laravel은 애플리케이션을 보다 표현적으로 테스트할 수 있도록 다양한 헬퍼 메서드도 제공합니다.

<!-- By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services. -->
기본적으로 여러분의 애플리케이션 `tests` 디렉터리에는 `Feature`와 `Unit`이라는 두 개의 하위 디렉터리가 존재합니다. 유닛 테스트(Unit test)는 코드의 아주 작은, 고립된 부분을 검증하는 테스트입니다. 대부분의 유닛 테스트는 하나의 메서드에 초점을 맞추는 경우가 많습니다. "Unit" 테스트 디렉터리에 있는 테스트들은 Laravel 애플리케이션을 부팅하지 않으므로, 데이터베이스나 프레임워크의 기타 서비스에 접근할 수 없습니다.

<!-- Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.** -->
피처 테스트(Feature test)는 여러 객체 간의 상호작용이나, JSON 엔드포인트를 포함한 전체 HTTP 요청 등 코드의 더 넓은 영역을 테스트할 수 있습니다. **일반적으로는 대부분의 테스트가 피처 테스트여야 하며, 이와 같은 테스트는 시스템 전체가 의도한 대로 동작하는지 가장 효과적으로 확인할 수 있습니다.**

<!-- An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` commands to run your tests. -->
`ExampleTest.php` 파일이 `Feature`와 `Unit` 테스트 디렉터리 각각에 제공됩니다. 새로 Laravel 애플리케이션을 설치했다면, `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
<!-- ## Environment -->
## Environment

<!-- When running tests, Laravel will automatically set the [configuration environment](/docs/11.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver so that no session or cache data will be persisted while testing. -->
테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수로 인해 [configuration environment](/docs/11.x/configuration#environment-configuration)이 자동으로 `testing`으로 지정됩니다. Laravel은 세션 및 캐시 드라이버도 자동으로 `array`로 설정하므로, 테스트 중에는 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

<!-- You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests! -->
필요에 따라 자유롭게 추가적인 테스트 환경 설정값을 지정할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` 아티즌 명령어로 설정 캐시를 비워야 합니다!

<a name="the-env-testing-environment-file"></a>
<!-- #### The `.env.testing` Environment File -->
#### The `.env.testing` Environment File

<!-- In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running Pest and PHPUnit tests or executing Artisan commands with the `--env=testing` option. -->
추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수도 있습니다. 이 파일은 Pest와 PHPUnit 테스트를 실행하거나, `--env=testing` 옵션과 함께 아티즌 명령어를 사용할 때 `.env` 파일 대신 적용됩니다.

<a name="creating-tests"></a>
<!-- ## Creating Tests -->
## Creating Tests

<!-- To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory: -->
새로운 테스트 케이스를 만들기 위해서는 `make:test` 아티즌 명령어를 사용하면 됩니다. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다.

```shell
php artisan make:test UserTest
```

<!-- If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command: -->
`tests/Unit` 디렉터리에 테스트를 생성하고 싶다면, `make:test` 명령어 실행 시 `--unit` 옵션을 추가하면 됩니다.

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁은 [stub publishing](/docs/11.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<!-- Once the test has been generated, you may define test as you normally would using Pest or PHPUnit. To run your tests, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` command from your terminal: -->
테스트가 생성되면, Pest나 PHPUnit을 이용해 일반적으로 테스트를 작성하면 됩니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 사용하면 됩니다.

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
> 테스트 클래스에서 직접 `setUp` 또는 `tearDown` 메서드를 정의했다면, 반드시 각각의 메서드에서 부모 클래스의 `parent::setUp()` 또는 `parent::tearDown()`을 호출해야 합니다. 일반적으로는 여러분이 작성한 `setUp` 메서드의 시작 부분에서 `parent::setUp()`을, `tearDown` 메서드의 끝 부분에서 `parent::tearDown()`을 호출해야 합니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- As mentioned previously, once you've written tests, you may run them using `pest` or `phpunit`: -->
앞서 설명한 것처럼, 테스트를 작성했다면 `pest` 또는 `phpunit`을 사용할 수 있습니다.

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

<!-- In addition to the `pest` or `phpunit` commands, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging: -->
`pest` 또는 `phpunit` 명령어 외에도, `test` 아티즌 명령어로 테스트를 실행할 수 있습니다. 아티즌 테스트 러너는 개발과 디버깅을 쉽게 할 수 있도록 자세한 테스트 리포트를 제공합니다.

```shell
php artisan test
```

<!-- Any arguments that can be passed to the `pest` or `phpunit` commands may also be passed to the Artisan `test` command: -->
`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인자(argument)는 아티즌 `test` 명령어에도 그대로 사용할 수 있습니다.

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
<!-- ### Running Tests in Parallel -->
### Running Tests in Parallel

<!-- By default, Laravel and Pest / PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, you should install the `brianium/paratest` Composer package as a "dev" dependency. Then, include the `--parallel` option when executing the `test` Artisan command: -->
기본적으로 Laravel과 Pest / PHPUnit은 하나의 프로세스에서 테스트를 순차적으로 실행합니다. 하지만 여러 프로세스에서 테스트를 동시에 실행하면 전체 테스트 시간을 크게 줄일 수 있습니다. 이를 위해서는 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 먼저 설치해야 합니다. 그런 다음, 아티즌 `test` 명령어 실행 시 `--parallel` 옵션을 추가하세요.

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

<!-- By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option: -->
기본적으로 Laravel은 여러분의 컴퓨터에 있는 CPU 코어 개수만큼 프로세스를 생성합니다. 필요하다면 `--processes` 옵션으로 프로세스 수를 직접 지정할 수도 있습니다.

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬로 테스트를 실행할 때는 일부 Pest / PHPUnit 옵션(예: `--do-not-cache-result`)을 사용할 수 없을 수 있습니다.

<a name="parallel-testing-and-databases"></a>
<!-- #### Parallel Testing and Databases -->
#### Parallel Testing and Databases

<!-- As long as you have configured a primary database connection, Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases. -->
기본 데이터베이스 연결이 구성되어 있다면, Laravel은 테스트 실행 중 각 병렬 프로세스별로 테스트용 데이터베이스를 생성하고 마이그레이션도 자동으로 수행합니다. 각 테스트 데이터베이스는 프로세스마다 고유한 토큰이 접미사로 붙어 구분됩니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 실행되는 경우 Laravel은 `your_db_test_1` 및 `your_db_test_2`와 같은 테스트 데이터베이스를 생성해 사용합니다.

<!-- By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option: -->
기본적으로 테스트 데이터베이스는 `test` 아티즌 명령어를 여러 번 실행해도 남아있기 때문에 이후 `test` 호출에서 재사용됩니다. 하지만 `--recreate-databases` 옵션을 사용하면 데이터베이스를 새로 생성할 수 있습니다.

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
<!-- #### Parallel Testing Hooks -->
#### Parallel Testing Hooks

<!-- Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes. -->
때때로, 애플리케이션 테스트에서 여러 테스트 프로세스에서 안전하게 사용할 리소스를 미리 준비해야 할 수도 있습니다.

<!-- Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively: -->
`ParallelTesting` 파사드를 사용하면 프로세스나 테스트 케이스의 `setUp`, `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 이때 전달되는 클로저는 프로세스 토큰 `$token`과 현재 테스트 케이스 `$testCase`를 인자로 받아 활용할 수 있습니다.

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
테스트 코드 내에서 현재 병렬 프로세스의 "토큰"을 사용하고 싶다면, `token` 메서드를 사용하면 됩니다. 이 토큰은 각 테스트 프로세스를 식별하는 고유한 문자열이며, 병렬 테스트 프로세스 간의 리소스를 구분하는 데 사용할 수 있습니다. 예를 들어, Laravel은 이 토큰을 각 병렬 테스트 프로세스에서 생성된 테스트 데이터베이스명 끝에 자동으로 붙여줍니다.

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
<!-- ### Reporting Test Coverage -->
### Reporting Test Coverage

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 혹은 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

<!-- When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command: -->
애플리케이션 테스트를 실행할 때, 실제로 테스트가 애플리케이션 코드를 얼마나 커버하는지 확인하고 싶을 수 있습니다. 이를 위해서 `test` 명령어 실행 시 `--coverage` 옵션을 사용할 수 있습니다.

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
<!-- #### Enforcing a Minimum Coverage Threshold -->
#### Enforcing a Minimum Coverage Threshold

<!-- You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met: -->
애플리케이션에 대해 최소 테스트 커버리지 임계값을 지정하고 싶다면 `--min` 옵션을 사용할 수 있습니다. 임계값을 충족하지 못하면 테스트가 실패합니다.

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
<!-- ### Profiling Tests -->
### Profiling Tests

<!-- The Artisan test runner also includes a convenient mechanism for listing your application's slowest tests. Invoke the `test` command with the `--profile` option to be presented with a list of your ten slowest tests, allowing you to easily investigate which tests can be improved to speed up your test suite: -->
아티즌 테스트 러너에는 느린 테스트를 찾기 위한 편리한 기능도 포함되어 있습니다. `--profile` 옵션과 함께 `test` 명령어를 실행하면, 가장 느린 테스트 10개의 목록이 표시되어 전체 테스트 속도를 개선할 수 있는 부분을 손쉽게 찾을 수 있습니다.

```shell
php artisan test --profile
```
