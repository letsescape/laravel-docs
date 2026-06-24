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
Laravel은 처음부터 테스트를 염두에 두고 설계된 프레임워크입니다. 실제로 PHPUnit을 이용한 테스트 기능이 기본적으로 내장되어 있으며, 애플리케이션에 이미 `phpunit.xml` 파일이 설정되어 있습니다. 또한 프레임워크에는 애플리케이션 테스트를 보다 직관적이고 쉽게 작성할 수 있도록 다양한 헬퍼 메서드도 제공됩니다.

<!-- By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services. -->
기본적으로 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 하위 디렉터리가 존재합니다. 단위 테스트(Unit test)는 코드의 아주 작은 일부, 보통 하나의 메서드에만 집중하는 테스트입니다. "Unit" 테스트 디렉터리 내의 테스트들은 Laravel 애플리케이션을 부팅하지 않으므로, 애플리케이션의 데이터베이스나 프레임워크 서비스에 접근할 수 없습니다.

<!-- Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.** -->
기능 테스트(Feature test)는 여러 객체 간의 상호작용이나 전체 HTTP 요청, JSON 엔드포인트까지 포함해 더 넓은 범위의 코드를 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트(Feature test)로 작성하는 것이 좋으며, 이 유형의 테스트가 시스템 전체가 의도대로 작동하고 있는지 가장 높은 신뢰를 제공합니다.**

<!-- An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/phpunit` or `php artisan test` commands to run your tests. -->
`Feature`와 `Unit` 테스트 디렉터리 모두에 기본적으로 `ExampleTest.php` 파일이 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행해 테스트를 수행할 수 있습니다.

<a name="environment"></a>
<!-- ## Environment -->
## Environment

<!-- When running tests, Laravel will automatically set the [configuration environment](/docs/10.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver so that no session or cache data will be persisted while testing. -->
테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 [configuration environment](/docs/10.x/configuration#environment-configuration)이 자동으로 `testing`으로 전환됩니다. 또한 세션과 캐시 설정이 자동으로 `array` 드라이버로 변경되어, 테스트 중에는 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

<!-- You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests! -->
필요하다면 추가적인 테스트 환경 설정값도 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트 실행 전에 `config:clear` 아티즌 명령어로 설정 캐시를 반드시 비워야 합니다.

<a name="the-env-testing-environment-file"></a>
<!-- #### The `.env.testing` Environment File -->
#### The `.env.testing` Environment File

<!-- In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running PHPUnit tests or executing Artisan commands with the `--env=testing` option. -->
추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션과 함께 아티즌 명령어를 실행할 때, `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
<!-- #### The `CreatesApplication` Trait -->
#### The `CreatesApplication` Trait

<!-- Laravel includes a `CreatesApplication` trait that is applied to your application's base `TestCase` class. This trait contains a `createApplication` method that bootstraps the Laravel application before running your tests. It's important that you leave this trait at its original location as some features, such as Laravel's parallel testing feature, depend on it. -->
Laravel에는 애플리케이션의 기본 `TestCase` 클래스에 적용된 `CreatesApplication` 트레이트(trait)가 포함되어 있습니다. 이 트레이트는 테스트 실행 전에 Laravel 애플리케이션을 부트스트랩하는 `createApplication` 메서드를 가지고 있습니다. Laravel의 병렬 테스트 기능 등 일부 주요 기능은 이 트레이트의 기존 위치에 의존하므로, 이 트레이트는 원래 위치 그대로 두어야 합니다.

<a name="creating-tests"></a>
<!-- ## Creating Tests -->
## Creating Tests

<!-- To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory: -->
새로운 테스트 케이스를 생성하려면 `make:test` 아티즌 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다.

```shell
php artisan make:test UserTest
```

<!-- If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command: -->
`tests/Unit` 디렉터리 내에 테스트를 만들고 싶다면, `make:test` 명령어 실행 시 `--unit` 옵션을 추가하면 됩니다.

```shell
php artisan make:test UserTest --unit
```

<!-- If you would like to create a [Pest PHP](https://pestphp.com) test, you may provide the `--pest` option to the `make:test` command: -->
[Pest PHP](https://pestphp.com) 방식의 테스트를 생성하려면, `make:test` 명령어에 `--pest` 옵션을 추가하면 됩니다.

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!NOTE]
> 테스트 스텁(stub)은 [stub publishing](/docs/10.x/artisan#stub-customization)를 통해 원하는 대로 커스터마이즈할 수 있습니다.

<!-- Once the test has been generated, you may define test methods as you normally would using [PHPUnit](https://phpunit.de). To run your tests, execute the `vendor/bin/phpunit` or `php artisan test` command from your terminal: -->
테스트가 생성된 후에는 [PHPUnit](https://phpunit.de) 방식에 따라 원하는 대로 테스트 메서드를 정의하면 됩니다. 테스트를 실행하려면 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 사용하세요.

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
> 테스트 클래스 내에 직접 `setUp` / `tearDown` 메서드를 정의하는 경우, 반드시 부모 클래스의 각각의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 일반적으로는 직접 작성한 `setUp` 메서드의 맨 앞에서 `parent::setUp()`을, `tearDown` 메서드의 마지막에서 `parent::tearDown()`을 호출해야 합니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- As mentioned previously, once you've written tests, you may run them using `phpunit`: -->
앞서 설명했듯, 테스트를 작성했으면 `phpunit` 명령어로 실행할 수 있습니다.

```shell
./vendor/bin/phpunit
```

<!-- In addition to the `phpunit` command, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging: -->
`phpunit` 명령어 외에도, 아티즌의 `test` 명령어를 이용해 테스트를 실행할 수도 있습니다. 아티즌 테스트 러너는 개발과 디버깅에 도움이 되도록 더 자세한 테스트 리포트를 제공합니다.

```shell
php artisan test
```

<!-- Any arguments that can be passed to the `phpunit` command may also be passed to the Artisan `test` command: -->
`phpunit` 명령어에 전달 가능한 모든 인자는 아티즌 `test` 명령어에도 동일하게 전달할 수 있습니다.

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
<!-- ### Running Tests in Parallel -->
### Running Tests in Parallel

<!-- By default, Laravel and PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, you should install the `brianium/paratest` Composer package as a "dev" dependency. Then, include the `--parallel` option when executing the `test` Artisan command: -->
기본적으로 Laravel과 PHPUnit은 테스트를 한 번에 한 프로세스에서 순차적으로 실행합니다. 하지만, 여러 프로세스에서 동시에 테스트를 실행하면 테스트 전체의 실행 시간을 크게 단축할 수 있습니다. 이를 위해서는 먼저 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그 후, 아티즌 `test` 명령어 실행 시 `--parallel` 옵션을 추가하면 됩니다.

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

<!-- By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option: -->
Laravel은 기본적으로 컴퓨터의 CPU 코어 수만큼 프로세스를 생성해 테스트를 분산 처리합니다. 필요한 경우 `--processes` 옵션으로 프로세스 수를 직접 지정할 수 있습니다.

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬 테스트 실행 시 일부 PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
<!-- #### Parallel Testing and Databases -->
#### Parallel Testing and Databases

<!-- As long as you have configured a primary database connection, Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases. -->
기본 데이터베이스 연결이 설정되어 있다면, Laravel이 각 병렬 테스트 프로세스마다 별도의 테스트용 데이터베이스를 생성하고 마이그레이션을 자동으로 처리합니다. 각 테스트 데이터베이스는 프로세스마다 고유한 토큰이 접미사로 붙습니다. 예를 들어, 병렬 테스트 프로세스가 2개라면 Laravel은 `your_db_test_1`과 `your_db_test_2`와 같은 테스트 데이터베이스를 생성하고 사용합니다.

<!-- By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option: -->
기본적으로 테스트 데이터베이스는 아티즌 `test` 명령어 실행 사이에 계속 유지되어, 이후 `test` 호출에도 재사용됩니다. 하지만, `--recreate-databases` 옵션을 사용하면 테스트 데이터베이스를 새로 만들 수 있습니다.

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
<!-- #### Parallel Testing Hooks -->
#### Parallel Testing Hooks

<!-- Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes. -->
간혹 애플리케이션의 테스트에서 여러 테스트 프로세스가 안전하게 사용할 수 있도록 리소스를 미리 준비해야 할 수도 있습니다.

<!-- Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively: -->
`ParallelTesting` 파사드를 이용하면 각 프로세스 및 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 여기서 전달되는 클로저에는 프로세스 토큰(`$token`)과 현재 테스트 케이스(`$testCase`) 정보가 제공됩니다.

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
애플리케이션의 테스트 코드 어느 곳에서든 현재 병렬 프로세스의 "토큰"에 접근하고 싶다면, `token` 메서드를 사용하면 됩니다. 이 토큰은 각 테스트 프로세스에 고유한 문자열 식별자로, 병렬 테스트 간 리소스를 구분하는 데 사용할 수 있습니다. 예를 들어, Laravel은 테스트 데이터베이스 이름의 끝에 이 토큰을 자동으로 추가합니다.

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
<!-- ### Reporting Test Coverage -->
### Reporting Test Coverage

> [!WARNING]
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

<!-- When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command: -->
애플리케이션 테스트를 실행할 때 실제로 테스트가 애플리케이션 코드를 얼마나 덮고(cover) 있는지, 즉 테스트가 실제 코드의 어느 부분까지 실행되는지 확인하고 싶을 수 있습니다. 이때 `test` 명령어 실행 시 `--coverage` 옵션을 추가하면 커버리지 리포트를 생성할 수 있습니다.

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
<!-- #### Enforcing a Minimum Coverage Threshold -->
#### Enforcing a Minimum Coverage Threshold

<!-- You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met: -->
`--min` 옵션을 사용해 애플리케이션의 최소 테스트 커버리지 기준을 지정할 수 있습니다. 지정한 기준에 미달하면 테스트가 실패합니다.

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
<!-- ### Profiling Tests -->
### Profiling Tests

<!-- The Artisan test runner also includes a convenient mechanism for listing your application's slowest tests. Invoke the `test` command with the `--profile` option to be presented with a list of your ten slowest tests, allowing you to easily investigate which tests can be improved to speed up your test suite: -->
아티즌 테스트 러너는 애플리케이션에서 가장 느린 테스트 목록을 손쉽게 확인할 수 있는 기능도 제공합니다. `test` 명령어에 `--profile` 옵션을 추가하면, 가장 실행 시간이 오래 걸리는 10개의 테스트 목록이 표시되어 어떤 테스트를 개선하면 전체 테스트 속도가 빨라질지 쉽게 파악할 수 있습니다.

```shell
php artisan test --profile
```
